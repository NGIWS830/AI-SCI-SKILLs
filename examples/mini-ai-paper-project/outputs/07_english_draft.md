# English Draft (CN→EN Conversion)

# Semantic-Guided Alignment: Fine-Grained Cross-Modal Retrieval via Learned Region-Phrase Re-Weighting

## Abstract

The core challenge in cross-modal text-to-image retrieval lies in establishing fine-grained semantic correspondence between natural language queries and visual content. Existing approaches fall into two paradigms: global alignment methods (e.g., CLIP, BLIP) that compress images into a single vector, sacrificing fine-grained region-phrase correspondence; and fine-grained methods (e.g., SCAN, CHAN) that compute region-phrase similarities but use fixed pooling strategies that cannot adaptively emphasize discriminative regions based on query semantics. To address this gap, we propose Semantic-Guided Alignment (SGA), whose key innovations are: (1) a Semantic-Guided Alignment module that learns to re-weight visual regions based on query semantics via a lightweight gating network (only 0.8M parameters); and (2) a Hierarchical Matching Loss (HML) that jointly supervises global image-text matching and local region-phrase matching. Experiments on MS-COCO, Flickr30k, and CUB-200 demonstrate that SGA consistently outperforms five baselines across all Recall@K metrics (improving R@1 by 1.2 to 2.6 percentage points), while adding only 6% parameter overhead (+11M) over the backbone. Ablation studies confirm that semantic re-weighting (contributing ~2.1-2.3 R@1) and hierarchical matching loss (contributing ~1.4-1.6 R@1) each independently contribute to performance gains, with approximately additive combined effect. Code will be released.

**Index Terms** — cross-modal retrieval; image-text matching; fine-grained alignment; vision-language; contrastive learning.

## I Introduction

Text-to-image retrieval — retrieving the most relevant images from a gallery given a natural language query — is a core task in multimedia search, with broad applications in e-commerce product search, digital asset management, content moderation, and assistive visual search. While vision-language pretraining has led to substantial progress, establishing fine-grained semantic correspondence between queries and images remains the key challenge.

Existing retrieval methods based on vision-language pretraining can be broadly categorized into two paradigms. The first is global alignment methods, exemplified by CLIP, BLIP, and ALBEF, which encode images and text into single global vectors and match them via cosine similarity. These methods are computationally efficient, but compressing an image into a single vector inevitably discards fine-grained visual information. The second is fine-grained alignment methods, exemplified by VSE++, SCAN, and CHAN, which extract image region features and text phrase features and compute region-phrase similarity matrices for more precise cross-modal matching. However, these methods employ fixed pooling strategies (average pooling, max pooling, or attention pooling) when aggregating region-phrase similarities — applying the same aggregation to all queries and implicitly assuming equal importance for all visual regions. This assumption often fails in practice.

Specifically, for the queries "a red car" and "a car parked under a tree," the relevant visual regions differ fundamentally: the former requires attention to color attributes on the car region, while the latter additionally requires attention to the spatial relationship with the tree. Fixed pooling strategies cannot make this query-dependent distinction, limiting the performance ceiling of fine-grained retrieval.

To address this gap, we propose Semantic-Guided Alignment (SGA). The core idea is to introduce a learnable semantic re-weighting mechanism: given a text query, a lightweight gating network predicts the semantic relevance weight of each visual region, and these weights are used to re-weight the region-phrase similarity matrix. Additionally, SGA introduces a Hierarchical Matching Loss (HML), which augments the standard global contrastive loss with a local Chamfer-style matching loss that encourages fine-grained cross-modal correspondence by aligning each text phrase with at least one visual region, and vice versa.

Our main contributions are:
(1) We identify the limitation of fixed region aggregation in existing fine-grained retrieval methods and validate the necessity of query-aware re-weighting through quantitative ablation studies (Section III-B).
(2) We propose the Semantic-Guided Alignment (SGA) module, a plug-and-play lightweight module that achieves query-aware region re-weighting via a gating network, adding only 0.8M parameters (Section III-B).
(3) We design the Hierarchical Matching Loss (HML), which combines a global InfoNCE loss with a local Chamfer-style matching loss to provide dual-level cross-modal supervision. The two components are shown via ablation to contribute approximately additively (Section III-C).
(4) On MS-COCO (R@1 64.2%), Flickr30k (R@1 78.5%), and CUB-200 (R@1 38.8%), SGA consistently outperforms five baselines across all Recall@K metrics, with R@1 improvements of 1.2 to 2.6 percentage points. The largest gain is observed on the fine-grained CUB-200 dataset (+2.6 R@1, 7.2% relative improvement), validating the effectiveness of semantic re-weighting in scenarios requiring precise visual attribute discrimination (Section IV).
(5) Code and pretrained models will be publicly released.

