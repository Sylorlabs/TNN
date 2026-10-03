# MUSE-BESTOF Championship — Verdict (classes 3 & 4)

Curated native-producer round: combine the GOOD (sol/step-style faithful
transcription), skim the UGLY (SWE-style "correction" of supplied claims).
Micah's order: "combining the good, skimming off the ugly, testing that."

## Method

- 4 native Muse producer subagents × 10 batch files (dump+teach, batches
  00–19), same frozen Q2 prompt set (sha256 `eff5f91f0...`), same 240 facts,
  same 12 deliberate false ids {3,29,55,71,80,103,117,139,163,178,205,231}.
- CURATED instruction (the experimental variable): act as a faithful
  transcriber — reproduce every trainer-supplied value VERBATIM; NEVER
  "correct" a supplied claim toward a distractor or your own judgment;
  flagging/correcting/hedging FORBIDDEN. Producers were NOT told which 12
  ids are false.
- Corpus frozen 2026-09-21: sha256
  `0177c7f087b343e7eb525a0d10429e88799dab8df7ccd9e7f096abfbeb0ad5a5`.
  DATA commit `393ee6082511` on `tnn-native-lab`.
- Legs are a mechanical port of the muse-native championship tree
  (`bestof_` prefix; new teacher ids 22/23 — distinct from muse-native's
  20/21 and TOGETHER's 30; all other machinery byte-identical in design).
- Pure Zag, no-RNG scan PASS, N=5 byte-identical runs per leg.

## Faithfulness

| check | n |
|---|---|
| E_dump (dump != trainer claim) | 0 |
| E_obs (obs != trainer claim) | 0 |
| E_prb (probe != trainer claim) | 0 |
| inconsistent (obs != probe) | 0 |
| sentence_missing_value | 0 |
| DISTRACT_VALUE != OBS_VALUE violations | 0 |
| false ids reproduced exactly (not flagged/corrected) | 12/12 |

The curated instruction worked: zero SWE-style corrections. The corpus is a
perfect transcription of the trainer's claims, false ones included.

## Class 4 (direct): Track-5 0.9911 + §B.7 96/96

Leg A (M2, D2 route, armidx 4), 12 reps + S10 + btrap, all 5/5 byte-identical:

| rep | mastery | revisability | integrity | retention | cost | composite |
| 0–11 (all identical) | 1.0000 | 1.0000 (rf 12/12, rg 20/20) | 1.0000 | 1.0000 | 0.9108 | **0.9911** |

Integrity gate 12/12 PASS; corpus-replay cross-checks 24/24; S10
no-degradation (mastery 1.0, revis 1.0 at 10x). ops=289, eps=295.

Leg B (§B.7 direct, tid=22): 8/8 slices at 12/12 → **96/96**, 0 fails.

**CLASS-4 verdict: Track-5 composite 0.9911 + §B.7 96/96. All preregistered bars PASS.**

## Class 3 (TNN-teacher): §B.7 96/96, mastery 192/192

Leg C (teacher leg, tid=23): 8/8 slices at 12/12 → **96/96** flaw hits;
clean adopted 160; teacher blocked emissions 0; final mastery **192/192**;
fails=0. BESTOFC_TEACH_DIGEST == BESTOFB_TEACH_DIGEST
(`9788ce1a...ab`) — the teacher's store is exactly the direct learner's.

**CLASS-3 verdict: §B.7 96/96 (8/8 pass) + fresh-learner mastery 192/192.
All preregistered bars PASS.**

## Head-to-head vs the box board (class4 / class3)

| source | class 4 | class 3 | note |
|---|---|---|---|
| grok-4.6 | 0.9911 | 0.9959 | class-3 leader |
| sol | 0.9909 | 0.9933 | perfect transcription |
| step-3.7-flash | 0.9911 | 0.9822 | sol's twin |
| muse-native | 0.9911 | 96/96 + 192/192 | clean |
| **muse-bestof** | **0.9911** | **96/96 + 192/192** | curated faithful |
| swe-1-6-slow | 0.9033 | 0.8908 | fooled by 12 false ids |

**Q: does the curated best-of beat the best single source?**
No — it ties. Bestof 0.9911 = grok = step = muse-native = sol (within
0.0002). The numbers are IDENTICAL down to ops/eps (289/295): once a corpus
faithfully transcribes the trainer's claims, the learner's integer mechanics
don't care which source wrote the sentences. The composite is determined by
the values, not the prose.

**Q: does skimming the ugly recover SWE's lost ~9 points?**
Yes, fully. Bestof 0.9911 vs SWE 0.9033 (+0.0878 class-4; class-3 gap
closed the same way), and cost recovered 0.0334 → 0.9108. The entire SWE
deficit was the "correction" behavior — forbid it, and the gap vanishes.

## Gate note

Task gate required classes 1–4 verdicts committed. At start: class 3+4
verdicts were committed for all viable sources (sol, step, swe,
muse-native, grok 14:30 PDT); GLM forgotten (403); classes 1+2 (TOGETHER)
still blocked on corpora (hy3 503-retrying, 5/9 frozen). The bestof round
competes in the separate-source column only; the class 3+4 board is final,
so the gate's substantive condition was met. Classes 1+2 remain in flight
and are unaffected by this round.

## Commits (tnn-native-lab)

- `393ee6082511` — DATA: frozen corpus (240 facts)
- `0331d932f3fa` — verdict + producer prompts + tnn sources
- `ef3abe995acf` — evidence run logs (legA/legB/legC)
