# FROZEN PREREG: H5R2, trial-loop provenance gate (stale-provenance fix)

Lane: TNN3H5R, wave-20261001-2321pdt. Status: FROZEN PREREG (fresh).

Lineage: H5 (wave-20261001-2021pdt, lane TNN3H5) was KILLED by red-team
dissent dbf25e447 (shadow fact on the MAP key; KB-B2 failure). H5R (same
wave, lane TNN3H5R, Option A substrate: shadow-fact teaching deleted,
activate admits tag-20 MAPs) was KILLED on KB-W2R 8/12
(SEALED_EVAL_H5R.md): KB-W0 36/36 PASS corrected the original sin, but
on the 4 revert probes the post-revert fresh MAP carried DEP edges to
the SUPERSEDED original fact node instead of the live reverted fact,
breaking the DEP-based revision chain. Root cause (white-box, traced in
the frozen trial loop): t2_trial accepts the first candidate whose
executed output matches the expected value, in BFS/node-id order, with
no check that the candidate's licensing facts are still live; on a
revert the candidate via the superseded original fact verifies first.
Per VOID discipline, this is a fresh prereg with fresh sealed worlds;
nothing from the killed batteries' worlds, keys, values, or ranges is
reused.

ORDERING RULE: this prereg is committed alone by the coordinator before
any implementation file is written. Any implementation artifact whose
mtime predates the prereg freeze commit is UNVERIFIABLE ORDERING and the
evaluation is VOID. Kill bars never move after freezing. Correction
after a kill proceeds only as a fresh prereg plus fresh sealed worlds,
never amend-and-promote.

## 1. Hypothesis under test (revised)

A superseded fact licenses nothing. The H5R substrate is kept byte-for-byte
except for one trial-loop provenance gate: t2_trial declines any
candidate whose licensing facts are not all live, tag-1, and
non-superseded, so promotion always anchors DEP edges to the current
(post-revision) fact lineage. Provenance is thereby carried forward
through each revision step: after a contradiction the dead fact can no
longer license a MAP, and a revert MAP lands on the live reverted fact.

Falsifiable prediction: on every revert and chained probe, the
post-revert fresh MAP must carry DEP (type-1) edges only to live,
non-superseded tag-1 facts. If any live MAP on a MAP key carries a DEP
edge to a superseded fact, H5R2 is dead: the stale-provenance flaw
survives and the revision chain is broken.

## 2. Key convention (pinned)

MAP keys (s_m, r_m) are the exact (subject, relation) pairs passed as
(s,r) to promote_graph at promotion time. Fact keys (s_f, r_f) are the
keys of licensing facts. Contradiction OBSERVE events arrive on fact
keys only. No behavioral bar probes a fact key for a MAP claim. Sealed
worlds use fresh key, relation, and value ranges (83xxx-86xxx) disjoint
from FW1-FW9, the 1421pdt battery, the killed H5 battery, the killed
H5R battery, and all smoke keys. Per-probe key ranges are disjoint
within a world.

## 3. Files

- Substrate base (read-only reference for the diff): the committed H5R
  working file
  docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5R/tnn3_h5r.zag at commit
  830f95ab7, SHA-256
  d98d08f0746cab4fef88fb062933a314c12492f78ee98b496e8d8912cd7fd384
  (the file that built the verified H5R binary, per SEALED_H5R.md).
- Working file (created at implementation time by byte-copy of the base,
  copy verified by SHA-256 before any edit):
  docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3H5R/tnn3_h5r2.zag.
- Frozen binary: TNN3H5R/tnn3_h5r2.bin plus a SHA-256 record, built with
  the pinned znc (src/tools/toolchain/znc_linux_x86_64_abed8aa1).
- This prereg: TNN3H5R/PREREG_H5R2.md. Process record:
  TNN3H5R/NAMECHECK.md.
- Sealed driver template (frozen pre-implementation):
  TNN3H5R/DRIVER_TMPL.zag, SHA-256
  f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af.
  Sealed worlds are assembled only after the implementation commit, per
  the frozen assembly rule in section 6.

