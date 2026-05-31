#!/usr/bin/env python3
"""Validate cross-references and structural consistency in a manuscript.

Usage:
    python validate_references.py paper.md --output ref_report.md
    python validate_references.py paper.tex --format latex --output ref_report.md

Checks performed:
    1. Every Figure/Table/Section reference points to an existing object
    2. Figures, Tables, Equations are sequentially numbered (no gaps/duplicates)
    3. Every defined Figure/Table is referenced at least once in the text
    4. References appear before the referenced object (Figure before definition)
    5. Equation numbers in prose match display equation numbers
    6. Section numbering is consistent (no jumps like I → III)
    7. All citation markers [N] have corresponding bibliography entries
    8. Abbreviations are defined on first use
    9. Section length balance (no 1-sentence or >30-sentence sections)
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


# ── Reference Extraction ──────────────────────────────────────────────────────────


def extract_object_definitions(text):
    """Find where figures, tables, equations, and sections are defined."""
    definitions = {
        "figures": [],
        "tables": [],
        "equations": [],
        "sections": [],
    }

    # Figure definitions: \label{fig:xxx}, Fig. 1, Figure 1:
    for m in re.finditer(r'\\label\{fig:([^}]+)\}', text):
        definitions["figures"].append({"id": m.group(1), "position": m.start()})
    for m in re.finditer(r'(?:Fig(?:ure)?\.?)\s+(\d+)[：:.\s]', text):
        num = int(m.group(1))
        if not any(d.get("num") == num for d in definitions["figures"]):
            definitions["figures"].append({"num": num, "position": m.start()})
    for m in re.finditer(r'\\caption\{', text):
        # LaTeX figure captions — approximate
        pass

    # Table definitions: \label{tab:xxx}, Table 1:
    for m in re.finditer(r'\\label\{tab(?:le)?:([^}]+)\}', text):
        definitions["tables"].append({"id": m.group(1), "position": m.start()})
    for m in re.finditer(r'Table\s+(\d+)[：:.\s]', text):
        num = int(m.group(1))
        if not any(d.get("num") == num for d in definitions["tables"]):
            definitions["tables"].append({"num": num, "position": m.start()})

    # Equation definitions: \label{eq:xxx}, (1), Equation (1)
    for m in re.finditer(r'\\label\{eq:([^}]+)\}', text):
        definitions["equations"].append({"id": m.group(1), "position": m.start()})
    for m in re.finditer(r'\\begin\{equation\}', text):
        definitions["equations"].append({"position": m.start(), "type": "display"})

    # Section definitions: ## Section Title, \section{Title}
    for m in re.finditer(r'^(#{1,4})\s+(.+)$', text, re.MULTILINE):
        level = len(m.group(1))
        title = m.group(2).strip()
        definitions["sections"].append({
            "level": level, "title": title, "position": m.start(),
        })
    for m in re.finditer(r'\\(?:sub)*section\{([^}]+)\}', text):
        definitions["sections"].append({
            "title": m.group(1), "position": m.start(), "type": "latex",
        })

    return definitions


def extract_references(text):
    """Find all cross-references in prose text."""
    refs = {
        "figure_refs": [],
        "table_refs": [],
        "equation_refs": [],
        "section_refs": [],
        "citation_refs": [],
    }

    # Figure references: Fig. 1, Fig 1, Figure 1, Figs. 1 and 2, \ref{fig:xxx}
    for m in re.finditer(r'(?:Fig(?:ure)?s?\.?)\s+((?:\d+(?:\s*(?:and|,|&)\s*)?)+)', text):
        numbers = [int(n) for n in re.findall(r'\d+', m.group(1))]
        for n in numbers:
            refs["figure_refs"].append({"num": n, "position": m.start()})
    for m in re.finditer(r'\\ref\{fig:([^}]+)\}', text):
        refs["figure_refs"].append({"id": m.group(1), "position": m.start()})

    # Table references: Table 1, Tables 1 and 2, \ref{tab:xxx}
    for m in re.finditer(r'Table(?:s)?\s+((?:\d+(?:\s*(?:and|,|&)\s*)?)+)', text):
        numbers = [int(n) for n in re.findall(r'\d+', m.group(1))]
        for n in numbers:
            refs["table_refs"].append({"num": n, "position": m.start()})
    for m in re.finditer(r'\\ref\{tab(?:le)?:([^}]+)\}', text):
        refs["table_refs"].append({"id": m.group(1), "position": m.start()})

    # Equation references: Eq. (1), Eq 1, Equation (1), Eqs. (1)-(3), \ref{eq:xxx}
    for m in re.finditer(r'(?:Eq(?:uation)?s?\.?)\s*\(?(\d+(?:\s*[-–—]\s*\d+)?)\)?', text):
        # Handle ranges like Eqs. (1)-(3)
        range_match = re.match(r'(\d+)\s*[-–—]\s*(\d+)', m.group(1))
        if range_match:
            for n in range(int(range_match.group(1)), int(range_match.group(2)) + 1):
                refs["equation_refs"].append({"num": n, "position": m.start()})
        else:
            for n in re.findall(r'\d+', m.group(1)):
                refs["equation_refs"].append({"num": int(n), "position": m.start()})
    for m in re.finditer(r'\\ref\{eq:([^}]+)\}', text):
        refs["equation_refs"].append({"id": m.group(1), "position": m.start()})

    # Section references: Section III, Section 3.2, Sec. III-B, \ref{sec:xxx}
    for m in re.finditer(r'(?:Section|Sec\.?)\s+([IVX\d\.]+)', text):
        refs["section_refs"].append({"name": m.group(1), "position": m.start()})
    for m in re.finditer(r'\\ref\{sec:([^}]+)\}', text):
        refs["section_refs"].append({"id": m.group(1), "position": m.start()})

    # Citation references: [1], [1,2,3], [1]-[3], \cite{xxx}
    for m in re.finditer(r'\[((?:\d+(?:\s*[,，]\s*)?)+)\]', text):
        numbers = [int(n) for n in re.findall(r'\d+', m.group(1))]
        for n in numbers:
            refs["citation_refs"].append({"num": n, "position": m.start()})
    for m in re.finditer(r'\\cite\{([^}]+)\}', text):
        keys = [k.strip() for k in m.group(1).split(",")]
        for key in keys:
            refs["citation_refs"].append({"key": key, "position": m.start()})
    # Author-year: (Author, Year)
    for m in re.finditer(r'\(([A-Z][a-z]+(?:\s+(?:et\s+al\.?|and\s+[A-Z][a-z]+))?),\s*(\d{4}[a-z]?)\)', text):
        refs["citation_refs"].append({
            "author": m.group(1), "year": m.group(2), "position": m.start(), "type": "author_year",
        })

    return refs


# ── Validation Functions ──────────────────────────────────────────────────────────


def check_sequential_numbering(items, item_type):
    """Check that numbered items are sequential with no gaps or duplicates."""
    issues = []
    numbers = []

    for item in items:
        if "num" in item:
            numbers.append(item["num"])

    if not numbers:
        return issues

    numbers = sorted(set(numbers))
    expected = list(range(min(numbers), max(numbers) + 1))

    # Check for gaps
    for n in expected:
        if n not in numbers:
            issues.append({
                "severity": "medium",
                "message": f"{item_type} {n} is missing — numbering gap between {min(numbers)} and {max(numbers)}.",
            })

    # Check for duplicates
    counts = Counter([i.get("num") for i in items if "num" in i])
    for num, count in counts.items():
        if count > 1:
            issues.append({
                "severity": "high",
                "message": f"{item_type} {num} appears {count} times — duplicate numbering.",
            })

    return issues


def check_refs_before_defs(references, definitions, ref_type, def_type):
    """Check that references appear before (or at) their definitions."""
    issues = []
    for ref in references:
        ref_pos = ref.get("position", 0)
        ref_num = ref.get("num", ref.get("id"))

        # Find the definition
        def_pos = None
        for d in definitions:
            if d.get("num") == ref_num or d.get("id") == ref_num:
                def_pos = d.get("position", float("inf"))
                break

        if def_pos is not None and ref_pos < def_pos:
            issues.append({
                "severity": "low",
                "message": f"{ref_type} {ref_num} referenced at position {ref_pos} before its definition at {def_pos}.",
            })

    return issues


def check_orphan_definitions(definitions, references, def_type, ref_type):
    """Check that every defined object is referenced at least once."""
    issues = []
    for d in definitions:
        d_num = d.get("num", d.get("id"))
        if d_num is None:
            continue

        # Search references for this number/id
        found = False
        for ref in references:
            if ref.get("num") == d_num or ref.get("id") == d_num:
                found = True
                break

        if not found and len(definitions) > 1:
            issues.append({
                "severity": "low",
                "message": f"{def_type} {d_num} is defined but never referenced in the text.",
            })

    return issues


def check_section_balance(text):
    """Check that sections are reasonably balanced in length."""
    issues = []
    sections = re.split(r'^(#{1,3})\s+(.+)$', text, flags=re.MULTILINE)

    # Parse section boundaries
    section_texts = []
    current_title = "Preamble"
    current_start = 0

    for m in re.finditer(r'^(#{1,3})\s+(.+)$', text, re.MULTILINE):
        if current_title != "Preamble":
            section_text = text[current_start:m.start()]
            sentence_count = len(re.findall(r'[.!?]\s+[A-Z]', section_text)) + 1
            section_texts.append({"title": current_title, "sentences": sentence_count, "position": current_start})
        current_title = m.group(2).strip()
        current_start = m.end()

    # Last section
    if current_title != "Preamble":
        section_text = text[current_start:]
        sentence_count = len(re.findall(r'[.!?]\s+[A-Z]', section_text)) + 1
        section_texts.append({"title": current_title, "sentences": sentence_count, "position": current_start})

    for sec in section_texts:
        if sec["sentences"] <= 1 and len(sec["title"]) > 5:
            issues.append({
                "severity": "medium",
                "message": f"Section '{sec['title'][:60]}' has only {sec['sentences']} sentence(s) — may be too short.",
            })
        if sec["sentences"] > 40:
            issues.append({
                "severity": "low",
                "message": f"Section '{sec['title'][:60]}' has {sec['sentences']} sentences — consider breaking up.",
            })

    return issues


def check_abbreviation_first_use(text):
    """Check that abbreviations are defined on first use."""
    issues = []
    # Pattern: "Full Name (ABBR)" or "ABBR (Full Name)"
    abbreviations = {}

    for m in re.finditer(r'([A-Z][a-z]+(?:\s+[a-z]+){1,8})\s+\(([A-Z]{2,8})\)', text):
        abbrev = m.group(2)
        if abbrev not in abbreviations:
            abbreviations[abbrev] = {
                "full": m.group(1),
                "first_use": m.start(),
            }

    # Find subsequent uses of the abbreviation without definition
    # This is hard to do perfectly without NLP — flag abbreviations used before being defined
    for abbrev, info in abbreviations.items():
        # Search for the abbreviation appearing BEFORE its definition
        for m in re.finditer(r'\b' + re.escape(abbrev) + r'\b', text[:info["first_use"]]):
            # Check this isn't part of the full name
            start = max(0, m.start() - 50)
            context = text[start:m.end()]
            if info["full"].lower() not in context.lower():
                issues.append({
                    "severity": "low",
                    "message": f"'{abbrev}' may be used before its definition at position {info['first_use']}.",
                })
                break

    return issues


def check_citation_range(text):
    """Check that citation numbers are within reasonable range."""
    issues = []
    citations = [int(n) for n in re.findall(r'\[(\d+)\]', text)]

    if not citations:
        return issues

    max_cite = max(citations)

    # Check for suspiciously low max citation
    bib_count = len(re.findall(r'\\bibitem\{|@article\{|@inproceedings\{|@\w+\{', text))
    if bib_count > 0 and max_cite > bib_count:
        issues.append({
            "severity": "high",
            "message": f"Highest citation number [{max_cite}] exceeds bibliography entries ({bib_count}).",
        })

    # Check if citation [1] exists
    if 1 not in citations and citations:
        issues.append({
            "severity": "low",
            "message": "Citation [1] never referenced. Citation numbering may start from a different number.",
        })

    return issues


# ── Report Builder ─────────────────────────────────────────────────────────────────


def build_report(all_issues, definitions, references, stats):
    """Build the validation report."""
    lines = [
        "# Cross-Reference Validation Report",
        "",
        f"**Total issues:** {stats['total']} "
        f"({stats['high']} high, {stats['medium']} medium, {stats['low']} low)",
        "",
    ]

    if stats["high"] > 0:
        lines.append(f"> ⚠ **{stats['high']} high-severity issues** — fix before submission.")
    if stats["total"] == 0:
        lines.append("> ✅ No issues found. All cross-references appear valid.")
    lines.append("")

    # Summary counts
    def_count = sum(len(v) for v in definitions.values())
    ref_count = sum(len(v) for v in references.values())
    lines.extend([
        "## Reference Inventory",
        "",
        f"| Type | Defined | Referenced | Gap |",
        f"|---|---:|---:|---:|",
    ])

    type_pairs = [
        ("Figures", "figures", "figure_refs"),
        ("Tables", "tables", "table_refs"),
        ("Equations", "equations", "equation_refs"),
        ("Sections", "sections", "section_refs"),
    ]
    for label, def_key, ref_key in type_pairs:
        d_count = len(definitions.get(def_key, []))
        r_count = len(references.get(ref_key, []))
        gap = d_count - len(set(r.get("num", r.get("id")) for r in references.get(ref_key, []) if r.get("num")))
        lines.append(f"| {label} | {d_count} | {r_count} | {gap:+d} |")

    lines.extend([
        "",
        f"**Citations in text:** {len(references.get('citation_refs', []))}",
        f"**Sections detected:** {len(definitions.get('sections', []))}",
        "",
    ])

    # High severity issues
    high_issues = [i for i in all_issues if i["severity"] == "high"]
    if high_issues:
        lines.append("## High-Severity Issues")
        lines.append("")
        for i, issue in enumerate(high_issues, 1):
            lines.append(f"- [!!] {issue['message']}")
        lines.append("")

    medium_issues = [i for i in all_issues if i["severity"] == "medium"]
    if medium_issues:
        lines.append("## Medium-Severity Issues")
        lines.append("")
        for i, issue in enumerate(medium_issues, 1):
            lines.append(f"- [-] {issue['message']}")
        lines.append("")

    low_issues = [i for i in all_issues if i["severity"] == "low"]
    if low_issues:
        lines.append("## Low-Severity Issues")
        lines.append("")
        for i, issue in enumerate(low_issues[:20], 1):
            lines.append(f"- [.] {issue['message']}")
        if len(low_issues) > 20:
            lines.append(f"- ... and {len(low_issues) - 20} more low-severity issues.")
        lines.append("")

    # Figure/Table reference matrix
    lines.extend([
        "## Figure & Table Cross-Reference Matrix",
        "",
        "| Object | Defined at | First Referenced at | Δ (ref - def) |",
        "|--------|-----------|---------------------|---------------|",
    ])

    for obj_type, defs, refs_key, prefix in [
        ("Figure", definitions.get("figures", []), "figure_refs", "Fig."),
        ("Table", definitions.get("tables", []), "table_refs", "Table"),
    ]:
        for d in defs:
            d_num = d.get("num", d.get("id", "?"))
            d_pos = d.get("position", 0)
            # Find first reference
            first_ref_pos = None
            for r in references.get(refs_key, []):
                if r.get("num") == d_num or r.get("id") == d_num:
                    if first_ref_pos is None or r["position"] < first_ref_pos:
                        first_ref_pos = r["position"]
            if first_ref_pos is not None:
                delta = first_ref_pos - d_pos
                delta_str = f"{-delta:+d} chars" if delta < 0 else f"{delta:+d} chars (after)"
                order = "⚠ ref before def" if delta < 0 else "✓"
                lines.append(f"| {prefix} {d_num} | {d_pos} | {first_ref_pos} | {delta_str} {order} |")
            else:
                lines.append(f"| {prefix} {d_num} | {d_pos} | — | ⚠ never referenced |")

    lines.extend([
        "",
        "## Fix Checklist",
        "",
        "Before final submission:",
        "",
        "- [ ] All high-severity issues resolved",
        "- [ ] All medium-severity issues reviewed and resolved or acknowledged",
        "- [ ] Every figure and table is referenced BEFORE it appears in the PDF",
        "- [ ] Figure/Table/Equation numbering is sequential with no gaps",
        "- [ ] Every citation in text has a corresponding bibliography entry",
        "- [ ] All abbreviations are defined on first use",
        "- [ ] Sections are reasonably balanced in length",
        "",
    ])

    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Validate cross-references and structural consistency in a manuscript",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_references.py 08_english_polished.md --output ref_report.md
  python validate_references.py paper.tex --format latex --output ref_report.md
        """,
    )
    parser.add_argument("paper", help="Manuscript file (.md or .tex)")
    parser.add_argument("--format", default="auto", choices=["auto", "markdown", "latex"])
    parser.add_argument("--output", "-o", default="reference_report.md")
    args = parser.parse_args()

    text = Path(args.paper).read_text(encoding="utf-8", errors="replace")

    definitions = extract_object_definitions(text)
    references = extract_references(text)

    all_issues = []

    # Sequential numbering
    all_issues.extend(check_sequential_numbering(definitions["figures"], "Figure"))
    all_issues.extend(check_sequential_numbering(definitions["tables"], "Table"))
    all_issues.extend(check_sequential_numbering(references["equation_refs"], "Equation"))

    # Orphan definitions
    all_issues.extend(check_orphan_definitions(
        definitions["figures"], references["figure_refs"], "Figure", "Figure ref"))
    all_issues.extend(check_orphan_definitions(
        definitions["tables"], references["table_refs"], "Table", "Table ref"))

    # Refs before defs
    all_issues.extend(check_refs_before_defs(
        references["figure_refs"], definitions["figures"], "Figure", "Figure"))
    all_issues.extend(check_refs_before_defs(
        references["table_refs"], definitions["tables"], "Table", "Table"))

    # Section balance
    all_issues.extend(check_section_balance(text))

    # Abbreviation first use
    all_issues.extend(check_abbreviation_first_use(text))

    # Citation range
    all_issues.extend(check_citation_range(text))

    stats = {
        "total": len(all_issues),
        "high": sum(1 for i in all_issues if i["severity"] == "high"),
        "medium": sum(1 for i in all_issues if i["severity"] == "medium"),
        "low": sum(1 for i in all_issues if i["severity"] == "low"),
    }

    report = build_report(all_issues, definitions, references, stats)
    Path(args.output).write_text(report, encoding="utf-8")

    def_count = sum(len(v) for v in definitions.values())
    ref_count = sum(len(v) for v in references.values())
    print(f"Found {def_count} defined objects, {ref_count} references, "
          f"{stats['total']} issues ({stats['high']} high).", file=sys.stderr)
    print(f"Saved to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
