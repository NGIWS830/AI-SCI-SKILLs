# Reference-Style Manuscript Outline

# Title

Semantic-Guided Alignment: Fine-Grained Cross-Modal Retrieval via Learned Region-Phrase Re-Weighting

## Abstract

Task, gap, SGA method, key results, implication.

## Index Terms

Cross-modal retrieval; image-text matching; fine-grained alignment; vision-language; contrastive learning.

## I Introduction

### Para 1: Task Importance
Text-to-image retrieval is fundamental to multimedia search, with applications in e-commerce, digital asset management, and content moderation. The core challenge is bridging the semantic gap between natural language queries and visual content.

### Para 2: Current Progress
Two paradigms dominate: (a) global alignment methods (CLIP, BLIP) that encode images and text into single vectors — efficient but coarse; (b) fine-grained methods (SCAN, CHAN) that compute region-word similarities — more precise but use fixed aggregation. Both have improved retrieval but leave room for better fine-grained matching.

### Para 3: Gap
Existing fine-grained methods treat all image regions as equally important during similarity computation. However, for a query like "a red car under a tree," the relevant regions depend on which part of the query is being matched. A fixed pooling strategy (average, max) cannot adaptively emphasize the discriminative regions for each specific query.

### Para 4: Proposed Method
We propose Semantic-Guided Alignment (SGA), which introduces: (1) a lightweight gating network that learns to re-weight visual regions based on their semantic relevance to the query; and (2) a Hierarchical Matching Loss (HML) that jointly supervises global image-text and local region-phrase alignment.

### Para 5: Contributions
1. We identify the limitation of fixed region aggregation in fine-grained retrieval and propose learned semantic re-weighting as a solution (Section III-B).
2. We introduce Hierarchical Matching Loss, a dual-level objective that improves both holistic and fine-grained alignment (Section III-C).
3. On MS-COCO, Flickr30k, and CUB-200, SGA consistently outperforms 5 baselines (+1.2 to +2.6 R@1) with only +6% parameter overhead. Ablation confirms both components contribute independently.

## II Related Work

### II-A Vision-Language Pretraining for Retrieval
CLIP, BLIP, ALBEF — global alignment paradigm. Efficient but coarse. Our method uses their pretrained encoders but adds fine-grained alignment on top.

### II-B Fine-Grained Image-Text Matching
VSE++, SCAN, CHAN, TERAN — region-word alignment. We differ by using learned re-weighting instead of fixed pooling, and hierarchical loss instead of single-level supervision.

### II-C Multi-Level Supervision in Multimodal Learning
FILIP (token-level), X-VLM (multi-granularity). Our HML draws on this line of work but adapts it specifically for retrieval with a lightweight Chamfer-style local loss.

## III Proposed Method

### III-A Overview
Figure 1 shows the SGA architecture. Given an image I and text query T: (1) ViT-B/16 extracts region features, (2) BERT-base extracts phrase features, (3) the SGA module computes region-phrase similarities with semantic re-weighting, (4) the final similarity score is aggregated via the gating network, (5) HML supervises both global and local alignment.

### III-B Semantic-Guided Alignment Module
Input → gating network → re-weighted similarity matrix → aggregated score. Design rationale: learned re-weighting adapts to query semantics.

### III-C Hierarchical Matching Loss
L_global (InfoNCE) + L_local (Chamfer-style bidirectional matching). λ = 0.3. Each loss term corresponds to an ablation row.

### III-D Training and Implementation Details
PyTorch 2.1, AdamW, cosine schedule, 4×A100, batch 128. ViT lr=1e-4, BERT lr=5e-5.

## IV Experiments

### IV-A Datasets and Metrics
MS-COCO (5K test), Flickr30k (1K test), CUB-200 (full). R@1, R@5, R@10. Higher is better.

### IV-B Implementation Details
(Full details from project_notes.md)

### IV-C Main Results
Table 1 — all 3 datasets, 5 baselines. SGA outperforms all on all metrics. Prose: COCO +1.2, Flickr +1.6, CUB +2.6 over CHAN.

### IV-D Ablation Study
Table 2 — 5 variants. Both SGA re-weighting and HML local level contribute independently. Combined effect is additive.

### IV-E Efficiency Analysis
Table 3 — parameters, latency comparison. SGA adds 11M (+6%) and 3ms (+10%) vs. CLIP zero-shot baseline.

### IV-F Qualitative Analysis
Figure 2 — retrieval examples. SGA vs. CHAN: SGA retrieves more relevant images for queries with spatial/color attributes.

## V Conclusion

SGA introduces learned semantic re-weighting and hierarchical matching for fine-grained retrieval. Consistent improvements on 3 datasets. Limitations: +6% overhead, English-only, untested on abstract images. Future: video retrieval, multilingual extension, distillation for edge deployment.

## References

[12 verified citations from literature matrix]
