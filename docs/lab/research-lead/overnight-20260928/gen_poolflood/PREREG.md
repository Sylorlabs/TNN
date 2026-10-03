# PREREG: GEN-POOLFLOOD -- Pool-Flood Battery at NM=11

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Steps 0-2) strictly precedes all
implementation. Worker: gen-poolflood. Date: 2026-10-03.

## 1. Question

GEN-NM10 (C438, INFORMATIVE) proved 10+ composition works at nm=11 and
recommended as follow-up "a pool-flood battery at nm=11 to confirm the
silent-drop signature is identical under the dynamic layout
(expected: same S5-class behavior, since the cap is constant)."

The 64-value pool cap is a constant of the mechanism, not a function
of NM, characterized at nm=4 by GEN-REDIM S5 (C9, canonical per
GEN-REDIM-CLEAN C434): ARM=GEN PROB=S5 ANS=-2 TRIES=2734, exactly
3 INTER= lines, exactly 2731 INTER2= lines, zero WIDEN=1 lines. The
pool regions MOVE under the dynamic layout (VPOOL 1024->1408,
KPOOL 1280->1664, PROV 1536->1920 from nm=4 to nm=11), so re-running
the flood at nm=11 is a genuine test of whether the silent-drop
signature survives re-dimensioning.

This battery asks: is the pool-flood signature NM-independent?
Concretely:

- PF1: re-run the exact S5 flood world at nm=4 on the dynamic layout.
  Predicted: byte-identical to the canonical S5 section (the frozen
  nm=4 signature, modulo the PROB label).
- PF2: run the S5 flood world at nm=11 with 7 additional taught
  structures (11 MAPs total, exercising the dynamic layout).
  Predicted: the flood dynamics are byte-identical to nm=4; the only
  NM-dependent difference is the 7 extra first-round tries the frozen
  rules mandate for the 7 extra structures.

A PASS means the pool bound (64-cap, silent drop, no panic,
deterministic decline) behaves identically at nm=11: the signature
is NM-independent.

## 2. What is reused unchanged

- The canonical GEN-REDIM sources rbase.zag, rgen.zag,
  rgen_nomain.zag (digests in NAMECHECK.md Step 1). This lane adds
  ONLY one new driver main; it does not copy, edit, or re-derive the
  mechanism. Assembly concatenates the canonical files with the new
  driver. Kill bar F5 verifies the canonical sources are
  byte-identical to the canonical digests.
- The canonical S5 section ../gen_redim/rd_sec_S5.txt (sha256
  a43078d4..., 2735 lines) as the frozen nm=4 flood signature.
- The pool mechanism (rgen.zag gen_addval): linear dup scan; if n<64,
  write V/K/P at index n and bump nv; else return -1 silently. A
  dropped value prints no line, raises no error, and never enters
  the pool, so no later pair try can observe it. Overflow is silent
  drop, not panic, by construction.
- Layout formulas (GEN-REDIM PREREG Section 2), tried2 pair encoding
  m*4096+i*64+j, 64-entry tried2 cap, 64-slot visit stack, 6-round
  cap, WIDEN-once, admission (g_khas, empty=compatible), trial order
  (1-input MAPs in id order, then 2-input MAPs in id order; lex pair
  order), round snapshots, quiet-round detection, success recording
  with provenance closure, one ADD2 class. No new behavior classes,
  opcodes, admission dimensions, modes, flags, or shape predicates.

world_new_nm invariant (GEN-REDIM REPORT Section 5): nm >= number of
MAPs the setup defines. PF1 defines 4 MAPs, uses world_new_nm(4);
PF2 defines 11 MAPs, uses world_new_nm(11).

## 3. Opaque naming (frozen)

Structures m0..m10, relations bare integers 91..93, entities bare
integers, queries PF1..PF2. No identifier carries task semantics.
Forbidden tokens (case-insensitive grep over all new sources, PREREG,
REPORT):

hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|
language|audio|interven|belie|goal|agent

## 4. Battery PF1: flood baseline at nm=4

setup_pf1 (new driver pf_main.zag) is a byte-exact copy of the frozen
setup_s5 (build.sh verifies by extraction + cmp):

```text
facts:
  201-91->211; 201-91->212; 201-92->221; 201-92->222; 201-92->223;
  231-93->232
maps:
  m0 COUNT(91)  teach(201,2)    in{1} out{2}
  m1 COUNT(92)  teach(201,3)    in{1} out{2}
  m2 ADD2       teach2(2,3,5)   in1{2} in2{2} out{2}
  m3 IDENT      teach(231,231)  in{1} out{1}
```

gen_solve(s=201, exp=999999, nm=4). The exp value is unreachable:
m2's sums grow but never hit 999999 within 6 rounds, and the pool
caps at 64 with silent drop.

