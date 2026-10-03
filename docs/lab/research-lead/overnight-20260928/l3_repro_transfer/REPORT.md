# REPORT: L3 Reproduction and Transfer (L3-REPRO-TRANSFER)

Worker: L3 Reproduction and Transfer Worker, 2026-10-02.
Prereg: PREREG.md, frozen and committed BEFORE implementation
(commit f843cba55). No prereg changes since.

## Verdict

L3-REPRO-TRANSFER-COMPLETE.

C281 is independently reproduced at full fidelity from committed
source: rebuilt binaries are byte-identical to the committed
binaries, rerun outputs are byte-identical to the committed run logs,
and every arm, trace line, and audit matches. In a NEW sealed world
(different validity rules T1/T2, different divisor range, different
relation numbers) with the generic machinery reused byte-identical,
the learner created a DIFFERENT intermediate M'=[ADD R0,R0]
(w = 2D), not a copy of the C281 solution [INC R0]: visible creation
trace, white-box learner state, persistence without rebuild, reuse on
a second sealed goal, and revision to M''=[ADD R0,R0,INC R0] under a
regime shift. Forced NO-M ablation destroys the advantage in both the
reproduction and the transfer. All 12 kill bars hold for both H1 and
H2, 3/3 byte-identical runs per binary.

## Part 1: Reproduction (R1-R4)

Source fidelity: the reference copies in this directory are
sha256-identical to git show output from commits e5b747176 and
762cda924 for glm_learner.zag, gl2m_h1.zag, gl2m_h2.zag, build.sh,
and both run logs.

- R1 REPRO-BUILD: PASS. Concatenation plus the pinned znc (the exact
  path the C281 build.sh names) compiled both binaries with zero
  errors. The rebuilt binaries are BYTE-IDENTICAL to the committed
  h1_bin/h2_bin (sha256 6f076073... and af7870cd..., matching the
  C281 report digests).
- R2 REPRO-DETERMINISM: PASS. 3/3 byte-identical runs per binary.
- R3 REPRO-FIDELITY: PASS. Run-output digests equal the committed
  digests (H1 abc3e018..., H2 ee0bf4ba...). The M creation trace is
  present verbatim: C-ROUND 1 base=0 win=4,0,0 gain=2 score=2;
  M-BUILT score=2; M-PROG n=1 gen=0 created=1 build_count=1
  bytes=4,0,0,. All 8 arms per binary match the committed
  ARM-RESULTs; TOTAL 9/9 for both.
- R4 REPRO-AUDIT: PASS. The C281 prereg section 8 grep specs return
  zero matches on the committed machinery (no relation/table
  literals, no SUPPLIED, no validity-rule shape). SUPPLIED-INSTALL
  appears exactly once per committed run log, inside the SUPPLIED
  arm section only; the TREAT path never invokes the installer.

The NO-M arm in the reproduction behaves as C281 reported: the
rebound finds divisor 24, but Y's memorized lookup has no entry for
24, so the goal fails (L2-FAIL). The intermediate is causally
necessary in the original world too.

## Part 2: Transfer (R5-R11)

The transfer world (frozen in PREREG.md section 3): training divisors
{24,36}, sealed divisors {48,60,72}, relations 81/82 with sealed
83/84, validity T1 (v = D*q + r, q in [2,3], r in [0,7]) and T2
(q in [2,3], r in [1,8]). The driver self-check passes with zero
mismatches (LABEL-CHECK T1 ok=22, T2 ok=18), so the hand-derived
label tables are consistent with the validity rules.

The machinery file tr_learner.zag is sha256-identical to the
committed C281 glm_learner.zag
(ca1110f65bc13b6bc05ba7bfc086a0f06d9e0323f0288f4126887453d9285e1f).
Only the driver world changed.

- R5 TRANSFER-SOLVE: PASS both. H1 TREAT Z: the frozen
  hand-derived trace reproduced exactly: PHASE1 tries 2 singles and
  4 pairs then L1-FAIL (6 tries); PHASE2 constructs M' with
  C-ROUND 1 base=0 win=1,0,0 gain=2 score=2; candidates scanned
  84, 83, 82 (distractor first); X rebound to 84 gives 7 -> 14,
  rejected; X rebound to 83 gives 48 -> 96, promoted: Z-COMP z=6
  a=5 b=1, REBOUND a=5 param=83 rebound_of=0, ARM-RESULT PASS (10
  tries total, as predicted). H2 TREAT Z: L1-FAIL on all 9 ordered
  mode pairs; PHASE2 builds M', rejects rel=84 (7->14), then
  VC-COMPOSE ok m1=1 m2=2 rel=83, ARM-RESULT PASS. m_created=1,
  M-PROG bytes (1,0,0) in both.
- R6 TRANSFER-NECESSITY: PASS both. L1-ONLY, ABL-X, ABL-Y, FRESH
  all fail as frozen.
- R7 TRANSFER-M-NECESSARY (ablation): PASS both. NO-M
  (allow_build=0): the rebound still finds divisor 48, but Y falls
  back to the memorized lookup, which has no entry for 48, so the
  goal fails (L2-FAIL). Removing M destroys the advantage while
  leaving rebinding intact: the intermediate is causally necessary,
  and L2 rebinding alone is insufficient.
- R8 TRANSFER-CREATED: PASS. (a) The creation trace shows
  C-ROUND 1 with gain=2, final program [ADD R0,R0] non-empty,
  score 2/2 on the T1 labels. (b) Origin audit clean: the
  machinery contains no transfer-world literals in code (the only
  word-boundary match is the byte-offset "24" in the M slot layout
  comment, documented in NAMECHECK.md; the constructor cannot read
  comments); in the transfer drivers every line containing 83 or 84
  also contains add_fact (world setup only); no
  GRAMMAR_TO_CONSTRUCTION, no CHAIN_COUNT, no signature literals in
  composer code. (c) The transfer TREAT output contains no
  SUPPLIED-INSTALL line (the installer fires exactly once per log,
  inside the SUPPLIED arm).
