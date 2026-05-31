# English Polished Manuscript

# Semantic-Guided Alignment: Fine-Grained Cross-Modal Retrieval via Learned Region-Phrase Re-Weighting

## Abstract

Establishing fine-grained semantic correspondence between natural language queries and visual content is the central challenge in cross-modal text-to-image retrieval. Existing approaches fall into two paradigms: global alignment methods (e.g., CLIP, BLIP), which compress images into single vectors at the cost of fine-grained region-phrase correspondence; and fine-grained methods (e.g., SCAN, CHAN), which compute region-phrase similarities but aggregate them via fixed pooling strategies, thereby treating all visual regions as equally important — an assumption that often fails in practice. To address this limitation, we propose Semantic-Guided Alignment (SGA), a method built on two innovations. First, the Semantic-Guided Alignment module learns to re-weight visual regions according to their semantic relevance to the query through a lightweight gating network (0.8M parameters). Second, the Hierarchical Matching Loss (HML) jointly supervises global image-text matching and local region-phrase matching, providing dual-level cross-modal supervision. Experiments on MS-COCO, Flickr30k, and CUB-200 demonstrate that SGA consistently outperforms five baselines across all Recall@K metrics, improving R@1 by 1.2 to 2.6 percentage points, while adding only 6% parameter overhead (+11M) over the backbone. Ablation studies confirm that semantic re-weighting (contributing ~2.1-2.3 R@1) and the hierarchical loss (contributing ~1.4-1.6 R@1) each independently improve performance, with approximately additive combined effects. Code will be released.

**Index Terms** — cross-modal retrieval; image-text matching; fine-grained alignment; vision-language; contrastive learning.

## I Introduction

Text-to-image retrieval — retrieving the most relevant images from a gallery given a natural language query — is a core task in multimedia search, with broad applications in e-commerce, digital asset management, content moderation, and assistive visual search. The rapid progress of vision-language pretraining has substantially advanced retrieval performance. Yet, establishing fine-grained semantic correspondence between queries and images remains the fundamental challenge that limits further progress.

Existing retrieval methods can be broadly categorized into two paradigms. Global alignment methods, exemplified by CLIP, BLIP, and ALBEF, encode images and text into single global vectors and match them via cosine similarity. These methods benefit from computational efficiency and large-scale pretraining, but compressing an image into a single vector inevitably discards fine-grained visual information — for a query like "a red car parked under a tree," a single global vector struggles to simultaneously encode color, object identity, and spatial relationships. Fine-grained alignment methods, exemplified by VSE++, SCAN, and CHAN, extract image region features and text phrase features, computing region-phrase similarity matrices for more precise cross-modal matching. However, when aggregating these similarities, these methods employ fixed pooling strategies (average, max, or attention pooling), applying the same aggregation to all queries. This implicitly assumes all visual regions are equally important for all queries — an assumption that fails when queries have different semantic foci.

Consider two queries: "a red car" and "a car parked under a tree." For the first, discriminative regions are those encoding the car's color; for the second, regions encoding both the car and the spatial relationship with the tree are relevant. Fixed pooling strategies cannot make this query-dependent distinction, and this limitation constrains the performance ceiling of fine-grained retrieval.

To address this gap, we propose Semantic-Guided Alignment (SGA). The key insight is that region importance should be query-dependent: a lightweight gating network can learn to predict, for each query, which visual regions are semantically relevant. SGA implements this insight through two complementary mechanisms. First, the SGA module computes a region-phrase similarity matrix and applies learned re-weighting via the gating network. Second, the Hierarchical Matching Loss (HML) augments the standard global contrastive loss with a local Chamfer-style matching loss, explicitly encouraging region-phrase alignment.

Our main contributions are:
1. We identify the limitation of fixed region aggregation in existing fine-grained retrieval and validate the necessity of query-aware re-weighting through quantitative ablation studies (Section III-B).
2. We propose the Semantic-Guided Alignment (SGA) module, a plug-and-play component that achieves query-aware region re-weighting via a lightweight gating network, adding only 0.8M parameters (Section III-B).
3. We design the Hierarchical Matching Loss (HML), combining global InfoNCE with local Chamfer-style matching for dual-level cross-modal supervision. Ablation confirms the two components contribute approximately additively (Section III-C).
4. Across MS-COCO (R@1 64.2%), Flickr30k (R@1 78.5%), and CUB-200 (R@1 38.8%), SGA consistently outperforms five baselines on all Recall@K metrics, with R@1 improvements of 1.2-2.6 percentage points. The largest gain occurs on the fine-grained CUB-200 dataset (+2.6 R@1; 7.2% relative), validating semantic re-weighting for tasks requiring precise visual attribute discrimination (Section IV).
5. Code and pretrained models will be publicly released.

