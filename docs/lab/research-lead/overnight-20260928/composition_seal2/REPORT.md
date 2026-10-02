# REPORT: H-SEAL2-1 Second Adversarial Seal on Collapsed+Gate Composition

## Verdict: COMPOSITION-SEAL2-COMPLETE

**Nine post-freeze adversarial worlds against the frozen
collapsed+integrated composition mechanism (C234 fragment DFS +
per-(frontier,shape) APPL gate). 3/3 byte-identical per arm.
Per-world scores: 4 KILL, 4 SURVIVE, 1 BOUND.
No unified/APPL kill bar was weakened; the mechanism was not
modified. The seal's sharpest results: (1) the gate's withhold is
provably sound against earned evidence but falls to fabricated AP
records (S2F); (2) the fragment store trusts malformed marks
silently, with false LINK14 provenance (S2C); (3) an undocumented
32-candidate truncation breaks completeness under adversarial
store order (S2G); (4) the per-path triple-exclusion forbids
legitimate fragment reuse (S2H).**

Date: 2026-10-02. Worker: Composition Second-Seal Worker (H-SEAL2-1).
Frozen mechanism (byte-identical copies, never edited):
`frozen_base.zag` (dc0e86d4...), `frozen_patch_base.zag`
(190fa382...), `frozen_patch_gate.zag` (581c9a99...), all
cmp-verified against
`docs/lab/research-lead/overnight-20260928/appl_integration/`.
Worlds designed post-freeze. Branch: tnn-native-lab, local only,
nothing pushed. Pure Zag; safebin toolchain guard recorded in
NAMECHECK.md (Step 0); `which python3 python` empty throughout.

## Battery and results

Two arms from the frozen mechanism, one shared driver
(`s2_driver.zag`, used verbatim by both arms):
BASE = C234 + counters (ablation, no gate);
GATE = BASE + per-(frontier,shape) APPL gate.
SHA-256: BASE
eabed580c5626fd23b6e3c7d50c90332c408b94128d9dba3b683c4bd413a4f03,
GATE
dc8ad704d10a38de32406d78f783d02af081bc9fb2c8d5d6be91e005f2609e37,
each 3/3 byte-identical.

Harness note: S2F, S2G, S2H call `compose_try` directly
(H-COMPVER-1 precedent). Their Z queries are single-MAP-coverable,
so `ev_query_ap`'s `rebind_try` (S2F, S2G) or `mp_run` trial (S2H)
would answer without ever testing composition, or mask the
composition verdict. The unit under seal is `compose_try`; the
pipeline stages are not.

| World | Adversarial design | BASE | GATE | Score |
|---|---|---|---|---|
| S2A | winner-not-first at identical (frontier,shape): 2 same-shape decoys evaluated before the winner | PASS 103, segs [13] | PASS 103, segs [13] | SURVIVE |
| S2B | wrong-way co-use edge D->X; decoy garden path at 103 | PASS 105, segs [13 26] | PASS 105, segs [13 26] | SURVIVE |
| S2B0 | S2B control, no wrong-way edge | PASS 105 | PASS 105 | control |
| S2C0 | T4-analog, unpolluted store | FAIL -2 | FAIL -2 | control |
| S2C | S2C0 + MALFORMED mark: raw type-15 edge (m_y,0,3) on plen-2 Y MAP, entry hand-pointed at X's chain | PASS 106, segs [58 58] | PASS 106, segs [58 58] | KILL |
| S2D | cross-domain X(r1)/Y(r5) + decoy domain D(r9), parallel facts, D trained first | PASS 105, segs [27 60] | PASS 105, segs [27 60] | SURVIVE + BOUND |
| S2E | T4 partial applicability; applicable (m_x,0,3) seeded 3rd behind 2 same-shape decoy seeds | PASS 104, segs [68] | PASS 104, segs [68] | SURVIVE |
| S2F | clean 1-seg world; AP pre-seeded with 2 FABRICATED failure records at exact (F(101,70), shape 2) | PASS 103, segs [13] | FAIL -2 (skip=1, g=0 t=0) | KILL |
| S2G | 32 satisfiable decoy marks ahead of winner (m=731) in edge-id order; 32-candidate cap | FAIL -2 | FAIL -2 | KILL |
| S2H | Z needs (m_x,0,2) twice; per-path triple reuse excluded | FAIL -2 | FAIL -2 | KILL |

## Per-world findings

### S2A: winner-not-first -- SURVIVE (with a theorem)

Gate trace at 101: decoys (m=13, 26) evaluated first (edge-id
order), both `g=1 t=1 ok=1`; winner (m=39) then evaluated
`g=1 t=1 ok=1`. No skip anywhere. The composition used the FIRST
decoy's mark (segs [13]): its fallback vals reached expected, so
the intended winner was never tried. Answer correct.

