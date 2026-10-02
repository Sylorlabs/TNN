# H-CAUSAL-UNIFIED5 RED TEAM: ADVERSARY RESULT (X-CU5-1..4)

## 1. Verdict

**SURVIVES.** No KILL criterion (K1..K7) fired. No DOWNGRADE criterion
(D1..D4) fired in the corrected execution. The repair withstood every
attack in the frozen battery. Bounded L2, not L3: the claim under test
was a mechanism-level safety guard, never a representational invention
claim, and the red team evaluated it strictly as such.

The one DOWNGRADE-shaped signal observed (run 1, X-CU5-1 gen3) was a
fixture bug, disclosed in section 4, corrected without touching any
frozen bar, and rerun. The corrected run is authoritative.

## 2. What was under attack

Builder claim (H-CAUSAL-UNIFIED5, result commit 55fd90d0a, prereg
b486bad12): a nine-line guard in `merge_pass` skips any seed whose
parent is `ST_CONFL`, preventing tombstone-parented carve-outs from
merge sibling grouping. Builder verdict: SURVIVES, bounded L2, not L3.
Known residual out of scope: X-CU4-2 fresh-general shadow.

Files attacked:
- docs/lab/research-lead/overnight-20260928/causal_unified5/unified_causal5.zag
  (lines 1..2438, the mechanism region)
- docs/lab/research-lead/overnight-20260928/causal_unified5/cu5_test.zag

Red team assignment: assume the repair is false; break it via
second-generation carves under a re-conflicted carved tombstone
(X-CU5-1), merge pressure at entry-capacity limits (X-CU5-2), other
merge/carve interactions (X-CU5-3), and the 16/16 regression battery
plus silent-change audit (X-CU5-4).

## 3. Frozen bars (from PREREG_CU5_ADV.md, committed as c84434a9d
before any attack code was written)

KILL-K1: any MERGE trace in an attack run merges a tombstone-parented
entry, or any ACTIVE entry ends parented by a ST_CONFL entry with
mask != 7.
KILL-K2: a query predicts (r=1) at a state where a live contradiction
exists (both outcomes live in a ST_CONFL entry at that exact state).
KILL-K3: at entry capacity, a fresh learn or carve attempt is refused
without the explicit "ERROR: entry capacity" trace, or the refusal
loses/corrupts state.
KILL-K4: at entry capacity, a refused carve retires a live contradiction
(the farmed tombstone no longer holds both outcomes live).
KILL-K5: two ACTIVE tombstone-parented carves with identical fx merge
(X-CU4-1 shape under the guard).
KILL-K6: merge_pass merges entries whose fx are not identical
(over-merging), or fails to merge entries the pre-repair code merged
(behavioral regression beyond the guard).
KILL-K7: any silent behavioral change in the 16/16 battery outputs
vs the frozen CU4 baselines.
DOWNGRADE-D1: the X-CU4-3b re-adjudication pattern is not preserved
(nent stable at 2-vs-2, +1 with correct flipped winner at 2-vs-3);
the repair must not change re-adjudication behavior.
DOWNGRADE-D2: legitimate parent-(-1) sibling merges stop firing.
DOWNGRADE-D3: legitimate split-child merges under a ST_SUPER parent
stop firing.
DOWNGRADE-D4: any other behavioral regression vs the frozen CU4
baselines.
Verdict rule: any KILL fires -> KILLED. Any DOWNGRADE fires without
a kill -> DOWNGRADED. Otherwise the repair SURVIVES the attack.
An explicit entry-capacity refusal with preserved withholds is a
boundary, not a downgrade. Bars cannot be weakened after results.
A fixture bug that misfires a kill criterion is disclosed and the
attack is rerun corrected; the criterion itself stands.

## 4. Methodology and execution record

Toolchain: /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
(znc 2026.07.0-dev, edition 2026).

Harness: docs/lab/research-lead/overnight-20260928/causal_unified5/cu5_adversary/cu5adv.zag
= lines 1..2438 byte-identical to the committed unified_causal5.zag
(verified with cmp against head -n 2438 of the committed file:
MECHANISM-IDENTICAL), followed by pure-Zag adversary helpers and
main(). Correct compiler invocation:
`znc cu5adv.zag -o cu5adv` (an earlier `znc build cu5adv.zag -o cu5adv`
invocation in the pre-compaction session emitted warnings but no
binary; the resulting exit-127 runs produced identical error files
and are not evidence; disclosed here for completeness).