## II Related Work

### II-A Vision-Language Pretraining for Retrieval

Contrastive language-image pretraining, pioneered by CLIP, enables strong zero-shot retrieval by training dual-tower encoders on web-scale image-text pairs. BLIP extends this paradigm with guided language modeling to unify vision-language understanding and generation. ALBEF proposes an "align before fuse" strategy, applying contrastive learning prior to cross-modal fusion. These methods all encode images into single global vectors, creating an information bottleneck for high-precision fine-grained retrieval. Our method inherits these pretrained encoders as backbones and builds fine-grained alignment modules on top.

### II-B Fine-Grained Image-Text Matching

VSE++ enhances visual-semantic embedding discriminativeness through hard negative mining, though it retains globally pooled features. SCAN introduces stacked cross-attention, modeling region-word correspondence explicitly for the first time. CHAN achieves multi-level region-word alignment through a hierarchical attention network, representing the state of the art among fine-grained methods. Despite their advances, these methods employ fixed attention or pooling mechanisms to aggregate region-level similarities — an approach that cannot dynamically adapt to query content. SGA directly addresses this limitation through a learnable gating network that performs query-aware region re-weighting.

### II-C Multi-Level Supervision in Multimodal Learning

FILIP demonstrates that token-level fine-grained alignment during contrastive pretraining substantially outperforms global CLIP-style alignment, providing strong evidence for the value of fine-grained supervision. Methods such as X-VLM further explore multi-granular vision-language correspondence. Our HML draws on this line of work but adapts the idea specifically for retrieval: we employ a bidirectional Chamfer-style matching loss for region-phrase alignment, which is more lightweight than dense token-level alignment.

## III Proposed Method

### III-A Overview

Figure 1 illustrates the SGA architecture. Given an image I and a text query T: (1) a visual encoder (ViT-B/16, CLIP-pretrained) extracts region features V ∈ R^{N×d}; (2) a text encoder (BERT-base) extracts phrase features U ∈ R^{M×d}; (3) the SGA module computes a region-phrase similarity matrix and applies semantic re-weighting (Section III-B); (4) the re-weighted similarity is aggregated into a single matching score; and (5) the Hierarchical Matching Loss provides dual-level supervision during training (Section III-C). At inference, SGA computes matching scores for all gallery images and returns results ranked by descending score.

### III-B Semantic-Guided Alignment Module

The SGA module is the core contribution of this work. Its design is motivated by the observation that discriminative visual regions depend on query semantics — a dependency that fixed pooling strategies fail to capture.

The module proceeds in two steps:

**Step 1: Region-Phrase Similarity Computation.** Given visual region features V and text phrase features U, we compute the similarity matrix S ∈ R^{N×M}:
    S_{i,j} = v_i^T u_j / τ                                          (1)
where τ is a learnable temperature parameter (initialized to 0.07).

**Step 2: Semantic Re-Weighting.** The flattened similarity matrix is passed through a lightweight gating network G_θ(·):
    W = G_θ(S) = σ(MLP(Flatten(S)))                                  (2)
where the MLP uses a bottleneck structure (d → d/4 → N), σ is the sigmoid activation, and W ∈ R^{N} represents the semantic relevance weight for each visual region. The final matching score is:
    score(I, T) = Σ_i W_i · max_j S_{i,j}                            (3)

The gating network contributes only 0.8M parameters (~0.5% of the backbone total), making the module practical for deployment. Ablation experiments comparing bottleneck architectures (Section IV-C) confirm this design achieves the best accuracy-efficiency trade-off.

### III-C Hierarchical Matching Loss

The training objective combines two complementary loss terms:
    L_total = L_global + λ L_local                                   (4)

**Global Matching Loss (L_global).** A symmetric InfoNCE loss over image-text pairs within the batch:
    L_global = -(1/2B) Σ_i [log(exp(s_{i,i}/τ_g) / Σ_j exp(s_{i,j}/τ_g)) + log(exp(s_{i,i}/τ_g) / Σ_j exp(s_{j,i}/τ_g))]  (5)

**Local Matching Loss (L_local).** A bidirectional Chamfer-style matching loss that encourages each text phrase to match at least one visual region, and each visual region to match at least one text phrase:
    L_local = (1/B) Σ_k [ (1/M) Σ_j min_i ||v_{k,i} - u_{k,j}||^2 + (1/N) Σ_i min_j ||v_{k,i} - u_{k,j}||^2 ]  (6)

The weight λ = 0.3 was selected via grid search on the MS-COCO validation set. Critically, ablation studies in Section IV-C demonstrate that L_local and semantic re-weighting contribute independently, with their combined effect being approximately additive. This independence suggests the two mechanisms address complementary aspects of fine-grained alignment.

### III-D Implementation Details

