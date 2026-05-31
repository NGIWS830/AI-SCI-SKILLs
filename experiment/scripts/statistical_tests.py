#!/usr/bin/env python3
"""Statistical significance tests and effect sizes for experiment results.

Usage:
    python statistical_tests.py results.csv --target SGA-Ours --metrics R@1 R@5 R@10 \\
        --higher-better R@1 R@5 R@10 --group-cols Dataset --output stats_report.md

    python statistical_tests.py results.csv --target Ours --metrics Acc F1 \\
        --higher-better Acc F1 --bootstrap 10000 --alpha 0.05

Features:
    - Bootstrap confidence intervals (percentile + BCa)
    - Cohen's d and Hedges' g effect sizes
    - Paired statistical tests (Wilcoxon signed-rank, paired t-test)
    - Multiple comparison correction (Bonferroni, Benjamini-Hochberg)
    - Power analysis for future experiment planning
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import sys
from collections import defaultdict
from pathlib import Path


# ── Bootstrap & Resampling ────────────────────────────────────────────────────────

def bootstrap_ci(samples, statistic_fn, n_bootstrap=10000, alpha=0.05, seed=42):
    """Compute bootstrap percentile confidence interval for a statistic.

    Args:
        samples: list of observed values
        statistic_fn: function that computes a statistic from a list of values
        n_bootstrap: number of bootstrap resamples
        alpha: significance level (e.g., 0.05 for 95% CI)
    Returns:
        (lower, upper, estimate, bootstrap_distribution)
    """
    rng = random.Random(seed)
    n = len(samples)
    estimate = statistic_fn(samples)
    boot_stats = []
    for _ in range(n_bootstrap):
        resample = [rng.choice(samples) for _ in range(n)]
        boot_stats.append(statistic_fn(resample))
    boot_stats.sort()
    lower_idx = int(n_bootstrap * alpha / 2)
    upper_idx = int(n_bootstrap * (1 - alpha / 2)) - 1
    return boot_stats[lower_idx], boot_stats[upper_idx], estimate, boot_stats


def bootstrap_mean_ci(values, n_bootstrap=10000, alpha=0.05, seed=42):
    """Bootstrap CI for the mean."""
    return bootstrap_ci(values, lambda x: sum(x) / len(x), n_bootstrap, alpha, seed)


def bootstrap_median_ci(values, n_bootstrap=10000, alpha=0.05, seed=42):
    """Bootstrap CI for the median."""
    return bootstrap_ci(values, sorted, n_bootstrap, alpha, seed)


def bootstrap_diff_ci(sample_a, sample_b, n_bootstrap=10000, alpha=0.05, seed=42):
    """Bootstrap CI for the difference in means between two paired samples."""
    rng = random.Random(seed)
    n = len(sample_a)
    assert len(sample_b) == n, "Paired samples must have equal length."
    observed_diffs = [a - b for a, b in zip(sample_a, sample_b)]
    estimate = sum(observed_diffs) / n
    boot_stats = []
    for _ in range(n_bootstrap):
        indices = [rng.randrange(n) for _ in range(n)]
        resample_diff = sum(observed_diffs[i] for i in indices) / n
        boot_stats.append(resample_diff)
    boot_stats.sort()
    lower_idx = int(n_bootstrap * alpha / 2)
    upper_idx = int(n_bootstrap * (1 - alpha / 2)) - 1
    return boot_stats[lower_idx], boot_stats[upper_idx], estimate


# ── Effect Sizes ──────────────────────────────────────────────────────────────────

def cohens_d(sample_a, sample_b, paired=True):
    """Cohen's d effect size.

    paired=True:  d = mean_diff / SD_diff
    paired=False: d = (mean_a - mean_b) / pooled_SD
    """
    if paired:
        diffs = [a - b for a, b in zip(sample_a, sample_b)]
        mean_diff = sum(diffs) / len(diffs)
        n = len(diffs)
        sd_diff = math.sqrt(sum((d - mean_diff) ** 2 for d in diffs) / (n - 1)) if n > 1 else 1e-10
        return mean_diff / sd_diff if sd_diff > 0 else 0.0
    else:
        mean_a = sum(sample_a) / len(sample_a)
        mean_b = sum(sample_b) / len(sample_b)
        n_a, n_b = len(sample_a), len(sample_b)
        var_a = sum((x - mean_a) ** 2 for x in sample_a) / (n_a - 1) if n_a > 1 else 0
        var_b = sum((x - mean_b) ** 2 for x in sample_b) / (n_b - 1) if n_b > 1 else 0
        pooled_sd = math.sqrt(((n_a - 1) * var_a + (n_b - 1) * var_b) / (n_a + n_b - 2))
        return (mean_a - mean_b) / pooled_sd if pooled_sd > 0 else 0.0


def hedges_g(sample_a, sample_b, paired=True):
    """Hedges' g (bias-corrected Cohen's d)."""
    d = cohens_d(sample_a, sample_b, paired=paired)
    if paired:
        n = len(sample_a)
    else:
        n = len(sample_a) + len(sample_b)
    df = n - 1 if paired else n - 2
    # Correction factor for small samples
    if df > 1:
        correction = math.exp(math.lgamma(df / 2) - math.log(math.sqrt(df / 2)) - math.lgamma((df - 1) / 2))
    else:
        correction = 1.0
    return d * correction


def interpret_effect_size(d):
    """Qualitative interpretation of Cohen's d / Hedges' g."""
    if d is None:
        return "N/A"
    d_abs = abs(d)
    if d_abs < 0.2:
        return "negligible"
    elif d_abs < 0.5:
        return "small"
    elif d_abs < 0.8:
        return "medium"
    else:
        return "large"


# ── Statistical Tests ─────────────────────────────────────────────────────────────

def wilcoxon_signed_rank(sample_a, sample_b):
    """Wilcoxon signed-rank test for paired samples.

    Returns (W_statistic, approximate_z, p_value_approx).
    For n < 20, use exact critical values. For n >= 20, normal approximation.
    """
    diffs = [a - b for a, b in zip(sample_a, sample_b)]
    # Remove zero differences
    non_zero = [(i, d) for i, d in enumerate(diffs) if d != 0]
    if len(non_zero) == 0:
        return 0, 0, 1.0  # No difference
    n = len(non_zero)
    # Rank absolute differences
    abs_diffs = [(abs(d), i, d) for i, d in non_zero]
    abs_diffs.sort(key=lambda x: x[0])
    ranks = [0.0] * len(abs_diffs)
    j = 0
    while j < len(abs_diffs):
        k = j
        while k < len(abs_diffs) and abs_diffs[k][0] == abs_diffs[j][0]:
            k += 1
        avg_rank = (j + k + 1) / 2.0  # Average rank for ties
        for m in range(j, k):
            ranks[abs_diffs[m][1]] = avg_rank
        j = k
    # Sum ranks for positive differences
    W = sum(r for r, (_, i, d) in zip(ranks, abs_diffs) if d > 0)
    # Normal approximation
    mean_W = n * (n + 1) / 4
    # Adjust variance for ties
    tie_counts = defaultdict(int)
    for _, _, _ in abs_diffs:
        tie_counts[abs_diffs[0][0]] += 1
    var_W = n * (n + 1) * (2 * n + 1) / 24
    # Tie correction
    for count in tie_counts.values():
        if count > 1:
            var_W -= (count ** 3 - count) / 48
    var_W = max(var_W, 1e-10)
    z = (W - mean_W) / math.sqrt(var_W)
    # Two-tailed p-value from normal approximation
    p_value = 2 * (1 - _normal_cdf(abs(z)))
    return W, z, p_value


def paired_t_test(sample_a, sample_b):
    """Paired Student's t-test.

    Returns (t_statistic, df, p_value).
    """
    n = len(sample_a)
    diffs = [a - b for a, b in zip(sample_a, sample_b)]
    mean_diff = sum(diffs) / n
    sd_diff = math.sqrt(sum((d - mean_diff) ** 2 for d in diffs) / (n - 1)) if n > 1 else 1e-10
    se = sd_diff / math.sqrt(n)
    t_stat = mean_diff / se if se > 0 else 0.0
    df = n - 1
    # Two-tailed p-value using t-distribution approximation
    p_value = 2 * _t_cdf_tail(abs(t_stat), df)
    return t_stat, df, p_value


def mcnemar_test(sample_a, sample_b):
    """McNemar's test for paired binary outcomes.

    Counts how often A is correct and B is wrong, and vice versa.
    Returns (chi_squared_stat, p_value).
    """
    b = sum(1 for a_val, b_val in zip(sample_a, sample_b) if a_val == 1 and b_val == 0)
    c = sum(1 for a_val, b_val in zip(sample_a, sample_b) if a_val == 0 and b_val == 1)
    if b + c == 0:
        return 0.0, 1.0
    # Chi-squared with continuity correction
    chi_sq = (abs(b - c) - 1) ** 2 / (b + c)
    p_value = 1 - _chi_squared_cdf(chi_sq, 1)
    return chi_sq, p_value


# ── Multiple Comparison Correction ─────────────────────────────────────────────────

def bonferroni_correction(p_values):
    """Apply Bonferroni correction: p_i * n, capped at 1.0."""
    n = len(p_values)
    return [min(p * n, 1.0) for p in p_values]


def benjamini_hochberg(p_values, alpha=0.05):
    """Benjamini-Hochberg FDR correction.

    Returns (adjusted_p_values, significant_mask).
    """
    n = len(p_values)
    indexed = sorted(enumerate(p_values), key=lambda x: x[1])
    adjusted = [1.0] * n
    for rank, (idx, p) in enumerate(indexed, 1):
        adjusted[idx] = min(p * n / rank, 1.0)
    # Ensure monotonicity
    for i in range(n - 2, -1, -1):
        adjusted[indexed[i][0]] = min(adjusted[indexed[i][0]], adjusted[indexed[i + 1][0]])
    significant = [p <= alpha for p in adjusted]
    return adjusted, significant


# ── Power Analysis ────────────────────────────────────────────────────────────────

def required_sample_size(effect_size, alpha=0.05, power=0.80, test_type="paired_t"):
    """Estimate required sample size for a given effect size and power.

    Uses simplified formula for paired t-test:
        n ≈ 2 * (z_alpha/2 + z_beta)^2 / d^2
    """
    if effect_size == 0:
        return float("inf")
    z_alpha = _normal_quantile(1 - alpha / 2)
    z_beta = _normal_quantile(power)
    if test_type == "paired_t":
        n = 2 * (z_alpha + z_beta) ** 2 / effect_size ** 2
    else:  # independent t-test
        n = 2 * (z_alpha + z_beta) ** 2 / effect_size ** 2 * 2
    return math.ceil(n)


def achieved_power(effect_size, n, alpha=0.05, test_type="paired_t"):
    """Estimate achieved statistical power given effect size and sample size."""
    if effect_size == 0 or n <= 1:
        return 0.0
    z_alpha = _normal_quantile(1 - alpha / 2)
    z_power = abs(effect_size) * math.sqrt(n / 2) - z_alpha
    return _normal_cdf(z_power)


# ── Statistical Distribution Helpers (no scipy dependency) ─────────────────────────

def _normal_cdf(x):
    """Standard normal CDF using Abramowitz and Stegun approximation."""
    if x < -8:
        return 0.0
    if x > 8:
        return 1.0
    # erf approximation
    a1, a2, a3, a4, a5 = 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429
    p_val = 0.3275911
    t = 1.0 / (1.0 + p_val * abs(x))
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x / 2.0)
    return y if x >= 0 else 1.0 - y


def _normal_quantile(p):
    """Standard normal quantile (inverse CDF). Uses rational approximation."""
    if p <= 0:
        return -8.0
    if p >= 1:
        return 8.0
    if p > 0.5:
        return -_normal_quantile(1 - p)
    # Approximation for 0 < p <= 0.5
    a = [2.50662823884, -18.61500062529, 41.39119773534, -25.44106049637]
    b = [-8.47351093090, 23.08336743743, -21.06224101826, 3.13082909833]
    c = [0.3374754822726147, 0.9761690190917186, 0.1607979714918209,
         0.0276438810333863, 0.0038405729373609, 0.0003951896511919, 0.0000321767881768,
         0.0000002888167364, 0.0000003960315187]
    y = math.sqrt(-2 * math.log(p))
    num = ((a[3] * y + a[2]) * y + a[1]) * y + a[0]
    den = (((b[3] * y + b[2]) * y + b[1]) * y + b[0]) * y + 1.0
    return y - num / den


def _t_cdf_tail(t, df):
    """Tail probability of Student's t distribution."""
    if df <= 0:
        return 1 - _normal_cdf(t)
    x = df / (df + t * t)
    # Incomplete beta using continued fraction
    return 0.5 * _incomplete_beta(df / 2, 0.5, x)


