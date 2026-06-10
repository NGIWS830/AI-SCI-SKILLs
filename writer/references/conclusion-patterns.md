# Conclusion Patterns

## Recommended Conclusion Structure

This is the **preferred** structure. Exactly two paragraphs, no more, no less.

```
## V 结论

[第一段：全文总结 — 3-5 句。重述问题 → 重述方法核心思路 → 总结关键实验结果（带数字）]

[第二段：不足与未来展望 — 2-4 句。指出当前方法的 1-2 个局限 → 提出具体的改进方向或拓展思路]
```

### Paragraph 1: 全文总结

> 本文针对[任务]中[具体问题]的挑战，提出了[方法名称]。[方法名称]
> 通过[核心机制—1-2句]，实现了[关键能力]。在[数据集]上的实验结果表明，
> [方法名称]在[关键指标]上达到[值]，较[最强基线]提升了[Δ]个百分点。
> 消融实验进一步验证了[组件A]和[组件B]对最终性能的关键贡献。

### Paragraph 2: 不足与未来展望

> 尽管[方法名称]在[任务]上取得了[效果描述]，其仍存在以下不足：
> 首先，[具体局限1]，这限制了其在[场景]中的适用性。
> 其次，[具体局限2，可选]。未来工作可从以下方向展开：
> (1) [具体改进方向1]；(2) [具体改进方向2]。此外，将[方法名称]
> 拓展至[其他任务/领域]也是一个值得探索的方向。

### Key Rules

1. **恰好两段**，不多不少。不用小标题拆分。
2. **第一段 = 总结**：问题 → 方法 → 关键结果（带数字），不引入新内容。
3. **第二段 = 不足 + 展望**：先承认局限（要具体，不能泛泛说"还有改进空间"），再给可操作的未来方向。
4. **不带新引用**：结论中不出现前文未引用过的文献。
5. **不带新声称**：所有结论必须在前文（方法、实验）中有对应证据。
6. **不重复摘要**：结论比摘要更具体（有数字），语气更收束（不展望过多）。
7. **未来方向要具体可执行**，避免"未来还有很多工作要做"这类空洞表述。

---

## Three Alternative Conclusion Structures (for special cases)

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
- "This paper has presented [Method], a [brief_description] that [core_mechanism]."
- "This paper proposed [Method], which addresses [problem] by [key_innovation]."
- "[Method] is proposed to tackle the challenge of [specific_problem] in [task]."

### Summary of Findings
- "Experiments on [datasets] demonstrated that [Method] achieves [key_result_1] and [key_result_2]."
- "Our results show that [core_insight], as evidenced by [specific_finding]."
- "Ablation studies confirmed that [component] contributes [delta] to overall performance."
- "Compared to existing [method_family] approaches, [Method] offers [advantage_1] and [advantage_2]."

### Implications
- "These findings suggest that [design_principle] is effective for [task]."
- "The success of [component] indicates that [broader_insight]."

### Limitations (if supported by evidence)
- "A limitation of this work is [specific_limitation], which future work will address by [direction]."
- "[Method] currently assumes [assumption], which may not hold in [scenario]."
- "Our evaluation is limited to [datasets/domains]. Extending to [other_domains] is an important next step."

### Future Work
- "Future work could explore [direction_1] and [direction_2]."
- "Extending [Method] to [related_task] is a natural next step."
- "Future work will investigate [open_question] in follow-up work."
- "The [component/module] proposed here may also benefit [other_task]. This exploration is left to future work."

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

[Restate method] This paper proposed Structure-Aware Boundary Refinement (SABR),
a plug-and-play module that improves boundary quality through directional
consistency modeling. SABR designs a Directional Consistency Module
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
