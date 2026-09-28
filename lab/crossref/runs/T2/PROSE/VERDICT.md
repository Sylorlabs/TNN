# T2-PROSE replication — VERDICT: **REPRODUCED**

**Crew:** T2-PROSE (REPLACEMENT — predecessor killed by daemon restart; empty
inherited state, re-cloned). **Date:** 2026-09-22 PDT. **Type:** A (full rerun).

## Frozen claims checklist (quoted verbatim from `PREREG_TIER2.md` §T2-PROSE,
frozen commit `7b2100d09911c5c10252c5756c7def288e70bd1f`)

> **Claims:** commit `d4c151c7e39c`: all four sources trip the ≥0.98 viability
> bar — sol 220/228 (0.9649, −3.5pp), step 0.8947 (−10.5pp), muse-native 0.8772
> (−12.3pp), grok-4.6 0.8289 (−17.1pp); extraction 240/240 perfect; cause =
> retrieval ties, not extraction; Q=+0.0022 → frozen NO-DIFFERENTIATION; fluent
> lies install 12/12 in prose. Honest scope: bag-of-stemmed-words retrieval.
> **Grok-4.7 rerun:** commit `fbecf64f08b6f5f41efbf33ef07384154cd48140`: on
> frozen prose bars, 4.7 yields Q=+0.0548 → mechanically QUALITY-MATTERS
> (boundary result at +0.05 band edge); prose viability still fails 0.9342 vs
> 0.98; both teachers absorb all 12 falsehoods; direct head-to-head clean
> mastery gain +10.5pp. Five live-4.7 items remain blocked — excluded.
> **Method:** rerun the four-source prose battery on committed corpora (clean
> checkout, ≥3 byte-identical); re-derive the Q statistic for 4.6 and for the
> committed 4.7 corpus with independent Zag code.
> **Rule:** REPRODUCED if all four viability figures match and
> Q(4.6)≈+0.0022/NO-DIFFERENTIATION while Q(4.7)≈+0.0548/QUALITY-MATTERS;
> NOT REPRODUCED if the quality verdict flips for either model.

## What was done

- Clean checkout of `sylorlabs/TNN` at frozen `7b2100d09911c5c10252c5756c7def288e70bd1f`
  (sparse, SHA-verified blobs; see RUNLOG for fetch-method note).
- Pins frozen before running: battery `d4c151c7e39c73c8f05b42697cd8fdc81466c025`
  ✓, grok-4.7 rerun `fbecf64f08b6f5f41efbf33ef07384154cd48140` ✓ (both confirmed
  via GitHub API: messages/dates match the prereg).
