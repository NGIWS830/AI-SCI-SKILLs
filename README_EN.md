<div align="center">

# AI-SCI-SKILLs

[![Version](https://img.shields.io/badge/version-v0.4.0-blue.svg)](https://github.com/NGIWS830/AI-SCI-SKILLs/releases)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Claude%20Code%20%7C%20Codex%20%7C%20Cursor%20%7C%20Any%20Agent-lightgrey.svg)
![Built with](https://img.shields.io/badge/AI%20Powered-Skill%20%7C%20Pipeline-orange.svg)

English | [中文](README.md)

</div>

---

<div align="center">

<h3><strong>One Skill. One Session. Raw materials → polished English SCI manuscript 🚀</strong></h3>

</div>

---

AI-SCI-SKILLs is a Chinese-first, end-to-end pipeline for writing SCI papers in deep learning, machine learning, computer vision, NLP, multimodal learning, and related AI research areas.


## Triggering the Skill

### Trigger Keywords

The skill activates automatically when any of these keywords appear in conversation (Claude Code natively supports auto-trigger; Codex, Cursor, Copilot, etc. can load `SKILL.md` as context):

`write paper` `SCI paper` `academic paper` `manuscript` `LaTeX paper` `journal paper` `conference paper` `submission` `draft paper` `paper writing` `polish paper` `translate paper` `academic writing` `research paper` `写论文` `论文写作`

### Trigger Phrases

Any of the following (and similar) will trigger the skill:

- "Write an SCI paper from my research materials"
- "Turn these experiment results into a paper"
- "I want to submit to CVPR/ICCV/NeurIPS/ICML/ACL/AAAI..."
- "Help me write a paper from this code and experiment tables"
- "Polish this English manuscript for SCI submission"
- "Translate this Chinese paper into English SCI style"
- "Generate a paper draft from my research notes"
- "Help me write a manuscript for journal submission"

### Targeting Specific Stages

You can also jump directly to a specific stage:

- "Analyze what claims these experiment results can support" (Stage 3)
- "Search the literature on cross-modal retrieval" (Stage 2)
- "Polish and translate this Chinese draft to English SCI" (Stage 4d-4e)

---

## Use Cases

> **One skill, pick your starting point.** This table shows how the same skill auto-detects the right stage based on what materials you provide and what you ask for. These are NOT separate skills — just different entry points into the same pipeline.

| What You Have | What You Want | Start At | Try Saying |
|--------------|---------------|----------|------------|
| Code + experiment tables + notes | Complete English SCI paper | Stage 0-4 Full pipeline | "Write an SCI paper from these materials" (Stage 0-4) |
| Project folder (code + README + configs) | Paper draft | Stage 0-4 Full pipeline | "Generate a paper from this project" (Stage 0-4) |
| Experiment CSV + method description | Results analysis and paper | Stage 3-4 | "Analyze these experiment results and write up the experiments section" (Stage 3-4) |
| Experiment data + method + literature list | English paper | Stage 3-4 | "I have experiment tables and method notes — write the paper" (Stage 3-4) |
| Existing paper + new experiment results | Update experiments section | Stage 3-4 | "Update the paper with these new experiment results" (Stage 3-4) |
| Chinese paper draft | English SCI journal submission | Stage 4d-4e | "Translate this Chinese paper into polished English SCI" (Stage 4d-4e) |
| English draft | Polish + self-critique + template output | Stage 4e-4g | "Polish this English draft and render it into IEEE template" (Stage 4e-4g) |
| Complete English manuscript | Quality check and self-critique | Stage 4f | "Review the quality of this manuscript" (Stage 4f) |
| Scattered notes and ideas | Structured research brief | Stage 1 | "Turn these research notes into a paper outline" (Stage 1) |
| Literature list + research direction | Literature review / Related Work | Stage 2 | "Search and organize literature for this research direction" (Stage 2) |
| Complete Chinese paper | LaTeX / Word template rendering | Stage 4g | "Render this paper into IEEE format" (Stage 4g) |

---

## Pipeline

```
Stage 0: INIT   → Inventory materials, create project state file
Stage 1: DIGEST → Read project materials, produce structured project brief
Stage 2: LIT    → Literature search (API), AI auto-filled matrix, verification, gap analysis, narrative synthesis (matrix→Introduction+Related Work)
Stage 3: EXPER  → Experiment analysis, improvement calculations, claims
Stage 4: WRITE  → 4a Storyline → 4b Chinese draft → 4c Chinese polish
               → 4d EN conversion → 4e EN polish → 4f Self-critique → 4g Template rendering
```

Resumable: if interrupted, reload `SKILL.md` with the existing `project-state.md` and continue from the last completed stage.

---

## Architecture

```
SKILL.md (root entry point)
├── digest/        — Extract paper-ready facts from project materials
│   ├── references/  — Code reading, task taxonomy, evidence rules, brief template
│   └── scripts/     — summarize_repo.py, extract_architecture.py
├── literature/    — Search → auto-fill matrix → verify → gap analysis → narrative synthesis
│   ├── references/  — Search strategies, API guide, citation verification, classic paper maps,
│   │                  literature synthesis guide (matrix→narrative)
│   └── scripts/     — search_literature.py, auto_fill_matrix.py, verify_citations.py,
│                      analyze_citations.py, synthesize_literature.py
├── experiment/    — Analyze experiments and validate claims
│   ├── references/  — Metrics guide, claim rules, ablation writing, reproducibility checklist
│   └── scripts/     — compute_improvements.py, statistical_tests.py, result_visualizer.py
├── writer/        — Chinese draft → polish → EN conversion → EN polish → Self-critique
│   └── references/  — Full section templates, CN-EN translation corpus, terminology glossary, quality rubric
├── scripts/       — Quality checks, LaTeX compilation, BibTeX formatting, Word rendering,
│                    rebuttal generation, paper-to-slides
└── templates/     — 11 conference/journal templates (CN/EN, CV/ML/NLP/AI/RS/CI/IP),
                     Cover Letter
```

---

## Quick Start

### Method 1: Use with Any AI Agent

`SKILL.md` is a universal structured instruction file — not tied to any single platform. Claude Code auto-triggers it natively; Codex, Cursor, GitHub Copilot, and others can load it as system prompt or context.

1. Clone this repository — `SKILL.md` is the entry point.
2. Provide `SKILL.md` as system instructions / context to your AI agent.
3. Say "Write an SCI paper from my research materials" or provide materials and say "Turn these into a paper."
4. The agent walks through all stages from Stage 0. Review and approve at key checkpoints.
5. Final output: English SCI manuscript (LaTeX + Word dual format), Chinese reference manuscript (LaTeX), plus all intermediate files and quality reports.

### Method 2: Standalone Scripts

You can also use individual stage scripts directly:

```bash
# -- Stage 1: Architecture extraction --
python digest/scripts/extract_architecture.py my_project/ --output arch_report.md

# -- Stage 2: Literature search -> fill matrix -> verify -> analyze -> synthesize --
python literature/scripts/search_literature.py "cross-modal retrieval contrastive learning" \
    --sources s2,arxiv --max 30 --output results.md
python literature/scripts/auto_fill_matrix.py results.md \
    --project-brief project_brief.md --output lit_matrix.md
python literature/scripts/verify_citations.py citations.txt --sources crossref,dblp
python literature/scripts/analyze_citations.py lit_matrix.md --output gap_analysis.md
python literature/scripts/synthesize_literature.py lit_matrix.md \
    --project-brief project_brief.md --output synthesis.md

# -- Stage 3: Experiment analysis + statistics + visualization --
python experiment/scripts/compute_improvements.py results.csv \
    --target MyModel --metrics R@1 R@5 R@10 \
    --higher-better R@1 R@5 R@10 --group-cols Dataset --stats --output improvements.md
python experiment/scripts/statistical_tests.py results.csv \
    --target MyModel --metrics R@1 R@5 R@10 \
    --higher-better R@1 R@5 R@10 --output stats_report.md
python experiment/scripts/result_visualizer.py results.csv \
    --target MyModel --metrics R@1 R@5 R@10 --output-dir ./figures/

# -- Stage 4f: Quality checks --
python scripts/check_quality.py output_dir/ --all --output quality_report.md

# -- Stage 4g: Template rendering --
python scripts/render_word.py content.json \
    --template templates/ieee-word/template.docx --output manuscript.docx

# -- Post-submission: Rebuttal + Slides --
python scripts/generate_rebuttal.py reviews.txt --paper paper.md --output rebuttal.md
python scripts/paper_to_slides.py paper.md --format beamer --author "J. Yang" --output slides.tex
```

---

## v0.4.0 Key Features

**Literature Pipeline (Stage 2 — Fully Upgraded)**
- API-automated search (Semantic Scholar / arXiv / CrossRef / DBLP)
- AI auto-fill of literature matrix (Category / Main Idea / Relation / Use in Paper)
- Citation metadata cross-verification
- Temporal trend analysis, venue distribution, method-family clustering, research gap identification
- **Literature narrative synthesis** — automatic conversion of matrix into logically organized Introduction and Related Work prose (by paradigm, not paper-by-paper; includes topic sentences, evolutionary arcs, method differentiation, logical flow verification)

**Statistical Analysis (Stage 3 — NEW)**
- Bootstrap confidence intervals, Cohen's d / Hedges' g effect sizes
- Paired t-test / Wilcoxon signed-rank test
- Multiple comparison correction (Bonferroni / Benjamini-Hochberg)
- Statistical power analysis
- Result visualization: bar charts, ablation waterfall, radar charts, heatmaps, Pareto frontiers

**Architecture Extraction (Stage 1 — NEW)**
- Auto-extract all nn.Module / Flax / Keras subclasses
- Loss function parsing, hyperparameter detection
- Framework identification (PyTorch / JAX / TF / HuggingFace)
- Training infrastructure detection (optimizer, scheduler, mixed precision, distributed training)

**Post-Submission Tools (Stage 4 — NEW)**
- Reviewer rebuttal letter generation (Markdown / LaTeX), comment auto-classification, cross-reviewer consistency check
- Paper-to-slides conversion (Beamer LaTeX / Marp Markdown) + speaker notes

**Quality Scoring System (Stage 4f)**
- 5-dimension rubric: Claims-Evidence Alignment / Citation Completeness / Method Precision / Experiment Rigor / Language Quality
- `scripts/check_quality.py` for automated checks; score ≥80 is submission-ready

**Anti-Overclaim · Dedup · De-AI**
- Banned CN+EN overclaim terms with safe alternatives and self-scan procedures
- Cross-section deduplication rules, AI-flavor detection
- Integrated into Chinese polish, English polish, and self-critique stages

**CN-EN Translation Corpus**
- High-frequency term/sentence mappings, claim-strength mapping (Chinese overclaims → safe English academic equivalents)

**Template Outputs (Stage 4g)**
- 11 conference/journal LaTeX templates: Chinese journal, IEEE Conference, IEEE TGRS (Remote Sensing), IEEE TETCI (Computational Intelligence), IEEE TIP (Image Processing), CVPR/ICCV, NeurIPS/ICML, ACL/EMNLP, AAAI/IJCAI
- IEEE Word template + Cover Letter (LaTeX + Word dual format)

---

## Example Project

`examples/mini-ai-paper-project/` — complete end-to-end example using a **cross-modal text-to-image retrieval** scenario:

| File | Stage | Description |
|------|-------|-------------|
| `materials/project_notes.md` | Input | Realistic research notes |
| `experiments/results.csv` | Input | 5 baselines, 3 datasets |
| `outputs/00_project_brief.md` | Stage 1 | Structured brief with evidence mapping |
| `outputs/02_literature_matrix.md` | Stage 2 | Literature matrix with verification status |
| `outputs/03_experiment_analysis.md` | Stage 3 | Claim analysis with evidence strength |
| `outputs/04_paper_storyline.md` | Stage 4a | Complete storyline |
| `outputs/05_chinese_draft.md` | Stage 4b | Chinese first draft |
| `outputs/08_english_polished.md` | Stage 4e | Final polished English manuscript |
| `outputs/10_critique_report.md` | Stage 4f | Quality self-critique report |

---

## Dependencies

```
python >= 3.8
requests, python-docx, pylatexenc
```

Install:

```bash
pip install requests python-docx pylatexenc
```

Optional dependencies:

```bash
pip install matplotlib          # result_visualizer.py for charts
pip install anthropic           # auto_fill_matrix.py / synthesize_literature.py --auto mode
```

LaTeX compilation (Stage 4g only) requires a local TeX Live or MiKTeX installation.

---

## Development

```bash
# Run tests
python -m unittest discover -s tests

# Package full suite
python scripts/package_skills.py --output-dir dist
```

---

## Safety Principles

- **No fabrication**: citations, DOIs, datasets, baselines, metrics, experiments, line numbers, or claims.
- Mark missing author input as `AUTHOR_INPUT_NEEDED`.
- Mark missing citations as `[CITATION NEEDED]`.
- **Preserve scientific meaning over fluency** during polishing, translation, and editing.
