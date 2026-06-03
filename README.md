<div align="center">

# AI-SCI-SKILLs

[![Version](https://img.shields.io/badge/version-v0.4.0-blue.svg)](https://github.com/NGIWS830/AI-SCI-SKILLs/releases)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Claude%20Code%20%7C%20Codex%20%7C%20Cursor%20%7C%20Any%20Agent-lightgrey.svg)
![Built with](https://img.shields.io/badge/AI%20Powered-Skill%20%7C%20Pipeline-orange.svg)

中文 | [English](README_EN.md)

</div>

---

<div align="center">

<h3><strong>一个 Skill，一次会话。原始材料 → 英文 SCI 论文终稿🚀</strong></h3>

</div>

---

AI-SCI-SKILLs 是一个以中文为先的端到端 SCI 论文写作流水线，覆盖深度学习、机器学习、计算机视觉、NLP、多模态学习及相关 AI 研究方向。


## 触发方式

### 触发关键词

对话中出现以下任意关键词时，AI Agent 会自动激活本 skill（Claude Code 原生支持自动触发；Codex、Cursor、Copilot 等可直接将 `SKILL.md` 作为上下文加载）：

`写论文` `SCI论文` `学术论文` `paper writing` `SCI paper` `manuscript` `LaTeX论文` `期刊论文` `会议论文` `投稿` `初稿` `论文写作` `写英文论文` `润色论文` `翻译论文` `学术写作` `academic writing`

### 触发语句示例

以下任意说法都能触发（不限于此）：

- "帮我写一篇 SCI 论文"
- "把这些实验数据整理成论文"
- "帮我从代码和实验表格出一篇英文论文初稿"
- "我要投 CVPR/ICCV/NeurIPS/ICML/ACL/AAAI..."
- "把这些材料写成一篇可以投稿的英文文章"
- "帮我润色这段论文"
- "把这篇中文论文翻译成英文 SCI 风格"
- "从研究笔记生成论文"
- "帮我写 paper"
- "write a paper from my research materials"

### 直接指定阶段

你也可以跳过前面阶段，直接指定：

- "帮我分析这批实验数据能支撑什么结论"（Stage 3）
- "帮我检索跨模态检索方向的文献"（Stage 2）
- "帮我把这篇中文稿润色成英文 SCI"（Stage 4d-4e）

---

## 适用场景

> **一个 skill，按需起跑。** 本表展示的是：提供不同材料 / 说不同的话，同一个 skill 会自动从对应阶段开始，无需每次都从零跑全流程。不是多个独立 skill。

| 你有的东西 | 你想要的 | 从哪开始 | 试试这样说 |
|-----------|---------|---------|-----------|
| 代码 + 实验表格 + 笔记 | 完整英文 SCI 论文 | Stage 0-4 全流程 | "帮我把这些材料写成一篇 SCI 论文"（Stage 0-4） |
| 研究项目文件夹（代码+README+配置） | 论文初稿 | Stage 0-4 全流程 | "从这个项目生成一篇英文 paper"（Stage 0-4） |
| 实验 CSV + 方法描述 | 实验结果分析和论文 | Stage 3-4 | "分析这些实验数据，写成论文的实验部分"（Stage 3-4） |
| 实验数据 + 方法描述 + 文献列表 | 英文论文 | Stage 3-4 | "我有实验表格和方法说明，帮我写论文"（Stage 3-4） |
| 已有论文 + 新实验结果 | 更新论文的实验部分 | Stage 3-4 | "把这些新实验结果更新到论文里"（Stage 3-4） |
| 中文论文初稿 | 英文 SCI 期刊投稿稿 | Stage 4d-4e | "把这篇中文论文翻译润色成英文 SCI"（Stage 4d-4e） |
| 英文初稿 | 润色 + 自审 + 模板输出 | Stage 4e-4g | "帮我润色这篇英文论文，然后套 IEEE 模板"（Stage 4e-4g） |
| 完整英文稿 | 质量检查和自批判 | Stage 4f | "帮我审查这篇论文的质量"（Stage 4f） |
| 零散笔记和想法 | 结构化研究简报 | Stage 1 | "帮我把这些研究笔记整理成论文大纲"（Stage 1） |
| 文献列表 + 研究方向 | 文献综述 / Related Work | Stage 2 | "帮我检索整理这个方向的文献"（Stage 2） |
| 完整中文论文 | LaTeX / Word 模板渲染 | Stage 4g | "把这篇文章渲染成 IEEE 格式"（Stage 4g） |

---

## 流水线

```
Stage 0: INIT   → 盘点材料，创建项目状态文件
Stage 1: DIGEST → 文件清单、深度代码分析、Jupyter 解析、依赖追踪、自动生成项目简报
Stage 2: LIT    → 文献检索（API 自动化）、AI 自动填矩阵、验证、缺口分析、叙述合成（矩阵→Introduction+Related Work）
Stage 3: EXPER  → 实验计划生成、改进计算、统计分析、可视化、叙述合成
Stage 4: WRITE  → 4a 故事线 → 4b 中文初稿 → 4c 中文润色
               → 4d 英译 → 4e 英文润色 → 4f 自批判 → 4g 模板渲染
```

支持断点续传：中断后重新加载 `SKILL.md` 并指向已有 `project-state.md` 即可继续。

---

## 架构

```
SKILL.md（根入口）
├── digest/        — 从项目材料中提取论文可用信息
│   ├── references/  — 代码阅读、任务分类、证据规则、简报模板
│   └── scripts/     — summarize_repo.py, extract_architecture.py,
│                      parse_notebooks.py, trace_dependencies.py,
│                      synthesize_brief.py
├── literature/    — 检索 → 自动填矩阵 → 验证 → 缺口分析 → 叙述合成
│   ├── references/  — 搜索策略、API 指南、引文验证、经典论文地图、
│   │                  文献合成指南（矩阵→叙事）
│   └── scripts/     — search_literature.py, auto_fill_matrix.py,
│                      verify_citations.py, analyze_citations.py,
│                      synthesize_literature.py
├── experiment/    — 分析实验并验证论点
│   ├── references/  — 指标指南、声明规则、消融写作、可复现性检查清单
│   └── scripts/     — compute_improvements.py, statistical_tests.py,
│                      result_visualizer.py, design_experiments.py,
│                      synthesize_experiments.py
├── writer/        — 中文初稿 → 润色 → 英译 → 英文润色 → 自批判
│   └── references/  — 全章节模板、中英翻译语料库、术语表、质量评分标准
├── scripts/       — 质量检查、声明-证据审计、交叉引用校验、
│                    LaTeX 编译、BibTeX 格式化、Word 渲染、
│                    审稿回复生成、论文转Slides
└── templates/     — 11 个会议/期刊模板（中英文、CV/ML/NLP/AI/遥感/
                     计算智能/图像处理）、Cover Letter
```

---

## 流水线详细机制

> 以下逐 Stage 展开操作语义：角色指令、决策树、评分标准、阈值判定、审计流程。这些是 SKILL.md 中驱动 AI Agent 行为的核心规则。

### Stage 0 — INIT：材料盘点与状态初始化

**目标**：清点用户提供的所有材料，建立追踪整个流水线的项目状态文件。

1. 询问用户：输出目录、目标期刊/会议、特殊要求。
2. 识别所有材料：代码仓库、README、配置文件、日志、实验表格（CSV/Excel）、框架图、笔记（Word/TXT/Markdown）、已有草稿、文献列表。
3. 创建 `<output_dir>/project-state.md`，包含材料清单、目标期刊、流水线进度复选框、各阶段输出占位区、缺失作者输入记录。
4. 更新状态为 `STAGE 1 | DIGEST`。

**两个核心标注规范（贯穿全流程）**：
- `AUTHOR_INPUT_NEEDED`：需要作者补充的信息（不得编造填充）
- `[CITATION NEEDED]`：未经数据库交叉验证的引用

---

### Stage 1 — DIGEST：项目消化

**目标**：从原始材料中提取论文可用的结构化事实，生成项目简报。

**5 步思维链：**

```
STEP 1: TASK IDENTIFICATION（任务识别）
→ 研究任务类型（分类/检测/分割/生成/检索/...）
→ 输入模态（图像/文本/音频/视频/多模态）
→ 输出形式（类别标签/掩码/边界框/文本/嵌入）

STEP 2: METHOD EXTRACTION（方法提取）
→ 骨干网络（ResNet/ViT/BERT/GPT/自定义）
→ 新颖模块（每个 nn.Module 子类或自定义函数）
→ 训练目标（每个损失项）
→ 推理流程（逐步描述）

STEP 3: EVIDENCE GROUNDING（证据定级）
→ HIGH: 代码/配置/笔记中直接可见（如 "使用 CrossEntropyLoss" 确认于 loss.py:42）
→ MEDIUM: 强暗示但未完全指定（如 "使用 AdamW" 仅凭配置键推断）
→ LOW: 合理推测，需作者确认

STEP 4: GAP ANALYSIS（缺口分析）
→ 声称了哪些数据集但未提供划分？
→ 提到了哪些指标但未计算值？
→ 列出了哪些基线但缺少实现细节？
→ 缺失哪些超参数？

STEP 5: CONTRIBUTION CANDIDATES（贡献候选）
→ 每组候选贡献标注：新颖性所在 + 支撑证据 + 待验证项
```

**5 个脚本链：**
```
summarize_repo.py → extract_architecture.py → parse_notebooks.py → trace_dependencies.py → synthesize_brief.py
```
`synthesize_brief.py --repo <path>` 可一键端到端运行全部 digest 流程。

**输出**：`00_project_brief.md`，包含研究任务、方法模块-证据映射表、数据流、候选贡献、缺失信息清单、论文写作风险。

**转换**：状态更新为 `STAGE 2 | LIT`。若关键信息缺失，先请用户补充再继续。

---

### Stage 2 — LIT：文献综述

**目标**：构建经过验证的文献支撑——经典基础、近年 SOTA、方法族论文、数据集论文、缺口证据。

**查询派生规则**（从 Stage 1 的任务描述和方法族中提取 3-5 个关键技术词，每个词生成 3 种查询变体）：

| 变体 | 模式 | 示例 |
|------|------|------|
| Broad | `"<task> <method_family>"` | `"text-to-image retrieval cross-modal alignment"` |
| Specific | `"<task> <specific_technique>"` | `"cross-modal retrieval contrastive learning"` |
| Gap-focused | `"<task> limitation <pain_point>"` | `"text-image retrieval fine-grained alignment"` |

**文献矩阵列含义：**

| 列 | 说明 |
|----|------|
| Relation to Our Work | 5 种分类：direct competitor / method inspiration / baseline comparison / dataset source / gap evidence |
| Use in Paper | 指定在论文中哪个章节、什么目的使用 |
| Verification | 3 级状态：✓ confirmed（DOI+arXiv）/ ~ single source / ✗ unverified |

**经典论文种子地图**：`cv-classic-papers.md` / `nlp-classic-papers.md` / `multimodal-classic-papers.md` 用于补漏——自动搜索可能遗漏的早期高影响力论文。

**文献叙述合成（NEW v0.4）**：`synthesize_literature.py` 将矩阵自动转化为 Introduction 和 Related Work 的有逻辑段落——按范式组织而非论文罗列，含主题句、论述演进、方法区分、逻辑流检查。

**脚本链**：`search_literature.py` → `auto_fill_matrix.py` → `verify_citations.py` → `analyze_citations.py` → `synthesize_literature.py`

**输出**：`02_literature_matrix.md`，包含搜索查询、文献矩阵、Related Work 主题结构、研究缺口证据、引文缺口。

**转换**：状态更新为 `STAGE 3 | EXPER`。

---

### Stage 3 — EXPER：实验分析

**目标**：将实验产物转化为有证据支撑的结果声明。

**声明强度决策树**（每条声明必须经过）：

```
Q1: 改善方向是否正确？（查 metrics-guide.md 确认 higher/lower is better）
    → 不确定则标记 AUTHOR_INPUT_NEEDED

Q2: 改善在数据集/设置间是否一致？
    → Consistent（所有数据集）→ 声明强度 = STRONG
    → Mixed（多数数据集）  → 声明强度 = MODERATE
    → Single（单个数据集）  → 声明强度 = WEAK
    → No evidence           → UNSUPPORTED — 不得声明

Q3: 改善幅度是否足够大？
    → 分类 >1pp | 检测 >1 mAP | 分割 >1 mIoU/Dice | 生成 >1 BLEU
    → 低于阈值则使用 "comparable to" / "on par with"

Q4: 混淆因素能否解释改善？
    → 不同的骨干容量？训练预算？数据预处理？
    → 若是，标注为 caveat
```

**结果段落填空模板：**
> As shown in Table [X], [Method] achieves [value] on [dataset], [direction] the strongest baseline [baseline] by [absolute] ([relative]%). On [dataset_2], [Method] achieves [value_2], a [absolute_2] improvement over [baseline_2]. These results demonstrate that [component] contributes to [capability], as evidenced by [specific_evidence].

**可视化消融设计（NEW v0.4）：**

消融实验不仅需要定量指标，还需要可视化展示每个组件如何工作。详见 `experiment/references/ablation-writing.md` 的 "Visual Ablation Analysis" 章节，覆盖 **10 种可视化类型**：

| 如果你的声明是... | 主要可视化 |
|-----|------|
| "我们的模块提升了特征质量" | t-SNE / PCA 嵌入分布 |
| "我们的模块引导注意力到正确区域" | Grad-CAM 热力图 |
| "门控机制选择性增强/抑制通道" | 通道权重分布 |
| "损失函数改善了类别可分性" | t-SNE + 轮廓系数 |
| "我们的方法更好地处理困难样本" | 错误案例对比 |
| "我们的模块加速收敛" | 训练动态曲线 |
| "注意力机制更具可解释性" | 注意力图 + Attention Rollout |
| "卷积核学到更丰富的模式" | 滤波器/卷积核可视化 |

另外还有：特征图对比、混淆矩阵差值、预测置信度分布。每张消融可视化图遵循 5 步叙述模式：提出问题 → 描述设置 → 指出关键观察 → 机理级解释 → 关联定量证据。

**5 个脚本：** `design_experiments.py`（实验计划生成）→ `compute_improvements.py`（改进计算 + Bootstrap CI）→ `statistical_tests.py`（效应量/显著性/多重比较校正/功效分析）→ `result_visualizer.py`（6 种图表）→ `synthesize_experiments.py`（叙述合成）。

**输出**：`03_experiment_analysis.md`，含分析表格列表、主要结果、基线上改善、消融发现、声明-证据映射表（含强度等级和注意事项）。

**转换**：状态更新为 `STAGE 4 | WRITE`。

---

### Stage 4a — 故事线

**目标**：起草前先提炼论文的单一科学叙事主线。

**5 要素结构：**
- **Problem**：论文回答的科学问题（一句话）
- **Gap**：先前工作未能解决的知识缺口（含 "because" 子句）
- **Method**：方法的核心机制（2-3 句，模块级）
- **Evidence**：支撑声明的 2-3 个关键实验结果
- **Contribution**：贡献声明（一句话，与证据对齐）

**5 项自检：**
1. 问题陈述是否与方法实际解决的问题匹配？
2. 缺口是否具体表述（不是 "few works study X" 而是 "existing methods fail to handle Y because Z"）？
3. 方法描述是否突出了新颖部分而非标准流程？
4. 每项贡献是否可追溯到 Stage 1 或 Stage 3 中的证据？
5. 贡献范围是否诚实——是否只声明了证据能支撑的内容？

---

### Stage 4b — 中文初稿（`05_chinese_draft.md`）

**角色指令：**
> 你现在正在撰写一篇中文学术论文初稿。目标是在形式中文语域中产出一份完整、逻辑连贯的初稿，每项事实性断言均应以项目状态文件中的证据为基础。使用 20-50 字的中短句。使用被动语态为主，避免以"我们"作主语。每段须有清晰的主题句。保留所有 `AUTHOR_INPUT_NEEDED` 和 `[CITATION NEEDED]` 标记。

**逐节指导：**

| 章节 | 结构规则 |
|------|---------|
| **Title** | 给出 3 个变体，选最具体且最不夸大的。推荐模式：`[Method Name]: [Core Mechanism] for [Task]` |
| **Abstract** | 2-6-2 结构，恰好 10 句：2 句背景/缺口 + 6 句方法（用 First/Second/Finally 串联，每对 = 声明+为什么有效）+ 2 句实验结果/结论。~250 汉字 |
| **Introduction** | 5 段：任务重要性 → 当前进展（2-3 个方法族）→ 剩余缺口（含 because 子句）→ 提出方法（核心机制 2-3 句）→ 贡献（3-4 条，每条指向证据） |
| **Related Work** | 按主题组织（来自 Stage 2），每主题 1 段：主题陈述 → 2-3 篇论文对比 → 你的方法如何不同。避免 "[Author] et al. [X] proposed..." 流水账 |
| **Method** | 大标题"方法"，开头 3-5 句总述整体框架（不设 Overview 小标题），随后三个创新点各为一个小标题。每个创新点按 动机→设计→公式/机制→作用 四段式展开，可穿插模块框架图或算法伪代码 |
| **Experiments** | 5 个子节：数据集与指标 → 实验设置 → 与最先进方法和经典方法的对比 → 消融实验（编号列表 1), 2), 3)...）→ 可视化 |
| **Conclusion** | 两段式：第一段全文总结（问题→方法→关键结果带数字），第二段不足与未来展望。不引入新引用或新声称 |

