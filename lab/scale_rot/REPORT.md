# Scale-rot battery — REPORT (pilot + official 1x/10x legs)

**Line:** B3 scale-rot. **Date:** 2026-09-27. **Branch:** `tnn-native-lab`.
**Prereg:** `docs/lab/scale_rot/PREREG.md` (commit `e60e5885f4e8095198b6b4286f0a2de0e2c800a9`), frozen BEFORE the official legs below.
**Standing law:** nothing should degrade with more scale — scale-rot is a defect.

## Headline

- **One-brain v3 (M1):** NO scale-rot at 10x. 23/44 → 230/440 (identical 52.3%), 0/440 verdict flips, byte-identical reruns.
- **Dialogue deliberation frozen R4 (M2):** NO scale-rot at 10x. 27/33 → 270/330 (identical 81.8%), 0/330 flips, byte-identical reruns.
- **Production chunker 57Q battery (M3a):** 57/57 correct, 57/57 native, 0 fallback; byte-identical reruns. PASS.
- **Production chunker text-length (M3b):** **SCALE-ROT DEFECT FOUND — the production intake PANICS on any input over 64 words** (`panic: slice index out of bounds`, rc=1). 64 words OK, 65 words crashes. Root cause identified (see WO-SR-1).
- **Native epistemics (M4):** BLOCKED ON DEPENDENCY — no passing label-blind Phase-1 verdict on origin (train-LOO `d758a876c` does not satisfy prereg `bbaa88099` K6).
- **100x legs:** BLOCKED ON DISK (K5) — home disk at 99–100% all night; see § Disk.

## Official results (post-prereg-commit)

All legs run twice; SHA-256 of full stdout compared.

| Mechanism | Leg | Result | Determinism (2 runs) | Flips vs 1x |
|---|---|---|---|---|
| M1 one-brain v3 | 1x (44) | 23/44 = 52.3% | `55389ee2…e8cc` identical | — |
| M1 one-brain v3 | 10x (440) | 230/440 = 52.3% | `fc713d12…05` identical | 0/440 |
| M2 deliberation R4 | 1x (33 probes) | 27/33 = 81.8% | `c22c908e…599` identical | — |
| M2 deliberation R4 | 10x (330 probes) | 270/330 = 81.8% | `84059355…44f` identical | 0/330 |
| M3a chunker 57Q | 1x | 57/57, 57 native, 0 fb | `0a341163…68` identical | — |
| M3b chunker text | 60 words | P2+P3 correct, det. | `c743583c…43` identical | n/a |
| M3b chunker text | 64 words | P2+P3 correct, det. | `0feed6c0…db` identical | n/a |
| M3b chunker text | 65+ words | **PANIC** rc=1 | n/a (crash) | n/a |

Kill bars: K1 (determinism) PASS everywhere it could run. K2 (zero flips) PASS (0/440, 0/330).
K3 (no crash) **FAIL** on M3b at 65+ words. K4 (≤5pt accuracy drop) PASS (0.0pt drops).
K5 (disk gate) blocks all 100x legs.

Replication method (M1/M2): frozen 1x set deterministically replicated with unique ID
suffixes (`_s00`…); item content and expected answers identical. This tests
problem-count/batch scale, not semantic-diversity scale (noted limitation — a
diverse-10x set needs labeled items this battery cannot manufacture overnight).

## WO-SR-1 (P0): production chunker panics on inputs over 64 words — K3 FAIL

- **Symptom:** `tnn_intake` (the promoted live production entry point,
  `docs/lab/mg_chunking_promote/intake.zag`) crashes with
  `panic: slice index out of bounds`, rc=1, on any text with ≥65 words.
  Bisected: 64 words OK, 65 words panics; 100/200/400/600/6000 all panic.
- **Root cause (white-box):** `cand_word` calls `enum_words(t, woffs, wlens)`,
  which writes `w_u32le(offs, n*4, …)` per word with **no bounds check**.
  Every production caller (`battery1.zag`, `regress_degen.zag`, and therefore the
  live intake path) passes 256-byte `woffs`/`wlens` buffers = **64 u32 slots**.
  Word 65 writes out of bounds → panic (loud here; heap corruption in an
  unchecked build).
