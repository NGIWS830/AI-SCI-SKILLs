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

---

## Visual Ablation Analysis

Quantitative metrics alone do not explain WHY a component works. Visual ablations show the mechanism — what the model learns, where it attends, and how intermediate representations change when a component is added or removed. Each visualization type answers a specific ablation question.

### Visualization Types and When to Use Them

#### 1. Feature Map Visualization

**What it shows**: Spatial activation patterns from intermediate convolutional or attention layers. Each channel highlights a different learned pattern.

**Ablation question**: Does this module help the model learn better intermediate representations?

**How to use**: Compare feature maps of the full model vs. w/o component. The full model should produce sharper, more semantically meaningful activations.

**Figure caption template**:
> "Fig. [X]. Feature map visualization of [layer_name] from (a) baseline, (b) w/o [component], (c) full model. Channels are selected by highest activation variance. The full model captures [semantic_property] more distinctly, while the ablated variant shows [degradation]."

**Prose template**:
> "Figure [X] visualizes the feature maps at [layer]. In the full model (row c), channels [N] and [M] strongly activate on [semantic_region], indicating that [component] enables the model to focus on [meaningful_pattern]. Without [component] (row b), activations are [diffuse/misplaced/suppressed]."

#### 2. Heatmap / Class Activation Map (Grad-CAM / Grad-CAM++ / Score-CAM)

**What it shows**: The spatial regions most influential for a specific class prediction, overlaid as a heatmap on the input image.

**Ablation question**: Does the proposed component guide the model to look at the right regions for its decision?

**How to use**: Generate heatmaps for full model vs. w/o component on the same inputs. The component is effective if attention shifts toward task-relevant regions.

**Figure caption template**:
> "Fig. [X]. Grad-CAM visualizations for (a) input image, (b) baseline, (c) w/o [component], (d) full model. Ground-truth label: [class]. Warmer colors (red) indicate higher influence on the prediction. The full model focuses on [discriminative_region], whereas the ablated variant attends to [irrelevant/background region]."

**Prose template**:
> "As shown in Figure [X], the full model's highest activations concentrate on [task-relevant region], aligning with human diagnostic intuition. Removing [component] disperses attention toward [background/distractor], confirming that [component] provides [localization/guidance] that directs the model to discriminative evidence."

**Note**: Heatmaps are correlational, not causal. Pair heatmap evidence with a quantitative localization metric (e.g., IoU with ground-truth masks, Pointing Game accuracy, Energy-Based Pointing Game) when claiming improved localization.

#### 3. Channel Weight / Importance Map

**What it shows**: Learned scalar weights (e.g., from SE/SK/ECA modules, gating mechanisms, or channel attention) that amplify or suppress each feature channel.

**Ablation question**: Does the channel gating/selection mechanism learn a meaningful importance distribution? Which channels are enhanced and which are suppressed?

**How to use**: Plot channel weights as a bar chart or heatmap across layer depth. Compare weight distributions with and without the gating component, or compare learned weights against a random/uniform baseline.

**Figure caption template**:
> "Fig. [X]. Channel weight distribution in [module_name]. (a) Learned weights across [N] channels, sorted by magnitude. (b) Weight distribution at [layer_depth]. High-weight channels (indices [range]) correspond to [semantic_meaning], while suppressed channels ([range]) encode [irrelevant_feature]. The inset shows weight sparsity: [X]% of channels receive near-zero weight (< [threshold])."

**Prose template**:
> "Figure [X] (a) shows the learned channel weights. The module selectively enhances [X]% of channels (weight > [threshold]) while suppressing the remainder. The enhanced channels primarily encode [semantic_pattern] (see Section [X] for channel-meaning mapping), consistent with the design intent of [mechanism]."

#### 4. t-SNE / PCA Feature Embedding Visualization

**What it shows**: High-dimensional feature vectors projected to 2D/3D, colored by class label or domain.

**Ablation question**: Does the proposed component improve class separability or domain invariance in the learned feature space?

**How to use**: Plot t-SNE of features BEFORE the classifier head, comparing full model vs. w/o component. Better class separation (higher silhouette score, larger inter-class margin) indicates the component improves representation quality.

