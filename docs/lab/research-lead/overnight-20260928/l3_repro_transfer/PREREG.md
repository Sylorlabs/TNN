# PREREG: L3 Reproduction and Transfer (L3-REPRO-TRANSFER)

Status: PREREG-FROZEN 2026-10-02, before implementation. Any change
requires a new prereg; this document is never edited after freezing.
Commit-order self-check: this prereg is committed BEFORE any new
implementation file exists.

Worker: L3 Reproduction and Transfer Worker (subagent, 2026-10-02).

Transparency note: reference copies orig_glm_learner.zag,
orig_gl2m_h1.zag, orig_gl2m_h2.zag, orig_build.sh, orig_run_h1_1.log,
orig_run_h2_1.log (byte-identical to frozen commits e5b747176 and
762cda924) were extracted into this directory before prereg freezing
for audit purposes only. They are not new implementation. All new
implementation files (tr_*.zag, transfer binaries, transfer logs,
repro binaries, repro logs) are created only after this prereg commit.

## 1. Question under test

C281 (commits e5b747176, 762cda924) is the first L3-class result: on
grammar to construction, the learner created intermediate M=[INC R0]
with a visible creation trace, persistence, and revision. Per Micah's
L3 bar this needs three things: (1) independent reproduction from
committed source, (2) transfer to a new sealed world, (3) ablation.
This experiment does all three.

## 2. Part 1: Reproduction (frozen protocol)

Source: the committed C281 source only (e5b747176 for the frozen
prereg, 762cda924 for implementation). Procedure:

1. Copy committed glm_learner.zag, gl2m_h1.zag, gl2m_h2.zag to
   repro reference files. Verify byte-identity against the commits
   (sha256 of git show output equals sha256 of the copies).
2. Rebuild: concatenate learner + driver exactly as the committed
   build.sh does, compile with the pinned znc at
   $HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1.
3. Run each rebuilt binary 3 times. Record sha256 of every run log.
4. Fidelity checks (kill bars R1-R4, section 5).

Expected: 3/3 byte-identical runs per binary; run-output digests
equal the committed digests recorded in the C281 report
(H1 abc3e0182c22f23e73e075549fd977c9f165d6cc000931c4b85f6ba5012ac426,
H2 ee0bf4ba9f8acc289d549c590b96c1ca41269b1939cd39dd8ab09e6f84b3a022);
M=[INC R0] program bytes (4,0,0) with the C-ROUND gain=2 creation
trace; all 8 arms per binary match the committed ARM-RESULTs
(TOTAL 9/9).

## 3. Part 2: Transfer world design (frozen)

A NEW sealed world. The generic machinery (glm_learner.zag) is reused
byte-identical; only the driver world changes. Differences from C281:
different validity rules (T1/T2 below, not G1/G2), different divisor
range (training {24,36}, sealed {48,60,72}; C281 used {16,8} and
{24,32,40}), different relation numbers (81/82/83/84; C281 used
71/72/73/74).

Training facts (fact store only):
- Grammar divisor facts: (1,81,24), (2,81,36). Relation 81 licenses
  divisor D for rule r.
- Range-hi distractor facts: (1,82,9), (2,82,6).

Y memorized construction table (driver table, not facts):
- (24,25), (36,37). Y as taught returns the memorized word or -1.

Sealed facts (insertion order frozen):
- (3,84,7): distractor relation, inserted FIRST (candidate scan meets
  the distractor before the genuine relation; discrimination, not luck).
- (3,83,48): genuine: rule 3 licenses divisor 48.
- (3,82,11): hi fact for rule 3.
- (4,83,60): rule 4 licenses divisor 60.
- (5,83,72): rule 5 licenses divisor 72.

Validity rules (WORLD/DRIVER ONLY; the learner constructor never sees
them; the driver self-checks every label triple against them at
startup and aborts on LABEL-MISMATCH):
- T1: word v valid under divisor D iff exists q in [2,3], r in [0,7]
  with v = D*q + r.
- T2 (revision regime): v valid under D iff exists q in [2,3],
  r in [1,8] with v = D*q + r.

Labeled word-validity experience (driver-generated literals, the only
thing the constructor may read). T1 labels, D in {24,36}, 22 triples:
- D=24 valid: 48, 49, 55, 73, 79. D=24 invalid: 24, 25, 32, 23, 1, 0.
- D=36 valid: 72, 73, 79, 109, 115. D=36 invalid: 36, 37, 44, 35, 1, 0.
T2 labels, D in {24,36}, 18 triples:
- D=24 valid: 49, 56, 73, 80. D=24 invalid: 48, 57, 81, 24, 25.
- D=36 valid: 73, 80, 109, 116. D=36 invalid: 72, 81, 117, 36, 37.

Sealed goals (expected-answer verification, same honest boundary as
all H1/H2 waves):
- Z: subject 3 -> 96. Needs X rebound to 83 (X=48), then M'(48)=96.
- Z2: subject 4 -> 120. M'(60)=120 via persisted composite/M.
- Z3: subject 5 -> 145. After T2 revision, M''(72)=145.

