# VERDICT — W13 EPISTEMIC LEASE PAM (WILD-B, generation 3)

**Status: HOLD** (prereg-sanctioned HOLD, not KILL — KB-W13-LIVE and the
K3-analog both miss; redesign the snapshot/active interaction, do not kill
the paradigm).

**Date:** 2026-09-24. **Frozen prereg:** `pam/round4/wild/prereg/PREREG_W13.md`.
**Instrument:** `pam/round4/wild/w13/w13_lease.zag` (pure Zag, zero RNG,
`[]u8` arenas + LE accessors, logical time only).
**Scorer:** `pam/round4/wild/w13/score_w13.py` (independent: full existential
corroboration recomputation via tag index, not the instrument's partner
pointer; re-derives staleness, eligibility, bars, diagnostics).

## Battery numbers (2026-09-24, 2× byte-identical)

- stdout SHA-256 (both runs):
  `e5c3ef148ab83c63d75441cf60c06e15a1298502e6a3218ea1771e07c8a6451b`
- 10,050 grants (10,000 G + 50 F); 10,050 checks; 10,050 per-lease finals.
- **K1:** 0/50 false leases renewed; 0/50 active past first `expires_at`.
  False lifetimes: granted g → expires g+10 → checked g+10, never extended.
  **PASS.**
- **K6 (F-K1):** every false-lease renewal check staleness ≤ 3 (max false
  staleness = 0 — all 50 false checks land on steps ≡ 0 mod 3; max over all
  checks = 2). **PASS.**
- **LIVE (F3):** genuine renewed 6650/10000 = **66.50%** (< 90% bar).
  **HOLD** (prereg: "else HOLD — redesign, not kill").
- **K3-analog:** genuine influence rate 6650/10000 = **66.50%** (< 66.78%
  frozen M1 bar). **HOLD** ("not expected" — it happened).
- **K4:** max per-step scan work 1 ≤ SCAN_BUDGET 64; table 10050 ≤ 16384.
  **PASS.**
- **K5:** terminates, t_end = 10060, all leases checked exactly once.
  **PASS.**
- **K2:** 2× stdout byte-identical. **PASS.**
- Independent scorer recomputed all 10,050 renewal decisions from the log +
  stream: **0 mismatches** vs the instrument.

## Diagnostics

- **D-W13-1** staleness histogram (all checks): {0: 3350, 1: 3350, 2: 3350} —
  perfectly uniform; bound ≤ 3 holds by construction and is verified.
- **D-W13-2** scanner backlog: max(due − checked) = **0** over all steps
  (no backlog; ~1 due/step, budget 64 never stressed).
- **D-W13-3** false lifetimes: e.g. lid 10000: granted 200 → expires 210 →
  checked 210; lid 10049: 10049 → 10059 → 10059. All 50 inert at first expiry.

## Why 66.50%: the snapshot-lag mechanism (not a bug)

The shortfall is structural in the frozen mechanism, verified by analysis +
two sensitivity probes:

1. Even genuine leases (2k, granted p): partner 2k+1 not yet due at check
   time → snapshot always shows it active → **5000/5000 renew**.
