# REPORT: xdomain_arith_plan -- Cross-Domain Arithmetic to Planning

## Verdict: XDOMAIN-ARITH-PLAN-COMPLETE

All 7 frozen kill bars PASS. 3/3 byte-identical runs.
SHA-256: `07495346457fd46409acf494bea518fc3187bbf1217c14decdff7a00c2ccd1f8`

## What was built

`ap.zag` (standalone, pure Zag, pinned znc): generality test of H1
(learned typed contracts) and H2 (value-level function composition)
on a new structurally-different domain pair.

- Domain X (arithmetic): SUM over `(s,71,v)` price facts. X(101)=15, X(102)=10.
- Domain Y (planning): ALLOC integer division `n/5` (packs affordable from
  budget). Y(15)=3, Y(10)=2, Y(7)=1.
- D1 (MAX distractor): same signature as X (NODE->NUM), wrong semantics.
  D1(101)=7.
- D2 (IDENT distractor): wrong signature (NODE->NODE).
- Sealed Z: (101,93)->3 requires X(101)=15 then Y(15)=3.
- Z2: (102,93)->2 requires X(102)=10 then Y(10)=2.

Behaviors installed as prior learning (per prereg honest boundaries);
under test is composition, not behavior induction. Mechanism logic
unmodified from H1/H2; only behavior implementations are new.

## Results

### Signatures learned (H1 mechanism, from probe observations only)
- X: 1->2 (NODE->NUM). Y: 2->2 (NUM->NUM).
- D1: 1->2 (NODE->NUM). D2: 1->1 (NODE->NODE).
All match prereg predictions. Zero per-MAP signature literals in source
(K4 audit: signatures only from `finalize_sig` computation and generic
contract composition in `promote_comp`).

### TREAT-TYPED (M1): PASS, 3 tries
- Singles: X(101)=15, D1(101)=7 (type filter admits only NODE->NUM).
- Pair (X,Y): 15->3. Composite z=4 promoted with provenance (a=0,b=1).
- Z2: solved via direct Z application (`T-SINGLE m=4`), 3 tries <= 3. Reuse.

### TREAT-VALUE (M2): PASS, 6 tries
- Singles: 15, 20, 7, 101 (no type filter; all tried).
- Pairs: (X,X)->0, then (X,Y): mid=15, r=3. Composite z=4, provenance (0,1).
- Z2: direct Z application (`V-SINGLE m=4`), 5 tries <= 6. Reuse.

### NOTYPE: PASS, 6 tries > 3 (K3a)
Type filter prunes the search: 6 tries without vs 3 with. The contract
is causally load-bearing on the new domain pair, not just chain-count.

### NOVC: PASS-expected-fail (K3b)
Singles only: 15, 20, 7, 101. None equals 3. Pair search is load-bearing
for M2.

### ABL-X: PASS-expected-fail, both solvers
Typed: (D1,Y)->1, (D2,D1)->7. All fail. D1 alone gives 7, not 3.
Value: all 9 pairs fail. X is causal.

### ABL-Y: PASS-expected-fail, both solvers
Typed: (D2,X)->15, (D2,D1)->7. All fail.
Value: all 9 pairs fail. Y is causal.

### FRESH: PASS-expected-fail, both solvers
No MAPs. Both solvers fail immediately.

## Kill bar verification

- K1 SOLVE: PASS. Both solvers produce composite (0,1) with correct provenance.
- K2 CAUSAL: PASS. ABL-X, ABL-Y, FRESH fail for both solvers, 3/3.
- K3 MECHANISM-CAUSAL: PASS. (a) NOTYPE 6 > TYPED 3. (b) NOVC fails.
- K4 LEARNED-NOT-ASSIGNED: PASS. Grep audit: no per-MAP signature literals.
- K5 DETERMINISM: PASS. 3/3 byte-identical.
- K6 NO-TEMPLATE: PASS. No ARITH_TO_PLAN in code (one comment disclaiming
  it). Composer functions contain no 101/102/15/3 literals.
- K7 REUSE: PASS. Z2 via direct Z: typed 3<=3, value 5<=6.

## Generality interpretation

H1 and H2 mechanism logic transferred unmodified to arithmetic->planning.
Both solve the sealed goal with correct causal provenance. The type
contract prunes search on the new pair (K3a), and pair search remains
load-bearing for value composition (K3b). This is per-mechanism generality
evidence, bounded as declared: one new domain pair, Level 1 (exact reuse)
composition, expected-answer verification.

## Honest boundaries (per prereg)

- Behavior implementations researcher-authored; composition is under test.
- Expected answers used for verification. Learner-owned verification future.
- Binary NODE/NUM kinds from syntactic probe.
- Level 1 only. Level 2 (adaptive) and Level 3 (novel intermediate) future.
- One domain pair. Does not establish arbitrary-domain generality.

## Files

- `PREREG.md` (frozen `aa708f552`, before implementation)
- `NAMECHECK.md` (Step 0 guard recorded)
- `ap.zag` (implementation, ~400 lines)
- `ap_bin` (pinned znc, exit 0)
- `compile.log`, `run1.txt`, `run2.txt`, `run3.txt` (byte-identical)

## Commits (local only, nothing pushed)

- Prereg: `aa708f552`
- Implementation + results: (this commit)

Toolchain: safebin active, `which python3 python` empty, pure Zag.
Zero em/en dashes (byte-verified). Paper untouched. Frozen read-only.
0 modes/bridges/handlers.
