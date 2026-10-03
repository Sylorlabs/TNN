# PREREG (FROZEN): DDES V2 independent reproduction from committed source + simple-baseline comparison

Wave: wave-20261002-0221pdt. Lane: DDES.
Status: FROZEN before any rebuild or baseline implementation.
Committed alone before any extraction, build, or run.
This prereg covers pipeline steps 4 (independent reproduction)
and 5 (simple-baseline comparison) only. No SURVIVES claim.

## The three BINDING citation caveats (restated verbatim)

(1) "a menu of size 2 reproduces the sealed phase-2 outputs"
(2) "World G is signature-identical to F by prereg design"
(3) "the derivation-to-record binding is enforced by offline reviewer checks only"

Omitting any caveat when citing the frozen V2 BUILD-PASS is
misrepresentation. The reproduction below neither removes nor
weakens them; the self-red-team section addresses them head on.

## Background (frozen facts, not re-argued here)

- DDES V2 BUILD-PASS stands FROZEN on the REBUILT evidence set
  (wave-20261001-1721pdt, RESULT_DDES_V2_STEPS7_11.md): t*=0
  hole closed (eff_waits clamp + FLAG marker; clamp load-bearing
  per no-clamp ablation; RT2 fails loudly, not silently wrong);
  9/9 bars K-R1 through K-R9; 5 binaries 3/3 byte-identical;
  the fabricated draft is voided and never citable.
- Prior pipeline steps completed: (1) prereg, (2) implementation,
  (3) sealed evaluation. Still open after this lane: (6)
  alternative-explanation attack on the rebuilt set, (7) OOD
  (done within steps 7-11; fresh OOD families still open),
  (8) ablation (done within steps 7-11), (9) transfer/reuse
  (done within steps 7-11; broader transfer open), (10)
  independent red team, (11) governance audit (partially done
  within step 11 of the prior lane; independent audit open).

## Committed source provenance (frozen)

