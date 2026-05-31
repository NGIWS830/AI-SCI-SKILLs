# Method Section Patterns

Default structure follows `reference-paper-structure.md`:

```markdown
## III Proposed Method
### III-A Overview
### III-B [User's Core Module 1]
### III-C [User's Core Module 2]
### III-D [User's Core Module 3 / Third Innovation]
```

Use the reference paper's flow, not its module names. Replace every method subsection with the user's actual architecture, algorithm, or innovation component. Reserve `III-D` for the third innovation unless the loss/objective is itself the third innovation.

Recommended content order:

1. Define inputs, outputs, symbols, and task setting.
2. Present the overall framework and data flow.
3. Explain each core module with evidence from code, diagrams, notes, or author input.
4. Add `III-E Training Objective` only when objective/loss/training strategy is supported and important enough to stand alone.
5. Describe inference and complexity only when supported.

All formulas and symbols must be consistent and evidence-grounded.
