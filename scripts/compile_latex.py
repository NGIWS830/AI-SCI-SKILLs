#!/usr/bin/env python3
"""Compile a LaTeX manuscript to PDF, handling bibtex and multiple passes.

Usage:
    python compile_latex.py manuscript.tex --output-dir build --bibtex refs.bib
"""

import argparse
import os
import re
import shutil
import subprocess
import sys


def find_pdflatex():
    """Find an available LaTeX compiler."""
    for cmd in ["pdflatex", "xelatex", "lualatex"]:
        if shutil.which(cmd):
            return cmd
    return None


def find_bibtex():
    """Find an available BibTeX compiler."""
    for cmd in ["bibtex", "biber"]:
        if shutil.which(cmd):
            return cmd
    return None


def run_latex(compiler, tex_file, output_dir, passes=1):
    """Run LaTeX compiler."""
    for i in range(passes):
        result = subprocess.run(
            [compiler, "-interaction=nonstopmode", "-output-directory", output_dir, tex_file],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            _parse_errors(result.stdout + result.stderr)
            return False
    return True


def run_bibtex(bibtex_cmd, aux_file, output_dir):
    """Run BibTeX on the auxiliary file."""
    aux_name = os.path.splitext(os.path.basename(aux_file))[0]
    result = subprocess.run(
        [bibtex_cmd, aux_name],
        capture_output=True, text=True,
        cwd=output_dir
    )
    if result.returncode != 0:
        print(f"BibTeX warning: {result.stderr[:500]}", file=sys.stderr)
    return True


def _parse_errors(log_text):
    """Parse LaTeX log for errors, warnings, and overfull boxes."""
    errors = re.findall(r'^!(.*?)$', log_text, re.MULTILINE)
    warnings = re.findall(r'^LaTeX Warning:(.*?)$', log_text, re.MULTILINE)
    overfull = re.findall(r'Overfull \\hbox.*?$', log_text, re.MULTILINE)

    if errors:
        print(f"\nLaTeX Errors ({len(errors)}):", file=sys.stderr)
        for e in errors[:10]:
            print(f"  ! {e.strip()}", file=sys.stderr)
    if warnings:
        print(f"\nLaTeX Warnings ({len(warnings)}):", file=sys.stderr)
        for w in warnings[:5]:
            print(f"  Warning: {w.strip()}", file=sys.stderr)
    if overfull:
        print(f"\nOverfull hboxes ({len(overfull)}):", file=sys.stderr)
        for o in overfull[:5]:
            print(f"  {o.strip()}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Compile LaTeX manuscript to PDF")
    parser.add_argument("tex_file", help="Main LaTeX file")
    parser.add_argument("--output-dir", "-o", default="build", help="Output directory")
    parser.add_argument("--bibtex", help="BibTeX file (optional)")
    parser.add_argument("--clean", action="store_true", help="Clean auxiliary files after compilation")
    args = parser.parse_args()

    compiler = find_pdflatex()
    if not compiler:
        print("Error: No LaTeX compiler found. Install texlive or miktex.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    tex_path = os.path.abspath(args.tex_file)
    output_dir = os.path.abspath(args.output_dir)
    tex_dir = os.path.dirname(tex_path)

    print(f"Compiling {os.path.basename(tex_path)} with {compiler}...")

    # Pass 1: Initial compilation
    if not run_latex(compiler, tex_path, output_dir, passes=1):
        print("Initial compilation failed.", file=sys.stderr)
        sys.exit(1)

    # BibTeX pass
    tex_name = os.path.splitext(os.path.basename(tex_path))[0]
    aux_path = os.path.join(output_dir, f"{tex_name}.aux")

    if args.bibtex or os.path.exists(aux_path):
        bibtex_cmd = find_bibtex()
        if bibtex_cmd:
            print(f"Running {bibtex_cmd}...")
            if args.bibtex:
                # Copy the bib file to output dir
                shutil.copy(args.bibtex, os.path.join(output_dir, os.path.basename(args.bibtex)))
            run_bibtex(bibtex_cmd, aux_path, output_dir)

    # Pass 2-3: Resolve references
    run_latex(compiler, tex_path, output_dir, passes=2)

    pdf_path = os.path.join(output_dir, f"{tex_name}.pdf")
    if os.path.exists(pdf_path):
        print(f"PDF generated: {pdf_path}")
    else:
        print("PDF was not generated. Check logs for errors.", file=sys.stderr)
        sys.exit(1)

    # Clean auxiliary files
    if args.clean:
        for ext in [".aux", ".log", ".out", ".toc", ".bbl", ".blg", ".synctex.gz"]:
            aux_file = os.path.join(output_dir, f"{tex_name}{ext}")
            if os.path.exists(aux_file):
                os.remove(aux_file)


if __name__ == "__main__":
    main()
