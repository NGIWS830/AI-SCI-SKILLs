# Chinese-to-English SCI Writing Rules

## Strategy

Translate meaning, not word order. Reorganize sentences when needed for natural English, but preserve scientific content and claim strength EXACTLY. This is NOT literal translation — it is rewriting Chinese academic prose into English SCI prose.

## Tense Conventions by Section

| Section | Primary Tense | When to Use Other Tenses |
|---------|--------------|--------------------------|
| Abstract | Present | Past for "We evaluated on..." |
| Introduction | Present | Past for past observations, Present perfect for "Recent work has shown..." |
| Related Work | Present perfect / Present | Past for specific historical results |
| Method | Present | Methods are described in present tense |
| Experiments | Past | Present for "Table 1 reports..." |
| Conclusion | Present | Past for summarizing specific results |

## Voice Conventions by Section

| Section | Guidance |
|---------|----------|
| Abstract | Active preferred: "We propose..." |
| Introduction | Active: "We propose...", "We evaluate..." |
| Related Work | Mix: passive for describing existing methods, active for "We differ from..." |
| Method | Passive acceptable for process: "Features are extracted..." Active for design rationale: "We design X to..." |
| Experiments | Active for narrative: "We compare...", "We observe..." Passive for procedure: "Models were trained..." |
| Conclusion | Active: "We have presented...", "We demonstrated..." |

---

## Claim-Strength Mapping Table

Organized by claim category. The "Safer English" column is the default; use "Overclaiming English" only when evidence strength is rated STRONG in Stage 3.

### Performance Claims

| Chinese | Overclaiming English | Safer English (Default) |
|---------|---------------------|------------------------|
| 显著提升 | significantly improves / dramatically boosts | achieves a [X.X] percentage point improvement over [baseline] |
| 大幅超越 | substantially outperforms | outperforms [baseline] by [X]% on [dataset] |
| 一致地提升 | consistently improves | improves across all [N] datasets evaluated |
| 性能优异 | achieves excellent performance | achieves [metric] = [value] on [dataset] |
| 接近 | approaches / is close to | achieves [X]% of [baseline]'s performance |

### Novelty / Contribution Claims

| Chinese | Overclaiming English | Safer English (Default) |
|---------|---------------------|------------------------|
| 首次提出 | is the first to / is novel | proposes (without "first" unless objectively verifiable) |
| 创新性地 | innovatively | — (delete; let the method speak for itself) |
| 开辟了新方向 | opens a new direction | explores a new perspective on |
| 从根本上解决了 | fundamentally solves | addresses a core challenge in / provides a solution to |

### Comparison Claims

| Chinese | Overclaiming English | Safer English (Default) |
|---------|---------------------|------------------------|
| 优于所有现有方法 | outperforms all existing methods / SOTA | outperforms [named baselines] on [specific datasets] |
| 达到了最优性能 | achieves state-of-the-art performance | achieves the best reported performance on [specific benchmark] |
| 全面超越 | comprehensively surpasses | outperforms across [N] out of [M] metrics |

### Evidence / Proof Claims

| Chinese | Overclaiming English | Safer English (Default) |
|---------|---------------------|------------------------|
| 证明了 | proves that | demonstrates that / suggests that / provides evidence that |
| 实验证实 | experimentally confirms | experimental results support / experiments indicate |
| 充分说明 | fully demonstrates | indicates / suggests |
| 揭示了 | reveals | shows / indicates / uncovers evidence of |

### Generalization / Robustness Claims

| Chinese | Overclaiming English | Safer English (Default) |
|---------|---------------------|------------------------|
| 具有很强的泛化能力 | generalizes well / is robust | achieves competitive performance on [out-of-domain dataset] |
| 适用于各种场景 | is applicable to various scenarios | has been evaluated on [specific scenarios] |
| 稳定的表现 | stable performance | performance varies by [X]% across [N] runs |
| 不易过拟合 | does not overfit | shows no significant overfitting on the evaluated datasets |

### Problem-Solving Claims

