# REPORT: XP-SELECT-3 (causal to intervention, INTERFACE-ARITY mismatch)

Date: 2026-10-02. Worker: XP-SELECT-3 (replacement for completed
XP-SELECT-2). Branch: lane-compinteg2-20261002, local only, nothing
pushed. Pure Zag throughout; safebin guard PASS (Step 0 in
NAMECHECK.md); pinned znc_linux_x86_64_abed8aa1.

## Verdict: XP-SELECT-3-PASS (K1-K13 all pass)

The learner selects the arity adaptation itself on the
causal-model to intervention pair: TRUNCATE in the too-deep world
(A1), EXTEND in the too-shallow world (A2), with no world flag, no
domain-pair handler, and no paired X to Y examples anywhere. This
breaks the domain-pair boundary of the XP-SELECT line (both priors
were arithmetic to planning) on the exact pair Micah's high-value
list names.

## Battery results (3/3 byte-identical runs)

| Arm | Expectation (frozen) | Result |
|---|---|---|
| A1 SELECT-TRUNCATE | ans=106, one adapted [91]x3, op=TRUNCATE only | PASS (12/12 assertions) |
| A2 SELECT-EXTEND | ans=108, one adapted [91]x5, op=EXTEND only | PASS (12/12) |
| A3 REJECT | ans=-2, zero type-16 | PASS |
| A4 L1-REGRESSION | ans=107, zero type-16, MAP_Z 14 to X and Y | PASS |
| A5 NO-ADAPT | ans=-2, zero adapted (one-line build) | PASS |
| A6 ABL-X | ans=-2 | PASS |
| A7 ABL-Y | ans=-2 | PASS |
| A8 FRESH | ans=-2 | PASS |
| A9 REUSE | 106/106, adapted count stays 1 | PASS |
| A10 AMBIGUOUS | ans=110, two adapted, verifier picks extend | PASS (11/11) |

Run sha256 (main binary, 3 runs): 
52a63054a86eaf9ce571a6d51d3f2dce0a7d7a924280a68eef05d45bbdc6ef11
Run sha256 (no-adapt binary, 3 runs):
08d7a7a7caf184422e53ae9859a289c6f667e0eae000a089ea7413f4f9b8c896
Binaries: xs3_bin
6ed3d9dce3758af51434eeb39808bc131d5ce1f0533de6c4516244ef3212f51b,
xs3_bin_noadapt
ecd37e82e335b294fefaf7c0902e6b1618bd96df114503d0bbfbe402f43da781.
Patch sha256: 7daa33f02109389aa5a2ed4a9e13315495b8d4193329bd399b1059eb13a13bf9.

## Per-arm evidence

A1: trace shows XS3-TRY op=TRUNCATE m=45 lp=3 (longest prefix
first), ADAPT-MK id=134 src=45 op=TRUNCATE, then XS3-TRY op=EXTEND
m=45 (full 4-hop walk fails on the 3-hop world, no candidate).
Exactly one adapted MAP: relseq [91,91,91], start 101, end 104,
type-16 to MAP_X (45). Phase 2 re-ran the unchanged compose_try:
COMP-SEGS n=2 134 58 (adapted + MAP_Y), ans=106. MAP_Z LINK14 to
134 and to MAP_Y (58), none to MAP_X. K13: [91]x3 strict prefix
of [91]x4; adapted licensing fact ids disjoint from MAP_X
training fact ids; exactly one type-16 edge workspace-wide.

A2: trace shows TRUNCATE prefixes lp=3,2,1 all walked but none
licensed (no native interface satisfies forward from 104/103/102
under r92), then EXTEND: full [91]x4 walk to 105 plus the live
frontier fact (105,91,106) read from the store, ADAPT-MK id=144
src=45 op=EXTEND, relseq [91,91,91,91,91], end 106. COMP-SEGS n=2
144 58, ans=108. MAP_Z LINK14 to 144 and 58, none to MAP_X. K13:
[91]x4 strict prefix of [91]x5; fact ids disjoint; one type-16
edge. No hardcoded extension depth: the fifth relation came from
the fact store.

A3: selector fired (ADAPT-TRY) and tried lp=3,2,1 plus EXTEND;
nothing licensed (r83 has no learned interface); ADAPT-CREATED
n=0; ans=-2; zero type-16 edges workspace-wide. Clean reject.

A4: exact composition solved the Z query (X [91]x4 then Y
[92]x2); the bracket never fired on the Z query (no ADAPT-TRY
between the training queries and the answer); ans=107; zero
type-16; MAP_Z LINK14 to MAP_X and MAP_Y. No regression.

A5: one-line no-adapt build (diff-verified: exactly one line,
adapt_on 1 to 0) on the A1 setup verbatim: ans=-2, zero adapted
MAPs. The exact pipeline provably cannot solve the arity-mismatch
task: activate misses; rebind fails (X unsatisfiable on 3 hops,
Y unsatisfiable from 101); compose_try DFS exhausts (X via the
contract fallback reaches 105, Y via the fallback reaches 103,
neither continues to expected); trial capped at plen 5 while the
full path needs plen 6; bootstrap misses.

