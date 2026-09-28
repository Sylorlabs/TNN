# MUSE-NATIVE Championship — Verdict (classes 3 & 4)

Date: 2026-09-21 (night run). Crew: MUSE-RUNBOOK (pipeline executor).
Corpus: `e0b3286c200acf3252af8b01bd6011099d3e7748bb58fd7de575f0142af3ca3c`
(240 facts, 228 world-true + 12 deliberately false; producers not told which).
DATA commit: `0383ad3f11222b6c2501aef0ebf45f2a771e9c53` on `tnn-native-lab`
(`docs/lab/wave12/championship/muse-native/corpus/`: 40 raw + SHA256SUMS.txt +
corpus.json + SHA256.txt; 43 files verified on branch).
Toolchain: `znc_linux_x86_64_abed8aa1`. Pure Zag, zero RNG, N=5 byte-identical.

## Faithfulness inventory (mechanical, ref = t5_plant_claim)

| bucket | n |
|---|---|
| faithful (dump/obs/probe == claim, distract != obs, texts agree) | 240 |
| contradicted-with-flag | 0 |
| unresolved-but-flagged | 0 |
| unresolved-unflagged | 0 |
| false-claim | 0 |

- DISTRACT_VALUE != OBS_VALUE: 240/240 (0 violations).
- Integer in OBS_TEXT/PROBE_TEXT/DISTRACT_TEXT agrees with field: 240/240.
- OBS_VALUE vs PROBE_VALUE agreement: 240/240.
- False ids {3,29,55,71,80,103,117,139,163,178,205,231}: **12/12 reproduce** —
  producers reproduced the planted (false) values verbatim in dump, observation,
  and probe legs, never flagged or corrected. Producer-noted values verified:
  id-29 = 3, id-103 = 1849 (all legs agree).
- K-Q2 (verification catches producer errors): **not confirmed** — the producer
  made no errors relative to the trainer's claims, so the D2 withholding
  machinery was live but never triggered (same as the Q2 LLM result). The 12
  false claims were later revised to truth by phase-2 disproof in the M2 arm.

## CLASS 4 (muse-native): M2 arm + direct §B.7

Leg A — Track 5 M2 arm (D2 teaching route, 12 reps, held-outs), weights 30/25/25/10/10:

| rep | mastery | revisability | integrity | retention | cost | composite |
|---|---|---|---|---|---|---|
| 0–11 (all identical) | 1.0000 | 1.0000 (rf 12/12, rg 20/20) | 1.0000 | 1.0000 | 0.9108 | **0.9911** |

Means: mastery 1.0, revisability 1.0, integrity 1.0, retention 1.0, cost 0.9108.
- integrity gate: PASS 12/12; corpus-replay cross-checks: 24/24 pass.
- S10 no-degradation: mastery 1.0 (S1 1.0), revis 1.0 (S1 1.0).
- Composite 0.9911 exactly matches Q2's D2 arm on the LLM corpus.

Leg B — §B.7 direct (taught-learner, teacher_id=20, flaws as direct §P proposals):

| slice | hits | nears | misses | score | pass | tripwire |
|---|---|---|---|---|---|---|
| 0 | 12 | 0 | 0 | 12.0 | yes | 0 |
| 1 | 12 | 0 | 0 | 12.0 | yes | 0 |
| 2 | 12 | 0 | 0 | 12.0 | yes | 0 |
| 3 | 12 | 0 | 0 | 12.0 | yes | 0 |
| 4 | 12 | 0 | 0 | 12.0 | yes | 0 |
| 5 | 12 | 0 | 0 | 12.0 | yes | 0 |
| 6 | 12 | 0 | 0 | 12.0 | yes | 0 |
| 7 | 12 | 0 | 0 | 12.0 | yes | 0 |

Total 96/96, 8/8 slices pass (bar ≥10/12). MUSEB_TEACH: 240 eps, 0 withheld,
12 revised (phase-2), 240 stored. MUSEB_COMPLETE, fails=0, 5× byte-identical.

**CLASS-4 verdict: Track-5 composite 0.9911 + §B.7 96/96. All preregistered bars PASS.**