| Chinese | Overclaiming English | Safer English (Default) |
|---------|---------------------|------------------------|
| 解决了...问题 | solves the problem of... | addresses / alleviates / mitigates |
| 克服了...困难 | overcomes the difficulty of... | reduces the impact of / improves handling of |
| 弥补了...不足 | fills the gap of... | partially addresses / takes a step toward filling |
| 消除了...限制 | eliminates the limitation of... | reduces the effect of / mitigates |

---

## Sentence Restructuring Patterns

Chinese academic prose follows topic-comment structure (topic first, what-is-said-about-it second). English follows subject-verb-object structure. Restructuring is required, not optional.

### Pattern 1: Topic-Prominence → Subject-Prominence

**Chinese (topic-drop):** "针对上述问题，提出了基于注意力机制的特征融合方法。"
→ Literal: "Regarding the above problem, proposed attention-based feature fusion method."
→ **English:** "To address this issue, **we propose** a feature fusion method based on attention mechanisms."

Rule: Add the missing subject (typically "we", "the model", or "this approach").

### Pattern 2: Modifier Stacking → Post-Modification

**Chinese (pre-modifiers):** "基于多尺度注意力机制的自适应特征融合模块"
→ Literal: "The based-on-multi-scale-attention-mechanism adaptive feature fusion module"
→ **English:** "an adaptive feature fusion module **that leverages multi-scale attention mechanisms**"

Rule: Move long modifiers after the noun using relative clauses or prepositional phrases.

### Pattern 3: Zero Article → Article Insertion

**Chinese:** "骨干网络采用ResNet-50架构"
→ **English:** "**The** backbone network adopts **a** ResNet-50 architecture"

Rule: Every singular countable English noun needs an article (a/an/the). Chinese has no articles.

### Pattern 4: Parallel Structure Alignment

**Chinese (repetition-based parallelism):** "该方法不仅提升了精度，还降低了计算量，同时增强了鲁棒性。"
→ **English:** "The method not only improves accuracy but also reduces computation **and** enhances robustness."

Rule: English uses conjunction reduction; Chinese uses repetition for emphasis.

### Pattern 5: Aspect Marker → Tense

**Chinese (了 = completion):** "实验结果表明，该方法有效提升了分割精度。"
→ **English (past for experiments):** "Experimental results **demonstrated** that the method effectively improved segmentation accuracy."

But in Method section:
**Chinese:** "我们采用了三阶段训练策略。"
→ **English (present for method):** "We **adopt** a three-stage training strategy."

Rule: 了 maps to past in Experiments, present in Method. Context determines tense.

---

## Common CN→EN Translation Pitfalls

### 1. Topic-Prominence Transfer
Chinese drops subjects when clear from context. English requires explicit subjects.
- Bad: "Extracts features using ResNet-50." (Who extracts?)
- Good: "**We extract** features using ResNet-50." or "**The backbone** extracts features using ResNet-50."

