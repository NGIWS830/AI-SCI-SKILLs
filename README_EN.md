# AI-SCI-SKILLs v0.3

[中文](README.md)

---

**One skill. One session. Raw materials → polished English SCI manuscript.**

AI-SCI-SKILLs is a Chinese-first, end-to-end pipeline for writing SCI papers in deep learning, machine learning, computer vision, NLP, multimodal learning, and related AI research areas.

---

## Triggering the Skill

### Trigger Keywords

The skill activates automatically when any of these keywords appear in conversation:

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
Stage 2: LIT    → Literature search (API-automated), verification, matrix
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
│   └── references/  — Code reading, task taxonomy, evidence rules, brief template
├── literature/    — Search, verify, and organize literature
│   ├── references/  — Search strategies, API guide, citation verification, classic paper maps
│   └── scripts/     — search_literature.py, verify_citations.py
├── experiment/    — Analyze experiments and validate claims
│   └── references/  — Metrics guide, claim rules, ablation writing, reproducibility checklist
├── writer/        — Chinese draft → polish → EN conversion → EN polish → Self-critique
│   └── references/  — Full section templates, CN-EN translation corpus, terminology glossary, quality rubric
├── scripts/       — Quality checks, LaTeX compilation, figure extraction, BibTeX formatting, Word rendering
└── templates/     — Chinese journal, IEEE LaTeX, IEEE Word, Cover Letter templates
```

---

## Quick Start

### Method 1: Use with Claude Code

1. Clone this repository — `SKILL.md` is the skill entry point.
2. Say "Write an SCI paper from my research materials" or provide materials and say "Turn these into a paper."
3. The agent walks through all stages from Stage 0. Review and approve at key checkpoints.
4. Final output: English SCI manuscript (LaTeX + Word dual format), Chinese reference manuscript (LaTeX), plus all intermediate files and quality reports.

**Note:** This is a Claude Code skill. `SKILL.md` is loaded automatically — no extra configuration needed.

### Method 2: Standalone Scripts

You can also use individual stage scripts directly:

```bash
# Literature search
python literature/scripts/search_literature.py "cross-modal retrieval contrastive learning" \
    --sources s2,arxiv --max 20 --output results.md

# Compute experiment improvements
python experiment/scripts/compute_improvements.py results.csv \
    --target MyModel --metrics R@1 R@5 R@10 \
    --higher-better R@1 R@5 R@10 --group-cols Dataset --output improvements.md

# Quality checks
python scripts/check_quality.py output_dir/ --all --output quality_report.md

# Render Word manuscript
python scripts/render_word.py content.json \
    --template templates/ieee-word/template.docx --output manuscript.docx
```

---

## v0.3 Key Features

**Quality Scoring System (Stage 4f)**
- 5-dimension rubric: Claims-Evidence Alignment / Citation Completeness / Method Precision / Experiment Rigor / Language Quality
- `scripts/check_quality.py` for automated checks; score ≥80 is submission-ready

**Anti-Overclaim · Dedup · De-AI**
- Banned CN+EN overclaim terms with safe alternatives and self-scan procedures
- Cross-section deduplication rules, AI-flavor detection
- Integrated into Chinese polish, English polish, and self-critique stages

**API-Automated Literature Search & Citation Verification**
- Semantic Scholar / arXiv automated search
- CrossRef / DBLP citation metadata verification

**CN-EN Translation Corpus**
- High-frequency term/sentence mappings, claim-strength mapping (Chinese overclaims → safe English academic equivalents)

**Template Outputs (Stage 4g)**
- Chinese LaTeX (generic Chinese journal format)
- English LaTeX (IEEE conference format)
- English Word (IEEE conference format)
- Cover Letter (LaTeX + Word dual format)

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
