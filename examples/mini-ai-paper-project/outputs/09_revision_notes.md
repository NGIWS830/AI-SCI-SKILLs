# Revision Notes: CN-EN Consistency, Terminology, and Claims Alignment

## CN-EN Consistency Check

| Check Item | Chinese (06) | English (08) | Status |
|-----------|-------------|-------------|--------|
| R@1 values | 64.2%, 78.5%, 38.8% | 64.2%, 78.5%, 38.8% | ✓ Match |
| Ablation numbers | −2.1, −1.4, −3.7 | −2.1, −1.4, −3.7 | ✓ Match |
| Parameter overhead | 6% (+11M) | 6% (+11M) | ✓ Match |
| λ value | 0.3 | 0.3 | ✓ Match |
| Datasets listed | COCO, Flickr30k, CUB-200 | COCO, Flickr30k, CUB-200 | ✓ Match |
| 5 baselines named | CLIP, BLIP, VSE++, SCAN, CHAN | CLIP, BLIP, VSE++, SCAN, CHAN | ✓ Match |
| Claim strength | "一致优于" (consistently outperforms) | "consistently outperforms" | ✓ Match |
| Limitation phrasing | "局限性包括" (limitations include) | "Several limitations merit acknowledgment" | ✓ Match |

## Terminology Consistency Check

| Concept | Chinese Term | English Term | Consistent? |
|---------|-------------|-------------|-------------|
| SGA method name | 语义引导对齐 (SGA) | Semantic-Guided Alignment (SGA) | ✓ |
| SGA module | 语义引导对齐模块 | Semantic-Guided Alignment module | ✓ |
| HML | 层次匹配损失 (HML) | Hierarchical Matching Loss (HML) | ✓ |
| Gating network | 门控网络 | gating network | ✓ |
| Region features | 区域特征 | region features | ✓ |
| Phrase features | 短语特征 | phrase features | ✓ |
| Recall@K | Recall@K (K=1,5,10) | Recall@K (K=1,5,10) | ✓ |
| Fine-grained | 细粒度 | fine-grained | ✓ |
| Backbone | 骨干网络 | backbone | ✓ |
| Ablation | 消融实验 | ablation study | ✓ |

## Claims Alignment Audit

| Claim | Evidence Source | CN Strength | EN Strength | Alignment |
|-------|----------------|-------------|-------------|-----------|
| SGA outperforms baselines | Table 1 (3 datasets) | 一致优于 | consistently outperforms | ✓ Strong, well-supported |
| Semantic re-weighting contributes ~2.1-2.3 R@1 | Ablation Table 2 | 独立贡献 | independently contribute | ✓ Strong, well-supported |
| HML contributes ~1.4-1.6 R@1 | Ablation Table 2 | 独立贡献 | independently contribute | ✓ Strong, well-supported |
| Contributions are additive | Ablation Table 2 | 近似可加 | approximately additive | ✓ Qualified ("approximately") |
| SGA benefits fine-grained tasks most | CUB-200 result | 验证了...有效性 | validates the effectiveness | ✓ Claim matches evidence |
| Parameter overhead is modest | 187M vs 176M | 仅增加6% | only 6% overhead | ✓ Honest and quantified |

## Issues Identified

### Must-Fix
(None)

### Should-Fix
1. **AUTHOR_INPUT_NEEDED (pending author input)**: Statistical significance tests, CUB-200 full evaluation, code URL.
2. **Competitor recency**: The baseline list may need updating to include the most recent methods (e.g., BEiT-3, SigLIP) — verify via literature search before submission.
3. **CUB-200 domain**: The CUB-200 dataset is cited as a "fine-grained" benchmark, but CUB-200 evaluates a specific domain (birds). A note clarifying that results on additional fine-grained benchmarks (e.g., SOP, DeepFashion) would strengthen the "fine-grained" generalization claim.

### Notes
- The R@10 saturation on Flickr30k (96.8%) makes this metric less informative for future comparisons. Consider reporting R-mean or adding a harder benchmark.
- The 6% parameter overhead is quantified honestly. The paper would benefit from comparing this overhead to other fine-grained methods' overheads.
