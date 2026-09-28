# Scale-rot battery — REPORT: 100x legs

**Line:** B3 scale-rot. **Date:** 2026-09-27 (evening). **Branch:** `tnn-native-lab`.
**Prereg:** `docs/lab/scale_rot/PREREG.md` (commit `e60e5885f4e8095198b6b4286f0a2de0e2c800a9`), frozen BEFORE all legs below. No amendment was needed: the 100x legs were already frozen in the prereg ("100x only if K5 allows").
**Official 1x/10x report:** `docs/lab/scale_rot/REPORT.md` (commit `6a649b45a585`). This document covers ONLY the 100x legs (plus fresh 1x/10x re-runs done here as comparability controls). It does not rewrite REPORT.md.

## Headline

| Mechanism | 100x leg | Verdict |
|---|---|---|
| M1 one-brain v3 (4400 problems) | 2300/4400 = 52.3%, **0/4400 flips**, byte-identical reruns | **PASS — no scale-rot at 100x** |
| M2 dialogue deliberation R4 (3300 probes) | **PANIC at dialogue 74/900** (`panic: slice index out of bounds`, rc=1) | **K3 FAIL — scale-rot defect found (WO-SR-3, P0)** |
| M3a chunker 57Q battery | 57/57, 57 native, 0 fallback; SHA reproduces committed baseline exactly | **PASS** |
| M3b chunker text length (60/600/6000 words) | all legs rc=0, P2+P3 correct at every size; WO-SR-1 fix verified first at 65 words | **PASS — WO-SR-1 closed** |
| M4 native epistemics | not run | **BLOCKED ON DEPENDENCY** (unchanged) |

K5 (disk gate): 25 GB free before and after every leg — CLEAR throughout.

## M1: one-brain v3 — PASS at 100x

Frozen source `docs/lab/onebrain3/impl/onebrain_v3.zag` (SHA `f8abec7220cce17d`), built with the pinned toolchain. Replication: deterministic, item-major, IDs suffixed `_s000`…`_s099`, item content and expected answers byte-identical. Every leg run twice; SHA-256 of full stdout compared; stderr captured separately.

| Leg | Items | Correct | Rate | Determinism (2 runs) | Flips vs 1x twins | Wall |
|---|---|---|---|---|---|---|
| 1x | 44 | 23 | 52.3% | `b202dc02…f103` identical | — | 0.9 s |
| 10x | 440 | 230 | 52.3% | `d0b4accb…699f` identical | 0/440 | 3.1 s |
| 100x | 4400 | 2300 | 52.3% | `3c019bce…bd02` identical | **0/4400** | 25.8 s |

- Flip check compares the FULL verdict tuple per item (winner, action, score, fork, close, answer) against the 1x twin (suffix stripped with `_s\d+$` on full IDs). Zero flips.
- Kill bars: K1 PASS, K2 PASS, K3 PASS (rc=0, empty stderr on all legs), K4 PASS (0.0 pp drop).
- Red-team note (cache replay): no content-keyed result cache exists in the source — the only "cache" is a per-problem evidence-slot tiebreak table inside the per-problem ledger, which `solve_one` re-initializes via `led_init` for every problem. Wall-time evidence agrees: per-item cost 19.6 → 7.1 → 5.9 ms across 1x/10x/100x (startup amortization, not a collapse to ~0 as memoization would show).
- Anomaly (not a kill-bar event, recorded for the one-brain line): my 1x/10x stdout SHAs do NOT match the official REPORT.md SHAs (`55389ee2…` / `fc713d12…`), although verdicts reproduce exactly (23/44, 230/440, 0 flips) and M2/M3a SHAs reproduce byte-exactly (see below). Four replication variants tried (item/block-major × `_s00`/`_s0`/`_repNN`, header/no-header) — none reproduce the official bytes. The frozen source is byte-identical between the report commit and now, and the toolchain SHA matches the pinned value (`498abcb5…`). Most likely the official M1 binary was built from a worktree with uncommitted source drift, or from a different replication input. K1 as preregged (my two runs byte-identical) holds.

## M2: dialogue deliberation frozen R4 — K3 FAIL at 100x (WO-SR-3)

Frozen source `docs/lab/dialogue/deliberation/build/deliberate_frozen_r4.zag` (SHA `7dec26d8600683f2`). Replication: DIALOGUE blocks replicated block-major, IDs suffixed `_s00`…`_s099`; kb.txt/gaz.txt unchanged (KB is constant by prereg design). "Probe" = one turn-verdict (T-line), matching the official report's 33-probe convention (non-NOVEL T-lines); flip checks cover all 38 turn-verdicts including the 5 `NOVEL=1` ones.

