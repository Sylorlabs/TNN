# REPORT: XP-SELECT-4 (grammar to program, CONSTRAINT-STRICTNESS mismatch)

Date: 2026-10-02. Worker: XP-SELECT-4 (replacement for completed
XP-SELECT-3). Shared lane branch, local only, nothing pushed. Pure
Zag throughout; safebin guard PASS (Step 0 in NAMECHECK.md); pinned
znc_linux_x86_64_abed8aa1.

## Verdict: XP-SELECT-4-PASS (K1-K13 all pass)

The learner selects the constraint-strictness adaptation itself on
the grammar-constraint to program-construction pair: TRUNCATE in the
too-strict world (A1), EXTEND with a store-read terminator relation
in the missing-dimension world (A2), with no world flag, no
domain-pair handler, and no paired X to Y examples anywhere. This
breaks the domain-pair boundary of the XP-SELECT line a second time
(priors: arithmetic to planning, causal to intervention) on the
exact pair Micah's high-value list names, and the first where X is a
learned well-formedness CONSTRAINT rather than a causal or
arithmetic chain.

## Battery results (3/3 byte-identical runs)

| Arm | Expectation (frozen) | Result |
|---|---|---|
| A1 SELECT-TRUNCATE | ans=106, one adapted [71]x3, op=TRUNCATE only | PASS (12/12 assertions) |
| A2 SELECT-EXTEND | ans=108, one adapted [71,71,71,71,73], op=EXTEND only | PASS (12/12) |
| A3 REJECT | ans=-2, zero type-16 | PASS |
| A4 L1-REGRESSION | ans=107, zero type-16, MAP_Z 14 to X and Y | PASS |
| A5 NO-ADAPT | ans=-2, zero adapted (one-line build) | PASS |
| A6 ABL-X | ans=-2 | PASS |
| A7 ABL-Y | ans=-2 | PASS |
| A8 FRESH | ans=-2 | PASS |
| A9 REUSE | 106/106, adapted count stays 1 | PASS |
| A10 AMBIGUOUS | ans=110, two adapted, verifier picks extend | PASS (11/11) |

Run sha256 (main binary, 3 runs):
fcfc1afcf9e4f704c4cefe72a2090e4f4e682f27d174080f03dca9538ef343a9
Run sha256 (no-adapt binary, 3 runs):
448d4690eddf70ee51924ad8cd9edd5674b9a3cd497020520711994de159d611
Binaries: xs4_bin
f461b43af074757802a396287e7430c2879ca07eb8c6f88bfeb3ec99b89cad52,
xs4_bin_noadapt
1ea7b3a6d19854c3ecaef8c0442563ee4148cf55c90845fcf3e6707f84aed824.
Patch sha256:
db607664f24502ba3b2ea8e4c68090f4bd3e3e33adb6e03f1a885deb7f9fa758.

## Per-arm evidence

Training (all arms): MAP_X id=45 relseq [71]x4 (grammar
well-formedness: 4 delimiter levels), MAP_Y id=58 relseq [72]x2
(program construction: 2 build steps). Training queries fired the
bracket with ADAPT-CREATED n=0 both times: no spurious adaptation
during learning.

A1: trace shows XS4-TRY op=TRUNCATE m=45 lp=3 s=101 (longest prefix
first), ADAPT-MK id=134 src=45 op=TRUNCATE; EXTEND on m=45 failed
(the full 4-hop walk fails on the 3-hop world); MAP_Y (58)
TRUNCATE/EXTEND tries failed. ADAPT-CREATED n=1. Phase 2 re-ran
the unchanged compose_try: COMP-SEGS n=2 134 58 (adapted + MAP_Y),
ans=106. MAP_Z LINK14 to 134 and to MAP_Y (58), none to MAP_X.
K13: [71]x3 strict prefix of [71]x4; adapted licensing fact ids
disjoint from MAP_X training fact ids; exactly one type-16 edge
workspace-wide.

A2: trace shows TRUNCATE lp=3,2,1 all tried and none licensed (no
native interface satisfies forward from 104/103/102), then EXTEND:
full [71]x4 walk to 105 plus the live frontier fact (105,73,106)
read from the store, ADAPT-MK id=144 src=45 op=EXTEND, relseq
[71,71,71,71,73], end 106. COMP-SEGS n=2 144 58, ans=108. MAP_Z
LINK14 to 144 and 58, none to MAP_X. K13: [71]x4 strict prefix of
[71,71,71,71,73]; fact ids disjoint; one type-16 edge. No hardcoded
extension relation or depth: the fifth relation (73, the
terminator dimension X never learned) came from the fact store and
differs from the walked relation (71).

A3: selector fired (ADAPT-TRY) and tried lp=3,2,1 plus EXTEND;
nothing licensed (r83 has no learned interface); ADAPT-CREATED
n=0; ans=-2; zero type-16 edges workspace-wide. Clean reject.

A4: exact composition solved the Z query (X [71]x4 then Y [72]x2);
no ADAPT-TRY between the Z facts and the answer (the two
ADAPT-TRY lines in the arm are the training queries, both
ADAPT-CREATED n=0); ans=107; zero type-16; MAP_Z LINK14 to MAP_X
and MAP_Y. No regression.

