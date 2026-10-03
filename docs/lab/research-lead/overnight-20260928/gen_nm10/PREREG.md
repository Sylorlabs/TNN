# PREREG: GEN-NM10 -- NM=10+ Batteries on the Canonical GEN-REDIM Composer

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Steps 0-2) strictly precedes all
implementation. Worker: gen-nm10. Date: 2026-10-03.

## 1. Question

GEN-REDIM (canonical per GEN-REDIM-CLEAN, C434) unblocked the 5/10+
structure question at the arena level: the dynamic NM-parameterized
layout executes the frozen GEN rules faithfully at NM=2,3,4,6,8, and the
addressable limit is now ARENASZ(NM), not 4. The worker's recommended
follow-up was NM=10+ batteries for the 10+ structure half.

This battery asks, at NM=11, with the layout formulas, the
m*4096+i*64+j tried2 encoding, and the 64-pool / 64-tried2 / 6-round
bounds all unchanged:

- B1: does the dynamic layout hold for a 10-chain (nm=11)? A 10-link
  chain needs 10 rounds; the round cap is 6. Predicted: clean decline
  at the round cap (ANS=-2), no corruption, no WIDEN.
- B2: does composition work at 10+ for a fan-out/fan-in DAG (nm=11)?
  Three chains (two 1-input chains and one COUNT-terminated chain)
  converge through one ADD2 structure inside 4 rounds. Predicted: PASS
  (ANS=315), 9 structures genuinely composing, 2 distractor structures
  live through every round.

Together they locate the binding limit at 10+: the 6-round cap (B1),
while the pool and tried2 bounds are NM-independent constants already
characterized by GEN-REDIM S5 (unchanged by construction).

## 2. What is reused unchanged

- The canonical GEN-REDIM sources rbase.zag and rgen.zag
  (implementation commit 341598554, verified by GEN-REDIM-CLEAN).
  This lane adds ONLY new driver mains; it does not copy, edit, or
  re-derive the mechanism. Assembly concatenates the canonical files
  with the new drivers. Kill bar N5 verifies the canonical sources
  are byte-identical to the canonical commit.
- Layout formulas (PREREG GEN-REDIM Section 2), tried2 pair encoding
  m*4096+i*64+j, 64-value pool cap (silent drop), 64-entry tried2 cap
  (retry inflation), 64-slot visit stack, 6-round cap, WIDEN-once
  semantics, admission (g_khas, empty=compatible), trial order
  (1-input MAPs in id order, then 2-input MAPs in id order; lex pair
  order), round snapshots, quiet-round detection, success recording
  with provenance closure. No new behavior classes, opcodes, modes,
  flags, or shape predicates.

NM=11 layout check (from the frozen formulas): TRIES=1216,
M2GBASE=1276, VPOOL=max(1024,1408)=1408, KPOOL=1664, PROV=1920,
TRIED1=2688 (2816 bytes), TRIED2C=5504, TRIED2E=5508, NV=5764,
WID=5768, VSTACK=5772, DONESET=5836, ARENASZ=5900. Regions pairwise
disjoint by exact size chaining. tried1 holds 11*64 entries; tried2
entries for m<=10 fit i32 (max 10*4096+63*64+63=45055).

world_new_nm invariant (GEN-REDIM REPORT Section 5): nm >= number of
MAPs the setup defines. Both setups define 11 MAPs; both drivers use
world_new_nm(11).

## 3. Opaque naming (frozen)

Structures m0..m10, relations bare integers 91..101, entities bare
integers, queries B1..B2. No identifier carries task semantics.
Forbidden tokens (case-insensitive grep over all new sources, PREREG,
REPORT): hypothesis|refine|evaluat|domain|plan|causal|navigat|
arithmet|grammar|language|audio|interven|belie|goal|agent.

## 4. Battery B1: 10-chain (nm=11)

Setup setup_b1 (new driver nm_b1main.zag):