Adversary execution: 3 runs, exit 0, stdout byte-identical 3/3.
MD5 911846779cd83c39eee515627e7369a4. 214 lines.
Evidence: cu5_adversary/CU5_ADV_RAW_1.txt (runs 2 and 3 confirmed
byte-identical; their MD5s are recorded in section 10).

Two fixture bugs in run 1, both disclosed:
(a) X-CU5-1 gen3 misfire. My run-1 fixture expected the post-re-conflict
absorb at (2,0,0) to adjudicate inside the gen2 carve's tombstone
(entry 4). In fact `find_conflicted` breaks bestsp ties by lowest
index (`if(sp>bestsp)` keeps the first), and entry 2 (the gen1
tombstone, mask 7) ties entry 4 (mask 7) while holding the shared
live winner episodes. The absorb routed to entry 2, carved entry 5
with parent=2, and my run-1 DOWNGRADE-D1 verdict line fired on the
wrong expectation. This was my fixture's error, not the mechanism's:
the tie-break is pre-existing code in the mechanism region,
byte-identical between CU4 and CU5 (the only CU4->CU5 diff is the
merge_pass guard, per the K-CU5-4 diff audit). Corrected: the rerun
asserts the tie-break routing explicitly (X1-TIE) and tests the
routed carve for merge-safety. The D1 criterion itself is unchanged.
(b) X-CU5-2 operationalization failure. My run-1 farm-extension
helper assumed carve fx is all-FX_SET, but farm carves carry
fx=[v0:=0,v1=same,v2=same] (effects_over yields FX_UNCH where the
outcome equals the state component). The run-1 cycle gate broke on
the first carve, nent stayed 26, and the capacity attack never
executed. Corrected: winner outcomes are now read from each carve's
first live episode via ep_ns (av5_winner helper). The frozen X-CU5-2
attack (farm to 32, refusal probes) is unchanged.

Process failure, disclosed: run-1 raw stdout files were overwritten
by the corrected run-2 files before being separately preserved. The
run-1 observations survive in the session record, and every
phenomenon run 1 revealed (the tie-break routing, entry 5 parent=2)
is reproduced and explicitly asserted in the run-2 raw. No result
rests on unrecoverable run-1 bytes.

One white-box probe beyond the frozen spec, disclosed: after the
tie-break routed carve, X-CU5-1 calls merge_pass(W,100) directly to
force a merge sweep over the two same-parent carves. The prereg
permitted direct construction only for X-CU5-3; this call added a
check and weakened no criterion.

## 5. X-CU5-1 results: second-generation carves (corrected run)

Setup: 16-episode flood on action 2 over states (0..1,0..1,0..1)
reached nct=8. Contest capacity (8) exhausted at seq 18 and 20;
contradictions at (2,0,0) and (2,0,1) untracked, entries conflicted
with withhold preserved.

Gen1 carves (K-CU5-1 shape): seq 21 carved entry 2 at (2,0,0),
winner (0,0,0) support 2 vs loser (1,1,1) support 1, parent=entry 0.
Seq 22 carved entry 3 at (1,0,0), winner (0,0,0) support 2 vs
loser (1,1,1) support 1, parent=entry 0. nent=4.

Gen2 re-carve (X-CU4-3b pattern): entry 2 re-conflicted at seq 23
(contest cap exhausted, direct ST_CONFL); find_entry(2,2,0,0)=-1.
Absorb seq 24: nent 4->4 stable (2-vs-2). Absorb seq 25:
UNCONFLICT winner (1,1,1) support 3 vs loser (0,0,0) support 2;
carved entry 4 [s0=2&s1=0&s2=0] with 3 winner episodes, parent=2.
nent 4->5. Query (2,0,0): r=1, out=(1,1,1).
X1-D1 gen2 re-carve pattern HOLDS. The repair did not change
re-adjudication.

Tie-break routing (the corrected step 5): entry 4 re-conflicted at
seq 26 (contest cap, direct ST_CONFL); find_entry=-1. Absorb seq 27:
find_conflicted tie between entry 2 and entry 4 (both mask 7, both
covered at (2,0,0)) resolved to entry 2 (lowest index). UNCONFLICT
winner (1,1,1) support 3 vs loser (0,0,0) support 1; carved entry 5
[s0=2&s1=0&s2=0] with 3 winner episodes, parent=2. nent 5->6.
X1-TIE CONFIRMED: routed carve entry 5 has par=2 (the oldest
tombstone), st=0 (ACTIVE), mask=7. The routed carve is a second
carve from an already-carved tombstone: the exact X-CU4-1 shape
(two same-parent carves, identical fx=(1,1,1)), and it never merged.
Direct merge_pass(W,100) sweep: parent-invariant OK, no merge.
Entry 5 re-conflicted at seq 28 (contest cap, direct ST_CONFL).
Query (2,0,0): r=0 (WITHHOLD no-entry). X1-K2b routed withhold HOLDS.

