#!/usr/bin/env python3
"""Auto-fill the literature matrix from search results using AI analysis.

Usage:
    # Generate a structured prompt for manual AI processing
    python auto_fill_matrix.py search_results.md --project-brief project_brief.md \\
        --output matrix_prompt.md

    # Direct fill using Anthropic SDK (if available)
    python auto_fill_matrix.py search_results.md --project-brief project_brief.md \\
        --auto --output literature_matrix.md

    # Batch process with your own API key
    python auto_fill_matrix.py search_results.md --project-brief project_brief.md \\
        --auto --api-key $ANTHROPIC_API_KEY --output literature_matrix.md

Workflow:
    1. search_literature.py → search_results.md (paper list with titles+abstracts)
    2. Stage 1 DIGEST → project_brief.md (research task, method, contributions)
    3. auto_fill_matrix.py → pre-filled literature matrix (Category + Main Idea +
       Relation to Our Work + Use in Paper all auto-populated)
    4. Human reviews and adjusts the matrix
    5. verify_citations.py → verify metadata
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


# ── Paper Extraction ──────────────────────────────────────────────────────────────


def extract_papers_from_search_results(md_text):
    """Extract paper entries from search_literature.py or literature matrix markdown.

    Handles two formats:
    1. search_literature.py output: | # | Title | Authors | Year | Venue | Citations | Links |
    2. Literature matrix:          | Category | Paper | Year | Venue | Main Idea | Relation | Use | Verification |
    """
    papers = []
    in_table = False
    is_search_format = None  # None=unknown, True=search output, False=literature matrix

    for line in md_text.split("\n"):
        line = line.strip()
        if not line:
            continue

        # Detect table format from header
        if "| # | Title |" in line or "| # | Title" in line:
            in_table = True
            is_search_format = True
            continue
        if "| Category | Paper |" in line or "| Category | Paper" in line:
            in_table = True
            is_search_format = False
            continue
        if in_table and line.startswith("|---"):
            continue

        if in_table and line.startswith("|") and not line.startswith("| |") and not line.startswith("| _"):
            cells = [c.strip() for c in line.split("|")[1:-1]]

            if is_search_format and len(cells) >= 6:
                papers.append({
                    "num": str(len(papers) + 1),
                    "title": cells[1] if len(cells) > 1 else "",
                    "authors": cells[2] if len(cells) > 2 else "",
                    "year": cells[3] if len(cells) > 3 else "",
                    "venue": cells[4] if len(cells) > 4 else "",
                    "citations": cells[5] if len(cells) > 5 else "",
                    "links": cells[6] if len(cells) > 6 else "",
                    "abstract": "",
                    "category": "",
                    "main_idea": "",
                    "relation": "",
                    "use_in_paper": "",
                    "verification": "",
                    "prefilled": False,
                })
            elif not is_search_format and len(cells) >= 4:
                papers.append({
                    "num": str(len(papers) + 1),
                    "title": cells[1] if len(cells) > 1 else "",
                    "authors": "",
                    "year": cells[2] if len(cells) > 2 else "",
                    "venue": cells[3] if len(cells) > 3 else "",
                    "citations": "",
                    "links": "",
                    "abstract": "",
                    "category": cells[0] if len(cells) > 0 else "",
                    "main_idea": cells[4] if len(cells) > 4 else "",
                    "relation": cells[5] if len(cells) > 5 else "",
                    "use_in_paper": cells[6] if len(cells) > 6 else "",
                    "verification": cells[7] if len(cells) > 7 else "",
                    "prefilled": True,
                })
            continue

        # Abstract continuation line (search format only)
        if in_table and is_search_format and line.startswith("| | _Abstract:_"):
            abstract_text = line.replace("| | _Abstract:_", "").strip().rstrip("|").strip()
            if papers:
                papers[-1]["abstract"] = abstract_text
            continue

        if in_table and not line.startswith("|"):
            in_table = False
            is_search_format = None

    return papers


def extract_project_brief(md_text):
    """Extract key information from Stage 1 project brief."""
    info = {
        "task": "",
        "method_name": "",
        "method_family": "",
        "datasets": "",
        "contributions": [],
        "novel_modules": [],
        "baselines": [],
    }

    # Try to find structured fields
    patterns = {
        "task": [r'## Research Task\s*\n(.*?)(?=\n##|\n\Z)',
                  r'research task[：:]\s*(.*?)(?=\n)'],
        "method_name": [r'method[：:]\s*[\*"]*(.*?)[\*"]*(?=\n)',
                         r'proposed?[：:]\s*[\*"]*(.*?)[\*"]*(?=\n)'],
    }

    for field, pats in patterns.items():
        for pat in pats:
            m = re.search(pat, md_text, re.IGNORECASE | re.DOTALL)
            if m:
                info[field] = m.group(1).strip()[:200]
                break

    # Extract contributions (numbered list items after "贡献" or "Contribution")
    contrib_section = re.search(
        r'(?:贡献|Contribution|candidate contributions?)[\s\S]*?((?:\n[-*\d.]+\s+.+)+)',
        md_text, re.IGNORECASE
    )
    if contrib_section:
        items = re.findall(r'[-*\d.]+\s+(.+?)(?=\n[-*\d.]|\n\n|\Z)', contrib_section.group(1))
        info["contributions"] = [item.strip()[:150] for item in items[:6]]

    # Extract module names
    module_col = re.findall(r'\|\s*(?:III-[A-Z]|Section\s*\d)\s*\|\s*(.+?)\s*\|', md_text)
    if module_col:
        info["novel_modules"] = [m.strip()[:80] for m in module_col if m.strip()]

    # Extract baselines
    baseline_section = re.search(
        r'(?:baselines?|Baselines?)[：:]\s*(.*?)(?=\n\n|\Z)',
        md_text, re.IGNORECASE | re.DOTALL
    )
    if baseline_section:
        info["baselines"] = [b.strip() for b in re.split(r'[,;，；]', baseline_section.group(1)) if b.strip()]

    return info


# ── Prompt Construction ────────────────────────────────────────────────────────────


RELATION_TYPES = [
    "direct competitor — same task + same method family; needs detailed comparison in Related Work and Experiments",
    "method inspiration — different task but similar technique; cite in Related Work as prior art for the technique",
    "baseline comparison — standard method for this task; use as experimental baseline in Table 1",
    "dataset source — paper that introduced a dataset we use; cite when describing the dataset",
    "gap evidence — paper that demonstrates or acknowledges a limitation we address; cite in Introduction para 3",
    "foundational — classic/benchmark paper that defined the task or method paradigm",
    "peripheral — tangentially related; cite only if needed for context",
]

SECTION_USES = [
    "Introduction para 2 — representative method in the 'current progress' paragraph",
    "Introduction para 3 — evidence for the remaining gap",
    "Related Work theme A — [method family A]",
    "Related Work theme B — [method family B]",
    "Related Work theme C — [gap evidence / contrasting approach]",
    "Experiments Table 1 — SOTA baseline for main comparison",
    "Experiments ablation baseline — simplified version for ablation",
    "Dataset description in Experiments Section IV-A",
    "Method Section III-B — component inspiration citation",
]


def build_matrix_prompt(papers, project_info):
    """Build a structured prompt for AI-assisted literature matrix filling."""
    papers_json = []
    has_prefilled = any(p.get("prefilled") for p in papers)

    for p in papers:
        entry = {
            "id": p["num"],
            "title": p["title"],
            "authors": p["authors"][:100],
            "year": p["year"],
            "venue": p["venue"],
            "abstract": p.get("abstract", "")[:500],
        }
        if has_prefilled:
            entry["current_category"] = p.get("category", "")
            entry["current_main_idea"] = p.get("main_idea", "")[:200]
            entry["current_relation"] = p.get("relation", "")
            entry["current_use"] = p.get("use_in_paper", "")
        papers_json.append(entry)

    task_desc = project_info.get("task", "[TASK DESCRIPTION]")
    method_name = project_info.get("method_name", "[METHOD NAME]")
    contributions = project_info.get("contributions", [])
    modules = project_info.get("novel_modules", [])
    baselines = project_info.get("baselines", [])

    mode_note = ""
    if has_prefilled:
        mode_note = (
            "\n> ⚠ **REVIEW MODE**: These papers are from an existing literature matrix with pre-filled columns. "
            "Review each entry for accuracy. If the existing classification is correct, keep it. "
            "If incorrect, provide the corrected version and mark Confidence as 'Corrected'.\n"
        )

    prompt = f"""# Literature Matrix {'Review & Fill' if has_prefilled else 'Auto-Fill'} Task
{mode_note}
## Research Context

