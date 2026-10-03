# REPORT: H1-L2 Integration (learned type contracts drive adaptation)

## Verdict: H1-L2-INTEG-COMPLETE. All 6 frozen kill bars PASS.

Date: 2026-10-02. Worker: H1-L2 Integration Worker.
Prereg: PREREG.md, commit 43f744aee (committed alone, strictly before
implementation). Branch: tnn-native-lab, local only, nothing pushed.

## What was built

`hl.zag` (single file, ~470 lines): H1's signature learner (probe_kind
observations, majority finalize, generic contract composition at promotion)
plus L2-style adaptation operators whose TRIGGER is the learned contract
mismatch at a composition seam and whose SELECTION is driven by the
mismatch type. Six previously-learned procedures: X chain-follow (1->1),
Y double (2->2), E count-81 (1->2, distractor adapter), C count-82 (1->2,
adapter), D subject-index (2->1, adapter), D1 identity (1->1). New generic
machinery: map behavior 6 (triple application A;P;B), the mismatch
detector (reads only learned sig slots), and the bridge selector
OP12/OP21. The ablation build `hl_na.zag` differs by exactly one line
(`type_on` 1 to 0), verified by diff, mirroring the L2 lane's methodology.

## Results

3/3 byte-identical runs per binary.
hl_bin runs sha256 `ab27cab5d0e287261777460a9bdf1e6fe9a818ce514f99f84611faadebe3ae66`.
hl_na_bin runs sha256 `e5c4ec75abbcbe5ba7cafe26b0766a8fc427d06251bdefbe172f9649df653c23`.

- TREAT-Z1 (31->4): PASS ans=4 tries=10. Well-typed singles/pairs all fail
  on value. MISMATCH a=0 b=1 have=1 need=2 fires at the (X,Y) seam; OP12
  selects 1->2 adapters by learned contract: p=2 (E) tried, triple gives
  0, rejected; p=3 (C) wins, triple X;C;Y = 34->2->4. Z-COMP3 z=6 a=0 p=3
  b=1, composite contract 1->2.
- TREAT-Z2 (43->34): PASS ans=34 tries=13. MISMATCH a=3 b=0 have=2 need=1
  fires at the (C,X) seam; OP21 selects the 2->1 adapter p=4 (D): triple
  C;D;X = 3->33->34. Z-COMP3 z=6 a=3 p=4 b=0, composite contract 1->1.
  (The trace also shows the learner honestly working through two failing
  OP21 attempts on (E,X) and (E,D1) and two failing OP12 attempts on (X,D)
  before the winner; selection is by contract plus execution check, not
  by luck of ordering.)
- ABL-C (adapter C deleted): PASS-expected-fail ans=-2. Only 1->2 adapter
  left is E; its triple fails; Z-FAIL.
- ABL-D (adapter D deleted): PASS-expected-fail ans=-2. NO-BRIDGE on all
  three (2,1) seams; Z-FAIL.
- FRESH (no teaching): PASS-expected-fail ans=-2, zero tries.
- REUSE-Z1: PASS ans=4 both solves; second solve via Z-SINGLE m=6
  (the promoted composite reused directly).
- NOTYPE-Z1: PASS-expected-fail ans=-2 tries=43. Trace shows the wrong
  operator: the ill-typed direct pair TRY2 a=0 b=1 r=68 executed across
  the mismatch, then BLIND-BRIDGE a=0 b=1 p=2 r=0 fails, Z-FAIL.
- NOTYPE-Z2: PASS-expected-fail ans=-2 tries=43. Closest blind call was
  (C,D) giving 33; blind bridge gives 0; Z-FAIL.

## Kill bars

- K-HL-1: PASS. TREAT-Z1 trace has MISMATCH a=0 b=1 have=1 need=2;
  TREAT-Z2 trace has MISMATCH a=3 b=0 have=2 need=1. Both mismatch
  directions exist as composition problems.
- K-HL-2: PASS. have/need values equal the learned signatures printed by
  the TEACH lines (m0 1->1, m1 2->2, m3 1->2, m4 2->1). The detector reads
  only sig_in/sig_out slots; no researcher per-problem flag exists in
  source (audit: the strings MISMATCH/BRIDGE-SEL are emitted with values
  computed from the signature slots).
