#!/usr/bin/env python3
"""Generate publication-grade experimental statistical figures from CSV results.

This script is intentionally narrower than result_visualizer.py. It is meant for
figures that can be inserted into SCI/IEEE-style manuscripts, with traceable
values, vector output, a manifest, and conservative defaults.

Examples:
    python publication_figures.py results.csv --target Ours --metrics Acc F1 --higher-better Acc F1 --group-col Dataset --output-dir figures
    python publication_figures.py results.csv --target Ours --metrics Acc F1 Params --higher-better Acc F1 --lower-better Params --formats png pdf svg
    python publication_figures.py results.csv --target Ours --metrics Acc F1 --dry-run
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


PALETTE = [
    "#0072B2",  # blue
    "#D55E00",  # vermillion
    "#009E73",  # green
    "#CC79A7",  # purple
    "#E69F00",  # orange
    "#56B4E9",  # sky blue
    "#000000",  # black
]


def to_float(value):
    try:
        text = str(value).strip().replace("%", "").replace(",", "")
        if not text:
            return None
        parsed = float(text)
        if math.isnan(parsed):
            return None
        return parsed
    except Exception:
        return None


def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def require_columns(rows, columns):
    if not rows:
        raise SystemExit("empty CSV table")
    missing = [col for col in columns if col and col not in rows[0]]
    if missing:
        raise SystemExit(f"missing columns: {', '.join(missing)}")


def unique_values(rows, column):
    values = []
    for row in rows:
        value = row.get(column, "") if column else "all"
        if value not in values:
            values.append(value)
    return values


def grouped_rows(rows, group_col):
    groups = {}
    for row in rows:
        group = row.get(group_col, "all") if group_col else "all"
        groups.setdefault(group, []).append(row)
    return groups


def metric_direction(metric, higher_better, lower_better):
    if metric in higher_better:
        return "higher"
    if metric in lower_better:
        return "lower"
    return "higher"


def best_baseline(rows, method_col, target, metric, direction, baseline_methods):
    best = None
    for row in rows:
        method = row.get(method_col, "")
        if method == target:
            continue
        if baseline_methods and method not in baseline_methods:
            continue
        value = to_float(row.get(metric))
        if value is None:
            continue
        if best is None:
            best = (method or "baseline", value)
        elif direction == "higher" and value > best[1]:
            best = (method or "baseline", value)
        elif direction == "lower" and value < best[1]:
            best = (method or "baseline", value)
    return best


def safe_name(text):
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in str(text)).strip("_") or "metric"


def import_matplotlib():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        raise SystemExit("matplotlib is required for figure generation. Install matplotlib or run with --dry-run.") from exc
    return plt


def apply_style(plt, dpi):
    plt.rcParams.update(
        {
            "figure.dpi": 150,
            "savefig.dpi": dpi,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.04,
            "font.family": "serif",
            "font.size": 9,
            "axes.labelsize": 9,
            "axes.titlesize": 10,
            "legend.fontsize": 8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "grid.linewidth": 0.5,
        }
    )


def save_figure(fig, output_dir, stem, formats):
    paths = []
    for fmt in formats:
        path = output_dir / f"{stem}.{fmt}"
        fig.savefig(path)
        paths.append(path)
    return paths


def plot_grouped_bars(rows, args, plt):
    methods = unique_values(rows, args.method_col)
    groups = unique_values(rows, args.group_col) if args.group_col else ["all"]
    group_map = grouped_rows(rows, args.group_col)
    outputs = []
    notes = []

    for metric in args.metrics:
        fig_width = max(4.2, 0.75 * len(groups) + 1.4)
        fig, ax = plt.subplots(figsize=(fig_width, 3.0), constrained_layout=True)
        width = min(0.82 / max(len(methods), 1), 0.2)
        x_positions = list(range(len(groups)))

        for method_idx, method in enumerate(methods):
            values = []
            for group in groups:
                match = next((row for row in group_map.get(group, []) if row.get(args.method_col) == method), None)
                value = to_float(match.get(metric)) if match else None
                values.append(value)
                if value is None:
                    notes.append(f"missing value: group={group}, method={method}, metric={metric}")
            offsets = [x + (method_idx - (len(methods) - 1) / 2) * width for x in x_positions]
            bars = ax.bar(
                offsets,
                [0 if value is None else value for value in values],
                width=width,
                label=method,
                color=PALETTE[method_idx % len(PALETTE)],
                edgecolor="black",
                linewidth=0.35,
                alpha=1.0 if method == args.target else 0.82,
            )
            for bar, value in zip(bars, values):
                if value is None:
                    bar.set_alpha(0.15)

        ax.set_ylabel(metric)
        ax.set_xlabel(args.group_col if args.group_col else "Setting")
        ax.set_xticks(x_positions)
        ax.set_xticklabels(groups, rotation=25 if max((len(g) for g in groups), default=0) > 10 else 0, ha="right")
        ax.legend(frameon=False, ncol=min(len(methods), 3))
        ax.set_title(f"Comparison on {metric}")
        outputs.extend(save_figure(fig, args.output_dir, f"fig_main_comparison_{safe_name(metric)}", args.formats))
        plt.close(fig)
    return outputs, notes


def plot_improvement_heatmap(rows, args, plt):
    if not args.target:
        return [], ["target method not specified; improvement heatmap skipped"]
    groups = unique_values(rows, args.group_col) if args.group_col else ["all"]
    group_map = grouped_rows(rows, args.group_col)
    higher = set(args.higher_better)
    lower = set(args.lower_better)
    baselines = set(args.baseline_methods)
    matrix = []
    notes = []

    for group in groups:
        group_rows = group_map.get(group, [])
        target_row = next((row for row in group_rows if row.get(args.method_col) == args.target), None)
        row_values = []
        for metric in args.metrics:
            direction = metric_direction(metric, higher, lower)
            target_value = to_float(target_row.get(metric)) if target_row else None
            baseline = best_baseline(group_rows, args.method_col, args.target, metric, direction, baselines)
            if target_value is None or baseline is None:
                row_values.append(0.0)
                notes.append(f"missing heatmap value: group={group}, metric={metric}")
            else:
                diff = target_value - baseline[1] if direction == "higher" else baseline[1] - target_value
                row_values.append(diff)
        matrix.append(row_values)

    fig_width = max(4.2, 0.72 * len(args.metrics) + 1.6)
    fig_height = max(2.8, 0.45 * len(groups) + 1.2)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), constrained_layout=True)
    vmax = max((abs(value) for row in matrix for value in row), default=1.0) or 1.0
    image = ax.imshow(matrix, cmap="RdBu_r", vmin=-vmax, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(args.metrics)))
    ax.set_xticklabels(args.metrics)
    ax.set_yticks(range(len(groups)))
    ax.set_yticklabels(groups)
    ax.set_title(f"{args.target} vs. strongest baseline")
    for row_idx, row in enumerate(matrix):
        for col_idx, value in enumerate(row):
            color = "white" if abs(value) > vmax * 0.55 else "black"
            ax.text(col_idx, row_idx, f"{value:.3g}", ha="center", va="center", color=color, fontsize=8)
    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label("Absolute improvement")
    outputs = save_figure(fig, args.output_dir, "fig_improvement_heatmap", args.formats)
    plt.close(fig)
    return outputs, notes


def write_manifest(output_dir, args, paths, notes):
    lines = [
        "# Experimental Figure Manifest",
        "",
        f"- Source table: `{args.csv_file}`",
        f"- Target method: `{args.target or 'not specified'}`",
        f"- Method column: `{args.method_col}`",
        f"- Group column: `{args.group_col or 'none'}`",
        f"- Metrics: `{', '.join(args.metrics)}`",
        "",
        "## Generated Figures",
        "",
    ]
    if paths:
        for path in paths:
            lines.append(f"- `{path.name}`")
    else:
        lines.append("- AUTHOR_INPUT_NEEDED: no figures generated.")
    lines.extend(
        [
            "",
            "## Caption Templates",
            "",
            "- Main comparison: Quantitative comparison across methods and settings. Values are taken directly from the source table.",
            "- Improvement heatmap: Absolute improvement of the target method over the strongest listed baseline. Positive values indicate better performance according to each metric direction.",
            "",
            "## Notes",
            "",
        ]
    )
    lines.extend(f"- {note}" for note in notes) if notes else lines.append("- No missing values detected by the script.")
    path = output_dir / "figure_manifest.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_plan(rows, args):
    methods = unique_values(rows, args.method_col)
    groups = unique_values(rows, args.group_col) if args.group_col else ["all"]
    lines = [
        "# Experimental Figure Plan",
        "",
        f"- Methods: {', '.join(methods)}",
        f"- Groups: {', '.join(groups)}",
        f"- Metrics: {', '.join(args.metrics)}",
        "",
        "## Planned Figures",
        "",
        "- Grouped bar chart for each metric.",
    ]
    if args.target:
        lines.append("- Improvement heatmap for the target method against the strongest listed baseline.")
    else:
        lines.append("- AUTHOR_INPUT_NEEDED: target method is required for improvement heatmap.")
    path = args.output_dir / "figure_plan.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser(description="Generate publication-grade experimental figures from CSV results")
    parser.add_argument("csv_file")
    parser.add_argument("--output-dir", default="figures")
    parser.add_argument("--method-col", default="Method")
    parser.add_argument("--group-col", default="Dataset")
    parser.add_argument("--target", default="")
    parser.add_argument("--metrics", nargs="+", required=True)
    parser.add_argument("--higher-better", nargs="*", default=[])
    parser.add_argument("--lower-better", nargs="*", default=[])
    parser.add_argument("--baseline-methods", nargs="*", default=[])
    parser.add_argument("--formats", nargs="+", default=["png", "pdf"], choices=["png", "pdf", "svg"])
    parser.add_argument("--dpi", type=int, default=600)
    parser.add_argument("--dry-run", action="store_true", help="Validate data and write a figure plan without importing matplotlib")
    args = parser.parse_args()

    args.output_dir = Path(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = read_rows(args.csv_file)
    required = [args.method_col, *args.metrics]
    if args.group_col:
        required.append(args.group_col)
    require_columns(rows, required)

    if args.dry_run:
        path = write_plan(rows, args)
        print(f"wrote {path}")
        return

    plt = import_matplotlib()
    apply_style(plt, args.dpi)
    paths = []
    notes = []
    bar_paths, bar_notes = plot_grouped_bars(rows, args, plt)
    heatmap_paths, heatmap_notes = plot_improvement_heatmap(rows, args, plt)
    paths.extend(bar_paths)
    paths.extend(heatmap_paths)
    notes.extend(bar_notes)
    notes.extend(heatmap_notes)
    manifest = write_manifest(args.output_dir, args, paths, notes)
    print(f"wrote {manifest}")


if __name__ == "__main__":
    main()
