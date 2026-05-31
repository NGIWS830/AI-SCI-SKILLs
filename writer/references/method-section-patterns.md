# Method Section Patterns

## Method Type Taxonomy

Different paper types require different method section organizations. Identify your type first.

### Type 1: Architecture Paper
You propose a new network design, module combination, or backbone modification.
- **Subsections**: Overview → Module A → Module B → (Module C) → Training Objective
- **Key evidence**: architecture diagram, per-module ablation, component contribution
- **Example papers**: ResNet, DETR, Swin Transformer, UNet++

### Type 2: Algorithm / Training Paper
You propose a new training procedure, loss function, or optimization strategy.
- **Subsections**: Overview → Preliminaries → Proposed Algorithm → Theoretical Analysis → Implementation
- **Key evidence**: convergence curves, loss ablation, sensitivity to hyperparameters
- **Example papers**: SimCLR, DPO, GRPO, MixUp, Label Smoothing

### Type 3: Representation / Feature Paper
You propose a new feature learning method or embedding approach.
- **Subsections**: Overview → Feature Extraction → Feature Transformation → (Fusion Module) → Training
- **Key evidence**: t-SNE/PCA visualizations, retrieval results, transfer learning performance
- **Example papers**: CLIP, SimCSE, MoCo, BYOL

### Type 4: Data / Methodology Paper
You propose a new benchmark, evaluation protocol, or training recipe.
- **Subsections**: Benchmark Design → Data Collection/Annotation → Evaluation Protocol → Baselines
- **Key evidence**: inter-annotator agreement, baseline comparison, statistical analysis
- **Example papers**: ImageNet, GLUE, CIFAR, VTAB, MLPerf

---

## Subsection Templates

### III-A: Overview

**Template 1 — Simple feed-forward pipeline:**
> Figure [X] illustrates the overall architecture of [Method]. Given an input [input_description], we first [step_1] using [component_1], which [purpose_1]. The resulting [intermediate_1] is then processed by [component_2], which [purpose_2]. Finally, [component_3] produces the [output_description] by [mechanism].

**Template 2 — Multi-branch architecture:**
> [Method] consists of [N] main components, as shown in Fig. [X]. The [Branch_A] processes [input_A] to extract [feature_A], while concurrently, the [Branch_B] operates on [input_B] to produce [feature_B]. These representations are then fused by [Fusion_Module] via [fusion_mechanism], yielding [fused_feature], which is subsequently used for [downstream_task].

**Template 3 — Iterative / sequential process:**
> [Method] proceeds in [N] sequential stages, depicted in Fig. [X].
> **Stage 1: [Name]**. Given [input], we [action], producing [output].
> **Stage 2: [Name]**. Using the output of Stage 1, we [action], which [purpose].
> **Stage N: [Name]**. The final stage [action], yielding [final_output].

### III-B / III-C / III-D: Core Module Description

For each module, cover these five aspects in order:

```
1. INPUT SPECIFICATION
   What enters this module? In what format? With what dimensions?
   "The [Module] takes as input [X] ∈ R^{[dims]}, where [explain_notation]."

2. PROCESS DESCRIPTION
   What computation does this module perform? Step by step.
   "First, we [operation_1]. Then, [operation_2]. Finally, [operation_3]."

3. OUTPUT SPECIFICATION
   What emerges from this module? Where does it go next?
   "The output of [Module] is [Y] ∈ R^{[dims]}, which is passed to [downstream]."

4. DESIGN RATIONALE
   WHY this design choice? Ground in intuition, prior work, or empirical observation.
   "We design [Module] to [mechanism] because [reason]. This is motivated by the observation that [empirical_finding] or the principle that [theoretical_argument]."

5. CONNECTION TO CLAIMS
   How does this module support a contribution claim?
   "This design enables [capability], which directly addresses [gap] and is validated by the ablation in Section IV-C (Table X)."
```

---

## Mathematical Notation Conventions

### Variable Naming

| Notation | Meaning | Example |
|----------|---------|---------|
| x, X | Input (lowercase: vector, uppercase: matrix/tensor) | x ∈ R^D, X ∈ R^{B×C×H×W} |
| y, Y | Output / label | y ∈ {1,...,K}, Y ∈ R^{H×W} |
| h | Hidden representation | h ∈ R^{d_h} |
| z | Latent variable | z ∈ R^{d_z} |
| W, w | Weight matrix / vector | W ∈ R^{d_out×d_in} |
| b | Bias | b ∈ R^{d_out} |
| θ | All learnable parameters | θ = {W_1, b_1, ..., W_L, b_L} |
| L | Loss function | L_total = L_task + λL_reg |
| λ, α, β | Hyperparameters / trade-off coefficients | λ = 0.1 |

### Dimension Annotation

