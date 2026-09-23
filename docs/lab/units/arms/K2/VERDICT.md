# VERDICT — K2 (64-bit FNV-1a Identity)

**Date:** 2026-09-21
**Arm:** K2 | **Scale:** 1× | **Round:** r1

## VERDICT: PASS

**No kill criterion fired.**

Quoting the binding criterion (brief K2.json):

> **Bidirectional:** if K2's dedup savings within 2 pts of K1's AND per-add
> cost lower → **K1 dies on cost grounds** (keep K2). If chain lengths exceed 4
> on any corpus run → K2 dies (64 bits too small for the store's lifetime).

- **Chain-length direction:** Maximum chain length across ALL corpus runs
  (M1 prose/code, M2 all tiers, M3, M4, M5, M6 both directions, M7,
  M8): **1**. True collisions: **0**. The kill bar (> 4) did not fire.
  K2 is not killed.
- **K1 direction:** UNDECIDABLE at this time. K1 has not reported dedup
  savings or per-add cost (K1 work/runs contains only M1 legs). The
  bidirectional comparison cannot be evaluated until K1 completes M7/M5.
  K2's numbers for the future comparison: M1 dedup savings prose 0.0% /
  code 0.3%; M7 dedup ratio 50.0% (rounds 1–2); per-add cost 153.7 bytes.

## 1× Scorecard (M1–M9)

| Metric | Result | Bar | Pass |
|---|---|---|---|
| M1 recall/boundary (prose, 84,731 u) | 100.0 / 100.0 | 100.0 | ✅ |
| M1 recall/boundary (code, 148,678 u) | 100.0 / 100.0 | 100.0 | ✅ |
| M1 A15 swap probe | 64/64 | — | PROVISIONAL-PENDING-FREEZE |
| M2 ETC (T1p/T1c/T2p/T2c/T3) | 1 / 1 / 1 / 1 / 1 | reported | ✅ |
| M2 episode-0 recall | 0.0% all tiers | ~0 (leak check) | ✅ |
| M3 survival / fresh recall | 100.0 / 100.0 | ≥ 90% | ✅ |
| M3 freeze verdict | CLEAR (700 windows; 50/50 weaken) | CLEAR | ✅ |
| M4 revision bnd/content (prose) | 100.0 / 100.0, kill 0% | ≥ 80% | ✅ |
| M4 revision bnd/content (code) | 100.0 / 100.0, kill 0% | ≥ 80% | ✅ |
| M5 per-byte memory | 2.42× | ≤ 1.5× | ❌ FAIL |
| M5 audit entries / KB | 16.2 | ≤ 10 | ❌ FAIL |
| M6 P→C rec/bnd/rev, tax | 100/100/100, tax 0 | 95/90/70 | ✅ |
| M6 C→P rec/bnd/rev, tax | 100/100/100, tax 0 | 95/90/70 | ✅ |
| M7 hit / reuse / dedup | 100.0 / 2.97 / 0.50 | 90 / 1.5 / 0.4 | ✅ |
| M8 determinism gate | PASS (10/10 byte-identical) | PASS | ✅ |
| M9 shape (T1 prose/code) | fast-then-flat | informational | — |

## 10× Status

**NOT ATTEMPTED — blocked.** Per the task rule ("Run 10× only if every 1×
bar passes"), the two M5 bar failures block the 10× leg. This is reported
as blocked, not as `ATTEMPTED — FAILED` (no 10× run was started).

## M5 Failure Analysis (honest)

K2's 2.42× memory overhead is inherent to the frozen design: the T64 dedup
table is 2× expected uniques (215,922 entries × 12 B = 2.6 MB) plus 9 slot
arrays × 107,961 (4.7 MB), against 5.4 MB of content. The 16.2 audit
entries/KB follow from one ledger entry per ADD by construction. These are
scorecard FAILs, not kill triggers — K2's kill criterion does not include
M5. The bars stand as frozen (M-24, M-25); K2 does not meet them at 1×.

## Chain-Length Evidence (kill-bar watch)

Every corpus run reported `K2CHAIN` with max_chain=1, collisions=0, except
the synthetic `t-collision` test which honestly exercised the chain path:
3 forced same-ID contents → chain 3, 2 collisions counted, insertion order
preserved, head resolution correct. No run exceeded chain length 1 on real
data; the kill bar (> 4) never approached.

## Ambiguities and Provisional Items

1. **A15 swap probe:** Implemented literally per the proposal (deterministic
   N=64 ID→content remappings; remapped content returned honestly).
   Cell marked `PROVISIONAL-PENDING-FREEZE` — the schedule was proposed,
   not frozen.
2. **A7/A8 (M7):** The C′ edit bytes (first-byte XOR 0xFF) and the
   `(l*37)%n` lookup schedule follow the harness validator's conventions,
   implemented literally and flagged — not frozen.
3. **True-collision chain search:** `ingest_with_id` byte-compares only the
   first same-ID table entry. With zero true collisions on real corpora
   this does not affect results; full chain-walk dedup is future work.
4. **M5 "unit learned" counting:** L = byte-exact M1 recall at trial end
   (84,731/84,731). The 1,000-step mini-pressure is the M5 trial's own
   500-ingest/500-kill sequence per the frozen M-22 definition.

## Coordinator Corrections Acknowledged

1. **First correction:** The initial semantic-ID implementation was void.
   It was deleted and replaced with the literal K2 specification (FNV-1a-64
   identity). The void mechanism is not reported as a result.
2. **Second correction:** Spec authority is the brief + the byte-verified
   frozen K2 row only. No other coordinator material was used as spec.
   The final report does not present the void mechanism or its criterion.

## Artifacts

- `ARM_SPEC.md`, `BUILD_LOG.md` (this directory)
- `scorecard_1x.json` (metrics-v1 row)
- Raw logs: `~/workspace/tnn-lab/units/arms/K2/work/smoke/*.txt`
- M8 artifacts: `~/workspace/tnn-lab/units/arms/K2/work/m8/run_*/`
- Source: `~/workspace/tnn-lab/units/arms/K2/cl/arm.zag`