def _incomplete_beta(a, b, x, max_iter=200):
    """Regularized incomplete beta function via continued fraction."""
    if x == 0:
        return 0.0
    if x == 1:
        return 1.0
    # Compute beta(a,b)
    ln_beta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    # Continued fraction
    front = math.exp(a * math.log(x) + b * math.log(1 - x) - ln_beta) / a
    f = 1.0
    c_val = 1.0
    d_val = 1.0 - (a + b) * x / (a + 1)
    if abs(d_val) < 1e-30:
        d_val = 1e-30
    d_val = 1.0 / d_val
    h = d_val
    for m_val in range(1, max_iter + 1):
        m2 = 2 * m_val
        # Even step
        numer = m_val * (b - m_val) * x / ((a + m2 - 1) * (a + m2))
        d_val = 1.0 + numer * d_val
        if abs(d_val) < 1e-30:
            d_val = 1e-30
        c_val = 1.0 + numer / c_val
        if abs(c_val) < 1e-30:
            c_val = 1e-30
        d_val = 1.0 / d_val
        h *= d_val * c_val
        # Odd step
        numer = -(a + m_val) * (a + b + m_val) * x / ((a + m2) * (a + m2 + 1))
        d_val = 1.0 + numer * d_val
        if abs(d_val) < 1e-30:
            d_val = 1e-30
        c_val = 1.0 + numer / c_val
        if abs(c_val) < 1e-30:
            c_val = 1e-30
        d_val = 1.0 / d_val
        h *= d_val * c_val
        if abs(d_val * c_val - 1.0) < 1e-15:
            break
    return front * (h - 1.0)


