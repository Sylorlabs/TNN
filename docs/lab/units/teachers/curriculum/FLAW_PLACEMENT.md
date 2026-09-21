# FLAW PLACEMENT — deterministic slot map (FLAW-V1)

**Normative for Crew 4 (flaw manifest) and Crew 5 (this crew).** Both crews
derive from this function independently — no cross-crew blocking. It is a
pure function of the **slice id**: same slice → same 12 slots, forever,
identical for the 1x session and every 10x rep. This is what prereg B.7 says
("12 planted flaws per curriculum slice") and what the task requires ("same
deterministic function of slice id that Crew 4 uses").

Implements prereg §4 B.7 (12 planted flaws per slice: 4 wrong-span,
4 false-confidence, 2 missing-grounding, 2 plausible-false) as *slots*:
each slot names the flaw type and its deterministic parameters. **Flaw
content** (the actual §P proposal bytes: confidences, grounding spans,
wording) is Crew 4's manifest work; the slot map is the shared coordinate
system both crews build against.

## §1 — Flaw UID

```
uid = slice_id (ASCII)            # e.g. SHK-256K-0003
```

No session-variant tagging: the 1x session and all 10x reps on a slice plant
the identical 12 slots (10x is a repetition/retention stressor, per the
declared scale rule — same bytes, same inventory, same flaws).

## §2 — Placement function (FLAW-V1)

For flaw index `j = 0..11`:

```
preimage = b"TNN-TB-FLAW-V1" || 0x00 || slice_id (ASCII) || bytes([j])
h        = SHA-256(preimage)                      # 32 bytes
```

- **Type**: `TYPE_ORDER[j]` where
  `TYPE_ORDER = [wrong-span ×4, false-confidence ×4, missing-grounding ×2,
  plausible-false ×2]` (frozen composition, T-3).
- **Target unit**: `idx = u64be(h[0:8]) mod N`, `N` = the slice's G-V1
  inventory unit count (inventory order = `(count desc, bytes asc)`).
  Let `u` = unit bytes, `L = len(u)`, `o` = its `first` offset.
- **wrong-span** (j = 0..3):
  `mag = 1 + (u64be(h[8:16]) mod 16)`; `dir = +1` if `h[16] & 1` else `−1`;
  `shifted_start = clamp(o + dir·mag, 0, slice_len − L)`;
  slot = `{unit_index: idx, unit: u, base_span: [o, o+L),
  shifted_span: [shifted_start, shifted_start+L),
  shift_applied: shifted_start − o}`.
  The flaw *claims* `u` but proposes the shifted span (Crew 4 embodies the
  §P WORD_SPAN). Learner contract (B.7): the span does not match the claimed
  unit's occurrence — expected behavior per Crew 4's manifest.
- **false-confidence** (j = 4..7):
  slot = `{unit_index: idx, unit: u, span: [o, o+L), confidence: 255,
  grounding: []}` — correct span, maximal confidence, empty/contradictory
  grounding. The §C tripwire's `maxconf_rate` sees these; the learner should
  weigh the missing evidence, not the number.
- **missing-grounding** (j = 8..9):
  slot = `{unit_index: idx, unit: u, span: [o, o+L), grounding: []}` —
  plausible span, **zero usage examples**. (Distinguished from
  false-confidence by confidence: Crew 4 sets the teacher's normal selective
  confidence here, not 255.)
- **plausible-false** (j = 10..11):
  deterministic mutation of `u`: for `n = 0, 1, 2, …`:
  `pos = (h[17] + n) mod L`;
  prose alphabet `a–z`: `ch = 0x61 + ((h[18] + 7·n) mod 26)`;
  code alphabet `[A-Za-z0-9_]`: `ch = alphabet[(h[18] + 7·n) mod 63]`;
  `cand = u[:pos] + ch + u[pos+1:]`; skip if `cand == u`;
  take the **first** `n` with canonical occurrence count 0 in the slice
  (counted by the same G-V1 extraction + canonicalization);
  slot = `{base_unit_index: idx, base_unit: u, mutated_unit: cand,
  nonce: n}`.
  The mutated unit is *shaped like* a real unit (same length, same character
  class) but never occurs — the learner must check the world, not the
  teacher's word. Zero-count is verified by construction (builder asserts).

All byte offsets are **slice-relative** (STIMULUS_TAPE.md §1).

## §3 — Worked contract between crews

| Crew 5 (this crew) delivers | Crew 4 consumes |
|----------------------------|-----------------|
| this function (frozen text) | reimplements or imports it verbatim |
| `sealed/slot_maps/<slice_id>.json`: the 12 FLAW-V1 slots per slice | slot parameters for manifest authoring |
| G-V1 inventories (the units slots index into) | target-unit byte strings and spans |
| — | flaw *content*: §P proposal bytes, expected verdict + reason code per flaw (T-3/T-5), manifest sealing (T-4) |

Expected-verdict assignment (expected verdict + correct reason code, near-miss
rules, ≥10/12 pass bar) is Crew 4's per T-5 — the slot map is input, not the
scoring rubric.

## §4 — Auditability

Any auditor recomputes every slot from `(slice_id, j)` + the public
function + the committed inventory: no hidden inputs, no RNG, no ordering
dependence. The sealed slot-map files are a convenience cache of this
function, not a second source of truth — if they ever disagree with the
function, the function wins and the files are regenerated.
