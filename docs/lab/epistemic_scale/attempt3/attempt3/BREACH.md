# CLEAN-ROOM BREACH — Attempt 3 parser line is INVALID as clean-room evidence

Date: 2026-09-27
Status: INVALID SCRATCH. Do not present as valid Attempt-3 evidence.

## Frozen rule (PREREG_ATTEMPT3.md)
"Train labels may be used only for LOO scoring, never parsing or mechanism behavior."

## Breach
During parser implementation (frames.py / parse.py), train class labels were
explicitly used to direct parser development:

- Train classes were compared against parser TYPE assignments.
- Individual opinion misses and fact false-evaluatives were inspected by label.
- Parser lexicons and rules were changed in response, including:
  - Adding evaluative words after examining labeled opinion misses.
  - Removing false triggers after examining labeled facts.
- The train corpus was inspected "by class to understand construction patterns."

Therefore the parser line is contaminated for clean-room purposes. Any frames,
addressing, vocab, LOO scores, or verdicts derived from it are NOT valid
Attempt-3 evidence, even if the later deliberation code itself is label-blind.

## What exists in this directory (invalid scratch)
- parse.py, frames.py, build.py — contaminated parser line.
- frames.tsv, address.tsv, vocab.tsv — contaminated artifacts.
- build_data.json — contaminated intermediate (regenerable; not for deliverable).
- gen_zag.py, deliberate.zag, deliberate (binary), deliberate_data.bin —
  post-breach deliberation work; label-blind in itself but operating on
  contaminated frames, so its outputs are not valid evidence either.
- loo_s0.txt, loo_s1.txt — contaminated development diagnostics, NOT valid
  LOO evidence. (For the record: uncontested-standing gave 10 fact→lie FPs;
  corroborated-standing gave 0 FPs but 0 lie catches. These numbers are
  diagnostics of the invalid line only.)

## Required remediation
1. Preserve this directory as invalid scratch / evidence of the breach.
2. A genuinely fresh implementer (no exposure to the label-directed tuning)
   restarts from the frozen prereg and label-blind texts.
3. Build parser and audit all 640 items without consulting labels.
4. Require ≥0.90 frame well-formedness before LOO.
5. Implement comparison/standing/status/verdict/NEED in pure Zag.
6. Run LOO only after mechanism freeze; labels only to score that frozen run.
7. Apply standing escalation automatically; apply GO/NO-GO bars mechanically.
8. Only on GO: held-out run + determinism rerun; copy and verify takeaways.
9. Remove regenerable files and build products before delivery.

Recorded by the implementer on 2026-09-27. Do not silently continue this line
and call the result clean-room.
