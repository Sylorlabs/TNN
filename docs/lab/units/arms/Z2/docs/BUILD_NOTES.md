# Z2 build notes — r1 1x (2026-09-21)

## Verdict: PASS

Binding kill criteria (frozen §3 row Z2, verified against brief Z2.json):
- "Breach-detection rate < 80% on the misuse battery — Z2 is theater":
  measured **100.0%** (9,000/9,000 misuse probes refused loudly) → criterion
  does NOT fire.
- ">30% of legitimate recall ops refused as breaches — restrictions unusable
  (kill the restriction half, keep obligations)": measured **0.0%**
  (0/165 legitimate probes refused) → criterion does NOT fire.
- "Hot-path characterization required (znc miscompile history)": delivered
  (`docs/HOTPATH.md` + `z2-hotpath-1x` evidence). 20,000 recalls, 40,000
  checker calls (exactly 2×ops), 0 self-check mismatches, decision-log
  sha256 `611a114be17c52d73005a174216601aa605b8a578eaceb6712e742bd90dbd1aa`
  byte-identical across two fresh processes.

Standard M8 gate: **PASS** (5 perturbations × 2 reruns, byte-identical
artifacts; ledger.bin sha256 identical across clean/frag/aslr/starve/
freelist: `5d7ce7479de47cbf2bc9694b4929f69c6c0e4a743ea3cffd3c6f95c46ab1a850`).

## Battery

19 legs, every leg run twice with stdout diffed: all rc=0, all byte-identical,
zero FATALs. M1 100/100 both corpora; M2 ETC=1 all tiers; M3 survival 100;
M4 revision 100; M6 transfer tax 0.0; memorizer validity gate PASS
(drop 54.8 ≥ 15); M7 N/A (no ID layer, honest non-ID classification).

## Mechanism

Pure Zag. Fixed 64-byte mechanical chunks (B-64 grid) + real contract layer:
per-slot restriction mask / ledger-seq expiry / value sign; contracts in ADD
aux fields (a1..a4); `z_check` on the recall hot path; loud REFUSE entries
(201 expired / 202 restriction breach / 203 tombstoned). Zero randomness in
any decision path; no wall-clock; no addresses in decisions.

## Honest observations (non-binding — not in Z2's kill criteria)

- M5 memory bar: 1.974 bytes/byte vs ≤1.5 bar → FAIL. The contract layer
  costs 3 extra slot arrays (40 vs 28 bytes/slot, honestly accounted) plus
  measured RSS delta. M5 audit bar: 16.19 entries/kb vs ≤10 → FAIL (one ADD
  entry per chunk; identical ledger behavior to the b64 grid mechanics).
  These are section-champion comparison inputs (§7), not kill criteria.
- Non-ID classification override (ARM_INTERFACE.md §9): arithmetic
  positional IDs, no persistent ID→storage map; M1 swap probe and M7
  honestly N/A.
- Battery-design lesson: the misuse battery's legit phase must run BEFORE
  any misuse REFUSE entries are logged, because refusals advance the ledger
  clock that expiry is measured in — otherwise the battery's own logging
  expires the legitimate sample (first draft measured 0 legit attempts).

## Build

znc `znc_linux_x86_64_abed8aa1` on this Linux VM (never GHA/Mac).
Sources: `cl/arm.zag` sha256 `6de491c5193e4744d4bc971189c4b188ee4c3bb5e3366fd8e1ab0a9d4f651993`;
substrate files byte-identical to the harness copies. Workdir
`units/arms/Z2/work/` (binaries, generators, raw battery dirs) is NOT
committed; committed evidence is `evidence/r1_1x/` (32K).
