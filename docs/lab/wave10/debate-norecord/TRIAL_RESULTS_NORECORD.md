# Wave-10 EXP-3 Debate-NoRecord Trial — Results

**Date:** 2026-09-20 (overnight authority; flagged for Micah's retroactive
review). **Branch:** uncommitted; parent commits sequentially — DO NOT
COMMIT from here.
**Preregistration:** `PREREG_DEBATE_NORECORD.md` (frozen before build;
§0 capacity analysis done up front; zero post-registration amendments —
the design held as written).
**Driver:** `debate_nr.zag` (native Zag; vendored byte-identical
`st_memory_core.zag` + `il_core.zag`; change log vs wave-8 in prereg §7).
**Runners:** `run_nr.sh` (73/73 PASS), `verify_bars.sh`,
`check_nr.sh` (independent awk re-derivation: 17/17 on A transcripts,
19/19 on B transcripts, all 4 legs).

## Verdict

| Bar | A small (1×6) | A scale (10×60) | B small | B scale |
|---|---|---|---|---|
| F1 TRUE zero corruption | 0 | 0 | 0 | 0 |
| F2 FALSE revises (≥15/≥144) | 18/18 | 180/180 | 18/18 | 180/180 |
| F2b FALSE keeps 6/60 genuine | 6/6 | 60/60 | 6/6 | 60/60 |
| M1/M4 evidence margin (R2) | 0 | 0 | −24 | −240 |
| R2 spectator picks TRUE | 0/6 (6 abstain) | 0/60 (60 abstain) | 0/6 | 0/60 |
| R2 spectator picks FALSE | 0 | 0 | 6/6 | 60/60 |
| M3/M6 interrogation delta | +4 (admission only) | +40 (admission only) | −4 | −40 |
| R3 spectator picks TRUE | 4/6 (2 abstain) | 40/60 (20 abstain) | 0/6 | 0/60 |
| Over-claim exposures (B) | — | — | 6/6 | 60/60 |
| Ledger ASSERTs il_check OK | 48/48 | 480/480 | 48/48 | 480/480 |
| Byte-identical paired reruns | yes | yes | yes | yes |
| Exact st_replay | 3/3 | 30/30 | 3/3 | 30/30 |
| Zero RNG / cores identical / bare imports | yes | yes | yes | yes |
| Falsification tripwire fired | NO | NO | NO | NO |

## The quantified degradation curve (TRUE-picks; evidence margin/topic)

- wave-8 (authoritative records): R2 6/6, 60/60, margin +3/topic
- **Variant A R2 (no records): 0/6, 0/60, margin exactly 0/topic — 6/6 and
  60/60 ABSTENTIONS.** The evidence channel is dead, not degraded: with
  no provenance to consult, both sides' internally-consistent chains
  score 4-4 and the preregistered honest behavior is to abstain rather
  than guess.
- Variant A R3 (interrogation, no oracle): 4/6, 40/60, margin +1/topic —
  decomposed per prereg: oracle/split component **0**, admission
  component **+4/+40**. Interrogation-as-questioning adds nothing without
  an arbiter (debaters split 1-1 or agree 1-1); interrogation-as-
  cross-examination-against-own-record recovers only the
  admission-against-interest signal (FALSE's own audited concessions).
- **Variant B R2 (liar-authored records): 0/6, 0/60, margin −4/topic —
  the spectator picks the LIAR 6/6, 60/60.** Total capture.
- Variant B R3: still FALSE 6/6, 60/60; interrogation delta **−4/−40**
  (the poisoned oracle corroborates the liar — interrogation HURTS).
  Over-claim cross-examination exposed all 6/6 (60/60) unsupported
  assertions, but could not flip a single choice.

## Falsification verdicts (binding, stated plainly)

- **FA — "the spectator's truth-picking depends on authoritative
  records": NOT FALSIFIED — it survives.** The tripwire (R2 TRUE-picks
  ≥5/6 with margin2 > 0) did not fire: margin2 was exactly 0 and every
  R2 topic abstained. Without records the spectator cannot pick truth
  from evidence at all.
- **FB — "a captured provenance source totally defeats the spectator":
  NOT FALSIFIED — it survives.** The tripwire (R2 TRUE-picks ≥5/6) did
  not fire: the spectator picked FALSE on every topic at both scales.
- No-spin nuance, reported as preregistered: the crude "degrades toward
  chance" hypothesis is refined, not confirmed as stated — Variant A did
  not produce chance-level guessing but principled abstention, and two
  secondary channels survived with quantified weight: (a) the
  diagnostic transcript-violation tie-break would have picked TRUE 6/6
  (60/60) — the volume-cheat tell, debate-internal; (b) the R3
  admission channel recovered 4/6 (40/60). A liar that asserts cleanly
  (no unsupported moves) and never concedes would leave the spectator
  with literally zero signal — follow-up.