---

### Stage 4c — 中文精修（`06_chinese_polished.md`）

**角色指令：**
> 你现在正在润色一篇中文学术稿件。润色学术清晰度、逻辑流畅度和表达简洁度。目标不是让文字华丽——而是消除歧义、收紧逻辑、删除冗余、确保每段文字都有存在的价值。科学含义不可侵犯——绝不为了更好听而改动它。

**De-AI 扫描（4 类中文 AI 套话）：**
1. 万能开头（"近年来，随着...的发展"）→ 替换为具体问题陈述
2. 万能结尾（"综上所述，本文提出的方法有效..."）→ 替换为具体发现
3. 空洞修饰语（"强大的性能""良好的效果"）→ 替换为具体数字
4. 过度解释基础知识 → 删除（SCI 审稿人已懂）

**跨章节去重：**
- 方法细节仅出现在方法节，不出现在引言
- 结果仅出现在实验节，不出现在方法
- 摘要、引言、结论使用不同措辞
- 无两节共享高度相似的句子

**10 项精修清单：**

| # | 检查项 | 不良示例 | 良好示例 |
|---|--------|---------|---------|
| 1 | 删除空洞修饰语 | 该方法取得了较好的性能提升 | 该方法在Cityscapes上提升了2.3 mIoU |
| 2 | 补充缺失主语（无人称） | 使用ResNet-50作为骨干网络 | ResNet-50被用作骨干网络 |
| 3 | 拆分长句（>50字） | （60字流水句） | （两句 25-35 字） |
| 4 | 统一术语 | 注意力机制/Attention机制混用 | 统一为"注意力机制"（首次标注英文） |
| 5 | 删除冗余近义词对 | 精度和准确率均得到提升 | 精度提升了1.2个百分点（指明指标） |
| 6 | 强化弱转折 | 另外，我们还做了... | 在效率方面，进一步分析了... |
| 7 | 落地模糊声明 | 性能优于所有基线方法 | 在三个数据集上，所提方法均优于所有基线方法（Table 2） |
| 8 | 修正悬空引用 | 如图所示 | 如图3所示 |
| 9 | 对齐平行结构 | 我们提出了X，设计了Y，以及对Z进行了优化 | 提出了X，设计了Y，优化了Z |
| 10 | 声明一致性检查 | 中文"显著提升" | 确保与 Stage 3 证据强度一致 |

