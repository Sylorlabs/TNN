# BUILD_REFFIRST.md — Engine (b) REF-FIRST build report

## What was built

`reffirst.zag` — pure Zag, zero RNG, pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Command: `znc_linux_x86_64_abed8aa1 reffirst.zag --no-zagd --no-analyze
--no-foreground-cache -o reffirst_bin` (run from the engine dir; the
binary runs with CWD = math_logic dir, same convention as round 1).

Sources in this dir: `reffirst.zag`, `dlb_delib.zag` (byte-identical copy
of the real H5 referee, SHA-256
35393253fe98528ef5fb79fe214109254d5a4a3695cee1a904035d29e96ed122 —
imported verbatim, not reimplemented), `DIRECTIVE_RUBRIC.md` (frozen
referee rules), this file.

Imports: the H5 harness via `../../../../deliberation_depth/harness/`
(R33_NATIVE_SHA256_V2, R33_NATIVE_IO_V1, dlb_util, dlb_json, dlb_cfg,
dlb_ledger), `./dlb_delib.zag`, and the shared derivation core via
`../../../engines/common/cx_fwd.zag` (match-and-bind S_MP/S_UI/S_PBC,
claim store, parser, schemas, guarded IO). `@import` paths resolve
relative to the importing file (AGENTS.md), verified by the build.

## Architecture: referee-driven, inverted from DUAL

DUAL's control flow: D forward-sweeps without a goal, D backward-proves
T and not(T) on two directives, D reports, R deliberates ONCE post-hoc.
REF-FIRST inverts this:

1. The referee owns the hypothesis agenda (H0/H1/H2 + per-hypothesis
   evidence count, status, depth-slice budget, last-selected round).
2. Each round: SELECT (frozen priority rule) -> referee issues a
   DIRECTIVE (goal + depth slice + schema set + premise constraints) ->
   the derivation subroutine executes it (it never runs otherwise) ->
   directive returns claims + audit chains + contradiction flags.
3. New evidence enters the referee's evidence list per the frozen rubric
   (W(d)=1000/(1+d), same as DUAL).
4. The referee scores partial evidence MID-SEARCH with the real H5
   (`R MID-SEARCH: leader=Hx conf=C margin=M` + ledger head, every round).
5. Both sides derivable -> referee WEIGHs (PQ + 200*CORR - 10*DEPTH),
   sustains one or shelves the pair, updates the per-schema trust ledger
   (starts uniform; distrust only from lost weighings).
6. Referee decides: deepen / switch / stop (derived-and-sustained,
   decisive conf=1000, agenda exhausted, round bound 8 / battery param).

The audit distinguishes this from DUAL-renamed: there is no D forward
sweep, no D->R candidate report; every derivation step is labeled
`SUB (derivation subroutine, referee-initiated)` under an `R DIR#k`
issued by the referee, and H5 deliberation runs mid-search, not once at
the end. Withhold is per-hypothesis (a refuted line never poisons the
other line); the only global withhold is H0 winning.

## PBC audit improvement (vs round 1)

`du_prove`'s PBC discharge cited only `ASSUME:not(T) FALSE_DERIVED`,
dropping the subproof's premises from the support chain (PQ scored 0 on
PBC claims). REF-FIRST inlines the subproof and cites the subproof's
store premises in the discharged claim's audit
(`S_PBC_BWD ASSUME:not(T) C1 C5 ... FALSE_DERIVED`), so the weighing
rubric's premise-quality walks the real chain. The subproof step trace
is preserved in the SUB log.

## Standup checks (all pass)

- Determinism: 3x in-process reruns byte-identical asserted (exit 5 on
  divergence); plus 3x external runs byte-identical SHA-256
  (d21757d3... on B2_08).
- Zero RNG: grep clean (no rand/seed/time/clock).
- B2 smoke: 12/12 match DUAL's verdicts (11 DERIVED + B2_07 WITHHELD;
  B2_07's target is genuinely underivable — verified by hand).
- Contradiction probe (premises a, imp(a,t), not(t) |- t): referee
  weighs mid-search (H_T sustains 1340 > 1200 on premise quality +
  corroboration), marks H_N REFUTED-BY-WEIGHING, flags
  CONTRADICTION_DERIVED, trust ledger intact.
- Sealed-solution guard: exit 3 on any path containing "sealed"
  (problem file and store file).
- Committed-schema assertion: exit 6 on hash mismatch (all three
  S_MP/S_UI/S_PBC hashes verified at startup).
- znc pitfalls: no `as []i32/u32/u16` indexed tables (all tables are
  []u8 arenas with au_* accessors); max slice 4MB < 2^25; struct
  literals dot-prefixed; slice-field access only through *T params;
  no chained s.field.subfield; `return;` in void fns.
- Battery bound parameter: argv[3] sets the referee round bound
  (default 8, max 128 for B6X).

## Commit

Sources only (`reffirst.zag`, `dlb_delib.zag`, `DIRECTIVE_RUBRIC.md`,
`BUILD_REFFIRST.md`) committed to
`docs/lab/math_logic/round2/engines/reffirst/` on branch tnn-native-lab
via commit_racefree.py. No binaries, no .zagd cache files.
