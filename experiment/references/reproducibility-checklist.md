# Reproducibility Checklist

Check whether the experiment section includes all items necessary for another researcher to reproduce the results.

## Core Checklist

- [ ] **Dataset names and splits**: Full dataset name, version, train/val/test split sizes.
- [ ] **Preprocessing details**: Resize, normalization, augmentation pipeline.
- [ ] **Baseline implementation source**: Official repo, reimplementation, or paper numbers.
- [ ] **Metric definitions**: Full name, abbreviation, computation method.
- [ ] **Metric direction**: Higher-is-better or lower-is-better for each metric.
- [ ] **Training epochs**: Total epochs, warmup epochs if applicable.
- [ ] **Batch size**: Per-GPU and effective batch size (if gradient accumulation used).
- [ ] **Optimizer**: Name, β1, β2, ε, weight decay.
- [ ] **Learning rate**: Initial LR, schedule type, decay milestones or rate.
- [ ] **Hardware**: GPU model, count, CPU, RAM.
- [ ] **Number of runs**: How many random seeds, what seeds.
- [ ] **Variance**: Standard deviation or confidence intervals.
- [ ] **Code availability**: URL or statement.
- [ ] **Hyperparameter selection method**: Grid search, manual tuning, Bayesian optimization.

## Venue-Specific Requirements

### NeurIPS Reproducibility Checklist
- Claims backed by error bars (at least 3 seeds).
- Hyperparameter search space described.
- Compute requirements stated (GPU-hours).
- Link to code.
- Empirical and theoretical results clearly separated.

### CVPR Reproducibility Guidelines
- Standard benchmarks used where possible.
- Pretrained models and training recipes released.
- Per-category results for detection/segmentation.
- Failure case analysis encouraged.

### ACL Reproducibility Criteria
- Data splits clearly documented.
- Preprocessing scripts available.
- Evaluation scripts available.
- Results with multiple random seeds for smaller datasets.

### General ML Reproducibility (TMLR, JMLR)
- Full experimental protocol described.
- Code submitted with paper.
- Reproducibility verified by an independent party (for some venues).

## Documentation Templates

### Dataset Documentation
```
[Dataset Name] ([citation]). [N_train] training, [N_val] validation,
[N_test] test samples. [N_classes] classes with [balanced/imbalanced] distribution.
Images resized to [H]×[W]. Normalization: mean=[...], std=[...].
Data augmentation: [list with parameters].
```

### Hyperparameter Documentation
```
Hyperparameters were selected via [method] on the [validation_set].
The search space was: learning rate ∈ {[values]}, weight decay ∈ {[values]},
batch size ∈ {[values]}. The best configuration was: lr=[val], wd=[val], bs=[val].
```

### Compute Documentation
```
All experiments were run on [GPU_model] ([VRAM]GB VRAM).
Training a single model takes approximately [time] ([GPU]-hours).
In total, this project consumed approximately [total_GPU_hours] GPU-hours
for all experiments including hyperparameter search and ablation studies.
```

Mark missing items as `AUTHOR_INPUT_NEEDED`. Never fabricate details.