**逻辑流审计**：逐段边界提问——这段是否从前一段逻辑推导而来？是引入新信息还是重述？论证链是否完整？

**冗余检测**：扫描连续同义句、引言与方法中相同措辞的方法描述、结果与结论中无新增解释的重复数值。

---

### Stage 4d — 中→英转换（`07_english_draft.md`）

**角色指令：**
> 你现在正在将一篇精修后的中文学术稿件转换为英文 SCI 散文。这不是逐字翻译，而是重写：将句子从中式话题-述题模式重组为英文 SVO 模式，补充中文省略的主语，将中文体标记转换为英文时态，添加冠词（a/an/the），并全程保持学术语域。所有数字、指标值、引用标记和声明强度必须精确保留。

**时态约定：**

| 章节 | 主要时态 | 例外 |
|------|---------|------|
| Abstract | Present | Past for evaluation: "Performance was evaluated on..." |
| Introduction | Present | Past for "Previous methods struggled...", Present perfect for "Recent work has shown..." |
| Related Work | Present perfect / Present | Past for specific historical results |
| Method | Present | — |
| Experiments | Past | Present for "Table 1 reports..." |
| Conclusion | Present | Past for summarizing specific results |

**语态约定：**

| 章节 | 指导 |
|------|------|
| Abstract | 偏好被动："A novel X is proposed..." |
| Introduction | 贡献列表（Para 5）用被动/无人称："This paper presents...", "A novel X is introduced..."；前 4 段叙事可用主动。贡献条目中不要写 "We propose X" |
| Related Work | 描述现有方法用被动；区分自身用无人称："This work differs from..." |
| Method | 偏好被动："Features are extracted..."；设计理由也倾向被动："X is designed to...", "This module enables..." |
| Experiments | 偏好被动："Models were trained on..."；叙事被动："As shown in Table 1, the proposed method achieves..." |
| Conclusion | 偏好被动/无人称："This paper has presented..." |

