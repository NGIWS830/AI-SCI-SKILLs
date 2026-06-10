# Related Work Patterns

## Three Organization Templates

### Template A: Taxonomy-by-Task (Most Common)
Organize by what problem each line of work addresses:
- **Theme 1**: [Task-Specific Methods]. Methods that address the same task.
- **Theme 2**: [Method-Family Methods]. Methods using similar technical approaches, even if for different tasks.
- **Theme 3**: [Gap-Relevant Methods]. Work that is closest to your specific gap.

Best when: Your paper addresses a well-defined task with clear sub-communities.

### Template B: Taxonomy-by-Technique
Organize by the technical approach:
- **Theme 1**: [Approach A]. One family of technical solutions (e.g., CNN-based, attention-based).
- **Theme 2**: [Approach B]. Another family (e.g., GNN-based, contrastive learning).
- **Theme 3**: [Hybrid / Related]. Methods combining approaches or from adjacent fields.

Best when: Your method synthesizes ideas from multiple technical communities.

### Template C: Gap-Driven
Organize around the specific problem you solve:
- **Theme 1**: [Aspect 1 of the Gap]. Work that partially addresses one dimension.
- **Theme 2**: [Aspect 2 of the Gap]. Work that addresses another dimension.
- **Theme 3**: [Closest Competitors]. Directly comparable work and why it falls short.

Best when: Your paper's main contribution is clearly identifying and filling a specific gap.

---

## Transition Phrase Library for Themed Related Work

**Introducing a new theme:**
- "A substantial body of work has addressed [theme]."
- "Another line of research focuses on [theme]."
- "Closely related to this work are methods that [theme]."
- "The proposed method also relates to research on [theme]."

**Describing representative work within a theme:**
- "For instance, [Author] et al. [X] proposed [method] which [mechanism]."
- "A representative approach is [Method] [X], where [description]."
- "Building on [prior_work], [Author] et al. [X] introduced [improvement]."

**Distinguishing the proposed method from a theme:**
- "While effective for [scenario], these methods [limitation]. In contrast, the proposed approach [difference]."
- "Unlike [method_family] approaches that rely on [assumption], the proposed method [alternative]."
- "A key difference from [prior_work] is that the proposed method [distinction], which enables [benefit]."
- "The proposed method shares [common_element] with [theme], but differs in that it [key_difference]."

---

## Comparison Sentence Patterns

**Direct comparison with specific work:**
- "Unlike [Method] [X] which employs [mechanism_A], the proposed method uses [mechanism_B], avoiding [limitation_of_A]."
- "While [Method] [X] achieves [result] through [approach], [approach] has the limitation of [limitation]. The proposed method instead [alternative]."
- "[Method] [X] and this work both [shared_goal], but while [X] [method_A], the proposed method [method_B]."

**Positioning among method families:**
- "Methods in [family_A] typically [characteristic_A], whereas methods in [family_B] tend to [characteristic_B]. The proposed approach combines [strength_of_A] with [strength_of_B]."
- "Unlike both [family_A] (which [limitation_A]) and [family_B] (which [limitation_B]), the proposed method [advantage]."

---

## Gap Articulation Templates

Respectfully identify limitations in prior work:

- "While [Method] [X] showed promising results on [dataset], its reliance on [assumption] limits applicability to [scenario] where [condition]."
- "Existing methods implicitly assume [assumption], which holds for [scenario_A] but fails in [scenario_B]."
- "A common limitation across [method_family] approaches is [limitation], which manifests as [observable_symptom]."
- "Although [Method] [X] addresses [aspect_A] effectively, it does not consider [aspect_B], which is found to be critical for [reason]."

**Anti-patterns:**
- "The work of [Author] is fundamentally flawed." → Too aggressive. Describe the limitation, not the flaw.
- "No prior work has addressed [X]." → Hard to verify. Use "Limited attention has been paid to [X]" or "[X] has received relatively little attention."

---

## How to Handle Relatedness

### Close Competitors
Give them fair treatment. Acknowledge their strengths before noting limitations. This builds credibility with reviewers (who may be the authors of those papers).
- "The closest work to ours is [Method] [X], which [mechanism]. [X] demonstrated that [finding]. However, [X] relies on [limitation]. Our method addresses this by [alternative]."

### Orthogonal Work
Briefly acknowledge and explain why it's not directly comparable.
- "Concurrent work by [Author] et al. [X] explores [related_direction] but focuses on [different_aspect]. Our work is complementary in that [relationship]."

### Prior Self-Citations
Be transparent but don't over-cite yourself.
- "This work extends a preliminary study [X], where [prior_finding] was established. The present work differs in [key_advancement]."

---

## Related Work Quality Self-Check

1. **Theme count**: 2-4 themes. Fewer than 2 = under-organized. More than 4 = over-fragmented.
2. **Papers per theme**: 2-4 papers per theme. Cover the representative ones, not everything.
3. **Comparison presence**: Does each theme paragraph end with a comparison to the proposed method? ("In contrast, the proposed method...", "Unlike these approaches, the proposed method...")
4. **Chronology avoidance**: Are papers organized by idea, not by year?
5. **Citation accuracy**: Are all citations verified? Any `[CITATION NEEDED]` remaining?
6. **Fairness**: Would the authors of the cited papers agree with your characterization of their work?

Write by themes:
- Task-specific methods
- Method-family approaches
- Limitations motivating this work

Do not write a chronological paper list. Do not cite unverified papers.