Predicted (kill-bar target): the PF1 section is byte-identical to
the canonical S5 section modulo the PROB label (S5->PF1):
ANS=-2, TRIES=2734, exactly 3 INTER= lines, exactly 2731 INTER2=
lines, zero WIDEN=1 lines, ARM line
`ARM=GEN PROB=PF1 ANS=-2 TRIES=2734`.

## 5. Battery PF2: flood at nm=11

setup_pf2 (new driver pf_main.zag): the S5 facts and S5's 4 MAPs
(m0..m3, identical teaches), plus 7 IDENT distractors:

```text
maps (m0..m3 as in Section 4):
  m4 IDENT  teach(201,201)  in{1} out{1}
  m5 IDENT  teach(201,201)  in{1} out{1}
  m6 IDENT  teach(201,201)  in{1} out{1}
  m7 IDENT  teach(201,201)  in{1} out{1}
  m8 IDENT  teach(201,201)  in{1} out{1}
  m9 IDENT  teach(201,201)  in{1} out{1}
  m10 IDENT teach(201,201)  in{1} out{1}
```

teach(m,201,201): exec_map class 3 returns the input 201, which
matches, so observe records in{1} (201 is a fact subject, kind 1).
Each distractor therefore admits exactly the kind-1 pool values.

gen_solve(s=201, exp=999999, nm=11).

Hand derivation from the frozen rules.

Kinds: 201 and 231 are kind 1 (fact subjects); every other value
that ever enters the pool (2, 3, all sums) is kind 2.

R1 (pool [201], snapshot ns0=1). 1-input loop, id order:
m0(201)->2 "INTER=2"; m1(201)->3 "INTER=3"; m2 skipped (arity 2);
m3(201)->201 dup "INTER=201"; m4(201)->201 dup "INTER=201"; ...
m10(201)->201 dup "INTER=201". tried1 marks (m,0) for
m in {0,1,3,4,5,6,7,8,9,10}. 2-input loop: m2 over pair (0,0);
kinds (1,1) rejected against in1{2} in2{2}: 0 tries.
R1 output: 10 INTER= lines (2, 3, then eight 201s), 0 INTER2= lines,
10 tries. Pool after R1: [201,2,3] (all IDENT results were dups;
nv=3) -- identical to S5's pool after R1.

R2..R6: the 7 distractors are never tried again. For pool index 0
they are tried1-marked; for every new pool value (all kind 2) their
in{1} contract rejects. m0/m1/m3 behave exactly as in S5 (the only
kind-1 value, 201, is already tried). m2's pair space is a
deterministic function of the pool sequence, which is byte-identical
to S5's (same adds, same dups, same silent drops at the 64-cap, in
the same order), so every one of the 2731 INTER2= lines is identical
to S5's R2..R6 lines.

Quiet rounds: R1 performs tries; R2..R6 are exactly S5's rounds,
which had no quiet round (S5 printed zero WIDEN=1). So PF2 prints
zero WIDEN=1 lines. exp=999999 is never produced: ANS=-2.

Predicted (kill-bar target): the PF2 section is byte-identical to
the canonical S5 section transformed as follows (mechanical,
verified by build.sh):

