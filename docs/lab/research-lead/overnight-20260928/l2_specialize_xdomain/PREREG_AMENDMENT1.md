# PREREG AMENDMENT 1 (pre-implementation, committed before any .zag exists)

Amends PREREG.md (frozen cb8545cb4). Reason: red-team self-review caught
researcher-specified literals inside the learner design.

1. TRIAL FLAGS (sections 2, 4, 5, 7): the design recorded TRIAL2F/TRIAL3OK
   with learner logic of the form "if L==2 set TRIAL2F". That names the
   candidate values 2 and 3 inside the learner, which is exactly what K3
   forbids (the learner must decide the values, not be told them).
   REPLACED by fully generic counters:
   - header 10: TRIAL_FAIL_N (u8): count of candidate trials that failed
     verification before the accepted trial (generic: incremented on any
     failed trial, no value literal).
   - header 11: TRIAL_TOTAL (u8): total candidate trials run (generic).
   - header 9 SPEC_NF stays: the accepted fold-count L (255=none).
   K3 in-Zag becomes: spec_nf==3 AND trial_fail_n>=1 AND
   trial_total>=2. The trace still shows `XS-TRIAL nf=2 FAIL` then
   `XS-TRIAL nf=3` + `XS-ACCEPT`, so the decision (try 2 from inventory,
   fail, fix 3 on verification) is auditable without any literal in
   learner logic.
   F-TRIAL becomes: trial_fail_n < 1 or trial_total < 2.
   Section 4 worksheet lines reading "TRIAL2F=1" now mean
   "trial_fail_n=1"; "TRIAL3OK=1" now means the nf=3 trial accepted
   (visible as XS-ACCEPT + SPEC_NF=3). No frozen S/E numbers change:
   the flags cost nothing.

2. TYPE-14 EDGES (section 2): type 14 is permitted by F-EDGE-NEW but NO
   type-14 edges are created anywhere in this design (delivery provenance
   is LAST_VIA only). F-EDGE-NEW still fires on any edge with type
   outside {14,16}; the frozen expectation is exactly two type-16 edges
   (3->1, 3->2) in ARM-FULL and zero edges in ARM-GENERAL/ARM-ABLATE-X.

No frozen kill-bar thresholds, worlds, queries, counting rules, or
expected S/E/ANS numbers change. Algorithmic content unchanged; only the
learner-side recording of the trial decision is de-literalized.