**声明强度映射（关键条目）：**

| 中文 | 夸大英译 ✗ | 安全英译 ✓ |
|------|-----------|-----------|
| 显著提升 | significantly improves | achieves a X.X pp improvement |
| 解决了...问题 | solves the problem of... | addresses / alleviates / mitigates |
| 优于现有方法 | outperforms all existing methods | outperforms [named baselines] on [specific datasets] |
| 首次提出 | is the first to / novel | introduces / proposes（若无验证则不称 first） |
| 证明了 | proves that | demonstrates that / provides evidence that |

**5 大中→英翻译陷阱：** 话题凸显迁移（补主语）、修饰语堆叠（前置→后置）、平行结构（重复→连词归并）、零冠词→冠词、体→时态。

---

### Stage 4e — 英文精修（`08_english_polished.md`）

**角色指令：**
> 你现在正在润色一篇英文 SCI 稿件。润色：学术语域、句式多样性、衔接、精度、可读性。不得改动科学内容、不得添加无支撑声明、不得强化声明措辞。若不确定某一修改是否会改变含义，保留原文。

**De-AI 扫描（5 类英文 AI 套话）：**
1. 通用开头（"In recent years, there has been growing interest in..."）→ 具体陈述
2. 过度使用的连接词（Moreover, Furthermore, In addition）→ 每节最多 2 个
3. 空洞形容词（"powerful", "effective", "promising"）→ 具体证据或删除
4. 公式化结尾句（"These results demonstrate the effectiveness of our approach."）→ 删除
5. 过度解释基础概念（CNN、attention、transformer 基础）→ 删除

