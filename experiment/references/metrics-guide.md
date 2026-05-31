# Metrics Guide

## Usually Higher Is Better

- **Classification**: Accuracy, Precision, Recall, F1 (micro/macro/weighted), AUC, AUROC, AUPRC
- **Detection**: mAP, AP, AP@50, AP@75, AP@[.50:.95], AR
- **Segmentation**: IoU, mIoU, Dice coefficient, Pixel Accuracy
- **Retrieval**: Recall@K (R@1, R@5, R@10), Precision@K, mAP, NDCG
- **Generation (text)**: BLEU, ROUGE-1/2/L, METEOR, CIDEr, SPICE, BERTScore, COMET
- **Generation (image)**: FID (inverted: lower is better), IS, CLIP Score
- **Image quality**: PSNR, SSIM, MS-SSIM, LPIPS (inverted: lower is better)

## Usually Lower Is Better

- **Errors**: Error rate, MAE, MSE, RMSE, WER, CER
- **Calibration**: ECE, MCE
- **Efficiency**: FLOPs, parameters, latency/ms, memory/MB, inference time
- **Diversity metrics**: Perplexity (for language models; lower can mean better or worse depending on context)

## Task-Specific Metric Recommendations

| Task | Primary Metric(s) | Secondary Metric(s) | Notes |
|------|-------------------|---------------------|-------|
| Image classification | Top-1 Accuracy | Top-5 Accuracy, F1 (for imbalanced) | For fine-grained, also report per-class accuracy |
| Object detection | mAP (AP@[.50:.95]) | AP@50, AP@75, AP_small/medium/large | COCO-style mAP is standard |
| Semantic segmentation | mIoU | Pixel Accuracy, Dice, Boundary F1 | mIoU can be sensitive to class count |
| Text classification | F1 (macro for imbalanced) | Accuracy | Accuracy is misleading for imbalanced classes |
| NER | Span-level F1 | Entity-level F1 | Token-level F1 is less meaningful |
| QA (extractive) | Exact Match, F1 | — | Both together give a complete picture |
| Summarization | ROUGE-1/2/L | BERTScore, METEOR | ROUGE alone is insufficient for evaluation |
| MT | BLEU, COMET | chrF | BLEU is standard but coarse; COMET is model-based and correlates better with human judgment |
| Image-text retrieval | Recall@K (R@1, R@5, R@10) | R@sum, R-mean | Both image→text and text→image retrieval should be reported |
| Efficiency | Parameters (M), FLOPs (G), Latency (ms) | Throughput (samples/s), Memory (GB) | Always report hardware + batch size for latency |

## Composite Metric Rules

- **Mean ± Std**: Report "82.3 ± 0.4" (not "82.3 (0.4)") over at least 3 runs.
- **Best-of-N**: Only report if you also report the mean. Best-of-N alone is cherry-picking.
- **Confidence intervals**: 95% CI is standard. Report as "[82.1, 82.5]".
- **Statistical significance**: Report p-value AND effect size. "p < 0.01" alone doesn't tell you if the improvement matters.

## What Counts as a Meaningful Improvement

| Domain | Metric | Meaningful Threshold |
|--------|--------|---------------------|
| ImageNet classification | Top-1 Accuracy | ≥1 percentage point |
| COCO detection | mAP (AP) | ≥1 mAP point |
| Cityscapes segmentation | mIoU | ≥1 mIoU point |
| Machine translation (WMT) | BLEU | ≥1 BLEU point |
| Summarization | ROUGE-L | ≥1 ROUGE point |
| Retrieval (Flickr30k) | R@1 | ≥2 percentage points |
| Efficiency | Latency / FLOPs | Context-dependent — report % change |

These are rough guidelines. A 0.5 point improvement can be meaningful if: (a) it's consistent across all datasets, (b) the baseline is already very strong, or (c) it comes with efficiency gains.

## Always Verify

Some metrics are task-specific or inverted (e.g., FID: lower is better; LPIPS: lower is better). When unclear, check the original paper that proposed the metric. If still unclear, ask for author confirmation rather than misinterpreting.
