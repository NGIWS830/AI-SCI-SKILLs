#!/usr/bin/env python3
"""Generate publication-quality result visualizations from CSV experiment data.

Usage:
    python result_visualizer.py results.csv --output-dir ./figures/
    python result_visualizer.py results.csv --target SGA-Ours --metrics R@1 R@5 \\
        --format pgf --output-dir ./figures/

Output formats:
    - png: raster images for quick preview
    - pdf: vector for LaTeX inclusion
    - svg: web-friendly vector
    - pgf: native LaTeX PGF/TikZ for direct embedding
    - json: raw plotting data for external tools

Requires: matplotlib (pip install matplotlib)
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    HAS_MPL = True
except ImportError:
    HAS_MPL = False


# ── Color Palettes ─────────────────────────────────────────────────────────────────

# Colorblind-friendly palettes
PALETTE_TOL = ["#332288", "#117733", "#44AA99", "#88CCEE", "#DDCC77", "#CC6677", "#AA4499", "#882255"]
PALETTE_TABLEAU = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948", "#B07AA1", "#FF9DA7"]
PALETTE_IBM = ["#648FFF", "#785EF0", "#DC267F", "#FE6100", "#FFB000", "#009E73", "#56B4E9", "#CC79A7"]


def to_float(x):
    try:
        return float(str(x).strip().replace("%", "").replace(",", ""))
    except (ValueError, TypeError):
        return None


def parse_csv(csv_path, method_col="Method"):
    """Parse CSV into structured data."""
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    all_cols = list(rows[0].keys()) if rows else []

    # Detect columns
    metric_cols = []
    std_cols = []
    group_cols = []
    for col in all_cols:
        if col == method_col:
            continue
        if col.endswith("_std") or col.endswith("_stdev"):
            std_cols.append(col)
        elif col.lower() in ("dataset", "setting", "condition", "task"):
            group_cols.append(col)
        else:
            metric_cols.append(col)

    if not group_cols:
        for col in ["Dataset", "Setting"]:
            if col in all_cols:
                group_cols = [col]
                break

    # Parse data
    data = defaultdict(dict)  # (group, method) -> {metric: value, metric_std: std_value}
    for row in rows:
        method = row.get(method_col, "").strip()
        group_key = tuple(row.get(gc, "").strip() for gc in group_cols) if group_cols else ("all",)
        for mc in metric_cols:
            val = to_float(row.get(mc))
            if val is not None:
                data[(group_key, method)][mc] = val
        # Match std columns to metrics
        for sc in std_cols:
            base_metric = sc.replace("_std", "").replace("_stdev", "")
            std_val = to_float(row.get(sc))
            if std_val is not None:
                data[(group_key, method)][f"{base_metric}_std"] = std_val

    return data, metric_cols, std_cols, group_cols


def _group_label(group):
    if isinstance(group, tuple) and len(group) == 1:
        return group[0]
    if isinstance(group, tuple):
        return ", ".join(str(g) for g in group)
    return str(group)


# ── Plot Functions ─────────────────────────────────────────────────────────────────

def _setup_style():
    """Apply consistent publication style."""
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05,
    })


def bar_chart(data, metric, group_cols, method_col, target=None, output_path=None,
              palette=None, figsize=(8, 5), title=None, xlabel=None, ylabel=None):
    """Generate a grouped bar chart comparing methods on a metric across groups.

    If target is specified, it is highlighted with a distinct color.
    """
    if not HAS_MPL:
        print("matplotlib is required for plotting. Install: pip install matplotlib", file=sys.stderr)
        return None

    _setup_style()
    if palette is None:
        palette = PALETTE_TOL

    # Organize data: {group: {method: value}}
    groups = defaultdict(dict)
    methods_set = set()
    for (group_key, method), values in data.items():
        if metric in values:
            groups[group_key][method] = values[metric]
            methods_set.add(method)

    groups_order = sorted(groups.keys(), key=lambda g: (isinstance(g, tuple), str(g)))
    methods_list = sorted(methods_set, key=lambda m: (m != target, m)) if target else sorted(methods_set)

    fig, ax = plt.subplots(figsize=figsize)

    n_groups = len(groups_order)
    n_methods = len(methods_list)
    bar_width = 0.8 / n_methods
    x_positions = range(n_groups)

    for i, method in enumerate(methods_list):
        values_list = [groups[g].get(method, 0) for g in groups_order]
        errors = []
        for g in groups_order:
            err_key = f"{metric}_std"
            err_val = None
            # Look up std in data
            for (gk, m), vals in data.items():
                if gk == g and m == method and err_key in vals:
                    err_val = vals[err_key]
                    break
            errors.append(err_val)

        offset = (i - (n_methods - 1) / 2) * bar_width
        color = "#DC267F" if (target and method == target) else palette[i % len(palette)]
        alpha_val = 1.0 if (target and method == target) else 0.85

        bars = ax.bar([x + offset for x in x_positions], values_list, bar_width * 0.9,
                      label=method, color=color, alpha=alpha_val, edgecolor="white", linewidth=0.3)

        if any(e is not None for e in errors):
            yerr = [(e if e is not None else 0) for e in errors]
            for bar, err in zip(bars, yerr):
                if err > 0:
                    ax.errorbar(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                                yerr=err, color="black", capsize=3, linewidth=0.8, fmt="none")

    ax.set_xticks(list(x_positions))
    ax.set_xticklabels([_group_label(g) for g in groups_order])
    ax.set_xlabel(xlabel or "Dataset")
    ax.set_ylabel(ylabel or metric)
    ax.set_title(title or f"Comparison of {metric}")
    ax.legend(loc="upper right", framealpha=0.9, ncol=min(n_methods, 4))
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    if output_path:
        fig.savefig(output_path)
        plt.close(fig)
        print(f"Saved: {output_path}", file=sys.stderr)
    return fig


def ablation_waterfall(data, metric, group_cols, method_col, target, ablation_order,
                       output_path=None, figsize=(8, 5), title=None):
    """Generate a waterfall chart for ablation studies.

    ablation_order: list of (variant_name, method_name_in_data) tuples.
    """
    if not HAS_MPL:
        print("matplotlib is required for plotting. Install: pip install matplotlib", file=sys.stderr)
        return None

    _setup_style()

    # Get values for the specified target across ablation variants
    variants = []
    values_list = []
    for variant_name, method_name in ablation_order:
        for (group_key, method), vals in data.items():
            if method == method_name and metric in vals:
                variants.append(variant_name)
                values_list.append(vals[metric])
                break

    if not values_list:
        print(f"No ablation data found for metric {metric}", file=sys.stderr)
        return None

    fig, ax = plt.subplots(figsize=figsize)

    # Waterfall: show cumulative decrease from full model
    full_value = values_list[0] if values_list else 0
    decreases = [full_value - v for v in values_list]

    colors = ["#2E86AB" if d >= 0 else "#A23B72" for d in decreases]
    # Full model in distinct color
    colors[0] = "#117733"

    bars = ax.bar(variants, values_list, color=colors, edgecolor="white", linewidth=0.5)

    # Annotate with values and deltas
    for i, (bar, val) in enumerate(zip(bars, values_list)):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(values_list) * 0.01,
                f"{val:.2f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
        if i > 0:
            delta = full_value - val
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2,
                    f"-{delta:.2f}", ha="center", va="center", fontsize=8, color="white")

    ax.set_ylabel(metric)
    ax.set_title(title or f"Ablation Study — {metric}")
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Adjust y-axis to show differences clearly
    ymin = min(values_list) * 0.95
    ymax = max(values_list) * 1.08
    ax.set_ylim(ymin, ymax)

    plt.xticks(rotation=25, ha="right")

    if output_path:
        fig.savefig(output_path)
        plt.close(fig)
        print(f"Saved: {output_path}", file=sys.stderr)
    return fig


def radar_chart(data, metrics, group_cols, method_col, methods_to_plot, group_key="all",
                output_path=None, figsize=(7, 7), title=None):
    """Generate a radar/spider chart comparing methods across multiple metrics."""
    if not HAS_MPL:
        print("matplotlib is required for plotting. Install: pip install matplotlib", file=sys.stderr)
        return None

    _setup_style()

    import numpy as np

    # Extract values: {method: {metric: value}}
    method_values = {}
    for method in methods_to_plot:
        method_values[method] = {}
        for (gk, m), vals in data.items():
            if m == method and (group_key == "all" or _group_label(gk) == group_key):
                for metric in metrics:
                    if metric in vals:
                        method_values[method][metric] = vals[metric]
                break

    n_metrics = len(metrics)
    angles = np.linspace(0, 2 * np.pi, n_metrics, endpoint=False).tolist()
    angles += angles[:1]  # Close the polygon

    fig, ax = plt.subplots(figsize=figsize, subplot_kw={"projection": "polar"})

    for i, (method, vals) in enumerate(method_values.items()):
        values_list = [vals.get(m, 0) for m in metrics]
        values_list += values_list[:1]
        color = PALETTE_TOL[i % len(PALETTE_TOL)]
        ax.fill(angles, values_list, alpha=0.1, color=color)
        ax.plot(angles, values_list, "o-", linewidth=2, color=color, label=method, markersize=5)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics, fontsize=10)
    ax.set_title(title or "Multi-Metric Comparison", pad=20, fontsize=13)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.0), framealpha=0.9)
    ax.grid(True, alpha=0.3)

    if output_path:
        fig.savefig(output_path)
        plt.close(fig)
        print(f"Saved: {output_path}", file=sys.stderr)
    return fig


def pareto_frontier(data, x_metric, y_metric, group_cols, method_col,
                    output_path=None, figsize=(7, 6), title=None):
    """Plot a Pareto frontier: accuracy vs. efficiency trade-off."""
    if not HAS_MPL:
        print("matplotlib is required for plotting. Install: pip install matplotlib", file=sys.stderr)
        return None

    _setup_style()

    fig, ax = plt.subplots(figsize=figsize)

    methods_seen = set()
    for (group_key, method), vals in data.items():
        if method in methods_seen:
            continue
        if x_metric in vals and y_metric in vals:
            methods_seen.add(method)
            ax.scatter(vals[x_metric], vals[y_metric], s=80, alpha=0.8,
                       edgecolors="black", linewidth=0.3)
            ax.annotate(method, (vals[x_metric], vals[y_metric]),
                        textcoords="offset points", xytext=(5, 5), fontsize=8)

    ax.set_xlabel(x_metric)
    ax.set_ylabel(y_metric)
    ax.set_title(title or f"Trade-off: {y_metric} vs {x_metric}")
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    if output_path:
        fig.savefig(output_path)
        plt.close(fig)
        print(f"Saved: {output_path}", file=sys.stderr)
    return fig


def improvement_heatmap(data, metric, group_cols, method_col, baseline_method=None,
                         output_path=None, figsize=(10, 5), title=None):
    """Generate a heatmap showing improvement over a baseline across groups."""
    if not HAS_MPL:
        print("matplotlib is required for plotting. Install: pip install matplotlib", file=sys.stderr)
        return None

    _setup_style()

    import numpy as np

    # Find all groups and methods
    groups_set = set()
    methods_set = set()
    for (gk, _), _vals in data.items():
        groups_set.add(gk)

    groups_order = sorted(groups_set, key=lambda g: str(g))
    group_labels = [_group_label(g) for g in groups_order]

    # Get baseline values per group
    baseline_vals = {}
    for (gk, method), vals in data.items():
        if baseline_method and method == baseline_method and metric in vals:
            baseline_vals[gk] = vals[metric]

    if not baseline_vals and not baseline_method:
        # Use minimum value per group as baseline
        for gk in groups_order:
            group_vals = []
            for (gkk, method), vals in data.items():
                if gkk == gk and metric in vals:
                    group_vals.append(vals[metric])
            baseline_vals[gk] = min(group_vals) if group_vals else 0

    # Build improvement matrix: [n_methods x n_groups]
    for (gk, method), vals in data.items():
        if metric in vals and method not in methods_set:
            methods_set.add(method)
    methods_list = sorted(methods_set, key=lambda m: (baseline_method and m == baseline_method, m))
    if baseline_method and baseline_method in methods_list:
        methods_list.remove(baseline_method)

    matrix = np.zeros((len(methods_list), len(groups_order)))
    for i, method in enumerate(methods_list):
        for j, gk in enumerate(groups_order):
            val = None
            for (gkk, m), vals in data.items():
                if gkk == gk and m == method and metric in vals:
                    val = vals[metric]
                    break
            if val is not None and gk in baseline_vals:
                matrix[i, j] = val - baseline_vals[gk]

    fig, ax = plt.subplots(figsize=figsize)
    im = ax.imshow(matrix, cmap="RdYlGn", aspect="auto", vmin=matrix.min(), vmax=matrix.max())

    ax.set_xticks(range(len(groups_order)))
    ax.set_xticklabels(group_labels)
    ax.set_yticks(range(len(methods_list)))
    ax.set_yticklabels(methods_list)
    ax.set_title(title or f"Improvement in {metric} over {baseline_method or 'best baseline'}")

    # Annotate cells
    for i in range(len(methods_list)):
        for j in range(len(groups_order)):
            val = matrix[i, j]
            color = "white" if abs(val) > matrix.max() * 0.5 else "black"
            ax.text(j, i, f"{val:+.2f}", ha="center", va="center", fontsize=9, color=color)

    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label(f"Δ {metric}")

    if output_path:
        fig.savefig(output_path)
        plt.close(fig)
        print(f"Saved: {output_path}", file=sys.stderr)
    return fig


# ── Export Functions ───────────────────────────────────────────────────────────────

def export_plot_data(data, metric_cols, group_cols, output_path):
    """Export structured plotting data as JSON for external tools (TikZ, Plotly, etc.)."""
    export = {
        "datasets": [],
        "methods": [],
        "metrics": metric_cols,
    }

    groups_set = set()
    methods_set = set()
    for (gk, method), _vals in data.items():
        groups_set.add(gk)
        methods_set.add(method)

    export["datasets"] = [list(g) if isinstance(g, tuple) else g for g in sorted(groups_set)]
    export["methods"] = sorted(methods_set)
    export["data"] = {}
    for group_key in sorted(groups_set):
        group_name = _group_label(group_key)
        export["data"][group_name] = {}
        for method in sorted(methods_set):
            if (group_key, method) in data:
                export["data"][group_name][method] = {
                    k: v for k, v in data[(group_key, method)].items()
                }

    Path(output_path).write_text(json.dumps(export, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Plot data exported to {output_path}", file=sys.stderr)


def export_tikz_data(data, metric, group_cols, output_path):
    """Export data as a simple format suitable for PGFPlots."""
    lines = []
    lines.append(f"% PGFPlots data for {metric}")
    groups_set = set()
    for (gk, _), _vals in data.items():
        groups_set.add(gk)
    groups_order = sorted(groups_set, key=str)

    for gk in groups_order:
        lines.append(f"% {_group_label(gk)}")
        for (gkk, method), vals in data.items():
            if gkk == gk and metric in vals:
                std_val = vals.get(f"{metric}_std", 0)
                lines.append(f"{method} {vals[metric]:.4f} {std_val:.4f}")

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"PGFPlots data exported to {output_path}", file=sys.stderr)


# ── CLI ────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate publication-quality figures from experiment results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Bar chart for each metric
  python result_visualizer.py results.csv --metrics R@1 R@5 --output-dir ./figures/

  # Highlight target method, generate PDF and PGF
  python result_visualizer.py results.csv --target SGA-Ours --metrics R@1 \\
      --format pdf,pgf --output-dir ./figures/

  # Ablation waterfall
  python result_visualizer.py results.csv --ablation \\
      --ablation-order "Full SGA,SGA-Ours;w/o S-R,SGA-NoSR;w/o HML,SGA-NoHML;w/o Both,SGA-NoBoth" \\
      --metrics R@1 --output-dir ./figures/

  # Radar chart for multi-metric comparison
  python result_visualizer.py results.csv --radar --metrics R@1 R@5 R@10 \\
      --plot-methods "SGA-Ours,CLIP-ViT,BLIP,SCAN,CHAN" --output-dir ./figures/
        """,
    )

    parser.add_argument("csv_file", help="Path to CSV results file")
    parser.add_argument("--target", help="Target/proposed method name (highlighted in plots)")
    parser.add_argument("--metrics", nargs="+", help="Metrics to plot (default: all numeric columns)")
    parser.add_argument("--method-col", default="Method", help="Column containing method names")
    parser.add_argument("--output-dir", default="./figures", help="Output directory for figures")
    parser.add_argument("--format", default="pdf", help="Output formats: png,pdf,svg,pgf,json (comma-separated)")
    parser.add_argument("--figsize", default="8,5", help="Figure size in inches: width,height (default: 8,5)")
    parser.add_argument("--dpi", type=int, default=300, help="Output DPI for raster formats")
    parser.add_argument("--ablation", action="store_true", help="Generate ablation waterfall chart")
    parser.add_argument("--ablation-order", help="Ablation order: 'Label1,Method1;Label2,Method2;...'")
    parser.add_argument("--radar", action="store_true", help="Generate radar chart")
    parser.add_argument("--plot-methods", help="Methods to include in radar/pareto: 'M1,M2,M3'")
    parser.add_argument("--group", default="all", help="Group/dataset for single-group plots")
    parser.add_argument("--baseline", help="Baseline method for improvement heatmap")
    parser.add_argument("--heatmap", action="store_true", help="Generate improvement heatmap")
    parser.add_argument("--pareto", action="store_true", help="Generate Pareto frontier (specify two metrics)")
    parser.add_argument("--x-metric", help="X-axis metric for Pareto plot")
    parser.add_argument("--y-metric", help="Y-axis metric for Pareto plot")
    parser.add_argument("--no-bar", action="store_true", help="Skip bar chart generation")

    args = parser.parse_args()

    if not HAS_MPL:
        print("Error: matplotlib is required. Install: pip install matplotlib", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    formats = [f.strip() for f in args.format.lower().split(",")]
    figsize = tuple(float(x) for x in args.figsize.split(","))

    data, metric_cols, std_cols, group_cols = parse_csv(args.csv_file, args.method_col)

    metrics_to_plot = args.metrics if args.metrics else metric_cols
    if not metrics_to_plot:
        print("No numeric metric columns found in CSV.", file=sys.stderr)
        sys.exit(1)

    # Generate requested plots
    plot_count = 0
    for fmt in formats:
        if fmt == "json":
            export_plot_data(data, metric_cols, group_cols,
                             os.path.join(args.output_dir, "plot_data.json"))
            plot_count += 1
        elif fmt == "pgf":
            for metric in metrics_to_plot:
                export_tikz_data(data, metric, group_cols,
                                 os.path.join(args.output_dir, f"data_{metric}.dat"))

    # Bar charts
    if not args.no_bar:
        for fmt in [f for f in formats if f in ("png", "pdf", "svg")]:
            for metric in metrics_to_plot:
                fname = os.path.join(args.output_dir, f"bar_{metric}.{fmt}")
                bar_chart(data, metric, group_cols, args.method_col, args.target,
                          output_path=fname, figsize=figsize)
                plot_count += 1

    # Ablation waterfall
    if args.ablation and args.ablation_order:
        order = []
        for pair in args.ablation_order.split(";"):
            parts = pair.split(",")
            if len(parts) == 2:
                order.append((parts[0].strip(), parts[1].strip()))
        for fmt in [f for f in formats if f in ("png", "pdf", "svg")]:
            for metric in metrics_to_plot:
                fname = os.path.join(args.output_dir, f"ablation_{metric}.{fmt}")
                ablation_waterfall(data, metric, group_cols, args.method_col,
                                   args.target, order, output_path=fname, figsize=figsize)
                plot_count += 1

    # Radar chart
    if args.radar and args.plot_methods:
        methods = [m.strip() for m in args.plot_methods.split(",")]
        for fmt in [f for f in formats if f in ("png", "pdf", "svg")]:
            fname = os.path.join(args.output_dir, f"radar.{fmt}")
            radar_chart(data, metrics_to_plot, group_cols, args.method_col, methods,
                        group_key=args.group, output_path=fname, figsize=(7, 7))
            plot_count += 1

    # Improvement heatmap
    if args.heatmap:
        for fmt in [f for f in formats if f in ("png", "pdf", "svg")]:
            for metric in metrics_to_plot:
                fname = os.path.join(args.output_dir, f"heatmap_{metric}.{fmt}")
                improvement_heatmap(data, metric, group_cols, args.method_col,
                                    baseline_method=args.baseline,
                                    output_path=fname, figsize=figsize)
                plot_count += 1

    # Pareto frontier
    if args.pareto and args.x_metric and args.y_metric:
        for fmt in [f for f in formats if f in ("png", "pdf", "svg")]:
            fname = os.path.join(args.output_dir, f"pareto.{fmt}")
            pareto_frontier(data, args.x_metric, args.y_metric, group_cols,
                            args.method_col, output_path=fname, figsize=figsize)
            plot_count += 1

    if plot_count == 0:
        print(f"No plots generated. Check your format and plot type selections.", file=sys.stderr)
    else:
        print(f"Generated {plot_count} output(s) in {args.output_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
