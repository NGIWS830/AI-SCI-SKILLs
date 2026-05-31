# Mini AI Paper Project Example

This example demonstrates the complete AI-SCI-SKILLs v0.3 workflow with a realistic scenario: **Cross-Modal Feature Alignment for Text-to-Image Retrieval**.

## Scenario

The project is a cross-modal retrieval method that improves text-to-image search by aligning visual and textual features in a shared embedding space. The method introduces a **Semantic-Guided Alignment (SGA)** module with a **Hierarchical Matching Loss (HML)**.

## What This Example Shows

The numbered output files correspond to sequential pipeline stages:

| File | Stage | What It Demonstrates |
|------|-------|---------------------|
| `materials/project_notes.md` | Input | Realistic research notes with method description, datasets, known limitations |
| `experiments/results.csv` | Input | Experiment table with 5 baselines, 3 datasets, metrics + std |
| `outputs/00_project_brief.md` | Stage 1 (DIGEST) | Structured brief with evidence mapping |
| `outputs/02_literature_matrix.md` | Stage 2 (LIT) | Literature matrix with verified citations |
| `outputs/03_experiment_analysis.md` | Stage 3 (EXPER) | Claim analysis with evidence strength |
| `outputs/03a_improvement_summary.md` | Stage 3 (EXPER) | Quantitative improvement calculations |
| `outputs/04_paper_storyline.md` | Stage 4a | Complete storyline with evidence mapping |
| `outputs/04a_reference_style_outline.md` | Stage 4a | Full paper outline |
| `outputs/05_chinese_draft.md` | Stage 4b | Complete Chinese first draft |
| `outputs/06_chinese_polished.md` | Stage 4c | Polished Chinese manuscript |
| `outputs/07_english_draft.md` | Stage 4d | CN→EN converted draft |
| `outputs/08_english_polished.md` | Stage 4e | Final polished English manuscript |
| `outputs/09_revision_notes.md` | Stage 4e | CN-EN consistency and terminology checks |
| `outputs/10_critique_report.md` | Stage 4f | Quality self-critique with rubric scores |

## How to Use

1. Load `SKILL.md` into the agent.
2. Point it to this directory and run the full pipeline.
3. The agent will produce outputs matching the files shown here.
4. Use the critique report (Stage 4f) to judge paper readiness.

## Running Experiment Scripts

```bash
python experiment/scripts/compute_improvements.py examples/mini-ai-paper-project/experiments/results.csv \
    --target SGA-Ours \
    --metrics R@1 R@5 R@10 \
    --higher-better R@1 R@5 R@10 \
    --group-cols Dataset \
    --output examples/mini-ai-paper-project/outputs/03a_improvement_summary.md
```
