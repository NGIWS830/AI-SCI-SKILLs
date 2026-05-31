# CVPR / ICCV LaTeX Template

## Setup

1. Download the official CVPR kit from: https://cvpr.thecvf.com/author_guidelines
2. Place `cvpr.sty` and `ieee_fullname.bst` in this directory
3. Uncomment the `\usepackage{cvpr}` line in `template.tex`
4. Remove the temporary `\usepackage[margin=1in]{geometry}` line
5. Compile: `pdflatex template.tex && bibtex template && pdflatex template.tex && pdflatex template.tex`

## CVPR vs ICCV

Both CVPR and ICCV use the same template format. The only change is:
- `\def\confName{CVPR}` or `\def\confName{ICCV}`

## Page Limits

| Conference | Main Paper | References | Supplemental |
|-----------|-----------|------------|--------------|
| CVPR 2025+ | 8 pages | unlimited | unlimited |
| ICCV 2025 | 8 pages | unlimited | unlimited |

## Key Requirements

- Anonymous submission: NO author names, affiliations, or acknowledgments in the initial submission.
- Do NOT use the `\cvprfinalcopy` command until the camera-ready version.
- Figures must be legible in grayscale (though color is allowed).
- Supplemental material as a separate PDF.
