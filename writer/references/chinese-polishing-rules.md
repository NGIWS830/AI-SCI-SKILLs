# Chinese Polishing Rules

## Goals

Improve academic clarity, coherence, paragraph logic, and technical precision.

## 20-Item Polishing Checklist

Apply to each section. Every item includes a concrete before/after example.

### Clarity & Precision
| # | Check | Before (BAD) | After (GOOD) |
|---|-------|-------------|--------------|
| 1 | Remove empty modifiers | 该方法取得了较好的性能提升 | 该方法在Cityscapes上提升了2.3 mIoU |
| 2 | Replace vague quantities | 在多个数据集上进行了验证 | 在Cityscapes、Mapillary Vistas和ADE20K三个数据集上进行了验证 |
| 3 | Specify comparison targets | 优于基线方法 | 在边界F1指标上优于SegFix（+2.3）和PIDNet（+1.7） |
| 4 | Define abbreviations on first use | 使用mIoU作为评价指标 | 使用均交并比（mean Intersection over Union, mIoU）作为评价指标 |

### Grammar & Style
| # | Check | Before (BAD) | After (GOOD) |
|---|-------|-------------|--------------|
| 5 | Add missing subjects | 使用ResNet-50作为骨干网络 | 我们使用ResNet-50作为骨干网络 |
| 6 | Fix dangling modifiers | 经过充分训练后，性能得到了提升 | 经过充分训练后，模型性能得到了提升 |
| 7 | Split run-on sentences (>50 chars) | (a 60-character run-on sentence without break) | (two 25-35 character sentences with proper punctuation) |
| 8 | Normalize punctuation | 该方法具有以下优点：1.计算量小2.精度高3.易部署 | 该方法具有以下优点：(1) 计算量小；(2) 精度高；(3) 易于部署。 |

### Logic & Flow
| # | Check | Before (BAD) | After (GOOD) |
|---|-------|-------------|--------------|
| 9 | Add transition between paragraphs | [段落A结束。] [段落B直接开始，无过渡] | [段落A结束。] [过渡句，连接AB的逻辑关系。] [段落B开始。] |
| 10 | Ensure topic sentence per paragraph | (段落直接从细节开始，无总起句) | 消融实验结果（表X）揭示了各组件的贡献差异。具体而言... |
| 11 | Remove information in wrong section | [方法section中出现] "该方法在Cityscapes上达到了82.3% mIoU" | [移入实验section；方法section只描述设计，不报告结果] |

### Consistency & Accuracy
| # | Check | Before (BAD) | After (GOOD) |
|---|-------|-------------|--------------|
| 12 | Unify terminology throughout | 注意力机制 / Attention机制 / attention机制 混用 | 统一为"注意力机制"（首次出现时标注英文 attention mechanism） |
| 13 | Align Chinese-English terms | 中文写"骨干网络"，英文写"backbone" | 全文统一映射：骨干网络 ↔ backbone network |
| 14 | Verify number consistency | 正文写"提升了2.3个百分点"，表格中是2.1 | 核对并统一为2.3 |
| 15 | Verify cross-reference accuracy | "如图3所示" 但图3实际是另一张图 | 核对所有图号、表号、公式号引用 |

### Redundancy & Conciseness
| # | Check | Before (BAD) | After (GOOD) |
|---|-------|-------------|--------------|
| 16 | Remove redundant word pairs | 精度和准确率均得到提升 | 精度提升了1.2个百分点（说明具体哪个指标） |
| 17 | Delete repeated information | 引言介绍了方法...方法section又逐字重复 | 引言：1-2句概述方法思路；方法section：详细展开实现 |
| 18 | Remove unnecessary adjectives | 该方法取得了非常显著的、令人印象深刻的性能提升 | 该方法在Cityscapes上将mIoU从78.2提升至80.5（+2.3个百分点） |
| 19 | Merge short related sentences | 我们使用AdamW优化器。我们设置学习率为1e-3。 | 我们使用AdamW优化器，初始学习率设为1e-3。 |

### Claim Alignment
| # | Check | Before (BAD) | After (GOOD) |
|---|-------|-------------|--------------|
| 20 | Match claim strength to evidence | 该方法大幅超越了所有现有方法 | 在三个数据集的边界F1指标上，该方法均优于所列基线方法（+1.7~2.3个百分点，Table 2） |

---

## Logic Flow Audit

Read the complete draft from start to finish. At each paragraph boundary, ask:

1. **Logical connection:** Does this paragraph follow from the previous one? If the reader asks "why?" or "how?", does the next paragraph answer?
2. **New information:** Does this paragraph introduce something new, or restate previous content? If restating, consider cutting.
3. **Argument chain:** Is there a clear through-line from problem → gap → method → evidence → conclusion? Identify any missing step.
4. **Transition quality:** Is the transition explicit (a transition word/sentence) or implicit (the reader must infer the connection)? Explicit is better.

**Fix strategies:**
- If two paragraphs feel disconnected, add a transition sentence at the start of the second paragraph.
- If a paragraph seems unrelated, either clarify its relevance or cut it.
- If the argument jumps (A → C without B), add a paragraph explaining B.

---

## Paragraph Coherence Rules

**Topic sentence placement:**
- The first sentence of each paragraph should state the paragraph's main point.
- Readers should be able to understand the paper's argument by reading only the first sentence of each paragraph.

**Supporting sentence ordering:**
- General → specific. Start with the claim, then provide evidence.
- Chronological, if describing a process.

**Concluding sentence (optional):**
- A paragraph's final sentence can: summarize, transition to the next paragraph, or state the implication.

---

## Academic Register Guidelines

Replace informal expressions with formal academic equivalents:

| Informal | Formal |
|----------|--------|
| 很多 | 大量 / 众多 / [具体数量] |
| 非常好 | 取得了有竞争力的结果 / 在[指标]上达到[值] |
| 不太好 | 在[场景]下表现受限 / 性能有待提升 |
| 其实 | (通常可删除) 或改为"事实上"、"本质上" |
| 做了 | 进行了 / 实施了 / 完成了 |
| 看一下 | 观察 / 分析 / 考察 |
| 总的来说 | 综上所述 / 总体而言 |
| 等等 / 什么的 | 等（学术写作中可以保留"等"，但不要加"什么的"） |

---

## Terminology Consistency Check

**Detection method:** Scan the document for:
- The same concept expressed with different Chinese terms (e.g., "特征提取网络" and "骨干网络" referring to the same thing).
- The same module named differently in different sections (e.g., "方向一致性模块" in III-B but "DCM" or "方向模块" elsewhere).

**Fix:** Choose one term per concept. Use it consistently. Define abbreviations on first use.

---

## Redundancy Detection

**Scan for:**
1. Consecutive sentences conveying the same information.
   - "我们使用AdamW优化器。优化器的选择是AdamW。" → "我们使用AdamW优化器。"
2. The same method component described identically in Introduction and Method.
   - Introduction: 1-2 sentence teaser. Method: full exposition. These should not be identical.
3. Metric values repeated in Results prose AND Conclusion with identical wording.
   - Results: "achieved 82.3% mIoU" (reporting). Conclusion: "achieved 82.3% mIoU, demonstrating..." (interpreting). Add interpretation layer.

---

## Preserve (Never Change During Polishing)

- Scientific meaning — never alter to improve wording
- Claim strength — never upgrade a weak claim to a strong one
- Metric values and dataset names
- Method names and module descriptions
- Citation placeholders (`[CITATION NEEDED]`)
- Author input markers (`AUTHOR_INPUT_NEEDED`)
- Numbers, table references, figure references
