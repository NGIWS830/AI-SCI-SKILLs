#!/usr/bin/env python3
"""Generate a structured reviewer response / rebuttal letter.

Usage:
    python generate_rebuttal.py reviews.txt --paper paper.md --output rebuttal.md
    python generate_rebuttal.py reviews.json --paper-dir ./outputs/ --output rebuttal.md
    python generate_rebuttal.py reviews.md --paper 08_english_polished.md --latex

Input formats supported:
    - Plain text reviews
    - JSON reviews (list of {reviewer, comments: [{id, text, type}]})
    - Markdown reviews
    - OpenReview-style structured reviews

Features:
    - Auto-categorize reviewer comments (clarity, experiments, novelty, correctness, presentation)
    - Generate structured response templates with evidence pointers
    - Track changes to avoid contradicting responses across reviewers
    - LaTeX output for direct submission
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


# ── Review Parsing ────────────────────────────────────────────────────────────────

def parse_reviews_text(text):
    """Parse free-form review text into structured comments."""
    reviewers = []
    current_reviewer = None
    current_comments = []

    # Pattern: "Reviewer X:" or "Reviewer #X:" or "Review X:"
    reviewer_pattern = re.compile(r'^(?:Reviewer|Review|Referee)\s*[#:]?\s*(\w+)', re.IGNORECASE)
    # Pattern: numbered comments "1.", "Q1:", "Comment 1:"
    comment_pattern = re.compile(r'^(?:\d+[\.\)]\s*|Q\d+\s*[:：]\s*|Comment\s*\d+\s*[:：]\s*|Weakness\s*\d+\s*[:：]\s*|Strength\s*\d*\s*[:：]\s*)')

    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        m = reviewer_pattern.match(line)
        if m:
            if current_reviewer and current_comments:
                reviewers.append({"reviewer": current_reviewer, "comments": current_comments})
            current_reviewer = m.group(1)
            current_comments = []
            i += 1
            continue

        m2 = comment_pattern.match(line)
        if m2 and current_reviewer:
            comment_text = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not reviewer_pattern.match(lines[i].strip()) and not comment_pattern.match(lines[i].strip()):
                comment_text.append(lines[i].strip())
                i += 1
            full_text = " ".join(comment_text)
            current_comments.append({"text": full_text, "type": _classify_comment(full_text)})
            continue

        # Continuation of previous comment or standalone
        if current_reviewer:
            current_comments.append({"text": line, "type": _classify_comment(line)})
        i += 1

    if current_reviewer and current_comments:
        reviewers.append({"reviewer": current_reviewer, "comments": current_comments})

    return reviewers


def parse_reviews_json(json_text):
    """Parse structured JSON reviews."""
    data = json.loads(json_text)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "reviews" in data:
        return data["reviews"]
    return [{"reviewer": "Unknown", "comments": data.get("comments", [])}]


def parse_reviews_markdown(text):
    """Parse markdown-formatted reviews."""
    return parse_reviews_text(text)


def _classify_comment(text):
    """Classify a reviewer comment into a category."""
    text_lower = text.lower()

    categories = {
        "experiments": [
            "experiment", "baseline", "dataset", "ablation", "result", "metric",
            "evaluation", "benchmark", "table", "figure", "comparison", "error bar",
            "standard deviation", "significance", "statistical",
            "实验", "基准", "消融", "数据集", "结果", "比较",
        ],
        "clarity": [
            "clarify", "explain", "unclear", "confusing", "understand", "readability",
            "notation", "typo", "grammar", "writing", "define", "definition",
            "meaning", "ambiguous", "vague",
            "不清楚", "不明白", "解释", "定义", "笔误",
        ],
        "novelty": [
            "novel", "contribution", "original", "incremental", "similar to",
            "difference", "distinction", "prior work", "existing", "previous",
            "新意", "贡献", "创新", "与.*相似", "区别",
        ],
        "correctness": [
            "incorrect", "wrong", "error", "mistake", "flaw", "bug",
            "theorem", "proof", "assumption", "justify", "valid",
            "错误", "不正确", "证明",
        ],
        "presentation": [
            "format", "citation", "reference", "figure quality", "table format",
            "organization", "structure", "abstract", "conclusion",
            "格式", "引用", "组织",
        ],
    }

    for category, keywords in categories.items():
        for kw in keywords:
            if re.search(kw, text_lower):
                return category

    return "general"


# ── Response Generation ───────────────────────────────────────────────────────────

RESPONSE_TEMPLATES = {
    "experiments": """
