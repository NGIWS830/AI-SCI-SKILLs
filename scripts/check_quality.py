#!/usr/bin/env python3
"""Automated quality checks on generated paper artifacts.

Usage:
    python check_quality.py <output_dir> --checks claims,citations,language
    python check_quality.py <output_dir> --all --output quality_report.md
"""

import argparse
import os
import re
import sys
from collections import Counter


# ── Check Functions ─────────────────────────────────────────────────────────────

def check_claims(text, state_text=""):
    """Check that claims are backed by evidence."""
    issues = []

    # Count claim-like statements
    claim_patterns = [
        (r'\b(significantly|substantially|dramatically)\s+improves?\b',
         "Strong claim word used: '{}'. Verify evidence strength supports this wording."),
        (r'\b(state-of-the-art|state of the art|SOTA)\b',
         "SOTA claim detected: '{}'. Must be supported by explicit SOTA comparison with statistical test."),
        (r'\bproves?\b',
         "'Prove' claim: '{}'. Use 'demonstrates', 'suggests', or 'provides evidence that' unless formal proof exists."),
        (r'\bfirst\b.*\b(propos|introduc|present)\b',
         "'First to propose' claim: '{}'. Nearly impossible to verify objectively."),
        (r'\bnovel\b',
         "'Novel': '{}'. Consider removing — let the contribution speak for itself."),
        (r'\buniversally\b',
         "'Universally': '{}'. Unless tested on a representative sample of all possible scenarios, avoid."),
        (r'\boptimal\b',
         "'Optimal': '{}'. Requires formal optimality proof or exhaustive search."),
        (r'\brobust across all\b',
         "'Robust across all': '{}'. Specify which conditions were tested."),
    ]

    found_claims = []
    for pattern, msg_template in claim_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            word = match.group(1) if match.lastindex else match.group(0)
            found_claims.append({
                "type": "overclaim_risk",
                "word": word,
                "message": msg_template.format(word),
            })

    # Check for evidence anchoring
    numbers_in_prose = re.findall(r'\b(\d+\.?\d*)\s*(%|percent|points|ms|seconds)\b', text)
    section_refs = re.findall(r'(Table|Figure|Fig\.?|Section)\s+[IVX\d]+', text)

    if numbers_in_prose and not section_refs:
        issues.append({
            "type": "weak_anchoring",
            "message": f"Found {len(numbers_in_prose)} numerical claims but no table/figure/section references.",
        })

    issues.extend(found_claims)
    return issues


def check_citations(text, state_text=""):
    """Check citation completeness and markers."""
    issues = []

    # Count [CITATION NEEDED] markers
    citation_needed = list(re.finditer(r'\[CITATION\s+NEEDED\]', text))
    if citation_needed:
        issues.append({
            "type": "citation_gap",
            "severity": "high",
            "message": f"Found {len(citation_needed)} [CITATION NEEDED] markers. Sections: " +
                       ", ".join(sorted(set(
                           _find_section(text, m.start()) for m in citation_needed
                       ))),
        })

    if len(citation_needed) > 3:
        issues.append({
            "type": "citation_gap",
            "severity": "critical",
            "message": f"Too many [CITATION NEEDED] markers ({len(citation_needed)}). Manuscript not ready.",
        })

    # Count AUTHOR_INPUT_NEEDED markers
    author_needed = list(re.finditer(r'AUTHOR_INPUT_NEEDED', text))
    if author_needed:
        issues.append({
            "type": "missing_input",
            "severity": "medium",
            "message": f"Found {len(author_needed)} AUTHOR_INPUT_NEEDED markers.",
        })

    # Check citation density per section
    sections = _split_sections(text)
    for section_name, section_text in sections.items():
        cites = len(re.findall(r'\[(\d+|[A-Z][a-z]+ et al\.)\]', section_text))
        if section_name in ["Introduction", "Related Work"] and cites < 3:
            issues.append({
                "type": "sparse_citations",
                "message": f"Section '{section_name}' has only {cites} citations. Consider adding more literature context.",
            })

    return issues