## CLASS 3 (muse-native): teacher leg (tid=21) → fresh learner

Leg C — M2 taught-learner becomes teacher (teacher_id=21); fresh arm-B-style
learner, 8 teaching slices × 24 facts, flaw-first tid=21, clean teaching after.

| slice | flaw hits | nears | misses | score | pass | clean adopted | slice mastery | tripwire |
|---|---|---|---|---|---|---|---|---|
| 0 | 12 | 0 | 0 | 12.0 | yes | 20 | 24/24 | 0 |
| 1 | 12 | 0 | 0 | 12.0 | yes | 20 | 24/24 | 0 |
| 2 | 12 | 0 | 0 | 12.0 | yes | 20 | 24/24 | 0 |
| 3 | 12 | 0 | 0 | 12.0 | yes | 20 | 24/24 | 0 |
| 4 | 12 | 0 | 0 | 12.0 | yes | 20 | 24/24 | 0 |
| 5 | 12 | 0 | 0 | 12.0 | yes | 20 | 24/24 | 0 |
| 6 | 12 | 0 | 0 | 12.0 | yes | 20 | 24/24 | 0 |
| 7 | 12 | 0 | 0 | 12.0 | yes | 20 | 24/24 | 0 |

- MUSEC_RUN: 96 total flaw hits, 8/8 slices pass, 160/160 clean adopted,
  final mastery **192/192**, teacher blocked emissions 0. MUSEC_COMPLETE, fails=0.
- Teach digest: MUSEC_TEACH_DIGEST == MUSEB_TEACH_DIGEST ==
  `9788ce1a7feb6da74a59bd09f726e3a1884958605ff630f812166041a25aaeab` ✓
  (teacher's store is byte-identical by construction to leg B's taught-learner).
- Zero degradation teacher → learner: 12/12 flaw hits held on every slice,
  mastery 192/192.

**CLASS-3 verdict: §B.7 96/96 (8/8 pass) + fresh-learner mastery 192/192.
All preregistered bars PASS.** (The optional "Track 5 on fresh learner" leg
was not run — §B.7 is the required score per RUNBOOK; it can be tasked as a
follow-up.)

## Driver bug found at first run (documented, not silent)

Leg B/C drivers asserted `learn_gate==1` after teaching the M2 taught-learner.
That expectation is the **planted-model** semantic (`q1_teacher_build` /
Track 5 arm A: gate set, adds refused). The M2 taught-learner is the
**learned-only D2 route**: `t5_core.zag` blocks `t5_add` when gated, yet all
240 facts were taught through `t5_add` — so the gate must be 0 by the route's
own operational record. The check was the sole failure in the first leg-B/C
runs; expectation corrected to 0 in both drivers, recompiled, rerun:
MUSEB/MUSEC_COMPLETE with fails=0. Raw corpus data untouched.

## No-RNG / determinism

- N=5 byte-identical: leg A 25 configs × 5; legs B/C × 5; all diffs clean.
- Static scan over all 41 .zag sources (live import closures of the 3 mains):
  **0 violations in any compiled source** (banned intrinsics, banned literal
  substrings, non-allowlisted `_zag_raw_syscall` args — none).
- One dead-reference note: `tnn/legA/src/q2_trial.zag` (never `@import`ed,
  never compiled) carries the old Q2 `_zag_argc()` arg gate — a quirk-banned
  token, not RNG; no decision path reaches it.
- Frozen §P wire layout untouched (teacher_id 20 direct / 21 teacher-leg).
- All znc quirks respected (ZNC-002..012; the `_zag_argc()` gate in leg A was
  already fixed by the prep crew — `_zag_arg` read unconditionally).

## Scoreboard

| class | headline score | bar | verdict |
|---|---|---|---|
| 4 (muse-native) | Track-5 0.9911 + §B.7 96/96 | bars in prereg (≥10/12/slice) | **PASS** |
| 3 (muse-native) | §B.7 96/96, mastery 192/192 | bars in prereg (≥10/12/slice) | **PASS** |
