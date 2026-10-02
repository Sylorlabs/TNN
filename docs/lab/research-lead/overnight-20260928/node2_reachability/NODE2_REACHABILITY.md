# Node 2 Reachability: UNREACHABLE

**Verdict: NODE2-REACHABILITY-COMPLETE with verdict UNREACHABLE.**

## Method

Implemented H3-lite Node 2 (guide template policy) on an unfrozen variant per frozen prereg `9084a7760` Section 3, minimal. Changes to frozen TNN-2 base:
1. `n2_pol_get`: finds/creates policy node (tag 40, subtype 2) with fields 20 (default action, init 30), 24 (default content, init -999), 28 (resolution count), 32 (miss count), 8/12/16 (3-slot action history).
2. Modified `miss_inquire`: reads action/content from policy fields 20/24 instead of literals 30/-999. Increments miss count.
3. New `resolve_uncertainty`: called from `ev_observe` no-fact branch. Finds open uncertainty (tag 30) for (s,r), supersedes it and its guide via type-3 self-edges, increments resolution count, records guide's action (field 20) in history, applies majority-of-three rule: if last 3 recorded actions are all A and A != current default, set default = A.
4. New `main`: probe driver.

3/3 byte-identical runs (SHA-256 `3c80de941932a8b74d5e1b25044d5d26a954d6f890a72f22b00fd51472239145`).

## Results

```
Phase 1: 3 misses -> def=30 res=0 miss=3 hist=[-999,-999,-999]
Phase 2: 3 observations ->
  def=30 res=1 miss=3 hist=[30,-999,-999]
  def=30 res=2 miss=3 hist=[30,30,-999]
  def=30 res=3 miss=3 hist=[30,30,30]
Phase 3: 3 more cycles -> def=30 res=6 miss=6 hist=[30,30,30]
Final: default=30. RESULT: UNREACHABLE.
```

The rule never fired. History filled with 30s (the guide actions), but 30 == default, so the `A != default` condition was always false.

## Logical Proof of Unreachability

The empirical result reflects a logical deadlock in the prereg's literal text:

1. Guides are created with action = current default (production read path: `miss_inquire` reads field 20).
2. `resolve_uncertainty` records the guide's action in history.
3. Therefore, every recorded action equals the default at guide-creation time.
4. The rule requires three recorded actions A where A != current default D.
5. For A != D with A from guides: guides with action A exist, so default was A at their creation. Current default is D != A, so default changed from A to D.
6. The ONLY production write path to field 20 (default) is the majority-of-three rule itself.
7. Therefore, the default can only change via the rule firing. But the rule firing requires the default to have already changed. Circular dependency.
8. By induction: the first firing would require a prior firing. Impossible.

**The majority-of-three update rule is unreachable from any stable default under the prereg's literal text.**

## Prereg Bug (Documented, Not Amended)

Frozen prereg `9084a7760` Section 3, Node 2, Production write path contains a bug:

> "If the most recent three resolutions all followed action A where A differs from the current default, set field 20 = A"

This condition cannot become true because:
- The "resolving action" is defined (implicitly) as the guide's action.
- Guides are created with the current default's action (explicit in Production read path).
- No other mechanism creates guides with non-default actions.
- The default only changes via this rule.

The prereg does not specify an alternative source for "resolving action" (e.g., a world-revealed action via a new `ev_observe` parameter, or an `ev_act`-returned action). The discrimination test mentions "the world reveals answers only after a different action" but `ev_observe(W,s,r,o)` has no action channel, and the write path does not reference `ev_act` output.

**This is a FROZEN PREREG BUG.** It does not invalidate the H3-lite diagnostic (Node 1 and Node 3 are unaffected), but Node 2 cannot pass K-H3 condition (c) -- the write path exists in source but is unreachable in any evaluation. Per the prereg's own Section 4: "A production write path exists but is unreachable in the sealed evaluation (e.g., gated behind a test-only flag). Write-path theater."

Node 2 as specified is write-path theater.

## Implications

1. **K-H3 audit:** Node 2 fails condition (c) before any sealed evaluation runs. The node should not proceed to capability interpretation.
2. **H3-lite scope:** The experiment remains valid for Nodes 1 and 3. Node 2 needs a prereg amendment (transparent, per Micah's rules) specifying a reachable action source.
3. **Possible fixes (for amendment, not implemented):**
   - (a) Add action parameter to `ev_observe` (world reveals action). Requires harness change.
   - (b) Record `ev_act` return value as "resolving action" (learner's taken action). Requires linking act to observe.
   - (c) Allow guides to be created with non-default actions via a separate mechanism. Unclear what this would be.
   - Each has treadmill/design implications. Not recommended without Micah's input.

## Constraints Honored

- UNFROZEN variant only. Node 2 only. Frozen prereg `9084a7760` read-only, not modified.
- Frozen TNN-2 source SHA-256 `a29972ca...` verified before/after. Build `f4de7ff46` untouched.
- Pure Zag, safebin, `which python3 python` empty. Zero forbidden executables.
- Zero em dashes byte-verified. Paper untouched. Nothing pushed. No sealed worlds.
- 3/3 byte-identical runs.

## Standing Metric

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 1 (Node 2 update rule unreachable by researcher specification error)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: 0
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: 0 (variant only, ~80 lines Node 2 implementation)
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0
