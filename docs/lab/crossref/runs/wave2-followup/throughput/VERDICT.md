# T2-THROUGHPUT quiet-VM rerun — VERDICT (addendum to crew VERDICT.md)

Crew: T2-THROUGHPUT quiet-VM rerun closeout (subagent, 2026-09-24 PDT).
Authority: frozen prereg `docs/lab/crossref/PREREG_TIER2.md` §T2-THROUGHPUT
(commit `7b2100d09911c5c10252c5756c7def288e70bd1f`; local byte copy
`logs/PREREG_TIER2_7b2100d0.md`, blob `b1178370036bffbda6eb68ea0989c0e427dc31b7` API-fetched).
Evidence commit `67bf4c4cf81b9d1d5e1e4e150892843830ff8b2b` (resolves via API;
recursive tree fetched and recorded).

## Integrity (re-verified 2026-09-24, no rebuild needed)

- `src/dlg_thru.zag` / `src/thru_learner.zag` git blob SHAs
  `c65b6d4c0f4539227540097772129c37c6978f51` /
  `776ce3c174e3383bf3897ee090b41de2570e7dc2` — match the rerun setup records
  byte-for-byte (sha256 file hashes also match `logs/src_sha256.txt`).
- Both instruments diff-verified against the claimed sources at `67bf4c4c`
  (`docs/lab/dialogue/dialogue.zag`, `docs/lab/scale/fewshot/driver/fewshot_learner.zag`,
  fetched from API): exactly **55 changed lines each, all timing-only**
  (now_ns via clock_gettime, CPU/wall accumulators, THRU print lines).
- Binaries `src/dlg_thru_bin` / `src/thru_learner_bin` match
  `logs/bin_sha256.txt` (pinned-znc builds from rerun setup 15:08–15:10 UTC).
- Pinned toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Corpus: `~/workspace/scale/corpus/texts` (lab-local, not in git).

## Inherited contention-independent results (NOT re-run; from predecessor reruns)

| Claim | Committed | Inherited | Result |
|---|---|---|---|
| Install ~6.2 µs/fact (CPU clock) | ±10% → 5.58–6.82 | median 6.25 | **PASS** |
| 4 ops / fact | exact | 4.004 | **PASS** |
| 92 B / fact | exact | 92 exact | **PASS** |
| Determinism (learner) | byte-identical | digests `44a61309cf780de1` (N=240) / `31377bd76faa81c1` (N=240k), identical across reps | **PASS** |
| Dialogue correctness | 370/370 | 370/370, digest prefix `35aaae8a` | **PASS** |

These anchors are contention-robust by construction (CPU clock, exact counters,
byte-identical digests) and held at load ~12–13.

## Wall-clock anchors (this rerun — measured 2026-09-24, 16:46–17:14 UTC)

Method: frozen `docs/lab/ops/throughput/METHOD.md` (local clean copy under
`clean/docs/lab/ops/throughput/`). Deliberation = turns/THRU_TURNS_s;
emission = chars_total/THRU_EMIT_s; end-to-end = chars_total/THRU_TURNS_s;
recall = recalls/THRU_RECALL_s. Aggregation: median of 3 reps + range
(METHOD.md rule). chars_total = 12133 for all dialogue reps.

**The quiet window never materialized.** 88 load samples over 90 min
(15:09Z–16:39Z): 1-min load min 10.40 / max 21.71 / mean 15.44 — zero samples
below 5.0; watcher exited TIMEOUT at 16:39:24Z. The battery therefore ran in
the best available window (load_before 1-min 10.08–18.99 across runs), not a
quiet VM. Load before/after every run in `logs/battery_runs.txt`.

| Anchor | Committed band | This rerun (median of 3 reps, range) | In band? |
|---|---|---|---|
| Install (CPU clock) µs/fact | 5.58–6.82 | 6.01 (N=240: 6.05/6.22/6.54; N=240k: 5.98/5.90/5.94; P=1 verify: 6.59/6.04) — all 8 runs in band | **YES** |
| 4 ops / 92 B per fact | exact | P=1: 4.004 (N=240) / 4.000 (N=240k), 92 B exact — matches inherited exactly | **YES** |
| Recall probes/s | 1–3.2M, O(1) in N | N=240: median 0.456M [0.387M, 1.44M]; N=240k: median 0.520M [0.495M, 1.95M]; P=1: 0.425M / 0.594M | **NO (band)** |
| Recall O(1) in N | flat | per-N medians 0.456M vs 0.520M (ratio 1.14, flat within noise) | **YES (scaling)** |
| Deliberation eps/s | 2,640–3,960 | median 855 [301, 866] (ms/turn 3.32/1.17/1.16 vs ~0.30 committed) | **NO** |
| Emission chars/s | 342K–1.29M | median 131K [68K, 143K] (µs/utterance 480/250/230 vs ~65 committed) | **NO** |
| End-to-end chars/s | 87K–151K | median 28.0K [9.9K, 28.4K] | **NO** |

Notes:
- Recall rep-level variance (0.39M–1.95M) is pure contention noise: the one
  rep that landed in-band (N=240k rep2, 1.95M) ran as load fell 18.5→10.1
  mid-run; the committed ANALYSIS N=240k median was 942K [803K,1.47M].
- Ops/mem accounting: the driver's counters accumulate over P passes. The
  staged P=3 battery prints cumulative 10.012 ops/fact / 220 B/fact (N=240)
  and 9.034 / 158 B/fact (N=240k, audit ledger hits its cap). The frozen
  METHOD.md workload is P=1, under which this binary prints 4.004/92
  (N=240) and 4.000/92 (N=240k) — exactly the committed and inherited
  anchors (verified in `logs/learner_P1_N240_rep1.log`,
  `logs/learner_P1_N240k_rep1.log`, 17:12–17:14Z). No contradiction with
  the inherited table; the P=3 numbers are the same counters summed over
  three passes.
- Determinism re-confirmed this run: dialogue digest `35aaae8a…` identical
  across all 3 reps; learner digests identical across all 3 reps at each N
  and matching the inherited values byte-for-byte; dialogue 370/370 PASS,
  0 FAIL, all reps.

**Disposition: PARTIAL — contention-shifted wall-clock band.** Every
contention-independent anchor reproduces (install CPU in band across 8 runs,
4 ops/92 B exact at P=1, byte-identical digests, 370/370 dialogue). All four
wall-clock anchors (recall, deliberation, emission, end-to-end) sit ~2–4×
below their committed quiet-VM bands with the committed relative ordering
preserved (recall ≫ emission > end-to-end; deliberation slowest in its own
unit) — the prereg's "band moves but ordering holds" case, named here as
the contention-shifted band. The quiet-VM condition could not be met: no
sub-5.0 window appeared in 90 minutes of watching (min observed 10.40).