```text
facts:
  201-91->211; 211-92->212; 212-93->213; 213-94->214; 214-95->215;
  215-96->216; 216-97->217; 217-98->218; 218-99->219;
  219-100->221; 219-100->222; 219-100->223;
  231-101->232
maps:
  m0 WALK(91)   teach(201,211)   in{1} out{1}
  m1 WALK(92)   teach(211,212)   in{1} out{1}
  m2 WALK(93)   teach(212,213)   in{1} out{1}
  m3 WALK(94)   teach(213,214)   in{1} out{1}
  m4 WALK(95)   teach(214,215)   in{1} out{1}
  m5 WALK(96)   teach(215,216)   in{1} out{1}
  m6 WALK(97)   teach(216,217)   in{1} out{1}
  m7 WALK(98)   teach(217,218)   in{1} out{1}
  m8 WALK(99)   teach(218,219)   in{1} out{1}
  m9 COUNT(100) teach(219,3)     in{1} out{2}
  m10 IDENT     teach(231,231)   in{1} out{1}
```

gen_solve(s=201, exp=3, nm=11). The chain end (m9 on 219) yields 3,
but reaching it needs 10 rounds (one link per round: values added
during a round are invisible until the next round snapshot). The cap
is 6, so the expected outcome is a clean decline exactly like
GEN-STRESS S4 at nm=8.

Derivation. All chain values are kind 1 (subjects); all MAPs admit
kind 1. Each round adds exactly one new pool value, so tried1 lets
each MAP try exactly the one new value per round: 11 tries/round.
R1: m0(201)->211; m1..m9 -> -2; m10(201)->201 (dup).
R2: m1(211)->212; m10(211)->211 (dup); rest -2.
R3: m2(212)->213; m10(212)->212 (dup); rest -2.
R4: m3(213)->214; m10(213)->213 (dup); rest -2.
R5: m4(214)->215; m10(214)->214 (dup); rest -2.
R6: m5(215)->216; m10(215)->215 (dup); rest -2.
Every round grows nv, so no round is quiet: no WIDEN=1. After round 6
the loop exits with found=0. TRIES = 6*11 = 66.

Predicted block (kill-bar target):

```text exp-B1
INTER=211
INTER=-2
INTER=-2
INTER=-2
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
INTER=-2
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
INTER=-2
INTER=-2
INTER=-2
INTER=215
ARM=GEN PROB=B1 ANS=-2 TRIES=66
```

## 5. Battery B2: fan-out/fan-in DAG (nm=11)

Setup setup_b2 (new driver nm_b2main.zag). Three chains fan out from
301 and converge through one ADD2 structure:

```text
facts:
  301-91->311; 311-92->312; 312-93->313          (chain A)
  301-94->321; 321-95->322; 322-96->341; 322-96->342   (chain B)
  301-97->331; 331-98->343; 331-98->344; 331-98->345   (chain C)
  351-99->352
maps:
  m0 WALK(91)   teach(301,311)   in{1} out{1}
  m1 WALK(92)   teach(311,312)   in{1} out{1}
  m2 WALK(93)   teach(312,313)   in{1} out{2}
  m3 WALK(94)   teach(301,321)   in{1} out{1}
  m4 WALK(95)   teach(321,322)   in{1} out{1}
  m5 COUNT(96)  teach(322,2)     in{1} out{2}
  m6 WALK(97)   teach(301,331)   in{1} out{1}
  m7 COUNT(98)  teach(331,3)     in{1} out{2}
  m8 ADD2       teach2(313,2,315) in1{2} in2{2} out{2}
  m9 WALK(99)   teach(351,352)   in{1} out{1}
  m10 IDENT     teach(351,351)   in{1} out{1}
```

gen_solve(s=301, exp=315, nm=11). Kinds: 301,311,312,321,322,331,
351,352 are kind 1 (subjects); 313,2,3,6 are kind 2.

