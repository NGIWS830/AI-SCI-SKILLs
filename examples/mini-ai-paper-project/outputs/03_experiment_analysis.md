# Experiment Analysis

## Tables Analyzed

`experiments/results.csv`

## Main Results

The placeholder method improves over the strongest listed baseline on Accuracy and F1 for both the internal and external evaluation rows.

## Improvement over Baselines

Run:

```bash
python ai-experiment-analyzer/scripts/compute_improvements.py examples/mini-ai-paper-project/experiments/results.csv --target Ours --metrics Acc F1 Params --higher-better Acc F1 --lower-better Params --group-cols Dataset
```

## Claims Supported by Evidence

| Claim | Evidence | Strength | Caveat |
|---|---|---|---|
| The method improves over selected baselines in the evaluated settings. | Accuracy and F1 are higher than the listed baselines on both rows. | Moderate | Only two baselines and no variance are available. |
| The method keeps parameter count close to baseline CNN. | Params is 1.9M vs 1.8M for BaseCNN and 2.1M for CNN-SE. | Weak | Parameter count alone does not prove runtime efficiency. |

## Risks of Overclaiming

- Do not claim state-of-the-art.
- Do not claim broad robustness without more datasets.
- Do not claim statistical significance without repeated runs.
