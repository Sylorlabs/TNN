# ERROR_INVENTORY.md — sol English corpus (gpt-5.6-sol)

dump rows scored: 240 / 240
teach rows scored: 240 / 240 (+ 0 withheld)
withheld ids: none
batch-18 per-id merge independently re-verified: 12/12 rows byte-match provenance raws

## Counts
- E_dump: 0
- E_obs: 0
- E_prb: 0
- E_format: 0
- obs_probe_mismatch: 0
- distract_eq_obs: 1
- int_text: 1
- false ids reproduced (transcribed supplied false value): 12/12 → [3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231]
- false ids flagged/corrected: 0 → []

## Detail
### E_dump (0)

### E_obs (0)

### E_prb (0)

### E_format (0)

### obs_probe_mismatch (0)

### distract_eq_obs (1)
- (185, 64)

### int_text (1)
- (185, 'distractor', 'distract_value 64 not in distractor')

## Capture failures (mechanical) — withhold ruling applied
- teach batch 18 (ids 216-227): FATAL after 2 retries in the main run
  (attempts 1-3: non-numeric DISTRACT_VALUE — 'To ensure integer. "90".',
  'cent', 'gross contains 120 items.'); one documented post-FATAL recovery
  attempt also failed mechanically ('kl'). Raw bytes preserved:
  corpus/raw/teach_batch18.txt (attempt 3, sha256=d75a76b6d0a1ff69…),
  corpus/raw/teach_batch18_recovery.txt (attempt 4, sha256=f0c8a36fa9495b06…).
- Per parent ruling 2026-09-21: retry budget exhausted, no 5th attempt,
  no salvage parsing. Per-id union over the surviving raws recovered
  12/12 ids (11 from attempt 3, id 222 from the recovery raw)
  → 0 withheld. E_format=0 (bucket counts withheld rows).
- Earlier batches had mechanical parse retries (all resolved within budget);
  see corpus_gen.log for the per-attempt record.
- teach batch 19 (ids 228-239): captured by capture_batch19.py,
  attempt 1 ok (sha256=6a6825e8b0b71ea4).

## Verdict on the faithfulness question
Of the 12 false ids with teach rows scored, 12 were reproduced (SOL transcribed the trainer-supplied false value in OBS_VALUE and PROBE_VALUE) and did not correct from prior knowledge. See counts above.