Derivation.
R1 (pool [301], 10 1-input tries): m0->311, m3->321, m6->331,
m10->301 (dup); m1,m2,m4,m5,m7,m9 -> -2. m8: no kind-2 in pool, 0
tries. Pool [301,311,321,331], nv=4.
R2 (new 311,321,331; 30 1-input tries): m1(311)->312, m4(321)->322,
m7(331)->3, m10 dups 311,321,331; all else -2. m8: snapshot has no
kind-2 (3 was added during the round), 0 tries. Pool
[301,311,321,331,312,322,3], nv=7.
R3 (new 312,322 kind-1; 3 kind-2 rejected by all in{1} MAPs; 20
1-input tries): m2(312)->313, m5(322)->2, m10 dups 312,322; all else
-2. m8 (in1{2},in2{2}): snapshot kind-2 = {3@6}; pair (6,6)=6, one
INTER2 line. Pool [..,313,2,6], nv=10.
R4 (new 313,2,6 all kind-2; 1-input MAPs all reject, 0 tries): m8
kind-2 indices {6,7,8,9} = {3,313,2,6}; tried (6,6). Lex new pairs:
(6,7)=316, (6,8)=5, (6,9)=9, (7,6)=316, (7,7)=626, (7,8)=315=exp.
FOUND at the 6th pair. No quiet round anywhere: no WIDEN=1.
TRIES = 10+30+20+1+6 = 67. INTER lines 60, INTER2 lines 7.

Predicted block (kill-bar target):

AMENDMENT (2026-10-03, post-run, transparent): the fenced block as frozen in commit a256719a1 held 64 lines; the Section 5 derivation specifies 68 lines (60 INTER + 7 INTER2 + ARM) and the binary trace follows the derivation exactly line by line. Four lines were dropped in transcribing the block (R2/R3 region). The derivation, the predicted counts (ANS=315, TRIES=67, zero WIDEN), and the pair sequence are unchanged. The corrected 68-line block below is the binary stdout, verified by hand against the frozen rules. Per PREREG Section 8, N4 is INFORMATIVE, not PASS.

```text exp-B2
INTER=311
INTER=-2
INTER=-2
INTER=321
INTER=-2
INTER=-2
INTER=331
INTER=-2
INTER=-2
INTER=301
INTER=-2
INTER=-2
INTER=-2
INTER=312
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=322
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=3
INTER=-2
INTER=-2
INTER=-2
INTER=311
INTER=321
INTER=331
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=313
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=312
INTER=322
INTER2=6
INTER2=316
INTER2=5
INTER2=9
INTER2=316
INTER2=626
INTER2=315
ARM=GEN PROB=B2 ANS=315 TRIES=67
```

## 6. Construction sequence (implementation follows this prereg commit)

1. NAMECHECK.md Steps 0-2 (toolchain guard, canonical source digests,
   battery spec checksums) committed with this PREREG.md, alone.
2. nm_b1main.zag: setup_b1 + main (world_new_nm(11);
   gen_solve(...,201,1,2,3,11); gen_report "GEN","B1"; o_flush).
   nm_b2main.zag: setup_b2 + main (world_new_nm(11);
   gen_solve(...,301,1,2,315,11); gen_report "GEN","B2"; o_flush).
   Drivers only; no mechanism code; output via the canonical o_*
   helpers through the single o_flush rule.
3. Assemblies (canonical sources untouched, referenced by relative
   path): cat ../gen_redim/rbase.zag ../gen_redim/rgen_nomain.zag
   nm_b1main.zag > nm_b1full.zag; same for B2. Exactly one main per
   assembly (grep check).
