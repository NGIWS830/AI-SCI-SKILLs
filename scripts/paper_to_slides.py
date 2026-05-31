#!/usr/bin/env python3
"""Convert an academic paper into presentation slides (Beamer LaTeX / Markdown).

Usage:
    python paper_to_slides.py paper.md --output slides.tex
    python paper_to_slides.py paper.md --format markdown --output slides.md
    python paper_to_slides.py paper.md --format beamer --theme Madrid --output slides.tex

Features:
    - Auto-extract key messages from each section
    - Generate Beamer LaTeX with proper structure
    - Generate Markdown slide decks (Marp/Deckset compatible)
    - Slide count estimation and section allocation
    - Figure/table placeholder insertion
    - Speaker notes generation
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


# ── Paper Parsing ─────────────────────────────────────────────────────────────────

def parse_paper_sections(markdown_text):
    """Parse paper markdown into sections."""
    sections = {}
    current_title = "Preamble"
    current_lines = []

    for line in markdown_text.split("\n"):
        # Match top-level and second-level headings
        m = re.match(r'^(#{1,3})\s+(.*?)$', line)
        if m:
            if current_lines:
                sections[current_title] = "\n".join(current_lines)
            level = len(m.group(1))
            title = m.group(2).strip()
            # Normalize section names
            current_title = title
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        sections[current_title] = "\n".join(current_lines)

    return sections


def extract_key_points(section_text, section_name=""):
    """Extract key bullet points from a section."""
    points = []

    # Find bold text (often key terms)
    bold_items = re.findall(r'\*\*(.*?)\*\*', section_text)
    for item in bold_items[:3]:
        if len(item) > 10 and len(item) < 120:
            points.append(item)

    # Find sentences with key metric numbers
    number_sentences = re.findall(
        r'([^.]*?(?:achieves|improves|outperforms|boosts|reduces|achieve)\s[^.]*?[\d.]+[%]?[^.]*\.)',
        section_text, re.IGNORECASE
    )
    for sent in number_sentences:
        cleaned = sent.strip()[:150]
        if cleaned not in points:
            points.append(cleaned)

    # Find sentences with contribution language
    contrib_sentences = re.findall(
        r'([^.]*?(?:propose|introduce|present|design|develop)\s[^.]*?(?:module|method|framework|approach|loss|strategy)[^.]*\.)',
        section_text, re.IGNORECASE
    )
    for sent in contrib_sentences[:3]:
        cleaned = sent.strip()[:150]
        if cleaned not in points:
            points.append(cleaned)

    # Fallback: first few substantial sentences
    if not points:
        sentences = re.split(r'(?<=[.!?])\s+', section_text)
        for sent in sentences[:5]:
            cleaned = sent.strip()[:150]
            if len(cleaned) > 30:
                points.append(cleaned)

    return points[:6]  # Max 6 points per section


def extract_figures_and_tables(text):
    """Extract figure and table references from paper text."""
    figures = re.findall(r'(Figure\s+\d+|Fig\.?\s*\d+)', text, re.IGNORECASE)
    tables = re.findall(r'(Table\s+\d+)', text, re.IGNORECASE)
    return list(set(figures)), list(set(tables))


# ── Slide Layout Templates ─────────────────────────────────────────────────────────

BEAMER_TEMPLATE = r"""\documentclass[aspectratio=169]{beamer}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{amsmath}

% Theme and colors
\usetheme{{{theme}}}
\usecolortheme{{default}}

% Title page info
\title[{short_title}]{{{full_title}}}
\author{{{authors}}}
\institute{{{affiliation}}}
\date{{\today}}

\begin{{document}}

% ── Title Slide ──
\begin{{frame}}
\titlepage
\end{{frame}}

% ── Outline ──
\begin{{frame}}{{Outline}}
\tableofcontents
\end{{frame}}

{slides}

\end{{document}}
"""

BEAMER_SLIDE_TEMPLATES = {
    "section_header": r"""
% ── {section_name} ──
\section{{{section_name}}}
\begin{{frame}}{{{section_name}}}
\begin{{itemize}}
{items}
\end{{itemize}}
\end{{frame}}
""",

    "content_slide": r"""
\begin{{frame}}{{{title}}}
\begin{{itemize}}
{items}
\end{{itemize}}
\end{{frame}}
""",

    "figure_slide": r"""
\begin{{frame}}{{{title}}}
\begin{{center}}
% \includegraphics[width=0.8\textwidth]{{{figure_path}}}
\framebox[0.7\textwidth]{{\LARGE [Figure {figure_ref}]}}
\end{{center}}
\begin{{itemize}}
{items}
\end{{itemize}}
\end{{frame}}
""",

    "table_slide": r"""