- Rebuilt `src/prose_learn.zag` from pinned source with pinned znc
  (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`); source
  sha256 `88e91670e2549e76a48a22252cbb6691a6f0407cf1749ba9dcf272f14a68057a`.
- Ran the battery on committed `inputs/` (240 train / 240 test / 12 false_ids
  per source, line counts verified): **5 sources × 5 reps = 25 runs**,
  CWD = clean checkout (learner performs no file writes; checkout pristine).
- Re-derived Q with **independently written** Zag program `q_derive.zag`
  (parses my run logs' SUMMARY lines, exact-fraction arithmetic, ±0.05 band
  rule applied in-code); 3/3 byte-identical outputs.

## Results — every figure vs committed

| Source | Claim (clean) | Measured clean | Claim (full) | Measured full | Extract | Absorb | 5/5 identical |
|---|---|---|---|---|---|---|---|
| grok-4.6 | 189/228 (0.8289, −17.1pp) | **189/228** ✓ | 197/240 | **197/240** ✓ | 240/240 ✓ | 12/12 ✓ | yes ✓ |
| gpt-5.6-sol | 220/228 (0.9649, −3.5pp) | **220/228** ✓ | 231/240 | **231/240** ✓ | 240/240 ✓ | 12/12 ✓ | yes ✓ |
| step-3.7-flash | 204/228 (0.8947, −10.5pp) | **204/228** ✓ | 214/240 | **214/240** ✓ | 240/240 ✓ | 12/12 ✓ | yes ✓ |
| muse-native | 200/228 (0.8772, −12.3pp) | **200/228** ✓ | 211/240 | **211/240** ✓ | 240/240 ✓ | 12/12 ✓ | yes ✓ |
| grok-4.7 | 213/228 (0.9342) | **213/228** ✓ | 223/240 | **223/240** ✓ | 240/240 ✓ | 12/12 ✓ | yes ✓ |

Strongest check: **all 25 of my run logs are byte-identical to the 25 committed
run logs** (`runs/<s>_rep<r>.log`) — DIGEST, DIGEST2, and LEDGER terminal hashes
match exactly per source/rep.

| Claim | Measured (independent Zag) | Match |
|---|---|---|
| All four sources trip ≥0.98 viability | TRIP on grok/sol/step/muse-native (0.8289/0.9649/0.8947/0.8772 all < 0.98) | ✓ |
| −pp vs integer baseline 1.0 | −17.1 / −3.5 / −10.5 / −12.3 pp (exact: 39,8,24,28 / 228) | ✓ |
| Cause = retrieval ties, not extraction | extraction 240/240 everywhere; tied probes (ties≥2): grok 106 (35 tied&wrong), sol 54 (9), step 43 (23), muse-native 12 (10) — exactly the committed tie table; grok47 73 (14) | ✓ |
| Q(4.6)=+0.0022 → NO-DIFFERENTIATION | Q = 1/456 = **0.002192** → **NO-DIFFERENTIATION** (\|Q\|<0.05) | ✓ |
| Q(4.7)=+0.0548 → QUALITY-MATTERS (boundary) | Q = 25/456 = **0.054824** → **QUALITY-MATTERS** (≥+0.05) | ✓ |
| 4.7 prose viability still fails (0.9342 vs 0.98) | 213/228 = 0.9342 < 0.98 → TRIP | ✓ |
| Both teachers absorb all 12 falsehoods | grok absorb=12/12, grok47 absorb=12/12 | ✓ |
| Head-to-head clean mastery gain +10.5pp | (213−189)/228 = **10.52pp** | ✓ |
| Five live-4.7 items blocked — excluded | committed grok47 inputs are 240/240/12 lines; exclusion sits upstream in the Leg C capture (builder asserts exactly 240 dump + 240 teach from the captured corpus); battery ran on the committed 240-item corpus with extract=240/240 | ✓ (lineage, not recomputable from battery inputs) |

Q-band note: the frozen ±0.05 three-bin rule (doc-sweep correction of the
prereg's ±0.02) was applied. Both Q values keep their verdicts under either
band (0.0022 < 0.02; 0.0548 ≥ 0.02), so the correction does not affect the
replication outcome. Q(4.7) remains a boundary result: 0.0548 vs the +0.05 edge.

## Verdict

**REPRODUCED.** All four viability figures match exactly; Q(4.6)≈+0.0022 /
NO-DIFFERENTIATION and Q(4.7)≈+0.0548 / QUALITY-MATTERS both re-derived with
independent Zag code from an independent rebuild; neither quality verdict
flips. No divergence of any kind was found — the replication is exact down to
byte-identical run logs, digests, and ledger terminal hashes.

## Caveats / notes for the parent

1. The "five blocked live-4.7 items" is upstream Leg C capture lineage
   (delisted-model capture), not visible in the battery inputs; the battery-level
   check is that the committed 4.7 corpus is complete (240/240/12) and yields
   extract=240/240 — both hold.
2. Fetch transport deviated from a literal `git clone` (VM OOM under concurrent
   crew load); blobs are the pinned commit's, SHA-verified — documented in
   RUNLOG. No source substitution.
3. Original `test_grok.jsonl` checksum amendment (VERDICT.md integrity note,
   needs Micah's signature) is untouched by this replication — the battery runs
   on the committed `.txt` conversions, which reproduce the committed logs
   byte-for-byte.
4. Artifacts: `crew/logs/` (25 run logs), `crew/build/prose_learn`,
   `crew/build/q_derive`, `crew/build/q_derive.zag`, this VERDICT.md,
   `crew/RUNLOG.md`. Nothing committed to any branch (no commit requested).