**句式多样性审计：**
- 每节 "We" 开头句若连续 >3 句 → 重组句式
- 句长分布：若整段均为 25-35 词，插入一句短句（10-15 词）
- 段长：无 1 句式段落或 >12 句式段落

**衔接手段注入（6 类）：**

| 功能 | 连接词 |
|------|--------|
| Addition | furthermore, moreover, in addition |
| Contrast | however, in contrast, conversely, whereas |
| Cause-effect | therefore, consequently, as a result, thus |
| Exemplification | for instance, specifically, in particular |
| Emphasis | notably, importantly |
| Sequence | first, second, finally, subsequently |

**学术语域检查（informal → formal）：**
"a lot of" → "substantial" / "considerable" · "big"/"huge" → "large" / "considerable" · "get" → "obtain" / "achieve" · "find out" → "determine" / "identify" · "look at" → "examine" / "investigate"

**额外检查**：扫描 `forbidden-overclaims.md` 中的英文禁用词；生成修订说明 `09_revision_notes.md`。

---

### Stage 4f — 自批判（`10_critique_report.md`）

**目的**：在宣告论文完成之前，使用质量评分标准和自动化检查进行系统性自批判。

**角色指令：**
> 你现在是这篇稿件的审稿人。采取批判、怀疑的立场。你的工作是找出每一个弱点、夸大声明、缺失引用和不精确表述。可以严厉但要公平。诚实打分——虚高分数对谁都没有好处。

