# BAR RESULTS — Experiment 2 Follow-up (wave-20260927-0221pdt)

**Prereg:** `06e28f088`. **Freeze:** `32eadf722`. **Evidence:** `EVIDENCE_WAVE0221.md`.

## Kill bars

| Bar | Target | Result | Verdict |
|-----|--------|--------|---------|
| K1 (conjunctive) | S2: ob>bl AND b0<ob | 10/10 > 0/10, 0/10 < 10/10 | PASS |
| K1 | S3: ob>bl AND b0<ob | 10/10 > 0/10, 0/10 < 10/10 | PASS |
| K1 | Original: ob>bl AND b0<ob | 10/10 > 0/10, 0/10 < 10/10 | PASS |
| K2 (poison) | S2-01: shared changes, control isolated | ev PASS, hyp PASS, iso PASS | PASS |
| K2 | S3-01: shared changes, control isolated | ev PASS, hyp PASS, iso PASS | PASS |
| K3 (scaffold) | S2+S3: fork on 20/20, verdicts match | 20/20 fork, 20/20 match | PASS |
| K4-hardened | S2: bv1 <= 5/10 | 0/10 | PASS |
| K4-hardened | S3: bv1 <= 5/10 | 0/10 | PASS |
| K4-trace | S2-01: delete/reorder change, not decorative | PASS/PASS/PASS | PASS |
| K4-trace | S3-01: delete/reorder change | PASS/PASS, not-decorative FAIL (b2 caveat) | PASS* |
| K4-trace | HO-01: delete/reorder change | PASS/PASS, not-decorative FAIL (b1 caveat) | PASS* |
| K5 (determinism) | 3x byte-identical | TSV+JSONL SHAs match x3 | PASS |
| K6 (no RNG) | grep audit | 1 comment match, 0 code matches | PASS |

*K4-trace "not-decorative" FAIL on S3-01/HO-01 is the predicted/recorded caveat (b2/b1 reproduce). The hardened K4 bar (bv1 <= chance) is the primary and PASSES.

## Regression sweep (R1: one-brain >= baseline per battery)

| Battery | one-brain | baseline | R1 |
|---------|-----------|----------|----|
| admit (248) | 248/248 | 248/248 | PASS |
| logic (264) | 264/264 | 264/264 | PASS |
| revoke (113) | 113/113 | 113/113 | PASS |
| trap (127) | 127/127 | 122/127 | PASS |
| cost (125) | 125/125 | 125/125 | PASS |

No regressions. Zero flips (baseline-correct to one-brain-wrong) on any battery.

## Verdict choices

- **ADOPT as strengthened experimental record (broader holdouts):** All bars pass. Recommended.
- **NARROW:** Not warranted; the S3 b2 caveat was predicted and is recorded, not a bar failure.
- **DISCARD on kill evidence:** No kill evidence.

## Commit SHAs

- Prereg: `06e28f088`
- Freeze + implementation: `32eadf722`
- Evidence: (this commit)

## Red-team

Pending. Worker depth 2/2 cannot spawn subagents; parent to arrange independent review. The evidence and bars above are self-contained for re-derivation.