A6/A7/A8: all ans=-2. Causal dependence on learned X (nothing to
arity-adapt), on learned Y (no native interface to license), and
the fresh learner fails outright.

A9: first query 106 with one ADAPT-MK (TRUNCATE); second query
106 with no ADAPT-TRY at all: the unchanged compose_try admitted
the adapted MAP as a level-0 candidate and reused it. Adapted
count 1 after both queries. Dedup plus reuse, no spurious
re-adaptation.

A10: both branches licensed expected-free: TRUNCATE walked
101->104 (Y reaches 106, wrong value but licensed), EXTEND
walked 101->107 plus frontier fact (107,91,108) to 108 (Y
reaches 110). Two adapted MAPs (t=155 end 104, p=177 end 108),
both type-16 to MAP_X, two type-16 edges total. Phase 2
COMP-SEGS n=2 177 58: the unchanged verifier composed only the
expected-consistent extension; MAP_Z LINK14 to p and to MAP_Y,
none to t and none to MAP_X; ans=110. Ambiguity resolved by the
verifier, not a world flag.

## Kill bars

K1 A1: all 12 assertions pass; trace shows exactly one ADAPT-MK
op=TRUNCATE. K2 A2: all 12 pass; exactly one ADAPT-MK op=EXTEND.
K3 A3: ans=-2, zero adapted. K4 A4: passes, zero type-16, bracket
inert. K5 A5: ans=-2, zero adapted. K6 A6/A7/A8: all -2. K7 A9:
106/106, adapted count stable at 1. K8 A10: all 11 assertions
pass; unused adaptation provably not composed (no LINK14 to t).
K9: 3/3 byte-identical runs both binaries (shas above). K10: zero
em/en dashes in all authored deliverables (byte-verified); the
only em dashes in the lane are compiler-emitted warning text
inside the two znc build logs (unavoidable toolchain output; the
base files that trigger the warnings are frozen read-only). K11:
cc_base.zag
dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
and un_patch.zag
3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2,
both used verbatim via build concatenation, never modified
(re-verified after the run). K12: 0 new edge/MAP types, 0 new
opcodes, 0 modes, 0 bridges, 0 handlers, 0 semantic cases; the
patch's link_edge calls use only pre-existing types (1, 2, 6, 8,
13, 16); 14/15 come from the unchanged compose_try re-run.
K13: per-arm driver assertions on strict-prefix parentage
(truncate: adapted strict prefix of source; extend: source
strict prefix of adapted), exactly one type-16 edge per adapted
MAP to live native MAP_X, and licensing fact ids disjoint from
MAP_X training fact ids. A from-scratch rebuild cannot satisfy
parentage, provenance, fact-disjointness, and dedup together.

## Governance

Prereg committed ALONE first (commit ea6f894df, 2 files;
commit-order self-check: prereg strictly precedes
implementation). Implementation second, report third. Explicit
pathspecs on every commit; no git reset; nothing pushed. Base
files frozen read-only.

## Honest disclosures

1. Pre-freeze well-formedness prototype (throwaway, never
   committed, deleted after): exact pipeline on all five Z shapes
   gave -2/-2/-2/107/-2; walk primitives confirmed (3-hop walk
   101->104, 4-hop walk 101->105 plus frontier fact to 106,
   Y-license from 104/106/108). No selector/orchestration code
   was prototyped; frozen bars were not adjusted to fit outcomes.
2. /tmp was full (another worker's 457M arena worktree,
   untouched), so the prototype ran in ~/workspace/_scratch_xs3
   (outside the repo, deleted after the run).
3. Reading: XP-SELECT-2 prereg/patch/driver via git show for API
   surface and assertion patterns (documented in NAMECHECK.md);
   the XS3 selector, driver, and battery were designed from the
   frozen prereg, not copied.
4. During implementation review I caught one deviation before
   freezing results: the A8 driver query used expected=106 while
   the frozen battery says (101,70,107). Fixed to 107, rebuilt,
   re-ran 3/3; the kill bar (ans=-2) is met either way since no
   path to either value exists without X/Y. No frozen bar was
   weakened; the final evidence matches the frozen battery
   exactly.
5. K10 disclosure as above (compiler-emitted em dashes in build
   logs only).

## Scope (honest boundaries)

One domain pair (causal to intervention), one mismatch family
(interface arity), two selectable operations. L2 adaptive reuse
with operation selection, not L3 invention: the operations are
researcher-defined; the selection among them by satisfiability
evidence is the learner's. The adaptation changes X's interface
arity; the cross-domain license (Y strictly satisfying from the
adapted endpoint) is what re-keys the causal variable to the
intervention action space. Follow-up candidates: a third
mismatch family on this pair (e.g. keying with unequal arity),
or the arity family on a third pair.
