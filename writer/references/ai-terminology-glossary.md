# AI Bilingual Terminology Glossary

Maintain consistency: every Chinese technical term maps to exactly one English term throughout the manuscript. On first use in the Chinese draft, include the English term in parentheses. On first use in the English draft, include only the English term.

---

## Architecture & Model Components

| 中文 | English |
|---|---|
| 主干网络 | backbone network |
| 特征提取器 | feature extractor |
| 特征融合 | feature fusion |
| 多尺度特征 | multi-scale features |
| 编码器 | encoder |
| 解码器 | decoder |
| 瓶颈层 | bottleneck layer |
| 跳跃连接 | skip connection |
| 残差块 | residual block |
| 残差连接 | residual connection |
| 特征金字塔 | feature pyramid |
| 特征金字塔网络 | Feature Pyramid Network (FPN) |
| 检测头 | detection head |
| 分割头 | segmentation head |
| 分类头 | classification head |
| 投影头 | projection head |
| 颈部 | neck |
| 区域提议网络 | Region Proposal Network (RPN) |

---

## Attention & Transformer

| 中文 | English |
|---|---|
| 注意力机制 | attention mechanism |
| 自注意力 | self-attention |
| 交叉注意力 | cross-attention |
| 多头注意力 | multi-head attention |
| 缩放点积注意力 | scaled dot-product attention |
| 前馈网络 | feed-forward network (FFN) |
| 位置编码 | positional encoding |
| 可学习位置编码 | learned positional encoding |
| 正弦位置编码 | sinusoidal positional encoding |
| 层归一化 | layer normalization |
| 视觉Transformer | Vision Transformer (ViT) |
| 注意力图 | attention map |
| 查询/键/值 | query / key / value (Q/K/V) |

---

## Training & Optimization

| 中文 | English |
|---|---|
| 损失函数 | loss function / objective |
| 训练目标 | training objective |
| 学习率 | learning rate |
| 权重衰减 | weight decay |
| 梯度裁剪 | gradient clipping |
| 预热 | warmup |
| 余弦退火 | cosine annealing |
| 知识蒸馏 | knowledge distillation |
| 数据增强 | data augmentation |
| 早停 | early stopping |
| 批归一化 | batch normalization |
| 实例归一化 | instance normalization |
| 组归一化 | group normalization |
| 随机失活 | dropout |
| 标签平滑 | label smoothing |
| 混合精度训练 | mixed-precision training |
| 梯度累积 | gradient accumulation |

---

## CV-Specific

| 中文 | English |
|---|---|
| 语义分割 | semantic segmentation |
| 实例分割 | instance segmentation |
| 全景分割 | panoptic segmentation |
| 目标检测 | object detection |
| 图像分类 | image classification |
| 边界框 | bounding box |
| 锚框 | anchor box |
| 非极大值抑制 | non-maximum suppression (NMS) |
| 交并比 | Intersection over Union (IoU) |
| 均交并比 | mean Intersection over Union (mIoU) |
| 平均精度 | Average Precision (AP) |
| 均平均精度 | mean Average Precision (mAP) |
| 感受野 | receptive field |
| 下采样 | downsampling |
| 上采样 | upsampling |
| 双线性插值 | bilinear interpolation |
| 转置卷积 | transposed convolution |
| 空洞卷积 | dilated convolution / atrous convolution |
| 可变形卷积 | deformable convolution |
| 深度可分离卷积 | depthwise separable convolution |

---

## NLP-Specific

| 中文 | English |
|---|---|
| 命名实体识别 | named entity recognition (NER) |
| 文本分类 | text classification |
| 情感分析 | sentiment analysis |
| 机器翻译 | machine translation |
| 文本摘要 | text summarization |
| 问答系统 | question answering |
| 分词 | tokenization |
| 词嵌入 | word embedding |
| 上下文嵌入 | contextual embedding |
| 因果掩码 | causal masking |
| 束搜索 | beam search |
| 困惑度 | perplexity |
| 双语评估替补 | BLEU |
| 前缀调优 | prefix tuning |
| 低秩适应 | Low-Rank Adaptation (LoRA) |
| 提示工程 | prompt engineering |
| 上下文学习 | in-context learning |
| 思维链 | chain-of-thought |

---

## Multimodal Learning

| 中文 | English |
|---|---|
| 多模态学习 | multimodal learning |
| 视觉-语言对齐 | vision-language alignment |
| 跨模态融合 | cross-modal fusion |
| 图文检索 | image-text retrieval |
| 视觉问答 | visual question answering (VQA) |
| 图文生成 | image captioning / text-to-image generation |
| 指令微调 | instruction tuning |
| 视觉指令微调 | visual instruction tuning |
| 多模态大语言模型 | multimodal large language model (MLLM) |

---

## Evaluation & Metrics

| 中文 | English |
|---|---|
| 评价指标 | evaluation metric |
| 基线方法 | baseline method |
| 最先进方法 | state-of-the-art method (use cautiously — see forbidden-overclaims.md) |
| 消融实验 | ablation study |
| 鲁棒性 | robustness |
| 泛化能力 | generalization ability |
| 过拟合 | overfitting |
| 欠拟合 | underfitting |
| 标准差 | standard deviation |
| 置信区间 | confidence interval |
| 统计显著性 | statistical significance |
| 超参数 | hyperparameter |
| 计算复杂度 | computational complexity |
| 浮点运算数 | FLOPs |
| 推理时间 | inference time / latency |
| 吞吐量 | throughput |
| 参数量 | number of parameters / parameter count |

---

## Paper Writing

| 中文 | English |
|---|---|
| 贡献 | contribution |
| 创新点 | innovation / novelty |
| 相关工作 | related work |
| 未来工作 | future work |
| 局限性 | limitation |
| 摘要 | abstract |
| 引言 | introduction |
| 方法 | method / proposed method |
| 实验 | experiments |
| 结论 | conclusion |
| 讨论 | discussion |
| 附录 | appendix |
| 补充材料 | supplementary material |

---

## Commonly Confused Pairs

| 中文 | 易混淆的英文翻译 | 正确用法 |
|------|----------------|---------|
| 精度 | precision vs. accuracy vs. performance | precision = 查准率; accuracy = 准确率; 泛指时用 performance |
| 准确率 | accuracy | accuracy = 正确分类的比例 |
| 精确率 | precision | precision = TP / (TP + FP) |
| 召回率 | recall | recall = TP / (TP + FN) |
| 模型 | model vs. method vs. approach | model = trained weights; method/approach = algorithm + design |
| 方案 | solution vs. scheme vs. approach | 学术论文中 prefer approach/method 而非 scheme |
| 框架 | framework vs. architecture | framework = software system; architecture = network design |
| 结构 | structure vs. architecture | structure = general organization; architecture = specific network design |
| 模块 | module vs. component | module = sub-network with defined interface; component = any part |
| 机制 | mechanism vs. scheme | mechanism = principled process; scheme = plan (less formal) |