## 4. Substrate change specification (frozen)

Exactly one change to the base, in t2_trial (lines 598-678 of the base):

4.1. Add a provenance-gate helper before t2_try_verify:

```
fn t2_prov_ok(W:[]u8,f:[]u8,nf:i32)i32 {
  let i:i32=0;
  while(i<nf){
    let fnn:i32=get32(f,i*4);
    if(ng(W,fnn,36)!=1 || ng(W,fnn,0)!=1 || is_superseded(W,fnn)==1){return 0;}
    i=i+1;
  }
  return 1;
}
```

4.2. Gate all four t2_trial promote sites on the gate (the fact array
and count at each site are unchanged):

- chain path: `if(v2!=-2){promote_graph(W,root,s,r,v2,f,k); ans=v2;}`
  becomes `if(v2!=-2 && t2_prov_ok(W,f,k)==1){promote_graph(W,root,s,r,v2,f,k); ans=v2;}`
- sum path: `if(v2!=-2){promote_graph(W,root,s,r,v2,ff,c); ans=v2;}`
  becomes `if(v2!=-2 && t2_prov_ok(W,ff,c)==1){promote_graph(W,root,s,r,v2,ff,c); ans=v2;}`
- count path: `if(v2!=-2){promote_graph(W,root,s,r,v2,f,len-1); ans=v2;}`
  becomes `if(v2!=-2 && t2_prov_ok(W,f,len-1)==1){promote_graph(W,root,s,r,v2,f,len-1); ans=v2;}`
- single-hop path: `if(v2!=-2){promote_graph(W,root,s,r,v2,f,1); ans=v2;}`
  becomes `if(v2!=-2 && t2_prov_ok(W,f,1)==1){promote_graph(W,root,s,r,v2,f,1); ans=v2;}`

4.3. What is explicitly NOT changed: activate, promote_graph,
ev_teach_in, ev_teach, ev_observe, ev_query, ev_act, miss_inquire,
mp_run, t2_try_verify, t2_gather, t2_gather_sum, t2_chain, bid,
ref_prot, is_superseded, supersede, resolve_uncertainty,
revise_on_contradict, the 4-op ISA and execute. No new modes, bridges,
routers, or handlers. The gate is a read-path predicate over existing
node state (is_superseded is existing machinery), not a new mode or
handler.

4.4. Implementability: is_superseded is tag-agnostic (scans edge fields
for a type-3 self-edge); get32/ng are existing field reads. The helper
adds 9 non-blank non-comment lines; the four sites are modified in
place (no lines added). Budget in KB-G1R: at most 15 added cognition
lines.

4.5. ORIGINAL-SIN PROHIBITION (frozen, inherited): activate and
promote_graph stay as the verified H5R versions (tag-20 MAP read path,
no shadow-fact teaching). KB-S1 gates the sealed run on both the H5R
hunks and the new gate in the committed diff.

4.6. Known consequence, pinned: a candidate whose only verifying
lineage runs through superseded facts is now declined (miss) rather
than promoted on dead provenance. The sealed worlds always teach a live
fact for the expected value (including reverts), so no bar depends on
dead-provenance promotion.

## 5. Sealed world specification (frozen before implementation)

5.1. Seeds (chosen pre-freeze; inputs hashed):
s1=48984 (world w_c1, value offset vo1=5),
s2=59920 (world w_c2, vo2=0),
s3=20822 (world w_w3a, vo3=4),
s4=29675 (world w_w3b, vo4=2).
Seed inputs: the strings
"TNN3H5R2|wave-20261001-2321pdt|world1" through
"TNN3H5R2|wave-20261001-2321pdt|world4" (SHA-256 digests recorded in
NAMECHECK.md Step 3). Value offsets are seed mod 7.

5.2. Assembly rule (frozen): each sealed world file is a byte-copy of
the committed substrate tnn3_h5r2.zag with exactly one line changed
(`fn main()i32 { return run_all(); }` to
`fn main()i32 { return sealed_main(); }`, verified by diff) plus
DRIVER_TMPL.zag appended plus one alias line selecting the world
(`fn sealed_main()i32 { return sealed_main_c1(); }`, etc.). Assembly
happens only after the implementation commit; the world file SHA-256s
are recorded before any run.

