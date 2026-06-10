---
name: ai-sci-skills
description: End-to-end automated SCI paper writing for deep learning, machine learning, computer vision, NLP, multimodal learning, and related AI research. Chinese-first pipeline: raw project materials → structured digest → literature review → experiment analysis → polished English manuscript. v0.4 adds statistical testing, architecture extraction, citation network analysis, and result visualization. Use when the user wants to write a complete SCI paper from code, notes, experiment tables, framework diagrams, or mixed research materials.
---

# AI SCI Paper Writer v0.4.0

## Mission

One-stop pipeline that takes raw research materials and produces a polished English SCI manuscript. Default to Chinese-first writing unless the user explicitly asks for direct English drafting.

## Pipeline Overview

```
STAGE 0: INIT     → Inventory materials, create project state file
STAGE 1: DIGEST   → Extract paper-ready facts from project materials
STAGE 2: LIT      → Search, verify, organize literature
STAGE 3: EXPER    → Analyze experiments, compute improvements, validate claims
STAGE 4: WRITE    → Chinese draft → Chinese polish → EN conversion → EN polish → Self-critique → Template Rendering
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
5. Run `digest/scripts/summarize_repo.py <repo_path>` for a file inventory.
6. Run `digest/scripts/extract_architecture.py <repo_path>` for deep code analysis: extract nn.Module subclasses, loss functions, hyperparameters, framework detection, and training infrastructure.
7. If Jupyter notebooks (`.ipynb`) exist, run `digest/scripts/parse_notebooks.py <notebooks>` to extract model definitions, training loops, and results tables from notebook cells (NEW in v0.4).
8. Run `digest/scripts/trace_dependencies.py <repo_path> --entry <entry_point>` to build import graph, trace data flow, and identify core pipeline modules (NEW in v0.4).
9. Run `digest/scripts/synthesize_brief.py --arch <arch_report> --deps <dep_report> --notebooks <nb_report> --output <output_dir>/00_project_brief.md` to auto-generate the complete project brief, or use `--repo <path>` to run the full digest pipeline end-to-end (NEW in v0.4).

### Prompt Guidance

When performing the digest, use this chain-of-thought:

```
STEP 1: TASK IDENTIFICATION
- What is the research task? (classification / detection / segmentation / generation / retrieval / ...)
- What is the input modality? (image / text / audio / video / multimodal)
- What is the output? (class label / mask / bounding box / text / embedding)

STEP 2: METHOD EXTRACTION
- What is the backbone? (ResNet / ViT / BERT / GPT / custom)
- What are the novel modules? Identify every nn.Module subclass or custom function.
- What is the training objective? List every loss term.
- What is the inference pipeline? Describe step-by-step.

STEP 3: EVIDENCE GROUNDING
For every extracted fact, classify its evidence level:
- HIGH: directly visible in code/configs/notes (e.g., "uses CrossEntropyLoss" confirmed by loss.py:42)
- MEDIUM: strongly implied but not fully specified (e.g., "uses AdamW" based on config keys)
- LOW: plausible interpretation needing author confirmation

STEP 4: GAP ANALYSIS
- What datasets are claimed but have no provided splits?
- What metrics are mentioned but have no computed values?
- What baselines are named but lack implementation details?
- What hyperparameters are missing?

STEP 5: CONTRIBUTION CANDIDATES
For each candidate contribution, note:
- What is novel? (architecture / algorithm / training strategy / application)
- What evidence supports the novelty claim?
- What validation is still needed? (literature check / experiment confirmation)
```

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
- `literature/references/api-search-guide.md` — API usage for automated search
- `literature/references/citation-verification.md` — before finalizing references
- `literature/references/cv-classic-papers.md` — seed map: CV
- `literature/references/nlp-classic-papers.md` — seed map: NLP
- `literature/references/multimodal-classic-papers.md` — seed map: multimodal
- `literature/references/related-work-patterns.md` — prose structure
- `literature/references/literature-matrix-template.md` — output template
- `literature/references/literature-synthesis-guide.md` — from matrix to narrative: theme extraction, logical arc, mapping to Introduction/Related Work (NEW v0.4)

### Automated Search

Run the literature search script to bootstrap the literature collection:

```bash
python literature/scripts/search_literature.py "<query>" --sources s2,arxiv --max 20 --output <output_dir>/02a_search_results.md
```

Query derivation procedure:
1. Extract 3-5 key technical terms from Stage 1's task description and method family.
2. For each term, compose 2-3 query variants:
   - Broad: `"<task> <method_family>"` (e.g., `"text-to-image retrieval cross-modal alignment"`)
   - Specific: `"<task> <specific_technique>"` (e.g., `"cross-modal retrieval contrastive learning"`)
   - Gap-focused: `"<task> limitation <pain_point>"` (e.g., `"text-image retrieval fine-grained alignment"`)
3. Run search for each query, merge and deduplicate results.
4. Use the seed maps in `cv-classic-papers.md` / `nlp-classic-papers.md` / `multimodal-classic-papers.md` to identify classic papers that automated search may miss (older papers with fewer citations on Semantic Scholar).

Citation verification (run after building the literature matrix):

```bash
python literature/scripts/verify_citations.py <output_dir>/citations_to_verify.txt --sources crossref,dblp --output <output_dir>/02b_citation_verification.md
```

### Actions
1. Derive search queries from the task, method family, datasets, and claims.
2. Run `search_literature.py` for automated discovery.
3. Consult seed maps for classic papers that automated search may miss.
4. For each paper: read title, abstract, and key contributions. Verify metadata across sources.
5. Verify every citation using `verify_citations.py`. Never fabricate DOI, arXiv ID, venue, year, or authors.
6. Build the literature matrix. Every row must have a verification status.
7. Draft related-work structure organized by themes, not paper-by-paper.
8. Run `literature/scripts/analyze_citations.py <output_dir>/02_literature_matrix.md` for gap analysis: temporal trends, venue distribution, method-family clustering, and missing citation suggestions (NEW in v0.4).
9. Run `literature/scripts/synthesize_literature.py <output_dir>/02_literature_matrix.md --project-brief <output_dir>/00_project_brief.md` to synthesize the matrix into narrative themes and generate Introduction + Related Work paragraph templates with logical flow (NEW in v0.4). Read `literature/references/literature-synthesis-guide.md` for the full methodology.

### Literature Matrix Column Guidance

When filling the matrix, be specific:
- **Relation to This Work**: Use one of: "direct competitor (same task+method family)", "method inspiration (different task, similar technique)", "baseline comparison", "dataset source", "gap evidence (shows limitation addressed by this paper)"
- **Use in Paper**: Which section and for what purpose (e.g., "Intro para 2 — representative method", "Related Work theme A — method-family paper", "Experiments Table 1 — SOTA baseline")
- **Verification**: One of: "✓ confirmed (DOI+arXiv)", "~ metadata from single source", "✗ unverified [CITATION NEEDED]"

### Output
Save to the project state file under `### Stage 2 Output (LIT)`:

