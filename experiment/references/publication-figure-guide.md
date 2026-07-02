# Publication Figure Guide

Use this guide for experimental statistical figures in the Experiments section. This is separate from method framework diagrams and algorithm structure diagrams.

## Boundary

- Method framework diagrams, module structure diagrams, and principle diagrams are author materials. They should be collected during material intake. If missing, insert `AUTHOR_INPUT_NEEDED` figure placeholders in the manuscript.
- Experimental statistical figures should be generated from source data tables or logs by scripts. Do not hand-draw or invent values.

## Preferred Figure Types

1. Main comparison grouped bar charts: methods x datasets/settings for each metric.
2. Improvement heatmaps: target method vs strongest listed baseline across datasets and metrics.
3. Ablation contribution charts: component variants or removal studies.
4. Efficiency-performance plots: Params/FLOPs/latency/memory against accuracy or task metric.
5. Robustness curves: performance under noise, corruption, domain shift, missing modality, or low-data ratio.
6. Training dynamics curves: loss/metric over epoch when logs are available.

## Style Requirements

- Export `pdf` for LaTeX inclusion and `png` at 600 dpi for review.
- Use a colorblind-safe palette and restrained line widths.
- Avoid 3D charts, decorative gradients, heavy backgrounds, and untraceable annotations.
- Show error bars only when standard deviation, standard error, confidence interval, or repeated-seed data are present.
- State metric direction in captions when needed.
- Keep all values traceable to the source table.

## Missing Data Policy

If a needed experiment figure cannot be generated because data are missing, write a placeholder instead of fabricating the figure:

```markdown
![AUTHOR_INPUT_NEEDED: Fig. X. Experimental statistical figure placeholder. Provide the source CSV/log for this figure.](figures/fig_x_placeholder.png)
```

## Caption Pattern

```text
Fig. X. Quantitative comparison on [dataset/setting]. Higher [metric] indicates better performance. Values are taken from [source table]. Error bars indicate [std/CI] over [N] runs when available.
```

For improvement heatmaps:

```text
Fig. X. Absolute improvement of [target method] over the strongest listed baseline. Positive values indicate better performance according to each metric direction.
```
