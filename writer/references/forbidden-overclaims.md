# Forbidden Overclaims

## Expanded Forbidden Claims List

Do not write these unless explicitly supported by evidence of sufficient strength. "Sufficient" means: multiple datasets, statistical significance, and consistency across settings.

### Absolute Claims

| Forbidden | Safer Alternative | Required Evidence |
|-----------|------------------|-------------------|
| state-of-the-art | achieves the best reported performance on [specific benchmark] | Comparison against prior SOTA on the standard benchmark |
| first / 首次 / 최초 | introduces / proposes (without "first") | Impossible to verify objectively — avoid entirely |
| solves the problem | addresses / alleviates / mitigates | A problem is "solved" only when no meaningful gap remains |
| proves | demonstrates that / suggests that / provides evidence that | "Proof" requires formal mathematical guarantee |
| universally applicable | has been evaluated on [N] datasets spanning [domains] | Evaluation across fundamentally different domains |
| optimal | achieves the best performance among compared methods | Proving optimality requires exhaustive search or proof |

### Exaggerated Magnitude

| Forbidden | Safer Alternative | Required Evidence |
|-----------|------------------|-------------------|
| significantly improves | achieves a [X.X] percentage point improvement over [baseline] | Statistical test + multiple datasets |
| dramatically / substantially | improves by [X]% / outperforms by [X] points | Just report the number; let the reader judge magnitude |
| robust across all scenarios | performs consistently on [evaluated conditions] | Multiple diverse test conditions with stable results |
| comprehensive comparison | comparison with [N] baselines on [M] datasets | Must include all major method families at comparable compute budget |
| negligible cost | requires [X]% more parameters / [Y]ms additional latency | Quantify; let the reader decide what's negligible |

### Unwarranted Generalization

| Forbidden | Safer Alternative | Required Evidence |
|-----------|------------------|-------------------|
| generalizes well | achieves competitive performance on [out-of-domain dataset X] | At least one truly out-of-domain evaluation |
| works for any [X] | has been tested on [specific X varieties] | Multiple varieties tested |
| applicable to real-world scenarios | has been evaluated on [real-world dataset/condition] | Real-world (not simulated) evaluation |
| scalable to [large scale] | scales to [specific size] on [hardware] | Measured scaling behavior |

### Novelty Inflation

| Forbidden | Safer Alternative |
|-----------|------------------|
| completely different from | differs from [specific prior work] in that [specific difference] |
| unprecedented | without direct precedent in [specific area] |
| paradigm shift | introduces a new approach to / explores a new perspective on |
| groundbreaking | contributes to / advances |
| revolutionizes | offers improvements in |

---

## Context-Dependent Detection Rules

Some words are overclaims only in context. Check before flagging:

**"Novel"** — Acceptable if: the contribution is clearly distinguished from all cited prior work AND the novelty is explained (what specifically is new?). Overclaim if: used as a generic adjective ("a novel method" without saying what's novel).

**"Efficient"** — Acceptable if: the paper includes explicit efficiency comparisons (FLOPs, latency, memory) against baselines. Overclaim if: claimed without any efficiency measurement.

**"Simple"** — Acceptable if: the method genuinely has fewer components or lines of code than baselines, and this is shown. Overclaim if: "simple" is used to mask a lack of rigor.

**"Effective"** — Acceptable if: supported by experiment results. Overclaim if: no baseline comparison is provided.

**"Robust"** — Acceptable if: tested under multiple perturbations, domains, or conditions with consistent results. Overclaim if: tested only under standard conditions.

---

## Self-Scan Procedure

After writing, scan for these danger words. For each occurrence, ask:
1. Is this claim supported by evidence in the paper? (Point to specific table/figure.)
2. Is the evidence of sufficient strength for this claim wording? (Check result-claim-rules.md.)
3. Would a skeptical reviewer accept this wording? If not, downgrade.

## Standard Safer Alternatives (Quick Reference)

| Category | Safer Phrasing |
|----------|---------------|
| Performance | achieves competitive performance, matches the best reported results, outperforms [named baselines] on [dataset] |
| Novelty | introduces, proposes, presents, explores |
| Problem-solving | addresses, alleviates, mitigates, reduces the impact of |
| Evidence strength | demonstrates that, suggests that, provides evidence that, is consistent with |
| Improvement claim | improves over [baseline] by [X] percentage points / [Y]% relative improvement |
| Generalization | achieves [X] on [out-of-domain dataset], transfers to [domain] with [Y]% performance |