- K-HL-3: PASS. Z1: BRIDGE-SEL OP12 lines select p with learned sig 1->2
  (m2 tried and rejected on value, m3 wins); winning triple Z-COMP3
  (0,3,1). Z2: BRIDGE-SEL OP21 selects p=4 with learned sig 2->1;
  winning triple Z-COMP3 (3,4,0). The operator (OP12 vs OP21) follows the
  mismatch kind pair, and the adapter follows the needed bridge
  signature.
- K-HL-4: PASS. TREAT-Z1 ans=4; in-code provenance check confirms
  comp_a=0, comp_b=3, comp_c=1 and composite contract 1->2. TREAT-Z2
  ans=34; comp_a=3, comp_b=4, comp_c=0 and composite contract 1->1.
- K-HL-5: PASS. NOTYPE-Z1 ans=-2 with TRY2 a=0 b=1 r=68 (wrong operator:
  direct ill-typed composition across the mismatch) and failed
  BLIND-BRIDGE; NOTYPE-Z2 ans=-2.
- K-HL-6: PASS. 3/3 byte-identical per binary (sha256 above). Stdout
  bytes verified well-formed (no print-miscompile corruption); output
  uses the single-buffer emit plus one raw write syscall.

## Cost table (tries per arm, from run output)

| arm       | ans | tries | note                                  |
|-----------|-----|-------|---------------------------------------|
| TREAT-Z1  | 4   | 10    | 2 single + 6 pair + 2 bridge          |
| TREAT-Z2  | 34  | 13    | 2 single + 6 pair + 5 bridge         |
| ABL-C     | -2  | 7     | adapter missing, honest fail          |
| ABL-D     | -2  | 6     | NO-BRIDGE, honest fail                |
| FRESH     | -2  | 0     | nothing learned, nothing tried        |
| REUSE-Z1b | 4   | 3     | composite reused as single            |
| NOTYPE-Z1 | -2  | 43    | 6 + 36 blind + 1 blind bridge, fail   |
| NOTYPE-Z2 | -2  | 43    | same, fail                            |

Type-directed adaptation adds a small constant number of tries over the
H1 pair baseline; the blind ablation burns 43 tries and still fails.

## Architecture accounting

- Cognition lines added: ~200 in hl.zag (d_index, triple behav 6,
  mismatch detector, OP12/OP21 bridge selector, arms).
- New hardcoded semantic cases: 0. Behaviors 0..5 are previously-learned
  procedures (same status as xt.zag); signatures are learned from probe
  observations; the composite contract is generic composition.
- Modes, bridges, handlers: 0. `type_on` is a build-time constant
  selecting the arm set per binary, not a cognitive mode.
- Learner-state structures created: composite MAPs with comp_a/b/c
  provenance slots and derived contracts (learner-persistent state).

## Provenance

- Compiler: pinned `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (sha256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`,
  matches safebin znc).
- hl_bin sha256: `ad4edd8d0129ce1d74a265a5868a9881b53781f67b50e9ec5c4d8c5084081515`.
- hl_na_bin sha256: `4d68678598fccd56f22659ff05fdbb4197e509ac2f15c31bc77d2d7073eea6f0`.
- hl_na.zag differs from hl.zag by exactly one line (diff-verified).
- Pure Zag throughout; toolchain guard verified (no python3/python in
  worker PATH); output bytes verified against the znc print miscompile.

## Honest boundaries

- Behavior induction (how X/Y/E/C/D/D1 got their behaviors) is assumed as
  prior learning, exactly as in the H1 lane; the tested claim is
  mismatch-triggered, mismatch-typed adaptation.
- The typed operators OP12/OP21 are the typed analogues of L2's EXTEND
  (extend the plan with a bridging procedure). L2's TRUNCATE and
  SPECIALIZE are walk-level operators with no typed-seam counterpart in
  this battery; they are out of scope here, not subsumed.
- Adapter inventory is small (2..3 candidates per seam); the selection
  claim scales with inventory size but that scaling run is not done here.
- Kinds are binary (NODE/NUM) from the H1 syntactic probe; richer type
  lattices remain future work.
- The na build's blind bridge is a deliberately crude lesion control; it
  demonstrates the causal role of contracts, not an optimal blind
  strategy.
