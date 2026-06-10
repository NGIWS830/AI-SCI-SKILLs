# English Polishing Rules

## Default Style

Use conservative SCI journal style: clear, precise, formal, and not overdecorated. Every sentence should carry information. If a sentence can be deleted without losing content, delete it.

## Polishing Modes

- **Conservative**: Fix grammar errors, improve clarity, smooth awkward phrasing. Minimal change.
- **Academic rewriting**: Restructure sentences and paragraphs for better flow while preserving content.
- **IEEE style**: Concise and technical. Short sentences. Minimal rhetorical flourish.
- **AI conference style** (NeurIPS/ICML/ICLR/CVPR): Clear problem formulation, precise claims, empirical rigor.
- **Nature-leaning style**: Stronger narrative arc, but never inflate significance claims.

---

## Section-Specific Polishing Checklists

### Abstract
- [ ] Exactly 10 sentences (2-6-2 structure)
- [ ] Sentences 3/5/7 start with "First," / "Second," / "Finally,"
- [ ] Every sentence carries unique information (no filler)
- [ ] Specific numbers present in sentence 9 (metric + dataset + value)
- [ ] No citations (abstracts rarely cite others)
- [ ] 180-250 words (target 210; count: ______)

### Introduction
- [ ] Para 1 hook is specific, not "X is important in many areas"
- [ ] Gap paragraph has a "because" clause
- [ ] Contribution bullets trace to evidence
- [ ] No HOW details leaked from Method section

### Related Work
- [ ] Organized by theme, not author/year
- [ ] Each theme ends with comparison to our method
- [ ] No laundry-list sentences ("Author A [1] did X. Author B [2] did Y.")
- [ ] Verbs are in present or present perfect, not simple past

### Method
- [ ] Every symbol in every equation explained in prose
- [ ] Dimensions annotated on first use
- [ ] Present tense throughout
- [ ] Design rationale (WHY) accompanies every module description (WHAT)
- [ ] No result numbers in Method section

### Experiments
- [ ] Metric direction stated for every metric
- [ ] Standard deviations or confidence intervals reported
- [ ] Past tense for what was done ("models were trained/evaluated")
- [ ] Present tense for tables/figures ("Table 1 reports/shows")
- [ ] Best results bold, second-best underlined

### Conclusion
- [ ] No new claims, citations, or results
- [ ] Future work is specific (not "more research is needed")
- [ ] Limitations acknowledged if significant
- [ ] Numbers present, but interpreted (not just restated)

---

## Sentence Variety Patterns

**Third-Person Sentence Variety:** Avoid monotonous sentence starts. Vary between subject-led ("The proposed method..."), passive construction ("Features are extracted via..."), and result-led ("Table X reports...") patterns:

- "This paper proposes..." → Vary with "A [module] is proposed that..."
- "The proposed method achieves..." → Vary with "As shown in Table X, [Method] achieves..."
- "The results indicate that..." → Vary with "Experiments confirm that..."
- "Subsequently, [step] is performed..." → Vary with "The next stage applies..."

**Anti-pattern:** More than 3 consecutive sentences starting with the same subject (e.g., "The proposed method... The proposed method... The proposed method...").

**Sentence length variety:**
- Mix lengths: a short sentence (10-15 words) followed by longer analytical ones (25-40 words) creates rhythm.
- If all sentences in a paragraph are 25-35 words, reading becomes monotonous.
- A 5-word sentence after three 30-word sentences delivers emphasis.

**Paragraph length:**
- No 1-sentence paragraphs (under-developed idea).
- No >12-sentence paragraphs (reader loses thread). Split into two.

---

## Cohesion Device Library

### Addition
- furthermore, moreover, in addition, additionally, also, besides

### Contrast / Concession
- however, nevertheless, nonetheless, in contrast, conversely, on the other hand, whereas, although, despite, while

### Cause-Effect
- therefore, thus, hence, consequently, as a result, accordingly, for this reason

### Exemplification
- for instance, for example, specifically, in particular, to illustrate, notably

### Emphasis
- indeed, in fact, notably, importantly, it is worth noting that, crucially

### Sequence / Enumeration
- first, second, third, finally, subsequently, next, then, lastly

### Summary / Conclusion
- in summary, overall, in conclusion, taken together, in short

**Usage rule:** Don't force a connector where the logical relationship is already obvious. "However" at the start of every other sentence is as bad as none. Use connectors when the logical relationship would otherwise be ambiguous.

---

## Academic Register Guidelines

### Informal → Formal Pairs

| Informal | Formal |
|----------|--------|
| a lot of, lots of | a substantial number of, considerable, many |
| big, huge, large | substantial, considerable, pronounced |
| get, got | obtain, achieve, attain |
| find out | determine, identify, discover |
| look at, look into | examine, investigate, explore |
| seem, looks like | appear, suggest |
| really, very | (use precise numbers instead, or "particularly", "notably") |
| kind of, sort of | (delete) or "type of" |
| thing | aspect, factor, element, component |
| good (performance) | strong, competitive, state-of-the-art (if verified) |
| bad (performance) | poor, suboptimal, degraded |

### Common Academic Writing Issues

1. **Hedging overuse:** "may possibly somewhat improve" → Choose one hedging word. "may improve" or "tends to improve."
2. **Dangling modifiers:** "After training, the model performed well." (The model didn't train itself.) → "After training for 100 epochs, we evaluated the model."
3. **Subject-verb distance:** "The method, which was trained on three datasets with varying characteristics and annotation quality, achieves..." → "We trained the method on three datasets with varying characteristics and annotation quality. It achieves..."
4. **Nominalization overload:** "The implementation of the feature extraction by the model..." → "The model extracts features by..."
5. **Missing "that":** "We found the method improves..." → "We found that the method improves..."

---

## Never (Hard Constraints)

- Strengthen claims without corresponding evidence
- Add unsupported "state-of-the-art", "novel", "significant", "first", or "comprehensive"
- Change metric values or dataset names
- Remove caveats, uncertainty markers, or hedging
- Add new citations, experiments, or methods
- Delete or alter `[CITATION NEEDED]` or `AUTHOR_INPUT_NEEDED` markers
- Change "suggests" to "demonstrates" or "proves" without evidence
- Replace precise numbers with vague adjectives
