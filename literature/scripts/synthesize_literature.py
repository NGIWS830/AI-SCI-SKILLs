#!/usr/bin/env python3
"""Synthesize literature matrix into coherent narrative for Introduction + Related Work.

Usage:
    # Generate synthesis prompt for AI processing
    python synthesize_literature.py lit_matrix.md --project-brief brief.md \\
        --output synthesis_prompt.md

    # Auto-synthesize using Anthropic API
    python synthesize_literature.py lit_matrix.md --project-brief brief.md \\
        --auto --api-key $ANTHROPIC_API_KEY --output synthesis.md

    # Generate only the Related Work synthesis
    python synthesize_literature.py lit_matrix.md --project-brief brief.md \\
        --section related_work --output related_work_synthesis.md

What this does:
    1. Reads the filled literature matrix + project brief
    2. Groups papers into narrative themes (NOT just categories)
    3. Identifies the logical arc across themes
    4. Generates structured content for Introduction paras 2-3 and Related Work
    5. Each theme gets: core idea, evolution, tension, gap, transition
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


# ── Paper & Matrix Parsing ────────────────────────────────────────────────────────


def parse_literature_matrix(md_text):
    """Parse a filled literature matrix into structured paper entries.

    Returns list of dicts with keys matching the matrix columns.
    """
    papers = []
    in_table = False
    headers = []

    for line in md_text.split("\n"):
        line = line.strip()
        if not line:
            continue

        # Detect table header
        if re.match(r'^\|\s*(?:Category|Paper|#)\s*\|', line):
            in_table = True
            headers = [h.strip().lower().replace(" ", "_") for h in line.split("|")[1:-1]]
            continue
        if in_table and re.match(r'^\|[\s\-:]+\|', line):
            continue
        if in_table and line.startswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) < 3:
                continue
            paper = {}
            for i, header in enumerate(headers):
                if i < len(cells) and cells[i]:
                    paper[header] = cells[i]
            if paper.get("paper") or paper.get("title") or paper.get("category"):
                papers.append(paper)
            continue
        if in_table and not line.startswith("|"):
            in_table = False

    return papers


def parse_related_work_structure(md_text):
    """Extract the Related Work structure (Theme A, Theme B, ...) from matrix."""
    themes = []
    theme_pattern = re.compile(r'###?\s*Theme\s+(\w+)[：:]\s*(.+?)(?:\((.+?)\))?\s*$', re.IGNORECASE)

    for m in theme_pattern.finditer(md_text):
        letter = m.group(1)
        name = m.group(2).strip()
        papers_str = m.group(3) if m.group(3) else ""
        papers = [p.strip() for p in papers_str.split(",")] if papers_str else []
        themes.append({"id": letter, "name": name, "paper_refs": papers})

    return themes


def parse_project_brief(md_text):
    """Extract key fields from Stage 1 project brief."""
    info = {
        "task": "",
        "problem": "",
        "method_name": "",
        "method_summary": "",
        "datasets": "",
        "contributions": [],
        "gap": "",
    }

    # Task
    for pat in [r'## Research Task\s*\n(.*?)(?=\n##|\n\Z)',
                r'research task[：:]\s*(.*?)(?=\n)',
                r'\*\*Task[：:]\*\*\s*(.*?)(?=\n)']:
        m = re.search(pat, md_text, re.IGNORECASE | re.DOTALL)
        if m:
            info["task"] = m.group(1).strip()[:200]
            break

    # Problem/Motivation
    for pat in [r'## Problem Motivation\s*\n(.*?)(?=\n##|\n\Z)',
                r'problem[：:]\s*(.*?)(?=\n##|\n\n)']:
        m = re.search(pat, md_text, re.IGNORECASE | re.DOTALL)
        if m:
            info["problem"] = m.group(1).strip()[:200]
            break

    # Method name
    for pat in [r'\*\*Proposed method[：:]\*\*\s*(.*?)(?=\n)',
                r'proposed?[：:]\s*(.*?)(?=\n)',
                r'method name[：:]\s*(.*?)(?=\n)']:
        m = re.search(pat, md_text, re.IGNORECASE)
        if m:
            info["method_name"] = m.group(1).strip()[:100]
            break

    # Method summary (from Method Overview section)
    m = re.search(r'## Method Overview\s*\n(.*?)(?=\n##|\n\Z)', md_text, re.DOTALL)
    if m:
        info["method_summary"] = m.group(1).strip()[:300]

    # Gap (from Claims or Missing Information)
    for pat in [r'gap[：:]\s*(.*?)(?=\n)', r'limitation[：:]\s*(.*?)(?=\n)']:
        m = re.search(pat, md_text, re.IGNORECASE)
        if m:
            info["gap"] = m.group(1).strip()[:200]
            break

    # Contributions
    contrib_section = re.search(
        r'(?:贡献|Contribution|candidate contribution)[\s\S]*?((?:\n[-*\d.]+\s+.+)+)',
        md_text, re.IGNORECASE)
    if contrib_section:
        info["contributions"] = re.findall(r'[-*\d.]+\s+(.+?)(?=\n[-*\d.]|\n\n|\Z)',
                                            contrib_section.group(1))

    # Datasets
    m = re.search(r'datasets?[：:]\s*(.*?)(?=\n)', md_text, re.IGNORECASE)
    if m:
        info["datasets"] = m.group(1).strip()

    return info


# ── Theme Builder ─────────────────────────────────────────────────────────────────


def build_themes(papers, project_info):
    """Group papers into narrative themes.

    Goes beyond the simple "Category" column to create argument-driven groups.
    """
    # First pass: group by explicit relation type
    relation_groups = defaultdict(list)
    for p in papers:
        rel = p.get("relation_to_our_work", p.get("relation", "")).lower()
        if "competitor" in rel or "direct" in rel:
            relation_groups["competitors"].append(p)
        elif "inspiration" in rel or "family" in rel:
            relation_groups["method_family"].append(p)
        elif "baseline" in rel:
            relation_groups["baselines"].append(p)
        elif "gap" in rel or "limitation" in rel:
            relation_groups["gap_evidence"].append(p)
        elif "dataset" in rel or "benchmark" in rel:
            relation_groups["datasets"].append(p)
        elif "foundational" in rel or "classic" in rel:
            relation_groups["foundational"].append(p)
        else:
            relation_groups["other"].append(p)

    # Build themes with narrative structure
    themes = []

    # Theme 1: The dominant paradigm (foundational + method_family papers)
    paradigm_papers = relation_groups.get("foundational", []) + relation_groups.get("method_family", [])
    if paradigm_papers:
        themes.append({
            "id": "A",
            "name": _derive_theme_name(paradigm_papers, "Current Paradigms"),
            "type": "current_progress",
            "papers": paradigm_papers,
            "intro_use": "Introduction para 2 — current progress",
            "related_work_role": "Establish the dominant approach and its achievements",
        })

    # Theme 2: Competing approaches (competitors)
    competitor_papers = relation_groups.get("competitors", [])
    if competitor_papers:
        themes.append({
            "id": "B",
            "name": _derive_theme_name(competitor_papers, "Fine-Grained / Alternative Approaches"),
            "type": "competing_paradigm",
            "papers": competitor_papers,
            "intro_use": "Introduction para 2 — alternative approach with specific limitation",
            "related_work_role": "Present the closest competing methods and their shortcomings",
        })

    # Theme 3: Gap evidence
    gap_papers = relation_groups.get("gap_evidence", [])
    if gap_papers:
        themes.append({
            "id": "C",
            "name": "The Remaining Gap",
            "type": "gap",
            "papers": gap_papers,
            "intro_use": "Introduction para 3 — evidence that the gap is real and recognized",
            "related_work_role": "Demonstrate that the limitation is acknowledged in the literature",
        })

    # Theme 4: Baselines (for Experiments context)
    baseline_papers = relation_groups.get("baselines", [])
    if baseline_papers:
        themes.append({
            "id": "D",
            "name": "Standard Baselines and Benchmarks",
            "type": "baselines",
            "papers": baseline_papers,
            "intro_use": "Not used in Introduction — used in Experiments",
            "related_work_role": "Describe standard methods we compare against",
        })

    # Sort themes into logical order for Introduction / Related Work
    type_order = {"current_progress": 0, "competing_paradigm": 1, "gap": 2, "baselines": 3}
    themes.sort(key=lambda t: type_order.get(t["type"], 99))

    return themes


def _derive_theme_name(papers, fallback):
    """Derive a descriptive theme name from the papers."""
    # Look for common keywords in titles
    all_text = " ".join(p.get("main_idea", "") + " " + p.get("paper", p.get("title", ""))
                        for p in papers).lower()

    keywords = [
        ("contrastive learning / vision-language pretraining", ["contrastive", "clip", "pretraining", "vision-language"]),
        ("fine-grained alignment / cross-modal attention", ["fine-grained", "cross-attention", "region", "alignment"]),
        ("transformer-based architectures", ["transformer", "vit", "attention mechanism"]),
        ("generative / diffusion models", ["diffusion", "generative", "generation"]),
        ("graph neural approaches", ["graph", "gnn", "relational"]),
        ("parameter-efficient / lightweight methods", ["efficient", "lightweight", "lora", "adapter"]),
        ("self-supervised / unsupervised learning", ["self-supervised", "unsupervised", "pretext"]),
    ]

    best_match = fallback
    best_count = 0
    for name, kws in keywords:
        count = sum(1 for kw in kws if kw in all_text)
        if count > best_count:
            best_count = count
            best_match = name

    return best_match


# ── Narrative Construction ────────────────────────────────────────────────────────


def build_intro_para2(themes, project_info):
    """Synthesize Introduction paragraph 2: current progress narrative."""
    progress_themes = [t for t in themes if t["type"] in ("current_progress", "competing_paradigm")]

    if not progress_themes:
        return ""

    parts = []
    for i, theme in enumerate(progress_themes):
        papers = theme["papers"]
        if not papers:
            continue

        # Representative papers (2-3)
        reps = papers[:3]
        paper_names = [p.get("paper", p.get("title", ""))[:60] for p in reps]

        # Core idea of this theme
        main_ideas = [p.get("main_idea", "") for p in reps if p.get("main_idea")]
        core = main_ideas[0] if main_ideas else f"methods in the {theme['name']} family"

        # What they achieve
        achievements = []
        for p in reps:
            # Look for metric numbers
            nums = re.findall(r'(\d+\.?\d*\s*%)', p.get("main_idea", ""))
            if nums:
                achievements.append(f"{nums[0]} on {p.get('paper', p.get('title', ''))[:30]}")

        parts.append({
            "theme": theme["name"],
            "papers": paper_names,
            "core_idea": core,
            "achievements": achievements,
            "limitation": _extract_limitation(papers, theme["name"]),
            "transition": _transition_sentence(i, len(progress_themes), theme["name"]),
        })

    return parts


def build_intro_para3(themes, project_info):
    """Synthesize Introduction paragraph 3: the gap narrative."""
    gap_themes = [t for t in themes if t["type"] == "gap"]
    all_limitations = []

    # Collect limitations from all themes
    for theme in themes:
        if theme["type"] == "gap":
            continue
        limitation = _extract_limitation(theme["papers"], theme["name"])
        if limitation["text"]:
            all_limitations.append(limitation)

    # Gap evidence papers
    gap_papers = []
    for t in gap_themes:
        gap_papers.extend(t["papers"])

    return {
        "accumulated_limitations": all_limitations,
        "gap_evidence_papers": [p.get("paper", p.get("title", ""))[:80] for p in gap_papers],
        "root_cause": project_info.get("gap", "[INSERT ROOT CAUSE — WHY existing methods fail]"),
        "specific_scenario": _find_gap_scenario(gap_papers, project_info),
    }


def build_related_work_sections(themes, project_info):
    """Synthesize Related Work sections as structured paragraph templates."""
    sections = []

    rw_themes = [t for t in themes if t["type"] in ("current_progress", "competing_paradigm", "gap")]

    for i, theme in enumerate(rw_themes):
        papers = theme["papers"]
        if not papers:
            continue

        # Representative papers with their main ideas
        paper_summaries = []
        for p in papers[:3]:
            paper_summaries.append({
                "name": p.get("paper", p.get("title", ""))[:80],
                "year": p.get("year", ""),
                "venue": p.get("venue", "")[:30],
                "main_idea": p.get("main_idea", "")[:200],
            })

        # How our method differs from this theme
        differentiation = _derive_differentiation(theme, project_info)

        section = {
            "subsection_title": f"{theme['id']}. {theme['name']}",
            "topic_sentence": _topic_sentence(theme, paper_summaries),
            "representative_papers": paper_summaries,
            "limitation": _extract_limitation(papers, theme["name"]),
            "differentiation": differentiation,
            "transition_to_next": "",
        }

        if i < len(rw_themes) - 1:
            section["transition_to_next"] = (
                f"While the above methods focus on {theme['name'].lower()}, "
                f"a complementary line of work addresses [{rw_themes[i+1]['name'].lower()}]."
            )

        sections.append(section)

    return sections


def _extract_limitation(papers, theme_name):
    """Extract limitations from a group of papers."""
    limitations = []
    for p in papers:
        idea = p.get("main_idea", "").lower()
        # Look for limitation language
        for kw in ["however", "but", "struggle", "fail", "cannot", "lack",
                    "missing", "limited", "bottleneck", "assumes", "only"]:
            if kw in idea:
                # Get the sentence containing this keyword
                sentences = re.split(r'[.!?]\s*', idea)
                for s in sentences:
                    if kw in s and len(s) > 20:
                        limitations.append(s.strip()[:150])
                        break
                break

    text = limitations[0] if limitations else ""
    return {"text": text, "source_theme": theme_name}


def _find_gap_scenario(gap_papers, project_info):
    """Extract the specific scenario where existing methods fail."""
    if not gap_papers:
        return project_info.get("gap", "")
    all_text = " ".join(p.get("main_idea", "") for p in gap_papers).lower()
    # Look for "when" clauses
    when_match = re.search(r'(?:when|particularly when|especially for|in the case of)\s+([^,.]+)', all_text)
    if when_match:
        return when_match.group(1).strip()
    return "conditions where [INSERT SPECIFIC FAILURE CONDITION]"


def _derive_differentiation(theme, project_info):
    """Derive how our method differs from this theme."""
    method_name = project_info.get("method_name", "our method")
    method_summary = project_info.get("method_summary", "")

    return {
        "what_we_do_differently": f"Unlike these methods, {method_name} [INSERT: what we do differently and why]",
        "key_advantage": "[INSERT: the resulting advantage over this line of work]",
    }


def _topic_sentence(theme, papers):
    """Generate a topic sentence for a Related Work subsection."""
    if not papers:
        return f"The {theme['name']} paradigm has been explored by several recent works."
    first = papers[0]
    return (
        f"{theme['name']} has emerged as a [dominant / promising / active] approach, "
        f"with representative works including {first['name']} ({first.get('year', '')})."
    )


def _transition_sentence(index, total, theme_name):
    """Generate a transition between themes in Introduction."""
    if index == 0:
        return f"A first major line of work focuses on {theme_name.lower()}."
    elif index == total - 1:
        return f"More recently, attention has shifted toward {theme_name.lower()}."
    else:
        return f"In parallel, researchers have explored {theme_name.lower()}."


# ── Prompt Builder ────────────────────────────────────────────────────────────────


def build_synthesis_prompt(papers, themes, project_info):
    """Build the AI synthesis prompt that turns themes into prose."""
    method_name = project_info.get("method_name", "[METHOD NAME]")
    task = project_info.get("task", "[TASK]")
    gap = project_info.get("gap", "[GAP DESCRIPTION]")
    contributions = project_info.get("contributions", [])
    method_summary = project_info.get("method_summary", "")

    # Theme summaries for the prompt
    theme_summaries = []
    for t in themes:
        paper_list = "\n".join(
            f"    - {p.get('paper', p.get('title', ''))[:100]} ({p.get('year', '')}): "
            f"{p.get('main_idea', '')[:150]}"
            for p in t["papers"][:4]
        )
        theme_summaries.append(
            f"### Theme {t['id']}: {t['name']}\n"
            f"Role in paper: {t['related_work_role']}\n"
            f"Papers:\n{paper_list}"
        )

    prompt = f"""# Literature Synthesis Task

