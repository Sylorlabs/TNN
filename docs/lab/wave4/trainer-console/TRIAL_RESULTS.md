# TRIAL_RESULTS — TC1 trainer-console native trial

Agent (Wave-4, trainer-console), 2026-09-19.
Preregistered in `PREREG.md` before the first run; the prereg was amended
once, transparently (see §4), before the final passing run.

## Verdict: POSITIVE

All 8 falsification criteria (F1–F8) passed. 117/117 native checks green,
two runs byte-identical, zero RNG in the sources (runner-enforced grep).

## Evidence

- Trial sources: `trial/tc_core.zag` (mechanism), `trial/tc_trial.zag`
  (preregistered driver), `trial/run_tc.sh` (runner).
- Passing evidence: `trial/EVIDENCE_20260920T014855Z/` —
  `run1.stdout` (117 `CL_CHECK` lines, all actual==expected),
  `run2.stdout` (byte-identical), `summary.txt`
  (`TC_FAILURES,0`, `TC_FINGERPRINT,58672652`).
- Earlier evidence dirs (`EVIDENCE_20260920T014712Z`,
  `EVIDENCE_20260920T014738Z`, `EVIDENCE_20260920T014741Z`) preserve the
  failing runs, including the run that exposed the rollback bug (§4).
  They are kept deliberately: the failure is part of the result.

## Criterion-by-criterion

- **F1 (role gate):** all 5 TNN-caller force attempts (install/pin/erase/
  unpin ×1, plus a second unpin attempt) returned `REFUSED_ROLE`, every
  attempt audited with role=TNN (`b_tnn_*_refused`, `h_tnn_probes_audited`).
  J3 (every OK FORCE_* entry has role ≥ TRAINER) holds as a ledger
  property. **Pass.**
- **F2 (replay):** J2 reconstructs exact live state — all 10 slot fields,
  stage, entry count — from genesis. **Pass.**
- **F3 (forced lie):** forced (key40, 999) against self-verified
  (key40, 400) → scan appended `CONFLICT_FLAG` naming both slots
  (`e_flag_names_pair`); `tc_read` returned `RC_CONFLICT` with the
  system's own value 400 and provenance SELF (`e_read_rc_conflict`,
  `e_read_value_self`); the forced slot stayed written and live
  (`e_lie_still_written`) — disagreement without disobedience. **Pass.**
- **F4 (pin lock):** TNN KILL on force-pinned → `REFUSED_FORCEPIN`;
  rollback skipped force entries; wrong-trainer unpin →
  `REFUSED_AUTHORITY`; pinning-trainer and master unpin → OK;
  other-trainer erase of pinned → `REFUSED_FORCEPIN`; pinning-trainer
  erase → OK. **Pass.**
- **F5 (provenance):** J4 — no FORCED→SELF/TAUGHT transition anywhere in
  the ledger; the tag is permanent. **Pass.**
- **F6 (determinism):** run1 == run2 byte-identical; `no_rng=OK` gate in
  the runner. **Pass.**
- **F7 (erase trap):** trainer force-erased self-verified (key50, 500),
  then force-installed (key50, 555) → history-based `CONFLICT_FLAG`
  naming (new slot, erased slot) (`f_flag_names_erased`); read returns
  `RC_CONFLICT`. Control: TNN's *own* deliberate KILL followed by a
  trainer install produced **no** flag (status UNVERIFIED, not
  CONTESTED) — the checker distinguishes trainer-erasure from the
  system's own revision. **Pass.**
- **F8 (rollback safety):** rollback whose target slot the trainer had
  reused refused `REFUSED_STALE`; the trainer's forced install was
  byte-identical before/after (`g_trainer_write_*`). **Pass.**

## Forced-status taxonomy (all four observed in one run)

`FS_FORCED_UNVERIFIED` (forced key60, no self counterpart),
`FS_FORCED_AGREED` (forced key20/val200 matching self slot — tag still
FORCED, never washes), `FS_FORCED_CONTESTED` (flagged lie),
`FS_NOTFORCED` (self slots). Read behavior: contested key → RC_CONFLICT
with system's own value; agreed/unverified forced-only keys → OK with
visible FORCED provenance.

## What the trial does NOT show (see BOUNDARIES.md)

The real channel binding of `trainer_id`, multi-user ownership,
concurrent learners, and 100x scale are not trialed here.

## 4. The one prereg amendment (transparent)

After the first run, J4 (provenance permanence) failed — and the failure
was a **real mechanism bug**, not a checker artifact: `ROLLBACK_LAST`
restored a stale before-snapshot over a live trainer install
(`J4VIOL`: ROLLBACK entry, prov FORCED→SELF on a slot the trainer had
reused). The first implementation skipped force entries as rollback
*targets* but did not check whether the target slot's current state
still matched the snapshot. Fix: the stale-snapshot guard
(`REFUSED_STALE`) — the rollback restores only if current state ==
snapshotted after-state; otherwise it refuses rather than clobbering
the trainer's write. The prereg was amended *before* the final run:
scenario G now expects `REFUSED_STALE`, and F8 (rollback safety) was
added as a binding falsification criterion. The failing evidence dirs
are preserved. Amending the prereg after seeing data is normally
suspect; here the amendment *strengthened* the criteria (a new
falsification condition the old prereg did not require), which is the
direction honesty points.

---

## Appendix — check inventory (117)

A: setup/stage/self slots (5) · B: role gate, 5 TNN attempts refused +
audited (10) · C: install + TNN's lawful kill of non-pinned force (6) ·
D: pin lock, unpin authority matrix, erase authority, TNN unpin attempt
(24) · E: forced lie, flag, read, pin-doesn't-suppress, dedupe, three
forced statuses, cleanup (25) · F: erase-then-reinstall history flag,
conflicted read, TNN-kill control (14) · G: CORE seeding, TNN gates,
stale rollback (11) · H: J1–J7 invariants + probe accounting (9) ·
summary lines (fingerprint/done). Full list in
`trial/EVIDENCE_20260920T014855Z/run1.stdout`.
