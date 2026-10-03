# GROK_ENGLISH_VERDICT.md — grok-4.6 English championship source

> Status: DRAFT — numbers filled after the corpus freeze and leg runs.

## 1. Reachability

| Check | Result |
|---|---|
| UnoRouter `/models` lists `grok-4.6` | PASS (7 models, incl. grok-4.6) |
| temperature-0 / seed-42 chat probe | PASS (`OK`, 8.1 s) |

## 2. Corpus

| Item | Value |
|---|---|
| Model | grok-4.6 (UnoRouter), temperature 0, seed 42 |
| Frozen inputs sha256 (facts.json) | `4f1ba933a75a0f9e488ae170366afe7f514aec425f92432f5b0e0b49c4bfede5` |
| Prompt-template sha256 | `ac5d7d3155f9a90dc60f4f3ec529a3c6125a0469ce5862c7193fb261441b8b7d` |
| corpus.json sha256 | `7f3a25739981c8276082ceeda7de3628afd88977e7a16bd0a5f220eba2bc2508` (post-freeze; pre-freeze run-1 sha `d5be2b95…` superseded — final run re-captured batches 13/14/15/17/19) |
| Dump rows / teach rows | 240 / 240 (all ids 0–239) |
| Retries (mechanical parse only, max 2) | 0 parse retries (corpus meta `retries=[]`); wrong values never retried. **Noted procedural deviation:** the frozen rule named only HTTP 429/503 for paced handling, but the generator's HTTP loop (`build/gen_corpus.py::api_call`) also applied a 10-attempt backoff (10s×attempt) to other transient errors — in practice HTTP 524 (Cloudflare timeout), recovered 19× in the initial full run and 9× in the final re-capture run (batches 13/14/15/17 one each, batch 19 five). A 524 is a failed request with no response body, so no model output was ever re-sampled; the rule's protective intent (no value cherry-picking) is evidenced as honored — grok's 7 dump word-length errors and all 12 supplied false values are preserved verbatim in the accepted corpus (`ERROR_INVENTORY.md`). 429/503 pacing (90s, abort-after-2h → BLOCKED) was implemented per rule but never triggered. Full HTTP-error log: `build/gen_corpus_full.log`. No prereg amendment for transient-HTTP retry handling was obtained; flagged for coordinator/Micah ruling. |
| Raw captures | 40 (20 dump + 20 teach batches), sha256 per capture in `corpus/raw/SHA256SUMS.txt` |

## 3. Faithfulness inventory (teacher-supplied claims vs model reproductions)

| Class | n | ids |
|---|---|---|
| E_dump (dump ≠ supplied) | 7 (ids 88–94: grok miscounted word lengths in dump; e.g. "grammar"=7 supplied, dump said 8) |
| E_obs (obs ≠ supplied) | 0 |
| E_prb (probe ≠ supplied) | 0 |
| inconsistent (obs ≠ probe) | 0 |
| distract ≠ obs | 240/240 (by design) |
| Integer/text agreement | 240/240 dump, obs, distractor |
| False-id reproduction | 12/12 reproduced the supplied false value in dump/obs/probe (no flagging); distractor used the true value 11/12, other(22) once |

Full detail: `ERROR_INVENTORY.md`.

## 4. Track-5 composite (leg A, M2 arm, D2 teaching route)

Weights 30/25/25/10/10. N=5 byte-identical per command; 12 S1 reps + S10. All 12 reps byte-identical on composite.

| Metric | Mean (12 reps) |
|---|---|
| Mastery | 1.0000 (d1=40/40, d2≈38/38, d3=120/120 every rep) |
| Revisability (rf/12, rg/20) | 1.0000 (12/12 false revised, 20/20 genuine revised, every rep) |
| Integrity | 1.0000 (k1=k2=k3=1, hallu=0, refusal=1, esc=0) |
| Retention | 1.0000 (r2=40/40, r3=40/40) |
| Cost | 0.9113 (ops=287, eps=295 per rep) |
| **Composite** | **0.9911** |

| Gate | Result |
|---|---|
| Integrity gate (trap families 1,2,3,4,6,7,8 = 20/20; ctrl 2/2; hallu ≤ 1; k1=k2=k3=1; refusal=1) | PASS 12/12 |
| Corpus-replay cross-checks (withheld + d1, 24) | 24/24 PASS |
| S10 no-degradation | PASS (mastery 1.0000, revis 1.0000 at 10×) |
| D2 two-hop mean valid landmarks | 38.7 (of 40 sampled) |
| E_obs / E_prb / inconsistent / E_format (§7 analog) | 0 / 0 / 0 / 0 |

