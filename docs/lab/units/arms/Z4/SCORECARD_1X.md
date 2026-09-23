# Z4 1x Scorecard (Z4-local, r1)

**Arm:** Z4 — Dialect (per-interlocutor) IDs
**Scale:** 1x, round r1
**Date:** 2026-09-21
**Battery:** 16/18 legs passed (m3-1x, m8 FAILED — implementation panic, see below)

## M1 — Ingest + recall + ID-swap probe (PROVISIONAL-PENDING-FREEZE per A15)

| corpus | recall | boundary | units | ID probe |
|--------|--------|----------|-------|----------|
| prose  | 100.0% | 99.9%    | 84731 | PASS |
| code   | 100.0% | 99.6%    | 148678| PASS |

Boundary misses are honest content-dedup artifacts (A22): prose has 1 duplicated
64-byte block, code has 589. One content ID records the last-ingested span.
**Verdict: PASS** (bars: recall ≥99.5%, boundary ≥95%).

## M2 — Tiered convergence + M9 probe

| tier | corpus | ETC | censored | final recall | final boundary |
|------|--------|-----|----------|--------------|----------------|
| t1   | prose  | 1   | no       | 100.0%       | 100.0% |
| t1   | code   | 1   | no       | 100.0%       | 99.7%  |
| t2   | prose  | 1   | no       | 100.0%       | 99.9%  |
| t2   | code   | 1   | no       | 100.0%       | 99.8%  |
| t3   | synth  | 50+ | yes      | 100.0%       | 54.6%  |

M9 (t1 legs): shape=fast-then-flat, takeoff_ep=1, steepness=100.0, late_gain=0.0.
**Verdict: PASS.**

## M3 — Pressure / retention

**FAILED** — implementation panic ("slice index out of bounds") during phase-1
S3 ingests. Root cause not isolated. Does not affect the binding kill verdict.
See DEATH_CERTIFICATE.md.

## M4 — Defect revision

| corpus | rev_boundary | rev_content | kill_rate | killsub |
|--------|--------------|-------------|-----------|---------|
| prose  | 100.0%       | 100.0%      | 0.0%      | false   |
| code   | 100.0%       | 100.0%      | 0.0%      | false   |

**Verdict: PASS.**

## M5 — Resource accounting

- units_learned: 84731, source_bytes: 5422721
- slot_table_bytes: 7387692, ledger_bytes: 5486784 (85731 entries)
- corpus_buffer_bytes: 5422721
- Note: shared assembler applies B-64-specific bars (1.5x memory, 10/kb audit)
  which are not Z4 bars. Z4 reports raw costs; no Z4-specific M5 bar was frozen.
**Verdict: PASS (raw costs reported; no frozen Z4 bar).**

## M6 — Transfer (p2c + c2p)

| dir | recall | boundary | revision | tax  | dup  | translate_hits | common_minted |
|-----|--------|----------|----------|------|------|----------------|---------------|
| p2c | 100.0% | 99.6%    | 100.0%   | 0.1% | 0.0% | 0              | 0             |
| c2p | 100.0% | 99.9%    | 100.0%   | 0.0% | 0.0% | 0              | 0             |

Memorizer control: p2c in-domain 82.2% → transfer 27.4% (drop 54.8%);
c2p in-domain 27.4% → transfer 82.2% (drop -54.8%). Validity gate: PASS.
Duplication 0.0% on both legs → binding kill disjunct 2 does NOT fire.
**Verdict: PASS.**

## M7 — ID dedup / C′ edit (PROVISIONAL per A18)

- hit_rate: 100.0% (5000/5000 lookups)
- reuse_rate: 3.0 (tenths; = refs*10/distinct, see ARM_SPEC)
- dedup_savings_bytes: 10791170
- dedup_ratio: 66.3%
- reread_bytes: 319937, units: 84731, distinct_live: 85578
- na_reason: null
**Verdict: PASS.**

## M8 — Determinism gate

**FAILED** — M8 gate did not pass: the m8-1x "clean" run exits non-zero due to
the same implementation panic as M3 (the M8 instance includes the M3 sequence).
No byte-divergence was observed (all 16 passing legs are byte-identical across
reruns); the failure is a crash, not non-determinism. Per the task spec, M8
DISQUALIFICATION applies to differing bytes; a crash is reported as FAILED.

## M9 — Learning curve shape

See M2 table above. Shape: fast-then-flat on t1 legs.
**Verdict: PASS.**

## Binding kill assessment (frozen §3 row)

> "Per-speaker lexicons do not converge ≥30% faster than a shared lexicon —
> namespacing buys nothing; OR >40% of chunks duplicated across namespaces
> (no real divergence — overhead without content). Conditional on Phase 4 working."

- **Disjunct 1 (convergence): FIRED.** zconv-1x (byte-identical reruns):
  ETC_S1=1, ETC_S2=2 (namespaced avg 1.5); ETC_sh_S1=1, ETC_sh_S2=2 (shared avg 1.5);
  speedup = 0% < 30%.
- **Disjunct 2 (duplication): NOT fired.** M6 dup = 0.0% on both legs (< 40%).
- Phase 4 conditional: treated as satisfied via explicit speaker tags (A19).

**Overall: KILLED by disjunct 1.**
