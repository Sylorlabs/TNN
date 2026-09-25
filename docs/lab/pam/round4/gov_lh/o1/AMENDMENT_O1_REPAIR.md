# Amendment — O1 FATAL kill-bar repair (signed)

**Status:** SIGNED 2026-09-25, decided-autonomously-per-Micah's-order (PAM Round 4 autonomous governance dispatch).

## The repaired bar (adopted)

**Kill iff K2 doesn't close within 2pp OR closes but RK-3 rises <3pp.**

Clause 1 (delivery): the K2 gap (K1 − K2') must close to within 2 percentage points.
Clause 2 (binding): with the gap closed, RK-3 must rise by ≥3 percentage points — a genuine throughput gain, not a paper repair.

## What the evidence proved

(`docs/lab/pam/round4/gov_lh/repairs/VERDICT_CREW5_REPAIRS.md`, leg O1; committed `o1.zag` rebuilt from digest-verified source with pinned znc; all runs 3× byte-identical; synthetic controls matched prereg predictions exactly with a fail-loud scorer.)

- **Real delivery fix → SURVIVES** (95.00%/95.00%, gap 0.00pp, RK-3 10.00%→16.00%, +6.00pp). The original bar killed this case (6.00 < 12.50 half-gap) — the FATAL defect (killing genuine throughput repairs) is cured, demonstrated.
- **Sham** (closes K2, no throughput) → **KILL clause 2** (gap 0.00pp, rise +0.00pp).
- **Null** (admits nothing) → **KILL clause 1** (gap 25.00pp).
- **Standing O1 kill preserved on its merits:** rebuilt binary reproduces committed metrics byte-identically; under the repaired bar K1=96.37%, K2'=86.57% (gap 9.80pp > 2pp) → KILL via clause 1, RK-3 rise +0.18pp. The repair attempt genuinely did not close the delivery gap.

## Effect

O1 is now judged by a bar that distinguishes genuine throughput gains from sham repairs and non-delivery. The standing kill stands — this repair changes the bar's aim, not the verdict on the evidence.

*Signed 2026-09-25 — PAM Round 4 autonomous governance dispatch.*