**Task:** {task_desc}
**Proposed Method:** {method_name}
**Key Contributions:**
{chr(10).join(f"- {c}" for c in contributions) if contributions else "- [extract from project brief]"}
**Novel Modules:** {', '.join(modules) if modules else '[extract from project brief]'}
**Baselines:** {', '.join(baselines) if baselines else '[extract from project brief]'}

## Papers to {'Review' if has_prefilled else 'Classify'}

{json.dumps(papers_json, indent=2, ensure_ascii=False)}

## Instructions

For EACH paper above, read the title and abstract{', then REVIEW the existing classification' if has_prefilled else ', then fill these 4 columns'}:

### 1. Category
Classify into one of:
- Method-family: same technical approach
- Task-specific: same research task
- Dataset/Benchmark: introduced a dataset we use
- Survey/Review: overview paper
- Theory/Analysis: theoretical contribution
- Application: applied similar method to different domain

### 2. Main Idea (1-2 sentences)
Summarize: what they did + how they did it + key finding.
Be specific. Do NOT copy the abstract verbatim.

### 3. Relation to Our Work
Choose the BEST FIT from:
{chr(10).join(f"- {r}" for r in RELATION_TYPES)}

### 4. Use in Paper
Choose where this paper belongs:
{chr(10).join(f"- {s}" for s in SECTION_USES)}