Source commit: 947675258 (wave-20261001-1721pdt wave record;
local only, never pushed). The lane files were deleted from
the committed tree by the later commit f461e812d (mass
deletion, flagged in that wave's GIT-HEALTH commit); the
947675258 blobs are the canonical committed record.
Build sources are extracted via `git show 947675258:...`
into this lane dir and sha256-verified against these pins
BEFORE any build:

- ddesv2_s7.zag:
  2c4fcc5c034e71d132ee3b29b5449fba13d5d012c9d4909d6fe0c1a69365e516
- ddesv2_pre.zag:
  b2e03a8dbc99d6a1c9afb4da7beafdae7957acca1d575d9890c21caa20bf866b
- abl_noclamp.zag:
  569a2312c34407794138229ef2024ddc4e299b34e4950dc3ddc60963a43830b6
- abl_noguard.zag:
  8470161be6f570cf7a52490cb386c7da395efad8ba68c506bb74ca7f12e6c4de
- abl_zerorecord.zag:
  eea8513082ca9eb4ce72868334217bd068bd75f2d5c6be043ea029bc632bd84d

No instrumented build. Plain `znc` build of the extracted
sources only. No edits to the sources; the ablation diffs
(1, 2, 1 changed lines vs main) are re-verified by diff.

## Frozen expected reproduction evidence

Rebuilt binaries must reproduce the frozen run-transcript
sha256 values exactly (each binary run 3/3, byte-identical):

- ddesv2_s7 runs:
  359531a8d94a6fa172597a7d448a14848cb09ba34a60985ed3e607a9a1260743
- ddesv2_pre runs:
  3226c6f11660db13519f87daa08c92695ded91aa5b9416cede3a0f7ae6313c93
- abl_noclamp runs:
  ac0ff81f359edae5b080cc2c8c14f13b296cf57cb97b187899c5f04e129bbcaa
- abl_noguard runs:
  dc2e239e81ee7454c741ead6f1f483a2e5abe04a22cbe2d741b76306dd5430b3
- abl_zerorecord runs:
  d3c1d19c29ddf078be97caa9d24a90572fe2595a69f3c81d0f34d8a223afa360

Rebuilt binary sizes expected: ddesv2_s7_bin 75589 bytes,
ddesv2_pre_bin 29780 bytes. Build stderr expected: exactly the
93-byte unconditional zagd-availability warning. Run stderr:
0 bytes every run. Exit 0 every run.

The sealed 9/9 bars (K-R1 through K-R9, frozen in
PLAN_DDES_V2_STEPS7_11.md of wave-20261001-1721pdt) must
re-pass on the rebuilt binaries, verified from the rebuilt
transcripts: exact FLAG lines (8 derivation targets with
t*==0, 8 FLAG lines, 0 zero-wait plans in the repaired trace),
pre-repair silent-wrong pattern on F, K loud
NO-DISCRIMINATING-PLAN, J loud CLASS-MISMATCH + CONVERGE-FAIL
with 0 EXEC lines, no-clamp re-opens silent-wrong on F,
no-guard prints ABL-PROBE with SCAFFOLD-CALLS 0,
zeroed-record 5 CLASS-MISMATCH on phase B, R_H byte-exact
carry-through on sealed I, RT1 2/2 correct, RT2 2/2 loud
CONVERGE-FAIL.

## Simple-baseline specification (frozen before implementation)

Purpose: compare the GUIDED derivation (arrival computation,
frontier scan, target V*/t* synthesis) against UNGUIDED
experiment synthesis with a strictly larger evaluation budget.
The baseline is not deliberately crippled: it uses the same
world-simulation semantics and gets more candidate evaluations
than the guided path.

- Name: ddes_randbase.zag (new file, written after this prereg
  is committed; it implements exactly this spec).
- Worlds: the six phase-A derivation worlds from the frozen
  1721pdt plan, same definitions (F, A, H, K, RT1, RT2).
- World simulator (shared semantics, identical to the EXEC
  ground truth of the frozen traces): variables X=0, Z=1, Y=2;
  rule (src,dst,d) fires at the first W tick t with t >= d
  while src is active; same-tick fixpoint chaining within a
  tick (a rule whose src becomes active during the tick may
  fire in the same tick); S stimulates X at t=0; OX/OY/OZ
  read the current value of X/Y/Z. This matches every frozen
  EXEC real value (F cfg0 [S,W,OY] real=1; F cfg1 real=0;
  A cfg0 real=0; A cfg1 real=1; H cfg0 [S,W,OZ] real=1;
  H cfg1 real=0; RT1 cfg0 [S,W,OZ] real=1).
- Candidate plan space (unguided, no arrival/frontier/target
  computation): [S] + w waits (w in 0..2) + one observation
  op (OX, OY, or OZ). 9 shapes.
- Sampling: B=64 candidates drawn with replacement by a seeded
  deterministic PRNG (xorshift32, seed 0x00DD4242; full determinism, no wall-clock seed). The same
  64-draw sequence is used per world.
- Candidate evaluation: simulate the candidate under h0 and h1;
  a candidate is discriminating iff predicted observations
  differ. Select the FIRST discriminating candidate in sample
  order; if none, emit NO-DISCRIMINATING-PLAN (loud fail, no
  convergence claimed).
- Execution check: run the selected plan on cfg0 (true h0) and
  cfg1 (true h1); eliminate the hypothesis whose prediction
  disagrees with the observed real value. Verdict per world:
  CORRECT (true hypothesis survives and false eliminated on
  both configs), SILENT-WRONG (false survives or true
  eliminated while convergence is claimed), LOUD-FAIL (no
  candidate or predictions agree at execution).
- Budget accounting: 64 candidate evaluations per world vs the
  guided path's 1 plan synthesis per world. The baseline's
  budget is strictly larger in candidate evaluations with
  identical per-evaluation simulation cost, so any guided-path
  advantage is guidance, not budget.
- Reporting: per-world baseline verdict vs guided verdict
  (guided: F CORRECT, A CORRECT, H CORRECT, K LOUD-FAIL,
  RT1 CORRECT, RT2 LOUD-FAIL), plus cost fields
  (candidates_evaluated, wall_ms). Interpretation must note
  that the baseline tests candidate proposal only; it does
  not exercise record persistence, the class-stamp gate, or
  phase-B reuse.

## Frozen kill bars for this lane

- R-R1 (source pins): all five extracted sources sha256-match
  the pins above before any build. Mismatch = stop.
- R-R2 (byte-identical rebuild): rebuilt binaries sha256-match
  the committed binaries at 947675258 (verified via git show
  of the _bin blobs). Mismatch = REPRODUCTION-FAIL.
- R-R3 (sealed 9/9 re-pass): rebuilt run transcripts
  sha256-match the frozen values AND all nine K-R bars
  re-verify from the rebuilt transcripts. Any byte or verdict
  divergence = REPRODUCTION-FAIL; stop, report the diff, do
  not patch forward.
- R-R4 (baseline comparison): baseline implements the frozen
  spec exactly; per-world verdicts and cost fields reported;
  baseline fully specified in BASELINE_COMPARISON.md.
- R-R5 (determinism): 3/3 byte-identical reruns of every
  rebuilt binary AND 3/3 byte-identical baseline runs.
- Governance: pure Zag at every stage; safebin PATH; zero
  em-dash and zero en-dash bytes in all lane files
  (byte-checked with check_no_dash.sh); no commits outside
  this lane dir; no push; no promotion claims; verdict names
  the exact frozen bars that governed it.

## Self-red-team prompts (answered in BASELINE_COMPARISON.md)

1. Does the eff_waits clamp make the reproduction result
   vacuous (i.e., does the guided path succeed only because
   the clamp trivializes the worlds)? Check: RT2 shows the
   clamp destroys a discrimination DDES's own predictor would
   otherwise see; K and J show loud failure is still reachable.
2. Is the baseline fair (not deliberately crippled)? Check:
   strictly larger candidate budget, same simulation
   semantics, deterministic, full reporting of the
   worlds where it matches or beats the guided path.
3. Does the reproduction strengthen or weaken caveat (3)
   (derivation-to-record binding enforced offline only)?
   Answer honestly: reproduction re-runs the same binding;
   it does not make the binding self-enforcing.
