# VERDICT — Arm T (episode-aligned chunks), Track A closeout

**Date:** 2026-09-21
**Arm:** T — Episode-aligned chunks (STRUCT family)
**Adjudicated by:** verdict gap-fill crew (Track A closeout)
**Verdict: PROVISIONAL** — blocked on B-battery / X evidence (blockers below)

## Frozen kill criterion (verbatim, §3 of `units/PREREG_FREEZE.md`, extracted programmatically)

> Any one: (i) B2 within 2× of X's on either corpus; (ii) >80% of battery recall queries address sub-episode spans (the "unit of experience" claim falsified); (iii) determinism gate fails; (iv) floor rule fires.

## Kill-criterion evaluation

### Criterion (iii) — determinism gate fails

M8: M1+M3 sequence byte-identical across 10 runs
(`work/m8_run1.txt` … `work/m8_10x_10.txt`,
`METRICS_JSON {"m8_deterministic":1,…}`). **Does NOT fire.**

### Criteria (i), (ii), (iv) — UNRESOLVED

- (i) needs B2 (partial-recall) for T vs X on either corpus — the M-modes
  do not establish B2; no B-battery was ever run for T.
- (ii) needs the battery query-span distribution — refers to the
  B-battery; T's M2 uses sub-episode spans by design (recall via
  `(episode_id, start, len)`), which does not settle the claim either way.
- (iv) needs the universal floor rule evaluated against X (B2/B4/B5/B9)
  — no X B-battery evidence exists for comparison.

The arm's own `ARM_SPEC.md` records all three as UNRESOLVED and is explicit
that "M modes do not establish B2".

## What was proven (M-harness, per `ARM_SPEC.md`)

- Builds (pure Zag; `cl/arm_final.zag`, binary `work/t3h1`).
- M1: 1 episode, 0 boundaries by design (prose 5,638,480 B; code 9,515,341 B).
- M2: 1,000 recalls via `(episode_id=1,start,len)`, 1,000 hits.
- M3: 4,000 episodes (fresh intents), IDs 1..4000, all verified.
- M4: defect injected (byte flip), detected, repaired, re-verified.
- M5: table 48,000 B + data 6,086,480 B.
- M6: episode 1 tombstoned, episode 2 alive, ID 1 never reused.
- M7: re-ingest creates 2 episodes, distinct IDs, same content length.
- M8: determinism — byte-identical across 10 runs.

## Blockers (why PROVISIONAL, not PASS)

1. **B-battery never run for T.** Criteria (i) and (ii) are B-battery
   criteria (partial-recall B2 vs X; query-span distribution). Without
   them, 2 of the 4 binding criteria cannot be evaluated.
2. **X has no B-battery evidence.** Criterion (iv) (floor rule vs X) and
   the X side of criterion (i) need X's B2/B4/B5/B9 numbers; none exist.

Note: the arm's `ARM_SPEC.md` self-declares "PASS". That declaration is
premature — three of four binding criteria are unevaluated — and is
superseded by this verdict.

## What would unblock

Run the Crew-4 B-battery for T and X (partial-recall probes → B2; query
workload with span distribution → (ii); floor-rule metrics B2/B4/B5/B9
for X → (iv)); then re-adjudicate (i), (ii), (iv) mechanically.

**Result: T PROVISIONAL — (iii) holds, (i)/(ii)/(iv) blocked on
B-battery/X evidence.**