**5 维度评分（1-4 分制，加权百分制）：**

| 维度 | 权重 | 评估内容 |
|------|------|---------|
| Claims-Evidence Alignment（声明-证据对齐） | **25%** | 每项事实声明是否有表/图/节引用支撑？措辞强度是否与证据匹配？ |
| Citation Completeness & Accuracy（引用完整性） | **15%** | 引用是否经 CrossRef/DBLP 验证？`[CITATION NEEDED]` 标记是否 >3？ |
| Method Description Precision（方法描述精度） | **20%** | 每模块是否覆盖输入/输出/过程/理由？符号一致？实现细节完整？ |
| Experiment Reporting Rigor（实验报告严谨性） | **25%** | 指标方向声明？标准差？基线描述？消融覆盖所有声称贡献？ |
| Language Quality（语言质量） | **15%** | 学术语域统一？术语一致？句式多样？无 AI 套话？ |

**分数三档判定：**

| 分数 | 判定 | 动作 |
|------|------|------|
| **≥ 80/100** | READY | 进入 Stage 4g 模板渲染 |
| **70-79/100** | NEEDS REVISION | 修复识别到的问题，重新运行自批判 |
| **< 70/100** | NOT READY | 回退到对应子阶段进行实质性修改 |

**回退指引（按失分维度）：**
- 声明/引用问题 → Stage 2（LIT）或 Stage 3（EXPER）
- 方法/实验问题 → Stage 1（DIGEST）或 Stage 3（EXPER）
- 语言问题 → Stage 4c（中文精修）或 Stage 4e（英文精修）

**5 项人工审计：**

| 审计 | 内容 |
|------|------|
| **Claims Audit** | 列出每项事实声明 → 定位证据源 → 标记无证据声明 → 标记措辞夸大声明 |
| **Citation Audit** | 统计引用标记 → `[CITATION NEEDED]` 若 >3 则稿件不合格 → 文内引用与参考文献双向验证 |
| **Overclaim Scan** | 扫描中英文禁用词（`forbidden-overclaims.md`）→ 逐条上下文核查 → 重写或加限定 |
| **Readability Audit** | 图/表在正文中先于图表本体被引用 → 交叉引用一致性 → 摘要可脱离全文理解 |
| **Terminology Audit** | 术语一致性扫描 → 缩写首次使用 → 中英术语 1:1 映射 |

**自动化检查**：`python scripts/check_quality.py <output_dir> --all --output 10a_auto_check.md`（9 项检查：声明对齐、引用完整、可复现性、语言质量、结构、中文过度声明、内容去重、AI 味道、术语一致）

**输出报告结构**：每维度得分 + 详细问题列表 + 自动化检查结果 + must-fix 清单 + should-fix 清单 + 总体建议（READY / NEEDS REVISION / NOT READY）

---

### Stage 4g — 模板渲染

**5 步流程：**
1. **中文 LaTeX**：复制 `templates/chinese/`，从 `06_chinese_polished.md` 填充，XeLaTeX 编译
2. **英文 LaTeX**：复制 `templates/ieee-latex/`，从 `08_english_polished.md` 填充，生成 `references.bib`，pdflatex 编译
3. **英文 Word**：构建 `word_content.json`，运行 `render_word.py` 填充 IEEE Word 模板
4. **Cover Letter**：5 段结构（投稿声明 / 背景+贡献 / 关键发现 / 为何投此刊 / 声明），LaTeX + Word 双格式。Cover Letter 不得复制摘要原文，所有夸大规则加倍适用
5. **跨模板一致性校验**：标题一致 / 作者顺序一致 / 所有指标值一致 / 引用数一致 / Cover Letter 声明不超出稿件 / 无 `[CITATION NEEDED]` 或 `AUTHOR_INPUT_NEEDED`

