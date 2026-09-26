# RUNLOG — chunking battery fix crew (2026-09-26)

## v0 baseline (frozen promote intake, reproduced in this workdir)

- Wall: 14/26, native=26 fallback=0, SHA-256
  `3cc35d29032cf0e2b367db5006606b28efdd5b3937db7b56c09b16b415541fc2`
  (byte-identical to frozen WALL1.out — harness faithful).
- 57Q: 57/57, SHA-256
  `0a34116398fcd22b313c785c1d1037d712a444f18b3925ce49ac29316a41d268`.

## Stage A (2026-09-26 ~12:30 PDT) — registry instrument + threading + telemetry + ordinal hook

Changes to intake.zag (from frozen v0):
- New knowledge registry: `know:[]u8` arena (2048 B, 3 sections:
  granularity 8x40B, ordinal 16x24B, relation 8x24B), placement primitives
  `tnn_bind_granularity/ordinal/relation`, `tnn_place_knowledge` (KNOW-SEED
  delimited), accessors, `know_init` (explicit zeroing — nio_alloc not
  reliably zeroed).
- `know` threaded through tnn_intake/cand_answer/all 9 candidates/
  classify/parse_pos_n/parse_wordref; `winner:i64` threaded through
  cand_answer/all 9 candidates (15 delegation sites updated).
- Telemetry: every emit now prints `cand_name(winner)` (the policy_winner
  executed path) instead of fork-era `zoom_choose` / hardcoded names.
- Ordinal hook: `parse_ordinal` (-2 digit-start, -1 unparsed, else registry
  value) consulted by `parse_pos_n` and `parse_wordref`; miss falls back to
  legacy `parse_digits` byte-identically.

Harness: battery1/battery2 copies differ from frozen ONLY by
`@import("./intake.zag")`, know alloc+init+placement, and the added `know`
arg at tnn_intake call sites (diffs published in evidence/).

Results:
- Wall: **16/26** (preregistered 16/26). Flips: qid 7 ('t'), qid 8 ('5').
  Reruns byte-identical (SHA `2a570fce…` x2).
- 57Q: **57/57** (preregistered). Reruns byte-identical
  (SHA `170bacd71b…` x2). Zero regression.
- Telemetry audit (`telemetry_audit.py`, faithful port of
  text_shape/policy_winner/cand_name): 26/26 wall lines + 57/57 production
  lines report the executed policy_winner path, 0 mismatches.
  (Audit needed 3 bugfixes during construction: kind-name char class,
  chunk-name `?`, W02 embedded-newline joining — all audit-side, none
  intake-side.)

Process note: first 57Q stage-A run accidentally used the frozen intake
(harness script wrote the battery1 plumbing to run/ instead of
promote_run/); caught because the binary size/SHA matched v0 exactly.
Rebuilt correctly; evidence SHAs above are the true stage-A build.

## Stage B (2026-09-26) — relative addressing + target delimitation + two-hop

**Preregistered targets:** B1 19/26, B2 20/26, B3 21/26, 57/57 production, zero regression.
**Measured:** wall **21/26**, production **57/57**, all preregistered exactly.

Changes in `run/intake.zag` (stage-B transform, script `stageB.py`):
- `rel_probe_pos(q,know,ri,left,right)` — builds the question probe at runtime
  from the registry's relation word; no relation literal in the machinery.
- `first_token(s)` — first whitespace-delimited token.
- `rel_anchor_idx(q,t,know,woffs,wlens)` — resolves " word <rel> <anchor>":
  anchor = single word after the probe, first-occurrence in t, registry signed
  delta applied; -2 (withhold) on absent anchor / out-of-range.
- `parse_wordref2(q,t,wn,know,woffs,wlens)` — relative resolver in front of
  legacy `parse_wordref`; all 27 call sites switched (verified each sits in a
  candidate with t/woffs/wlens in scope).
- `zoom_locate` — first-token fallback when the "of "-tail lookup fails; only
  fires on legacy failure (W17: tail "the in the quick brown the fox" ->
  first token "the" -> 2nd letter 'h'). Static check: no 57Q kind-2/8/9
  question can fire it (every 57Q tail is whole-text or a found single word).
- classify reroutes: "letter <rel> the " -> kind 21 (TWO_HOP); " word <rel> "
  -> kinds 10/11/12/13/14/15/17. Probes built from registry at runtime.
- Candidate 10 `cand_delim` ("DELIM") wired through cand_answer, policy_winner,
  zoom_choose, cand_name, cand_why, coarseness, policy_why.
- kind 21 arm: two-hop "letter <rel> the <ord> letter of <target>"; target =
  first token after "of " (stops at context); inner ordinal from registry;
  relation delta from registry; out-of-range -> '?'.

Per-trap deltas vs stage A:
| trap | stage A | stage B | path |
|---|---|---|---|
| W03 | ? | x | kind=TWO_HOP chunk=DELIM, two-hop fox->2nd letter 'o'->after +1='x' |
| W04 | ? | 3 | kind=LETTER_COUNT_WORD, word after first 'the'='cheese', e-count 3 |
| W05 | ? | b | kind=POSITION_WORD, word before 'fox'='brown', 1st letter 'b' |
| W06 | ehtt... (whole-text reverse) | nworb | kind=REVERSE_WORD, word after 'quick'='brown', word-scoped reverse |
| W17 | ? | h | kind=POSITION chunk=WORD>CHAR, first-token delimitation -> first 'the' -> 'h' |

