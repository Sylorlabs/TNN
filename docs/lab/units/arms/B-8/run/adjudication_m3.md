# M3 adjudication evidence — B-8 (2026-09-21, follow-up crew)

Question: is the r1 M3 result (`100.0, 67.6, 64050, 50, FROZEN-UNDER-PRESSURE`)
real or a build defect?

## Protocol verification (frozen prereg, not the crew's notes)

PREREG_FREEZE.md M3 (frozen, commit b0b9140c0eda):

- "Valuable set V = 1,000 units (deterministic schedule), deliberately marked
  valuable (pin/promote, logged)."
- "Pressure: 10,000 churn steps (3,000 fresh ingests / 3,000 kills of fresh
  units only / 4,000 ingests at capacity)."
- "Freeze-vs-retention distinguisher (mandatory): (1) fresh-material
  accounting — 500-unit fresh sample must show recall ≥ 80% (a frozen store
  shows ≈0%) … **FROZEN-UNDER-PRESSURE → M3 = 0.**"

The churn fixture `churn_fresh.bin` = 448,000 bytes = exactly 7,000 64B spans
= 3,000 + 4,000. The prereg's churn-phase "units" are therefore the fixture's
64B spans (the fixture is sized for exactly this reading). The crew's
implementation — phases in spans (3000/3000/4000), fresh sample = last 500
spans, V = 1,000 arm-native 8B chunks drawn from prose/code — implements the
frozen spec literally. No protocol defect.

## Independent reproduction

- Rebuilt `cl/arm.zag` with frozen toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Two independent `m3-1x` runs on `corpora/r1`: byte-identical metric lines:
  `M3,100.0,67.6,64050,50,FROZEN-UNDER-PRESSURE`
- Prior battery's M3 (run/battery_r1/m3-1x) matches: same numbers.

## Eviction-victim analysis (instrumented debug build, not committed)

50,000 eviction victims logged (21,000 phase-1 + 29,000 phase-3):

- Phase-1 victims: chunks 0–20999 (1,000 per 1,000-bin) — perfect FIFO.
- Phase-3 victims: chunks 24000–50999 (full bins) + 706/673/621 scattered
  across bins 51000–51999 / 52000–52999 / 53000–53999 = 2,000 victims.
- Live fresh set: chunks 51001–55999 (3,000).
- Phase-2 kills: spans 0–2999 = chunks 0–23999, of which only the 3,000 live
  ones (21000–23999, the phase-1 survivors) succeed — mgmt window confirms
  exactly 3,000 KILL entries.

Trace conclusion: eviction is **block-level FIFO**. The last 2,000 evictions
consume stale insertion-queue entries (slot numbers recorded when the slots
held older blocks); the slots now hold block-8 chunks 51000–53999 in
hash-permuted assignment, so the 2,000 victims are a hash-scattered subset of
51000–53999 rather than the insertion-ordered 51000–52999.

## The number, decomposed

- Fresh sample = last 500 fixture spans = chunks 52000–55999 (4,000 chunks).
- Live in sample: 327 + 379 (bins 52000–53999 survivors) + 2,000 (54000–55999)
  = 2,706 → 67.6%.
- Insertion-order-perfect FIFO would keep 53000–55999 → 3,000/4,000 = 75.0%.
- The 67.6 vs 75.0 gap = within-block hash-scattering from stale slot-queue
  entries (real implementation wart, logged in RETIREMENT.md).
- **Both numbers are below the 80% bar.** The FROZEN-UNDER-PRESSURE flag
  (survival ≥ 90 AND fresh < 80) fires under perfect FIFO too. The flag is
  driven by genuine capacity pressure — 4,000 slots, 1,000 pinned for V,
  4,000 fresh chunks demanded by the sample — not by the wart and not by any
  metric-path defect.

## Adjudication

**REAL.** The 67.6 is what the actual mechanism produces under the correct
frozen protocol; the freeze flag is genuine granularity/capacity pressure;
no fix changes any verdict. Production source left untouched.