```markdown
## Search Queries Used
| # | Query | Source | Results |
|---|-------|--------|---------|
| 1 |       | s2     | 15      |

## Literature Matrix
| Category | Paper | Year | Venue | Main Idea | Relation to Our Work | Use in Paper | Verification |
|---|---:|---:|---|---|---|---|---|

## Related Work Structure
### Theme A: [Name] (2-3 papers)
### Theme B: [Name] (2-3 papers)
### Theme C: [Name] (2-3 papers)

## Research Gap Evidence
| Gap | Supporting Papers | Strength |
|-----|-------------------|----------|

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

For statistical significance testing (NEW in v0.4), run:
```bash
python experiment/scripts/statistical_tests.py <table_path> --target <method_name> --metrics <m1,m2> --higher-better <m1> --output <output_dir>/03b_statistical_tests.md
```

For result visualizations (NEW in v0.4), run:
```bash
python experiment/scripts/result_visualizer.py <table_path> --target <method_name> --metrics <m1,m2> --output-dir <output_dir>/figures/
```

**Experiment planning (NEW in v0.4):** Generate a structured experiment plan BEFORE running experiments:
```bash
python experiment/scripts/design_experiments.py --project-brief <output_dir>/00_project_brief.md --venue cvpr --output <output_dir>/experiment_plan.md
```

**Experiment narrative synthesis (NEW in v0.4):** After analysis, synthesize into prose:
```bash
python experiment/scripts/synthesize_experiments.py --improvements <output_dir>/03a_improvement_summary.md --stats <output_dir>/03b_statistical_tests.md --project-brief <output_dir>/00_project_brief.md --output <output_dir>/experiment_synthesis.md
```

**Claim-evidence audit (NEW in v0.4):** Before submission, verify every claim has evidence:
```bash
python scripts/claim_evidence_auditor.py <output_dir>/08_english_polished.md --output-dir <output_dir>/ --output <output_dir>/claim_audit.md
```

### Prompt Guidance

Before making any claim, apply this decision tree:

```
Q1: Is the improvement direction correct given the metric?
    → Check metrics-guide.md for higher-is-better vs lower-is-better.
    → If unsure, mark as AUTHOR_INPUT_NEEDED.

Q2: Is the improvement consistent across datasets/settings?
    → Consistent (all datasets): claim strength = STRONG
    → Mixed (most datasets): claim strength = MODERATE
    → Single dataset: claim strength = WEAK
    → No direct evidence: UNSUPPORTED — do not claim.

Q3: Is the improvement large enough to matter?
    → Classification: >1 percentage point difference is meaningful
    → Detection: >1 mAP point is meaningful
    → Segmentation: >1 mIoU/Dice point is meaningful
    → Generation: >1 BLEU point is meaningful
    → If below threshold, use "comparable to" or "on par with" language.

Q4: Could confounding factors explain the improvement?
    → Different backbone capacity?
    → Different training budget (epochs, batch size)?
    → Different data preprocessing?
    → If yes, flag as caveat.
