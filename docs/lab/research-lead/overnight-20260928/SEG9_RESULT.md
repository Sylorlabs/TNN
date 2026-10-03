# H-SEG9 RESULT: SURVIVES (4/4)

**Date:** 2026-09-29 (PDT)
**Researcher:** H-SEG9 Frontier Researcher (independent subagent)
**Target:** H-SEG8 SURVIVES (4/4). Builder prereg `44cee8122`,
builder result `5923f16af`. H-SEG8 red team SURVIVES all 4 attacks,
result `40038b13f`.
**Verdict:** SURVIVES. All four frozen kill bars PASS.
Classification: bounded L2 structural-learning repair
(observability plus inherited-path closure). Not L3: no
representational invention; the counting remains mechanical.

## Lineage

- Prereg `PREREG_SEG9.md` committed alone as `43482e649` BEFORE
  any implementation edit, build, or run. No amendments.
- `seg9_learn.zag` = `seg8_learn.zag` at `5923f16af` copied
  verbatim (cmp-verified) plus exactly the frozen R9a-R9d edits.
  `seg8_learn.zag` untouched.
- Prereg is a verified strict ancestor of the result commit
  (`git merge-base --is-ancestor 43482e649 <result>`, checked at
  commit time).
- Pure Zag throughout: implementation, fixtures, builds, runs,
  greps, md5, cmp, diff, independent reference. Zero Python at
  any stage. (Shell heredocs/sed/awk used only for file surgery;
  all computation is Zag.)
- Toolchain: `znc 2026.07.0-dev (edition 2026)`. Builds in
  /tmp/sg9 only; no binaries committed.

## Repairs implemented (exactly per frozen prereg)

**R9a: NDINFO diagnostic.** `run_exp` declares `iters` beside
`nd`, increments it once per adaptive-loop iteration, and emits
one `<tag> NDINFO sat=<s> nd=<nd> iters=<it>` line after NOPT,
before VERDICT. Unsaturated path reads `sat=0 nd=0 iters=0`.
DP, accumulation, and print logic untouched (instrumentation
only).

**R9b: sat-boundary sweep.** New fixtures SG9-K02..SG9-K14
(`"ab" x k`, k=2..14, H1 table) between SG9-XL and SENT60.
Pre-prereg scratch verified `T = 2^(k-1)` for the whole range.

**R9c/R9d: renames and header.** `H-SEG8 SEG-LEX-H` to
`H-SEG9 SEG-LEX-I`; `SG8` to `SG9` in tags, banners, and
mechanism comments; header rewritten for SEG-LEX-I.

Diff audit (`diff` frozen SEG8 vs SEG9): 93 changed lines, every
hunk in a preregistered category (header rewrite; NDIGITS
comment rename; `iters` declaration/increment; NDINFO emit
block; adaptive-loop comment rename; label-block comment
rename; main banner; ADD-UNIT renames; BIG/HUGE/XL tag and
comment renames; K-sweep insertion; COMPLETE banner). No
undeclared hunks.

## Frozen kill-bar evidence

Raw: `SEG9_RAW_OUTPUT.txt` (md5
`983d78de98b90aa2eeaebda216c8c9b6`), program output only
(direct binary run, exit 0, zero stderr).

Independent reference (pure Zag, /tmp scratch, never committed):
repeated-doubling big-int with 8 scalar base-1e9 digits (own
doubling routine; no DP, no chunk table, no saturation logic).
Prints 2^(k-1) for k=2..14, one value per line.

- **K-SG9-1 PASS (sat-boundary sweep):** all 13 SG9-K<k> NOPT
  values byte-equal (`cmp`) to the reference lines
  (2,4,...,8192). Zero FAIL lines. NDINFO `sat=0` for k=2..10
  and `sat=1` for k=11..14: the branch flips exactly where
  `T_n` crosses 1000 (512 vs 1024). The inherited H-SEG5
  equivalence `sat[n]==1` iff `T_n >= 1000` now holds measured
  evidence at its sharpest point; a misplaced flip or a
  misprinted count would have killed.
- **K-SG9-2 PASS (measured memory bound):** NDINFO (nd, iters)
  equal the frozen deterministic pairs: SG9-BIG (64,1);
  SG9-HUGE (128,2); SG9-XL (256,3); SG9-K11..K14 (64,1) each.
  General bound `nd <= 2*ceil(D/9)` verified on both doubled
  fixtures with D read off the printed NOPT: HUGE 128 <= 130
  (D=577); XL 256 <= 268 (D=1204). iters=1 fixtures sit on the
  disclosed constant initial budget of 64 (no doubling).
- **K-SG9-3 PASS (regression):** mechanical transform of
  SEG8_RAW_OUTPUT.txt (`SG8`->`SG9`, `H-SEG8`->`H-SEG9`): all
  410 non-banner lines appear byte-identical in the SEG9
  output (0 missing). All 376 extra SEG9 lines are categorized:
  NDINFO lines, SG9-K02..SG9-K14 sections, or the two banner
  lines (0 unexpected). U1/U2/U3 print PASS; zero FAIL lines.
- **K-SG9-4 PASS (determinism):** 3 consecutive full runs
  byte-identical (`cmp`), md5
  `983d78de98b90aa2eeaebda216c8c9b6` x3, exit 0, zero stderr.

Final tally: **4/4. H-SEG9 SURVIVES.**

## What H-SEG9 closed

1. The H-SEG8 red team explicitly left the inherited H-SEG5
   sat/no==999 path unopened. K-SG9-1 re-opens it
   adversarially: 13 exact counts straddling the 1000 boundary,
   byte-checked against an independent computation, with the
   branch bit exposed and asserted. The path holds.
2. The nd_final memory bound was inspection-only ("nd is not
   printed"). R9a prints it; K-SG9-2 asserts the exact
   (nd, iters) pairs and the general doubling bound as measured
   facts.

## Honest limits (per frozen prereg)

1. Count capacity was already unconditional at H-SEG8; H-SEG9
   measures its cost, it does not extend it.
2. The exact-999 case is approached from both sides, not
   constructed exactly.
3. The per-position move-list cap (8) and 5-candidate
   enumeration cap are unchanged; they bound VERDICT/CAND
   output, never NOPT.
4. Counts above 2^19999 remain untested (machine memory bound,
   inherited).
5. All other H-SEG8 honest limits unchanged.

## Governance disclosures

1. Prereg committed alone before any implementation; strict
   ancestry verified at result time.
2. Pure Zag throughout; zero Python at any stage.
3. No binaries committed (builds in /tmp/sg9 only).
4. Only the three owned files staged/committed
   (`seg9_learn.zag`, `SEG9_RAW_OUTPUT.txt`, `SEG9_RESULT.md`)
   via pathspec-restricted adds. No other worker's files
   touched.
5. No em dashes in loop documentation (byte-checked:
   `grep -c` U+2014 = 0 on all authored files).
6. `seg8_learn.zag` and all prior evidence files untouched.
7. Reference implementation (`ref.zag`) kept in /tmp only,
   never committed, by design (independent re-verification
   stays independent).

## Suggested follow-ups for parent

1. Independent red team on H-SEG9 (natural attacks: forge a
   T_n-exactly-999 corpus to test the un-constructed case;
   adversarial iters inflation; NDINFO tamper-evidence).
2. Per the standing mandate the segmentation arc (H-SEG
   through H-SEG9) has now survived three consecutive full red
   teams at its tip and closed every residual the red teams
   named. It remains a candidate for transfer/integration into
   the continuing learner.
