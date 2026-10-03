# PREREG: H-PI-REV2 narrowed single-conflict claim (step-7 follow-up, FROZEN)

Status: FROZEN (drafted wave-20261001-2321pdt, HPIREV2 lane; the lane
worker commits this document alone before any narrowed-step
implementation file, transcript, binary, or build log exists in the
lane; commit-order self-check applies; UNVERIFIABLE ORDERING voids
this prereg). The five sealed world files already exist in
sealed_s8/ (they were generated and mechanically validated during
prereg preparation); their sha256 hashes are frozen in this document
and the executor verifies them at load time before any run. No
implementation, no execution follows this freeze in this wave beyond
what this text specifies; any further amendment must be committed
transparently and re-frozen before execution; no bar may be altered
after seeing results. Builders report BUILD-PASS/BUILD-FAIL only.

## Provenance and the narrowed step

Step 7 (wave-20261001-2021pdt) returned FAIL with bounding on the
bounded-L2 revision claim: families A, C, D passed every bar;
family B (two simultaneous conflicts) tripped K-OOD-W1
(fails_total=1, confined to the held-out RW) and K-OOD-W3. Per the
frozen bounding matrix, the bounded-L2 claim BOUNDED to
single-conflict revision: it was not killed (no family-A fail) and
not voided (all V0-V3 prechecks passed). The step-5 PASS and step-6
PASS records are untouched by that outcome and by this follow-up.

This prereg freezes the surviving narrowed claim and tests it on
fresh sealed single-conflict worlds. It does not re-litigate the
two-conflict case: the single-conflict bound is already established.
It does not weaken any bar to force a pass.

## The narrowed claim (one mechanism, one question)

The frozen bounded-L2 revision procedure (proc_revise2.zag at
847a8f10f, byte-identical) revises correctly and cheaply on every
sealed world with at most one conflict, and on multi-conflict worlds
it flags the uncovered conflict explicitly rather than converging
silently to a wrong solution.

Question: does the frozen procedure meet the frozen bars below on
five fresh sealed single-conflict worlds spanning novel bytes,
novel positions, longer inputs, novel template shape, and the two
single-conflict variants of the step-7 family-B regime, and does it
produce the frozen explicit bound-trip signal (never silent wrong
convergence) on the established two-conflict world?

## Frozen reference points (not re-decided here)

- Frozen mechanism: proc_revise2.zag at 847a8f10f, sha256
  dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12.
  Cognition source delta must be 0.
- Frozen executor lineage: the step-7 harness approach (frozen
  machinery lines 1-606 byte-verbatim plus a new staging main) is
  reused; harness code is recorded separately from cognition source.
- Step-7 two-conflict specimen for the bound-trip regression:
  wave-20261001-2021pdt sealed family-B world, executed via the
  frozen s7_exec_bin (sha256
  155cea26379389788b1f3e8bb3b771763083489d81447791fdb479072054dc9b,
  110645 bytes). Regression use only; it is not part of the sealed
  set and its outcome cannot change the established bound.
- Ceiling: bounded L2, not L3. A BUILD-PASS here means the narrowed
  single-conflict claim holds on the tested worlds; it is not
  evidence toward L3 and must not be claimed as such.

## The five sealed worlds (fresh; step-7 worlds are regression only)

Each world is a directory entry set under sealed_s8/ with five
files: TW.txt (3 base pairs), FW.txt (1 counterexample pair), RW.txt
(1 held reuse pair, sealed from the revision phase until revision
completes), CONFLICT.txt (declared conflict set, intended rule R_w
in words, and for D2 the intended structure S_w), EW.txt (exactly 5
expectation pairs: the 3 base pairs as updated by R_w, plus FW, plus
RW). Pair notation matches the frozen fixtures, one pair per line.

Design seeds (committed here; the byte/position/length choices are
the seeds, applied through a deterministic hand construction):

