# Literature Synthesis Guide

## From Matrix to Narrative

A filled literature matrix is raw data. Converting it to prose requires synthesis,
not summarization. The difference:

- **Summarization**: listing what each paper did (the "laundry list" pattern)
- **Synthesis**: identifying patterns, tensions, and evolution across papers,
  then organizing them into a logical argument

## The Synthesis Process

### Step 1: Theme Extraction

Read the matrix's "Category" and "Relation" columns. Group papers into 3-5 themes.
A theme is NOT the same as a category — it's a narrative unit:

| Category in Matrix | Becomes Theme |
|-------------------|---------------|
| Method-family A + Method-family B | "The Shift from Global to Fine-Grained Alignment" |
| Gap evidence × 2 | "The Remaining Challenge: Query-Dependent Attention" |
| Foundational × 3 | "Vision-Language Pretraining: A New Foundation" |

**Rule**: Each theme should contain 2-4 papers. If a theme has 1 paper, merge it.
If it has 6+, split it into sub-themes.

### Step 2: Identify the Narrative Arc

For EACH theme, answer:

1. **What's the core idea?** One sentence that captures what all papers in this theme share.
2. **What's the evolution?** How did the approach change over time? (chronological)
   - "First, [earliest paper] established that..."
   - "Then, [middle paper] improved this by..."
   - "More recently, [latest paper] showed that..."
3. **What's the tension?** What disagreement or trade-off exists?
   - "While [method A] achieves [X], it sacrifices [Y]..."
   - "The key unresolved question is whether [X] or [Y] is more important..."
4. **What's the gap?** What do ALL papers in this theme miss?
   - "However, all these approaches share a common limitation: [gap]."
   - "Critically, none of these methods address [specific problem]."

### Step 3: Build the Argument Chain

The themes must connect logically. Typical patterns:

**Pattern A: Escalating Problem**
Theme 1 (established baseline) → Theme 2 (improved but revealed new problem) →
Theme 3 (the unresolved gap we address)

**Pattern B: Converging Evidence**
Theme 1 (one approach) → Theme 2 (complementary approach) →
Theme 3 (both point to the same limitation)

**Pattern C: Paradigm Shift**
Theme 1 (old paradigm) → Theme 2 (transitional work) →
Theme 3 (new paradigm we contribute to)

### Step 4: Map to Introduction Paragraphs

| Introduction Para | What It Needs | Where It Comes From |
|------------------|---------------|---------------------|
| Para 1: Context | Why this task matters | Project brief + task description |
| Para 2: Current Progress | 2-3 method families, their achievements | Themes with "method-family" papers |
| Para 3: The Gap | What ALL prior work misses + WHY | Gap evidence papers + synthesis of limitations |
| Para 4: Our Method | Core mechanism teaser | Project brief method description |
| Para 5: Contributions | 3-4 bullets with evidence | Project brief + experiment results |

**Critical rule for Para 2**: Do NOT list papers. Describe paradigms.
- BAD: "CLIP [1] proposed... BLIP [2] extended... ALBEF [3] introduced..."
- GOOD: "Global alignment methods (CLIP, BLIP, ALBEF) encode images and text
  into single vectors via dual-tower encoders pretrained on web-scale data.
  These methods achieve strong zero-shot performance but compress fine-grained
  visual information into a single representation."

### Step 5: Map to Related Work Sections

Each theme becomes one subsection. The structure within each subsection:

1. **Topic sentence**: What this line of work is about (1 sentence)
2. **Representative papers**: 2-3 papers with brief description + key finding
3. **Limitation statement**: What this line of work does NOT address
4. **Transition to our work**: How we differ / what we do instead

```
[Theme A: Vision-Language Pretraining]

Contrastive language-image pretraining, pioneered by CLIP [1], has established
a new paradigm for cross-modal retrieval. These dual-tower models encode images
and text independently, then match them via cosine similarity in a shared
embedding space. BLIP [2] extended this with guided language modeling, and
ALBEF [3] introduced an "align before fuse" strategy. While these methods excel
at coarse-grained retrieval and benefit from web-scale training, their global
pooling compresses all visual details into a single vector — an information
bottleneck that limits performance on queries requiring fine-grained
discrimination, such as distinguishing between similar objects with different
attributes. Our method retains the pretrained dual-tower backbone but builds
fine-grained alignment modules on top, preserving both efficiency and
discriminative capability.
```

### Step 6: Check Logical Flow

After drafting, verify:

1. **Theme order is logical**: Does each theme naturally lead to the next?
   If you can swap two themes without breaking the argument, the order is wrong.

2. **Gap is specific**: The gap statement must contain a "because" clause.
   "Existing methods are limited" → rejected.
   "Existing methods are limited because they assume X, which fails when Y" → accepted.

3. **Every cited paper has a purpose**: No citation stuffing.
   Each citation answers: "Why is this paper here?"

4. **Transitions connect themes**: Not "Another approach is..." but
   "In contrast to global methods that sacrifice detail for efficiency,
   fine-grained approaches explicitly model..."

5. **Our method is clearly differentiated**: After reading Related Work,
   a reader should know exactly what distinguishes your work from ALL prior work.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Laundry list: "Author A [1] proposed X. Author B [2] proposed Y. Author C [3] proposed Z." | Synthesize: "Methods in this family share [core mechanism] but differ in [key design choice]." |
| Vague gap: "Few works have studied X." | Specific gap: "Existing methods fail to handle X because Y is assumed constant, which does not hold when Z." |
| Disconnected themes: each subsection is isolated | Use transition sentences: "A second line of work addresses [B] from a different angle..." |
| Overclaiming our novelty: "No prior work has ever..." | Accurate differentiation: "Unlike [specific method] which uses [A], we use [B] because [reason]." |
| Uneven depth: 3 paragraphs on one theme, 1 sentence on another | Balance: each major theme gets comparable treatment. |
