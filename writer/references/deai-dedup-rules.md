# De-AI & Deduplication Rules

## Purpose

Two-part quality control applied after drafting and polishing:
1. **De-AI**: Remove formulaic, generic, or hollow phrases that signal AI-generated text — in both Chinese and English.
2. **Dedup**: Detect and eliminate duplicated content across sections.

---

## Part 1: De-AI — 去 AI 味

### What Is "AI Flavor"?

LLM-generated academic text tends to contain recognizable patterns:
- **Generic framing**: Opening sentences that restate well-known facts without adding specificity.
- **Filler transitions**: Overused connectors that pad text without advancing the argument.
- **Hollow praise**: Vague positive adjectives ("effective", "powerful", "promising") without evidence.
- **Over-explanation**: Explaining basic concepts that the target audience already knows.
- **Formulaic structure**: Every paragraph following the exact same sentence pattern.

The goal is NOT to make the text sound less polished — it's to make it sound like a human expert wrote it.

### English: AI-Flavor Phrases to Avoid

#### Generic Openers (BAD)
These opening phrases are hallmarks of AI-generated academic text:

| AI Phrase | Why It's Bad | Better Approach |
|-----------|-------------|-----------------|
| In recent years, there has been growing interest in... | Every paper says this; it says nothing specific. | Start with the concrete problem or application. |
| With the rapid development of deep learning... | Generic and uninformative. | Name the specific development relevant to this work. |
| The field of X has witnessed remarkable progress... | Hollow praise. | Cite specific breakthroughs with references. |
| In the era of big data / AI / deep learning... | Cliché. | Delete entirely; start with the problem. |
| To the best of our knowledge... | Overused hedge. | Use only once if truly needed, otherwise delete. |
| It is widely recognized that... | Usually false. | Either cite evidence or delete. |

#### Filler Connectors (Overused)
These are fine in moderation — but AI overuses them. If >2 appear in a section, restructure:

| Overused | Acceptable Frequency |
|----------|---------------------|
| Moreover / Furthermore | Max 1-2 per section |
| In addition | Max 1 per section |
| It is worth noting that | Delete — just state the point |
| Specifically / In particular | Max 1-2 per section |
| Notably / Importantly | Max 1 per section |
| On the other hand | Use only for genuine contrast |
| In other words | Use only when genuinely rephrasing a complex idea |

#### Hollow Adjectives (Replace with Evidence)

| Hollow | Replace With |
|--------|-------------|
| a powerful framework | a framework that achieves [X] on [benchmark] |
| an effective approach | an approach that improves [metric] by [Y] |
| a promising direction | (describe the specific potential with evidence) |
| comprehensive experiments | experiments on [N] datasets with [M] baselines |
| extensive evaluation | evaluation across [specific conditions] |
| a novel architecture | (describe the architecture — the novelty should be self-evident) |
| state-of-the-art performance | [metric] of [value] on [benchmark], matching/outperforming [named baseline] |

#### Formulaic Concluding Sentences (BAD)
Every paragraph does not need a concluding sentence:

| AI Pattern | Fix |
|-----------|-----|
| "These results demonstrate the effectiveness of our approach." | Delete. The results speak for themselves. |
| "This highlights the importance of X in Y." | Delete. If not obvious, the evidence was missing. |
| "These findings provide valuable insights into..." | Be specific: what insight? Or delete. |
| "Our work opens up several avenues for future research." | List the specific avenues, or delete. |

#### Over-explanation of Basics (Condescending)
Do not explain concepts that the target audience (SCI reviewers) already knows:

| Explain → Remove or Shorten |
|------------------------------|
| Deep learning is a subset of machine learning that uses neural networks with multiple layers... | Remove. Reviewers know this. |
| Convolutional neural networks (CNNs) are widely used for image processing tasks... | Keep only if directly relevant to the contribution. |
| The attention mechanism allows the model to focus on relevant parts of the input... | Remove. Common knowledge since 2017. |
| Transformers have become the dominant architecture in NLP... | Keep only if paper is about an alternative to transformers. |

---

### Chinese: AI-Flavor 套话 to Avoid

#### 万能开头 (BAD)

| AI 套话 | 为什么不好 | 替代方式 |
|---------|-----------|---------|
| 近年来，随着深度学习技术的飞速发展... | 每篇AI生成论文都这样开头。 | 直接描述具体问题和应用场景。 |
| 随着人工智能技术的不断进步... | 空洞无信息。 | 引用与本工作直接相关的具体进展。 |
| 在当今大数据时代... | 陈词滥调。 | 删除，直接切入问题。 |
| 近年来，XX领域取得了长足的进步... | 无具体内容。 | 引用2-3个里程碑工作并说明进展。 |

