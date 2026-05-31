# Abstract Patterns

## Three Abstract Structures

### 1. Problem-Driven (Default)
```
[1-2 sentences: task background + importance]
[1 sentence: specific gap or limitation]
[1-2 sentences: proposed method + core mechanism]
[1-2 sentences: key experimental result with numbers]
[1 sentence: implication or broader significance]
```
Best for: Most papers. Clear, balanced, reviewer-friendly.

### 2. Method-Driven
```
[1 sentence: core technical challenge]
[1-2 sentences: proposed method + key insight]
[1 sentence: why this approach works]
[1-2 sentences: experimental validation with numbers]
```
Best for: Papers introducing a fundamentally new architecture or paradigm.

### 3. Results-Driven
```
[1 sentence: task + its importance]
[1 sentence: method name + one-line description]
[2-3 sentences: empirical findings — what the experiments reveal]
[1 sentence: what these findings mean for the field]
```
Best for: Empirical papers where the findings are the main contribution.

---

## Sentence Template Bank

### Background / Problem Statement
- "[Task] is a fundamental challenge in [field] with applications in [app1], [app2], and [app3]."
- "Accurate [task] is critical for [downstream_application], yet it remains challenging because [core_difficulty]."
- "The ability to [task_verb] accurately is essential for [application], where [requirement]."

### Gap / Limitation
- "Existing [method_family] methods [what_they_do], but they [limitation], particularly in [scenario]."
- "A key limitation of current approaches is their inability to [specific_capability]."
- "While recent methods have improved [aspect_A], they still struggle with [aspect_B] due to [root_cause]."

### Method Introduction
- "We propose [Method], a [brief_description] that [core_mechanism_in_one_clause]."
- "To address this gap, we introduce [Method], which [key_innovation]."
- "We present [Method], which combines [component_A] and [component_B] to achieve [capability]."

### Evidence / Results
- "On [dataset_1], [Method] achieves [metric] = [value]%, outperforming [baseline] by [absolute] percentage points."
- "Experiments on [N] datasets show that [Method] improves [metric] by [X]% on average compared to [baseline_type]."
- "[Method] achieves [result_1] while [result_2], demonstrating [key_finding]."

### Implication / Closing
- "These results demonstrate that [core_insight], offering a new approach to [task]."
- "Our findings suggest that [broader_implication], with potential applications in [domain]."
- "[Method] provides a [adjective] solution for [task], advancing the state of [field]."

---

## Word Budget Guidelines

| Venue Type | Typical Abstract Length | Style Notes |
|-----------|------------------------|-------------|
| CVPR / ICCV / ECCV | 150-250 words | Dense, result-heavy. Every word must earn its place. |
| NeurIPS / ICML / ICLR | 150-250 words | Problem formalism + key insight. Less application context. |
| ACL / EMNLP / NAACL | 150-250 words | Task definition + result. Metrics matter. |
| AAAI / IJCAI | 150-250 words | Accessible to broad AI audience. |
| TPAMI / TIP / TNNLS | 200-300 words | Deeper summary allowed. Include key ablation finding. |

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

---

## Two Complete Annotated Example Abstracts

### Example 1: CV Paper (Boundary Refinement)

```
[Background] Semantic segmentation is fundamental to visual understanding,
with critical applications in autonomous driving and medical imaging.
[Gap] Despite significant progress, existing methods struggle with
fine-grained boundary delineation, especially for thin and elongated
structures, because they treat all boundary pixels uniformly without
distinguishing geometrically regular structures from stochastic textures.
[Method] We propose Structure-Aware Boundary Refinement (SABR), a
plug-and-play module that introduces a Directional Consistency Module
to explicitly model the spatial continuity of boundary pixels along
geometric directions.
[Evidence] On Cityscapes, SABR improves mIoU by 2.3 points over
the strongest boundary-aware baseline, with gains of up to 4.1 points
on thin-structure categories. On Mapillary Vistas, SABR achieves
consistent improvements across diverse geographic conditions.
[Implication] These results establish directional consistency as an
effective inductive bias for boundary refinement, with broad
applicability to dense prediction tasks.
```

[Annotation]
- Background: 1 sentence, establishes task + applications
- Gap: 1 sentence with "because" — explains WHY the problem exists
- Method: 1 sentence, what + how (plug-and-play, Directional Consistency)
- Evidence: 2 sentences, each with dataset + metric + value
- Implication: 1 sentence, "dense prediction tasks" broadens relevance

### Example 2: NLP Paper (Efficient Fine-Tuning)

```
[Background] Parameter-efficient fine-tuning methods such as LoRA have
enabled the adaptation of large language models with minimal trainable
parameters, but they introduce inference overhead because adapted
weights cannot be cleanly merged with frozen parameters.
[Gap] Existing approaches either accept this overhead or resort to
approximate merging that degrades performance.
[Method] We propose Mergeable Low-Rank Adaptation (MeLoRA), which
constrains the low-rank decomposition to permit exact merging into
the original weight matrix via a single matrix addition.
[Evidence] On the GLUE benchmark, MeLoRA matches full LoRA accuracy
while reducing inference latency by 27% (14.2ms to 10.4ms per token).
On MMLU, MeLoRA achieves 68.3% (vs. LoRA's 68.1%) with zero
inference overhead.
[Implication] By eliminating the accuracy-efficiency trade-off in
parameter-efficient fine-tuning, MeLoRA makes multi-adapter serving
practical for latency-sensitive deployments.
```

---

## Abstract Quality Self-Check

1. **Numbers**: Does the abstract contain at least 2 specific numbers (metric + dataset + value)?
2. **Gap specificity**: Does the gap sentence contain a "because" clause? Or is it a vague "while existing methods are limited"?
3. **Method precision**: Can a reader explain your method's core mechanism after reading the abstract? Or is it "We propose NovelNet, which uses novel mechanisms"?
4. **No overclaim**: Scan for forbidden terms (state-of-the-art, first, novel without verification, solve without evidence, prove without proof).
5. **Standalone**: Can the abstract be fully understood without reading the paper? Are all acronyms defined?
6. **Length**: Within the target venue's word limit? (Count words, not characters.)

Do not include unsupported SOTA claims. Use exact metrics only when verified.
