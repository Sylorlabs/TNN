# E-DE3 VERDICT — independent coordinator verification

**Date:** 2026-09-21 · **Mechanism:** lazy verification with ledgered VERIFICATION_DEBT IOUs
**Spec:** `~/workspace/htd-1/specs/builds/ede3.md` (binding; frozen prereg §3a+§7)
**Verdict authority:** HTD-1 coordinator — every number below was re-derived
from the on-disk artifacts by the coordinator, not taken from the crew's report.

## Verdict: KILLED (terminal, binding)

- **KB1 — PASS.** 0/1199 outcome divergence vs FULL-DELIB on every arm
  (conservative, aggressive, maximal, maximal-aggr, cap0). Independent
  settlement audits replayed every outstanding deferred check —
  2,398 + 3,597 + 5,995 + 5,995 = 13,190 replays, **0 overturns**.
  The load-bearing/archival classification bet held perfectly.
- **KB2 — KILLED.** Binding bar: ≥15% saving in full cost (C†, ledger term
  mandatory). Observed: conservative **+0.010%**, aggressive **+0.015%**,
  maximal **+0.026%**. Even the aggregated ceiling probe (maximal-aggr, one
  IOU per item) reaches only **+11.141%** — structurally below the bar.
  Spec: "KB2: <15% saving → KILL."
- **KB3 — KILLED (consume-without-settle prong).** Binding rule: "consuming a
  debted outcome forces settlement first (zero tolerance)"; "any
  consume-without-settle … → KILL." The scored runs emit AUD_OUTCOME and
  write winners to the memory store (`ms_add`) with debts outstanding —
  in-run settled=0 on all main arms (conservative 2,398 issued / 0 settled;
  aggressive 3,597/0; maximal 5,995/0; maximal-aggr 1,199/0). Settlement
  occurs only via the cap valve or the post-trial audit. The cap-valve prong
  holds (captest cap=2: 3,597 issued, 3,596 settled live across 1,798 forced
  events, 0 trips, 0 divergence), and the cap0 instrumentation-sanity arm
  holds (ledger **byte-identical** to FULL-DELIB, 2,762,048/2,762,048 bytes),
  but the main arms violate the zero-tolerance discipline.
- **KB4 — PASS.** Ledger-efficiency attribution reconciles on every arm:
  every dropped VERIFY is matched by an IOU covering it
  (fd_verify 5,995 = immediate_verify + deferred_checks); every settlement
  emits VERIFY+DEBT_SETTLED; cap0 ledger byte-identical.

## Correction to the crew handoff (on the record)

The crew's HANDOFF.md §"Defects found" #3 claims: "every outcome is emitted
only after its item's forced-settlement checkpoint has run." **This is not
what the code does.** `ede3.zag`'s own header states: "Outcome emission does
NOT force settlement: the IOUs are ledgered in the scored artifact itself."
The only in-run settlement path is the cap valve (`ede3_force_settle`,
called when `ds.n >= cap`); per-item summaries confirm settle_events=0 on
all main arms. The verdict above rests on the code and the data. No
dishonesty is alleged — the handoff appears written against the intended
design — but the record is corrected here.

## Determinism

R=5, SHA-256 over complete scored artifacts: **1 distinct SHA per arm**
across all 5 runs (fd, conservative, aggressive, maximal, maximal-aggr,
cap0). Byte-identical reruns confirmed independently.

## Head-to-head: deferral (E-DE3) vs narrowing (E-DE5)

Run by this crew on the identical 1,199-item manifest + snapshot, using
E-DE5's own binary (E-DE5's canonical verdict belongs to its crew; these
are head-to-head observations):
- E-DE5a (verify-proposal-only): **+37.07%** full-cost saving, 0 winner
  divergence, 1,013 items with skipped hypotheses.
- E-DE5b (proposal-ordered elimination): **+9.49%** saving, 0 divergence.
- E-DE3 best prereg arm: +0.015%.

On identical workload with zero outcome divergence, narrowing beats
deferral decisively. Deferral-vs-narrowing is resolved in narrowing's
favor here.

## Why the mechanism fails (cost anatomy)

Deferring a check swaps one ledger entry for another (AUD_VERIFY →
AUD_VERIFICATION_DEBT ≈ 1:1); the checks themselves are cheap relative to
the ledger-dominated cost (ledger term ≈ 1,021.28/entry × 43,157 entries).
Only aggregation moves the needle (maximal-aggr: 38,361 entries, −11.1%
ledger bytes), and even the ceiling sits below KB2's 15%. A re-entry that
settled before emission would obey KB3 but cannot clear KB2 — the
headroom is structural, not a tuning gap. (Per the binding spec both bars
are KILL, so no re-entry is authorized regardless.)

## Surviving scientific value

1. The classification bet held 100%: 13,190 deferred-check replays, 0
   overturns, 0/1,199 divergence. In this workload the v0..v4 verification
   checks are redundant with the outcome — actionable intelligence for
   check-pruning work elsewhere.
2. The debt-cap valve works exactly as specified (live settlement under
   cap pressure, 0 trips, 0 divergence) — the discipline machinery is
   sound; it was the main-arm policy (never settle in-run) that violated
   the zero-tolerance rule.
3. The audit-mode + attribution-reconciliation instrumentation is solid
   and reusable (independent replay, per-entry-class reconciliation).

## Caveats

- Workload 1,199 items: one 72,658-byte D-P2 item excluded (>65,536-byte
  manifest cap; same exclusion as E-DE5's manifest; manifests
  sort-identical). D-P3 adversarial orderings not run (calibration-only
  per spec; no E-DE3 kill bar references D-P3).
- Analyzer bug found and fixed during verification: `analyze.py`
  asserted cap0 arm id 20; binary writes 13 (MODE_EDE3_CAP0). Data
  unaffected.
- E-DE3 crew was lost to a daemon restart at ~08:37 UTC with the battery
  80% complete; coordinator finished the remaining 8 legs with the crew's
  own scripted battery (`finish_battery.sh`) and computed the verdict
  independently. Infrastructure loss, not an experimental result.

## Evidence SHAs (run_0; all 5 reruns identical — see SHA256SUMS.txt)

- fd:             7ec2a599…
- conservative:  0ea57422…
- aggressive:    bcada367…
- maximal:       4cc0de49…
- maximal-aggr:  cad548f8…
- cap0:          21a422d5…
- captest:       (see SHA256SUMS.txt)
- e5a / e5b:     (see SHA256SUMS.txt — E-DE5's canonical evidence)

## Files

Source `ede3.zag` (+ byte-identical R2 modules per the crew's reuse audit),
`compare.py`, `analyze.py` (coordinator-fixed), `HANDOFF.md` (crew's,
with the §3 correction above), `finish_battery.sh`, `runs/VERDICT.json`,
`runs/ANALYSIS.json`, `runs/SHA256SUMS.txt`, `runs/battery.log`,
per-arm `runs/<arm>_r0.bin` evidence. Binaries excluded from git.
