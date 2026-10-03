# PREREG: GEN-REDIM -- Dynamic Arena Re-dimensioning for the Frozen GEN Composer

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Steps 0-2) strictly precedes all
implementation. Worker: gen-redim. Date: 2026-10-03.

## 1. Question

GEN-STRESS (verdict BOUNDARY-FOUND (ARENA-4MAP), 2026-10-03) proved the frozen
GEN artifact cannot address 5 or more structures: its scratch arena is
hard-dimensioned for 4 MAPs in four places (MAP table 776+m*40 aliasing the
936/940/944 counters at m>=4; m2g table 968+m*12 sized for 4; tried1
2304+(m*64+i)*4 sized for 4, aliasing tried2/nv/widened/visit regions at
m>=4 and overflowing the 4096-byte arena at m=7). At nm=5..7 the mechanism
produces deterministic silent corruption; at nm=8 it panics. The
compositional rules (admission, rounds, widening, pool dedup, recording)
were never the limiting factor.

This battery builds the GEN successor GEN-STRESS called for: the same
composer with a DYNAMIC, NM-parameterized scratch layout. It then runs the
GEN-STRESS S1-S5 battery against the original predictions, plus the frozen
nm<=4 batteries as byte-identity regressions.

## 2. The dynamic layout (frozen spec; the only authorized change)

NM (the structure count for the query) is stored at arena offset 772
(4 bytes; previously unused -- the fact store ends at 772). Every region
base after the MAP table is an affine function of NM. The MAP table itself
keeps base 776 and stride 40 (it grows in place; no formula change).

Frozen region formulas (all offsets in bytes, 4-aligned):

```
NM        = get32(A,772)
TRIES     = 776 + NM*40
FOUND     = 776 + NM*40 + 4
ANS       = 776 + NM*40 + 8
CLBASE    = 776 + NM*40 + 12        (class list, NM*4 bytes; vestigial,
                                     unused by any code path, kept placed)
NCLASS    = CLBASE + NM*4
M2GBASE   = NCLASS + 4              (NM*12 bytes)
VPOOL     = max(1024, M2GBASE + NM*12)   (64*4 bytes)
KPOOL     = VPOOL + 256             (64*4)
PROV      = KPOOL + 256             (64*3*4)
TRIED1    = PROV + 768              (NM*64*4 bytes)
TRIED2C   = TRIED1 + NM*256         (4 bytes; 64-entry cap UNCHANGED)
TRIED2E   = TRIED2C + 4             (64*4 bytes)
NV        = TRIED2E + 256           (4 bytes)
WID       = NV + 4                  (4 bytes)
VSTACK    = WID + 4                 (64 bytes, UNCHANGED)
DONESET   = VSTACK + 64             (64 bytes, UNCHANGED)
ARENASZ   = DONESET + 64
world_new_nm(nm): z_alloc(ARENASZ(nm)); set32(A,772,nm); return A.
```

Regions are pairwise disjoint by construction (each base is the previous
base plus the previous exact size). The tried2 64-entry cap, the pool
64-value cap, the 64-slot visit stack, and the 6-round cap are pre-existing
resource bounds, NOT 4-dimensioned defects; they are unchanged (GEN-STRESS
mapped them as independent boundaries: WIDEN, POOL).

NM=4 reproduction proof (the reduction anchor). Substituting NM=4:
TRIES=936, FOUND=940, ANS=944, CLBASE=948, NCLASS=964, M2GBASE=968,
VPOOL=max(1024,1016)=1024, KPOOL=1280, PROV=1536, TRIED1=2304,
TRIED2C=3328, TRIED2E=3332, NV=3588, WID=3592, VSTACK=3596,
DONESET=3660, ARENASZ=3724. Every frozen offset is reproduced exactly,
so at NM=4 the successor addresses byte-identical storage to the frozen
artifact. (ARENASZ=3724 < 4096; all accesses are below 3724, so the
smaller allocation is behaviorally identical.)

## 3. Mechanism identity (frozen; what changes and what does not)

CHANGES (arena addressing only):
- New accessor fns r_nm, r_tries, r_found, r_ans, r_clb, r_ncl, r_m2g,
  r_vp, r_kp, r_pv, r_t1, r_t2c, r_t2e, r_nv, r_wid, r_vs, r_dn,
  r_size_nm, and world_new_nm (in rbase.zag).