| Leg | Probes | Pass (33-convention) | Determinism (2 runs) | Flips vs 1x twins | Wall |
|---|---|---|---|---|---|
| 1x | 33 | 27/33 (32/38 incl. NOVEL) | `c22c908e…4b81` identical — **matches official REPORT.md byte-exactly** | — | 0.7 s |
| 10x | 330 | 270/330 | `e5e139a1…41d0` identical | 0/380 | 3.7 s |
| 100x | 3300 planned | **crashed** | panic output byte-identical across both runs (`d0fd3a45…78f7`) | 0/1299 on completed portion | ~9 s to crash |

**The crash.** The 100x leg panics with `panic: slice index out of bounds`, rc=1, after completing 73 of 900 DIALOGUE blocks (1299 turn-verdicts emitted, then stderr `panic: slice index out of bounds`). Bisected: 72 dialogues run clean, 74 panic; the 74th dialogue alone runs clean — pure accumulated cross-dialogue state, deterministic.

**White-box root cause.** `proc_sentence` appends every query's key IDs into the shared `keya` arena via `arena_append` (4 bytes/key, **no bounds check**). `keya` (65536 bytes = 16384 key slots) is initialized once at startup and **never reset** — not per query, not per dialogue (the per-query reset only clears `linka`). Measured with an instrumented debug build: `keya_used` grows 896 bytes (224 keys) per R4-01 dialogue — 812 → 1708 → 2604 … → 65324 — then the next append writes past the 64 KB slice and panics. 65536/896 ≈ 73.1 dialogues: the cliff lands exactly on dialogue 74. Vocab (`vent`) is steady-state (idempotent interning, confirmed 228 entries throughout); the response accumulator (`dacc`) reaches only ~67 KB of its 128 KB. Verdicts were stable (0 flips) on all 1299 completed turn-verdicts right up to the crash — the defect is a fixed-arena capacity cliff, not gradual rot.

**Assessment.** This is scale-rot under the prereg definition (crash appearing only at larger scale) and under standing law (a fixed 64 KB table that fills as a pure function of total queries processed — the same arbitrary-fixed-table class as WO-SR-1). Per the prereg, the M2 mechanism is STOPPED at 100x; 1x/10x results stand. Note this vindicates the battery's sensitivity: the replication legs caught a real cross-item state leak (the z.ai critique's "ledger/state crossing item boundaries" — here it is, in `keya`).

### WO-SR-3 (P0): frozen R4 deliberation build panics past ~73 dialogues — K3 FAIL

- **Symptom:** `deliberate_frozen_r4.zag` panics (`panic: slice index out of bounds`, rc=1) on the 74th DIALOGUE block of a multi-dialogue run. 1x (9) and 10x (90) legs pass; 100x (900) crashes deterministically.
- **Root cause (white-box):** shared `keya` key arena (64 KB) in `proc_sentence` accumulates every query's key IDs via unbounded `arena_append`, never reset between queries or dialogues. +224 keys per R4-01 dialogue → arena exhaustion at ~73 dialogues.
- **Repro:** replicate `docs/lab/dialogue/round4/battery.txt` DIALOGUE blocks ×74 with suffixed IDs, run the frozen build; or run the 74-dialogue prefix battery. Debug evidence: instrumented `DBG keya_used=` trace shows linear growth to 65324 before the fatal append.
- **Routing:** dialogue-deliberation owning line. Fix direction (not prescribed): reset `keya` per query like `linka` (key offsets are per-query absolute, so a reset is semantics-preserving), or bound `arena_append`.
- **Not fixed by this battery** (owning line fixes; this battery files work orders).

## M3a: production chunker 57Q — PASS (baseline reproduced exactly)

`battery1.zag` through the FIXED `intake.zag` (WO-SR-1 repair, commit `b257c02cc`): **57/57 correct, 57 native, 0 fallback, `# VERDICT PASS`**. Full-stdout SHA `0a34116398fcd22b313c785c1d1037d712a444f18b3925ce49ac29316a41d268` — **byte-identical to the SHA in the committed REPORT.md and in the WO-SR-1 fix commit's regression gate**. Two runs byte-identical, rc=0, empty stderr. K1/K3 PASS. The fix did not move the 57Q baseline by a single byte.

## M3b: chunker text length — PASS (WO-SR-1 verified closed)

Per the task order, the WO-SR-1 fix was verified FIRST at 65 words (the exact count that panicked pre-fix) with a dedicated driver through live `tnn_intake`: `correct=1 native=1 fallback=0`, rc=0, byte-identical across 2 runs, empty stderr. Then the frozen `scale_text.zag` legs:

| Leg | Words | P1 "{N}th word" | P2 "last word" | P3 "a's in {N/2}th word" | rc |
|---|---|---|---|---|---|
| 60 | 60 | correct=0 (pre-existing WO-SR-2, unclassified shape — same at all sizes) | 1 | 1 | 0 |
| 600 | 600 | 0 (WO-SR-2) | 1 | 1 | 0 |
| 6000 | 6000 | 0 (WO-SR-2) | 1 | 1 | 0 |

