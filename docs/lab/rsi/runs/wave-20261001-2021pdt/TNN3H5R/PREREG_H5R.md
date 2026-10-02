# FROZEN PREREG: H5R, MAP-key supersession on a single retrieval structure

Lane: TNN3H5R, wave-20261001-2021pdt. Status: FROZEN PREREG (Phase 1, re-prereg).

Lineage: H5 (lane TNN3H5, same wave) was KILLED by red-team dissent
dbf25e447. The killing finding: KB-B2 failed on the MAP key because
promote_graph teaches an uncontradicted shadow fact on the MAP key, so
the MAP key never misses and MAP supersession is behaviorally inert
(write-only CON edges). Root cause: SHADOW_DIAGNOSIS.md (committed at
71b09b624). Per VOID discipline, H5 may return only via a fresh prereg
plus fresh sealed worlds. This document is that fresh prereg. Nothing
from the killed battery's worlds, keys, values, or ranges is reused.

What survives from H5 (genuine, adversary-tested, undisputed by the
dissent): the generic protected supersede transition (4 lines,
COMPARE+LINK only); guide supersession with behavioral effect (ev_act
30 to 0, 8/8); MAP CON-edge writing (8/8); selectivity (control-live,
wrong-key-resolves-nothing); net -22 cognition lines; determinism;
process. What does not survive: the MAP re-derivation story (H5 prereg
3.6); KB-B2/KB-B3 as MAP claims; any behavioral consequence of MAP
supersession.

ORDERING RULE: this prereg is committed alone by the coordinator before
any implementation file is written. Any implementation artifact whose
mtime predates the prereg freeze commit, or any implementation written
before the coordinator's explicit authorization, is UNVERIFIABLE
ORDERING and the resulting evaluation is VOID. Correction after a kill
proceeds only as a fresh prereg plus fresh sealed worlds, never
amend-and-promote.

## 1. Hypothesis under test (revised)

The H5 generic supersession transition becomes behaviorally
load-bearing for MAPs once the MAP node itself is the retrieval
structure. Concretely: with the shadow fact removed from
promote_graph and activate extended to admit non-superseded tag-20
MAPs on the key, a contradiction that supersedes a MAP removes the
only retrieval handle for the MAP key; the next MAP-key query
genuinely misses; the existing trial loop (mp_run) re-derives against
live facts; promote_graph promotes a fresh MAP. Supersession of a MAP
then causes revision, which is the claim H5 failed to evidence. The
guide half of H5 is re-tested unchanged to confirm the substrate
change does not regress it.

Falsifiable prediction: if the substrate change is correctly
implemented, then on every C-family probe the MAP-key query issued
after a contradiction must not be answerable from any
pre-contradiction structure. White-box snapshots must show zero live
tag-1 facts on (s_m,r_m) at every MAP-key probe, and each
post-contradiction probe must promote a fresh MAP (node id strictly
greater than the superseded MAPs, DEP edges anchored to live fact
nodes). If instead any post-contradiction MAP-key probe returns a
value sourced from a tag-1 node, or a live tag-1 fact exists on the
MAP key at probe time, or a probe returns the stale value with no
fresh promotion, H5R is dead: the shadow fact survives under another
name, MAP supersession is again behaviorally inert, and the original
sin is uncorrected.

## 2. Key convention (pinned; the killed battery's error may not recur)

2.1. Every C-family behavioral bar probes the MAP key (s_m, r_m),
defined as the exact (subject, relation) pair passed as (s,r) to
promote_graph at promotion time.

2.2. Fact keys (s_f, r_f) are the keys of licensing facts.
Contradiction OBSERVE events arrive on fact keys. No behavioral bar in
this prereg probes a fact key for a MAP claim.

2.3. The killed H5 battery operationalized KB-B2/KB-B3 on fact keys.
The red team showed the unmodified TNN-2 baseline passes those bars,
so they are non-discriminating. This prereg DROPS the fact-key
KB-B2/KB-B3 bars entirely. Fact-key contradiction behavior is
pre-existing machinery (ev_observe teach and supersede predate H5) and
cannot evidence the H5R substrate change. Their MAP-key successors are
KB-B2R and KB-B3R in section 8.

