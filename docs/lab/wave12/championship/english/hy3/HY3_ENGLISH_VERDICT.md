# HY3 ENGLISH — championship source-team verdict: **BLOCKED (model unavailable)**

Model: `hy3:free` via UnoRouter (opportunistic classes 3+4 leg).
Date: 2026-09-21. Corpus: frozen `championship-english/corpus-input` (40 prompts,
set hash `ac5d7d3155f9a90dc60f4f3ec529a3c6125a0469ce5862c7193fb261441b8b7d`).

## Probe outcome: BLOCKED

| Item | Value |
|---|---|
| Probe start | 2026-09-21T21:44:30Z |
| Deadline / end | 2026-09-21T22:45:00Z (41st attempt would have exceeded the ~1h policy window) |
| Total attempts | 41 (attempt 1 at 21:44:30Z, then every ~90s) |
| Interval | 90 seconds |
| Every attempt | HTTP 503 `get_channel_failed` — "All providers for model `hy3:free` are busy right now (they hit their rate limit). This is not a spelling error." |
| Successful responses | 0 |
| Corpus captured | **none** |

Per the frozen availability policy, retrying stops at the deadline. No corpus
was captured, so no learner legs ran, no corpus SHA256 exists, and there is
no faithfulness or class-3/4 evidence for `hy3:free`.

## What was built (model-independent, complete, compile-verified)

Everything below is real, prepared infrastructure — **calibration/smoke only**,
not headline evidence, and **no substitute for the missing corpus**.

All leg sources are ported from the frozen muse-native trial, compile clean
with `znc_linux_x86_64_abed8aa1`, and run to completion on a stub corpus
(values wrong by construction; control flow verified):

- `tnn/build_gen.py` — verifies `corpus.json` vs `SHA256.txt` (FATAL on
  mismatch), emits `hy3_corpus.zag` accessors (if/else integer chains, no
  heap), and the English domain block (`t5_cat`/`t5_truth`/`t5_plant_claim`,
  4 categories, 12 false ids) parsed from the frozen `ground_truth_notes.md`
  and mechanically verified (alpha-pos/word-len derivations recomputed;
  the 12 false-id TRUE values match the prereg list exactly).
- `tnn/assemble_legs.py` — mechanical port with explicit transforms:
  teacher ids 20/21 → 55/45 (direct/taught-teacher), `TbSess.last55/last45`,
  flat dispatch (ZNC-2026-09-21-013), 4-category geometry (bases 0/48/96/144),
  `q2_false_val = truth+1`, D2 battery as two-hop word-len→alpha-pos
  inference (structural analog of the Zharovia landmark→ruler chain;
  38/48 word-len ids battery-valid pre-heldout), §B.7 flaw battery VERBATIM
  (value-agnostic).
- `tnn/legA/analysis/analyze_hy3_m2.py` — Track-5 metrics, 30/25/25/10/10.
- `tnn/norng_scan_hy3.py` — static no-RNG scan (passes modulo the
  not-yet-generated `hy3_corpus.zag`).
- `run_hy3.sh` — compile + N=5 byte-identical runs per leg.

## English-class deltas (documented, frozen)

- Categories: 0=alpha-pos (0–47), 1=word-len (48–95), 2=pub-year (96–143),
  3=count-fact (144–239). Per-category disconnects: 4.
- `t5_truth` = real-world TRUE value (228 = supplied; 12 false-id overrides:
  3→4, 29→4, 55→8, 71→20, 80→9, 103→1678, 117→1850, 139→1895, 163→3,
  178→9, 205→37, 231→8).
- `t5_plant_claim` = trainer's SUPPLIED value (authoritative for the model).
- Teacher 45 / direct probe 55. §B.7 battery unchanged (value-agnostic).

## Explicitly NOT done (blocked — would be fabrication to claim otherwise)

- No corpus capture (`gen_corpus_hy3.py` was never run; `corpus/raw/` does not exist).
- No real `hy3_corpus.zag`; no real leg A/B/C runs; no N=5 byte-identical executions.
- No `faithfulness_inventory.py` output (E_dump/E_obs/E_prb, disagreement counts,
  the 12 false-ID reproduce-vs-correct classification).
- No static no-RNG scan re-run with real corpus imports.
- No `analyze_hy3_m2.py` results; no Track-5 weights; no §B.7 results.
- No corpus SHA256 (nothing was captured to hash).
- The English D2 two-hop adaptation (word-len → alpha-pos) remains documented
  and stub smoke-tested but unverified against any authoritative English
  championship document; it is **not** prereg authority.

## Verdict

**BLOCKED** — the infrastructure is ready and standing by; the model was never
reachable. If `hy3:free` becomes available, the path is: run `gen_corpus_hy3.py`,
run `build_gen.py`, re-run the no-RNG scan with corpus imports present, run the
three legs N=5 byte-identical, then `analyze_hy3_m2.py` and the faithfulness
inventory, and finally fill in the verdict tables above. Nothing further was
attempted after the deadline.

Probe log: `probe.log` (41 attempts, all 503).