\begin{{frame}}{{{title}}}
{{
\footnotesize
% \input{{{table_path}}}
\begin{{center}}
\framebox[0.8\textwidth]{{\LARGE [Table {table_ref}]}}
\end{{center}}
}}
\begin{{itemize}}
{items}
\end{{itemize}}
\end{{frame}}
""",

    "conclusion_slide": r"""
\begin{{frame}}{{Summary}}
\begin{{itemize}}
{items}
\end{{itemize}}
\vspace{{1em}}
\begin{{block}}{{Key Takeaway}}
{key_takeaway}
\end{{block}}
\end{{frame}}
""",

    "thank_you_slide": r"""
\begin{{frame}}{{Thank You}}
\begin{{center}}
{\LARGE Thank you!}

\vspace{{1em}}
Questions?

\vspace{{2em}}
{contact_info}
\end{{center}}
\end{{frame}}
""",
}

MARKDOWN_SLIDE_TEMPLATE = """---
# Marp Slide Deck — {full_title}

---

<!-- _class: lead -->
# {full_title}
## {authors}
{affiliation}

---

<!-- _class: toc -->
# Outline

{outline}

---

{slides}

---

<!-- _class: lead -->
# Thank You
{contact_info}
"""


# ── Slide Generation ───────────────────────────────────────────────────────────────

def build_beamer_slides(sections, args):
    """Build Beamer LaTeX slides."""
    # Identify key sections
    title = ""
    abstract = ""
    intro = ""
    method = ""
    experiments = ""
    conclusion = ""

    for name, text in sections.items():
        name_lower = name.lower()
        if "abstract" in name_lower or "摘要" in name_lower:
            abstract = text
        elif "intro" in name_lower or "引言" in name_lower:
            intro = text
        elif "method" in name_lower or "proposed" in name_lower or "方法" in name_lower:
            method = text
        elif "experiment" in name_lower or "实验" in name_lower or "result" in name_lower:
            experiments = text
        elif "conclusion" in name_lower or "结论" in name_lower:
            conclusion = text
        elif "title" in name_lower or name.startswith("#"):
            title = name

    # Extract title from first heading if not found
    if not title:
        for name in sections:
            if name not in ("Preamble", "Abstract", "摘要"):
                title_match = re.match(r'^#\s+(.+)$', name, re.MULTILINE)
                if title_match:
                    title = title_match.group(1)
                    break
                title = name
                break

    if not title:
        title = args.title or "Paper Title"

    intro_points = extract_key_points(intro, "Introduction")
    method_points = extract_key_points(method, "Method")
    experiment_points = extract_key_points(experiments, "Experiments")
    conclusion_points = extract_key_points(conclusion, "Conclusion")
    figures, tables = extract_figures_and_tables(experiments)

    slides = []

    # Introduction slides
    slides.append(BEAMER_SLIDE_TEMPLATES["section_header"].format(
        section_name="Motivation & Problem",
        items="\n".join(f"  \\item {p}" for p in intro_points[:4]),
    ))

    # Method slides
    slides.append(BEAMER_SLIDE_TEMPLATES["section_header"].format(
        section_name="Proposed Method",
        items="\\item Overview of the proposed approach",
    ))

    # Method overview slide
    overview_points = [p for p in method_points if len(p) < 100][:4]
    if overview_points:
        slides.append(BEAMER_SLIDE_TEMPLATES["content_slide"].format(
            title="Method Overview",
            items="\n".join(f"  \\item {p}" for p in overview_points),
        ))

    # Figure slide (architecture diagram placeholder)
    if figures:
        slides.append(BEAMER_SLIDE_TEMPLATES["figure_slide"].format(
            title="Architecture Overview",
            figure_ref=figures[0],
            figure_path="figures/architecture.pdf",
            items="\\item Key components of the proposed method",
        ))

    # Experiments
    slides.append(BEAMER_SLIDE_TEMPLATES["section_header"].format(
        section_name="Experiments",
        items="\\item Experimental setup and main results",
    ))

    for point in experiment_points[:5]:
        if any(c.isdigit() for c in point):
            slides.append(BEAMER_SLIDE_TEMPLATES["content_slide"].format(
                title="Results",
                items=f"  \\item {point}",
            ))

    if tables:
        slides.append(BEAMER_SLIDE_TEMPLATES["table_slide"].format(
            title="Main Results",
            table_ref=tables[0],
            table_path="tables/results.tex",
            items="\\item Our method consistently outperforms baselines",
        ))

    # Conclusion
    takeaway = conclusion_points[0] if conclusion_points else "Our method provides a practical solution."
    slides.append(BEAMER_SLIDE_TEMPLATES["conclusion_slide"].format(
        items="\n".join(f"  \\item {p}" for p in conclusion_points[:3] + intro_points[-2:]),
        key_takeaway=takeaway,
    ))

    slides.append(BEAMER_SLIDE_TEMPLATES["thank_you_slide"].format(
        contact_info=f"{args.email}\\\\{args.website}" if args.email else "",
    ))

    # Determine short title
    short_title = title[:50] if len(title) > 50 else title

    beamer = BEAMER_TEMPLATE.format(
        theme=args.theme,
        full_title=_latex_escape(title),
        short_title=_latex_escape(short_title),
        authors=_latex_escape(args.author),
        affiliation=_latex_escape(args.affiliation),
        slides="\n".join(slides),
    )
    return beamer


def build_markdown_slides(sections, args):
    """Build Markdown (Marp-compatible) slides."""
    title = args.title or list(sections.keys())[0] if sections else "Paper Title"

    # Collect key points
    all_points = []
    for name, text in sections.items():
        if len(name) > 5:
            points = extract_key_points(text, name)
            if points:
                all_points.append((name, points))

    slides = []
    slide_num = 1
    for section_name, points in all_points:
        slides.append(f"---\n\n## {section_name}\n")
        for p in points[:4]:
            # Convert bold markers
            p_clean = re.sub(r'\*\*(.*?)\*\*', r'**\1**', p)
            slides.append(f"- {p_clean}")
        slides.append("")
        slide_num += 1

    # Outline
    outline = "\n".join(f"- {name}" for name, _ in all_points if len(name) > 3)

    return MARKDOWN_SLIDE_TEMPLATE.format(
        full_title=title,
        authors=args.author,
        affiliation=args.affiliation,
        outline=outline,
        slides="\n".join(slides),
        contact_info=f"Email: {args.email}" if args.email else "",
    )


def build_speaker_notes(sections):
    """Generate speaker notes from paper content."""
    notes = ["# Speaker Notes\n"]
    for name, text in sections.items():
        if len(name) < 3 or "preamble" in name.lower():
            continue
        sentences = re.split(r'(?<=[.!?])\s+', text)
        key_sentences = [s.strip() for s in sentences[:6] if len(s.strip()) > 40]
        if key_sentences:
            notes.append(f"## {name}\n")
            for s in key_sentences[:4]:
                notes.append(f"- {s}")
            notes.append("")
    return "\n".join(notes)


def _latex_escape(text):
    chars = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
             "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\^{}"}
    return "".join(chars.get(c, c) for c in text)


# ── CLI ────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convert an academic paper into presentation slides",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate Beamer LaTeX slides
  python paper_to_slides.py 08_english_polished.md --format beamer --output slides.tex

  # Generate Marp markdown slides
  python paper_to_slides.py 08_english_polished.md --format markdown --output slides.md

  # With metadata
  python paper_to_slides.py paper.md --author "J. Yang et al." \\
      --affiliation "University" --theme Copenhagen

  # Generate speaker notes only
  python paper_to_slides.py paper.md --notes-only --output speaker_notes.md
        """,
    )
    parser.add_argument("paper", help="Path to the polished English manuscript (.md)")
    parser.add_argument("--output", "-o", default="slides.tex", help="Output file path")
    parser.add_argument("--format", "-f", default="beamer", choices=["beamer", "markdown"],
                        help="Output format (default: beamer)")
    parser.add_argument("--title", help="Presentation title (default: auto-extract)")
    parser.add_argument("--author", default="", help="Author list")
    parser.add_argument("--affiliation", default="", help="Author affiliation/institution")
    parser.add_argument("--email", default="", help="Contact email for final slide")
    parser.add_argument("--website", default="", help="Project website")
    parser.add_argument("--theme", default="Madrid",
                        choices=["Madrid", "Copenhagen", "Berlin", "Singapore", "Warsaw",
                                 "CambridgeUS", "Rochester", "Pittsburgh", "Boadilla"],
                        help="Beamer theme (default: Madrid)")
    parser.add_argument("--notes-only", action="store_true",
                        help="Generate speaker notes only, skip slides")
    args = parser.parse_args()

    paper_text = Path(args.paper).read_text(encoding="utf-8", errors="replace")
    sections = parse_paper_sections(paper_text)

    if args.notes_only:
        output = build_speaker_notes(sections)
    elif args.format == "beamer":
        output = build_beamer_slides(sections, args)
    elif args.format == "markdown":
        output = build_markdown_slides(sections, args)
    else:
        output = build_beamer_slides(sections, args)

    Path(args.output).write_text(output, encoding="utf-8")
    print(f"Slides saved to {args.output} ({len(sections)} sections processed)")

    if args.notes_only:
        note_path = args.output.replace(".tex", "_notes.md").replace(".md", "_notes.md")
        if note_path == args.output:
            note_path = str(Path(args.output).with_suffix("")) + "_notes.md"
        speaker_notes = build_speaker_notes(sections)
        Path(note_path).write_text(speaker_notes)
        print(f"Speaker notes saved to {note_path}")


if __name__ == "__main__":
    main()
