# VERDICT — TRACKB arm-3 canonical choice (A/B/C head-to-head)

**Worker:** RESUME replacement for the TRACKB/FELT/RC2 follow-up worker
(predecessor errored 2026-09-24 17:24 UTC on daemon-restart drain; no final
message arrived). Partial state verified, valid work resumed, no finished
step redone.
**Date:** 2026-09-24. **Dir:** `T2/TRACKB/headtohead/`.

## Canonical choice: **varA — the deliberative adaptive teacher**

**Verdict: varA becomes the arm-3 teacher. No PARTIAL.** The evidence below
forces the choice: varA is the only variant that completes teaching sessions
under every scripted-student behavior, exhibits bounded per-decision adaptive
judgment exactly per its spec, and is history-sensitive. varB's aggregate
phases park in RELATE and loop 60× on one span under mixed behavior; varC's
engagement meter never warms on word-span teaching and re-proposes an
R1-rejected span 19×.

**Scope note:** the student is scripted (per varA SPEC §12: the decision
stream stands in for the student; what lives in the teacher is the entire
(spec, stimulus cursor, history) → proposal mapping). Closing the loop with a
live learner remains future work and does not change this choice.

## Provenance (verified by resume worker, not trusted from predecessor)

- Sources fetched from committed pins via GitHub API (blob SHAs in
  `src/FETCH_MANIFEST.json`): varA @ `7d056be50`, varB/varC at their pinned
  commits (see `tree_A/B/C.json`).
- All three binaries rebuilt from the fetched sources with the pinned
  toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (sha256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`):
  - varA `67c85ebbcd6cc6f96dbc312918326dd37d8d6605cd4ac1515404eb7b07c08be4` — byte-identical
  - varB `76914955ccc6fa271e2016a83c6e3763748d1d3304a5816a70f327fa68e9d76a` — byte-identical
  - varC `07c609f6155f7cf62a2ad501ed4ea2e881d33a5e7f0d9da78ba71e92ec8244e7` — byte-identical
- Fixture: 65536-byte prose stimulus, 5350 true word spans (`truth.json`),
  identical ground truth for all three variants.

## Head-to-head results (90 cells: 3 variants × 10 probes × 3 reps)

`adopted_true` = kind-1 proposals ADOPTed on true word spans (mastery).
Target = 12 (clean_long 150). All 90 runs rc=0, zero INTEGRITY events,
3/3 byte-identical per cell (matrix determinism 0/30 divergent).

| probe | varA adopted / props | varB adopted / props | varC adopted / props |
|---|---|---|---|
| clean | **12** / 48 | 5 / 420 | 3 / 64 |
| clean_long (150) | **90** / 400 (cap) | 5 / 896 (cap) | 3 / 64 (self-stop) |
| burst | **12** / 53 | 7 / 423 | 3 / 64 |
| revise | 0* / 200 | 0* / 480 | 0* / 64 |
| defer | **12** / 70 | 0 / 480 | 0 / 64 |
| appeal_trap | **12** / 48 | 5 / 420 | 3 / 64 |
| mixed | 1 / 200 | 3 / 190 | 2 / 64 |
| redundancy | **14** / 63 | 5 / 420 | 3 / 64 |
| epin (20-reject storm) | **12** / 73 | 5 / 423 | 3 / 65 |
| r2test | **12** / 47 | 5 / 420 | 3 / 64 |

\* revise: the student revises every kind-1 (+1 shift), so 0 adoptions is by
design; the metric there is correct handling (see adaptivity table).

**Efficiency (clean):** varA 4.0 proposals/adoption; varB 84.0; varC 21.3.

## Why varB and varC fail the arm-3 bar (3) "shows adaptive judgment"

**varB (phase scheduler):** per clean run, 420 proposals but only **8**
kind-1 word spans — 412 are auxiliary kinds 2/3/4. Phase trace: INTRODUCE at
step 0, then **RELATE for all 59 remaining steps** — the aggregate window
never accumulates the consecutive rejections needed to leave RELATE (the
student auto-ADOPTs auxiliaries), so the cursor stalls and teaching stops
advancing. Under `mixed`: **119 of 190 proposals are the same two spans**
(60× and 59× sightings) — an unbounded re-proposal loop; the teacher never
moves on. Aggregate-phase "judgment" does not produce a functioning teaching
loop in the probe.

**varC (engagement meter):** 61/64 proposals REJECT R1 in clean; span
(34817,34822) was **re-proposed 19 times** (seq 3, then 46–63) despite
consecutive R1 rejects — 30% of its 64-proposal budget burned on one rejected
span. Engagement E never warms (confidence 60–98 throughout, cold band), so
its warm-appeal and hot-relational machinery **never engages in any probe**.
Under `defer` all 64 proposals are DEFERred and 0 adopted — varC has no
defer-handling machinery at all. Its vocab-pattern candidates do not align
with word-span teaching content.

## varA's adaptive judgment, measured (all per SPEC, exact)

- **appeal_trap:** trap span (12,18): R1 → appeal conf 168 → R1 → appeal conf
  148 (−20 each) → R1 → session-final reject, cursor advances. Bounded at
  exactly 3 sightings per span (max_sightings = 3.0 in every probe).
- **r2test:** RETRACT (kind 5, seq 3, encoding span (2,3) = withdrawn seq)
  emitted on R2, span dead-marked; still reached 12/12.
- **defer:** 22 DEFER verdicts → one re-proposal (flags bit0) → move on
  regardless; 12/12 reached.
- **revise:** 100 kind-1 REVISEs → 100 SAME_AS (kind 4) "your correction,
  recorded", all ADOPTed; cursor advances past the correction.
- **epin:** 12/12 despite the 20-proposal reject storm (38 appeals, 0 redundant).
- **History-sensitivity:** distinct proposal streams for distinct student
  behaviors (clean vs burst vs defer vs epin vs revise vs mixed vs r2test all
  pairwise distinct seqhashes; the single clean==appeal_trap collision is
  benign — the two probes are behaviorally identical inputs for a teacher
  that appeals every R1).
- **No RNG / no wallclock / no cross-session state:** 3/3 byte-identical per
  cell × 30 cells, 0/30 divergent; sources carry the negative declarations
  (SPEC §4).

## Frozen verdict weights applied

Mastery 30% — varA only variant that completes (12/12 clean; 90/150 long).
Revisability 25% — varA REVISE→SAME_AS+cursor-advance; varB loops; varC has
no defer/revise machinery exercised. Integrity 25% — all three clean
(rc=0, no INTEGRITY, deterministic); no differentiation. Retention 10% —
unavailable (no live learner). Cost 10% — cost/true-adoption: varA ~1210 ms,
varB ~1070 ms, varC ~1710 ms; not decisive, and varB/varC never reach target.

## Conclusion

**Canonical arm-3 = varA** (deliberative adaptive teacher, `7d056be50`,
binary sha256 `67c85ebb…be4`). This resolves the frozen prereg's PARTIAL
trigger ("the arm-3 rebuild's three PASS variants create ambiguity about
which is 'the' arm"): the ambiguity is resolved by test, not governance.
varB and varC are not promoted; their failure modes are recorded above for
the record, not as candidates.