- R9 TRANSFER-REUSE: PASS both. Z2 (4 -> 120) solved via the
  persisted composite (H1: Z-SINGLE m=6 in PHASE1; H2: M-PRESENT
  reuse then VC-COMPOSE ok m1=1 m2=2 rel=83); build_count stays 1
  after Z and Z2 (M persisted, not rebuilt).
- R10 TRANSFER-REVISE: PASS both. T2 labels arrive: ADAPT
  cur_score=0, extension round winner (4,0,0)=INC R0 gain=2,
  ADAPT-CODE 2; M-PROG n=2 gen=1 created=1 build_count=2
  bytes=1,0,0,4,0,0,; M-PREV n=1 sup=1 bytes=1,0,0,; Z3 (5 -> 145)
  solved through the revised M (H1: Z-SINGLE m=6, 72 -> 145).
- R11 TRANSFER-DETERMINISM: PASS. 3/3 byte-identical runs per
  transfer binary (sha256 below).
- R12 TOOLCHAIN: PASS. Safebin active for the whole run;
  `which python3 python` empty at start and end; pure Zag; 0
  modes/bridges/handlers.

## The critical transfer result, in detail

The transfer world's validity rule T1 makes the C281 solution
[INC R0] (w = D+1) score 0: D+1 is labeled 0 for both training
divisors. A learner that merely retrieved the C281 intermediate
would fail. Instead the greedy constructor, running the identical
generic machinery over the new labeled experience, selected
[ADD R0,R0] (w = 2D) as the unique first-max winner with gain 2.
The final program form differs from C281's because the world
differs: the intermediate is constructed from experience, not
recalled. Under the T2 regime shift the learner extended (not
rebuilt) the intermediate to [ADD R0,R0, INC R0], retired the old
form to Mprev with sup=1, and the persisted composite solved the
new sealed goal through the revised M without recomposition.

SUPPLIED-vs-TREAT discrimination held in the transfer: the
researcher-supplied [ADD R0,R0] passes, and the TREAT path passes
with a visible construction trace (C-ROUND gain>0, created=1, no
SUPPLIED-INSTALL), proving the installer was not involved.

## Digests

Reproduction (rebuilt from committed source):
- repro_h1_bin: 6f076073eb1fdb2728b55c790369588310349e7423692bdaf72c8aba5e764eba (byte-identical to committed h1_bin)
- repro_h2_bin: af7870cd5332a97ab1f2df0ed61674dd77c5b2417ccacf20849533b6b04dc995 (byte-identical to committed h2_bin)
- repro runs H1 1-3: abc3e0182c22f23e73e075549fd977c9f165d6cc000931c4b85f6ba5012ac426 (identical; equals committed)
- repro runs H2 1-3: ee0bf4ba9f8acc289d549c590b96c1ca41269b1939cd39dd8ab09e6f84b3a022 (identical; equals committed)

Transfer (new sealed world):
- tr_h1_bin: 9baef8dc204d624077deb4b457987758a8d4b378fec9f529088f6cb2cadd451e
- tr_h2_bin: 7e77b679b029a53160da2a34dd824df5861c5e19723a5cab8cd14323a6fbcf89
- transfer runs H1 1-3: c03202cddec8074ee75ed0f407be974e8212dce46fd47f769bbc7b1eef767f32 (identical)
- transfer runs H2 1-3: 6bae6757c7f5924f01ba7f6b017fe7a4eeb332a77e043768e6fd07e48bf3368a (identical)

Machinery reuse:
- tr_learner.zag sha256 ca1110f65bc13b6bc05ba7bfc086a0f06d9e0323f0288f4126887453d9285e1f (identical to committed C281 glm_learner.zag)

## Files (all under l3_repro_transfer/)

PREREG.md (frozen in f843cba55), NAMECHECK.md, REPORT.md,
orig_glm_learner.zag, orig_gl2m_h1.zag, orig_gl2m_h2.zag,
orig_build.sh (byte-identical reference copies of committed C281
source), orig_run_h1_1.log, orig_run_h2_1.log (reference copies of
committed run logs), repro_h1_full.zag, repro_h2_full.zag,
repro_h1_bin, repro_h2_bin, repro_h1_compile.log,
repro_h2_compile.log, repro_run_h1_1..3.log, repro_run_h2_1..3.log,
tr_learner.zag (byte-identical copy of the committed machinery),
tr_h1.zag, tr_h2.zag (transfer drivers; logic identical to C281
drivers, world literals changed), tr_h1_full.zag, tr_h2_full.zag,
tr_build.sh, tr_h1_bin, tr_h2_bin, tr_h1_compile.log,
tr_h2_compile.log, tr_run_h1_1..3.log, tr_run_h2_1..3.log.

## Caveats (all preregistered)

- The transfer world is worker-designed, not adversary-designed;
  adversarial-world generality stays open, as with FORAGE before
  RELAY.
- One L2 form (relation rebinding) composed with one intermediate
  form (generator program), as in C281.
- Expected answers used for verification (same honest boundary as
  all H1/H2 waves).
- This build targets the 12 frozen bars; it does not claim Micah's
  full 12-criterion L3 bar.

## Constraints honored

Pure Zag; zero Python (safebin held, `which python3 python` empty);
no em/en dashes in loop documentation; paper untouched; nothing
pushed (commits local on tnn-native-lab, explicit pathspecs only);
0 modes/bridges/handlers; the original C281 directory
(xdomain_grammar_l2m) was never modified (git status clean for that
path throughout).
