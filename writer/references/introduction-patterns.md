# Introduction Patterns

## Three Alternative Introduction Structures

Choose the structure that best fits your paper type. Most AI papers use Problem-First.

### 1. Problem-First (Default for Most AI Papers)

```
Para 1: Task importance + real-world applications
Para 2: Current progress — 2-3 representative method families
Para 3: Remaining gap — what existing methods fail to do, and WHY
Para 4: Proposed method — core mechanism + intuition
Para 5: Contributions — evidence-grounded bullet list
```

Best for: papers with a clear gap in existing methods (most common).

### 2. Method-First (For Papers Where the Method Is the Story)

```
Para 1: Core technical challenge in [task]
Para 2: Why existing paradigms fail at this specific challenge
Para 3: Proposed method — lead with the key insight, then elaborate
Para 4: How the method connects to broader research landscape
Para 5: Contributions — emphasize methodological novelty
```

Best for: papers introducing a fundamentally new architecture or training paradigm.

### 3. Application-Driven (For Applied / Domain-Specific Papers)

```
Para 1: Real-world problem in [domain] (medical, industrial, scientific)
Para 2: Why existing AI methods are insufficient for this domain
Para 3: Domain-specific requirements and constraints
Para 4: Proposed method — how it addresses domain constraints
Para 5: Contributions — emphasize practical impact alongside technical novelty
```

Best for: medical imaging, remote sensing, scientific ML, industrial applications.

---

## Sentence Template Bank

### Paragraph 1: Context / Background (Task Importance)

Choose 2-3 templates that fit your task:

**Problem statement openers:**
- "[Task] plays a critical role in [domain], underpinning applications ranging from [app1] to [app2]."
- "The ability to accurately [task_verb] is essential for [downstream_application]."
- "[Task] has emerged as a fundamental challenge in [field], with broad implications for [area1] and [area2]."
- "Advances in [task] have enabled breakthroughs in [application], where [specific_requirement] is paramount."

**Trend-driven openers:**
- "The rapid progress of [technology] has fueled significant advances in [task] over the past [time_range]."
- "With the proliferation of [data_type/modality], [task] has become increasingly important for [reason]."
- "Recent years have witnessed remarkable progress in [task], driven largely by advances in [technique]."

**Application-driven openers:**
- "In [real-world domain], practitioners routinely face the challenge of [task_description]."
- "[Domain] applications such as [example1] and [example2] critically depend on accurate [task]."
- "Deploying [AI system] in [domain] requires [task] that is [requirement1] and [requirement2]."

### Paragraph 2: Current Progress (Representative Methods)

**Method-family summary openers:**
- "A prominent line of work approaches [task] via [method_family_A], where [core_mechanism]."
- "An alternative paradigm, exemplified by [method_family_B], instead [core_mechanism]."
- "More recently, [method_family_C] has shown promising results by [core_mechanism]."
- "The current landscape of [task] methods can be broadly categorized into [N] families: [family1], [family2], and [family3]."

**Transition between families:**
- "While [family_A] methods excel at [strength], they typically [limitation]."
- "In contrast to [family_A], [family_B] methods [key_difference]."
- "A complementary direction, pursued by [authors] among others, focuses on [aspect]."
- "Parallel to these developments, [community] has explored [alternative_approach]."

**Specific example introduction:**
- "For instance, [Method] ([Author], [Year]) [core_idea_in_one_clause]."
- "A representative example is [Method], which [mechanism] to achieve [result]."

### Paragraph 3: Gap Statement (Remaining Problem)

The gap paragraph is the most important paragraph in the introduction. A weak gap makes for a weak paper.

**Precise gap templates:**
- "Despite these advances, [specific_capability] remains underexplored. Existing methods [what_they_do], but they fail to [what_they_cannot_do], because [reason]."
- "A key limitation of existing [method_family] approaches is that they [specific_behavior], which leads to [consequence] in [scenario]."
- "Current methods address [aspect_A] effectively, but they neglect [aspect_B], which is essential when [condition]."
- "While [method_family] has proven effective for [setting_A], its performance degrades significantly in [setting_B] due to [underlying_reason]."
- "Existing approaches implicitly assume [assumption]. However, in practice, [why_assumption_fails], resulting in [failure_mode]."

**Gap strength calibration:**
| Strength | Template | When to Use |
|----------|----------|-------------|
| Strong gap | "Existing methods fundamentally fail when [condition] because [mechanism]. This is not a minor limitation — it renders them unusable for [important_scenario]." | Multiple papers explicitly acknowledge this limitation; you have evidence that a core design choice is the cause |
| Moderate gap | "Current approaches exhibit a consistent weakness in [scenario]: they [specific_behavior], which limits their applicability to [domain]." | The limitation is observable but prior work hasn't characterized it precisely |
| Weak gap | "[Aspect] has received relatively little attention in the [task] literature. Most work focuses on [other_aspect]." | A true unexplored area, but be careful — "understudied" needs a justification for WHY it matters now |

