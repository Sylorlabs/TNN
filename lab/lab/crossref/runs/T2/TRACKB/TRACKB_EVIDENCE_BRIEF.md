# TRACKB Discriminating Evidence Brief — WAVE-2 CROSSREF

**Status:** Evidence only. No verdict, ranking, weighting, or recommendation.
**Prereg:** `TRACKB_DISCRIM_PREREG.md` (commit `7a0d6722b7590f4d113cfcd9591dfa1ad679cbc0`, 2026-09-23).
**Method note:** All mechanisms, learners, and verification are pure Zag.
Python was used only as glue (process orchestration, byte-shuffling, tabulation).
Zero RNG in any decision path. Every scored leg ran 3× byte-identically.
A background Python-policy pilot was run first and is **diagnostic only**;
all numbers below come from the prereg-faithful battery unless marked otherwise.

**Variant pins (frozen):**
- varA `7d056be` · teacher blob `a888c52b5ca5…` (57,281 B)
- varB `d7929bb` · blob `63a96728557e…` (32,082 B)
- varC `f0031d9` · blob `fe353381e760…` (42,726 B)

**Reproducibility gap (evidence quality):** varB and varC import
`../../harness/substrate/R33_NATIVE_IO_V1.zag`, a path absent at their pins
and at the current branch head. All varB/varC runs in this battery used a
scratch copy byte-identical (SHA-256 `e6379ddb…f61d8`) to varA's committed
runtime. This is reported, not repaired in-repo.

---

## D1 — Adversarial decision regimes (determinism + proposal geometry)

All legs 3× byte-identical. `conv` = fixed-point convergence within 5 rounds
(varA only; varB/varC are turn-sequential).

| Variant | Regime | n | Kind histogram | Conf range | Terminal | Conv |
|---|---|---:|---|---|---|---|
| A | adopt_all | 160 | 1:98, 2:31, 3:31 | 120–172 | clean_end | yes |
| A | r1storm | 160 | 1:160 | 108–172 | clean_end | yes |
| A | r34storm | 160 | 1:160 | 148–172 | clean_end | yes |
| A | revise_spam | 160 | 1:1, 4:159 | 120–148 | clean_end | **no** |
| A | mixed | 160 | 1:34, 3:7, 4:119 | 90–172 | clean_end | **no** |
| B | adopt_all | 211 | 1:8, 2:29, 3:87, 4:87 | 145–164 | empty_batch | n/a |
| B | r1storm | 120 | 1:120 | 136–180 | empty_batch | n/a |
| B | r34storm | 79 | 1:79 | 136–168 | empty_batch | n/a |
| B | revise_spam | 240 | 1:240 | 136–168 | empty_batch | n/a |
| B | mixed | 237 | 1:216, 2:3, 3:9, 4:9 | 136–176 | empty_batch | n/a |
| C | adopt_all | 64 | 1:7, 2:1, 3:19, 4:37 | 60–203 | turn_cap | n/a |
| C | r1storm | 64 | 1:64 | 60 | turn_cap | n/a |
| C | r34storm | 64 | 1:64 | 60 | turn_cap | n/a |
| C | revise_spam | 64 | 1:64 | 60–220 | turn_cap | n/a |
| C | mixed | 64 | 1:64 | 60–98 | turn_cap | n/a |

Readings (no verdict):
- varA emits a **SAME_AS (kind 4)** re-proposal for essentially every REVISE
  (159/160 under revise_spam; 119/160 under mixed). Its revision machinery is
  the most structurally visible.
- varA's fixed point **does not converge** under revise_spam, mixed, or the
  frozen GT student (tested to 15 rounds): rejects dead-mark spans, which
  shifts every subsequent proposal. Adopt/reject-only regimes converge in ≤2.
- varB's proposal **count** is regime-sensitive (79–240); its kind mix collapses
  to all-WORD_SPAN under reject/revise pressure.
- varC emits a **fixed 64 proposals** in every regime (turn cap), but its kind
  mix and confidence range move (conf 60–220 under revise_spam vs flat 60
  under reject storms).

## D2 — Curriculum shift

- **Mid-stream swap without history reset (preregistered):**
  - varB: 10 turns on X, swap bytes, 20 turns on Y. Post-shift: 140 proposals,
    **42.9%** match Y's GT spans; first Y-match at post-turn 0.
  - varC: 10 turns on X, swap slice, 20 turns on Y. Post-shift: 20 proposals,
    **95.0%** match Y's GT spans; first Y-match at post-turn 1.
  - varA: session-locked by design — cannot swap mid-session. D2 for varA is a
    new session on Y with the same decision pattern (see shifted-curriculum
    legs below). This architectural difference is evidence, not a defect.
- **Shifted curriculum, fresh session (supplementary):** all three produce
  proposal streams on Y statistically indistinguishable in shape from X
  (A: 160, kinds 1:105/2:26/3:29; B: 211, kinds 1:8/2:29/3:87/4:87;
  C: 64, kinds 1:11/2:2/3:17/4:34).

## D3 — Edge stimuli (graceful vs cliff)