We implement SGA in PyTorch 2.1. The visual encoder uses OpenAI CLIP ViT-B/16 weights (86M parameters) and the text encoder uses BERT-base (110M parameters). The SGA module adds approximately 11M parameters, of which the gating network accounts for 0.8M.

Training uses AdamW with separate learning rates: 1e-4 for the visual encoder, 5e-5 for the text encoder, and 1e-3 for the randomly initialized SGA module. The learning rate follows a cosine annealing schedule preceded by 5 epochs of linear warmup, with weight decay of 0.01. We use a batch size of 128 across four NVIDIA A100-80GB GPUs, training for 30 epochs on MS-COCO and 20 epochs on Flickr30k. Input images are resized to 224×224 (COCO/Flickr) or 256×256 (CUB), with a maximum text length of 77 BERT WordPiece tokens. All results are reported as the mean ± standard deviation over five random seeds (42, 123, 456, 789, 1024).

## IV Experiments

### IV-A Datasets and Metrics

We evaluate SGA on three public datasets spanning general and fine-grained retrieval scenarios:

**MS-COCO (5K test set)** contains 5,000 test images with 25,010 captions, using the standard Karpathy split. **Flickr30k (1K test set)** contains 1,000 test images with 5,000 captions. **CUB-200** is a fine-grained bird retrieval dataset with 11,788 images and 10 captions per image, testing the model's ability to discriminate subtle visual differences.

All experiments use Recall@K (K=1,5,10) as the evaluation metric, where higher values indicate better performance. Results are reported as mean ± standard deviation over five random seeds.

We compare against five baselines: CLIP (ViT-B/16), BLIP (ViT-B/16), VSE++, SCAN, and CHAN — spanning both global and fine-grained paradigms. All baselines use their officially released code and recommended hyperparameters.

### IV-B Main Results

Table 1 reports the comparison across all three datasets. SGA consistently outperforms all five baselines on every Recall@K metric.

On MS-COCO, SGA achieves R@1 = 64.2% (±0.3), outperforming the strongest baseline CHAN (63.0% ±0.3) by 1.2 percentage points (1.9% relative improvement). R@5 reaches 87.3% (+1.2 over CHAN) and R@10 reaches 93.9% (+0.7).

On Flickr30k, SGA achieves R@1 = 78.5% (±0.3), surpassing CHAN (76.9% ±0.3) by 1.6 percentage points (2.1% relative). R@5 reaches 93.5% (+0.7) and R@10 reaches 96.8% (+0.5). The diminishing gain at higher K values reflects the near-saturation of R@10 on this benchmark (both SGA and CHAN exceed 96%).

On CUB-200, SGA achieves its largest margin: R@1 = 38.8% (±0.6), surpassing CHAN (36.2% ±0.6) by 2.6 percentage points (7.2% relative improvement). R@5 reaches 67.5% (+2.7) and R@10 reaches 81.3% (+2.2). The substantially larger gain on this fine-grained dataset validates our hypothesis that semantic re-weighting is particularly beneficial when discriminative visual details must be precisely matched to query attributes.

Three patterns emerge from these results. First, SGA's advantage is consistently largest at R@1 and diminishes at higher K, indicating that the method primarily improves the most challenging retrieval cases — precisely where fine-grained discrimination matters most. Second, the gain magnitude correlates with the granularity of the retrieval task: general datasets show moderate gains (+1.2-1.6 R@1) while the fine-grained dataset shows a substantially larger gain (+2.6 R@1). Third, the small standard deviations (±0.1-0.6) across five seeds indicate that SGA's improvements are stable and not an artifact of random initialization.

### IV-C Ablation Study

Table 2 reports the ablation results across all three datasets, isolating the contributions of semantic re-weighting and hierarchical matching.

Starting from the full SGA model (COCO R@1 = 64.2%), we individually remove each component. Removing semantic re-weighting (replacing the gating network with uniform weights) reduces R@1 to 62.1% (−2.1). This consistent 2.1-2.3 point drop across all three datasets confirms that query-aware region weighting is the primary driver of SGA's advantage. Removing the local term of HML (keeping only L_global) reduces R@1 to 62.8% (−1.4), demonstrating that explicit region-phrase supervision provides a meaningful but smaller complementary benefit. Removing both components simultaneously (effectively reducing to a global alignment model with InfoNCE loss) reduces R@1 to 60.5% (−3.7). As a lower bound, the CLIP zero-shot baseline (no SGA module, no fine-tuning) achieves only 58.3% R@1 (−5.9).

The two components' contributions are approximately additive: the sum of individual drops (−2.1) + (−1.4) = −3.5 approximately equals the joint removal drop of −3.7. This near-additivity suggests that semantic re-weighting and local matching supervision operate through complementary mechanisms — re-weighting determines *which regions to focus on*, while local matching ensures *the selected regions are correctly aligned with text*.

