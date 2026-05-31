#!/usr/bin/env python3
"""Extract figure and table references from a manuscript and verify numbering.

Usage:
    python extract_figures.py manuscript.md --check-numbering
    python extract_figures.py manuscript.md --output figures.md
"""

import argparse
import os
import re
import sys
from collections import defaultdict


def extract_references(text):
    """Extract all figure, table, equation, and section references."""
    refs = {
        "figures": [],
        "tables": [],
        "equations": [],
        "sections": [],
    }

    # Figure references: Fig. X, Figure X, Fig X, 图X
    for m in re.finditer(r'(?:Fig\.?|Figure|图)\s*(\d+)', text, re.IGNORECASE):
        refs["figures"].append({
            "number": int(m.group(1)),
            "context": _get_context(text, m.start()),
            "raw": m.group(0),
        })

    # Table references: Table X, Tab. X, 表X
    for m in re.finditer(r'(?:Table|Tab\.?|表)\s*(\d+)', text, re.IGNORECASE):
        refs["tables"].append({
            "number": int(m.group(1)),
            "context": _get_context(text, m.start()),
            "raw": m.group(0),
        })

    # Equation references: Eq. (X), Equation X, Eqn. X, 公式(X)
    for m in re.finditer(r'(?:Eq\.?|Equation|Eqn\.?|公式)\s*[\(\[]?\s*(\d+)\s*[\)\]]?', text, re.IGNORECASE):
        refs["equations"].append({
            "number": int(m.group(1)),
            "context": _get_context(text, m.start()),
            "raw": m.group(0),
        })

    # Section references: Section X, §X, § X, 第X节
    for m in re.finditer(r'(?:Section|§|第)\s*([IVX\d]+)', text, re.IGNORECASE):
        refs["sections"].append({
            "number": m.group(1),
            "context": _get_context(text, m.start()),
            "raw": m.group(0),
        })

    return refs


def _get_context(text, pos, window=80):
    """Get surrounding text for context."""
    start = max(0, pos - window)
    end = min(len(text), pos + window)
    context = text[start:end].replace("\n", " ").strip()
    return f"...{context}..."


def check_numbering(refs):
    """Check that references are sequential and complete."""
    issues = []

    for ref_type in ["figures", "tables", "equations"]:
        numbers = [r["number"] for r in refs[ref_type]]
        if not numbers:
            continue

        unique = sorted(set(numbers))
        expected = list(range(1, max(unique) + 1))

        # Check for gaps
        missing = set(expected) - set(unique)
        if missing:
            issues.append(
                f"{ref_type.capitalize()}: Missing reference(s) for {' ,'.join(str(m) for m in sorted(missing))}. "
                f"References found: {unique}"
            )

        # Check order of first occurrence
        first_occurrence = []
        seen = set()
        for r in refs[ref_type]:
            if r["number"] not in seen:
                first_occurrence.append(r["number"])
                seen.add(r["number"])

        if first_occurrence != sorted(first_occurrence):
            issues.append(
                f"{ref_type.capitalize()}: References not in sequential order. "
                f"First occurrence order: {first_occurrence}"
            )

    return issues


def find_unreferenced(text):
    """Find figure/table environments that may not be referenced."""
    issues = []

    # Find figure captions
    fig_captions = re.findall(
        r'(?:Fig\.?|Figure)\s*(\d+)[.:]\s*(.+?)$',
        text, re.MULTILINE | re.IGNORECASE
    )

    for num, caption in fig_captions:
        # Check if this figure number is referenced elsewhere
        referenced = bool(re.search(
            rf'(?:Fig\.?|Figure|图)\s*{num}\b',
            text.replace(caption, "", 1),  # Don't match the caption itself
            re.IGNORECASE
        ))
        if not referenced:
            issues.append(f"Figure {num} caption exists but figure {num} may not be referenced in text.")

    # Find table captions
    table_captions = re.findall(
        r'(?:Table|Tab\.?)\s*(\d+)[.:]\s*(.+?)$',
        text, re.MULTILINE | re.IGNORECASE
    )
    for num, caption in table_captions:
        referenced = bool(re.search(
            rf'(?:Table|Tab\.?|表)\s*{num}\b',
            text.replace(caption, "", 1),
            re.IGNORECASE
        ))
        if not referenced:
            issues.append(f"Table {num} caption exists but table {num} may not be referenced in text.")

    return issues


def format_report(refs, numbering_issues, unreferenced_issues):
    """Format a Markdown report."""
    lines = ["# Figure & Table Reference Report\n"]

    # Summary
    lines.append("## Summary\n")
    lines.append(f"- Figures referenced: {len(refs['figures'])}")
    lines.append(f"- Tables referenced: {len(refs['tables'])}")
    lines.append(f"- Equations referenced: {len(refs['equations'])}")
    lines.append(f"- Section references: {len(refs['sections'])}")

    # Numbering issues
    if numbering_issues:
        lines.append("\n## Numbering Issues\n")
        for issue in numbering_issues:
            lines.append(f"- ⚠️ {issue}")

    # Unreferenced
    if unreferenced_issues:
        lines.append("\n## Unreferenced Items\n")
        for issue in unreferenced_issues:
            lines.append(f"- ⚠️ {issue}")

    # Detailed listing
    for ref_type, label in [("figures", "Figures"), ("tables", "Tables"), ("equations", "Equations")]:
        if refs[ref_type]:
            lines.append(f"\n## {label} Referenced\n")
            lines.append("| # | Context |")
            lines.append("|---|---------|")
            for r in refs[ref_type]:
                context = r["context"][:120]
                lines.append(f"| {r['raw']} | {context} |")

    if not numbering_issues and not unreferenced_issues:
        lines.append("\n✅ All references appear sequential and complete.\n")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Extract and verify figure/table references from a manuscript"
    )
    parser.add_argument("manuscript", help="Path to the manuscript file")
    parser.add_argument("--check-numbering", action="store_true",
                        help="Check sequential numbering")
    parser.add_argument("--check-unreferenced", action="store_true",
                        help="Check for unreferenced figures/tables")
    parser.add_argument("--output", "-o", help="Output report path")
    args = parser.parse_args()

    with open(args.manuscript, "r", encoding="utf-8") as f:
        text = f.read()

    refs = extract_references(text)

    numbering_issues = []
    if args.check_numbering:
        numbering_issues = check_numbering(refs)

    unreferenced_issues = []
    if args.check_unreferenced:
        unreferenced_issues = find_unreferenced(text)

    report = format_report(refs, numbering_issues, unreferenced_issues)

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to {args.output}", file=sys.stderr)
    else:
        print(report)

    # Exit with error if issues found
    if numbering_issues or unreferenced_issues:
        sys.exit(1)


if __name__ == "__main__":
    main()