**Response to [{category}] Comment:** {comment_summary}

**Action Taken:** We conducted the requested experiment on {dataset}. {result_summary}. We have added the results to {section} (Table {table_ref}) and updated the corresponding discussion.

**Manuscript Changes:**
- Added {new_content_summary} in Section {section}.
- Updated Table {table_ref} with {new_data_description}.
""",

    "clarity": """
**Response to [{category}] Comment:** {comment_summary}

**Action Taken:** We have revised the text to clarify {topic}. Specifically, we {change_description}.

**Manuscript Changes:**
- Revised {section}, paragraph {para}: "{before_snippet}" → "{after_snippet}".
- Added a footnote/definition for {term}.
""",

    "novelty": """
**Response to [{category}] Comment:** {comment_summary}

**Action Taken:** We thank the reviewer for this observation. We have {change_description}. Our work differs from {related_work} in that {key_difference}.

**Manuscript Changes:**
- Revised {section} to explicitly discuss {discussion_topic}.
- Added comparison with {additional_related_work} in Related Work.
""",

    "correctness": """
**Response to [{category}] Comment:** {comment_summary}

**Action Taken:** {correction_description}. We have {fix_description}.

**Manuscript Changes:**
- Corrected {error_location}: "{incorrect_text}" → "{corrected_text}".
- {additional_fix_description}
""",

    "general": """
**Response to [{category}] Comment:** {comment_summary}

**Action Taken:** {action_summary}.