- A2 (novel alphabet and position): single conflict; all input bytes
  disjoint from A_frozen and from every step-7 world byte; declared
  conflict (1,84), position not 0; input lengths <= 4. Base program:
  repeat last byte. Predicted: V0 first_fit=38, DIAG (0,81), ALT
  first_fit=3 (constant-1), revision_evals=6.
- B1 (single-conflict variant, first-conflict style): declared
  conflict (0,33); base program repeat last byte. Predicted: V0=38,
  DIAG (0,33), ALT first_fit=2 (C0), revision_evals=6.
- B2 (single-conflict variant, second-conflict style): declared
  conflict (2,58); base program repeat last byte. Predicted: V0=38,
  DIAG (0,47), ALT first_fit=4 (C2), revision_evals=6.
- C2 (longer inputs): single conflict; every input length >= 8 (TW
  9, 11, 8; FW 9; RW 9); declared conflict (0,59); base program
  repeat last byte. Predicted: V0=38, DIAG (0,59), ALT first_fit=2
  (C0), revision_evals=11.
- D2 (novel template shape): declared conflict (3,83); base program
  repeat input[1] (benum index 3). Intended structure S_w =
  IF(byte-equality(0,80), C3 (benum index 24), repeat-input[1]):
  branch count 1 vs 2 in S_frozen, then-branch C3 vs C0,
  else-branch repeat-input[1] vs repeat-last-byte; also distinct
  from the step-7 D world (C2 then-branch, repeat-first-byte else).
  Expressible by the frozen construction operators (single IF
  wrapping per specialize; alt via frozen dsearch on FW alone; v_old
  via frozen dsearch on TW). Predicted: V0 first_fit=3, DIAG
  (0,80), ALT first_fit=24, revision_evals=6.

Frozen sha256 hashes (executor verifies at load time; any mismatch
aborts the run, no verdict):

A2_CONFLICT.txt 756251b8a0b6bbddb0cb409ba21c997706a224040cb72b999f1ae3452b6080c2
A2_EW.txt 7069934ac08bdbe61570afed7c2d2d12d6cd12b4f4ce8e4d5a8b072e73a1ab00
A2_FW.txt bf1815258ccc7afb5f090106fc9b32ece0e278aedd419e09631e5e980e640922
A2_RW.txt 105860a0227161f0ee8d36224b6f8364dd5acb7866554c87ce8425da15c11071
A2_TW.txt f458f839f86764e896f680bfdf66423865391398210b39008b7506230f4b2757
B1_CONFLICT.txt 8b0e4efbc076a7cfb644eb8a65f65331d0f32fdc02f6622b875c37029766e3ef
B1_EW.txt 7439e18404648fe16da24a12ebf9c490110a905c9d961fddf944a4ebaba8efc5
B1_FW.txt 4e8617656ce3b5be60fd33499290fc3a3ea47df562773c87419c063c548c3fd2
B1_RW.txt efbaa6114ce6df0e50794e2bb32af7603b8ed9eaf2e600f5c84b887d3dbc3e38
B1_TW.txt 1f30bb1c8b2b8810053946959ed716ffcdfbb1f72ddcc2e1604acac2f766fc7c
B2_CONFLICT.txt 16a03ea8a9b214acf8d86d6fe016be60c7b41c4ee17edfc0840ec5f646364a50
B2_EW.txt 4952ff45300d83691d1b9040ec587634d99ec3f67e86c66b9fb93703a41efd10
B2_FW.txt aba803ad26f57a48283540886957b934c67950e5cfbd41e7db0fac0dbe310bf3
B2_RW.txt 6407adffa3622c2624d3b2566faf75b138fa37db456f6bcb5385e31c1646cfba
B2_TW.txt 8433db91a4d5924f2d7c87d164f81c490046e8bb79fed8e1d2462d3760f1cdb4
C2_CONFLICT.txt 457bd91bf2aa6f1f16918fd1dc7d77556bec60c4fda2255fa576c7349bb3e605
C2_EW.txt a71c90e415d809b378fb41c93001ebc02cd7a82c15510d839de356c058348d94
C2_FW.txt 59187d96a192068080a0ca7c1dc6ddca77f47a035b7276159a680d37266e1cd1
C2_RW.txt 4d6427de04268e5f1d9c77bfff20e248aa101d32e378eb359c5daa5354179c60
C2_TW.txt 329c6f68d78ff1e023625a2ed864c5303d95070242196d0d7355f87954e8288d
D2_CONFLICT.txt ccc3e62fc18eb9af24d66b301b46a47efc587159241032c3782739a588d73a20
D2_EW.txt 1de830960b2640a6f8abfd8de7085b48d790af194fb8fccf1fd368efc3373675
D2_FW.txt 2d5083a3c47f0f41fc5f44d3a9e66e02f520db072e74755c6eddc27fa57
D2_RW.txt 96d45fd7dc77af5cdcc58177a746336b4b7c4cf86a892db9539895c2ea17d56c
D2_TW.txt fdf7a14258247d058e861aeec00b590736c6f5cf7bf2cdf984c241d07a086814

