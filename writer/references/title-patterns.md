# Title Patterns

Good AI SCI titles are specific about task and method without overclaiming.

## Expanded Pattern Catalog

### Pattern 1: Method-for-Task
```
[Method Name]: [Core Mechanism] for [Task]
```
Examples:
- "SABR: Structure-Aware Boundary Refinement for Semantic Segmentation"
- "MeLoRA: Mergeable Low-Rank Adaptation for Efficient LLM Fine-Tuning"
- "DETR: End-to-End Object Detection with Transformers"

Best for: Papers introducing a named method. Most common in AI.

### Pattern 2: Mechanism-for-Task
```
[Core Mechanism] for [Task] via [Key Insight]
```
Examples:
- "Directional Consistency Modeling for Semantic Segmentation via Learnable Sobel Convolution"
- "Efficient Text-to-Image Retrieval via Cross-Modal Feature Alignment"

Best for: Papers where the mechanism is the story, not the method name.

### Pattern 3: Problem-Aware
```
[Problem Statement]: A [Method-Type] Approach
```
Examples:
- "Addressing Fine-Grained Boundary Errors in Semantic Segmentation: A Directional Consistency Approach"
- "Closing the Gap Between Vision and Language: A Contrastive Pretraining Framework"

Best for: Papers addressing a well-recognized problem.

### Pattern 4: Task-Specific
```
[Adjective] [Task] with [Key Technique]
```
Examples:
- "Boundary-Aware Semantic Segmentation with Directional Consistency Constraints"
- "Efficient Object Detection with Learned Region Proposals"

Best for: Incremental but solid contributions.

### Pattern 5: Colon-Separated (Method: What-How)
```
[Short Catchy Name]: [Descriptive Subtitle Explaining the Method]
```
Examples:
- "Mask R-CNN: A Unified Framework for Object Instance Segmentation"
- "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"

Best for: Papers introducing a fundamental method that will be widely cited.

### Pattern 6: Question-Based (Rare, but Effective)
```
[Question]?
```
Examples:
- "Do Vision Transformers See Like Convolutional Neural Networks?"
- "How Much Does Attention Actually Attend?"

Best for: Analysis papers, not method papers. Use with caution.

### Pattern 7: Verb-Led
```
[Verb] [Task] via [Mechanism]
```
Examples:
- "Improving Semantic Segmentation by Directional Boundary Modeling"
- "Learning Transferable Visual Representations with Contrastive Pretraining"

### Pattern 8: Component-Focused
```
[Key Component]: A [Type] for [Task]
```
Examples:
- "Directional Consistency Loss: A Geometry-Aware Regularizer for Boundary-Sensitive Segmentation"

---

## Domain-Specific Title Conventions

| Domain | Convention | Typical Length |
|--------|-----------|----------------|
| CV | Short, descriptive, method name + task. Often colon-separated. | 8-15 words |
| NLP | Method name prominent. Task often in subtitle after colon. | 10-18 words |
| ML (Theory) | Problem statement, formalism hinted in title. Method name secondary. | 8-14 words |
| Systems / HPC | Problem solved + key technique. Practical framing. | 10-16 words |
| Multimodal | Both modalities named. "for", "via", or "with" as connector. | 10-16 words |

---

## Title Evaluation Criteria

Rate your title on these 4 dimensions (1-5 each):

| Criterion | Question | 1 (Bad) | 5 (Good) |
|-----------|----------|---------|----------|
| Informativeness | Does the title tell you what the paper does? | "A Novel Method for Image Analysis" | "SABR: Structure-Aware Boundary Refinement for Semantic Segmentation" |
| Specificity | Can you tell what the technical contribution is? | "Improving Neural Networks" | "Directional Consistency Modeling for Boundary-Aware Semantic Segmentation" |
| Memorability | Would you remember this title tomorrow? | Generic, forgettable | Distinctive method name or concept |
| Searchability | Will researchers in the field find this paper? | Missing key task/method terms | Contains task, method, and technique keywords |

Target: 4+ on informativeness and specificity. 3+ on memorability and searchability.

---

## Common Title Problems

| Problem | Example | Fix |
|---------|---------|-----|
| Vague | "A Novel Approach to Image Understanding" | Specify the approach and the task |
| Overclaiming | "A Novel State-of-the-Art Method for Robust and Efficient..." | Remove "novel", "state-of-the-art", "robust" unless proven |
| Colon abuse | "Method: A Novel Approach: Using Attention: for Segmentation" | One colon maximum. Two in extreme cases (method name: subtitle). |
| Too long | >18 words, multiple clauses, hard to parse | Cut to core: Method + Task + one distinguishing feature |
| Too short | "On Image Segmentation" | Add what about image segmentation — the method, the problem, the finding? |
| Buzzword stuffing | "Deep Learning Transformer Attention Multi-Scale Fusion..." | Pick the 2-3 most important technical terms |

## Rules

Avoid titles that claim "novel", "efficient", or "robust" unless the paper strongly supports those claims. The title is the first thing a reviewer sees — if it overclaims, they start skeptical.