### 2. Dangling Modifiers
Chinese tolerates dangling modifiers more than English.
- Bad: "After training for 100 epochs, the model achieves convergence." (The model isn't doing the training.)
- Good: "After **we train** for 100 epochs, the model converges."

### 3. Run-On Sentences (Comma Splice)
Chinese uses commas to join independent clauses. English requires periods, semicolons, or conjunctions.
- Bad: "We propose Method X, it uses attention to fuse features, this improves accuracy."
- Good: "We propose Method X, **which** uses attention to fuse features, **leading to** improved accuracy."

### 4. Missing Conjunctions
Chinese often omits "that" / "which" where English requires them.
- Bad: "We find the module contributes significantly to performance."
- Good: "We find **that** the module contributes significantly to performance."

### 5. Over-Use of "can" / "could"
Chinese 可以/能够 often becomes unnecessary "can" in English.
- Bad: "The module can extract features..." (implies it has the ability, not that it does)
- Good: "The module extracts features..." (it does, by design)

### 6. "Respectively" Misuse
Chinese 分别 maps to "respectively" but only when two lists align exactly.
- Bad: "Methods A and B achieve 80% and 82% accuracy, respectively." (Correct but overused)
- Over-use: "We use datasets X, Y, and Z, respectively." (Only use when mapping is 1:1 across two lists)

### 7. "On the one hand... on the other hand..."
Chinese 一方面...另一方面... often becomes this pair, but English uses it only for contrasting trade-offs, not for simply listing two aspects.
- Bad: "On the one hand, we evaluate accuracy. On the other hand, we evaluate speed."
- Good: "We evaluate **both** accuracy **and** speed." or use "First, ... Second, ..."

### 8. Redundant "method" / "approach"
Chinese 该方法/该方案 often appears redundantly when translated.
- Bad: "The method's approach uses attention." (method + approach is redundant)
- Good: "The method uses attention." or "Our approach uses attention."

### 9. "Carry out" / "conduct" Over-Use
Chinese 进行/开展 often maps to "carry out" or "conduct" which sound bureaucratic in English.
- Bad: "We carry out experiments on three datasets."
- Good: "We **evaluate** on three datasets." or "We conduct experiments on three datasets." (conduct is acceptable in Methods)

### 10. Missing Plural -s
Chinese nouns don't mark number; English requires singular/plural distinction.
- Bad: "We evaluate on three dataset."
- Good: "We evaluate on three **datasets**."

### 11. "Such as" + etc.
Chinese 等 maps to both "such as" and "etc." — don't use both.
- Bad: "such as ResNet, ViT, etc."
- Good: "such as ResNet and ViT." or "including ResNet, ViT, and others."

### 12. Numerical Range Format
- Bad: "2~3 percentage points" (Chinese tilde)
- Good: "2–3 percentage points" (en-dash) or "two to three percentage points"

### 13. Over-capitalization in Headings
- Bad: "Related Work On Image Retrieval"
- Good: "Related Work on Image Retrieval" (sentence case or title case, but be consistent)

### 14. Citations as Words
Chinese allows "文献[X]提出..."; English does not.
- Bad: "[42] proposed a method..."
- Good: "Author et al. [42] proposed a method..." or "A method was proposed [42] that..."

### 15. "In this paper" vs. "In this work"
Both are acceptable but use consistently. "In this paper" is slightly more common in CS.
- Don't: Mix "in this paper", "in this work", "in this study" randomly across sections.

---

## Keep Placeholders

Never translate, remove, or fill these markers:
- `[CITATION NEEDED]`
- `AUTHOR_INPUT_NEEDED`

They must appear in the English output exactly as they appear in the Chinese input.

---

## Domain-Specific Translation Patterns

### CNN / Vision Architectures
- 卷积层 → convolutional layer
- 池化层 → pooling layer
- 全连接层 → fully connected layer
- 批归一化 → batch normalization
- 跳跃连接 → skip connection
- 特征金字塔 → feature pyramid
- 感受野 → receptive field
- 下采样/上采样 → downsampling / upsampling

### Transformer Components
- 多头注意力 → multi-head attention
- 前馈网络 → feed-forward network
- 位置编码 → positional encoding
- 层归一化 → layer normalization
- 残差连接 → residual connection
- 编码器/解码器 → encoder / decoder
- 自注意力/交叉注意力 → self-attention / cross-attention

### Training Terminology
- 损失函数 → loss function / objective
- 学习率 → learning rate
- 权重衰减 → weight decay
- 梯度裁剪 → gradient clipping
- 预热 → warmup
- 余弦退火 → cosine annealing
- 知识蒸馏 → knowledge distillation
- 数据增强 → data augmentation
- 早停 → early stopping

### Evaluation Terminology
- 准确率 → accuracy
- 精确率 → precision
- 召回率 → recall
- F1分数 → F1 score
- 均交并比 → mean Intersection over Union (mIoU)
- 平均精度 → average precision (AP) / mean Average Precision (mAP)
- 困惑度 → perplexity
- 双语评估替补 → BLEU (not "Bilingual Evaluation Understudy" in prose)

## Output Options

When presenting translation to the user, you may show:
- Literal translation (for transparency)
- SCI-style rendering (the final output)
- Notes on terminology or ambiguity (when a Chinese term has multiple possible English equivalents)