```

### Result Paragraph Drafting Template

Use this fill-in-the-blank structure for the first results paragraph:

> As shown in Table [X], [Method] achieves [metric_value] on [dataset], [direction_description] the strongest baseline [baseline_name] by [absolute_value] ([relative_value]%). On [dataset_2], [Method] achieves [metric_value_2], a [absolute_2] improvement over [baseline_2]. These results demonstrate that [component/design_choice] contributes to [capability], as evidenced by [specific_evidence].

### Visual Ablation Design

Beyond quantitative tables, design visual ablations to show HOW each component works. Read `experiment/references/ablation-writing.md` "Visual Ablation Analysis" for full guidance. The selection guide:

| If your claim is... | Primary visualization |
|-----|------|
| "Our module improves feature quality" | t-SNE / PCA embedding |
| "Our module guides attention to the right regions" | Grad-CAM heatmap |
| "Our gating mechanism selects informative channels" | Channel weight distribution |
| "Our loss function improves class separability" | t-SNE embedding + silhouette score |
| "Our method handles challenging cases better" | Error case comparison |
| "Our module accelerates convergence" | Training dynamics curves |
| "Our attention mechanism is more interpretable" | Attention map + rollout |
| "Our filters learn more diverse patterns" | Filter / kernel visualization |

10 visualization types are covered: Feature Map, Grad-CAM Heatmap, Channel Weight, t-SNE/PCA, Attention Map, Error Case Comparison, Filter/Kernel, Confusion Difference Matrix, Training Dynamics, Prediction Confidence Distribution.

For every visual ablation, follow the 5-step prose pattern: (1) state the question → (2) describe the setup → (3) point to key observations → (4) interpret mechanistically → (5) link back to quantitative evidence.

### Actions
1. Identify table types: main results, ablation, robustness, efficiency, hyperparameter, qualitative, failure cases.
2. Plan visual ablations: for each claimed component, select at least one visualization type from the guide above.
3. Identify datasets, metrics, metric direction (higher/lower is better), baselines, and proposed method.
4. Calculate absolute and relative improvements.
5. Map each possible paper claim to concrete evidence using the claim strength decision tree above.
6. Draft results and analysis paragraphs in Chinese first unless user requests English.

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
Produce a complete SCI manuscript through the Chinese-first pipeline: Chinese draft → Chinese academic polish → English SCI conversion → English polish → Self-critique.

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
- `writer/references/cn-en-translation-corpus.md` — translation error prevention (check before translating any technical term)
- `writer/references/english-polishing-rules.md` — English refinement
- `writer/references/forbidden-overclaims.md` — before finalizing claims (includes Chinese overclaims list)
- `writer/references/deai-dedup-rules.md` — de-AI language & cross-section deduplication rules
- `writer/references/ai-terminology-glossary.md` — bilingual term consistency
- `writer/references/quality-rubric.md` — self-critique scoring criteria

### Sub-stages

---

#### 4a: Paper Storyline

Before drafting, produce a storyline summary. Use this chain-of-thought:

```
First, identify the ONE scientific question the paper answers.
Then, identify the ONE piece of missing knowledge that previous work didn't address.
Then, state your method's core mechanism in 2-3 sentences.
Then, list the 2-3 key experimental results that support your claims.
Finally, draft a single-sentence contribution statement aligned with the evidence.
```

**Self-check after writing the storyline:**
1. Does the problem statement match what the method actually solves?
2. Is the gap articulated with specificity (not "few works study X" but "existing methods fail to handle Y because Z")?
3. Does the method description highlight the novel part, not the standard pipeline?
4. Does every contribution bullet trace to evidence in Stage 1 or Stage 3?
5. Is the contribution scope honest — does it claim only what the evidence supports?

**Few-shot example (CV — semantic segmentation):**

```
Problem: Semantic segmentation models struggle with fine-grained boundary delineation,
        especially for thin and elongated structures (roads, poles, text).

Gap:     Existing boundary-refinement methods rely on multi-scale feature fusion,
        but they treat all boundary pixels equally and fail to distinguish
        structural edges from texture edges, leading to blurred boundaries
        for geometrically regular structures.

Method:  Structure-Aware Boundary Refinement (SABR) is proposed, which designs
        a Geometric Continuity Module that explicitly models the spatial
        continuity of boundaries via a directional consistency loss.
        SABR can be plugged into any encoder-decoder segmentation architecture
        without modifying the backbone.

Evidence: On Cityscapes, SABR improves mIoU by 2.3 points over the strongest
          boundary-aware baseline (SegFix), with the largest gains (+4.1 mIoU)
          on thin-structure categories (pole, traffic sign). Ablation confirms
          the directional consistency loss contributes 1.6 of the 2.3 point gain.

Contribution: A plug-and-play boundary refinement module with a novel directional
              consistency loss that explicitly regularizes geometric continuity
              of predicted boundaries, achieving state-of-the-art boundary quality
              on Cityscapes and Mapillary Vistas.
```

**Few-shot example (NLP — efficient fine-tuning):**

```
Problem: Fine-tuning large language models for downstream tasks is computationally
        expensive, especially when serving many task-specific adapters simultaneously.

Gap:     Existing parameter-efficient methods (LoRA, Adapters, Prefix-tuning) reduce
        trainable parameters, but they add inference-time overhead because adapted
        layers cannot be merged with frozen weights without approximation error.

Method:  Mergeable Low-Rank Adaptation (MeLoRA) is proposed, which constrains
        the low-rank decomposition such that the adapter can be exactly merged
        into the original weight matrix via a single matrix addition at inference
        time, eliminating adapter overhead entirely with zero accuracy loss.

Evidence: On GLUE, MeLoRA matches full LoRA accuracy while reducing inference
          latency by 27% (from 14.2ms to 10.4ms per token on A100). On MMLU,
          MeLoRA achieves 68.3% accuracy vs LoRA's 68.1% with zero overhead.

Contribution: A mergeable low-rank adaptation method that achieves the parameter
              efficiency of LoRA with zero inference-time overhead, enabled by
              a constrained decomposition that permits exact weight merging.