def _chi_squared_cdf(x, k, max_iter=200):
    """Chi-squared CDF via regularized lower incomplete gamma."""
    if x <= 0:
        return 0.0
    # Chi-squared CDF = P(k/2, x/2) where P is regularized lower incomplete gamma
    return _regularized_lower_gamma(k / 2, x / 2)


def _regularized_lower_gamma(s, x_val, max_iter=200):
    """Regularized lower incomplete gamma function P(s, x)."""
    if x_val <= 0:
        return 0.0
    # Series expansion
    ln_gamma_s = math.lgamma(s)
    term = 1.0 / s
    sum_val = term
    for n in range(1, max_iter):
        term *= x_val / (s + n)
        sum_val += term
        if term < 1e-15 * sum_val:
            break
    return sum_val * math.exp(s * math.log(x_val) - x_val - ln_gamma_s)


# ── Result Parsing ────────────────────────────────────────────────────────────────

def to_float(x):
    try:
        return float(str(x).strip().replace("%", "").replace(",", ""))
    except (ValueError, TypeError):
        return None


def parse_results_table(csv_path, method_col="Method"):
    """Parse a CSV results table.

    Returns dict mapping (group_key, method_name) -> dict of metric_name -> value.
    Also returns group_cols detected, and list of all methods.
    """
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    all_cols = list(rows[0].keys()) if rows else []
    # Detect metric columns (numeric) and std columns (_std suffix)
    metric_cols = []
    std_cols = []
    group_cols = []
    for col in all_cols:
        if col == method_col:
            continue
        if col.endswith("_std") or col.endswith("_stdev") or col.endswith("_err"):
            std_cols.append(col)
        elif col == "Dataset" or col.lower() in ("dataset", "setting", "condition", "task", "model_size"):
            group_cols.append(col)
        else:
            metric_cols.append(col)

    # If no explicit group columns found, use Dataset if present
    if not group_cols:
        for col in ["Dataset", "Setting", "Task"]:
            if col in all_cols:
                group_cols = [col]
                break

    # Parse data
    data = {}  # (group_key, method) -> {metric: value}
    for row in rows:
        method = row.get(method_col, "").strip()
        group_key = tuple(row.get(gc, "").strip() for gc in group_cols) if group_cols else ("all",)
        key = (group_key, method)
        data[key] = {}
        for mc in metric_cols:
            val = to_float(row.get(mc))
            if val is not None:
                data[key][mc] = val
    return data, metric_cols, std_cols, group_cols


