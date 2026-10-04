# Transparent amendment: H1 deletion-bar calibration (wave-20261001-2021pdt)

Date: 2026-10-02. Status: committed alone BEFORE any sealed evaluation.

Background: the frozen prereg PREREG_H1.md (committed alone at 1942eb51b)
estimated the section-3.1 deletion set at "about 155" lines and set the
delta bar at >=150 deleted, 0 added.

Measured fact from the implementation (TNN3H1-IMPL, pure deletion, diff
verified d-hunks only): the complete 3.1 set is 135 lines
(t2_asm_chain, t2_asm_count, t2_asm_sum lines 362-410; t2_trial plus the
menu-order comment lines 581-666). Applied deletions total 143 lines:
the 135-line 3.1 set, plus 5 lines of dead mp_run wrapper (667-671,
dead after trial deletion), plus 3 lines of ev_query miss-path call
site (826-828, so the miss path falls through to the pre-existing
bootstrap/inquiry fallback). Insertions: 0. Modified lines: 0.

Amendment: the delta bar is recalibrated from ">=150 deleted" to
"the complete 3.1 deletion set (135 lines) removed, total deletions
143, insertions 0". Rationale: the bar's intent was complete removal
of the assembler/menu-order machinery; the estimate was wrong, the
complete set is verifiably gone (zero residual references), and the
implementer did not delete extra code to chase the number. This is a
calibration to the measured complete set, not a weakening to force a
pass: the net line accounting (0 added, 143 deleted) still satisfies
the hypothesis's zero-or-negative cognition-source claim with margin.

All other frozen bars are unchanged. The sealed evaluation runs
against this amended bar.
