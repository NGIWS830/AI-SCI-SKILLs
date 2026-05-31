<div align="center">

# AI-SCI-SKILLs v0.3

[![Version](https://img.shields.io/badge/version-v0.3-blue.svg)](https://github.com/NGIWS830/AI-SCI-SKILLs/releases)
![Platform](https://img.shields.io/badge/platform-Claude%20Code%20%7C%20Any%20Agent-lightgrey.svg)
![Built with](https://img.shields.io/badge/AI%20Powered-Skill%20%7C%20Pipeline-orange.svg)

[English](README_EN.md)

</div>

---

<div align="center">

<h3><strong>一个 Skill，一次会话。原始材料 → 英文 SCI 论文终稿。🚀</strong></h3>

</div>

---

AI-SCI-SKILLs 是一个以中文为先的端到端 SCI 论文写作流水线，覆盖深度学习、机器学习、计算机视觉、NLP、多模态学习及相关 AI 研究方向。

---

## 触发方式

### 触发关键词

对话中出现以下任意关键词时，Claude Code 会自动激活本 skill：

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
Stage 2: LIT    → 文献检索（API 自动化）、验证、矩阵整理
Stage 3: EXPER  → 实验分析、改进计算、论点提炼
Stage 4: WRITE  → 4a 故事线 → 4b 中文初稿 → 4c 中文润色
               → 4d 英译 → 4e 英文润色 → 4f 自批判 → 4g 模板渲染
```

支持断点续传：中断后重新加载 `SKILL.md` 并指向已有 `project-state.md` 即可继续。

---

## 架构

```
SKILL.md（根入口）
├── digest/        — 从项目材料中提取论文可用信息
│   └── references/  — 代码阅读、任务分类、证据规则、简报模板
├── literature/    — 检索、验证并组织文献
│   ├── references/  — 搜索策略、API 指南、引文验证、经典论文地图
│   └── scripts/     — search_literature.py, verify_citations.py
├── experiment/    — 分析实验并验证论点
│   └── references/  — 指标指南、声明规则、消融写作、可复现性检查清单
├── writer/        — 中文初稿 → 润色 → 英译 → 英文润色 → 自批判
│   └── references/  — 全章节模板、中英翻译语料库、术语表、质量评分标准
├── scripts/       — 质量检查、LaTeX 编译、图表抽取、BibTeX 格式化、Word 渲染
└── templates/     — 中文期刊、IEEE LaTeX、IEEE Word、Cover Letter 模板
```

---

## 快速开始

### 方式一：在 Claude Code 中使用

1. 将本仓库克隆到本地，`SKILL.md` 即 skill 入口。
2. 在对话中说"帮我写一篇 SCI 论文"，或提供材料后说"把这些写成论文"。
3. Agent 会从 Stage 0 开始，逐步走完全部流水线。你在关键检查点进行审阅。
4. 最终输出：英文 SCI 论文（LaTeX + Word 双格式）、中文参考稿（LaTeX），以及所有中间文件和质量报告。

**注意：** 本项目是 Claude Code 的 skill，SKILL.md 需在对话中被加载才能生效。直接对话即可触发，无需额外配置。

### 方式二：作为独立工具使用

你也可以直接调用各阶段脚本：

```bash
# 文献搜索
python literature/scripts/search_literature.py "cross-modal retrieval contrastive learning" \
    --sources s2,arxiv --max 20 --output results.md

# 实验改进计算
python experiment/scripts/compute_improvements.py results.csv \
    --target MyModel --metrics R@1 R@5 R@10 \
    --higher-better R@1 R@5 R@10 --group-cols Dataset --output improvements.md

# 质量检查
python scripts/check_quality.py output_dir/ --all --output quality_report.md

# 渲染 Word 稿件
python scripts/render_word.py content.json \
    --template templates/ieee-word/template.docx --output manuscript.docx
```

---

## v0.3 核心能力

**质量评分体系（Stage 4f）**
- 5 维度评分：声明-证据对齐 / 引文完整性 / 方法描述精度 / 实验报告严谨性 / 语言质量
- `scripts/check_quality.py` 自动检查，分数 ≥80 可交付

**去夸大 · 去重 · 去AI味**
- 中英文夸大表述禁用词表 + 安全替代 + 自查流程
- 跨章节去重规则、AI套话检测
- 集成到中文润色、英文润色、自批判三个阶段

**API 自动化文献检索与引文验证**
- Semantic Scholar / arXiv 自动搜索
- CrossRef / DBLP 引文元数据验证

**中英翻译语料库**
- 高频术语、句式对照，声明强度映射（中文夸大 → 英文学术安全表述）

**模板输出（Stage 4g）**
- 中文 LaTeX（中文期刊通用格式）
- 英文 LaTeX（IEEE 会议格式）
- 英文 Word（IEEE 会议格式）
- Cover Letter（LaTeX + Word 双格式）

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
