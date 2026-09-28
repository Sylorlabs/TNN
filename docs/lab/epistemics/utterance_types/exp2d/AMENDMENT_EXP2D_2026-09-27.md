# Amendment: exp2d Experimental Protocol (C1/C2/C3)

**Date:** 2026-09-27
**Amends:** `docs/lab/epistemics/utterance_types/exp2c/EXP_PREREG.md` (frozen; this is a separate experimental amendment)
**Sign-off:** Micah, 2026-09-27 (per 2026-09-27 orders)

## C1: Near-duplicate dedupe

**Rule (preregistered):** Replace any corpus item if it has:
- any 16-byte overlap with a curriculum utterance, OR
- any shared word 4-gram with a curriculum utterance, OR
- unigram Jaccard ≥ 0.60 with a curriculum utterance.

**Scanner:** `analysis/c1_scan.py` (deterministic, zero RNG).

**Replacements (exact):**
| ID | Old (flagged) | New (verified clean) | Reason flagged |
|----|---------------|----------------------|----------------|
| cc01 | (Jaccard 0.86 vs si3_14) | `Ask if the clinic accepts new patients.` | Jaccard 0.86 |
| cc05 | (Jaccard 0.62 vs si3_16) | `See if the upstairs window is shut.` | Jaccard 0.62 |
| cc40 | (4-gram `it is as if` vs si3_15) | `It is too dim to read the timetable.` | shared 4-gram |

IDs, polarities, speakers, and contexts are preserved. Only the utterance text changes.

**Verification:** Scanner re-run on final files: 0 flags.

## C2: Extended novel-family probes

**New files (frozen before runs):**
- `items/sinc3x_wi.txt`: 10 sincere `what if` lookalikes (nominalized: "the what ifs", "each what if", etc.)
- `items/sinc3x_wd.txt`: 10 sincere `where do` questions.

**Authoring rules:**
- Target bigram (`what if` / `where do`) required in each probe.
- Zero ≥16-byte overlap with curriculum and all corpora (verified by `stage2/author_xprobes.py`).
- Six-speaker rotation, sincere context (`says evenly`).
- Avoid surviving longer hypothetical markers (`where do we`, `where do they`, `what if the`).

**Scoring:** New `X2C_CURVE` block in source (inside `if(mode.len>0)`, after t3 loop). Read-only (log=0). Bar: ≥9/10.

**A priori finding:** The `wd` probes are confounded by cc19 (sincere "where do" in A+B) → predicted 10/10 on all corpus legs. The `wi` probes are the clean D/E diagnostic (0/10 → 10/10).

## C3: N-gram collision bound (not fixed in source)

**White-box:** Three support-1 provisional markers fire on sincere probes:
- `the clock` (hypothetical) → si3_03 (T3 DP 8/10 on v96)
- `is out` (hypothetical) → si5_01 (T5 DP 9/10 on ab2/abc2/v96; pre-existing in A+B)
- `at night` (joke) → si4_05, si5_09 (T4 DP 9/10, T5 DP 8/9 on v96)

**Decision:** PRECISELY BOUND, not fixed. The DP predictions INCLUDE these misses. A generic support-1 revocation was considered but NOT implemented (risk to D/E and load-bearing markers). The bound is: these 3 markers cause exactly the predicted misses, no more.

## Battery

- base, ab2-a/b, abc2-a (α control)/b (β), v96-a/b, de2-a/b: 3 reps each, byte-identical.
- empty: 3 reps, frozen SHA.
- Predictions locked in `PREDICTIONS_LOCKED.md` before runs.

## Source

- `h7_exp2d.zag`: v3 source + X2C block (no mechanism changes).
- `assemble_exp2d.py`: provenance script.
- HARD0: 11 hits, identical to v3 (zero new).
