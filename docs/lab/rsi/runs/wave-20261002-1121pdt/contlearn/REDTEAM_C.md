# REDTEAM_C: adversarial review of the cross-kind rebind (exercise c)

Status: RED-TEAM-COMPLETE. Wave: wave-20261002-1121pdt. Lane: CONTLEARN
(queue item 9, exercise c). Date: 2026-10-02. Every attack was executed
against the frozen sources and transcripts. Nothing here moves a kill
bar.

Note: hyphens only in this document; no em or en dashes.

## Attack 1: is the rebind real, or just chain discovery from facts?

This is the deepest attack. The prereg claims "a COUNT-kind learned
structure is rebound as CHAIN-kind procedure". The red-team probe
(rt_xk_probe): phase-A facts taught, NO count queries issued (so no
COUNT MAPs ever exist), then the (s,40) rebind query. Result: CHAIN
MAP builds fine, ans=95201.

Finding: the COUNT MAPs are NOT causally necessary for the CHAIN
rebind. The trial assembles CHAIN graphs directly from phase-A FACTS,
bypassing the COUNT MAPs. The "rebind" is FACT-level reuse across
kinds, not MAP-transformation.

Implication (conceded): the stronger reading "COUNT MAPs transformed
into CHAIN MAPs" does NOT hold. What holds: the same learned content
(the phase-A chains), previously organized and exercised as COUNT
(C-R0 proves the learner had count-kind structures), is now organized
and exercised as CHAIN (C-R1), with the kind shift discriminated
white-box (C-R2). This is cross-kind REUSE of learned content, not
cross-kind TRANSFORMATION of a learned structure. The verdict must
scope the claim accordingly. Attack outcome: PARTIALLY SUSTAINED;
the claim survives only in the weaker (reuse) form.

## Attack 2: smuggling via INT3 or interference facts

- DEP provenance probe (rt_xk_dep): the CHAIN MAP's type-1 DEP edges
  cite ONLY phase-A facts (95001,21,95101) and (95101,21,95201). No
  edges to INT3 facts (95801/95811/95821) or INT1 facts. The trial
  BFS from 95001 cannot reach the disjoint INT3 subjects.
- The INT3 family uses different subjects (95801+i) and relation 22;
  INT1 facts are single links on relation 870. Neither can supply a
  2-hop chain from 95001+i.
- Attack outcome: FAILED. No smuggling path.

## Attack 3: does the control really elide the structures?

- xk_nophase runs INT1/INT2/INT3 identically but elides CAPABILITY
  (no phase-A facts, no COUNT MAPs). Rebind queries answer -2 on all
  6 (CONTROL_MISS_OK 6/6), 0 MAPs for (95001+i,40) (CONTROL_NOMAP
  6/6), all 3 reps. The rebind depends on phase-A structures.
- Attack outcome: FAILED.

## Attack 4: does RETENTION teach the rebind?

- RETENTION queries r=43, not r=40. No 40-facts are ever taught in
  any phase (source audit: no ev_teach with r=40 in either driver).
  The rebind queries are the first 40-events; they miss and trigger
  trial assembly. RETENTION cannot teach what it never touches.
- Attack outcome: FAILED.

## Attack 5: kind-confusion (are the CHAIN MAPs just relabeled COUNT?)

- C-R2: t2_sig white-box. The 6 rebind MAP graphs contain 0 tag-103
  (INC) cells each; the 6 count MAP graphs contain >=2 each (3
  observed). The procedures are structurally different kinds, not
  relabeled.
- Attack outcome: FAILED.

## Findings carried to the verdict

- The cross-kind claim survives ONLY in the scoped form: the
  learner reuses phase-A learned content across kinds (COUNT then
  CHAIN) within one continuing run, without reset, with white-box
  kind discrimination and control-proven structure dependence.
- It does NOT establish MAP-transformation (COUNT MAPs are not
  causally upstream of CHAIN MAPs; the probe proves they are
  bypassed). The "learned structure" that is rebound is the
  phase-A chain content, not the COUNT MAP nodes.
- This is L2 evidence (structural reuse across kinds), not L3. The
  trial's chain assembly is frozen machinery; the learner does not
  invent the chain form.
- No bar was moved. C-R2 (the kill bar) passes as frozen.
