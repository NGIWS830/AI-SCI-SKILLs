# Abstract Patterns

## Primary Structure: 2-6-2 (10 sentences, ~210 English words)

Every abstract follows a fixed 10-sentence structure divided into three parts. This structure is mandatory — it ensures every abstract is comparably detailed, reviewer-friendly, and self-contained.

```
Part 1 — Background & Gap (2 sentences, ~40 words)
  Sentence 1: Task context + why it matters
  Sentence 2: Specific gap — what existing methods fail to do, and WHY

Part 2 — Method (6 sentences, ~130 words)
  Sentences 3-4  [First]:  Component 1 — what it does + why it works
  Sentences 5-6  [Second]: Component 2 — what it does + why it works
  Sentences 7-8  [Finally]: Innovation 3 — what it does + why it works

Part 3 — Results & Implication (2 sentences, ~40 words)
  Sentence 9:  Key quantitative result (dataset + metric + value)
  Sentence 10: Broader implication or what this enables
```

### Why This Structure

- **2 sentences for background/gap** forces you to name ONE specific gap, not a vague "many challenges remain."
- **6 sentences for method** ensures the core technical contribution is communicated precisely. Readers who stop after the abstract should understand WHAT you built and WHY it works.
- **2 sentences for results/implication** prevents result-dumping. Pick the single most important number; the rest belongs in the paper body.

### Method 6-Sentence Rules

Each pair follows the pattern: **claim → mechanism/justification**.

| Pair | Signal | Sentence 1 (Claim) | Sentence 2 (Why) |
|------|--------|-------------------|-------------------|
| 1 | **First,** | What is the first key component or mechanism? | How does it work? What does it enable? |
| 2 | **Second,** | What is the second key component or mechanism? | How does it complement the first? What gap does it fill? |
| 3 | **Finally,** | What is the third innovation or key design choice? | How does it complement the first two? What gap does it fill? |

**If the method has fewer than 3 clear innovations:**
- Sentences 3-4 [First]: Innovation 1 — what it does + why it works
- Sentences 5-6 [Second]: Innovation 2 — what it does + why it works
- Sentences 7-8 [Finally]: Key design choice, training strategy, or efficiency constraint + why it matters

**If the method has only one core innovation:**
- Sentences 3-4 [First]: Core mechanism + why it works
- Sentences 5-6 [Second]: Key design choice or training strategy + why it matters
- Sentences 7-8 [Finally]: How it differs from prior work + resulting capability

**If the method has more than 3 innovations:** merge the less central ones under the closest-fitting signal word.

### Word Budget

| Language | Target | Hard Range | Check |
|----------|--------|------------|-------|
| English | 210 words | 180–250 words | Count words, not characters |
| Chinese | 250 characters | 200–280 characters | Count Chinese characters (punctuation excluded) |

Venue-specific adjustments:
- CVPR/ICCV/ECCV, NeurIPS/ICML/ICLR, ACL/EMNLP/NAACL, AAAI/IJCAI: stay within 250 words
- TPAMI/TIP/TNNLS (journal): up to 300 words allowed, but 210 remains the recommended target

---

## Sentence Template Bank

### Part 1: Background & Gap (Sentences 1-2)

**Sentence 1 — Context:**
- "[Task] is a fundamental challenge in [field] with applications in [app1], [app2], and [app3]."
- "Accurate [task] is critical for [downstream_application], yet it remains challenging because [core_difficulty]."
- "The ability to [task_verb] accurately is essential for [application], where [requirement]."

**Sentence 2 — Gap (must contain a "because" clause):**
- "Existing [method_family] methods [what_they_do], but they [limitation], particularly when [specific_scenario]."
- "A key limitation of current approaches is their inability to [specific_capability], because [root_cause]."
- "While recent methods have improved [aspect_A], they still struggle with [aspect_B] due to [root_cause]."

### Part 2: Method (Sentences 3-8)

**First (Sentences 3-4):**
- S3: "First, this paper [designs / proposes] a [component_name] that [what_it_does_in_one_clause]."
- S4: "This [enables / ensures / allows] [specific_capability] by [mechanism]."

**Second (Sentences 5-6):**
- S5: "Second, this paper [designs / proposes] a [component_name] that [what_it_does_in_one_clause]."
- S6: "This [addresses / complements / overcomes] [specific_limitation] by [mechanism]."

**Finally (Sentences 7-8):**
- S7: "Finally, this paper [designs / proposes] a [component_name / strategy] that [what_it_does_in_one_clause]."
- S8: "This [complements / extends / addresses] [aspect] by [mechanism], [specific_benefit]."

**Alternative for papers with fewer than 3 innovations (Sentences 3-8):**

