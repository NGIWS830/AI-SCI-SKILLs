# AI-SCI-SKILLs v0.2

[中文版本](README.md)

---

AI-SCI-SKILLs is a Chinese-first, end-to-end pipeline for writing SCI papers in deep learning, machine learning, computer vision, natural language processing, multimodal learning, and related AI research areas.

**One skill. One session. Raw materials → polished English manuscript.**

### Architecture

v0.2 replaces the v0.1 "5 independent skills" model with a unified pipeline:

```
SKILL.md (root entry point)
├── digest/        — Extract paper-ready facts from project materials
├── literature/    — Search, verify, and organize literature
├── experiment/    — Analyze experiments and validate claims
└── writer/        — Chinese draft → polish → EN conversion → EN polish
```

Each module contains `references/` (detailed domain guidance) and optional `scripts/`. The root `SKILL.md` orchestrates the full pipeline, saving progress to a shared `project-state.md` file after each stage.

### Pipeline

```
Stage 0: INIT   → Inventory materials, create project state
Stage 1: DIGEST → Read project materials, produce project brief
Stage 2: LIT    → Literature search, verification, matrix
Stage 3: EXPER  → Experiment analysis, improvement calc, claims
Stage 4: WRITE  → Chinese draft → polish → EN conversion → EN polish
```

The pipeline is resumable: if interrupted, reload `SKILL.md` and point to the existing `project-state.md` to continue from the last completed stage.

### Quick Start

1. Load `SKILL.md` into any agent that supports markdown-based skill definitions.
2. Provide your research materials: code, notes, experiment tables, framework diagrams, literature.
3. The agent walks through all 5 stages automatically. You review and approve at key checkpoints.
4. Output: a polished English SCI manuscript plus all intermediate files.

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

See `examples/mini-ai-paper-project/` for a minimal end-to-end sample containing:

- project notes
- an experiment CSV
- a project brief
- a literature matrix with citation gaps
- an experiment analysis
- a paper storyline
- a Chinese draft excerpt

Run the experiment helper on the example:

```bash
python experiment/scripts/compute_improvements.py examples/mini-ai-paper-project/experiments/results.csv --target Ours --metrics Acc F1 Params --higher-better Acc F1 --lower-better Params --group-cols Dataset --output examples/mini-ai-paper-project/outputs/03a_improvement_summary.md
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
