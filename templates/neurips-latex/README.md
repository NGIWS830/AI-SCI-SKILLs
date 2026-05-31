# NeurIPS / ICML LaTeX Template

## Setup

1. Download official NeurIPS style files from: https://neurips.cc/Conferences/2026/PaperInformation/StyleFiles
2. Place `neurips_2026.sty` in this directory
3. Uncomment the `\usepackage[final]{neurips_2026}` line
4. Remove the temporary `\usepackage[margin=1in]{geometry}` line
5. Compile: `pdflatex template.tex && bibtex template && pdflatex template.tex && pdflatex template.tex`

## NeurIPS vs ICML

| Conference | Pages | Style | Key Difference |
|-----------|-------|-------|----------------|
| NeurIPS | 9 pages + references | `neurips_2026.sty` | Broader Impact statement required; Anonymous by default |
| ICML | 8 pages + references | `icml2026.sty` (separate download) | No Broader Impact requirement; Anonymous by default |

## NeurIPS-Specific Requirements

- **Broader Impact Statement**: Required for camera-ready. Discuss potential societal consequences.
- **Checklist**: NeurIPS requires a paper checklist (reproducibility, ethics, etc.).
- **Code/Data**: Strongly encouraged to release code; reviewers will check.
- **Dual Submission Policy**: Cannot be submitted to other archival venues simultaneously.

## ICML-Specific

- Download ICML style from: https://icml.cc/Conferences/2026/StyleFiles
- Replace `neurips_2026.sty` with `icml2026.sty`
