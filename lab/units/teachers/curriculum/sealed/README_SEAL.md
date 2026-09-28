# SEAL RULE — flaw manifests and ground-truth inventories

**Binding: prereg §4 B.7 / T-4.** The learner never sees the flaw manifest
until scoring; the ground-truth inventories are the answer key and are
likewise never shown to the learner.

## What is sealed

- `sealed/slot_maps/<slice_id>.json` — the 12 FLAW-V1 flaw slots per slice
  (the coordinate input to Crew 4's flaw manifest). Identical for the 1x
  session and every 10x rep: the slot map is a pure function of the slice id.
- `inventories/<slice_id>.json` — the G-V1 ground-truth unit lists.
  (Committed at the curriculum root for auditor visibility, but sealed from
  the *student process* exactly like the slot maps.)

## The rule

1. The harness MUST NOT expose sealed files (or their bytes, hashes, or
   any deterministic derivative an auditor could invert into targets) to
   the student process, the teacher programs, or any replay under test.
   The student's only window onto the stimulus is the tape's stimulus
   segment; the teacher's only window is the wiring spec / live judgment.
2. The arm-5 oracle's answer function (`builder/oracle_ref.py`) reads the
   inventory **inside the harness**, never inside the student: the student
   sends span queries, the harness answers YES/NO. The student must not be
   able to enumerate the inventory through the query budget (budget K is
   T-9's, frozen — the budget is the anti-tiling mechanism).
3. **Leak rule (T-4):** manifest leak → run invalid + fresh-slice rescore.
   "Fresh-slice" means a slice the learner has never seen: any of the 44
   slices not yet used. The deterministic slot function makes minting a
   fresh slice's manifest a pure recomputation.

## What is NOT sealed (auditor-visible by design)

- `OPERATIONALIZATION.md`, `FLAW_PLACEMENT.md`, `STIMULUS_TAPE.md`,
  `PROVENANCE.md`, the builder source, and `manifests/slices_manifest.json`
  (slice ids, byte ranges, SHA-256s — but NOT the unit lists or slot maps).
- The *method* is public; the *instantiations* are sealed. An auditor can
  recompute every sealed byte from the public method — that is the point.
  The seal binds the harness and the student, not the auditor.
