# ACL / EMNLP / NAACL LaTeX Template

## Setup

1. Download official ACL style files: https://acl-org.github.io/ACLPUB/
2. Place `acl.sty` and `acl_natbib.bst` in this directory
3. Uncomment the `\usepackage[review]{acl}` line
4. Remove the temporary `\usepackage[margin=1in]{geometry}` line
5. Compile: `pdflatex template.tex && bibtex template && pdflatex template.tex && pdflatex template.tex`

## ACL Conference Family

| Conference | Full Name | Typical Month |
|-----------|-----------|---------------|
| ACL | Association for Computational Linguistics | July-August |
| EMNLP | Empirical Methods in Natural Language Processing | November-December |
| NAACL | North American Chapter of the ACL | June-July |
| EACL | European Chapter of the ACL | March-April |
| AACL | Asia-Pacific Chapter of the ACL | November-December |

## Key Requirements

- **Anonymous**: All *ACL conferences use double-blind review; remove author info for initial submission.
- **Limitations section**: REQUIRED. Discuss computational requirements, language coverage, domain specificity.
- **Ethics Statement**: REQUIRED. Discuss data privacy, bias, potential misuse.
- **Citation style**: Use `\citep{}` and `\citet{}` (natbib). NOT numeric citations.
- **Page limit**: 8 pages (long paper) or 4 pages (short paper) + unlimited references.

## ACL-specific Formatting

- Use `\begin{table*}` for full-width tables
- NLP terminology should be precise (e.g., "accuracy" vs "precision" vs "F1")
- Include BLEU/ROUGE/BERTScore for generation tasks
- Report statistical significance with bootstrap or paired t-test
