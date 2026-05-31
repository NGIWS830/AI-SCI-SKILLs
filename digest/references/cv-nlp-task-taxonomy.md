# CV/NLP/AI Task Taxonomy

## Computer Vision

### Image-Level Tasks
- **Image classification**: Assign a label to an image. Single-label / multi-label / fine-grained.
  - Metrics: Accuracy, Top-5 Accuracy, F1 (multi-label)
  - Benchmarks: ImageNet, CIFAR-10/100, iNaturalist
- **Image generation**: Generate images from noise / text / other images.
  - Metrics: FID, IS, CLIP Score
  - Benchmarks: MS-COCO (text-to-image), LSUN, ImageNet (class-conditional)
- **Image restoration/enhancement**: Denoising, super-resolution, deblurring, inpainting.
  - Metrics: PSNR, SSIM, LPIPS

### Region-Level Tasks
- **Object detection**: Localize and classify objects in an image.
  - Metrics: mAP (AP@50, AP@75, AP@[.5:.95]), AR
  - Benchmarks: MS-COCO, Pascal VOC, OpenImages
- **Instance segmentation**: Segment each object instance.
  - Metrics: mask mAP, box mAP
  - Benchmarks: MS-COCO, Cityscapes (instance), LVIS

### Pixel-Level Tasks
- **Semantic segmentation**: Assign a class to every pixel.
  - Metrics: mIoU, Pixel Accuracy, Dice
  - Benchmarks: Cityscapes, ADE20K, Pascal Context, COCO-Stuff
- **Panoptic segmentation**: Semantic + instance segmentation combined.
  - Metrics: PQ, SQ, RQ
  - Benchmarks: Cityscapes, MS-COCO Panoptic

### Video Tasks
- **Video classification / action recognition**: What action occurs in a video clip.
  - Benchmarks: Kinetics-400/600/700, Something-Something, UCF-101
- **Video object segmentation**: Segment objects across frames.
  - Benchmarks: DAVIS, YouTube-VOS

### Specialized Domains
- **Medical image analysis**: Diagnosis, segmentation, detection in medical scans.
  - Benchmarks: MIMIC-CXR, CheXpert, BraTS, LiTS, ISIC
- **Remote sensing**: Satellite/aerial image analysis, land cover classification, change detection.
  - Benchmarks: DOTA, xView, DeepGlobe, SpaceNet

### Learning Paradigms
- Few-shot learning, domain adaptation, continual learning, self-supervised learning, semi-supervised learning.

---

## Natural Language Processing

### Classification & Labeling
- **Text classification**: Topic, sentiment, stance, intent classification.
  - Metrics: Accuracy, F1, AUC
  - Benchmarks: SST-2, AG News, TREC, Yahoo Answers
- **Named Entity Recognition (NER)**: Identify entities in text.
  - Metrics: Span F1, Entity F1
  - Benchmarks: CoNLL-2003, OntoNotes 5.0, WNUT
- **Relation extraction**: Identify relations between entities.
  - Benchmarks: TACRED, SemEval, DocRED

### Generation Tasks
- **Machine translation**: Translate between languages.
  - Metrics: BLEU, COMET, chrF
  - Benchmarks: WMT, IWSLT
- **Summarization**: Condense text into shorter form.
  - Metrics: ROUGE-1/2/L, BERTScore
  - Benchmarks: CNN/DailyMail, XSum, arXiv/PubMed
- **Question answering**: Answer questions given context.
  - Metrics: Exact Match, F1
  - Benchmarks: SQuAD, Natural Questions, TriviaQA, HotpotQA

### Understanding & Reasoning
- **Natural language inference (NLI)**: Determine if a hypothesis follows from a premise.
  - Benchmarks: SNLI, MNLI, ANLI
- **Dialogue systems**: Task-oriented and open-domain conversation.
  - Benchmarks: MultiWOZ, PersonaChat, DailyDialog

### LLM-Specific
- **Instruction tuning**: Training models to follow instructions.
- **Alignment (RLHF/DPO)**: Aligning models with human preferences.
  - Benchmarks: AlpacaEval, MT-Bench, Chatbot Arena
- **Long-context understanding**: Processing documents beyond 4K-8K tokens.
  - Benchmarks: LongBench, L-Eval, Needle-in-a-Haystack

---

## Multimodal Learning

- **Vision-language pretraining**: CLIP-style contrastive, BLIP-style generative, LLaVA-style instruction-tuned.
  - Benchmarks: MS-COCO, Flickr30k, ARO, Winoground
- **Image-text retrieval**: Retrieve images from text queries and vice versa.
  - Metrics: Recall@K (R@1, R@5, R@10)
  - Benchmarks: MS-COCO, Flickr30k
- **Visual question answering (VQA)**.
  - Benchmarks: VQA v2, GQA, OK-VQA, TextVQA
- **Document understanding**: Extract information from document images.
  - Benchmarks: FUNSD, CORD, DocVQA
- **Video-language modeling**: Video captioning, retrieval, QA.
- **Medical multimodal**: Chest X-ray report generation, medical VQA.
- **Multimodal instruction tuning**: LLaVA, InstructBLIP-style models.

---

## Common Method Families

| Family | Typical Components | Common For |
|--------|-------------------|------------|
| CNN | Conv2d, Pooling, BN, Residual connections | Image classification, detection, segmentation |
| RNN/LSTM/GRU | Sequential processing, hidden states | (Declining: replaced by Transformers for most NLP) |
| Transformer | Self-attention, FFN, LayerNorm, positional encoding | NLP, vision (ViT), multimodal |
| Vision Transformer (ViT) | Patch embedding, transformer encoder | Image classification, segmentation, detection |
| Contrastive learning | Paired encoders, similarity loss, temperature | Self-supervised learning, retrieval, multimodal |
| Diffusion models | Forward/reverse process, U-Net denoiser | Image generation, video generation |
| Graph neural networks | Message passing, graph convolution | Molecular modeling, social networks, scene graphs |
| Retrieval-Augmented Generation | Retriever + generator, knowledge integration | QA, factuality, long-tail knowledge |
| LoRA / Adapters | Low-rank decomposition, parameter-efficient tuning | LLM fine-tuning |
| Mixture of Experts | Sparse activation, routing, load balancing | Large-scale training efficiency |

## Typical Baselines per Task

| Task | Expected Baselines |
|------|-------------------|
| Image classification (CNN era) | ResNet-50/101/152, DenseNet-121, EfficientNet-B0-B7 |
| Image classification (ViT era) | ViT-B/L, Swin-T/S/B, ConvNeXt-T/S/B |
| Object detection | Faster R-CNN, YOLOv5/v8, DETR, Deformable DETR, DINO |
| Semantic segmentation | FCN, DeepLabV3+, PSPNet, SegFormer, Mask2Former |
| NLP classification | BERT-base/large, RoBERTa-base/large, DeBERTa |
| Text generation | GPT-2, T5, BART, LLaMA-family, GPT-family |
| Image-text retrieval | CLIP, BLIP, ALBEF, BEiT-3 |
| VQA | LXMERT, UNITER, ViLT, BLIP-2, LLaVA |

These are search directions, not verifiable citations. Always verify specific papers before citing.
