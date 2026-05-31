# Experiment Section Patterns

Default structure follows `reference-paper-structure.md`:

```markdown
## IV Experiments
### IV-A Datasets and Metrics
### IV-B Implementation Details
### IV-C Comparison Results on [Dataset or Benchmark 1]
### IV-D Comparison Results on [Dataset or Benchmark 2]
### IV-E Ablation Study
```

Use dataset-specific comparison sections when multiple datasets or benchmarks exist. Under each comparison section, add supported analysis subsections such as:

```markdown
#### Quantitative Analysis
#### Qualitative Analysis
#### Results in Complex Scenarios / Robustness Analysis
```

For ablations, adapt headings to the user's modules and evidence:

```markdown
#### Effectiveness of [Module 1]
#### Analysis of [Loss / Hyperparameter / Design Choice]
#### Analysis of [Module 2]
#### Visualization of [Feature / Attention / Case Study]
#### Computational Cost Comparison
```

Delete unsupported subsections rather than inventing results. Do not fabricate implementation details, qualitative findings, robustness claims, computational cost, or statistical significance.

---

## Section Structure Variants

### Single-Dataset Paper
```
IV-A. Experimental Setup (Datasets + Metrics + Implementation + Baselines)
IV-B. Main Results
IV-C. Ablation Study
IV-D. Analysis (Qualitative / Efficiency / Robustness)
```

### Two-Dataset Paper (Most Common)
```
IV-A. Datasets and Metrics
IV-B. Implementation Details
IV-C. Results on [Dataset 1]
IV-D. Results on [Dataset 2]
IV-E. Ablation Study
IV-F. Analysis and Discussion
```

### Multi-Dataset / Multi-Task Paper
```
IV-A. Datasets and Evaluation Protocol
IV-B. Implementation Details
IV-C. Main Results (summary table across all datasets)
IV-D. Per-Dataset Analysis (one subsection per dataset)
IV-E. Ablation Study (on representative dataset)
IV-F. Efficiency Analysis
IV-G. Qualitative Results
```

---

## Result Reporting Sentence Templates

### Main Comparison Results

**Single result:**
> "As reported in Table [X], [Method] achieves [X.X]% [metric] on [dataset], outperforming [baseline] by [absolute] percentage points ([relative]% relative improvement)."

**Across datasets:**
> "Across [N] datasets, [Method] consistently outperforms [baseline_type] methods. On [dataset_1], [Method] achieves [X.X]% ([+Y.Y] over [baseline]); on [dataset_2], it reaches [X.X]% ([+Y.Y])."

**Metric-specific highlight:**
> "The improvement is most pronounced in [metric], where [Method] achieves [X.X] vs. [baseline]'s [Y.Y] (+[Z.Z] percentage points)."

### Ablation Results

**Component contribution:**
> "Removing [component] (row [X], w/o [component]) causes a drop of [X.X] percentage points in [metric], confirming its contribution to [capability]."

**Additive contribution:**
> "Starting from the baseline (row 1), adding [component_A] improves [metric] by [X.X] points (row 2); further adding [component_B] yields an additional [Y.Y] points (row 3). The full model achieves [Z.Z]."

**Interaction effect:**
> "[Component_A] alone improves [metric] by [X.X]; [component_B] alone by [Y.Y]. Together, they yield an improvement of [Z.Z], which is [greater_than/less_than] the sum of individual contributions ([X.X+Y.Y]), indicating [synergy/interference]."

### Efficiency Results

> "With [X]M parameters and [Y]ms inference time per sample (measured on [GPU]), [Method] achieves [Z]% of [baseline]'s accuracy while using only [W]% of its parameters."

> "[Method] reduces inference latency from [X]ms to [Y]ms ([Z]% reduction) while maintaining [metric] within [delta] of the best-performing method."

### Robustness / Generalization

> "Under [perturbation_type], [Method]'s performance degrades by only [X]%, compared to [Y]% for [baseline], demonstrating improved robustness to [condition]."

> "When transferred from [source_dataset] to [target_dataset] without fine-tuning, [Method] retains [X]% of its in-domain performance, vs. [Y]% for [baseline]."

### Qualitative Results

> "Figure [X] shows qualitative comparisons on [dataset]. [Method] produces [desirable_property] (highlighted in [color/marker]), whereas [baseline] exhibits [failure_mode] (indicated by [visual_cue])."

---

## Table Formatting Standards

