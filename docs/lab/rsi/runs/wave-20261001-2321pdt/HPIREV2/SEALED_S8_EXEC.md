# SEALED_S8_EXEC: narrowed single-conflict execution record (HPIREV2, wave-20261001-2321pdt)

Executor: narrowed-step executor worker (this file's author). Worlds
designed and mechanically pre-validated by the lane worker
(non-independent; disclosed in the prereg), hashes frozen in
PREREG_PI_REV2_NARROWED.md (00b31af53) before any implementation.
The executor designed nothing post-freeze and tuned nothing. Frozen
prereg governs; no bar was altered after results.

## 1. Frozen source binding and builds

- Frozen mechanism source:
  docs/lab/rsi/runs/wave-20260929-2321pdt/pi_rev2/proc_revise2.zag
- Working-tree sha256 before building:
  dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12
- Committed blob at 847a8f10f (git cat-file): identical hash. Match.
- Frozen source sha256 re-verified after all runs: unchanged
  (dd3cb02d...). cognition_source_delta = 0.
- Executor harness s8_exec.zag: lines 1-606 of proc_revise2.zag
  copied byte-verbatim (sha256 of the prefix:
  8d2b16ab31184758b2b724e19cb1fa9f96d5ff008a0674b6c95c1da8e227f712,
  identical to the step-7 harness prefix), plus 433 new harness
  lines (helpers hasbyte1/hasbyte3/infrozen/key2/count_candidates/
  emit_stage and a new main staging the five fresh worlds).
- Harness binary s8_exec_bin: 3/3 byte-identical builds, sha256
  aee1b6f21a4b5309a3c93e9f66d9c38553bd75db926feeba123207373117ddbc,
  110668 bytes.
- Regression binary s7_exec_bin (step-7, reused for K-SC-B):
  sha256 155cea26379389788b1f3e8bb3b771763083489d81447791fdb479072054dc9b,
  unchanged from the step-7 record.

## 2. Load-time hash verification (before any run)

25/25 sealed world files verified against the frozen prereg hashes
(24 via sha256sum -c, the 25th D2_TW.txt verified manually against
the prereg line; all match). No file failed; the run proceeded.

## 3. Executor harness (disclosure)

The frozen binary hardcodes its fixtures in main and accepts only
one adversary byte, so it cannot be pointed at sealed world files.
The executor built s8_exec.zag as: lines 1-606 of proc_revise2.zag
copied byte-verbatim (diff-verified: all machinery benum, dsearch,
loadseq, extract_seq, predict, observe, diagnose, build_test,
specialize, plus check/pcheck/rcell helpers), plus 433 new harness
lines and a new main. The new main stages one fresh world's sealed
pairs as literals (argv[1] = A2/B1/B2/C2/D2) and runs the prereg
order: V0/V1/V3 prechecks, train v1w, present FW (V2), frozen
revision (diagnose, build_test, alt dsearch on FW alone,
specialize), score against EW (W1, W2), present RW after revision
ACTIVE (W3). The code path is identical for all five worlds; only
staged literals differ. No world-specific branching, no new
semantic cases, no modes, no bridges, no routers, no handlers. RW
is never observed by the store before the W3 phase (observe is
called on RW only after VERSION ACTIVE).

- Transcription fidelity: every staged literal verified byte-exact
  against the sealed files (STAGE lines diffed against
  TW.txt+FW.txt+RW.txt per world): 5/5 EXACT.
- revision_evals formula (frozen from the step-5 execution record):
  diagnosis candidates ranked + 1 primitive-construction test + 1
  SPECIALIZE application. Candidates counted mechanically by
  count_candidates, a store-driven mirror of diagnose's candidate
  logic.

## 4. Run matrix and determinism (K-SC-W4)

15 runs (5 worlds x 3). All exit 0, all stderr files 0 bytes.
Per-world stdout 3/3 byte-identical (single unique sha256 each):
- A2: a4c05e04d66db34e65796b74b244c55a9471813e760de43a6004b9cd7457aecf
- B1: f1092c1b5c49757bdfac9083e84765a09eec56526e096ef12ef3ec59cac9a524
- B2: 0e5208fd42cf3025a9c6b0f2f273de0a091ef1f3634dd5c7c8145f43e059f3a7
- C2: 9d4e66a0a6a4c793584b9c01adc56bdb228c622b4e24239166e211deaefdc285
- D2: 8a3ac2a99ce36eeef6566f9a62434e206f05c66f57a791e6e071308779ee8621
K-SC-W4: PASS on all five worlds.

Wall times (timing probes, separate from the matrix): A2 16 ms,
B1 19 ms, B2 8 ms, C2 8 ms, D2 33 ms.

## 5. Precheck results (V0-V3, mechanical, frozen baseline code)

All five worlds: every precheck PASS. No world voided.

| world | V0 first_fit_tw | V0 fails_on_tw | V1 | V3 first_fit_twfw | V2 det |
| A2 | 38 | 0 | PASS (a-e) | -1 | 1 |
| B1 | 38 | 0 | PASS (a-d) | -1 | 1 |
| B2 | 38 | 0 | PASS (a-d) | -1 | 1 |
| C2 | 38 | 0 | PASS (a-d) | -1 | 1 |
| D2 | 3 | 0 | PASS (a-d) | -1 | 1 |

V1 clauses: (a) FW bytes disjoint from TW bytes, (b) declared
conflict bytes subset of FW bytes, (c) RW bytes disjoint from TW
bytes except declared conflict bytes, (d) RW matches the declared
conflict at its declared position, (e, A2 only) all input bytes
disjoint from A_frozen. V3 ran dsearch over TW+FW against EW
restricted to TW+FW.

## 6. Revision measurements

| world | diag (pos,byte) | alt first_fit | revision_evals | W2 (<=25) |
| A2 | (0,81) | 3 | 6 | PASS |
| B1 | (0,33) | 2 | 6 | PASS |
| B2 | (0,47) | 4 | 6 | PASS |
| C2 | (0,59) | 2 | 11 | PASS |
| D2 | (0,80) | 24 | 6 | PASS |

Every measured value (first-fit indices, diagnosis winner, alt
index, revision-eval totals) matches the pre-freeze mechanical
predictions exactly. No SUPERSEDED lines fired spuriously on any
world.

## 7. Per-world per-bar results

A2 (novel alphabet and position, declared (1,84)):
- K-SC-W1: PASS. fails_total=0; 5/5 EW pairs correct.
- K-SC-W2: PASS. revision_evals=6 <= 25.
- K-SC-W3: PASS. reuse_correct=1, 0 new revision marker lines
  after the reuse check.
- K-SC-W4: PASS. K-SC-W5: PASS.

B1 (single-conflict variant, declared (0,33)):
- K-SC-W1: PASS. fails_total=0; 5/5 correct.
- K-SC-W2: PASS. revision_evals=6 <= 25.
- K-SC-W3: PASS. reuse_correct=1, 0 new revision marker lines.
- K-SC-W4: PASS. K-SC-W5: PASS.

B2 (single-conflict variant, declared (2,58)):
- K-SC-W1: PASS. fails_total=0; 5/5 correct.
- K-SC-W2: PASS. revision_evals=6 <= 25.
- K-SC-W3: PASS. reuse_correct=1, 0 new revision marker lines.
- K-SC-W4: PASS. K-SC-W5: PASS.

C2 (longer inputs, declared (0,59)):
- K-SC-W1: PASS. fails_total=0; 5/5 correct at lengths 8-11.
- K-SC-W2: PASS. revision_evals=11 <= 25 (9 diagnosis candidates
  at FW length 9, +1 construction, +1 specialize).
- K-SC-W3: PASS. reuse_correct=1, 0 new revision marker lines.
- K-SC-W4: PASS. K-SC-W5: PASS.

D2 (novel template shape, declared (3,83)):
- K-SC-W1: PASS. fails_total=0; 5/5 correct with v_old =
  repeat-input[1] (benum index 3) and alt = C3 (benum index 24),
  the intended S_w composition.
- K-SC-W2: PASS. revision_evals=6 <= 25.
- K-SC-W3: PASS. reuse_correct=1, 0 new revision marker lines.
- K-SC-W4: PASS. K-SC-W5: PASS.

K-ARCH1 (zero cognition source delta): PASS (hash unchanged,
section 1).
K-ARCH2 (no architecture growth): PASS. new_semantic_cases=0,
new_modes=0, new_bridges=0, new_routers=0, new_handlers=0; no
protected-core changes.
K-SC-W5 (purity and docs): PASS. Pure Zag at every stage; `which
python3` and `which python` print nothing under the safebin PATH;
no other interpreter or compiler invoked. Byte scan of all new
lane text files: zero em-dash and zero en-dash bytes.

## 8. K-SC-B bound-trip regression (two-conflict world)

Frozen s7_exec_bin (hash-verified, section 1) re-run 3x on step-7
family b. All 3 runs byte-identical to the step-7 recorded
transcript (sha256
f56080d65aeb2ceba9a8134784872381bd17293d8df48010835b482d17d9268d),
exit 0, zero stderr.

- S1: w_fails_total=1 > 0 on all 3 runs. The run reports failure
  on EW (RW "uzvz" predicted "zzzz", expected "vvvv") and does not
  claim success.
- S2: COUNTEREXAMPLE_DETECTED at the W3 reuse probe on all 3 runs
  (1 post-W3 detection line; 2 total including the FW
  presentation). The uncovered second conflict is explicitly
  flagged when probed.
- S3: 0 new DIAGNOSIS/PRIMITIVE-CONSTRUCTED/VERSION lines after
  the W3 marker on all 3 runs. The mechanism does not silently
  re-revise into a wrong stable state.

K-SC-B: PASS. No silent wrong convergence: the failure is loud on
all three conjuncts.

## 9. Cost accounting (machine-greppable, run1 values)

w_first_fit_tw: A2=38 B1=38 B2=38 C2=38 D2=3
w_b1w_enumerated: 1055 (all worlds)
w_revision_evals: A2=6 B1=6 B2=6 C2=11 D2=6
w_fails_total: A2=0 B1=0 B2=0 C2=0 D2=0
w_reuse_correct: A2=1 B1=1 B2=1 C2=1 D2=1
w_reuse_new_revision_lines: 0 (all 15 runs)
w_wall_ms: A2=16 B1=19 B2=8 C2=8 D2=33
binary_bytes: s8_exec_bin=110668 s7_exec_bin=110645
source_delta_lines (harness only): 433
source_delta_lines (validator, certification only): 427
cognition_source_delta: 0
new_semantic_cases: 0
new_modes: 0
new_bridges: 0
new_routers: 0
new_handlers: 0

## 10. Verdict

BUILD-PASS on the narrowed claim.

All frozen bars hold: K-SC-W1/W2/W3 on all five fresh sealed
single-conflict worlds; K-SC-W4 determinism 15/15; K-SC-W5 purity;
K-SC-B bound-trip signal S1+S2+S3 on 3/3 regression runs;
K-ARCH1/K-ARCH2. Cost accounting complete. No precheck voided any
world.

What this establishes (bounded): the frozen revision procedure
revises correctly and cheaply on sealed single-conflict worlds
spanning novel bytes, novel conflict positions, longer inputs, a
novel template shape (repeat-input[1] base with C3 consequent),
and both single-conflict variants of the step-7 family-B regime;
and on the established two-conflict world it flags the uncovered
conflict explicitly (COUNTEREXAMPLE_DETECTED at the held-out
probe, honest failure report, no silent re-revision) rather than
converging silently to a wrong solution.

What this does not establish: representational invention,
template invention, L3 (bounded-L2 ceiling stands); broad
generality beyond the tested regimes; SURVIVES (transfer/reuse
beyond the single probe, second independent red team, and
governance audit remain). The step-5 PASS, step-6 PASS, and step-7
FAIL-with-bounding records are untouched.

## 11. Code-sharing and sealing disclosure

- The harness shares only the frozen machinery (byte-verbatim
  lines 1-606 of proc_revise2.zag); no revision-machinery code was
  altered.
- The frozen baseline discovery code is the only cognitive code
  path exercised; the harness adds staging, checks, and scoring
  only.
- RW was held from the revision machinery until after revision
  completion on every run: the store's observe() was never called
  on RW before the VERSION ACTIVE marker (transcript shows the RW
  STAGE line and RW observation only after "=== W3 REUSE CHECK
  ===").
- The 25 world files were generated and mechanically validated
  during prereg preparation by the lane worker (non-independent);
  hashes were frozen in the prereg before any implementation;
  three design slips were found and fixed pre-freeze and are
  disclosed in the prereg; no world was tuned after seeing
  execution results.
- Executables invoked (K-SC-W5 audit): safebin tools only (bash,
  sha256sum, cmp, diff, grep, sed, awk, stat, date, head, cat, wc,
  znc, chmod, cp, sort, uniq). No python3, python, gcc, cc, perl,
  ruby, or node at any stage.

No em-dashes or en-dashes appear in this file.
