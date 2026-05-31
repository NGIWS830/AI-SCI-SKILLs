# Literature Search Strategies

## Query Layers (Search in This Order)

1. **Problem-defining classics**: `task name classic paper`, `task benchmark survey`, `foundational method task`.
2. **Method-family papers**: `method family task`, `transformer segmentation`, `contrastive learning retrieval`, etc.
3. **Recent SOTA**: `task state of the art 2024 2025 2026`, `benchmark leaderboard paper`.
4. **Dataset/benchmark**: `dataset name paper`, `benchmark name dataset split metric`.
5. **Gap evidence**: `task limitation`, `small object detection scale variation`, `long document qa limitation`, `domain shift segmentation`.

## Concrete Query Templates

### For Vision Tasks
```
"[task] [method_family]" — broad, high recall
"[task] benchmark survey" — to find survey papers and leaderboards
"[specific_technique] for [task]" — narrow, high precision
"[dataset_name] [task] benchmark" — dataset papers
"[task] [challenge_type]" — gap evidence (e.g., "semantic segmentation boundary error", "small object detection scale")
```

### For NLP Tasks
```
"[task] state of the art" — SOTA papers
"[model_architecture] [task]" — method papers (e.g., "BERT named entity recognition")
"[task] dataset benchmark" — dataset papers
"[task] limitation [specific_issue]" — gap evidence (e.g., "long document summarization hallucination")
"[task] evaluation metric" — metrics and evaluation papers
```

### For Multimodal Tasks
```
"[modality1]-[modality2] [task]" — broad (e.g., "vision-language retrieval")
"[model_name] [task]" — specific model (e.g., "CLIP image-text retrieval")
"cross-modal [mechanism]" — technique-focused (e.g., "cross-modal attention alignment")
"[benchmark_name] multimodal" — dataset papers
```

### Boolean Operator Patterns
```
"[term1] AND [term2]" — both must appear
"[term1] OR [term2]" — either can appear
"[term1] AND ([term2] OR [term3])" — combine with grouping
"[term1] -[excluded_term]" — exclude (for removing noise; not all APIs support this)
```

## Venue-Specific Search Strategies

| Domain | Key Venues to Search | Query Additions |
|--------|---------------------|-----------------|
| CV | CVPR, ICCV, ECCV, TPAMI, IJCV | Papers on arXiv cs.CV are often CV venue preprints |
| NLP | ACL, EMNLP, NAACL, TACL, CL | ACL Anthology is comprehensive for NLP |
| ML | NeurIPS, ICML, ICLR, JMLR, TMLR | Search for the method family, not just the task |
| Multimodal | CVPR, NeurIPS, ACL, ECCV, EMNLP | Cross-disciplinary — search both CV and NLP venues |
| Medical AI | MICCAI, TMI, MIA, MedIA | May have separate indexing; PubMed is complementary |
| Robotics | ICRA, IROS, CoRL, RSS | DBLP coverage is good for these |

## Query Expansion Methodology

Given a seed query (e.g., "boundary refinement semantic segmentation"):

1. **Synonym generation**: Replace key terms with synonyms.
   - "boundary" → "edge", "contour", "border"
   - "refinement" → "improvement", "enhancement", "correction"
   - "semantic segmentation" → "dense prediction", "pixel-wise classification"

2. **Abbreviation handling**: Include both full form and abbreviation.
   - "boundary refinement (BR)" or "semantic segmentation (SS)"

3. **Hyponym inclusion**: Replace specific terms with broader ones.
   - "boundary refinement" → "structured edge detection"
   - "semantic segmentation" → "scene parsing", "image understanding"

4. **Year qualification** (for recent SOTA):
   - Add "2024 2025 2026" to focus on recent work
   - Add "recent advances" for survey-style results

## Source Priorities

- Official proceedings and publisher pages (most reliable metadata)
- arXiv with venue version cross-check (up-to-date but possibly unreviewed)
- ACL Anthology for NLP (authoritative for ACL venues)
- IEEE/ACM/Springer/Elsevier official pages for SCI/CS venues
- PubMed for biomedical and medical imaging work
- CrossRef or Semantic Scholar for metadata verification
- DBLP for CS venue verification and author disambiguation

## Recency

For AI research, "latest" should normally include papers from the past 12-24 months plus influential preprints. Always verify the current date and publication status when possible. Preprints on arXiv should be checked for subsequent peer-reviewed publication — if a preprint was later published at a venue, cite the venue version.
