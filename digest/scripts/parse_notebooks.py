#!/usr/bin/env python3
"""Extract model definitions, training code, and results from Jupyter notebooks.

Usage:
    python parse_notebooks.py notebook.ipynb --output notebook_analysis.md
    python parse_notebooks.py experiments/*.ipynb --output-dir ./digest_outputs/

Extracts:
    - Model class definitions (nn.Module / tf.keras.Model / flax.linen.Module)
    - Training loops and hyperparameters
    - Loss function definitions and usage
    - Results tables (DataFrame outputs, printed metrics)
    - Markdown cell summaries
    - Cell dependency order (which cells must run before others)
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


# ── Notebook Parser ────────────────────────────────────────────────────────────────


def parse_notebook(path):
    """Parse a .ipynb file and extract code + markdown cells."""
    with open(path, encoding="utf-8") as f:
        nb = json.load(f)

    cells = []
    for i, cell in enumerate(nb.get("cells", [])):
        cell_type = cell.get("cell_type", "code")
        source = "".join(cell.get("source", []))
        outputs = cell.get("outputs", [])
        cells.append({
            "index": i,
            "type": cell_type,
            "source": source,
            "outputs": outputs,
            "execution_count": cell.get("execution_count"),
        })

    metadata = nb.get("metadata", {})
    return {
        "path": str(path),
        "cells": cells,
        "n_cells": len(cells),
        "kernel": metadata.get("kernelspec", {}).get("display_name", "unknown"),
        "language": metadata.get("language_info", {}).get("name", "unknown"),
    }


# ── Content Extraction ─────────────────────────────────────────────────────────────


def extract_model_definitions(cells):
    """Find model class definitions in code cells."""
    models = []
    for cell in cells:
        if cell["type"] != "code":
            continue
        try:
            tree = ast.parse(cell["source"])
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                bases = [_name_str(b) for b in node.bases]
                is_model = any(
                    base in ("nn.Module", "Module", "LightningModule",
                             "tf.keras.Model", "keras.Model",
                             "flax.linen.Module", "linen.Module",
                             "pl.LightningModule", "pl.LightningDataModule",
                             "torch.utils.data.Dataset", "Dataset")
                    for base in bases
                )
                if is_model or any("model" in base.lower() for base in bases):
                    methods = []
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            methods.append(item.name)
                    models.append({
                        "name": node.name,
                        "bases": bases,
                        "methods": methods,
                        "cell": cell["index"],
                        "line": node.lineno,
                    })

    return models


def extract_training_loop(cells):
    """Find training loop code and extract hyperparameters."""
    training_info = {
        "found": False,
        "cells": [],
        "hyperparams": {},
        "optimizer": "",
        "loss_function": "",
        "scheduler": "",
    }

    hp_patterns = {
        "learning_rate": [r'lr\s*[=:]\s*([\d.eE+-]+)', r'learning.rate\s*[=:]\s*([\d.eE+-]+)'],
        "batch_size": [r'batch.size\s*[=:]\s*(\d+)', r'batch_size\s*[=:]\s*(\d+)'],
        "epochs": [r'(?:num_)?epochs?\s*[=:]\s*(\d+)', r'n_epochs\s*[=:]\s*(\d+)'],
        "weight_decay": [r'weight.decay\s*[=:]\s*([\d.eE+-]+)'],
        "seed": [r'(?:random_)?seed\s*[=:]\s*(\d+)'],
    }

    for cell in cells:
        if cell["type"] != "code":
            continue
        source = cell["source"]

        # Detect training loop
        is_training = any(kw in source for kw in
                          ["for epoch in", "for batch in", "model.train()",
                           "optimizer.zero_grad", "loss.backward", "optimizer.step",
                           "model.fit(", ".fit(", "Trainer(", "trainer.fit"])

        if is_training:
            training_info["found"] = True
            training_info["cells"].append(cell["index"])

        # Extract hyperparameters
        for hp_name, patterns in hp_patterns.items():
            for pat in patterns:
                m = re.search(pat, source, re.IGNORECASE)
                if m and hp_name not in training_info["hyperparams"]:
                    training_info["hyperparams"][hp_name] = m.group(1)

        # Detect optimizer
        opt_match = re.search(r'(?:optimizer|optim)\s*[=:]\s*(?:torch\.)?optim\.?(\w+)', source)
        if opt_match:
            training_info["optimizer"] = opt_match.group(1)
        elif re.search(r'AdamW?', source) and not training_info["optimizer"]:
            training_info["optimizer"] = "AdamW" if "AdamW" in source else "Adam"

        # Detect loss function
        loss_match = re.search(r'(?:loss|criterion)\s*[=:]\s*(?:torch\.)?nn\.?(\w+)', source)
        if loss_match:
            training_info["loss_function"] = loss_match.group(1)
        elif re.search(r'CrossEntropyLoss', source):
            training_info["loss_function"] = "CrossEntropyLoss"

        # Detect scheduler
        sched_match = re.search(r'scheduler\s*[=:]\s*\w+\.(\w+)', source)
        if sched_match:
            training_info["scheduler"] = sched_match.group(1)

    return training_info


def extract_results(cells):
    """Extract numerical results from cell outputs (printed metrics, DataFrames)."""
    results = []
    for cell in cells:
        if cell["type"] != "code":
            continue

        for output in cell.get("outputs", []):
            text = ""

            # Text output (printed metrics)
            if output.get("output_type") == "stream":
                text = "".join(output.get("text", []))
            # Execute result (last expression)
            elif output.get("output_type") == "execute_result":
                data = output.get("data", {})
                text = "".join(data.get("text/plain", []))

            if text:
                # Find metric-like patterns
                for m in re.finditer(
                    r'(?:Accuracy|Acc|Precision|Recall|F1|mAP|mIoU|BLEU|ROUGE|PSNR|SSIM|R@\d+|Loss)'
                    r'\s*[:=]?\s*([\d.]+(?:e[+-]?\d+)?)\s*%?',
                    text, re.IGNORECASE
                ):
                    results.append({
                        "metric": m.group(0).split(":")[0].split("=")[0].strip()[:40],
                        "value": m.group(1),
                        "cell": cell["index"],
                        "execution_count": cell.get("execution_count"),
                    })

            # DataFrame output (structured tables)
            if output.get("output_type") == "execute_result":
                data = output.get("data", {})
                html = "".join(data.get("text/html", []))
                if html and "<table" in html:
                    # Extract table rows
                    rows = re.findall(r'<tr>\s*(?:<th>.*?</th>\s*)?((?:<td>.*?</td>\s*)+)</tr>', html)
                    if rows:
                        results.append({
                            "type": "dataframe",
                            "n_rows": len(rows),
                            "cell": cell["index"],
                            "execution_count": cell.get("execution_count"),
                        })

    return results


def extract_markdown_summaries(cells):
    """Extract section headings and key sentences from markdown cells."""
    summaries = []
    for cell in cells:
        if cell["type"] != "markdown":
            continue
        source = cell["source"]

        # Extract headings
        headings = re.findall(r'^(#{1,3})\s+(.+)$', source, re.MULTILINE)
        for level, title in headings:
            summaries.append({
                "type": "heading",
                "level": len(level),
                "text": title.strip()[:120],
                "cell": cell["index"],
            })

        # Extract first substantial sentence after each heading
        sentences = re.findall(r'(?:^|\n)\s*([A-Z][^.!?]{30,200}[.!?])', source)
        for sent in sentences[:3]:
            if not any(s["type"] == "sentence" and s["text"] == sent.strip() for s in summaries):
                summaries.append({
                    "type": "sentence",
                    "text": sent.strip(),
                    "cell": cell["index"],
                })

    return summaries


# ── Dependency Analysis ────────────────────────────────────────────────────────────


def trace_cell_dependencies(cells):
    """Trace which cells define variables used by other cells."""
    # Track variable assignments per cell
    assignments = defaultdict(set)
    usages = defaultdict(set)

    for cell in cells:
        if cell["type"] != "code":
            continue
        try:
            tree = ast.parse(cell["source"])
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assignments[cell["index"]].add(target.id)

        # Track function/class definitions
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                assignments[cell["index"]].add(node.name)

        # Track variable usage
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                usages[cell["index"]].add(node.id)

    # Build dependency edges
    deps = []
    for cell_idx, used_vars in usages.items():
        for dep_idx, defined_vars in assignments.items():
            if dep_idx >= cell_idx:
                continue
            common = used_vars & defined_vars
            if common:
                deps.append({
                    "from": dep_idx,
                    "to": cell_idx,
                    "variables": sorted(common)[:5],
                })

    return deps


# ── Report Builder ─────────────────────────────────────────────────────────────────


def build_report(nb_data, models, training, results, summaries, deps):
    """Build comprehensive notebook analysis report."""
    lines = [
        f"# Notebook Analysis: {Path(nb_data['path']).name}",
        "",
        f"**Kernel:** {nb_data['kernel']} | **Language:** {nb_data['language']}",
        f"**Total cells:** {nb_data['n_cells']} "
        f"({sum(1 for c in nb_data['cells'] if c['type'] == 'code')} code, "
        f"{sum(1 for c in nb_data['cells'] if c['type'] == 'markdown')} markdown)",
        "",
    ]

    # Models
    lines.append("## Model Definitions")
    lines.append("")
    if models:
        lines.append("| Model | Base Class | Methods | Cell |")
        lines.append("|-------|-----------|---------|------|")
        for m in models:
            method_str = ", ".join(m["methods"][:8])
            lines.append(f"| `{m['name']}` | {', '.join(m['bases'])} | {method_str} | [{m['cell']}] |")
    else:
        lines.append("No model class definitions found in code cells.")
    lines.append("")

    # Training
    lines.append("## Training Configuration")
    lines.append("")
    if training["found"]:
        lines.append(f"**Training cells detected:** {training['cells']}")
        lines.append(f"**Optimizer:** {training['optimizer'] or 'not detected'}")
        lines.append(f"**Loss function:** {training['loss_function'] or 'not detected'}")
        lines.append(f"**Scheduler:** {training['scheduler'] or 'not detected'}")
        lines.append("")
        if training["hyperparams"]:
            lines.append("| Hyperparameter | Value |")
            lines.append("|---|---|")
            for k, v in training["hyperparams"].items():
                lines.append(f"| {k} | {v} |")
    else:
        lines.append("No training loop detected in code cells.")
    lines.append("")

    # Results
    lines.append("## Extracted Results")
    lines.append("")
    metric_results = [r for r in results if "metric" in r]
    if metric_results:
        lines.append("| Metric | Value | Cell |")
        lines.append("|--------|-------|------|")
        for r in metric_results[:30]:
            lines.append(f"| {r['metric']} | {r['value']} | [{r['cell']}] |")
    df_results = [r for r in results if r.get("type") == "dataframe"]
    if df_results:
        lines.append(f"\n**DataFrame outputs:** {len(df_results)} table(s) found.")
    if not results:
        lines.append("No numerical results extracted from cell outputs.")
    lines.append("")

    # Markdown structure
    lines.append("## Document Structure (from Markdown cells)")
    lines.append("")
    for s in summaries[:20]:
        if s["type"] == "heading":
            prefix = "#" * s["level"]
            lines.append(f"{prefix} {s['text']}")
        else:
            lines.append(f"- {s['text'][:120]}")
    lines.append("")

    # Cell dependencies
    lines.append("## Cell Dependency Graph")
    lines.append("")
    if deps:
        lines.append("| From Cell | To Cell | Shared Variables |")
        lines.append("|---|---|---|")
        for d in deps[:20]:
            lines.append(f"| [{d['from']}] | [{d['to']}] | {', '.join(d['variables'])} |")
    else:
        lines.append("No cross-cell dependencies detected.")
    lines.append("")

    return "\n".join(lines)


def _name_str(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{_name_str(node.value)}.{node.attr}"
    if isinstance(node, ast.Call):
        return _name_str(node.func)
    return ""


# ── CLI ────────────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Extract model code, training config, and results from Jupyter notebooks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python parse_notebooks.py experiments.ipynb --output analysis.md
  python parse_notebooks.py *.ipynb --output-dir ./digest_outputs/
        """,
    )
    parser.add_argument("notebooks", nargs="+", help="Jupyter notebook file(s)")
    parser.add_argument("--output", "-o", help="Single output file (for single notebook)")
    parser.add_argument("--output-dir", default="./digest_outputs", help="Output directory for multiple notebooks")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    for nb_path in args.notebooks:
        path = Path(nb_path)
        if not path.exists():
            print(f"Warning: {path} not found, skipping.", file=sys.stderr)
            continue

        nb_data = parse_notebook(path)
        models = extract_model_definitions(nb_data["cells"])
        training = extract_training_loop(nb_data["cells"])
        results = extract_results(nb_data["cells"])
        summaries = extract_markdown_summaries(nb_data["cells"])
        deps = trace_cell_dependencies(nb_data["cells"])

        print(f"{path.name}: {len(models)} models, {len(results)} metrics, "
              f"training={'yes' if training['found'] else 'no'}", file=sys.stderr)

        if args.json:
            import json as _json
            output = _json.dumps({
                "notebook": nb_data["path"],
                "models": models,
                "training": training,
                "results": results,
                "summaries": summaries,
                "dependencies": deps,
            }, indent=2, default=str)
            out_path = Path(args.output_dir) / f"{path.stem}_analysis.json"
        else:
            output = build_report(nb_data, models, training, results, summaries, deps)
            out_path = args.output if args.output else Path(args.output_dir) / f"{path.stem}_analysis.md"

        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        Path(out_path).write_text(output, encoding="utf-8")
        print(f"  → {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