**Figure caption template**:
> "Fig. [X]. t-SNE visualization of [feature_type] features on [dataset] test set. (a) Baseline, (b) w/o [component], (c) full model. Colors denote [class_label/domain]. The full model produces more compact intra-class clusters and wider inter-class margins ([silhouette_score] vs. [baseline_score])."

**Prose template**:
> "Figure [X] (c) shows that features from the full model form well-separated clusters with high intra-class compactness. Without [component] (b), clusters for [class_A] and [class_B] partially overlap, consistent with the [delta] point drop in [metric] for those classes (Table [X]). This confirms that [component] contributes to learning more discriminative representations."

**Important**: Always report the perplexity parameter used for t-SNE. Use a fixed random seed for reproducibility. Supplement qualitative t-SNE with quantitative metrics (silhouette score, NMI, Davies-Bouldin index).

#### 5. Attention Map Visualization

**What it shows**: Attention weight matrices from self-attention, cross-attention, or spatial attention layers. In vision transformers, attention maps show which image patches attend to each other.

**Ablation question**: Does the attention mechanism learn meaningful relationships? Does the proposed attention variant produce sharper/structured attention patterns?

**Sub-types**:
- **Self-Attention Map**: Shows pairwise patch/pixel relationships. Effective models produce structured patterns (e.g., object boundaries, part-whole relationships).
- **Cross-Attention Map**: In multi-modal tasks, shows which regions in modality A are queried by modality B.
- **Attention Rollout**: Accumulates attention across transformer layers to show the effective receptive field.

**Figure caption template**:
> "Fig. [X]. Attention map visualization. (a) Input image with query patch highlighted. (b)-(d) Attention maps from layer [L] for baseline, w/o [component], and full model. The full model's attention concentrates on [structurally_related_region], indicating that [component] helps the model discover [relationship_type]."

**Prose template**:
> "Figure [X] shows the attention patterns at layer [L]. The full model (d) attends strongly to patches belonging to the same [object/semantic_unit] as the query, forming a coherent object-level attention mask. Without [component] (c), attention is fragmented across unrelated patches. This structured attention explains the [delta] point gain in [metric]."

#### 6. Error Case Visualization

**What it shows**: Side-by-side comparison of success and failure cases, annotated with the specific error type.

**Ablation question**: What specific failure modes does each component address? Which failure cases persist after adding the component?

**How to use**: Select representative cases: (1) cases where full model succeeds but w/o component fails, (2) cases where both fail, (3) cases where both succeed. Annotate the visual difference.

**Figure caption template**:
> "Fig. [X]. Qualitative ablation of [component]. Top row: cases where removing [component] causes failure. Middle row: cases where both variants succeed. Bottom row: challenging cases where both fail. Failure modes are annotated in [color]. [Component] primarily prevents [failure_type]."

**Prose template**:
> "Figure [X] (top row) shows three cases where the full model correctly predicts [label] while the ablated model fails. The failure is consistently [failure_type] — the model without [component] struggles with [specific_challenge]. This visual evidence aligns with the quantitative result that [component] improves [metric] most on the [challenging_subset] subset ([+delta])."

#### 7. Filter / Kernel Visualization

**What it shows**: Patterns that maximally activate each convolutional filter, obtained via gradient ascent or by selecting top-activating image patches.

**Ablation question**: Does the proposed module change what low-level or mid-level patterns the network learns?

**How to use**: Visualize filters at multiple depths. Shallow filters should show oriented edges, textures, colors; deep filters should show more semantic patterns. Compare filter diversity with and without the component.

**Figure caption template**:
> "Fig. [X]. Visualization of [N] filters from [layer_name] via gradient ascent. (a) w/o [component], (b) full model. Filters from the full model exhibit greater diversity ([diversity_metric]) and more structured patterns, suggesting that [component] encourages the learning of [desirable_filter_property]."

#### 8. Per-Class Performance Shift (Confusion Matrix Difference)

**What it shows**: The element-wise difference between two confusion matrices (full model minus ablated), highlighting which classes benefit most from the component.

**Ablation question**: Which specific classes or categories benefit from this component, and which are unaffected?

**How to use**: Compute Δ = CM_full − CM_ablation. Positive diagonal entries indicate classes where the component improves accuracy. Off-diagonal patterns reveal shifts in confusion.