- m2g/m2p: base 968 -> r_m2g(A).
- In rgen.zag, every absolute scratch literal becomes the corresponding
  accessor call: 936->r_tries(A), 940->r_found(A), 944->r_ans(A),
  1024->r_vp(A), 1280->r_kp(A), 1536->r_pv(A) (+4/+8 for the -1 slots),
  2304->r_t1(A), 3328->r_t2c(A), 3332->r_t2e(A), 3588->r_nv(A),
  3592->r_wid(A), 3596->r_vs(A), 3660->r_dn(A).
- world_new() is replaced by world_new_nm(nm) (callers pass the query's
  nm). The old main in rgen.zag has its world_new() calls updated to
  world_new_nm(2)/world_new_nm(4) per query (it is stripped in all
  assemblies; the change keeps the file self-consistent).
- Layout comments updated to the Section 2 formulas.

DOES NOT CHANGE:
- mg/mp (776+m*40+f*4) -- the MAP table formula is already NM-general.
- The tried2 pair encoding m*4096+i*64+j.
- Admission (g_khas, empty=compatible), trial order (id order; 1-input
  MAPs then 2-input MAPs; lex pair order), round snapshots, quiet-round
  detection, WIDEN=1 once, success recording with provenance closure,
  observe/observe2 contract growth, exec_map/exec_map2, walkf,
  count_rel, pkind, teaching, all world setups, output formatting.
- No new behavior classes, opcodes, admission dimensions, modes, flags,
  or shape predicates. No new branches in any trial/record path.

Consequence: at NM<=4 the successor MUST print byte-identical stdout to
the frozen artifact on every battery (kill bars C3, C4, C7, C9). Any
divergence there is a logic change, not a re-dimensioning.

## 4. Opaque naming (frozen; kill bar C11)

Same scheme as GEN-STRESS Section 4: structures m0..m7, relations bare
integers 91..98, entities bare integers, queries S1..S5. No structure,
relation, or entity identifier carries human task semantics. Forbidden
tokens (case-insensitive grep over all built sources, PREREG, REPORT):
hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|
language|audio|interven|belie|goal|agent.

## 5. Batteries

### 5.1 Frozen nm<=4 regressions (byte-identity)

- DIAMOND: rbase.zag + rgen (main stripped) + rd_dmain.zag
  (byte-exact setups of the frozen diamond battery; world_new_nm(2/4)).
  Target: stdout byte-identical to gen_cycles/ref_diamond_out.txt
  (sha256 962ca4f0...).
- GENERALITY: rbase.zag + rgen (main stripped) + rd_gmain.zag
  (byte-exact generality setups; world_new_nm(4)).
  Target: stdout byte-identical to gen_cycles/ref_gg_out.txt
  (sha256 4b81226d...).

### 5.2 GEN-STRESS battery (S1-S5; the original predictions)

Driver rd_smain.zag: setup_s1..setup_s5 byte-exact extracts from the
frozen gen_stress/gs_new.zag; main runs S1..S5 on fresh worlds via
world_new_nm(6,6,3,8,4); single o_flush at end. Report labels
"GEN","S1".."S5" unchanged.

S1 (s=201, exp=2, nm=6): 5-chain. Predicted PASS: ANS=2, TRIES=29, no
WIDEN, exact block:

```text exp-S1
INTER=211
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=201
INTER=-2
INTER=212
INTER=-2
INTER=-2
INTER=-2
INTER=211
INTER=-2
INTER=-2
INTER=213
INTER=-2
INTER=-2
INTER=212
INTER=-2
INTER=-2
INTER=-2
INTER=214
INTER=-2
INTER=213
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=2
ARM=GEN PROB=S1 ANS=2 TRIES=29
```

S3 (s=205, exp=207, nm=3): near-miss. Predicted (as on frozen):
WIDEN=1, ANS=207, TRIES=8, exact block:

```text exp-S3
INTER=2
INTER=205
INTER2=410
WIDEN=1
INTER=-2
INTER=-2
INTER=2
INTER=410
INTER2=207
ARM=GEN PROB=S3 ANS=207 TRIES=8
```

S4 (s=201, exp=2, nm=8): 7-chain, 7 rounds needed, cap is 6. Predicted
CLEAN DECLINE: ANS=-2, TRIES=48, no WIDEN=1 line, exact block:

