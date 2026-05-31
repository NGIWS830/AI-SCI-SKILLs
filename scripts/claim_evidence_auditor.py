#!/usr/bin/env python3
"""Audit claim-evidence alignment in a manuscript.

Usage:
    python claim_evidence_auditor.py paper.md --tables results.csv,ablation.csv \\
        --output audit_report.md

    python claim_evidence_auditor.py paper.md --output-dir ./outputs/ \\
        --output audit_report.md

What this does:
    1. Parses the manuscript and extracts all factual claims
    2. For each claim, searches for evidence (table/figure/section reference)
    3. Verifies that numerical claims in prose match actual table values
    4. Flags: unsupported claims, overclaimed statements, missing evidence,
       stale references, number mismatches
    5. Produces a per-claim audit report with severity ratings
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path


# ── Claim Extraction ───────────────────────────────────────────────────────────────


def extract_claims(text):
    """Extract all factual claims from manuscript text.

    A "claim" is any sentence that asserts a fact about the method, results,
    or contribution. We identify them by patterns.
    """
    claims = []

    # Pattern 1: Performance claims (most important)
    # "achieves X on Y", "improves by Z", "outperforms W", "reduces X by Y"
    perf_patterns = [
        (r'(?:achieves?|reaches?|obtains?|yields?)\s+([^.]*?(?:\d+\.?\d*|%)[^.]*?\.)',
         "performance_claim"),
        (r'(?:improves?|boosts?|increases?)\s+(?:over|upon)?\s*([^.]*?(?:\d+\.?\d*|%)[^.]*?\.)',
         "improvement_claim"),
        (r'(?:outperforms?|surpasses?|exceeds?|beats?)\s+([^.]*?(?:\d+\.?\d*|%)[^.]*?\.)',
         "superiority_claim"),
        (r'(?:reduces?|decreases?|lowers?|cuts?)\s+([^.]*?(?:\d+\.?\d*|%)[^.]*?\.)',
         "reduction_claim"),
        (r'(?:comparable to|on par with|competitive with|matches?)\s+([^.]*?\.)',
         "parity_claim"),
    ]

    for pattern, claim_type in perf_patterns:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            claim_text = m.group(1).strip()[:250]
            section = _find_section(text, m.start())
            claims.append({
                "text": claim_text,
                "type": claim_type,
                "section": section,
                "position": m.start(),
                "has_number": bool(re.search(r'\d+\.?\d*', claim_text)),
                "has_reference": bool(re.search(r'(?:Table|Figure|Fig\.?|Section)\s+\d+', claim_text)),
            })

    # Pattern 2: Contribution / novelty claims
    contrib_patterns = [
        (r'(?:we propose|we introduce|we present|we design|we develop)\s+([^.]*?\.)',
         "contribution_claim"),
        (r'(?:is the first to|to the best of our knowledge|novel)\s+([^.]*?\.)',
         "novelty_claim"),
        (r'(?:our (?:method|approach|model|framework)\s+(?:is|can|enables|allows)\s+[^.]*?\.)',
         "capability_claim"),
    ]

    for pattern, claim_type in contrib_patterns:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            claim_text = m.group(1).strip()[:250] if m.lastindex else m.group(0).strip()[:250]
            section = _find_section(text, m.start())
            if not any(c["text"][:80] == claim_text[:80] for c in claims):
                claims.append({
                    "text": claim_text,
                    "type": claim_type,
                    "section": section,
                    "position": m.start(),
                    "has_number": bool(re.search(r'\d+\.?\d*', claim_text)),
                    "has_reference": bool(re.search(r'(?:Table|Figure|Fig\.?|Section)\s+\d+', claim_text)),
                })

    # Pattern 3: Ablation / component claims
    ablation_patterns = [
        (r'(?:ablation|(?:w/o|without)\s+\w+|component\s+\w+|module\s+\w+)\s+(?:shows?|demonstrates?|confirms?|reveals?|contributes?)\s+([^.]*?\.)',
         "ablation_claim"),
    ]

    for pattern, claim_type in ablation_patterns:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            claim_text = m.group(1).strip()[:250] if m.lastindex else m.group(0).strip()[:250]
            section = _find_section(text, m.start())
            if not any(c["text"][:80] == claim_text[:80] for c in claims):
                claims.append({
                    "text": claim_text,
                    "type": claim_type,
                    "section": section,
                    "position": m.start(),
                    "has_number": bool(re.search(r'\d+\.?\d*', claim_text)),
                    "has_reference": bool(re.search(r'(?:Table|Figure|Fig\.?|Section)\s+\d+', claim_text)),
                })

    return claims


def _find_section(text, pos):
    """Find the section name containing a given position."""
    sections = list(re.finditer(r'^(#{1,3})\s+(.+)$', text[:pos], re.MULTILINE))
    if sections:
        return sections[-1].group(2).strip()[:60]
    return "Preamble"


# ── Table Data Extraction ──────────────────────────────────────────────────────────


def extract_table_data(args):
    """Read CSV tables and return a searchable dict."""
    tables = {}

    # If output_dir specified, search for CSV files
    if args.output_dir:
        output_path = Path(args.output_dir)
        for csv_file in output_path.glob("*.csv"):
            try:
                with open(csv_file, newline="", encoding="utf-8-sig") as f:
                    rows = list(csv.DictReader(f))
                tables[csv_file.name] = rows
            except Exception:
                pass

    # If specific tables specified
    if args.tables:
        for table_path in args.tables.split(","):
            table_path = table_path.strip()
            try:
                with open(table_path, newline="", encoding="utf-8-sig") as f:
                    rows = list(csv.DictReader(f))
                tables[Path(table_path).name] = rows
            except Exception as e:
                print(f"Warning: could not read {table_path}: {e}", file=sys.stderr)

    return tables


def search_table_for_number(tables, number_str, tolerance=0.01):
    """Search all tables for a given number. Returns (table_name, row_context) or None."""
    try:
        target = float(number_str.replace("%", "").replace(",", ""))
    except ValueError:
        return None

    for table_name, rows in tables.items():
        for row in rows:
            for key, val in row.items():
                try:
                    val_float = float(str(val).replace("%", "").replace(",", ""))
                    if abs(val_float - target) < tolerance * max(abs(target), 1):
                        return (table_name, {k: v for k, v in row.items()})
                except (ValueError, TypeError):
                    continue
    return None


# ── Overclaim Detection ────────────────────────────────────────────────────────────


OVERCLAIM_PATTERNS = [
    (r'\b(?:state-of-the-art|state of the art|SOTA)\b', "SOTA claim — requires explicit SOTA comparison", "high"),
    (r'\b(?:significant(?:ly)?)\s+(?:improves?|outperforms?|better|higher|lower|faster)\b',
     "'Significantly' — should be backed by statistical test", "high"),
    (r'\b(?:proves?|proof)\b(?!.*theorem|.*lemma|.*\d)', "'Prove' — use 'demonstrates' or 'suggests' unless formal proof", "high"),
    (r'\b(?:first|novel|unprecedented|groundbreaking|revolutionary)\b',
     "Novelty inflation — avoid 'first'/'groundbreaking', let contribution speak", "medium"),
    (r'\b(?:robust across all|universally|optimal|perfect|completely solves?)\b',
     "Absolute claim — requires extraordinary evidence", "high"),
    (r'\b(?:dramatically|substantially|remarkably|massively)\s+(?:improves?|outperforms?|boosts?)\b',
     "Exaggerated magnitude — replace with specific numbers", "medium"),
    (r'\b(?:generalizes?\s+well|widely\s+applicable)\b',
     "Generalization claim — must be tested on OOD data", "medium"),
]


def detect_overclaims(claim_text):
    """Check a claim for overclaim language."""
    issues = []
    for pattern, message, severity in OVERCLAIM_PATTERNS:
        if re.search(pattern, claim_text, re.IGNORECASE):
            issues.append({"pattern": pattern, "message": message, "severity": severity})
    return issues


# ── Evidence Audit ─────────────────────────────────────────────────────────────────


def audit_claim(claim, tables, manuscript_text):
    """Audit a single claim and return its evidence assessment."""
    issues = []
    evidence = {"type": "none", "details": ""}

    # Check 1: Does the claim reference a table/figure?
    if claim["has_reference"]:
        refs = re.findall(r'(?:Table|Figure|Fig\.?)\s*(\d+)', claim["text"])
        evidence["type"] = "explicit_reference"
        evidence["details"] = f"References: {', '.join(f'{r}' for r in refs)}"
    else:
        issues.append({
            "severity": "medium",
            "message": "Claim has no explicit Table/Figure reference. Add '(Table X)' or '(Figure Y)' to anchor the evidence.",
        })

    # Check 2: Does the claim contain a number that can be traced to a table?
    numbers = re.findall(r'(\d+\.?\d*)\s*(?:%|percent|points|ms|seconds)?', claim["text"])
    if numbers and tables:
        found_in_table = False
        for num in numbers[:3]:
            result = search_table_for_number(tables, num)
            if result:
                table_name, row = result
                evidence["type"] = "number_verified"
                evidence["details"] += f" | Number {num} found in {table_name}"
                found_in_table = True
        if not found_in_table and claim["has_number"]:
            issues.append({
                "severity": "high",
                "message": f"Numerical claim ({numbers[0]}...) not found in any provided table. Verify or add the source table.",
            })

    # Check 3: Overclaim language
    overclaims = detect_overclaims(claim["text"])
    for oc in overclaims:
        issues.append(oc)

    # Check 4: Stale or missing evidence markers
    if "AUTHOR_INPUT_NEEDED" in claim["text"]:
        issues.append({"severity": "high", "message": "Claim contains AUTHOR_INPUT_NEEDED marker — needs author input."})
    if "CITATION NEEDED" in claim["text"]:
        issues.append({"severity": "high", "message": "Claim contains [CITATION NEEDED] — citation missing."})

    # Check 5: Section appropriateness
    if claim["type"] == "performance_claim" and "method" in claim.get("section", "").lower():
        issues.append({"severity": "low",
                        "message": "Performance claim in Method section — results belong in Experiments."})

    return {
        "claim_text": claim["text"][:200],
        "type": claim["type"],
        "section": claim["section"],
        "evidence": evidence,
        "issues": issues,
        "severity": _max_severity(issues),
    }


def _max_severity(issues):
    if not issues:
        return "clean"
    if any(i["severity"] == "high" for i in issues):
        return "high"
    if any(i["severity"] == "medium" for i in issues):
        return "medium"
    return "low"


# ── Report ─────────────────────────────────────────────────────────────────────────


def build_audit_report(audit_results, stats):
    """Format audit results as markdown report."""
    lines = [
        "# Claim-Evidence Alignment Audit",
        "",
        f"**Total claims extracted:** {stats['total']}",
        f"**Clean:** {stats['clean']} | **Low issues:** {stats['low']} | "
        f"**Medium issues:** {stats['medium']} | **High issues:** {stats['high']}",
        "",
    ]

    if stats["high"] > 0:
        lines.append(f"> ⚠ **{stats['high']} high-severity issues found.** These must be resolved before submission.")
    if stats["medium"] > 0:
        lines.append(f"> {stats['medium']} medium-severity issues — review and address as appropriate.")
    lines.append("")

    # Severity summary
    lines.extend([
        "## Severity Summary",
        "",
        "| Severity | Count | Action |",
        "|----------|-------|--------|",
        f"| High | {stats['high']} | Must fix before submission |",
        f"| Medium | {stats['medium']} | Review and fix recommended |",
        f"| Low | {stats['low']} | Consider fixing |",
        f"| Clean | {stats['clean']} | No issues |",
        "",
    ])

    # Section breakdown
    section_counts = defaultdict(lambda: {"total": 0, "issues": 0})
    for r in audit_results:
        sec = r["section"]
        section_counts[sec]["total"] += 1
        section_counts[sec]["issues"] += len(r["issues"])
    lines.extend([
        "## Claims by Section",
        "",
        "| Section | Claims | Issues | Issue Rate |",
        "|---------|--------|--------|------------|",
    ])
    for sec, counts in sorted(section_counts.items()):
        rate = f"{counts['issues'] / counts['total']:.1f}" if counts["total"] else "0"
        lines.append(f"| {sec} | {counts['total']} | {counts['issues']} | {rate}/claim |")
    lines.append("")

    # High severity issues
    high_issues = [r for r in audit_results if r["severity"] == "high"]
    if high_issues:
        lines.append("## High-Severity Issues (Must Fix)")
        lines.append("")
        for i, result in enumerate(high_issues, 1):
            lines.append(f"### Issue {i}: {result['section']} — {result['type']}")
            lines.append(f"> **Claim:** {result['claim_text']}")
            lines.append("")
            for issue in result["issues"]:
                if issue["severity"] == "high":
                    lines.append(f"- [!!] {issue['message']}")
            lines.append("")

    # Medium severity
    medium_issues = [r for r in audit_results if r["severity"] == "medium"]
    if medium_issues:
        lines.append("## Medium-Severity Issues (Recommended Fix)")
        lines.append("")
        for i, result in enumerate(medium_issues[:15], 1):
            lines.append(f"### Issue {i}: {result['section']} — {result['type']}")
            lines.append(f"> **Claim:** {result['claim_text']}")
            lines.append("")
            for issue in result["issues"]:
                lines.append(f"- [-] {issue['message']}")
            lines.append("")

    # Evidence map
    lines.extend([
        "## Evidence Coverage",
        "",
        "| # | Claim (truncated) | Section | Type | Has Ref | Has Number | Evidence | Issues |",
        "|---|------------------|---------|------|---------|------------|----------|--------|",
    ])
    for i, result in enumerate(audit_results, 1):
        ref = "✓" if result["claim_text"] and re.search(r'(?:Table|Figure|Fig\.?)', result["claim_text"]) else "✗"
        num = "✓" if re.search(r'\d+\.?\d*', result["claim_text"]) else "✗"
        evidence_type = result["evidence"]["type"]
        issues_count = len(result["issues"])
        icon = {0: "✅", 1: "⚠", 2: "⚠"}.get(issues_count, "❌") if issues_count <= 2 else "❌"
        lines.append(
            f"| {i} | {result['claim_text'][:80]}... | {result['section']} | "
            f"{result['type']} | {ref} | {num} | {evidence_type} | "
            f"{icon} {issues_count} |"
        )

    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Audit claim-evidence alignment in a manuscript",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python claim_evidence_auditor.py paper.md --output-dir ./outputs/ --output audit.md
  python claim_evidence_auditor.py paper.md --tables results.csv,ablation.csv --output audit.md
        """,
    )
    parser.add_argument("paper", help="Manuscript file (.md or .tex)")
    parser.add_argument("--tables", help="Comma-separated CSV table paths")
    parser.add_argument("--output-dir", help="Directory containing CSV files (auto-discover)")
    parser.add_argument("--output", "-o", default="claim_audit.md")
    args = parser.parse_args()

    paper_text = Path(args.paper).read_text(encoding="utf-8", errors="replace")
    tables = extract_table_data(args)

    if tables:
        print(f"Loaded {len(tables)} tables: {list(tables.keys())}", file=sys.stderr)
    else:
        print("No tables provided. Number verification disabled. Use --tables or --output-dir.", file=sys.stderr)

    claims = extract_claims(paper_text)
    print(f"Extracted {len(claims)} claims from manuscript.", file=sys.stderr)

    audit_results = []
    for claim in claims:
        result = audit_claim(claim, tables, paper_text)
        audit_results.append(result)

    stats = {
        "total": len(audit_results),
        "clean": sum(1 for r in audit_results if r["severity"] == "clean"),
        "low": sum(1 for r in audit_results if r["severity"] == "low"),
        "medium": sum(1 for r in audit_results if r["severity"] == "medium"),
        "high": sum(1 for r in audit_results if r["severity"] == "high"),
    }

    print(f"Audit: {stats['high']} high, {stats['medium']} medium, "
          f"{stats['low']} low, {stats['clean']} clean.", file=sys.stderr)

    report = build_audit_report(audit_results, stats)
    Path(args.output).write_text(report, encoding="utf-8")
    print(f"Saved to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
