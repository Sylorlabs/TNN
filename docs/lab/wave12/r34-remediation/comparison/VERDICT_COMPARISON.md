# VERDICT — was the hidden RNG helping TNN?

**Workstream:** COMPARISON (r34 remediation). **Prereg:**
`PREREG_COMPARISON.md` (frozen `a01a5e838935`, no amendments).
**Analysis:** `ANALYSIS_COMPARISON.md` (this workstream). **Date:**
2026-09-20. **Owner:** Micah.

## Verdict: DID-NOT-HELP

The hidden LCG did not help TNN. Not on clean legs, not on the corruption
leg. What it did:

1. **On clean legs (LH-1/2/3): pure tax, zero behavioral return.** The
   state-blind 1-in-5 flips (88 / 389 / 989 explores vs the clean rule's
   16 / 16 / 11) changed **zero** switch decisions (19/19, 79/79, 439/439
   identical) and **zero** eval outcomes (16/16 everywhere, identical
   return gates, byte-identical drift schedule, mirror assignment, and
   mode-2 probe artifact). Every explore beyond block-0 discovery was a
   confident-regime wrong-cell tap: a lost +100 on a correct cell and a
   −100 on a wrong cell, with the switch safely blocked by
   `pending_explore=1`. Costs, all reproducible: correct cells pinned
   2–3 blocks later (block 16 vs 13/14), max|score| 18900 vs 22300 at the
   LH-1 endpoint, wrong cells sunk ~4.4× deeper (−21100/−20100 vs
   −4700/−4800 at LH-2 block 39; pinned −30000 by ~51/59 vs still sinking
   at −22100/−18800 in LH-3).
2. **On the corruption leg (LH-5): the finding is RNG-independent; the
   only "help" was accidental damping of a pathology.** The knee (between
   0% and 10%), the 10% collapse blocks (5-B, 9-A), the 25% collapse
   blocks (3-A, 4-B, 9-A), and the 0% baseline are **byte-identical**
   with and without the RNG — the fragility verdict stands on the switch
   rule's lack of corroboration, not on exploration policy. At 25–50%
   the tainted arm switched somewhat less (149 vs 154; 181 vs 198)
   because explore episodes are switch-immune (`pending_explore=1`
   blocks the trigger) and the LCG supplied ~98 uniform immune episodes
   per lineage vs the clean rule's 61/76 streak-gated ones. But the
   effect is chaos-modulated, not a function: the explore-delta to
   switch-delta mapping is non-monotonic (Δ60 explores → −1 switch at
   10%; Δ22 → +17 at 50%), and the 50% endpoint consequence (tainted
   B=16/16 vs clean B=0/16) sits inside the chaotic envelope **both**
   arms exhibit — the tainted arm's own supplementary seeds end B=0/16
   at 10% and 25% corruption. Per the frozen H2 (chaos check), this
   cannot carry a HELPED claim.
3. **The useful exploration is fully preserved.** Block-0 discovery
   volumes match (13–14 tainted vs 11–16 clean): the deterministic
   uncertainty predicate (`margin<=200`) does everything the LCG ever
   did usefully. Independent corroboration: LH-P3 C1 — 29 adaptive
   explores beat 84 fixed 1-in-5 flips on training positives (432/480
   vs 379/480) with identical endpoints.

Against the frozen criteria: H1 fails (no headline metric is strictly
better in the tainted arm once the chaotic 50% endpoint is excluded per
H2); D1 holds on every non-chaotic headline; D2 holds (all deltas are
the Mechanism-1 tax or chaotic-envelope noise); D3 holds (no traced
benefit mechanism — the damping candidate is already honestly
implemented by the clean disappointment path, prereg F4, differing only
in volume). Not MIXED: no metric satisfies H1+H2+H3.

## Named caveat (prereg F3 — reported, not omitted)

The 50% primary-seed endpoint differs (tainted A=0/B=16 vs clean A=0/B=0)
with switches 181 vs 198. This is a real delta, but it fails the frozen
chaos check: both arms lose whole regimes at endpoint on other seeds in
the same chaotic regime (13/20 vs 12/20 collapsed probes; tainted supp
seeds (10%,7777) and (25%,7777) both end B=0/16). It is classified as a
D2 chaotic-envelope delta, not evidence of help. If a future experiment
wants to settle it, the preregistered way is more corruption seeds at
50%, not argument.

## Design implication for the deterministic mechanism

**Nothing needs to be added; one thing must be protected; one thing is
the real fix.**

1. **Keep the uncertainty path exactly as is** (`margin<=200`). It
   already captures 100% of the RNG's useful function — discovery under
   genuine indecision. The head-to-head proves the surplus flips were
   never doing discovery work, only taxing settled regimes.
2. **Protect the disappointment path** (`neg_streak>=3`). Under
   corruption it is load-bearing and scales with noise (16→38→61→76
   explores at 0/10/25/50%) — it is the deterministic mechanism's honest
   version of "try something different when what you're doing isn't
   working," and its episodes are switch-immune, which is the only
   damping function the RNG ever accidentally served. Do not tune it
   away to chase fewer explores.
3. **Do NOT reintroduce state-blind flips.** They would restore the
   measured tax (2–3 blocks later saturation, ~4.4× deeper wrong-cell
   sink, ~20% of accepts wasted in settled regimes) in exchange for an
   unreliable, chaos-modulated damper.
4. **The real fix for the noise pathology is the switch rule, not the
   explore policy** (LH-5's standing open item): a corroboration
   requirement on the switch trigger (e.g. two consecutive non-explore
   negatives) would eliminate the spurious-switch storm honestly, making
   the accidental damping irrelevant.
5. **Instrumentation note for future work:** the LH-5 evidence logs do
   not decompose which predicate fired each explore under corruption
   (uncertainty vs disappointment). If the explore rule is ever tuned,
   log the trigger path per explore — the current analysis had to treat
   the 38/61/76 as an aggregate.

## Falsification accounting (prereg §5)

- **F1:** PASS — LCG replay reproduces the LH-P3 fixed arm's documented
  per-block counts `11,7,8,8,7,12,10,7,9,5` exactly; replay program
  byte-identical across two runs.
- **F2:** no "helped" mechanism claim is made, so no attribution to
  falsify; the damping mechanism is explicitly scoped as incidental and
  chaos-modulated.
- **F3:** all six frozen metrics addressed in `ANALYSIS_COMPARISON.md`;
  the single contradicting point (50% endpoint) is named above.
- **F4:** the candidate help-function (switch-immune episodes during
  negative streaks) is already implemented honestly by the clean rule —
  stated explicitly; no reintroduction recommended.

## Out of scope (unchanged)

LH-4 / LH-7 claims remain suspended (no clean counterpart rerun);
tainted explore volumes reconstructed for the record only: LH-4 53/288
(18.4%), LH-7 92/480 (19.2%). LH-6 stays blocked.

## Evidence

- `PREREG_COMPARISON.md` — frozen prereg (committed `a01a5e838935`)
- `lcg_reconstruct.zag` — pure-Zag LCG explore-sequence replay (no RNG)
- `lcg_reconstruct_output.txt` — reconstruction output (F1 validation:
  `11,7,8,8,7,12,10,7,9,5`, sum 84)
- `ANALYSIS_COMPARISON.md` — metric-by-metric analysis
- `VERDICT_COMPARISON.md` — this verdict
