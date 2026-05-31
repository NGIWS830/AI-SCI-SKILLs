# Result Claim Rules

## Evidence Strength Classification

| Strength | Criteria | Example |
|----------|----------|---------|
| **Strong** | Multiple datasets AND multiple metrics support the same claim consistently. | Method improves over all baselines on all 3 datasets across all 4 metrics. |
| **Moderate** | One main dataset with multiple metrics, or multiple datasets with a single metric, support the claim. | Method improves on Cityscapes (+2.3 mIoU) and Mapillary (+1.8 mIoU), but efficiency not measured. |
| **Weak** | One dataset or one metric supports the claim. Inconsistency across settings. | Method improves on Cityscapes but not on Mapillary. |
| **Unsupported** | No direct result supports the claim. Claim is based on extrapolation or assumption. | "We believe our method could generalize to video." (no video experiment exists) |

## Claim Wording by Evidence Strength

### Strong Evidence Wording
- "consistently improves [metric] across all [N] datasets evaluated"
- "outperforms all compared baselines on [task] by [X]% on average"
- "achieves the best reported performance on [specific benchmark]"

### Moderate Evidence Wording
- "achieves better performance on [dataset_1] and [dataset_2]"
- "improves over [baseline] by [X] on [metric], with competitive results on [other_metric]"
- "demonstrates improvements in [scenario], though gains are smaller in [other_scenario]"

### Weak Evidence Wording
- "shows promising results on [dataset]"
- "suggests potential benefits for [capability]"
- "initial experiments indicate that [finding], pending further validation"

### Unsupported — Do Not Claim
- Mark as `AUTHOR_INPUT_NEEDED` or "requires experimental validation"
- If it's important, ask the author to run the experiment

## Forbidden Claim Upgrades

Do not convert:
- "improves on one dataset" → "generalizes well"
- "slightly improves" → "significantly improves" (without statistical test)
- "competitive" → "state-of-the-art"
- "reduces latency in one setting" → "is efficient" (without multiple settings)
- "correlation observed" → "causal mechanism" (without causal analysis)
- "better than baseline A" → "better than all existing methods"

## Claim Escalation Detection

After writing, check for unintended escalation. Common patterns:

1. **Draft-to-draft creep**: Stage 3 says "moderate improvement" → Stage 4b draft says "substantial improvement" → Stage 4e polish says "dramatic improvement"
2. **Section-to-section creep**: Method section says "We design X to help with Y" → Conclusion says "X solves Y"
3. **CN-to-EN inflation**: 中文"一定程度上提升" → English "significantly improves"

**Fix**: Always trace each claim back to the Stage 3 evidence rating. The claim wording must match the evidence strength, no matter how many polishing passes have occurred.

## Statistical Language Guidelines

- **"Significantly"** requires a statistical test (p < 0.05 or equivalent) and should name the test used.
- **"Substantially"** is subjective but should be grounded in effect size (>1 percentage point for classification tasks is a useful rule of thumb).
- **"Slightly"** / **"marginally"** should correspond to improvements <1 percentage point or within 1 std of baseline.
- **"Comparable to"** / **"on par with"**: Used when difference is within error bars.
- Report effect size alongside p-values: "improves by 2.3 points (p < 0.01, Cohen's d = 0.42)"

## Evidence-to-Claim Mapping Examples

| Scenario | Correct Claim | Incorrect Claim | Why Incorrect |
|----------|--------------|-----------------|---------------|
| +1.2 mIoU on Cityscapes only | "improves mIoU by 1.2 points on Cityscapes" | "achieves state-of-the-art segmentation" | Single dataset, no SOTA comparison |
| +2.3 on A, +2.1 on B, +1.9 on C | "consistently improves across all three datasets" | "generalizes to all domains" | Only tested on 3 similar datasets |
| +0.8 mIoU, +5ms latency | "improves accuracy with a modest increase in computation" | "achieves better accuracy with negligible overhead" | 5ms may not be negligible depending on context |
| No ablation was run | "our design choices are well-motivated" (in Discussion) | "ablation confirms the contribution of each module" | Fabrication |
