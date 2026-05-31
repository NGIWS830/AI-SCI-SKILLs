---
name: ai-sci-skills
description: End-to-end automated SCI paper writing for deep learning, machine learning, computer vision, NLP, multimodal learning, and related AI research. Chinese-first pipeline: raw project materials → structured digest → literature review → experiment analysis → polished English manuscript. Use when the user wants to write a complete SCI paper from code, notes, experiment tables, framework diagrams, or mixed research materials.
---

# AI SCI Paper Writer v0.2

## Mission

One-stop pipeline that takes raw research materials and produces a polished English SCI manuscript. Default to Chinese-first writing unless the user explicitly asks for direct English drafting.

## Pipeline Overview

```
STAGE 0: INIT     → Inventory materials, create project state file
STAGE 1: DIGEST   → Extract paper-ready facts from project materials
STAGE 2: LIT      → Search, verify, organize literature
STAGE 3: EXPER    → Analyze experiments, compute improvements, validate claims
STAGE 4: WRITE    → Chinese draft → Chinese polish → EN conversion → EN polish
```

Each stage saves its output to a shared project state file. The pipeline can be paused and resumed at any stage.

## Getting Started

When the user provides research materials, always begin at Stage 0. Ask for the project output directory where state files will be saved.

If the user points to an existing `project-state.md` file, read the `**Status**` field and resume from that stage.

---

## STAGE 0: INIT — Material Inventory & State Setup

### Purpose
Inventory all user-provided materials and create a project state file that tracks the pipeline.

### Actions
1. Ask the user for: project output directory, target venue/journal, and any specific requirements.
2. Identify every provided material: code repos, README, configs, logs, experiment tables (CSV/Excel), framework diagrams, notes (Word/TXT/Markdown), prior drafts, literature lists.
3. Create `<output_dir>/project-state.md` with this structure:

```markdown
# Project State — [Paper Title or Placeholder]

**Status**: STAGE 0 | INIT
**Created**: YYYY-MM-DD
**Last Updated**: YYYY-MM-DD

## Available Materials

| # | Type | Path/Description | Notes |
|---|------|-----------------|-------|
| 1 |       |                  |       |

## Target Venue & Requirements

## Pipeline Progress

- [ ] Stage 1: DIGEST
- [ ] Stage 2: LIT
- [ ] Stage 3: EXPER
- [ ] Stage 4: WRITE

## Stage Outputs

### Stage 1 Output (DIGEST)
*(empty — run Stage 1 to populate)*

### Stage 2 Output (LIT)
*(empty)*

### Stage 3 Output (EXPER)
*(empty)*

### Stage 4 Output (WRITE)
*(empty)*

## Missing Author Inputs
*(populated across stages)*

## Paper Storyline
*(populated after Stage 1)*
```

4. Update `**Status**` to `STAGE 1 | DIGEST`. Advance to Stage 1.

---

## STAGE 1: DIGEST — Project Digestion

### Purpose
Extract paper-ready facts from project materials. Produce a structured project brief.

### Required Inputs
- All materials listed in the project state file

### References
Read these files for detailed guidance:
- `digest/references/code-reading-guide.md` — code/material inspection methodology
- `digest/references/cv-nlp-task-taxonomy.md` — task classification
- `digest/references/method-evidence-rules.md` — evidence-grounding rules
- `digest/references/project-brief-template.md` — output template

### Actions
1. Read all available materials thoroughly.
2. Extract: research task, problem motivation, method pipeline, core modules, datasets, baselines, metrics, training/inference flow.
3. Link every method claim to concrete evidence from the materials.
4. Propose contribution candidates. Distinguish evidence-backed facts from interpretation.
5. If code is available, optionally run `digest/scripts/summarize_repo.py <repo_path>` for a file inventory.

### Output
Save to the project state file under `### Stage 1 Output (DIGEST)`:

```markdown
## Research Task
## Problem Motivation
## Method Overview
## Core Modules and Evidence
| Module | Role | Evidence Source | Confidence |
|---|---|---|---|
## Method Innovation Slots for Manuscript
| Subsection | Innovation/Module | Evidence Source | Missing Details |
|---|---|---|---|
| III-B |  |  |  |
| III-C |  |  |  |
## Data Flow
## Datasets, Baselines, and Metrics
## Candidate Contributions
## Claims Supported by Current Materials
## Missing Information
## Paper-Writing Risks
```

### Transition
1. Update `**Status**` to `STAGE 2 | LIT`.
2. Mark `[x] Stage 1: DIGEST` in the pipeline progress.
3. If all needed inputs are present, advance to Stage 2. Otherwise, ask the user to provide missing information before proceeding.

---

## STAGE 2: LIT — Literature Review

### Purpose
Build verified literature support: classic foundations, recent SOTA, method-family papers, dataset papers, and gap evidence.

### Required Inputs
- Stage 1 output (research task, method family, datasets, candidate contributions)
- User-provided literature (if any)
- Target venue

