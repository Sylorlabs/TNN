# Preregistration: G0 Diagnostic on the Failing Unified Beam (R3 Arm 2)

Date: 2026-09-30. Worker: G0 Diagnostic Builder.
Status: FROZEN. Committed before any implementation is written.

## 0. Standing rules name-check

- Pure Zag only. No Python at any stage: authoring, building with znc,
  running, verification (shell tools only: sha256sum, md5sum, cmp, grep,
  wc, awk, sort, uniq, git, diff), byte checks
  (worker_snippets/check_no_dash.sh). Zero Python has been invoked from
  task start. No purity disclosure is needed.
- No em/en dash bytes in loop documentation (shell-verified before commit).
- Prereg commit strictly precedes implementation (commit-order self-check).
- Frozen sources are never edited; work happens on a copy under beam_g0/.
- The contaminated research paper is not touched.
- Commits local, owned pathspec only
  (docs/lab/research-lead/overnight-20260928/beam_g0/).
- Other workers' files are not touched.
- If a git lock is encountered, wait; never remove a live lock.

## 1. Design adopted

Section 3 of beam_next/BEAM_NEXT_DESIGN.md (commit 446233dd5,
BEAM-NEXT-DESIGN-COMPLETE), the G0 instrumented diagnostic. This prereg
adopts section 3 verbatim with the operationalizations in section 4
below. No amendment to the design. G1/G2/G3 are not built here.

## 2. Target

- Failing niched beam: the clean unified rebuild r3u.zag
  (beam_unified_clean/, commit fc03664f2, sha256
  be9dba07c642573f518796d7b286e01d9493f8b310a13319455245d48aa07612).
  Per the design ("the unified beam if it fails F-DIVERSE-FAIL"), this
  is the governing failing beam: BEAM-UNIFIED-FAIL fired
  F-DIVERSE-FAIL on R3 Arm 2 (A2-REUSE: hit_iv 24, true 52/64,
  HAS_D=1; bar requires 64/64).
- Diagnostic scope: R3 Arm 2, A2-REUSE driver invocation only
  (fam 8, seed 710202, use_lib 1). The instrumented copy runs the full
  frozen battery (both arms, both reuse/scratch) so the sealed harness
  is unchanged; logging is gated to the A2-REUSE invocation.
- Query signature Q (harness-side only, never in learner code): the
  species signature the true target E = OR(AND(D,Y4), AND(NOT(D),Y5))
  occupies under the U2 definition (tree depth, sorted operator
  multiset). E has operators [n_AND=2, n_OR=1, n_NOT=1, n_XOR=0] and
  depth 3 (OR -> AND -> NOT -> D is 3 edges). So Q = (depth 3,
  h [2,1,1,0]). Q is computed once from the known target in the
  analysis step. The instrumented learner logs signatures generically;
  only the shell post-processing knows Q.

## 3. The question (frozen)

On R3 Arm 2 A2-REUSE with the same seed and sealed harness as the
failing run, are Q-signature candidates:

(a) never proposed by the generator,
(b) proposed but merged away by the species-merge rule, or
(c) proposed but pruned within their species by higher-scoring mates?

## 4. Instrumentation (logging only; zero decision perturbation)

Work on an instrumented COPY r3u_g0.zag of the frozen r3u.zag. The
frozen source is never edited. Changes, all confined to the copy:

- New helpers (generic, no target knowledge): z_cstr, w_open, w_write,
  w_close (raw-syscall file append, same pattern as
  lifetime_race/race_tnn.zag lines 84-106), and a small line-buffer
  appender g0app.
- beam_extend_u gains two trailing params (g0fd:i64, g0inv:i32).
  phase2 gains the same two params and passes them through. phase1
  (dead code, never called by main) gains the params for compilation
  only. main opens the log file once (w_open, truncate), passes the fd
  and the invocation index (A1-REUSE 0, A1-SCRATCH 1, A2-REUSE 2,
  A2-SCRATCH 3) to each phase2 call, and closes the fd at the end.
- Logging is gated on g0inv==2 (A2-REUSE) and g0fd>=0. Three line
  kinds, written to the log file only, never to stdout:
  - C lines, emitted after species assignment and before the merge
    loop, one per candidate k in 0..tn-1:
    "C 2 <round> <k> <depth> <h0> <h1> <h2> <h3> <acc> <opc>"
    using the already-computed cdep, chist, ca, co arrays.
  - M lines, one per merge event, emitted inside the merge loop after
    the cspec relabel and before the skey compaction, capturing the
    absorbed species key skey[s2] (still intact at that point):
    "M 2 <round> <d> <h0> <h1> <h2> <h3>".
  - P lines, emitted after the final beam write, one per candidate k:
    "P 2 <round> <k> <p>" where p=1 if picked[k]>0 else 0.
