# Computer Vision Seed Map

Use this file only to generate search directions. Verify every citation before final use.

This seed map ensures the literature search doesn't miss foundational papers that automated API searches may overlook (older papers with lower recent citation velocity).

## CNN Classification
- AlexNet (Krizhevsky et al., NeurIPS 2012) — Deep learning breakthrough on ImageNet
- VGG (Simonyan & Zisserman, ICLR 2015) — Deep uniform architecture
- ResNet (He et al., CVPR 2016) — Residual learning, 152 layers
- DenseNet (Huang et al., CVPR 2017) — Dense connectivity
- EfficientNet (Tan & Le, ICML 2019) — Compound scaling
- ConvNeXt (Liu et al., CVPR 2022) — Modernized CNN design

## Object Detection
- R-CNN family: R-CNN → Fast R-CNN → Faster R-CNN (Girshick, Ren et al., 2014-2017)
- YOLO family: YOLOv1-v8 (Redmon, Bochkovskiy, Ultralytics, 2015-2023)
- SSD (Liu et al., ECCV 2016) — Single-shot detection
- RetinaNet + Focal Loss (Lin et al., ICCV 2017) — Class imbalance in detection
- DETR (Carion et al., ECCV 2020) — Transformer-based detection
- Deformable DETR (Zhu et al., ICLR 2021) — Efficient attention for detection
- DINO (Zhang et al., ICLR 2023) — Improved DETR-style detection

## Semantic Segmentation
- FCN (Long et al., CVPR 2015) — Fully convolutional segmentation
- U-Net (Ronneberger et al., MICCAI 2015) — Encoder-decoder with skip connections
- DeepLab family: v1, v2, v3, v3+ (Chen et al., 2014-2018) — Atrous convolution, ASPP
- PSPNet (Zhao et al., CVPR 2017) — Pyramid pooling
- Mask R-CNN (He et al., ICCV 2017) — Instance segmentation
- SegFormer (Xie et al., NeurIPS 2021) — Hierarchical transformer for segmentation
- Mask2Former (Cheng et al., CVPR 2022) — Universal segmentation architecture

## Vision Transformers
- ViT (Dosovitskiy et al., ICLR 2021) — Pure transformer for image classification
- DeiT (Touvron et al., ICML 2021) — Data-efficient ViT training
- Swin Transformer (Liu et al., ICCV 2021) — Hierarchical shifted-window transformer
- MAE (He et al., CVPR 2022) — Masked autoencoders for self-supervised pretraining

## Self-Supervised / Contrastive Learning
- SimCLR (Chen et al., ICML 2020) — Contrastive learning framework
- MoCo v1/v2 (He et al., CVPR 2020) — Momentum contrast
- BYOL (Grill et al., NeurIPS 2020) — Bootstrap without negatives
- DINO (Caron et al., ICCV 2021) — Self-distillation for self-supervised ViT

## Medical Imaging
- U-Net variants: 3D U-Net, V-Net, Attention U-Net
- nnU-Net (Isensee et al., Nature Methods 2021) — Self-configuring segmentation
- TransUNet (Chen et al., 2021) — Transformer + U-Net hybrid
- For specific modalities: search "[organ] [modality] segmentation" and "[disease] detection [modality]"

## Remote Sensing
- Oriented object detection: R3Det, S2ANet, Oriented R-CNN
- Small object detection in aerial images
- Change detection methods
- Hyperspectral image classification

## Evolution Timeline (Key Turning Points)

```
2012: AlexNet — deep learning enters vision
2015: FCN + U-Net — end-to-end dense prediction
2016: ResNet — residual learning enables deep networks
2017: Transformer (Vaswani et al.) — attention mechanism
2018: DeepLabV3+ — atrous spatial pyramid pooling matures
2020: ViT + DETR — transformers enter vision
2021: Swin Transformer — hierarchical vision transformers
2022: ConvNeXt + MAE — CNNs survive, self-supervision matures
2023: Segment Anything (SAM) — foundation models for vision
2024: Vision Mamba — state-space models challenge transformers
```

## Research Direction Guidance

- **If your work focuses on efficiency**: Start with MobileNet, ShuffleNet, EfficientNet for CNNs; FastViT, MobileViT for transformers.
- **If your work focuses on accuracy**: Start with ConvNeXt, SwinV2, ViT-G for classification; DINO, Mask2Former for detection/segmentation.
- **If your work focuses on self-supervision**: Start with SimCLR, MoCo, BYOL, MAE, DINOv2.
- **If your work focuses on few-shot/domain adaptation**: Search separately for "few-shot [task]" and "domain adaptation [task]."

Use these seed directions to initiate API searches via `literature/scripts/search_literature.py`. The seed map provides the "classic" anchor; the API provides the "recent SOTA" extension.
