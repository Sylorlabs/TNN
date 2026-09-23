# TRIAL_RESULTS_WB3 — Selective audit at scale (2026-09-19, native Zag)

Protocol: PREREG_WB3.md (plus amendment A1 below). Evidence:
`trial/EVIDENCE_20260919T*/run.stdout` (2469 CL_CHECK lines, all
actual==expected; `WB_FAILURES,0`; binary exit 0).

## Outcome: PASS on all preregistered gates

| Gate (prereg falsification criterion) | Result |
|---|---|
| Replay == live state at 1x (64 slots) and 10x (640 slots) | PASS (`WB_REPLAY,rc=0` both scales) |
| T1 digest tamper detected | PASS (replay rc=2, digest mismatch) |
| T2 out-of-band state mutation detected | PASS (replay rc=1, divergence) |
| T3 ledger overflow fail-closed, no drops | PASS (rc=107 `WB_REFUSED_AUDITFULL`, `audit_n` pinned at 16, replay still rc=0, state intact) |
| No illegal op succeeds (SUMMARY on CORE/pinned, FLUSH on empty batch, ops at stage < required) | PASS (109/109/110/105 all refused, state untouched) |
| Two deterministic runs byte-identical | PASS (`deterministic_ledger` checksum equal) |
| Manifest re-derivation == cache | PASS (`live_cfg == rederived_cfg` both scales) |
| Per-op ledger bytes constant across 1x/10x (linearity) | PASS (marginal: `(bytes2-bytes1)*26 == (ops2-ops1)*952` exactly) |
| Refusals never mutate state | PASS (global, both scales) |

## Measured numbers

- 1x: `audit_n=126` full entries (40 B), `sum_n=41` compact records (24 B),
  6 batches, 6 refusals; coverage `r0full=1 r0sum=0 r1full=62 r1sum=41`.
- 10x: `audit_n=981`, `sum_n=401`, 51 batches, 6 refusals;
  coverage `r0full=1 r0sum=0 r1full=512 r1sum=401`.
- Marginal ledger cost per churn op: **952 B / 26 ops = 36.6 B/op,
  identical at both scales** (exact integer equality, no rounding).
- The single `r0full=1` is the CORE-slot ADD; zero summary records touch
  region 0 — the structural floors held under churn.

## Honest record: what the first run caught (not silently rerun)

The first run failed 9/2469 checks. All three causes were implementation
bugs against the prereg's stated invariants, found by the trial's own
assertions — this is the machinery working as designed:

1. **Manifest digest ordering.** Replay verified the MANIFEST entry's
   config digest *before* applying the entry's policy update, but the
   digest covers the post-update policy. Fix: apply then verify.
2. **KILL reset broke the level fold.** KILL reset the slot's region and
   audit level (MA1 parity), which (a) misattributed USER-slot KILLs to
   region 0 in coverage, and (b) made the main-ledger-only level fold
   diverge from live state (compact KILL records are invisible to it).
   Fix (design refinement, recorded as prereg amendment A1): **KILL
   preserves region and audit level** — the dead slot stays attributable
   and keeps its visibility budget until reallocated. Attribution beats
   canonical zeroing.
3. **Naive scale cross-multiplication.** The fixed setup/ending cost is
   amortized over 5 blocks at 1x vs 50 at 10x, so average bytes/op
   differs. Fix: assert linearity on the **margin**
   (`dbytes*26 == dops*952`), which is the actual scaling claim.

## What this does NOT show (prereg §What it does NOT show, unchanged)

Judgment quality of audit-level choices (protocol-fixed); whether
batch-granular rollback is acceptable policy in general; 100x scale
(WB3-SCALE-100x named next); real deployment; multi-region serving.
The digest is a deterministic tamper-evidence mixer, not a cryptographic
commitment — the threat model is accidental/bypass detection, and
malicious same-user mutation resistance is explicitly not claimed
(cf. ZAG_PLAYBOOK.md §9).
