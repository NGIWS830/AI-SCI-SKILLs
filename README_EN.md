# AI-SCI-SKILLs v0.3

[中文](README.md)

---

AI-SCI-SKILLs is a Chinese-first, end-to-end pipeline for writing SCI papers in deep learning, machine learning, computer vision, natural language processing, multimodal learning, and related AI research areas.

**One skill. One session. Raw materials → polished English manuscript.**

### Architecture

v0.3 deep upgrade on the unified pipeline: enriched reference files, API automation, quality scoring system, and self-critique stage.

```
SKILL.md (root entry point)
├── digest/        — Extract paper-ready facts from project materials
│   └── references/  — Code reading, task taxonomy, evidence rules, brief template
├── literature/    — Search, verify, and organize literature
│   ├── references/  — Search strategies, API guide, citation verification, classic paper maps, related work patterns
│   └── scripts/     — search_literature.py, verify_citations.py (API automation)
├── experiment/    — Analyze experiments and validate claims
│   └── references/  — Metrics guide, claim rules, ablation writing, reproducibility checklist
├── writer/        — Chinese draft → polish → EN conversion → EN polish → Self-critique
│   └── references/  — Full section templates, CN-EN translation corpus, terminology glossary, quality rubric
└── scripts/       — Quality checks, LaTeX compilation, figure extraction, BibTeX formatting, packaging
```

### Pipeline

```
Stage 0: INIT   → Inventory materials, create project state
Stage 1: DIGEST → Read project materials, produce project brief
Stage 2: LIT    → Literature search (API automated), verification, matrix
Stage 3: EXPER  → Experiment analysis, improvement calc, claims
Stage 4: WRITE  → 4a Storyline → 4b Chinese draft → 4c Chinese polish → 4d EN conversion → 4e EN polish → 4f Self-critique
```

The pipeline is resumable: if interrupted, reload `SKILL.md` and point to the existing `project-state.md` to continue from the last completed stage.

### What's New in v0.3

**API-Automated Literature Search & Citation Verification**
- `literature/scripts/search_literature.py` — Search via Semantic Scholar and arXiv APIs
- `literature/scripts/verify_citations.py` — Verify citation metadata via CrossRef and DBLP
- Query derivation procedure: extract keywords from Stage 1 outputs, compose query variants, merge and deduplicate

**Quality Scoring System (Stage 4f Self-Critique)**
- 5-dimension scoring rubric (Claims-Evidence Alignment / Citation Completeness / Method Precision / Experiment Rigor / Language Quality)
- `scripts/check_quality.py` — Automated quality checks on generated papers
- `writer/references/quality-rubric.md` — Detailed scoring criteria
- Score ≥80: ready; 70-79: needs fixes; <70: return for substantive revision

**Chinese-English Translation Corpus**
- `writer/references/cn-en-translation-corpus.md` — High-frequency term and sentence pattern mappings
- Claim-strength mapping: common Chinese overclaims → safe English academic equivalents

**Writing Tool Scripts**
- `scripts/compile_latex.py` — Compile LaTeX manuscript to PDF
- `scripts/extract_figures.py` — Extract figures from papers
- `scripts/format_bibtex.py` — Validate and normalize BibTeX entries

**Enhanced Prompt Engineering**
- Chain-of-thought guidance at each stage
- Role instructions for each writing sub-stage
- Polish checklists (10-item checklist for Chinese and English)
- Few-shot examples for CV and NLP domains

### Quick Start

1. Load `SKILL.md` into any agent that supports markdown-based skill definitions.
2. Provide your research materials: code, notes, experiment tables, framework diagrams, literature.
3. The agent walks through all stages automatically. You review and approve at key checkpoints.
4. Output: a polished English SCI manuscript plus all intermediate files and quality reports.

### Package

Package the full suite:

```bash
python scripts/package_skills.py --output-dir dist
```

Package a single module:

```bash
python scripts/package_skills.py --module experiment --output-dir dist
```

### Example Project

See `examples/mini-ai-paper-project/` for a complete end-to-end example using a **cross-modal text-to-image retrieval** scenario:

| File | Stage | What It Demonstrates |
|------|-------|---------------------|
| `materials/project_notes.md` | Input | Realistic research notes |
| `experiments/results.csv` | Input | Experiment table with 5 baselines, 3 datasets |
| `outputs/00_project_brief.md` | Stage 1 | Structured brief with evidence mapping |
| `outputs/02_literature_matrix.md` | Stage 2 | Literature matrix with verification status |
| `outputs/03_experiment_analysis.md` | Stage 3 | Claim analysis with evidence strength |
| `outputs/03a_improvement_summary.md` | Stage 3 | Quantitative improvement calculations |
| `outputs/04_paper_storyline.md` | Stage 4a | Complete storyline with evidence mapping |
| `outputs/05_chinese_draft.md` | Stage 4b | Chinese first draft |
| `outputs/06_chinese_polished.md` | Stage 4c | Polished Chinese manuscript |
| `outputs/07_english_draft.md` | Stage 4d | CN→EN converted draft |
| `outputs/08_english_polished.md` | Stage 4e | Final polished English manuscript |
| `outputs/09_revision_notes.md` | Stage 4e | Revision notes |
| `outputs/10_critique_report.md` | Stage 4f | Quality self-critique report |

Run the experiment helper on the example:

```bash
python experiment/scripts/compute_improvements.py examples/mini-ai-paper-project/experiments/results.csv \
    --target SGA-Ours \
    --metrics R@1 R@5 R@10 \
    --higher-better R@1 R@5 R@10 \
    --group-cols Dataset \
    --output examples/mini-ai-paper-project/outputs/03a_improvement_summary.md
```

Run literature search:

```bash
python literature/scripts/search_literature.py "cross-modal retrieval contrastive learning" \
    --sources s2,arxiv --max 20 \
    --output examples/mini-ai-paper-project/outputs/02a_search_results.md
```

Run quality checks:

```bash
python scripts/check_quality.py examples/mini-ai-paper-project/outputs --all \
    --output examples/mini-ai-paper-project/outputs/10a_auto_check.md
```

### Development Checks

Run the offline test suite:

```bash
python -m unittest discover -s tests
```

### Safety Principles

- Do not fabricate citations, DOI, arXiv IDs, datasets, baselines, metrics, experiments, line numbers, or claims.
- Mark missing author input as `AUTHOR_INPUT_NEEDED`.
- Mark missing citations as `[CITATION NEEDED]`.
- Preserve scientific meaning over fluency during Chinese polishing, translation, and English polishing.
