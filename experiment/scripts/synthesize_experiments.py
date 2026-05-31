#!/usr/bin/env python3
"""Synthesize experiment analysis into narrative paragraphs.

Usage:
    python synthesize_experiments.py --improvements improvements.md \\
        --stats stats_report.md --project-brief brief.md --output exp_synthesis.md

    python synthesize_experiments.py --improvements improvements.md \\
        --ablations ablation.csv --project-brief brief.md --template --output outline.md

What this does:
    Like synthesize_literature.py but for experiments. Takes the outputs of
    compute_improvements.py, statistical_tests.py, and ablation data, then
    generates structured paragraph templates for:
    - Experimental Setup (datasets, baselines, metrics, implementation)
    - Main Results (comparison narrative, per-dataset highlights)
    - Ablation Study (component contribution narrative)
    - Efficiency Analysis (trade-off discussion)
    - Qualitative Analysis framework
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


# ── Input Parsing ──────────────────────────────────────────────────────────────────


def parse_improvements(text):
    """Parse the output of compute_improvements.py."""
    comparisons = []
    in_table = False
    headers = []

    for line in text.split("\n"):
        line = line.strip()
        if "| Group | Metric |" in line:
            in_table = True
            headers = [h.strip() for h in line.split("|")[1:-1]]
            continue
        if in_table and re.match(r'\|[\s\-:]+\|', line):
            continue
        if in_table and line.startswith("|") and not line.startswith("| #"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 5:
                entry = {}
                for i, h in enumerate(headers):
                    if i < len(cells):
                        entry[h.lower().replace(" ", "_")] = cells[i]
                comparisons.append(entry)
        if in_table and not line.startswith("|"):
            in_table = False

    return comparisons


def parse_ablation_csv(csv_path):
    """Parse ablation CSV. Expected format: Variant, Metric1, Metric2, ..."""
    import csv
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    return rows


def extract_numbers(text):
    """Extract all numbers from text, preserving context."""
    return [(m.group(0), m.start()) for m in re.finditer(r'\d+\.?\d*\s*(?:%|points?|ms)?', text)]


# ── Narrative Builder ──────────────────────────────────────────────────────────────


def build_setup_narrative(project_info, improvements):
    """Generate Experimental Setup paragraph templates."""
    datasets = set()
    baselines = set()
    metrics = set()

    for c in improvements:
        group = c.get("group", "")
        if group and group != "all":
            datasets.add(group.split("=")[-1] if "=" in group else group)
        baseline = c.get("strongest_baseline", "")
        if baseline:
            baselines.add(baseline)
        metric = c.get("metric", "")
        if metric:
            metrics.add(metric)

    return {
        "datasets": sorted(datasets),
        "baselines": sorted(baselines),
        "metrics": sorted(metrics),
        "template": _setup_paragraph_template(datasets, baselines, metrics),
    }


def _setup_paragraph_template(datasets, baselines, metrics):
    lines = [
        "**Datasets paragraph:**",
        f"We evaluate on {len(datasets)} datasets: {', '.join(datasets)}. ",
        "[Dataset 1]: [N] images, [description], [split].",
        "[Dataset 2]: [N] images, [description], [split].",
        "",
        "**Baselines paragraph:**",
    ]
    for b in sorted(baselines):
        lines.append(f"- {b}: [one-sentence description + citation].")
    lines.extend([
        "",
        "**Metrics paragraph:**",
        f"We report {', '.join(metrics)}. ",
        "[Metric 1] ([higher/lower] is better): [definition].",
        "All results are reported as mean ± std over [N] random seeds.",
        "",
        "**Implementation details paragraph:**",
        "We implement [Method] in [framework + version]. ",
        "Training uses [optimizer] with lr=[X], [scheduler], batch size [N], for [E] epochs. ",
        "All experiments run on [hardware]. Training takes approximately [X] GPU-hours.",
    ])
    return "\n".join(lines)


def build_main_results_narrative(improvements, stats_comparisons, project_info):
    """Generate Main Results narrative with structured paragraph templates."""
    method_name = project_info.get("method_name", "our method")

    # Group improvements by dataset
    by_dataset = defaultdict(list)
    for c in improvements:
        group = c.get("group", "all")
        by_dataset[group].append(c)

    paragraphs = []
    for dataset, entries in by_dataset.items():
        if dataset == "all" and len(by_dataset) > 1:
            continue  # Skip aggregate if we have per-dataset

        # Find the most notable results
        sorted_entries = sorted(entries, key=lambda e: _parse_num(e.get("δ_abs", e.get("abs_improvement", "0"))), reverse=True)
        if not sorted_entries:
            continue

        best = sorted_entries[0]
        worst = sorted_entries[-1]
        best_baseline = best.get("strongest_baseline", "the strongest baseline")
        best_value = best.get("target_value", best.get("target_mean", "N/A"))
        best_metric = best.get("metric", "metric")
        best_improvement = best.get("δ_abs", best.get("abs_improvement", "N/A"))
        best_rel = best.get("δ_rel", best.get("rel_improvement_pct", "N/A"))

        paragraph = {
            "dataset": dataset,
            "n_metrics": len(entries),
            "best_improvement": f"{best_metric}: +{best_improvement} ({best_rel}%) over {best_baseline}",
            "overall_statement": _result_statement(sorted_entries, method_name, dataset),
            "template": (
                f"On {dataset}, {method_name} achieves {best_value} {best_metric}, "
                f"outperforming {best_baseline} by {best_improvement} "
                f"({best_rel}% relative improvement). "
                f"[Additional metric highlights]. "
                f"These results demonstrate that [core capability], "
                f"as evidenced by [specific comparison]."
            ),
        }
        paragraphs.append(paragraph)

    return paragraphs


def _parse_num(s):
    try:
        return abs(float(str(s).replace("%", "").replace(",", "")))
    except (ValueError, TypeError):
        return 0.0


def _result_statement(entries, method_name, dataset):
    """Generate a one-sentence result statement."""
    if not entries:
        return "No data available."

    # Count how many metrics we win on
    wins = 0
    total = len(entries)
    for e in entries:
        imp = _parse_num(e.get("δ_abs", e.get("abs_improvement", "0")))
        if imp > 0:
            wins += 1

    if wins == total and total > 1:
        return f"{method_name} outperforms all baselines on all {total} metrics."
    elif wins > total / 2:
        return f"{method_name} outperforms baselines on {wins}/{total} metrics, with mixed results on the remainder."
    else:
        return f"{method_name} shows competitive performance across {total} metrics."


def build_ablation_narrative(ablation_rows, project_info):
    """Generate Ablation Study narrative."""
    if not ablation_rows:
        return {"template": "[No ablation data provided. Add CSV with --ablations.]",
                "variants": []}

    # Identify "full model" row and component-removal rows
    full_row = None
    ablations = []

    for row in ablation_rows:
        variant = row.get("Variant", row.get("Method", row.get("variant", "")))
        if not variant:
            continue
        if re.search(r'full|complete|ours?|proposed', variant, re.IGNORECASE) and not re.search(r'w/o|without', variant, re.IGNORECASE):
            full_row = row
        elif re.search(r'w/o|without|remove', variant, re.IGNORECASE):
            ablations.append({"variant": variant, "row": row})

    if not full_row:
        full_row = ablation_rows[0] if ablation_rows else {}

    # Calculate component contributions
    components = []
    for ab in ablations:
        # Find the first metric column
        metric_cols = [k for k in ab["row"].keys() if k.lower() not in ("variant", "method", "model")]
        if metric_cols:
            metric = metric_cols[0]
            try:
                full_val = float(str(full_row.get(metric, "0")).replace("%", ""))
                ab_val = float(str(ab["row"].get(metric, "0")).replace("%", ""))
                delta = full_val - ab_val
                components.append({
                    "name": ab["variant"].replace("w/o ", "").replace("without ", ""),
                    "full_value": full_val,
                    "ablated_value": ab_val,
                    "delta": delta,
                    "contribution": "major" if delta > abs(full_val) * 0.02 else "minor" if delta > 0 else "none",
                })
            except (ValueError, TypeError):
                pass

    # Build narrative
    template_lines = [
        "**Ablation narrative template:**",
        "",
        "We conduct ablation experiments on [primary dataset] to isolate the contribution of each component.",
    ]

    if components:
        template_lines.append(f"The full model achieves {_safe_get(full_row, metric_cols[0] if metric_cols else 'N/A')}.")
        for c in components:
            if c["contribution"] == "major":
                template_lines.append(
                    f"Removing {c['name']} causes a {c['delta']:.2f} point drop, "
                    f"confirming it is a critical component."
                )
            elif c["contribution"] == "minor":
                template_lines.append(
                    f"Removing {c['name']} results in a {c['delta']:.2f} point decrease, "
                    f"indicating a modest but consistent contribution."
                )

        # Check additivity
        if len(components) >= 2:
            total_delta = sum(c["delta"] for c in components)
            template_lines.append(
                f"The combined effect of all components ({total_delta:.2f} points) is approximately "
                f"{'additive' if abs(total_delta - components[0]['delta'] - components[1]['delta']) < 0.5 else 'synergistic'}, "
                f"suggesting that the components address {'complementary' if total_delta > max(c['delta'] for c in components) * 1.3 else 'overlapping'} aspects of the task."
            )

    template_lines.extend([
        "",
        "**Key ablation findings to highlight in prose:**",
    ])
    for c in components:
        template_lines.append(f"- [ ] {c['name']}: contributes {c['delta']:.2f} points ({c['contribution']} impact)")

    return {
        "template": "\n".join(template_lines),
        "components": components,
        "full_row": full_row,
    }


def _safe_get(row, key):
    if not row or not key:
        return "N/A"
    return row.get(key, "N/A")


def build_efficiency_narrative(improvements):
    """Generate Efficiency Analysis narrative template."""
    return {
        "template": (
            "**Efficiency narrative template:**\n\n"
            "We compare the computational cost of [Method] against key baselines.\n"
            "With [X]M parameters, [Method] is [more/less/comparably] parameterized "
            "relative to [baseline] ([Y]M).\n"
            "In terms of FLOPs, [Method] requires [X]G FLOPs vs. [baseline]'s [Y]G "
            "([Z]% [increase/decrease]).\n"
            "Inference latency is [X]ms per sample (batch size 1, [GPU]), "
            "which is [faster/slower/comparable] than [baseline] ([Y]ms).\n"
            "GPU memory consumption during training is [X]GB with batch size [B].\n\n"
            "**Efficiency trade-off statement:**\n"
            "[Method] achieves its performance gains at the cost of [X] [additional parameters / ms / GB]. "
            "Whether this trade-off is acceptable depends on [application context]. "
            "For [latency-sensitive / memory-constrained] deployments, [alternative / lighter variant] may be preferred."
        ),
    }


def build_discussion_narrative(project_info, all_results):
    """Generate Discussion section template connecting results to broader implications."""
    method_name = project_info.get("method_name", "our method")

    return {
        "template": (
            "**Discussion narrative template:**\n\n"
            "### Why the Method Works\n"
            f"Our experiments reveal that {method_name}'s strong performance stems from "
            f"[specific mechanism identified by ablation]. "
            f"The ablation confirms that [component A] is the primary driver, "
            f"contributing [X] points, while [component B] provides complementary gains. "
            f"This aligns with our design hypothesis that [original motivation].\n\n"
            "### Limitations\n"
            "Several limitations merit discussion:\n"
            "- [Dataset limitation]: tested on [N] datasets — generalization to [other domains] remains to be validated.\n"
            "- [Computational limitation]: [method] adds [X]% overhead compared to the simplest baseline.\n"
            "- [Failure mode]: the method struggles with [specific cases], as shown in Section IV-E.\n"
            "- [Domain limitation]: evaluation is limited to [language / resolution / domain].\n\n"
            "### Future Work\n"
            "Concrete directions for future work include:\n"
            "- Extending to [related task / domain] by [specific modification].\n"
            "- Reducing the computational cost through [specific technique, e.g., distillation, pruning].\n"
            "- Exploring [alternative design choice] that may address the identified failure modes.\n"
        ),
    }


# ── Output Builder ─────────────────────────────────────────────────────────────────


def build_synthesis_report(setup, main_results, ablation, efficiency, discussion, project_info):
    """Build the complete experiment synthesis report."""
    method_name = project_info.get("method_name", "[METHOD]")
    lines = [
        "# Experiment Section — Narrative Synthesis",
        "",
        f"**Method:** {method_name}",
        "",
        "> This report provides fill-in-the-blank paragraph templates for the Experiments section.",
        "> Numbers in [brackets] should be replaced with actual values from your experiment outputs.",
        "> Statistical notations: report p-values, confidence intervals, and effect sizes where available.",
        "",
        "---",
        "",
        "## IV-A. Experimental Setup",
        "",
        setup["template"],
        "",
        "---",
        "",
        "## IV-B. Main Results",
        "",
    ]

    for para in main_results:
        lines.append(f"### {para['dataset']}")
        lines.append(f"\n**Key result:** {para['best_improvement']}")
        lines.append(f"\n**Overall:** {para['overall_statement']}")
        lines.append(f"\n**Draft paragraph:**\n")
        lines.append(f"> {para['template']}")
        lines.append("")
        lines.append("[Add 2-3 more sentences comparing to other baselines and discussing metric-level details.]")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## IV-C. Ablation Study",
        "",
        ablation["template"],
        "",
    ])

    if ablation.get("components"):
        lines.append("### Ablation Summary Table")
        lines.append("")
        lines.append("| Component Removed | Metric Value | Δ from Full | Impact |")
        lines.append("|---|---:|---:|")
        for c in ablation["components"]:
            lines.append(f"| {c['name']} | {c['ablated_value']} | -{c['delta']:.2f} | {c['contribution']} |")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## IV-D. Efficiency Analysis",
        "",
        efficiency["template"],
        "",
        "---",
        "",
        "## IV-E. Qualitative Analysis (optional guide)",
        "",
        "**Success cases:** Show [N] examples where [Method] excels. For each:",
        "- Input + our output + strongest baseline output + ground truth",
        "- One-sentence explanation: why does our method succeed here? (e.g., 'The query-dependent re-weighting correctly emphasizes the car region.')",
        "",
        "**Failure cases:** Show [N] examples where [Method] struggles. For each:",
        "- Input + our output + strongest baseline output + ground truth",
        "- Analysis: what went wrong? Is it a systematic failure mode?",
        "- Hypothesis: what capability is missing? (This feeds into Discussion → Future Work.)",
        "",
        "---",
        "",
        "## Discussion & Conclusion Integration",
        "",
        discussion["template"],
        "",
        "---",
        "",
        "## Narrative Quality Checklist",
        "",
        "After drafting, verify:",
        "",
        "- [ ] Every number in prose matches a number in the corresponding table",
        "- [ ] Best results use **bold**, second-best use underline",
        "- [ ] Statistical significance is reported for key comparisons",
        "- [ ] Ablation results are interpreted (what do the deltas MEAN?), not just listed",
        "- [ ] Efficiency metrics (params, FLOPs, latency) are reported if 'efficient' is claimed",
        "- [ ] Qualitative examples include BOTH successes and failures",
        "- [ ] No result appears in prose that is not in a table",
        "- [ ] No table value is discussed in detail in more than one section",
        "- [ ] The Conclusion does not introduce new results not in Experiments",
        "- [ ] Effect sizes are reported alongside p-values for key claims",
        "",
    ])

    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Synthesize experiment analysis into narrative paragraphs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python synthesize_experiments.py --improvements improvements.md \\
      --stats stats_report.md --project-brief brief.md --output exp_synthesis.md

  python synthesize_experiments.py --improvements improvements.md \\
      --ablations ablation.csv --project-brief brief.md --output synthesis.md
        """,
    )
    parser.add_argument("--improvements", help="compute_improvements.py output (.md)")
    parser.add_argument("--stats", help="statistical_tests.py output (.md)")
    parser.add_argument("--ablations", help="Ablation CSV file")
    parser.add_argument("--project-brief", help="Stage 1 project brief (.md)")
    parser.add_argument("--output", "-o", default="experiment_synthesis.md")
    args = parser.parse_args()

    project_info = {"method_name": "[METHOD]", "task": ""}
    if args.project_brief and Path(args.project_brief).exists():
        text = Path(args.project_brief).read_text(encoding="utf-8", errors="replace")
        for pat in [r'(?:propose|method|we present)\s+["\']?(\w+(?:\s+\w+){0,4})["\']?',
                    r'## Research Task\s*\n(.*?)(?=\n##|\n\Z)']:
            m = re.search(pat, text, re.IGNORECASE | re.DOTALL)
            if m:
                val = m.group(1).strip()[:100]
                if "task" in pat.lower():
                    project_info["task"] = val
                else:
                    project_info["method_name"] = val
                    break

    improvements = []
    if args.improvements and Path(args.improvements).exists():
        imp_text = Path(args.improvements).read_text(encoding="utf-8", errors="replace")
        improvements = parse_improvements(imp_text)
    else:
        improvements = [{"group": "all", "metric": "Metric",
                          "strongest_baseline": "Baseline", "target_value": "N/A",
                          "abs_improvement": "N/A"}]

    stats_comps = []
    if args.stats and Path(args.stats).exists():
        stats_text = Path(args.stats).read_text(encoding="utf-8", errors="replace")
        stats_comps = parse_improvements(stats_text)

    ablation_rows = []
    if args.ablations and Path(args.ablations).exists():
        ablation_rows = parse_ablation_csv(args.ablations)

    print(f"Loaded {len(improvements)} improvement entries.", file=sys.stderr)
    print(f"Loaded {len(ablation_rows)} ablation rows.", file=sys.stderr)

    setup = build_setup_narrative(project_info, improvements)
    main_results = build_main_results_narrative(improvements, stats_comps, project_info)
    ablation = build_ablation_narrative(ablation_rows, project_info)
    efficiency = build_efficiency_narrative(improvements)
    discussion = build_discussion_narrative(project_info, {})

    report = build_synthesis_report(setup, main_results, ablation, efficiency, discussion, project_info)
    Path(args.output).write_text(report, encoding="utf-8")
    print(f"Saved to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
