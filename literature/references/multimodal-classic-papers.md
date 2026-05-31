# Multimodal Seed Map

Use this file only to generate search directions. Verify every citation before final use.

## Image-Text Pretraining
- CLIP (Radford et al., ICML 2021) — Contrastive language-image pretraining at scale
- ALIGN (Jia et al., ICML 2021) — Billion-scale noisy image-text pretraining
- BLIP (Li et al., ICML 2022) — Bootstrapping language-image pretraining
- BLIP-2 (Li et al., ICML 2023) — Q-Former bridge between vision encoder and LLM
- SigLIP (Zhai et al., ICCV 2023) — Sigmoid loss for vision-language pretraining
- EVA-CLIP (Fang et al., 2023) — Scaling CLIP training

## Vision-Language Models (VLMs)
- Flamingo (Alayrac et al., NeurIPS 2022) — Few-shot visual understanding
- LLaVA family (Liu et al., 2023-2024) — Visual instruction tuning
- InstructBLIP (Dai et al., NeurIPS 2023) — Instruction-tuned VLM
- MiniGPT-4 (Zhu et al., 2023) — Aligning vision encoder with LLM
- Qwen-VL, DeepSeek-VL, InternVL — Open-source VLMs (2024)

## Image-Text Retrieval
- VSE++ (Faghri et al., BMVC 2018) — Hard negative mining for retrieval
- SCAN (Lee et al., ECCV 2018) — Stacked cross-attention
- ViLBERT (Lu et al., NeurIPS 2019) — Vision-and-language BERT
- UNITER (Chen et al., ECCV 2020) — Unified vision-language pretraining
- ALBEF (Li et al., NeurIPS 2021) — Align before fuse
- BEiT-3 (Wang et al., NeurIPS 2022) — Multi-way transformer

## Visual Question Answering
- VQA v2 (Goyal et al., CVPR 2017) — Balanced VQA benchmark
- LXMERT (Tan & Bansal, EMNLP 2019) — Cross-modal transformer
- GQA (Hudson & Manning, CVPR 2019) — Compositional VQA
- OK-VQA (Marino et al., CVPR 2019) — Outside-knowledge VQA
- TextVQA (Singh et al., CVPR 2019) — Text reading in VQA
- PaliGemma (Beyer et al., 2024) — Versatile VLM

## Document Understanding
- LayoutLM family (Xu et al., 2020-2022) — Document layout + text
- Donut (Kim et al., ECCV 2022) — OCR-free document understanding
- DocVQA benchmark
- FUNSD, CORD for form/key extraction

## Video-Language Learning
- VideoBERT (Sun et al., ICCV 2019) — Video + language joint modeling
- TimeSformer (Bertasius et al., ICML 2021) — Space-time attention
- VideoCLIP (Xu et al., EMNLP 2021) — Video-text contrastive learning
- Video-LLaMA, VideoChat — Video + LLM (2023-2024)

## Medical Multimodal
- Chest X-ray report generation: R2Gen, RGRG
- Medical VQA: PathVQA, VQA-RAD
- Multimodal medical foundation models: Med-PaLM, Med-Flamingo, LLaVA-Med

## Multimodal RAG
- Multimodal retrieval-augmented generation
- Document-grounded visual question answering
- Knowledge-grounded image captioning

## Evolution Timeline

```
2017: VQA v2 — balanced visual question answering
2018: Visual grounding + image-text retrieval matures
2019: ViLBERT + LXMERT — cross-modal transformers
2020: UNITER + Oscar — unified pretraining
2021: CLIP + ALIGN + ALBEF — contrastive pretraining at scale
2022: Flamingo + BLIP — bridging vision and language models
2023: LLaVA + InstructBLIP — visual instruction tuning
2024: Multimodal agents + long-form video understanding
```

## Research Direction Guidance

- **If your work focuses on retrieval**: Start with CLIP, ALBEF, BLIP for contrastive methods.
- **If your work focuses on VQA**: Start with LLaVA, BLIP-2, InstructBLIP for generative VQA.
- **If your work focuses on document understanding**: Start with LayoutLM, Donut, DocVQA.
- **If your work focuses on efficiency**: Start with ViLT, ALBEF, MobileVLM for efficient VLMs.
- **If your work focuses on instruction tuning**: Start with LLaVA, InstructBLIP for VLM instruction data.

Use these seed directions to initiate API searches via `literature/scripts/search_literature.py`.