### References
Read these files for detailed guidance:
- `literature/references/search-strategies.md` — query patterns
- `literature/references/citation-verification.md` — before finalizing references
- `literature/references/cv-classic-papers.md` — seed map: CV
- `literature/references/nlp-classic-papers.md` — seed map: NLP
- `literature/references/multimodal-classic-papers.md` — seed map: multimodal
- `literature/references/related-work-patterns.md` — prose structure
- `literature/references/literature-matrix-template.md` — output template

### Actions
1. Derive search queries from the task, method family, datasets, and claims (see `search-strategies.md`).
2. Search for: classic papers, recent SOTA, method-family papers, dataset/benchmark papers, gap-supporting papers.
3. Verify every citation. Never fabricate DOI, arXiv ID, venue, year, or authors.
4. Build the literature matrix.
5. Draft related-work structure organized by themes, not paper-by-paper.

### Output
Save to the project state file under `### Stage 2 Output (LIT)`:

```markdown
## Search Queries
## Literature Matrix
| Category | Paper | Year | Venue | Main Idea | Relation to Our Work | Use in Paper | Verification |
|---|---:|---:|---|---|---|---|---|
## Related Work Structure
## Research Gap Evidence
## Citation Gaps
```

### Transition
1. Update `**Status**` to `STAGE 3 | EXPER`.
2. Mark `[x] Stage 2: LIT` in the pipeline progress.
3. Mark unverified citations as `[CITATION NEEDED]`.
4. Advance to Stage 3.

---

## STAGE 3: EXPER — Experiment Analysis

### Purpose
Convert experiment artifacts into evidence-grounded result claims. Calculate improvements, validate claims, flag risks.

### Required Inputs
- Experiment tables (CSV/Excel/screenshots/logs) from materials
- Stage 1 output (datasets, baselines, metrics)
- Stage 2 output (SOTA baseline numbers from literature, if available)

### References
Read these files for detailed guidance:
- `experiment/references/metrics-guide.md` — metric directions
- `experiment/references/result-claim-rules.md` — before writing claims
- `experiment/references/ablation-writing.md` — ablation interpretation
- `experiment/references/experiment-section-patterns.md` — section structure
- `experiment/references/reproducibility-checklist.md` — completeness check

### Script
When CSV/Excel tables are provided, run:
```bash
python experiment/scripts/compute_improvements.py <table_path> --target <method_name> --metrics <m1,m2,...> --higher-better <m1,m2> --lower-better <m3> --group-cols <col> --output <output_dir>/03a_improvement_summary.md
```

### Actions
1. Identify table types: main results, ablation, robustness, efficiency, hyperparameter, qualitative, failure cases.
2. Identify datasets, metrics, metric direction (higher/lower is better), baselines, and proposed method.
3. Calculate absolute and relative improvements.
4. Map each possible paper claim to concrete evidence.
5. Draft results and analysis paragraphs in Chinese first unless user requests English.

### Output
Save to the project state file under `### Stage 3 Output (EXPER)`:

```markdown
## Tables Analyzed
## Main Results
## Improvement over Baselines
## Ablation Findings
## Efficiency / Complexity Findings
## Robustness / Generalization Findings
## Claims Supported by Evidence
| Claim | Evidence | Strength | Caveat |
|---|---|---|---|
## Missing Experiments or Metadata
## Risks of Overclaiming
## Draft Results Paragraphs (Chinese)
```

### Transition
1. Update `**Status**` to `STAGE 4 | WRITE`.
2. Mark `[x] Stage 3: EXPER` in the pipeline progress.
3. Advance to Stage 4.

---

## STAGE 4: WRITE — Paper Drafting & Polishing

### Purpose
Produce a complete SCI manuscript through the Chinese-first pipeline: Chinese draft → Chinese academic polish → English SCI conversion → English polish.

### Required Inputs
- Stage 1 output: project brief, contribution claims, method modules
- Stage 2 output: literature matrix, related work structure
- Stage 3 output: experiment analysis, result claims, draft results paragraphs
- Target venue format requirements

### References
Read in order as each sub-stage progresses:
- `writer/references/reference-paper-structure.md` — manuscript skeleton (read first)
- `writer/references/paper-storyline.md` — storyline before drafting
- `writer/references/title-patterns.md` — title
- `writer/references/abstract-patterns.md` — abstract
- `writer/references/introduction-patterns.md` — introduction
- `writer/references/related-work-patterns.md` — related work
- `writer/references/method-section-patterns.md` — method
- `writer/references/experiment-section-patterns.md` — experiments
- `writer/references/conclusion-patterns.md` — conclusion
- `writer/references/discussion-patterns.md` — discussion
- `writer/references/chinese-draft-patterns.md` — Chinese first draft
- `writer/references/chinese-polishing-rules.md` — Chinese academic polish
- `writer/references/chinese-to-english-writing-rules.md` — CN→EN conversion
- `writer/references/english-polishing-rules.md` — English refinement
- `writer/references/forbidden-overclaims.md` — before finalizing claims
- `writer/references/ai-terminology-glossary.md` — bilingual term consistency

