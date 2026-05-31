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
