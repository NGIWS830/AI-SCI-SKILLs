#!/usr/bin/env python3
"""Generate a structured experiment plan from project claims and context.

Usage:
    python design_experiments.py --project-brief brief.md --claims claims.md \\
        --output experiment_plan.md

    python design_experiments.py --project-brief brief.md --output plan.md \\
        --venue cvpr --datasets "Cityscapes,Mapillary" --method "SABR"

What this does:
    Given Stage 1 claims + method description + target venue, generates a
    complete experiment plan covering:
    1. Main comparison experiments (which baselines, which datasets, which metrics)
    2. Ablation study design (what to ablate, in what order)
    3. Efficiency / complexity analysis
    4. Robustness / generalization experiments
    5. Hyperparameter sensitivity
    6. Qualitative analysis plan
    7. Statistical reporting requirements
    8. Completeness checklist before writing the paper
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


# ── Experiment Type Definitions ────────────────────────────────────────────────────


EXPERIMENT_TYPES = {
    "main_comparison": {
        "name": "Main Comparison with State-of-the-Art",
        "priority": "critical",
        "description": "Compare the proposed method against all relevant baselines on all evaluation datasets using standard metrics.",
        "what_to_report": [
            "Per-dataset, per-metric results for ALL methods",
            "Bold = best, underline = second-best",
            "Mean ± std over N random seeds (N ≥ 3)",
            "Absolute improvement over strongest baseline",
            "Relative improvement (%)",
        ],
        "common_mistakes": [
            "Missing an important baseline (check literature matrix)",
            "Reporting only one metric when the community uses multiple",
            "Not reporting standard deviations",
            "Cherry-picking the best seed instead of reporting mean",
        ],
        "venue_notes": {
            "cvpr": "Typically 2-3 datasets. Efficiency metrics encouraged but not mandatory.",
            "neurips": "Statistical significance testing expected. At least 3 seeds.",
            "acl": "Include both automatic metrics and human evaluation if applicable.",
            "aaai": "Broader comparison encouraged — include methods from different families.",
            "journal": "Comprehensive comparison across 3+ datasets with full statistical reporting.",
        },
    },
    "ablation": {
        "name": "Ablation Study",
        "priority": "critical",
        "description": "Isolate the contribution of each proposed component by systematically removing or replacing them.",
        "what_to_report": [
            "Full model (all components)",
            "Full model − Component A (others kept)",
            "Full model − Component B (others kept)",
            "Full model − Component C (optional, if 3+ components)",
            "Full model − All novel components (= baseline)",
            "Delta (Δ) from full model for each variant",
        ],
        "ablated_questions": [
            "Does each component independently improve performance?",
            "Are the improvements additive or overlapping?",
            "Which component contributes the most?",
            "Is the combination necessary, or is one component sufficient?",
        ],
        "common_mistakes": [
            "Only reporting 'w/o X' but not 'X only' — can't tell if X works alone",
            "Ablating components in wrong order (should ablate most dependent first)",
            "Not ablating hyperparameters of the new components (λ, temperature, etc.)",
        ],
    },
    "efficiency": {
        "name": "Efficiency / Computational Complexity Analysis",
        "priority": "high",
        "description": "Compare computational cost against baselines: parameters, FLOPs, latency, memory.",
        "what_to_report": [
            "Number of trainable parameters (M)",
            "FLOPs or MACs (G) for a standard input size",
            "Inference latency (ms) per sample, batch size 1",
            "Training time (GPU-hours) and GPU memory (GB)",
            "Throughput (samples/second) if relevant",
        ],
        "common_mistakes": [
            "Claiming 'lightweight' or 'efficient' without ANY efficiency measurement",
            "Comparing FLOPs but not latency (they don't always correlate)",
            "Reporting only parameters (memory ≠ FLOPs ≠ speed)",
        ],
    },
    "robustness": {
        "name": "Robustness and Generalization",
        "priority": "medium",
        "description": "Test whether the method works under distribution shift, different conditions, or out-of-domain data.",
        "what_to_report": [
            "Cross-dataset generalization (train on A, test on B)",
            "Performance under perturbations (noise, blur, compression, etc.)",
            "Performance on different sub-populations or data slices",
            "Performance across different hyperparameter ranges",
        ],
        "common_mistakes": [
            "Claiming 'robust' or 'generalizes well' without any OOD evaluation",
            "Only testing on similar datasets (e.g., COCO → Flickr is still natural images)",
        ],
    },
    "hyperparameter": {
        "name": "Hyperparameter Sensitivity Analysis",
        "priority": "medium",
        "description": "Show that the method is not overly sensitive to key hyperparameters.",
        "what_to_report": [
            "Performance vs. hyperparameter value (line plot or table)",
            "Identify which parameters are most sensitive",
            "Show stable region where performance is within 1% of best",
            "Default values used for all other experiments",
        ],
        "key_hyperparameters": [
            "Loss weights (λ values)",
            "Temperature parameters (τ)",
            "Novel module-specific parameters (e.g., number of attention heads, hidden dim)",
            "Training hyperparameters (learning rate, batch size) — less critical if standard",
        ],
    },
    "qualitative": {
        "name": "Qualitative Analysis",
        "priority": "medium",
        "description": "Show visual examples or case studies that illustrate the method's behavior.",
        "what_to_report": [
            "Success cases: where the method excels",
            "Failure cases: where the method struggles + analysis of WHY",
            "Comparison against the strongest baseline on the same examples",
            "Attention/feature visualizations if the method is interpretable",
        ],
        "common_mistakes": [
            "Showing only cherry-picked success cases",
            "Failure cases without analysis (just showing bad examples is not useful)",
            "Not comparing against baselines on the same examples",
        ],
    },
    "statistical": {
        "name": "Statistical Significance Testing",
        "priority": "high",
        "description": "Validate that improvements are statistically significant, not due to random chance.",
        "what_to_report": [
            "Paired statistical test (bootstrap, t-test, Wilcoxon) comparing our method vs. each baseline",
            "p-values with appropriate multiple comparison correction",
            "Confidence intervals (95% CI) for key metrics",
            "Effect size (Cohen's d or Hedges' g)",
            "Number of random seeds and justification",
        ],
        "tools": ["statistical_tests.py (bootstrap CI, effect sizes, paired tests)"],
    },
}


# ── Baseline Coverage ──────────────────────────────────────────────────────────────


EXPECTED_BASELINE_CATEGORIES = [
    ("classical", "Classical / non-deep-learning methods (if applicable)"),
    ("standard_backbone", "Standard backbone without modifications (e.g., ResNet-50, ViT-B, BERT-base)"),
    ("method_family_a", "Methods from the same technical family (e.g., other attention-based methods)"),
    ("method_family_b", "Methods from alternative technical families (e.g., CNN-based if you propose ViT-based)"),
    ("recent_sota", "Most recent published SOTA (last 2 years)"),
    ("simple_baseline", "Simple / intuitive baseline that validates the problem is non-trivial"),
]


# ── Claim Parser ───────────────────────────────────────────────────────────────────


def parse_claims(text):
    """Extract claims from project brief or claims document."""
    claims = []
    # Numbered claims
    for m in re.finditer(r'(?:claim|candidate|contribution)\s*\d*\s*[：:]\s*(.+?)(?=\n\n|\n(?:claim|candidate|contribution)|\Z)',
                         text, re.IGNORECASE | re.DOTALL):
        claims.append({"text": m.group(1).strip()[:200], "source": "explicit"})

    # Bullet-point contributions
    bullet_section = re.search(r'(?:contributions?|贡献)[\s\S]*?((?:\n[-*\d.]+\s+.+)+)', text, re.IGNORECASE)
    if bullet_section:
        for m in re.finditer(r'[-*\d.]+\s+(.+?)(?=\n[-*\d.]|\n\n|\Z)', bullet_section.group(1)):
            claim_text = m.group(1).strip()[:200]
            if claim_text not in [c["text"] for c in claims]:
                claims.append({"text": claim_text, "source": "contribution_bullet"})

    return claims


def classify_claim(claim_text):
    """Classify a claim to determine what experiments are needed."""
    text = claim_text.lower()
    categories = []

    if any(kw in text for kw in ["outperform", "improve", "achieve", "better", "boost", "surpass",
                                   "优于", "提升", "超越"]):
        categories.append("performance")
    if any(kw in text for kw in ["efficient", "lightweight", "faster", "fewer param", "less memory",
                                   "轻量", "高效", "快速"]):
        categories.append("efficiency")
    if any(kw in text for kw in ["robust", "generaliz", "transfer", "domain", "cross-dataset",
                                   "鲁棒", "泛化"]):
        categories.append("robustness")
    if any(kw in text for kw in ["module", "component", "mechanism", "design", "architecture",
                                   "模块", "组件", "架构"]):
        categories.append("architecture")
    if any(kw in text for kw in ["loss", "training", "objective", "optimization",
                                   "损失", "训练"]):
        categories.append("training")
    if any(kw in text for kw in ["novel", "new", "first", "propose", "introduce",
                                   "提出", "首次"]):
        categories.append("novelty")

    return categories if categories else ["general"]


# ── Plan Generation ─────────────────────────────────────────────────────────────────


def generate_experiment_plan(claims, project_info, datasets, baselines, venue):
    """Generate a complete experiment plan."""

    experiment_needed = set()
    for claim in claims:
        cats = classify_claim(claim["text"])
        if "performance" in cats:
            experiment_needed.update(["main_comparison", "ablation", "statistical"])
        if "efficiency" in cats:
            experiment_needed.add("efficiency")
        if "robustness" in cats:
            experiment_needed.add("robustness")
        if "architecture" in cats:
            experiment_needed.update(["ablation", "main_comparison"])
        if "training" in cats:
            experiment_needed.add("ablation")

    # Always include critical ones
    experiment_needed.update(["main_comparison", "ablation", "statistical", "qualitative"])

    plan = {
        "experiments": [],
        "checklist": [],
    }

    for exp_key in sorted(experiment_needed, key=lambda k: EXPERIMENT_TYPES[k]["priority"]):
        exp_info = EXPERIMENT_TYPES[exp_key]
        plan["experiments"].append({
            "key": exp_key,
            "name": exp_info["name"],
            "priority": exp_info["priority"],
            "description": exp_info["description"],
            "items": exp_info["what_to_report"],
            "common_mistakes": exp_info.get("common_mistakes", []),
            "venue_specific": exp_info.get("venue_notes", {}).get(venue, ""),
        })

    # Baseline coverage check
    plan["baseline_coverage"] = _check_baseline_coverage(baselines, project_info)

    # Ablation design
    plan["ablation_design"] = _design_ablation_variants(project_info)

    plan["datasets"] = [d.strip() for d in datasets.split(",") if d.strip()]
    plan["checklist"] = _build_checklist(plan, venue)

    return plan


def _check_baseline_coverage(baselines, project_info):
    """Check if the baseline list covers expected categories."""
    baselines_lower = [b.lower() for b in baselines]
    coverage = []

    for cat_key, cat_desc in EXPECTED_BASELINE_CATEGORIES:
        # Heuristic detection
        likely_covered = False
        notes = ""

        if cat_key == "classical":
            likely_covered = any(
                kw in b.lower() for b in baselines
                for kw in ["svm", "random forest", "knn", "traditional", "hand-crafted", "non-deep",
                           "bm3d", "nlm", "tv-", "bilateral"]
            )
            if not likely_covered:
                notes = "Consider adding a classical/non-DL baseline for context (if applicable to your task)."

        elif cat_key == "standard_backbone":
            likely_covered = any("resnet" in b or "vit" in b or "bert" in b or "efficient" in b
                                 for b in baselines_lower)
            notes = "Include the backbone model without your modifications as a minimal baseline."

        elif cat_key == "method_family_a":
            notes = "Ensure at least 2 methods from your primary method family are included."

        elif cat_key == "method_family_b":
            notes = "Include at least 1 method from an alternative technical paradigm."

        elif cat_key == "recent_sota":
            notes = "Check literature matrix for the most recent SOTA method (last 2 years)."

        elif cat_key == "simple_baseline":
            notes = "A simple baseline (e.g., nearest neighbor, majority class) validates the task is non-trivial."

        coverage.append({"category": cat_desc, "covered": likely_covered if likely_covered else "unknown",
                         "notes": notes})

    return coverage


def _design_ablation_variants(project_info):
    """Design ablation variants based on method description."""
    # Try to identify components from the project brief
    method_text = project_info.get("method_summary", "") + " " + project_info.get("task", "")
    components = []

    # Look for component descriptions
    component_patterns = [
        (r'(?:module|component|block|layer|network|mechanism)\s*(?:called|named|:)?\s*["\']?(\w+(?:\s+\w+){0,3})["\']?',
         "named_component"),
        (r'(?:introduce|propose|design|develop)\s+(?:a|the|our)\s+["\']?(\w+(?:\s+\w+){0,4})["\']?(?:\s*(?:module|component|block|loss|mechanism|strategy))',
         "introduced_component"),
    ]

    for pattern, ctype in component_patterns:
        for m in re.finditer(pattern, method_text, re.IGNORECASE):
            name = m.group(1).strip()
            if len(name) > 3 and name.lower() not in ("the", "our", "new", "novel", "based", "using"):
                if name not in [c["name"] for c in components]:
                    components.append({"name": name, "type": ctype})

    if not components:
        return {"variants": ["Full Model", "w/o Component A", "w/o Component B",
                             "w/o Both = Baseline"],
                "note": "Auto-generated template. Replace with actual component names from your method."}

    variants = ["Full Model (= all components active)"]
    for c in components:
        variants.append(f"w/o {c['name']} (other components kept)")
    variants.append("w/o All Novel Components (= baseline backbone only)")

    # Suggest additional ablations
    extra = []
    if len(components) >= 2:
        extra.append(f"{components[0]['name']} only (w/o {', '.join(c['name'] for c in components[1:])}) — tests if first component works alone")
    extra.append(f"Replace {components[0]['name']} with [simpler alternative] — tests if complexity is justified")
    extra.append(f"Vary key hyperparameters of {components[0]['name']} — tests sensitivity")

    return {"variants": variants, "additional_ablations": extra,
            "components_found": [c["name"] for c in components]}


def _build_checklist(plan, venue):
    """Build a completeness checklist."""
    venue_reqs = {
        "cvpr": ["Statistical significance recommended", "Efficiency analysis encouraged"],
        "neurips": ["Statistical significance expected (p-values + effect sizes)",
                     "Broader impact of computational cost"],
        "acl": ["Human evaluation for generation tasks",
                 "Statistical significance with appropriate tests"],
        "aaai": ["Reproducibility checklist may be required"],
        "journal": ["Comprehensive statistical reporting", "Full implementation details",
                     "Parameter sensitivity analysis"],
    }

    checklist = [
        {"category": "Main Results", "items": [
            "All baselines from literature matrix are included",
            "All evaluation datasets are included",
            "All standard metrics for the task are reported",
            "Results reported as mean ± std over ≥3 random seeds",
            "Best result in bold, second-best underlined",
            "Absolute and relative improvement over strongest baseline",
        ]},
        {"category": "Ablation", "items": [
            "Every claimed component is ablated",
            "Ablation order is logically justified (not arbitrary)",
            "Delta (Δ) from full model reported for each variant",
            "Combined ablation (all components removed) = baseline",
        ]},
        {"category": "Statistical Reporting", "items": [
            "Statistical test specified (bootstrap / t-test / Wilcoxon)",
            "p-values or confidence intervals reported",
            "Multiple comparison correction applied (if comparing >2 methods)",
            "Effect size reported for key claims",
        ]},
        {"category": "Efficiency", "items": [
            "Parameter count reported",
            "FLOPs or MACs reported",
            "Inference latency reported (ms per sample)",
            "Training time and hardware specified",
        ]},
        {"category": "Reproducibility", "items": [
            "All hyperparameters documented",
            "Random seeds specified",
            "Hardware and software versions specified",
            "Data preprocessing pipeline documented",
            "Code will be released (with URL placeholder)",
        ]},
        {"category": "Qualitative", "items": [
            "At least 3 success cases shown",
            "At least 3 failure cases shown with analysis",
            "Comparison against strongest baseline on same examples",
        ]},
    ]

    # Add venue-specific items
    for req in venue_reqs.get(venue, []):
        checklist.append({"category": f"{venue.upper()} Requirements", "items": [req]})

    return checklist


# ── Report Formatting ──────────────────────────────────────────────────────────────


def format_plan_report(plan, project_info, venue):
    """Format experiment plan as markdown report."""
    lines = [
        "# Experiment Design Plan",
        "",
        f"**Method:** {project_info.get('method_name', '[METHOD NAME]')}",
        f"**Target Venue:** {venue.upper()}",
        f"**Datasets:** {', '.join(plan['datasets']) if plan['datasets'] else '[DATASETS]'}",
        "",
        "> This plan is generated from your project claims and method description.",
        "> Review and adjust before running experiments.",
        "",
        "---",
        "",
    ]

    # Required experiments
    lines.append("## Required Experiments")
    lines.append("")
    for exp in plan["experiments"]:
        badge = {"critical": "[!! REQUIRED]", "high": "[! IMPORTANT]", "medium": "[-] RECOMMENDED"}.get(exp["priority"], "")
        lines.append(f"### {exp['name']} {badge}")
        lines.append(f"\n{exp['description']}\n")
        lines.append("**What to report:**")
        for item in exp["items"]:
            lines.append(f"- [ ] {item}")
        if exp.get("venue_specific"):
            lines.append(f"\n**{venue.upper()} note:** {exp['venue_specific']}")
        if exp.get("common_mistakes"):
            lines.append("\n**Common mistakes to avoid:**")
            for mistake in exp["common_mistakes"]:
                lines.append(f"- ⚠ {mistake}")
        lines.append("")

    # Ablation design
    lines.append("## Ablation Variant Design")
    lines.append("")
    abl = plan["ablation_design"]
    if abl.get("components_found"):
        lines.append(f"**Detected components:** {', '.join(abl['components_found'])}")
        lines.append("")
    lines.append("### Core Variants")
    for i, v in enumerate(abl["variants"], 1):
        lines.append(f"{i}. {v}")
    if abl.get("additional_ablations"):
        lines.append("\n### Additional Analyses")
        for a in abl["additional_ablations"]:
            lines.append(f"- [ ] {a}")
    if abl.get("note"):
        lines.append(f"\n> {abl['note']}")
    lines.append("")

    # Baseline coverage
    lines.append("## Baseline Coverage Check")
    lines.append("")
    for bc in plan["baseline_coverage"]:
        icon = {"True": "✓", "unknown": "?"}.get(str(bc["covered"]), "?")
        lines.append(f"- {icon} **{bc['category']}**: {bc['notes']}")
    lines.append("")

    # Experiment roadmap
    lines.append("## Recommended Experiment Roadmap")
    lines.append("")
    lines.append("### Phase 1: Core Validation (run first)")
    lines.append("1. Train baseline (backbone only) on all datasets")
    lines.append("2. Train full proposed method on all datasets")
    lines.append("3. Verify that full method > baseline — if not, debug before proceeding")
    lines.append("")
    lines.append("### Phase 2: Ablation (confirm contributions)")
    lines.append("4. Run all ablation variants on the primary dataset")
    lines.append("5. If any component shows <0.5% improvement, consider removing or strengthening it")
    lines.append("6. Run hyperparameter sensitivity on the key parameters")
    lines.append("")
    lines.append("### Phase 3: Full Evaluation (build the paper's tables)")
    lines.append("7. Run all baselines on all datasets")
    lines.append("8. Run efficiency measurements (params, FLOPs, latency)")
    lines.append("9. Run statistical significance tests")
    lines.append("10. Run robustness/generalization experiments if claimed")
    lines.append("")
    lines.append("### Phase 4: Qualitative & Polish")
    lines.append("11. Generate qualitative examples (success + failure)")
    lines.append("12. Run additional seeds if std is too large (>1% of metric value)")
    lines.append("13. Finalize all tables and figures")
    lines.append("")

    # Completeness checklist
    lines.append("## Pre-Writing Completeness Checklist")
    lines.append("")
    for section in plan["checklist"]:
        lines.append(f"### {section['category']}")
        for item in section["items"]:
            lines.append(f"- [ ] {item}")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Next Steps",
        "",
        "1. Review this plan and adjust experiments to match your specific method and resources.",
        "2. After running experiments, use `compute_improvements.py` to calculate pairwise improvements.",
        "3. Use `statistical_tests.py` for bootstrap CI, effect sizes, and significance testing.",
        "4. Use `synthesize_experiments.py` to generate the Experiments section prose.",
        "",
    ])

    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Generate a structured experiment plan from project claims",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python design_experiments.py --project-brief brief.md --output plan.md
  python design_experiments.py --project-brief brief.md --venue neurips \\
      --datasets "Cityscapes,Mapillary,ADE20K" --method "SABR" --output plan.md
        """,
    )
    parser.add_argument("--project-brief", help="Stage 1 project brief (.md)")
    parser.add_argument("--claims", help="Claims document (optional, extracted from brief if omitted)")
    parser.add_argument("--output", "-o", default="experiment_plan.md")
    parser.add_argument("--venue", default="journal", choices=["cvpr", "iccv", "neurips", "icml", "acl", "aaai", "journal"])
    parser.add_argument("--datasets", default="", help="Comma-separated dataset names")
    parser.add_argument("--baselines", default="", help="Comma-separated baseline method names")
    parser.add_argument("--method", default="", help="Proposed method name")
    args = parser.parse_args()

    project_info = {"method_name": args.method, "method_summary": "", "task": ""}
    claims = []

    if args.project_brief and Path(args.project_brief).exists():
        text = Path(args.project_brief).read_text(encoding="utf-8", errors="replace")
        claims = parse_claims(text)

        # Extract method info
        for pat in [r'## Research Task\s*\n(.*?)(?=\n##|\n\Z)',
                    r'task[：:]\s*(.*?)(?=\n)']:
            m = re.search(pat, text, re.IGNORECASE | re.DOTALL)
            if m:
                project_info["task"] = m.group(1).strip()[:200]
                break
        for pat in [r'## Method Overview\s*\n(.*?)(?=\n##|\n\Z)',
                    r'method[：:]\s*(.*?)(?=\n##|\n\n)']:
            m = re.search(pat, text, re.IGNORECASE | re.DOTALL)
            if m:
                project_info["method_summary"] = m.group(1).strip()[:500]
                break
        if not project_info["method_name"]:
            m = re.search(r'(?:propose|proposed|method|we present)\s+["\']?(\w+(?:\s+\w+){0,4})["\']?',
                          text, re.IGNORECASE)
            if m:
                project_info["method_name"] = m.group(1).strip()

    if args.claims and Path(args.claims).exists():
        claims_text = Path(args.claims).read_text(encoding="utf-8", errors="replace")
        claims.extend(parse_claims(claims_text))

    baselines = [b.strip() for b in args.baselines.split(",") if b.strip()]

    if not claims:
        claims = [{"text": "[No claims extracted — manually add your paper's claims]", "source": "manual"}]

    print(f"Found {len(claims)} claims.", file=sys.stderr)
    for c in claims:
        cats = classify_claim(c["text"])
        print(f"  [{', '.join(cats)}] {c['text'][:80]}...", file=sys.stderr)

    plan = generate_experiment_plan(claims, project_info, args.datasets, baselines, args.venue)
    report = format_plan_report(plan, project_info, args.venue)

    Path(args.output).write_text(report, encoding="utf-8")
    print(f"Saved to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
