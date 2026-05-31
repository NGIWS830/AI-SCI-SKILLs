# Reference Paper Structure

Use this as the default manuscript skeleton for standard AI conference/journal papers.

## Fixed Top-Level Flow

Keep these first-level sections in this order:

```markdown
# Title
## Abstract
## Index Terms
## I Introduction
## II Related Work
## III Proposed Method
## IV Experiments
## V Conclusion
## References
```

## Adaptable Second-Level Headings

Second-level headings should follow the same rhetorical role as the reference paper, but must be rewritten for the user's own method and evidence.

### II Related Work

Use 2-4 topic-based subsections. Choose themes from the user's task and method family.

```markdown
### II-A [Task or Application Background]
### II-B [Core Method Family or Baseline Family]
### II-C [Specific Gap Closest to This Work]
```

### III Proposed Method

Do not copy the reference paper's module names. Replace them with the user's actual method components.

```markdown
### III-A Overview
### III-B [Core Module 1]
### III-C [Core Module 2]
### III-D [Core Module 3 / Third Innovation]
```

If the user's method has more or fewer components, adjust the subsection count while keeping `III-A Overview` first. Use `III-D` for the third innovation by default. Only add `III-E Training Objective`, `III-F Inference Procedure`, or complexity subsections when they are supported and genuinely needed. If the loss/objective is itself the third innovation, it may be used as `III-D`; otherwise do not force it into the method section.

### IV Experiments

Keep the experimental logic close to the reference paper, but adapt all dataset, metric, baseline, and analysis headings to the user's evidence.

```markdown
### IV-A Datasets and Metrics
#### IV-A1 [Dataset 1]
#### IV-A2 [Dataset 2]
### IV-B Implementation Details
### IV-C Comparison Results on [Dataset or Benchmark 1]
#### IV-C1 Quantitative Analysis
#### IV-C2 Qualitative Analysis
#### IV-C3 Results in Complex Scenarios / Robustness Analysis
### IV-D Comparison Results on [Dataset or Benchmark 2]
### IV-E Ablation Study
#### IV-E1 Effectiveness of [Module 1]
#### IV-E2 Analysis of [Loss / Hyperparameter / Design Choice]
#### IV-E3 Analysis of [Module 2]
#### IV-E4 Visualization of Feature Map / Attention Map / Case Study
#### IV-E5 Effectiveness across Stages / Components
#### IV-E6 Computational Cost Comparison
```

Delete unsupported subsections rather than inventing experiments. If only one dataset is available, use one comparison section. If no qualitative, robustness, or efficiency evidence is available, mark the missing item as `AUTHOR_INPUT_NEEDED`.

## Writing Rules

- Treat the reference article as a structure template only; do not copy its claims, module names, datasets, or result wording.
- Keep `Introduction` contribution bullets evidence-grounded and aligned with the user's project brief and experiment analysis.
- In `Related Work`, organize by themes instead of listing papers one by one.
- In `Proposed Method`, start with the overall framework before describing modules.
- In `Experiments`, report metric direction, baseline scope, and caveats before making result claims.
- In `Conclusion`, include limitations and future work only when supported or explicitly provided by the author.