Always annotate dimensions on first use:
```
"Let X ∈ R^{B×C×H×W} denote a batch of B images with C channels and spatial size H×W."
```

Re-annotate after any dimension-changing operation:
```
"The backbone f_θ(·) maps the input X ∈ R^{B×3×224×224} to a feature map F ∈ R^{B×D×7×7}, where D = 2048."
```

### In-text Math vs. Display Equations

- **In-text**: Short expressions, variable definitions, scalar relationships.
  "We set λ = 0.1 throughout." "The attention weight α_ij is computed as..."
- **Display equations**: Multi-term expressions, derivations, key formulas.
  ```
  L_total = L_task + λ_1 L_consistency + λ_2 L_sparsity   (1)
  ```
- **Numbering**: Use "Eq. (1)", not "Equation 1". Only number equations referenced later.

### Equation Writing Patterns

**Attention mechanism:**
```
The attention output is computed as:
    Attention(Q, K, V) = softmax(QK^T / √d_k) V          (1)
where Q, K, V ∈ R^{N×d} denote the query, key, and value matrices,
d_k = d/h is the per-head dimension, and h is the number of attention heads.
```

**Loss function (component-wise):**
```
The total training objective consists of three terms:
    L_total = L_task + α L_consistency + β L_sparsity    (2)
The task loss L_task is the standard cross-entropy between predicted
and ground-truth labels. The consistency loss L_consistency, defined
in Eq. (3), enforces [property]. The sparsity regularization L_sparsity
encourages [behavior] via an L1 penalty on [parameters].
```

**Normalization:**
```
LayerNorm(x) = γ ⊙ (x - μ) / σ + β                       (3)
where μ and σ are the mean and standard deviation computed over
the feature dimension, and γ, β are learnable affine parameters.
```

### The "Explain Every Symbol" Rule

Every symbol in a display equation must be explained in the surrounding prose. No orphan variables. If you introduce σ twice with different meanings, the reader will be confused — rename one.

---

## Pseudocode Formatting Standards

Use algorithm2e LaTeX package conventions:

```
\begin{algorithm}[t]
\caption{[Algorithm Name]: [One-line description]}
\label{alg:label}
\begin{algorithmic}[1]
\REQUIRE [Input specifications]
\ENSURE [Output specifications]
\STATE \textbf{// Step 1: [Description]}
\FOR{$i = 1$ \TO $N$}
    \STATE $h_i \gets \text{[Operation]}(x_i)$
\ENDFOR
\STATE \textbf{// Step 2: [Description]}
\STATE $y \gets \text{[Final Operation]}(h)$
\RETURN $y$
\end{algorithmic}
\end{algorithm}
```

**When to use pseudocode instead of prose:**
- The algorithm has multiple steps with branching or iteration.
- The order of operations is critical and prose would be ambiguous.
- The method is the main contribution and deserves formal presentation.

**When to use prose instead of pseudocode:**
- The method is a standard architecture description (use the diagram).
- The algorithm is simple enough to describe in 3-4 sentences.
- Pseudocode would duplicate information already clear from equations.

---

## Architecture Diagram Description Template

**Prose guide for diagrams:**
> As illustrated in Fig. [X], [Method] consists of [N] main components: (a) the [Component_A], which [function]; (b) the [Component_B], which [function]; and (c) the [Component_C], which [function]. The data flow proceeds as follows: [input] → [Component_A] → [intermediate] → [Component_B] → [output]. Key design choices are highlighted with [visual cues].

**Caption template:**
> Fig. [X]. Overview of the proposed [Method] architecture. [One-sentence description of the complete data flow]. [Optional: one sentence highlighting the novel component in a different color].

**Diagram design conventions:**
- Use distinct colors for: backbone (gray/blue), proposed modules (orange/red), loss functions (green).
- Arrows should clearly show data flow direction. Bidirectional arrows only if information flows both ways.
- Dimension annotations on tensors are helpful (e.g., "H×W×C" below a feature map block).
- Keep the diagram self-contained: a reader looking only at Fig. 1 should understand the high-level method.

---

## Loss Function Description Patterns

### Component-by-Component Pattern

> The total training loss is a weighted sum of [N] terms:
>
>     L = L_task + α L_aux + β L_reg
>
> **Task Loss (L_task).** We use [standard_loss] for the primary task. Given [inputs], L_task is computed as [formula_or_description]. This term ensures that the model learns to [primary_objective].
>
> **Auxiliary Loss (L_aux).** The auxiliary loss term encourages [desired_property]. Specifically, [formula_or_description]. The weight α controls the trade-off between [tradeoff_A] and [tradeoff_B]; we set α = [value] based on [selection_method].
>
> **Regularization (L_reg).** We apply [regularization_type] to [parameters] to prevent [overfitting/other]. With weight β = [value].

