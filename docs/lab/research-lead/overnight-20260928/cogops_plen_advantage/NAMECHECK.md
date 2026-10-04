# NAMECHECK: cogops_plen_advantage

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
COGOPS-PLEN-GRANULARITY lane).

Isolated worktree `~/workspace/tnn-rsi-plenadv` (detached at
tnn-native-lab) used for this lane to avoid touching other
workers' checkouts. Commits assembled via git plumbing onto
the tnn-native-lab tip with explicit pathspecs; local only,
never pushed.

## Step 1: Scope

- Follow-up to COGOPS-PLEN-GRANULARITY (verdict INCOMPLETE,
  negative on bars, with the sign-reversal correction:
  PADAPT 0->1 costs <= plen=3 in 24/24 matched arms,
  strictly less in 3 pairs; sign test p=0.125). This lane
  does NOT modify that lane; it tests the reversed
  hypothesis (adaptive/lower plen is BENEFICIAL) on 8 fresh
  pair seeds plus the original 8, with a new fixed-plen-0
  arm (P0) to discriminate level from adaptivity.
- Base machinery (interpreter, worlds, constructor, revise
  driver, scorers, matched-RNG protocol) ported from
  `cogops_plen_granularity/gran.zag` (tnn-native-lab,
  sha256
  8b5cd1da7c761543ce51cbc8a5f4bd4b3560fde95f54646f1778a41bca8a2740).
  Behavioral additions: the plen_hold cell 2405 (new P0
  arm only), fresh-seed branch in the pair-seed functions,
  widened inversion-diagnostic gate (pmode>0, reporting
  only), QUALITY emit line, FLIP gains inv=.
- Research paper untouched.
- Lane:
  docs/lab/research-lead/overnight-20260928/cogops_plen_advantage/
  on branch tnn-native-lab. Non-ledger task (claim minting
  paused). Commits local only, explicit pathspecs, never
  pushed.

## Step 2: Computation

- All research logic in pure Zag, compiled with the pinned
  znc. New Zag code respects the pinned-compiler defect
  workarounds: no `as *i32` slice construction, no
  `_zag_print` for dynamic content (existing emit/e64
  helpers), no >3-deep if-nesting with calls in conditions,
  no `!(A && B)` in while conditions, no `_MODE` token.
- Shell used only for: invoking znc, running binaries, git
  operations, moving/copying files, build.sh guard greps,
  and awk/diff analysis of emitted lines for the report
  (same analysis role as the parent lanes).
- No forbidden interpreter in verifiers, scorers, harnesses,
  analysis, or scratch. build.sh asserts python3/python do
  not resolve under the safebin PATH.

## Step 3: Naming

- COGOPS-PLEN-ADVANTAGE. Kill bars AH1..AH8 (frozen in
  PREREG.md before implementation). Verdict mapping frozen.
- Files: PREREG.md, NAMECHECK.md (this file), adv.zag,
  build.sh, analysis.sh, adv_bin, adv_run{1,2,3}.txt,
  adv_err{1,2,3}.txt, adv_sha.txt, build_run.log,
  REPORT.md.
- Arms: P0 (plenmode 5: fixed plen 0, hold), PA (plenmode 4:
  adaptive 0->1), P1 (plenmode 1: fixed plen 1),
  P3 (plenmode 3: fixed plen 3).
- Pairs: k2 0..7 original seeds, 8..15 fresh seeds.
  Granularities: rg=0 (quantized), rg=2 (fine).
