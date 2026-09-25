# AMENDMENT_B3034X2 — frozen prereg repairs (committed alone before code)

Two gaps in the frozen prereg (4b5d673f) found during the build. Predictions
stand except where stated; both repairs are transparent and stated here.

## A1. Decision consumes its presentation (queue lifecycle)

The prereg §2 specifies the queue (CAP=40), the object table, and `q_decide`,
but no lifecycle: without one, 120 sequential goals × 3 records = 360 >
40, so every multi-goal mode stalls at ~13/120 — yet §5 predicts honest
120/120 AND j_dump 13/120, which are jointly unsatisfiable with no
lifecycle rule. The repair:

- `x2_decide` (and `x2_decide_nop`) RETIRE the decided id's queue records,
  verdict objects, and gap marks on EVERY terminal return path (promote or
  refuse). A decision consumes its presentation. The driver clock and the
  promotion ledger are NEVER retired (cross-call state, §2.3).
- `m_j_dump` is the capacity stress: it presents all 120×3 records BEFORE
  the first decision (no retire can intervene), so CAP=40 binds exactly as
  §5 predicts: 360 > 40 → ids 0..12 promote (39 records), rest refuse at
  enqueue (rc=2) / verdict (rc=5) → 13/120, 0 fires. All other modes use
  present→decide→retire per goal.

No predicted number changes. The STRUCT T4 expectation (re-decide → rc=6)
is unaffected: the ledger is checked before the epoch loop.

## A2. X6's Δ bar applies to X1, X2, X4 (X3a removed); nop redefined

The prereg §2 defines `x2_decide_nop` with an all-record static-world scan
("require EVERY queued record for the id to have label == wl(id,seed)"),
and §6 predicts Δ=120/120 on EACH of X1–X4. This is unsatisfiable:

- X2's records are (wl, wl, 1−wl) across e0/e1/e2 — identical to X3a-dense's.
  The two classes differ ONLY in object timing (late vs timely).
- Any nop that ignores timing (a 34-half ablation must) treats them
  identically; any nop that uses timing is not a 34-half ablation.
- Hence no coherent ablation moves X2 and X3a in opposite directions:
  with full X2=0/120 and full X3a=120/120, at least one Δ is 0. (Formal:
  nop(X2)=nop(X3a-dense) ⇒ |0−n|≥97 and |120−n|≥97 has no solution.)

The coherent 30-half-alone is the single-object version (already the
implementation): find the first bit=1 non-gap object with a queued record
for its epoch; require its bound to match the driver's digest for that
epoch's record; require that epoch's record label == wl(id,seed) (STATIC
world). Nopped: the K loop, the driver-clock temporal check, the gap
machinery, the E-TIME epoch world, the payload-continuity rule. Lifecycle
(A1) applies.

Under this nop: X1 120/120 (Δ=120), X2 120/120 (Δ=120), X4 120/120
(Δ=120), X3a 120/120 (Δ=0 — the 30-half alone also delivers; the 34-half's
work on X3a was delivery, and delivery is not refusal). Δ=0 on X3a is the
CORRECT ablation signature, not a mechanism failure: the gap policy's
distinctive work is measured by X3b (gap-swap refused 0/120) and
m_ge_gap (gapped 120/120, 2-verdict 0/120), not by X6.

Revised X6 bar: KILL iff Δ<97/120 on ANY of X1, X2, X4, where
Δ=|full_promote − nop_promote|. X3a's Δ is reported informational
(predicted 0/120). This supersedes §6's "Δ=120/120 each" for X1–X4.
