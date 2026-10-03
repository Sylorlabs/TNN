# REPORT: H3-INCORPORATED (reasons + importance source)

Date: 2026-10-03. Worker: H3-INCORPORATED worker (non-ledger task;
claim minting paused).
Prereg: committed alone as 732b89982 (strictly before implementation,
build, and runs).

## Verdict: 9/9 kill bars hold (R1..R9)

3/3 runs byte-identical (sha256
0ea657f0e0caaf12b0f32a3bc38b41a937a25d2b6018de8dab61671073d12d76).
Binary sha256
3bc869d52a8a524166c319e7a724956e3bdc7e6768e16c584c4032b31e822b9f.

This lane closes the last open item from the H3 arc named in
H3-SEALED-B's follow-ups: "INCORPORATED/SUPERSEDED reasons and the
successful-episode importance source." It is a hybrid lane: a focused
Zag experiment (TESTED, R1..R9) plus reasoned analysis. The two are
separated explicitly below; nothing reasoned is presented as tested.

## Results (identical across run1/run2/run3)

| cond              | cf | ev | drop | rel | av | ai | ar | lc | haz | trs      |
|-------------------|----|----|------|-----|----|----|----|----|-----|----------|
| RSN-REVISED       | 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 0   | 11111111 |
| RSN-SUPERSEDED    | 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 0   | 33333333 |
| RSN-INCORPORATED  | 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 0   | 22222222 |
| RSN-MIXED         | 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 0   | 11122233 |
| RSN-INCREF        | 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 8   | 22222222 |
| RSN-INCREF-GUARD  | 8  | 0  | 0    | 0   | 0  | 0  | 0  | 12 | 0   | -        |
| RSN-REVGUARD      | 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 0   | 11111111 |

IMP-LEARN order=102 103 104 101; IMP-TOUCH order=103 104 101 102.

Kill bars (in-band + external, all 3 runs):
- R1 REASON-AGNOSTIC-SUP: HOLD (RSN-SUPERSEDED bit-identical to
  RSN-REVISED in all 9 numeric columns; trs=33333333).
- R2 REASON-AGNOSTIC-INC: HOLD (RSN-INCORPORATED bit-identical to
  RSN-REVISED; trs=22222222).
- R3 MIXED-TRACE: HOLD (releases=8, av=8, ai=0, hazard=0,
  trs=11122233).
- R4 INCORPORATED-HAZARD: HOLD (RSN-INCREF under the current gate:
  releases=8, av=8, hazard=8).
- R5 GUARD-BLOCKS: HOLD (RSN-INCREF-GUARD: releases=0, hazard=0,
  av=0, ai=0, lc=12, cf=8).
- R6 GUARD-REASON-SPECIFIC: HOLD (RSN-REVGUARD: releases=8,
  hazard=0, av=8).
- R7 IMPORTANCE-SOURCE: HOLD (IMP-LEARN exactly 102 103 104 101;
  IMP-TOUCH exactly 103 104 101 102).
- R8 DETERMINISM: HOLD (3/3 byte-identical).
- R9 CLEAN: HOLD (ai=0, ar=0, lc=12, av==releases in all 7 rows).

Every measured row matches the frozen prereg predictions exactly,
including the trace-reason strings and both importance orders.

## What was TESTED (R1..R9)

1. The H3 release gate is reason-agnostic. With reason codes carried
   in the revision log (16-byte entries: key, old, new, reason) and
   passed verbatim into the release trace, SUPERSEDED (R1) and
   INCORPORATED (R2) entries release through the identical path as
   REVISED: bit-identical rows in all 9 numeric columns, audit 8/0,
   learner intact. Mixed reasons (R3) release 8/8 with the trace
   recording each entry's reason verbatim (11122233). The mechanism
   cannot and does not discriminate on reason: the release authority
   is the learner's log membership + old_value match +
   belief-changed check, exactly as H3/H3B/H3-SEALED proved.
2. The INCORPORATED reference hazard is real under the current gate.
   When the absorbing composite references the absorbed pooled entry
   (harness reference pattern: 900000<=value<910000,
   value-900000==key), the current gate releases all 8 absorbed
   entries anyway (R4: releases=8, hazard=8, audit still 8/0: the
   audit verifies the revision, not the reference graph). Release
   here would hand the absorbing structure a dangling reference:
   silent knowledge corruption, not capacity loss.