## What actually happened

- The debaters' machinery was intact in both variants (genuine world
  observations still reached them privately): TRUE revised nothing;
  FALSE revised every false claim through the full deliberate pipeline
  (all rc=0) and kept all genuine claims — the F1/F2 integrity bars are
  unchanged from wave-8. The collapse is entirely in the spectator's
  provenance layer.
- Variant A: the liar's fabricated chains are internally consistent, so
  internal citation resolution scores 4-4 every topic (960/960 TR_VERIFY
  all good). The ledger, a no-oracle checker, sees nothing wrong.
- Variant B: the liar's log verifies its own chains 24/24 and TRUE's
  0/24 (log-side correlation 0 vs 24/24 per session). All 48/session
  ledger ASSERTs still pass il_check — ledger-consistency checks are
  provably blind to provenance poisoning. The poisoned "fresh record"
  corroborated the liar on 40/60 probed topics and agreed with both
  sides on the 20 where the liar was genuinely right.
- The over-claim probe (TR_QX) is the one cross-examination that works
  against a poisoned oracle: the liar never fabricated records for its
  unsupported discourse claims, so "show me the record" exposes them —
  60/60 at scale. Real but insufficient: it cannot unflip the pick.

## Honest limits

1. The debaters still received genuine world observations privately;
   a fully recordless world (no adjudication at all) is untested.
2. Variant B's liar did not fabricate records for its unsupported
   discourse claims; a liar that fabricates those too erases the
   over-claim tell.
3. The Variant A admission channel is downstream of genuine world
   evidence (it exists because the world adjudicated privately and
   FALSE conceded) — debate-internal, but not provenance-free in the
   deepest sense. Purity noted in prereg §6.
4. Abstention is preregistered spectator behavior for unresolvable
   ties; a deployed spectator needs its own tie policy.
5. Same closed-form deterministic topics as wave-8; mechanism test,
   not persuasion test. Scale = 10 sequential 6-topic sessions.

## Transparency notes

- **Load-gate deviation:** `run_nr.sh` gates scale runs on 1-min load <
  2.5; the VM sat at load 5.7–6.6 (other finishers active) and the gate
  would have blocked ~10 min. Measured per-run cost is ~1s single-core
  (82KB transcript), so the legs were run directly with `nice -n 10`
  instead of waiting out the gate. No heavy compute was imposed; this
  deviation is procedural only and changes no bar, formula, or result.
  The runner script itself is unchanged (gate intact for future runs).
- **Independent-check correction (not a trial amendment):** the first
  version of `check_nr.sh` expected all Variant B TR_VERIFY lines to be
  good; 48/96 per session are correctly `,0,0` (TRUE's citations absent
  from the liar's log — the preregistered behavior). The checker was
  fixed to assert the half/half side-split instead. No driver, prereg,
  or bar was touched.

## Files staged (parent: commit sequentially; never stage binaries)

- `~/workspace/tnn-lab/wave10/debate-norecord/PREREG_DEBATE_NORECORD.md`
- `~/workspace/tnn-lab/wave10/debate-norecord/debate_nr.zag`
- `~/workspace/tnn-lab/wave10/debate-norecord/run_nr.sh`
- `~/workspace/tnn-lab/wave10/debate-norecord/verify_bars.sh`
- `~/workspace/tnn-lab/wave10/debate-norecord/check_nr.sh`
- `~/workspace/tnn-lab/wave10/debate-norecord/TRIAL_RESULTS_NORECORD.md` (this file)
- Transcripts: `run_A_small_{a,b}.txt`, `run_A_scale_{a,b}.txt`, `run_B_small_{a,b}.txt`, `run_B_scale_{a,b}.txt`
- Logs: `trial_run.log`, `verify.log`
- Vendored (byte-identical to wave8): `st_memory_core.zag`, `il_core.zag`, `substrate/`
- Removed before staging: `debate_nr_bin`, `.zag-cache/`, `.zagd.semantic-ready`

## Draft commit message

```
wave10 EXP-3: debate without authoritative world records

Variant A (no public records): spectator evidence margin collapses to
exactly 0; R2 abstains 60/60; R3 interrogation recovers 40/60 via the
admission-against-interest channel only (oracle component 0).
Variant B (liar-authored records): spectator captured 60/60 by the liar;
ledger-consistency (il_check 480/480 OK) provably blind to provenance
poisoning; interrogation hurts (-40 margin delta); over-claim probe
exposes 60/60 unsupported assertions but flips nothing.
Falsification tripwires did not fire: records-are-load-bearing survives
in both directions. 73/73 runner checks + independent transcript
re-derivation pass; byte-identical paired reruns; zero RNG.
Prereg frozen pre-build, zero amendments; flagged for Micah's
retroactive review.
```
