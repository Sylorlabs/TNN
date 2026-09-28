# RUNLOG — Round-C cheap falsification probes

**Date:** 2026-09-24
**Prereg:** `PREREG_ROUNDC_PROBES.md` (committed alone: `0db769f222802a98c484b77d129e62eb2d20ee46`)
**Source:** `probe/roundc_probe.zag` (pure Zag, zero randomness; written AFTER the prereg commit)
**Build:** from `probe/` with `R33_NATIVE_IO_V1.zag` copied in;
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 roundc_probe.zag -o roundc_probe`
(build warnings: 4× E0101 "adding 0 has no effect" on intentional no-op lines; binary wrote clean)
**Runner:** one binary, `argv[1]` selects mode; 3 runs per mode; SHA-256 compared.

## Run table (all 3× byte-identical)

| Mode | SHA-256 (all 3 runs) | honest sanity | Bar | Result |
|---|---|---|---|---|
| sep | `51e745b2…e65559` | 60/60, 60/60 | lemma_demo_fired | FIRED (attack 60/60, 60/60) |
| irrev | `0f3b4e264…b9b515` | 60/60 | naive_irrev_dead_fired | FIRED (attack 60/60) |
| mepoch | `f8806695…97fc199` | 20/20 | naive_mepoch_dead_fired | FIRED (attack 20/20) |
| pow | `4d0973f5…ef0bc557` | 60/60 | pow_dead_fired | FIRED (attack 60/60, cost ratio 98 ∈ [90,110]) |
| trmod | `2416e4cc…13641e3` | 60/60 | module_trainer_dead_fired | FIRED (attack 60/60) |
| tror | `1b50ac65…30f252c0d` | 60/60 | oracle_bound_holds | PASS (attack 0/60, honest 60/60) |
| tier | `5ec77f42…7000fc04f` | 60/60, 60/60 | tier_boundary_holds | PASS (promotions 0, act 0, premise 0, high attacks 0/40) |
| bond | `b5368bbe…84beb6e3df` | bond 60, 196/196 | bond_dynamics_hold | PASS (adv 10 ≤ 15; residual single lie = 1, recorded) |
| chan | `c72d6849…54b65620cd` | 20/20 | win_condition_shift | PASS (content 20/20 minted; channel 0/20 minted, 0/20 tampered, 20/20 intact) |
| mepoch_tr | `f7033d30…0d9024c` | n/a | coverage_gap | PASS (per-verdict 0.875, full-seq 0.625 ≤ 0.750) |

## Notes

- No mode voided on honest sanity (all honest bars PASS).
- `pow` cost ratio measured 98 (×100), inside the prereg's [90,110] symmetry band.
- `mepoch_tr` full-sequence accuracy measured 0.625 vs prereg "expected ≈0.67";
  within noise of the 1/8 flip model (expected 0.875³ ≈ 0.670); the binding bar
  (≤ 0.750) is satisfied with margin.
- `bond` predicted honest bond end 60 / adversary 10 — measured exactly.
- `tier`, `tror`, `chan`, `mepoch_tr` PASS their syntactic bars; grok-4.7's
  objection record (grok_objections_roundc.md) argues these bars false-pass
  against IF/SL (tier), XR (tror), WG (chan), RC (mepoch_tr) — see VERDICT.md.
  The probes were run exactly as preregistered; the objections are recorded
  against the *claims*, not the *measurements*.
- Outputs: `probe/outputs/o_<mode>{1,2,3}.txt` (30 files).
- Binary and `.zagd` NOT committed (standing rule).
