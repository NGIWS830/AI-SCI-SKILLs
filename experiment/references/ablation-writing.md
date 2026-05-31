# Ablation Writing

## Purpose

Ablation studies should support component-level claims, not merely list variants.

## Pattern

```text
Removing [component] decreases [metric] from [A] to [B], indicating that [component] contributes to [specific capability].
```

## Cautions

- Do not claim a module is essential if improvement is tiny or inconsistent.
- Do not claim generality from a single dataset unless framed carefully.
- If variants change multiple factors at once, avoid attributing the effect to one factor.
