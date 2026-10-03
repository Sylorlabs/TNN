# SEALED_S7_EXEC: step-7 sealed OOD execution record (HPIREV2, wave-20261001-2021pdt)

Executor: step-7 executor worker (this file's author). Worlds designed by
the independent adversary (dea2694d1), certified V1-V4 by the independent
certifier (53e92c8ce, CERT_S7_V1V4.md). The executor designed no world and
certified nothing. Frozen prereg PREREG_PI_REV2_STEP7.md (201ed5a05)
governs; no bar was altered after results.

## 1. Frozen source binding and builds

- Frozen mechanism source:
  docs/lab/rsi/runs/wave-20260929-2321pdt/pi_rev2/proc_revise2.zag
- Working-tree sha256 before building:
  dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12
- Committed blob at 847a8f10f (git cat-file): identical hash. Match.
- Pinned znc rebuilds (3x): byte-identical, sha256
  7b4caa77d2e67e6df14f5f1fecf0f75180d50338961b80e00073ec06883a395c,
  106770 bytes, cmp-clean against the lane's rev2_r_bin (same hash).
- Frozen source sha256 re-verified after all runs: unchanged
  (dd3cb02d...). cognition_source_delta = 0.

## 2. Load-time hash verification (before any build or run)

20/20 world files verified against the adversary manifest
SEALED_S7_WORLDS.md, using the corrected C_FW.txt hash from
CERT_S7_V1V4.md Erratum 1
(8d6f3362dc476447f1e07402e97958a654fe76558114adcad4ef7af40bd3fbf8);
the manifest file itself was not edited, per the no-modify rule.
The malformed 61-character manifest line for C_FW was not used.
All 20 files: OK. No file failed; the run proceeded.

## 3. Executor harness (disclosure)

The frozen binary hardcodes its fixtures in main and accepts only one
adversary byte, so it cannot be pointed at sealed world files. The
executor built s7_exec.zag as: lines 1-606 of proc_revise2.zag copied
byte-verbatim (diff-verified: all machinery benum, dsearch, loadseq,
extract_seq, predict, observe, diagnose, build_test, specialize), plus
427 new harness lines (helpers hasbyte1/hasbyte3/infrozen,
count_candidates, emit_stage, and a new main). The new main stages one
family's sealed pairs as literals (argv[1] = a/b/c/d) and runs the
prereg order: V0/V1/V3 prechecks, train v1w, present FW (V2), frozen
revision (diagnose, build_test, alt dsearch on FW alone, specialize),
score against EW (W1, W2), present RW after revision ACTIVE (W3). The
code path is identical for all four families; only staged literals
differ. No world-specific branching, no new semantic cases, no modes,
no bridges, no routers, no handlers. RW is never observed by the store
before the W3 phase (observe is called on RW only after VERSION ACTIVE).

- Harness binary s7_exec_bin: 3/3 byte-identical builds, sha256
  155cea26379389788b1f3e8bb3b771763083489d81447791fdb479072054dc9b,
  110645 bytes.
- Transcription fidelity: every staged literal verified byte-exact
  against the sealed files (STAGE lines diffed against TW.txt+FW.txt and
  RW.txt per family): 8/8 EXACT.
- revision_evals formula (frozen from the step-5 execution record):
  diagnosis candidates ranked + 1 primitive-construction test + 1
  SPECIALIZE application. Candidates counted mechanically by
  count_candidates, a store-driven mirror of diagnose's candidate logic.

## 4. Run matrix and determinism (K-OOD-W4)

12 runs (4 worlds x 3). All exit 0, all stderr files 0 bytes.
Per-family stdout 3/3 byte-identical (cmp-clean):
- A: 88a7475ffdf77f178be48109fc8c4527266c4e8cb5ae5c5176208b364a38f966
- B: f56080d65aeb2ceba9a8134784872381bd17293d8df48010835b482d17d9268d
- C: 9335409533bd44714430ee2bc7c072ef5668121d6c18bcd67656dbb9a36d923d
- D: 757dc89aead014f7326f5945ab497972c1f2ccf8828b32f5775dd284712c5e9e
K-OOD-W4: PASS on all four worlds.

Wall times (run1): A 9 ms, B 9 ms, C 17 ms, D 24 ms.

## 5. Precheck results (V0-V3, mechanical, frozen baseline code)

All four worlds: every precheck PASS. No world voided.

| world | V0 first_fit_tw | V0 fails_on_tw | V1 | V3 first_fit_twfw | V2 det |
| A | 38 | 0 | PASS (a-e) | -1 | 1 |
| B | 38 | 0 | PASS (a-d) | -1 | 1 |
| C | 38 | 0 | PASS (a-d) | -1 | 1 |
| D | 2 | 0 | PASS (a-d) | -1 | 1 |

V1 clauses: (a) FW bytes disjoint from TW bytes, (b) declared conflict
bytes subset of FW bytes, (c) RW bytes disjoint from TW bytes except
declared conflict bytes, (d) RW matches a declared conflict at its
declared position, (e, family A only) all input bytes disjoint from
A_frozen. V3 ran dsearch over TW+FW against EW restricted to TW+FW.

## 6. Revision measurements

| world | diag (pos,byte) | alt first_fit | alt_evals | revision_evals | W2 (<=25) |
| A | (0,115) | 4 | 5 | 6 | PASS |
| B | (0,115) | 2 | 3 | 6 | PASS |
| C | (0,115) | 2 | 3 | 10 | PASS |
| D | (0,116) | 4 | 5 | 6 | PASS |

Every measured value (first-fit indices, diagnosis winner, alt index,
revision-eval totals) matches the certifier's static predictions
exactly. No SUPERSEDED lines fired spuriously on any world.

## 7. Per-family per-bar results

Family A (novel conflict alphabet and position):
- K-OOD-W1: PASS. fails_total=0; 5/5 EW pairs correct
  ("hij"->"jjj", "kl"->"ll", "mnop"->"pppp", "stvz"->"vvvv",
  "suvz"->"vvvv").
- K-OOD-W2: PASS. revision_evals=6 <= 25.
- K-OOD-W3: PASS. reuse_correct=1 (det=0), 0 new
  DIAGNOSIS/PRIMITIVE-CONSTRUCTED/VERSION lines after the reuse check.
- K-OOD-W4: PASS. K-OOD-W5: PASS.

Family B (multi-conflict):
- K-OOD-W1: FAIL. fails_total=1; the single fail is RW:
  "uzvz" predicted "zzzz", expected "vvvv". TW (3/3) and FW correct.
  This is the certified expected honest outcome: one branch cannot
  cover two simultaneous conflicts.
- K-OOD-W2: PASS. revision_evals=6 <= 25.
- K-OOD-W3: FAIL. reuse_correct=0 (det=1, COUNTEREXAMPLE_DETECTED);
  0 new DIAGNOSIS/PRIMITIVE-CONSTRUCTED/VERSION lines after the reuse
  check (the fail is the misprediction itself, not a new revision).
- K-OOD-W4: PASS. K-OOD-W5: PASS.

Family C (longer inputs):
- K-OOD-W1: PASS. fails_total=0; 5/5 correct at lengths 8-12.
- K-OOD-W2: PASS. revision_evals=10 <= 25 (8 diagnosis candidates at
  length 8, +1 construction, +1 specialize).
- K-OOD-W3: PASS. reuse_correct=1, 0 new revision marker lines.
- K-OOD-W4: PASS. K-OOD-W5: PASS.

Family D (novel template shape):
- K-OOD-W1: PASS. fails_total=0; 5/5 correct with v_old =
  repeat-first-byte and alt = C2 (the certified S_w composition).
- K-OOD-W2: PASS. revision_evals=6 <= 25.
- K-OOD-W3: PASS. reuse_correct=1, 0 new revision marker lines.
- K-OOD-W4: PASS. K-OOD-W5: PASS.

K-ARCH1 (zero cognition source delta): PASS (hash unchanged, section 1).
K-ARCH2 (no architecture growth): PASS. new_semantic_cases=0,
new_modes=0, new_bridges=0, new_routers=0, new_handlers=0; no
protected-core changes.
K-OOD-W5 (purity and docs): PASS. Pure Zag at every stage; `which
python3` and `which python` print nothing under the safebin PATH; no
other interpreter or compiler invoked. Byte scan of all new lane text
files: zero em-dash and zero en-dash bytes.

## 8. Cost accounting (machine-greppable, run1 values)

w_first_fit_tw: A=38 B=38 C=38 D=2
w_b1w_enumerated: 1055 (all worlds)
w_revision_evals: A=6 B=6 C=10 D=6
w_fails_total: A=0 B=1 C=0 D=0
w_reuse_correct: A=1 B=0 C=1 D=1
w_reuse_new_revision_lines: 0 (all 12 runs)
w_wall_ms: A=9 B=9 C=17 D=24
binary_bytes: s7_exec_bin=110645 rev2_r_bin=106770
source_delta_lines (harness only): 427
cognition_source_delta: 0
new_semantic_cases: 0
new_modes: 0
new_bridges: 0
new_routers: 0
new_handlers: 0

Supplementary (not in the frozen formula): alt dsearch evals on FW
alone: A=5 B=3 C=3 D=5. revision_evals + alt_evals stays far below 25
on every world (max 13 on C).

## 9. Verdict

step-7 FAIL with bounding, per the frozen bounding matrix.

Tripped bars: K-OOD-W1 on family B (fails_total=1, confined to RW),
K-OOD-W3 on family B (reuse_correct=0 on RW). No other bar tripped on
any world.

Bounding consequence (matrix: "Only family B fails (any of W1/W2/W3)"):
the bounded-L2 claim is BOUNDED to single-conflict revision. Surviving
narrowed claim: revision generalizes across novel bytes, novel
positions, longer inputs, and novel template shapes, but only for
single conflicts. The claim is NOT killed (kill requires a family-A
fail or two or more failing families). The run is NOT void (all V0-V3
prechecks passed on all four worlds; no world was laundered into a
FAIL). The step-5 PASS and step-6 PASS records are untouched.

Observed outcomes match the certified predictions with zero
divergence: Family A full PASS, Family B honest W1 fail on RW only,
Family C PASS, Family D PASS, exactly as CERT_S7_V1V4.md predicted.
No outcome here weakens any frozen bar from steps 5 or 6, and nothing
in this result is evidence toward L3 (bounded-L2 ceiling stands).

## 10. Code-sharing and sealing disclosure

- The harness shares only the frozen machinery (byte-verbatim lines
  1-606 of proc_revise2.zag); no revision-machinery code was altered.
- The frozen binary and frozen baseline discovery code are the only
  cognitive code paths exercised; the harness adds staging, checks,
  and scoring only.
- RW was held from the revision machinery until after revision
  completion: the store's observe() was never called on RW before the
  VERSION ACTIVE marker (transcript shows the RW STAGE line and RW
  observation only after "=== W3 REUSE CHECK ===").
- Executables invoked (K-OOD-W5 audit): safebin tools only (bash,
  sha256sum, cmp, diff, grep, sed, awk, stat, date, head, cat, wc,
  znc, chmod, cp). No python3, python, gcc, cc, perl, ruby, or node
  at any stage.

No em-dashes or en-dashes appear in this file.
