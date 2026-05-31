# Quality Rubric

Use this rubric to evaluate the manuscript before declaring it complete. Score each dimension 1-4. A score below 70/100 means the manuscript needs substantive revision.

---

## Dimension 1: Claims-Evidence Alignment (25 points)

**What to evaluate:** Every factual claim in the manuscript must be backed by evidence in the project state file, experiment tables, or verified citations. Claim strength must match evidence strength.

| Score | Criteria |
|-------|----------|
| 4 (25 pts) | Every claim maps to specific evidence in tables/figures/materials. Claim wording matches evidence strength exactly. No overclaims detected. |
| 3 (19 pts) | Most claims have evidence. 1-2 claims have slightly inflated wording or missing evidence anchors. |
| 2 (13 pts) | Multiple claims lack evidence, overstate findings, or reference non-existent tables/figures. |
| 1 (6 pts) | Systematic overclaiming, fabricated evidence, or claims completely disconnected from provided materials. |

**Checklist:**
- [ ] Every contribution bullet in Introduction maps to a specific table/figure/section.
- [ ] Every performance claim ("improves", "outperforms", "achieves") is followed by a specific number.
- [ ] No claim uses "proves" without formal proof.
- [ ] No claim uses "state-of-the-art" without explicit SOTA comparison and statistical test.
- [ ] Claim strength descriptors ("consistently", "substantially", "slightly") match the Stage 3 evidence rating.
- [ ] All numbers in prose match numbers in tables.

---

## Dimension 2: Citation Completeness & Accuracy (15 points)

**What to evaluate:** All citations must be verified against at least one academic database. The manuscript must not contain fabricated references. Required citations for claims, baselines, and datasets must be present.

| Score | Criteria |
|-------|----------|
| 4 (15 pts) | All citations verified via CrossRef, DBLP, or equivalent. Zero `[CITATION NEEDED]` markers. Every claim that relies on prior work has a citation. |
| 3 (11 pts) | Core citations verified. 1-2 peripheral citations unverified and marked `[CITATION NEEDED]`. |
| 2 (8 pts) | Multiple key citations unverified or missing. Multiple `[CITATION NEEDED]` markers in critical positions. |
| 1 (4 pts) | Citations fabricated, systematically unverified, or key claims lack any citation support. |

**Checklist:**
- [ ] All citations in the text appear in the References section.
- [ ] All entries in References are cited in the text.
- [ ] Every `[CITATION NEEDED]` marker counts against this dimension.
- [ ] Baseline methods, datasets, and benchmarks are cited.
- [ ] Citation format is consistent throughout.
- [ ] No citation is provably wrong (wrong venue, wrong year, wrong authors).
- [ ] Self-citations are reasonable in proportion (<20% of total references).

---

## Dimension 3: Method Description Precision (20 points)

**What to evaluate:** The method section must describe the proposed approach with sufficient precision that a knowledgeable researcher could re-implement it. Every module, equation, and design choice must be explained.

| Score | Criteria |
|-------|----------|
| 4 (20 pts) | Every module described with input/output/process/rationale. Notation consistent throughout. All equations have symbols explained. Implementation details complete (optimizer, LR, batch size, epochs, hardware, seeds). |
| 3 (15 pts) | Most modules well-described. 1-2 minor details omitted or ambiguous. Notation mostly consistent. |
| 2 (10 pts) | Modules described at surface level only. Missing key details. Notation inconsistent or unexplained. |
| 1 (5 pts) | Method description is vague, unfalsifiable, or missing entirely. Key equations absent. No implementation details. |

**Checklist:**
- [ ] III-A Overview references an architecture figure.
- [ ] Each III-B/C/D subsection covers: Input → Process → Output → Rationale → Connection to claims.
- [ ] Every symbol in every equation is explained in surrounding prose.
- [ ] Dimensions are annotated on first use.
- [ ] Training details include: optimizer, LR schedule, batch size, epochs, hardware, data augmentation.
- [ ] Loss function terms are clearly defined and motivated.
- [ ] Any pseudocode has clear Input/Output specifications.

---

## Dimension 4: Experiment Reporting Rigor (25 points)

**What to evaluate:** Experiments must be reported with sufficient detail to assess the validity of the claims. Metrics, baselines, datasets, and analysis must be complete and honest.

