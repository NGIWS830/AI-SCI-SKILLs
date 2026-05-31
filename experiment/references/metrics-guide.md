# Metrics Guide

## Usually higher is better

- Accuracy, Precision, Recall, F1
- AUC, AUROC, AUPRC
- mAP, AP, AP50, AP75
- IoU, mIoU, Dice
- BLEU, ROUGE, METEOR, CIDEr, SPICE
- PSNR, SSIM

## Usually lower is better

- Loss
- Error rate
- MAE, MSE, RMSE
- WER, CER
- ECE calibration error
- Latency, FLOPs, parameters, memory when evaluating efficiency

## Always verify

Some metrics are task-specific or inverted. If unclear, ask for author confirmation rather than interpreting.
