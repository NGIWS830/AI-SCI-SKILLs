# Experiment Analysis

## Tables Analyzed

`experiments/results.csv` — 18 data rows (6 methods × 3 datasets), with R@1, R@5, R@10 and standard deviations over 5 seeds.

## Main Results

SGA consistently outperforms all 5 baselines across all 3 datasets and all 3 Recall@K metrics. The largest gains are on the fine-grained CUB-200 dataset — suggesting the semantic re-weighting mechanism is especially beneficial when discriminative visual details matter.

## Improvement over Baselines

| Dataset | Metric | SGA | Best Baseline | Baseline Name | Δ Absolute | Δ Relative |
|---------|--------|-----|---------------|---------------|------------|------------|
| MS-COCO | R@1 | 64.2 | 63.0 | CHAN | +1.2 | +1.9% |
| MS-COCO | R@5 | 87.3 | 86.1 | CHAN | +1.2 | +1.4% |
| MS-COCO | R@10 | 93.9 | 93.2 | CHAN | +0.7 | +0.8% |
| Flickr30k | R@1 | 78.5 | 76.9 | CHAN | +1.6 | +2.1% |
| Flickr30k | R@5 | 93.5 | 92.8 | CHAN | +0.7 | +0.8% |
| Flickr30k | R@10 | 96.8 | 96.3 | CHAN | +0.5 | +0.5% |
| CUB-200 | R@1 | 38.8 | 36.2 | CHAN | +2.6 | +7.2% |
| CUB-200 | R@5 | 67.5 | 64.8 | CHAN | +2.7 | +4.2% |
| CUB-200 | R@10 | 81.3 | 79.1 | CHAN | +2.2 | +2.8% |

### Ablation

| Variant | COCO R@1 | Flickr R@1 | CUB R@1 |
|---------|----------|------------|---------|
| Full SGA | 64.2 ± 0.3 | 78.5 ± 0.3 | 38.8 ± 0.6 |
| w/o Semantic Re-weighting | 62.1 ± 0.4 (−2.1) | 76.3 ± 0.4 (−2.2) | 36.5 ± 0.7 (−2.3) |
| w/o HML Local Level | 62.8 ± 0.3 (−1.4) | 76.9 ± 0.3 (−1.6) | 37.2 ± 0.6 (−1.6) |
| w/o Both (Global Only) | 60.5 ± 0.5 (−3.7) | 74.8 ± 0.5 (−3.7) | 34.9 ± 0.8 (−3.9) |
| Global Only (CLIP zero-shot) | 58.3 ± 0.4 (−5.9) | 72.1 ± 0.5 (−6.4) | 28.5 ± 0.8 (−10.3) |

Key finding: Both SGA and HML contribute independently. Removing semantic re-weighting costs ~2.1-2.3 R@1; removing local-level loss costs ~1.4-1.6 R@1. The combined effect (−3.7 to −3.9) is approximately additive, suggesting minimal interaction between the two mechanisms.

## Claims Supported by Evidence

| Claim | Evidence | Strength | Caveat |
|-------|----------|----------|--------|
| SGA outperforms existing fine-grained retrieval methods. | +1.2 to +2.6 R@1 over CHAN (closest competitor) on all 3 datasets. | Strong | Gains on COCO (+1.2) and Flickr (+1.6) are moderate. CUB gain (+2.6) is larger. |
| Semantic re-weighting contributes to fine-grained alignment. | Removing re-weighting costs 2.1-2.3 R@1 across datasets (ablation). | Strong | Ablation confirms component-level contribution. |
| Hierarchical matching loss improves over standard contrastive loss. | Removing local-level HML costs 1.4-1.6 R@1 (ablation). | Strong | Two-level supervision is demonstrably better than global-only InfoNCE. |
| SGA is parameter-efficient. | 187M total (only +11M / +6% over backbones). | Moderate | 6% overhead is modest but not negligible. No latency benchmark against all baselines. |
| SGA generalizes across domains. | Gains on general (COCO, Flickr) and fine-grained (CUB) datasets. | Moderate | Only 3 datasets. CUB is within the image domain, not a true domain shift. |

## Missing Experiments or Metadata

- AUTHOR_INPUT_NEEDED: Statistical significance tests (paired bootstrap) for pairwise comparisons.
- AUTHOR_INPUT_NEEDED: CUB-200 full evaluation (current results marked preliminary).
- AUTHOR_INPUT_NEEDED: Text-to-image AND image-to-text retrieval results (currently only t2i reported).
- AUTHOR_INPUT_NEEDED: Efficiency benchmarking (FLOPs, latency) for all baseline methods (currently only SGA vs. CLIP compared).

## Risks of Overclaiming

- Do not claim SOTA — the baseline list may not include the most recent methods (e.g., BEiT-3, SigLIP).
- Do not claim "substantial" improvement on COCO (+1.2 R@1) without statistical test.
- Do not claim "generalization to all fine-grained tasks" — only one fine-grained dataset (CUB-200) evaluated.
- The ablation shows additive effects, but do not claim "optimal design" without exploring more configurations.