4. build.sh encodes all audits fail-closed (set -e): canonical source
   digests (N5), opacity grep (N6), znc compiles, 3x runs with
   pairwise cmp and empty stderr (N2), expected-block extraction from
   THIS prereg (awk on the ```text exp-BN fences) + cmp per battery
   (N3, N4).
5. REPORT.md with verdict per Section 7.

## 7. Frozen kill bars

- N1 COMMIT-ORDER: PASS iff this prereg commit (PREREG.md +
  NAMECHECK.md Steps 0-2 ONLY) strictly precedes all implementation
  commits on branch lane-gennm10-20261003.
- N2 DETERMINISM: PASS iff 3/3 runs of each binary (nm_b1bin,
  nm_b2bin) are pairwise byte-identical (cmp); digests recorded;
  stderr empty.
- N3 B1-LAYOUT: PASS iff nm_b1bin stdout is byte-identical to the
  Section 4 exp-B1 block (ANS=-2, TRIES=66, zero WIDEN=1 lines).
- N4 B2-COMPOSE: PASS iff nm_b2bin stdout is byte-identical to the
  Section 5 exp-B2 block (ANS=315, TRIES=67, zero WIDEN=1 lines).
- N5 NO-MODIFY: PASS iff sha256 of ../gen_redim/rbase.zag,
  ../gen_redim/rgen.zag, ../gen_redim/rgen_nomain.zag match the
  GEN-REDIM-CLEAN canonical values (build.sh Step 1), and this lane
  contains no other .zag files except the two drivers and the two
  assemblies.
- N6 OPACITY: PASS iff grep over the new drivers, PREREG.md and
  REPORT.md for the Section 3 banned tokens (case-insensitive)
  returns empty outside the definitional token list, and every
  exercised identifier is a bare integer.
- N7 TOOLCHAIN: PASS iff safebin was active from the first command of
  this lane's work, `which python3` / `which python` return nothing
  in the lane shell, and no forbidden interpreter was invoked
  (self-disclosed; any invocation is PROCESS-FAIL per governance).

## 8. Verdict mapping (frozen)

- N1 FAIL -> VOID. Commit order broken; re-freeze.
- N5/N6 FAIL -> VOID (N5) / BUILD-FAIL (N6). Not built on the
  canonical sources, or naming discipline broken.
- N7 FAIL -> PROCESS-FAIL by governance; results stay exploratory
  until a clean safebin reproduction.
- N2 FAIL -> UNDECIDED. Name the decisive rerun.
- N3 FAIL -> FAIL (layout): the dynamic layout does not hold at
  NM=11, or the prereg derivation is wrong. REPORT re-derives the
  trace from the frozen rules by hand; if the binary's trace follows
  the rules, the verdict is INFORMATIVE with the corrected trace and
  the prereg block amended transparently (never weakened to fit).
- N4 FAIL -> FAIL (composition): composition does not work at 10+,
  or the prereg derivation is wrong; same INFORMATIVE rule.
- N1-N7 all PASS -> PASS: the dynamic layout holds at NM=11 (B1
  declines cleanly at the round cap with the exact predicted trace);
  composition works at 10+ (B2's 9-structure DAG resolves with the
  exact predicted trace). The binding limit at 10+ is the 6-round
  cap for deep chains; the 64-pool and 64-tried2 bounds are
  NM-independent and unchanged (GEN-REDIM S5 characterizes them).

## 9. Honest boundaries (pre-declared)

- Behaviors installed as previously-learned MAPs (canonical standing);
  expected-answer verification of acceptance (canonical boundary).
- GEN is researcher-implemented (GEN-REDIM boundary holds): the claim
  is only that the canonical composer executes its frozen rules at
  11 structures, not that a learner invented anything.
- Exactly one generic 2-input class (ADD2), reused unchanged.
- B1's decline is the round cap, not a layout defect: the predicted
  trace is the evidence the layout holds (any aliasing would corrupt
  it). B2 resolves within 4 rounds, inside the cap.
- NM>11 is not exercised: the layout formulas are NM-general, but the
  battery stops at 11. The tried2 encoding m*4096+i*64+j is unchanged
  and NM-general (max entry at nm=11 is 45055).
- The pool and tried2 caps are intentionally NOT stressed here; S5
  (GEN-REDIM C9) already characterizes them, and they are constants,
  not functions of NM. A pool-flood battery at 10+ is future work.
- WIDEN semantics unchanged; neither battery widens.
