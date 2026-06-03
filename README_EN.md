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
Stage 1: DIGEST → File inventory, deep code analysis, notebook parsing, dependency tracing, auto-generate project brief
Stage 2: LIT    → Literature search (API), AI auto-filled matrix, verification, gap analysis, narrative synthesis (matrix→Introduction+Related Work)
Stage 3: EXPER  → Experiment planning, improvement calculation, statistical analysis, visualization, narrative synthesis
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
│   └── scripts/     — summarize_repo.py, extract_architecture.py,
│                      parse_notebooks.py, trace_dependencies.py,
│                      synthesize_brief.py
├── literature/    — Search → auto-fill matrix → verify → gap analysis → narrative synthesis
│   ├── references/  — Search strategies, API guide, citation verification, classic paper maps,
│   │                  literature synthesis guide (matrix→narrative)
│   └── scripts/     — search_literature.py, auto_fill_matrix.py, verify_citations.py,
│                      analyze_citations.py, synthesize_literature.py
├── experiment/    — Analyze experiments and validate claims
│   ├── references/  — Metrics guide, claim rules, ablation writing, reproducibility checklist
│   └── scripts/     — compute_improvements.py, statistical_tests.py,
│                      result_visualizer.py, design_experiments.py,
│                      synthesize_experiments.py
├── writer/        — Chinese draft → polish → EN conversion → EN polish → Self-critique
│   └── references/  — Full section templates, CN-EN translation corpus, terminology glossary, quality rubric
├── scripts/       — Quality checks, claim-evidence audit, cross-reference validation,
│                    LaTeX compilation, BibTeX formatting, Word rendering,
│                    rebuttal generation, paper-to-slides
└── templates/     — 11 conference/journal templates (CN/EN, CV/ML/NLP/AI/RS/CI/IP),
                     Cover Letter
```

---

## Pipeline Detailed Mechanisms

> The following sections unpack the operational semantics of each stage: role instructions, decision trees, scoring criteria, threshold logic, and audit procedures. These are the core rules from SKILL.md that drive AI agent behavior.

### Stage 0 — INIT: Material Inventory & State Setup

**Purpose**: Inventory all user-provided materials and create a project state file that tracks the pipeline.

1. Ask the user for: output directory, target venue/journal, and any specific requirements.
2. Identify all materials: code repos, README, configs, logs, experiment tables (CSV/Excel), framework diagrams, notes (Word/TXT/Markdown), prior drafts, literature lists.
3. Create `<output_dir>/project-state.md` with material inventory, target venue, pipeline progress checkboxes, stage output placeholders, and a missing-author-input log.
4. Update status to `STAGE 1 | DIGEST`.

**Two core annotation conventions (used throughout all stages):**
- `AUTHOR_INPUT_NEEDED`: information requiring author input (never fabricate)
- `[CITATION NEEDED]`: citations not yet cross-verified against databases

---

### Stage 1 — DIGEST: Project Digestion

**Purpose**: Extract paper-ready facts from project materials and produce a structured project brief.

**5-Step Chain-of-Thought:**

```
STEP 1: TASK IDENTIFICATION
→ What is the research task? (classification/detection/segmentation/generation/retrieval/...)
→ Input modality? (image/text/audio/video/multimodal)
→ Output format? (class label/mask/bounding box/text/embedding)

STEP 2: METHOD EXTRACTION
→ Backbone? (ResNet/ViT/BERT/GPT/custom)
→ Novel modules? Every nn.Module subclass or custom function
→ Training objective? Every loss term
→ Inference pipeline? Step-by-step description

STEP 3: EVIDENCE GROUNDING
→ HIGH: directly visible in code/configs/notes (e.g., "uses CrossEntropyLoss" confirmed at loss.py:42)
→ MEDIUM: strongly implied but not fully specified (e.g., "uses AdamW" inferred from config keys)
→ LOW: plausible interpretation requiring author confirmation

STEP 4: GAP ANALYSIS
→ What datasets are claimed but lack provided splits?
→ What metrics are mentioned but have no computed values?
→ What baselines are named but lack implementation details?
→ What hyperparameters are missing?

