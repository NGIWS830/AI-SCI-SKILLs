# Forbidden Overclaims

## Expanded Forbidden Claims List

Do not write these unless explicitly supported by evidence of sufficient strength. "Sufficient" means: multiple datasets, statistical significance, and consistency across settings.

### Absolute Claims

| Forbidden | Safer Alternative | Required Evidence |
|-----------|------------------|-------------------|
| state-of-the-art | achieves the best reported performance on [specific benchmark] | Comparison against prior SOTA on the standard benchmark |
| first / 首次 / 최초 | introduces / proposes (without "first") | Impossible to verify objectively — avoid entirely |
| solves the problem | addresses / alleviates / mitigates | A problem is "solved" only when no meaningful gap remains |
| proves | demonstrates that / suggests that / provides evidence that | "Proof" requires formal mathematical guarantee |
| universally applicable | has been evaluated on [N] datasets spanning [domains] | Evaluation across fundamentally different domains |
| optimal | achieves the best performance among compared methods | Proving optimality requires exhaustive search or proof |

### Exaggerated Magnitude

| Forbidden | Safer Alternative | Required Evidence |
|-----------|------------------|-------------------|
| significantly improves | achieves a [X.X] percentage point improvement over [baseline] | Statistical test + multiple datasets |
| dramatically / substantially | improves by [X]% / outperforms by [X] points | Just report the number; let the reader judge magnitude |
| robust across all scenarios | performs consistently on [evaluated conditions] | Multiple diverse test conditions with stable results |
| comprehensive comparison | comparison with [N] baselines on [M] datasets | Must include all major method families at comparable compute budget |
| negligible cost | requires [X]% more parameters / [Y]ms additional latency | Quantify; let the reader decide what's negligible |

### Unwarranted Generalization

| Forbidden | Safer Alternative | Required Evidence |
|-----------|------------------|-------------------|
| generalizes well | achieves competitive performance on [out-of-domain dataset X] | At least one truly out-of-domain evaluation |
| works for any [X] | has been tested on [specific X varieties] | Multiple varieties tested |
| applicable to real-world scenarios | has been evaluated on [real-world dataset/condition] | Real-world (not simulated) evaluation |
| scalable to [large scale] | scales to [specific size] on [hardware] | Measured scaling behavior |

### Novelty Inflation

| Forbidden | Safer Alternative |
|-----------|------------------|
| completely different from | differs from [specific prior work] in that [specific difference] |
| unprecedented | without direct precedent in [specific area] |
| paradigm shift | introduces a new approach to / explores a new perspective on |
| groundbreaking | contributes to / advances |
| revolutionizes | offers improvements in |

---

## Context-Dependent Detection Rules

Some words are overclaims only in context. Check before flagging:

