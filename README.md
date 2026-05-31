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
Stage 1: DIGEST → 阅读项目材料，生成结构化简报
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
│   └── scripts/     — summarize_repo.py, extract_architecture.py
├── literature/    — 检索 → 自动填矩阵 → 验证 → 缺口分析 → 叙述合成
│   ├── references/  — 搜索策略、API 指南、引文验证、经典论文地图、
│   │                  文献合成指南（矩阵→叙事）
│   └── scripts/     — search_literature.py, auto_fill_matrix.py,
│                      verify_citations.py, analyze_citations.py,
│                      synthesize_literature.py
├── experiment/    — 分析实验并验证论点
│   ├── references/  — 指标指南、声明规则、消融写作、可复现性检查清单
│   └── scripts/     — compute_improvements.py, statistical_tests.py,
│                      result_visualizer.py
├── writer/        — 中文初稿 → 润色 → 英译 → 英文润色 → 自批判
│   └── references/  — 全章节模板、中英翻译语料库、术语表、质量评分标准
├── scripts/       — 质量检查、声明-证据审计、交叉引用校验、
│                    LaTeX 编译、BibTeX 格式化、Word 渲染、
│                    审稿回复生成、论文转Slides
└── templates/     — 11 个会议/期刊模板（中英文、CV/ML/NLP/AI/遥感/
                     计算智能/图像处理）、Cover Letter
```

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
# ── Stage 1: 架构提取 ──
python digest/scripts/extract_architecture.py my_project/ --output arch_report.md

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

**架构提取（Stage 1 — NEW）**
- 自动提取所有 nn.Module / Flax / Keras 子类
- 损失函数解析、超参数检测
- 框架识别（PyTorch / JAX / TF / HuggingFace）
- 训练基础设施检测（优化器、调度器、混合精度、分布式训练）

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