### Intuition-First Pattern

> To encourage the model to focus on [desired_behavior], we introduce a [loss_name] that penalizes [undesired_behavior]. The key observation is that [insight_motivating_the_loss]. Formally:
>
>     L_name = [formula]
>
> This term is minimized when [ideal_condition], and increases as [deviation_from_ideal]. Combined with the standard task loss, the full objective guides the model toward [desired_outcome] while [secondary_benefit].

### Ablation Relationship

Each loss term should correspond to at least one ablation row in the experiments. When writing the loss section, note mentally: "Loss term L_aux will be ablated in Table X, row 'w/o L_aux'." If a loss term cannot be cleanly ablated, explain why in the ablation section.

---

## Training Procedure Description Template

```
Implementation details. We implement [Method] in [framework] ([version]).
All models are trained on [GPU_type] for [N] epochs with a batch size of [B].
We use [optimizer] with β_1 = [val], β_2 = [val], and weight decay = [val].
The learning rate is initialized to [lr_init] and follows a [schedule]
schedule: [description of warmup + decay]. For data augmentation, we apply
[augmentation_list]. All input images are resized to [H]×[W]. Training a
single model takes approximately [time] on [hardware].

We report results averaged over [N] runs with different random seeds
([seed_list]). Standard deviations are reported in all result tables.
Hyperparameters were selected via [method] on the [validation_set].
```

**What to always include:**
- Optimizer name, β values, weight decay
- Learning rate schedule (warmup epochs, peak LR, decay type and rate)
- Batch size (effective batch size if gradient accumulation is used)
- Number of epochs and early stopping criteria
- Input resolution / sequence length
- Data augmentation pipeline
- Hardware and training time
- Number of runs for error bars, seed values
- Hyperparameter selection method

---

## Annotated Example Method Section (Chinese + English)

### Chinese Draft (Core Module)

```
III-B. 方向一致性模块 (Directional Consistency Module)

输入与动机. 给定主干网络提取的特征图 F ∈ R^{H×W×D}，方向一致性模块的目标
是显式建模边界像素沿空间方向的连续性。我们的设计动机源于一个关键观察：
自然图像中的结构边界（如道路边缘、建筑物轮廓）通常沿特定方向连续延伸，
而纹理边界（如树叶、草地）则呈现随机分布。现有方法将所有边界像素等同
对待，未能利用这一方向先验。

[注释] 第一段功能: 输入规格 + 设计动机。从"给定输入"到"为什么这样设计"。

方向感知特征提取. 如图[2]所示，我们首先通过四个方向卷积核
{K_0°, K_45°, K_90°, K_135°} 对特征图 F 进行卷积，提取沿四个主方向的
边缘响应：
    E_θ = Conv_θ(F),   θ ∈ {0°, 45°, 90°, 135°}                (4)
其中每个方向卷积核 K_θ 是一个 Sobel 型可学习滤波器，初始化为对应方向
的 Sobel 算子并在训练中微调。

[注释] 第二段功能: 计算过程。公式(4)每个符号在文中解释。

方向一致性约束. 对于结构边界上的像素，其边缘响应在不同方向之间应具有
一致性模式。具体而言，若像素 p 位于水平结构边界上，则其 0° 方向响应
应显著强于 90° 方向响应，且沿边界方向相邻像素的响应应保持稳定。
我们将这一约束形式化为方向一致性损失 L_dc（详见 III-D 节）。

[注释] 第三段功能: 约束设计 + 直觉解释。"若...则..."的直觉先行。
```

---

## Method Section Quality Self-Check

1. **Overview**: Can a reader understand the complete data flow from Fig. 1 + III-A alone?
2. **Modules**: Does each module subsection cover all five aspects (Input → Process → Output → Rationale → Connection to claims)?
3. **Notation**: Is every symbol in every equation explained in the surrounding prose? Are dimensions annotated on first use?
4. **Pseudocode**: If present, does it add value beyond prose? Is input/output clearly specified?
5. **Loss**: Can each loss term be mapped to an ablation row in Section IV?
6. **Training details**: Could another researcher reproduce training from this description?
7. **Design rationale**: Is every design choice motivated, not just described? A method section that only says WHAT without WHY reads like documentation, not a research paper.
8. **No forward references to results**: The method section describes the method, not its performance. "This design leads to improved accuracy (see Section IV)" is acceptable; "This design achieves 82.3% accuracy" is not.

Recommended content order:
1. Define inputs, outputs, symbols, and task setting.
2. Present the overall framework and data flow.
3. Explain each core module with evidence from code, diagrams, notes, or author input.
4. Add Training Objective only when objective/loss/training strategy is supported and important enough to stand alone.
5. Describe inference and complexity only when supported.

All formulas and symbols must be consistent and evidence-grounded.