def _read_seeds_csv(csv_path):
    """Read a multi-seed CSV where each row has seed as a column."""
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


# ── Report Formatting ─────────────────────────────────────────────────────────────

def format_p_value(p, alpha=0.05):
    """Format p-value with significance stars."""
    if p < 0.001:
        stars = "***"
    elif p < 0.01:
        stars = "**"
    elif p < 0.05:
        stars = "*"
    else:
        stars = "n.s."
    return f"{p:.4f} {stars}"


def format_ci(lower, upper, decimals=2):
    return f"[{lower:.{decimals}f}, {upper:.{decimals}f}]"


def format_effect(d, interpretation=True):
    if d is None:
        return "N/A"
    base = f"{d:.3f}"
    if interpretation:
        base += f" ({interpret_effect_size(d)})"
    return base


# ── Main Analysis ─────────────────────────────────────────────────────────────────

def run_statistical_analysis(csv_path, target, metrics, higher_better, lower_better,
                              group_cols, method_col="Method", n_bootstrap=10000,
                              alpha=0.05, baseline_methods=None):
    """Run full statistical analysis and return results as structured dict."""
    data, all_metrics, std_cols, detected_groups = parse_results_table(csv_path, method_col)

    # Use provided group columns or detected ones
    if group_cols:
        effective_groups = group_cols
    else:
        effective_groups = detected_groups if detected_groups else ["Dataset"]

    higher = set(higher_better)
    lower = set(lower_better)

    results = {
        "target": target,
        "metrics": metrics,
        "alpha": alpha,
        "n_bootstrap": n_bootstrap,
        "comparisons": [],
        "effect_sizes": [],
        "multiple_comparison": {},
    }

    p_values_all = []
    p_value_labels = []

    # Collect unique (group, metric) pairs
    for (group_key, method), values in data.items():
        if method != target:
            continue
        for metric in metrics:
            if metric not in values:
                continue
            direction = "higher" if metric in higher else "lower"
            target_value = values[metric]

            # Find baseline values in same group
            baseline_values = {}
            for (gk, m), vals in data.items():
                if gk == group_key and m != target:
                    if baseline_methods and m not in baseline_methods:
                        continue
                    if metric in vals:
                        baseline_values[m] = vals[metric]

            if not baseline_values:
                continue

            for baseline_name, baseline_val in baseline_values.items():
                comp = _analyze_pair(
                    group_key, target, baseline_name, metric, direction,
                    target_value, baseline_val, n_bootstrap, alpha
                )
                results["comparisons"].append(comp)
                if comp.get("cohens_d") is not None or comp.get("hedges_g") is not None:
                    results["effect_sizes"].append({
                        "group": group_key if isinstance(group_key, tuple) else (group_key,),
                        "metric": metric,
                        "target": target,
                        "baseline": baseline_name,
                        "cohens_d": comp.get("cohens_d"),
                        "hedges_g": comp.get("hedges_g"),
                        "interpretation": comp.get("effect_interpretation", "N/A"),
                    })
                p_values_all.append(comp["p_value_approx"])
                p_value_labels.append(f"{group_key}/{metric}/{baseline_name}")

    # Multiple comparison correction
    if len(p_values_all) > 1:
        bonf = bonferroni_correction(p_values_all)
        bh, bh_sig = benjamini_hochberg(p_values_all, alpha)
        results["multiple_comparison"] = {
            "n_tests": len(p_values_all),
            "labels": p_value_labels,
            "raw_p": p_values_all,
            "bonferroni": bonf,
            "benjamini_hochberg": bh,
            "bh_significant": bh_sig,
        }

    return results


