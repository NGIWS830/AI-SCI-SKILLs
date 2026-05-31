#!/usr/bin/env python3
"""Unified literature search across Semantic Scholar, arXiv, CrossRef, and DBLP.

Usage:
    python search_literature.py "cross-modal retrieval" --sources s2,arxiv --max 20 --output results.md
    python search_literature.py --query-file queries.txt --sources all --format matrix --output lit_matrix.md
"""

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Optional

# ── API Configuration ──────────────────────────────────────────────────────────

SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
ARXIV_API_URL = "http://export.arxiv.org/api/query"
CROSSREF_API_URL = "https://api.crossref.org/works"
DBLP_API_URL = "https://dblp.org/search/publ/api"

# Semantic Scholar API key (optional: set SEMANTIC_SCHOLAR_API_KEY env var for higher rate limits)
S2_API_KEY = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "")

USER_AGENT = "AI-SCI-SKILLs/0.4.0 (mailto:research@example.com)"

# ── Helper Functions ────────────────────────────────────────────────────────────

def _make_request(url, headers=None, max_retries=3):
    """Make an HTTP request with retry logic and rate limiting."""
    if headers is None:
        headers = {}
    headers.setdefault("User-Agent", USER_AGENT)

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code == 429:  # Rate limited
                wait = 2 ** attempt
                time.sleep(wait)
                continue
            if e.code == 404:
                return None
            print(f"HTTP error {e.code} for {url}", file=sys.stderr)
            return None
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            print(f"Request failed: {e}", file=sys.stderr)
            return None
    return None


def _safe_get(d, *keys, default=""):
    """Safely traverse nested dicts."""
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, {})
        else:
            return default
    return d if d != {} else default


# ── Search Functions ────────────────────────────────────────────────────────────

def search_semantic_scholar(query, limit=20, offset=0):
    """Search Semantic Scholar for papers.

    Returns list of dicts with: title, authors, year, venue, abstract,
    citationCount, arXivId, DOI, paperId, url.
    """
    params = {
        "query": query,
        "limit": min(limit, 100),
        "offset": offset,
        "fields": "title,authors,year,venue,abstract,citationCount,externalIds,url",
    }
    url = SEMANTIC_SCHOLAR_URL + "?" + urllib.parse.urlencode(params)
    headers = {}
    if S2_API_KEY:
        headers["x-api-key"] = S2_API_KEY

    data = _make_request(url, headers=headers)
    if not data:
        return []

    try:
        results = json.loads(data)
    except json.JSONDecodeError:
        return []

    papers = []
    for item in results.get("data", []):
        authors = item.get("authors", [])
        author_names = [a.get("name", "") for a in authors]
        external_ids = item.get("externalIds", {}) or {}
        papers.append({
            "title": item.get("title", ""),
            "authors": ", ".join(author_names[:8]),  # First 8 authors
            "year": item.get("year", ""),
            "venue": item.get("venue", ""),
            "abstract": (item.get("abstract") or "")[:500],
            "citationCount": item.get("citationCount", 0),
            "arXivId": external_ids.get("ArXiv", ""),
            "DOI": external_ids.get("DOI", ""),
            "paperId": item.get("paperId", ""),
            "url": item.get("url", ""),
            "source": "s2",
        })
    return papers


def search_arxiv(query, limit=20, start=0):
    """Search arXiv for papers.

    Returns list of dicts compatible with other search sources.
    """
    params = {
        "search_query": f"all:{query}",
        "start": start,
        "max_results": min(limit, 100),
        "sortBy": "relevance",
    }
    url = ARXIV_API_URL + "?" + urllib.parse.urlencode(params)
    data = _make_request(url)
    if not data:
        return []

    papers = []
    try:
        root = ET.fromstring(data)
        ns = {"atom": "http://www.w3.org/2005/Atom",
              "arxiv": "http://arxiv.org/schemas/atom"}
        for entry in root.findall("atom:entry", ns):
            title_el = entry.find("atom:title", ns)
            title = title_el.text.strip().replace("\n", " ") if title_el is not None else ""
            summary_el = entry.find("atom:summary", ns)
            abstract = summary_el.text.strip().replace("\n", " ") if summary_el is not None else ""
            published_el = entry.find("atom:published", ns)
            year = published_el.text[:4] if published_el is not None else ""

            authors = []
            for author_el in entry.findall("atom:author", ns):
                name_el = author_el.find("atom:name", ns)
                if name_el is not None:
                    authors.append(name_el.text)

            id_url = ""
            for link in entry.findall("atom:id", ns):
                id_url = link.text or ""

            arxiv_id = id_url.split("/abs/")[-1] if "/abs/" in id_url else ""

            papers.append({
                "title": title,
                "authors": ", ".join(authors[:8]),
                "year": year,
                "venue": "arXiv preprint",
                "abstract": abstract[:500],
                "citationCount": 0,
                "arXivId": arxiv_id,
                "DOI": "",
                "paperId": arxiv_id,
                "url": id_url,
                "source": "arxiv",
            })
    except ET.ParseError:
        pass

    return papers


