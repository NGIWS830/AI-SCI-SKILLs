# Improvement Summary

- Source: `experiments/results.csv`
- Target method: `SGA-Ours`
- Baseline method: `CHAN` (strongest competitor across all datasets)
- Group columns: `Dataset`

| Group | Metric | Direction | Target | Baseline | Δ Absolute | Δ Relative |
|---|---:|---:|---|---|---|---|
| CUB-200 | R@1 | higher | 38.8 | 36.2 | +2.6 | +7.18% |
| CUB-200 | R@5 | higher | 67.5 | 64.8 | +2.7 | +4.17% |
| CUB-200 | R@10 | higher | 81.3 | 79.1 | +2.2 | +2.78% |
| Flickr30k | R@1 | higher | 78.5 | 76.9 | +1.6 | +2.08% |
| Flickr30k | R@5 | higher | 93.5 | 92.8 | +0.7 | +0.75% |
| Flickr30k | R@10 | higher | 96.8 | 96.3 | +0.5 | +0.52% |
| MS-COCO | R@1 | higher | 64.2 | 63.0 | +1.2 | +1.90% |
| MS-COCO | R@5 | higher | 87.3 | 86.1 | +1.2 | +1.39% |
| MS-COCO | R@10 | higher | 93.9 | 93.2 | +0.7 | +0.75% |

## Key Takeaways

- **Largest absolute gain**: +2.7 R@5 on CUB-200 (fine-grained retrieval benefits most from semantic alignment).
- **Largest relative gain**: +7.18% on CUB-200 R@1.
- **Most competitive setting**: MS-COCO R@10 (+0.7 absolute, +0.75% relative) and Flickr30k R@10 (+0.5, +0.52%) — R@10 is saturating on Flickr30k (both >96%).
- **Consistent pattern**: SGA's advantage is largest at R@1 and decreases at higher K values, suggesting the method primarily helps with the hardest (most discriminative) retrieval cases.
