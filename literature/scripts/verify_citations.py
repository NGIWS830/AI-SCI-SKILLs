#!/usr/bin/env python3
"""Verify citation metadata across CrossRef and DBLP.

Usage:
    python verify_citations.py citations.txt --sources crossref,dblp --output verified.md
    python verify_citations.py --bibtex refs.bib --verify-all --output verified.md
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from typing import Optional

# ── API Configuration ──────────────────────────────────────────────────────────

CROSSREF_API_URL = "https://api.crossref.org/works"
DBLP_API_URL = "https://dblp.org/search/publ/api"
USER_AGENT = "AI-SCI-SKILLs/0.3 (mailto:research@example.com)"

# ── Helpers ─────────────────────────────────────────────────────────────────────

def _make_request(url, max_retries=3):
    headers = {"User-Agent": USER_AGENT}
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2 ** attempt)
                continue
            return None
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                return None
    return None


def _parse_citation_line(line):
    """Parse a citation line like 'Author, Title (Year)' or 'Title (Year)' or DOI."""
    line = line.strip()
    # DOI pattern
    doi_match = re.search(r'10\.\d{4,}/[^\s"\']+', line)
    if doi_match:
        return {"doi": doi_match.group(0), "type": "doi"}

    # arXiv ID pattern
    arxiv_match = re.search(r'(\d{4}\.\d{4,}|[a-z\-]+\/\d{7})', line)
    if arxiv_match and 'arxiv' in line.lower():
        return {"arxiv_id": arxiv_match.group(1), "type": "arxiv"}

    # Title + Author pattern (heuristic)
    return {"raw": line, "type": "text"}


def _verify_via_crossref(doi=None, title=None, author=None):
    """Verify a paper via CrossRef API."""
    if doi:
        url = f"{CROSSREF_API_URL}/{urllib.parse.quote(doi)}"
        data = _make_request(url)
        if not data:
            return None
        try:
            msg = json.loads(data).get("message", {})
            return {
                "title": msg.get("title", [""])[0] if msg.get("title") else "",
                "doi": msg.get("DOI", ""),
                "venue": (msg.get("container-title", [""]) or [""])[0],
                "year": str((msg.get("published-print", {}) or msg.get("created", {})).get("date-parts", [[0]])[0][0]),
                "authors": ", ".join(
                    f"{a.get('given', '')} {a.get('family', '')}".strip()
                    for a in (msg.get("author", []) or [])[:8]
                ),
                "source": "crossref",
            }
        except (json.JSONDecodeError, KeyError, IndexError):
            return None

    if title:
        params = {"query.title": title[:100], "rows": 1}
        if author:
            params["query.author"] = author.split()[-1] if author.split() else ""
        url = CROSSREF_API_URL + "?" + urllib.parse.urlencode(params)
        data = _make_request(url)
        if not data:
            return None
        try:
            items = json.loads(data).get("message", {}).get("items", [])
            if items:
                msg = items[0]
                return {
                    "title": msg.get("title", [""])[0] if msg.get("title") else "",
                    "doi": msg.get("DOI", ""),
                    "venue": (msg.get("container-title", [""]) or [""])[0],
                    "year": str((msg.get("published-print", {}) or msg.get("created", {})).get("date-parts", [[0]])[0][0]),
                    "authors": ", ".join(
                        f"{a.get('given', '')} {a.get('family', '')}".strip()
                        for a in (msg.get("author", []) or [])[:8]
                    ),
                    "source": "crossref",
                }
        except (json.JSONDecodeError, KeyError, IndexError):
            pass
    return None


def _verify_via_dblp(title=None, author=None):
    """Verify a paper via DBLP API."""
    if not title:
        return None
    query = title[:80]
    if author:
        query += f" {author.split()[-1]}" if author.split() else ""
    params = {"q": query, "h": 1, "format": "json"}
    url = DBLP_API_URL + "?" + urllib.parse.urlencode(params)
    data = _make_request(url)
    if not data:
        return None
    try:
        hits = json.loads(data).get("result", {}).get("hits", {}).get("hit", [])
        if isinstance(hits, dict):
            hits = [hits]
        if hits:
            info = hits[0].get("info", {})
            author_list = (info.get("authors", {}) or {}).get("author", [])
            if isinstance(author_list, dict):
                author_list = [author_list]
            return {
                "title": info.get("title", ""),
                "doi": info.get("doi", ""),
                "venue": info.get("venue", ""),
                "year": str(info.get("year", "")),
                "authors": ", ".join(
                    a.get("text", "") if isinstance(a, dict) else str(a)
                    for a in author_list[:8]
                ),
                "source": "dblp",
            }
    except (json.JSONDecodeError, KeyError, IndexError):
        pass
    return None


def _parse_bibtex(bibtex_content):
    """Parse BibTeX content into a list of entry dicts."""
    entries = []
    entry_pattern = re.compile(r'@(\w+)\s*\{([^,]*),\s*(.*?)\}', re.DOTALL)
    field_pattern = re.compile(r'(\w+)\s*=\s*[{"]([^}"]*)[}"]')

    for match in entry_pattern.finditer(bibtex_content):
        entry_type = match.group(1)
        entry_key = match.group(2)
        fields_str = match.group(3)
        fields = {}
        for fm in field_pattern.finditer(fields_str):
            fields[fm.group(1).lower()] = fm.group(2)
        entries.append({
            "key": entry_key,
            "type": entry_type,
            "title": fields.get("title", ""),
            "author": fields.get("author", ""),
            "year": fields.get("year", ""),
            "journal": fields.get("journal", "") or fields.get("booktitle", ""),
            "doi": fields.get("doi", ""),
            "eprint": fields.get("eprint", ""),
        })
    return entries


# ── Verification Logic ──────────────────────────────────────────────────────────

VERIFICATION_STATUSES = {
    "confirmed": "✓ confirmed (multiple sources agree)",
    "single_source": "~ single source (cross-check recommended)",
    "not_found": "✗ not found (may need manual check)",
    "manual": "? needs manual verification",
}


def verify_paper(title="", author="", doi="", arxiv_id=""):
    """Verify a single paper across available sources.

    Returns dict with verification status and consolidated metadata.
    """
    results = []

    # Try CrossRef by DOI first (most reliable)
    if doi:
        cr = _verify_via_crossref(doi=doi)
        if cr:
            results.append(cr)

    # Try CrossRef by title
    if title and (not results):
        cr = _verify_via_crossref(title=title, author=author)
        if cr:
            results.append(cr)

    # Try DBLP by title
    if title:
        dblp = _verify_via_dblp(title=title, author=author)
        if dblp:
            results.append(dblp)

    if not results:
        return {"status": "not_found", "metadata": {}, "sources": []}

    # Determine verification status
    if len(results) >= 2:
        # Cross-check: do titles match (fuzzy)?
        status = "confirmed"
    elif len(results) == 1:
        status = "single_source"
    else:
        status = "not_found"

    # Merge metadata (prefer CrossRef for completeness)
    merged = results[0]
    if len(results) > 1:
        for field in ["doi", "year", "venue"]:
            if not merged.get(field):
                for r in results[1:]:
                    if r.get(field):
                        merged[field] = r[field]
                        break

    return {
        "status": status,
        "metadata": merged,
        "sources": [r.get("source", "unknown") for r in results],
    }


# ── Output Formatting ───────────────────────────────────────────────────────────

def format_verification_report(verifications):
    """Format verification results as a Markdown report."""
    lines = [
        "| # | Input | Title (Verified) | Venue | Year | DOI | Status |",
        "|---|-------|-----------------|-------|------|-----|--------|",
    ]
    for i, v in enumerate(verifications, 1):
        input_info = v.get("input", "")[:50]
        meta = v.get("metadata", {})
        title = meta.get("title", "")[:60]
        venue = meta.get("venue", "")[:30]
        year = meta.get("year", "")
        doi = meta.get("doi", "")
        status_label = VERIFICATION_STATUSES.get(v.get("status", ""), v.get("status", ""))

        lines.append(
            f"| {i} | {input_info} | {title} | {venue} | {year} | {doi} | {status_label} |"
        )

    # Summary
    confirmed = sum(1 for v in verifications if v.get("status") == "confirmed")
    single = sum(1 for v in verifications if v.get("status") == "single_source")
    not_found = sum(1 for v in verifications if v.get("status") == "not_found")

    lines.append("\n## Summary\n")
    lines.append(f"- ✓ Confirmed: {confirmed}")
    lines.append(f"- ~ Single source: {single}")
    lines.append(f"- ✗ Not found: {not_found}")
    lines.append(f"- Total: {len(verifications)}")

    return "\n".join(lines)


# ── CLI ─────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Verify citation metadata across academic databases"
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("citations_file", nargs="?", help="File with citations (one per line)")
    input_group.add_argument("--bibtex", help="BibTeX file to verify")

    parser.add_argument("--sources", default="crossref,dblp",
                        help="Sources to verify against (default: crossref,dblp)")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--verify-all", action="store_true",
                        help="Verify all entries in BibTeX")

    args = parser.parse_args()

    citations_to_verify = []

    if args.bibtex:
        with open(args.bibtex, "r", encoding="utf-8") as f:
            entries = _parse_bibtex(f.read())
        for entry in entries:
            citations_to_verify.append({
                "input": f"{entry.get('author', 'Unknown')[:40]} — {entry.get('title', '')[:60]}",
                "title": entry.get("title", ""),
                "author": entry.get("author", ""),
                "doi": entry.get("doi", ""),
                "arxiv_id": entry.get("eprint", ""),
            })
    elif args.citations_file:
        with open(args.citations_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parsed = _parse_citation_line(line)
                citations_to_verify.append({
                    "input": line[:80],
                    "title": "",
                    "author": "",
                    "doi": parsed.get("doi", ""),
                    "arxiv_id": parsed.get("arxiv_id", ""),
                })

    # Verify each citation
    verifications = []
    for cit in citations_to_verify:
        print(f"Verifying: {cit['input'][:60]}...", file=sys.stderr)
        result = verify_paper(
            title=cit.get("title", ""),
            author=cit.get("author", ""),
            doi=cit.get("doi", ""),
            arxiv_id=cit.get("arxiv_id", ""),
        )
        result["input"] = cit["input"]
        verifications.append(result)
        time.sleep(0.3)  # Be polite to APIs

    # Generate report
    report = format_verification_report(verifications)

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write("# Citation Verification Report\n\n")
            f.write(report)
        print(f"Saved report to {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