2.4. Sealed worlds use fresh key, relation, and value ranges disjoint
from FW1-FW9, the 1421pdt battery, and the killed H5 battery
(51xxx-54xxx). Per-probe key ranges are disjoint within a world.

## 3. Files

- Substrate base (read-only reference for the diff): the H5 lane's
  committed working file
  docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5/tnn3_h5.zag. The
  coordinator records its SHA-256 at freeze; it must be the file that
  built the verified tnn3_h5.bin (SHA-256
  344ac89fb338ddbf46bea6be4c526d99410ea643278ab91fb06d76b7e33c4eb7).
- Ultimate base reference (read-only, never edited):
  docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag
  (SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd,
  1591 lines).
- Working file (created at implementation time by byte-copy of the H5
  working file, copy verified by SHA-256 before any edit):
  docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5R/tnn3_h5r.zag.
- Frozen binary: TNN3H5R/tnn3_h5r.bin plus a SHA-256 record, built
  with the pinned znc (src/tools/toolchain/znc_linux_x86_64_abed8aa1).
- This prereg: TNN3H5R/PREREG_H5R.md. Process record:
  TNN3H5R/NAMECHECK.md.
- Sealed worlds: sealed directory chosen by the coordinator; NOT in
  this prereg; designed post-freeze per section 7.

## 4. Substrate change specification: Option A pinned