## World validity prechecks (void, never a verdict)

The executor runs these mechanically before any revision execution,
using only frozen baseline code; any failure voids that world and
the whole narrowed run: no verdict is recorded, and the remedy is a
transparent amendment with a redesigned world, re-frozen. A malformed
world must never be laundered into a FAIL.

- V0 (base learnable): B1 (frozen dsearch over the 1055 benum
  programs) on TW alone achieves first_fit >= 0 with fails-on-TW=0.
  Record w_first_fit_tw.
- V1 (disjointness): bytes(FW input) disjoint from bytes(TW inputs);
  the declared conflict bytes are a subset of bytes(FW input);
  bytes(RW input) disjoint from bytes(TW inputs) except for declared
  conflict bytes; RW's input matches the declared conflict at its
  declared position. Family A2 additionally: all TW/FW/RW input
  bytes disjoint from A_frozen.
- V2 (problem real): v1w (the V0 first fit) mispredicts FW.
- V3 (impossibility recheck): B1 over TW+FW evaluated against EW
  restricted to TW+FW enumerates all 1055 benum programs with
  first_fit=-1.
- V4 (expectation consistency): EW equals R_w applied to the 5
  check inputs; R_w is a strict parametric (A2, B1, B2, C2) or
  structural (D2) generalization of the frozen conflict-rule form.
  For D2, S_w differs structurally from S_frozen and is expressible
  by the frozen construction operators, as documented in
  D2_CONFLICT.txt.

## Frozen kill bars

Per sealed world w in {A2, B1, B2, C2, D2}; BUILD-PASS requires all
of them.

- K-SC-W1 (correctness, accuracy floor 100 percent): the revised
  procedure achieves fails=0 on all 5 EW pairs. Kill: any
  w_fails_total > 0. A trip KILLS the narrowed single-conflict
  claim: the bound was exactly single-conflict, so a
  single-conflict failure falsifies even the narrowed claim.
- K-SC-W2 (revision-eval ceiling): revision_evals <= 25, strict.
  Kill: revision_evals > 25.
- K-SC-W3 (reuse): RW is predicted correctly with zero new
  DIAGNOSIS, PRIMITIVE-CONSTRUCTED, or VERSION lines after the
  reuse check. Kill: any misprediction or any new revision marker.
- K-SC-W4 (determinism): per world, 3/3 runs byte-identical
  (sha256 match), exit 0, zero stderr bytes. Run matrix: 15 runs
  (5 worlds x 3). Kill: any divergence, nonzero exit, or any
  stderr byte.
- K-SC-W5 (purity and docs): pure Zag only at every stage; zero
  Python; zero em-dash and zero en-dash bytes in all new lane
  files (byte-checked). Kill: any Python use or any forbidden
  byte.

Bound-trip bar (the second half of the narrowed claim):