**Figure caption template**:
> "Fig. [X]. Confusion matrix difference (full model − w/o [component]) on [dataset]. Blue (positive) cells indicate classes where [component] improves accuracy. The largest gains are in [class_group], consistent with the design motivation of [component]."

**Prose template**:
> "The confusion difference matrix (Fig. [X]) reveals that [component] primarily improves accuracy on [class_group] (average +[delta] points), with negligible effect on [other_group]. This is expected because [component] is designed to address [specific_challenge] that predominantly affects [class_group]."

#### 9. Training Dynamics Visualization

**What it shows**: Training/validation curves over epochs, comparing convergence speed and stability with and without the component.

**Ablation question**: Does the component accelerate convergence? Improve training stability? Reduce overfitting?

**How to use**: Plot loss and key metrics vs. epoch for full model, w/o component, and baseline. Use smoothing for readability but show raw data in faint background.

**Figure caption template**:
> "Fig. [X]. Training dynamics on [dataset]. (a) Validation [metric] vs. epoch. (b) Training loss vs. epoch. The full model converges [N] epochs faster and reaches a [delta]-point higher final [metric] than the ablated variant."

#### 10. Prediction Confidence Distribution

**What it shows**: Histogram or KDE of softmax confidence scores for correct and incorrect predictions.

**Ablation question**: Does the component make the model better calibrated — confident when correct, uncertain when wrong?

**How to use**: Overlay confidence distributions for full model vs. ablated. The better model should have well-separated correct/incorrect peaks (high confidence for correct, low for incorrect).

**Figure caption template**:
> "Fig. [X]. Prediction confidence distribution on [dataset]. Solid lines: correct predictions; dashed: incorrect. The full model exhibits better separation between correct and incorrect confidence, with fewer overconfident errors (confidence > [threshold] yet wrong)."

### Visual Ablation Selection Guide

| If your claim is... | Primary visualization | Secondary visualization |
|-----|------|------|
| "Our module improves feature quality" | t-SNE / PCA embedding | Feature map comparison |
| "Our module guides attention to the right regions" | Grad-CAM heatmap | Attention map |
| "Our gating mechanism selects informative channels" | Channel weight distribution | Per-class performance shift |
| "Our loss function improves class separability" | t-SNE embedding + silhouette score | Confusion matrix difference |
| "Our method handles challenging cases better" | Error case comparison | Prediction confidence distribution |
| "Our module accelerates convergence" | Training dynamics | — |
| "Our attention mechanism is more interpretable" | Attention map + rollout | Grad-CAM heatmap |
| "Our filters learn more diverse patterns" | Filter / kernel visualization | Feature map comparison |

### Visual Ablation Prose Integration Pattern

For every visual ablation figure, follow this 5-step pattern in prose:

1. **State the question**: "To understand HOW [component] contributes to the observed improvement, we visualize..."
2. **Describe the setup**: "Figure [X] compares [visualization_type] on [N] representative examples from [dataset]."
3. **Point to key observations**: "The full model (row/column c) shows [specific_observation], while w/o [component] (row/column b) exhibits [degraded_behavior]."
4. **Interpret mechanistically**: "This suggests that [component] enables the model to [mechanism_explanation], which is consistent with its design motivation ([cite design section])."
5. **Link back to quantitative evidence**: "The visual difference aligns with the [delta]-point quantitative gain in [metric] (Table [X], row [N])."

---

## Cautions

- Do not claim a module is essential if improvement is tiny or inconsistent.
- Do not claim generality from a single dataset unless framed carefully.
- If variants change multiple factors at once, avoid attributing the effect to one factor.
- An ablation that shows "full model > w/o X" is weak evidence that X is the right design — it only shows X helps, not that X is better than alternatives. Use substitution ablation for design choice claims.
- **Visual ablation cautions**:
  - Never cherry-pick only the examples that make your method look good. Always show at least one failure case.
  - t-SNE results depend on perplexity — report the parameter and use a consistent random seed.
  - Grad-CAM shows correlation, not causation. Pair with a quantitative localization metric.
  - Feature maps from different layers are not directly comparable — always show the same layer across variants.
  - Channel weight visualizations are only meaningful if the channels have interpretable semantics; otherwise, report sparsity and distribution shape instead.
