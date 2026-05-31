# Conclusion Patterns

## Three Conclusion Structures

### 1. Restatement-Heavy (Default)
```
[Restate problem — 1 sentence]
[Restate method — 1-2 sentences, focus on what's novel]
[Summarize key findings — 2-3 sentences with numbers]
[Future work — 1-2 sentences]
```
Best for: Most papers. Safe, clear, covers all bases.

### 2. Forward-Looking
```
[Brief method restatement — 1 sentence]
[What this work enables — 2-3 sentences]
[Concrete future directions — 2-3 sentences]
```
Best for: Papers that open a new direction or release a significant resource.

### 3. Limitation-First
```
[Brief method restatement — 1 sentence]
[Honest limitations — 1-2 sentences]
[Key contributions despite limitations — 2 sentences]
[How limitations will be addressed in future work]
```
Best for: Papers with clear limitations that reviewers will notice. Proactively addressing them builds trust.

---

## Sentence Templates per Component

### Summary of Method
- "We have presented [Method], a [brief_description] that [core_mechanism]."
- "This paper introduced [Method], which addresses [problem] by [key_innovation]."
- "We proposed [Method] to tackle the challenge of [specific_problem] in [task]."

### Summary of Findings
- "Experiments on [datasets] demonstrated that [Method] achieves [key_result_1] and [key_result_2]."
- "Our results show that [core_insight], as evidenced by [specific_finding]."
- "Ablation studies confirmed that [component] contributes [delta] to overall performance."
- "Compared to existing [method_family] approaches, [Method] offers [advantage_1] and [advantage_2]."

### Implications
- "These findings suggest that [design_principle] is effective for [task]."
- "The success of [component] indicates that [broader_insight]."

### Limitations (if supported by evidence)
- "A limitation of this work is [specific_limitation], which we plan to address by [direction]."
- "[Method] currently assumes [assumption], which may not hold in [scenario]."
- "Our evaluation is limited to [datasets/domains]. Extending to [other_domains] is an important next step."

### Future Work
- "Future work could explore [direction_1] and [direction_2]."
- "Extending [Method] to [related_task] is a natural next step."
- "We plan to investigate [open_question] in follow-up work."
- "The [component/module] proposed here may also benefit [other_task]. We leave this exploration to future work."

**Future work anti-patterns:**
- Vague: "Much work remains to be done." → Too generic.
- Aspirational without grounding: "We plan to achieve human-level performance." → Overclaim.
- Excuse-making: "With more computational resources, better results could be obtained." → Avoid.

**Good future work:**
- Specific: "Extending [Method] to video segmentation via temporal consistency constraints."
- Grounded: "The current method uses a fixed number of direction templates (4). Adaptive direction selection is worth exploring."
- Actionable: "Our released codebase provides a baseline for future comparisons on [benchmark]."

---

## Complete Annotated Example Conclusion

```
[Restate problem] Semantic segmentation in safety-critical applications
demands precise object boundaries, yet existing methods struggle to
delineate fine structures.

[Restate method] We proposed Structure-Aware Boundary Refinement (SABR),
a plug-and-play module that improves boundary quality through directional
consistency modeling. SABR introduces a Directional Consistency Module
that distinguishes structural from textural boundaries by exploiting
their geometric continuity.

[Summarize findings] Experiments on Cityscapes and Mapillary Vistas
demonstrated consistent improvements in boundary-sensitive metrics
(+2.3 F1 points on Cityscapes), with the largest gains on thin-structure
categories. Ablation studies confirmed that both the directional
convolution and the consistency loss contribute to the overall improvement,
with the latter contributing 1.6 of the 2.3 point gain.

[Limitation + future work] A current limitation is that SABR uses a fixed
set of four directional templates, which may not capture all structural
orientations in scenes with complex geometry (e.g., curved roads).
Future work could explore adaptive direction selection and extend SABR
beyond segmentation to other dense prediction tasks such as depth
estimation and surface normal prediction.

[Closing] The code and pretrained models are publicly available to
facilitate further research in boundary-aware segmentation.
```

---

## Conclusion Quality Self-Check

1. **No new claims**: Are there any claims, citations, or results not already presented in the body?
2. **No new citations**: Does the conclusion cite any paper not already cited earlier?
3. **Specific numbers**: Does the conclusion restate key results with specific numbers?
4. **Future work specificity**: Are future directions concrete and grounded in the paper's findings?
5. **Limitation honesty**: If there are obvious limitations, are they acknowledged?
6. **Length**: 3-5 paragraphs. Shorter than introduction, longer than abstract.