- K-SC-B (explicit bound-trip signal, never silent wrong
  convergence): on the two-conflict regression world (step-7
  family B, frozen s7_exec_bin, hash-verified before running),
  3/3 runs exhibit ALL of: (S1) w_fails_total > 0, the run
  reports failure on EW and does not claim success; (S2) the
  transcript contains COUNTEREXAMPLE_DETECTED at the W3 reuse
  probe for the held-out RW, the uncovered conflict is explicitly
  flagged when probed; (S3) zero new DIAGNOSIS,
  PRIMITIVE-CONSTRUCTED, or VERSION lines appear after the W3
  marker, the mechanism does not silently re-revise into a wrong
  stable state. Kill (silent wrong convergence): w_fails_total=0
  on the two-conflict world, or no COUNTEREXAMPLE_DETECTED at the
  reuse probe. A trip KILLS the flagging half of the narrowed
  claim. This bar re-verifies the already-established bound; it
  does not re-litigate it.

Architecture bars (preserved):

- K-ARCH1 (zero cognition source delta): the frozen mechanism
  source is byte-identical before and after; cognition source
  delta = 0 exactly. World files, validator, and test harness code
  are recorded separately. Kill: any nonzero cognition source
  delta.
- K-ARCH2 (no architecture growth): new_semantic_cases=0,
  new_modes=0, new_bridges=0, new_routers=0, new_handlers=0; no
  protected-core changes. Kill: any nonzero value.

## Verdict semantics

BUILD-PASS: every bar above holds; cost accounting complete.
BUILD-FAIL: names every tripped bar. A K-SC-W1/W2/W3 trip on any
sealed single-conflict world, or a K-SC-B trip, KILLS the narrowed
claim as stated (it is already the narrowed residue; there is no
further honest narrowing without changing the question). A
K-SC-W4, K-SC-W5, K-ARCH1, or K-ARCH2 trip is FAIL with cause
named (determinism, purity, or architecture): no claim about the
mechanism follows because the failure is in the run's premises,
recorded as information gained. Any validity precheck failure:
VOID, never a verdict; transparent amendment with a redesigned
world, re-frozen. No outcome here weakens, reinterprets, or
re-scores any frozen bar from steps 5, 6, or 7; the step-7
FAIL-with-bounding record stands.

## Sealed evaluation protocol and disclosure

- The five worlds were designed and mechanically validated by the
  lane worker (non-independent: no separate adversary or red team
  was available in this wave). Mitigations, frozen here: the
  world byte/position/length seeds and the sha256 of all 25 world
  files are committed in this prereg before any execution; the
  executor verifies hashes at load time; the executor re-runs
  V0-V3 mechanically and any void triggers transparent amendment
  and re-freeze, never silent repair; no world may be tuned after
  seeing execution results.
- The pre-freeze mechanical validation ran the frozen dsearch,
  diagnose, and scoring logic over the world designs: V0
  first fits (38/38/38/38/3), V1a-e, V2 det=1 on all five, V3
  first_fit_twfw=-1 on all five, predicted DIAG winners
  (0,81)/(0,33)/(0,47)/(0,59)/(0,80), predicted ALT first fits
  (3/2/4/2/24), predicted revision_evals (6/6/6/11/6), V4 EW
  consistency: ALL-WORLDS-VALID, exit 0. Two design slips found
  and fixed pre-freeze (A2 RW byte at the declared position; B2
  FW/RW transcription and conflict-byte placement; C2 FW/RW
  length); the frozen hashes above are of the corrected files.
- Per world execution order: load-time hash verify, V0/V1/V2/V3
  prechecks, train v1w, present FW, run the frozen revision
  (record revision_evals), score against EW (W1, W2), present RW
  after revision ACTIVE (W3). Repeat 3x per world (W4). 15 runs.
  Then the K-SC-B regression: 3x runs of the frozen s7_exec_bin
  on family b, hash-verified byte-identical to the step-7 record.