**Bold and underline convention:**
- **Bold**: best result in each column
- Underline: second-best result
- Only bold/underline within comparable groups (e.g., don't bold a parameter-count minimum if the paper is about accuracy)

**Standard deviation format:**
- "82.3 ± 0.4" (not "82.3 (0.4)" or "82.3±0.4" without space)
- Report at one more decimal place than the mean if std is very small

**Statistical significance:**
- Use superscript symbols: * = p < 0.05, ** = p < 0.01, *** = p < 0.001
- Define the test used in the caption: "Statistical significance determined by [test_name] with [correction]."

**Caption templates:**
> "Table [X]. [One-line description of content]. Best results in **bold**, second-best underlined. [Optional: significance note]."

> "Table [X]. Ablation study on [dataset]. The full model (row [N]) achieves [metric] = [value]. Removing any component degrades performance, with [component] having the largest impact ([delta] points)."

---

## Figure Caption Templates

### Architecture Diagram
> "Fig. [X]. Overview of the proposed [Method] architecture. [One-sentence data flow description]. [Novel components] are highlighted in [color]."

### Confusion Matrix
> "Fig. [X]. Confusion matrix of [Method] on [dataset]. Diagonal entries indicate per-class accuracy. The most frequent confusion is between [class_A] and [class_B]."

### Attention / Feature Maps
> "Fig. [X]. Visualization of [attention/feature] maps from [Method]. Warmer colors indicate higher activation. [Method] focuses on [region_of_interest], while [baseline] (bottom row) attends to [irrelevant/noisy regions]."

### t-SNE / PCA Plot
> "Fig. [X]. t-SNE visualization of [feature_type] extracted by (a) [baseline] and (b) [Method]. Points are colored by [label_type]. [Method] produces [more_compact/better_separated] clusters."

### Loss Curves
> "Fig. [X]. Training and validation [loss/accuracy] curves. [Method] converges within [N] epochs, with no significant overfitting observed (validation loss stabilizes at [value])."

### Bar Chart / Radar Plot
> "Fig. [X]. [Metric] comparison across [N] methods on [dataset]. Error bars indicate standard deviation over [K] runs. [Method] (red) achieves the best overall [metric]."

---

## Statistical Significance Patterns

**When to report significance:**
- When comparing your method to the single best baseline (claim of superiority).
- When an improvement is small (< 1 percentage point).
- When the benchmark has known high variance (e.g., RL, small datasets).

**How to report:**
> "We assess statistical significance using a [paired t-test / Wilcoxon signed-rank test / bootstrap test] with [Bonferroni/Holm] correction for multiple comparisons."

> "The improvement of [Method] over [baseline] is statistically significant at p < 0.01 on [datasets]."

**When NOT to claim significance:**
- When you have only 1 run (no variance estimate).
- When the test was not pre-registered and you are cherry-picking.

---

## Ablation Analysis Writing

**Component contribution:**
> "Table [X] reports the ablation results. Removing [component_A] (row 2, 'w/o [A]') reduces [metric] from [X.X] to [Y.Y] (−[delta] points), confirming that [component_A] is essential for [capability]."

**Design choice justification:**
> "We compare [design_choice_A] against [alternatives] in Table [X]. [Choice_A] achieves [X.X]%, outperforming [alternative_1] ([Y.Y]%) and [alternative_2] ([Z.Z]%). This confirms that [design_rationale]."

**Hyperparameter sensitivity:**
> "Figure [X] shows [metric] as a function of [hyperparameter]. Performance is stable for [hyperparameter] ∈ [range] (within [delta]% of peak). We use [value] for all experiments."

---

## Qualitative Analysis Description

> "Figure [X] presents qualitative results. We select representative examples covering [challenging_scenario_1], [scenario_2], and [scenario_3]. [Method] (column [N]) produces [observation_1] and [observation_2], whereas [baseline] (column [M]) struggles with [failure_mode]."

**Case study selection:**
- State how examples were selected (random, most challenging, most improved, failure cases).
- Never present only cherry-picked best cases without also showing failures.

---

## Experiment Section Quality Self-Check

1. **Metric direction stated**: Is it clear for each metric whether higher or lower is better?
2. **Variance reported**: Are standard deviations or confidence intervals included?
3. **Baseline scope**: Are all baselines described (with citations if published)?
4. **Implementation details**: Could another researcher reproduce training from the provided details?
5. **Ablation coverage**: Does every claimed contribution have a corresponding ablation row?
6. **No unsupported claims**: Are all result numbers traceable to tables/figures?
7. **Statistical rigor**: If claiming superiority, is it supported by a significance test?
