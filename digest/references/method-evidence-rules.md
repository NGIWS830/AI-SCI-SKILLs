# Method Evidence Rules

## Evidence Levels

- **High**: Explicitly found in code, equations, diagrams, or author notes with unambiguous detail.
  - Example: A custom `DirectionalConsistencyLoss(nn.Module)` class found in `losses/dc_loss.py` with forward() computing `L_dc = L_direction + λ * L_continuity`.
- **Medium**: Strongly implied by file names, config keys, or repeated comments, but not fully specified.
  - Example: A config key `use_boundary_refinement: true` with a file `models/refinement.py` that exists but lacks documentation.
- **Low**: Plausible interpretation that requires author confirmation.
  - Example: A module named `SpatialModule` with convolutional layers — inference that it processes spatial information, but its exact purpose is unclear.

## Detailed Evidence Level Examples

### High Evidence Scenarios
- Complete source code for the module with clear variable names and comments.
- Architecture diagrams with labeled components matching code modules.
- Author notes explicitly stating the design rationale.
- Hyperparameters documented with explanation of how they were chosen.
- Loss function with full mathematical formulation in code comments or documentation.

### Medium Evidence Scenarios
- Module file exists but uses generic variable names (`x`, `y`, `out`) with no comments.
- Config file references a module but the module file imports an external library component.
- README mentions a technique but the code only partially implements it.
- Training script has multi-stage logic but stages aren't documented.

### Low Evidence Scenarios
- A paper draft (not yet verified) describes a module not found in code.
- The code has a module with a suggestive name but no clear role in the data flow.
- Results mention a "variant" without specifying what changed.
- The author's notes say "we also tried X" without details.

## Claim Wording by Evidence Level

- High: "The method includes [module], which [mechanism]."
- Medium: "The materials suggest that [module] performs [function], likely via [mechanism]."
- Low: "A possible interpretation is that [module] contributes to [capability]. AUTHOR_INPUT_NEEDED"

## Contribution Type Taxonomy

| Type | Description | Evidence Required |
|------|-------------|-------------------|
| **Architectural** | New network design, module, or component | Code for the module + ablation showing its contribution |
| **Algorithmic** | New training procedure, optimization, or inference algorithm | Code + convergence/efficiency analysis |
| **Training Strategy** | New loss function, regularization, data augmentation | Code for the loss + ablation of the loss term |
| **Data/Methodology** | New benchmark, dataset, evaluation protocol | Dataset description + baseline evaluation |
| **Analysis** | New understanding or insight about existing methods | Systematic experiments across methods + clear findings |
| **Application** | Novel application of existing techniques to a new domain | Domain-specific evaluation + comparison to domain baselines |

## Evidence-to-Claim Mapping Patterns

| What the Evidence Shows | Maximum Claim Allowed |
|------------------------|----------------------|
| Code + ablation on 3 datasets | "We propose [Method], which improves [metric] by [X] on [datasets]." |
| Code only, no experiments | "We present [Method], a [description]. Experimental validation is ongoing." |
| Author notes describe method, no code | "The authors describe a method that [mechanism]. AUTHOR_INPUT_NEEDED for implementation details." |
| Results table from author, no code | "Reported results indicate [finding]. Code not provided for reproduction verification." |
| Code + results + multiple ablation variants | "Ablation confirms [component] contributes [X] points to [metric] (Table Y)." |

## Never Invent

- Module purpose without evidence
- Mathematical formulas not present in materials
- Loss terms not in the code or notes
- Dataset splits not specified
- Hyperparameters not documented
- Training tricks not mentioned
- Baseline names not listed
- Performance claims without numbers

## Contribution Candidates

Contribution candidates must be framed as candidates until supported by literature and experiments. Use:

```text
Candidate contribution: ...
Evidence: ...
Needs validation: novelty / experiment support / citation support
```

If a candidate contribution cannot be validated by the end of Stage 3, either:
- Demote it to "design choice" (still worth mentioning but not a main contribution)
- Mark it as `AUTHOR_INPUT_NEEDED` and ask the author to provide supporting evidence
- Remove it if the author confirms it is not a contribution
