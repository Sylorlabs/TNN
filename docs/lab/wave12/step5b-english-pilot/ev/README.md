# Evidence transcripts — STEP 5b English curriculum 1x pilot

The full transcripts were too large for single-blob GitHub commits, so
each is split into ~2,000-line text chunks. Reassemble with:

    cat run_a_part_*.txt > run_a.txt

- `run_a_part_*.txt` → run A (evidence run; checker: CHECK,GO, 44/44).
- `run_b_part_*.txt` → run B. `sha256(run_a) == sha256(run_b)`
  (`f17671e7a454b19cade4a4489b959e3a2fc37d009c7d1930e7b4eaf8db270124`):
  byte-identical deterministic rerun.
- `smoke_old_part_*.txt` → the first full run, INVALID as evidence: it
  predates two harness fixes (scratch/log slot value collision and the E5
  zero-drift token-buffer overwrite). Kept because the independent checker
  correctly returned DEAD on it and caught the second bug — the diagnostic
  trail is part of the record.

All three regenerate byte-identically via `../run_step5b.sh`
(deterministic native build; zero RNG).