STEP 5: CONTRIBUTION CANDIDATES
→ For each candidate: what is novel + what evidence supports it + what validation is still needed
```

**5-Script Chain:**
```
summarize_repo.py → extract_architecture.py → parse_notebooks.py → trace_dependencies.py → synthesize_brief.py
```
`synthesize_brief.py --repo <path>` runs the full digest pipeline end-to-end in one command.

**Output**: `00_project_brief.md` — research task, method module→evidence mapping table, data flow, candidate contributions, missing information checklist, paper-writing risks.

**Transition**: Update status to `STAGE 2 | LIT`. If critical information is missing, ask the user before proceeding.

---

### Stage 2 — LIT: Literature Review

**Purpose**: Build verified literature support — classic foundations, recent SOTA, method-family papers, dataset papers, and gap evidence.

**Query Derivation Rules** (extract 3-5 key technical terms from Stage 1; generate 3 query variants per term):

| Variant | Pattern | Example |
|---------|---------|---------|
| Broad | `"<task> <method_family>"` | `"text-to-image retrieval cross-modal alignment"` |
| Specific | `"<task> <specific_technique>"` | `"cross-modal retrieval contrastive learning"` |
| Gap-focused | `"<task> limitation <pain_point>"` | `"text-image retrieval fine-grained alignment"` |

**Literature Matrix Column Meanings:**

| Column | Description |
|--------|-------------|
| Relation to Our Work | 5 categories: direct competitor / method inspiration / baseline comparison / dataset source / gap evidence |
| Use in Paper | Which section and for what purpose (e.g., "Intro para 2 — representative method") |
| Verification | 3-tier: ✓ confirmed (DOI+arXiv) / ~ single source / ✗ unverified |

**Classic Paper Seed Maps**: `cv-classic-papers.md` / `nlp-classic-papers.md` / `multimodal-classic-papers.md` catch high-impact older papers that automated search might miss.

**Literature Narrative Synthesis (NEW v0.4)**: `synthesize_literature.py` converts the matrix into logically organized Introduction and Related Work prose — organized by paradigm, not paper-by-paper; includes topic sentences, evolutionary arcs, method differentiation, and logical flow checks.

**Script Chain**: `search_literature.py` → `auto_fill_matrix.py` → `verify_citations.py` → `analyze_citations.py` → `synthesize_literature.py`

**Output**: `02_literature_matrix.md` — search queries, literature matrix, Related Work theme structure, research gap evidence, citation gaps.

**Transition**: Update status to `STAGE 3 | EXPER`.

---

### Stage 3 — EXPER: Experiment Analysis

**Purpose**: Convert experiment artifacts into evidence-grounded result claims.

**Claim-Strength Decision Tree** (every claim must pass through):

```
Q1: Is the improvement direction correct given the metric?
    → Check higher-is-better vs lower-is-better. If unsure, flag AUTHOR_INPUT_NEEDED.

Q2: Is the improvement consistent across datasets/settings?
    → Consistent (all datasets) → STRONG
    → Mixed (most datasets)     → MODERATE
    → Single dataset            → WEAK
    → No direct evidence        → UNSUPPORTED — do not claim.

Q3: Is the improvement large enough to matter?
    → Classification >1pp | Detection >1 mAP | Segmentation >1 mIoU/Dice | Generation >1 BLEU
    → Below threshold → use "comparable to" / "on par with"

Q4: Could confounding factors explain the improvement?
    → Different backbone capacity? Training budget? Data preprocessing?
    → If yes, flag as caveat.
