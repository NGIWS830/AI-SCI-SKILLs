# Project Notes

## Task

Cross-modal text-to-image retrieval: given a natural language query, retrieve the most relevant images from a gallery. The task requires aligning visual and textual features in a shared embedding space where semantically similar pairs are close and dissimilar pairs are far apart.

## Method Description

We propose **Semantic-Guided Alignment (SGA)**, a cross-modal retrieval method with two novel components:

### 1. Semantic-Guided Alignment Module (SGA Module)

The SGA module learns fine-grained correspondences between visual regions and textual phrases. Unlike global pooling approaches (e.g., CLIP-style) that collapse each modality into a single vector, SGA:

- Extracts region-level visual features from a ViT-B/16 backbone (patch tokens before the CLS token).
- Extracts phrase-level text features from a BERT-base encoder (token embeddings before pooling).
- Computes a cross-modal similarity matrix between all region-phrase pairs.
- Applies a **semantic re-weighting mechanism** that up-weights discriminative regions (e.g., "red car" → car regions weighted by color attribute) and down-weights background regions.

The final image-text similarity score is a weighted sum over region-phrase similarities, where weights are learned via a lightweight gating network.

### 2. Hierarchical Matching Loss (HML)

Standard triplet/contrastive losses only enforce global image-text matching. HML adds two levels of supervision:

- **Global level**: InfoNCE loss over image-text pairs in the batch (standard contrastive).
- **Local level**: A region-phrase matching loss that encourages each text phrase to match at least one visual region (and vice versa). This is implemented as a bidirectional Chamfer-style matching loss.

The total loss: `L_total = L_global + λ L_local`, with λ = 0.3 selected via validation.

## Datasets

- **MS-COCO (1K test split)**: 5,000 test images, 25,010 captions. Standard Karpathy split. R@1/R@5/R@10 reported.
- **Flickr30k (1K test split)**: 1,000 test images, 5,000 captions. Standard split.
- **CUB-200 (Text-to-Image)**: Fine-grained bird retrieval. 11,788 images, 10 captions per image. Tests fine-grained alignment capability.

## Baselines

| Baseline | Type | Description |
|----------|------|-------------|
| CLIP (ViT-B/16) | Global alignment | Standard CLIP zero-shot retrieval |
| BLIP (ViT-B/16) | Global + captioning | BLIP retrieval model |
| VSE++ | Fine-grained | Visual-semantic embedding with hard negative mining |
| SCAN | Fine-grained | Stacked cross-attention for region-word matching |
| CHAN | Fine-grained | Cross-modal hierarchical attention network |

## Experiments

### Main Results (R@1, R@5, R@10)

See `experiments/results.csv`. All numbers are mean ± std over 5 random seeds (42, 123, 456, 789, 1024).

### Ablation

| Variant | COCO R@1 | Flickr R@1 |
|---------|----------|------------|
| Full SGA | 64.2 | 78.5 |
| w/o Semantic Re-weighting | 62.1 | 76.3 |
| w/o HML Local Level | 62.8 | 76.9 |
| w/o Both | 60.5 | 74.8 |
| Global Only (CLIP-style baseline) | 58.3 | 72.1 |

### Efficiency

- Parameters: 187M (ViT-B/16 86M + BERT-base 110M + SGA module 11M; the SGA overhead is ~6% of the backbone total).
- Inference time: 34ms per query (batch size 1, A100 GPU) vs. 31ms for CLIP (zero-shot, same backbone).
- The gating network adds ~0.8M parameters and <1ms overhead.

## Implementation Details

- Framework: PyTorch 2.1
- Pretrained weights: ViT-B/16 from OpenAI CLIP, BERT-base from HuggingFace
- Optimizer: AdamW, lr=1e-4 (ViT), lr=5e-5 (BERT), weight_decay=0.01
- Schedule: Cosine annealing with 5-epoch linear warmup
- Batch size: 128 (across 4×A100-80GB)
- Epochs: 30 (COCO), 20 (Flickr30k)
- Image size: 224×224 (COCO/Flickr), 256×256 (CUB)
- Max text length: 77 tokens (BERT tokenizer)

## Missing Information

- AUTHOR_INPUT_NEEDED: CUB-200 results are preliminary; full evaluation pending.
- AUTHOR_INPUT_NEEDED: Video retrieval extension results not yet available.
- AUTHOR_INPUT_NEEDED: Statistical significance tests (paired bootstrap) for all dataset pairs.
- AUTHOR_INPUT_NEEDED: Code release URL.

## Known Limitations

1. The SGA module adds ~6% parameter overhead. For deployment on edge devices, model distillation may be needed.
2. The method assumes paired image-text training data. For domains with limited paired data, alternative training strategies may be required.
3. Performance on abstract/artistic images (not in training distribution) is untested.
4. The current evaluation is limited to English queries. Multilingual retrieval is not evaluated.