```text exp-S4
INTER=211
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=201
INTER=-2
INTER=212
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=211
INTER=-2
INTER=-2
INTER=213
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=212
INTER=-2
INTER=-2
INTER=-2
INTER=214
INTER=-2
INTER=-2
INTER=-2
INTER=213
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=215
INTER=-2
INTER=-2
INTER=214
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=216
INTER=-2
INTER=215
ARM=GEN PROB=S4 ANS=-2 TRIES=48
```

S5 (s=201, exp=999999, nm=4): pool-cap load. Predicted (as on frozen):
ARM line EXACTLY `ARM=GEN PROB=S5 ANS=-2 TRIES=2734`, exactly 3 INTER=
lines, exactly 2731 INTER2= lines, zero WIDEN=1 lines.

## 6. S2 prediction correction (preregistered BEFORE any run)

GEN-STRESS's S2 block (51 lines, ANS=219 TRIES=48) is reproduced here
for reference; it is NOT the kill-bar target, because it contains
hand-derivation errors against the frozen rules it claims to derive
from. The errors, each checkable against ref_gs_gen.zag:

E1. R3 1-input overcount. The derivation counts m2 and m4 trying on
pool values 3 and 2 (kind 2 = NUM). But m2's learned contract is
in{1} (teach(m2,211,214): 211 is a fact subject, kind 1) and m4's is
in{1} (teach(m4,202,211)); g_khas({1},2)=0, so both are
kind-REJECTED on 3 and 2: no try, no INTER line, not marked tried.
The derivation's "m2 on 3,2,214: -2,-2,-2 / m4 on 3,2,214: -2,-2,-2"
(6 tries) should be 2 tries (on 214 only). 4 phantom tries.

E2. R4 1-input overcount. The derivation counts "m2/m4 on the 8 new
NUMs: -2 each (16 tries)". The 8 new pool values
(205,217,204,213,216,6,5,4) are all kind 2; m2/m4 admit only kind 1.
All 16 are rejected: 0 tries, 0 lines. 16 phantom tries.

E3. R4 pool order. The derivation lists the R4 pool as
[202,211,3,2,214,6,5,4,205,217,204,213,216], placing m5's sums before
m3's. But gen_round runs 2-input MAPs in id order: m3's pairs execute
before m5's in R3, so 205 is pool index 5, not 9. The derivation's
R4 pairs "(5,0): 208 ... (6,4): 219" index the wrong values; per the
rules (5,0) = 205+202 = 407.

E4. Internal inconsistency: the block holds 50 INTER/INTER2 lines but
its ARM line claims TRIES=48; the derivation text implies 8 R3
1-input tries while the block shows 10 such lines.

The block was never empirically observed (frozen S2 actual: ANS=-2
TRIES=62 with spurious WIDEN=1, the arena corruption). The corrected
prediction below is derived directly from the frozen rules in
ref_gs_gen.zag (admission per observed kind; id order; 1-input MAPs
then 2-input MAPs in id order; lex pair order; round snapshots;
rejected-not-tried). Because kill bars C3/C4/C7/C9 prove the
successor's logic byte-identical to frozen at NM<=4, this corrected
block is what the frozen rules faithfully executed would print.

Corrected S2 derivation (s=202, exp=219, nm=6). Contracts:
m4 in{1} out{1}; m0 in{1} out{2}; m1 in{1} out{2}; m2 in{1} out{1};
m5 in1{2} in2{2} out{2}; m3 in1{2} in2{1} out{2}. Kind-1 values: 202,
211, 214 (214 via the (214,95,241) fact).

