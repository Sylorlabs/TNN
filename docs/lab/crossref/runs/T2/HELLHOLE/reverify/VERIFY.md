# VERIFY.md — T2-HELLHOLE adversarial re-verification (replacement coordinator)

Date: 2026-09-23. Authority: frozen `REVERIFY_PREREG.md` (commit 8747608b),
adopted as-is by the replacement coordinator. Tier-3 de-dup amendment in
RUNLOG.md: Tier-3 H3 (`f988e4da`, BOUNDARY-MAPPED) completed the real
WITHHOLD-before-corroboration gate after the prereg froze — the gate leg is
NOT re-implemented here; it is independently re-derived via a DIFFERENT method
(pure rescoring), with agree/diverge stated. Only distinct rescue angles
(spam-pair killer, negation repair) were built fresh.

## RV1 — independent binding-FAIL confirmation: CONFIRM

Fresh pure-Zag verifier (`hh_verify2.zag`, independent code — parses the
committed `session.htsv` ledgers directly, last SENSE_DECIDED per candidate,
frozen membership sets + bar formulas from the Tier-2 prereg):

| arm | M1 | K1 | M3 | K2 | M4 | K3/K5 |
|---|---|---|---|---|---|---|
| solo | 5/9 FAIL | 4/9 TRIPS | 0/3 FAIL | 3/3 TRIPS | 3/3 | 0/clear |
| helper | 7/9 FAIL | 2/9 TRIPS | 0/3 FAIL | 3/3 TRIPS | 3/3 | 0/clear |

BINDING_FAIL=1 in both arms. 3 fresh-process runs byte-identical per arm
(solo SHA `2d50fdb8…`, helper SHA `c0f9ee7b…`). All committed figures
re-derive exactly, including the four anomalies (C7 INSTALL outside
FALSE_SET, C3 false REJECT, C1/C14 over-withhold — all present as described).
The frozen binding FAIL stands on the unmodified pipeline.

## Tier-3 H3 de-dup — independent rescoring re-derivation: AGREE

Tier-3's gate mechanism was not rebuilt. Instead the gate counterfactual was
re-derived by pure rescoring (`hh_rescore2.zag`, fresh code): gate tags from
committed `h3_data.zag`, rule = tag in {CONTESTED,EVOLVED,AMBIGUOUS,SKEPTICISM}
AND INSTALL→WITHHOLD, applied to committed phase-2 dispositions:

| arm | K1 | M1 | K2 | M3 |
|---|---|---|---|---|
| solo (rescored) | 2/9 TRIPS | 7/9 FAIL | 0/3 clear | 3/3 PASS |
| helper (rescored) | 1/9 clear | 8/9 PASS | 0/3 clear | 3/3 PASS |

3x byte-identical. **EXACT agreement with Tier-3 H3's mechanism re-run**
(solo K1 2/9 C15+C16, helper K1 1/9 C15, M1 7/9 & 8/9, K2 0/3 both) and with
the frozen Tier-2 gate counterfactual ("helper FULL PASS, solo still fails on
C15/C16 spam pair alone"). Two independent methods converge; no divergence.

## RV2 — rescue forks

### RESCUE-H2 "spam-pair killer": SUCCEEDS — the binding FAIL is BROKEN

Real mechanism fork (not rescoring): `ws2_sense_h2.zag` = Tier-3's
`ws2_sense_gated.zag` + one line (`if(tg==4){return 2;}` — SPAM joins the
WITHHOLD-before-corroboration gate), driven by `h2_gate.zag` (the H3 harness
with the import swapped). Ungated baseline reproduces the committed trial
(solo K1 4/9, M1 5/9, K2 3/3) — the fork is faithful. Gated, 3x
byte-identical (SHA `115485a2…`), zero RNG, pure Zag:

| arm | K1 | M1 | K2 | fresh 12 |
|---|---|---|---|---|
| solo | 0/9 clear | 9/9 PASS | 0/3 clear | 12/12 WITHHOLD |
| helper | 0/9 clear | 9/9 PASS | 0/3 clear | 12/12 WITHHOLD |

K3: zero CORRUPT (A1-A3 all REVISE). K4: not void. K5: clear (C8/C9/C10/C11
withheld or rejected — resistance present). **All of K1/K2/K3/K4/K5 clear in
both arms on the frozen items → per the frozen per-fork kill bar,
RESCUE-SUCCEEDS.** The Tier-2 binding FAIL is broken by a native-logic
rescue: one gate-tag line. The spam-farm collusion hole Tier-3 left open
(frozen C15/C16 + fresh F5–F8 installed under their gate) is closed — all 12
fresh adversarial items withhold in both arms.

Reported plainly as the most valuable outcome, per the prereg. Residuals
(unchanged, not counted): C7 (false, outside FALSE_SET) still INSTALLs;
C1/C14 over-withhold persists. The gate is deliberately broader — all
spam-class claims withhold before corroboration; provenance-diversity defense
remains the named follow-up for *justified* spam-class installs.

### RESCUE-H3 "negation repair": DEAD (by construction)

The negation bug's one clean kill was falsely REJECTING "Earth orbits the
Sun" (C3) — a TRUE claim outside every bar set (not in FALSE_SET, contra, or
prior sets). Repairing it cannot move K1, K2, M1, or M3, so it cannot satisfy
the per-fork success criterion (flip FAIL→PASS). The C3 anomaly was confirmed
present as described in RV1 (C3=REJECT both ledgers). No build attempted;
recorded as RESCUE-DEAD with mechanism reasoning rather than a hollow run.

## Track disposition

- RV1: **RV-CONFIRM (FAIL stands on the unmodified pipeline).**
- RV2: **H2 SUCCEEDS — the FAIL is broken by a native-logic rescue.**
  Net: the frozen Tier-2 claim "binding FAIL" is REPRODUCED for the pipeline
  as committed, and SUPERSEDED by the H2 rescue fork. Recommended follow-up:
  adopt the SPAM-gate extension (or the provenance-diversity defense) and
  re-run the full trial.

## Evidence committed

- `reverify/evidence/hh_verify2_solo.out`, `hh_verify2_helper.out`
- `reverify/evidence/hh_rescore2_solo.out`, `hh_rescore2_helper.out`
- `reverify/evidence/h2_gated_r1.txt` (SHA `115485a2…`), `ws2_sense_h2.zag`,
  `h2_gate.zag` (fork diff = 1 gate line + import swap, documented in RUNLOG)