### Sub-stages

#### 4a: Paper Storyline
Before drafting, produce a storyline summary saved to state file:
```markdown
## Paper Storyline
- Problem: (one sentence)
- Gap: (one sentence)
- Method: (2-3 sentences, module-level)
- Evidence: (key results supporting the method)
- Contribution: (one sentence, aligned with evidence)
```

#### 4b: Chinese Draft (`05_chinese_draft.md`)
1. Read `writer/references/reference-paper-structure.md` for the manuscript skeleton.
2. Build the outline. Keep top-level sections: Title, Abstract, Index Terms, I Introduction, II Related Work, III Proposed Method, IV Experiments, V Conclusion, References.
3. Rewrite second-level headings for the user's own method, datasets, and evidence.
4. Generate Chinese draft for each section using `writer/references/chinese-draft-patterns.md`.
5. Save to `<output_dir>/05_chinese_draft.md`.

#### 4c: Chinese Polish (`06_chinese_polished.md`)
1. Polish the Chinese draft using `writer/references/chinese-polishing-rules.md`.
2. Improve academic clarity and logic. Preserve scientific meaning over fluency.
3. Save to `<output_dir>/06_chinese_polished.md`.

#### 4d: CN→EN Conversion (`07_english_draft.md`)
1. Convert polished Chinese to English SCI prose using `writer/references/chinese-to-english-writing-rules.md`.
2. Maintain terminology consistency using `writer/references/ai-terminology-glossary.md`.
3. Save to `<output_dir>/07_english_draft.md`.

#### 4e: English Polish (`08_english_polished.md`)
1. Polish English manuscript using `writer/references/english-polishing-rules.md`.
2. Check claims against `writer/references/forbidden-overclaims.md`.
3. Produce revision notes (`09_revision_notes.md`): CN-EN consistency, terminology check, claims alignment.
4. Save final manuscript to `<output_dir>/08_english_polished.md`.

### Output Files
```
<output_dir>/
├── project-state.md
├── 05_chinese_draft.md
├── 06_chinese_polished.md
├── 07_english_draft.md
├── 08_english_polished.md
└── 09_revision_notes.md
```

### Transition
1. Update `**Status**` to `DONE`.
2. Mark `[x] Stage 4: WRITE` in the pipeline progress.
3. The pipeline is complete. Summarize the output files produced.

---

## Resuming from a Saved State

When the user provides a `project-state.md` file:
1. Read the `**Status**` field to identify the current stage (the one to resume from).
2. Check `Pipeline Progress` checkboxes to confirm which stages are already done.
3. Load the completed stages' outputs from `Stage Outputs` — you already have them.
4. If materials were added since last run, update Available Materials first.

---

## Non-Negotiable Rules

Apply at every stage:

- **No fabrication**: Never invent citations, DOI, arXiv IDs, datasets, baselines, metrics, experiments, line numbers, or claims.
- **Mark missing info**: Use `AUTHOR_INPUT_NEEDED` when author input is required. Use `[CITATION NEEDED]` for unverified citations.
- **Preserve meaning over fluency**: During Chinese polishing, translation, and English polishing, never alter scientific meaning to improve wording.
- **Do not add unsupported content**: Do not add experiments, citations, methods, or conclusions not backed by provided materials.
- **Do not strengthen claims**: Claims must match the evidence level from experiments. Never upgrade a weak finding to a strong claim.
- **Keep terminology consistent**: Across Chinese and English, use consistent technical terms (see `writer/references/ai-terminology-glossary.md`).
- **Use "percentage points"** for absolute differences in percent-like metrics. Use "relative improvement" only when calculated.
- **State metric direction**: Always clarify whether higher or lower is better.

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `digest/scripts/summarize_repo.py <path>` | Quick file inventory of a code repo |
| `experiment/scripts/compute_improvements.py <csv> --target <name> --metrics <m1,m2> --higher-better <m1> --lower-better <m2> --group-cols <col> --output <path>` | Compute pairwise improvements from CSV |

## Module Reference Index

| Module | Directory | What it provides |
|--------|-----------|-----------------|
| Digest | `digest/references/` | Code reading, task taxonomy, evidence rules, project brief template |
| Literature | `literature/references/` | Search strategies, citation verification, classic paper maps, related work patterns, literature matrix template |
| Experiment | `experiment/references/` | Metrics guide, claim rules, ablation writing, experiment section patterns, reproducibility checklist |
| Writer | `writer/references/` | Full writing pipeline: title, abstract, introduction, related work, method, experiments, conclusion, discussion patterns; Chinese drafting/polishing; CN→EN conversion; English polishing; forbidden overclaims; terminology glossary |