## 5. Class-4 §B.7 direct leg (leg B)

| Slice | Raw hits (/12) | Notes |
|---|---|---|
| 0–7 | 12/12 each | 96/96 total; bar ≥10/12 per slice → PASS |

| Check | Result |
|---|---|
| 5× byte-identical | PASS |
| Tripwire (no scaffold leakage) | PASS (0 fired, 0 leak; stim 72/72, manifest 12/12) |
| TEACH_DIGEST == leg C | PASS (`be5dba84…05d` both; also == muse-native box digest — same faithfully-reproduced values) |

## 6. Class-3 teacher leg (leg C)

| Check | Result |
|---|---|
| 5× byte-identical | PASS |
| 8/8 slices ≥10/12 flaw hits (flaw-first, tid=44) | PASS (12/12 each, 96/96) |
| Final mastery 192/192 | PASS |
| Teacher holds curriculum (blocked=0) | PASS |
| TEACH_DIGEST == leg B | PASS (`be5dba84…05d`) |

## 7. Determinism and no-RNG evidence

| Evidence | Result |
|---|---|
| Static no-RNG scan (37 .zag files) | PASS (no randomness sources; intrinsic inventory in `legs/build/NO_RNG_SCAN.md`) |
| N=5 byte-identical, leg B (direct §B.7) | PASS — `driver_B.log`: "ok: b7_direct (exit 0, 5x byte-identical)", GROKB_COMPLETE |
| N=5 byte-identical, leg C (teacher leg) | PASS — `driver_C.log`: "ok: teacher_leg (exit 0, 5x byte-identical)", GROKC_COMPLETE |
| N=5 byte-identical, leg A (every run command) | PASS — `driver_A.log`: "ALL LEG-A RUNS OK", 25/25 configs "exit 0, 5x byte-identical" |
| Zero RNG in learner paths | by construction (pure Zag, scan-verified) |

## 8. Verdict

**GROK ENGLISH CHAMPIONSHIP LEGS COMPLETE — class-4 composite 0.9911, §B.7 96/96
(direct and teacher-taught), class-3 teacher leg clean on all checks (96/96 flaw,
160/192 clean adopted, 192/192 final mastery, blocked=0); corpus frozen at
sha256 `7f3a2573…` with zero withholdings; TEACH_DIGEST identical across legs B/C
and the muse-native box.**

Head-to-head (grounded numbers only):

| Source | class-4 composite | §B.7 direct | class-3 (teacher leg) |
|---|---|---:|---|
| grok-4.6 (this box) | **0.9911** | 96/96, 8/8 | 96/96 flaw, 160/192 adopted, 192/192 mastery |
| gpt-5.6-sol (English) | 0.9911 | 96/96, 8/8 | clean (verdict: class-3 teacher leg clean) |
| muse-native (English) | 0.9911 | 96/96, 8/8 | 96/96 flaw, 160/192 adopted, 192/192 mastery |
| grok-4.6 (toy G-GROK) | 0.9911 | 96/96, 8/8 | composite 0.9959 |
| swe-1-6-slow (English) | 0.9033 / 0.8824 | 96/96, 8/8 | composite 0.9921 |

Three English boxes (grok, sol, muse-native) and the toy grok run converge on
class-4 composite **0.9911** to four decimals — the Track-5 battery is saturated
at this corpus scale; it no longer discriminates among faithful teachers.
swe trails on class-4 (≈0.90) and is banned as a future teacher regardless.

Faithfulness notes (grok-specific):
- E_dump=7 (ids 88–94): grok miscounted word lengths in the dump leg only
  (e.g. "grammar" supplied 7, dump said 8); the teach legs (obs/probe) are
  error-free (E_obs=0, E_prb=0, inconsistent=0).
- The 12 deliberate falsehoods were reproduced word-perfect in dump/obs/probe
  (no flagging, no correction) — grok is a faithful carrier, like sol.
- Curiosity: grok's DISTRACTOR leg "corrected" toward the true value 11/12
  times (other(22) once for id 71). The correction instinct lives in the
  distractor leg, never in the teaching legs — the learner never sees it.
- TEACH_DIGEST `be5dba84…05d` is byte-identical to the muse-native box's,
  confirming both boxes' teach sequences carry the same values.

No-RNG: static scan PASS (37 .zag files, intrinsic inventory in
`legs/build/NO_RNG_SCAN.md`); every leg command N=5 byte-identical
(drivers A/B/C all "ALL LEG-? RUNS OK"); pure Zag by construction.