**Determinism:** wall 2 runs SHA `287b7b41a7dad015b2674bd488c828b79106456683e2247e26d3d574044eebe8`;
production 2 runs SHA `170bacd71ba5f57c79be20786978964bbb094117e452b1a00d5289cbca351a23`
(byte-identical to stage A production output: no 57Q question exercises the new
paths, verified by probe-absence scan — zero behavior change, as required).
**Telemetry audit:** 26/26 wall + 57/57 production, 0 mismatches.
**Remaining misses (5):** W00, W01, W02, W19 (sentence/line granularity — stage C1),
W18 (residual nesting, currently 'w' — stage C2).

Note: a first stageB.py run aborted on an assert (a parse_wordref site inside
cand_char the author list missed); the script writes its output only at the
end, so run/intake.zag was untouched; the assert list was corrected and the
transform re-applied cleanly. No partial state.

## Stage C0 (2026-09-26) — registry rewrite (no-score-change refactor)

**Goal:** resolve the arbitrary-limits violation (hardcoded 8/16/8 per-kind caps,
15-byte word cap in know_cword) before shipping.
**Change:** sectioned fixed-slot registry -> append-log registry
(`registry_new.zag`, `stageC0.py`). Layout: free:u32 @0, then kind-tagged
entries (1=granularity, 2=ordinal, 3=relation); readers scan the log, so
capacity is purely the caller-supplied arena length. Placement API unchanged;
`tnn_place_knowledge` seed block byte-identical.
**Measured:** wall output BYTE-IDENTICAL to stage B
(SHA `287b7b41...`, 21/26). The rewrite is behavior-preserving.

## Stage C1 (2026-09-26) — sentence/line granularity

**Preregistered target:** 25/26, 57/57 production.
**Measured:** wall **25/26** (2 runs SHA `248dedf660fc52cbc088d962efed9c20b59000168d1ec0d864068d5b44670c05`),
only W18 still missing.

Changes (`stageC1_block.zag`, `cand_delim_c1.zag`, `stageC1.py`):
- `gran_named(q,know)` — granularity index from the registry's bound names.
- `gran_split(t,delim,offs,lens)` — delimiter splitter (registry delim byte;
  trims leading spaces, drops empties). Nested if/else flattened (ZNC-013).
- `parse_ord_before_name(q,know,gi)` — ordinal preceding the granule name,
  registry-driven via parse_ordinal.
- classify pre-pass: plural+"how many" -> 18 (GRAN_COUNT); singular ->
  19 (GRAN_SELECT) or 20 (GRAN_WORD, " word of the " present).
- cand_delim arms 18/19/20; policy_why branches; kind_name/policy already
  wired in stage B.
- Static scan: no 57Q question contains "sentence"/"line"; no 57Q double
  "word of".

Per-trap deltas vs stage B:
| trap | stage B | stage C1 | path |
|---|---|---|---|
| W00 | "" | 2 | kind=GRAN_COUNT chunk=DELIM, split on "." -> 2 |
| W01 | "" | the dog ran | kind=GRAN_SELECT chunk=DELIM, 2nd segment |
| W02 | "" | 3 | kind=GRAN_COUNT chunk=DELIM, split on newline -> 3 |
| W19 | "" | cat | kind=GRAN_WORD chunk=DELIM, 2nd word of 1st sentence |

(A first stageC1.py run aborted on a duplicated `if (kind==21) {` assert;
the script writes only at the end so intake.zag was untouched; fixed the
pattern and re-applied cleanly.)

## Stage C2 (2026-09-26) — residual nesting abstention

**Preregistered target:** 26/26, 57/57 production.
**Measured:** wall **26/26** (2 runs SHA `cd86da4355b6e059ea829c63ca41de63e4d7d0a0fea84773d661c1827f1be24b`);
production **57/57** (2 runs SHA `170bacd71ba5f57c79be20786978964bbb094117e452b1a00d5289cbca351a23`,
byte-identical to every stage since A — zero production behavior change).

Changes (`stageC2.py`):
- classify: `count_sub(q," word of ")>=2` -> kind 22 (NESTED). Only W18
  matches (verified: no 57Q question, no other wall question has 2+).
- kind 22 -> policy 10 (DELIM) -> cand_delim arm answers "?" (withhold, never
  guess). Telemetry: kind=NESTED chunk=DELIM why="residual word-of-word
  nesting is not compositionally addressable; withhold, never guess".
- W18: ans="?" exp="?" correct=1.

**Telemetry audit (final):** 26/26 wall + 57/57 production, 0 mismatches.

## Noseed control (2026-09-26) — knowledge-dependence proof

**Method:** `tnn_place_knowledge` with the KNOW-SEED block mechanically emptied
(markers kept); rebuilt both batteries; ran wall + production.
**Measured:** wall **16/26** (vs 26/26 seeded); production **57/57** (unchanged).

Traps that FAIL without the seed (knowledge-driven, 10):
W00/W01/W02/W19 (granularity names -> no binding -> kind 0 -> ""),
W03 (no kind-21 probe -> legacy kind 2 -> first-token "fox" -> confident
wrong "f"), W04 (no relative probe -> legacy "'s in" kind 1 -> whole-text
e-count "6"), W05/W06 (no probe -> legacy kinds), W07/W08 (ordinal words
"second"/"third" unreadable -> digit parse -> 0 -> miss).

Traps that PASS without the seed (structural, survive noseed):
W17 (first-token target delimitation is machinery, not knowledge),
W18 (nesting abstention is machinery), W25 (degenerate guard), all others.

Production 57/57 noseed proves the production battery exercises no
seeded knowledge (digits only, no ordinal words/relations/granularity);
the regression gate is knowledge-independent.
Evidence: `evidence/stageC/W_NS.out`, `evidence/stageC/B_NS.out`.