def search_crossref(query, limit=20, offset=0):
    """Search CrossRef for papers (metadata verification).

    Returns list of dicts compatible with other search sources.
    """
    params = {
        "query": query,
        "rows": min(limit, 100),
        "offset": offset,
        "filter": "type:journal-article",
    }
    url = CROSSREF_API_URL + "?" + urllib.parse.urlencode(params)
    data = _make_request(url)
    if not data:
        return []

    try:
        results = json.loads(data)
    except json.JSONDecodeError:
        return []

    papers = []
    for item in results.get("message", {}).get("items", []):
        title_list = item.get("title", [])
        title = title_list[0] if title_list else ""
        author_list = item.get("author", [])
        authors = ", ".join(
            f"{a.get('given', '')} {a.get('family', '')}".strip()
            for a in author_list[:8]
        )
        doi = item.get("DOI", "")
        published = item.get("published-print", {}) or item.get("created", {})
        date_parts = published.get("date-parts", [[0]])[0]
        year = str(date_parts[0]) if date_parts else ""
        venue = item.get("container-title", [""])
        venue = venue[0] if venue else ""

        papers.append({
            "title": title,
            "authors": authors,
            "year": year,
            "venue": venue,
            "abstract": (item.get("abstract") or "")[:500],
            "citationCount": 0,
            "arXivId": "",
            "DOI": doi,
            "paperId": doi,
            "url": f"https://doi.org/{doi}" if doi else "",
            "source": "crossref",
        })
    return papers


def search_dblp(query, limit=20):
    """Search DBLP for CS publications.

    Returns list of dicts compatible with other search sources.
    """
    params = {
        "q": query,
        "h": min(limit, 100),
        "format": "json",
    }
    url = DBLP_API_URL + "?" + urllib.parse.urlencode(params)
    data = _make_request(url)
    if not data:
        return []

    try:
        results = json.loads(data)
    except json.JSONDecodeError:
        return []

    papers = []
    hits = results.get("result", {}).get("hits", {}).get("hit", [])
    if isinstance(hits, dict):
        hits = [hits]
    for hit in hits:
        info = hit.get("info", {})
        authors_info = info.get("authors", {})
        author_list = authors_info.get("author", [])
        if isinstance(author_list, dict):
            author_list = [author_list]
        authors = ", ".join(
            a.get("text", "") if isinstance(a, dict) else str(a)
            for a in author_list[:8]
        )
        venue_info = info.get("venue", "")
        venue = venue_info if isinstance(venue_info, str) else ""

        papers.append({
            "title": info.get("title", ""),
            "authors": authors,
            "year": str(info.get("year", "")),
            "venue": venue,
            "abstract": "",
            "citationCount": 0,
            "arXivId": "",
            "DOI": info.get("doi", ""),
            "paperId": info.get("doi", "") or info.get("url", ""),
            "url": info.get("url", ""),
            "source": "dblp",
        })
    return papers


# ── Post-Processing ─────────────────────────────────────────────────────────────

def _paper_key(paper):
    """Generate a dedup key from title and first author."""
    title = paper.get("title", "").lower().strip().rstrip(".")
    first_author = paper.get("authors", "").split(",")[0].strip().lower() if paper.get("authors") else ""
    return (title, first_author)


def deduplicate(papers_list):
    """Merge results from multiple sources, removing duplicates.

    Prefers results with more complete metadata (DOI + venue present).
    """
    seen = {}
    for paper in papers_list:
        key = _paper_key(paper)
        if key not in seen:
            seen[key] = paper
        else:
            existing = seen[key]
            # Merge: fill in missing fields from new paper
            for field in ["DOI", "arXivId", "venue", "abstract"]:
                if not existing.get(field) and paper.get(field):
                    existing[field] = paper[field]
            # Accumulate sources
            if paper.get("source") and paper["source"] not in existing.get("_sources", ""):
                existing["_sources"] = (existing.get("_sources", "") + "," + paper["source"]).strip(",")
            # Prefer higher citation count
            if paper.get("citationCount", 0) > existing.get("citationCount", 0):
                existing["citationCount"] = paper.get("citationCount", 0)
                existing["year"] = paper.get("year", existing.get("year"))
    return list(seen.values())


def expand_queries(seed_terms):
    """Generate query variants from seed terms."""
    variants = [seed_terms]  # Original query
    terms = seed_terms.split()
    if len(terms) >= 2:
        # Broad variant: first 2-3 terms
        variants.append(" ".join(terms[:3]))
        # Method-focused: add "deep learning" or "neural"
        variants.append(f"{seed_terms} deep learning")
        variants.append(f"{seed_terms} transformer")
        # Recent: add year
        variants.append(f"{seed_terms} 2024 2025")
    return list(set(variants))  # dedup


# ── Output Formatting ────────────────────────────────────────────────────────────

