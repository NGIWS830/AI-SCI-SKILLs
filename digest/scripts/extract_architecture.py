#!/usr/bin/env python3
"""Deep code analysis: extract architecture, loss functions, and hyperparameters.

Usage:
    python extract_architecture.py /path/to/repo --output arch_report.md
    python extract_architecture.py /path/to/repo --output arch_report.json --format json

Extracts:
    1. All nn.Module / flax.linen.Module / tf.keras.Model subclasses
    2. Loss function definitions with forward() logic
    3. Hyperparameters from argparse, click, OmegaConf, dataclasses
    4. Framework detection and version inference
    5. Module dependency graph (which module imports which)
    6. Training infrastructure (optimizer, scheduler, mixed precision)
    7. Data pipeline overview
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


DEFAULT_IGNORE = {".git", "__pycache__", ".ipynb_checkpoints", "wandb", "runs",
                   "checkpoints", "outputs", "dist", "build", ".venv", "venv",
                   "node_modules", ".eggs", "*.egg-info", "logs"}


# ── AST Visitors ──────────────────────────────────────────────────────────────────

class ModuleExtractor(ast.NodeVisitor):
    """Extract PyTorch nn.Module, Flax linen.Module, Keras Model subclasses."""

    def __init__(self, source_file=""):
        self.modules = []
        self.source_file = source_file

    def visit_ClassDef(self, node):
        for base in node.bases:
            base_name = self._name_str(base)
            if base_name in ("nn.Module", "Module", "torch.nn.Module",
                             "nn.Module", "flax.linen.Module", "linen.Module",
                             "tf.keras.Model", "keras.Model",
                             "pl.LightningModule", "LightningModule",
                             "pl.LightningDataModule", "LightningDataModule",
                             "torch.utils.data.Dataset", "Dataset"):
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append({
                            "name": item.name,
                            "lineno": item.lineno,
                            "args": [a.arg for a in item.args.args],
                            "decorators": [self._name_str(d) for d in item.decorator_list],
                        })
                # Count nn submodules (self.X = nn.Sequential / nn.Conv2d / ...)
                submodules = []
                forward_body = ""
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == "forward":
                        forward_body = ast.get_source_segment(self._source_code, item) if self._source_code else ""
                    if isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == "self":
                                sub_name = target.attr
                                if isinstance(item.value, ast.Call):
                                    sub_type = self._name_str(item.value.func)
                                    submodules.append({"name": sub_name, "type": sub_type})

                self.modules.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "file": self.source_file,
                    "base_class": base_name,
                    "methods": methods,
                    "n_methods": len(methods),
                    "submodules": submodules,
                    "n_submodules": len(submodules),
                    "has_forward": any(m["name"] == "forward" for m in methods),
                    "forward_snippet": forward_body[:500] if forward_body else "",
                })
        self.generic_visit(node)

    def _name_str(self, node):
        if node is None:
            return ""
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return f"{self._name_str(node.value)}.{node.attr}"
        if isinstance(node, ast.Call):
            return self._name_str(node.func)
        return ""


class LossExtractor(ast.NodeVisitor):
    """Extract loss function classes and functions."""

    LOSS_KEYWORDS = {"loss", "Loss", "criterion", "objective", "cost", "error"}
    LOSS_PATTERNS = [
        r"nn\.\w+Loss",
        r"F\.\w+_loss",
        r"torch\.nn\.functional\.\w+_loss",
    ]

    def __init__(self, source_file="", source_code=""):
        self.losses = []
        self.source_file = source_file
        self._source_code = source_code

    def visit_ClassDef(self, node):
        # Check if class name or base class suggests a loss
        is_loss = any(kw in node.name for kw in self.LOSS_KEYWORDS)
        for base in node.bases:
            if any(kw in self._name_str(base) for kw in ("Loss", "Criterion", "Objective")):
                is_loss = True
        if not is_loss:
            self.generic_visit(node)
            return

        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                body_str = ""
                if self._source_code:
                    try:
                        body_str = ast.get_source_segment(self._source_code, item) or ""
                    except Exception:
                        pass
                methods.append({
                    "name": item.name,
                    "lineno": item.lineno,
                    "body_snippet": body_str[:300],
                })

        self.losses.append({
            "type": "class",
            "name": node.name,
            "file": self.source_file,
            "lineno": node.lineno,
            "methods": methods,
        })

    def visit_FunctionDef(self, node):
        if any(kw in node.name for kw in self.LOSS_KEYWORDS):
            body_str = ""
            if self._source_code:
                try:
                    body_str = ast.get_source_segment(self._source_code, node) or ""
                except Exception:
                    pass
            self.losses.append({
                "type": "function",
                "name": node.name,
                "file": self.source_file,
                "lineno": node.lineno,
                "body_snippet": body_str[:300],
            })
        self.generic_visit(node)

    def _name_str(self, node):
        if node is None:
            return ""
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return f"{self._name_str(node.value)}.{node.attr}"
        return ""


class HyperparamExtractor(ast.NodeVisitor):
    """Extract hyperparameters from argparse, dataclass configs, and constants."""

    HP_KEYWORDS = {
        "lr", "learning_rate", "learning rate", "batch_size", "batch size",
        "epochs", "num_epochs", "weight_decay", "weight decay",
        "dropout", "temperature", "tau", "hidden_dim", "hidden_size",
        "embedding_dim", "num_heads", "num_layers", "warmup", "warmup_steps",
        "max_length", "image_size", "patch_size", "optimizer", "scheduler",
        "momentum", "beta1", "beta2", "eps", "epsilon",
    }

    def __init__(self, source_file=""):
        self.hyperparams = []
        self.source_file = source_file

    def visit_Call(self, node):
        # argparse: parser.add_argument('--lr', type=float, default=1e-3)
        func_name = self._name_str(node.func)
        if "add_argument" in func_name:
            args = []
            kwargs = {}
            for arg in node.args:
                if isinstance(arg, ast.Constant):
                    args.append(arg.value)
            for kw in node.keywords:
                if isinstance(kw.value, ast.Constant):
                    kwargs[kw.arg] = kw.value
                elif isinstance(kw.value, ast.UnaryOp) and isinstance(kw.value.operand, ast.Constant):
                    kwargs[kw.arg] = -kw.value.operand.value

            param_name = ""
            for a in args:
                a_str = str(a)
                if a_str.startswith("--"):
                    param_name = a_str[2:].replace("-", "_")
                elif a_str.startswith("-") and len(a_str) == 2:
                    param_name = a_str[1:]

            if param_name and any(kw in param_name.lower() for kw in self.HP_KEYWORDS):
                self.hyperparams.append({
                    "name": param_name,
                    "type": "argparse",
                    "file": self.source_file,
                    "lineno": node.lineno,
                    "default": kwargs.get("default"),
                    "help": kwargs.get("help", ""),
                })

        # OmegaConf / dataclass: lr: float = 1e-3 (via AnnAssign)
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        if isinstance(node.target, ast.Name):
            name = node.target.id
            if any(kw in name.lower() for kw in self.HP_KEYWORDS):
                default = None
                if isinstance(node.value, ast.Constant):
                    default = node.value.value
                elif isinstance(node.value, ast.UnaryOp) and isinstance(node.value.operand, ast.Constant):
                    default = -node.value.operand.value
                self.hyperparams.append({
                    "name": name,
                    "type": "dataclass/config",
                    "file": self.source_file,
                    "lineno": node.lineno,
                    "default": default,
                    "annotation": self._name_str(node.annotation),
                })

    def visit_Assign(self, node):
        # Constants: TEMPERATURE = 0.07, LEARNING_RATE = 1e-3
        for target in node.targets:
            if isinstance(target, ast.Name):
                name = target.id
                if any(kw in name.lower() for kw in self.HP_KEYWORDS) or name.isupper():
                    val = None
                    if isinstance(node.value, ast.Constant):
                        val = node.value.value
                    elif isinstance(node.value, ast.Num):
                        val = node.value.n
                    if val is not None:
                        self.hyperparams.append({
                            "name": name,
                            "type": "constant",
                            "file": self.source_file,
                            "lineno": node.lineno,
                            "default": val,
                            "annotation": "",
                        })
        self.generic_visit(node)

    def _name_str(self, node):
        if node is None:
            return ""
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return f"{self._name_str(node.value)}.{node.attr}"
        if isinstance(node, ast.Call):
            return self._name_str(node.func)
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        return ""


class ImportVisitor(ast.NodeVisitor):
    """Extract library imports to detect framework and dependencies."""

    def __init__(self):
        self.imports = set()
        self.from_imports = defaultdict(set)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name.split(".")[0])
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            top = node.module.split(".")[0]
            self.from_imports[top].add(node.module)
        self.generic_visit(node)


# ── Framework Detection ───────────────────────────────────────────────────────────

def detect_framework(imports, from_imports):
    """Detect ML framework from imports."""
    frameworks = []

    if "torch" in imports or "torch" in from_imports:
        torch_mods = from_imports.get("torch", set())
        version_hints = []
        if any("torch.cuda.amp" in m for m in torch_mods):
            version_hints.append(">=1.6 (AMP support)")
        if any("torch.distributed" in m for m in torch_mods):
            version_hints.append("distributed training")
        frameworks.append({
            "framework": "PyTorch",
            "modules": sorted(torch_mods)[:10],
            "version_hints": version_hints,
        })

    if "pytorch_lightning" in from_imports or "lightning" in from_imports:
        frameworks.append({"framework": "PyTorch Lightning", "modules": sorted(from_imports.get("pytorch_lightning", from_imports.get("lightning", [])))[:5], "version_hints": []})

    if "jax" in imports or "jax" in from_imports:
        frameworks.append({"framework": "JAX", "modules": sorted(from_imports.get("jax", []))[:5], "version_hints": []})

    if "flax" in from_imports:
        frameworks.append({"framework": "Flax (JAX NN library)", "modules": sorted(from_imports.get("flax", []))[:5], "version_hints": []})

    if "tensorflow" in imports or "tensorflow" in from_imports:
        frameworks.append({"framework": "TensorFlow", "modules": sorted(from_imports.get("tensorflow", []))[:5], "version_hints": []})

    if "transformers" in from_imports:
        frameworks.append({"framework": "HuggingFace Transformers", "modules": sorted(from_imports.get("transformers", []))[:10], "version_hints": []})

    if "diffusers" in from_imports:
        frameworks.append({"framework": "HuggingFace Diffusers", "modules": sorted(from_imports.get("diffusers", []))[:5], "version_hints": []})

    if "timm" in imports or "timm" in from_imports:
        frameworks.append({"framework": "timm (PyTorch Image Models)", "modules": [], "version_hints": []})

    return frameworks


# ── Training Infrastructure Detection ──────────────────────────────────────────────

def detect_training_infra(source_code, filepath):
    """Detect optimizer, scheduler, mixed precision, and distributed training setup."""
    infra = {
        "optimizer": [],
        "scheduler": [],
        "mixed_precision": False,
        "distributed": False,
        "early_stopping": False,
        "checkpointing": False,
        "logging": [],
    }

    optimizer_patterns = [
        (r"torch\.optim\.(\w+)", "PyTorch"),
        (r"optim\.(\w+)", "PyTorch"),
        (r"AdamW?", "PyTorch"),
        (r"SGD", "PyTorch"),
        (r"optax\.(\w+)", "JAX/optax"),
        (r"tf\.keras\.optimizers\.(\w+)", "TensorFlow"),
    ]
    for pattern, framework in optimizer_patterns:
        for m in re.finditer(pattern, source_code):
            name = m.group(1) if m.lastindex else m.group(0)
            if name not in [o["name"] for o in infra["optimizer"]]:
                infra["optimizer"].append({"name": name, "framework": framework})

    scheduler_patterns = [
        (r"(CosineAnnealing\w*)", ""),
        (r"(StepLR)", ""),
        (r"(ReduceLROnPlateau)", ""),
        (r"(OneCycleLR)", ""),
        (r"(cosine|linear)_\w*schedule", ""),
        (r"(warmup|WarmUp|warm_up)", ""),
    ]
    for pattern, _ in scheduler_patterns:
        for m in re.finditer(pattern, source_code, re.IGNORECASE):
            if m.group(1) not in infra["scheduler"]:
                infra["scheduler"].append(m.group(1))

    if re.search(r"torch\.cuda\.amp|autocast|GradScaler|mixed.precision|FP16|BF16|float16|bfloat16", source_code):
        infra["mixed_precision"] = True

    if re.search(r"DistributedDataParallel|DDP|distributed\.init|torch\.distributed|horovod|deepspeed|fsdp", source_code):
        infra["distributed"] = True

    if re.search(r"EarlyStopping|early_stopping", source_code):
        infra["early_stopping"] = True

    if re.search(r"ModelCheckpoint|save_checkpoint|torch\.save|checkpoint", source_code):
        infra["checkpointing"] = True

    if re.search(r"wandb|tensorboard|TensorBoard|mlflow|neptune|comet", source_code):
        for m in re.finditer(r"(wandb|tensorboard|TensorBoard|mlflow|neptune|comet)", source_code):
            infra["logging"].append(m.group(0))

    return infra


# ── Main Scan ─────────────────────────────────────────────────────────────────────

def scan_repository(repo_path, max_files=200):
    """Full scan of an AI project repository."""
    root = Path(repo_path).resolve()
    if not root.exists():
        return {"error": f"Path not found: {repo_path}"}

    py_files = []
    config_files = []
    doc_files = []

    for p in sorted(root.rglob("*")):
        if any(part in DEFAULT_IGNORE for part in p.parts):
            continue
        if p.is_file():
            if p.suffix == ".py":
                py_files.append(p)
                if len(py_files) >= max_files:
                    break
            elif p.suffix in (".yaml", ".yml", ".json", ".toml"):
                config_files.append(p)
            elif p.suffix in (".md", ".txt", ".rst") and p.name in ("README.md", "requirements.txt"):
                doc_files.append(p)

    # Scan Python files
    all_modules = []
    all_losses = []
    all_hyperparams = []
    all_imports = set()
    all_from_imports = defaultdict(set)
    training_infra_list = []

    for py_file in py_files[:max_files]:
        try:
            source = py_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue

        # Extract modules
        extractor = ModuleExtractor(str(py_file.relative_to(root)))
        extractor._source_code = source
        extractor.visit(tree)
        all_modules.extend(extractor.modules)

        # Extract losses
        loss_extractor = LossExtractor(str(py_file.relative_to(root)), source)
        loss_extractor.visit(tree)
        all_losses.extend(loss_extractor.losses)

        # Extract hyperparams
        hp_extractor = HyperparamExtractor(str(py_file.relative_to(root)))
        hp_extractor.visit(tree)
        all_hyperparams.extend(hp_extractor.hyperparams)

        # Extract imports
        imp_visitor = ImportVisitor()
        imp_visitor.visit(tree)
        all_imports.update(imp_visitor.imports)
        for k, v in imp_visitor.from_imports.items():
            all_from_imports[k].update(v)

        # Training infrastructure
        infra = detect_training_infra(source, py_file.relative_to(root))
        if any(v for v in infra.values() if v):
            infra["file"] = str(py_file.relative_to(root))
            training_infra_list.append(infra)

    # Framework detection
    frameworks = detect_framework(all_imports, all_from_imports)

    # Merge training infra across files
    merged_infra = {
        "optimizer": [],
        "scheduler": [],
        "mixed_precision": False,
        "distributed": False,
        "early_stopping": False,
        "checkpointing": False,
        "logging": [],
    }
    for infra in training_infra_list:
        merged_infra["optimizer"].extend(infra["optimizer"])
        merged_infra["scheduler"].extend(infra["scheduler"])
        merged_infra["mixed_precision"] = merged_infra["mixed_precision"] or infra["mixed_precision"]
        merged_infra["distributed"] = merged_infra["distributed"] or infra["distributed"]
        merged_infra["early_stopping"] = merged_infra["early_stopping"] or infra["early_stopping"]
        merged_infra["checkpointing"] = merged_infra["checkpointing"] or infra["checkpointing"]
        merged_infra["logging"].extend(infra["logging"])
    merged_infra["optimizer"] = list({o["name"]: o for o in merged_infra["optimizer"]}.values())
    merged_infra["scheduler"] = list(set(merged_infra["scheduler"]))
    merged_infra["logging"] = list(set(merged_infra["logging"]))

    return {
        "repo": str(root),
        "n_py_files": len(py_files),
        "n_config_files": len(config_files),
        "frameworks": frameworks,
        "modules": all_modules,
        "n_modules": len(all_modules),
        "losses": all_losses,
        "n_losses": len(all_losses),
        "hyperparameters": all_hyperparams,
        "n_hyperparams": len(all_hyperparams),
        "imports": sorted(all_imports),
        "from_imports": {k: sorted(v)[:10] for k, v in sorted(all_from_imports.items())},
        "training_infrastructure": merged_infra,
    }


# ── Output Formatting ──────────────────────────────────────────────────────────────

def format_markdown(scan_result):
    """Format scan results as markdown report."""
    lines = [
        "# Architecture & Code Analysis Report",
        "",
        f"**Repository:** `{scan_result['repo']}`",
        f"**Python files scanned:** {scan_result['n_py_files']}",
        f"**Config files found:** {scan_result['n_config_files']}",
        "",
    ]

    # Frameworks
    lines.append("## Detected Frameworks")
    lines.append("")
    for fw in scan_result["frameworks"]:
        lines.append(f"- **{fw['framework']}**")
        if fw.get("version_hints"):
            for hint in fw["version_hints"]:
                lines.append(f"  - {hint}")
        if fw.get("modules"):
            lines.append(f"  - Modules: {', '.join(fw['modules'])}")
    if not scan_result["frameworks"]:
        lines.append("- No major ML framework detected.")

    # Training Infrastructure
    infra = scan_result["training_infrastructure"]
    lines.extend([
        "",
        "## Training Infrastructure",
        "",
    ])
    if infra["optimizer"]:
        lines.append("**Optimizers detected:**")
        for o in infra["optimizer"]:
            lines.append(f"- `{o['name']}` ({o['framework']})")
    if infra["scheduler"]:
        lines.append(f"**LR Schedulers:** {', '.join(f'`{s}`' for s in infra['scheduler'])}")
    lines.append(f"**Mixed Precision (AMP/FP16/BF16):** {'Yes' if infra['mixed_precision'] else 'Not detected'}")
    lines.append(f"**Distributed Training (DDP/FSDP/DeepSpeed):** {'Yes' if infra['distributed'] else 'Not detected'}")
    lines.append(f"**Early Stopping:** {'Yes' if infra['early_stopping'] else 'Not detected'}")
    lines.append(f"**Model Checkpointing:** {'Yes' if infra['checkpointing'] else 'Not detected'}")
    if infra["logging"]:
        lines.append(f"**Experiment Logging:** {', '.join(infra['logging'])}")

    # Architecture Modules
    lines.extend([
        "",
        "## Custom Modules (nn.Module / Flax Module / Keras Model)",
        "",
        f"**Total custom modules found:** {scan_result['n_modules']}",
        "",
    ])
    if scan_result["modules"]:
        lines.append("| # | Module | File | Base Class | Methods | Submodules | Has forward() |")
        lines.append("|---|--------|------|------------|---------|------------|--------------|")
        for i, mod in enumerate(scan_result["modules"], 1):
            method_names = ", ".join(m["name"] for m in mod["methods"][:6])
            if len(mod["methods"]) > 6:
                method_names += f" ... (+{len(mod['methods'])-6})"
            sub_names = ", ".join(s["name"] for s in mod["submodules"][:5])
            if len(mod["submodules"]) > 5:
                sub_names += f" ... (+{len(mod['submodules'])-5})"
            lines.append(
                f"| {i} | `{mod['name']}` | `{mod['file']}`:{mod['lineno']} | {mod['base_class']} "
                f"| {method_names} | {sub_names or '—'} | {'✓' if mod['has_forward'] else '✗'} |"
            )
    else:
        lines.append("No custom neural network modules found.")

    # Loss Functions
    lines.extend([
        "",
        "## Loss Functions",
        "",
        f"**Loss functions/classes detected:** {scan_result['n_losses']}",
        "",
    ])
    if scan_result["losses"]:
        for loss in scan_result["losses"]:
            lines.append(f"### `{loss['name']}` ({loss['type']}) — `{loss['file']}`:{loss['lineno']}")
            lines.append("")
            for m in loss.get("methods", []):
                lines.append(f"- **{m['name']}()**:")
                snippet = m.get("body_snippet", "").strip()
                if snippet:
                    lines.append("```python")
                    lines.append(snippet)
                    lines.append("```")
                    lines.append("")
    else:
        lines.append("No custom loss functions detected (likely using standard torch.nn losses).")

    # Hyperparameters
    lines.extend([
        "",
        "## Extracted Hyperparameters",
        "",
        f"**Total hyperparameters found:** {scan_result['n_hyperparams']}",
        "",
    ])
    if scan_result["hyperparameters"]:
        lines.append("| Name | Type | Default | File |")
        lines.append("|------|------|---------|------|")
        for hp in scan_result["hyperparameters"]:
            lines.append(f"| `{hp['name']}` | {hp['type']} | `{hp['default']}` | `{hp['file']}`:{hp['lineno']} |")

    # Key libraries
    lines.extend([
        "",
        "## Key Library Dependencies",
        "",
    ])
    ml_imports = {"torch", "tensorflow", "jax", "transformers", "diffusers", "datasets",
                  "numpy", "scipy", "sklearn", "pandas", "PIL", "cv2", "timm",
                  "einops", "accelerate", "deepspeed", "optax", "flax"}
    imports_set = set(scan_result["imports"])
    detected_ml = sorted(imports_set & ml_imports)
    other_imports = sorted(imports_set - ml_imports)
    if detected_ml:
        lines.append("**ML-relevant imports:** " + ", ".join(f"`{i}`" for i in detected_ml))
    if other_imports:
        lines.append("**Other imports:** " + ", ".join(f"`{i}`" for i in other_imports[:20]))
        if len(other_imports) > 20:
            lines.append(f"  ... and {len(other_imports) - 20} more")

    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Deep analysis: extract architecture, loss functions, and hyperparameters from AI project code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python extract_architecture.py /path/to/repo --output arch_report.md
  python extract_architecture.py /path/to/repo --format json --output arch_report.json
  python extract_architecture.py /path/to/repo --max-files 500 --output full_scan.md
        """,
    )
    parser.add_argument("repo", help="Path to the AI project repository")
    parser.add_argument("--output", "-o", default="arch_report.md", help="Output file path")
    parser.add_argument("--format", "-f", default="markdown", choices=["markdown", "json"],
                        help="Output format (default: markdown)")
    parser.add_argument("--max-files", type=int, default=200, help="Max Python files to scan")
    args = parser.parse_args()

    scan = scan_repository(args.repo, max_files=args.max_files)

    if "error" in scan:
        print(f"Error: {scan['error']}", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        output = json.dumps(scan, indent=2, ensure_ascii=False, default=str)
    else:
        output = format_markdown(scan)

    Path(args.output).write_text(output, encoding="utf-8")
    print(f"wrote {args.output} ({scan['n_modules']} modules, {scan['n_losses']} losses, {scan['n_hyperparams']} hyperparams)")


if __name__ == "__main__":
    main()
