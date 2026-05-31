#!/usr/bin/env python3
"""Analyze citation networks, identify research gaps, and visualize trends.

Usage:
    # From a literature matrix markdown file
    python analyze_citations.py lit_matrix.md --output gap_analysis.md

    # From a BibTeX file
    python analyze_citations.py references.bib --format bibtex --output analysis.md

    # From a JSON paper list
    python analyze_citations.py papers.json --format json --output analysis.md

Features:
    - Temporal trend analysis (publications per year, topic shifts)
    - Venue distribution analysis
    - Research gap identification from literature matrix
    - Method-family clustering
    - Citation density heatmap data generation
    - Recommended missing citations detection
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


# ── Parsers ────────────────────────────────────────────────────────────────────────

def parse_literature_matrix(md_text):
    """Parse a literature matrix markdown table.

    Expected format from SKILL.md Stage 2 output:
    | Category | Paper | Year | Venue | Main Idea | Relation to Our Work | Use in Paper | Verification |
    """
    papers = []
    in_table = False
    headers = []

    for line in md_text.split("\n"):
        line = line.strip()
        if not line:
            continue

        # Detect table start
        if line.startswith("| Category") or line.startswith("| Paper"):
            in_table = True
            headers = [h.strip() for h in line.split("|")[1:-1]]
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table and line.startswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) < 3:
                continue
            paper = {}
            for i, header in enumerate(headers):
                if i < len(cells):
                    paper[header.lower().replace(" ", "_")] = cells[i]
            if paper.get("paper") or paper.get("title"):
                papers.append(paper)

    return papers


def parse_bibtex(bib_text):
    """Parse BibTeX entries."""
    papers = []
    # Find all @article{...} or @inproceedings{...} entries
    entries = re.findall(r'@(\w+)\{([^,]*),\s*(.*?)\}\s*(?=@|\Z)', bib_text, re.DOTALL)

    for entry_type, key, fields_str in entries:
        paper = {"type": entry_type, "key": key.strip()}

        # Extract fields
        for field_match in re.finditer(r'(\w+)\s*=\s*[\{"]((?:[^"{}]|\{[^{}]*\})*?)[\}"]', fields_str):
            field_name = field_match.group(1).lower()
            field_value = field_match.group(2).strip()
            paper[field_name] = field_value

        papers.append(paper)

    return papers


def parse_json_papers(json_text):
    """Parse a JSON paper list."""
    data = json.loads(json_text)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("papers", data.get("data", []))
    return []


# ── Analysis Functions ─────────────────────────────────────────────────────────────

def analyze_temporal_trends(papers):
    """Analyze publication year distribution."""
    years = []
    for p in papers:
        year_str = str(p.get("year", "")).strip()
        if year_str:
            m = re.search(r'(\d{4})', year_str)
            if m:
                years.append(int(m.group(1)))

    if not years:
        return {"trend": "No year data available", "years": []}

    year_counts = Counter(years)
    sorted_years = sorted(year_counts.items())

    # Detect trend direction
    if len(sorted_years) >= 3:
        recent = [c for y, c in sorted_years[-3:]]
        older = [c for y, c in sorted_years[:3]]
        recent_avg = sum(recent) / len(recent)
        older_avg = sum(older) / len(older) if older else recent_avg
        if recent_avg > older_avg * 1.5:
            trend = "increasing (growing research interest)"
        elif recent_avg < older_avg * 0.67:
            trend = "decreasing (maturing area)"
        else:
            trend = "stable"
    else:
        trend = "insufficient data for trend"

    return {
        "n_papers_with_year": len(years),
        "year_range": f"{sorted_years[0][0]}-{sorted_years[-1][0]}" if sorted_years else "N/A",
        "years": dict(sorted_years),
        "peak_year": f"{sorted_years[-1][0]} ({sorted_years[-1][1]} papers)" if sorted_years else "N/A",
        "trend": trend,
    }


def analyze_venues(papers):
    """Analyze venue distribution."""
    venues = []
    for p in papers:
        venue = p.get("venue", p.get("journal", p.get("booktitle", ""))).strip()
        if venue:
            venues.append(venue)

    venue_counts = Counter(venues)
    top_venues = venue_counts.most_common(10)

    venue_tiers = {
        "CVPR": "Top CV",
        "ICCV": "Top CV",
        "ECCV": "Top CV",
        "NeurIPS": "Top ML",
        "ICML": "Top ML",
        "ICLR": "Top ML",
        "ACL": "Top NLP",
        "EMNLP": "Top NLP",
        "NAACL": "Top NLP",
        "AAAI": "Top AI",
        "IJCAI": "Top AI",
        "TPAMI": "Top Journal",
        "IJCV": "Top Journal",
        "TIP": "Top Journal",
        "TNNLS": "Top Journal",
        "JMLR": "Top Journal",
        "arXiv": "Preprint",
    }

    venue_tier_counts = defaultdict(int)
    for v, c in venue_counts.items():
        tier = "Other"
        for key, t in venue_tiers.items():
            if key.lower() in v.lower():
                tier = t
                break
        venue_tier_counts[tier] += c

    return {
        "n_venues": len(venues),
        "top_venues": [{"venue": v, "count": c} for v, c in top_venues],
        "tier_distribution": dict(venue_tier_counts),
    }


def analyze_method_families(papers):
    """Cluster papers by method family based on keywords in title/abstract."""
    method_keywords = {
        "Contrastive Learning": ["contrastive", "infoNCE", "simclr", "moco"],
        "Transformer/ViT": ["transformer", "vit", "attention", "self-attention"],
        "CNN-based": ["convolution", "cnn", "resnet", "residual"],
        "Diffusion Models": ["diffusion", "ddpm", "denoising"],
        "GAN": ["gan", "generative adversarial", "adversarial network"],
        "Graph Neural Networks": ["graph neural", "gnn", "graph convolution", "message passing"],
        "Reinforcement Learning": ["reinforcement", "rl", "policy gradient", "dqn", "ppo"],
        "LoRA/PEFT": ["lora", "adapter", "peft", "parameter-efficient"],
        "Retrieval-Augmented": ["rag", "retrieval augmented", "retrieval-augmented"],
        "Multimodal": ["multimodal", "cross-modal", "vision-language", "text-image"],
        "Self-Supervised": ["self-supervised", "ssl", "pretext", "pre-training"],
        "Knowledge Distillation": ["distillation", "knowledge distillation", "teacher", "student"],
        "Mixture of Experts": ["mixture of experts", "moe", "sparse gating", "routing"],
        "State Space Models": ["mamba", "state space", "ssm", "s4"],
    }

    method_counts = defaultdict(int)
    for p in papers:
        text = (p.get("title", "") + " " + p.get("abstract", "") +
                p.get("main_idea", "") + " " + p.get("notes", "")).lower()
        for family, keywords in method_keywords.items():
            if any(kw in text for kw in keywords):
                method_counts[family] += 1

    return dict(Counter(method_counts).most_common())


def identify_gaps(papers, method_name="the proposed method"):
    """Identify potential research gaps from literature matrix.

    Analyzes the "Relation to Our Work" and "Main Idea" columns to find:
    1. Areas with few papers (underexplored)
    2. Consistent limitations mentioned across papers
    3. Missing method-family comparisons
    """
    gaps = []
    relation_counts = defaultdict(int)
    limitations = []

    for p in papers:
        relation = p.get("relation_to_our_work", p.get("relation", "")).lower()
        relation_counts[relation] += 1

        # Extract limitation keywords from main idea / notes
        idea = (p.get("main_idea", "") + " " + p.get("notes", "")).lower()
        for kw in ["limitation", "however", "but", "struggle", "fail", "cannot",
                    "lack", "missing", "insufficient", "limited", "challenge",
                    "假设", "局限", "但", "然而", "不足"]:
            if kw in idea:
                limitations.append({"paper": p.get("paper", p.get("title", "")), "keyword": kw})

    # Gap 1: Underexplored method families
    gap_methods = [r for r, c in relation_counts.items() if "gap" in r or "limitation" in r]
    if gap_methods:
        gaps.append({
            "type": "explicit_gap_evidence",
            "description": f"Papers explicitly identified as 'gap evidence': {', '.join(gap_methods)}",
            "n_papers": sum(relation_counts[g] for g in gap_methods),
        })

    # Gap 2: Sparse categories
    sparse = [r for r, c in relation_counts.items() if c <= 1 and r.strip()]
    if sparse:
        gaps.append({
            "type": "sparse_coverage",
            "description": f"Categories with only one paper: {', '.join(sparse)}",
        })

    # Gap 3: Missing relation types
    expected_relations = {"direct competitor", "method inspiration", "baseline comparison",
                          "dataset source", "gap evidence"}
    found_relations = set(relation_counts.keys())
    missing_relations = expected_relations - found_relations
    if missing_relations:
        gaps.append({
            "type": "missing_coverage",
            "description": f"Recommended relation types not found in matrix: {', '.join(missing_relations)}",
        })

    if limitations:
        top_limitations = Counter(l["keyword"] for l in limitations).most_common(5)
        gaps.append({
            "type": "common_limitations",
            "description": "Most frequent limitation indicators across papers",
            "details": [{"keyword": k, "count": c} for k, c in top_limitations],
        })

    return gaps


def analyze_citation_density(papers):
    """Analyze citation density and coverage."""
    n_papers = len(papers)
    if n_papers == 0:
        return {"density": "No papers"}

    # Distribution by relation type
    relation_dist = Counter(
        p.get("relation_to_our_work", p.get("relation", "unspecified")).strip()
        for p in papers
    )

    # Verification status
    verification_dist = Counter(
        "verified" if "✓" in p.get("verification", "") else
        "partial" if "~" in p.get("verification", "") else
        "unverified" if "✗" in p.get("verification", "") or "needed" in p.get("verification", "").lower() else
        "unspecified"
        for p in papers
    )

    # Category coverage
    categories = Counter(
        p.get("category", p.get("use_in_paper", "unspecified")).strip()
        for p in papers
    )

    return {
        "n_total": n_papers,
        "relation_distribution": dict(relation_dist),
        "verification_status": dict(verification_dist),
        "n_verified": verification_dist.get("verified", 0),
        "n_unverified": verification_dist.get("unverified", 0),
        "category_coverage": dict(categories),
    }


def suggest_missing_citations(papers, knowledge_base=None):
    """Suggest potentially missing citations based on gap patterns.

    knowledge_base: optional dict of classic papers by area (from classic-papers.md)
    """
    suggestions = []

    # Check method families covered
    method_families = analyze_method_families(papers)

    # Common gaps: if no paper from a key method family
    key_families = {"Transformer/ViT", "Contrastive Learning", "CNN-based"}
    covered_families = set(method_families.keys())
    missing_families = key_families - covered_families
    if missing_families:
        suggestions.append({
            "type": "missing_family",
            "message": f"No papers from method families: {', '.join(missing_families)}. Consider adding foundational papers from these families.",
        })

    # Verification concerns
    unverified = [p for p in papers if "✗" in p.get("verification", "") or "needed" in p.get("verification", "").lower()]
    if unverified:
        suggestions.append({
            "type": "unverified_citations",
            "message": f"{len(unverified)} papers have unverified citations. Verify with crossref/dblp.",
            "papers": [p.get("paper", p.get("title", ""))[:80] for p in unverified[:5]],
        })

    # Year coverage
    years = []
    for p in papers:
        y = re.search(r'(\d{4})', str(p.get("year", "")))
        if y:
            years.append(int(y.group(1)))
    if years and max(years) - min(years) < 3:
        suggestions.append({
            "type": "narrow_year_range",
            "message": f"Year range is narrow ({min(years)}-{max(years)}). Consider expanding to older foundational work and very recent preprints.",
        })

    return suggestions


# ── Visualization Data Export ──────────────────────────────────────────────────────

def export_timeline_data(papers, output_path):
    """Export year-count data for timeline visualization."""
    years_data = analyze_temporal_trends(papers)
    with open(output_path, "w") as f:
        json.dump(years_data["years"], f, indent=2)
    print(f"Timeline data → {output_path}", file=sys.stderr)


def export_network_data(papers, output_path):
    """Export citation adjacency data for network visualization."""
    nodes = []
    edges = []
    method_families = analyze_method_families(papers)

    for p in papers:
        title = p.get("paper", p.get("title", "Unknown"))[:60]
        nodes.append({
            "id": title,
            "year": p.get("year", ""),
            "venue": p.get("venue", ""),
            "category": p.get("category", ""),
        })

    # Create edges between papers in same category or year
    for i, p1 in enumerate(papers):
        for j, p2 in enumerate(papers):
            if i >= j:
                continue
            cat1 = p1.get("category", "")
            cat2 = p2.get("category", "")
            if cat1 and cat2 and cat1 == cat2:
                edges.append({"source": i, "target": j, "type": "same_category"})
            year1 = p1.get("year", "")
            year2 = p2.get("year", "")
            if year1 and year2 and year1 == year2:
                edges.append({"source": i, "target": j, "type": "same_year"})

    network = {"nodes": nodes, "edges": edges, "method_families": method_families}
    with open(output_path, "w") as f:
        json.dump(network, f, indent=2)
    print(f"Network data → {output_path} ({len(nodes)} nodes, {len(edges)} edges)", file=sys.stderr)


# ── Main Report ────────────────────────────────────────────────────────────────────

def build_report(papers, args):
    """Build comprehensive gap analysis report."""
    lines = [
        "# Literature Analysis Report",
        "",
        f"**Papers analyzed:** {len(papers)}",
        f"**Method name:** {args.method_name}",
        "",
    ]

    # Citation Density
    density = analyze_citation_density(papers)
    lines.extend([
        "## Citation Density & Coverage",
        "",
        f"**Total papers:** {density['n_total']}",
        f"**Verified citations:** {density['n_verified']} / {density['n_total']}",
        f"**Unverified citations:** {density['n_unverified']} / {density['n_total']}",
        "",
        "### Relation Distribution",
        "",
    ])
    for relation, count in density["relation_distribution"].items():
        bar = "█" * min(count, 20)
        lines.append(f"- {relation}: {count} {bar}")
    lines.append("")
    lines.extend([
        "### Verification Status",
        "",
    ])
    for status, count in density["verification_status"].items():
        lines.append(f"- {status}: {count}")
    lines.append("")

    # Temporal Trends
    trends = analyze_temporal_trends(papers)
    lines.extend([
        "## Temporal Trends",
        "",
        f"**Year range:** {trends.get('year_range', 'N/A')}",
        f"**Trend:** {trends.get('trend', 'N/A')}",
        f"**Peak year:** {trends.get('peak_year', 'N/A')}",
        "",
        "### Publications per Year",
        "",
    ])
    for year, count in sorted(trends.get("years", {}).items()):
        bar = "▓" * min(count, 25)
        lines.append(f"- {year}: {count} {bar}")
    lines.append("")

    # Venue Analysis
    venues = analyze_venues(papers)
    lines.extend([
        "## Venue Distribution",
        "",
    ])
    for item in venues.get("top_venues", [])[:10]:
        lines.append(f"- **{item['venue']}**: {item['count']}")
    lines.append("")
    if venues.get("tier_distribution"):
        lines.extend([
            "### Tier Distribution",
            "",
        ])
        for tier, count in sorted(venues["tier_distribution"].items()):
            lines.append(f"- {tier}: {count}")
        lines.append("")

    # Method Families
    families = analyze_method_families(papers)
    lines.extend([
        "## Method Family Distribution",
        "",
    ])
    for family, count in families.items():
        bar = "█" * min(count, 20)
        lines.append(f"- **{family}**: {count} {bar}")
    lines.append("")

    # Gap Identification
    gaps = identify_gaps(papers, args.method_name)
    lines.extend([
        "## Research Gap Analysis",
        "",
    ])
    if gaps:
        for gap in gaps:
            lines.append(f"### {gap['type'].replace('_', ' ').title()}")
            lines.append(f"{gap['description']}")
            if "details" in gap:
                for d in gap["details"]:
                    lines.append(f"  - {d['keyword']}: {d['count']}")
            if "n_papers" in gap:
                lines.append(f"  _Papers in this category: {gap['n_papers']}_")
            lines.append("")
    else:
        lines.append("No gaps identified — consider expanding the literature matrix with more diverse papers.")
    lines.append("")

    # Missing Citation Suggestions
    suggestions = suggest_missing_citations(papers)
    lines.extend([
        "## Recommended Actions",
        "",
    ])
    if suggestions:
        for s in suggestions:
            icon = {"missing_family": "[!!]", "unverified_citations": "[!]", "narrow_year_range": "[-]"}.get(s["type"], "[.]")
            lines.append(f"- {icon} **{s['type'].replace('_', ' ').title()}**: {s['message']}")
            if "papers" in s:
                for p in s["papers"]:
                    lines.append(f"  - {p}")
    else:
        lines.append("- Literature coverage looks adequate based on automated analysis.")

    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Analyze citations, identify research gaps, and visualize trends",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # From literature matrix (Stage 2 output)
  python analyze_citations.py outputs/02_literature_matrix.md --output gap_analysis.md

  # From BibTeX file with network export
  python analyze_citations.py references.bib --format bibtex --network network.json

  # From JSON paper list
  python analyze_citations.py papers.json --format json --output analysis.md --timeline timeline.json
        """,
    )
    parser.add_argument("input_file", help="Literature matrix (.md), BibTeX (.bib), or JSON file")
    parser.add_argument("--format", "-f", default="auto", choices=["auto", "matrix", "bibtex", "json"],
                        help="Input format (default: auto-detect)")
    parser.add_argument("--output", "-o", default="gap_analysis.md", help="Output report path")
    parser.add_argument("--method-name", default="the proposed method", help="Name of the proposed method for gap analysis")
    parser.add_argument("--network", help="Export citation network data as JSON")
    parser.add_argument("--timeline", help="Export timeline data as JSON")

    args = parser.parse_args()

    input_text = Path(args.input_file).read_text(encoding="utf-8", errors="replace")

    # Auto-detect format
    fmt = args.format
    if fmt == "auto":
        if args.input_file.endswith(".bib"):
            fmt = "bibtex"
        elif args.input_file.endswith(".json"):
            fmt = "json"
        else:
            fmt = "matrix"

    if fmt == "bibtex":
        papers = parse_bibtex(input_text)
    elif fmt == "json":
        papers = parse_json_papers(input_text)
    else:
        papers = parse_literature_matrix(input_text)

    if not papers:
        print(f"Warning: No papers found in {args.input_file}. Check format.", file=sys.stderr)

    # Export data files
    if args.timeline:
        export_timeline_data(papers, args.timeline)
    if args.network:
        export_network_data(papers, args.network)

    # Build and write report
    report = build_report(papers, args)
    Path(args.output).write_text(report, encoding="utf-8")
    print(f"Report saved to {args.output} ({len(papers)} papers)", file=sys.stderr)


if __name__ == "__main__":
    main()