**Anti-patterns (avoid these):**
- "Few studies have investigated [X]." → Too vague. Why should anyone care?
- "To the best of our knowledge, no prior work has..." → Aggressive claim; hard to verify.
- "[X] is still an open problem." → Too broad. What specific sub-problem?

### Paragraph 4: Method Teaser (What You Propose)

**Method introduction templates:**
- "To address this gap, we propose [Method], which [core_mechanism_in_one_sentence]. Unlike [existing_approach], [Method] [key_difference]."
- "We introduce [Method], a [type_of_contribution] that [core_mechanism]. The key insight is that [intuition]."
- "In this work, we take a different approach: rather than [conventional_wisdom], we [counterintuitive_insight], which enables [benefit]."

**Intuition / design rationale:**
- "The intuition behind [Method] is straightforward: [one_sentence_explanation]."
- "Our design is motivated by the observation that [empirical_observation], which suggests that [design_principle]."
- "The core idea is to [action] so that [desired_outcome], which in turn [downstream_benefit]."

**Distinguish WHAT vs. WHY:**
- WHAT: "We introduce a [module_name] that [computation]." (save details for Method section)
- WHY: "This design enables [capability], because [reason]." (tease the rationale here)

### Paragraph 5: Contributions (Bullet List)

**Contribution bullet patterns:**

Pattern A — Method + Experiment + Resource:
```
Our main contributions are:
1. We propose [Method], a [brief_description] that [key_innovation]. (→ Section III)
2. We demonstrate through extensive experiments on [datasets] that [Method] achieves
   [key_result_1] and [key_result_2]. (→ Section IV, Tables X-Y)
3. We release [code/dataset/benchmark] to facilitate future research in [area]. (→ URL)
```

Pattern B — Method-only heavy paper:
```
Our main contributions are:
1. We identify [insight/observation] as a key bottleneck in [task]. (→ Section I, III-A)
2. Building on this insight, we propose [Method], which introduces [module_1] and
   [module_2] to address [challenge]. (→ Section III-B, III-C)
3. We provide theoretical analysis showing that [property] holds under [conditions]. (→ Section III-D)
4. Experiments on [datasets] validate that [Method] [key_result]. (→ Section IV)
```

Pattern C — Systems/Resource paper:
```
Our main contributions are:
1. We present [System/Dataset], a [scale/description]. (→ Section III)
2. Using [System/Dataset], we conduct a systematic study of [research_question],
   revealing [key_finding_1] and [key_finding_2]. (→ Section IV)
3. We establish [benchmark_result] as a strong baseline for future comparisons. (→ Section V)
```

**Evidence mapping rule:** Every contribution bullet must cross-reference a specific section, table, or figure. If you cannot point to the evidence, demote the bullet to "We also explore..." or remove it.

**Anti-pattern:** Bullets that only say "We propose [X]" without "We find/demonstrate/show that [Y]". A contribution is not the act of proposing — it is the value created by the proposal.

---

## Venue-Specific Introduction Conventions

### CVPR / ICCV / ECCV (Computer Vision)
- **Style**: Application vignette in para 1, visual motivation emphasized.
- **Contribution framing**: Generalization across datasets is highly valued. "On [Dataset A], [Method] improves [metric] by [X]. On [Dataset B] without any fine-tuning, [Method] achieves [Y]."
- **Length**: ~1 page (conference), ~1.5 pages (journal TPAMI)
- **What reviewers look for**: Is this a real vision problem? Does the gap motivate a vision-specific solution? Are the datasets standard?

### NeurIPS / ICML / ICLR (Machine Learning)
- **Style**: More problem formalism and theoretical motivation. Para 1 often starts with a problem statement rather than an application.
- **Contribution framing**: Principle-driven. "We prove that..." / "We show theoretically that..." / "We provide insight into why..."
- **Length**: ~1 page conference, tight prose expected.
- **What reviewers look for**: Is the problem well-defined? Is the method principled? Is there an insight beyond engineering?

### ACL / EMNLP / NAACL (Natural Language Processing)
- **Style**: Linguistic motivation in para 1, task definition precision.
- **Contribution framing**: Task-specific results + analysis. "On [benchmark], [Method] achieves [score], a [X] point improvement."
- **Length**: ~1 page conference.
- **What reviewers look for**: Is the linguistic phenomenon well-characterized? Is the task definition precise? Are the evaluation metrics appropriate?

