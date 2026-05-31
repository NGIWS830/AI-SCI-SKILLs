# IEEE TETCI (Transactions on Emerging Topics in Computational Intelligence) LaTeX Template

## About IEEE TETCI

- **Full Name:** IEEE Transactions on Emerging Topics in Computational Intelligence
- **Publisher:** IEEE Computational Intelligence Society (CIS)
- **ISSN:** 2471-285X
- **First Published:** 2017
- **Frequency:** Bimonthly (6 issues/year)
- **Scope:** Emerging and interdisciplinary topics in computational intelligence including neural networks, evolutionary computation, fuzzy systems, and hybrid CI approaches

## Setup

1. Copy `IEEEtran.cls` and `IEEEtran.bst` from `templates/ieee-latex/` (or your TeX distribution) into this directory
2. Compile:
   ```bash
   pdflatex template.tex
   bibtex template
   pdflatex template.tex
   pdflatex template.tex
   ```

## TETCI Scope and Expectations

### What TETCI Publishes
- **Emerging topics** — new CI paradigms, novel combinations of CI techniques, CI applied to new problem domains
- **Interdisciplinary CI** — methods bridging multiple CI subfields (e.g., neuro-evolution, fuzzy deep learning)
- **Theoretically grounded** — papers with convergence proofs, complexity analysis, or formal guarantees
- **Application-driven CI** — CI solutions to pressing real-world problems (healthcare, energy, manufacturing, sustainability)

### What TETCI Does NOT Publish
- Incremental improvements to established CI methods without new insight
- Pure application papers without CI novelty
- Survey/review papers (these go to IEEE CI Magazine or Proceedings of the IEEE)

## TETCI vs Other IEEE CI Journals

| Journal | Full Name | Focus |
|---------|-----------|-------|
| **TETCI** | Trans. Emerging Topics in CI | **Cross-cutting, emerging, interdisciplinary CI** |
| TEVC | Trans. Evolutionary Computation | Evolutionary algorithms, swarm intelligence |
| TNNLS | Trans. Neural Networks and Learning Systems | Neural networks, deep learning, learning theory |
| TFS | Trans. Fuzzy Systems | Fuzzy logic, rough sets, granular computing |
| TCYB | Trans. Cybernetics | Cybernetics, control, human-machine systems |
| TAI | Trans. Artificial Intelligence | Broad AI, not specific to CI |

If your paper fits squarely within a single CI subfield, consider the subfield-specific journal. TETCI is for work that crosses boundaries or addresses emerging CI topics.

## Key Requirements

### Theoretical Rigor
TETCI expects at least some theoretical contribution:
- Convergence analysis for iterative algorithms
- Complexity analysis (time/space) with comparison to baselines
- Formal problem definition and properties
- Generalization bounds or stability analysis for learning methods
- Approximation capability proofs for fuzzy/neural systems

### Experimental Rigor
- **Statistical validation**: Always use statistical tests (Wilcoxon, Friedman + post-hoc) with appropriate corrections for multiple comparisons
- **Reproducibility**: Report all parameter settings, random seeds, hardware, and software versions
- **Standard benchmarks**: Use CEC competition benchmarks for evolutionary methods; standard ML benchmarks for learning methods
- **Ablation**: Demonstrate the contribution of EACH proposed component
- **Real-world validation**: At least one real-world application if possible

### CI-Specific Notations
| Notation | Meaning |
|----------|---------|
| $\mathbf{x}$ | Decision vector (bold lowercase) |
| $\mathcal{X}$ | Decision/search space |
| $f(\mathbf{x})$ | Objective function |
| $\mathcal{P}$ | Population |
| $N$ | Population size |
| $g$ | Generation counter |
| $p_c, p_m$ | Crossover/mutation probabilities |
| $\mu(\mathbf{x})$ | Membership function |
| $\mathcal{R}$ | Rule base |

## Documentclass Options

During writing:
```latex
\documentclass[journal,onecolumn,draftcls]{IEEEtran}
```

Final submission:
```latex
\documentclass[journal]{IEEEtran}
```
