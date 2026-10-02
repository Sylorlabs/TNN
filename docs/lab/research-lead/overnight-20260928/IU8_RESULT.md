# H-INTENT-UNIFIED8 RESULT: B1 rank-hidden verbatim dissenter repair

Status: **SURVIVES 9/9** (bounded L2 integration repair, not L3).
Date: 2026-09-30 UTC.
Toolchain: `znc 2026.07.0-dev (edition 2026)`, binary at
`/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc`.

## Lineage

- Prereg: `PREREG_INTENT_UNIFIED8.md`, committed alone as
  `240493be7` BEFORE any implementation. Prereg commit strictly
  precedes all implementation work in this wave. No Python anywhere.
- Implementation: R10 block inserted identically into
  `unified_learn.zag` and `intent_learn.zag` (50 insertions each,
  0 deletions; only the frozen R10 hunk changed).
- Harness: `iu8_verify.zag` (mechanism region lines 1-1579
  byte-identical to the new `unified_learn.zag`; helpers carried
  verbatim from `iu7_verify.zag` lines 1530-1612; new `iu8_show`
  setup-validity helper; new frozen-bar main).
- Raw evidence: `IU8_VERIFY_RAW.txt`,
  md5 `bd089adddaeb2e4d0cf51fa7c142b1c0`, 3/3 direct binary runs
  byte-identical, exit code 0, zero stderr bytes.
- Supersedes the B1 disclosure of H-INTENT-UNIFIED7: the learnable
  rank-3 and rank-4 configurations are now repaired. The IU7 red-team
  finding itself stands as written; this wave closes the hole it
  named.

## What changed and why

`intent_winner` had guards for: top-two both-verbatim (IU3),
top-two truncated pairs, R8 (all-pairs both-truncated), R9
(all-pairs verbatim-vs-truncated), then `gap==0` tie. The red team
showed a genuine verbatim-vs-verbatim contradiction can hide at rank
3 or 4 behind two agreeing verbatim anchors, because the only
both-verbatim check was top-two-only. R10 adds an all-pairs
both-verbatim guard after R9 and before `gap==0`:

- For every candidate pair with `em==1` on both sides, compute both
  answers and compare all `qlen` bytes.
- On disagreement emit exactly
  `INTENT VERBATIM-CONFLICT: verbatim candidates disagree beyond top two; WITHHOLD AMBIGUOUS`,
  set kind=-2 slot=-1, return.
- Precedence is structural: the top-two guards, R8, and R9 fire
  first with their exact diagnostics; R10 runs only if they did not.
- Pair-class exclusivity holds by construction: R8 checks em=0 on
  both sides, R9 checks em=1 on exactly one side with the em=0 side
  truncated, R10 checks em=1 on both sides. No pair is checked by
  two guards.

## Frozen bars and outcomes

| Bar | Frozen expectation | Observed |
|---|---|---|
| K-IU8-1a (B1 rank-3) | candidates xxx(50000), xxx(40000), bax(40000), all em=1; kind=-2 with ONLY the new R10 diagnostic | PASS. Shows: V1 em=1 ans xxx, V2 em=1 ans xxx, V3 em=1 ans bax. Decision window: one diagnostic line, the new R10 text. |
| K-IU8-1b (B1 rank-4) | answers xxx/xxx/xxx/bax, all em=1; kind=-2 with ONLY the new R10 diagnostic | PASS. Shows: four candidates em=1, answers as frozen. One diagnostic line, the new R10 text. |
| K-IU8-2a top-two both-truncated | kind=-2, exact old text | PASS. `INTENT TRUNCATED-CONFLICT-POSSIBLE: both records truncated with different answers; WITHHOLD AMBIGUOUS` fired 1x. |
| K-IU8-2b top-two verbatim-vs-truncated | kind=-2, exact old text | PASS. `... verbatim candidate meets truncated record with different answer; WITHHOLD AMBIGUOUS` fired 1x. |
| K-IU8-2c R8-only | kind=-2, exact R8 text | PASS. `INTENT TRUNCATED-CONFLICT-POSSIBLE: truncated candidates disagree beyond top two; WITHHOLD AMBIGUOUS` fired 1x. |
| K-IU8-2d in-cap verbatim conflict | kind=-2, exact old top-two verbatim text | PASS. `INTENT VERBATIM-CONFLICT: top two candidates both have exact_match=1 but disagree; WITHHOLD AMBIGUOUS` fired 1x. Shows: PROC em=1 ans bax, BR em=1 ans xxx. |
| K-IU8-3a R9 regression | kind=-2, exact R9 text, R10 must not fire | PASS. `... verbatim candidate meets truncated record with different answer beyond top two; WITHHOLD AMBIGUOUS` fired 1x. New R10 text appears exactly 2x in the whole raw (1a, 1b only). |
| K-IU8-3b 20-char cap | rc=-1, no panic | PASS. |
| K-IU8-3c 129-pair WORK guard | rc=-1 | PASS. |

