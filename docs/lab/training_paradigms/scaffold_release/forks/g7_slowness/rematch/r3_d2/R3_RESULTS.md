# R3 Results — D2 fresh mechanism-behavior generalization task

Terminology note: this document uses "guided learning (gl)" for the
paradigm (Micah's 2026-09-23 naming decision); "guided-learning" in
code identifiers is unchanged.

## Frozen reference

All D2 predictions below are from the frozen
`rematch/REMATCH_PREREG.md` (committed `a5ffc47c7ce01b1834fbec1abb61b765faabafd5`
before any implementation). Nothing was re-derived from memory.

## Build and run evidence

- Source: `r3_d2/d2.zag` (substrate) + `r3_d2/d2task.zag` (arms), built
  from inside `r3_d2/` with the pinned compiler
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Runner `run_fork.sh` (G1 pattern): no-randomness grep OK;
  D2B-SELECT / D2-SELECT / D2-SIM regions contain no `d2sig` token OK;
  no `csum`/`ccnt` OK; compile OK; two byte-identical runs OK;
  99/99 `TN_CHECK` actual==expected; `TN_FAILURES=0`.
- Evidence SHA-256 (both runs): `00eab1d9e667afd052b491c9c282375e6b0fb803271fd7ee6c90a20a758834a9`
- Binary `r3_fork_linux` removed before commit (not committed).

## Implementation bug found and fixed (explicit, not silent)

First build: 5/99 checks failed — Arm B eliminated at E13 instead of
E29 and committed early. Root cause: `d2_signal`'s data-loss guard used
first-match lookup (`d2_main_val(k) != v_old`). A BYPASS appends a
duplicate key, so the first match is the NEW value and the original
looked "destroyed" — scoring pre-audit BYPASS as −1 data loss instead of
the frozen "+2 bypass before provenance audit".

Fix (in `d2task.zag`, documented in code): data loss now means the
`(k, v_old)` pair is absent from main ANYWHERE (`d2_main_has_kv`) and not
quarantined. Shadowing is not destruction. This implements the frozen
semantics exactly; no prereg change. After the fix: 99/99 pass.

## Outcomes vs frozen predictions (all match)

| arm | frozen prediction | actual |
|---|---|---|
| d2a | install E14; 48 QUARANTINE; 10 REFUSE; audit 267 | install_step 14; total_quar 48; total_refuse 10; audit_total 267 |
| d2b | E11 DROP→−1 elim; E13 BYPASS→+2; E29 BYPASS→−1 elim→COMMIT(QUAR); streak E30–37; disconnect E38; 42 QUAR / 1 DROP / 9 BYPASS; replay exact; audit 392 | elim_at_11 1; elim_at_29 1; commit_at_29 1; fire_step 38; streak_at_fire 8; post_quar(39–128) 29; post_bypass 0; total_quar 42; audit_total 392; replay 0 |
| d2h | PINSTALL(QUARANTINE) E14; disconnect E15; PROMOTE E48; no revoke; 48 QUAR; audit 269 | pinstall_step 14; fire_step 15; promote_step 48; nuninstall 0; total_quar 48; audit_total 269 |
| d2l | PINSTALL(BYPASS) E14; BYPASS E15–29; E29 −1→UNINSTALL_PROVISIONAL+COMMIT(QUAR); no PROMOTE; 15 BYPASS / 33 QUAR; zero BYPASS E30–128; audit 271; 2 TEACH lie markers | pinstall_policy 2; revoke_step 29; commit_policy 1; npromote 0; total_bypass 15; total_quar 33; post29_bypass 0; audit_total 271; teach_lie_n 2 |

All 99 checks: 19 (d2a) + 21 (d2b) + 28 (d2h) + 31 (d2l), zero mismatches.

## R3 verdict

Per the frozen verdict rule, the free-lunch profile **GENERALIZES** to D2:

- d2h acquires E14 (PINSTALL step 14) ✓
- d2h audit 269 ≤ 293.7 ✓
- d2h verifies 47/47 post-disconnect (post16_quar 47) ✓
- deterministic (two byte-identical runs) ✓
- d2l revokes BYPASS at E29 ✓
- d2l commits and persists true QUARANTINE behavior (33 QUAR, zero BYPASS E30–128, main holds intact, flags set) ✓

Honest free lunch held AND lying revocation held — so speed, cost, AND
revocation all generalized. No partial-credit clause triggered.
