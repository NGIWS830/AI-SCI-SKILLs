# Project Brief Template

```markdown
# Project Brief

## One-Sentence Summary

## Research Field and Task

## Input and Output

## Problem Addressed

## Proposed Method

## Core Components
| Component | Description | Evidence |
|---|---|---|

## Method Innovation Slots for Manuscript
| Manuscript Subsection | Innovation / Module | Evidence | Missing Details |
|---|---|---|---|
| III-B | AUTHOR_INPUT_NEEDED |  |  |
| III-C | AUTHOR_INPUT_NEEDED |  |  |
| III-D | AUTHOR_INPUT_NEEDED |  |  |

## Training and Inference Pipeline

## Datasets

## Baselines

## Metrics

## Key Results Available

## Candidate Contributions

## Author Inputs Needed

## Risks Before Paper Writing
```

## Guiding Questions per Section

### One-Sentence Summary
- If you could only tell one colleague about this work in 30 seconds, what would you say?
- What is the ONE thing the reader should remember?

### Research Field and Task
- Is this CV, NLP, multimodal, or another field?
- What is the specific task? (classification, detection, segmentation, retrieval, generation, QA, NER, etc.)
- Is this a standard task or a novel problem formulation?

### Problem Addressed
- What specific problem does this work solve?
- Why do existing methods fail at this problem? (The "because" — root cause, not just symptom.)
- Who cares about this problem? (Researchers? Practitioners? Both?)

### Proposed Method
- What is the method's name? (If the author has one. Otherwise, propose a placeholder.)
- What is the core mechanism? (1-2 sentences — the "elevator pitch" of the method.)
- What makes it different from existing approaches?
- Is the method plug-and-play or does it require a specific architecture?

### Core Components
Each component should answer:
- What does this component do? (Function)
- How does it do it? (Mechanism, at a high level)
- Why is it needed? (Motivation — what gap does it fill?)
- Where is the evidence? (Code file, diagram, author note)

### Method Innovation Slots
Map components to manuscript subsections. Common mapping:
- III-A: Overview (always)
- III-B: First core module (the main innovation)
- III-C: Second core module (supporting innovation)
- III-D: Third innovation or Training Objective

For each slot, identify:
- What evidence exists for this innovation?
- What details are still missing?
- Is this slot genuinely novel or just infrastructure?

### Candidate Contributions
List potential contributions with:
- Type: Architectural / Algorithmic / Training Strategy / Data / Analysis / Application
- Novelty: What is new relative to published work? (Will be checked against literature in Stage 2)
- Evidence: What in the materials supports this as a contribution?
- Risk: Could a reviewer dismiss this as trivial/obvious/insufficient?

### Risks Before Paper Writing
Common risks:
- Missing baseline comparisons → Can't claim improvement.
- Missing ablation → Can't claim component contributions.
- Missing related work → Can't establish novelty.
- Thin experimental results (one dataset, one metric) → Can't claim robustness or generalization.
- Method is a minor modification of existing work → Contribution risk.
- No code available → Reproducibility risk.