3. The guarded gate fixes it without over-blocking. Adding the
   no-live-reference precondition for reason==2 only: 0 releases,
   0 hazard, learner intact (R5). Applied to REVISED entries with
   unrelated references present, the same guard releases all 8
   (R6): the precondition is reason-specific and does not change
   REVISED/SUPERSEDED behavior.
4. The two importance sources order oppositely. Given a successful
   episode where belief A (key 101) participated causally and entry B
   (key 102) was incidentally touched 10x (the H1 IMPADV inflation
   pattern), learner-attributed importance (A=10,B=1,C=1,D=1) evicts
   102,103,104 before 101 (A survives longest), while
   mechanism-observed touch-during-success (A=1,B=10,C=0,D=0) evicts
   103,104,101 before 102 (the causal belief dies before the
   incidental entry) (R7).

## What is REASONED (not tested; analysis for the parent)

### (a) What distinguishes INCORPORATED from SUPERSEDED

- SUPERSEDED: belief B_old replaced by B_new, where B_new is strictly
  better (more accurate, more general, subsuming B_old's role). The
  old content is dead: after the revision, no live learner structure's
  correctness depends on B_old's specific content. The revision is a
  substitution.
- INCORPORATED: belief B_old absorbed into a larger structure S (a
  composite, a generalization) that contains B_old's content as a
  copy, a special case, or a derived consequence. The old content is
  alive inside S: S's correctness depends on it. The revision is an
  absorption, not a substitution.

The distinguishing test is learner-internal and counterfactual:
after the revision, does any live structure's correctness still
depend on the old content? For SUPERSEDED the answer is no; for
INCORPORATED it is yes by definition. The two reasons therefore make
different predictions about the reference graph, which is why they
are not interchangeable metadata.

### (b) Does the distinction matter for the unpin decision?

At the mechanism's release gate: no, and it should not. R1/R2 prove
the gate reason-agnostic; making the mechanism discriminate on reason
would install a mechanism-level semantic judgment about the
learner's revision kinds, which is exactly the researcher/observer
semantics the H3 architecture relocates into the learner. The gate's
job is to verify that the learner revised (authority), not to
second-guess what kind of revision it was.

At the learner's release judgment: yes, as a precondition, not as a
verdict. The recommendation, grounded in R4/R5/R6:

- REVISED and SUPERSEDED: release under the identical gate. Their
  old content is dead in both cases; the reason distinction is audit
  metadata (why the learner revised), not a gate input. Neither
  "both release" nor any split between them is indicated: R1 shows
  no behavioral difference to exploit.
- INCORPORATED: release iff the standard gate holds AND no live
  structure references the pooled entry. The absorption act itself
  creates the reference, so the learner knows it exists; releasing
  the pooled entry while the absorbing structure points at it is a
  self-contradiction within one cognitive act (R4 measures the price:
  hazard=8). The guard (R5) enforces the consistency; R6 shows it
  costs REVISED nothing.

So the answer to "both release? neither? only one?" is: neither
blanket rule. REVISED/SUPERSEDED release under one shared gate;
INCORPORATED releases conditionally. The distinction matters as a
release-safety precondition.

A composition note for the architecture: the no-live-reference
precondition is the H1 dependency-count signal (popcount of
referencing structures) repurposed as a release precondition rather
than an eviction ranking. H1's importance signal and H3's release
authority compose cleanly: the mechanism observes the reference
graph (as H1's policy 7 already does); the decision stays the
learner's (as H3 proved). No new mode, bridge, or subsystem is
required.

### (c) The successful-episode importance source

The reclamation synthesis named two importance sources: dependency
count (implemented as H1 policy 7) and "a learner-written importance
weight updated when the entry participates in a successful episode"
(never implemented). The parent's question: how does the learner know
which beliefs matter?

Specification (reasoned; the demo in R7 tests only the signal
semantics, not a learner's attribution machinery):

- The source is the learner's own episode ledger. For each cognitive
  episode the learner records the episode's goal/criterion, whether it
  succeeded, and which beliefs participated causally. On success it
  increments the importance weights of the causally-participating
  beliefs. The mechanism honors the weight as an opaque signal; it
  never manufactures it.
- It must be learner-attributed, not mechanism-observed, because the
  mechanism sees touches, not causal roles. "Participated in a
  successful episode" as observed from outside means "touched during
  an episode that succeeded", which conflates incidental contact with
  causal contribution. R7 measures the consequence: touch-observed
  importance ranks the incidentally-touched entry above the causal
  belief and evicts the causal belief first; learner-attributed
  importance protects it. The H1 adversarial controls already showed
  workload touch patterns inflate mechanism-observed signals; a
  touch-observed episode weight would be gameable the same way.
- How the learner knows which beliefs matter: it knows the episode's
  success criterion (its own goal), it knows which beliefs it applied
  toward that goal (its own reasoning trace), and it observes the
  outcome. All three are learner-internal facts, inaccessible to the
  mechanism from outside. This is the same relocation H3 proved for
  unpin: the judgment is the learner's cognitive act; the mechanism
  enforces the resulting signal.
- The two sources answer different questions and compose:
  dependency count asks "what references this?" (structural,
  mechanism-observable); episode-success weight asks "what has this
  done for me?" (experiential, learner-attributed). Neither subsumes
  the other.

Open (not tested): the credit-assignment problem (per-belief vs
per-structure attribution, weight decay, cross-episode
interference). The R7 demo used harness-simulated attribution; a
real learner's attribution machinery is future work, and any claim
about it would need its own preregistered lane.

## Honest caveats

- The learner is simulated throughout (as in all H3 lanes); the
  reason codes are harness-written. The tested claim is about the
  gate's behavior given reasons, not about a real learner producing
  them.
- The reference pattern (900000+k) is a harness convention modeling
  "the absorbing structure references the absorbed entry." A real
  substrate needs genuine reference tracking; this lane models the
  decision logic, not the tracking.
- The guarded consolidate is a proposed gate extension,
  demonstrated but NOT canonized: it modifies the release gate that
  H3-SEALED-B sealed. Adoption would require its own sealed lane;
  this report proposes, it does not promote.
- The importance demo is minimal (4 entries, simulated attribution);
  it discriminates the two signal semantics but does not implement
  learner credit assignment.
- No churn phase was run: downstream retention/capacity behavior of
  the release gate stands as proven in H3/H3B/H3-SEALED; this lane
  isolates the gate itself.
- Non-ledger task: no claims minted.

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which python`
return nothing under that PATH (verified 2026-10-03 before the prereg
commit); no forbidden executable invoked at any point (shell used
only for mkdir, file writes, znc invocation, binary execution,
sha256sum, grep, git ops). No PROCESS-FAIL condition triggered.
Pinned znc verified byte-identical to
src/tools/toolchain/znc_linux_x86_64_abed8aa1 before the prereg
commit (sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
Build ran in foreground (zagd unavailable warning only), first try,
no defect symptoms. New-code audit: no negated-conjunction while
conditions, no `as *i32` slice construction, no `[]u8 as *u8` casts,
if-nesting at most 3. Git writes via /usr/bin/git directly (safebin
git symlink EPERM lesson); explicit pathspecs; no git reset; local
only, never pushed.

## Commits

- 732b89982: frozen prereg (PREREG.md + NAMECHECK.md), alone,
  strictly before implementation, build, and runs.
- This commit: h3_incorporated.zag (implementation),
  h3_incorporated_bin (sha256
  3bc869d52a8a524166c319e7a724956e3bdc7e6768e16c584c4032b31e822b9f),
  build.err, run1/2/3.txt, run1/2/3.err, REPORT.md. Local only,
  never pushed.

## Follow-ups for the parent

- The H3 arc's last open item is now closed empirically at the gate
  level (R1..R6) and specified at the source level (R7 + analysis):
  (a) INCORPORATED vs SUPERSEDED differ in whether the old content
  stays live inside an absorbing structure; (b) the distinction does
  not belong in the mechanism's gate (reason-agnostic, proven) but
  does belong in the learner's release judgment as a
  no-live-reference precondition for INCORPORATED only; (c) the
  successful-episode importance source is learner-attributed episode
  credit, mechanism-honored, specified above.
- Proposed (not canonized): the guarded consolidate (reason-2
  no-live-reference precondition) as a candidate H3 gate refinement;
  needs its own sealed lane before any architectural adoption.
- The H1 dependency-count signal and the H3 release authority compose
  without new modes/bridges: reference observation is mechanism-side
  (already in policy 7), release decision is learner-side (H3).
- Open future work: real learner credit assignment for
  episode-success weights (per-belief vs per-structure, decay,
  interference); genuine reference tracking in the substrate.
