# REPORT: L2 SUBSTITUTE-XDOMAIN (cross-domain substitute with interface adaptation)

Worker: L2 Adaptive Reuse subagent (depth 2/2), 2026-10-02.
Prereg: `l2_substitute_xdomain/PREREG.md`, frozen alone at commit
6bed092c3 before any implementation existed. Two transparent
amendments, both pre-verdict: PREREG_AMENDMENT1.md (fold-discovery
valrel skip + FULL count correction 671->865, pre-implementation,
commit d6d8e01ee); PREREG_AMENDMENT2.md (FULL A_SEARCH 865->941,
pure arithmetic correction: the arity LINK phase examines all
addends with no early exit, pre-verdict, commit 4d69d7459).

## Verdict

**L2-SUBSTITUTE-XDOMAIN-PASS.** All eight kill bars PASS, no
falsifier fired, 3/3 byte-identical.

## What was built

A standalone pure-Zag learner (`learner.zag`, ~700 lines) plus
environment side (`world.zag`: frozen 38-fact table + COST kill)
and experiment side (`driver.zag`: teaching, five arms, in-Zag
bar evaluation), assembled as
`cat learner.zag world.zag driver.zag > xa_full.zag` (1296 lines)
and compiled with the pinned znc to `xa_bin` (build exit 0,
warnings only: A0102 ignored-return-value class, same as the
predecessor lane).

The learner holds a fact store, a MAP inventory with
capability/domain/interface-descriptor records, an edge store
using only types 14/15/16, and the generic cross-domain
SUBSTITUTE-ADAPT operator: on a query whose (domain, capability)
has no native MAP, it collects the query's step set via the
domain's route MAP, searches the whole inventory in MAP-id order
for the first capability-matching MAP (any domain), extracts
that source's interface descriptor (entry hop + alternating
fold-pair + fold count + value-relation, all discovered at teach
time), scans entries from the query start, discovers fold-chains
by runtime pair-pattern matching (skipping the discovered
value-annotation relation), enforces the target domain's pair
interface (every addend VAL-checked and COST-linked from a plan
step through one uniform discovered link relation), builds Z by
remapping the source interface onto the discovered grounding,
verifies Z by real execution to the query target with terminal
value check, promotes Z with adapted-from provenance to both
source structures, and delivers through Z. A generic BFS
rebuild (L=1..7, AGG shape + VAL + arity checks, no learned
structure guiding it) is the honest from-scratch baseline. The
no-adaptation control arm runs the same adapter with the pair-
interface check disabled.

## Kill-bar results (in-Zag BARS + shell checks on xa_run1.txt)

- K1 (X and Y exist before Z, learned independently): in-Zag
  qa_via=1, qb_via=2, q2_via=3, and mA's rels are all in
  {18,5,6} while mB0's are all 7 (disjoint vocabularies);
  shell: `Q QA` (line 2) < `Q QB` (line 4) < `Q Q2`
  (line 6). PASS.
- K2 (Z causally depends on both): ABLATE-X (mA retired):
  ans=75 via=3 NATIVE id 3, t16=0, e_has(3,1,16)=0 (the
  adapted Z, defined by its adapted-from provenance, cannot
  exist without mA; blind BFS rebuilds a native lookalike at
  A_SEARCH=2060, ~2.19x the guided adapt). ABLATE-Y (COST
  facts killed): ans=-2, t16=0, NM=3 (no grounding satisfies
  the pair interface). PASS.
- K3 (interface adaptation actually occurs, not exact copy):
  in-Zag NOADAPT ans=-2, t16=0, NM=3 (decoy Z' grounded from
  facts 19,28..33, verify 67 != 73 FAIL, never promoted).
  Shell verbatim: `XA-REMAP 5->15 6->16`, `XA-ENTRY 18->17`,
  `XA-ARITY u=70 addvals=20,30,25 cost_rel=8 OK`,
  `XA-ZBUILD rels=17,15,16,15,16,15,16
  facts=20,21,22,23,24,25,26`, `ANS term=73 val=75 via=3`
  all present. The relation remap, entry remap, discovered
  cost_rel=8, B-range addvals, and B-fact-grounded ZBUILD
  prove runtime interface derivation; the exact-copy path
  provably fails. PASS.
- K4 (fresh learner fails): FRESH (no MAPs): steps fallback
  {50}, BFS finds the Z-walk shape at L7 but arity fails
  (addend 61 not linked from 50); ans=-2, t16=0, NM=0.
  PASS.
- K5 (determinism): 3/3 sha256 identical:
  eea8678d436a927788fdb451d5fadecf3ff39cc563539a2ec9a9d29e9d439b08.
  PASS.
- K6 (no domain-pair template): all 10 frozen grep patterns
  return 0 hits on learner.zag. PASS.
- K7 (learner-triggered): in-Zag SRC_ID=1 with mD (id 0)
  live=1 (distractor survives unchosen); shell verbatim
  `XA-SEARCH id=0 cap=2 SKIP` and `XA-SEARCH id=1 cap=1
  MATCH`; the driver issues Q2 as (50,73,75,AGG,B) with no
  MAP id. PASS.
- K8 (Z persists and is reused): Q2B ans=75 via=3,
  ADAPT_ENTERED=0, Z live=1. PASS.

No falsifier fired: F-EDGE-NEW (all arms oth=0), F-COUNT
(FULL A_SEARCH=941, A_EXEC=3), F-WRONG-Z, F-NO-GROUND,
F-NO-LINK14, F-NO-T16-SRC, F-T16-COUNT, F-T15-COUNT all
silent.