5.3. C-family worlds (w_c1, w_c2): 6 probes each (4 double-contradiction
+ 2 revert), 12 probes total, 36 MAP-key probes total.
Double-contradiction pattern per probe: teach chain a-RF1->b, b-RF2->c0;
QUERY a RM c0 (promote); OBSERVE b RF2 c1; QUERY a RM c1 (expect c1 via
fresh MAP); OBSERVE b RF2 c2; QUERY a RM c2 (expect c2 via fresh MAP).
Revert pattern per probe: teach chain; QUERY a RM c0 (promote);
OBSERVE b RF2 c1; QUERY a RM c1 (expect c1 via fresh MAP);
OBSERVE b RF2 c0 (revert); QUERY a RM c0 (expect c0 via fresh MAP).
w_c1: RF1=8301, RF2=8302, RM=8303 (subjects 83101-83104, 83201-83202).
w_c2: RF1=8401, RF2=8402, RM=8403 (subjects 84101-84104, 84201-84202).
The two worlds differ materially in relation family and subject
distribution. Concrete values are in DRIVER_TMPL.zag.

5.4. W3-family worlds (w_w3a, w_w3b): 4 chained probes each, 8 total.
Chained pattern per probe: teach chain a-RF1->b, b-RF2->c0;
QUERY a RM c0 (promote); OBSERVE b RF2 c1; QUERY a RM c1;
OBSERVE b RF2 c2; QUERY a RM c2; OBSERVE b RF2 c0 (revert);
QUERY a RM c0 (expect c0 via a fresh MAP whose DEP edges land on the
live reverted fact). Two successive revisions occur before the revert.
w_w3a: RF1=8501, RF2=8502, RM=8503 (subjects 85101-85104).
w_w3b: RF1=8601, RF2=8602, RM=8603 (subjects 86101-86104).
Materially different relation families and subject distributions.
Concrete values are in DRIVER_TMPL.zag.

5.5. World-design constraints (frozen): no OBSERVE on any MAP key in any
world; a white-box snapshot is taken before every MAP-key probe;
per-probe key ranges disjoint within a world; all keys, relations, and
values absent from FW1-FW9, the 1421pdt battery, the killed H5 battery,
the killed H5R battery, and all smoke keys.

5.6. Seal-integrity disclosure (frozen): this wave has a single worker
acting as coordinator, builder, and evaluator (no separate adversary
lane was assigned). Mitigations, all frozen here: the seeds, key
ranges, value offsets, event patterns, and driver template are frozen in
this prereg before implementation; the template hash above binds the
driver; world assembly is mechanical from the template; the builder's
smoke tests use unsealed keys (9xxx) disjoint from all sealed ranges;
the evaluator attests no world output was used to tune the substrate.
The worlds are fresh (new seeds, new ranges, new W3 family), never
salvaged from a killed battery.

## 6. Sealed evaluation protocol

6.1. Coordinator commits this prereg alone; records commit hash and UTC
timestamp in the lane dir.
6.2. Builder implements section 4 after freeze authorization, byte-copy
base verified by SHA-256, compiles with the pinned znc, freezes the
binary (SHA-256), and runs a 3/3 determinism self-check on unsealed
smoke worlds only (keys 9xxx).
6.3. KB-S1 is verified on the committed diff BEFORE any sealed world is
assembled or run: the diff against the verified base must contain the
H5R activate hunk, the H5R promote_graph hunk, and the t2_prov_ok gate
at all four t2_trial promote sites. Absent any of these, the battery
does not run; H5R2 is VOID for substrate non-compliance (NC-0R2).
6.4. Worlds are assembled per section 5.2; world file SHA-256s recorded
before any run. Each world binary is run 3/3; SHA-256 of full stdout
compared (KB-D1).
6.5. The evaluator applies the kill bars in section 7 and publishes the
verdict with evidence. If fewer than 2 valid worlds per family survive
validation, the battery is VOID and H5R2 is untested (not passed).