| Score | Criteria |
|-------|----------|
| 4 (25 pts) | All metrics defined with direction. All baselines described. Implementation details complete. Standard deviations reported. Ablation covers every method component. Statistical tests where appropriate. | 
| 3 (19 pts) | Most details present. 1-2 minor omissions (e.g., missing std for one table, one baseline not fully described). |
| 2 (13 pts) | Several key experimental details missing. No standard deviations. Incomplete ablation. |
| 1 (6 pts) | Results fabricated, critically incomplete, or metrics undefined. No ablation or baseline comparison. |

**Checklist:**
- [ ] Every metric has its direction stated (higher is better / lower is better).
- [ ] Standard deviations or confidence intervals are reported.
- [ ] Every baseline is described (name, citation, configuration).
- [ ] Datasets are described (size, splits, preprocessing).
- [ ] Ablation covers every claimed contribution component.
- [ ] Main results table uses bold for best, underline for second-best.
- [ ] Qualitative examples show both successes and failures.
- [ ] Efficiency metrics (parameters, FLOPs, latency) are reported if claimed.
- [ ] Statistical significance is reported if claiming superiority.
- [ ] Missing analyses are marked `AUTHOR_INPUT_NEEDED` rather than fabricated.

---

## Dimension 5: Language Quality (15 points)

**What to evaluate:** The manuscript must use appropriate academic register, consistent terminology, correct grammar, and clear logical flow. Language should not distract from the scientific content.

| Score | Criteria |
|-------|----------|
| 4 (15 pts) | Academic register consistent. Terminology uniform throughout. Grammar and style correct. Logical flow clear — reader never confused about the argument. |
| 3 (11 pts) | Minor language issues (occasional colloquialism, slight terminology drift) that don't affect comprehension. |
| 2 (8 pts) | Frequent language issues affecting readability. Consistent terminology problems. |
| 1 (5 pts) | Language severely impedes understanding. Pervasive errors. |

**Checklist:**
- [ ] No informal/colloquial expressions in the English version.
- [ ] Technical terms are consistent throughout (same concept = same term).
- [ ] Chinese terminology maps 1:1 to English terminology.
- [ ] Sentence variety: no >3 consecutive sentences starting with "We".
- [ ] Paragraph length balanced: no 1-sentence or >12-sentence paragraphs.
- [ ] All abbreviations defined on first use.
- [ ] Figure and table cross-references are correct.
- [ ] Transition words are used appropriately at logical boundaries.

---

## Scoring Summary

| Dimension | Weight | Score (1-4) | Weighted Score |
|-----------|--------|-------------|----------------|
| Claims-Evidence Alignment | 25% | ___ | ___ / 25 |
| Citation Completeness | 15% | ___ | ___ / 15 |
| Method Description Precision | 20% | ___ | ___ / 20 |
| Experiment Reporting Rigor | 25% | ___ | ___ / 25 |
| Language Quality | 15% | ___ | ___ / 15 |
| **Total** | **100%** | | **___ / 100** |

### Interpretation

| Score | Rating | Action |
|-------|--------|--------|
| 90-100 | Excellent | Ready for author review. Minor polish only. |
| 80-89 | Good | Ready for author review. Fix identified should-fix issues. |
| 70-79 | Needs Revision | Fix must-fix issues, re-run critique. |
| 50-69 | Not Ready | Return to relevant Stage 4 sub-stage for substantive revision. |
| <50 | Critical Issues | Return to Stage 1-3 to fill major evidence/citation gaps. |

---

## How to Use This Rubric

1. **Read the complete manuscript** before scoring any dimension.
2. **For each dimension**, read the checklist items and the score descriptors. Choose the score that best matches the manuscript.
3. **Document issues found** for each dimension. Be specific: "Claim X on page 3 says 'significantly improves' but evidence is one dataset with +1.2 points."
4. **Compute the weighted total**. If <70, identify which sub-stage to return to:
   - Claims/Citations issues → Stage 2 (LIT) or Stage 3 (EXPER)
   - Method/Experiment issues → Stage 1 (DIGEST) or Stage 3 (EXPER)
   - Language issues → Stage 4c (Chinese Polish) or 4e (English Polish)
5. **Re-score after revision.** Iterate until score ≥ 80.