def check_reproducibility(text, state_text=""):
    """Check that experiments are reproducible."""
    issues = []

    # Implementation details checklist
    impl_checks = [
        (r'optimizer|Adam|SGD|AdamW', "Optimizer specified"),
        (r'learning rate|lr\s*=', "Learning rate specified"),
        (r'batch\s*size', "Batch size specified"),
        (r'epochs?', "Number of epochs specified"),
        (r'GPU|A100|V100|RTX|TPU', "Hardware specified"),
        (r'seed', "Random seed specified"),
    ]

    found = []
    missing = []
    for pattern, label in impl_checks:
        if re.search(pattern, text, re.IGNORECASE):
            found.append(label)
        else:
            missing.append(label)

    if missing:
        issues.append({
            "type": "reproducibility",
            "severity": "medium",
            "message": f"Missing implementation details: {', '.join(missing)}",
        })

    issues.append({
        "type": "reproducibility",
        "severity": "info",
        "message": f"Found details: {', '.join(found)}. Missing: {', '.join(missing) if missing else 'none'}",
    })

    # Check for standard deviations
    if not re.search(r'(\d+\.\d+\s*[±+-]\s*\d+\.\d+)', text):
        issues.append({
            "type": "reproducibility",
            "severity": "medium",
            "message": "No standard deviations detected in results. Consider reporting variance across runs.",
        })

    return issues


def check_language(text, state_text=""):
    """Check language quality heuristics."""
    issues = []

    # Sentence starter variety
    we_starts = re.findall(r'^(We\s)', text, re.MULTILINE)
    consecutive_we = 0
    max_consecutive = 0
    for line in text.split('\n'):
        if re.match(r'^\s*We\s', line):
            consecutive_we += 1
            max_consecutive = max(max_consecutive, consecutive_we)
        else:
            consecutive_we = 0

    if max_consecutive > 3:
        issues.append({
            "type": "style",
            "severity": "low",
            "message": f"Found {max_consecutive} consecutive sentences starting with 'We'. Vary sentence openers.",
        })

    # Check for informal words
    informal_checks = [
        (r'\ba lot of\b', "Replace with 'many', 'substantial', or a specific number"),
        (r'\bkind of\b', "Remove or replace with 'type of'"),
        (r'\b(a )?big\b', "Replace with 'large', 'substantial', or 'considerable'"),
        (r'\bget\b', "Consider 'obtain' or 'achieve'"),
        (r'\blook(ing|s|ed)? at\b', "Consider 'examine', 'investigate', or 'analyze'"),
    ]
    for pattern, suggestion in informal_checks:
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        if matches:
            issues.append({
                "type": "informal_language",
                "severity": "low",
                "message": f"'{matches[0].group(0)}' — {suggestion} (found {len(matches)} occurrences)",
            })

    return issues


def check_structure(text, state_text=""):
    """Check manuscript structure."""
    issues = []

    # Check required sections
    required_sections = ["Abstract", "Introduction", "Related Work", "Proposed Method", "Experiments", "Conclusion"]
    for section in required_sections:
        if not re.search(rf'#+\s+.*{section}', text, re.IGNORECASE):
            # Also check Chinese section names
            cn_map = {
                "Abstract": "摘要",
                "Introduction": "引言|绪论",
                "Related Work": "相关工作",
                "Proposed Method": ".*方法|本文方法",
                "Experiments": "实验",
                "Conclusion": "结论|总结",
            }
            cn_pattern = cn_map.get(section, "")
            if not cn_pattern or not re.search(cn_pattern, text):
                issues.append({
                    "type": "structure",
                    "severity": "high",
                    "message": f"Required section '{section}' not found.",
                })

    # Check figure/table references are sequential
    fig_refs = [int(m.group(1)) for m in re.finditer(r'Fig(?:ure)?\.?\s*(\d+)', text)]
    if fig_refs and fig_refs != sorted(set(fig_refs)):
        issues.append({
            "type": "structure",
            "severity": "low",
            "message": "Figure references may not be sequential or have gaps.",
        })

    return issues


def check_terminology(text, state_text=""):
    """Check terminology consistency."""
    issues = []

    # Common inconsistent pairs (Chinese)
    cn_pairs = [
        (r'注意力机制|Attention机制|attention机制', "注意力机制"),
        (r'骨干网络|主干网络|backbone网络', "骨干网络"),
        (r'特征提取器|特征提取网络', "特征提取器"),
        (r'消融实验|消融研究|ablation study', "消融实验"),
    ]
    for pattern, expected in cn_pairs:
        variants = set()
        for m in re.finditer(pattern, text, re.IGNORECASE):
            variants.add(m.group(0))
        if len(variants) > 1:
            issues.append({
                "type": "terminology",
                "severity": "medium",
                "message": f"Inconsistent terms: {variants}. Use '{expected}' consistently.",
            })

    return issues


