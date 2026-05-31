#!/usr/bin/env python3
"""Compute pairwise improvements from a CSV result table.

Usage:
    python compute_improvements.py results.csv --method-col Method --target Proposed --metrics Acc F1 --higher-better Acc F1
    python compute_improvements.py results.csv --target Ours --metrics Acc Params --higher-better Acc --lower-better Params --group-cols Dataset
    python compute_improvements.py results.csv --target Ours --metrics R@1 R@5 --higher-better R@1 R@5 --group-cols Dataset --stats --bootstrap 10000
    python compute_improvements.py results.csv --all-pairs --metrics Acc --higher-better Acc --format json
    python compute_improvements.py seeds_results.csv --target Ours --metrics R@1 --higher-better R@1 --seed-col Seed --group-cols Dataset

New in v0.4:
    - Automatic _std column detection and error reporting
    - --stats flag for bootstrap confidence intervals
    - --all-pairs for full pairwise comparison matrix
    - --format json for machine-readable output
    - --seed-col for multi-seed/repetition data
    - --top-k to show only top K baselines
"""
from __future__ import annotations
import argparse
import csv
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path


def to_float(x):
    try:
        text = str(x).strip().replace('%', '').replace(',', '')
        return float(text)
    except Exception:
        return None


def row_group(row, group_cols):
    if not group_cols:
        return ("all",)
    return tuple(row.get(col, "") for col in group_cols)


def group_label(group_cols, group):
    if not group_cols:
        return "all"
    return ", ".join(f"{col}={value}" for col, value in zip(group_cols, group))


def metric_direction(metric, higher_better, lower_better):
    if metric in higher_better:
        return "higher"
    if metric in lower_better:
        return "lower"
    return "lower"


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


def all_baselines_sorted(rows, method_col, target, metric, direction, baseline_methods):
    """Return all baselines sorted from best to worst."""
    results = []
    for row in rows:
        method = row.get(method_col, "")
        if method == target:
            continue
        if baseline_methods and method not in baseline_methods:
            continue
        value = to_float(row.get(metric))
        if value is None:
            continue
        results.append((method or "baseline", value))
    reverse = direction == "higher"
    results.sort(key=lambda x: x[1], reverse=reverse)
    return results


def find_std_column(metric, all_columns):
    """Find matching standard deviation column for a metric."""
    candidates = [f"{metric}_std", f"{metric}_stdev", f"{metric}_err",
                   f"{metric}_stddev", f"std_{metric}", f"stdev_{metric}"]
    for c in candidates:
        if c in all_columns:
            return c
    return None


def bootstrap_mean_ci(values, n_bootstrap=10000, alpha=0.05, seed=42):
    """Compute bootstrap confidence interval for the mean of a list."""
    rng = random.Random(seed)
    n = len(values)
    estimate = sum(values) / n
    boot_means = []
    for _ in range(n_bootstrap):
        sample = [rng.choice(values) for _ in range(n)]
        boot_means.append(sum(sample) / n)
    boot_means.sort()
    lower_idx = int(n_bootstrap * alpha / 2)
    upper_idx = int(n_bootstrap * (1 - alpha / 2)) - 1
    return boot_means[lower_idx], boot_means[upper_idx], estimate


def compute_improvement_with_ci(target_values, baseline_values, direction, n_bootstrap=10000, alpha=0.05):
    """Compute improvement with bootstrap CI from multi-seed data."""
    target_mean = sum(target_values) / len(target_values)
    baseline_mean = sum(baseline_values) / len(baseline_values)
    raw_diff = target_mean - baseline_mean if direction == "higher" else baseline_mean - target_mean
    rel = (raw_diff / abs(baseline_mean) * 100) if baseline_mean != 0 else None

    # Bootstrap CI on the difference
    rng = random.Random(42)
    n = len(target_values)
    boot_diffs = []
    for _ in range(n_bootstrap):
        indices = [rng.randrange(n) for _ in range(n)]
        t_sample = [target_values[i] for i in indices]
        b_sample = [baseline_values[i] for i in indices]
        t_mean = sum(t_sample) / n
        b_mean = sum(b_sample) / n
        d = t_mean - b_mean if direction == "higher" else b_mean - t_mean
        boot_diffs.append(d)
    boot_diffs.sort()
    lower_idx = int(n_bootstrap * alpha / 2)
    upper_idx = int(n_bootstrap * (1 - alpha / 2)) - 1
    return raw_diff, rel, boot_diffs[lower_idx], boot_diffs[upper_idx]


