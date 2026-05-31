# AI-SCI-SKILLs v0.2

[English](README_EN.md)

---

AI-SCI-SKILLs 是一个以中文为先的端到端 SCI 论文写作流水线，覆盖深度学习、机器学习、计算机视觉、自然语言处理、多模态学习及相关 AI 研究方向。

**一个技能，一次会话。原始材料 → 打磨好的英文稿件。**

### 架构

v0.2 将 v0.1 的"5 个独立技能"模型替换为统一流水线：

```
SKILL.md（根入口）
├── digest/        — 从项目材料中提取论文可用的信息
├── literature/    — 检索、验证并组织文献
├── experiment/    — 分析实验并验证论点
└── writer/        — 中文初稿 → 润色 → 英译 → 英文润色
```

每个模块包含 `references/`（详细领域指导）和可选的 `scripts/`。根目录的 `SKILL.md` 编排整个流水线，每个阶段完成后将进度保存到共享的 `project-state.md` 文件中。

### 流水线

```
Stage 0: INIT   → 盘点材料，创建项目状态文件
Stage 1: DIGEST → 阅读项目材料，生成项目简报
Stage 2: LIT    → 文献检索、验证、矩阵整理
Stage 3: EXPER  → 实验分析、改进计算、论点提炼
Stage 4: WRITE  → 中文初稿 → 润色 → 英译 → 英文润色
```

流水线可断点续传：若流程中断，重新加载 `SKILL.md` 并指向已有的 `project-state.md`，即可从上一完成阶段继续。

### 快速开始

1. 将 `SKILL.md` 加载到任何支持 Markdown 技能定义的 agent 中。
2. 提供你的研究材料：代码、笔记、实验表格、框架图、文献等。
3. Agent 自动走完 5 个阶段。你在关键检查点进行审阅和确认。
4. 输出：一篇打磨好的英文 SCI 论文，以及所有中间文件。

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

参见 `examples/mini-ai-paper-project/`，包含一个最小的端到端示例：

- 项目笔记
- 实验 CSV
- 项目简报
- 带引用缺失标注的文献矩阵
- 实验分析
- 论文故事线
- 中文初稿节选

在示例上运行实验辅助脚本：

```bash
python experiment/scripts/compute_improvements.py examples/mini-ai-paper-project/experiments/results.csv --target Ours --metrics Acc F1 Params --higher-better Acc F1 --lower-better Params --group-cols Dataset --output examples/mini-ai-paper-project/outputs/03a_improvement_summary.md
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
