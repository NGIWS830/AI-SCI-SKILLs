# Related Work Patterns (Literature Stage)

This file provides the literature-stage perspective on related work. For the writer-stage patterns (sentence templates, transition libraries, annotated examples), see:

**`writer/references/related-work-patterns.md`**

## Preferred Structure (Literature Stage)

Organize by theme for the literature matrix and related work section:

```markdown
## 2. Related Work

### 2.1 Task-specific methods
Explain the task lineage and representative methods.

### 2.2 Method-family literature
Group methods by mechanism and limitation.

### 2.3 Relationship to our work
Clarify how the proposed method differs and what gap it addresses.
```

## Good Related Work Paragraph Structure

1. Opens with the theme statement.
2. Summarizes 2-3 papers together by shared characteristics.
3. Identifies a common limitation or unresolved gap.
4. Connects that gap to the current method.

## From Literature Matrix to Related Work

The literature matrix built in Stage 2 maps directly to the related work section:

| Matrix Category | Maps to Related Work Theme | Content |
|----------------|---------------------------|---------|
| Classic / Foundational | Theme 1 background | Establish the task lineage |
| Method family | Theme 1 or 2 | Group by shared mechanism |
| Recent SOTA | Theme 2 or 3 | Competitors and baselines |
| Gap evidence | Theme 3 | Papers that show the limitation you address |
| Dataset / Benchmark | Experiments section | Don't include here unless introducing the dataset |

## Avoid

- Chronological laundry lists ("[A] proposed X. [B] proposed Y. [C] proposed Z." — no grouping, no analysis).
- Unsupported "few studies have..." claims — if you haven't exhaustively searched, don't claim sparsity.
- Claiming novelty without search evidence — "Unlike all prior work..." requires a comprehensive search.
- Citing papers that were not verified — every citation in Related Work must be verified.