## Key numbers

- FULL adapt: A_SEARCH=941, A_EXEC=3. Trace: capsearch
  SKIP mD / MATCH mA; descriptor (18,5,6,3,valrel 2);
  entries (7,51) FAIL-SHAPE, (8,60) FAIL-SHAPE,
  (17,64) decoy SHAPE-OK then LINK-FAIL,
  (17,70) SHAPE-OK then arity OK; Z promoted id 3.
- Provenance: t16 {3->1, 3->2}, t15 {1->2, 2->1},
  LINK14 answer42->3, zero other edge types.
- NOADAPT: ans=-2, t16=0, NM=3 (A_SEARCH=552 inform.).
- ABLATE-X: native id 3, ans=75 via=3, t16=0,
  A_SEARCH=2060 (~2.19x), A_EXEC=3.
- ABLATE-Y: ans=-2, t16=0, NM=3 (A_SEARCH=820 inform.).
- FRESH: ans=-2, t16=0, NM=0 (A_SEARCH=2528 inform.).
- Binary sha256:
  8e7508f09678c066fd59f9a902cacc28ccf8d0e571be600bacb79fee23ea0bd0

## Implementation notes (disclosed)

- Two implementation fixes were made to match the frozen
  prereg (both pre-verdict, both documented here):
  (a) `map_create` moved to after verification success in
  `xa_adapter` and `xa_rebuild`: the prereg requires "a
  graph that does not execute to its terminal is never
  promoted" and NOADAPT NM=3; the first build created the
  MAP record before verify, leaking NM=4 on the failing
  control. (b) Driver F-COUNT updated 865->941 per
  AMENDMENT2.
- A /tmp debug build (never committed) with A_SEARCH
  snapshots pinpointed the 865->941 slip to the arity LINK
  loop examining all three addends (3x38) rather than
  early-exiting; the frozen counting rules (+1 per fact id
  examined) confirm 941.
- Pinned-znc workarounds honored: u8 cells + get32/set32
  (no `as *i32` slices), cursor emit helpers + single
  raw-syscall write (no `_zag_print` for dynamic content),
  if-nesting <= 4 with == comparisons, no `!(A && B)`
  while-conditions (grep-verified zero hits).

## Architecture accounting

- Cognition lines added: 1296 (learner.zag ~700,
  world.zag ~70, driver.zag ~230, assembled xa_full.zag;
  new files, nothing else touched).
- New hardcoded semantic cases: 0. New modes: 0. New
  bridges: 0. New handlers: 0. New edge types: 0
  (14/15/16 reused). New opcodes: 0. No domain-pair
  literal in learner.zag (K6 audit).
- Capability-source delta: the cross-domain substitution
  lives in one generic operator plus learned MAP state;
  the source selection, relation remap, entry remap,
  cost_rel discovery, and value sourcing are all
  runtime-derived from learner state, never
  researcher-selected per problem.

## Why this is L2 adaptive reuse (cross-domain)

The planning domain had no aggregation capability. The
learner did not copy the arithmetic SUM structure (different
rels, different entry, 1-arity bare addends vs 2-arity
(step,COST,cost) pairs, single- vs double-digit ranges); it
adapted the interface: discovered the fold-pair pattern in
B's facts under a runtime remap {5->15, 6->16, 18->17},
enforced B's pair interface via discovered cost_rel=8,
rejected a structurally valid decoy on interface grounds,
sourced values from B's range through the discovered
valrel, verified by execution, and promoted Z with
dual-source provenance. Ablations prove Z depends on both
the X structure (no mA -> no adapted Z, only a 2.19x
native rebuild) and the Y interface (no COST facts -> no
grounding), and the fresh learner fails outright.

## Files

All under `docs/lab/research-lead/overnight-20260928/l2_substitute_xdomain/`:

- PREREG.md (frozen, committed alone at 6bed092c3)
- PREREG_AMENDMENT1.md (fold valrel skip, pre-implementation)
- PREREG_AMENDMENT2.md (FULL A_SEARCH 865->941, pre-verdict)
- NAMECHECK.md (toolchain guard Step 0 record)
- REPORT.md (this file)
- learner.zag (generic cross-domain SUBSTITUTE-ADAPT learner)
- world.zag (38-fact table + COST kill; environment side)
- driver.zag (teaching, five arms, in-Zag bar evaluation)
- xa_full.zag (assembled 1296-line build input)
- xa_bin (compiled binary)
- xa_compile.txt (build log; exit 0)
- xa_run1.txt, xa_run2.txt, xa_run3.txt (3/3 byte-identical)

## Non-claims and bounds

- One world family (arithmetic SUM x plan-cost aggregation).
  No generality claim beyond the five arms. Cross-domain
  substitution with other interface mismatches, and
  sealed-adversary generality, are open future work.
- Does not claim Micah's full 12-criterion L3 bar; this is
  an L2 operator demonstration against eight frozen bars.
- The world (fact table, decoy chain, COST kill) was
  builder-designed, not adversary-designed.
- The SUBSTITUTE-ADAPT operator, descriptor extraction,
  entry/fold search, arity check, rebuild BFS, edge-type
  conventions, and cost counters are disclosed
  researcher-supplied generic machinery. The claim is
  narrow: cross-domain substitution with runtime-derived
  interface adaptation, execution verification, dual-source
  provenance, and a provably failing no-adaptation control.
- Pure Zag, safebin toolchain, zero forbidden executables.
  Paper untouched. Nothing pushed. Commits local with
  explicit pathspec.