## 4. Frozen hand-derived transfer expectations

The implementation must reproduce these; deviation is a falsifier,
not a tuning opportunity.

T1 fresh construction from empty: baseline score 0 (w=D labeled 0
for both divisors). Round 1: all 16 op-0 CPY candidates gain 0
(w=D or w=0, both label 0); (1,0,0)=ADD R0,R0 is the first
positive-gain candidate with gain 2 (w=2D: labels 1,1 for D=24,36);
no other candidate reaches gain 2. M' = [ADD R0,R0], program bytes
(1,0,0), score 2/2, stop. Trace: C-ROUND 1 base=0 win=1,0,0 gain=2
score=2; M-BUILT score=2; M-PROG n=1 gen=0 created=1 build_count=1
bytes=1,0,0,.

T2 adapt from [ADD R0,R0]: base score 0 (w=2D labeled 0 for both
divisors). Extension round: ops 0-3 all gain 0 (CPY gives 2D or 0;
ADD gives 4D miss or 2D; MUL gives 4D*D miss or 0; SET1 gives 1
miss); (4,0,0)=INC R0 is the first positive-gain candidate with
gain 2 (w=2D+1: labels 1,1). M'' = [ADD R0,R0,INC R0], program bytes
(1,0,0,4,0,0), score 2/2, adapt code 2, Mprev holds (1,0,0) with
sup=1.

H1 predicted TREAT Z trace: PHASE1: TRY single m=0 r=-1; TRY single
m=2 r=11; TRY pair a=0 b=1 r=-1; TRY pair a=2 b=1 r=-1; TRY pair
a=3 b=0 r=-1; TRY pair a=3 b=2 r=11; L1-FAIL (6 tries). PHASE2:
M' constructed as above; CANDIDATES n=3 84 83 82; REBIND m=0 cr=84
nm=4: TRY single m=4 r=7, TRY pair a=4 b=1 r=14 rejected; REBIND
m=0 cr=83 nm=5: TRY single m=5 r=48, TRY pair a=5 b=1 r=96;
Z-COMP z=6 a=5 b=1; REBOUND a=5 param=83 rebound_of=0; ARM-RESULT
PASS. Total tries 10.

H1 predicted TREAT Z2 trace: PHASE1: TRY single m=0 r=-1; m=2 r=-1;
m=4 r=-1; m=5 r=60; m=6 r=120; Z-SINGLE m=6 (persisted composite).
Z2-RESULT PASS, build_count unchanged.

H1 predicted REVISE trace: Z sanity as above; ADAPT cur_score=0;
C-ROUND 1 base=0 win=4,0,0 gain=2 score=2; ADAPT-CODE 2; M-PROG n=2
gen=1 created=1 build_count=2 bytes=1,0,0,4,0,0,; M-PREV n=1 sup=1
bytes=1,0,0,; Z3 (5,145): PHASE1 Z-SINGLE via persisted composite
(72 -> 145 through revised M); ARM-RESULT PASS.

H2 predicted TREAT Z trace: PHASE1: all 9 ordered mode pairs fail
(L1-FAIL). PHASE2: M' built as above; rel=84: (1,2): 7->14
rejected, (3,2): 11->22 rejected; rel=83: (1,2): 48->96 VC-COMPOSE
ok m1=1 m2=2 rel=83; ARM-RESULT PASS.

H2 predicted Z2: PHASE1 L1-FAIL (stored composite uses training
relation); PHASE2: M-PRESENT reuse; CANDIDATES n=1 83; (1,2)
rel=83: 60->120 VC-COMPOSE ok; Z2-RESULT PASS.

H2 predicted REVISE: adapt code 2, Mprev (1,0,0) sup=1, M
(1,0,0,4,0,0), Z3 (5,145) PASS.

## 5. Transfer arms (frozen, per mechanism, mirroring C281)

- TREAT-L2: teach; sealed facts; l2_on=1, allow_build=1. Solve Z,
  then Z2 in the SAME workspace (M must persist; build_count stays 1).
  Expect Z PASS with rebound provenance and learner-created M';
  Z2 PASS via the persisted composite.
- L1-ONLY: l2_on=0. Expect FAIL (Z unsolved).
- ABL-X: delete X (H1) / behav 0 (H2); l2_on=1. Expect FAIL.
- ABL-Y: delete Y (H1) / behav 1 (H2); l2_on=1. Expect FAIL.
- FRESH: facts only, no teaching; l2_on=1. Expect FAIL.
- NO-M: teach; l2_on=1, allow_build=0 (M stays absent; Y falls back to
  memorized lookup). Expect FAIL. This is the causal-necessity
  ablation for the intermediate.
- SUPPLIED: teach; l2_on=1; driver installs M'=[ADD R0,R0] as
  researcher-supplied (supplied marker, NO construction trace).
  Expect PASS. Diagnostic only.