#### 万能结尾 (BAD)

| AI 套话 | 为什么不好 | 替代方式 |
|---------|-----------|---------|
| 综上所述，本文提出的方法有效解决了... | 公式化总结。 | 具体重述方法做了什么，实验证明了什么。 |
| 实验结果表明，我们的方法具有良好的性能... | 没有具体数值。 | 报告具体指标：在[数据集]上达到[值]，优于[基线] |
| 未来的工作将围绕以下几个方面展开... | 泛泛而谈。 | 列出1-2个具体、可执行的未来方向，或不写。 |
| 本文的研究为相关领域提供了新的思路... | 空话。 | 删除或用具体贡献替代。 |

#### 冗余连接词 (Overused)

| 中文套话 | 处理方式 |
|---------|---------|
| 值得注意的是 / 值得一提的是 | 删除，直接陈述内容 |
| 此外 / 另外 / 同时 | 每节最多1-2次 |
| 不仅如此 / 更重要的是 | 只在有真正递进关系时使用 |
| 换句话说 / 也就是说 | 只在确实需要换说法解释时使用 |
| 总体而言 / 总的来说 | 每篇文章最多1次（结论段） |

#### 空洞修饰语 → 删除或替换

| 空洞 | 替换为 |
|------|--------|
| 强大的性能 | 在[数据集]上达到了[X]（具体数值） |
| 有效的方法 | 使[指标]提升了[Y]的方法 |
| 充分的实验 | 在[N]个数据集上与[M]个基线进行了对比实验 |
| 良好的效果 | [指标]从[A]提升至[B] |
| 较为优秀 | 在所列方法中排名第[K] |
| 令人满意的结果 | 删除，直接报告结果 |
| 达到国际先进水平 | 在[基准]上的性能[具体值]，与[SOTA方法]相当 |

#### 过度解释基础知识 → 删除

如果目标读者是SCI审稿人，不需要解释的概念：

| 不需要解释的概念（除非是你的核心贡献） |
|------------------------------------------|
| 深度学习的定义和分类 |
| CNN、RNN、Transformer 的基本原理 |
| 注意力机制的定义 |
| 什么是 ResNet / BERT / ViT |
| 什么是 ImageNet / COCO / GLUE 数据集 |
| 什么是准确率 / 召回率 / F1 |
| 什么是交叉熵损失 / SGD / Adam |
| 什么是过拟合 / 正则化 / dropout |

**规则**：如果一个概念出现在任何深度学习入门教材中，不要在论文正文中解释它。

---

## Part 2: Deduplication — 去重

### Core Principle

**Each fact should appear in detail in exactly ONE section.**

Different sections may *reference* the same fact at different levels of detail:
- **Mention** (1 sentence): Refer to a finding established elsewhere.
- **Detail** (full exposition): The one place where the fact is fully described with evidence.

### Section Content Boundary Rules

| Content | Primary Section | May Be Briefly Referenced In |
|---------|----------------|------------------------------|
| Method design & architecture | III. Proposed Method | Abstract (6 sentences, First/Second/Finally structure), Introduction (1-2 sentences) |
| Experiment setup | IV.A. Datasets and Implementation Details | — |
| Main results | IV.B. Comparison with SOTA | Abstract (1 sentence, sentence 9), Introduction (contribution bullets), Conclusion |
| Ablation findings | IV.C. Ablation Study | Abstract (optionally), Conclusion |
| Efficiency data | IV.D. Efficiency Analysis | — |
| Problem motivation | I. Introduction (detailed) | Abstract (1 sentence, sentence 1) |
| Background & gap | I. Introduction (detailed) | — |
| Literature positioning | II. Related Work (detailed) | Introduction (brief citation of key gaps) |

### Duplication Patterns to Catch

#### Type 1: Method Repeated in Introduction
**BAD**: Introduction paragraph 4 repeats the full method pipeline with all module names and details → exactly the same content appears in Section III.

**Rule**: Introduction should give a 2-3 sentence *teaser* of the method (WHAT it does + core intuition), not the HOW. Leave module names, formulas, and detailed descriptions for Section III.

#### Type 2: Results Repeated in Conclusion
**BAD**: Conclusion copies results paragraphs from Section IV with identical wording and numbers.