If the method has only two clear innovations, the third pair describes a key design choice or training strategy:
- Sentences 3-4 [First]: Innovation 1 — what it does + why it works
- Sentences 5-6 [Second]: Innovation 2 — what it does + why it works
- Sentences 7-8 [Finally]: Key design choice, training strategy, or efficiency constraint + why it matters

If the method has only one core innovation:
- Sentences 3-4 [First]: Core mechanism + why it works
- Sentences 5-6 [Second]: Key design choice or training strategy + why it matters
- Sentences 7-8 [Finally]: How it differs from prior work + resulting capability

If the method has more than 3 innovations, group the less central ones under the closest-fitting signal word.

### Part 3: Results & Implication (Sentences 9-10)

**Sentence 9 — Key result:**
- "On [dataset_1], [Method] achieves [metric] = [value]%, outperforming [strongest_baseline] by [absolute] percentage points."
- "Experiments on [N] datasets show that [Method] improves [metric] by [X]% on average compared to [baseline_type]."
- "[Method] achieves [result_1] on [dataset_1] and [result_2] on [dataset_2], with consistent gains across all [N] benchmarks."

**Sentence 10 — Implication:**
- "These results demonstrate that [core_insight], offering a [adjective] approach to [task]."
- "Our findings suggest that [broader_implication], with potential applications in [domain]."
- "[Method] provides a [adjective] solution for [task] that [key_advance]."

---

## Annotated Example: SGA Paper (2-6-2 Format, ~210 words)

```
[S1 — Context] Establishing fine-grained semantic correspondence between
natural language queries and visual content is the central challenge in
cross-modal text-to-image retrieval.

[S2 — Gap] Existing fine-grained methods compute region-phrase similarities
but aggregate them via fixed pooling strategies, which treat all visual
regions as equally important — an assumption that fails when queries have
distinct semantic foci.

[S3 — First: claim] First, a Semantic-Guided Alignment (SGA) module is proposed that
learns to re-weight visual regions according to their query-specific
semantic relevance.

[S4 — First: why] A lightweight gating network (0.8M parameters) predicts
per-region weights, enabling the model to dynamically emphasize
discriminative regions for each query.

[S5 — Second: claim] Second, a Hierarchical Matching Loss (HML) is proposed
that jointly supervises global image-text matching and local region-phrase
matching.

[S6 — Second: why] This dual-level supervision explicitly encourages
fine-grained cross-modal alignment that global-only losses overlook.

[S7 — Finally: claim] Finally, a staged optimization strategy is designed
that decouples region re-weighting pretraining from joint hierarchical
fine-tuning.

[S8 — Finally: why] This prevents the two loss terms from competing
during early training, enabling stable convergence and consistent gains
across all evaluated datasets.

[S9 — Results] On MS-COCO, Flickr30k, and CUB-200, SGA improves R@1 by
1.2 to 2.6 percentage points over five baselines, with the largest gain
on the fine-grained CUB-200 dataset (+2.6 R@1).

[S10 — Implication] These results establish query-dependent region
re-weighting as an effective, lightweight strategy for fine-grained
vision-language retrieval.
```

[Annotation]
- Sentences 1-2: ~38 words. Gap has a clear "because" (fixed pooling → equal importance → fails on distinct queries).
- Sentences 3-8: ~126 words. Three clear First/Second/Finally signals. Each pair: claim → mechanism.
- Sentences 9-10: ~42 words. One dataset triad + best number. Implication is specific, not "advances the field."
- Total: ~206 words. All acronyms (SGA, HML) defined on first use.

---

## Abstract Quality Self-Check

1. **Structure**: Does the abstract follow 2-6-2 exactly? Count the sentences. There must be 10.
2. **Signals**: Are "First," "Second," and "Finally" present at the start of sentences 3, 5, and 7?
3. **Numbers**: Does sentence 9 contain at least one triple (dataset + metric + value)? Is the strongest baseline named or typed?
4. **Gap specificity**: Does sentence 2 contain a "because" clause? Or is it a vague "existing methods are limited"?
5. **Method precision**: Can a reader sketch your method's architecture after reading sentences 3-8? If not, the sentences are too vague.
6. **No overclaim**: Scan for forbidden terms — "state-of-the-art", "first", "novel" (unverified), "solve", "prove".
7. **Standalone**: Can the abstract be understood without reading the paper? Are all acronyms defined on first use?
8. **Length**: English: 180-250 words (target 210). Chinese: 200-280 characters (target 250). Count precisely.
9. **Sentence length**: No single sentence over 35 words. If longer, split it.

---

## Keyword / Index Term Rules

**Selection:**
- Choose 3-6 keywords that are NOT already in the title.
- Mix: task name, method type, domain, core technique.
- Avoid overly broad terms ("deep learning", "neural network") unless the paper is about them.
- Use established ACM/IEEE keyword taxonomies when available.

**Format:**
```
Index Terms — image-text retrieval, cross-modal alignment,
contrastive learning, multimodal representation
```
