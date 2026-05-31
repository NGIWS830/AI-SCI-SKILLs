#!/usr/bin/env python3
"""Validate and normalize BibTeX entries.

Usage:
    python format_bibtex.py refs.bib --validate --normalize --output refs_clean.bib
"""

import argparse
import os
import re
import sys


# ── BibTeX Parsing ──────────────────────────────────────────────────────────────

def parse_bibtex(bib_content):
    """Parse BibTeX content into a list of entries."""
    entries = []
    entry_pattern = re.compile(
        r'@(\w+)\s*\{\s*([^,]*?)\s*,\s*(.*?)\}\s*$',
        re.DOTALL | re.MULTILINE
    )

    for match in entry_pattern.finditer(bib_content):
        entry_type = match.group(1).lower()
        entry_key = match.group(2).strip()
        fields_str = match.group(3)

        fields = _parse_fields(fields_str)
        entries.append({
            "type": entry_type,
            "key": entry_key,
            "fields": fields,
        })

    return entries


def _parse_fields(fields_str):
    """Parse BibTeX field assignments."""
    fields = {}
    # Match field = "value" or field = {value}
    pattern = re.compile(r'(\w+)\s*=\s*[{"]([^}"]*)[}"]')
    for m in pattern.finditer(fields_str):
        fields[m.group(1).lower()] = m.group(2)
    return fields


def format_bibtex(entries):
    """Format entries back to BibTeX string."""
    lines = []
    for entry in entries:
        entry_type = entry["type"]
        key = entry["key"]
        fields = entry["fields"]

        lines.append(f"@{entry_type}{{{key},")
        for field, value in sorted(fields.items()):
            # Use braces for values that contain special characters
            if any(c in value for c in ['{', '}', '\\', '&', '#', '_', '^', '~']):
                lines.append(f"  {field} = {{{value}}},")
            else:
                lines.append(f"  {field} = {{{value}}},")
        lines.append("}")
        lines.append("")

    return "\n".join(lines)


# ── Validation ──────────────────────────────────────────────────────────────────

REQUIRED_FIELDS = {
    "article": ["author", "title", "journal", "year"],
    "inproceedings": ["author", "title", "booktitle", "year"],
    "incollection": ["author", "title", "booktitle", "year"],
    "inbook": ["author", "title", "chapter", "publisher", "year"],
    "book": ["author", "title", "publisher", "year"],
    "phdthesis": ["author", "title", "school", "year"],
    "mastersthesis": ["author", "title", "school", "year"],
    "techreport": ["author", "title", "institution", "year"],
    "misc": ["author", "title", "year"],
}

RECOMMENDED_FIELDS = {
    "article": ["volume", "number", "pages", "doi"],
    "inproceedings": ["pages", "doi", "address"],
    "misc": ["eprint", "archiveprefix", "note"],
}


def validate_entry(entry):
    """Validate a BibTeX entry. Returns list of issues."""
    issues = []
    entry_type = entry["type"]
    fields = entry["fields"]
    key = entry["key"]

    # Check required fields
    required = REQUIRED_FIELDS.get(entry_type, ["author", "title", "year"])
    for field in required:
        if field not in fields or not fields[field].strip():
            issues.append(f"[{key}] Missing required field: {field}")

    # Check recommended fields
    recommended = RECOMMENDED_FIELDS.get(entry_type, [])
    for field in recommended:
        if field not in fields or not fields[field].strip():
            issues.append(f"[{key}] Missing recommended field: {field} (info only)")

    # Check for empty values
    for field, value in fields.items():
        if not value.strip():
            issues.append(f"[{key}] Empty value for field: {field}")

    # Check key format
    if not re.match(r'^[a-zA-Z0-9_\-:]+$', key):
        issues.append(f"[{key}] Key contains unusual characters. Consider: {_suggest_key(entry)}")

    return issues