## II Related Work

### II-A Vision-Language Pretraining for Retrieval

Contrastive language-image pretraining methods, led by CLIP, achieve strong zero-shot retrieval by training dual-tower encoders on hundreds of millions of image-text pairs. BLIP further introduces guided language modeling to unify vision-language understanding and generation. ALBEF proposes an "align before fuse" strategy, performing contrastive learning before cross-modal fusion. However, these methods encode images into single global vectors, creating an information bottleneck for high-precision fine-grained retrieval. Our method builds upon these pretrained encoders and adds fine-grained alignment modules on top.

### II-B Fine-Grained Image-Text Matching

VSE++ enhances the discriminativeness of visual-semantic embeddings through hard negative mining, but still uses globally pooled features. SCAN introduces stacked cross-attention for iterative fine-grained matching between image regions and text words, explicitly modeling region-word correspondence for the first time. CHAN further achieves multi-level region-word alignment through a hierarchical attention network. However, these methods use fixed attention or pooling mechanisms when aggregating region-level similarities, unable to dynamically adjust the aggregation strategy based on query content — this limitation is precisely the core problem addressed by our SGA. Unlike these methods, SGA achieves query-aware region re-weighting through a learnable gating network.

### II-C Multi-Level Supervision in Multimodal Learning

FILIP demonstrates that token-level fine-grained alignment during contrastive pretraining significantly outperforms global CLIP-style alignment. Methods such as X-VLM further explore multi-granularity vision-language correspondence learning. Our HML draws on the idea of multi-level supervision but adapts it specifically for retrieval: we use a bidirectional Chamfer-style matching loss for region-phrase alignment, which is more lightweight and efficient than dense token-level alignment.

## III Proposed Method

### III-A Overview

Figure 1 illustrates the overall SGA architecture. Given an image I and a text query T, SGA performs retrieval as follows: (1) a visual encoder (ViT-B/16, CLIP-pretrained weights) extracts region features V ∈ R^{N×d}; (2) a text encoder (BERT-base) extracts phrase features U ∈ R^{M×d}; (3) the SGA module computes a region-phrase similarity matrix and applies semantic re-weighting (Section III-B); (4) the weighted similarity score is aggregated as the image-text matching score; (5) during training, the Hierarchical Matching Loss provides dual-level supervision (Section III-C). At inference, SGA computes matching scores between the query and all images in the gallery, returning results ranked by descending score.

### III-B Semantic-Guided Alignment Module

The SGA module is the core innovation of this work. Its design is motivated by the key observation that discriminative visual regions differ depending on the semantic focus of the query. Fixed pooling strategies cannot capture this query dependency.

The SGA module consists of two sub-steps.

**Step 1: Region-Phrase Similarity Computation.** Given visual region features V and text phrase features U, we compute the similarity matrix S ∈ R^{N×M}:
    S_{i,j} = v_i^T u_j / τ                                          (1)
where τ is a learnable temperature parameter (initialized to 0.07).

**Step 2: Semantic Re-Weighting.** The similarity matrix S is flattened and passed through a lightweight gating network G_θ(·):
    W = G_θ(S) = σ(MLP(Flatten(S)))                                  (2)
where MLP uses a bottleneck structure (dimension d → d/4 → N), σ is the sigmoid activation, and output W ∈ R^{N} represents the semantic relevance weight for each visual region. The final image-text matching score is:
    score(I, T) = Σ_i W_i · max_j S_{i,j}                            (3)

The gating network adds only 0.8M parameters (~0.5% of the backbone).

### III-C Hierarchical Matching Loss

The SGA training objective consists of two levels of loss:
    L_total = L_global + λ L_local                                   (4)

**Global Matching Loss (L_global).** Symmetric InfoNCE loss over image-text pairs in the batch:
    L_global = -(1/2B) Σ_i [log(exp(s_{i,i}/τ_g) / Σ_j exp(s_{i,j}/τ_g)) + log(exp(s_{i,i}/τ_g) / Σ_j exp(s_{j,i}/τ_g))]  (5)

**Local Matching Loss (L_local).** Bidirectional Chamfer-style matching loss, encouraging each text phrase to match at least one visual region and vice versa:
    L_local = (1/B) Σ_k [ (1/M) Σ_j min_i ||v_{k,i} - u_{k,j}||^2 + (1/N) Σ_i min_j ||v_{k,i} - u_{k,j}||^2 ]  (6)

The weight λ = 0.3 was selected via validation. Ablation studies show that L_local's contribution (~1.4-1.6 R@1) is independent of semantic re-weighting's contribution (~2.1-2.3 R@1), with approximately additive combined effects.

### III-D Implementation Details