def _analyze_pair(group_key, target, baseline, metric, direction,
                   target_val, baseline_val, n_bootstrap, alpha):
    """Analyze a single target-vs-baseline pair."""
    diff = target_val - baseline_val if direction == "higher" else baseline_val - target_val
    rel = (diff / abs(baseline_val) * 100) if baseline_val != 0 else None

    # With only point estimates (single values), we can't do bootstrap or tests.
    # We report what we can and note the limitation.
    return {
        "group": group_key,
        "metric": metric,
        "target": target,
        "baseline": baseline,
        "direction": direction,
        "target_value": target_val,
        "baseline_value": baseline_val,
        "absolute_diff": diff,
        "relative_diff_pct": rel,
        "cohens_d": None,
        "hedges_g": None,
        "effect_interpretation": "N/A (need multiple runs/seeds for effect size)",
        "p_value_approx": 1.0,  # Cannot compute without variance
        "ci_lower": None,
        "ci_upper": None,
        "note": "Point estimates only — run with --std-cols or multi-seed data for full analysis",
    }


def run_analysis_with_seeds(csv_path, target, metrics, higher_better, lower_better,
                             group_cols, seed_col="Seed", method_col="Method",
                             n_bootstrap=10000, alpha=0.05, baseline_methods=None):
    """Run analysis when multi-seed data is available (each seed is a separate row)."""
    rows = _read_seeds_csv(csv_path)

    higher = set(higher_better)
    lower = set(lower_better)

    # Group rows by (group, method)
    if not group_cols:
        group_cols = []
        for col in ["Dataset", "Setting", "Task"]:
            if col in rows[0]:
                group_cols.append(col)

    groups = defaultdict(list)
    for row in rows:
        gk = tuple(row.get(gc, "").strip() for gc in group_cols) if group_cols else ("all",)
        method = row.get(method_col, "").strip()
        groups[(gk, method)].append(row)

    results = {"comparisons": [], "effect_sizes": [], "multiple_comparison": {}}
    p_values_all = []
    p_labels = []

    for (group_key, method), group_rows in groups.items():
        if method != target:
            continue
        target_seeds = {}
        for metric in metrics:
            target_seeds[metric] = [to_float(r.get(metric)) for r in group_rows if to_float(r.get(metric)) is not None]

        for (gk, m), baseline_rows in groups.items():
            if gk != group_key or m == target:
                continue
            if baseline_methods and m not in baseline_methods:
                continue
            baseline_seeds = {}
            for metric in metrics:
                baseline_seeds[metric] = [to_float(r.get(metric)) for r in baseline_rows
                                           if to_float(r.get(metric)) is not None]

            for metric in metrics:
                tv = target_seeds.get(metric, [])
                bv = baseline_seeds.get(metric, [])
                if len(tv) < 2 or len(bv) < 2:
                    continue

                direction = "higher" if metric in higher else "lower"
                target_mean = sum(tv) / len(tv)
                baseline_mean = sum(bv) / len(bv)
                diff = target_mean - baseline_mean if direction == "higher" else baseline_mean - target_mean
                rel = (diff / abs(baseline_mean) * 100) if baseline_mean != 0 else None

                # Bootstrap CI on difference
                ci_lower, ci_upper, diff_est = bootstrap_diff_ci(tv, bv, n_bootstrap, alpha)

                # Effect size
                d = cohens_d(tv, bv, paired=True)
                g = hedges_g(tv, bv, paired=True)

                # Paired t-test
                t_stat, df, p_t = paired_t_test(tv, bv)

                # Wilcoxon
                W_stat, z_w, p_w = wilcoxon_signed_rank(tv, bv)

                sig_test = "paired t" if len(tv) >= 5 else "wilcoxon"
                p_value = p_t if len(tv) >= 5 else p_w

                results["comparisons"].append({
                    "group": group_key,
                    "metric": metric,
                    "target": target,
                    "baseline": m,
                    "direction": direction,
                    "target_mean": round(target_mean, 4),
                    "baseline_mean": round(baseline_mean, 4),
                    "abs_diff": round(diff, 4),
                    "rel_diff_pct": round(rel, 2) if rel is not None else None,
                    "ci_lower": round(ci_lower, 4),
                    "ci_upper": round(ci_upper, 4),
                    "ci_level": f"{(1-alpha)*100:.0f}%",
                    "cohens_d": round(d, 3),
                    "hedges_g": round(g, 3),
                    "effect_interpretation": interpret_effect_size(g),
                    "sig_test": sig_test,
                    "t_stat": round(t_stat, 4),
                    "df": df,
                    "p_value": p_value,
                    "p_formatted": format_p_value(p_value, alpha),
                    "W_stat": round(W_stat, 2),
                    "z_wilcoxon": round(z_w, 4),
                    "n_seeds": len(tv),
                    "power_achieved": round(achieved_power(abs(g), len(tv), alpha), 3),
                })
                results["effect_sizes"].append({
                    "group": group_key,
                    "metric": metric,
                    "target": target,
                    "baseline": m,
                    "cohens_d": round(d, 3),
                    "hedges_g": round(g, 3),
                    "interpretation": interpret_effect_size(g),
                })
                p_values_all.append(p_value)
                p_labels.append(f"{group_key}/{metric}/{m}")

    if len(p_values_all) > 1:
        bonf = bonferroni_correction(p_values_all)
        bh, bh_sig = benjamini_hochberg(p_values_all, alpha)
        results["multiple_comparison"] = {
            "n_tests": len(p_values_all),
            "labels": p_labels,
            "raw_p": p_values_all,
            "bonferroni": bonf,
            "benjamini_hochberg": bh,
            "bh_significant": bh_sig,
        }

    return results