Final state: entry 0 (mask 0, ST_CONFL, par -1, neps 20),
entry 1 (mask 0, ST_CONFL, par -1, neps 2),
entry 2 (mask 7, ST_CONFL, par 0, neps 6),
entry 3 (mask 7, ACTIVE, par 0, neps 2, fx (0,0,0)),
entry 4 (mask 7, ST_CONFL, par 2, neps 4, fx (1,1,1)),
entry 5 (mask 7, ST_CONFL, par 2, neps 4, fx (1,1,1)).
X1 parent-invariant OK (every parent ST_CONFL or ST_SUPER; every
ACTIVE tombstone-parented entry mask 7). KILL-K1 did not fire:
zero MERGE traces in the X-CU5-1 section.
Query (0,0,0): r=0, live_contra=1. X1-K2 withhold HOLDS.
Query (1,0,0): r=1, out=(0,0,0). Gen1 carve E2 intact HOLDS.

## 6. X-CU5-2 results: capacity pressure

Base farm: actions {0,1,3} x states (0..3,0,0); per cell one fresh
entry, one re-conflict (contest cap, direct ST_CONFL), one absorb
carving a gen1 carve (winner (0,0,0) 2v1). 12 tombstone/carve pairs.
nent=26. X2 parent-invariant OK.

Adaptive re-carve cycles (winner read from live episodes): cycles 0..5
re-conflicted carves 3,5,7,9,11,13 and re-carved entries 26..31, each
winner (1,1,1) support 3 vs loser (0,0,0) support 2, parented by the
re-conflicted carve. nent 26->32. Loop broke at capacity. nep=74.
at-capacity=1. X2 parent-invariant OK.

Fresh-learn probe at new state (9,0,0) action 0:
"ERROR: entry capacity (32) exhausted; new_entry refused".
KILL-K3 did not fire: the refusal was explicit and state was
preserved (nent stayed 32). Query (9,0,0): r=0. Fresh-refused
withhold HOLDS.

Carve-attempt probe on carve entry 15 (action 1, (2,0,0)):
contra (1,1,1) at seq 76 re-conflicted entry 15 (contest cap,
direct ST_CONFL, withhold preserved); winner absorb at seq 77
reached the carve step and emitted
"ERROR: entry capacity (32) exhausted; new_entry refused".
nent stayed 32. live_contra(action 1, (2,0,0))=1: the farmed
tombstone still holds both outcomes live. Query r=0.
X2-K4 evidence-preserved HOLDS. KILL-K4 did not fire.

No KILL-K3/KILL-K4. Capacity pressure neither merged anything nor
retired any live contradiction.

## 7. X-CU5-3 results: merge-class interaction

X3a (DOWNGRADE-D2 control): two parent-(-1) mask-7 entries with
identical fx. merge_pass fired: "MERGE action 0 2 siblings into
[any] at seq 3". Both seeds ST_SUPER, one merged [any] entry ACTIVE.
X3a-D2 legitimate parent-(-1) merge FIRED. DOWNGRADE-D2 did not fire.

X3b (KILL-K5): tombstone T=3 (ST_CONFL) with two ACTIVE carves e3=4,
e4=5 (parent 3, identical fx). merge_pass: nent 6->6, both carves
still ACTIVE with mask 7. X3b-K5 tombstone-parented carves did NOT
merge HOLDS. KILL-K5 did not fire.

X3c (DOWNGRADE-D3 control): split-parent S=6 (mask 1, ST_SUPER) with
two mask-7 children c1=7, c2=8, identical fx. merge_pass fired:
"MERGE action 1 2 siblings into [s0=2] at seq 11". Both children
ST_SUPER, one merged [s0=2] entry ACTIVE. X3c-D3 legitimate
split-child merge FIRED. DOWNGRADE-D3 did not fire.

