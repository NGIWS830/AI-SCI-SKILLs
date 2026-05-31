# Discussion Patterns

## Discussion Structure Templates

### Interpretation-First
```
[Brief restatement of main finding]
[Why the method works — mechanistic interpretation]
[When it works best and why]
[When it struggles and why]
[Broader implications]
```
Best for: Papers where understanding the mechanism is the main contribution.

### Limitation-First (if limitations are significant)
```
[Honest acknowledgment of limitations]
[Despite limitations, what we learned]
[Why the method still matters]
[How future work can address limitations]
```
Best for: Papers that are a first step in a new direction. Honesty builds credibility.

### Synthesis-First
```
[How our findings fit into the broader literature]
[What we now understand that we didn't before]
[How this changes the research landscape]
[Open questions for the community]
```
Best for: Papers that resolve a debate or establish a new baseline understanding.

---

## Interpretation Patterns

### Why the Method Works

> "The strong performance of [Method] can be attributed to [key_design_choice]. Unlike prior approaches that [previous_assumption], [Method] [different_approach], which enables [capability]. This interpretation is supported by the ablation study (Table [X]), which shows that removing [component] degrades [metric] by [delta]."

> "We hypothesize that [Method]'s effectiveness stems from [mechanism_hypothesis]. Evidence for this comes from [qualitative_observation] (Fig. [X]), where [Method] exhibits [behavior] while [baseline] does not."

### When It Works Best

> "[Method] performs particularly well on [scenario_type] (+[delta] over [baseline]), suggesting that [design_choice] is especially beneficial when [condition]. Conversely, gains are more modest on [other_scenario] (+[smaller_delta]), likely because [reason]."

### Failure Cases and Limitations

> "We identify two failure modes. First, [Method] occasionally [failure_1] when [condition] (see Fig. [X], row [N]). We attribute this to [root_cause]. Second, performance degrades on [failure_2_scenario], likely due to [reason]. Addressing these failure cases is a priority for future work."

> "A limitation of our evaluation is [missing_analysis]. While our results on [evaluated_datasets] are promising, testing on [additional_scenarios] would strengthen the claims of [generalization/robustness]."

### Generalization Discussion

> "To assess generalization, we evaluated [Method] on [out_of_domain_dataset] without fine-tuning. [Method] achieves [X.X] vs. [baseline]'s [Y.Y], suggesting that [capability] transfers across domains. However, the gap to in-domain performance ([delta]) indicates that domain shift remains a challenge."

> "While [Method] was developed for [task_A], its core mechanism — [brief_description] — may generalize to related tasks. Preliminary experiments on [task_B] (Appendix [X]) show [result], suggesting broader applicability."

### Practical Implications

> "From a practical standpoint, [Method]'s [practical_advantage] (e.g., [N]× fewer parameters, [M]× faster inference) makes it suitable for [deployment_scenario]. The trade-off between [advantage] and [disadvantage] should be considered when [context]."

---

## Discussion Quality Self-Check

1. **Interpretation vs. repetition**: Does the discussion interpret results (WHY) rather than restate them (WHAT)?
2. **Limitation honesty**: Are the main limitations acknowledged? A paper with no limitations is suspicious.
3. **Failure cases**: Are specific failure cases shown and explained?
4. **Generalization**: If claiming generalization, is it backed by cross-domain experiments?
5. **Practical relevance**: Would a practitioner know when to use (and not use) this method after reading the discussion?
6. **No over-interpretation**: Are interpretations clearly labeled as hypotheses when evidence is suggestive rather than conclusive?

Discuss:
- Why the method works.
- When it works best.
- Failure cases or limitations.
- Generalization and practical implications, only if supported.

Avoid repeating results without interpretation.