R1 (pool [202]): m0: -2; m1: -2; m2: -2; m4: 211 (pool+=211). m3/m5:
(0,0) kind-rejected. 4 tries.
R2 (pool [202,211]): m0: 3 (pool+=3); m1: 2 (pool+=2); m2: 214
(pool+=214); m4: -2. m3/m5 pairs kind-rejected. 4 tries.
R3 (pool [202,211,3,2,214]): m0/m1/m2/m4 on 214: -2 x4 (3 and 2 are
kind-rejected; 202/211 already tried). m3 (in1{2} in2{1}):
(2,0)=205 add, (2,1)=214 dup, (2,4)=217 add, (3,0)=204 add,
(3,1)=213 add, (3,4)=216 add. m5 (in1{2} in2{2}):
(2,2)=6 add, (2,3)=5 add, (3,2)=5 dup, (3,3)=4 add. 14 tries.
Pool is now [202,211,3,2,214,205,217,204,213,216,6,5,4].
R4: 1-input MAPs: 0 tries (kind-1 values already tried; new values
all kind 2, rejected). m3: (5,0)=407 add, (5,1)=416 add,
(5,4)=419 add, (6,0)=419 dup, (6,1)=428 add, (6,4)=431 add,
(7,0)=406 add, (7,1)=415 add, (7,4)=418 add, (8,0)=415 dup,
(8,1)=424 add, (8,4)=427 add, (9,0)=418 dup, (9,1)=427 dup,
(9,4)=430 add, (10,0)=208 add, (10,1)=217 dup, (10,4)=220 add,
(11,0)=207 add, (11,1)=216 dup, (11,4)=219 = exp SUCCESS.
21 tries. No quiet round, so no WIDEN.
Total: 4+4+14+21 = 43 tries. ANS=219.

Frozen corrected S2 block (kill-bar target):

```text exp-S2
INTER=-2
INTER=-2
INTER=-2
INTER=211
INTER=3
INTER=2
INTER=214
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER2=205
INTER2=214
INTER2=217
INTER2=204
INTER2=213
INTER2=216
INTER2=6
INTER2=5
INTER2=5
INTER2=4
INTER2=407
INTER2=416
INTER2=419
INTER2=419
INTER2=428
INTER2=431
INTER2=406
INTER2=415
INTER2=418
INTER2=415
INTER2=424
INTER2=427
INTER2=418
INTER2=427
INTER2=430
INTER2=208
INTER2=217
INTER2=220
INTER2=207
INTER2=216
INTER2=219
ARM=GEN PROB=S2 ANS=219 TRIES=43
```

Census after S2 (for REPORT cross-check, not a kill bar): m0..m5 each
n=2 (one teach + one provenance-closure observe); in/out masks as in
Section 6 header; m3 inmask2=1.

## 7. Construction sequence (implementation follows this prereg commit)

1. ref_rd_base.zag, ref_rd_gen.zag, ref_gs_new.zag: byte-copies of the
   gen_stress frozen files; sha256 must match NAMECHECK.md Step 1.
2. rbase.zag: ref copy + Section 2 accessor fns + m2g/m2p rebase +
   world_new -> world_new_nm + comment updates (Section 3 list).
3. rgen.zag: ref copy + Section 3 literal->accessor substitutions +
   old-main world_new_nm updates.
4. rd_dmain.zag: frozen diamond driver with world_new_nm(2/4);
   rd_gmain.zag: frozen generality driver with world_new_nm(4);
   rd_smain.zag: byte-exact setup_s1..setup_s5 extracts + main with
   world_new_nm(6,6,3,8,4), labels GEN/S1..S5, single o_flush.
5. Assemblies: rd_dfull = rbase + rgen-minus-main + rd_dmain;
   rd_gfull = rbase + rgen-minus-main + rd_gmain;
   rd_sfull = rbase + rgen-minus-main + rd_smain.
   (main stripped via sed '/^fn main()i32 {/,$d', as GEN-STRESS did.)
