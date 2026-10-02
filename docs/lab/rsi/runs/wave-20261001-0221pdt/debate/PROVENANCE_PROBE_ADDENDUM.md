# Addendum: skeptic's provenance probe for wave-20261001-0221pdt debate

Parent-agent, 2026-10-01. The wave's debate transcript
(DEBATE_0221PDT.md) does not contain the verbatim skeptic's
provenance probe required by the standing provenance-honesty rule.
This addendum supplies the probe and its answers for the verdicts
adopted, so the record is complete. It does not change any verdict.

## M1: H-EXP2 v2 BUILD-PASS

Skeptic's provenance probe: What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?

Answer: The prereg (PREREG_H_EXP2_V2.md) is inherited from the
1121pdt wave, committed alone at cc87d6f09; the commit-order
self-check passes (prereg strictly before this wave's
implementation). The sealed laws W-A=(A=2,B=3) and W-B=(A=2,B=1)
are inherited sealed fixtures from the 1121pdt prereg, read only by
the world program. New this wave: the implementation (expworld.zag,
expseq.zag, run_exp2.sh), the bar-text audit (BAR_TEXT_AUDIT.md,
the judge-ordered precondition from the 11:21 M3 ruling), and the
sealed run evidence (wa_run1/2, wb_run1/2). The implementation hit
the pinned-znc `as *i32` slice miscompile during the wave and was
rewritten to the mandatory u8-cell workaround; no frozen bar
changed, implementation repair only. Nothing is re-certified: this
is the first execution of a frozen prereg, not a re-run of prior
evidence. Classification bounded L2, explicitly not L3, per the
prereg's own Criterion 0 disclaimer.

## M2: ddes_followup BUILD-FAIL + UNVERIFIABLE ORDERING

Skeptic's provenance probe: same question.

Answer: The prereg (PREREG_DDES_FOLLOWUP.md) and the implementation
(ddesp.zag) are both new, both first committed in 904e9b6f6 (the
20:21 wave's INCOMPLETE record commit). Because prereg and
implementation share one commit, the commit-order self-check cannot
show the prereg strictly predating the code: UNVERIFIABLE ORDERING
per the standing rule, correctly recorded. The implementation does
not compile (ddes_world arity mismatch: 14 passed, 15 expected),
verified independently by the parent with the pinned znc:
BUILD-FAIL. No verdict beyond the kill is possible. Re-freeze and
re-run is queued.

## M3: Fresh disjoint adversary byte set {k,m,r} FROZEN

New this wave, no inherited artifacts. This executes the 11:21 M1
judge ruling (the {k,m,r,v} set is exhausted; the next round needs
a fresh disjoint set). No evidence attached; it is a frozen fixture
for future rounds.