```

Save storyline to the project state file:

```markdown
## Paper Storyline
- Problem: (one sentence)
- Gap: (one sentence)
- Method: (2-3 sentences, module-level)
- Evidence: (key results supporting the method)
- Contribution: (one sentence, aligned with evidence)
```

Transition to 4b.

---

#### 4b: Chinese Draft (`05_chinese_draft.md`)

**Role Instruction (read before drafting any section):**

> You are now drafting a Chinese academic paper manuscript. Your goal is to produce a complete, logically coherent first draft where every factual claim is grounded in the project state file's evidence. Write in formal Chinese academic register. Use short to medium sentences (20-50 characters). Prefer passive voice; avoid using "we" (我们) as the subject. Every paragraph should have a clear topic sentence. Preserve all `AUTHOR_INPUT_NEEDED` and `[CITATION NEEDED]` markers — do not remove or fill them.

1. Read `writer/references/reference-paper-structure.md` for the manuscript skeleton.
2. Build the outline first. Keep top-level sections: Title, Abstract, Index Terms, I Introduction, II Related Work, III Proposed Method, IV Experiments, V Conclusion, References.
3. Rewrite second-level headings for the user's own method, datasets, and evidence.
4. Draft each section following the templates in `writer/references/chinese-draft-patterns.md`.

**Section-by-section drafting guidance:**

**Title:** Read `writer/references/title-patterns.md`. Propose 3 title variants. Choose the one that is most specific and least overclaiming. Use the pattern `[Method Name]: [Core Mechanism] for [Task]` or `[Core Mechanism] for [Task] via [Key Insight]`.

**Abstract:** Use the 2-6-2 structure from `writer/references/abstract-patterns.md`. Exactly 10 sentences: 2 for background/gap, 6 for method (signaled by First/Second/Finally), 2 for experimental results/conclusion. Target ~250 Chinese characters or ~210 English words. The method's 6 sentences are the core — each pair is claim + why-it-works. Self-check: (1) exactly 10 sentences? (2) do sentences 3/5/7 start with First/Second/Finally (or 首先/其次/最后 in Chinese)? (3) does sentence 9 contain dataset + metric + value? (4) is the gap sentence backed by a "because" clause?

**Introduction:** Use the structure from `writer/references/introduction-patterns.md`. Five paragraphs:
- Para 1: Task importance and real-world applications
- Para 2: Current progress — 2-3 representative method families with specific examples
- Para 3: Remaining gap — what existing methods fail to do and WHY
- Para 4: Proposed method — core mechanism in 2-3 sentences, intuition for why it works
- Para 5: Contributions — prose lead-in (2-3 sentences summarizing problem, method, and three innovations), then "Our main contributions are:" followed by exactly 3 detailed bullets, each matching one innovation point with what + why + evidence pointer

Self-check after drafting Introduction:
1. Is the gap stated with a "because" clause? (Not just "X is understudied" but "X is understudied because existing methods assume Y which fails when Z.")
2. Does the contribution paragraph have a prose lead-in before the bullet list?
3. Are there exactly 3 contribution bullets, each matching one innovation point?
4. Is each bullet detailed (what + why + evidence), not a one-line summary?
5. Is the contribution scope aligned with evidence strength from Stage 3?
6. Is the method teaser at the right level of detail — tells WHAT and WHY, not HOW?

**Related Work:** Use the theme-based structure from Stage 2's "Related Work Structure." Each theme gets 1 paragraph: lead with the theme statement, discuss 2-3 papers with comparison, end with how your method differs. Avoid the "Author et al. [X] proposed..." laundry-list pattern.

**Method:** Use the modular structure from `writer/references/method-section-patterns.md`. III-A Overview with architecture diagram reference. III-B/C/D for each module with: input → process → output → design rationale. Every formula must be explained in prose — no orphan equations.

**Experiments:** Use the structure from `writer/references/experiment-section-patterns.md`. Subsections: Datasets & Implementation Details, Main Results, Ablation Study, Efficiency Analysis, Qualitative Analysis. Every result number must appear in both the table AND the prose.

**Conclusion:** Use the structure from `writer/references/conclusion-patterns.md`. Restate problem, method, key findings. Do not add new claims or citations. End with 1-2 specific future work directions.

5. Save to `<output_dir>/05_chinese_draft.md`.

---

#### 4c: Chinese Polish (`06_chinese_polished.md`)

**Role Instruction:**

> You are now polishing a Chinese academic manuscript. Polish for academic clarity, logical flow, and concise expression. The goal is NOT to make the text flowery — it is to remove ambiguity, tighten logic, eliminate redundancy, and ensure every paragraph earns its place. Scientific meaning is sacred — never alter it to sound better.

1. Polish the Chinese draft using the detailed rules in `writer/references/chinese-polishing-rules.md`.

**De-AI & Dedup Scan** (before finalizing Chinese polish):

1. Read `writer/references/deai-dedup-rules.md` for the complete rules.
2. Scan for AI 套话 (Chinese section of deAI rules):
   - Replace 万能开头 (e.g., "近年来，随着...的发展") with concrete problem statements.
   - Replace 万能结尾 (e.g., "综上所述，本文提出的方法有效...") with specific findings.
   - Delete 空洞修饰语 (e.g., "强大的性能", "良好的效果") — replace with specific numbers.
   - Remove 过度解释基础知识 — no explanations of basic concepts that SCI reviewers already know.
3. Run cross-section dedup (Chinese section of dedup rules):
   - Verify method details appear only in 方法 section, not in 引言.
   - Verify results appear only in 实验 section, not in 方法.
   - Verify no two sections share near-identical sentences.
   - Check that Abstract, Introduction, and Conclusion use distinct phrasing.

**10-Item Polishing Checklist** (apply to each section):

| # | Check | Before (BAD) | After (GOOD) |
|---|-------|-------------|--------------|
| 1 | Remove empty modifiers | 该方法取得了较好的性能提升 | 该方法在Cityscapes上提升了2.3 mIoU |
| 2 | Add missing subjects (impersonal) | 使用ResNet-50作为骨干网络 | ResNet-50被用作骨干网络 |
| 3 | Split long sentences (>50 chars) | (a 60-character run-on) | (two 25-35 character sentences) |
| 4 | Unify terminology | 注意力机制/Attention机制/attention混用 | 统一为"注意力机制"（首次出现标注英文） |
| 5 | Remove redundant pairs | 精度和准确率均得到提升 | 精度提升了1.2个百分点（具体说明哪个指标） |
| 6 | Strengthen weak transitions | 另外，我们还做了... | 在效率方面，进一步分析了... |
| 7 | Ground vague claims | 性能优于所有基线方法 | 在三个数据集上，所提方法均优于所有基线方法（Table 2） |
| 8 | Fix dangling references | 如图所示 | 如图3所示 |
| 9 | Align parallel structures | 我们提出了X，设计了Y，以及对Z进行了优化 | 提出了X，设计了Y，优化了Z |
| 10 | Check claim-consistency | 中文"显著提升" vs 英文"significant" | 确保改善幅度表述与Stage 3证据强度一致 |

**Logic Flow Audit:**
Read the complete draft from start to finish. At each paragraph boundary, ask:
- Does this paragraph logically follow from the previous one? If not, insert a transition sentence.
- Does this paragraph introduce new information, or does it restate previous content? If restating, cut it.
- Is the argument chain unbroken? Identify any missing logical step and fill it.

**Redundancy Detection:**
Scan for:
- Consecutive sentences that convey the same information
- The same method component described in both Introduction and Method with identical wording
- Metric values repeated in both Results prose and Conclusion without adding interpretation

2. Save polished version to `<output_dir>/06_chinese_polished.md`.

---

#### 4d: CN→EN Conversion (`07_english_draft.md`)

**Role Instruction:**

> You are now converting a polished Chinese academic manuscript into English SCI prose. This is NOT literal translation. You are rewriting: restructure sentences from Chinese topic-comment pattern to English SVO pattern, add explicit subjects where Chinese omitted them, convert Chinese aspect markers to English tense, add articles (a/an/the), and maintain academic register throughout. Preserve all numbers, metric values, citation markers, and claim strength EXACTLY.

**Tense Conventions by Section:**

| Section | Primary Tense | When to Use Other Tenses |
|---------|--------------|--------------------------|
| Abstract | Present | Past for evaluation: "Performance was evaluated on..." |
| Introduction | Present | Past for "Previous methods struggled with...", Present perfect for "Recent work has shown..." |
| Related Work | Present perfect / Present | Past for specific historical results |
| Method | Present | — (Methods are described in present) |
| Experiments | Past | Present for "Table 1 reports..." |
| Conclusion | Present | Past for summarizing specific results |

**Voice Conventions by Section:**

| Section | Guidance |
|---------|----------|
| Abstract | Passive preferred: "A novel X is proposed..." |
| Introduction | Third-person for contribution bullets (Para 5): "This paper proposes...", "A novel X is proposed...", "Extensive experiments on Y demonstrate..." Do NOT write "We propose X" in contribution bullets. |
| Related Work | Passive for describing existing methods; impersonal for differentiation: "This work differs from..." |
| Method | Passive preferred for process: "Features are extracted..." Passive / impersonal for design rationale: "X is designed to...", "This module enables..." |
| Experiments | Passive preferred for procedure: "Models were trained on..." Passive for narrative: "As shown in Table 1, the proposed method achieves..." |
| Conclusion | Passive / impersonal preferred: "This paper has presented..." |

**Claim-Strength Mapping (key entries — see `chinese-to-english-writing-rules.md` for full table):**

| Chinese | Overclaiming English | Safer English |
|---------|---------------------|---------------|
| 显著提升 | significantly improves / dramatically boosts | achieves a X.X percentage point improvement / outperforms by X% |
| 解决了...问题 | solves the problem of... | addresses / alleviates / mitigates |
| 优于现有方法 | outperforms all existing methods / state-of-the-art | outperforms [named baselines] on [specific datasets] |
| 首次提出 | is the first to / novel | proposes (without "first" unless verifiable) |
| 证明了 | proves that | demonstrates that / suggests that / provides evidence that |
| 具有很强的泛化能力 | generalizes well / is robust | achieves competitive performance on [out-of-domain dataset X] |

**Common CN→EN Translation Pitfalls:**

1. **Topic-prominence transfer**: Chinese drops subjects when clear from context; English prefers explicit impersonal subjects. Add "The model", "This module", "The proposed method" where Chinese omitted them (avoid "We").
2. **Modifier stacking**: Chinese stacks modifiers before the noun ("基于注意力机制的特征融合模块"); English prefers post-modification ("a feature fusion module based on attention mechanisms").
3. **Parallel structure**: Chinese parallelism uses重复 (repetition); English uses conjunction reduction. "我们提出了X，设计了Y，优化了Z" should NOT be rendered as "We propose X, design Y, and optimize Z" — use passive: "X is proposed, Y is designed, and Z is optimized."
4. **Zero article → article**: Every English singular countable noun needs a/an/the. "Backbone网络采用ResNet-50" → "The backbone network adopts ResNet-50."
5. **Aspect → tense**: Chinese 了（completion）often maps to past tense in Experiments section, but present in Method. "我们采用了..." → Method: "X is adopted..."; Experiments: "X was adopted..."

1. Before translating, scan the Chinese draft for technical terms against `writer/references/cn-en-translation-corpus.md`. Use the verified translations exactly.
2. Convert the polished Chinese to English SCI prose following `writer/references/chinese-to-english-writing-rules.md`.
3. Maintain terminology consistency using `writer/references/ai-terminology-glossary.md`.
3. After conversion, audit: every number in the Chinese draft appears in the English draft exactly; every `AUTHOR_INPUT_NEEDED` and `[CITATION NEEDED]` marker is preserved.
4. Save to `<output_dir>/07_english_draft.md`.

---

#### 4e: English Polish (`08_english_polished.md`)

**Role Instruction:**

> You are now polishing an English SCI manuscript. Polish for: academic register, sentence variety, cohesion, precision, and readability. Do NOT change scientific content, add unsupported claims, or strengthen claim wording. If in doubt about whether a change alters meaning, keep the original.

1. Polish the English draft using `writer/references/english-polishing-rules.md`.

**De-AI Scan** (before finalizing English polish):

1. Read `writer/references/deai-dedup-rules.md` Part 1 (English section).
2. Scan for AI-flavor patterns:
   - Replace generic openers (e.g., "In recent years, there has been growing interest in...") with concrete statements.
   - Reduce overused connectors (Moreover, Furthermore, In addition) — max 2 per section.
   - Replace hollow adjectives ("powerful", "effective", "promising") with specific evidence or delete.
   - Delete formulaic concluding sentences ("These results demonstrate the effectiveness of our approach.")
   - Remove over-explanation of basic concepts (CNN, attention, transformer basics).
3. Re-run cross-section dedup (same procedure as Stage 4c, applied to English text).

**Sentence Variety Audit:**
- Count sentences starting with "The proposed method" in each section. If >3 consecutive sentences begin with the same subject, restructure (e.g., vary between "The model achieves...", "Results on [dataset] show...", "A key observation is...").
- Measure sentence length distribution. If all sentences in a paragraph are 25-35 words, vary them: mix a short punchy sentence (10-15 words) among longer analytical ones (25-40 words).
- Check paragraph length: no paragraph should be 1 sentence or >12 sentences.

**Cohesion Device Injection:**
At each logical transition point in the text, verify that an appropriate connector is present:
- **Addition**: furthermore, moreover, in addition
- **Contrast**: however, in contrast, conversely, whereas
- **Cause-effect**: therefore, consequently, as a result, thus
- **Exemplification**: for instance, specifically, in particular
- **Emphasis**: notably, importantly, it is worth noting that
- **Sequence**: first, second, finally, subsequently

**Academic Register Check:**
Replace informal/colloquial phrasing with formal academic equivalents:
- "a lot of" → "a substantial number of" / "considerable"
- "kind of" / "sort of" → delete or use "type of"
- "big" / "huge" → "substantial" / "considerable" / "large"
- "get" → "obtain" / "achieve"
- "find out" → "determine" / "identify"
- "look at" → "examine" / "investigate"

2. Check claims against `writer/references/forbidden-overclaims.md`.
3. Produce revision notes (`09_revision_notes.md`): CN-EN consistency, terminology check, claims alignment.
4. Save final manuscript to `<output_dir>/08_english_polished.md`.

---

#### 4f: Self-Critique (`10_critique_report.md`) **[NEW in v0.3]**

**Purpose:** Before declaring the paper complete, conduct a systematic self-critique using the quality rubric and automated checks.

**Role Instruction:**

> You are now the reviewer of this manuscript. Adopt a critical, skeptical stance. Your job is to find every weakness, overclaim, missing citation, and imprecise statement. Be harsh but fair. Rate each dimension honestly — inflating scores helps no one.

1. Read `writer/references/quality-rubric.md` for the 5-dimension scoring criteria.
2. Rate the manuscript on each dimension (1-4 scale, see rubric for detailed descriptors):

| Dimension | Weight | Score (1-4) | Issues Found |
|-----------|--------|-------------|--------------|
| Claims-Evidence Alignment | 25% | | |
| Citation Completeness & Accuracy | 15% | | |
| Method Description Precision | 20% | | |
| Experiment Reporting Rigor | 25% | | |
| Language Quality | 15% | | |
| **Weighted Total** | **100%** | **/100** | |

3. Run automated quality checks:

```bash
python scripts/check_quality.py <output_dir> --all --output <output_dir>/10a_auto_check.md
```

4. Conduct these manual audits:

**Claims Audit:**
- List every factual claim in the manuscript.
- For each claim, identify its evidence source (table/figure/section reference).
- Flag claims without evidence → mark for removal or `AUTHOR_INPUT_NEEDED`.
- Flag claims whose wording overstates the evidence → rewrite with weaker language.

**Citation Audit:**
- Count all citation markers in the text.
- Count `[CITATION NEEDED]` markers → if >3, the paper is not ready.
- Verify that every citation in the text appears in the References section and vice versa.
- Check that every citation is used for a clear purpose (not "citation stuffing").

**Overclaim Scan (Chinese + English):**
- Scan for English forbidden terms listed in `writer/references/forbidden-overclaims.md`.
- Scan for Chinese forbidden terms listed in `writer/references/forbidden-overclaims.md` (Chinese Overclaims section).
- Key Chinese words to flag: 完美, 彻底解决, 首次, 最优, 颠覆, 大幅, 显著, 极大, 通用, 众所周知, 毋庸置疑.
- For each flagged term, check context: is the claim supported by evidence of sufficient strength?
- Rewrite or caveat every overclaim.

**Readability Audit:**
- Check that every figure and table is referenced in the text BEFORE it appears.
- Verify all cross-references (section numbers, equation numbers, figure numbers) are consistent.
- Check that the abstract can be understood without reading the full paper.

**Terminology Audit:**
- Scan for inconsistent terminology (same concept, different terms).
- Verify that all technical abbreviations are defined on first use.
- Check bilingual consistency: does every Chinese term map to exactly one English term?

5. Compute the weighted total score:
   - If score >= 80/100: the manuscript is ready for author review.
   - If score 70-79/100: fix identified issues, re-run critique.
   - If score < 70/100: return to the relevant sub-stage (4b/4c/4d/4e) for substantive revision.

6. Save the critique report to `<output_dir>/10_critique_report.md` with:
   - Per-dimension score and detailed issues
   - Automated check results (from `10a_auto_check.md`)
   - List of must-fix issues (blocking)
   - List of should-fix issues (non-blocking)
   - Recommendation: READY / NEEDS REVISION / NOT READY

**Transition to 4g if score >= 80.** If < 80, fix issues and re-evaluate before proceeding.

---

#### 4g: Template Rendering (`chinese_manuscript/`, `english_manuscript/`, `english_manuscript.docx`) **[NEW in v0.3]**

**Purpose:** Render polished content into submission-ready formats: Chinese LaTeX, English LaTeX, English Word, and Cover Letter (LaTeX + Word).

**Required Inputs:**
- `06_chinese_polished.md` (for Chinese LaTeX)
- `08_english_polished.md` (for English LaTeX, Word, and cover letter)
- Stage 2: Verified literature matrix (for .bib generation)
- Stage 0: Author-provided author/affiliation/funding info, target journal

**References:**
- `writer/references/template-filling-guide.md` — complete filling rules for all three templates

**Templates:**

| Template | Location | Output |
|----------|----------|--------|
| Chinese LaTeX (cjc) | `templates/chinese/` | `<output_dir>/chinese_manuscript/` |
| IEEE LaTeX | `templates/ieee-latex/` | `<output_dir>/english_manuscript/` |
| IEEE TGRS LaTeX (NEW) | `templates/ieee-tgrs-latex/` | `<output_dir>/tgrs_manuscript/` |
| IEEE TETCI LaTeX (NEW) | `templates/ieee-tetci-latex/` | `<output_dir>/tetci_manuscript/` |
| IEEE TIP LaTeX (NEW) | `templates/ieee-tip-latex/` | `<output_dir>/tip_manuscript/` |
| IEEE Word | `templates/ieee-word/` | `<output_dir>/english_manuscript.docx` |
| Cover Letter LaTeX | `templates/cover-letter/` | `<output_dir>/cover_letter/` |
| Cover Letter Word | `templates/ieee-word/` | `<output_dir>/cover_letter.docx` |
| CVPR/ICCV LaTeX (NEW) | `templates/cvpr-latex/` | `<output_dir>/cvpr_manuscript/` |
| NeurIPS/ICML LaTeX (NEW) | `templates/neurips-latex/` | `<output_dir>/neurips_manuscript/` |
| ACL/EMNLP LaTeX (NEW) | `templates/acl-latex/` | `<output_dir>/acl_manuscript/` |
| AAAI/IJCAI LaTeX (NEW) | `templates/aaai-latex/` | `<output_dir>/aaai_manuscript/` |

**Actions:**

**Step 1: Chinese LaTeX Manuscript**
1. Copy `templates/chinese/` to `<output_dir>/chinese_manuscript/`.
2. Fill `chinese_manuscript.tex` using content from `06_chinese_polished.md`:
   - `\classsetup{}`: Bilingual metadata (title, authors, affiliations, abstract, keywords, grants).
   - 引言, 相关工作, 方法, 实验, 结论: Fill from corresponding sections.
   - 致谢: From author-provided acknowledgments.
3. Generate `references.bib` from Stage 2's verified literature entries.
4. Compile check: `python scripts/compile_latex.py <output_dir>/chinese_manuscript/chinese_manuscript.tex --compiler xelatex`

**Step 2: English LaTeX Manuscript**
1. Copy `templates/ieee-latex/` to `<output_dir>/english_manuscript/`.
2. Fill `english_manuscript.tex` using content from `08_english_polished.md`:
   - `\title{}`, `\author{}`: From Stage 0 author info.
   - Abstract, Introduction, Related Work, Proposed Method, Experiments, Conclusion: Fill from corresponding sections.
   - Apply IEEE-specific formatting (tense conventions, figure/table style, citation style).
3. Generate `references.bib` from Stage 2's verified literature entries (same entries, different BibTeX style via `IEEEtran.bst`).
4. Compile check: `python scripts/compile_latex.py <output_dir>/english_manuscript/english_manuscript.tex`

**Step 3: English Word Manuscript**
1. Build a JSON content file at `<output_dir>/word_content.json` from `08_english_polished.md`. See `template-filling-guide.md` for the JSON schema.
2. Run the Word script:
   ```bash
   python scripts/render_word.py <output_dir>/word_content.json \
       --template templates/ieee-word/template.docx \
       --output <output_dir>/english_manuscript.docx
   ```

**Step 4: Cover Letter (LaTeX + Word)**
1. Generate cover letter content from pipeline outputs. See `template-filling-guide.md` for the full structure.
2. Content structure: Para 1 (submission statement), Para 2 (background + 3-4 contribution bullets), Para 3 (key findings with numbers), Para 4 (why this journal), Para 5 (declarations).
3. All overclaim rules apply doubly to cover letters — never use "first", "groundbreaking", or "solves".
4. Cover letter must NOT copy-paste the abstract — use fresh phrasing.
5. LaTeX output: Copy `templates/cover-letter/` to `<output_dir>/cover_letter/`, fill `cover_letter.tex`, compile with pdflatex.
6. Word output: Create `<output_dir>/cover_letter_content.json`, run `python scripts/render_word.py <output_dir>/cover_letter_content.json --output <output_dir>/cover_letter.docx`.
7. Verify: title in cover letter matches manuscript title exactly. Numbers in cover letter match manuscript numbers exactly. Cover letter claims do not exceed manuscript claims.

**Step 5: Cross-Template Consistency Check**
Verify across all outputs (see `template-filling-guide.md` for detailed checklist):
1. Titles match (Chinese `title*` == IEEE title == Word title == cover letter).
2. Author lists match in order and affiliation.
3. English abstracts match between LaTeX and Word (cover letter must NOT copy-paste abstract).
4. All metric values are identical across all files.
5. Citation counts are consistent.
6. Cover letter claims do not exceed manuscript claims.
7. No `AUTHOR_INPUT_NEEDED` or `[CITATION NEEDED]` in any final output.

### Post-Submission Scripts (NEW in v0.4)

After submission, use these scripts for reviewer response and presentation:

**Rebuttal Generation:**
```bash
python scripts/generate_rebuttal.py reviews.txt --paper <output_dir>/08_english_polished.md --output <output_dir>/rebuttal.md
python scripts/generate_rebuttal.py reviews.json --latex --output rebuttal.tex
```

**Presentation Slides Generation:**
```bash
python scripts/paper_to_slides.py <output_dir>/08_english_polished.md --format beamer --output slides.tex
python scripts/paper_to_slides.py <output_dir>/08_english_polished.md --format markdown --output slides.md
python scripts/paper_to_slides.py <output_dir>/08_english_polished.md --notes-only --output speaker_notes.md
```

### Final Output Files
```
<output_dir>/
├── project-state.md
├── 05_chinese_draft.md
├── 06_chinese_polished.md
├── 07_english_draft.md
├── 08_english_polished.md
├── 09_revision_notes.md
├── 10_critique_report.md
├── 10a_auto_check.md
├── word_content.json
├── english_manuscript.docx
├── cover_letter_content.json
├── cover_letter.docx
├── cover_letter/
│   └── cover_letter.tex
├── chinese_manuscript/
│   ├── chinese_manuscript.tex
│   ├── cjc.cls, cjc.bst
│   ├── references.bib
│   └── figures/
└── english_manuscript/
    ├── english_manuscript.tex
    ├── IEEEtran.cls, IEEEtran.bst
    ├── references.bib
    └── figures/