Result line: `=== H-INTENT-UNIFIED8 RESULT: 9/9 ===` /
`H-INTENT-UNIFIED8 SURVIVES`. No setup failures on any bar.

## Exact-text inventory across the raw (diagnostic fired counts)

- New R10 text: 2 (K-IU8-1a, K-IU8-1b only).
- Top-two both-truncated text: 1. R8 text: 1. R9 text: 1.
- Top-two verbatim-vs-truncated text: 1. Old top-two verbatim text: 1.
- No other diagnostic text appears. R10 never fires where an older
  guard owns the pair class.

## Regression (production mains rebuilt and rerun)

- `unified_learn.zag` main: 20/20, output md5
  `904de9f83a2873c7a8862b71804a9065` (frozen IU7 hash reproduced).
- `intent_learn.zag` main: 10/10, output md5
  `98315faec8faea24e75533892c0b240d` (frozen IU7 hash reproduced).
- R10 did not change any regression-suite behavior.

## Faithfulness invariant

All 10 `fn intent_*` function bodies (proc_base, br_base, init,
record_inputs, record_proc, record_br, exact_match, qscore,
winner, trace_emit) are byte-identical between the two production
sources. The only change in either file is the frozen R10 insertion
(100 insertions total, 0 deletions).

## Failures, boundaries, interpretation

- No bar failed. No setup failure. No panic, no stderr output.
- B2 (em=0 non-truncated disagreement beyond top two) remains a
  disclosed design boundary: an em=0 non-truncated candidate
  supplies no exact recorded contradiction, so withholding on it
  would be speculation, not evidence. R10 does not touch it.
- B3 (POSSIBLE-diagnostic precision cost) is untouched.
- The `gap==0` tie rule is untouched and still last.
- Causal reading: the B1 miss was a coverage gap in guard rank,
  not a scoring or emission bug. The IU3 verbatim guard compared
  only the top two, so any verbatim dissenter ranked third or lower
  was invisible to every verbatim check while the top two agreed.
  R10 closes the rank dimension for the both-verbatim pair class
  without reordering precedence or redefining any older diagnostic.
- Classification: bounded L2 integration repair. The mechanism
  adds no new representation, no new primitive, no learned
  structure; it extends an existing white-box guard family. Not L3.

## Governance disclosures

- The em dash in `// unified_learn.zag ... End-to-end ...` on line 1
  of the production source is pre-existing and predates this wave
  (same disclosure the IU7 red team made). It is carried
  byte-verbatim into `iu8_verify.zag` to keep the mechanism-region
  comparison exact. All code and documentation authored in this wave
  contains zero em dashes.
- Prereg preceded implementation strictly; no bar was weakened or
  redefined after any observation; no Python was used anywhere.
- Commit set for this wave: the two production sources, the
  harness, the raw evidence file, and this report. The prereg was
  committed alone beforehand (`240493be7`).

## Recommended follow-up

Independent red team on H-INTENT-UNIFIED8: adversarial fixtures
targeting R10 (rank-5+ dissenters, mixed bridge/proc verbatim
dissenters, near-tie scores around R10, R10 vs R9 boundary pairs),
plus a precision audit of whether R10 over-withholds on agreeing
answers with different internal slots.