| Stimulus | A | B | C |
|---|---|---|---|
| single word | 1 prop, clean | 1 prop, clean | 64 props, clean |
| all-spaces | 0 props, clean | 0 props, clean | **CLIFF rc=13** |
| 1-byte | 0 props, clean | 0 props, clean | **CLIFF rc=13** |
| no-vocab slice (C only) | — | — | 64 props, all kind-1, clean |
| 1 MB stimulus (B only) | — | 211 props (same as 2.7KB), clean | — |

varC hits its integrity tripwire (rc=13) on degenerate inputs; varA/varB
degrade to zero proposals with clean exits. varC emits its fixed 64
kind-1 proposals even with zero vocabulary matches; varB's proposal count
is identical (211) on 1 MB vs 2.7 KB stimuli.

## D4 — Adversarial history/evidence

| Test | A | B | C |
|---|---|---|---|
| 20-DEFER storm | 160 props, clean, conv | 214 props, clean | 64 props, turn_cap |
| contradictory (ADOPT then REJECT R2, same span) | 0 contra pairs (spans never re-occur; dead-marked) | **87 contra pairs** executed | **19 contra pairs** executed |
| forged-but-well-formed history | n/a (script is history; seq mismatch → rc=13) | **trusted**: continued seq 106–112, 7 props, rc=0 | **rejected**: rc=4 "history: replay rejected" |
| truncated final record | n/a | rc=12 "bad history size" | rc=10 "history: bad size" |

varC validates history provenance (replay rejected); varB trusts
well-formed forgeries; varA's script model makes forgery a seq-integrity
error. All three fail cleanly (exact codes) on truncation.

## D5 — Raw measures (unweighted; frozen prereg has no §7 weights for TRACKB)

Frozen GT student (ADOPT on exact match; REVISE iff IoU≥0.5; else REJECT R1,
escalating to R5 after two rejects of the same span):

| Measure | A | B | C |
|---|---|---|---|
| mastery (% GT adopted) | 15.5% (75/484) | 19.6% (95/484) | 0.1% (11/11518) |
| revisability (revise→adopt within 2) | 1.3% exact / 20.9% IoU≥0.5 / **99.4% kind-4 re-proposal** | 0.8% exact / **51.7% IoU≥0.5** / 0% kind-4 | **0% / 0% / 0%** (revision-deaf) |
| integrity violations | 0 | 0 | 0 |
| retention (adopted never contradicted) | 1.0 | 1.0 | 1.0 |
| cost (proposals/adopted; wall s) | 1.57; 8.4s | 1.16; 5.4s | 1.03; 13.5s |

Notes:
- The GT student issued **zero REVISE decisions** on this curriculum (no
  IoU≥0.5 near-miss without exact match), so revisability is measured under a
  revise-then-adopt student instead (reported above).
- Revisability discriminates sharply: varA re-proposes via SAME_AS (kind 4)
  on 99.4% of REVISEs but rarely lands the exact requested span (1.3%);
  varB re-proposes near the target (51.7% IoU≥0.5) without a SAME_AS kind;
  varC ignores REVISE entirely (0% on all three).
- varC's GT denominator (11,518) is per-slice-byte spans; its 11 adopted spans
  are coarse. The mastery % is not cross-comparable without normalization —
  reported raw per the no-weighting rule.
- varA/GT does not converge (see D1); measures are from the final round.

## D7 — Persistence / re-derivation

Fresh workdirs, retained artifacts only: all three variants re-derived the D5
GT legs byte-identically (A `1207b4ca…`, B `e84a9b92…`, C `bbc23f29…` — MATCH).

## D8 — Negative control (varD, ineligible for selection)

Pure-Zag teacher emitting valid frozen §P v1 (teacher_id=3), deterministic
from stimulus only; history path never opened.
- Different histories → **byte-identical stdout** (SHA-256
  `cfb33c30…4c4665fd`): zero history sensitivity. **Kill bar PASSED.**
- Output passes the §P iron-rule validator (5 proposals, kind=1, conf=128).
- Different stimulus → different output (stimulus-sensitive, not constant).

## Surprises / limits

1. varB/varC's missing runtime import (see header) — the battery's varB/varC
   evidence rests on a scratch runtime copy, byte-identical to varA's.
2. varA has no decision fixed point under any revise-containing student.
3. varC's rc=13 integrity tripwire fires on degenerate stimuli (all-spaces,
   1-byte) — graceful for A/B, cliff for C.
4. varB trusts forged history; varC rejects it. This is the sharpest
   integrity discrimination in the battery.
5. The frozen GT student never revises on this curriculum; revisability had to
   be measured under a different student (disclosed above).
6. D2's preregistered mid-stream swap is impossible for varA by design;
   reported as an architectural difference with the fresh-session equivalent.
7. No §7 champion weights exist for TRACKB; all measures are raw and unweighted.
   **No measurable-difference claim is made where the battery found none;
   no arm is named, ranked, or recommended.**

## Artifact SHAs (full SHA-256 of canonical proposal streams)

See `sha_manifest.json` (31 entries). All legs ran 3× byte-identically;
rep0 SHAs are representative. D8 varD output:
`cfb33c30082915641d70263568e52390b0d8de13b0257e51facf586b4c4665fd`.