def _suggest_key(entry):
    """Suggest a BibTeX key based on first author + year."""
    authors = entry["fields"].get("author", "Unknown")
    first_author = authors.split(" and ")[0].split(",")[0].strip().split()[-1]
    year = entry["fields"].get("year", "0000")
    key = f"{first_author}{year}"
    return "".join(c for c in key if c.isalnum())


# ── Normalization ───────────────────────────────────────────────────────────────

VENUE_ABBREVIATIONS = {
    "proceedings of the ieee/cvf conference on computer vision and pattern recognition": "CVPR",
    "proceedings of the ieee international conference on computer vision": "ICCV",
    "advances in neural information processing systems": "NeurIPS",
    "international conference on machine learning": "ICML",
    "international conference on learning representations": "ICLR",
    "proceedings of the conference on empirical methods in natural language processing": "EMNLP",
    "proceedings of the annual meeting of the association for computational linguistics": "ACL",
    "proceedings of the aaai conference on artificial intelligence": "AAAI",
}


def normalize_venue(venue):
    """Normalize venue names to standard abbreviations."""
    venue_lower = venue.lower().strip().rstrip(".")
    if venue_lower in VENUE_ABBREVIATIONS:
        return VENUE_ABBREVIATIONS[venue_lower]
    return venue


def normalize_entry(entry):
    """Normalize fields in a BibTeX entry."""
    fields = entry["fields"]

    # Normalize venue
    for field in ["journal", "booktitle"]:
        if field in fields:
            fields[field] = normalize_venue(fields[field])

    # Normalize year
    if "year" in fields:
        year_match = re.search(r'\d{4}', fields["year"])
        if year_match:
            fields["year"] = year_match.group(0)

    # Normalize DOI
    if "doi" in fields:
        doi = fields["doi"].strip()
        doi = re.sub(r'^https?://doi\.org/', '', doi)
        fields["doi"] = doi

    # Normalize author list
    if "author" in fields:
        fields["author"] = fields["author"].strip()

    entry["fields"] = fields
    return entry


def detect_duplicates(entries):
    """Detect potential duplicate entries."""
    seen = {}
    duplicates = []
    for entry in entries:
        title = entry["fields"].get("title", "").lower().strip().rstrip(".")
        if title in seen:
            duplicates.append(f"Possible duplicate: '{entry['key']}' and '{seen[title]}' (same title)")
        else:
            seen[title] = entry["key"]
    return duplicates


# ── CLI ─────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Validate and normalize BibTeX entries")
    parser.add_argument("bib_file", help="BibTeX file to process")
    parser.add_argument("--validate", action="store_true", help="Validate entries for missing fields")
    parser.add_argument("--normalize", action="store_true", help="Normalize venue names, DOI, year, etc.")
    parser.add_argument("--output", "-o", help="Output normalized BibTeX file")
    parser.add_argument("--detect-duplicates", action="store_true", help="Detect duplicate entries")
    args = parser.parse_args()

    with open(args.bib_file, "r", encoding="utf-8") as f:
        content = f.read()

    entries = parse_bibtex(content)

    if not entries:
        print("No BibTeX entries found.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(entries)} entries.", file=sys.stderr)

    all_issues = []

    # Validate
    if args.validate:
        print("\nValidation:", file=sys.stderr)
        for entry in entries:
            issues = validate_entry(entry)
            all_issues.extend(issues)
        if all_issues:
            for issue in all_issues:
                print(f"  - {issue}", file=sys.stderr)
            print(f"\n  {len(all_issues)} issue(s) found.", file=sys.stderr)
        else:
            print("  All entries pass validation.", file=sys.stderr)

    # Detect duplicates
    if args.detect_duplicates:
        dups = detect_duplicates(entries)
        if dups:
            print("\nDuplicate check:", file=sys.stderr)
            for d in dups:
                print(f"  - {d}", file=sys.stderr)

    # Normalize
    if args.normalize:
        entries = [normalize_entry(e) for e in entries]
        print(f"\nNormalized {len(entries)} entries.", file=sys.stderr)

    # Output
    output = format_bibtex(entries)
    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