## 7. Frozen kill bars (exact numbers)

KB-W0 (white-box, PRIMARY): across all 36 MAP-key probe snapshots in
the C battery (w_c1, w_c2), the count of live tag-1 facts with
(f20,f24)==(s_m,r_m) is 0, and each probe's returned value equals the
f28 of the single live tag-20 MAP with (f8,f4)==(s_m,r_m). PASS: 36/36.
Any nonzero shadow count, or any probe answered from a tag-1 node,
KILLS H5R2.

KB-S1 (substrate gate, pre-run): the committed diff of tnn3_h5r2.zag
against the verified H5R base contains the activate tag-20 admission
hunk, the promote_graph ev_teach_in deletion hunk, and the t2_prov_ok
gate at all four t2_trial promote sites. Absent any of these, the
sealed run does not proceed; H5R2 is VOID for substrate non-compliance
(NC-0R2).

KB-W2R (white-box MAPs, the killed bar): on each of the 12 C probes,
the final dump shows exactly 2 superseded tag-20 MAPs with
(f8,f4)==(s_m,r_m) (carrying CON self-edges) and exactly 1 live tag-20
MAP with f28 equal to the probe's final expected value and DEP
(type-1) edges, every one of which targets a live tag-1
non-superseded fact node. PASS: 12/12. Any DEP edge to a superseded
fact KILLS H5R2.

KB-B2R (behavioral MAP): on each of the 8 double-contradiction probes,
the post-first-contradiction MAP-key probe returns c1 and the
post-second-contradiction MAP-key probe returns c2 (16/16); on each of
the 4 revert probes, the post-contradiction MAP-key probe returns c1
and the post-revert MAP-key probe returns c0 (8/8). PASS: 24/24.

KB-W3 (white-box provenance chain, NEW): on each of the 8 chained
probes (w_w3a, w_w3b), the final dump shows exactly 3 superseded
tag-20 MAPs with (f8,f4)==(s_m,r_m) (carrying CON self-edges) and
exactly 1 live tag-20 MAP with f28 equal to c0 (the reverted value)
and DEP (type-1) edges, every one of which targets a live tag-1
non-superseded fact node. PASS: 8/8. Any DEP edge to a superseded fact
KILLS H5R2.

KB-B3 (behavioral chain): on each of the 8 chained probes, the
post-first-revision MAP-key probe returns c1, the post-second-revision
MAP-key probe returns c2, and the post-revert MAP-key probe returns c0
(24/24). Each answering node is a fresh MAP (strictly increasing ids).

KB-G1R (architecture accounting): the incremental committed diff
(tnn3_h5r2.zag against the verified H5R base) shows added cognition
lines <= 15 (non-blank, non-comment), no new modes, bridges, routers,
or handlers, no core-ISA additions, and none of the forbidden protected
semantic operations. The cumulative diff against the TNN-2 base is
reported for the record. Any violation KILLS regardless of behavior.

KB-D1 (determinism): 3/3 byte-identical full-stdout runs per sealed
world (4 worlds: w_c1, w_c2, w_w3a, w_w3b). Any byte difference KILLS.

KB-P1 (process): zero forbidden-executable invocations during
construction and evaluation; safebin PATH recorded at lane startup
(NAMECHECK.md Step 0). Any violation is PROCESS-FAIL, terminal.

## 8. Negative controls

NC-0R2: KB-S1 absent. The preregistered substrate was not built.
Battery does not run. H5R2 VOID, untested.

NC-1R2: zero MAP-CON edges across a world. The supersession transition
never fires on MAPs. KILL.

NC-2R2: any behavioral bar passes while KB-W0 fails (a tag-1 node
answers a MAP-key probe, or a live tag-1 fact sits on the MAP key).
Causal attribution is broken. KILL.

NC-3R2: a MAP carries a CON self-edge but a later MAP-key probe returns
the stale value with no fresh MAP promotion. The supersession is
cosmetic. KILL.

NC-4R2: net-positive cognition lines beyond the KB-G1R budget, or any
new mode, bridge, router, or handler, or any core-ISA addition, or any
forbidden protected semantic operation. Governance KILL regardless of
behavior.

