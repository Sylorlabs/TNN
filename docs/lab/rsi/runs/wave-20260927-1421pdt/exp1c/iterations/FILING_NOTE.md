# Filing note: EXP1c retune trail, wave-20260927-1421pdt (uncertified historical record)

Status: UNCERTIFIED. This trail is committed only as an auditability
record per the wave debate (DEBATE_1421.md, motion M1). It carries no
certified readings and may not support a frozen verdict.

M5 (frozen retune protocol) was violated on all iterations: no
per-iteration commits were made, so the stopping rule is uncheckable and
retune shopping cannot be ruled out. Prereg item 7 was violated: the
worker parsed calibration outputs with shell text-processing (grep, sed,
awk), which voids certification of the calibration medians. No Python was
used (credited; does not cure the item-7 void).

Iteration 5 is STRUCK from evidence (unauthorized post-stop run): one-line
process note only, no iter5 artifacts committed. The variant source files
carry a mislabeled header (all say "retune iteration 1"); the file names
here (iter1 through iter4) are the corrected mapping per the red-team
audit. The worker-invented |vel|-in-{1,2} check has no frozen standing.

Headline of the attempt (worker-reported, uncertified): C1 (median P
>= 960/1200) unmet in all iterations (best 649); C2 read PASS (Z=45);
C3 unmet. The worker's "proven limit cycle" unsatisfiability claim was
REJECTED by the red team (committed template has no mote-P coupling;
the worker's own iter1 artifact shows a scripted lamp-farm surviving
1200/1200 in all 12 variants). The lo==hi deterministic escape is a real
code fact but out-of-spec input; no frozen-template repair (see debate M1
and REDTEAM_EXP1C_1421.md).

Future wave requirements (binding, debate M1): redo the retune from
scratch under M5 with per-iteration commits; try vel=0/lo<hi and
boundary-trap families before any satisfiability claim; fix the iteration
emitter label; mode_check must gate calibration; item 7 verbatim end to
end.