- The executor uses only the frozen mechanism machinery and
  frozen baseline code; the harness stages world literals
  transcribed from the sealed files, verified byte-exact
  (STAGE lines diffed); no world-specific branching, no new
  semantic cases, no modes, no bridges, no routers, no handlers.
  RW is never observed before the W3 phase.
- Code-sharing disclosure is mandatory in the result doc.

## Cost accounting (required in the result doc)

Machine-greppable fields, per world w in {A2,B1,B2,C2,D2}:
w_first_fit_tw, w_b1w_enumerated, w_revision_evals, w_fails_total,
w_reuse_correct, w_reuse_new_revision_lines, w_wall_ms; plus
binary_bytes (each binary), source_delta_lines (harness and
validator only), cognition_source_delta (must be 0),
new_semantic_cases, new_modes, new_bridges, new_routers,
new_handlers. Kill: any missing field; any nonzero
architecture-growth field; any nonzero cognition_source_delta.

## Honest boundaries: bounded L2 ceiling, NOT L3, never SURVIVES

This follow-up does not test representational invention, template
invention, or any L3 criterion. A BUILD-PASS means the narrowed
single-conflict claim holds on the five tested worlds; it is not
evidence toward L3 and must not be claimed as such. It is never
SURVIVES: remaining pipeline steps (transfer/reuse beyond the
single probe, second independent red team, governance audit) are
untouched. Nothing here alters the step-5 PASS, step-6 PASS, or
step-7 FAIL-with-bounding records.

## Skeptic self-attack (and answers)

Attack 1: the worlds were designed and validated by the same worker
that executes, so the seal is theater; the worker could have tuned
the worlds until the validator passed, which is exactly what
happened with the three pre-freeze fixes.

Answer: the pre-freeze fixes are disclosed above, and tuning
pre-freeze is the legitimate role of design plus certification
(the step-7 adversary and certifier iterated the same way before
committing hashes). The seal binds post-freeze: hashes are frozen
here, the executor re-verifies V0-V3, and any void forces
transparent amendment and re-freeze rather than silent repair. The
non-independence is a stated limitation, not a hidden one, and it
caps the claim: this is a narrowed re-test, never SURVIVES, and a
second independent red team remains a pipeline requirement.

Attack 2: the bound-trip signal is just the mechanism failing
loudly; calling COUNTEREXAMPLE_DETECTED a decline or abstain
dresses up a limitation as a feature.

Answer: the claim is phrased to match the frozen binary exactly:
it flags rather than silently misbehaving. S1-S3 operationalize
the distinction between loud failure (honest, usable: the learner
knows the revision did not cover the evidence) and silent wrong
convergence (the revision claims success it did not earn). The
prereg does not claim the mechanism abstains from revising; it
claims the mechanism never silently claims success on
multi-conflict worlds. A future mechanism could add an explicit
ABSTAIN primitive; that would be a different claim under a new
prereg.

Attack 3: five worlds cannot establish even a bounded generality
claim; a PASS here is five anecdotes.

Answer: the claim is already bounded to single-conflict revision,
and the five worlds span the four dimensions the step-6 ablation
pinned as load-bearing (bytes, position, length, template shape)
plus both single-conflict variants of the bounding regime. The
verdict claims only the tested regimes, never broad generality,
and the never-SURVIVES rule caps inflation. Five worlds test the
narrowed claim; they do not certify it.

## Commit-order self-check (binding)

This prereg must be committed ALONE before any narrowed-step
implementation file (validator source beyond this commit,
executor harness source, binary, transcript, or build log)
exists in the lane. Verification: `git log --format=%H --
docs/lab/rsi/runs/wave-20261001-2321pdt/HPIREV2/PREREG_PI_REV2_NARROWED.md`
must show exactly one commit for this file, and that commit must
strictly precede the first commit adding any narrowed-step
implementation artifact. The sealed world files in sealed_s8/ are
design artifacts whose hashes are frozen here; they are committed
after this prereg. UNVERIFIABLE ORDERING voids this prereg. No bar
may be altered after results are seen.

No em-dashes in this documentation.
