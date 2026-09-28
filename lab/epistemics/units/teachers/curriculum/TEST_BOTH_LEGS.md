# TEST-BOTH LEGS — flaw-slot keying reconciliation (FLAW-V1S vs FLAW-V1V)

**Status: frozen test-both legs** (program law #2: genuine doubt → test
both, per no-free-lunch). Two Track B workers built incompatible flaw-slot
designs for the same curriculum; both are committed as sealed, frozen legs.
Neither is "the" curriculum — the wave-2 battery scores **both**.

## The two legs

| | FLAW-V1S (slice-keyed) | FLAW-V1V (variant-keyed) |
|---|---|---|
| Sealed maps | `sealed/slot_maps_slicekeyed/<SLICE>.json` (44 files) | `sealed/slot_maps/<SLICE>.json` (44 files) |
| Keying | 12 slots = pure function of **slice id** | 12 slots per **session variant** (1x + 10x-R0..R9), 11 × 12 per slice |
| Provenance | recovered verbatim from commit `7b10f4d4e5e6` | current branch-tip build |
| B.7 reading | literal: "12 planted flaws per curriculum slice" | per-variant: 12 flaws per session instance |

### FLAW-V1S — what it tests
Flaw-slot identity is invariant across reps of a slice. Tests **flaw-detection
stability across reps**: does the learner's detection of a fixed flaw set
improve/degrade with repetition? Follows `FLAW_PLACEMENT.md` (the normative
FLAW-V1 placement function — SHA-256 preimage over slice id, "No
session-variant tagging") and `OPERATIONALIZATION.md` §1.4's declared rule
("Slice bytes, ground-truth inventory, and the 12 FLAW-V1 flaw slots are
identical across reps"). Slicing (SLICE-V1), inventories (G-V1), and slice
byte ranges are byte-identical to the V1V leg — verified against
`manifests/slices_manifest.json` (44/44 slice ids, byte ranges match).

### FLAW-V1V — what it tests
Each session variant plants a novel 12-slot draw. Tests **generalization to
novel flaws** and makes the 10x leg statistically informative (10x is no
longer pure repetition — 11 distinct flaw instantiations per slice).
Same per-slot JSON schema as V1S (4 wrong-span / 4 false-confidence /
2 missing-grounding / 2 plausible-false; identical field sets per slot type —
verified by spot-check), so the battery's flaw scorer reads either leg
without modification: it consumes a 12-slot list, keyed by `(slice_id,
session_variant)`.

## Sealed protections (both legs)
Both map sets are sealed under `sealed/README_SEAL.md`: the harness MUST NOT
expose sealed files (or invertible derivatives) to the student process,
teacher programs, or any replay under test; leak → run invalid +
fresh-slice rescore. The seal binds harness and student, not the auditor.

## Wiring requirements
- **Arm-1 wiring must support both legs**: the flaw-scorer interface takes
  `(slice_id, session_variant) -> 12-slot list`. For V1S the map returns the
  same list for every variant key; for V1V it returns the variant's list.
- The wave-2 battery scores both legs separately; any champion verdict must
  state which leg it was earned on (or both).
- No leg may be deleted or "fixed" without Micah's re-approval — both are
  frozen prereg-bound artifacts.

## Provenance notes
- V1S maps: extracted from `7b10f4d4e5e6`'s git tree via the GitHub API
  (blob SHAs from the contents listing at that ref), committed byte-identical
  under `sealed/slot_maps_slicekeyed/`. Slice-id set and byte ranges match
  the current `slices_manifest.json` exactly (44/44, zero mismatches).
- The V1S-vs-V1V divergence is recorded here, not in `FLAW_PLACEMENT.md`
  (left untouched). Note: `sealed/slot_maps/` (V1V) currently diverges from
  `FLAW_PLACEMENT.md`'s "No session-variant tagging" clause — that divergence
  is exactly what this test-both reconciliation covers; resolution awaits the
  wave-2 battery verdict.
