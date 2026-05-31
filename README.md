# AI-SCI-SKILLs v0.3

[English](README_EN.md)

---

AI-SCI-SKILLs 是一个以中文为先的端到端 SCI 论文写作流水线，覆盖深度学习、机器学习、计算机视觉、自然语言处理、多模态学习及相关 AI 研究方向。

**一个技能，一次会话。原始材料 → 打磨好的英文稿件。**

### 架构

v0.3 在统一流水线基础上深度升级：增强参考文件、集成 API 自动化、引入质量评分体系、新增自批判阶段。

```
SKILL.md（根入口）
├── digest/        — 从项目材料中提取论文可用的信息
│   └── references/  — 代码阅读、任务分类、证据规则、简报模板
├── literature/    — 检索、验证并组织文献
│   ├── references/  — 搜索策略、API 指南、引文验证、经典论文地图、综述模式
│   └── scripts/     — search_literature.py, verify_citations.py（API 自动化）
├── experiment/    — 分析实验并验证论点
│   └── references/  — 指标指南、声明规则、消融写作、可复现性检查清单
├── writer/        — 中文初稿 → 润色 → 英译 → 英文润色 → 自批判
│   └── references/  — 全章节模板、中英翻译语料库、术语表、质量评分标准
└── scripts/       — 质量检查、LaTeX 编译、图表抽取、BibTeX 格式化、打包
```

### 流水线

```
Stage 0: INIT   → 盘点材料，创建项目状态文件
Stage 1: DIGEST → 阅读项目材料，生成项目简报
Stage 2: LIT    → 文献检索（API 自动化）、验证、矩阵整理
Stage 3: EXPER  → 实验分析、改进计算、论点提炼
Stage 4: WRITE  → 4a 故事线 → 4b 中文初稿 → 4c 中文润色 → 4d 英译 → 4e 英文润色 → 4f 自批判
```

流水线可断点续传：若流程中断，重新加载 `SKILL.md` 并指向已有的 `project-state.md`，即可从上一完成阶段继续。

### v0.3 新增功能

**API 自动化文献检索与引文验证**
- `literature/scripts/search_literature.py` — 对接 Semantic Scholar、arXiv API，自动搜索文献
- `literature/scripts/verify_citations.py` — 对接 CrossRef、DBLP，验证引文元数据
- 查询衍生流程：从 Stage 1 的任务描述中提取关键词，组合多组查询，合并去重

**质量评分体系（Stage 4f 自批判）**
- 5 维度评分标准（声明-证据对齐 / 引文完整性 / 方法描述精度 / 实验报告严谨性 / 语言质量）
- `scripts/check_quality.py` — 自动检查生成的论文
- `writer/references/quality-rubric.md` — 详细评分细则
- 分数 ≥80 可交付；70-79 需修复；<70 需返回重写

**中英翻译语料库**
- `writer/references/cn-en-translation-corpus.md` — 高频术语、句式对照，防止翻译错误
- 声明强度映射表：中文常见夸大表述 → 英文学术安全表述

**写作工具脚本**
- `scripts/compile_latex.py` — 编译 LaTeX 稿件为 PDF
- `scripts/extract_figures.py` — 从论文中抽取图表
- `scripts/format_bibtex.py` — 验证并规范化 BibTeX 条目

**增强的 Prompt 工程**
- 每个阶段包含思维链引导（Chain-of-Thought）
- 写作各子阶段包含角色指令（Role Instruction）
- 中英文润色清单（10 项检查清单）
- CV 和 NLP 领域的 few-shot 示例

### 快速开始

1. 将 `SKILL.md` 加载到任何支持 Markdown 技能定义的 agent 中。
2. 提供你的研究材料：代码、笔记、实验表格、框架图、文献等。
3. Agent 自动走完全部阶段。你在关键检查点进行审阅和确认。
4. 输出：一篇打磨好的英文 SCI 论文，以及所有中间文件和质量报告。

### 打包

打包完整套件：

```bash
python scripts/package_skills.py --output-dir dist
```

打包单个模块：

```bash
python scripts/package_skills.py --module experiment --output-dir dist
```

### 示例项目

参见 `examples/mini-ai-paper-project/`，以**跨模态文本-图像检索**为场景的完整端到端示例：

| 文件 | 阶段 | 说明 |
|------|------|------|
| `materials/project_notes.md` | 输入 | 真实风格的研究笔记 |
| `experiments/results.csv` | 输入 | 含 5 个基线、3 个数据集的实验表 |
| `outputs/00_project_brief.md` | Stage 1 | 结构化简报含证据映射 |
| `outputs/02_literature_matrix.md` | Stage 2 | 含验证状态的文献矩阵 |
| `outputs/03_experiment_analysis.md` | Stage 3 | 论据强度分析 |
| `outputs/03a_improvement_summary.md` | Stage 3 | 量化改进计算 |
| `outputs/04_paper_storyline.md` | Stage 4a | 完整故事线 |
| `outputs/05_chinese_draft.md` | Stage 4b | 中文初稿 |
| `outputs/06_chinese_polished.md` | Stage 4c | 中文润色稿 |
| `outputs/07_english_draft.md` | Stage 4d | 英译稿 |
| `outputs/08_english_polished.md` | Stage 4e | 英文终稿 |
| `outputs/09_revision_notes.md` | Stage 4e | 修订说明 |
| `outputs/10_critique_report.md` | Stage 4f | 质量自批判报告 |

运行实验辅助脚本：

```bash
python experiment/scripts/compute_improvements.py examples/mini-ai-paper-project/experiments/results.csv \
    --target SGA-Ours \
    --metrics R@1 R@5 R@10 \
    --higher-better R@1 R@5 R@10 \
    --group-cols Dataset \
    --output examples/mini-ai-paper-project/outputs/03a_improvement_summary.md
```

运行文献搜索：

```bash
python literature/scripts/search_literature.py "cross-modal retrieval contrastive learning" \
    --sources s2,arxiv --max 20 \
    --output examples/mini-ai-paper-project/outputs/02a_search_results.md
```

运行质量检查：

```bash
python scripts/check_quality.py examples/mini-ai-paper-project/outputs --all \
    --output examples/mini-ai-paper-project/outputs/10a_auto_check.md
```

### 开发检查

运行离线测试套件：

```bash
python -m unittest discover -s tests
```

### 安全原则

- 不得伪造引用、DOI、arXiv ID、数据集、基线、指标、实验、行号或任何声明。
- 缺失的作者输入标注为 `AUTHOR_INPUT_NEEDED`。
- 缺失的引用标注为 `[CITATION NEEDED]`。
- 在中文润色、翻译和英文润色过程中，优先保留科学含义，而非追求语言流畅。
