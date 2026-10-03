# PREREG: Valley Satisfiability Search (bounded)

Date: 2026-09-30. Status: PREREG. Frozen on commit. No search is run
by this commit. No validation verdict is authorized by this commit.
Authority: VALLEY-REDESIGN-FAIL (prereg 0310c7076, validation
ea920137b): 0/10 accepted, all failed V3 with concrete 1- or 2-edit
solvers; three architectural lemmas (3-op solver, 1-gate, MOD/DIV
universality). This prereg adopts the recommended next step: freeze
the V3 checker as an oracle and run a bounded search over
(target, canonical-path) pairs with L <= 11.

## 1. Oracle-freezing method (frozen)

The V3 enumeration logic is used BYTE-IDENTICAL. Build input is the
concatenation: myinst.zag + v2gen_frozen.zag, where v2gen_frozen.zag
is extracted via
`git show ea920137b:docs/lab/research-lead/overnight-20260928/valley_redesign2/v2gen.zag`
and must sha256 to
a93f9cd624294b7e1e2c475b392024e300f1a8be05173438979b8c6fc37604a9
before compiling; the build aborts otherwise. The build script
re-verifies by diffing the v2gen section of the concatenated input
against the extracted blob. myinst.zag supplies ONLY the instance
table (v2_nep, v2_in0, v2_in1, v2_tgt, v2_p0_op, v2_p0_arg,
v2_p0_len, v2_cpath, v2_kind, v2_depth, v2_s0_frozen, v2_n) plus
verbatim copies of the generic helpers from frozen v2inst.zag
(sha256 2b9b8bca05ffb88bd39fad1cff2dd1fed922833573e9d516c7486bf09b54e5a4:
v2_get32, v2_set32, v2_alloc, v2_emit, v2_e64, v2_nl,
v2_mod_nonneg, v2_vm_run, v2_score, v2_s0), confirmed by diff to be
identical. No validation logic (v2_v1, v2_v2, v2_v3,
v2_v3_second, v2_is_f_prefix, v2_v4a, v2_v4g, v2_v4,
v2_validate_one, main, alphabet, VM) is altered in any byte.
The frozen main drives v2_validate_one over all ids; id 0 is a
CAL-0 clone (section 2) as harness sanity.

## 2. Candidate table (frozen, 72 ids)

Opcodes: 0=PUSH 1=IN0 2=IN1 3=ADD 4=SUB 5=MUL 6=DIV 7=MOD 8=NEG
9=DUP 10=DROP 11=SWAP 12=OVER 13=LT 14=EQ 15=GT. P0=[PUSH 0] for
all ids. Single input x=e. depth=2 for ids >= 1.

id 0 (CAL-0 clone): nep=9, x in 0..8, tgt=x. cpath=[IN0]. kind=0.

F1 quadratic residue (ids 1..30): for pro in {A,B,C}, m in {5,7},
k in 1..m-1. id = 1 + pro*10 + (k-1 if m=5 else 4+(k-1)).
nep=2m+1, x in 0..2m, tgt = 1 iff (x*x) mod m == k.
core = [IN0,DUP,MUL,PUSH m,MOD,PUSH k,EQ] (7 ops).
A: cpath=core (L=8). B: cpath=[DROP]+core (L=9).
C: cpath=[PUSH 7,PUSH 5,DROP]+core (L=11). kind=1.

F2 two-point (ids 31..33): (a,b) in {(3,11),(5,13),(2,14)}.
id = 31+ab. nep=16, x in 0..15, tgt = 1 iff x==a or x==b.
cpath = [DROP,IN0,PUSH a,SUB,IN0,PUSH b,SUB,MUL,PUSH 0,EQ]
(L=11). kind=2. Prologue B only (A proven dead, section 3).

F3 shifted residue (ids 34..63): a=1, for pro in {A,B,C},
m in {5,7}, k in 1..m-1. id = 34 + pro*10 + (k-1 if m=5
else 4+(k-1)). nep=2m+1, x in 0..2m,
tgt = 1 iff (x+1) mod m == k.
core = [IN0,PUSH 1,ADD,PUSH m,MOD,PUSH k,EQ] (7 ops).
A: L=8. B: L=9. C: L=11. kind=3.

