#!/usr/bin/env python3
"""
Fill the IEEE Word template with structured manuscript content.

Reads a JSON content file and an IEEE conference Word template (.docx),
then produces a formatted Word manuscript.

Usage:
    python scripts/render_word.py <content.json> --output <output.docx>
    python scripts/render_word.py <content.json> --template <template.docx> --output <output.docx>
"""

import argparse
import json
import os
import sys
from copy import deepcopy

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor


def load_content(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    required = ["title", "authors", "abstract", "keywords", "sections", "references"]
    for key in required:
        if key not in content:
            raise ValueError(f"Missing required field: {key!r}")
    return content


def set_run_font(run, name="Times New Roman", size=Pt(10)):
    """Set font properties on a run."""
    run.font.name = name
    run.font.size = size


def add_title(doc, content):
    """Add paper title at the top of the document."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(content["title"])
    run.bold = True
    set_run_font(run, size=Pt(22))
    # Add spacing after title
    p.space_after = Pt(6)


def add_authors(doc, content):
    """Add author block."""
    author_lines = []
    for author in content["authors"]:
        name = author.get("name", "")
        affiliation = author.get("affiliation", "")
        email = author.get("email", "")
        lines = [name]
        if affiliation:
            lines.append(affiliation)
        if email:
            lines.append(email)
        author_lines.append("\n".join(lines))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("\n\n".join(author_lines))
    set_run_font(run, size=Pt(10))
    p.space_after = Pt(12)


def add_abstract(doc, content):
    """Add abstract section."""
    # Abstract heading
    p = doc.add_paragraph()
    run = p.add_run("Abstract")
    run.bold = True
    set_run_font(run, size=Pt(10))
    p.space_after = Pt(2)

    # Abstract body
    p = doc.add_paragraph()
    run = p.add_run(content["abstract"])
    set_run_font(run, size=Pt(9))
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.right_indent = Inches(0.25)
    p.space_after = Pt(8)


def add_keywords(doc, content):
    """Add keywords line."""
    p = doc.add_paragraph()
    run_label = p.add_run("Keywords—")
    run_label.bold = True
    set_run_font(run_label, size=Pt(9))
    run_value = p.add_run(", ".join(content["keywords"]))
    set_run_font(run_value, size=Pt(9))
    p.space_after = Pt(12)


def add_sections(doc, content):
    """Add body sections: headings and paragraphs."""
    heading_font_sizes = {1: Pt(12), 2: Pt(11), 3: Pt(10)}
    body_font_size = Pt(10)

    for section in content["sections"]:
        heading_text = section.get("heading", "")
        level = section.get("level", 1)
        body_text = section.get("content", "")

        # Add heading
        if heading_text:
            # IEEE uses Roman numerals for top-level sections
            if level == 1 and not heading_text.startswith("Acknowledgment") and not heading_text.startswith("References"):
                pass  # The heading text is used as-is; the agent should include numbering

            h = doc.add_heading(heading_text, level=min(level, 3))
            for run in h.runs:
                font_size = heading_font_sizes.get(level, Pt(10))
                set_run_font(run, size=font_size)

        # Add body paragraphs
        if body_text:
            # Split on double newline for paragraph breaks
            paragraphs = [p.strip() for p in body_text.split("\n\n") if p.strip()]
            for para_text in paragraphs:
                p = doc.add_paragraph()
                run = p.add_run(para_text)
                set_run_font(run, size=body_font_size)
                p.paragraph_format.first_line_indent = Inches(0.25)
                p.space_after = Pt(4)


def add_references(doc, content):
    """Add references section."""
    if not content["references"]:
        return

    # References heading
    h = doc.add_heading("References", level=1)
    for run in h.runs:
        set_run_font(run, size=Pt(12))

    for ref in content["references"]:
        p = doc.add_paragraph()
        run = p.add_run(ref)
        set_run_font(run, size=Pt(8))
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.space_after = Pt(2)


def add_figures(doc, content):
    """Add figure placeholders."""
    figures = content.get("figures", [])
    if not figures:
        return

    for fig in figures:
        caption = fig.get("caption", "")
        image_path = fig.get("image_path", "")
        width = fig.get("width_inches", 3.5)

        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        if image_path and os.path.exists(image_path):
            run = p.add_run()
            run.add_picture(image_path, width=Inches(width))
        else:
            # Placeholder box
            run = p.add_run(f"[Figure: {image_path or 'placeholder'}]")
            set_run_font(run, size=Pt(8))

        # Caption below figure
        cap_p = doc.add_paragraph()
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = cap_p.add_run(caption)
        set_run_font(run, size=Pt(8))
        cap_p.space_after = Pt(8)


def add_tables(doc, content):
    """Add tables with data."""
    tables = content.get("tables", [])
    if not tables:
        return

    for tbl_data in tables:
        caption = tbl_data.get("caption", "")
        header = tbl_data.get("header", [])
        rows = tbl_data.get("rows", [])

        # Caption above table
        if caption:
            cap_p = doc.add_paragraph()
            cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = cap_p.add_run(caption)
            run.bold = True
            set_run_font(run, size=Pt(8))
            cap_p.space_after = Pt(2)

        num_cols = len(header) if header else (len(rows[0]) if rows else 1)
        table = doc.add_table(rows=1 + len(rows), cols=num_cols)
        table.style = "Table Grid"

        # Header row
        if header:
            for j, cell_text in enumerate(header):
                cell = table.rows[0].cells[j]
                cell.text = ""
                run = cell.paragraphs[0].add_run(cell_text)
                run.bold = True
                set_run_font(run, size=Pt(8))

        # Data rows
        for i, row_data in enumerate(rows):
            for j, cell_text in enumerate(row_data):
                if j < num_cols:
                    cell = table.rows[i + 1].cells[j]
                    cell.text = ""
                    run = cell.paragraphs[0].add_run(str(cell_text))
                    set_run_font(run, size=Pt(8))

        # Spacing after table
        doc.add_paragraph().space_after = Pt(4)


def _create_blank_doc():
    """Create a blank document with IEEE conference page layout (US Letter, two-column-like margins)."""
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(1.0)
    return doc


def render(content, template_path, output_path):
    """Main rendering function.

    Loads the template, fills it with content, saves to output_path.
    Falls back to a blank IEEE-layout document if the template cannot be loaded.
    """
    doc = None
    if template_path and os.path.exists(template_path):
        try:
            doc = Document(template_path)
            # Clear existing body content
            for p in doc.paragraphs:
                p.clear()
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for p in cell.paragraphs:
                            p.clear()
        except (KeyError, ValueError, OSError) as e:
            print(f"Warning: Could not load template ({e}), using blank IEEE layout.", file=sys.stderr)

    if doc is None:
        doc = _create_blank_doc()

    add_title(doc, content)
    add_authors(doc, content)
    add_abstract(doc, content)
    add_keywords(doc, content)
    add_sections(doc, content)
    add_figures(doc, content)
    add_tables(doc, content)
    add_references(doc, content)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    doc.save(output_path)
    print(f"Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Fill IEEE Word template with manuscript content"
    )
    parser.add_argument(
        "content",
        help="JSON file containing manuscript content",
    )
    parser.add_argument(
        "--template",
        default=None,
        help="Path to IEEE Word template (.docx). If omitted, uses default page layout.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output .docx file path",
    )
    args = parser.parse_args()

    content = load_content(args.content)
    render(content, args.template, args.output)


if __name__ == "__main__":
    main()