**Rule**: Conclusion should *distill* the most important findings, not re-list every number. Mention 1-2 key metrics; refer readers to the Experiments section for details.

#### Type 3: Abstract ≈ Introduction Paragraph 1
**BAD**: The abstract's background sentence is nearly identical to the introduction's first sentence.

**Rule**: The abstract should be self-contained but should not copy-paste from the Introduction. Write the abstract last, synthesizing fresh phrasing.

#### Type 4: Related Work Describes at Wrong Level
**BAD**: A paper discussed in Related Work is described again in full detail in the Method section.

**Rule**: In Related Work, describe what others did and how you differ (1-3 sentences per paper). In Method, describe only YOUR method — do not re-explain prior methods.

#### Type 5: Contribution Bullets = Results Paragraphs
**BAD**: Introduction contribution bullets repeat the exact sentences from the Experiment Results section.

**Rule**: Contribution bullets should summarize the contribution TYPE (e.g., "a lightweight module for X that achieves Y"), while Results paragraphs provide the full evidence.

#### Type 6: Abstract Method Sentences ≈ Section III Sentences
**BAD**: The abstract's 6 method sentences (First/Second/Finally) copy or near-copy sentences from Section III (Proposed Method).

**Rule**: The abstract's method sentences should describe WHAT each component does and WHY it works at a conceptual level. Section III describes HOW in full detail (architectures, formulas, dimensions). Write the abstract's method sentences first as a high-level sketch, then expand each into a full subsection in Section III — never the reverse.

### Dedup Self-Scan Procedure

After writing the complete draft, run this scan:

1. **Sentence-level dedup**: Search for any sentence that appears (near-identically) in two different sections. Flag and remove from the less appropriate section.
2. **Number-level dedup**: List every numeric metric value in the paper. For each, note which sections it appears in. If a metric appears in >3 sections (e.g., Abstract, Introduction, Results, Conclusion), keep it only in Abstract, Results, and optionally Conclusion.
3. **Paragraph-level dedup**: Read the *first sentence* of every paragraph in sequence. If two paragraphs start with near-identical topic sentences, merge or restructure.
4. **Terminology dedup**: Check that each technical concept uses exactly one term throughout. See `ai-terminology-glossary.md`.

### Section Content Checklist

Use this to verify each section contains only what it should:

**Abstract** (should contain):
- [ ] Problem context (1 sentence)
- [ ] Gap with "because" clause (1 sentence)
- [ ] Method — First component + why it works (2 sentences)
- [ ] Method — Second component + why it works (2 sentences)
- [ ] Method — Third innovation or key design choice + why it matters (2 sentences)
- [ ] Key evidence — specific numbers with dataset + metric + value (1 sentence)
- [ ] Implication (1 sentence, optional)
- [ ] Total: exactly 10 sentences. English: 180-250 words (target 210). Chinese: 200-280 characters (target 250).

Should NOT contain:
- [ ] Method implementation details
- [ ] Citations
- [ ] Future work
- [ ] Any sentence that appears verbatim in another section

**Introduction** (should contain):
- [ ] Problem & importance (para 1)
- [ ] Current progress (para 2)
- [ ] Remaining gap with specific reason (para 3)
- [ ] Method teaser + intuition (para 4)
- [ ] Contribution bullets (para 5)

Should NOT contain:
- [ ] Implementation details (hyperparameters, training recipes)
- [ ] Detailed results tables or long lists of numbers
- [ ] Related Work laundry list

**Method** (should contain):
- [ ] Architecture overview (subsection A)
- [ ] Per-module design: input → process → output → rationale (subsections B-D)
- [ ] Loss function formulation

Should NOT contain:
- [ ] Experiment results
- [ ] Comparison to baselines
- [ ] Repetition of Introduction's motivation

**Experiments** (should contain):
- [ ] Datasets and implementation details (subsection A)
- [ ] Main results comparison (subsection B)
- [ ] Ablation study (subsection C)
- [ ] Efficiency analysis (subsection D)
- [ ] Qualitative analysis (subsection E)

Should NOT contain:
- [ ] Method design rationale (belongs in Method)
- [ ] Literature review (belongs in Related Work)
- [ ] Broad motivation (belongs in Introduction)

**Conclusion** (should contain):
- [ ] Restated problem and method summary (1-2 sentences)
- [ ] Key findings (1-2 most important results)
- [ ] 1-2 specific future work directions

Should NOT contain:
- [ ] New claims not in Experiments
- [ ] New citations
- [ ] Detailed method description
- [ ] Text copied verbatim from Introduction or Abstract