## Your Role
You are writing the Introduction and Related Work sections of a scientific paper.
You must synthesize the literature below into coherent, logically flowing prose.
Do NOT write a paper-by-paper laundry list. Write a SYNTHESIS.

## Our Paper
**Method Name:** {method_name}
**Research Task:** {task}
**Method Summary:** {method_summary or '[INSERT — 2-3 sentence method description]'}
**The Gap We Address:** {gap or '[INSERT — specific gap with "because" clause]'}
**Contributions:**
{chr(10).join(f"- {c}" for c in contributions) if contributions else '- [INSERT]'}

## Literature Themes
{chr(10).join(theme_summaries)}

## Instructions

### Part 1: Introduction Paragraph 2 — Current Progress
Write ONE paragraph (150-200 words) synthesizing Themes A and B.
- Describe PARADIGMS, not papers. Group papers by approach, not by author.
- Mention representative paper names in parentheses when introducing a paradigm.
- Include specific performance numbers where available (not "high performance" but "R@1 of 63%").
- End with the shared limitation that leads naturally to Paragraph 3.

**Pattern:**
> [Paradigm A] methods (Author1 et al., Year1; Author2 et al., Year2) [what they do + achievement].
> In contrast, [Paradigm B] approaches (Author3 et al., Year3) [what they do differently].
> However, both paradigms share a fundamental limitation: [the gap].