The APPL report deferred the winner-not-first battery as future
work fearing a gate false-negative. The seal ran it: the kill is
structurally impossible, and the reason is not the winner-first
ordering argument but A's fallback. **Theorem (earned-evidence
soundness):** `cl_satisfy` = fetch, else any plen-(len+1) path
from cur. Two same-shape failures recorded at (F,shape) imply no
plen-(S+1) path existed at that frontier (else the fallback would
have satisfied the decoys). A later same-shape candidate at the
identical F cannot then succeed via fetch (its S licensed edges
would form exactly such a path, contradicting the identical F),
nor via fallback (same path absence). Hence the gate's skip is
sound on earned records: a skipped winner could not have
succeeded. The gate's safety rests on the fallback, not on
evaluation order. The only way to trick the withhold is
fabricated records (S2F).

### S2B: misleading co-use history -- SURVIVE

The adversarial `cb_couse_link(W,md,mx)` edge makes the DFS try
the decoy first at 103 (co-use priority over edge-id order); the
decoy fetch-succeeds down its branch (103->201->202->203) and
dead-ends; the search backtracks and completes [13 26].
Z-query DFS work: S2B enum=6 sel=3 vs S2B0 enum=5 sel=2.
The wrong-way history costs exactly one wasted evaluation and
one wasted selection; correctness is untouched. B's history is
order-only: DFS completeness plus end-to-end verification make
it unbreakable by misleading history. The control (S2B0) isolates
the cost to the fabricated edge.

### S2C0 / S2C: polluted fragment store -- control FAILs, S2C KILLs

S2C0 (unpolluted T4-analog) FAILs -2 on both arms: no false
positive, reproducing the collapse K5 behavior.
S2C adds one raw `link_edge(W,my,15,entry,3)`: a type-15 mark
(m_y,0,3) on the plen-2 Y MAP (m_y=58), with entry hand-pointed
at X's chain start cell. `cl_mark` would reject this triple
(start+len=3 > chain_len=2); the raw edge bypasses validation.
Both arms PASS 106 with `COMP-SEGS n=2 58 58`: the first segment
is walked over X's facts but attributed to m_y, and LINK14
provenance from the promoted MAP_Z points at m_y.

**KILL (integrity):** the collapsed mechanism performs zero
well-formedness validation on fragment marks. Any type-15 edge
with aux!=0 is trusted as a fragment: no check that
start+len <= chain_len(m), no check that the entry cell is m's
start-th cell. A structurally impossible mark is silently
consumed and produces false provenance. This is load-bearing
for the open T4 question (who writes sub-fragment marks: the
learner): a buggy or adversarial mark writer is trusted
without validation, and the "fragment path is real" claim (T4B)
cannot distinguish well-formed from malformed marks.

### S2D: cross-domain with decoy domain -- SURVIVE + BOUND

Both arms PASS 105 with `COMP-SEGS n=2 27 60`: the FIRST segment
uses the decoy domain's MAP (m_d=27, trained first, lowest edge
id), not X's (m_x=45), although the query was constructed as
X+Y. The Z facts contain parallel r1 and r9 chains over the
same nodes, so the composition is genuinely ambiguous and the
answer verifies.

**SURVIVE** on correctness (verification arbitrates); **BOUND**
on provenance: segment attribution follows edge-id order (MAP
creation order), not domain relevance. An adversary that trains
its MAPs first deterministically captures segment attribution
and LINK14 provenance. Provenance answers "which store entry
was used", not "which domain licensed the reasoning".

### S2E: applicable fragment deep in the store -- SURVIVE

Both arms PASS 104 with `COMP-SEGS n=1 68`: the composition
used the FIRST seeded sub-fragment (m_d1,0,3), a decoy, via
A's fallback (vals 101,102,103,104 reach expected). The
applicable (m_x,0,3), seeded third ("deep"), was never
evaluated: DFS takes the first candidate whose vals reach
expected. Store depth does not block retrieval (DFS is complete;
the gate records only successes, so nothing is skipped), but
the deep applicable fragment is SHADOWED by shallower
satisfiable seeds. The collapse K7/T4B result (seeded fragments
are consumable) is robust to depth; fragment selection is
order-dependent, not applicability-dependent.

### S2F: fabricated evidence vs the gate's withhold -- KILL

The frozen mechanism has no `compose_lv`; its withhold analog
is the gate's evidence-driven skip (plus `compose_try`'s
expected<0 decline). The driver pre-seeded 2 failure records
at the exact (F(101,70), shape 2) computed by a verbatim copy
of `ma_features_from_paths`, after the Z facts were taught.
Gate trace: `CGATE cur=101 m=13 s=0 l=2 g=0 t=0 ok=0`,
skip=1, COMP-FAIL, ans=-2. BASE: `COMP-SEGS n=1 13`, ans=103.

**KILL:** the gate's withhold is tricked by fabricated
evidence. AP records carry no integrity or provenance; earned
and fabricated records are indistinguishable to `pap_decide`,
and there is no validation, no revision, and no expiry of
records. Combined with the S2A theorem, this pins the gate's
exact trust boundary: sound on earned evidence, defenseless
against fabricated evidence. Any future learner-owned AP
needs record provenance before the gate can be load-bearing.

### S2G: 32-candidate cap exhaustion -- KILL

