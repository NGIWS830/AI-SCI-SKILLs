# Improvement Summary

- Source: `examples/mini-ai-paper-project/experiments/results.csv`
- Target method: `Ours`
- Group columns: `Dataset`

| Group | Metric | Direction | Target | Strongest Baseline | Baseline | Absolute Improvement | Relative Improvement |
|---|---:|---|---:|---|---:|---:|---:|
| Dataset=External | Acc | higher | 85.8 | CNN-SE | 85 | 0.8 | 0.94% |
| Dataset=External | F1 | higher | 83.9 | CNN-SE | 83.1 | 0.8 | 0.96% |
| Dataset=External | Params | lower | 1.9 | BaseCNN | 1.8 | -0.1 | -5.56% |
| Dataset=Internal | Acc | higher | 90.4 | CNN-SE | 89.1 | 1.3 | 1.46% |
| Dataset=Internal | F1 | higher | 88.6 | CNN-SE | 87.4 | 1.2 | 1.37% |
| Dataset=Internal | Params | lower | 1.9 | BaseCNN | 1.8 | -0.1 | -5.56% |