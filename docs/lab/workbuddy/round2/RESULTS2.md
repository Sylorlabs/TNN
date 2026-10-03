# Crew D Results — Workbuddy Round 2 (strict re-run)

**Binary SHA-256:** `7636a577fff29de6eae10fe238e33514083a3059aa9df8f64784a9601a684a09`
(built from source `0bec5459b2959ec056c6c8771de7de009d7fd9406d7029d98fa97faa1a9d531b`;
binary is evidence only, not delivered)
**Date:** 2026-09-27

## Verdict table

| Gate | Result |
|------|--------|
| Crew A strict battery (24 probes) | **24 PASS / 0 WEAK / 0 FAIL** |
| Crew C probe set (32 probes, incl. 6 adversarial) | 26 byte-identical to Crew B; 6 intended repairs, all correct |
| S1 frozen checksum | **PASS** — `3d60c4e33c0259b12fd7d27363aed6e8eca095a75bbc8a4daadcc2b6bbcf418f` |
| S1 under `MALLOC_PERTURB_=165` | same SHA — **PASS** |
| S1 under `MALLOC_PERTURB_=90` | same SHA — **PASS** |
| Round-1 fixtures (4) | 3 byte-identical to Crew B; 1 intended single-line diff |
| Fresh-process determinism | every session/probe run twice, byte-identical |
| Confident-wrong scan | none found in any final output |

## Crew A battery — strict scores

Scorer: `~/workspace/wb2/crewA/battery/score_battery.py` (frozen).

| Session | Gate | Result |
|---------|------|--------|
| b_t1a–b_t1f (6) | T1 composition operators | PASS |
| b_t2a–b_t2d (4) | T2 anaphora | PASS |
| b_t3a–b_t3c (3) | T3 supersede | PASS |
| b_t4a–b_t4b (2) | T4 | PASS |
| b_t5a–b_t5b (2) | T5 | PASS |
| b_t6a–b_t6c (3) | T6 | PASS |
| (4 additional) | | PASS |

**TOTAL: 24 PASS / 0 WEAK / 0 FAIL (n=24)**

Evidence: `battery_run/` (all 20 battery sessions, fresh outputs; the scorer
evaluates 24 gates across them).

## Crew C probes — 32 files, 2 runs each, byte-identical pairs

| Probe group | Count | vs Crew B |
|-------------|------:|-----------|
| c_a1–a5, c_b1–b3, c_c1, c_c7, c_d1–d2, c_e1–e2, c_f1–f2, c_g1–g3, c_i1, g_t1–t6 | 26 | byte-identical |
| c_c2 (`actually,` correction) | 1 | **repaired:** serves `9876.` |
| c_c3 (distinct complements) | 1 | **repaired:** counts 2 |
| c_c4 (correction after question) | 1 | **repaired:** serves `2222.` |
| c_c5 (coexist + affirm) | 1 | **repaired:** both `yes.`, count 2 |
| c_c6 (period) | 1 | **repaired:** exactly one period |
| c_h1 (stale withheld) | 1 | **repaired:** `I don't know.` instead of affirming the retracted fact |

Evidence: `crewc_run/` (`<probe>.r1`, `<probe>.r2`).

## Crew D fresh probes (d_p1–d_p8)

| Probe | What it covers | Outcome |
|-------|----------------|---------|
| d_p1 | same subject/verb, distinct complements coexist | both affirmed; count 2 |
| d_p2 | verb-changing correction; aux-less corrected fact | stale withheld; `the beacon failed.` served; count 1 |
| d_p3 | correction immediately after a session question | corrected value served |
| d_p4 | double correction chain | newest served; count 1 |
| d_p5 | aux-less corrected fact retrievable | corrected served; stale withheld |
| d_p6 | aux-less declarative correction after a KB question | installed (`Noted.`), not mangled into a KB answer |
| d_p7 | correction retracts an earlier anaphoric fact | `who commands the ship?` → `I don't know.`; correction served |
| d_p8 | pronoun teaching after tombstoning | resolves to the surviving subject |

All run twice, byte-identical. Evidence: `probes/d_p*.txt`, `probes/d_p*.r1`, `probes/d_p*.r2`.

## Round-1 regression fixtures

| Fixture | Determinism | vs Crew B |
|---------|-------------|-----------|
| base_anaph | byte-identical ×2 | identical |
| val_teach | byte-identical ×2 | identical |
| base_correct | byte-identical ×2 | identical |
| val_shapes | byte-identical ×2 | **one intended diff, final turn:** `15 facts.` → `16 facts.` |

The `val_shapes` diff is the repair working as specified: a later plain
`quinn was promoted.` now correctly coexists with the live `quinn was demoted.`
under complement-aware identity, instead of overwriting it. Every other line is
identical.

## Footprint and hygiene

| Item | Status |
|------|--------|
| `~/workspace/wb2/crewD/` total | **5.3 MB** (limit: 300 MB) |
| `wb2_dialogue_bin` | removed from the commit-ready set (evidence-only) |
| `.zag-cache/`, `.zagd` | excluded |
| Crew A / B / C trees | not modified by Crew D |
| Original Workbuddy tree | not modified by Crew D |
| Commits by Crew D | none (parent owns branch surgery) |

## Known remaining behaviors (not defects)

- Aux-less yes/no questions echo the fact (`was the beacon failed?` →
  `the beacon failed`) rather than answering `yes.`. This matches the legacy
  echo path for verbless facts and never affirms a falsehood.
- `was quinn resigned?` after a verb-changing correction: Crew B answered `no.`
  (wrong — the fact was live); the repaired build serves the fact. Changed
  output, correct behavior.

## Honest verdict

All four Crew C defects are repaired, the full Crew A battery passes strictly,
S1 holds under heap perturbation, regressions are clean apart from the one
intended `val_shapes` line, and every output is deterministic across fresh
processes. The repair loop ran longer than the planned single loop (disclosed in
`REPAIR.md`); the source is now frozen and no further edits will be made.
