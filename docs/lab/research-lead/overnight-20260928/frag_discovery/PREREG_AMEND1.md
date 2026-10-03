# Transparent amendment A1 to PREREG_FRAGDISC.md (pre-implementation)

Date: 2026-09-30.
Status: FROZEN. This amendment strictly precedes any implementation commit.
It does not weaken any frozen bar; it repairs a routing gap found while
the prereg was being implemented (no implementation exists yet).

## What changed

Section 3b, rule R2.

Was: "R2: single-input, K_T non-empty, no such fragment -> assembler (3c)
iff |K_T| == 1; otherwise FAIL (assembler scope is single-kink by design)."

Now: "R2: single-input, K_T non-empty, no such fragment -> assembler (3c)
iff |K_T| == 1; on assembler decline or assembler failure, fall back to
the bounded base constructor (3a, sizes 1..8); if the base fails, FAIL."

## Why

T2 (x mod 3, x in 0..16) is a sawtooth: its train kink set is
{2,3,5,6,8,9,11,12,14,15} (10 kinks), so it routes R2 but cannot use the
single-kink assembler. Without a base fallback it would FAIL despite being
a straight-line task the base constructor solves in 3 ops
([IN0,PUSH3,MOD]). The unamended rule would manufacture a false FAIL on a
task the frozen predictions (section 4) mark SOLVE via base. This restores
the v1 Hypothesis B routing structure (v1 R2 had exactly this fallback:
"On success, done. On failure, bounded base (sizes 1..5), then FAIL").

## What does not change

- No prediction changes. T2 remains SOLVE via base. T4/T5 ablation remain
  FAIL: on the ablation the base fallback exhausts sizes 1..8 on the P-VM
  without success (a jump-free P-VM program cannot fit the kinked targets
  at these sizes; Lemma 1 plus the degree arguments in the redesign).
- Falsifier coverage is unchanged: section 6 already specifies that a base
  SOLVE on a P-VM kinked task fires F-TRICK (the task is VOID, not passed).
  The driver operationalizes this on the fallback path: if the base
  constructor returns an exact program on a P-VM task with a non-empty
  kink set, it logs F-TRICK-TRIPPED, the verdict is VOID, and the program
  is preserved as evidence.
- The assembler's single-kink scope is unchanged. The composer is unchanged.
  K1/K2/K3 are unchanged.