The prereg pins Option A from SHADOW_DIAGNOSIS.md section 4
(one-system-rule aligned: one structure, one read path; the duplicated
representation is removed, not patched). Option B (provenance-linked
shadow fact with cache invalidation) is NOT authorized in this prereg.
A builder wanting Option B needs a fresh prereg, because the frozen
white-box bar KB-W0 (zero live tag-1 facts on the MAP key at probe
time) distinguishes the options and would fail under Option B.
Option C (in-place patch of the shadow fact's field28) stays rejected
per the H5 Q1 ruling.

4.1. promote_graph: DELETE the shadow-fact teaching. The exact line to
be removed is line 551, `ev_teach_in(W,s,r,ans);`, inside
promote_graph (lines 543-554, quoted in section 5). After the change,
promote_graph creates the tag-20 MAP node only. Net -1 line on this
function.

4.2. activate: admit non-superseded tag-20 MAPs on the key. The exact
hunk to be changed is lines 150-161 (quoted in section 5). The tag
filter at line 153 (`ng(W,n,0)==1`) is extended so that a node
qualifies iff it is live, not superseded, and either (a) tag 1 with
(f20,f24)==(s,r) (the unchanged fact path), or (b) tag 20 with
(f8,f4)==(s,r) (the new MAP path; promote_graph stores s at f8 and r
at f4, line 545). The answer continues to come from f28 (ev_query line
770, `return ng(W,n,28)`, unchanged), which promote_graph writes as
the promoted answer (line 546; sealed dump evidence N13 f28=100).
Budget: at most +10 lines on this hunk.

4.3. Consequence, no extra code: on contradiction, ev_observe
supersedes the contradicted fact and revise_on_contradict supersedes
MAPs with DEP edges to it (unchanged H5 machinery). The MAP key now
has no live retrieval handle (no shadow fact; the MAP is superseded),
so the next MAP-key query misses in activate, ev_query's trial loop
(mp_run) runs against live facts, and promote_graph promotes a fresh
MAP. Re-derivation is the existing path, not new code.

4.4. What is explicitly NOT changed: ev_teach_in (the generic teach
primitive; only promote_graph's call to it is removed), ev_teach,
ev_observe, ev_query, ev_act, miss_inquire, mp_run, t2_try_verify,
bid, ref_prot, is_superseded, supersede, resolve_uncertainty,
revise_on_contradict, the 4-op ISA and execute. No trigger counting is
added (evidence-weighted triggers stay H6/H11 territory). No standing
machinery is connected (map_standing stays dormant).

4.5. ORIGINAL-SIN PROHIBITION (frozen): this prereg claims MAP-key
re-derivation. It is therefore forbidden to freeze activate and
promote_graph byte-identical to the H5 working file while claiming
that re-derivation. KB-S1 gates the sealed run on the presence of both
hunks in the committed diff. A MAP-supersession claim with no MAP-key
read-path change is a white-box write claim, not a cognition claim,
and must be labeled as such.

4.6. Known consequence, pinned: ev_observe on a MAP key would now
address the MAP node. The sealed worlds contain no OBSERVE on MAP keys
(section 7 pins this as a world-design constraint); KB-W0 verifies the
invariant held.

## 5. Substrate verification (verification-first; the change is implementable)

Quoted from the H5 working file tnn3_h5.zag (line numbers verified by
direct read on 2026-10-01):

activate (lines 150-161):
```
fn activate(W:[]u8,s:i32,r:i32)i32 {
  let best:i32=-1; let bb:i32=-1; let n:i32=2;
  while(n<1024){
    if(ng(W,n,36)==1 && ng(W,n,0)==1 && is_superseded(W,n)==0){
      if(ng(W,n,20)==s && ng(W,n,24)==r){
        let b:i32=bid(W,n);
        if(b>bb){bb=b; best=n;}
      }
    }
    n=n+1;
  }
  return best;
}
```
Change: line 153's `ng(W,n,0)==1` filter gains the tag-20 alternative
keyed on (f8,f4).

promote_graph (lines 543-554):
```
fn promote_graph(W:[]u8,root:i32,s:i32,r:i32,ans:i32,facts:[]u8,nf:i32)i32 {
  let m:i32=alloc_node(W); if(m<0){return -1;}
  ns(W,m,0,20); ns(W,m,4,r); ns(W,m,8,s); ns(W,m,12,-1); ns(W,m,16,-1);
  write_node(W,m,root,hg(W,24),ans,0);
  link_edge(W,m,13,m,hg(W,0));
  link_edge(W,m,2,m,0); link_edge(W,m,6,m,0);
  let i:i32=0;
  while(i<nf){link_edge(W,m,1,get32(facts,i*4),0); i=i+1;}
  ev_teach_in(W,s,r,ans);
  return m;
}
```
Change: delete line 551, `ev_teach_in(W,s,r,ans);`.

Implementability proof (each point code-verified; no new machinery):

a. The MAP already carries everything the read path needs: s at f8
and r at f4 (line 545), the promoted answer at f28 (line 546; sealed
dump N13: f4=5203, f8=52101, f28=100), tag 20 at f0, live at f36.

b. Tag-20 discrimination on a read path already has precedent in the
codebase: revise_on_contradict line 692 tests `ng(W,m,0)==20`. The
activate extension reuses that exact predicate shape.

c. is_superseded (lines 136-144) is tag-agnostic: it scans only edge
fields for a type-3 self-edge, so superseded MAPs are filtered by the
existing check with no change.

d. bid (lines 247-257) is tag-agnostic: it counts edge types
(1, 2, 6, 7 minus 3) plus POLICY_ROOT type-10 inbound contributions.
It makes no tag assumption, so calling it on MAP nodes is safe.

e. ref_prot (lines 286-292) is tag-agnostic: it refreshes type-9
protection edges; MAPs carry none, so it no-ops on MAP hits in
ev_query's hit path.

f. ev_query's hit path (lines 765-785) needs no change:
`return ng(W,n,28)` (line 770) returns the promoted answer for a MAP
hit exactly as it returned the fact value before.

g. Deletion safety: ev_teach_in (lines 320-325) stays for ev_observe's
normal teach path; only promote_graph's call is removed, and no other
caller teaches on MAP keys. The sealed worlds contain no OBSERVE on
MAP keys, so no tag-1 fact can appear on a MAP key by any remaining
path; KB-W0 verifies this empirically.

h. The re-derivation path is the already-exercised trial loop: the
killed battery promoted MAPs via mp_run on MAP-key probes with
supplied expected values, so the loop is known-good on exactly the
probe pattern section 7 pins. The only change is that the probe now
reaches the loop (the miss is no longer pre-empted by the shadow
fact).

i. Risk named honestly: if the trial loop cannot derive on some
probe, the MAP-key query returns miss (-2) and no fresh MAP is
promoted; the bars then fail loudly (KB-B2R, KB-W2R), which is the
correct failure mode, not a silent stale answer.

## 6. Sealed evaluation protocol and family requirements

6.1. Coordinator commits this prereg alone and records the commit hash
and UTC timestamp in the lane dir (PREREG_FREEZE record).
6.2. An independent adversary (a different lane agent, no shared
working state with the builder) designs the sealed worlds strictly
after the freeze timestamp, writes them to a sealed directory the
builder cannot read, and commits them with SHA-256 records. The
builder attests in writing that it has not read the world fixtures.
6.3. The adversary verifies KB-S1 (both substrate hunks present in the
committed diff) BEFORE running any sealed world. If either hunk is
absent, the battery does not run; H5R is VOID for substrate
non-compliance (section 9, NC-0R).
6.4. Builder implements after freeze authorization, compiles with
pinned znc, freezes the binary (SHA-256), and runs a 3/3 determinism
self-check on unsealed smoke worlds only.
6.5. The adversary runs the frozen binary on the sealed worlds,
collects behavioral outputs and white-box state dumps (Zag dump
program, pinned znc), applies the kill bars in section 8, and
publishes the verdict with evidence.
6.6. Any leak of world content to the builder before the run voids the
battery. If fewer than 2 valid worlds per family survive validation,
the battery is VOID and H5R is untested (not passed).

6.7. Adversarial families (minimum composition):

R-family (resolution, guide half re-test): 2 worlds. Each delivers 4
true misses creating guides on distinct keys; each miss is later
resolved by an OBSERVE on the same (s,r); after each resolution the
subject is re-presented in context and ev_act is invoked. R1 includes
1 never-resolved control guide. R2 includes 1 wrong-key OBSERVE probe.
Total: 8 resolution events. The two worlds differ materially in
structure (different relation families and subject distributions).

C-family (contradiction, MAP half, the new claim): 2 worlds. Each
world contains 4 double-contradiction probes and 2 MAP-key revert
probes (6 probes per world, 12 total; per-probe key ranges disjoint).
Per double-contradiction probe, the event pattern is:
QUERY s_m r_m c0 (promote; expect c0 answered via the MAP node),
then OBSERVE s_f r_f c1,
then QUERY s_m r_m c1 (expect c1 via a fresh MAP),
then OBSERVE s_f r_f c2,
then QUERY s_m r_m c2 (expect c2 via a fresh MAP).
Per revert probe, the pattern is:
QUERY s_m r_m c0 (promote),
then OBSERVE s_f r_f c1,
then QUERY s_m r_m c1 (expect c1 via a fresh MAP),
then OBSERVE s_f r_f c0 (revert),
then QUERY s_m r_m c0 (expect c0 via a fresh MAP).
The two C worlds differ materially (different relation families and
subject distributions). All keys, relations, and values are absent
from FW1-FW9, the 1421pdt battery, and the killed H5 battery. At least
two worlds are designed after freeze with no knowledge of the
implementation.

6.8. World-design constraints (frozen): no OBSERVE on any MAP key in
any world; a white-box snapshot is taken before every MAP-key probe
(12 probes x 3 probes = 36 snapshots); context hygiene per probe is
documented by the adversary (per the H5 Attack 4 precedent, now
pinned rather than invented mid-course).

## 7. Frozen kill bars (exact numbers)

KB-W0 (white-box, PRIMARY, the root-cause confrontation): across all
36 MAP-key probe snapshots in the C battery, the count of live tag-1
facts with (f20,f24)==(s_m,r_m) is 0, and each probe's returned value
equals the f28 of the single live tag-20 MAP with
(f8,f4)==(s_m,r_m). PASS: 36/36. Any nonzero shadow count, or any
probe answered from a tag-1 node, KILLS H5R: the shadow fact persists
and the original sin is uncorrected.

KB-S1 (substrate gate, pre-run): the committed diff of tnn3_h5r.zag
against the verified H5 working file contains the activate hunk
(tag-20 admission on (f8,f4)) and the promote_graph hunk (deletion of
the ev_teach_in call). Absent either hunk, the sealed run does not
proceed; H5R is VOID for substrate non-compliance (NC-0R).

KB-W1R (white-box guides): exactly 8 guide-CON self-edges across the
R battery (exactly 4 per world), on guide-class nodes (tag 1,
field24==-999, type-1 edge to a tag-30 node). PASS: 8/8 with exact
per-world counts 4 and 4 (not just >=).

KB-S1R (selectivity, control-live): R1 shows exactly 1 live
guide-class node with no CON edge (the never-resolved control). PASS.

KB-S2R (selectivity, wrong-key): R2's wrong-key OBSERVE produces 0 new
guide-CON edges and leaves all 4 R2 guides live. PASS.

KB-B1R (behavioral guides): ev_act returns 0 on all 8 R-events after
resolution and subject re-presentation. PASS: 8/8.

KB-W2R (white-box MAPs): on each of the 12 C probes, the final dump
shows exactly 2 superseded tag-20 MAPs with (f8,f4)==(s_m,r_m)
(carrying CON self-edges) and exactly 1 live tag-20 MAP with f28
equal to the probe's final expected value and DEP (type-1) edges to
live fact nodes. PASS: 12/12 probes.

KB-B2R (behavioral MAP; the M3-W2 analog, on the MAP key): on each of
the 8 double-contradiction probes, the post-first-contradiction
MAP-key probe returns c1 and the post-second-contradiction MAP-key
probe returns c2. PASS: 16/16.

KB-B3R (behavioral MAP revert; the M3-W3 analog, on the MAP key): on
each of the 4 revert probes, the post-revert MAP-key probe returns c0,
the c1-answering MAP carries a CON self-edge at end, and the answering
node is a fresh MAP with f28==c0. PASS: 4/4.

KB-R1R (retention): 12/12 collateral probes correct on a
no-contradiction retention world with fresh keys. Supplementary:
zero MAP-CON edges under interference (selectivity check, logged).

KB-G1R (architecture accounting): the incremental diff
(tnn3_h5r.zag against the verified H5 working file) shows added
cognition lines <= 15 (non-blank, non-comment), no new modes,
bridges, routers, or handlers, no core-ISA additions, and none of the
forbidden protected semantic operations. The cumulative diff against
the TNN-2 base is reported for the record (expected net negative,
inheriting H5's -22). Any violation KILLS regardless of behavior.

KB-D1 (determinism): 3/3 byte-identical full state dumps per sealed
world (5 worlds: r1, r2, c1, c2, ret). Any byte difference KILLS.

KB-P1 (process): zero forbidden-executable invocations during
construction and evaluation; safebin PATH recorded at lane startup
(NAMECHECK.md Step 0). Any violation is PROCESS-FAIL, terminal.

## 8. Negative controls (what KILLS or VOIDS H5R)

NC-0R: KB-S1 absent (activate or promote_graph hunk missing from the
diff). The preregistered substrate was not built. Battery does not
run. H5R VOID, untested.

NC-1R: zero MAP-CON edges across the C battery. The transition never
fires on MAPs. H5R dead per its falsifiable prediction. KILL.

NC-2R: any behavioral bar passes while KB-W0 fails (a tag-1 node
answers a MAP-key probe, or a live tag-1 fact sits on the MAP key).
Causal attribution is broken. KILL.

NC-3R: a MAP carries a CON self-edge but a later MAP-key probe returns
the stale value with no fresh MAP promotion (no new tag-20 node on the
key). The supersession is cosmetic. KILL.

NC-4R: net-positive cognition lines beyond the KB-G1R budget, or any
new mode, bridge, router, or handler, or any core-ISA addition, or any
forbidden protected semantic operation. Governance KILL regardless of
behavior.

NC-5R: any byte difference across the 3/3 reruns. Determinism KILL.

NC-6R: the adversary judges a world a trivial variant of FW1-FW9, the
1421pdt battery, or the killed H5 battery. That world is VOID; if
fewer than 2 valid worlds per family remain, the battery is VOID and
H5R is untested.

NC-7R: implementation mtime predates the prereg freeze commit, or the
base copy SHA-256 does not match the frozen record, or world content
leaked to the builder. UNVERIFIABLE ORDERING or SEAL BREAK. VOID.

## 9. Architecture prohibitions and core-ISA boundary

No new modes, bridges, routers, or handlers are added by this change.
The activate extension is a read-path admission predicate over an
existing node type, not a new mode or handler; the MAP answering from
f28 is existing ev_query behavior, not a new handler. One structure
(the MAP node) serves as both the promoted representation and the
retrieval handle; the duplicated shadow representation is removed
rather than patched, per the one-system rule.

Core-ISA boundary (per the 2026-09-30 protected core ruling): no
additions to the protected core. The change uses only the existing
field reads (ns/ng), COMPARE, and edge/link operations already
present in these functions: machinery, not intelligence. Forbidden as
protected semantic operations: FIND_POLYNOMIAL_ORDER,
DETECT_NEGATION, BUILD_CAUSAL_RULE, LEARN_PROCEDURE, FIND_THRESHOLD,
MAKE_CONDITIONAL, and any benchmark or domain equivalent. Adding any
of these is NC-4R, governance KILL.

## 10. Pure-Zag construction

Builder PATH is $HOME/safebin (36 tools, no python3, verified at lane
startup and recorded in NAMECHECK.md Step 0). All research logic
(implementation, verifiers, scorers, harnesses, world drivers,
white-box dump and analysis programs) is written in Zag and
compiled/run with the pinned znc. Shell is used only to invoke znc,
run binaries, do git ops, and move/copy files. No Python for glue,
analysis, verifiers, harnesses, or fixture provisioning. Any
forbidden executable invocation is automatic PROCESS-FAIL and is
reported honestly.

## 11. Determinism protocol

3/3 byte-identical reruns of every sealed world against the frozen
binary, compared by SHA-256 of the full state dump. Zero randomness in
decision paths: the incremental diff is grepped for
time/clock/random/rand/seed/PID reads and must show none. The H5 base
has no randomness; the substrate change adds none.

## 12. Verdict rules (three-valued)

H5R ADVANCES iff ALL frozen bars in section 7 pass, no killing
negative control fires, and no void condition fires.

H5R is KILLED iff any frozen bar fails (KB-S1 excepted, see below) or
any killing negative control (NC-1R through NC-5R) fires. Terminal for
this wave: no re-tune, no amend-and-promote. A killed H5R may return
only via a fresh prereg plus fresh sealed worlds.

H5R is VOID (untested, not passed) iff a battery-level void condition
fires (NC-0R, NC-6R shortfall, NC-7R). The hypothesis was not tested;
no advance and no kill are recorded. Substrate non-compliance (NC-0R)
is VOID rather than KILL because the preregistered mechanism was not
built, so the wave tests nothing; the builder's non-compliance is
recorded separately.

## 13. Design questions for the coordinator (ruling needed before implementation)

Q1: Confirm Option A (delete the shadow-fact teaching; the MAP node
itself is the retrieval structure) as the pinned substrate, with
Option B requiring a fresh prereg.
Q2: Confirm the working-file base: byte-copy of the H5 lane's
committed tnn3_h5.zag (coordinator records SHA-256; must match the
file that built the verified tnn3_h5.bin).
Q3: Confirm the dropped fact-key KB-B2/KB-B3 bars (non-discriminating;
the unmodified baseline passes) and their replacement by the MAP-key
KB-B2R/KB-B3R bars.
Q4: Assign the adversary lane and the sealed directory location,
confirm the builder has no read path to it, and confirm at least two
worlds are designed post-freeze with no implementation knowledge.
Q5: Confirm the 36-snapshot white-box protocol (snapshot before every
MAP-key probe) and the frozen world-design constraint of no OBSERVE
on MAP keys.
