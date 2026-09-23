# Evidence index — PAMs v2 red-team (Team 8b), 2026-09-23

Deterministic attack evidence for `REDTEAM_V2.md`. All sha256 digests were
reproduced by an independent second run of the full pipeline.

- `TRIALS.sha256` — dual-span trial set manifest (288 trials + 288 G-span
  files + 288 truth sidecars).
- `run1_sense.sha256` — sha256 of all 576 sense outputs (288 dual-span,
  288 G-as-F); run 2 byte-identical.
- `rec_clean.records`, `rec_withhold.records`, `rec_install.records`,
  `rec_decoy.records` — the four gate record streams (13 fields:
  seq|tcode|fixture|prog|jcode|judgment|confidence|pred|measure|phash|truth|jG|confG).
- `run1_records.sha256` — record-stream digests; run 2 byte-identical.
- `gate_{a,d}_{clean,withhold,install,decoy}.out` — gate stdout
  dispositions; `run1_gateout.sha256`.
- `ledger_{a,d}_{clean,withhold,install,decoy}.txt` — hash-chained ledgers
  (sha256(prev_raw32 || canonical) per link); `run1_ledger.sha256`.
- `score_{a,d}_{clean,withhold,install,decoy}.score` — per-family and total
  scores; `run1_score.sha256`.
- `verify_ledger.py` — Python glue that verifies each ledger's hash chain
  and cross-checks dispositions against gate stdout (analysis only).

V2-C vknow detector sweep digest (0 fires on all 288 fixtures):
`ae8a506c47f8cff092a3bf97dc1c5af4710919b8fc4c395317eb346558f2711f`

Attack harnesses (pure Zag, zero RNG): `../src/rt_trials.zag`,
`../src/rt_records.zag`, `../src/rt_score.zag`, `../src/rt_vknow.zag`.