1. Verify the canonical section's sha256 and that its last line is
   exactly `ARM=GEN PROB=S5 ANS=-2 TRIES=2734` and its first three
   lines are exactly `INTER=2`, `INTER=3`, `INTER=201` (R1's tries).
2. exp_PF2 = first 3 lines, then exactly 7 lines `INTER=201`, then
   the remaining 2732 lines with `PROB=S5` -> `PROB=PF2` and
   `TRIES=2734` -> `TRIES=2741`.

Result: ANS=-2, TRIES=2741, exactly 10 INTER= lines (the first 10
lines of the section: 2, 3, eight 201s), exactly 2731 INTER2=
lines, zero WIDEN=1 lines, ARM line
`ARM=GEN PROB=PF2 ANS=-2 TRIES=2741`.

Why this tests the silent-drop signature: the 2731 pair-result
lines are a deterministic function of the pool's add/dup/drop
sequence. At nm=11 the pool lives at VPOOL=1408 (not 1024), kinds at
1664, provenance at 1920, nv at 5764. Byte-identity of all 2731
lines across that move proves the 64-cap and the silent drop
(gen_addval returning -1 with no line and no panic) are preserved
exactly: any misaddressing, cap change, or drop corruption at
nm=11 would diverge the sums. The ONLY permitted NM-dependent
difference is the 7 extra R1 tries, which the frozen trial-order
rules mandate for 7 extra admitted structures.

## 6. Construction sequence (implementation follows this prereg commit)

1. NAMECHECK.md Steps 0-2 (toolchain guard, canonical source
   digests, battery spec) committed with this PREREG.md, alone.
2. pf_main.zag: setup_pf1 (byte-exact copy of frozen setup_s5) +
   setup_pf2 + main (world_new_nm(4) then world_new_nm(11);
   gen_solve(...,201,1,2,999999,4/11); gen_report "GEN","PF1"/"PF2";
   single o_flush). Driver only; no mechanism code.
3. Assembly (canonical sources untouched, referenced by relative
   path): cat ../gen_redim/rbase.zag ../gen_redim/rgen_nomain.zag
   pf_main.zag > pf_full.zag. Exactly one main (grep check).
4. build.sh encodes all audits fail-closed (set -e): canonical
   source digests + canonical S5-section digest (F5), setup_pf1
   byte-exactness vs the frozen setup_s5 extract, opacity grep (F6),
   znc compile, 3x runs with pairwise cmp and empty stderr (F2),
   section split on ARM lines, mechanical expected-file
   construction with pre-verification of the canonical section
   (head/ARM checks), cmp per battery (F3, F4), exact line counts.
5. REPORT.md with verdict per Sections 7-8.

## 7. Frozen kill bars

- F1 COMMIT-ORDER: PASS iff this prereg commit (PREREG.md +
  NAMECHECK.md Steps 0-2 ONLY) strictly precedes all implementation
  commits on branch lane-genpoolflood-20261003.
- F2 DETERMINISM: PASS iff 3/3 runs of pf_bin are pairwise
  byte-identical (cmp); digests recorded; stderr empty.
- F3 PF1-BASELINE: PASS iff the PF1 section is byte-identical to the
  canonical S5 section modulo the PROB label (S5->PF1): ANS=-2,
  TRIES=2734, 3 INTER= lines, 2731 INTER2= lines, zero WIDEN=1.
- F4 PF2-FLOOD: PASS iff the PF2 section is byte-identical to the
  Section 5 constructed expected block: ANS=-2, TRIES=2741,
  10 INTER= lines, 2731 INTER2= lines, zero WIDEN=1 lines.
- F5 NO-MODIFY: PASS iff sha256 of ../gen_redim/rbase.zag,
  ../gen_redim/rgen.zag, ../gen_redim/rgen_nomain.zag and
  ../gen_redim/rd_sec_S5.txt match the NAMECHECK.md Step 1 values,
  setup_pf1 is byte-exact vs the frozen setup_s5 extract, and this
  lane contains no other .zag files except the driver and the one
  assembly.
- F6 OPACITY: PASS iff grep over the new driver, PREREG.md and
  REPORT.md for the Section 3 banned tokens (case-insensitive)
  returns empty outside the definitional token list, and every
  exercised identifier is a bare integer.
- F7 TOOLCHAIN: PASS iff safebin was active from the first command
  of this lane's work, `which python3` / `which python` return
  nothing in the lane shell, and no forbidden interpreter was
  invoked (self-disclosed; any invocation is PROCESS-FAIL per
  governance).

## 8. Verdict mapping (frozen)

- F1 FAIL -> VOID. Commit order broken; re-freeze.
- F5/F6 FAIL -> VOID (F5) / BUILD-FAIL (F6). Not built on the
  canonical sources, or naming discipline broken.
- F7 FAIL -> PROCESS-FAIL by governance; results stay exploratory
  until a clean safebin reproduction.
- F2 FAIL -> UNDECIDED. Name the decisive rerun.
- F3 FAIL -> FAIL (baseline): the frozen nm=4 flood signature is not
  reproduced on the dynamic layout. The comparison anchor moved;
  diagnose before any nm=11 claim.
- F3 PASS and F4 FAIL -> re-derive the PF2 trace from the frozen
  rules by hand. If the binary's trace follows the rules, the
  verdict is INFORMATIVE with the corrected trace and the prereg
  construction amended transparently (never weakened to fit). If the
  trace violates the rules (e.g. pool corruption, a panic, or drops
  that are not silent), the verdict is FAIL: the pool-flood
  signature is NM-dependent.
- F1-F7 all PASS -> PASS: the pool-flood signature is
  NM-independent. The 64-pool cap, the silent drop, and the
  deterministic decline behave identically at nm=11; the only
  NM-dependent term is the +7 first-round tries the frozen rules
  mandate.

## 9. Honest boundaries (pre-declared)

- Behaviors installed as previously-learned MAPs (canonical
  standing); expected-answer verification of acceptance (canonical
  boundary).
- GEN is researcher-implemented (GEN-REDIM boundary holds): the
  claim is only that the canonical composer executes its frozen
  pool rules identically at nm=11, not that a learner invented
  anything.
- Exactly one generic 2-input class (ADD2), reused unchanged.
- The silent drop is verified behaviorally (full-trace identity),
  not by printing nv: the drop produces no output by design, and
  the 2731 pair-result lines are the observable record of the
  add/dup/drop sequence.
- S5's 2731 pair lines are not hand-enumerated here (GEN-REDIM
  precedent); the NM-independence claim rests on byte-identity of
  the full pair trace across the layout move, plus the hand-derived
  +7 insertion.
- NM>11 is not exercised. The tried2 64-entry cap is not stressed
  (m2's entries stay far below 64 in both batteries).
- WIDEN semantics unchanged; neither battery widens.