A5: one-line no-adapt build (diff-verified: exactly one line,
adapt_on 1 to 0) on the A1 setup verbatim: ans=-2, zero adapted
MAPs. The exact pipeline provably cannot solve the too-strict
constraint task: activate misses; rebind fails (X unsatisfiable on
3 hops, Y unsatisfiable from 101); compose_try DFS exhausts (X via
the contract fallback reaches 105, Y via the fallback reaches 103,
neither continues to expected); trial capped at plen 5 while the
full path needs plen 6; bootstrap misses.

A6/A7/A8: all ans=-2. Causal dependence on learned X (nothing to
strictness-adapt), on learned Y (no native interface to license),
and the fresh learner fails outright.

A9: first query 106 with one ADAPT-MK (TRUNCATE); second query 106
with no ADAPT-TRY at all: the unchanged compose_try admitted the
adapted MAP as a level-0 candidate and reused it. Adapted count 1
after both queries. Dedup plus reuse, no spurious re-adaptation.

A10: both branches licensed expected-free: TRUNCATE walked
101->104 (Y reaches 106, wrong value but licensed), EXTEND walked
101->107 plus frontier terminator fact (107,73,108) to 108 (Y
reaches 110). Two adapted MAPs (t=155 end 104, p=177 end 108),
both type-16 to MAP_X, two type-16 edges total. Phase 2
COMP-SEGS n=2 177 58: the unchanged verifier composed only the
expected-consistent extension; MAP_Z LINK14 to p and to MAP_Y,
none to t and none to MAP_X; ans=110. Ambiguity resolved by the
verifier, not a world flag.

## Kill bars

K1 A1: all 12 assertions pass; trace shows exactly one ADAPT-MK
op=TRUNCATE. K2 A2: all 12 pass; exactly one ADAPT-MK op=EXTEND
with store-read relation 73. K3 A3: ans=-2, zero adapted. K4 A4:
passes, zero type-16, bracket inert on the Z query. K5 A5:
ans=-2, zero adapted. K6 A6/A7/A8: all -2. K7 A9: 106/106,
adapted count stable at 1, second query fired no bracket. K8 A10:
all 11 assertions pass; unused adaptation provably not composed
(no LINK14 to t). K9: 3/3 byte-identical runs both binaries (shas
above). K10: zero em/en dashes in all authored deliverables
(byte-verified); the only em dashes in the lane are
compiler-emitted warning text inside the two znc build logs
(unavoidable toolchain output; the base files that trigger the
warnings are frozen read-only). K11: cc_base.zag
dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
and un_patch.zag
3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2,
both used verbatim via build concatenation, never modified
(re-verified after the run). K12: 0 new edge/MAP types, 0 new
opcodes, 0 modes, 0 bridges, 0 handlers, 0 semantic cases; the
patch's link_edge calls use only pre-existing types (1, 2, 6, 8,
13, 16); 14/15 come from the unchanged compose_try re-run. K13:
per-arm driver assertions on strict-prefix parentage (truncate:
adapted strict prefix of source; extend: source strict prefix of
adapted), exactly one type-16 edge per adapted MAP to live native
MAP_X, and licensing fact ids disjoint from MAP_X training fact
ids. A from-scratch rebuild cannot satisfy parentage, provenance,
fact-disjointness, and dedup together.

## Governance

Prereg committed ALONE first (commit b631afac7, 2 files;
commit-order self-check: prereg strictly precedes
implementation). Implementation second, report third. Explicit
pathspecs on every commit; no git reset; nothing pushed. Base
files frozen read-only.

## Honest disclosures

1. Pre-freeze well-formedness prototype (throwaway, never
   committed, deleted after): exact pipeline on all five Z shapes
   gave -2/-2/-2/107/-2; walk primitives confirmed (3-hop walk
   101->104, 4-hop walk 101->105 plus frontier terminator fact
   (105,73,106), Y-license from 104/106/108). No
   selector/orchestration code was prototyped; frozen bars were not
   adjusted to fit outcomes.
2. Reading: XP-SELECT-3 prereg/patch/driver and
   xdomain_grammar_construct prereg/report read in-checkout for API
   surface, selector architecture, and assertion patterns
   (documented in NAMECHECK.md); the XS4 selector, driver, and
   battery were designed from the frozen prereg in this lane, not
   copied. Function names use the xs4_ prefix; trace tags use XS4-.
3. K10 disclosure as above (compiler-emitted em dashes in build
   logs only).
4. The selector architecture is the XP-SELECT line's shared
   arity-family selector applied to a third domain pair; this
   worker's contribution is the evidence-driven selector on the
   grammar to program pair with the constraint-strictness family,
   not a new operator set.

## Scope (honest boundaries)

One domain pair (grammar constraint to program construction), one
mismatch family (constraint strictness: too-strict and
missing-dimension), two selectable operations. L2 adaptive reuse
with operation selection, not L3 invention: the operations are
researcher-defined; the selection among them by satisfiability
evidence is the learner's. New evidence over XP-SELECT-3: (a) the
family applies to a constraint-type X (well-formedness bound) on
the grammar to program pair; (b) EXTEND demonstrably adds a
genuinely different constraint relation (73) read live from the
fact store, not another hop of the walked relation; (c) the A10
ambiguity arm resolves through the unchanged verifier. Follow-up
candidates: the strictness family on a fourth pair, or a third
mismatch family on this pair.