F4 cubic residue (ids 64..71): for pro in {A,B}, k in 1..4.
id = 64 + pro*4 + (k-1). nep=10, x in 0..9,
tgt = 1 iff (x*x*x) mod 5 == k.
core = [IN0,DUP,DUP,MUL,MUL,PUSH 5,MOD,PUSH k,EQ] (9 ops).
A: L=10. B: L=11. kind=4.

## 3. Lemma-exclusion audit (frozen)

L1 (3-op solver lemma): every target needs >= 4 ops after IN0
(F1: DUP,MUL for x^2 then MOD then compare; F2: two SUBs then
MUL then compare; F3: ADD then MOD then compare; F4: x^3 needs
4 ops). No [IN0,X,Y] 3-op program computes any target: X,Y
offer at most one nonlinear step or one compare, never the
required nonlinear-then-mod-then-compare chain; the
negative-divisor MOD coincidence ([IN0,PUSH -C,MOD] = x mod C
for x >= 0) yields x mod C, not x^2 mod m or (x+1) mod m
patterns, and is in the oracle's 2-edit alphabet regardless.
L2 (1-gate lemma): no canonical path exposes two computed 0/1
bits on any proper prefix; the only bit-producing op is the
final EQ. Residue values are integers, not bit pairs.
L3 (MOD/DIV universality): canonical MOD divisors are all
positive; no negative-divisor tables in canonical paths.
Prologue C is the designated repurposing-stress control.
Proven-dead exclusions (not searched): (i) k=0 in F1/F3/F4:
1-edit append EQ after the MOD prefix computes (r==0)=T and is
not a canonical prefix; (ii) F2 prologue A: 2-edit [MUL,EQ]
from [0,x-a,x-b] reuses the prologue 0 to compute
((x-a)(x-b)==0)=T, not a canonical prefix.

## 4. Procedure and budget (frozen)

BUILD.sh extracts and hash-verifies the oracle, concatenates,
compiles with the pinned znc, runs the binary 3 times,
sha256sums the three logs. Per-candidate gates run in frozen
order V1, V2, V3, V4 with early exit; a candidate counts as
FOUND iff V1, V2, V3 all PASS (V4 reported separately as
calibration info). CAL-0 (id 0) must pass or the run is void.
Budget: 71 search candidates + CAL-0. Run 1 doubles as timing
pilot; if one run exceeds 90 minutes wall time, the verdict is
INCOMPLETE (K2 fails) and the table is trimmed in a new prereg.

## 5. Verdicts (frozen)

VALLEY-SATSEARCH-FOUND: >= 1 candidate id >= 1 with V1, V2, V3
all PASS, committed with the per-gate frozen output as proof;
mechanism runs may then be proposed on accepted instances.
VALLEY-SATSEARCH-UNSATISFIABLE: zero candidates pass V1-V3
across the full table; the report carries the exact coverage
argument (families, params, prologues enumerated above) and an
analysis of the failure modes toward a general obstruction.
No claim is made about targets outside the frozen table. The
battery stays void unless FOUND.

## 6. Governance (frozen)

Pure Zag throughout: no Python in implementation, search,
measurement, analysis, or byte checks. Dash checks use only
worker_snippets/check_no_dash.sh. The contaminated research
paper is never touched. Owned path:
docs/lab/research-lead/overnight-20260928/valley_satsuch/.
Step 0 name-check is in STEP0_NAMECHECK.md. If a live
.git/index.lock is met, wait and retry; never remove it.

## 7. Kill bars (frozen)

K1: this prereg committed alone; strictly precedes any
implementation commit (verified with git merge-base
--is-ancestor).
K2: one of the two section-5 verdicts reached with committed
evidence (per-candidate frozen gate outputs, 3/3 byte-identical
logs).
K3: pure Zag, zero Python, dash-clean per the shell-only
snippet; the frozen V3 oracle byte-identical (section-1
verification in BUILD.sh).
