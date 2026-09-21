# VERDICT — Arm K1 (full SHA-256 identity), Track A closeout

**Date:** 2026-09-21
**Arm:** K1 — Full SHA-256 identity (IDENT family)
**Adjudicated by:** verdict gap-fill crew (Track A closeout)
**Verdict: PROVISIONAL** — kill (ii) unevaluable (chain-mode defect); kills (i) and (iii) do not fire

## Frozen kill criterion (verbatim, §3 of `units/PREREG_FREEZE.md`, extracted programmatically)

> Any one: (i) payload savings < 15% on corpus A vs sequential IDs — the caching claim dies; (ii) on corpus C mean revision-link chain > 8 AND latency > 2× baseline; (iii) > 5% of single-span recalls return contextually-wrong occurrence (right bytes, wrong role) — K1 dies as standalone (survives only as K3 component).

## Kill-criterion evaluation

### Kill (i) — payload savings < 15% on corpus A vs sequential IDs

Mode `k1-dedup-1x` (`work/runs/r1b/k1_dedup_a.txt`):

- prose: 963,478 spans, 71,167 unique → savings **87.2%**
- code: 1,223,384 spans, 130,817 unique → savings **73.3%**
- Bar: < 15% kills. 87.2% / 73.3% ≫ 15%. **Does NOT fire.**

### Kill (ii) — corpus C mean revision-link chain > 8 AND latency > 2× baseline

**UNEVALUABLE — measurement defect.** Mode `k1-chain-1x` (corpus C =
prose + 100 deterministic revision batches over every-1000th token;
reports mean chain length and stale-vs-clean recall latency) prints
`FATAL,k1-chain,recall` and returns before reporting — recall by the
occurrence's current digest fails inside the revision loop
(`cl/arm.zag:2056`). This crew re-ran the mode with the shipped binary
(`cl/k1test`) on the frozen r1 corpora: **same FATAL, deterministic**
(`work/runs/k1_chain_b.txt`). The defect is in the arm's measurement
code, not in the evidence pipeline — but with no chain-length or latency
numbers, criterion (ii) cannot be evaluated either way. It is a broken
measurement, not a kill.

### Kill (iii) — > 5% of single-span recalls contextually-wrong occurrence

Mode `k1-role-1x`: 400 distinct repeated words given a second,
role=taught occurrence; 800 role-tagged queries must each resolve to the
occurrence with the matching role and exact bytes. This crew ran the mode
with the shipped binary (it had never produced output):

```
K1ROLE,queries=800,wrong=0,role_blind_digests=400
```

- Contextually-wrong rate = **0.0%** (0/800). Bar: > 5% kills.
- **Does NOT fire.** (`work/runs/k1_role_b.txt`; metrics-v1 JSON inline.)

## What else was proven

- Builds: pure Zag, native binary `cl/k1test` (whitespace tokenizer,
  SHA-256 digest as u64[4], open-addressing table, append-only payload
  store, `OP_DEDUP_HIT`/`OP_REVISE_LINK` audit ops, occurrence records
  with role metadata; stores chunked — no slice over 2^25 bytes).
- `k1-selftest`: 9/9 pass. M1 prose: recall 100.0 / boundary 100.0,
  963,478 units, swap probe 100.0 (64/64).
- Determinism: zero RNG in decision paths; double runs byte-identical
  (dedup, m1, role all re-verified by this crew where runnable).

## Blocker (why PROVISIONAL, not PASS)

`k1-chain-1x` FATALs deterministically — mean revision-link chain length
and stale-vs-clean recall latency are unmeasured, so binding criterion
(ii) is unevaluable. Fix the chain mode's recall path (arm-crew work;
re-verify the battery after the fix), then re-adjudicate (ii)
mechanically: kill iff mean chain > 8 AND latency > 2× baseline.

## Evidence trail

- Source: `cl/arm.zag` (~2,470 lines); binary `cl/k1test`; spec
  `ARM_SPEC.md`; build log `BUILD_LOG.md`.
- Battery script: `work/run_battery.sh` (20 modes × 2; full battery was
  "in progress" per BUILD_LOG — never completed).
- Evidence: `work/runs/r1a/` (m1), `work/runs/r1b/` (dedup, chain),
  `work/runs/k1_chain_b.txt` + `work/runs/k1_role_b.txt` (this crew's
  re-runs, 2026-09-21).
- Scorecard (metrics-v1): `scorecard_r1_1x.json` (this verdict).

**Result: K1 PROVISIONAL — (i) and (iii) do not fire; (ii) blocked on
the chain-mode FATAL.**