### Part 2: Introduction Paragraph 3 — The Gap
Write ONE paragraph (80-120 words) articulating the remaining gap.
- State the gap with a BECAUSE clause: "Existing methods fail to X because Y."
- Cite gap evidence papers (Theme C if available) to show this is a recognized problem.
- Provide a concrete scenario where the gap manifests.
- End with a natural lead-in to our method.

**Pattern:**
> Despite these advances, [specific gap statement with because].
> This limitation is evident in [concrete scenario].
> Evidence from [citation] confirms that [supporting finding].
> Existing approaches cannot [capability] because [root cause].
> To address this, we propose [method name], which [1-sentence teaser].

### Part 3: Related Work (3-4 subsections)
Write one subsection per theme. Each subsection:

1. **Topic sentence** (1 sentence): what this line of work is about
2. **Body** (3-5 sentences): representative papers with brief descriptions
3. **Limitation statement** (1-2 sentences): what this line of work does NOT address
4. **Differentiation** (1 sentence): how our method differs

**Pattern per subsection:**
> [Theme name] has been [studied / advanced / explored] by [X] recent works.
> [Paper A] ([Year]) [what they did + key finding].
> [Paper B] ([Year]) extended this by [what they added].
> More recently, [Paper C] ([Year]) demonstrated that [finding].
> However, these methods [shared limitation], because [reason].
> Our method differs in that we [key difference], enabling [advantage].

