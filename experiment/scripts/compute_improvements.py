#!/usr/bin/env python3
"""Compute pairwise improvements from a CSV result table.

Usage:
    python compute_improvements.py results.csv --method-col Method --target Proposed --metrics Acc F1 --higher-better Acc F1
    python compute_improvements.py results.csv --target Ours --metrics Acc Params --higher-better Acc --lower-better Params --group-cols Dataset
"""
from __future__ import annotations
import argparse
import csv
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


def format_number(value):
    return f"{value:.6g}"


def format_relative(value):
    return "n/a" if value is None else f"{value:.2f}%"


def main():
    p = argparse.ArgumentParser()
    p.add_argument('csv_file')
    p.add_argument('--method-col', default='Method')
    p.add_argument('--target', required=True)
    p.add_argument('--metrics', nargs='+', required=True)
    p.add_argument('--higher-better', nargs='*', default=[])
    p.add_argument('--lower-better', nargs='*', default=[])
    p.add_argument('--group-cols', nargs='*', default=[])
    p.add_argument('--baseline-methods', nargs='*', default=[])
    p.add_argument('--output', default='improvements.md')
    args = p.parse_args()

    with open(args.csv_file, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))

    missing_columns = [
        col for col in [args.method_col, *args.metrics, *args.group_cols]
        if rows and col not in rows[0]
    ]
    if missing_columns:
        raise SystemExit(f"missing columns: {', '.join(missing_columns)}")

    groups = {}
    for row in rows:
        groups.setdefault(row_group(row, args.group_cols), []).append(row)

    higher = set(args.higher_better)
    lower = set(args.lower_better)
    baseline_methods = set(args.baseline_methods)
    lines = [
        '# Improvement Summary',
        '',
        f'- Source: `{args.csv_file}`',
        f'- Target method: `{args.target}`',
        f'- Group columns: `{", ".join(args.group_cols) if args.group_cols else "none"}`',
        '',
        '| Group | Metric | Direction | Target | Strongest Baseline | Baseline | Absolute Improvement | Relative Improvement |',
        '|---|---:|---|---:|---|---:|---:|---:|',
    ]

    emitted = False
    for group, group_rows in sorted(groups.items()):
        target_rows = [row for row in group_rows if row.get(args.method_col) == args.target]
        if not target_rows:
            lines.append(f'| {group_label(args.group_cols, group)} | all | n/a | n/a | n/a | n/a | n/a | target method not found |')
            continue
        target = target_rows[0]
        for metric in args.metrics:
            direction = metric_direction(metric, higher, lower)
            target_value = to_float(target.get(metric))
            if target_value is None:
                lines.append(f'| {group_label(args.group_cols, group)} | {metric} | {direction} | n/a | n/a | n/a | n/a | target value is not numeric |')
                continue
            base = best_baseline(group_rows, args.method_col, args.target, metric, direction, baseline_methods)
            if base is None:
                lines.append(f'| {group_label(args.group_cols, group)} | {metric} | {direction} | {format_number(target_value)} | n/a | n/a | n/a | no numeric baseline found |')
                continue
            diff = target_value - base[1] if direction == "higher" else base[1] - target_value
            rel = diff / abs(base[1]) * 100 if base[1] != 0 else None
            lines.append(
                f'| {group_label(args.group_cols, group)} | {metric} | {direction} | '
                f'{format_number(target_value)} | {base[0]} | {format_number(base[1])} | '
                f'{format_number(diff)} | {format_relative(rel)} |'
            )
            emitted = True

    if not emitted and not any(row.get(args.method_col) == args.target for row in rows):
        raise SystemExit(f'target method not found: {args.target}')

    Path(args.output).write_text('\n'.join(lines), encoding='utf-8')
    print(f'wrote {args.output}')

if __name__ == '__main__':
    main()