6. build.sh encodes all audits fail-closed (set -e): digest checks,
   region diffs, minimal-diff allowlist audit (Section 8 C10),
   opacity grep, znc compiles, 3x runs with pairwise cmp, expected
   block extraction from THIS prereg (awk on the ```text exp-SN
   fences) + transcription check against the gen_stress originals
   for S1/S3/S4, section split + cmp, S5 line counts.
7. REPORT.md with verdict per Section 9.

## 8. Frozen kill bars

- C1 COMMIT-ORDER: PASS iff this prereg commit (PREREG.md +
  NAMECHECK.md Steps 0-2 ONLY) strictly precedes all implementation
  commits on branch lane-genredim-20261003.
- C2 DETERMINISM: PASS iff 3/3 runs of each binary (rd_dbin,
  rd_gbin, rd_sbin) are pairwise byte-identical (cmp); digests
  recorded; stderr empty.
- C3 DIAMOND-REGRESSION: PASS iff rd_dbin stdout is byte-identical
  (cmp, empty diff) to gen_cycles/ref_diamond_out.txt.
- C4 GENERALITY-REGRESSION: PASS iff rd_gbin stdout is byte-identical
  to gen_cycles/ref_gg_out.txt.
- C5 STRESS-S1: PASS iff the S1 section of rd_sbin stdout is
  byte-identical to the Section 5.2 exp-S1 block (ANS=2, TRIES=29,
  no WIDEN).
- C6 STRESS-S2: PASS iff the S2 section is byte-identical to the
  Section 6 corrected exp-S2 block (ANS=219, TRIES=43, no WIDEN).
- C7 STRESS-S3: PASS iff the S3 section is byte-identical to the
  Section 5.2 exp-S3 block (WIDEN=1, ANS=207, TRIES=8).
- C8 STRESS-S4: PASS iff the S4 section is byte-identical to the
  Section 5.2 exp-S4 block (ANS=-2, TRIES=48, no WIDEN=1 line).
- C9 STRESS-S5: PASS iff the S5 section ends with EXACTLY
  `ARM=GEN PROB=S5 ANS=-2 TRIES=2734`, contains exactly 3 INTER=
  lines, exactly 2731 INTER2= lines, and zero WIDEN=1 lines.
- C10 MINIMAL-DIFF: PASS iff the unified diffs ref_rd_base.zag ->
  rbase.zag and ref_rd_gen.zag -> rgen.zag contain ONLY: (a) the new
  Section 2 accessor fns; (b) literal->accessor substitutions from
  the Section 3 list; (c) world_new -> world_new_nm (+ call-site nm
  args); (d) layout comment updates. Audit: every added/removed line
  matches the allowlist (accessor defs, r_* calls, world_new_nm,
  comments); REPORT records the diffstat and the audit method.
- C11 OPACITY: PASS iff grep over all built sources (rbase.zag,
  rgen.zag, rd_dmain.zag, rd_gmain.zag, rd_smain.zag), PREREG.md and
  REPORT.md for the Section 4 banned tokens (case-insensitive)
  returns empty, and every exercised identifier is a bare integer.

## 9. Verdict mapping (frozen)

- C1 FAIL -> VOID. Commit order broken; re-freeze.
- C2 FAIL -> UNDECIDED. Name the decisive rerun.
- C10/C11 FAIL -> VOID (C10) / BUILD-FAIL (C11). The change was not
  minimal or broke naming discipline.
- C3 or C4 FAIL -> FAIL (regression): the re-dimensioning altered
  NM<=4 semantics. The successor is not a pure re-dimensioning.
- C3+C4+C7+C9 PASS but C5/C6/C8 FAIL -> the logic is proven identical
  to frozen, so the failure is isolated to the NM>=5 addressing or to
  the prereg derivation. REPORT re-derives the failing section from
  the frozen rules by hand; if the binary's trace follows the rules,
  the verdict is INFORMATIVE with the corrected trace and the
  prereg block is amended transparently (never weakened to fit).
- C1-C11 all PASS -> PASS: GEN-REDIM executes the frozen GEN rules
  faithfully at NM=5..8. S1 now passes (5-chain), S2 now passes
  (6-structure DAG, corrected trace), S4 declines cleanly at the
  round cap as originally predicted, S3/S5 reproduce their frozen
  outcomes. The 5/10+ structure question is unblocked at the arena
  level: the addressable limit is now ARENASZ(NM), not 4.

## 10. Honest boundaries (pre-declared)

- Behaviors installed as previously-learned MAPs (canonical standing);
  expected-answer verification of acceptance (canonical boundary).
- GEN is researcher-implemented (GEN-STRESS boundary holds): the claim
  is only that the re-dimensioned artifact executes the frozen rules
  at 5-8 structures, not that a learner invented anything.
- Exactly one generic 2-input class (ADD2), reused unchanged.
- Unchanged pre-existing bounds: 64-value pool (silent drop),
  64-entry tried2 (retry inflation), 64-slot visit stack, 6-round cap.
  S5 re-verifies the first two; the visit-stack bound is not stressed
  by S1-S5 (provenance closures stay shallow).
- NM>8 is not exercised: the layout formulas are NM-general, but the
  battery stops at 8. The tried2 encoding m*4096+i*64+j is unchanged
  and NM-general.
- S5's INTER2 listing is not hand-enumerated (as in GEN-STRESS); the
  bar is the exact TRIES count, exact line counts, absence of WIDEN,
  and 3/3 byte-identical determinism.
- WIDEN semantics are unchanged: S3 still yields the contract-violating
  success (GEN-STRESS BOUNDARY-FOUND (WIDEN) stands as characterized).