# ── Helpers ─────────────────────────────────────────────────────────────────────

def _find_section(text, pos):
    """Find the section name containing position pos."""
    sections = list(re.finditer(r'^(#{1,4})\s+(.+)$', text[:pos], re.MULTILINE))
    if sections:
        return sections[-1].group(2).strip()[:40]
    return "(unknown)"


def _split_sections(text):
    """Split text into sections."""
    sections = {}
    current_section = "Preamble"
    current_text = []

    for line in text.split('\n'):
        if re.match(r'^#{1,4}\s+', line):
            if current_text:
                sections[current_section] = '\n'.join(current_text)
            current_section = re.sub(r'^#+\s+', '', line).strip()[:50]
            current_text = []
        else:
            current_text.append(line)

    if current_text:
        sections[current_section] = '\n'.join(current_text)

    return sections


def _read_artifacts(output_dir):
    """Read all generated manuscript files from output directory."""
    text = ""
    state_text = ""

    files_to_check = [
        "08_english_polished.md",
        "07_english_draft.md",
        "05_chinese_draft.md",
        "06_chinese_polished.md",
    ]

    for fname in files_to_check:
        fpath = os.path.join(output_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                text += f.read() + "\n"

    state_path = os.path.join(output_dir, "project-state.md")
    if os.path.exists(state_path):
        with open(state_path, "r", encoding="utf-8") as f:
            state_text = f.read()

    return text, state_text


# ── CLI ─────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Automated quality checks on paper artifacts")
    parser.add_argument("output_dir", help="Directory containing generated paper files")
    parser.add_argument("--checks", default="all",
                        help="Comma-separated checks: claims,citations,reproducibility,language,structure,terminology,all")
    parser.add_argument("--output", "-o", help="Output report path")
    args = parser.parse_args()

    # Read artifacts
    text, state_text = _read_artifacts(args.output_dir)

    if not text.strip():
        print(f"Warning: No manuscript files found in {args.output_dir}", file=sys.stderr)
        # Still run checks — they'll report missing sections

    # Determine which checks to run
    if args.checks == "all":
        checks_to_run = ["claims", "citations", "reproducibility", "language", "structure", "terminology"]
    else:
        checks_to_run = [c.strip() for c in args.checks.split(",")]

    CHECK_MAP = {
        "claims": ("Claims-Evidence Alignment", check_claims),
        "citations": ("Citation Completeness", check_citations),
        "reproducibility": ("Reproducibility", check_reproducibility),
        "language": ("Language Quality", check_language),
        "structure": ("Structure", check_structure),
        "terminology": ("Terminology Consistency", check_terminology),
    }

    all_issues = {}
    total_issues = 0
    critical_count = 0

    for check_name in checks_to_run:
        if check_name not in CHECK_MAP:
            continue
        label, fn = CHECK_MAP[check_name]
        issues = fn(text, state_text)
        all_issues[label] = issues
        total_issues += len(issues)
        for issue in issues:
            if issue.get("severity") == "critical":
                critical_count += 1

    # Build report
    report_lines = ["# Quality Check Report\n"]

    report_lines.append(f"**Artifacts directory:** `{args.output_dir}`\n")
    report_lines.append(f"**Checks run:** {', '.join(checks_to_run)}\n")
    report_lines.append(f"**Total issues found:** {total_issues}")
    if critical_count:
        report_lines.append(f"**Critical issues:** {critical_count} :warning:\n")
    else:
        report_lines.append("")

    for label, issues in all_issues.items():
        report_lines.append(f"\n## {label}\n")
        if not issues:
            report_lines.append("✅ No issues found.\n")
        else:
            for issue in issues:
                severity = issue.get("severity", "info")
                icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢", "info": "ℹ️"}.get(severity, "")
                report_lines.append(f"- {icon} [{severity}] {issue['message']}")

    # Summary
    report_lines.append(f"\n---\n")
    report_lines.append(f"### Summary\n")
    if critical_count > 0:
        report_lines.append(f"> :warning: **{critical_count} critical issue(s)** must be resolved before submission.\n")
    elif total_issues > 5:
        report_lines.append(f"> **{total_issues} issues** found. Review and address as appropriate.\n")
    else:
        report_lines.append(f"> Only {total_issues} minor issue(s) found. The manuscript is in good shape.\n")

    report = "\n".join(report_lines)

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
