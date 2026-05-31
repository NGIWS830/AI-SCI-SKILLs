# AAAI / IJCAI LaTeX Template

## Setup

1. Download official AAAI Author Kit from: https://aaai.org/authorkit24-2/
2. Place `aaai24.sty` and `aaai24.bst` in this directory
3. Uncomment the `\usepackage{aaai24}` line
4. Remove the temporary `\usepackage[margin=1in]{geometry}` line
5. Compile: `pdflatex template.tex && bibtex template && pdflatex template.tex && pdflatex template.tex`

## AAAI vs IJCAI

| Conference | Full Name | Style | Pages | Frequency |
|-----------|-----------|-------|-------|-----------|
| AAAI | Assoc. for the Advancement of AI | `aaai24.sty` | 7 pages + refs | Annual (Feb) |
| IJCAI | Int'l Joint Conference on AI | `ijcai24.sty` (separate) | 7 pages + refs | Annual (Aug, odd years) |

## Key Requirements

- **Broad AI audience**: AAAI reviewers span ALL AI subfields. Write the introduction and abstract so a non-specialist can understand your contribution.
- **Anonymous submission**: Double-blind review.
- **Page limit**: 7 pages + up to 2 additional pages for references and appendices (check current CFP — this varies by year).
- **Reproducibility**: AAAI encourages code release and has a reproducibility checklist.
- **Two-column format**: All figures and tables must fit within columns (use `table*`/`figure*` for full-width).

## Formatting Notes

- Use Times Roman font family (provided by `times` package)
- Do NOT use `\vspace` or `\vskip` to squeeze more content
- Do NOT change font sizes from the defaults
- Reference style: `(Author, Year)` format via aaai24.bst
