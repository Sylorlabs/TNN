# INTEGRATED Build Notes — Round-2 Dialogue Repair Merge

## Source
- `merge.py`: deterministic merge script. 18 anchored edits, all `sub_once`
  (asserts uniqueness). Regenerates `dialogue.zag` (2,930 lines) from the five
  family forks plus canonical.
- Canonical files (`dialogue.zag`, `kb.txt`, `gaz.txt`, IO/SHA) are COPIED,
  never modified. Hashes verified unchanged after build (see VERDICT.md).

## Pipeline order (per PREREG_INT.md)
1. F5 router (utterance-type dispatch)
2. correction
3. resume
4. F4 challenge/provenance
5. composition: F3 difference engine → F1 do_compare → did-write → birth-year
6. assertion/contradiction
7. default retrieval with F2 withhold gate between `retrieve()` and `emit_fact()`

## pv slot map (per PREREG_INT.md)
- 0–28: canonical unchanged
- 32: F4 `prevbn` (bound-pronoun count of previous turn)
- 40/44: F1 compared pair (persists across turns for "those two" anaphora)
- 48/52: F3 carry pair (one-turn, for "how much taller is it?" follow-ups)
- 56: F3 dimension (write-only, as in F3's fork)
- 60: F3 carry turn

## Bugs found and fixed during integration

### 1. Old "which is taller" branch shadowed F1's do_compare
The merge initially INSERTED the F3 branch + F1 engine before the did-write
branch but LEFT the two old canonical prefix branches ("was the author of",
"which is taller") in place. The old "which is taller" branch fired first,
returning the correct string but NOT writing the F1 pair (40/44) or the F3
carry (48/52/60). This broke round-2 turns 6 ("120") and 7 ("the eiffel tower
was built first.").
**Fix**: `merge.py` now REPLACES the span from `do_compose` signature through
the end of the old "which is taller" branch with the merged body (F3 branch +
F1 engine + carry write).

### 2. Duplicate `retrieve()` from F2 gate extraction
The F2 gate block was extracted as F2 lines 1965–2005, but line 1965 is F2's
own `let fid3:i32=retrieve(...)`. The merge anchor already contained that
line, producing a DUPLICATE `let fid3` (two consecutive `retrieve()` calls).
**Fix**: extract from F2 line 1966 (the comment) instead.

### 3. Malformed `DIALOGUE` header in test battery (not a merge bug)
Single-turn diagnostic batteries used `DIALOGUE A` (no section type), causing
`stype_idx` to return -1 and a slice panic. The canonical format requires
`DIALOGUE <id> <TYPE>`. Not a merge defect.

## Known unresolved: 7 round-1 deltas (see VERDICT.md)
The merged system is NOT byte-identical to canonical on the round-1 battery:
- FOLLOWUP 44/45 (1): FU-08 3 "What about the Amazon River?" → "I don't know."
  (F2 withhold over-fires on the follow-up)
- REFERENT 57/60 (3): RE-01/06/11 turn 3 "What about the Louvre?" →
  "I don't know." (F2 withhold over-fires)
- TOPIC 57/60 (3): TO-02/07/(+1) turn 2 "What about Pride and Prejudice?" →
  "Jane Austen wrote the novel Pride and Prejudice." instead of
  "Pride and Prejudice was published in 1813."
  (F4's ellipsis resolves "What about X?" to the previous "who wrote"
  shape because pv[8] holds a valid entity in merged but not in F4's fork;
  root cause is a merge interaction in pe3/eout state, not fully diagnosed)

These are honest regressions against the PREREG_INT.md byte-identical kill
bar. The round-2 (18/18) and held-out (36/36) targets are fully met.

## Build
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- 7 analyzer warnings (inherited dead-loop/ignored-return + one `fid3`
  overwrite note from the fixed duplicate; no errors).
- Binary: ~387KB, builds in ~70s.

## Files
- `merge.py`: the merge script (rerunnable, deterministic)
- `dialogue.zag`: generated merged source
- `kb.txt`, `gaz.txt`, `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag`:
  canonical copies
- `round2_expected_battery.txt`: 18-turn expected battery (DIALOGUE R2-INT TOPIC)
- `PREREG_INT.md`: frozen preregistration (committed before merge code existed)
- Logs: `round2_run1.log`, `round2_run2.log` (byte-identical),
  `heldout_f*_run1.log`/`run2.log` (byte-identical pairs),
  `round1_run1.log`, `round1_run2.log` (byte-identical to each other, NOT to canonical)