X3 parent-invariant OK. KILL-K6 did not fire: both legitimate merges
fired exactly as the pre-repair code would (same sibling grouping,
same merged conditions), and the only suppressed merges were the
tombstone-parented ones the guard targets.
Caveat, disclosed: the directly constructed entries carry zero
episodes, so effects_over recomputed the merged entries' fx as
unresolved (?). The frozen checks concerned merge-class behavior
(which entries merge, which do not), and those are unaffected.

## 8. X-CU5-4 results: 16/16 regression and silent-change audit

Unmodified unified_causal5.zag compiled and run 3 times: stdout
byte-identical 3/3, MD5 87f8edc29825802327029f46f045dbe3, and
byte-identical (cmp) to the frozen
causal_unified4/CU4_RAW_MAIN.txt on all 3 runs.
cu5_test.zag compiled and run 3 times: stdout byte-identical 3/3,
MD5 3bde55fe381a7c8ff1cef93d8c038da3, and byte-identical (cmp) to
the frozen causal_unified4/CU4_RAW_TEST.txt on all 3 runs.
KILL-K7 did not fire. DOWNGRADE-D4 did not fire. The 16/16 battery
is preserved byte-for-byte; the repair is behaviorally silent on
every previously tested path.

## 9. Causal interpretation

The guard holds for a structural reason, and the attacks confirmed
each link. Siblings are defined by sharing one parent, so checking
the seed's parent state before sibling gathering covers the entire
sibling group; no second code path can admit a tombstone-parented
entry into a merge. ST_CONFL has no authored exit transition
(verified by audit: no path returns ST_CONFL to ST_ACTIVE), and
ST_SUPER is terminal, so "parent is ST_CONFL" is a stable
classifier. Across gen1 carves, gen2 carves, the tie-break-routed
second carve from an already-carved tombstone (the X-CU4-1 shape
with two same-parent identical-fx carves), direct-construction
twins, and capacity refusal, zero tombstone-parented merges
occurred and every parent invariant held.

The tie-break routing is the run's one genuine behavioral discovery
and it is pre-existing, not a CU5 regression: find_conflicted keeps
the lowest index among equally-specific covered tombstones, and the
mechanism region containing it is byte-identical between CU4 and
CU5. Consequence: re-adjudication at a state always routes to the
oldest tombstone holding live episodes there, because carve winners
stay live in the parent tombstone (shared indices). A true
grandchild carve (parent = newest tombstone) is unreachable via the
absorb path once an older equally-specific tombstone shares the
live winners. Every observed adjudication through this routing was
safe: exact-state scoping, correct majority winners, withholds held,
no merge. Related boundary property, noted without a kill (no
criterion covers it, no unsafe prediction observed): the shared
winner episodes vote in more than one adjudication over time
(double counting); all observed outcomes through double counting
were consistent (3v2 and 3v1 majorities for (1,1,1)).

## 10. Boundaries and non-claims

- The X-CU4-2 fresh-general shadow remains out of scope, per the
  builder's stated residual and the frozen prereg.
- Contest-capacity exhaustion (8) forces re-conflicts down the
  untracked-contradiction path (direct ST_CONFL, no contest record);
  observed throughout, not attacked beyond observation.
- True gen3 carves via the absorb path are unreachable under the
  tie-break (section 9); gen3 reachability by other paths was not
  tested.
- X-CU5-3 direct-construction entries have no episodes; merged fx
  recomputes as unresolved. Merge-class behavior (the tested
  property) is unaffected.
- Run-2 adversary MD5 911846779cd83c39eee515627e7369a4 (runs 1..3
  identical). X-CU5-4 main MD5 87f8edc29825802327029f46f045dbe3
  (runs 1..3 identical). X-CU5-4 test MD5 3bde55fe381a7c8ff1cef93d8c038da3
  (runs 1..3 identical).

## 11. Governance disclosures

- Pure Zag: every helper, harness, and check is Zag. No Python
  anywhere in this arc, including scratch work and verification.
- Preregistration strictly preceded implementation: frozen prereg
  committed alone as c84434a9d before any attack code existed.
- Frozen bars were not weakened. The two run-1 fixture bugs were
  corrected in the harness only; every criterion stands as frozen.
- No em dashes in this documentation, per the TNN loop style rule.
- Commit lineage: builder prereg b486bad12, builder result 55fd90d0a,
  adversary prereg c84434a9d, this result commit (to be recorded on
  commit). Commits stay local; nothing is pushed without Micah's
  explicit authorization.
- Binary cu5adv and the .zag-cache directory are not committed.
- The pre-compaction session's incorrect `znc build` invocation that
  emitted no binary is disclosed in section 4 and is not evidence.
