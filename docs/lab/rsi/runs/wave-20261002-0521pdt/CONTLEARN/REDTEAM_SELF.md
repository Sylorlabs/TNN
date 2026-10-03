# REDTEAM_SELF: CLH2 longer-horizon delayed rebind

Wave: wave-20261002-0521pdt. Lane: CONTLEARN (CLH2). Date: 2026-10-02.
Role: adversarial review of the lane's own design, oracles, and
interpretation. Nothing here weakens a frozen bar; findings are
reported, not patched.

## R1. Is the reuse learner-driven or scaffold-cued?

Attack: the driver teaches the rebind anchors (T_i->A_i, U_i->S_i) 12
events before the rebind queries. The anchors are researcher-supplied
structure placed exactly where the machinery needs it. Is the "rebind"
just the machinery walking a researcher-laid path?

Response, kept honest: the anchor is the new problem's premise, not an
answer leak. It names the entry node (A_i / S_i), never the answer
(B_i / A_i), and the relation used at query time (863/866) is novel.
The learner-side work the test measures is all post-anchor and all
frozen-machinery: 2-hop chain discovery through facts that are 148
events old and never re-taught, verification, MAP promotion, and DEP
citation binding old structure into the new solution. No per-query
researcher signal exists beyond the fixed kind-1/2/3 protocol
(expected=-2, flags=1; the supervisor is disconnected). The NOPHASE
control isolates the cue question causally: identical anchors,
identical interference, identical queries, no phase-A structure gives
answers of 1, not the chain answers. If the anchors alone cued the
answers, NOPHASE would produce them. It does not.

Residual: the anchor placement (mid-chain vs root) is researcher-chosen,
so the ENTRY POINT is cued even though the answer is not. A stronger
future design would have the learner select its own entry point into
old structure. Not claimed here.

## R2. Knowledge vs architecture: could the machinery answer without the structure?

Attack: maybe B_i/A_i are machinery defaults reachable without phase-A
facts (e.g., via bootstrap or the count branch).

Killed by CP-R5: the NOPHASE binary (same treat core, same
interference, same anchors and queries, phase A elided) returns 1 on all
12 rebind queries, exactly the frozen count-branch prediction, and the
phase-A facts are verified absent. The TREAT answers therefore require
the phase-A structure in learner state. Additionally REBIND_OK pins
provenance, not just answers: each new MAP must DEP-cite the phase-A
chain fact (tail: fact(96101+i,851,96201+i); head: fact(96001+i,850,
96101+i)). A correct answer via any other route would fail the oracle.

## R3. Are the oracles tautological (metric gaming)?

Attack: the expected answers are exactly what the frozen chain
semantics produce by construction, so 12/12 was never at risk.

Assessment: the value predictions were derived from the frozen source
before implementation (prereg section 3b/3c), not tuned after results,
which is the correct preregistration posture; but the red team rates
the INFORMATION VALUE honestly. What was genuinely at stake: (a)
whether the phase-A structures survive 118 unrelated interference
events structurally intact (the LH lane proved this machinery CAN lose
composed answers under conflict; survival was not axiomatic); (b)
whether chain discovery re-traverses 148-event-old facts through new
anchors (reachability through a changed arena); (c) whether the DEP
provenance binds old facts into new MAPs. All three held. What was NOT
at stake: the machinery's chain semantics themselves (frozen and
previously characterized). Verdict: a demonstration with a reusable
discriminator protocol (NOPHASE), not a discovery. Consistent with the
binding no-generality caveat.

## R4. Head-family value is allocation-order-determined

Attack: for the head family, two valid 2-hop compositions exist
([U,S,A]->A_i via the 850 fact, [U,S,B]->B_i via the promoted 852
fact). The machinery tries paths in node-id order, so the 850 fact
(allocated earlier) wins and the answer is A_i. The "rebind" value is
therefore decided by allocation order, a machinery property, not by
anything cognitive.

