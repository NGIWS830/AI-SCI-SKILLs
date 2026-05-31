# Paper Storyline

## One-Sentence Contribution

We propose Semantic-Guided Alignment (SGA), a fine-grained cross-modal retrieval method that aligns visual regions with textual phrases through learned semantic re-weighting and hierarchical matching, achieving consistent improvements (+1.2 to +2.6 R@1) over existing fine-grained methods with only +6% parameter overhead.

## Research Problem

Text-to-image retrieval requires understanding fine-grained correspondences between textual descriptions and visual content. A query like "a red car parked under a tree" requires the model to associate "red" with the car's color, "parked" with its state, and "under a tree" with the spatial relationship — all from a single embedding comparison.

## Research Gap

Existing methods either:
(1) Collapse each modality into a global vector (CLIP, BLIP), losing fine-grained region-phrase correspondence; or
(2) Compute region-phrase similarities (SCAN, CHAN) but use fixed pooling strategies (average, max) that treat all regions as equally important.

Neither approach can adaptively emphasize the *semantically discriminative* regions for each specific query. For example, when searching for "a red car," car-related regions should be up-weighted, but when searching for "a car under a tree," both the car and the spatial relationship (tree + car position) are relevant.

## Proposed Method

SGA introduces two innovations:
1. **Semantic-Guided Alignment Module**: Computes a region-phrase similarity matrix and applies a learned gating network to re-weight regions based on their semantic relevance to the query. The gating network is lightweight (0.8M parameters) and trained end-to-end.
2. **Hierarchical Matching Loss**: Combines a global InfoNCE loss (image-text pair level) with a local Chamfer-style loss (region-phrase level). This dual supervision ensures both holistic and fine-grained alignment.

## Main Evidence

- On MS-COCO, SGA achieves 64.2 R@1 (+1.2 over CHAN). On Flickr30k, 78.5 R@1 (+1.6 over CHAN). On fine-grained CUB-200, 38.8 R@1 (+2.6 over CHAN).
- Ablation: removing semantic re-weighting costs 2.1-2.3 R@1; removing local-level loss costs 1.4-1.6 R@1. Combined contribution is approximately additive.
- Parameter overhead: only 11M parameters (+6%) added to the ViT+BERT backbone.

## Claims and Evidence

| Claim | Evidence | Support | Risk |
|-------|----------|---------|------|
| SGA outperforms fine-grained retrieval baselines | +1.2 to +2.6 R@1 on 3 datasets vs. CHAN | Strong (3 datasets, 5 seeds) | Low |
| Semantic re-weighting improves fine-grained alignment | Ablation: −2.1 to −2.3 R@1 when removed | Strong (consistent across datasets) | Low |
| Hierarchical matching loss improves retrieval | Ablation: −1.4 to −1.6 R@1 when removed | Strong (consistent across datasets) | Low |
| SGA is parameter-efficient | +11M / +6% over backbone | Moderate (single comparison point) | Medium — need more baselines for context |
| SGA benefits fine-grained tasks | +7.2% relative on CUB-200 vs. +1.9% on COCO | Moderate (one fine-grained dataset) | Medium — more fine-grained benchmarks needed |