We implement SGA in PyTorch 2.1. The visual encoder uses OpenAI CLIP ViT-B/16 (86M parameters), and the text encoder uses BERT-base (110M parameters). The SGA module adds approximately 11M parameters. We use the AdamW optimizer with lr=1e-4 for the visual encoder, lr=5e-5 for the text encoder, and lr=1e-3 for the SGA module. The learning rate follows a cosine annealing schedule with 5-epoch linear warmup, and weight decay of 0.01. Batch size is 128 across 4×A100-80GB GPUs. MS-COCO is trained for 30 epochs, Flickr30k for 20 epochs. Input images are resized to 224×224 (COCO/Flickr) or 256×256 (CUB), with a maximum text length of 77 BERT tokens. All results are reported as mean ± standard deviation over five random seeds (42, 123, 456, 789, 1024).

## IV Experiments

### IV-A Datasets and Metrics

We evaluate SGA on three public datasets: (1) MS-COCO (5K test set: 5,000 images, 25,010 captions); (2) Flickr30k (1K test set: 1,000 images, 5,000 captions); and (3) CUB-200 (11,788 images, 10 captions per image). Evaluation metrics are Recall@K (K=1,5,10), where higher is better for all metrics. Results are reported as mean ± standard deviation over five random seeds.

Baselines include five methods: CLIP (ViT-B/16), BLIP (ViT-B/16), VSE++, SCAN, and CHAN. All baselines use their officially released code and recommended hyperparameters.

### IV-B Main Results

SGA consistently outperforms all baselines across all datasets and all Recall@K metrics. On MS-COCO, SGA achieves R@1 = 64.2% (+1.2 over CHAN) and R@5 = 87.3% (+1.2). On Flickr30k, R@1 = 78.5% (+1.6 over CHAN) and R@5 = 93.5% (+0.7). On CUB-200, R@1 = 38.8% (+2.6 over CHAN, 7.2% relative improvement).

Key findings: (1) The largest gain is on the fine-grained CUB-200 dataset (+2.6 R@1 vs. +1.2-1.6 on general datasets), validating the value of semantic re-weighting in scenarios requiring precise visual attribute discrimination. (2) SGA's gain is larger at R@1 than at R@5 and R@10, indicating that the method primarily improves the most challenging retrieval cases. (3) R@10 on Flickr30k is near saturation (SGA 96.8% vs. CHAN 96.3%).

### IV-C Ablation Study

We conduct ablation studies on all three datasets (Table 2). Full SGA achieves R@1 = 64.2% on COCO. Removing semantic re-weighting reduces R@1 to 62.1% (−2.1). Removing the HML local term reduces it to 62.8% (−1.4). Removing both reduces it to 60.5% (−3.7). Using only CLIP zero-shot reduces it to 58.3% (−5.9). The two components' contributions are approximately additive across all three datasets: the sum of individual contributions (~3.5-3.9) ≈ the cost of joint removal (3.7-3.9).

### IV-D Efficiency Analysis

SGA has 187M total parameters (ViT 86M + BERT 110M + SGA module 11M), representing only a 6% increase over the CLIP zero-shot baseline (176M). Single-query inference time is 34ms on an A100 GPU (batch size 1), compared to 31ms for CLIP — a 10% increase (~3ms), of which the gating network contributes less than 1ms.

### IV-E Qualitative Analysis

Figure 2 shows qualitative retrieval comparisons between SGA and CHAN on MS-COCO. For color-attribute queries (e.g., "a red double-decker bus"), SGA retrieves only red buses while CHAN's results include a non-red bus (rank 2). For spatial-relationship queries (e.g., "a cat sitting on a chair"), SGA's results correctly match the spatial relationship while CHAN's results include a case where the cat is beside rather than on the chair. These qualitative results intuitively demonstrate the effectiveness of semantic re-weighting in emphasizing discriminative visual attributes.

## V Conclusion

This paper proposed Semantic-Guided Alignment (SGA) to address the limitation of fixed region aggregation in fine-grained cross-modal retrieval. SGA achieves query-aware visual region re-weighting through a lightweight gating network and introduces Hierarchical Matching Loss (HML) to provide dual-level supervision. Across three datasets, SGA consistently outperforms five baselines on all Recall@K metrics (R@1 improvements of 1.2-2.6 percentage points), with only 6% parameter overhead. Ablation studies confirm the independent contributions of both components.

Limitations of SGA include: (1) 6% parameter increase and 10% inference latency overhead; (2) evaluation limited to English queries; and (3) performance on out-of-distribution abstract/artistic images is untested. Future work may extend SGA to video-text retrieval, multilingual retrieval, and model distillation for edge deployment.

## References

[1-12] (See 05_chinese_draft.md for full reference list)
