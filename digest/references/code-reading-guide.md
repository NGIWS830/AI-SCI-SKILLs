# Code and Material Reading Guide

## Systematic File Reading Order

### Tier 1: Project-Level Understanding (Read First)
- `README.md`, `README_EN.md` — project overview, installation, usage
- `requirements.txt`, `environment.yml`, `pyproject.toml`, `setup.py` — dependencies
- `Makefile`, `Dockerfile` — build and run procedures
- Top-level config files (`config.yaml`, `config.json`, `*.toml`)

### Tier 2: Entry Points (Understand the Pipeline)
- `train.py`, `main.py`, `run.py` — training entry point
- `test.py`, `eval.py`, `inference.py` — evaluation and inference
- `scripts/` directory — utility and helper scripts
- `configs/` directory — experiment configurations

### Tier 3: Core Implementation (Extract Method Details)
- `models/`, `networks/`, `modules/` — architecture definitions
- `losses/`, `criterions/` — loss functions and objectives
- `datasets/`, `data/`, `dataloaders/` — data loading and preprocessing
- `layers/`, `ops/`, `blocks/` — custom layers and operations

### Tier 4: Supporting Code
- `utils/`, `tools/` — utility functions
- `metrics/`, `evaluation/` — metric implementations
- `checkpoints/`, `logs/`, `outputs/` — results and artifacts

---

## Architecture Pattern Recognition

### CNN-Based Architectures
**Signs to look for:**
- `nn.Conv2d`, `nn.ConvTranspose2d`
- `nn.MaxPool2d`, `nn.AdaptiveAvgPool2d`
- BatchNorm (`nn.BatchNorm2d`), InstanceNorm
- Residual blocks (`class ResidualBlock(nn.Module)`)
- Feature pyramid structures (`class FPN`, multi-scale feature maps)

**What to extract:**
- Backbone model (e.g., ResNet-50, EfficientNet-B3)
- Number of layers, channels per stage
- Skip connection topology
- Downsampling/upsampling strategy

### Transformer-Based Architectures
**Signs to look for:**
- `nn.MultiheadAttention`, custom `attention()` functions
- `PositionalEncoding` class or `nn.Parameter` for position embeddings
- LayerNorm (`nn.LayerNorm`), not BatchNorm
- `nn.TransformerEncoder`, `nn.TransformerDecoder`
- Self-attention and cross-attention patterns

**What to extract:**
- Number of attention heads, head dimension
- Position encoding type (sinusoidal, learned, relative, RoPE)
- Encoder/decoder layer count
- Feed-forward expansion ratio

### Hybrid Architectures
**Signs to look for:**
- Both CNN and transformer components
- CNN backbone + transformer neck/head
- Convolutional token embedding (e.g., patch embedding via Conv2d)
- Multi-scale + attention fusion

**What to extract:**
- Where the CNN→Transformer transition happens
- How multi-scale features are injected into attention

### MLP / Other Architectures
**Signs to look for:**
- MLP-Mixer-style channel + spatial mixing
- State-space models (Mamba, S4)
- Graph neural networks (`dgl`, `torch_geometric`)

---

## Custom Module Identification

Distinguish custom code from library calls:

**Custom (potential contribution):**
- `class X(nn.Module)` defined in the project's `models/` or `modules/`
- Functions decorated with `@torch.jit.script` or custom CUDA kernels
- Novel loss function classes (`class CustomLoss(nn.Module)`)

**Library (not a contribution):**
- `torchvision.models.resnet50(pretrained=True)`
- `nn.CrossEntropyLoss()`, `nn.MSELoss()`
- HuggingFace model imports (`AutoModel.from_pretrained(...)`)
- Standard optimizers (`torch.optim.AdamW`)

**When a library call is wrapped:** A `class MyResNet(nn.Module)` that only calls `torchvision.models.resnet50()` internally is NOT a contribution. The wrapping is infrastructure.

---

## Hyperparameter Extraction Guide

Look for hyperparameters in these locations:

1. **argparse / click definitions** in `train.py`, `main.py`:
   ```python
   parser.add_argument('--lr', type=float, default=1e-3)
   parser.add_argument('--batch-size', type=int, default=32)
   ```

2. **YAML/JSON config files** in `configs/`:
   ```yaml
   optimizer:
     name: AdamW
     lr: 1e-3
     weight_decay: 0.01
   ```

3. **Hardcoded constants** in model/loss files:
   ```python
   TEMPERATURE = 0.07
   EPSILON = 1e-6
   ```

4. **Shell scripts** in `scripts/` or `experiments/`:
   ```bash
   python train.py --lr 1e-3 --batch-size 32 --epochs 200
   ```

---

## Contribution Candidate Spotting

What makes a potential contribution:

| Type | Signal in Code | Paper Value |
|------|---------------|-------------|
| **Novel architecture** | Custom `nn.Module` subclass with non-trivial forward() | Method contribution |
| **Novel loss function** | Custom loss class, novel regularization term | Training contribution |
| **Novel training strategy** | Custom training loop, multi-stage schedule, curriculum | Algorithmic contribution |
| **Novel data processing** | Custom dataset class with non-trivial transforms | Data/methodology |
| **Novel application** | Standard method applied to new domain | Application contribution |
| **System optimization** | Custom CUDA kernels, memory optimizations | Systems contribution |

**Contribution quality signals:**
- The custom code is substantial (>50 lines of novel logic)
- The design has a clear motivation (comments, docstrings, related work section in README)
- The method is ablated or compared against alternatives
- The module has a meaningful name (not `Module1`, `BlockA`, `Untitled`)

---

## Extract

From the materials, extract:
- **Task**: classification, detection, segmentation, retrieval, generation, QA, summarization, NER, RAG, multimodal reasoning, etc.
- **Inputs and outputs**: Data format, dimensions, preprocessing.
- **Backbone and key modules**: Architecture type, novel components.
- **Training objective and loss terms**: Multi-component losses, their weights.
- **Datasets and preprocessing**: Names, splits, augmentation.
- **Baselines and evaluation metrics**: With metric directions.
- **Claims that can be supported**: What the code + results actually demonstrate.

## Red Flags

- Method described in notes but absent from code → mark as `AUTHOR_INPUT_NEEDED`.
- Results table without dataset split or metric direction → flag for Stage 3.
- Baselines without implementation source → harder to reproduce; note this.
- Hyperparameters missing from config → reproducibility at risk.
- Claims of SOTA without verified comparison → overclaim risk for Stage 3/4.
- Code has no license → flag for author.
- Hardcoded paths → the code may not run outside the author's machine.