## Output Format

Return a Markdown table:

| # | Paper | Year | Category | Main Idea | Relation to Our Work | Use in Paper | Confidence |
|---|-------|------|----------|-----------|---------------------|--------------|------------|
| 1 | Title | YYYY | Category | One-sentence summary | Relation type | Section/use | High/Medium/Low |

Confidence levels:
- **High**: Abstract clearly describes task+method; classification is unambiguous
- **Medium**: Abstract provides partial information; reasonable inference
- **Low**: Abstract is vague or the paper seems tangential

## Rules

1. NEVER fabricate information not in the title/abstract.
2. If the abstract is empty, mark Main Idea as "[NEEDS READING]" and Confidence as "Low".
3. A paper CANNOT be both "direct competitor" AND "baseline comparison" — choose the primary relation.
4. If uncertain about Relation, default to "TBD — needs reading".
5. Every paper must have a suggested Use in Paper — this determines where it appears in the manuscript.
6. For papers with High confidence, the Main Idea should be a self-contained summary a reader can understand without seeing the original abstract.

## Example Output

| # | Paper | Year | Category | Main Idea | Relation to Our Work | Use in Paper | Confidence |
|---|-------|------|----------|-----------|---------------------|--------------|------------|
| 1 | CLIP: Learning Transferable Visual Models... | 2021 | Method-family | Contrastive pretraining on 400M image-text pairs; zero-shot transfer to 30+ vision tasks without task-specific fine-tuning. | Foundational — defined the contrastive VL pretraining paradigm | Introduction para 2 — representative global-alignment method | High |
| 2 | Fine-Grained Image-Text Matching via Cross-Modal... | 2023 | Task-specific | Cross-attention between image regions and text tokens with adaptive pooling for fine-grained retrieval. | Direct competitor — same task (text-to-image retrieval), similar technique (cross-modal attention) | Related Work theme A + Experiments Table 1 baseline | High |
| 3 | Why Existing Retrieval Models Fail on Compositional Queries | 2024 | Analysis | Systematic study showing that global-alignment models achieve <40% R@1 on queries with novel attribute-object compositions. | Gap evidence — demonstrates the limitation we address (query-dependent region importance) | Introduction para 3 | Medium |