- **Why this is scale-rot, not a corner:** the 64-word ceiling is an arbitrary
  fixed table, exactly the class Micah's no-arbitrary-limits law kills. Any real
  user text over ~64 words crashes the production intake. The 57-question
  promotion battery never caught it because its longest text is far shorter.
- **Repro:** build `docs/lab/mg_chunking_promote/scale_text.zag` (committed with
  this battery) and run the 65-word leg; or call `tnn_intake` on any >64-word text.
- **Routing:** chunker-owning line (intake.zag); cc B2 native-authorship (it is
  converting chunker policy — the table sizing belongs in that conversion).
  Fix direction (not prescribed): bound `enum_words` by buffer capacity with a
  graceful fallback, or size the word table from the input. Broad fix, not a
  per-item patch.

## WO-SR-2 (P2): "what is the Nth word of …" unclassified (KIND0) — pre-existing, not scale-rot

- **Symptom:** the question shape "what is the {ordinal} word of {text}" is not
  classified by the frozen learned policy (`kind=KIND0`, "question unclassified
  by the parser"); the default deliberative magnifier answers "" (correct=0).
  Fails identically at 10 words — present before any scaling.
- **Note:** the 57-question promotion battery contains only first/last bare-word
  ordinals, so the learned policy never saw numeric word ordinals. The sibling
  shape "how many a's in the {ordinal} word of …" classifies fine
  (LETTER_COUNT_WORD) at all tested sizes.
- **Routing:** chunker-owning line / B2 (classifier coverage).

## Observation for the deliberation-repair coordinator (not a work order)

The committed frozen R4 build scores **27/33** on the committed `round4/battery.txt`
(the 6 FAILs are withhold-behavior items: the build answers substantively where the
battery expects "I don't know…" — e.g. R4-01 probe 2, R4-03 probe 4, R4-06 probes
1/3, R4-07 probe 1, R4-09 probe 2). This differs from the 38/38 round-4 adoption
claim — likely battery/build skew between committed state and the repair worktree's
staged changes. The 27/33 baseline replicated to 270/330 with zero flips, so the
scale result stands regardless; the absolute gap is the repair line's to reconcile.

## Blocked / deferred

- **100x problem-count legs (M1/M2) and 600/6000-word text legs (M3b):** BLOCKED ON
  DISK per K5. M3b's 600/6000-word legs are additionally moot until WO-SR-1 is fixed.
- **M4 native epistemics:** BLOCKED ON DEPENDENCY (no passing Phase-1 verdict on origin).

## Disk incident (this session)

- Home disk went 99% (1.3G free) → **100% (64K free)** during this battery.
- Freed **537MB** by deleting 23,453 orphaned `tmp*.json` commit-staging payloads
  older than 6h in `~/workspace/tmp_commit/` (regenerable; commit scripts re-upload
  idempotently; nothing from the last 6h touched).
- Even after freeing 537MB, only ~152M showed free — **something is actively
  consuming disk at high rate tonight**. Flagged for the night-shift line; K5
  remains the binding constraint on 100x work.

## Pre-freeze disclosure (from PREREG.md)

M1/M2 1x/10x pilots ran before the prereg was written (harness validation only).
All official legs above re-ran AFTER the prereg commit `e60e5885f`; SHAs match the
pilots exactly (no tuning occurred — bars were frozen from standing law).

## Files committed with this battery

- `docs/lab/scale_rot/PREREG.md` (commit `e60e5885f4e8095198b6b4286f0a2de0e2c800a9`)
- `docs/lab/mg_chunking_promote/scale_text.zag` — text-length scale driver (same commit)
- This report → `docs/lab/scale_rot/REPORT.md` (to commit next)

## Recommended follow-ups (for parent routing)

1. WO-SR-1 → chunker owner + B2 (P0).
2. WO-SR-2 → chunker owner / B2 (P2).
3. Re-run M3b 600/6000-word legs after WO-SR-1 fix; re-run M1/M2 100x legs when K5 clears.
4. M4 scale leg when a passing Phase-1 verdict lands.
5. z.ai skeptic review of this battery's design is in flight (`scalerot-q1`); amend if it changes verdicts.