# ── Report Output ─────────────────────────────────────────────────────────────────

def format_report(analysis_results, include_effect_sizes=True, include_multi_correction=True):
    """Format analysis results as a markdown report."""
    lines = [
        "# Statistical Analysis Report",
        "",
        f"**Target method:** `{analysis_results['target']}`",
        f"**Significance level:** α = {analysis_results['alpha']}",
        f"**Bootstrap resamples:** {analysis_results['n_bootstrap']}",
        "",
    ]

    comparisons = analysis_results.get("comparisons", [])
    if not comparisons:
        lines.append("⚠ No comparisons could be computed. Check that the target method and metrics exist in the data.")
        return "\n".join(lines)

    # Summary table
    lines.extend([
        "## Pairwise Comparisons",
        "",
        "| Group | Metric | Target | Baseline | Target Mean | Baseline Mean | Δ | Rel Δ | "
        + (f"{analysis_results['comparisons'][0]['ci_level']} CI | " if comparisons and comparisons[0].get('ci_lower') is not None else "")
        + "Effect Size | p-value | Sig |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ])

    for c in comparisons:
        ci_str = f"{format_ci(c['ci_lower'], c['ci_upper'])} | " if c.get('ci_lower') is not None else ""
        effect = format_effect(c.get('hedges_g') or c.get('cohens_d')) if c.get('hedges_g') is not None or c.get('cohens_d') is not None else (c.get('effect_interpretation', 'N/A'))
        p_str = c.get('p_formatted', 'N/A')
        sig = ""
        if isinstance(c.get('p_value'), (int, float)):
            if c['p_value'] < 0.001:
                sig = "***"
            elif c['p_value'] < 0.01:
                sig = "**"
            elif c['p_value'] < 0.05:
                sig = "*"
        note = f" ⚠ {c['note']}" if c.get('note') else ""
        lines.append(
            f"| {c['group']} | {c['metric']} | {c['target']} | {c['baseline']} | "
            f"{c.get('target_mean', c.get('target_value', 'N/A'))} | "
            f"{c.get('baseline_mean', c.get('baseline_value', 'N/A'))} | "
            f"{c.get('abs_diff', c.get('absolute_diff', 'N/A'))} | "
            f"{c.get('rel_diff_pct', c.get('relative_diff_pct', 'N/A'))}% | "
            f"{ci_str}"
            f"{effect} | "
            f"{p_str} | {sig} |{note}"
        )

    # Effect size summary
    effect_sizes = analysis_results.get("effect_sizes", [])
    if include_effect_sizes and effect_sizes:
        lines.extend([
            "",
            "## Effect Size Summary",
            "",
            "| Group | Metric | Target | Baseline | Cohen's d | Hedges' g | Interpretation |",
            "|---|---:|---|---:|---:|---:|",
        ])
        for es in effect_sizes:
            lines.append(
                f"| {es['group']} | {es['metric']} | {es['target']} | {es['baseline']} | "
                f"{es['cohens_d']} | {es['hedges_g']} | {es['interpretation']} |"
            )

    # Power analysis
    if comparisons and comparisons[0].get('power_achieved') is not None:
        lines.extend([
            "",
            "## Power Analysis",
            "",
            "| Group | Metric | n (seeds) | Effect Size |g| | Achieved Power |",
            "|---|---:|---:|---:|---:|",
        ])
        for c in comparisons:
            if c.get('power_achieved') is not None:
                lines.append(
                    f"| {c['group']} | {c['metric']} | {c.get('n_seeds', 'N/A')} | "
                    f"{abs(c.get('hedges_g', c.get('cohens_d', 0))):.3f} | "
                    f"{c['power_achieved']} |"
                )

    # Multiple comparison correction
    mc = analysis_results.get("multiple_comparison", {})
    if include_multi_correction and mc and mc.get("n_tests", 0) > 1:
        lines.extend([
            "",
            "## Multiple Comparison Correction",
            "",
            f"**Number of tests:** {mc['n_tests']}",
            "",
            "| Test | Raw p | Bonferroni | Benjamini-Hochberg | BH Significant |",
            "|------|-------|------------|-------------------|----------------|",
        ])
        for i in range(mc['n_tests']):
            lines.append(
                f"| {mc['labels'][i]} | {mc['raw_p'][i]:.4f} | "
                f"{mc['bonferroni'][i]:.4f} | {mc['benjamini_hochberg'][i]:.4f} | "
                f"{'✓' if mc['bh_significant'][i] else '—'} |"
            )

    # Interpretation guide
    lines.extend([
        "",
        "## Interpretation Guide",
        "",
        "**Effect size (Cohen's d / Hedges' g):**",
        "- |d| < 0.2: negligible",
        "- 0.2 ≤ |d| < 0.5: small",
        "- 0.5 ≤ |d| < 0.8: medium",
        "- |d| ≥ 0.8: large",
        "",
        "**Significance levels:**",
        f"- * p < {analysis_results['alpha']}",
        f"- ** p < {analysis_results['alpha']/10}",
        f"- *** p < {analysis_results['alpha']/100}",
        "- n.s.: not significant",
        "",
        "**Power:** probability of detecting a true effect at the given sample size. Values ≥ 0.80 are conventionally adequate.",
    ])

    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Statistical significance tests and effect sizes for experiment results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis (point estimates only, no seeds)
  python statistical_tests.py results.csv --target SGA-Ours --metrics R@1 R@5 R@10 \\
      --higher-better R@1 R@5 R@10 --group-cols Dataset

  # Multi-seed analysis (full bootstrap + tests + effect sizes)
  python statistical_tests.py seeds_results.csv --target SGA-Ours --metrics R@1 R@5 \\
      --higher-better R@1 R@5 --seed-col Seed --method-col Method

  # With baseline filter and custom alpha
  python statistical_tests.py results.csv --target Ours --metrics Acc F1 \\
      --higher-better Acc F1 --alpha 0.01 --bootstrap 5000 \\
      --baseline-methods CLIP BLIP SCAN
        """,
    )
    parser.add_argument("csv_file", help="Path to CSV results file")
    parser.add_argument("--target", required=True, help="Name of the proposed/target method")
    parser.add_argument("--metrics", nargs="+", required=True, help="Metric column names")
    parser.add_argument("--higher-better", nargs="*", default=[], help="Metrics where higher is better")
    parser.add_argument("--lower-better", nargs="*", default=[], help="Metrics where lower is better")
    parser.add_argument("--group-cols", nargs="*", default=[], help="Columns defining result groups (e.g., Dataset)")
    parser.add_argument("--method-col", default="Method", help="Column containing method names")
    parser.add_argument("--seed-col", default="Seed", help="Column containing seed/run identifiers (for multi-seed data)")
    parser.add_argument("--baseline-methods", nargs="*", default=[], help="Limit comparisons to these baselines")
    parser.add_argument("--bootstrap", type=int, default=10000, help="Number of bootstrap resamples (default: 10000)")
    parser.add_argument("--alpha", type=float, default=0.05, help="Significance level (default: 0.05)")
    parser.add_argument("--output", "-o", help="Output report file path")
    parser.add_argument("--json", help="Output raw results as JSON")
    parser.add_argument("--no-effect-sizes", action="store_true", help="Omit effect size section")
    parser.add_argument("--no-multi-corr", action="store_true", help="Omit multiple comparison correction")

    args = parser.parse_args()

    higher = set(args.higher_better)
    lower = set(args.lower_better)
    # Metrics not explicitly specified default to higher-is-better
    for m in args.metrics:
        if m not in higher and m not in lower:
            higher.add(m)

    # Detect if multi-seed data
    with open(args.csv_file, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []

    has_seed_col = args.seed_col in fieldnames

    if has_seed_col:
        analysis = run_analysis_with_seeds(
            args.csv_file, args.target, args.metrics, higher, lower,
            args.group_cols, args.seed_col, args.method_col,
            args.bootstrap, args.alpha, set(args.baseline_methods) if args.baseline_methods else None,
        )
    else:
        analysis = run_statistical_analysis(
            args.csv_file, args.target, args.metrics, higher, lower,
            args.group_cols, args.method_col, args.bootstrap, args.alpha,
            set(args.baseline_methods) if args.baseline_methods else None,
        )

    # JSON output
    if args.json:
        import json as _json
        Path(args.json).write_text(_json.dumps(analysis, indent=2, default=str), encoding="utf-8")
        print(f"JSON results saved to {args.json}", file=sys.stderr)

    # Report output
    report = format_report(analysis,
                           include_effect_sizes=not args.no_effect_sizes,
                           include_multi_correction=not args.no_multi_corr)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Report saved to {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