### Part 4: Logical Flow Check
After writing all sections, verify:
1. Can you read each theme subsection independently and understand the message?
2. Do adjacent themes connect logically? Or do they feel like separate encyclopedia entries?
3. Does every cited paper serve a clear purpose?
4. Is our differentiation explicit in EVERY theme subsection?
5. Does the Introduction para 2 → para 3 → method teaser form an unbroken chain?

### Format
Output as Markdown with clear section headers. Use [CITATION NEEDED] for papers whose details are uncertain. Do NOT fabricate information beyond what is provided in the literature themes above.
"""
    return prompt


def build_structured_output(themes, project_info):
    """Build a pre-structured outline (for template mode)."""
    intro2 = build_intro_para2(themes, project_info)
    intro3 = build_intro_para3(themes, project_info)
    rw_sections = build_related_work_sections(themes, project_info)

    lines = [
        "# Literature Synthesis — Structured Outline",
        "",
        "> This outline provides the logical structure. Fill each section with prose following the patterns.",
        "",
    ]

    # Introduction Para 2
    lines.append("## Introduction Paragraph 2: Current Progress")
    lines.append("")
    for part in intro2:
        lines.append(f"### Paradigm: {part['theme']}")
        lines.append(f"- **Representative papers:** {', '.join(p[:60] for p in part['papers'])}")
        lines.append(f"- **Core idea:** {part['core_idea'][:200]}")
        if part["achievements"]:
            lines.append(f"- **Key results:** {', '.join(part['achievements'])}")
        lines.append(f"- **Limitation:** {part['limitation']['text'][:200] or '(extract from paper abstracts)'}")
        lines.append(f"- **Transition:** {part['transition']}")
        lines.append("")
    lines.append("**Draft space — write your paragraph here:**")
    lines.append("")
    lines.append("> [Write 150-200 words synthesizing the above paradigms. Group by approach, not paper-by-paper.]")
    lines.append("")

    # Introduction Para 3
    lines.append("## Introduction Paragraph 3: The Gap")
    lines.append("")
    if intro3["accumulated_limitations"]:
        lines.append("**Accumulated limitations from prior work:**")
        for lim in intro3["accumulated_limitations"]:
            lines.append(f"- From {lim['source_theme']}: {lim['text'][:150]}")
        lines.append("")
    if intro3["gap_evidence_papers"]:
        lines.append(f"**Gap evidence papers:** {', '.join(intro3['gap_evidence_papers'])}")
        lines.append("")
    lines.append(f"**Root cause:** {intro3['root_cause']}")
    lines.append(f"**Specific failure scenario:** {intro3['specific_scenario']}")
    lines.append("")
    lines.append("**Draft space — write your paragraph here:**")
    lines.append("")
    lines.append("> [Write 80-120 words. State the gap with a BECAUSE clause. Provide a concrete scenario. End with our method teaser.]")
    lines.append("")

    # Related Work
    lines.append("## Related Work")
    lines.append("")
    for i, sec in enumerate(rw_sections):
        lines.append(f"### {sec['subsection_title']}")
        lines.append("")
        lines.append(f"**Topic sentence:** {sec['topic_sentence']}")
        lines.append("")
        lines.append("**Representative papers:**")
        for ps in sec["representative_papers"]:
            lines.append(f"- {ps['name']} ({ps['year']}, {ps['venue']}): {ps['main_idea'][:150]}")
        lines.append("")
        lines.append(f"**Limitation of this line of work:** {sec['limitation']['text'][:200] or '(identify from paper abstracts)'}")
        lines.append("")
        lines.append(f"**Our differentiation:** {sec['differentiation']['what_we_do_differently']}")
        lines.append("")
        if sec["transition_to_next"]:
            lines.append(f"**Transition to next theme:** {sec['transition_to_next']}")
            lines.append("")
        lines.append("**Draft space:**")
        lines.append("")
        lines.append("> [Write 5-8 sentences following the pattern: topic → papers → limitation → differentiation.]")
        lines.append("")

    # Logical flow check
    lines.append("## Logical Flow Checklist")
    lines.append("")
    lines.append("After drafting, verify:")
    lines.append("")
    for i, sec in enumerate(rw_sections):
        lines.append(f"- [ ] {sec['subsection_title']}: can be understood independently, has clear differentiation from our method")
    lines.append("- [ ] Introduction para 2 → para 3 forms an unbroken argument chain")
    lines.append("- [ ] Every citation has a clear purpose (no citation stuffing)")
    lines.append("- [ ] No paper is described in full detail in both Introduction AND Related Work")
    lines.append("- [ ] Our method is explicitly differentiated from every major theme")
    lines.append("")

    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Synthesize literature matrix into narrative for Introduction + Related Work",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate synthesis prompt (provider-agnostic — use with any AI agent)
  python synthesize_literature.py lit_matrix.md --project-brief brief.md \\
      --output synthesis_prompt.md

  # Generate structured outline (template mode)
  python synthesize_literature.py lit_matrix.md --project-brief brief.md \\
      --template --output synthesis_outline.md

  # Auto-synthesize using Anthropic API
  python synthesize_literature.py lit_matrix.md --project-brief brief.md \\
      --auto --api-key $ANTHROPIC_API_KEY --output synthesis.md
        """,
    )
    parser.add_argument("literature_matrix", help="Filled literature matrix (.md)")
    parser.add_argument("--project-brief", required=True, help="Stage 1 project brief (.md)")
    parser.add_argument("--output", "-o", default="literature_synthesis.md", help="Output file")
    parser.add_argument("--auto", action="store_true", help="Auto-synthesize using Anthropic API")
    parser.add_argument("--api-key", help="Anthropic API key (or set ANTHROPIC_API_KEY)")
    parser.add_argument("--model", default="claude-sonnet-4-6-20250514",
                        help="Model for synthesis (default: claude-sonnet-4-6)")
    parser.add_argument("--template", action="store_true",
                        help="Generate structured outline only (no AI processing)")
    parser.add_argument("--prompt-only", action="store_true",
                        help="Generate the synthesis prompt only (for manual AI processing)")
    args = parser.parse_args()

    # Load inputs
    matrix_text = Path(args.literature_matrix).read_text(encoding="utf-8", errors="replace")
    brief_text = Path(args.project_brief).read_text(encoding="utf-8", errors="replace")

    papers = parse_literature_matrix(matrix_text)
    project_info = parse_project_brief(brief_text)
    existing_themes = parse_related_work_structure(matrix_text)

    if not papers:
        print("Error: No papers found in literature matrix.", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(papers)} papers from matrix.", file=sys.stderr)
    print(f"Project: task='{project_info.get('task', 'N/A')[:60]}...'", file=sys.stderr)

    # Build themes
    themes = build_themes(papers, project_info)

    # If the matrix already has a Related Work Structure, incorporate it
    if existing_themes:
        # Map existing theme names to our auto-generated themes
        name_map = {t["name"]: t for t in themes}
        for i, et in enumerate(existing_themes):
            if i < len(themes):
                themes[i]["name"] = et["name"]
                themes[i]["id"] = et["id"]

    print(f"Identified {len(themes)} narrative themes: {[t['name'] for t in themes]}", file=sys.stderr)

    # Generate output based on mode
    if args.template:
        output = build_structured_output(themes, project_info)
    elif args.prompt_only:
        output = build_synthesis_prompt(papers, themes, project_info)
    elif args.auto:
        api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("Error: --api-key required for --auto mode. Falling back to prompt generation.", file=sys.stderr)
            output = build_synthesis_prompt(papers, themes, project_info)
            args.output = args.output.replace(".md", "_prompt.md")
        else:
            prompt = build_synthesis_prompt(papers, themes, project_info)
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=api_key)
                resp = client.messages.create(
                    model=args.model,
                    max_tokens=4096,
                    temperature=0.2,
                    system="You are an expert scientific writer synthesizing literature into coherent narrative. "
                           "Write in formal academic English. Synthesize by PARADIGM, not paper-by-paper. "
                           "Every paragraph must have a clear topic sentence. Every claim must trace to a paper in the literature matrix.",
                    messages=[{"role": "user", "content": prompt}],
                )
                output = resp.content[0].text
                print(f"Synthesized with {args.model}.", file=sys.stderr)
            except ImportError:
                print("Install anthropic SDK: pip install anthropic", file=sys.stderr)
                output = prompt
            except Exception as e:
                print(f"API error: {e}. Falling back to prompt.", file=sys.stderr)
                output = prompt
    else:
        # Default: generate both prompt and structured outline
        outline = build_structured_output(themes, project_info)
        prompt = build_synthesis_prompt(papers, themes, project_info)
        output = (
            "# Literature Synthesis Package\n\n"
            "This file contains:\n"
            "1. A structured outline with fill-in-the-blank templates\n"
            "2. An AI synthesis prompt for automated prose generation\n\n"
            "Use the outline to manually draft, or copy the prompt to an AI agent.\n\n"
            "---\n\n"
            + outline
            + "\n\n---\n\n# AI Synthesis Prompt\n\n"
            + prompt
        )

    Path(args.output).write_text(output, encoding="utf-8")
    file_size = Path(args.output).stat().st_size
    print(f"Saved to {args.output} ({file_size:,} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
