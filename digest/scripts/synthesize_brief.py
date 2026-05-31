#!/usr/bin/env python3
"""Auto-generate a structured project brief from code analysis outputs.

Usage:
    python synthesize_brief.py --arch arch_report.md --deps dependency_report.md \\
        --output project_brief.md

    python synthesize_brief.py --repo /path/to/project --output project_brief.md

    python synthesize_brief.py --arch arch_report.md --notebooks nb_analysis.md \\
        --deps dependency_report.md --output project_brief.md

What this does:
    Takes the outputs of extract_architecture.py, trace_dependencies.py, and
    parse_notebooks.py, then synthesizes a complete project_brief.md matching
    the Stage 1 template structure.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


# ── Input Parsing ──────────────────────────────────────────────────────────────────


def parse_arch_report(text):
    """Parse extract_architecture.py output."""
    info = {
        "modules": [],
        "losses": [],
        "hyperparams": [],
        "frameworks": [],
        "training_infra": {},
    }

    # Extract modules
    in_table = False
    for line in text.split("\n"):
        if "| # | Module | File |" in line:
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table and re.match(r'^\|\s*\d+\s*\|', line):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 5:
                info["modules"].append({
                    "name": cells[1].strip("`"),
                    "file": cells[2].strip("`") if len(cells) > 2 else "",
                    "base": cells[3] if len(cells) > 3 else "",
                    "methods": cells[4] if len(cells) > 4 else "",
                })
        if in_table and not line.startswith("|"):
            in_table = False

    # Extract frameworks
    for m in re.finditer(r'[-*]\s+\*\*(\w+(?:\s+\w+)*)\*\*', text):
        info["frameworks"].append(m.group(1))

    # Extract training infra
    for key, pattern in [
        ("optimizer", r'Optimizers detected.*?\n((?:\s*-\s*.+\n?)+)'),
        ("scheduler", r'LR Schedulers.*?`([^`]+)`'),
        ("mixed_precision", r'Mixed Precision.*?\*\*(Yes|No|Not detected)\*\*'),
        ("distributed", r'Distributed Training.*?\*\*(Yes|No|Not detected)\*\*'),
    ]:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            info["training_infra"][key] = m.group(1).strip() if m.lastindex else m.group(0)

    return info


def parse_deps_report(text):
    """Parse trace_dependencies.py output."""
    info = {
        "entry_point": "",
        "data_modules": [],
        "model_modules": [],
        "loss_modules": [],
        "orphan_modules": [],
        "ml_libraries": [],
    }

    for m in re.finditer(r'Training entry.*?`([^`]+)`', text):
        info["entry_point"] = m.group(1)

    for section, key in [
        (r'Data modules.*?\n((?:\s*-\s*.+\n?)+)', "data_modules"),
        (r'Model modules.*?\n((?:\s*-\s*.+\n?)+)', "model_modules"),
        (r'Loss modules.*?\n((?:\s*-\s*.+\n?)+)', "loss_modules"),
    ]:
        m = re.search(section, text, re.IGNORECASE)
        if m:
            items = re.findall(r'`([^`]+)`', m.group(1))
            info[key] = items

    # Orphan modules
    m = re.search(r'Potentially Unused Modules.*?\n((?:\s*-\s*.+\n?)+)', text, re.IGNORECASE | re.DOTALL)
    if m:
        info["orphan_modules"] = re.findall(r'`([^`]+)`', m.group(1))

    # ML libraries
    m = re.search(r'ML libraries.*?`(.+?)`', text)
    if m:
        info["ml_libraries"] = [lib.strip() for lib in m.group(1).split(",")]

    return info


def parse_notebook_report(text):
    """Parse parse_notebooks.py output."""
    info = {
        "models": [],
        "results": [],
        "hyperparams": {},
        "training_found": False,
    }

    # Check for training
    if "Training cells detected" in text:
        info["training_found"] = True

    # Extract hyperparameters
    for m in re.finditer(r'\|\s*(\w+)\s*\|\s*([\d.eE+-]+)\s*\|', text):
        info["hyperparams"][m.group(1)] = m.group(2)

    # Extract result metrics
    in_table = False
    for line in text.split("\n"):
        if "| Metric | Value |" in line:
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table and re.match(r'^\|', line):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 2:
                info["results"].append({"metric": cells[0], "value": cells[1]})
        if in_table and not line.startswith("|"):
            in_table = False

    return info


# ── Brief Builder ──────────────────────────────────────────────────────────────────


def build_project_brief(arch, deps, notebooks, project_info):
    """Build a complete project_brief.md."""
    lines = [
        f"# Project Brief — {project_info.get('title', '[Paper Title]')}",
        "",
        f"**Generated:** {project_info.get('date', '[DATE]')}",
        f"**Repository:** {project_info.get('repo', '[REPO PATH]')}",
        "",
        "---",
        "",
    ]

    # Research Task
    lines.extend([
        "## Research Task",
        "",
        f"{project_info.get('task', '[Extract from README or author notes]')}",
        "",
    ])

    # Problem Motivation
    lines.extend([
        "## Problem Motivation",
        "",
        f"{project_info.get('problem', '[Extract from README or author notes]')}",
        "",
    ])

    # Method Overview
    lines.append("## Method Overview")
    lines.append("")

    framework_str = ", ".join(arch.get("frameworks", [])) if arch.get("frameworks") else "[DETECTED FRAMEWORKS]"
    lines.append(f"**Framework:** {framework_str}")
    lines.append("")

    # Entry point
    if deps.get("entry_point"):
        lines.append(f"**Entry point:** `{deps['entry_point']}`")
    lines.append("")

    # Model modules
    model_modules = arch.get("modules", [])
    if model_modules:
        lines.append("### Core Architecture")
        lines.append("")
        lines.append("| Module | File | Base Class | Key Methods |")
        lines.append("|--------|------|------------|-------------|")
        for m in model_modules[:15]:
            lines.append(f"| `{m['name']}` | `{m['file']}` | {m['base']} | {m['methods'][:80]} |")
        lines.append("")

    # Pipeline flow
    lines.append("### Data Flow")
    lines.append("")
    pipeline_steps = _infer_pipeline(deps, arch)
    for i, step in enumerate(pipeline_steps, 1):
        lines.append(f"{i}. **{step['name']}** — `{step['module']}` → {step['description']}")
    lines.append("")

    # Core Modules and Evidence
    lines.append("## Core Modules and Evidence")
    lines.append("")
    lines.append("| Module | Role | Evidence Source | Confidence |")
    lines.append("|---|---|---|---|")
    for m in model_modules[:12]:
        evidence = f"`{m['file']}`"
        confidence = "High" if m["methods"] else "Medium"
        lines.append(f"| `{m['name']}` | [INFER FROM CODE] | {evidence} | {confidence} |")
    if not model_modules:
        lines.append("| — | No custom modules detected | — | — |")
    lines.append("")

    # Method Innovation Slots
    lines.append("## Method Innovation Slots for Manuscript")
    lines.append("")
    lines.append("| Subsection | Innovation/Module | Evidence Source | Missing Details |")
    lines.append("|---|---|---|---|")

    # Assign modules to typical paper sections
    section_map = {"III-B": [], "III-C": [], "III-D": []}
    for i, m in enumerate(model_modules[:9]):
        if i < 3:
            section_map["III-B"].append(m["name"])
        elif i < 6:
            section_map["III-C"].append(m["name"])
        else:
            section_map["III-D"].append(m["name"])

    for section, modules in section_map.items():
        if modules:
            lines.append(f"| {section} | {', '.join(modules)} | Code: `{model_modules[0]['file']}` | Author confirmation needed |")
    if not model_modules:
        lines.append("| III-B | [COMPONENT] | — | Needs author input |")
    lines.append("")

    # Data Flow detail
    lines.append("## Data Flow")
    lines.append("")
    lines.append(_generate_data_flow_description(arch, deps))
    lines.append("")

    # Datasets, Baselines, and Metrics
    lines.append("## Datasets, Baselines, and Metrics")
    lines.append("")

    lines.append("### Datasets")
    lines.append("")
    datasets = project_info.get("datasets", "").split(",") if project_info.get("datasets") else []
    if datasets:
        for ds in datasets:
            lines.append(f"- **{ds.strip()}**: [description, size, split, source]")
    else:
        lines.append("- [DATASET 1]: [description] — AUTHOR_INPUT_NEEDED")
        lines.append("- [DATASET 2]: [description] — AUTHOR_INPUT_NEEDED")
    lines.append("")

    lines.append("### Baselines")
    lines.append("")
    baselines = project_info.get("baselines", "").split(",") if project_info.get("baselines") else []
    if baselines:
        for b in baselines:
            lines.append(f"- {b.strip()}")
    else:
        lines.append("- [BASELINE 1] — AUTHOR_INPUT_NEEDED")
        lines.append("- [BASELINE 2] — AUTHOR_INPUT_NEEDED")
    lines.append("")

    lines.append("### Evaluation Metrics")
    lines.append("")
    notebook_metrics = notebooks.get("results", [])
    if notebook_metrics:
        for r in notebook_metrics[:10]:
            lines.append(f"- **{r['metric']}**: {'higher' if 'accuracy' in r['metric'].lower() or 'R@' in r['metric'] else 'lower'} is better — detected value: {r['value']}")
    else:
        lines.append("- [METRIC 1]: [higher/lower is better] — AUTHOR_INPUT_NEEDED")
    lines.append("")

    # Training Infrastructure
    lines.append("## Training Infrastructure")
    lines.append("")
    infra = arch.get("training_infra", {})
    nb_hp = notebooks.get("hyperparams", {})

    lines.append("| Setting | Value | Source |")
    lines.append("|---|---|---|")
    lines.append(f"| Optimizer | {infra.get('optimizer', 'AUTHOR_INPUT_NEEDED')} | arch_report |")
    lines.append(f"| Learning Rate | {nb_hp.get('learning_rate', 'AUTHOR_INPUT_NEEDED')} | notebook |")
    lines.append(f"| Batch Size | {nb_hp.get('batch_size', 'AUTHOR_INPUT_NEEDED')} | notebook |")
    lines.append(f"| Epochs | {nb_hp.get('epochs', 'AUTHOR_INPUT_NEEDED')} | notebook |")
    lines.append(f"| Weight Decay | {nb_hp.get('weight_decay', 'AUTHOR_INPUT_NEEDED')} | notebook |")
    lines.append(f"| Mixed Precision | {infra.get('mixed_precision', 'AUTHOR_INPUT_NEEDED')} | arch_report |")
    lines.append(f"| Distributed | {infra.get('distributed', 'AUTHOR_INPUT_NEEDED')} | arch_report |")
    lines.append(f"| ML Libraries | {', '.join(deps.get('ml_libraries', [])) if deps.get('ml_libraries') else 'AUTHOR_INPUT_NEEDED'} | deps_report |")
    lines.append("")

    # Candidate Contributions
    lines.append("## Candidate Contributions")
    lines.append("")
    # Infer contributions from modules
    contrib_num = 1
    for m in model_modules[:6]:
        lines.append(f"{contrib_num}. **{m['name']}**: [describe what this module does and why it's novel]. Evidence: `{m['file']}`. Needs validation: novelty check against literature, experiment confirmation.")
        contrib_num += 1
    if not model_modules:
        lines.append("1. [CANDIDATE CONTRIBUTION 1] — AUTHOR_INPUT_NEEDED")
    lines.append("")

    # Claims Supported by Current Materials
    lines.append("## Claims Supported by Current Materials")
    lines.append("")
    lines.append("| Claim | Evidence | Strength | Caveat |")
    lines.append("|---|---|---|---|")
    if notebook_metrics:
        for r in notebook_metrics[:5]:
            lines.append(f"| Method achieves {r['value']} {r['metric']} | Notebook output | Preliminary | Needs statistical validation |")
    lines.append(f"| Method has {len(model_modules)} custom modules | Code analysis | High | Novelty needs literature confirmation |")
    if deps.get("entry_point"):
        lines.append(f"| Training pipeline is functional | Entry point `{deps['entry_point']}` exists | High | — |")
    lines.append("")

    # Missing Information
    lines.append("## Missing Information")
    lines.append("")
    missing = _identify_missing(arch, deps, notebooks)
    for item in missing:
        lines.append(f"- {item}")
    lines.append("")

    # Paper-Writing Risks
    lines.append("## Paper-Writing Risks")
    lines.append("")
    risks = _identify_risks(arch, deps, notebooks, model_modules)
    for risk in risks:
        lines.append(f"- ⚠ {risk}")
    lines.append("")

    return "\n".join(lines)


def _infer_pipeline(deps, arch):
    """Infer the data flow pipeline from module analysis."""
    steps = []
    data_modules = deps.get("data_modules", [])
    model_modules = deps.get("model_modules", [])
    loss_modules = deps.get("loss_modules", [])

    if data_modules:
        steps.append({"name": "Data Loading", "module": data_modules[0],
                       "description": "Load and preprocess input data"})
    else:
        steps.append({"name": "Data Loading", "module": "[NOT DETECTED]",
                       "description": "AUTHOR_INPUT_NEEDED"})

    if model_modules:
        steps.append({"name": "Feature Extraction", "module": model_modules[0],
                       "description": "Extract features from input via backbone"})
        if len(model_modules) > 1:
            steps.append({"name": "Core Processing", "module": model_modules[1],
                           "description": "Apply proposed method to extracted features"})

    if loss_modules:
        steps.append({"name": "Loss Computation", "module": loss_modules[0],
                       "description": "Compute training objective"})
    else:
        steps.append({"name": "Loss Computation", "module": "[NOT DETECTED]",
                       "description": "Standard loss (CrossEntropy / MSE) likely used"})

    steps.append({"name": "Output", "module": deps.get("entry_point", "main.py"),
                   "description": "Generate predictions / evaluation results"})
    return steps


def _generate_data_flow_description(arch, deps):
    """Generate a prose description of the data flow."""
    parts = []
    entry = deps.get("entry_point", "the entry script")
    model_count = len(arch.get("modules", []))

    parts.append(f"The project entry point is `{entry}`. ")
    if model_count > 0:
        parts.append(f"The model architecture contains {model_count} custom module(s): ")
        module_names = [m["name"] for m in arch.get("modules", [])[:5]]
        parts.append(", ".join(f"`{n}`" for n in module_names) + ". ")
    else:
        parts.append("No custom neural network modules were detected. ")

    data_mods = deps.get("data_modules", [])
    if data_mods:
        parts.append(f"Data loading is handled by `{data_mods[0]}`. ")

    loss_mods = deps.get("loss_modules", [])
    if loss_mods:
        parts.append(f"Loss computation is in `{loss_mods[0]}`. ")

    frameworks = arch.get("frameworks", [])
    if frameworks:
        parts.append(f"Built with {', '.join(frameworks)}.")

    return "".join(parts)


def _identify_missing(arch, deps, notebooks):
    missing = []
    if not arch.get("modules"):
        missing.append("AUTHOR_INPUT_NEEDED: No custom model modules detected. Provide a description of the proposed method architecture.")
    if not deps.get("data_modules"):
        missing.append("AUTHOR_INPUT_NEEDED: Data loading pipeline not detected from code. Specify datasets and preprocessing steps.")
    if not notebooks.get("training_found") and not deps.get("entry_point"):
        missing.append("AUTHOR_INPUT_NEEDED: No training loop or entry point detected. Describe the training procedure.")
    if not notebooks.get("results"):
        missing.append("AUTHOR_INPUT_NEEDED: No experimental results provided. Share experiment tables (CSV) or notebook outputs.")
    if len(arch.get("modules", [])) > 0:
        missing.append("AUTHOR_INPUT_NEEDED: For each custom module, author must explain the design rationale and confirm its novelty relative to prior work.")
    if deps.get("orphan_modules"):
        missing.append(f"Note: {len(deps['orphan_modules'])} modules appear unused — verify they are part of the method pipeline.")
    return missing


def _identify_risks(arch, deps, notebooks, modules):
    risks = []
    if len(modules) == 0:
        risks.append("No custom modules detected — the method's novelty is unclear. Risk: paper may lack a clear technical contribution.")
    elif len(modules) == 1:
        risks.append("Only one custom module found — ensure the contribution is substantial enough for the target venue.")
    if not notebooks.get("results"):
        risks.append("No experimental results provided — cannot map claims to evidence. Risk: claims based on interpretation only.")
    if not deps.get("data_modules"):
        risks.append("Data pipeline not detected — reproducibility may be compromised. Risk: reviewer questions about dataset handling.")
    if deps.get("orphan_modules"):
        risks.append(f"{len(deps['orphan_modules'])} unused modules detected — verify codebase completeness.")
    infra = arch.get("training_infra", {})
    if not infra.get("optimizer"):
        risks.append("Optimizer not detected — implementation details may be incomplete for reproducibility.")
    return risks


# ── Run-all mode ───────────────────────────────────────────────────────────────────


def run_full_pipeline(repo_path):
    """Run all digest scripts and synthesize the brief."""
    import subprocess
    import tempfile

    tmpdir = Path(tempfile.mkdtemp())
    arch_out = tmpdir / "arch_report.md"
    deps_out = tmpdir / "dependency_report.md"

    scripts_dir = Path(__file__).resolve().parent

    # Run extract_architecture
    subprocess.run([sys.executable, str(scripts_dir / "extract_architecture.py"),
                     repo_path, "--output", str(arch_out)], check=False)
    # Run trace_dependencies
    subprocess.run([sys.executable, str(scripts_dir / "trace_dependencies.py"),
                     repo_path, "--output", str(deps_out)], check=False)

    arch_text = arch_out.read_text(encoding="utf-8") if arch_out.exists() else ""
    deps_text = deps_out.read_text(encoding="utf-8") if deps_out.exists() else ""

    arch = parse_arch_report(arch_text) if arch_text else {}
    deps = parse_deps_report(deps_text) if deps_text else {}
    notebooks = {}

    return build_project_brief(arch, deps, notebooks, {"repo": repo_path})


# ── CLI ────────────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Auto-generate structured project brief from code analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # From individual analysis outputs
  python synthesize_brief.py --arch arch_report.md --deps dependency_report.md \\
      --output project_brief.md

  # Run full digest pipeline automatically
  python synthesize_brief.py --repo /path/to/project --output project_brief.md

  # With manual overrides
  python synthesize_brief.py --arch arch_report.md --deps dep_report.md \\
      --task "Semantic segmentation" --datasets "Cityscapes,Mapillary" \\
      --baselines "FCN,DeepLabV3,SegFormer" --output brief.md
        """,
    )
    parser.add_argument("--arch", help="extract_architecture.py output")
    parser.add_argument("--deps", help="trace_dependencies.py output")
    parser.add_argument("--notebooks", help="parse_notebooks.py output")
    parser.add_argument("--repo", help="Path to project repo (runs full digest pipeline)")
    parser.add_argument("--task", help="Research task description (manual override)")
    parser.add_argument("--datasets", help="Comma-separated dataset names")
    parser.add_argument("--baselines", help="Comma-separated baseline method names")
    parser.add_argument("--title", help="Paper title placeholder")
    parser.add_argument("--output", "-o", default="project_brief.md")
    args = parser.parse_args()

    # Full pipeline mode
    if args.repo:
        output = run_full_pipeline(args.repo)
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Full digest pipeline complete. Saved to {args.output}", file=sys.stderr)
        return

    # Manual assembly mode
    arch = {}
    deps = {}
    notebooks = {}

    if args.arch and Path(args.arch).exists():
        arch = parse_arch_report(Path(args.arch).read_text(encoding="utf-8", errors="replace"))
    if args.deps and Path(args.deps).exists():
        deps = parse_deps_report(Path(args.deps).read_text(encoding="utf-8", errors="replace"))
    if args.notebooks and Path(args.notebooks).exists():
        notebooks = parse_notebook_report(Path(args.notebooks).read_text(encoding="utf-8", errors="replace"))

    project_info = {
        "title": args.title or "[Paper Title]",
        "task": args.task or "",
        "datasets": args.datasets or "",
        "baselines": args.baselines or "",
        "repo": args.repo or "[REPO]",
        "date": "[DATE]",
        "problem": "",
    }

    print(f"Assembling brief: {len(arch.get('modules', []))} modules, "
          f"{len(deps.get('model_modules', []))} model deps, "
          f"{len(notebooks.get('results', []))} notebook metrics.",
          file=sys.stderr)

    output = build_project_brief(arch, deps, notebooks, project_info)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"Saved to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
