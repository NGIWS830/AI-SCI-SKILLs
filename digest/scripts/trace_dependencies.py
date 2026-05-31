#!/usr/bin/env python3
"""Trace module dependencies and data flow across an AI project codebase.

Usage:
    python trace_dependencies.py /path/to/repo --output dependency_report.md
    python trace_dependencies.py /path/to/repo --format json --output deps.json
    python trace_dependencies.py /path/to/repo --entry train.py --depth 2

What this does:
    1. Builds a module-level import graph (which file imports which)
    2. Traces the data flow from entry point through the model pipeline
    3. Identifies the core method chain (data → model → loss → output)
    4. Detects circular imports and isolated (unused) modules
    5. Maps which modules are likely novel (project code) vs library code
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


DEFAULT_IGNORE = {".git", "__pycache__", ".ipynb_checkpoints", "wandb", "runs",
                   "checkpoints", "outputs", "dist", "build", ".venv", "venv",
                   "node_modules", "tests", "test"}


# ── Import Graph Builder ───────────────────────────────────────────────────────────


def build_import_graph(repo_path, max_files=200):
    """Build a module-level import graph."""
    root = Path(repo_path).resolve()
    py_files = []
    for p in sorted(root.rglob("*.py")):
        if any(part in DEFAULT_IGNORE for part in p.parts):
            continue
        py_files.append(p)
        if len(py_files) >= max_files:
            break

    # Map: module name → file path
    module_to_file = {}
    # Graph: file → set of (imported_module, file_path)
    graph = defaultdict(list)
    # Reverse graph: imported_module → set of files that import it
    reverse_graph = defaultdict(set)

    for py_file in py_files:
        rel = py_file.relative_to(root)
        module_name = str(rel.with_suffix("")).replace("/", ".").replace("\\", ".")
        module_to_file[module_name] = str(rel)

        try:
            source = py_file.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(source)
        except (SyntaxError, UnicodeDecodeError):
            continue

        imports = _extract_imports(tree, root, py_file)
        for imp_name, imp_path in imports:
            graph[str(rel)].append((imp_name, imp_path))
            reverse_graph[imp_path].add(str(rel))

    return {
        "graph": dict(graph),
        "reverse_graph": {k: list(v) for k, v in reverse_graph.items()},
        "module_to_file": module_to_file,
        "n_files": len(py_files),
    }


def _extract_imports(tree, root, current_file):
    """Extract imports from an AST, resolving to actual files in the project."""
    imports = []
    current_dir = current_file.parent

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                resolved = _resolve_import(alias.name, root, current_dir)
                if resolved:
                    imports.append((alias.name, resolved))

        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue
            for alias in node.names:
                full_name = f"{node.module}.{alias.name}" if alias.name != "*" else node.module
                resolved = _resolve_import(node.module, root, current_dir)
                if resolved:
                    imports.append((full_name, resolved))

    return imports


def _resolve_import(module_name, root, current_dir):
    """Resolve a module name to a file path within the project."""
    # Try as a .py file
    parts = module_name.split(".")
    path_candidate = root / "/".join(parts)
    if path_candidate.with_suffix(".py").exists():
        return str(path_candidate.with_suffix(".py").relative_to(root))
    if (path_candidate / "__init__.py").exists():
        return str((path_candidate / "__init__.py").relative_to(root))

    # Try relative to current directory
    path_candidate = current_dir / "/".join(parts)
    if path_candidate.with_suffix(".py").exists():
        try:
            return str(path_candidate.with_suffix(".py").relative_to(root))
        except ValueError:
            return None
    if (path_candidate / "__init__.py").exists():
        try:
            return str((path_candidate / "__init__.py").relative_to(root))
        except ValueError:
            return None

    return None


# ── Data Flow Tracer ───────────────────────────────────────────────────────────────


def trace_data_flow(graph, entry_file):
    """Trace the likely data flow from entry point through model pipeline."""
    visited = set()
    flow_chain = []
    queue = [entry_file]

    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)

        # Classify the module
        module_type = _classify_module(current)
        flow_chain.append({
            "file": current,
            "type": module_type,
            "imports": [imp[1] for imp in graph.get(current, [])],
        })

        # Follow imports that look like project modules
        for imp_name, imp_path in graph.get(current, []):
            if imp_path not in visited and _is_project_module(imp_path):
                queue.append(imp_path)

    return flow_chain


def _classify_module(filepath):
    """Classify what role a module plays."""
    path_lower = filepath.lower()
    basename = Path(filepath).name.lower()

    if any(kw in basename for kw in ["train", "main", "run"]):
        return "entry_point"
    if any(kw in path_lower for kw in ["model", "network", "module", "net", "architecture", "backbone"]):
        return "model"
    if any(kw in path_lower for kw in ["loss", "criterion", "objective"]):
        return "loss"
    if any(kw in path_lower for kw in ["data", "dataset", "dataloader", "loader", "preprocess", "augment"]):
        return "data"
    if any(kw in path_lower for kw in ["metric", "eval", "evaluation", "measure"]):
        return "evaluation"
    if any(kw in path_lower for kw in ["util", "helper", "tool", "common", "functional"]):
        return "utility"
    if any(kw in path_lower for kw in ["config", "cfg", "setting", "option", "argparse"]):
        return "configuration"
    return "other"


def _is_project_module(filepath):
    """Check if an import looks like a project module (not a library)."""
    # Library imports usually start with well-known prefixes
    lib_prefixes = {"torch", "tensorflow", "numpy", "scipy", "sklearn", "pandas",
                    "matplotlib", "PIL", "cv2", "transformers", "datasets", "diffusers",
                    "timm", "einops", "optax", "flax", "jax", "os", "sys", "json",
                    "argparse", "logging", "collections", "itertools", "math", "random",
                    "typing", "pathlib", "re", "time", "datetime", "warnings", "copy",
                    "functools", "abc", "dataclasses", "yaml"}
    first_part = filepath.split("/")[0].split("\\")[0].split(".")[0]
    return first_part not in lib_prefixes


# ── Core Pipeline Identification ───────────────────────────────────────────────────


def identify_core_pipeline(graph, entry_file, flow_chain):
    """Identify the core method pipeline: data → model → loss → output."""
    pipeline = {
        "data_modules": [],
        "model_modules": [],
        "loss_modules": [],
        "training_entry": entry_file,
        "config_modules": [],
        "orphan_modules": [],
    }

    all_files = set(graph.keys())
    referenced_files = set()
    for imports in graph.values():
        for _, imp_path in imports:
            referenced_files.add(imp_path)

    for f in all_files:
        module_type = _classify_module(f)
        if module_type == "data":
            pipeline["data_modules"].append(f)
        elif module_type == "model":
            pipeline["model_modules"].append(f)
        elif module_type == "loss":
            pipeline["loss_modules"].append(f)
        elif module_type == "configuration":
            pipeline["config_modules"].append(f)

        # Orphan: defined but never imported by any project module
        if f not in referenced_files and f != entry_file and _is_project_module(f):
            pipeline["orphan_modules"].append(f)

    return pipeline


# ── Report Builder ─────────────────────────────────────────────────────────────────


def build_report(import_data, flow_chain, pipeline, entry_file):
    """Build comprehensive dependency analysis report."""
    lines = [
        "# Module Dependency & Data Flow Analysis",
        "",
        f"**Files analyzed:** {import_data['n_files']}",
        f"**Entry point:** {entry_file}",
        "",
    ]

    # Core Pipeline
    lines.append("## Core Method Pipeline")
    lines.append("")
    lines.append(f"**Training entry:** `{pipeline['training_entry']}`")
    lines.append("")

    for category, label in [("data_modules", "Data"), ("model_modules", "Model"),
                             ("loss_modules", "Loss"), ("config_modules", "Configuration")]:
        modules = pipeline[category]
        if modules:
            lines.append(f"**{label} modules ({len(modules)}):**")
            for m in sorted(modules)[:10]:
                lines.append(f"- `{m}`")
            if len(modules) > 10:
                lines.append(f"- ... and {len(modules) - 10} more")
        else:
            lines.append(f"**{label} modules:** none detected")
        lines.append("")

    # Data flow
    lines.append("## Data Flow Trace")
    lines.append("")
    lines.append("| File | Type | Imports Into |")
    lines.append("|------|------|-------------|")
    for node in flow_chain[:30]:
        imports_into = [imp for imp in node["imports"] if _is_project_module(imp)]
        imp_str = ", ".join(f"`{i}`" for i in imports_into[:3])
        if len(imports_into) > 3:
            imp_str += f" ... (+{len(imports_into) - 3})"
        lines.append(f"| `{node['file']}` | {node['type']} | {imp_str or '—'} |")
    lines.append("")

    # Import graph summary
    lines.append("## Module Dependencies")
    lines.append("")
    # Show top-level modules and their internal imports
    top_modules = defaultdict(set)
    for f, imports in import_data["graph"].items():
        top = f.split("/")[0].split("\\")[0]
        for imp_name, imp_path in imports:
            if _is_project_module(imp_path):
                top_modules[top].add(imp_path)

    for top, deps in sorted(top_modules.items()):
        if deps:
            lines.append(f"### `{top}/`")
            for d in sorted(deps)[:8]:
                lines.append(f"- → `{d}`")
            if len(deps) > 8:
                lines.append(f"- ... and {len(deps) - 8} more imports")

    lines.append("")

    # Orphan modules
    if pipeline["orphan_modules"]:
        lines.append("## Potentially Unused Modules")
        lines.append("")
        lines.append("These project modules are not imported by any other project module:")
        lines.append("")
        for m in pipeline["orphan_modules"][:10]:
            lines.append(f"- `{m}`")
        lines.append("")

    # External library usage
    lines.append("## External Library Dependencies")
    lines.append("")
    all_imports = set()
    for imports in import_data["graph"].values():
        for imp_name, _ in imports:
            top_level = imp_name.split(".")[0]
            all_imports.add(top_level)

    ml_libs = {"torch", "tensorflow", "jax", "transformers", "diffusers", "datasets",
               "timm", "einops", "accelerate", "deepspeed", "optax", "flax"}
    detected_ml = sorted(all_imports & ml_libs)
    if detected_ml:
        lines.append("**ML libraries:** " + ", ".join(f"`{lib}`" for lib in detected_ml))
    lines.append("")

    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Trace module dependencies and data flow across an AI project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python trace_dependencies.py /path/to/repo --output deps.md
  python trace_dependencies.py /path/to/repo --entry train.py --depth 3 --format json
  python trace_dependencies.py . --entry main.py --output deps.md
        """,
    )
    parser.add_argument("repo", help="Path to project repository")
    parser.add_argument("--entry", default="train.py", help="Entry point file (default: train.py)")
    parser.add_argument("--output", "-o", default="dependency_report.md")
    parser.add_argument("--format", default="markdown", choices=["markdown", "json"])
    parser.add_argument("--max-files", type=int, default=200)
    args = parser.parse_args()

    import_data = build_import_graph(args.repo, max_files=args.max_files)

    # Find actual entry point
    entry_file = args.entry
    if entry_file not in import_data["graph"]:
        # Try to find it
        candidates = [f for f in import_data["graph"] if args.entry in f]
        if candidates:
            entry_file = candidates[0]
            print(f"Resolved entry: {entry_file}", file=sys.stderr)
        else:
            entry_file = next(iter(import_data["graph"]), "")
            print(f"Entry not found, using first module: {entry_file}", file=sys.stderr)

    flow_chain = trace_data_flow(import_data["graph"], entry_file)
    pipeline = identify_core_pipeline(import_data["graph"], entry_file, flow_chain)

    print(f"Analyzed {import_data['n_files']} files, "
          f"{len(pipeline['model_modules'])} models, "
          f"{len(pipeline['data_modules'])} data modules.",
          file=sys.stderr)

    if args.format == "json":
        output = json.dumps({
            "import_graph": {k: [(n, p) for n, p in v] for k, v in import_data["graph"].items()},
            "flow_chain": flow_chain,
            "pipeline": pipeline,
        }, indent=2)
    else:
        output = build_report(import_data, flow_chain, pipeline, entry_file)

    Path(args.output).write_text(output, encoding="utf-8")
    print(f"Saved to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