```

**Results Paragraph Fill-in-the-Blank Template:**
> As shown in Table [X], [Method] achieves [value] on [dataset], [direction] the strongest baseline [baseline] by [absolute] ([relative]%). On [dataset_2], [Method] achieves [value_2], a [absolute_2] improvement over [baseline_2]. These results demonstrate that [component] contributes to [capability], as evidenced by [specific_evidence].

**Visual Ablation Design (NEW v0.4):**

Ablation studies need both quantitative metrics and visual evidence of HOW each component works. See `experiment/references/ablation-writing.md` "Visual Ablation Analysis" for full guidance, covering **10 visualization types**:

| If your claim is... | Primary visualization |
|-----|------|
| "Our module improves feature quality" | t-SNE / PCA embedding |
| "Our module guides attention to the right regions" | Grad-CAM heatmap |
| "Our gating mechanism selects informative channels" | Channel weight distribution |
| "Our loss function improves class separability" | t-SNE + silhouette score |
| "Our method handles challenging cases better" | Error case comparison |
| "Our module accelerates convergence" | Training dynamics curves |
| "Our attention mechanism is more interpretable" | Attention map + rollout |
| "Our filters learn more diverse patterns" | Filter / kernel visualization |

Also covered: Feature Map Comparison, Confusion Matrix Difference, Prediction Confidence Distribution. Every visual ablation figure follows a 5-step prose pattern: state the question → describe setup → point to key observations → interpret mechanistically → link to quantitative evidence.

**5 Scripts**: `design_experiments.py` (experiment plan) → `compute_improvements.py` (improvements + Bootstrap CI) → `statistical_tests.py` (effect sizes/significance/multiple comparison correction/power analysis) → `result_visualizer.py` (6 chart types) → `synthesize_experiments.py` (narrative synthesis).

**Output**: `03_experiment_analysis.md` — tables analyzed, main results, improvement over baselines, ablation findings, claim→evidence mapping (with strength level and caveats).

**Transition**: Update status to `STAGE 4 | WRITE`.

---

### Stage 4a — Storyline

**Purpose**: Distill the paper's single scientific narrative before drafting.

**5-Element Structure:**
- **Problem**: The ONE scientific question the paper answers (one sentence)
- **Gap**: The missing piece of knowledge, with a "because" clause
- **Method**: Core mechanism in 2-3 sentences (module-level)
- **Evidence**: 2-3 key experimental results supporting the claims
- **Contribution**: One sentence, aligned with evidence

**5-Point Self-Check:**
1. Does the problem statement match what the method actually solves?
2. Is the gap articulated with specificity (not "few works study X" but "existing methods fail to handle Y because Z")?
3. Does the method description highlight the novel part, not the standard pipeline?
4. Does every contribution bullet trace to evidence in Stage 1 or Stage 3?
5. Is the contribution scope honest — claiming only what the evidence supports?

---

### Stage 4b — Chinese Draft (`05_chinese_draft.md`)

**Role Instruction:**
> You are now drafting a Chinese academic paper manuscript. Your goal is to produce a complete, logically coherent first draft where every factual claim is grounded in the project state file's evidence. Write in formal Chinese academic register. Use short to medium sentences (20-50 characters). Prefer passive voice; avoid using "we" (我们) as the subject. Every paragraph should have a clear topic sentence. Preserve all `AUTHOR_INPUT_NEEDED` and `[CITATION NEEDED]` markers.

**Section-by-Section Guidance:**

| Section | Structure Rules |
|---------|----------------|
| **Title** | Propose 3 variants; choose the most specific and least overclaiming. Pattern: `[Method Name]: [Core Mechanism] for [Task]` |
| **Abstract** | 2-6-2 structure, exactly 10 sentences: 2 background/gap + 6 method (signaled by First/Second/Finally; each pair = claim + why-it-works) + 2 experimental results/conclusion. ~210 words |
| **Introduction** | 5 paragraphs: task importance → current progress (2-3 method families) → remaining gap (with "because" clause) → proposed method (core mechanism in 2-3 sentences) → contributions (prose lead-in then 3 detailed bullets, each matching one innovation point with evidence) |
| **Related Work** | Theme-based (from Stage 2), 1 paragraph per theme: theme statement → 2-3 papers with comparison → how your method differs. Avoid laundry-list pattern |
| **Method** | Main heading "方法", 3-5 sentence overview of the full framework (no separate Overview subsection), then three innovation points each as a sub-heading. Each innovation follows motivation→design→formula/mechanism→effect, with optional module diagrams or pseudocode |
| **Experiments** | 5 subsections: Datasets & Metrics → Experimental Setup → Comparison with SOTA and Classical Methods → Ablation Study (numbered list 1), 2), 3)...) → Visualization |
| **Conclusion** | Two paragraphs: first = full summary (problem→method→key results with numbers), second = limitations + future work. No new citations or claims |

---

### Stage 4c — Chinese Polish (`06_chinese_polished.md`)

**Role Instruction:**
> You are now polishing a Chinese academic manuscript. Polish for academic clarity, logical flow, and concise expression. The goal is NOT to make the text flowery — it is to remove ambiguity, tighten logic, eliminate redundancy, and ensure every paragraph earns its place. Scientific meaning is sacred — never alter it to sound better.

**De-AI Scan (4 categories of Chinese AI boilerplate):**
1. Generic openers ("近年来，随着...的发展") → concrete problem statements
2. Generic closers ("综上所述，本文提出的方法有效...") → specific findings
3. Hollow modifiers ("强大的性能", "良好的效果") → replace with specific numbers
4. Over-explanation of basic concepts → delete (SCI reviewers already know them)

**Cross-Section Dedup:**
- Method details appear ONLY in Method section, not Introduction
- Results appear ONLY in Experiments section, not Method
- Abstract, Introduction, and Conclusion use distinct phrasing
- No two sections share near-identical sentences

**10-Item Polishing Checklist:**

| # | Check | Before (BAD) | After (GOOD) |
|---|-------|-------------|--------------|
| 1 | Remove empty modifiers | 该方法取得了较好的性能提升 | 该方法在Cityscapes上提升了2.3 mIoU |
| 2 | Add missing subjects (impersonal) | 使用ResNet-50作为骨干网络 | ResNet-50 is adopted as the backbone |
| 3 | Split long sentences (>50 chars) | (a 60-character run-on) | (two 25-35 character sentences) |
| 4 | Unify terminology | Mixed 注意力机制/Attention机制 | Unify to one term (with English on first use) |
| 5 | Remove redundant pairs | 精度和准确率均得到提升 | 精度提升了1.2个百分点 (specify which metric) |
| 6 | Strengthen weak transitions | 另外，我们还做了... | 在效率方面，进一步分析了... |
| 7 | Ground vague claims | 性能优于所有基线方法 | On all three datasets, the proposed method outperforms all baselines (Table 2) |
| 8 | Fix dangling references | 如图所示 | 如图3所示 |
| 9 | Align parallel structures | 我们提出了X，设计了Y，以及对Z进行了优化 | X is proposed, Y is designed, Z is optimized |
| 10 | Check claim-consistency | CN "显著提升" vs EN "significant" | Ensure magnitude language matches Stage 3 evidence strength |

**Logic Flow Audit**: At each paragraph boundary, ask: does it follow logically? New information or restated? Is the argument chain unbroken?

**Redundancy Detection**: Scan for consecutive same-meaning sentences, identical wording across sections, repeated numbers without added interpretation.

---

### Stage 4d — CN→EN Conversion (`07_english_draft.md`)

**Role Instruction:**
> You are now converting a polished Chinese academic manuscript into English SCI prose. This is NOT literal translation. You are rewriting: restructure sentences from Chinese topic-comment pattern to English SVO pattern, add explicit subjects where Chinese omitted them, convert Chinese aspect markers to English tense, add articles (a/an/the), and maintain academic register throughout. Preserve all numbers, metric values, citation markers, and claim strength EXACTLY.

**Tense Conventions:**

| Section | Primary Tense | Exceptions |
|---------|--------------|------------|
| Abstract | Present | Past for evaluation: "Performance was evaluated on..." |
| Introduction | Present | Past for "Previous methods struggled...", Present perfect for "Recent work has shown..." |
| Related Work | Present perfect / Present | Past for specific historical results |
| Method | Present | — |
| Experiments | Past | Present for "Table 1 reports..." |
| Conclusion | Present | Past for summarizing specific results |

**Voice Conventions:**

| Section | Guidance |
|---------|----------|
| Abstract | Passive preferred: "A novel X is proposed..." |
| Introduction | Passive / impersonal for contribution bullets (Para 5): "This paper presents...", "A novel X is introduced..."; active acceptable for narrative setup (Paras 1-4). Do NOT write "We propose X" in contribution bullets |
| Related Work | Passive for existing methods; impersonal for differentiation: "This work differs from..." |
| Method | Passive preferred for process; passive / impersonal for design rationale: "X is designed to...", "This module enables..." |
| Experiments | Passive preferred for procedure: "Models were trained on..."; passive for narrative: "As shown in Table 1, the proposed method achieves..." |
| Conclusion | Passive / impersonal preferred: "This paper has presented..." |

**Claim-Strength Mapping (key entries):**

| Chinese | Overclaiming English ✗ | Safer English ✓ |
|---------|----------------------|-----------------|
| 显著提升 | significantly improves | achieves a X.X pp improvement |
| 解决了...问题 | solves the problem of... | addresses / alleviates / mitigates |
| 优于现有方法 | outperforms all existing methods | outperforms [named baselines] on [specific datasets] |
| 首次提出 | is the first to / novel | proposes (no "first" unless verifiable) |
| 证明了 | proves that | demonstrates that / provides evidence that |

**5 CN→EN Translation Pitfalls**: topic-prominence transfer (add subjects), modifier stacking (pre→post), parallel structure (repetition→conjunction reduction), zero article→article, aspect→tense.

---

### Stage 4e — English Polish (`08_english_polished.md`)

**Role Instruction:**
> You are now polishing an English SCI manuscript. Polish for: academic register, sentence variety, cohesion, precision, and readability. Do NOT change scientific content, add unsupported claims, or strengthen claim wording. If in doubt about whether a change alters meaning, keep the original.

**De-AI Scan (5 categories of English AI boilerplate):**
1. Generic openers ("In recent years, there has been growing interest in...") → concrete statements
2. Overused connectors (Moreover, Furthermore, In addition) → max 2 per section
3. Hollow adjectives ("powerful", "effective", "promising") → specific evidence or delete
4. Formulaic conclusions ("These results demonstrate the effectiveness of our approach.") → delete
5. Over-explanation of basic concepts (CNN, attention, transformer basics) → delete

**Sentence Variety Audit:**
- Count "We"-starting sentences per section. If >3 consecutive, restructure (e.g., "The model achieves...", "Results on [dataset] show...")
- Sentence length: if all sentences in a paragraph are 25-35 words, mix in a short punchy sentence (10-15 words)
- Paragraph length: no 1-sentence paragraphs or >12-sentence paragraphs

**Cohesion Device Injection (6 categories):**

| Function | Connectors |
|----------|-----------|
| Addition | furthermore, moreover, in addition |
| Contrast | however, in contrast, conversely, whereas |
| Cause-effect | therefore, consequently, as a result, thus |
| Exemplification | for instance, specifically, in particular |
| Emphasis | notably, importantly |
| Sequence | first, second, finally, subsequently |

**Academic Register Check (informal → formal):**
"a lot of" → "substantial" / "considerable" · "big"/"huge" → "large" / "considerable" · "get" → "obtain" / "achieve" · "find out" → "determine" / "identify" · "look at" → "examine" / "investigate"

**Additional checks**: scan `forbidden-overclaims.md` for banned English terms; produce revision notes `09_revision_notes.md`.

---

### Stage 4f — Self-Critique (`10_critique_report.md`)

**Purpose**: Before declaring the paper complete, conduct a systematic self-critique using the quality rubric and automated checks.

**Role Instruction:**
> You are now the reviewer of this manuscript. Adopt a critical, skeptical stance. Your job is to find every weakness, overclaim, missing citation, and imprecise statement. Be harsh but fair. Rate each dimension honestly — inflating scores helps no one.

**5-Dimension Scoring (1-4 scale, weighted to 100):**

| Dimension | Weight | What It Evaluates |
|-----------|--------|-------------------|
| Claims-Evidence Alignment | **25%** | Does every factual claim have a table/figure/section reference? Does wording match evidence strength? |
| Citation Completeness & Accuracy | **15%** | Are citations verified via CrossRef/DBLP? Are `[CITATION NEEDED]` markers >3? |
| Method Description Precision | **20%** | Does each module cover input/output/process/rationale? Notation consistent? Implementation details complete? |
| Experiment Reporting Rigor | **25%** | Metric directions stated? Std devs reported? Baselines described? Ablation covers all claimed contributions? |
| Language Quality | **15%** | Academic register consistent? Terminology uniform? Sentence variety? No AI boilerplate? |

**Three-Tier Score Thresholds:**

| Score | Verdict | Action |
|-------|---------|--------|
| **≥ 80/100** | READY | Proceed to Stage 4g Template Rendering |
| **70-79/100** | NEEDS REVISION | Fix identified issues, re-run critique |
| **< 70/100** | NOT READY | Return to the relevant sub-stage for substantive revision |

**Fallback Guidance (by failing dimension):**
- Claims/Citation issues → Stage 2 (LIT) or Stage 3 (EXPER)
- Method/Experiment issues → Stage 1 (DIGEST) or Stage 3 (EXPER)
- Language issues → Stage 4c (Chinese Polish) or 4e (English Polish)

**5 Manual Audits:**

| Audit | What It Checks |
|-------|---------------|
| **Claims Audit** | List every factual claim → locate evidence source → flag unsupported claims → flag overstated wording |
| **Citation Audit** | Count citation markers → `[CITATION NEEDED]` >3 means paper is not ready → bidirectional text↔references verification |
| **Overclaim Scan** | Scan CN+EN banned terms (`forbidden-overclaims.md`) → check each in context → rewrite or caveat |
| **Readability Audit** | Figure/table referenced in text BEFORE it appears → cross-reference consistency → abstract standalone comprehensibility |
| **Terminology Audit** | Inconsistent term detection → abbreviation first-use check → bilingual 1:1 term mapping |

**Automated Check**: `python scripts/check_quality.py <output_dir> --all --output 10a_auto_check.md` (9 checks: claims alignment, citation completeness, reproducibility, language quality, structure, CN overclaims, dedup, AI-flavor, terminology consistency)

**Output Report Structure**: per-dimension score + detailed issues + automated check results + must-fix list + should-fix list + overall recommendation (READY / NEEDS REVISION / NOT READY)

---

### Stage 4g — Template Rendering

**5-Step Process:**
1. **Chinese LaTeX**: Copy `templates/chinese/`, fill from `06_chinese_polished.md`, compile with XeLaTeX
2. **English LaTeX**: Copy `templates/ieee-latex/`, fill from `08_english_polished.md`, generate `references.bib`, compile with pdflatex
3. **English Word**: Build `word_content.json`, run `render_word.py` against IEEE Word template
4. **Cover Letter**: 5-paragraph structure (submission statement / background+contributions / key findings / why this journal / declarations), LaTeX + Word dual format. Cover letter must NOT copy-paste the abstract; all overclaim rules apply doubly
5. **Cross-Template Consistency Check**: titles match / author order matches / all metric values identical / citation counts consistent / Cover Letter claims ≤ manuscript claims / no `[CITATION NEEDED]` or `AUTHOR_INPUT_NEEDED`

**11 Available Templates**: Chinese Journal / IEEE Conference / IEEE TGRS / IEEE TETCI / IEEE TIP / CVPR·ICCV / NeurIPS·ICML / ACL·EMNLP / AAAI·IJCAI / IEEE Word / Cover Letter

---

### Post-Submission Tools (NEW v0.4)

| Tool | Script | Function |
|------|--------|----------|
| Rebuttal | `generate_rebuttal.py` | Comment auto-classification / per-comment response template / cross-reviewer consistency check / Markdown + LaTeX output |
| Paper-to-Slides | `paper_to_slides.py` | Beamer LaTeX / Marp Markdown dual format + speaker notes |

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
# -- Stage 1: Inventory -> Architecture -> Notebooks -> Dependencies -> Brief --
python digest/scripts/summarize_repo.py my_project/ --output repo_inventory.md
python digest/scripts/extract_architecture.py my_project/ --output arch_report.md
python digest/scripts/parse_notebooks.py experiments/*.ipynb --output-dir ./digest/
python digest/scripts/trace_dependencies.py my_project/ --entry train.py --output deps.md
python digest/scripts/synthesize_brief.py --repo my_project/ --output project_brief.md

# -- Stage 2: Literature search -> fill matrix -> verify -> analyze -> synthesize --
python literature/scripts/search_literature.py "cross-modal retrieval contrastive learning" \
    --sources s2,arxiv --max 30 --output results.md
python literature/scripts/auto_fill_matrix.py results.md \
    --project-brief project_brief.md --output lit_matrix.md
python literature/scripts/verify_citations.py citations.txt --sources crossref,dblp
python literature/scripts/analyze_citations.py lit_matrix.md --output gap_analysis.md
python literature/scripts/synthesize_literature.py lit_matrix.md \
    --project-brief project_brief.md --output synthesis.md

# -- Stage 3: Design -> Analyze -> Test -> Visualize -> Synthesize --
python experiment/scripts/design_experiments.py \
    --project-brief project_brief.md --venue cvpr --output experiment_plan.md
python experiment/scripts/compute_improvements.py results.csv \
    --target MyModel --metrics R@1 R@5 R@10 \
    --higher-better R@1 R@5 R@10 --group-cols Dataset --stats --output improvements.md
python experiment/scripts/statistical_tests.py results.csv \
    --target MyModel --metrics R@1 R@5 R@10 \
    --higher-better R@1 R@5 R@10 --output stats_report.md
python experiment/scripts/result_visualizer.py results.csv \
    --target MyModel --metrics R@1 R@5 R@10 --output-dir ./figures/
python experiment/scripts/synthesize_experiments.py \
    --improvements improvements.md --stats stats_report.md \
    --project-brief project_brief.md --output exp_synthesis.md

# -- Stage 4f: Quality checks + Claim-evidence audit + Cross-reference validation --
python scripts/check_quality.py output_dir/ --all --output quality_report.md
python scripts/claim_evidence_auditor.py paper.md \
    --output-dir output_dir/ --output claim_audit.md
python scripts/validate_references.py paper.md --output ref_report.md

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

**Experiment Full Pipeline (Stage 3 — Fully Upgraded)**
- **Experiment design planner** — derives required experiments and ablation variants from claims, baseline coverage check, phased roadmap
- Improvement calculation + Bootstrap CI (v0.3 + v0.4 enhanced)
- Statistical testing: effect sizes, significance tests, multiple comparison correction, power analysis
- Result visualization: 6 chart types (PNG/PDF/SVG/PGF)
- **Experiment narrative synthesis** — auto-generates paragraph templates for Setup / Results / Ablation / Efficiency / Discussion

**Quality Assurance Suite (Stage 4f — NEW)**
- **Quality Scoring** — 5-dimension 100-point automated check
- **Claim-Evidence Audit** — extracts all factual claims, traces to table/figure refs, cross-verifies numbers, detects overclaims
- **Cross-Reference Validator** — sequential numbering check, orphan object detection, ref-before-def order, abbreviation first-use, citation range

**Project Digestion (Stage 1 — Fully Upgraded)**
- File inventory + deep code analysis (nn.Module / Flax / Keras subclass extraction)
- Jupyter Notebook parsing (model definitions, training loops, hyperparameters, results tables)
- Cross-file dependency tracing (import graph, data flow, core pipeline identification, orphan detection)
- Loss function parsing, hyperparameter detection, framework identification, training infrastructure detection
- **Project brief auto-synthesis** — one-click complete `project_brief.md` generation (`--repo` mode for end-to-end)

**Post-Submission Tools (Stage 4 — NEW)**
- Reviewer rebuttal letter generation (Markdown / LaTeX), comment auto-classification, cross-reviewer consistency check
- Paper-to-slides conversion (Beamer LaTeX / Marp Markdown) + speaker notes

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
pip install jupyter             # parse_notebooks.py for .ipynb files (usually pre-installed)
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
