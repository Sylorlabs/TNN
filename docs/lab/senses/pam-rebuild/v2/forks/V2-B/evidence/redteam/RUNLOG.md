# RUNLOG — Gap Crew C V2-B red-team
- 2026-09-23 ~21:04Z: built vsense_bin from committed src/vsense.zag
  (R2-4 lut/gcheck/R33 support); smoke-tested on R2-4 fixture.
- 2026-09-23 ~21:10Z: built attack_gate.zag (pure Zag) -> attack_gate_bin.
- 2026-09-23 21:1xZ: ATTACK_PREREG_V2-B.md committed (f3ed865d) BEFORE execution.
- 2026-09-23 ~21:15-21:35Z: gen_attacks.py generated 180 spans / 36 records
  (one stall killed under load; one stale-records incident caught by
  span-count audit and fully regenerated from fresh vsense runs).
- 2026-09-23 ~21:36Z: attack_gate_bin run 3x per mode (full/judg):
  byte-identical within mode. Ledgers independently verified (verify_ledger.py).
- vsense sampled spans: byte-identical x3.
- Zero RNG throughout. All artifacts deterministic.