def format_number(value):
    return f"{value:.6g}"


def format_relative(value):
    return "n/a" if value is None else f"{value:.2f}%"


def main():
    p = argparse.ArgumentParser(
        description="Compute pairwise improvements from CSV experiment results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (v0.3 compatible)
  python compute_improvements.py results.csv --target Ours --metrics Acc F1 --higher-better Acc F1

  # With std columns, bootstrap CI, and group-by dataset
  python compute_improvements.py results.csv --target SGA-Ours --metrics R@1 R@5 R@10 \\
      --higher-better R@1 R@5 R@10 --group-cols Dataset --stats --bootstrap 10000

  # All-pairs comparison matrix as JSON
  python compute_improvements.py results.csv --all-pairs --metrics Acc --higher-better Acc --format json

  # Multi-seed data with bootstrap
  python compute_improvements.py seeds.csv --target Ours --metrics Acc --higher-better Acc \\
      --seed-col Seed --stats --bootstrap 5000
        """,
    )
    p.add_argument('csv_file')
    p.add_argument('--method-col', default='Method')
    p.add_argument('--target', help='Name of the proposed/target method (omit with --all-pairs)')
    p.add_argument('--metrics', nargs='+', required=True)
    p.add_argument('--higher-better', nargs='*', default=[])
    p.add_argument('--lower-better', nargs='*', default=[])
    p.add_argument('--group-cols', nargs='*', default=[])
    p.add_argument('--baseline-methods', nargs='*', default=[])
    p.add_argument('--output', default='improvements.md')
    p.add_argument('--format', dest='fmt', default='markdown', choices=['markdown', 'json'],
                   help='Output format (default: markdown)')
    p.add_argument('--stats', action='store_true', help='Include bootstrap confidence intervals')
    p.add_argument('--bootstrap', type=int, default=10000, help='Bootstrap resamples for --stats (default: 10000)')
    p.add_argument('--alpha', type=float, default=0.05, help='Significance level for CI (default: 0.05)')
    p.add_argument('--all-pairs', action='store_true', help='Compare all method pairs, not just vs target')
    p.add_argument('--top-k', type=int, default=0, help='Show only top K baselines per metric-group (0=all)')
    p.add_argument('--seed-col', help='Column identifying different seeds/runs for bootstrap')
    args = p.parse_args()

    if not args.target and not args.all_pairs:
        raise SystemExit("Either --target or --all-pairs is required.")

    with open(args.csv_file, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise SystemExit("CSV file is empty or unparseable.")

    all_columns = list(rows[0].keys())

    # Check required columns exist
    required_cols = [args.method_col, *args.metrics]
    if not args.all_pairs and args.target:
        required_cols.extend(args.group_cols)
    missing_columns = [col for col in required_cols if col not in all_columns and col]
    if missing_columns:
        raise SystemExit(f"missing columns: {', '.join(missing_columns)}")

    higher = set(args.higher_better)
    lower = set(args.lower_better)
    # Metrics not explicitly specified default to higher-is-better
    for m in args.metrics:
        if m not in higher and m not in lower:
            higher.add(m)

    baseline_methods = set(args.baseline_methods)

    # Detect std columns
    std_col_map = {}
    for metric in args.metrics:
        std_col = find_std_column(metric, all_columns)
        if std_col:
            std_col_map[metric] = std_col

    if std_col_map and not args.stats:
        print(f"Note: detected std columns: {std_col_map}. Use --stats for confidence intervals.", file=sys.stderr)

    # Multi-seed mode
    if args.seed_col and args.seed_col in all_columns:
        results = _compute_multi_seed(rows, args, higher, lower, baseline_methods, std_col_map)
    elif args.all_pairs:
        results = _compute_all_pairs(rows, args, higher, lower, baseline_methods)
    else:
        results = _compute_target_vs_baselines(rows, args, higher, lower, baseline_methods, std_col_map)

    # Output
    if args.fmt == 'json':
        output_text = json.dumps(results, indent=2, ensure_ascii=False, default=str)
    else:
        output_text = _format_markdown(results, args, std_col_map)

    Path(args.output).write_text(output_text, encoding='utf-8')
    print(f'wrote {args.output}')


def _compute_target_vs_baselines(rows, args, higher, lower, baseline_methods, std_col_map):
    """Original behavior: target vs best baseline per group/metric."""
    groups = {}
    for row in rows:
        groups.setdefault(row_group(row, args.group_cols), []).append(row)

    results = {
        "source": args.csv_file,
        "target": args.target,
        "metrics": args.metrics,
        "group_cols": args.group_cols,
        "with_stats": args.stats,
        "has_std_cols": bool(std_col_map),
        "comparisons": [],
    }

    for group, group_rows in sorted(groups.items()):
        target_rows = [row for row in group_rows if row.get(args.method_col) == args.target]
        if not target_rows:
            results["comparisons"].append({
                "group": group_label(args.group_cols, group),
                "error": "target method not found in this group",
            })
            continue
        target = target_rows[0]
        for metric in args.metrics:
            direction = metric_direction(metric, higher, lower)
            target_value = to_float(target.get(metric))
            if target_value is None:
                results["comparisons"].append({
                    "group": group_label(args.group_cols, group),
                    "metric": metric,
                    "error": "target value is not numeric",
                })
                continue

            target_std = None
            if std_col_map.get(metric):
                target_std = to_float(target.get(std_col_map[metric]))

            # Get all baselines sorted
            all_bases = all_baselines_sorted(group_rows, args.method_col, args.target, metric, direction, baseline_methods)
            if not all_bases:
                results["comparisons"].append({
                    "group": group_label(args.group_cols, group),
                    "metric": metric,
                    "direction": direction,
                    "target_value": target_value,
                    "error": "no numeric baseline found",
                })
                continue

            # Best baseline (original behavior)
            best = all_bases[0]
            diff = target_value - best[1] if direction == "higher" else best[1] - target_value
            rel = diff / abs(best[1]) * 100 if best[1] != 0 else None

            entry = {
                "group": group_label(args.group_cols, group),
                "metric": metric,
                "direction": direction,
                "target_value": target_value,
                "target_std": target_std,
                "strongest_baseline": best[0],
                "baseline_value": best[1],
                "abs_improvement": diff,
                "rel_improvement_pct": rel,
            }

            # Include all baselines if top_k > 0
            if args.top_k > 0:
                entry["all_baselines"] = [{"name": m, "value": v} for m, v in all_bases[:args.top_k]]

            # Bootstrap CI
            if args.stats:
                all_values = _collect_values_for_bootstrap(
                    group_rows, args.method_col, args.target, best[0], metric, args.seed_col
                )
                if all_values and all_values["target"] and all_values["baseline"]:
                    diff_ci, rel_ci, ci_low, ci_high = compute_improvement_with_ci(
                        all_values["target"], all_values["baseline"], direction, args.bootstrap, args.alpha
                    )
                    entry["bootstrap_ci"] = {
                        "abs_diff_ci": [ci_low, ci_high],
                        "ci_level": f"{(1 - args.alpha) * 100:.0f}%",
                        "n_bootstrap": args.bootstrap,
                    }

            results["comparisons"].append(entry)

    return results


def _compute_all_pairs(rows, args, higher, lower, baseline_methods):
    """All-pairs comparison matrix."""
    groups = {}
    for row in rows:
        groups.setdefault(row_group(row, args.group_cols), []).append(row)

    all_methods = sorted(set(row.get(args.method_col, "").strip() for row in rows if row.get(args.method_col, "").strip()))

    results = {
        "source": args.csv_file,
        "metrics": args.metrics,
        "group_cols": args.group_cols,
        "methods": all_methods,
        "comparisons": [],
    }

    for group, group_rows in sorted(groups.items()):
        for metric in args.metrics:
            direction = metric_direction(metric, higher, lower)
            for method_a in all_methods:
                for method_b in all_methods:
                    if method_a >= method_b:
                        continue  # Only upper triangle
                    val_a = None
                    val_b = None
                    for row in group_rows:
                        m = row.get(args.method_col, "").strip()
                        if m == method_a:
                            val_a = to_float(row.get(metric))
                        if m == method_b:
                            val_b = to_float(row.get(metric))
                    if val_a is None or val_b is None:
                        continue
                    diff = val_a - val_b if direction == "higher" else val_b - val_a
                    rel = diff / abs(val_b) * 100 if val_b != 0 else None
                    results["comparisons"].append({
                        "group": group_label(args.group_cols, group),
                        "metric": metric,
                        "direction": direction,
                        "method_a": method_a,
                        "value_a": val_a,
                        "method_b": method_b,
                        "value_b": val_b,
                        "abs_diff": diff,
                        "rel_diff_pct": rel,
                        "winner": method_a if diff > 0 else method_b,
                    })

    return results


def _compute_multi_seed(rows, args, higher, lower, baseline_methods, std_col_map):
    """Multi-seed analysis with bootstrap CI."""
    # Collect values per (group, method, seed)
    seed_data = defaultdict(lambda: defaultdict(list))
    for row in rows:
        gk = row_group(row, args.group_cols)
        method = row.get(args.method_col, "").strip()
        for metric in args.metrics:
            val = to_float(row.get(metric))
            if val is not None:
                seed_data[(gk, method)][metric].append(val)

    results = {
        "source": args.csv_file,
        "target": args.target,
        "metrics": args.metrics,
        "group_cols": args.group_cols,
        "with_stats": args.stats,
        "n_bootstrap": args.bootstrap,
        "alpha": args.alpha,
        "comparisons": [],
    }

    groups_set = set(gk for gk, _ in seed_data.keys())

    for gk in sorted(groups_set):
        if (gk, args.target) not in seed_data:
            continue
        target_data = seed_data[(gk, args.target)]

        for metric in args.metrics:
            if metric not in target_data or len(target_data[metric]) < 2:
                continue
            direction = metric_direction(metric, higher, lower)
            target_mean = sum(target_data[metric]) / len(target_data[metric])

            all_bases = []
            for (bgk, method), bdata in seed_data.items():
                if bgk != gk or method == args.target:
                    continue
                if baseline_methods and method not in baseline_methods:
                    continue
                if metric in bdata and len(bdata[metric]) >= 2:
                    baseline_mean = sum(bdata[metric]) / len(bdata[metric])
                    diff = target_mean - baseline_mean if direction == "higher" else baseline_mean - target_mean
                    all_bases.append((method, baseline_mean, diff))

            reverse = True
            all_bases.sort(key=lambda x: x[2], reverse=reverse)
            if not all_bases:
                continue

            best = all_bases[0]
            _, ci_low, ci_high = compute_improvement_with_ci(
                target_data[metric], seed_data[(gk, best[0])][metric],
                direction, args.bootstrap, args.alpha
            )
            rel = best[2] / abs(best[1]) * 100 if best[1] != 0 else None

            entry = {
                "group": group_label(args.group_cols, gk),
                "metric": metric,
                "direction": direction,
                "target_mean": target_mean,
                "target_n": len(target_data[metric]),
                "strongest_baseline": best[0],
                "baseline_mean": best[1],
                "abs_improvement": best[2],
                "rel_improvement_pct": rel,
                "bootstrap_ci": [ci_low, ci_high],
                "ci_level": f"{(1 - args.alpha) * 100:.0f}%",
                "n_bootstrap": args.bootstrap,
            }
            if args.top_k > 0:
                entry["all_baselines"] = [{"name": m, "mean": v, "diff": d} for m, v, d in all_bases[:args.top_k]]
            results["comparisons"].append(entry)

    return results


def _collect_values_for_bootstrap(group_rows, method_col, target, baseline, metric, seed_col):
    """Extract seed-level values when seed_col is available."""
    if not seed_col:
        return None
    seed_map = defaultdict(dict)
    for row in group_rows:
        method = row.get(method_col, "").strip()
        if method not in (target, baseline):
            continue
        seed = row.get(seed_col, "").strip()
        val = to_float(row.get(metric))
        if val is not None:
            seed_map[seed][method] = val
    target_vals = []
    baseline_vals = []
    for seed, methods in seed_map.items():
        if target in methods and baseline in methods:
            target_vals.append(methods[target])
            baseline_vals.append(methods[baseline])
    if len(target_vals) < 2 or len(baseline_vals) < 2:
        return None
    return {"target": target_vals, "baseline": baseline_vals}


def _format_markdown(results, args, std_col_map):
    """Format results as markdown table."""
    lines = [
        '# Improvement Summary',
        '',
        f'- Source: `{results["source"]}`',
    ]
    if results.get("target"):
        lines.append(f'- Target method: `{results["target"]}`')
    lines.append(f'- Group columns: `{", ".join(args.group_cols) if args.group_cols else "none"}`')
    if results.get("with_stats"):
        lines.append(f'- Bootstrap CI: {results.get("ci_level", "95%")}, {results.get("n_bootstrap", 10000)} resamples')
    if std_col_map:
        lines.append(f'- Std columns detected: {std_col_map}')
    lines.append('')

    comparisons = results.get("comparisons", [])
    if not comparisons:
        lines.append("⚠ No comparisons computed.")
        return '\n'.join(lines)

    if results.get("target"):
        # Target vs baselines format
        has_ci = results.get("with_stats") and any("bootstrap_ci" in c for c in comparisons)
        header = '| Group | Metric | Direction | Target' + (' (std)' if std_col_map else '') + \
                 ' | Strongest Baseline | Baseline | Δ Abs | Δ Rel'
        if has_ci:
            header += ' | ' + comparisons[0].get("ci_level", "95%") + ' CI'
        header += ' |'
        sep = '|---|---:|---|---:|---:|---:|---:|---:' + ('|---:|' if has_ci else '|')
        lines.extend([header, sep])

        for c in comparisons:
            if c.get("error"):
                lines.append(f'| {c["group"]} | {c.get("metric", "all")} | n/a | n/a | n/a | n/a | n/a | n/a | {c["error"]} |')
                continue
            target_str = f'{format_number(c.get("target_value", c.get("target_mean", "n/a")))}'
            if c.get("target_std") is not None:
                target_str += f' ± {format_number(c["target_std"])}'
            row = f'| {c["group"]} | {c["metric"]} | {c["direction"]} | {target_str} | ' \
                  f'{c.get("strongest_baseline", "n/a")} | ' \
                  f'{format_number(c.get("baseline_value", c.get("baseline_mean", "n/a")))} | ' \
                  f'{format_number(c.get("abs_improvement", "n/a"))} | ' \
                  f'{format_relative(c.get("rel_improvement_pct"))}'
            if has_ci:
                ci = c.get("bootstrap_ci")
                if ci:
                    row += f' | [{format_number(ci[0])}, {format_number(ci[1])}]'
                else:
                    row += ' | n/a'
            row += ' |'
            lines.append(row)
    else:
        # All-pairs format
        lines.extend([
            '| Group | Metric | Method A | Value A | Method B | Value B | Δ Abs | Δ Rel | Winner |',
            '|---|---:|---:|---:|---:|---:|---:|---:|---:|',
        ])
        for c in comparisons:
            lines.append(
                f'| {c["group"]} | {c["metric"]} | {c["method_a"]} | {format_number(c["value_a"])} | '
                f'{c["method_b"]} | {format_number(c["value_b"])} | {format_number(c["abs_diff"])} | '
                f'{format_relative(c["rel_diff_pct"])} | {c["winner"]} |'
            )

    return '\n'.join(lines)


if __name__ == '__main__':
    main()