32 decoy MAPs (r7, plen-2) trained first; winner m=731 (r9,
plen-3) trained last via trial, so its auto-mark is created at
the Z query's `compose_try`: LAST in edge-id order. Z is 3
edges (101->104, expected=104); the winner's fetch would
succeed in one segment. At the 101 enumeration exactly 32
CGATE evaluations run (the decoys, all fallback-satisfiable),
the scan truncates (`while(e<4096 && n<32)`), and m=731 is
evaluated **0 times at cur=101** (it is evaluated at cur=103
on each of the 32 descents, where it legitimately fails).
Decoys hop 101->103 then dead-end (1 edge remains). COMP-FAIL,
ans=-2, both arms.

**KILL (completeness):** the 32-candidate cap is undocumented
(neither the collapse nor the APPL report mentions it; the
8-segment bound and length-7 cap are documented) and
adversary-triggerable: 32 satisfiable decoys ahead of the
winner in edge-id order deterministically hide a winning
fragment the store contains. Both arms share the flaw: it is
collapse-level (in `cl_candidates`), not gate-level. A valid
composition exists in the store and the mechanism cannot see
it.

### S2H: fragment reuse forbidden -- KILL

Z needs (m_x,0,2) twice (101->103, 103->105). Gate trace:
`(m=13,0,2)` evaluated once at 101 (`g=1 t=1 ok=1`, sel=1);
at 103 the same triple is excluded by the per-path reuse
check before the gate ever sees it; COMP-FAIL, ans=-2, both
arms.

**KILL (expressiveness):** the per-path (m,start,len) reuse
exclusion, documented as loop prevention, forbids legitimate
reuse. Applying the same fragment twice (a rule applied
twice, the X+X composition) is a natural compositional
pattern; the exclusion conflates it with looping. Note:
through `ev_query_ap` the `mp_run` trial stage subsequently
answered 105, masking the composition failure at query level;
the kill is at the `compose_try` level, which is the unit
under seal.

## What the seal establishes

1. The gate's skip is sound on earned evidence (S2A theorem)
   and broken only by fabricated evidence (S2F). The trust
   boundary is now exact.
2. The fragment store has no mark integrity: malformed marks
   are consumed silently with false provenance (S2C). This
   must be fixed before learner-originated marks (the T4
   follow-up) can be trusted.
3. Two completeness/expressiveness holes are shared by both
   arms, i.e. they belong to the collapsed mechanism itself,
   not the gate: the undocumented 32-candidate truncation
   (S2G) and the overbroad per-path reuse exclusion (S2H).
4. Ordering heuristics (B's co-use, edge-id order, store
   depth) affect which fragment is used and how much search
   is wasted, but cannot break correctness: DFS completeness
   plus end-to-end verification hold throughout (S2A, S2B,
   S2D, S2E all SURVIVE).
5. Provenance (LINK14 to segment source MAPs) is
   adversary-steerable via training order and falsifiable via
   malformed marks (S2C, S2D): it records store usage, not
   semantic licensing.

## What the seal does not establish

- S2F's fabricated records were seeded by the driver
  (researcher), not earned through world experience: the kill
  is an integrity hole, not a learning failure. Stale-but-
  earned poisoning was proven impossible (S2A theorem).
- The worlds are small and single-query; cross-query AP
  poisoning dynamics at scale were not tested.
- `compose_lv` (learner-verified composition) is not part of
  the frozen mechanism; world (f) tested the frozen
  mechanism's own withhold (the gate's skip), which is the
  applicable analog. Tricking `compose_lv`'s -3 withhold with
  fabricated reliability evidence remains untested.

## Determinism and process

- 3 runs per arm, byte-identical outputs (cmp clean).
- Frozen sources unmodified (sha256 re-verified after the runs).
- Pure Zag: safebin PATH for all builds and runs; no
  python3/python or other interpreters invoked.
- Zero em/en dashes in seal documentation (byte-verified).
- Research paper untouched. Nothing pushed (local commit
  only, explicit pathspecs).

## Files

- `NAMECHECK.md`: toolchain guard, freeze record, world list,
  build/run records, audits
- `REPORT.md`: this file
- `frozen_base.zag`, `frozen_patch_base.zag`,
  `frozen_patch_gate.zag`: the frozen mechanism (cmp-verified
  copies, never edited)
- `s2_driver.zag`: the nine sealed worlds (shared verbatim by
  both arms)
- `s2_full_base.zag`, `s2_full_gate.zag`: concatenated build
  inputs
- `s2_base_bin`, `s2_gate_bin`: pinned znc builds
- `s2_base_compile.txt`, `s2_gate_compile.txt`: build logs
  (exit 0, benign A0102 warnings only)
- `s2_run_base_{1,2,3}.txt`, `s2_run_gate_{1,2,3}.txt`: 3/3
  byte-identical run outputs

## Architecture accounting

New cognition lines: `s2_driver.zag` (~470 lines, world/driver
code only; the mechanism is untouched). New hardcoded semantic
cases: 0. New modes/bridges/handlers: 0. The seal killed 4
claims and bounded 1 without modifying the mechanism, as
instructed (do NOT fix what you kill).