def format_markdown(papers, include_abstract=True):
    """Format results as a Markdown table."""
    lines = [
        "| # | Title | Authors | Year | Venue | Citations | Links |",
        "|---|-------|---------|------|-------|-----------|-------|",
    ]
    for i, p in enumerate(papers, 1):
        links = []
        if p.get("DOI"):
            links.append(f"[DOI](https://doi.org/{p['DOI']})")
        if p.get("arXivId"):
            links.append(f"[arXiv](https://arxiv.org/abs/{p['arXivId']})")
        if p.get("url") and not links:
            links.append(f"[link]({p['url']})")
        link_str = " ".join(links)
        lines.append(
            f"| {i} | {p.get('title', '')[:100]} | {p.get('authors', '')[:60]} "
            f"| {p.get('year', '')} | {p.get('venue', '')[:40]} "
            f"| {p.get('citationCount', 0)} | {link_str} |"
        )
        if include_abstract and p.get("abstract"):
            lines.append(f"| | _Abstract:_ {p['abstract'][:300]}... | | | | | |")
    return "\n".join(lines)


def format_literature_matrix(papers):
    """Format results as a literature matrix compatible with the template."""
    lines = [
        "| Category | Paper | Year | Venue | Main Idea | Relation to Our Work | Use in Paper | Verification |",
        "|---|---:|---|---|---|---|---|",
    ]
    for p in papers:
        verified = "~ single source" if len(p.get("_sources", "").split(",")) < 2 else "✓ confirmed"
        lines.append(
            f"| TBD | {p.get('title', '')[:80]} | {p.get('year', '')} "
            f"| {p.get('venue', '')[:30]} | _(needs reading)_ | TBD | TBD | {verified} |"
        )
    return "\n".join(lines)


def format_bibtex(papers):
    """Generate BibTeX entries for papers."""
    entries = []
    for p in papers:
        key = f"{p.get('authors', 'Unknown').split(',')[0].split()[-1] if p.get('authors') else 'Unknown'}{p.get('year', '0000')}"
        key = "".join(c for c in key if c.isalnum())
        first_author = p.get("authors", "").split(",")[0].strip() if p.get("authors") else ""
        entry = f"""@article{{{key},
  title = {{{{{p.get('title', '')}}}}},
  author = {{{{{first_author} et al.}}}},
  year = {{{{{p.get('year', '')}}}}},
  journal = {{{{{p.get('venue', '')}}}}},
  doi = {{{{{p.get('DOI', '')}}}}},
}}"""
        if p.get("arXivId"):
            entry = entry.replace(
                "},",
                f",\n  eprint = {{{{{p['arXivId']}}}}},\n  archivePrefix = {{arXiv}},"
            )
        entries.append(entry)
    return "\n\n".join(entries)


# ── CLI ─────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Search academic literature across multiple APIs"
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("query", nargs="?", help="Search query string")
    input_group.add_argument("--query-file", help="File with queries (one per line)")

    parser.add_argument("--sources", default="s2,arxiv",
                        help="Sources: s2,arxiv,crossref,dblp,all (default: s2,arxiv)")
    parser.add_argument("--max", dest="max_results", type=int, default=20,
                        help="Max results per source (default: 20)")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--format", dest="fmt", default="markdown",
                        choices=["markdown", "matrix", "bibtex"],
                        help="Output format (default: markdown)")
    parser.add_argument("--no-expand", action="store_true",
                        help="Disable query expansion")
    parser.add_argument("--no-abstract", action="store_true",
                        help="Omit abstracts from markdown output")

    args = parser.parse_args()

    # Determine queries
    if args.query_file:
        with open(args.query_file, "r", encoding="utf-8") as f:
            queries = [line.strip() for line in f if line.strip()]
    else:
        queries = [args.query]

    # Expand queries
    if not args.no_expand:
        expanded = []
        for q in queries:
            expanded.extend(expand_queries(q))
        queries = list(set(expanded))

    # Determine sources
    if args.sources == "all":
        sources = ["s2", "arxiv", "crossref", "dblp"]
    else:
        sources = [s.strip() for s in args.sources.split(",")]

    SOURCE_MAP = {
        "s2": search_semantic_scholar,
        "arxiv": search_arxiv,
        "crossref": search_crossref,
        "dblp": search_dblp,
    }

    all_papers = []
    for query in queries[:8]:  # Cap queries to avoid excessive API calls
        for src in sources:
            if src not in SOURCE_MAP:
                continue
            print(f"Searching {src}: {query[:80]}...", file=sys.stderr)
            papers = SOURCE_MAP[src](query, limit=args.max_results // len(sources) + 1)
            all_papers.extend(papers)
            time.sleep(0.5)  # Be polite to APIs

    # Deduplicate
    papers = deduplicate(all_papers)
    # Sort by citation count (descending)
    papers.sort(key=lambda p: p.get("citationCount", 0), reverse=True)
    papers = papers[:args.max_results]

    # Format output
    formatters = {
        "markdown": lambda ps: format_markdown(ps, include_abstract=not args.no_abstract),
        "matrix": format_literature_matrix,
        "bibtex": format_bibtex,
    }
    output = formatters[args.fmt](papers)

    # Write output
    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(f"# Literature Search Results\n\n")
            f.write(f"**Query:** {args.query or 'from file'}\n")
            f.write(f"**Sources:** {', '.join(sources)}\n")
            f.write(f"**Results:** {len(papers)} papers (deduplicated)\n\n")
            f.write(output)
        print(f"Saved {len(papers)} results to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
