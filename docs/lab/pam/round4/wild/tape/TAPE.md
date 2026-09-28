# ROUND-4 WILD TRACK — FROZEN SHARED ADMISSION TAPE

**Date:** 2026-09-24. **Author:** WILD-B crew (W4/W5/W7/W10/W11/W12/W13/W15).
**Status:** FROZEN — committed before any round-4 wild fixture, build, or run.
Shared verbatim by WILD-A (W1/W2/W3/W6/W8/W9) and WILD-B. Any extension
(attack fixtures) lands as a committed addendum in this directory; the
admission tape below is never modified.

## 1. Canonical admission tape

| Item | Value |
|---|---|
| File (repo path) | `docs/lab/pam/round3/m1/m1_cases.txt` |
| Local path | `~/workspace/tnn-lab/pam/round3/m1/m1_cases.txt` |
| sha256 | `5d4160d1e1a06c8250376bc85367981722fe0002296ae168c581c8353322c611` |
| Rows | 2241: `C`=1102, `W`=12, `P`=18, `B`=1109 |

Line format (frozen, from `PREREG_M1_BAR.md` §10):
- `C|conf|mrgF|strong|agree` — 1,102 correct trials (`judgment==truth`, `conf>=700`).
  The RK-3 denominator. Correct-admit rates are computed over these 1,102.
- `W|conf|mrgF|1|1` — 12 sustained TMB-5 cross-span wrongs (seq 24–35 of the
  frozen D1 `rec_install.records`). `strong`/`agree` = 1 by the frozen
  worst-case convention (record format carries none).
- `P|pairid|conf|mrgF|1|1` — 18 rows = 9 CC1 wrong pairs (`CC1`, `CC1-V1`…`CC1-V8`;
  wrong members = trials idx 2,3 of each cell, `jcode=2 ≠ truth=3`).
  A pair "installs"/"passes" only if BOTH members pass.
- `B|conf|mrgF|strong|agree` — 1,109 diagnostic broad wrongs
  (`judgment!=truth`, `conf>=700`). NEVER constrains a search or a kill bar;
  reported as a safety diagnostic only.

## 2. Frozen sources (all verified on this VM, 2026-09-24)

| # | Source | sha256 (verified) |
|---|---|---|
| D/B | `~/workspace/pam_round2/o1_delivery/sweep.jsonl` (11,840 rows) | `4163fffa65f18f552d48f7efec0e9800a7406547a27c6259d39a48ec7f0833f2` |
| W | `~/workspace/pam_round2/d1_stack/rec_install.records` | `c26ac9743b8c079e782cdf8511caf2350f653556ac11ac70dfda03720c17c4ad` |
| P | `~/workspace/pam_round2/cc1_guard/prereg/gen_guard.py` | `49eef7b169790207dd53b140a3586144fe34a8b99a134e18d2244702ae2c214b` |

Extraction integrity: the frozen Round-3 extractor
(`pam/round3/m1/gen_m1.py`, committed) was re-run on this VM into scratch;
its output is byte-identical to the canonical tape
(sha256 `5d4160d1…c611`, `cmp` clean, counts 1102/12/18/1109 confirmed).
Nothing in this tape was transcribed by hand.

## 3. Usage rules (both tracks, verbatim)

1. Every design reads the tape from the canonical repo path above; the
   sha256 is asserted by each battery's scorer before any metric is computed.
2. K1 (program prereg §4) applies to the frozen wrong set: the 12 `W` rows
   and the 9 `P` pairs (pair = both members). Per-design preregs may
   reinterpret "admit" for non-binary paradigms (W8-provisional,
   W13-lease, W15-tier, W12-defer) but must state the mapping explicitly;
   they may not weaken K1.
3. K3's baseline is the C3-repair RK-3′ = 71.78% over the 1,102 `C` rows.
4. `B` rows never trigger a kill bar; they are reported as diagnostics.
5. No design may filter, reorder (except a preregistered deterministic order
   stated before the run), or subsample the tape without recording the rule
   in its prereg.

## 4. Attack-tape extensions (addenda, committed before use)

The program prereg (§3 M-attack, debate notes) requires attack fixtures:
provenance-laundering (GEN→EXT relabel), forged declarations (Declaration
Fork), forged authority. No frozen fixtures for these exist in the round-2
sources on this VM, so each track builds its own deterministically-generated,
committed addenda:

- `TAPE_W7_ADDENDUM.md` (WILD-B): frozen laundering fixture set —
  generator-authored entries relabeled EXT mixed with genuinely external
  entries, content/behavioral signals, label-blind instrument.
  (Committed after PREREG_W7, before the W7 build.)
- Further addenda (W10 duel bundles, W11 chains, W12 streams, W13 leases,
  W15 tiers) are per-design fixtures documented in their preregs; each is
  committed before its design's build.

## 5. Provenance of this document

Written 2026-09-24 by the WILD-B crew after verifying all three frozen
sources and the byte-identical re-extraction. WILD-A had not written to
`round4/wild/` at the time of writing; this file is the coordination point —
WILD-A must use it verbatim and flag any discrepancy before running.
