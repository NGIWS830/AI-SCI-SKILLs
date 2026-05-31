# Literature Matrix Template

## Template

```markdown
| Category | Paper | Year | Venue | Main Idea | Relation to Our Work | Use in Paper | Verified |
|---|---:|---|---:|---|---|---|---|
| Classic |  |  |  |  | background | Introduction |  |
| Method family |  |  |  |  | method contrast | Related Work |  |
| Recent SOTA |  |  |  |  | baseline/gap | Related Work/Experiments |  |
| Dataset |  |  |  |  | benchmark | Experiments |  |
| Gap evidence |  |  |  |  | motivation | Introduction |  |
```

## Column Guidance

### Category
One of: `Classic / Foundational`, `Method Family`, `Recent SOTA`, `Dataset / Benchmark`, `Gap Evidence`, `Theory / Analysis`, `Survey / Review`

### Paper
Full paper title. Use the official title from the proceedings/journal, not arXiv working title if they differ.

### Year
Publication year of the peer-reviewed version. For arXiv-only papers, use arXiv submission year and mark venue as "arXiv preprint."

### Venue
Conference acronym (CVPR, NeurIPS, ACL, ICCV, ICML) or journal abbreviation (TPAMI, TIP, JMLR). Use standard abbreviations consistently.

### Main Idea
One sentence: what the paper does and its key contribution. Not a copy of the abstract — your synthesis of what matters for your paper. 

Examples:
- Good: "Proposes boundary refinement via direction-aware convolution; plug-and-play for any segmentation model."
- Bad: "Presents a novel approach to improve segmentation boundaries using deep learning."

### Relation to Our Work
Precise relationship from one of these categories:
- `direct competitor (same task + method family)`
- `method inspiration (different task, similar technique)`
- `baseline comparison` — we compare against this paper's results
- `dataset source` — we use their dataset/benchmark
- `gap evidence` — this paper demonstrates the limitation we address
- `background` — foundational work we build upon
- `orthogonal` — related but not directly comparable

### Use in Paper
Which section and for what purpose. Examples:
- `Introduction para 2 — representative method`
- `Related Work, Theme A — method-family literature`
- `Experiments Table 1 — SOTA baseline`
- `Method III-B — adapter design inspiration`

### Verified
One of:
- `✓ confirmed (DOI + arXiv)` — metadata confirmed from multiple sources
- `~ single source` — verified from one source only
- `✗ unverified [CITATION NEEDED]` — needs verification before finalizing

## How to Fill the Matrix

1. **Start with categories**: Determine which categories are relevant for your paper.
2. **Fill from seed maps**: Use the seed map files (cv/nlp/multimodal-classic-papers.md) to populate classic/foundational papers.
3. **Search for SOTA**: Run `search_literature.py` to find recent and competitive papers.
4. **Identify gaps**: Searches for limitations and failure cases populate the gap evidence rows.
5. **Verify everything**: Run `verify_citations.py` before finalizing any row.
6. **Map to sections**: Once the matrix is complete, the "Use in Paper" column becomes the outline for your Related Work section.
