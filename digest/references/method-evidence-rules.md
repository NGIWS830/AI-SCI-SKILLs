# Method Evidence Rules

## Evidence levels

- **High**: explicitly found in code, equations, diagrams, or author notes.
- **Medium**: strongly implied by file names, config, or repeated comments but not fully specified.
- **Low**: plausible interpretation that requires author confirmation.

## Claim wording by evidence level

- High: “the method includes...”
- Medium: “the materials suggest that...”
- Low: “a possible interpretation is... AUTHOR_INPUT_NEEDED”

## Never invent

- Module purpose
- Mathematical formulas
- Loss terms
- Dataset split
- Hyperparameters
- Training tricks
- Baselines
- Performance claims

## Contribution candidates

Contribution candidates must be framed as candidates until supported by literature and experiments. Use:

```text
Candidate contribution: ...
Evidence: ...
Needs validation: novelty / experiment support / citation support
```
