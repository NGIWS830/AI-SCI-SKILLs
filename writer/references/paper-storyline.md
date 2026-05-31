# Paper Storyline

Before drafting, establish a coherent storyline. The storyline is the paper's narrative spine — every section, paragraph, and sentence should serve this story.

## Storyline Framework

```markdown
## One-Sentence Contribution
## Research Problem
## Research Gap
## Proposed Method
## Main Evidence
## Why It Matters
## Claims and Evidence
| Claim | Evidence | Citation/Experiment Support | Risk |
|---|---|---|---|
```

## Contribution Narrative Patterns

### Single-Contribution Paper
Most common in CS conferences. One clear technical idea, thoroughly validated.
- **Story arc**: Problem → Why existing solutions fail → Our solution → Evidence it works.
- **Risk**: If the contribution is too thin, reviewers call it "incremental."

### Multi-Contribution Paper
Two or three interrelated contributions (e.g., new module + new loss + new dataset).
- **Story arc**: Problem has multiple facets → Each contribution addresses one facet → Together they enable a system.
- **Risk**: Contributions must be coherent. Three unrelated contributions is not a paper.

### Incremental but Solid
A clear improvement over a specific baseline, with thorough analysis.
- **Story arc**: Existing method X has limitation Y → We fix Y with technique Z → Thorough analysis shows Z works.
- **Risk**: Reviewers may ask "is this just an ablation of X?" Preempt this by explaining why Z is non-obvious.

---

## Storyline Coherence Checks

Before drafting, verify:

1. **Problem-Gap alignment**: Does the problem statement logically imply the gap? (If the problem is "segmentation is slow", the gap shouldn't be "existing methods have low accuracy.")
2. **Gap-Method alignment**: Does the method directly address the gap? Can you trace a straight line from "existing methods fail to do X" to "our method does X"?
3. **Method-Evidence alignment**: Does every method component have a corresponding evidence row (experiment, ablation, or analysis)?
4. **Evidence-Contribution alignment**: Is the contribution statement fully supported by the evidence? If evidence is "moderate" (one dataset), contribution shouldn't claim "generalizes well."

---

## Evidence-Claim Mapping Template

| Claim | Evidence Type | Evidence Source | Strength | Risk |
|-------|--------------|-----------------|----------|------|
| [Module A] improves [capability] | Ablation (Table X) | w/o Module A: [value], with: [value] | Strong | Low |
| [Method] outperforms baselines on [dataset] | Main results (Table Y) | [Our value] vs [baseline value] | Strong | Low |
| [Method] generalizes to [domain] | Cross-dataset (Table Z) | [value] on [out-of-domain dataset] | Moderate | Medium — only one OOD dataset |
| [Mechanism] is the reason for improvement | Qualitative (Fig. X) | Visualization shows [behavior] | Weak | High — correlation, not causation |

If any claim has Risk = High, consider: should this claim be in the paper? If yes, what caveat language is needed?

---

## Storyline Quality Self-Check

1. **One-sentence test**: Can you state the paper's contribution in one sentence that a colleague would understand?
2. **Gap test**: Would a knowledgeable reader say "yes, that's a real gap" or "that's just an engineering detail"?
3. **Evidence test**: For every claim in the storyline, is there at least one table or figure providing evidence?
4. **Scope test**: Is the contribution scope honest? Are you claiming a breakthrough for what is actually a solid incremental improvement?

Do not write a full paper until the storyline is coherent. A coherent storyline means: the gap follows from the problem, the method addresses the gap, the evidence supports the method, and the contribution is fully backed by the evidence.
