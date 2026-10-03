# FROZEN PREREG: H5R3, the revision chain through full revert cycles

Lane: HPI, wave-20261002-0521pdt. Status: FROZEN PREREG.

Lineage: H5 (wave-20261001-2021pdt, lane TNN3H5) was KILLED by red-team
dissent dbf25e447 (shadow fact on the MAP key; MAP supersession
behaviorally inert). H5R (same wave, lane TNN3H5R, Option A substrate:
shadow-fact teaching deleted, activate admits tag-20 MAPs) was KILLED
on KB-W2R 8/12 (SEALED_EVAL_H5R.md): on the 4 revert probes the
post-revert fresh MAP carried DEP edges to the SUPERSEDED original
fact instead of the live reverted fact, breaking the DEP based
revision chain. Root cause, white-box traced: t2_trial accepted the
first candidate whose executed output matched the expected value, in
BFS/node-id order, with no check that the candidate's licensing facts
were still live; on a revert the candidate via the superseded original
fact verified first. H5R2 (wave-20261001-2321pdt, fresh prereg, the
trial-loop stale-provenance fix: the t2_prov_ok gate, "a superseded
fact licenses nothing") ADVANCED (BUILD-PASS): KB-W2R 12/12, KB-W3 8/8,
KB-B2R 24/24, KB-B3 24/24. H5R2-SYNTH (wave-20261002-0221pdt) tested a
newest-live-among-all-live gate and BUILD-FAILed with the
pre-registered newest-bias signature; no tie-breaking rule is crowned
and none is repeated here.

The remaining gap, stated honestly in H5R2's sealed eval: H5R2's
worlds tested the revert step (contradict, then revert) and checked
the final anchor, but they never contradicted the reverted fact again.
H5R's sealed eval identified the exact consequence of stale anchoring:
revise_on_contradict locates stale MAPs via DEP edges to the
contradicted fact, so a MAP that does not anchor to its live licensing
fact cannot be reached by a future contradiction of that fact, and the
MAP keeps answering via the MAP read path. H5R2 repaired the anchor;
whether the chain actually fires through it (the revert MAP gets
superseded when its live licensing fact is contradicted, and
re-derivation lands on the next live fact) is untested. That is this
prereg's question. Per VOID discipline this is a fresh prereg with
fresh sealed worlds; nothing from the killed or passed batteries'
worlds, keys, values, or ranges is reused.

ORDERING RULE: this prereg is committed alone (after NAMECHECK.md, a
process record, not implementation) before any implementation artifact
is written. Any implementation artifact whose mtime predates the prereg
freeze commit is UNVERIFIABLE ORDERING and the evaluation is VOID. Kill
bars never move after freezing. Correction after a kill proceeds only
as a fresh prereg plus fresh sealed worlds, never amend-and-promote.

## 1. Hypothesis under test

The H5R2 provenance gate sustains the revision chain through FULL
revert cycles. Concretely: after a revert promotes a fresh MAP
anchored to the live reverted fact, a subsequent contradiction of that
reverted fact still supersedes the revert MAP via its DEP edges, and
the next MAP-key query re-derives through the trial loop and promotes
a fresh MAP anchored to the new live fact. Provenance is carried
forward not just at the revert step but through every subsequent
revision: the revision chain stays anchored to live facts through
revert.

Falsifiable prediction: on every cycle and revert-after-revert probe,
the final white-box dump shows the full supersession history (every
MAP superseded at its step carries a CON self-edge), exactly one live
MAP, and every DEP edge of the live MAP targets a live tag-1
non-superseded fact. Behaviorally, the post-re-revision probe returns
the newest value via a fresh MAP. If any live MAP carries a DEP edge
to a superseded fact, or a revert MAP survives the contradiction of
its live licensing fact, H5R3 is dead: the chain breaks at the revert
step and the H5R2 gate repairs anchoring without sustaining revision.

## 2. Pinned substrate (Option A, carried forward byte-identical)

Option A in this prereg means the H5R2 trial-loop stale-provenance
fix, carried forward with zero source change: the substrate is the
frozen H5R2 source
docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3H5R/tnn3_h5r2.zag at commit
9db334bd4a01d21cce52da3bb2a1c45a10c4c172, SHA-256
04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a.
This includes the H5R hunks (activate tag-20 admission on (f8,f4);
promote_graph shadow-fact teaching deleted) and the t2_prov_ok gate at
all four t2_trial promote sites. No new cognition code is written for
H5R3; the hypothesis under test is a property of this frozen
substrate. The frozen binary reference is SHA-256
19dcf2e4436079a4ab6f9cf48b2b6a556f743d3d9d16102249cd5ac970287
(rebuilt with the pinned znc; must match byte for byte). KB-S1 gates
the sealed run on byte-identity: extracted source SHA-256 must equal
the frozen record, and the diff against the verified H5R base
(tnn3_h5r.zag at commit 830f95ab7, SHA-256
d98d08f0746cab4fef88fb062933a314c12492f78ee98b496e8d8912cd7fd384)
must contain exactly the H5R activate hunk, the promote_graph
deletion hunk, and the t2_prov_ok gate at all four sites, with zero
added or removed cognition lines.

No-regression is inherited by byte-identity: the substrate is the same
bytes that passed H5R2's battery, and KB-D3 determinism holds, so
re-running H5R2's C/W3 worlds would reproduce their transcripts
exactly and adds no information. The CY battery below tests only the
unexamined full-cycle behavior.

## 3. Key convention (pinned)

MAP keys (s_m, r_m) are the exact (subject, relation) pairs passed as
(s,r) to promote_graph at promotion time. Fact keys (s_f, r_f) are the
keys of licensing facts. Contradiction OBSERVE events arrive on fact
keys only. No behavioral bar probes a fact key for a MAP claim. Sealed
worlds use fresh key, relation, and value ranges (95xxx-98xxx)
disjoint from FW1-FW9, the 1421pdt battery, the killed H5 battery
(51xxx-54xxx), the killed H5R battery (61xxx-65xxx, 71xxx-72xxx), the
H5R2 battery (83xxx-86xxx), the decoy families (87xxx-90xxx), the
separator family (91xxx-92xxx), the DT family (93xxx-94xxx), and all
smoke keys (9xxx). Per-probe key ranges are disjoint within a world.

## 4. Sealed world specification (frozen before implementation)

4.1. Seeds (chosen pre-freeze; inputs hashed with safebin sha256sum):
- y1: "TNN3H5R3|wave-20261002-0521pdt|world-y1" ->
  b303b30cbc6109141d3560b4797517fa63b83f8b91e9dc5e5874a740fa4de0b6,
  first byte 0xb3 = 179, vo1 = 179 mod 7 = 4.
- y2: "TNN3H5R3|wave-20261002-0521pdt|world-y2" ->
  bf14edcd3f5707352e1b400ed80d1bec5472e3b5b7a06cc2e7769e17aa786813,
  first byte 0xbf = 191, vo2 = 191 mod 7 = 2.

4.2. Key and value layout (frozen):
- w_y1: RF1=9501, RF2=9502, RM=9503. Cycle probes on subjects
  95101, 95102, 95103; revert-after-revert probe on subject 95104.
  Value base 95301; probe i (0..3): c0 = 95301 + vo1 + 10*i,
  c1 = c0+1, c2 = c0+2. (Probe 0: 95305/95306/95307; probe 1:
  95315/95316/95317; probe 2: 95325/95326/95327; probe 3:
  95335/95336/95337.)
- w_y2: RF1=9601, RF2=9602, RM=9603. Cycle probes on subjects
  96101, 96102, 96103; revert-after-revert probe on subject 96104.
  Value base 96301; probe i (0..3): c0 = 96301 + vo2 + 10*i,
  c1 = c0+1, c2 = c0+2. (Probe 0: 96303/96304/96305; probe 1:
  96313/96314/96315; probe 2: 96323/96324/96325; probe 3:
  96333/96334/96335.)
The two worlds differ materially in relation family and subject
distribution. Concrete values are fixed above; the driver uses them
verbatim.

4.3. Cycle probe pattern (3 per world, 6 total). Chain a-RF1->b,
b-RF2->c0; MAP on (a, RM):
1. ev_teach(a,RF1,b); ev_teach(b,RF2,c0). Teaches chain fact and F0.
2. QUERY a RM c0 (promote M0; DEP edges to F0 and the chain fact).
3. OBSERVE b RF2 c1. F0 superseded; revise_on_contradict supersedes
   M0 (CON self-edge); F1 (c1) taught.
4. QUERY a RM c1. Expect c1 via a fresh MAP M1 (DEP to F1).
5. OBSERVE b RF2 c0 (revert). F1 superseded; M1 superseded (CON);
   F3 (c0) taught.
6. QUERY a RM c0. Expect c0 via a fresh MAP M3; the gate must decline
   the candidate via the superseded F0 (lowest node id, value c0
   verifies). DEP edges to F3.
7. OBSERVE b RF2 c2 (contradict the reverted fact). F3 superseded;
   revise_on_contradict must supersede M3 (CON self-edge); F4 (c2)
   taught.
8. QUERY a RM c2. Expect c2 via a fresh MAP M4 (DEP to F4).

4.4. Revert-after-revert probe pattern (1 per world, 2 total). Chain
a-RF1->b, b-RF2->c0; MAP on (a, RM):
1. ev_teach(a,RF1,b); ev_teach(b,RF2,c0).
2. QUERY a RM c0 (promote M0; DEP to F0).
3. OBSERVE b RF2 c1. F0 superseded; M0 superseded (CON); F1 (c1).
4. QUERY a RM c1. Expect c1 via fresh M1 (DEP to F1).
5. OBSERVE b RF2 c0 (revert). F1 superseded; M1 superseded (CON);
   F3 (c0).
6. QUERY a RM c0. Expect c0 via fresh M3 (gate declines F0's
   candidate; DEP to F3).
7. OBSERVE b RF2 c1 (revert-after-revert). F3 superseded; M3
   superseded (CON); F5 (c1).
8. QUERY a RM c1. Expect c1 via a fresh MAP M5. The gate must decline
   the candidate via the superseded F1 (lowest node id among c1
   facts; its executed output c1 verifies, the exact H5R killing
   configuration in a new structural position). DEP edges to F5.

This probe is the sharpest discriminator in the battery: without the
provenance gate, step 8 anchors the fresh MAP to the dead F1, the
exact stale-anchoring failure that killed H5R.

4.5. World-design constraints (frozen): no OBSERVE on any MAP key in
any world; a white-box snapshot is taken before every MAP-key probe
(16 per world, 32 total); per-probe key ranges disjoint within a
world; all keys, relations, and values absent from every range listed
in section 3.

4.6. Marker contract (frozen; the post-freeze driver CY_FRAG.zag
implements it verbatim; its SHA-256 is recorded before any run):
- SNAP-IN line before every MAP-key probe: probe id, t1live (count of
  live tag-1 facts with (f20,f24)==(s_m,r_m)), livemap (1 iff exactly
  one live tag-20 MAP with (f8,f4)==(s_m,r_m)), f28 of that MAP, and
  the returned value.
- Per QUERY: a Q line with probe id, expected value, returned value,
  and answering node id; a FRESH line confirming the answering node id
  is strictly greater than every earlier promoted MAP id on the key
  in that probe.
- Final dump per probe: per tag-20 MAP node on (s_m,r_m): node id,
  f28, CON self-edge present (1/0), live (1/0); per DEP (type-1) edge
  of the live MAP: target node id, target tag, target superseded bit.
- Zero unexpected FAIL marker lines.

4.7. Assembly rule (frozen): each sealed world file is a byte-copy of
the committed substrate tnn3_h5r3.zag with exactly one line changed
(`fn main()i32 { return run_all(); }` to
`fn main()i32 { return sealed_main(); }`, verified by diff: exactly
one line differs in the substrate portion) plus the frozen CY_FRAG.zag
appended plus one alias line selecting the world
(`fn sealed_main()i32 { return sealed_main_y1(); }`, etc.). Assembly
happens only after the implementation commit; the world file SHA-256s
are recorded before any run.

4.8. Seal-integrity disclosure (frozen): this wave has a single worker
acting as coordinator, builder, and evaluator (no separate adversary
lane was assigned), following the H5R2 2321pdt mitigations: the seeds,
key ranges, value offsets, event patterns, and marker contract are
frozen in this prereg before implementation; the driver hash binds the
worlds; world assembly is mechanical from the driver; the builder's
smoke tests use unsealed keys (9xxx) disjoint from all sealed ranges;
the evaluator attests no world output was used to tune the substrate.
The worlds are fresh (new seeds, new ranges, new cycle family), never
salvaged from a killed or passed battery.

## 5. Frozen kill bars (exact numbers)

KB-W0 (white-box, PRIMARY, the original-sin confrontation): across
all 32 MAP-key probe snapshots (16 in w_y1, 16 in w_y2), the count of
live tag-1 facts with (f20,f24)==(s_m,r_m) is 0, and each probe's
returned value equals the f28 of the single live tag-20 MAP with
(f8,f4)==(s_m,r_m). PASS: 32/32. Any nonzero shadow count, or any
probe answered from a tag-1 node, KILLS H5R3.

KB-S1 (substrate gate, pre-run): the extracted substrate source
SHA-256 equals
04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a;
the committed diff against the verified H5R base contains the activate
tag-20 admission hunk, the promote_graph ev_teach_in deletion hunk,
and the t2_prov_ok gate at all four t2_trial promote sites; zero added
and zero removed cognition lines versus the frozen H5R2 source.
Absent any of these, the sealed run does not proceed; H5R3 is VOID
for substrate non-compliance (NC-0R3).

KB-CY (white-box cycle, the core new bar): on each of the 6 cycle
probes, the final dump shows exactly 3 superseded tag-20 MAPs with
(f8,f4)==(s_m,r_m) carrying CON self-edges, exactly 1 live tag-20 MAP
with f28 equal to c2, and every DEP (type-1) edge of the live MAP
targets a live tag-1 non-superseded fact. PASS: 6/6. Any DEP edge to
a superseded fact KILLS H5R3 (the exact H5R killing failure mode). A
revert MAP still live after its licensing fact was contradicted KILLS
H5R3 (the chain broke at the revert step).

KB-RR (white-box revert-after-revert): on each of the 2
revert-after-revert probes, the final dump shows exactly 3 superseded
tag-20 MAPs with (f8,f4)==(s_m,r_m) carrying CON self-edges, exactly
1 live tag-20 MAP with f28 equal to c1, and every DEP edge of the live
MAP targets a live tag-1 non-superseded fact (in particular the c1
re-reverted fact, not the superseded F1). PASS: 2/2. Any DEP edge to
a superseded fact KILLS H5R3.

KB-BCY (behavioral cycle): on each of the 6 cycle probes, the
post-first-contradiction probe returns c1, the post-revert probe
returns c0, and the post-re-revision probe returns c2, each via a
fresh MAP (strictly increasing node ids on the key). PASS: 18/18.

KB-BRR (behavioral revert-after-revert): on each of the 2 probes, the
post-contradiction probe returns c1, the post-revert probe returns
c0, and the post-re-revert probe returns c1, each via a fresh MAP
(strictly increasing node ids). PASS: 6/6.

KB-G3 (architecture accounting): the substrate source is byte-identical
to the frozen H5R2 record (0 added, 0 removed cognition lines); no new
modes, bridges, routers, or handlers; no core-ISA additions; none of
the forbidden protected semantic operations
(FIND_POLYNOMIAL_ORDER, DETECT_NEGATION, BUILD_CAUSAL_RULE,
LEARN_PROCEDURE, FIND_THRESHOLD, MAKE_CONDITIONAL, or benchmark or
domain equivalents); no time, clock, or random reads in any new code.
The driver is evaluation scaffolding, not cognition. Any violation
KILLS regardless of behavior.

KB-D3 (determinism): 3/3 byte-identical full-stdout runs per sealed
world (w_y1, w_y2), SHA-256 compared. Any byte difference KILLS.

KB-P3 (process): zero forbidden-executable invocations during
construction and evaluation; safebin PATH; `which python3` empty at
lane startup; the toolchain guard recorded in NAMECHECK.md Step 0.
Any violation is PROCESS-FAIL, terminal.

Supplementary (logged, not kill bars): at each final dump, zero CON
self-edges on MAPs of probes not under contradiction (selectivity
check); the counts are reported for the record.

## 6. Negative controls (what KILLS or VOIDS H5R3)

NC-0R3: KB-S1 absent (source hash mismatch, or any of the three
substrate hunks missing from the diff, or any cognition-line delta).
The preregistered substrate was not built. Battery does not run. H5R3
VOID, untested.

NC-1R3: zero MAP-CON edges across the CY battery. The transition never
fires on MAPs. H5R3 dead per its falsifiable prediction. KILL.

NC-2R3: any behavioral bar passes while KB-W0 fails (a tag-1 node
answers a MAP-key probe, or a live tag-1 fact sits on the MAP key).
Causal attribution is broken. KILL.

NC-3R3: a MAP carries a CON self-edge but a later MAP-key probe returns
the stale value with no fresh MAP promotion (no new tag-20 node on the
key). The supersession is cosmetic. KILL.

NC-4R3 (the full-cycle chain control, NEW): after contradicting the
reverted fact, the revert MAP remains live (no CON self-edge), or the
post-re-revision probe returns the stale reverted value. The revision
chain broke at the revert step: the gate repaired anchoring without
sustaining revision. This is the exact consequence H5R's sealed eval
identified. KILL.

NC-5R3: net nonzero cognition-line delta versus the frozen H5R2
source, or any new mode, bridge, router, or handler, or any core-ISA
addition, or any forbidden protected semantic operation. Governance
KILL regardless of behavior.

NC-6R3: any byte difference across the 3/3 reruns. Determinism KILL.

NC-7R3: any forbidden-executable invocation during construction or
evaluation. PROCESS-FAIL, terminal.

NC-8R3: the evaluator judges a world a trivial variant of FW1-FW9,
the 1421pdt battery, the killed H5 or H5R batteries, or the H5R2
battery. That world is VOID; if fewer than 2 valid worlds remain in
the CY family, the battery is VOID and H5R3 is untested.

## 7. Verdict rules (three-valued)

H5R3 ADVANCES iff ALL frozen bars in section 5 pass, no killing
negative control fires, and no void condition fires.

H5R3 is KILLED iff any frozen bar fails (KB-S1 excepted, see below) or
any killing negative control (NC-1R3 through NC-7R3) fires. Terminal
for this wave: no re-tune, no amend-and-promote. A killed H5R3 may
return only via a fresh prereg plus fresh sealed worlds.

H5R3 is VOID (untested, not passed) iff a battery-level void condition
fires (NC-0R3, NC-8R3 shortfall, ordering violation). The hypothesis
was not tested; no advance and no kill are recorded. Substrate
non-compliance (NC-0R3) is VOID rather than KILL because the
preregistered mechanism was not built.

## 8. Pre-registered expectations (not kill bars; recorded for honesty)

The H5R2 substrate already passed the revert step on structurally
identical machinery, and the full-cycle steps use the same
revise_on_contradict path that H5R and H5R2 exercised. Expected: all
bars PASS, NC-4R3 does not fire. An honest KILL via NC-4R3 would be
informative negative evidence: it would show the provenance gate
repairs anchoring without sustaining the revision chain through
revert, falsifying the hypothesis in section 1 while leaving H5R2's
BUILD-PASS intact within its tested scope.

## 9. Pre-registered red-team self-attack

Attack 1 (indiscriminate supersession): the full-cycle white-box bars
could pass trivially if revise_on_contradict superseded every MAP on
any contradiction instead of only DEP-linked ones; then NC-4R3 would
pass without the DEP chain doing any work. Answer: the bars require
DEP edges to land on the correct live facts (KB-CY, KB-RR), and the
supplementary selectivity check logs zero CON edges on MAPs of probes
not under contradiction; indiscriminate supersession would leave
wrong DEP targets or stray CON edges.

Attack 2 (dead-candidate starvation): the gate could make the trial
loop miss when only dead candidates verify, returning miss (-2)
instead of re-deriving. Answer: the worlds always teach a live fact
for the expected value (the H5R2 4.6 pinned consequence is carried),
and KB-BCY/KB-BRR require exact values, so starvation fails loudly
rather than silently.

Attack 3 (fresh-key luck): the cycle worlds might pass merely because
dead facts sit at low node ids that enumeration never reaches first.
Answer: the revert-after-revert probe is constructed so the dead
candidate (F1, the lowest node-id c1 fact) verifies before the live
one in enumeration order; without the gate, H5R's exact killing
failure recurs there. The discrimination is structural, not luck.

If the experiment contradicts these attacks, the bars decide, not the
predictions: report honestly.

## 10. Scope boundary (explicit)

This lane does not re-litigate H5R2's BUILD-PASS: that verdict stands
within its frozen battery scope. This lane makes no broad generality
claim and no L3 claim. The verdict reports only whether the DEP based
revision chain holds through full revert cycles on the two tested
worlds. The re-teach separator family remains an explicit open gap in
H5R2's scope, named as such, not a retroactive bar move. No verdict
here crowns any tie-breaking rule as the correct provenance policy in
general.

## 11. Pure-Zag construction

Builder PATH is $HOME/safebin (36 tools, no python3, verified at lane
startup and recorded in NAMECHECK.md Step 0). All research logic
(implementation, verifiers, scorers, harnesses, world drivers,
white-box dump and analysis programs) is written in Zag and
compiled/run with the pinned znc
(src/tools/toolchain/znc_linux_x86_64_abed8aa1). Shell is used only to
invoke znc, run binaries, do git ops, and move/copy files. Any
forbidden executable invocation is automatic PROCESS-FAIL.

## 12. Implementation plan (queued next wave; frozen here)

1. Extract tnn3_h5r2.zag via git show from commit
   9db334bd4a01d21cce52da3bb2a1c45a10c4c172; verify SHA-256 equals
   04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a
   before any use. Do not rebuild from working files.
2. KB-S1 pre-check on the committed file: the three hunks present at
   the recorded locations, zero cognition-line delta versus the
   frozen H5R2 source.
3. Rebuild with the pinned znc (3/3 byte-identical builds); the binary
   SHA-256 must equal
   19dcf2e4436079a4ab6f9cf48b2b6a556f743d3d9d16102249cd5ac970287.
4. Write CY_FRAG.zag post-freeze to the section 4.6 marker contract
   (probe functions, sealed_main_y1/sealed_main_y2, SNAP-IN lines,
   final dumps); record its SHA-256 before any run.
5. Smoke test on unsealed keys (9xxx) only, 3/3 determinism
   self-check.
6. Assemble w_y1/w_y2 per section 4.7; record world file SHA-256s
   before any run; run each 3/3; compare full-stdout SHA-256 (KB-D3).
7. Score the section 5 bars from the drivers' own markers; apply the
   section 6 negative controls; write SEALED_EVAL.md with frozen
   numbers and the verdict line; write REDTEAM_SELF.md.
8. Commit locally, pathspec-only: implementation, SEALED_EVAL.md,
   REDTEAM_SELF.md. Never push.

No em-dashes or en-dashes in this document (checked with
check_no_dash.sh before commit).