We also compare alternative gating architectures (Table 3). A simpler design without the bottleneck (d → N directly) uses 3.2M parameters for the gating network alone and achieves R@1 = 64.0% on COCO — only 0.2 points below the bottleneck design despite 4× more parameters. A deeper design with two hidden layers (d → d/2 → d/4 → N, 1.7M parameters) yields 64.1% — statistically indistinguishable from our design. We adopt the single-bottleneck design for its favorable accuracy-parameter trade-off.

### IV-D Efficiency Analysis

Table 4 compares model size and inference speed. SGA uses 187M total parameters, of which the SGA module accounts for 11M. Compared to the CLIP ViT-B/16 baseline (176M), SGA adds only 6% in parameters. Among fine-grained methods, SCAN uses 152M (lighter but less accurate) and CHAN uses 195M (heavier). On a single A100 GPU with batch size 1, SGA requires 34ms per query — 3ms more than the CLIP zero-shot baseline (31ms), of which the gating network accounts for less than 1ms. This 10% latency increase is modest relative to the retrieval accuracy gains, and the absolute latency remains practical for interactive retrieval applications.

### IV-E Qualitative Analysis

Figure 2 presents qualitative retrieval comparisons between SGA and CHAN on MS-COCO. For color-attribute queries (e.g., "a red double-decker bus"), SGA's top-3 results all correctly contain red double-decker buses, whereas CHAN's second-ranked result depicts a non-red bus, suggesting CHAN prioritizes object category over color attribute. For spatial-relationship queries (e.g., "a cat sitting on a chair"), SGA correctly retrieves images where the cat is positioned on top of the chair in all top results, while CHAN includes an image where the cat is beside the chair. These examples qualitatively illustrate the mechanism underlying SGA's quantitative advantage: semantic re-weighting enables the model to emphasize query-relevant visual attributes (color, spatial relationship) rather than relying predominantly on object category matches.

## V Conclusion

We have presented Semantic-Guided Alignment (SGA), a method that addresses the limitation of fixed region aggregation in fine-grained cross-modal retrieval through two complementary mechanisms: a lightweight gating network that performs query-aware visual region re-weighting, and a Hierarchical Matching Loss that provides dual-level cross-modal supervision. Across MS-COCO, Flickr30k, and the fine-grained CUB-200 dataset, SGA consistently outperforms five baselines on all Recall@K metrics, improving R@1 by 1.2 to 2.6 percentage points, while incurring only a 6% parameter overhead. Ablation studies confirm the independent and approximately additive contributions of both innovations.

Several limitations merit acknowledgment. First, the 6% parameter increase and 10% inference latency overhead, while modest, may require model distillation for deployment in latency-critical applications. Second, our evaluation is limited to English queries; multilingual retrieval capability remains untested. Third, performance on out-of-distribution abstract or artistic images has not been assessed. We regard addressing these limitations — through video-text extension, multilingual adaptation, and edge-oriented distillation — as promising directions for future work.

## References

[1] A. Radford et al., "Learning Transferable Visual Models From Natural Language Supervision," in Proc. ICML, 2021.
[2] J. Li et al., "BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation," in Proc. ICML, 2022.
[3] J. Li et al., "Align before Fuse: Vision and Language Representation Learning with Momentum Distillation," in Proc. NeurIPS, 2021.
[4] F. Faghri et al., "VSE++: Improving Visual-Semantic Embeddings with Hard Negatives," in Proc. BMVC, 2018.
[5] K.-H. Lee et al., "Stacked Cross Attention for Image-Text Matching," in Proc. ECCV, 2018.
[6] J. Pan et al., "CHAN: Cross-Modal Hierarchical Attention Network for Image-Text Matching," IEEE Trans. Image Processing, 2023.
[7] L. Yao et al., "FILIP: Fine-grained Interactive Language-Image Pre-training," in Proc. ICLR, 2022.
[8] T.-Y. Lin et al., "Microsoft COCO: Common Objects in Context," in Proc. ECCV, 2014.
[9] B. A. Plummer et al., "Flickr30k Entities: Collecting Region-to-Phrase Correspondences for Richer Image-to-Sentence Models," in Proc. ICCV, 2015.
[10] C. Wah et al., "The Caltech-UCSD Birds-200-2011 Dataset," Caltech, Tech. Rep. CNS-TR-2011-001, 2011.
[11] A. Mogadala et al., "Trends in Integration of Vision and Language: A Survey," Comput. Vis. Image Understand., 2021.
[12] N. Messina et al., "TERAN: Transformer-based Fine-grained Image-Text Matching," IEEE Trans. Image Processing, 2021.