**11 个可用模板**：中文期刊 / IEEE 会议 / IEEE TGRS / IEEE TETCI / IEEE TIP / CVPR·ICCV / NeurIPS·ICML / ACL·EMNLP / AAAI·IJCAI / IEEE Word / Cover Letter

---

### 投稿后工具（NEW v0.4）

| 工具 | 脚本 | 功能 |
|------|------|------|
| 审稿回复 | `generate_rebuttal.py` | 评论自动分类 / 逐条回复模板 / 跨审稿人一致性检查 / Markdown + LaTeX 输出 |
| 论文转 Slides | `paper_to_slides.py` | Beamer LaTeX / Marp Markdown 双格式 + 讲稿生成 |

---

## 快速开始

### 方式一：在 AI Agent 中使用

`SKILL.md` 是一个通用的结构化指令文件，不绑定特定平台。Claude Code 可自动触发；Codex、Cursor、GitHub Copilot 等可将文件内容作为系统 prompt 或上下文加载使用。

1. 将本仓库克隆到本地，`SKILL.md` 即入口文件。
2. 将 `SKILL.md` 内容作为系统指令/上下文提供给 AI Agent。
3. 在对话中说"帮我写一篇 SCI 论文"，或提供材料后说"把这些写成论文"。
4. Agent 会从 Stage 0 开始，逐步走完全部流水线。你在关键检查点进行审阅。
5. 最终输出：英文 SCI 论文（LaTeX + Word 双格式）、中文参考稿（LaTeX），以及所有中间文件和质量报告。

### 方式二：作为独立工具使用

你也可以直接调用各阶段脚本：

```bash
# ── Stage 1: 文件清单 → 架构提取 → Notebook解析 → 依赖追踪 → 简报合成 ──
python digest/scripts/summarize_repo.py my_project/ --output repo_inventory.md
python digest/scripts/extract_architecture.py my_project/ --output arch_report.md
python digest/scripts/parse_notebooks.py experiments/*.ipynb --output-dir ./digest/
python digest/scripts/trace_dependencies.py my_project/ --entry train.py --output deps.md
python digest/scripts/synthesize_brief.py --repo my_project/ --output project_brief.md

# ── Stage 2: 文献检索 → 填矩阵 → 验证 → 分析 → 合成 ──
python literature/scripts/search_literature.py "cross-modal retrieval contrastive learning" \
    --sources s2,arxiv --max 30 --output results.md
python literature/scripts/auto_fill_matrix.py results.md \
    --project-brief project_brief.md --output lit_matrix.md
python literature/scripts/verify_citations.py citations.txt --sources crossref,dblp
python literature/scripts/analyze_citations.py lit_matrix.md --output gap_analysis.md
python literature/scripts/synthesize_literature.py lit_matrix.md \
    --project-brief project_brief.md --output synthesis.md

# ── Stage 3: 实验设计 → 分析 → 统计 → 可视化 → 合成 ──
python experiment/scripts/design_experiments.py \
    --project-brief project_brief.md --venue cvpr --output experiment_plan.md
python experiment/scripts/compute_improvements.py results.csv \
    --target MyModel --metrics R@1 R@5 R@10 \
    --higher-better R@1 R@5 R@10 --group-cols Dataset --stats --output improvements.md
python experiment/scripts/statistical_tests.py results.csv \
    --target MyModel --metrics R@1 R@5 R@10 \
    --higher-better R@1 R@5 R@10 --output stats_report.md
python experiment/scripts/result_visualizer.py results.csv \
    --target MyModel --metrics R@1 R@5 R@10 --output-dir ./figures/
python experiment/scripts/synthesize_experiments.py \
    --improvements improvements.md --stats stats_report.md \
    --project-brief project_brief.md --output exp_synthesis.md

# ── Stage 4f: 质量检查 + 声明-证据审计 + 交叉引用校验 ──
python scripts/check_quality.py output_dir/ --all --output quality_report.md
python scripts/claim_evidence_auditor.py paper.md \
    --output-dir output_dir/ --output claim_audit.md
python scripts/validate_references.py paper.md --output ref_report.md

# ── Stage 4g: 模板渲染 ──
python scripts/render_word.py content.json \
    --template templates/ieee-word/template.docx --output manuscript.docx

# ── 投稿后: 审稿回复 + Slides ──
python scripts/generate_rebuttal.py reviews.txt --paper paper.md --output rebuttal.md
python scripts/paper_to_slides.py paper.md --format beamer --author "J. Yang" --output slides.tex
```

---

## v0.4.0 核心能力

