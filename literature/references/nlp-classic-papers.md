# NLP Seed Map

Use this file only to generate search directions. Verify every citation before final use.

## Sequence Modeling (Pre-Transformer)
- RNN, LSTM (Hochreiter & Schmidhuber, 1997), GRU (Cho et al., EMNLP 2014)
- Seq2Seq with attention (Bahdanau et al., ICLR 2015; Luong et al., EMNLP 2015)
- ELMo (Peters et al., NAACL 2018) — Deep contextualized word representations

## Transformer Era
- Transformer (Vaswani et al., NeurIPS 2017) — The foundational architecture
- BERT (Devlin et al., NAACL 2019) — Bidirectional pretraining
- GPT family: GPT-1 (2018), GPT-2 (2019), GPT-3 (NeurIPS 2020), GPT-4 (2023)
- RoBERTa (Liu et al., 2019) — Better BERT training
- T5 (Raffel et al., JMLR 2020) — Text-to-text framework
- BART (Lewis et al., ACL 2020) — Denoising seq2seq pretraining
- DeBERTa (He et al., ICLR 2021) — Disentangled attention

## Task-Specific Milestones
- **NER**: BiLSTM-CRF → BERT-NER → few-shot NER
- **QA**: SQuAD → BERT-QA → T5-QA → RAG → long-context QA
- **Summarization**: Pointer-Generator → BART → PEGASUS → LLM-based
- **MT**: Seq2Seq → Transformer → Multilingual models (mBART, NLLB)
- **Sentiment/Classification**: fastText → BERT → few-shot with LLMs

## Retrieval and RAG
- Dense retrieval: DPR (Karpukhin et al., EMNLP 2020), ColBERT (Khattab & Zaharia, SIGIR 2020)
- RAG (Lewis et al., NeurIPS 2020) — Retrieval-augmented generation
- FiD (Izacard & Grave, 2020) — Fusion-in-Decoder
- Atlas (Izacard et al., 2022) — Retrieval-augmented LM
- Recent: REPLUG, Self-RAG, RAPTOR, FLARE

## LLMs and Alignment
- Instruction tuning: FLAN (Wei et al., ICLR 2022), T0 (Sanh et al., 2021)
- RLHF: InstructGPT (Ouyang et al., NeurIPS 2022), constitutional AI
- DPO (Rafailov et al., NeurIPS 2023) — Direct preference optimization
- Parameter-efficient tuning: LoRA (Hu et al., ICLR 2022), adapters, prefix tuning
- Reasoning: Chain-of-thought (Wei et al., NeurIPS 2022), Tree-of-thought, ReAct

## Evaluation
- Robustness: CheckList, TextFlint, adversarial evaluation
- Factuality: TruthfulQA, FActScore, HaluEval
- Hallucination detection and mitigation
- Long-context evaluation: LongBench, L-Eval, SCROLLS

## Evolution Timeline

```
2013: word2vec — distributed word representations
2015: Seq2Seq + Attention — neural MT becomes viable
2017: Transformer — the architecture that changed NLP
2018: ELMo + BERT — pretrained contextual embeddings
2019: GPT-2 + RoBERTa — scaling and training improvements
2020: GPT-3 + T5 + RAG — scaling to 175B and retrieval
2022: ChatGPT + InstructGPT — instruction following and RLHF
2023: Llama + DPO + CoT — open models and alignment techniques
2024: Long-context + multi-agent — scaling context and collaboration
```

## Research Direction Guidance

- **If your work focuses on efficiency**: Start with DistilBERT, ALBERT for compression; LoRA, QLoRA for PEFT.
- **If your work focuses on factuality**: Start with RAG, Self-RAG, truthfulness benchmarks.
- **If your work focuses on reasoning**: Start with chain-of-thought, tree-of-thought, ReAct.
- **If your work focuses on alignment**: Start with RLHF, DPO, constitutional AI.
- **If your work focuses on multilingual**: Start with mBERT, XLM-R, NLLB, multilingual LLMs.

Use these seed directions to initiate API searches via `literature/scripts/search_literature.py`.
