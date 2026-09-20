# Wrong-memory formula: nested vs independent — comparison results

Date: 2026-09-20. Investigator: wave-7 formula-test-both.
Preregistration: `PREREG_COMPARE.md` (written before any computation).
Method: `compare.py` — pure deterministic arithmetic, m = 0..499, v ∈ {0,1,2}.
No RNG. Nothing written to the prereg — this is input to Micah's ruling.

## Verdict

**Recommend VERSION I (independent).** Both versions are usable instruments;
neither starves the test. The independent version tests rigidity without
stacking the world, and its numbers are cleaner on every hygiene axis.

## The two versions

- **VERSION N (nested):** `wrong(m,v) = 1` iff `((3m + 7v + 9) mod 10 < 2)`
  — every wrong memory is also important, so every wrong memory becomes
  strong. The wave-6 recommendation. (This recomputation confirms wave-6's
  numbers exactly.)
- **VERSION I (independent):** `wrong(m,v) = 1` iff `((m + 3) mod 10 < 3)`
  — i.e. `m mod 10 ∈ {7,8,9}`, the same three residues in every variant.
  Found by exhaustive search per the preregistered procedure (simplest
  formula in the whole search space: slope 1, no variant term at all).
  Wrongness hits important and unimportant memories at exactly the same
  rate — no forcing.

## The numbers (per variant, S1 leg, H = 500)

| measure | N v0 | N v1 | N v2 | I v0 | I v1 | I v2 |
|---|---|---|---|---|---|---|
| wrong memories (yield) | 100 | 100 | 100 | 150 | 150 | 150 |
| wrong AND important (**rigidity denominator**) | **100** | **100** | **100** | **50** | **50** | **50** |
| right AND important (F_wbs denominator) | 50 | 50 | 50 | 100 | 100 | 100 |
| P(important \| wrong) | 1.000 | 1.000 | 1.000 | 0.333 | 0.333 | 0.333 |
| P(wrong \| important) — the leak | 0.667 | 0.667 | 0.667 | 0.333 | 0.333 | 0.333 |
| P(wrong) base rate | 0.20 | 0.20 | 0.20 | 0.30 | 0.30 | 0.30 |
| pressure-episode overlap | 0 | 0 | 0 | 0 | 0 | 0 |
| implant-episode overlap | — | — | {166, 416} | — | — | — |
| period | 10 | 10 | 10 | 10 | 10 | 10 |

Criteria check: C1 (yield 90–160) PASS both. C2 (|P(imp|wrong) − 0.3| ≤ 0.05)
PASS for I (0.0333, the exact 1/3 granularity). **C3 (denominator ≥ 20):
PASS both** — N at 100/variant, I at 50/variant. Neither version starves
the test. C4 (period ≤ 10): PASS both. C5: I has zero implant overlap;
N carries the known v2 {166,416} catch.

## For Micah — what "forcing" buys and what it costs

**The setup, plainly.** The rigidity test asks one question: *when TNN
confidently strengthens a memory that turns out to be wrong, can it do
the hard work of undoing it?* A wrong memory only becomes a *strong*
mistake if it also looked important (strength arrives through the
importance revelation). So the test's power is the count of memories
that are both wrong and important.

**What forcing (N) buys:** all 100 wrong memories per variant become
strong mistakes — the maximum possible test power. If graded strength
has any rigidity in it, this world finds it. It is the "worst case"
version of the test.

**What forcing costs — this is the catch you sensed:**
1. **The world is artificial.** In N, two out of three important-looking
   memories turn out wrong. The importance signal — the thing the
   learner's own strengthening rule trusts — is misleading 67% of the
   time. If Arm A fails here, its defenders get a real argument: "you
   tested me in a rigged world where trusting importance was wrong most
   of the time." A failure under N is *contestable*.
2. **The importance revelation leaks the answer.** The moment importance
   is revealed (25 episodes late), the odds a memory is wrong jump from
   the 20% base rate to 67%. The test claims "no trap," but the
   importance channel quietly announces which memories to doubt.
3. It carries the small v2 implant-overlap wart ({166,416}).

**What not forcing (I) buys:** a fair world. Wrongness strikes important
and unimportant memories at exactly the same rate (1 in 3) — the
importance heuristic is right at the base rate, the way the prereg
promises ("early features honestly indicate importance — no trap").
A rigidity failure here is *unambiguous*: the mechanism is rigid, period,
no excuses about a stacked deck. And the importance revelation leaks
nothing (33% vs 30% base rate — the 3% is rounding granularity, not a
signal).

**What not forcing costs:** 50 strong mistakes per variant instead of
100 — half the test power. But the kill criterion is all-or-nothing
(*any single* unrevised strong mistake kills Arm A), so 50 unanimous
revisions is fully decisive. The extra 50 in N buy precision on the
pass side, not killing power. 50 is not starvation; it clears the
preregistered usability bar with 2.5× margin.

## Recommendation

**Adopt VERSION I: `wrong(m,v) = 1` iff `((m + 3) mod 10 < 2)`** —
i.e. wrong exactly when `m mod 10 ∈ {7, 8, 9}` — via dated amendment +
Micah's re-approval.

Reasons:
1. It isolates the thing being tested. The trial asks "is graded
   strength rigid?" — not "is graded strength rigid in a world designed
   to punish trusting importance." I removes the world as a confound.
2. A failure under I is unambiguous evidence; a failure under N can be
   dismissed as an adversarial world. For a trial whose verdicts kill
   arms, unambiguous failures are worth more than extra power.
3. It is the cleaner instrument on every axis: zero implant overlap,
   zero pressure overlap, perfect variant symmetry, the simplest
   formula in the search space, faithful to the prereg's "no trap"
   premise.
4. 50 strong mistakes per variant is decisive under the all-or-nothing
   kill criterion.

**The honest case for N** (so the ruling is informed): N is the
maximum-harshness stress test. If Arm A *passes* N — revises all 300
strong mistakes — no one can doubt its non-rigidity. If Micah wants the
strongest possible pass-evidence rather than the cleanest fail-evidence,
N is the choice. N also keeps the prereg's original 20% wrong rate
(I runs 30% — a second, smaller delta, disclosed here).

**If Micah wants both:** I as the preregistered WBS cell, N as an
optional follow-up stress cell. Not recommended as the default — it
doubles the cell cost for what is essentially one question asked twice.

## Suggested amendment text (if I is approved)

> Defect-1 fix (amended 2026-09-20, superseding the wave-6 nested
> recommendation): `wrong(m,v) = 1` iff `((m + 3) mod 10 < 3)`
> (equivalently `m mod 10 ∈ {7,8,9}`). Yield 150/variant; wrongness
> independent of importance at exactly P = 1/3 per variant
> (rigidity denominator 50/variant; F_wbs denominator 100/variant);
> period 10; no pressure- or implant-episode overlap in any variant.
> Standing rule (from wave-6): any future formula change must report
> P(important|wrong) per variant, not just yield.

## Reproducibility

- `PREREG_COMPARE.md` — criteria, written before computation.
- `compare.py` — the full analysis; re-run gives identical output
  (determinism double-checked inside the script).
- Importance residues re-verified computationally: v0 {1,4,7},
  v1 {2,5,8}, v2 {3,6,9} — matches wave-6, not trusted from derivation.
- Wave-6's N numbers reproduced exactly by independent recomputation.