- REVISE: teach; build M' on T1; sanity-solve Z; T2 labels arrive;
  m_adapt; solve Z3. Expect adapt code 2, Mprev=(1,0,0) sup=1,
  M=(1,0,0,4,0,0), Z3 PASS.

## 6. Kill bars (all must hold for the verdict)

- R1 REPRO-BUILD: rebuild from committed source with the pinned znc
  succeeds; zero compile errors.
- R2 REPRO-DETERMINISM: 3/3 byte-identical runs per rebuilt binary.
- R3 REPRO-FIDELITY: rebuilt run-output sha256 equals the committed
  digests (H1 abc3e018..., H2 ee0bf4ba...); M-PROG bytes (4,0,0)
  with C-ROUND gain=2 trace present; TOTAL 9/9 for both binaries.
- R4 REPRO-AUDIT: the C281 prereg section 8 grep specs return zero
  matches on the committed machinery; the committed run logs contain
  no SUPPLIED-INSTALL line on the TREAT path.
- R5 TRANSFER-SOLVE: transfer TREAT Z ARM-RESULT PASS for both H1
  and H2; composite comp_a has rebound_of=X and param=83 (H1);
  VC-COMPOSE ok m1=1 m2=2 rel=83 (H2); m_created=1; M-PROG bytes
  (1,0,0).
- R6 TRANSFER-NECESSITY: L1-ONLY, ABL-X, ABL-Y, FRESH fail for both.
- R7 TRANSFER-M-NECESSARY (ablation): NO-M fails for both (rebinding
  succeeds but Y lookup misses; the intermediate is causally
  necessary). Also the reproduction NO-M arm fails as in C281.
- R8 TRANSFER-CREATED: (a) the transfer trace shows at least one
  C-ROUND with gain>0, final program non-empty, score 2/2 on the T1
  labels; (b) the transfer-world origin audit is clean: the
  machinery file (byte-identical to committed glm_learner.zag)
  contains no standalone literals 81, 82, 83, 84, 24, 36, 48, 60,
  72, 96, 120, or 145, and in the transfer drivers every line
  containing 83 or 84 also contains add_fact; (c) the transfer
  TREAT output contains no SUPPLIED-INSTALL line.
- R9 TRANSFER-REUSE: Z2 PASS for both; m_build_count==1 after Z and
  Z2 (M persisted, not rebuilt).
- R10 TRANSFER-REVISE: adapt returns code 2 for both; Mprev holds
  program (1,0,0) with sup=1; current M program is (1,0,0,4,0,0);
  Z3 PASS for both.
- R11 TRANSFER-DETERMINISM: 3/3 byte-identical runs per transfer
  binary (sha256 recorded).
- R12 TOOLCHAIN: safebin active, `which python3 python` empty, pure
  Zag, no forbidden executable invoked, 0 modes/bridges/handlers.

## 7. Verdict rule

- R1-R12 all PASS: L3-REPRO-TRANSFER-COMPLETE. C281 is independently
  reproduced at full fidelity; in the new sealed world the learner
  created a DIFFERENT intermediate M'=[ADD R0,R0] (not a copy of the
  C281 solution), persisted it, reused it, and revised it under a
  regime shift; ablation confirms causal necessity.
- R1-R4 fail: L3-REPRO-FAIL. Reproduction failed; transfer results
  are reported but do not rescue the reproduction claim. Failing bar
  named.
- R5 or R8 fail but transfer SUPPLIED passes: transfer verdict L2:
  the intermediate must be researcher-supplied in the new world;
  the learner does not create it there.
- Any other bar failure: verdict FAIL, failing bar named.

## 8. Honest boundaries (declared in advance)

- The C281 result is prior work under test for reproduction, not
  re-adjudicated here.
- The transfer world (validity rules, labels, facts, divisors,
  relations, expected answers) is worker-designed, not
  adversary-designed. Adversarial-world generality stays open.
- Expected answers used for verification (same honest boundary as
  all H1/H2 waves).
- The SUPPLIED arm installs the transfer solution [ADD R0,R0] as a
  researcher-authored diagnostic; it is never on the TREAT path.
- One L2 form (relation rebinding) composed with one intermediate
  form (generator program), as in C281.
- This build targets the 12 frozen bars above; it does not claim
  Micah's full 12-criterion L3 bar.

## 9. Build and determinism spec

Pure Zag. u8-backed workspace, little-endian cell helpers. Output via
one preallocated buffer and a single _zag_raw_syscall write per arm
sequence (no _zag_print for dynamic content). No RNG. Fixed orders
everywhere. 3/3 byte-identical required for repro and transfer runs.
0 modes/bridges/handlers. No em/en dashes in loop documentation.
Paper untouched. Nothing pushed. Commits local on tnn-native-lab with
EXPLICIT pathspecs. The original C281 directory
(xdomain_grammar_l2m) is never modified.