**Manuscript Changes:**
- {change_list}
""",
}


def generate_response(comment, paper_context=None, section_map=None):
    """Generate a structured response for a single reviewer comment."""
    category = comment.get("type", "general")
    text = comment.get("text", str(comment))

    # Truncate for summary
    comment_summary = text[:120] + ("..." if len(text) > 120 else "")

    template = RESPONSE_TEMPLATES.get(category, RESPONSE_TEMPLATES["general"])

    # Fill template with available context
    filled = template.format(
        category=category.upper(),
        comment_summary=comment_summary,
        dataset="[INSERT DATASET]",
        result_summary="[INSERT RESULT SUMMARY]",
        section="[INSERT SECTION]",
        table_ref="[INSERT TABLE/FIGURE #]",
        new_content_summary="[INSERT NEW CONTENT DESCRIPTION]",
        new_data_description="[INSERT NEW DATA DESCRIPTION]",
        topic="[INSERT TOPIC]",
        change_description="[INSERT CHANGE DESCRIPTION]",
        before_snippet="[INSERT BEFORE]",
        after_snippet="[INSERT AFTER]",
        term="[INSERT TERM]",
        related_work="[INSERT RELATED WORK]",
        key_difference="[INSERT KEY DIFFERENCE]",
        discussion_topic="[INSERT DISCUSSION]",
        additional_related_work="[INSERT ADDITIONAL RELATED WORK]",
        correction_description="[INSERT CORRECTION DESCRIPTION]",
        fix_description="[INSERT FIX DESCRIPTION]",
        error_location="[INSERT ERROR LOCATION]",
        incorrect_text="[INSERT INCORRECT]",
        corrected_text="[INSERT CORRECTED]",
        additional_fix_description="",
        action_summary="[INSERT ACTION SUMMARY]",
        change_list="- [INSERT CHANGE 1]\n- [INSERT CHANGE 2]",
    )
    return filled


# ── Cross-Reviewer Consistency ─────────────────────────────────────────────────────

def detect_conflicts(responses):
    """Detect potentially conflicting responses across reviewers."""
    conflicts = []
    for i, (rev_a, resp_a) in enumerate(responses):
        for j, (rev_b, resp_b) in enumerate(responses):
            if j <= i:
                continue
            # Simple check: shared keywords in responses
            words_a = set(re.findall(r'\b\w{6,}\b', " ".join(r[:200] for r in resp_a).lower()))
            words_b = set(re.findall(r'\b\w{6,}\b', " ".join(r[:200] for r in resp_b).lower()))
            common = words_a & words_b
            if len(common) > 10:
                conflicts.append({
                    "reviewer_a": rev_a,
                    "reviewer_b": rev_b,
                    "shared_terms": sorted(common)[:10],
                    "note": "Responses share substantial terminology — verify they do not contradict each other.",
                })
    return conflicts


# ── Response Document Builder ──────────────────────────────────────────────────────

def build_rebuttal_document(reviews, paper_path=None, output_format="markdown"):
    """Build a complete rebuttal document."""
    lines = []

    if output_format == "latex":
        lines.extend([
            r"\documentclass[11pt]{article}",
            r"\usepackage[margin=1in]{geometry}",
            r"\usepackage{hyperref}",
            r"\usepackage{enumitem}",
            r"\usepackage{xcolor}",
            r"\definecolor{responseblue}{RGB}{0,51,102}",
            r"\newcommand{\response}[1]{\textcolor{responseblue}{#1}}",
            r"\begin{document}",
            r"\title{Response to Reviewers}",
            r"\maketitle",
            r"\section*{Cover Letter}",
            r"",
            r"We thank all reviewers for their careful reading and constructive feedback.",
            r"We have addressed every comment and believe the revised manuscript is substantially improved.",
            r"",
            r"Below, reviewer comments are in \textit{italic}, and our responses are in \textcolor{responseblue}{blue}.",
            r"",
        ])
    else:
        lines.extend([
            "# Response to Reviewers",
            "",
            "We thank all reviewers for their careful reading and constructive feedback.",
            "We have addressed every comment and believe the revised manuscript is substantially improved.",
            "",
            "---",
            "",
        ])

    # Summary of changes
    lines.extend([
        "## Summary of Major Changes",
        "",
        "1. [SUMMARY ITEM 1 — fill after generating responses]",
        "2. [SUMMARY ITEM 2]",
        "3. [SUMMARY ITEM 3]",
        "",
        "---",
        "",
    ])

    # Per-reviewer responses
    all_responses = []
    for i, reviewer_data in enumerate(reviews):
        reviewer_id = reviewer_data.get("reviewer", f"Reviewer {i+1}")
        comments = reviewer_data.get("comments", [])

        if output_format == "latex":
            lines.append(rf"\section{{Response to {reviewer_id}}}")
            lines.append("")
        else:
            lines.append(f"## Response to {reviewer_id}")
            lines.append("")

        reviewer_responses = []
        for j, comment in enumerate(comments):
            comment_text = comment.get("text", str(comment))
            comment_type = comment.get("type", _classify_comment(comment_text))

            if output_format == "latex":
                lines.append(rf"\subsection*{{Comment {j+1} [{comment_type.upper()}]}}")
                lines.append(rf"\textit{{{_latex_escape(comment_text)}}}")
                lines.append("")
                lines.append(r"\response{")
                lines.append(r"[RESPONSE: INSERT YOUR RESPONSE HERE]")
                lines.append(r"}")
                lines.append("")
            else:
                lines.append(f"### Comment {j+1} [{comment_type.upper()}]")
                lines.append("")
                lines.append(f"> **Reviewer:** {comment_text}")
                lines.append("")
                lines.append("**Response:** [INSERT YOUR RESPONSE HERE]")
                lines.append("")
                lines.append("**Manuscript Changes:**")
                lines.append("- [INSERT CHANGE 1]")
                lines.append("- [INSERT CHANGE 2]")
                lines.append("")

            reviewer_responses.append(f"[RESPONSE TO COMMENT {j+1}]")

        all_responses.append((reviewer_id, reviewer_responses))

    # Cross-reviewer consistency notes
    conflicts = detect_conflicts(all_responses)
    if conflicts:
        if output_format == "latex":
            lines.append(r"\section{Cross-Reviewer Consistency Check}")
        else:
            lines.append("## Cross-Reviewer Consistency Check")
            lines.append("")
        for conflict in conflicts:
            lines.append(f"- Reviewers **{conflict['reviewer_a']}** and **{conflict['reviewer_b']}**: {conflict['note']}")
            lines.append(f"  Shared terms: {', '.join(conflict['shared_terms'])}")
        lines.append("")

    # Checklist
    lines.extend([
        "## Rebuttal Checklist",
        "",
        "Before submitting, verify:",
        "",
        "- [ ] Every reviewer comment has a specific response (no template placeholders remain).",
        "- [ ] All claimed manuscript changes are reflected in the revised manuscript.",
        "- [ ] No response contradicts another response.",
        "- [ ] Claims in responses match claims in the revised manuscript exactly.",
        "- [ ] New experiments (if any) are described with dataset, metric, and result.",
        "- [ ] Responses are respectful and professional, even to critical comments.",
        "- [ ] The cover letter does not copy-paste the abstract.",
        "- [ ] Numbers in rebuttal match numbers in manuscript.",
        "",
    ])

    if output_format == "latex":
        lines.append(r"\end{document}")

    return "\n".join(lines)


def _latex_escape(text):
    """Escape special LaTeX characters."""
    chars = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
             "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\^{}"}
    return "".join(chars.get(c, c) for c in text)


# ── CLI ────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate a structured reviewer response / rebuttal letter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # From plain text reviews
  python generate_rebuttal.py reviews.txt --output rebuttal.md

  # Generate LaTeX rebuttal
  python generate_rebuttal.py reviews.txt --latex --output rebuttal.tex

  # From JSON reviews with paper context
  python generate_rebuttal.py reviews.json --paper 08_english_polished.md --output rebuttal.md

  # Generate structured response templates for manual completion
  python generate_rebuttal.py reviews.md --template-only --output rebuttal_draft.md
        """,
    )
    parser.add_argument("reviews", help="Review file (.txt, .json, .md)")
    parser.add_argument("--paper", help="Path to polished English manuscript (for context)")
    parser.add_argument("--output", "-o", default="rebuttal.md", help="Output file")
    parser.add_argument("--latex", action="store_true", help="Generate LaTeX output")
    parser.add_argument("--template-only", action="store_true",
                        help="Generate response templates only (manual fill-in)")
    args = parser.parse_args()

    # Read reviews
    review_text = Path(args.reviews).read_text(encoding="utf-8", errors="replace")

    if args.reviews.endswith(".json"):
        reviews = parse_reviews_json(review_text)
    else:
        reviews = parse_reviews_text(review_text)

    if not reviews:
        print("No reviews found. Expected format: 'Reviewer 1:' followed by numbered comments.",
              file=sys.stderr)
        print("Trying JSON parse...", file=sys.stderr)
        try:
            reviews = parse_reviews_json(review_text)
        except json.JSONDecodeError:
            print("Could not parse reviews. Check input format.", file=sys.stderr)
            sys.exit(1)

    # Optionally read paper for context
    paper_text = ""
    if args.paper and Path(args.paper).exists():
        paper_text = Path(args.paper).read_text(encoding="utf-8", errors="replace")

    fmt = "latex" if args.latex else "markdown"
    rebuttal = build_rebuttal_document(reviews, paper_text, output_format=fmt)

    Path(args.output).write_text(rebuttal, encoding="utf-8")
    print(f"Rebuttal saved to {args.output} ({len(reviews)} reviewer(s), "
          f"{sum(len(r.get('comments', [])) for r in reviews)} total comments)", file=sys.stderr)


if __name__ == "__main__":
    main()
