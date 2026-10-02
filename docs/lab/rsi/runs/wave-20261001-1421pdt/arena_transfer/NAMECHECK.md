# NAMECHECK.md: arena_transfer lane worker (TRANSFER / REUSE)
Wave: wave-20261001-1421pdt. Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.

## Step 0: Toolchain guard (MANDATORY)
- Ran `bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
- Exported PATH="$HOME/safebin" (36 tools; znc pinned OK)
- `which python3` prints nothing (exit 1). `which python` also nothing.
- PURE ZAG ONLY for this lane: all programs written and run will be Zag compiled with the pinned znc. No Python, no other interpreters, anywhere (no glue, analysis, verifiers, harnesses).
- No git commit/push/checkout/branch changes; all files stay uncommitted.
- Documentation rule: no em-dashes in docs I write (colons or parentheses only).

## Step 1: Locate arena records
- Baseline arena design (15 capabilities):
  docs/lab/research-lead/overnight-20260928/baseline_arena/BASELINE_ARENA_DESIGN.md.
  Transfer = C6 "Procedure invention and cross-domain transfer", scoring
  S = 1 - (transfer_examples / fresh_examples), clipped to [0, 1].
- Competitive arena (16 capabilities, sealed):
  docs/lab/research-lead/overnight-20260928/competitive_arena/ (ARENA_PREREG.md,
  tnn_contestant.zag, arena.zag, world_gen.zag). Transfer = C12 there.
- Prior state (parent-provided): actual contestant 0.676 (v4, 7/7 kill bars);
  clean canonical 0.573; transfer currently zero. The literal "0.676" string
  was not found in the wave docs searched; cited as parent-provided prior.
- No runnable frozen TNN-2 binary was available to this lane, so the sealed
  evaluation is a protocol-level probe with a minimal simulated learner
  (evaluator-only, TNN source untouched). Any positive is CANDIDATE pending
  the refreeze protocol; it does not move the canonical 0.573.

## Step 2: Frozen prereg (writing-only first)
- Wrote PREREG_TRANSFER.md BEFORE any implementation. Frozen kill bars
  K1..K8 with numeric thresholds, determinism bar, anti-memorization bar,
  pure-Zag bar, architecture accounting, honest boundaries.

## Step 3: Implementation and sealed runs
- transfer_eval.zag: one pure-Zag binary. LEARN on world A (arithmetic,
  digit surface), TRANSFER on world B (geometric, letter-code surface),
  plus ABLATED (S_A wiped) and STORAGE (verbatim lookup) controls.
- Built with pinned znc, exit 0, zero analyzer warnings.
- Ran 3x: run1.txt run2.txt run3.txt byte-identical (cmp), sha256
  4344e9ddd4d98e33d9f830df6a253a4b1872a73795bc6f68db6cba6edbb9e3e0.
- Results: T_B=4, F_B=6, X_B=6, M_B=24, S_A order=[DIFF,RATIO,COPY,MEAN],
  score_x10000=3333 (S=0.3333). K1..K3,K5,K6 PASS; K4 PASS (3x cmp);
  K7 PASS (no python anywhere, which python3 empty, 0 .py files);
  K8 PASS by construction. VERDICT=CANDIDATE.
- No git commit/push/checkout/branch change. No tracked files modified
  (git status shows only pre-existing untracked files plus this new lane
  dir). TNN source untouched: 0 new modes/bridges/routers/handlers,
  0 new hardcoded semantic cases.
