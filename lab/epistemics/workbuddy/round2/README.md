# Workbuddy — Round 2: composition over session facts (2026-09-27)

Round 1 (commit `de0bb103a`, see `../WORKBUDDY.md`) could store and retrieve
session facts but not compose them. Round 2 implements six composition targets
(compare facts, anaphoric composition, correction supersession, task-shaped
bullets, grounded work-order review, further composition) on the frozen
deliberate-memory substrate.

**Note:** this `docs/lab/workbuddy/` directory was accidentally deleted from
HEAD by an unrelated commit (`dfb2e6848`) and is restored here; the round-1
files (`wb_dialogue.zag`, `wb_chat2.py`, `WORKBUDDY.md`, `OPTIMIZATIONS.md`,
`apply_edits.py`) are byte-identical restorations.

## Arc

| Phase | Result |
|---|---|
| Crew A — frozen 24-probe battery + strict scorer (`battery/`) | baseline **2 PASS / 1 WEAK / 21 FAIL** (incl. a baseline unsafe failure: after teaching a replacement vault code, TNN confidently returned the stale `7750`) |
| Crew B — composition implementation (`wb2_dialogue.zag` v1, `PREREG.md`, `RESULTS.md`) | claimed **24/24** |
| Crew C — independent red team (`REDTEAM.md`, `redteam_probes/`) | 24/24 **reproduced**, but the workbuddy claim **KILLED**: T3's `(subject, verb)`-keyed upsert silently destroyed taught facts on ordinary teaching (`quinn was promoted.` + `quinn was praised.` → `was quinn promoted?` → `no.`) and served stale facts after verb-changing corrections (`no, quinn resigned.` → still `quinn was promoted.`) — confident-wrong regressions vs a baseline that never lied |
| Crew D — bounded repair (`REPAIR.md`, `RESULTS2.md`, `repair_probes/`) | complement-aware identity `(subject, verb, complement-signature)` + subject-level correction retractions + one-period normalization; 24/24 again, all kill probes fixed |
| Parent — independent verification (`VERIFY.md`) | clean-room rebuild byte-identical (`7636a577…`), battery 24/24 re-derived, S1 frozen stream held ×3 incl. allocator perturbations |

## Verdict

The repaired build is a **workbuddy within its envelope**: single-hop composition
over taught declarative facts in narrow grammatical shapes — compare quantities,
resolve pronouns, supersede corrections, draft bullets, review work orders,
count/sum/composed yes-no — with honest withholds at the boundary (multi-hop,
unit mismatch, no relevant facts, nothing invented). The red-team kill is
resolved and the resolution re-verified independently.

## Files

- `wb2_dialogue.zag` — final repaired source (SHA-256
  `0bec5459b2959ec056c6c8771de7de009d7fd9406d7029d98fa97faa1a9d531b`).
  Built with the pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  → binary `7636a577fff29de6eae10fe238e33514083a3059aa9df8f64784a9601a684a09`
  (binary not committed; rebuild is byte-identical).
- `PREREG.md` — Crew B's frozen prereg (hypotheses, targets, kill bars).
- `RESULTS.md` — Crew B's 24/24 result.
- `REDTEAM.md` — Crew C's kill report (measurement survives, claim killed).
- `REPAIR.md` — Crew D's repair mechanism documentation.
- `RESULTS2.md` — Crew D's results table.
- `VERIFY.md` — parent's independent verification.
- `SHA256SUMS.md` — Crew D's hash manifest.
- `battery/` — frozen battery spec, strict scorer, 20 session inputs,
  expected outputs (independent re-derivation).
- `redteam_probes/` — Crew C's 29 adversarial probes + verbatim outputs.
- `repair_probes/` — Crew D's 8 new lifecycle probes.

## Frozen gates

- S1 round-4 answer stream: `3d60c4e33c0259b12fd7d27363aed6e8eca095a75bbc8a4daadcc2b6bbcf418f`
- Round-1 session reproductions: `base_anaph`, `val_teach` byte-identical;
  `base_correct`, `val_shapes` only intended improvements.
- Determinism: every session run twice through fresh processes, byte-identical.
- Confident-wrong scan: zero (the unsafe direction is the binding constraint).