Full-stdout SHA `f148f925bba4a01492eb384d495d48defde9119340c141f1b36219f42fb5f714`, 2 runs byte-identical, stderr empty. K1 PASS, K3 PASS at every leg — the 65+ word panic is gone. P1's `correct=0` is the pre-existing WO-SR-2 classifier gap (identical at 10 words; not scale-rot). **WO-SR-1 is CLOSED by this battery.** WO-SR-2 remains open (P2, with the chunker-owning line).

## M4: native epistemics — BLOCKED ON DEPENDENCY (unchanged)

Not run, per prereg. `docs/lab/epistemic_native/NO_GO_REPORT.md` is on origin: the label-blind rerun failed fairly at 6/10 vs the K6 ≥8/10 gate. No passing Phase-1 verdict has landed since.

## Kill-bar readings (100x legs)

| Bar | M1 | M2 | M3a | M3b | M4 |
|---|---|---|---|---|---|
| K1 determinism (absolute) | PASS | PASS (panic itself deterministic) | PASS | PASS | n/a |
| K2 zero flips (absolute) | PASS (0/4400) | PASS on completed portion (0/1299); leg incomplete | n/a (fixed battery) | n/a (closed-form) | n/a |
| K3 no crash (absolute) | PASS | **FAIL** → WO-SR-3 (P0) | PASS | PASS (was FAIL pre-fix) | n/a |
| K4 ≤5 pp accuracy drop | PASS (0.0 pp) | n/a (crashed) | PASS | PASS | n/a |
| K5 disk gate | CLEAR (25 GB free) | CLEAR | CLEAR | CLEAR | n/a |

## Red-team notes (on this battery's own verdict)

1. **Flip-check logic:** full verdict tuples compared (M1: winner+action+score+fork+close+answer; M2: NOVEL-flag+verdict+answer-text), suffix stripped via `_s\d+$` on complete IDs only. Record counts reconcile exactly (M1: 4400/4400 matched; M2 10x: 380/380; M2 100x partial: 1299/1299). No silent degenerate matching.
2. **Determinism:** every leg ran twice; SHA-256 over full stdout; stderr captured separately (empty everywhere except the M2 100x panic's own stderr, which is part of the finding).
3. **Cache-replay (z.ai critique):** source-audited both mechanisms — no content-keyed result memoization exists (M1's "corr cache" is a per-problem evidence-slot table inside the per-problem ledger; M2's sha256 is trace/DIGEST-only). Wall-time scaling corroborates (M1 0.9→3.1→25.8 s; M2 0.7→3.7 s then crash — no collapse to constant time). The M2 crash itself is the counter-evidence to "replication legs test only the harness": they caught a genuine cross-item state leak.
4. **Scope honesty:** replication tests problem-count scale only — KB breadth/density, per-item complexity, and order permutation are NOT covered here; they are proposed as prereg amendments in `AMENDMENT_PROPOSAL_ZAI.md` (awaiting Micah's signature, not adopted, not run).

## Provenance

- Toolchain `znc_linux_x86_64_abed8aa1` SHA-256 `498abcb5ab346f8c…` (matches pinned value).
- Frozen sources (origin/tnn-native-lab): `onebrain_v3.zag` `f8abec7220cce17d`, `deliberate_frozen_r4.zag` `7dec26d8600683f2`, `battery1.zag` `ffabd23b525769dd`, `intake.zag` (fixed) `ffc9fe9d110662a8`, `scale_text.zag` `ad6feac1e16b2716`, `v6.tsv` `42d215ecebc93021`, `round4/battery.txt` `90c277e1be0d98cf`.
- Built binaries (scratch only, NOT committed): onebrain `9f407fa2…`, deliberate `9ac5da16…`, battery1 `1896893a…`, scale_text `4c2092c9…`.
- Replication generators: deterministic Python (no RNG); replicated inputs hashed (`v6_100x.tsv` `e39b9b6d…`, `m2_100x.txt` `124a0ef7…`). Full run outputs (13 MB M1 100x etc.) are regenerable scratch — not committed; SHAs above are the evidence.

## Files

- This report → `docs/lab/scale_rot/REPORT_100X.md` (this commit)
- `docs/lab/scale_rot/AMENDMENT_PROPOSAL_ZAI.md` — z.ai skeptic-review amendment draft, **AWAITING MICAH'S SIGNATURE** (not adopted; proposed legs not run)

## Work orders

- **WO-SR-3 (P0, NEW):** M2 frozen R4 build panics past ~73 dialogues — shared `keya` arena exhaustion. → dialogue-deliberation owning line. (This report, § M2.)
- WO-SR-1 (P0): **CLOSED** — fix verified at 65 words + 60/600/6000-word legs all pass.
- WO-SR-2 (P2): still open — "{ordinal} word of …" unclassified (pre-existing, not scale-rot).