### AAAI / IJCAI (General AI)
- **Style**: Accessible motivation. Assumes broader AI audience — minimize field-specific jargon in the introduction.
- **Contribution framing**: Balance technical and practical. Broader impact often expected.
- **Length**: ~1 page conference.
- **What reviewers look for**: Is this accessible to a general AI audience? Does it advance AI broadly?

### Journal: TPAMI / TIP / TNNLS / TMLR
- **Style**: Longer, more comprehensive. Can spend more words on literature coverage in the introduction itself.
- **Contribution framing**: Deeper analysis, more ablation, theoretical underpinning.
- **Length**: 1.5-2 pages for introduction is normal.
- **What reviewers look for**: Depth, comprehensiveness, maturity of the contribution.

---

## Annotated Example Introduction

### Chinese Draft (Semantic Segmentation — Boundary Refinement Paper)

```
第1段 (Context):
语义分割是计算机视觉中的核心任务之一，其目标是为图像中的每个像素分配语义
类别标签。该技术在自动驾驶、医学影像分析和遥感图像解译等领域具有广泛的
应用价值。在这些应用中，精确的目标边界分割对于下游决策至关重要——例如，
自动驾驶系统需要精确的道路边界来规划安全行驶路径，医学诊断依赖准确的
病灶边界来评估病变范围。

[注释] 第1段功能: 确立任务重要性和应用场景。从"语义分割"这个宽泛任务
逐步聚焦到"边界精度"这个具体关注点。自动驾驶和医学影像两个应用覆盖了
"安全关键"和"诊断关键"两类场景。

第2段 (Current Progress):
近年来，基于深度学习的方法在语义分割任务上取得了显著进展。以FCN、DeepLab
系列和SegFormer为代表的方法通过多尺度特征融合，有效提升了整体分割精度。
在边界优化方面，现有工作主要沿着两条技术路线展开：一类方法（如SegFix、
BPR）通过后处理步骤修正边界预测；另一类方法（如GSCNN、PIDNet）设计专门
的边界分支来学习边界感知特征。这些方法在多个基准数据集上取得了有竞争力
的结果。

[注释] 第2段功能: 总结现有方法，按技术路线分类。为第3段的gap做铺垫：
后处理方法"分离了边界学习与主任务学习"，边界分支方法"无法区分结构边界
和纹理边界"。

第3段 (Gap):
然而，现有方法面临一个共性挑战：它们将所有边界像素等同对待，未能区分
具有几何连续性的结构边界（如道路、杆状物）和随机的纹理边界（如树叶、
草地）。在实际场景中，结构边界的精确分割对于自动驾驶等应用尤为关键，
而纹理边界的微小偏差通常可以容忍。现有方法要么平等地优化所有边界
（导致结构边界精度不足），要么依赖手工设计的几何先验（缺乏对多样化
场景的适应性）。

[注释] 第3段功能: 精确阐述gap。关键要素：(1) 具体指出什么被忽视了
（结构边界 vs 纹理边界的区分）；(2) 解释为什么重要（自动驾驶等应用）；
(3) 说明现有方法为什么无法解决（平等对待 or 手工先验）。这是一个
"strong gap"——有明确的失效机制和重要的实际后果。

第4段 (Method Teaser):
针对上述问题，本文提出结构感知边界优化方法SABR（Structure-Aware
Boundary Refinement）。SABR的核心创新在于引入方向一致性模块
（Directional Consistency Module），该模块通过显式建模边界像素的
空间连续性，使网络能够区分具有几何结构的边界和随机纹理边界。SABR
可即插即用地集成到任何编码器-解码器架构的分割网络中，无需修改主干网络。

[注释] 第4段功能: 方法简介。只讲WHAT（方向一致性模块 + 即插即用）
和WHY（显式建模空间连续性来区分边界类型），不讲HOW（具体实现留到
Method section）。

第5段 (Contributions):
本文的主要贡献如下：
(1) 我们揭示了现有边界优化方法的一个根本局限——无法区分结构边界和
    纹理边界——并通过定量实验验证了这一观察（Section III-A）。
(2) 我们提出方向一致性损失（Directional Consistency Loss），一种
    新的正则化项，显式约束边界预测的几何连续性（Section III-C）。
(3) 在Cityscapes和Mapillary Vistas数据集上的实验表明，SABR在边界
    敏感指标上显著优于现有方法（边界F1提升2.3点），同时在标准mIoU
    指标上也取得有竞争力的结果（Section IV-B, Table 2）。
(4) 我们开源了代码和预训练模型，以促进边界感知分割研究。

[注释] 第5段功能: 贡献列表。每个贡献都有证据指向（Section + Table）。
贡献(1)是分析性贡献，(2)是方法贡献，(3)是实验贡献，(4)是资源贡献。
```