Now process all {len(papers_json)} papers above and output the filled matrix table.
"""
    return prompt


# ── Anthropic API Automation ───────────────────────────────────────────────────────


def auto_fill_with_anthropic(papers, project_info, api_key, model="claude-haiku-4-5-20251001"):
    """Use Anthropic API to auto-fill the literature matrix."""
    try:
        import anthropic
    except ImportError:
        print("Install anthropic SDK: pip install anthropic", file=sys.stderr)
        return None

    prompt = build_matrix_prompt(papers, project_info)

    client = anthropic.Anthropic(api_key=api_key)

    # Split into batches of 15 papers to avoid context overflow
    BATCH_SIZE = 15
    all_results = []

    for batch_start in range(0, len(papers), BATCH_SIZE):
        batch_papers = papers[batch_start:batch_start + BATCH_SIZE]
        batch_info = dict(project_info)
        batch_prompt = build_matrix_prompt(batch_papers, batch_info)

        if batch_start > 0:
            print(f"Processing batch {batch_start // BATCH_SIZE + 1}...", file=sys.stderr)

        try:
            resp = client.messages.create(
                model=model,
                max_tokens=4096,
                temperature=0.0,
                system="You are a research assistant filling a literature matrix. "
                       "Be precise, honest, and conservative. Never fabricate information. "
                       "If uncertain, mark as 'TBD — needs reading'. "
                       "Return ONLY the Markdown table, no preamble or commentary.",
                messages=[{"role": "user", "content": batch_prompt}],
            )
            all_results.append(resp.content[0].text)
        except Exception as e:
            print(f"API error on batch {batch_start}: {e}", file=sys.stderr)
            all_results.append(f"<!-- Batch {batch_start} failed: {e} -->")

    return "\n\n".join(all_results)


# ── Output Formatting ──────────────────────────────────────────────────────────────


def build_matrix_markdown(papers, project_info):
    """Build a pre-structured matrix for manual or AI filling."""
    lines = [
        "# Literature Matrix",
        "",
        f"**Research Task:** {project_info.get('task', 'TBD')}",
        f"**Proposed Method:** {project_info.get('method_name', 'TBD')}",
        "",
        "## Search Queries Used",
        "",
        "| # | Query | Source | Results |",
        "|---|-------|--------|---------|",
        "| 1 | [INSERT QUERY] | s2 | [INSERT COUNT] |",
        "",
        "## Instructions",
        "",
        "Fill the matrix below. For each paper, read the title and abstract, then fill:",
        "- **Category**: Method-family / Task-specific / Dataset / Survey / Theory / Application",
        "- **Main Idea**: 1-2 sentence summary of what they did and found",
        f"- **Relation to Our Work**: {' / '.join(r.split(' — ')[0] for r in RELATION_TYPES)}",
        f"- **Use in Paper**: which section and why",
        "- **Verification**: leave as '~ pending' until verify_citations.py is run",
        "",
        "## Literature Matrix",
        "",
        "| # | Paper | Year | Venue | Category | Main Idea | Relation to Our Work | Use in Paper | Verification |",
        "|---|-------|------|-------|----------|-----------|---------------------|--------------|--------------|",
    ]

    has_prefilled = any(p.get("prefilled") for p in papers)

    for p in papers:
        if has_prefilled:
            lines.append(
                f"| {p['num']} | {p['title'][:100]} | {p['year']} | {p['venue'][:30]} | "
                f"{p.get('category', 'TBD')} | {p.get('main_idea', 'TBD')[:150]} | "
                f"{p.get('relation', 'TBD')[:60]} | {p.get('use_in_paper', 'TBD')[:50]} | "
                f"{p.get('verification', '~ pending')} |"
            )
        else:
            abstract_snippet = p.get("abstract", "")[:80]
            lines.append(
                f"| {p['num']} | {p['title'][:100]} | {p['year']} | {p['venue'][:30]} | "
                f"TBD | _(from abstract: {abstract_snippet}...)_ | TBD | TBD | ~ pending |"
            )

    return "\n".join(lines)


# ── Confidence Scoring ─────────────────────────────────────────────────────────────


def analyze_matrix_completeness(matrix_text):
    """Check how complete an auto-filled matrix is."""
    issues = []

    tbd_count = len(re.findall(r'\bTBD\b', matrix_text))
    needs_reading = len(re.findall(r'NEEDS READING', matrix_text))
    pending = len(re.findall(r'~ pending', matrix_text))
    total_rows = len(re.findall(r'^\|\s*\d+\s*\|', matrix_text, re.MULTILINE))

    if tbd_count > total_rows * 2:
        issues.append(f"[!!] {tbd_count} TBD cells — matrix needs substantial manual review")
    elif tbd_count > 5:
        issues.append(f"[!] {tbd_count} TBD cells — manual review recommended")
    else:
        issues.append(f"[.] {tbd_count} TBD cells — minor manual touch-up needed")

    if needs_reading > 0:
        issues.append(f"[!] {needs_reading} papers marked 'NEEDS READING' — manually read and update")

    issues.append(f"[i] {total_rows} papers in matrix, {pending} pending verification")

    return issues


# ── CLI ────────────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Auto-fill the literature matrix from search results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a prompt for manual AI processing (provider-agnostic)
  python auto_fill_matrix.py search_results.md --project-brief project_brief.md \\
      --output matrix_prompt.md

  # Generate a pre-structured matrix template
  python auto_fill_matrix.py search_results.md --template-only --output matrix_template.md

  # Auto-fill using Anthropic API
  python auto_fill_matrix.py search_results.md --project-brief project_brief.md \\
      --auto --api-key $ANTHROPIC_API_KEY --output literature_matrix.md

  # Auto-fill with a specific model
  python auto_fill_matrix.py search_results.md --project-brief project_brief.md \\
      --auto --model claude-sonnet-4-6 --output literature_matrix.md

  # From JSON paper list
  python auto_fill_matrix.py papers.json --format json --project-brief brief.md \\
      --auto --api-key $ANTHROPIC_API_KEY --output matrix.md
        """,
    )
    parser.add_argument("search_results", help="Search results file (.md from search_literature.py or .json)")
    parser.add_argument("--format", default="auto", choices=["auto", "markdown", "json"],
                        help="Input format (default: auto-detect)")
    parser.add_argument("--project-brief", help="Stage 1 project brief (for context)")
    parser.add_argument("--output", "-o", default="literature_matrix.md", help="Output file path")
    parser.add_argument("--auto", action="store_true", help="Auto-fill using Anthropic API")
    parser.add_argument("--api-key", help="Anthropic API key (or set ANTHROPIC_API_KEY env var)")
    parser.add_argument("--model", default="claude-haiku-4-5-20251001",
                        help="Model for auto-fill (default: claude-haiku-4-5)")
    parser.add_argument("--template-only", action="store_true",
                        help="Only generate empty matrix template (no AI prompt)")
    parser.add_argument("--prompt-only", action="store_true",
                        help="Generate the fill prompt without calling any API")
    args = parser.parse_args()

    input_text = Path(args.search_results).read_text(encoding="utf-8", errors="replace")

    # Parse input
    if args.format == "json" or args.search_results.endswith(".json"):
        try:
            papers_data = json.loads(input_text)
            papers = papers_data if isinstance(papers_data, list) else papers_data.get("papers", [])
        except json.JSONDecodeError:
            print("Invalid JSON.", file=sys.stderr)
            sys.exit(1)
    else:
        papers = extract_papers_from_search_results(input_text)

    if not papers:
        print("No papers found in search results. Check input format.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(papers)} papers in search results.", file=sys.stderr)

    # Load project brief
    project_info = {}
    if args.project_brief and Path(args.project_brief).exists():
        brief_text = Path(args.project_brief).read_text(encoding="utf-8", errors="replace")
        project_info = extract_project_brief(brief_text)
        print(f"Loaded project brief: task='{project_info.get('task', 'N/A')[:60]}...'", file=sys.stderr)

    # Mode selection
    if args.template_only:
        output = build_matrix_markdown(papers, project_info)
    elif args.prompt_only:
        output = build_matrix_prompt(papers, project_info)
    elif args.auto:
        api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("Error: --api-key required for --auto mode (or set ANTHROPIC_API_KEY env var)", file=sys.stderr)
            print("Fallback: generating prompt instead. Use --prompt-only to generate a prompt for manual AI processing.", file=sys.stderr)
            output = build_matrix_prompt(papers, project_info)
            args.output = args.output.replace(".md", "_prompt.md")
        else:
            print(f"Auto-filling matrix with {args.model}...", file=sys.stderr)
            result = auto_fill_with_anthropic(papers, project_info, api_key, args.model)
            if result:
                # Prepend header, append completeness check
                header = f"""# Literature Matrix (Auto-Filled)

**Research Task:** {project_info.get('task', 'TBD')}
**Proposed Method:** {project_info.get('method_name', 'TBD')}
**Auto-filled by:** {args.model}
**Papers analyzed:** {len(papers)}

> ⚠ **Review required.** This matrix was auto-generated. Verify all entries before using in your manuscript.
> Flag any incorrect classifications and update 'TBD' entries.

## Search Queries Used

| # | Query | Source | Results |
|---|-------|--------|---------|
| 1 | [INSERT QUERY] | s2,arxiv | {len(papers)} |

"""
                completeness = analyze_matrix_completeness(result)
                check_section = "\n## Auto-Fill Completeness Check\n\n" + "\n".join(f"- {c}" for c in completeness)
                output = header + result + "\n" + check_section
            else:
                output = build_matrix_prompt(papers, project_info)
                print("API fill failed. Generated prompt for manual processing instead.", file=sys.stderr)
    else:
        # Default: generate both prompt and template
        prompt = build_matrix_prompt(papers, project_info)
        template = build_matrix_markdown(papers, project_info)
        output = (
            "# Literature Matrix — Auto-Fill Package\n\n"
            "This file contains TWO sections:\n"
            "1. An AI processing prompt (copy into any AI agent to auto-fill)\n"
            "2. An empty matrix template (fill manually or after AI processing)\n\n"
            "---\n\n"
            + template
            + "\n\n---\n\n# AI Fill Prompt\n\n"
            + prompt
        )

    Path(args.output).write_text(output, encoding="utf-8")
    file_size = Path(args.output).stat().st_size
    print(f"Saved to {args.output} ({file_size:,} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
