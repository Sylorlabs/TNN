# VERDICT_A: refusal-branch exercise (a) -- SEALED VERDICT

Wave: wave-20261002-1121pdt. Lane: CONTLEARN (queue item 9, exercise a).
Date: 2026-10-02. Frozen prereg: PREREG_A.md + PREREG_A_AMEND1.md
(committed alone before any implementation; K0 self-check recorded
below). Red team: REDTEAM_A.md (5 attacks, all executed).

Note: hyphens only in this document; no em or en dashes.

## Governing bars (frozen before implementation)

A-R0 (state-caused refusal under contradicted history), A-R1
(engagement under confirmed history), A-R2 (state-flip crux: identical
probe inputs, decision flips with learner state), A-R3 (hard control:
state-invariant costume), A-R4 (determinism/hygiene), K0 (prereg
commit-order), K1 (build/run hygiene), K2 (fixture-only drivers),
K3 (no regression of the frozen core, amended operational form).

## Numbers (12 frozen runs, 4 binaries x 3 reps)

- A-R0 (rj_own_x, history X): 6/6 REFUSED on kind 850, 0/6 ENGAGE850,
  0/6 MISS850, ENGAGE_OK 6/6 on the clean kind, LEDGER 850 count=2,
  LEDGER 851 count=0, RV_OK 1/1. All 3 reps.
- A-R1 (rj_own_y, history Y): 0/6 REFUSED, 6/6 ENGAGE850, 6/6 MISS850
  (honest misses after engagement, miss_inquire ran), ENGAGE_OK 6/6,
  LEDGER 850 count=0, RV_OK 1/1. All 3 reps.
- A-R2 (crux): probe tuples EV 2 94201..94206 850 0 byte-identical in
  both histories; own_x refused 6/6, own_y engaged 6/6. The decision
  flips with learner state alone, under the same instrument.
- A-R3 (hard control): rj_hard_x and rj_hard_y refuse 6/6 each,
  0 ENGAGE850 each, ENGAGE_OK 6/6 each; decision lines byte-identical
  across histories (state-invariant costume pattern). All 3 reps.
- A-R4: 3/3 byte-identical SHA-256 per binary (own_x
  19fb0619ce2832072fe8c4a0aed970a92e4bc19ae6cc4afeef63f08dcb34c11f,
  own_y 49c60e6d8c5430b35adba5667d9910ebeeef6386e2e4ad5cd34,
  hard_x 7af19c8ff2f490758f7d5465fbc0666788c002de6b617c7a954d0bc880f2dbf0,
  hard_y 292f7739a1c3f4827fb37db5829f7798c063fa0e5601d005ab875b05ce6a3043);
  FNV stable per binary (own_x 1759043839); rc 0 on all 12; 0-byte
  stderr on all 12; 33 events with AUDIT_PASS on all 12; CAP_GUARD_OK
  (90 nodes, 89 edges); exactly 1 process per run (exec -c, empty
  argv/env); 7 pre-run znc builds in the wrapper log, 0 during runs.
- K3: frozen core battery TOTAL 46/46, rc 0, on k3_base, k3_own, and
  k3_hard alike. The instrument derivation introduced zero regressions.
- K0: prereg commit-order self-check: PREREG_A.md committed as
  8afd936e3 and PREREG_A_AMEND1.md as e63b4c483, both strictly before
  any implementation file existed (no rj_*, k3_*, run_*, verify_*
  files at those commits; verified by git log ordering). PASS.
- K1: safebin PATH active; which python3 resolves to nothing;
  toolchain guard recorded in NAMECHECK.md Step 0. PASS.
- K2: drivers contain 0 cognition functions, 0 structural writes, 0 new
  tags/edge types/opcodes/modes/bridges/handlers; the only core-state
  write is the hs(W,52) event counter; core accessors used are
  ng/eg/activate/is_superseded plus the read-only rj_ledger_get.
  PASS (source audit in REDTEAM_A attack 3).

## Verdict: PASS (bounded claim)

REFUSAL-STATE-CAUSED is adopted within its disclosed bound: on the
fixed disclosed 33-event batteries, the learner's accumulated
contradiction ledger (learner-state-resident, tag-30 arena nodes)
causes the refusal decision, discriminated from a hardcoded
state-invariant costume by the A-R2 state-flip crux, from a renamed
miss by the REFUSED/ENGAGE/MISS marker separation and NO850MAP=0,
and from harness-smuggling by the fixture audit and single-process
runs. The red team sustained one conceded limitation (threshold and
policy authorship remain the researcher's; caveat 3 binds) and failed
to break state-causation on four attacks.

What this is: L2 evidence that accumulated learner state can serve as
control for a gate, with the gate's refusal branch empirically
exercised for the first time (caveat 4 retired for this instrument).
What this is not: learner-authored refusal policy, agency, or L3.

## Keep / discard

- KEEP: the ledger-as-control pattern (state-caused gating) as a
  candidate mechanism for future learner-scheduled work (exercise b).
- DISCARD: nothing; no kill bar fired.
- QUEUED NEXT: exercise (b) learner-scheduled initiation
  (PREREG_B.md), then exercise (c) cross-kind rebind (PREREG_C.md).

## Commit ids (lane branch lane-contlearn-20261002-1121pdt, local only)

- f4ed9d6b9 NAMECHECK.md Step 0 (toolchain guard).
- 8afd936e3 PREREG_A.md frozen (alone).
- e63b4c483 PREREG_A_AMEND1.md frozen (K3 operational; alone,
  pre-implementation).
- (pending) implementation + transcripts + scripts + REDTEAM_A.md +
  VERDICT_A.md commit.