### English Rendering (Annotated)

```
1. Introduction

Semantic segmentation — the task of assigning a semantic category label to
every pixel in an image — is a core problem in computer vision, with
wide-ranging applications in autonomous driving, medical image analysis,
and remote sensing interpretation. In each of these domains, precise object
boundaries are critical for downstream decision-making: an autonomous vehicle
requires accurate road boundaries to plan safe trajectories; medical diagnosis
relies on precise lesion boundaries for severity assessment.

[Annotation] Para 1: Context. Narrows from broad "semantic segmentation" to
specific concern "boundary precision." Two application domains illustrate
both safety-critical and diagnostic-critical use cases.

Recent years have seen remarkable progress in semantic segmentation, driven
by deep learning. Architectures such as FCN, the DeepLab family, and more
recently SegFormer have steadily improved overall segmentation accuracy
through multi-scale feature fusion. For boundary quality specifically,
existing work follows two main directions: post-processing methods (e.g.,
SegFix, BPR) that refine boundary predictions after the initial segmentation;
and boundary-branch methods (e.g., GSCNN, PIDNet) that incorporate a dedicated
boundary stream to learn boundary-aware features. Both paradigms have achieved
competitive results on standard benchmarks.

[Annotation] Para 2: Current progress. Organizes existing methods into two
technical families, setting up the gap: post-hoc methods separate boundary
learning from the main task; boundary-branch methods cannot distinguish
structural from textural edges.

However, a common challenge limits these methods: they treat all boundary
pixels equally, failing to distinguish between geometrically continuous
structural boundaries (e.g., roads, poles, building edges) and stochastic
texture boundaries (e.g., foliage, grass, clouds). In practice, precise
delineation of structural boundaries is critical for applications like
autonomous driving, while small deviations in texture boundaries are
typically tolerable. Existing methods either optimize all boundaries
uniformly (sacrificing structural boundary precision) or rely on
hand-crafted geometric priors (lacking adaptability to diverse scenes).

[Annotation] Para 3: Gap. Key elements: (1) specific problem identified
(structural vs. texture boundary distinction); (2) explains why it matters
(practical application consequences); (3) explains why existing methods fail
(uniform treatment or hand-crafted priors). This is a "strong gap" with a
clear failure mechanism.

To address this gap, we propose Structure-Aware Boundary Refinement (SABR).
The key innovation is a Directional Consistency Module that explicitly models
the spatial continuity of boundary pixels, enabling the network to distinguish
geometrically structured boundaries from random texture edges. SABR is designed
as a plug-and-play module that integrates into any encoder-decoder segmentation
architecture without modifying the backbone.

[Annotation] Para 4: Method teaser. Only WHAT and WHY — not HOW.

Our main contributions are:
1. We identify a fundamental limitation of existing boundary refinement
   methods — the inability to distinguish structural from textural boundaries
   — and validate this observation through quantitative analysis (Section III-A).
2. We propose the Directional Consistency Loss, a novel regularization term
   that explicitly enforces geometric continuity of boundary predictions
   (Section III-C).
3. Experiments on Cityscapes and Mapillary Vistas demonstrate that SABR
   substantially outperforms existing methods on boundary-sensitive metrics
   (+2.3 points boundary F1) while remaining competitive on standard mIoU
   (Section IV-B, Table 2).
4. We release code and pretrained models to facilitate future research in
   boundary-aware segmentation.

[Annotation] Para 5: Contributions. Each bullet has an evidence pointer.
```

---

## Introduction Quality Self-Check

Answer these 8 questions before finalizing:

1. **Specificity**: Does the gap paragraph contain a "because" clause explaining the root cause, not just the symptom?
2. **Evidence grounding**: Does every contribution bullet trace to a specific section/table/figure?
3. **Scope honesty**: Is the contribution scope aligned with Stage 3 evidence strength? No upgrade from "moderate" to "strong".
4. **Application relevance**: Does para 1 establish real-world importance without overclaiming societal impact?
5. **Method teaser precision**: Does para 4 tell WHAT and WHY without diving into HOW (which belongs in Section III)?
6. **Citation balance**: Are citations spread across relevant method families, not just self-citations?
7. **Transition logic**: Can you trace a clear logical chain from para 1 through para 5? If a reader stops at para 3, do they know exactly what the paper will address?
8. **Length**: Conference paper intro should be ~1 page; journal intro 1.5-2 pages. Cut if significantly over.