**文献流水线（Stage 2 — 全面升级）**
- API 自动搜索（Semantic Scholar / arXiv / CrossRef / DBLP）
- AI 自动填充文献矩阵（Category / Main Idea / Relation / Use in Paper）
- 引文元数据交叉验证
- 时间趋势分析、会议分布、方法家族聚类、研究缺口识别
- **文献叙述合成** — 矩阵自动转化为 Introduction 和 Related Work 的有逻辑段落（按范式组织，非论文罗列；含主题句、论述演进、方法区分、逻辑流检查）

**实验全流程（Stage 3 — 全面升级）**
- **实验计划生成** — 从声明推导所需实验类型和消融变体，基线覆盖检查，分阶段路线图
- 改进计算 + Bootstrap CI（v0.3 + v0.4 增强）
- 统计检验：效应量、显著性检验、多重比较校正、功效分析
- 结果可视化：6 种图表类型（PNG/PDF/SVG/PGF）
- **实验叙述合成** — 自动生成 Setup / Results / Ablation / Efficiency / Discussion 段落模板

**质量保障三件套（Stage 4f — NEW）**
- **质量评分** — 5 维度 100 分制自动检查
- **声明-证据审计** — 提取全部事实性声明，逐条追溯表/图引用，数值交叉验证，夸大表述检测
- **交叉引用校验** — 图/表/公式/章节编号连续性、孤立对象检测、引用-定义顺序检查、缩写首次使用检测

**项目消化（Stage 1 — 全面升级）**
- 文件清单 + 深度代码分析（nn.Module / Flax / Keras 子类提取）
- Jupyter Notebook 解析（模型定义、训练循环、超参数、结果表格）
- 跨文件依赖追踪（导入图、数据流、核心管线识别、孤立模块检测）
- 损失函数解析、超参数检测、框架识别、训练基础设施检测
- **项目简报自动合成** — 一键生成完整的 `project_brief.md`（`--repo` 模式端到端运行）

**投稿后工具（Stage 4 — NEW）**
- 审稿回复信生成（Markdown / LaTeX）、评论自动分类、跨审稿人一致性检查
- 论文转 Slides（Beamer LaTeX / Marp Markdown）+ 讲稿生成

**去夸大 · 去重 · 去AI味**
- 中英文夸大表述禁用词表 + 安全替代 + 自查流程
- 跨章节去重规则、AI套话检测
- 集成到中文润色、英文润色、自批判三个阶段

**中英翻译语料库**
- 高频术语、句式对照，声明强度映射（中文夸大 → 英文学术安全表述）

**模板输出（Stage 4g）**
- 11 个会议/期刊 LaTeX 模板：中文期刊、IEEE 会议、IEEE TGRS（遥感）、IEEE TETCI（计算智能）、IEEE TIP（图像处理）、CVPR/ICCV、NeurIPS/ICML、ACL/EMNLP、AAAI/IJCAI
- IEEE Word 模板 + Cover Letter（LaTeX + Word 双格式）

---

## 示例项目

`examples/mini-ai-paper-project/` 提供了一个以**跨模态文本-图像检索**为场景的完整端到端示例：

| 文件 | 阶段 | 说明 |
|------|------|------|
| `materials/project_notes.md` | 输入 | 真实风格的研究笔记 |
| `experiments/results.csv` | 输入 | 含 5 个基线、3 个数据集的实验表 |
| `outputs/00_project_brief.md` | Stage 1 | 结构化简报含证据映射 |
| `outputs/02_literature_matrix.md` | Stage 2 | 含验证状态的文献矩阵 |
| `outputs/03_experiment_analysis.md` | Stage 3 | 论据强度分析 |
| `outputs/04_paper_storyline.md` | Stage 4a | 完整故事线 |
| `outputs/05_chinese_draft.md` | Stage 4b | 中文初稿 |
| `outputs/08_english_polished.md` | Stage 4e | 英文终稿 |
| `outputs/10_critique_report.md` | Stage 4f | 质量自批判报告 |

---

## 依赖

```
python >= 3.8
requests, python-docx, pylatexenc
```

安装：

```bash
pip install requests python-docx pylatexenc
```

可选依赖（按需安装）：

```bash
pip install matplotlib          # result_visualizer.py 可视化图表
pip install anthropic           # auto_fill_matrix.py / synthesize_literature.py 的 --auto 模式
pip install jupyter             # parse_notebooks.py 解析 .ipynb 文件（通常已安装）
```

LaTeX 编译需要本地安装 TeX Live 或 MiKTeX（仅 Stage 4g 需要）。

---

## 开发

```bash
# 运行测试
python -m unittest discover -s tests

# 打包完整套件
python scripts/package_skills.py --output-dir dist
```

---

## 安全原则

- **不伪造任何内容**：引用、DOI、数据集、基线、指标、实验、行号均不得虚构。
- 缺失的作者输入标注为 `AUTHOR_INPUT_NEEDED`。
- 缺失的引用标注为 `[CITATION NEEDED]`。
- 在润色、翻译过程中，**科学含义优先于语言流畅**。