**"Novel"** — Acceptable if: the contribution is clearly distinguished from all cited prior work AND the novelty is explained (what specifically is new?). Overclaim if: used as a generic adjective ("a novel method" without saying what's novel).

**"Efficient"** — Acceptable if: the paper includes explicit efficiency comparisons (FLOPs, latency, memory) against baselines. Overclaim if: claimed without any efficiency measurement.

**"Simple"** — Acceptable if: the method genuinely has fewer components or lines of code than baselines, and this is shown. Overclaim if: "simple" is used to mask a lack of rigor.

**"Effective"** — Acceptable if: supported by experiment results. Overclaim if: no baseline comparison is provided.

**"Robust"** — Acceptable if: tested under multiple perturbations, domains, or conditions with consistent results. Overclaim if: tested only under standard conditions.

---

## Self-Scan Procedure

After writing, scan for these danger words. For each occurrence, ask:
1. Is this claim supported by evidence in the paper? (Point to specific table/figure.)
2. Is the evidence of sufficient strength for this claim wording? (Check result-claim-rules.md.)
3. Would a skeptical reviewer accept this wording? If not, downgrade.

---
**Chinese Overclaims (NEW)** — see bottom of this file for the comprehensive Chinese banned-word list.
---

## Standard Safer Alternatives (Quick Reference)

| Category | Safer Phrasing |
|----------|---------------|
| Performance | achieves competitive performance, matches the best reported results, outperforms [named baselines] on [dataset] |
| Novelty | introduces, proposes, presents, explores |
| Problem-solving | addresses, alleviates, mitigates, reduces the impact of |
| Evidence strength | demonstrates that, suggests that, provides evidence that, is consistent with |
| Improvement claim | improves over [baseline] by [X] percentage points / [Y]% relative improvement |
| Generalization | achieves [X] on [out-of-domain dataset], transfers to [domain] with [Y]% performance |

---

## Chinese Overclaims — 中文夸大表述禁用词

### 绝对化表述 → 禁止使用

| 禁用词 | 安全替代 | 原因 |
|--------|---------|------|
| 完美 | 有效 / 可行 / 取得了良好效果 | 没有任何方法是完美的 |
| 完全解决 / 彻底解决 / 根本解决 | 缓解 / 改善 / 在一定程度上解决了 |"解决"意味着问题不再存在 |
| 彻底消除 | 有效抑制 / 显著降低 | 几乎不可能"彻底消除" |
| 最优 / 最佳 | 在[数据集]上取得了最优性能 / 在所列方法中表现最好 | 必须限定比较范围 |
| 首次提出 / 首次实现 | 提出了 / 实现了（不加"首次"） | 客观上无法验证是否为真正首次 |
| 颠覆性 / 革命性 | 提出了一种新思路 / 从[视角]探索了 | 让读者和历史评判，不自封 |
| 史无前例 | 与现有方法不同，该方法... | 避免绝对化历史判断 |
| 证明了 | 表明 / 实验结果表明 / 为...提供了证据 |"证明"需要严格的数学推导 |
| 普遍适用 / 通用 | 在[N]个不同领域的数据集上得到了验证 | 仅说明已测试的范围 |
| 鲁棒性极强 / 鲁棒性非常好 | 在[具体扰动/条件]下性能波动小于[X]% | 量化描述，不含形容词 |
| 完美地 / 精确地 | 准确地 / 有效地 |"完美"在科学中不存在 |

### 夸张量级 → 替换为具体数值

| 禁用表述 | 安全替代 |
|---------|---------|
| 大幅提升 / 大幅度提高 | 提升了[X]个百分点（相对提升[Y]%） |
| 显著改善 / 显著提高 / 显著降低 | 在[数据集]上从[X]提升至[Y]（+[Z]个百分点） |
| 极大地增强了 / 极大改善了 | 增强了 / 改善了（不加副词），给出具体数值 |
| 性能远超 / 远远超过 | 在[数据集]上，性能优于[基线名称]（+[X]个百分点） |
| 实现了惊人的 / 令人印象深刻的 | 删除形容词，直接报告数值 |
| 极低的计算开销 | 仅增加[X]%的参数量 / [Y]ms的推理延迟 |
| 几乎不增加 / 几乎不影响 | 增加[X]% / 下降[Y]%（量化） |

### 虚泛概括 → 限定具体范围

| 禁用表述 | 安全替代 |
|---------|---------|
| 在所有数据集上均优于 | 在[列出的N个数据集]上均优于 |
| 具有良好的泛化能力 | 在[域外数据集X]上达到了[Y]（域内为[Z]） |
| 可以广泛应用于 | 已测试[具体场景1]和[具体场景2] |
| 适用于各种... | 适用于[已测试的具体类型] |
| 具有重要的理论意义和实际应用价值 | 删除（空话），或用具体应用场景替代 |
| 达到了国际先进水平 | 在[基准]上与[SOTA方法]性能相当（[具体数值]） |

### 冗余强调词 → 删除

这些词在学术写作中几乎总是多余的。搜索并删除：

| 冗余词 | 原因 |
|--------|------|
| 非常 / 十分 / 极其 | 用具体数值替代 |
| 毫无疑问 / 显然 | 如果真显然，不需要说；如果需强调，说明原因 |
| 众所周知 | 如果是真的，引用文献；如果不是，这是撒谎 |
| 毋庸置疑 | 科学中一切都可质疑 |
| 必须指出 / 特别强调的是 | 直接说内容，不需要预告 |
| 值得注意的是 / 值得一提的是 | 删除，直接陈述 |

### 中文自查流程

写完后扫描以下危险词。每处出现时追问：

1. 这个说法是否有证据支撑？（指出具体表格/图表编号。）
2. 证据强度是否匹配这个措辞的强度？
3. 审稿人会接受这个措辞吗？如果不确定，降级措辞。

**快速扫描关键词（中英文混合）：**

```
CN: 完美 彻底 完全解决 首次 最优 颠覆 大幅 显著 极大 极其 惊人 通用 鲁棒 毫无疑问 众所周知 毋庸置疑
EN: perfect completely solved first optimal groundbreaking revolutionary dramatically significantly extremely remarkably universally undoubtedly obviously
```
