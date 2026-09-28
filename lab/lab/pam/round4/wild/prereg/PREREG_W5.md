# PREREG — W5 PAM-AS-MEMORY (wild track, WILD-B)

**Date:** 2026-09-24. **Crew:** WILD-B. **Status:** FROZEN — committed before
any W5 fixture, build, or run. Parent: `pam/round4/prereg/PREREG_ROUND4.md`
(§4 seed design W5). Shared tape: `wild/tape/TAPE.md` (frozen).

## 1. Falsifiable claim

W5 stores admission decisions as memories (signature → decision + strength)
and answers queries by memory lookup instead of recomputation. Claims:

- **F1 (fidelity):** after the store is warm, memory-lookup decisions MATCH
  recomputation by the frozen M1 bar (705, 3588, 1, 1 — used as-is, hands-off
  §5(a)) on 100% of the frozen tape rows. Any mismatch is a defect, not noise.
- **F2 (elimination beats promotion):** a poisoned store (wrong ADMIT
  decisions injected with HIGH strength) is fully repaired by confirmed-miss
  signals: every poisoned entry is eliminated, strength is irrelevant to
  elimination, and post-elimination lookups agree with recomputation
  (REJECT for all 12 W wrongs).
- **F3 (bounded growth):** store size ≤ number of distinct signatures seen;
  per-query work O(1) amortized (open-addressing hash table, no rehash
  past a frozen capacity).

## 2. Frozen mechanism

**Signature** (frozen quantization): sig(t) = (conf//50, mrgF//500, strong,
agree), packed into a u64 key. Two trials with the same quantized signature
share one memory. (Quantization is part of the design, frozen here.)

**Reference recompute** (frozen): the M1 bar PASS(t) ⟺ conf≥705 ∧ mrgF≥3588 ∧
strong≥1 ∧ agree≥1. Used as-is; W5 never modifies it.

**Store:** open-addressing hash table in a []u8 arena (LE accessors),
capacity 4096 slots (frozen; asserted sufficient — distinct signatures over
the tape are < 1000, verified at runtime; overflow → HALT with a finding, not
silent drop). Entry: (key, decision∈{ADMIT,REJECT}, strength u8).

**Rules (frozen):**
- R-LOOKUP: on query for t: if sig(t) in store → return stored decision
  (and log hit/match-vs-recompute); else → recompute, store (decision,
  strength=1), return it.
- R-PROMOTE: on a lookup hit where the recompute agrees with the stored
  decision (corroborated repeat), strength := min(strength+1, 255).
  Strength NEVER changes the decision — it is metadata only.
- R-ELIMINATE: on a CONFIRMED MISS signal for signature s (an external,
  preregistered signal stream — in the battery, the frozen wrong set):
  delete s from the store (tombstone), log `ELIM|sig|old_strength`, and
  record a tombstone that forces the NEXT lookup to recompute (no
  resurrect-from-promotion). Elimination wins over any strength, always.
- R-NO-RESURRECT: a tombstoned signature re-stored by a later recompute gets
  strength=1 (never inherits the eliminated strength).

**Battery phases (frozen order):**
- Phase A (warm + fidelity): stream all 2241 tape rows once, R-LOOKUP each;
  every hit's stored decision is compared against recompute; count matches.
  Claim: 100% match; store size = distinct signatures.
- Phase B (poison + elimination): deterministically OVERWRITE the store
  entries for the 12 W signatures to (ADMIT, strength=9) — simulating a
  corrupted/promoted-wrong store. Then feed confirmed-miss signals for the
  12 W signatures in tape order. Then re-query all 12: claim = all REJECT,
  all match recompute, 12 ELIM log lines with old_strength=9.
- Phase C (strength-never-overrides): re-poison ONE W signature to
  (ADMIT, strength=10), promote it 10 more times via corroborated-repeat
  simulation is NOT possible (recompute says REJECT — promotion requires
  agreement, so strength stays); instead directly set strength=255
  (maximally promoted wrong). Then confirmed miss → eliminated anyway.
  Claim: ELIM logged with old_strength=255; post lookup = REJECT.

## 3. Kill bars (program §4 K1–K5 verbatim + W5 additions, add-only)

- **K1:** any false-admit FROM MEMORY on the frozen wrong set (12 W + 9 P
  pairs) at any point after Phase A completes → KILL. (Phase B/C poison is
  injected deliberately; K1 applies to the store's answers: post-elimination
  queries must be REJECT. A poisoned entry that SURVIVES elimination and
  answers ADMIT = K1.)
- **KB-W5-M (added):** any lookup-hit decision ≠ recompute decision during
  Phase A (or post-elimination re-query) → KILL (deterministic given state;
  a mismatch is an implementation defect).
- **KB-W5-E (added):** any confirmed-miss signal that does NOT produce an
  ELIM log line, or any signature with old_strength>0 surviving elimination
  (still answering ADMIT) → KILL (elimination must beat promotion).
- **K2:** the two battery runs' stdout differ by even one byte → KILL.
- **K3:** correct-admit via memory must equal the frozen bar's correct-admit
  (910/1102 = 82.58%) — by F1's 100%-match claim this holds by construction;
  any deviation → KILL (it would imply KB-W5-M already fired).
- **K4:** store slots used > distinct signatures seen, or per-query probe
  length growing superlinearly → KILL (instrument logs max probe length and
  final slot count; capacity 4096 hard).
- **K5:** non-termination on any fixture → KILL.

## 4. Diagnostics (reported, never kill — frozen list)

- **D-W5-1:** distinct signature count over the tape; slot utilization;
  max probe length; collision count.
- **D-W5-2:** Phase A hit rate (hits/2241) — measures how much recomputation
  the memory actually saves.
- **D-W5-3:** per-phase strength histogram (shows promotion happened on
  corroborated repeats).

## 5. Battery

Instrument: pure-Zag `w5_memory.zag`. CLI: `w5_memory <tape>`. Emits phase
markers, per-phase metrics, ELIM log, and `kb_*` lines. Runs: 2×;
sha256(stdout) must match. Scorer: `score_w5.py` (Python mirror: recomputes
signatures, simulates the store, checks every claim — never the instrument).

## 6. Hands-off / laws compliance

- Frozen M1 bar used as-is (reference recompute); no threshold touched.
- Fable's 4 kill-bar repairs: not applied. 3 HELD items: not run.
- Zero RNG; no wall-clock; deterministic given (tape, rules).
- []u8 arenas + LE accessors; no `as []i32/u32/u16` indexed casts.

## 7. Standing-law cap note (for verdict-time classification)

Frozen numeric caps: table capacity 4096, strength cap 255, quantization
buckets (50/500). Classified at verdict time per the 2026-09-24 standing law.
(Design note: capacity is a physical-memory load-bearing bound; the bucket
widths are calibration.)