Upheld as a LIMITATION, disclosed: the prereg derived this prediction
explicitly (section 3c) and the oracle additionally requires the DEP
citation to the 850 head fact, which pins WHICH composition was used
(6/6). The head result is consistent with rebind-through-old-structure,
but the value selection among two valid compositions is
order-determined. The tail family has no such ambiguity (unique path
through A_i). The rebind claim is correspondingly stronger for the tail
family; the verdict carries this note.

## R5. One learner, no reset: is 9 processes "one continuing learner"?

The lane semantics (inherited from CONTLEARN3/CONTLEARN-LH): "one
learner" means one process, one arena, no reset WITHIN a run. All 166
(resp. 142) events in a run share one tnn2_init arena; no re-init, no
recompile, no task label occurs mid-run. Across reps/binaries the
learners are independent, which is the determinism design, not a reset.
Holds.

## R6. What does the proposal gate contribute? (CP-R7 reading)

CONTROL reproduces TREAT exactly on every rebind bar (CP-R7 PASS, no
anomaly). The rebind capability is therefore frozen-core behavior; the
proposal gate contributes ordering provenance (CP-R0: 24/24 proposals
before machinery, 12/12 rebind pairs ordered with matching prop ids,
12/12 proposal citations on rebind MAPs) but not the rebind itself.
This is reported plainly, not as a defect: the lane's continuing
learner under test is the frozen TNN-2 core; the proposal-first
instrument is a measurement overlay whose ordering guarantee held while
preserving rebind. It also bounds the instrument's causal claims.

## R7. Refusal branch still unexercised

0 MACHINERY_SKIPPED on all TREAT reps. The gate's refusal path is
structurally enforced (pf_mp_run returns -2 with no live proposal) but
empirically untested for the third consecutive lane experiment. The
binding caveat from CONTLEARN3 stands unchanged. The queued adversarial
exercise (delete a proposal mid-run, attempt engagement) remains open
and is re-queued.

## R8. Interference realism

INT1's 96 facts are disconnected from the chains: the pressure is
volumetric (arena occupancy: 426 nodes / 421 edges at REBIND vs caps
1024/4096), not semantic. INT2's conflict is deliberately on unrelated
facts (scoping decision per the CONTLEARN-LH lesson: conflict on
licensing facts has known single-propagation semantics and would make
the oracle indefensible). INT3 is a same-shape second family. The delay
is 118 events between capability and rebind (longer than CONTLEARN3's
24-event gap, shorter than LH's 276). The rebind problems are new in
surface (subjects, relations, entry points) but same in structural kind
(2-hop chains). No cross-kind transfer is claimed or tested.

## R9. AGENTS.md toolchain update (2026-10-02, SA1 lane)

During this lane, AGENTS.md gained three znc lessons (a second
name/layout-dependent miscompile in print helpers using _zag_print; as
[]f64 len semantics; WAV 2-byte reads). Assessed for this lane: NOT
APPLICABLE. Both drivers use only the frozen core's own emit/e64 for
output (no new print helpers, no _zag_print calls, no f64 casts, no
WAV). Stdout trust was established independently: 3x byte-identical
transcripts per binary, oracle lines and answers verified by content.
No driver change needed.

## R10. What would have falsified the claim

REBIND_OK < 12/12; SURVIVE_OK < 6/6; NOPHASE answers equal to the chain
answers (machinery default without structure); rebind MAPs citing only
anchor facts without phase-A citations; capacity guard trip; any K-bar
failure. None occurred. The decision rule's REBIND-FAIL,
STRUCTURE-LOST, and DISCRIMINATOR-FAIL branches were live and did not
trigger.

## Summary

No killing evidence found. Two limitations carried into the verdict:
(R4) head-family value selection is allocation-order-determined among
two valid compositions; (R6) the rebind capability is frozen-core
behavior reproduced by CONTROL, with the proposal gate contributing
ordering provenance only. Binding caveats from CONTLEARN3 all stand
(Section 1 of the verdict).