2. Odd genuine leases (2k+1, due p+11): renewal needs partner 2k ACTIVE per
   the **snapshot**. 2k renews at p+10, but the snapshot (refreshed every 3
   steps, before the step's scan) shows the renewal only if a refresh landed
   in (p+10, p+11] — a 1-step window against a 3-step refresh → **1/3 renew**
   (1650/5000; exactly the p0%3==1 class).
3. Total ≈ (1 + 1/3)/2 = 2/3 ≈ 66.7% (measured 66.50%; edge + p0%3
   distribution effects). The 3-step snapshot lag **structurally caps**
   genuine renewal at ~2/3 because corroboration requires *observing* the
   partner's renewal through a stale snapshot.

Probes (Python model of the frozen mechanism):
- Refresh-after-scan instead of before: **same 6650 total**, different
  1650 leases (p0%3==2 class instead of p0%3==1). The 2/3 cap is
  phase-independent — robust, not an implementation artifact.
- Literal asymmetric window `[granted_at, granted_at+3]`: 5000/10000 = 50%.
  (Not used — see prereg-ambiguity note.)

## Prereg-ambiguity resolutions (documented, frozen text unchanged)

1. **Corroboration window symmetric (|Δgranted| ≤ 3), not literal
   `[granted_at, granted_at+3]`.** The literal text would leave every odd
   genuine lease with NO possible corroborator, contradicting the frozen
   fixture comment ("corroboration exists within 3 steps for **every**
   genuine lease"), the "(independent corroboration within 3 steps)"
   parenthetical, and F3's own ≥90% prediction. Symmetric is the only
   reading consistent with the frozen fixtures.
2. **Snapshot refresh before the step's scan** ("snapshots the ledger at
   scan start"). The after-scan variant was probed: identical totals.
3. **ACTIVE evaluated against the snapshot** (literal "every renewal check
   is evaluated against the current snapshot"): active ⟺
   granted ≤ check_time < snapshot_expires_at. This is what costs the
   1/3 of odd leases.
4. M1 gate for genuine grants uses (705, 3588) — matching `gen_lease.py`'s
   `passes_m1` (the prereg's "(705,3588,1,1)" is loose notation for the
   frozen (0,0) optimum; the 910-count is the (0,0) true-pass).

## What HOLD means here / redesign direction

The lease paradigm's safety claims (K1 containment, K6 freshness) **pass**.
What fails is liveness: the frozen snapshot discipline starves ~1/3 of
genuine leases of renewal because the ACTIVE test demands the snapshot
reflect the partner's renewal, which a 3-step-lagged snapshot misses 2/3
of the time. Redesign candidates (for the parent, not this verdict):
evaluate the ACTIVE test against fresher state than the grant-snapshot, or
decouple "active" from observed-renewal (e.g. active ⟺ within
granted_at + duration unless expiry observed). The DURATION mechanism
itself (bounded influence window) is load-bearing and works — 0/50 falses
persist past it.

## Standing-law cap classification (2026-09-24 law)

- **Load-bearing mechanisms:** bounded lease duration (damage window must
  exist); snapshot refresh (freshness bound must exist); scan budget
  (per-step work bound); corroboration window (independence must be
  time-bounded); one-time renewal check (termination).
- **Values are calibration / arbitrary-flagged:** 10 / 10 / 3 / 64 / 3.
  Capacity 16384 arbitrary and flagged (10050 used; no pressure on it).
  The 66.50% shortfall is caused by the *interaction* of the lag-3 and
  window-3 values, not by any single value alone.

## Commits

- Evidence/source: `7bf0924fc22b52c34813734d384ff1a748cd8f32`
- Verdict (this file): *committed separately per protocol*

## Paths

- `pam/round4/wild/w13/w13_lease.zag`
- `pam/round4/wild/w13/score_w13.py`
- `pam/round4/wild/w13/evidence/w13_stdout_run1.txt`
- `pam/round4/wild/w13/evidence/w13_run_hashes.txt`
- `pam/round4/wild/w13/evidence/w13_score.txt`
- Frozen stream: `pam/round4/wild/w13/w13_stream.txt`
  (generator `pam/round4/wild/w13/gen_lease.py`)

## Cross-design notes

- W13's K1-passing containment (0 false renewals via unique tags) is the
  lease-paradigm analog of W11's chain-of-custody allowlist: both bound
  influence by *provenance*, but W13 bounds it *temporally*.
- The 66.50% influence rate just misses the frozen M1 bar (66.78%) that W4
  (39.29% correct admits, 0 wrong) and W12 (82.58%) were measured against —
  W13's liveness failure is a mechanism-interaction finding, not a
  threshold-tuning issue.