NC-5R2: any byte difference across the 3/3 reruns. Determinism KILL.

NC-6R2: a world is judged a trivial variant of FW1-FW9, the 1421pdt
battery, the killed H5 battery, or the killed H5R battery. That world
is VOID; if fewer than 2 valid worlds per family remain, the battery is
VOID and H5R2 is untested.

NC-7R2: implementation mtime predates the prereg freeze commit, or the
base copy SHA-256 does not match the frozen record, or world content
was used to tune the substrate. UNVERIFIABLE ORDERING or SEAL BREAK.
VOID.

## 9. Architecture prohibitions and core-ISA boundary

No new modes, bridges, routers, or handlers are added by this change.
The t2_prov_ok gate is a candidate-admission predicate over existing
node state (live flag, tag, is_superseded), not a new mode or handler.
One structure (the MAP node) remains both the promoted representation
and the retrieval handle.

Core-ISA boundary (per the 2026-09-30 protected core ruling): no
additions to the protected core. The change uses only existing field
reads (ng/get32), COMPARE, and the existing is_superseded predicate:
machinery, not intelligence. Forbidden as protected semantic
operations: FIND_POLYNOMIAL_ORDER, DETECT_NEGATION, BUILD_CAUSAL_RULE,
LEARN_PROCEDURE, FIND_THRESHOLD, MAKE_CONDITIONAL, and any benchmark or
domain equivalent. Adding any of these is NC-4R2, governance KILL.

## 10. Pure-Zag construction

Builder PATH is $HOME/safebin (36 tools, no python3, verified at lane
startup and recorded in NAMECHECK.md Step 0). All research logic
(implementation, verifiers, scorers, harnesses, world drivers,
white-box dump and analysis programs, world assembly helpers) is
written in Zag and compiled/run with the pinned znc. Shell is used
only to invoke znc, run binaries, do git ops, and move/copy files. Any
forbidden executable invocation is automatic PROCESS-FAIL and is
reported honestly.

## 11. Determinism protocol

3/3 byte-identical reruns of every sealed world against the assembled
world binaries, compared by SHA-256 of full stdout. Zero randomness in
decision paths: the incremental diff is grepped for
time/clock/random/rand/seed/PID reads and must show none.

## 12. Verdict rules (three-valued)

H5R2 ADVANCES iff ALL frozen bars in section 7 pass, no killing
negative control fires, and no void condition fires.

H5R2 is KILLED iff any frozen bar fails (KB-S1 excepted, see below) or
any killing negative control (NC-1R2 through NC-5R2) fires. Terminal for
this wave: no re-tune, no amend-and-promote. A killed H5R2 may return
only via a fresh prereg plus fresh sealed worlds.

H5R2 is VOID (untested, not passed) iff a battery-level void condition
fires (NC-0R2, NC-6R2 shortfall, NC-7R2). Substrate non-compliance
(NC-0R2) is VOID rather than KILL because the preregistered mechanism
was not built.

## 13. Coordinator rulings needed before implementation

Q1: Confirm the t2_prov_ok provenance gate as the pinned substrate
change (section 4), with no other trial-loop modifications.
Q2: Confirm the working-file base: byte-copy of the H5R lane's
committed tnn3_h5r.zag at 830f95ab7 (SHA-256
d98d08f0746cab4fef88fb062933a314c12492f78ee98b496e8d8912cd7fd384).
Q3: Confirm the seed-derived world parameters and the frozen assembly
rule (section 5), including the single-worker seal-integrity
disclosure and mitigations.
Q4: Confirm the frozen bar list (section 7), including the new KB-W3
family and the KB-W2R DEP-to-live-facts clause that killed H5R.
Q5: Confirm the 36-snapshot KB-W0 protocol and the frozen world-design
constraint of no OBSERVE on MAP keys.

Coordinator rulings (recorded at freeze): Q1 CONFIRM, Q2 CONFIRM,
Q3 CONFIRM, Q4 CONFIRM, Q5 CONFIRM.
