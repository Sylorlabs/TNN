# NAMECHECK: cogops_plen_granularity

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, 2026-10-03:

```
export PATH="$HOME/safebin"
which python3; echo "python3-exit=$?"
which python; echo "python-exit=$?"
```

Result: `which python3` and `which python` returned NOTHING
(exit 1). Safebin active for all subsequent commands; PATH
restricted to $HOME/safebin for the whole session.

Pinned znc:
`$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(verified present before use; same pinned binary as the
COGOPS-ADAPTIVEPLEN-RNG lane).

The committed `rng_bin` from 6daff87c5 was executed once from
/tmp (timing probe only, 16 arms in 0.9s) to size the new
experiment; it is not part of this lane's implementation.

## Step 1: Scope

- Follow-up to COGOPS-ADAPTIVEPLEN-RNG (commits d8bf929f9
  prereg, 6daff87c5 implementation+report: verdict INCOMPLETE
  negative; plen=1 vs plen=3 byte-identical in 8/8 matched
  pairs). This lane does NOT modify that lane; it tests the
  report's explicit follow-up proposal: finer replay
  granularity so the plen coefficient can flip selections.
- Base machinery (interpreter, worlds, constructor, P1
  composite fitness, plen_of, matched-RNG driver) adapted from
  `cogops_adaptiveplen_rng/rng.zag` (commit 6daff87c5, cited
  in PREREG.md). Behavioral additions: the three-level replay
  scorer (cell 2402), the counterfactual flip diagnostic
  (cells 2403/2404, reporting only), and the adaptive arm
  (plenmode 4: pmode 3, cell 2370 = 0, plen_adapt live).
  No change to selection, operators, worlds, or adopt bars.
- Research paper untouched.
- Lane:
  docs/lab/research-lead/overnight-20260928/cogops_plen_granularity/
  on branch tnn-native-lab. Non-ledger task (claim minting
  paused). Commits local only, explicit pathspecs, never
  pushed.

## Step 2: Computation

- All research logic in pure Zag, compiled with the pinned
  znc. New Zag code respects the pinned-compiler defect
  workarounds: no `as *i32` slice construction, no
  `_zag_print` for dynamic content (existing emit/e64
  helpers), no >3-deep if-nesting with calls in conditions,
  no `!(A && B)` in while conditions, i32-safe saturating
  abs for the near-miss term (no i64->i32 casts).
- Shell used only for: invoking znc, running binaries, git
  operations, moving/copying files, build.sh guard greps,
  and diff/grep analysis of emitted GEN sequences for the
  report (same analysis role as the RNG lane).
- No forbidden interpreter in verifiers, scorers, harnesses,
  analysis, or scratch. build.sh asserts python3/python do
  not resolve under the safebin PATH.

## Step 3: Naming

- COGOPS-PLEN-GRANULARITY. Kill bars GF1..GF6 (frozen in
  PREREG.md before implementation). Verdict mapping frozen.
- Files: PREREG.md, NAMECHECK.md (this file), gran.zag,
  build.sh, gran_bin, gran_compile.txt, gran_run{1,2,3}.txt,
  gran_err{1,2,3}.txt, gran_sha.txt, build_run.log,
  REPORT.md.
- Replay granularity levels: g=0 quantized (control),
  g=1 medium (25-point), g=2 fine (1-point + near-miss).
  Granularity field in output: `rg=`. (`g=` in GEN lines
  remains the generation index, unchanged from rng.zag.)
