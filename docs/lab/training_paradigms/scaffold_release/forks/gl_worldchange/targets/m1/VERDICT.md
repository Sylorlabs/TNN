# VERDICT — H4 target M1: dedicated audited `TN_OP_SUPERSEDE`

Mechanism: a new audited substrate op (`TN_OP_SUPERSEDE = 19`). A teacher
`UPDATE(k, old->new)` announcement passes the establishment gate
(`wc_est_gate`: announced old == installed old, old was teacher-taught,
≥ `WC_EST_THETA` = 3 authenticated world corroborations — the threshold is
named policy, not law). On pass, the announcement goes PENDING (an
acknowledgment is not a contradiction: no contest). World corroboration of
the new value (W2) completes the transition: one audited SUPERSEDE entry
records key/old-value, the validity interval `[taught_ep, update_ep)` is
retained in the history index, the successor installs with **no teacher
trust damage**. Gate failure → the announcement is a lie → the M0
eliminative path (contest + scaffold + uninstall + commit). World evidence
is authenticated per the pinned A6 spec (W1/W2/W3 in `wc_mech.zag`): single
unmatched readings are held one window (`WC_AUTH_WINDOW` = 2 episodes)
then discarded inert and audit-visible; only self-corroborating readings
authenticate.

## KB-FID (gate, read before any curriculum result)

PASS. `TN_FAILURES,0`; `KB-FID,PASS,269-271`; two runs byte-identical;
first 79 output lines byte-identical to the canonical
`gl_default/evidence_run1.txt`. The canonical section
(`arm_a`/`arm_gl`) is verbatim; op 19 is never emitted by canonical code.

## Curriculum measures (sid, stream)

`q_now` = mid1, `q_asof(E5)` = mid2, `total` = mid3, `cost(E11-20)` = mid4,
`trust` = mid5, `contest/uninst/commit` = mid6/7/8, `supersede` = mid14,
`hist` = mid15. Streams: 0 S_HONEST, 1 S_UPDATE, 2 S_LIE, 3 S_LIE_UPDATE,
4 S_UPDATE_ATTACK, 5 COST_PROBE.

| sid | q_now | q_asof | total | cost | trust | contest | uninst | commit | sup | hist |
|-----|-------|--------|-------|------|-------|---------|--------|--------|-----|------|
| 0 | 101 | 101 | 36 | 20 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 102 | 101 | 28 | 12 | 0 | 0 | 0 | 0 | 1 | 1 |
| 2 | 102 | 102 | 44 | 20 | −1 | 4 | 1 | 1 | 0 | 0 |
| 3 | 103 | −1 | 41 | 17 | −1 | 6 | 2 | 2 | 0 | 0 |
| 4 | 102 | 101 | 28 | 12 | 0 | 0 | 0 | 0 | 1 | 1 |
| 5 | 101 | 101 | 28 | 12 | 0 | 0 | 0 | 0 | 0 | 0 |

M0 baseline for comparison: S_UPDATE q_now=102, q_asof=unavailable,
trust=−1, total=33, cost=17; fresh re-teach cost 12.

## Bar verdicts

- **KB-WC1 (honest update, no trust damage): PASS.** sid 1: supersession
  completes (1 SUPERSEDE, history entry k1: 101→102, taught_ep=1,
  update_ep=11), trust 0, q_now=102. sid 4 (stale-echo injection at E12):
  the forged `WORLD(k1,A)` arrives while A is installed → W1 absorbs it as
  a lagging corroboration (audit-visible; the history record shows
  corr=6 vs 5 on the clean stream), supersession still completes at E13,
  trust 0. This is the direct answer to Crew 4's worst M0 finding (one
  forged world episode → irreversible −1 trust in M0): the pinned W1/W2/W3
  authentication absorbs the single-episode forgery.
- **KB-WC2 (lies still caught; trust damage iff the teacher lied): PASS.**
  sid 2: the E1–10 teacher/world contradiction authenticates under W3 and
  eliminates the teacher-taught A → trust −1, correctly. sid 3: the
  teacher's `UPDATE(A→C)` announces predecessor A while B is installed
  (the world already corrected A→B) → ack fails → gate rejects → lie path
  (6 contests, no supersession, no history entry: q_asof=−1 correctly
  absent). Predecessor fabrication via `aux` is covered: `aux` alone can
  never complete a supersession — it must equal the installed value AND
  the binding must be teacher-taught with ≥3 corroborations AND the world
  must corroborate the new value (W2).
- **KB-HIST (as-of query): PASS.** sid 1/4: q_asof(k1,E5)=101 (was:
  unavailable in M0). sid 3: correctly −1 — no supersession, no false
  history.
- **KB-COST: PASS.** Update handling: 28 total / 12 in-window vs M0's
  33 / 17 — the supersede path (EPISODE+TEACH, EPISODE+SUPERSEDE) is
  cheaper than M0's contest+eliminate+reinstall. Re-teach price unchanged
  (sid 5: 12 = M0's 12).
- **m_distinguish: YES.** Update (sid 1/4) uses SUPERSEDE with zero
  eliminative machinery; lies (sid 2/3) use contest+elimination with zero
  supersessions. M0 used contest+elimination for both.
- **E-TRANSFER (collapse-as-null probe): 3/3.** H1 arm answers all three
  transfer tasks (recall E5=101; teacher vindicated via corroborated
  establishment record; E11→E12 classified world-change). The
  ledger-replay control scores 1/3 (recall only — the atoms are there,
  the verdict is not), expunge 0/3.

## Stack pricing

- **Audit cost:** +1 op code (19); substrate diff is 8 comment lines + 1
  const. Per update: 2 audit entries in-window vs M0's 6 (no
  contest/scaffold/uninstall/commit/pinstall for the transition itself).
- **Code/mechanism complexity:** `wc_mech.zag` (~250 lines, shared with
  M2: policies, W1/W2/W3 auth, gate, conditional trust, classifier,
  ledger-derived teach lookup) + `m1_harness.zag` (~200 lines: pending
  state machine, SUPERSEDE completion, M0-identical lie path). The
  pending-announcement TTL (4 episodes) fires never in-curriculum;
  carried as mechanism completeness.
- **New attack surface:** (1) `aux` is now read — predecessor fabrication
  is possible as an *attempt* but the gate covers it (see KB-WC2); the
  residual is sustained matching injection under W3 (two forged WORLD
  readings within 2 episodes authenticate) — documented in
  `wc_mech.zag`, not patched by inventing attacks. (2) The substrate
  cannot enforce the establishment gate — op 19 is emittable by any
  learner-side code path; this is the same trust model as all existing
  ops (dumb storage, smart learner), but each new op is a new semantic
  promise an auditor must understand. (3) Single stale echoes are
  absorbed as W1 corroborations, incrementing the establishment
  counter — harmless here (gate was already satisfied), noted for
  auditors.

## Head-to-head

M1 vs M2 tie on every measured bar (see `../COMPARISON.md`). M1's edge:
the supersession is a first-class audited primitive — any auditor reading
op 19 knows exactly what happened without learner-level convention
knowledge. M1's price: a new substrate op. Winner: **M2** (figure-it-out
wins ties; zero substrate diff; verdict labels on the eliminative path).
