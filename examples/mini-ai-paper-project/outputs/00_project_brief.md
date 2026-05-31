# Project Brief

## One-Sentence Summary

This work proposes Semantic-Guided Alignment (SGA), a fine-grained cross-modal retrieval method that aligns visual regions with textual phrases through semantic re-weighting and hierarchical matching, achieving consistent improvements on three benchmarks while adding only 6% parameter overhead.

## Research Field and Task

**Field**: Multimodal learning, vision-language retrieval.
**Task**: Text-to-image retrieval — given a natural language query, retrieve the most relevant images from a gallery.
**Metrics**: Recall@K (R@1, R@5, R@10). Higher is better for all metrics.

## Proposed Method

**Semantic-Guided Alignment (SGA)** with two core innovations:
1. A Semantic-Guided Alignment module that computes fine-grained region-phrase similarities with learned re-weighting.
2. A Hierarchical Matching Loss (HML) that supervises both global image-text pairs and local region-phrase pairs.

## Core Components

| Component | Description | Evidence |
|---|---|---|
| ViT-B/16 Visual Encoder | Extracts region-level patch features. CLIP-pretrained weights. | `project_notes.md`, standard architecture |
| BERT-base Text Encoder | Extracts phrase-level token features. HuggingFace pretrained. | `project_notes.md`, standard architecture |
| Semantic-Guided Alignment Module | Computes region-phrase similarity matrix; learned gating network re-weights discriminative regions. | `project_notes.md` — 11M parameters, custom nn.Module |
| Hierarchical Matching Loss | Bidirectional InfoNCE (global) + Chamfer-style region-phrase matching (local). λ = 0.3. | `project_notes.md` — two-level supervision |

## Method Innovation Slots for Manuscript

| Manuscript Subsection | Innovation / Module | Evidence | Missing Details |
|---|---|---|---|
| III-B | Semantic-Guided Alignment Module | `project_notes.md` — custom module with gating network | Architecture diagram needed from author |
| III-C | Hierarchical Matching Loss | `project_notes.md` — two-level loss with λ=0.3 | Ablation results confirm contribution |
| III-D | Training Objective | `project_notes.md` — L_total = L_global + 0.3 L_local | Standard; no additional innovation here |

## Datasets

| Dataset | Images (test) | Captions | Split | Notes |
|---------|--------------|----------|-------|-------|
| MS-COCO | 5,000 | 25,010 | Karpathy split | Standard benchmark |
| Flickr30k | 1,000 | 5,000 | Standard split | Standard benchmark |
| CUB-200 | 11,788 | 10/im | Standard split | Fine-grained; preliminary results |

## Baselines

| Baseline | Type | Venue |
|----------|------|-------|
| CLIP (ViT-B/16) | Global alignment baseline | ICML 2021 |
| BLIP (ViT-B/16) | Global + captioning | ICML 2022 |
| VSE++ | Fine-grained, hard negatives | BMVC 2018 |
| SCAN | Fine-grained, stacked attention | ECCV 2018 |
| CHAN | Fine-grained, hierarchical attention | — |

## Metrics

- R@1, R@5, R@10 (Recall@K). Higher is better for all.
- All results reported as mean ± std over 5 random seeds.
- Statistical significance: not yet computed (AUTHOR_INPUT_NEEDED).

## Key Results Available

| Dataset | SGA R@1 | Best Baseline R@1 | Δ | SGA R@5 | Best Baseline R@5 | Δ |
|---------|--------|-------------------|---|---|---------|-------------------|---|---|
| MS-COCO | 64.2 | 63.0 (CHAN) | +1.2 | 87.3 | 86.1 (CHAN) | +1.2 |
| Flickr30k | 78.5 | 76.9 (CHAN) | +1.6 | 93.5 | 92.8 (CHAN) | +0.7 |
| CUB-200 | 38.8 | 36.2 (CHAN) | +2.6 | 67.5 | 64.8 (CHAN) | +2.7 |

## Candidate Contributions

1. **Architectural**: Semantic-Guided Alignment module — fine-grained region-phrase alignment with learned re-weighting.
2. **Algorithmic**: Hierarchical Matching Loss — joint global-local supervision for cross-modal retrieval.
3. **Empirical**: Consistent improvements over 5 baselines on 3 datasets (+1.2 to +2.6 R@1), with only +6% parameter overhead.
4. **Analysis**: Ablation shows both semantic re-weighting and local-level loss contribute independently.

## Risks Before Paper Writing

- CUB-200 results are preliminary (AUTHOR_INPUT_NEEDED: full evaluation).
- Statistical significance tests not yet run for all comparisons.
- The +6% parameter overhead may matter for some deployment scenarios; needs honest discussion.
- Competitor CHAN is close on COCO (+1.2 R@1); the gap is moderate.
- Code not yet released (AUTHOR_INPUT_NEEDED: URL).