- F-NOPERTURB (frozen): the instrumented run's stdout must be
  byte-identical (md5) to the committed uninstrumented failing run
  (raw/R3U_RAW_1.txt, md5 6a8568a7232de691606e09712df0f17d). Verified
  with md5sum/cmp BEFORE any log line is read. If the decision
  behavior moved, the diagnostic is void.
- Control first: compile the unmodified r3u.zag with the pinned znc,
  run once, and confirm stdout md5 equals the committed raw md5. If
  the control fails to reproduce, halt and report; do not run the
  instrumented build against a moved baseline.

Log path (frozen): docs/lab/research-lead/overnight-20260928/beam_g0/g0q.log,
written relative to the repo root; the build script cds to the repo
root before running. Run artifacts: G0Q_RAW_1/2/3.txt (stdout),
G0Q_RAW_1/2/3.err (stderr, must be empty).

## 5. Analysis (shell only; zero Python)

Shell tools only (grep, awk, sort, uniq, wc). Steps:

1. From the log, take C lines with depth=3, h0=2, h1=1, h2=1, h3=0.
   PROPOSED_Q = their count across all 25 rounds (round 0..24).
2. From M lines, build the per-round set of absorbed signatures.
3. For each Q candidate (round r, index k): merged iff its
   (depth,h0..h3) is in round r's absorbed set. MERGED_Q = count.
4. Join with P lines on (round, k): retained iff p=1.
   RETAINED_Q = count of merged-or-not Q candidates with p=1.
   PRUNED_Q = Q candidates not merged and p=0.
5. Report the four numbers plus per-round tabulation.

## 6. Decision rule (frozen, from the design)

- (a) iff PROPOSED_Q == 0. The generator never proposes E-shaped
  candidates. Cause 1 confirmed in its strongest form.
  Verdict: G0-NEVER-PROPOSED.
- (b) dominant iff PROPOSED_Q > 0 and MERGED_Q > 0 and
  RETAINED_Q == 0. Cause 2 confirmed.
  Verdict: G0-MERGED.
- (c) dominant iff PROPOSED_Q > 0 and PRUNED_Q > 0 and
  RETAINED_Q == 0. Cause 3 confirmed (retention ranking implicated).
  Verdict: G0-PRUNED.
- Mixed: PROPOSED_Q > 0, RETAINED_Q == 0, both MERGED_Q > 0 and
  PRUNED_Q > 0. Report the raw numbers; verdict names the branch
  with the larger count as dominant, disclosed as mixed.
- F-G0-INCONCLUSIVE (design-killing, reported honestly):
  PROPOSED_Q > 0 and RETAINED_Q > 0 while Arm 2 still fails. Then the
  generation-gap premise is wrong: E-shaped candidates were proposed
  AND survived, and the true E still was not found. Sections 4-5 of
  the design do not apply.

## 7. Kill bars (this diagnostic task)

- K1 (prereg frozen before implementation): this document committed
  strictly before any diagnostic source is written. Commit-order
  self-check required.
- K2 (diagnostic runs): control reproduces the committed raw; the
  instrumented build runs 3x; F-NOPERTURB verified before any log is
  read; the trichotomy is resolved (or F-G0-INCONCLUSIVE fires).
- K3 (pure Zag, deterministic): Zag at every stage; shell tools only
  for verification. Zero Python at every stage, from task start.
  3/3 byte-identical instrumented stdout runs, zero stderr bytes.
  Zero em/en dash bytes in loop documentation (shell-verified).

## 8. Verdict rule (frozen)

- G0-NEVER-PROPOSED iff branch (a) resolves per section 6.
- G0-MERGED iff branch (b) resolves per section 6.
- G0-PRUNED iff branch (c) resolves per section 6.
- F-G0-INCONCLUSIVE iff the design-killing condition in section 6
  holds; reported honestly with the raw numbers.
- Any other outcome (control fails, F-NOPERTURB fails, K3 fails) is
  G0-VOID with the failure named, not a trichotomy verdict.

## 9. Governance

- Prereg-first; no implementation before this commit.
- Frozen base sources are never edited; work happens on a copy in
  beam_g0/.
- The contaminated research paper is not touched.
- Commits local, owned pathspec only
  (docs/lab/research-lead/overnight-20260928/beam_g0/).
- Other workers' files are not touched.
- If a git lock is encountered, wait; never remove a live lock.

## 10. Honest scope (frozen)

G0 is a diagnostic. Its output is data, not a mechanism. No L3 claim,
no Criterion 0 claim, no Q4 revival. A trichotomy verdict selects
which conditional branch (G1/G2/G3) a future builder may preregister;
it does not itself repair anything. Bounded-L2 diagnostic only.