```

### Transition
1. Update `**Status**` to `DONE`.
2. Mark `[x] Stage 4: WRITE` in the pipeline progress.
3. The pipeline is complete. Summarize all output files and the critique score.

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
| `digest/scripts/extract_architecture.py <path> --output <report>` | Deep code analysis: nn.Module extraction, loss function parsing, hyperparameter detection, framework identification (NEW v0.4) |
| `digest/scripts/parse_notebooks.py <notebook.ipynb> --output <report>` | Extract model definitions, training loops, hyperparameters, results tables from Jupyter notebooks (NEW v0.4) |
| `digest/scripts/trace_dependencies.py <repo> --output <report>` | Module-level import graph, data flow tracing, core pipeline identification, orphan module detection (NEW v0.4) |
| `digest/scripts/synthesize_brief.py --arch <arch.md> --deps <dep.md> --output <brief>` | Auto-generate complete project_brief.md from all digest outputs (NEW v0.4) |
| `experiment/scripts/compute_improvements.py <csv> --target <name> --metrics <m1,m2> --higher-better <m1> --lower-better <m2> --group-cols <col> --output <path>` | Compute pairwise improvements from CSV (v0.4: added --stats, --all-pairs, --format json, --seed-col) |
| `experiment/scripts/statistical_tests.py <csv> --target <name> --metrics <m1,m2> --higher-better <m1> --output <path>` | Bootstrap CI, Cohen's d/Hedges' g, paired t-test, Wilcoxon, multiple comparison correction (NEW v0.4) |
| `experiment/scripts/result_visualizer.py <csv> --target <name> --metrics <m1,m2> --output-dir <dir>` | Bar charts, ablation waterfall, radar charts, heatmaps, Pareto frontiers (NEW v0.4) |
| `experiment/scripts/design_experiments.py --project-brief <brief> --output <plan>` | Generate structured experiment plan: required tables, ablation design, baseline coverage check, completeness checklist (NEW v0.4) |
| `experiment/scripts/synthesize_experiments.py --improvements <imp.md> --stats <stats.md> --output <synth>` | Synthesize experiment results into narrative paragraphs for Setup, Results, Ablation, Efficiency, Discussion (NEW v0.4) |
| `literature/scripts/search_literature.py "<query>" --sources s2,arxiv --max 20 --output <path>` | Search literature across Academic APIs |
| `literature/scripts/verify_citations.py <citations_file> --sources crossref,dblp --output <path>` | Verify citation metadata |
| `literature/scripts/analyze_citations.py <lit_matrix.md> --output <gap_analysis>` | Temporal trends, venue distribution, method-family clustering, research gap identification, network data export (NEW v0.4) |
| `literature/scripts/auto_fill_matrix.py <search_results.md> --project-brief <brief> --output <matrix>` | Auto-fill literature matrix from search results — classifies papers by task relation, summarizes main ideas, assigns section placement (NEW v0.4) |
| `literature/scripts/synthesize_literature.py <lit_matrix.md> --project-brief <brief> --output <synthesis>` | Synthesize matrix into narrative for Introduction + Related Work — theme grouping, logical arc, paragraph templates with differentiation (NEW v0.4) |
| `scripts/check_quality.py <output_dir> --checks all --output <path>` | Quality checks: claims, citations, reproducibility, language, structure, terminology, CN-overclaims, dedup, AI-flavor |
| `scripts/claim_evidence_auditor.py <paper.md> --tables <csv> --output <audit>` | Structured claim-evidence audit: extracts claims, checks table references, verifies numbers, detects overclaims, flags unsupported statements (NEW v0.4) |
| `scripts/validate_references.py <paper.md> --output <report>` | Cross-reference consistency: sequential numbering, orphan figures/tables, ref-before-def order, section balance, abbreviation first-use, citation range (NEW v0.4) |
| `scripts/compile_latex.py <tex_file> --output-dir <dir>` | Compile LaTeX manuscript to PDF |
| `scripts/format_bibtex.py <bib_file> --validate --normalize --output <path>` | Validate and normalize BibTeX entries |
| `scripts/render_word.py <content.json> --template <template.docx> --output <output.docx>` | Fill IEEE Word template with structured content |
| `scripts/generate_rebuttal.py <reviews> --paper <paper> --output <rebuttal>` | Structured reviewer response / rebuttal letter generation (NEW v0.4) |
| `scripts/paper_to_slides.py <paper> --format beamer|markdown --output <slides>` | Paper to presentation slides (Beamer LaTeX / Marp Markdown) + speaker notes (NEW v0.4) |
| `scripts/package_skills.py --output-dir <dir>` | Package skill suite for distribution |

## Module Reference Index

| Module | Directory | What it provides |
|--------|-----------|-----------------|
| Digest | `digest/references/` | Code reading, task taxonomy, evidence rules, project brief template |
| Literature | `literature/references/` | Search strategies, API search guide, citation verification, classic paper maps, related work patterns, literature matrix template |
| Experiment | `experiment/references/` | Metrics guide, claim rules, ablation writing, experiment section patterns, reproducibility checklist |
| Writer | `writer/references/` | Full writing pipeline: title, abstract, introduction, related work, method, experiments, conclusion, discussion patterns; Chinese drafting/polishing; CN→EN conversion; English polishing; forbidden overclaims (CN+EN); de-AI & dedup rules; terminology glossary; quality rubric; template filling guide |
| Templates | `templates/` | Chinese journal LaTeX (cjc), IEEE conference LaTeX (IEEEtran), IEEE conference Word, Cover letter LaTeX |
