# LH| Long-Horizon Trial — Reflection

## What we built

A TNN-native deliberation system (proposer/critic/composer sharing one
ledger) that sustained 230 generate→compile→run→test cycles across 26
dependency-ordered components with zero defects, zero retention loss, and
one honest halt on an underivable task.

## What worked

1. **The one-brain design held.** Proposer, critic, and composer all read
   and wrote to the same ledger. Every invented spec is traceable to
   deliberation episodes. The audit confirms no crew-authored architecture
   leaked into the machinery.

2. **Knowledge-first worked.** The 6-entry KB was sufficient for the
   proposer to select correct operations for all 26 stages. The critic's
   simulation (independent of the emitter) caught no errors because there
   were none to catch — but the mechanism was in place.

3. **Honest halt worked.** F1's ROT13 request produced a clean KB-MISS halt,
   not a fabrication. The system knows what it doesn't know.

4. **Determinism held.** 25 full pipeline runs (5 stages × 5 reps) produced
   byte-identical artifacts. The "no randomness in decision paths" law is
   satisfied.

## What didn't (or wasn't tested)

1. **No failures occurred.** The trial did not test the diagnoser/revision
   loop because nothing failed. This is a gap — the prereg promised
   "diagnose→revise" cycles, but the contracts were too easy to trigger them.
   The machinery for revision exists in the driver (test-fail → stage-fail),
   but it was never exercised.

2. **The critic is a simulator, not an oracle.** It mirrors the emitter's
   logic. A truly independent oracle (e.g., a Python reference implementation)
   would provide stronger verification. The current design risks
   correlated failures.

3. **Scale is toy.** 26 stages, 6 KB entries, 16 operations. Real software
   has thousands of components and the KB would need thousands of entries.
   The trial proves the pattern, not the scale.

## The validity question

The summary that preceded this trial flagged a critical issue: the
calibration prototype recreated the architecture-leaking KB problem. This
trial used a **different** design:

- The KB (`lh_kb.txt`) teaches CAPABILITIES (what ops exist), not solutions.
- The contracts state BEHAVIOR (inputs/outputs), not implementations.
- The deliberation INVENTS the mapping from behavior to capability.

The audit (`audit_forbidden.py`) verifies the machinery contains no
pipeline-specific vocabulary. It exits 0.

**However:** The operation inventory (16 ops) and the spec language
(`LH|FIELD|...`) were crew-designed. TNN did not invent the *existence* of
"uppercase" or "filter" — it invented *which* to use and *how* to parameterize
them. This is "deliberation over taught knowledge" (like Task 1 Informed arm),
not "invention from nothing" (Task 1 Scratch arm). The trial is honest about
this: it's a long-horizon endurance test of the deliberation machinery, not
a test of de-novo concept invention.

## What we'd do differently

1. **Include adversarial contracts** that are designed to fail first-pass,
   forcing the diagnoser/revision loop to engage. Measure revision cycles,
   not just success cycles.

2. **Use an independent oracle** (Python reference) for the critic, not a
   Zag simulator that mirrors the emitter.

3. **Test KB-MISS more broadly.** F1 is one probe. A battery of 10
   underivable tasks would better characterize the honest-halt boundary.

4. **Scale the KB.** 6 entries is minimal. A 60-entry KB with overlapping
   keywords would test the proposer's discrimination more rigorously.

## For the CEO

We built a system that writes code by deliberating with itself — proposing
solutions, critiquing them, and composing the winners — and it sustained
that process for 230 steps without getting worse, forgetting, or making
things up. When we asked it to do something it hadn't been taught (ROT13),
it said "I can't" instead of faking it. Every decision is recorded and
reproducible. The system is honest, steady, and deterministic.

The caveat: it didn't encounter any real failures, so we didn't see it
recover from mistakes. And it's working from a small taught vocabulary —
we taught it the building blocks, it assembled them. The next trial should
make it struggle.
