# Ablation Writing

## Purpose

Ablation studies should support component-level claims, not merely list variants. Every ablation row should answer a specific question about the method.

## Ablation Design Patterns

### 1. Component Removal (Most Common)
Remove one component at a time from the full model.
- **Question**: Does this component contribute to performance?
- **Pattern**: Full model → w/o Component A → w/o Component B → w/o Component C
- **Presentation**: "Removing [component] decreases [metric] from [A] to [B] (−[delta]), indicating that [component] contributes to [specific capability]."

### 2. Component Isolation (Additive)
Start from a minimal baseline, add components one at a time.
- **Question**: What is the marginal contribution of each component?
- **Pattern**: Baseline → +Component A → +Component B → +Component C (= Full)
- **Presentation**: "Starting from the baseline ([value]), adding [A] improves [metric] to [value] (+[delta_A]). Further adding [B] yields [value] (+[delta_B])."

### 3. Component Substitution
Replace each component with a simpler alternative.
- **Question**: Is the specific design of this component better than alternatives?
- **Pattern**: Full model → Replace A with Alternative A1 → Replace A with Alternative A2
- **Presentation**: "Replacing [Component A] with [Alternative] decreases [metric] by [delta], confirming that [design choice] is important beyond [simple alternative]."

### 4. Hyperparameter Sensitivity
Vary a key hyperparameter and measure impact.
- **Question**: How sensitive is the method to this hyperparameter?
- **Pattern**: Performance vs. [hyperparameter] ∈ [range]
- **Presentation**: "Performance is stable for [hyperparameter] in [stable_range] ([metric] varies by ≤[delta]). We use [value] for all experiments."

### 5. Data Ablation
Vary training data (amount, source, augmentation).
- **Question**: How much does the method depend on data scale/augmentation?
- **Pattern**: 25% data → 50% data → 75% data → 100% data
- **Presentation**: "Performance improves with more data, but [Method] already achieves [X]% of peak performance with only [Y]% of the data."

---

## Result Interpretation Templates

### Single Component
> "Removing [component] causes a drop of [X.X] percentage points in [metric] (Table [X], row [N]), confirming that [component] is essential for [capability]."

### Comparative Component Importance
> "Among the [N] components ablated, [Component A] has the largest impact (−[delta_A] points), followed by [Component B] (−[delta_B]), and [Component C] (−[delta_C]). This suggests that [capability_A] is the most critical factor."

### Interaction Effect
> "[Component A] alone improves [metric] by [delta_A]; [Component B] alone by [delta_B]. Together, they yield an improvement of [delta_AB], which is [greater/less] than the sum (+[delta_A+delta_B]), indicating [positive/negative] interaction."

### Negative Result (Honest)
> "Removing [component] has negligible impact on [metric] ([delta] < [threshold]). This suggests that [component] may not be necessary for [task] under the current settings, or its contribution is redundant with [other_component]."

---

## Ablation Presentation

**Table format:**
| # | Variant | [Metric 1] | [Metric 2] | Δ [Metric 1] |
|---|---------|-----------|-----------|-------------|
| 1 | Full Model | 82.3 | 75.1 | — |
| 2 | w/o Component A | 80.1 | 73.5 | −2.2 |
| 3 | w/o Component B | 81.5 | 74.2 | −0.8 |
| 4 | w/o Component C | 81.8 | 74.6 | −0.5 |

**Prose integration:**
1. State the question the ablation answers.
2. Point to the table.
3. Report the key numbers.
4. Interpret what the numbers mean.
5. (Optional) Caveat the interpretation.

---

## Common Ablation Pitfalls

1. **Confounding factors**: If removing Component A also changes the number of parameters, is the drop due to the component's design or reduced capacity? Control for capacity (e.g., replace with a parameter-matched dummy layer).

2. **Over-interpreting small deltas**: A 0.3 percentage point drop from removing a component, with 0.5 std, is not meaningful. Don't claim "Component A is important" based on noise.

3. **Ignoring interaction effects**: If Component A and B interact, removing one at a time underestimates their joint contribution. Test both singly-removed and jointly-removed.

4. **Cherry-picking the metric**: If Component A helps Metric 1 but hurts Metric 2, report both. Don't only report the metric that makes the ablation look good.

5. **Not ablating the right thing**: If your claim is "our loss function is novel," the ablation should compare your loss vs. standard losses, not just "w/o loss." A model without a loss function is meaningless.

---

## Cautions

- Do not claim a module is essential if improvement is tiny or inconsistent.
- Do not claim generality from a single dataset unless framed carefully.
- If variants change multiple factors at once, avoid attributing the effect to one factor.
- An ablation that shows "full model > w/o X" is weak evidence that X is the right design — it only shows X helps, not that X is better than alternatives. Use substitution ablation for design choice claims.
