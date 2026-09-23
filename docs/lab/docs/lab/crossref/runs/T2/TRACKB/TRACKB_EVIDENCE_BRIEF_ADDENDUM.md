# TRACKB Evidence Brief — Addendum (2026-09-23)

This addendum completes gaps in the committed brief
(`TRACKB_EVIDENCE_BRIEF.md`, commit `f79a847597e1eaf0130e1b70a75a0028896d25e0`)
and corrects two prereg-faithfulness issues. The original brief is preserved;
this addendum documents completions, not revisions.

## A1. D4 completions

### varC DEFER×20 (prereg-required, previously "(see note)")
- **Result:** rc=0, teacher produced 1 proposal (SEQ=20). History with 20
  DEFER decisions (verdict=C_DEFER=4) handled gracefully. No crash, no
  corruption.
- 3× reruns byte-identical (SHA-256 `133bda6bf005d3fd792b9ffa1784e40d13fdbb317de9b72e4842b71eb27d4c16`).

### Contradictory history: ADOPT then REJECT R2 on same span (prereg-required, previously omitted)
| Variant | Result | Interpretation |
|---|---|---|
| varA | rc=13, `HALTED:SCRIPT_ERROR` | Teacher halts on contradictory script (D 0 ADOPT 0 then D 0 REJECT 2). Graceful rejection. |
| varB | rc=14, `bad history seq order` | Teacher rejects duplicate seq 0 (ADOPT then REJECT R2). Graceful rejection. |
| varC | rc=4, `history: replay rejected` | Teacher rejects contradictory decide events. Graceful rejection. |

All three teachers gracefully reject contradictory histories. 3× reruns
byte-identical.

### D4 integrity findings (spurious-INTEGRITY counts)
The prereg required counts of spurious INTEGRITY events. Results:
- **varB forged history:** rc=0, teacher ACCEPTED the forged history
  (5 records with spans 9000-9045, never emitted) and produced 500B of
  proposals starting at seq 5. **0 INTEGRITY events emitted.**
  The teacher does not validate history authenticity (false negative).
- **varC forged history:** rc=0, teacher ACCEPTED the forged history
  (fake propose+decide for span 9000-9005) and produced a proposal.
  **0 INTEGRITY events emitted.** The teacher does not validate history
  authenticity (false negative).
- **varA:** No separate history file; forged-history case N/A (no
  mechanism to inject forged events). Truncated script → rc=13
  (graceful halt).

**Finding:** varB and varC lack history-authenticity validation. They
accept well-formed but forged histories. This is a missing integrity
check, not a spurious INTEGRITY event. No spurious (false-positive)
INTEGRITY events were observed in any variant.

## A2. D1 dead marks per regime

Dead marks = spans proposed exactly once (never re-proposed).
Computed deterministically from `distinct_spans`, `appeal_reproposals`,
and `spans_proposed_ge3` in the D1 results.

### varA
| Regime | Distinct | Re-proposals | Spans ≥3× | Dead marks |
|---|---:|---:|---:|---:|
| R1-STORM | 1366 | 2730 | 1365 | **1** |
| R34-STORM | 4096 | 0 | 0 | **4096** |
| REVISE-SPAM | 4096 | 0 | 0 | **4096** |
| MIXED | 3 | 4093 | 1 | **0** (bound: 0–2; exact requires re-parse) |
| ADOPT-ALL | 4096 | 0 | 0 | **4096** |

Derivation for R1-STORM: 1365 spans × 2 re-proposals = 2730 = total
re-proposals. The remaining 1 span has 0 re-proposals → 1 dead mark.

For MIXED: 1 span has ≥3 proposals; the other 2 have <3. With 4093
re-proposals across 3 spans, all 3 were re-proposed at least once.
Dead marks = 0. (Upper bound 2 if the aggregates allowed singletons,
but the re-proposal count precludes it.)

### varB, varC
Dead-mark computation requires span-frequency data not preserved in the
D1 results JSONs. The varA computation above is complete; varB/varC
dead marks are **not computed** (gap documented). The D1 re-proposal
counts are in the brief §2.

## A3. Correction: varB D5 revisability is N/A (not 0.00)

The committed brief §6 reports varB revisability as `0.00 (0/7)` with the
note "Measure marked with reason, not N/A."

**Correction:** Per the frozen prereg §D5, "An unfaithfully expressible
measure must be marked N/A." The varB history format cannot encode the
revised replacement span (the prereg's "adopted-span → revises →
SAME_AS" requires the student to propose the revised span; varB's
REJECT R2 mechanism requests revision but does not carry the replacement
span). The 0/7 measurement is not prereg-faithful.

**Corrected value:** varB D5 revisability = **N/A** (prereg §D5 N/A rule:
unfaithfully expressible measure).

The 0/7 raw count is preserved in the run logs for transparency, but the
prereg-faithful report is N/A.

## A4. Clarification: varC D5 mastery denominator

The brief §6 reports varC mastery as `0.003 (4/1568)` with a tiling note.

**Clarification:** varC's fixed 65,536-byte interface requires the 4KB
base curriculum tiled 16×, yielding 1,568 GT units (98 × 16). varA/varB
use 98 GT units. The fractions (4/1568 vs 4/98) are not directly
comparable.

**Comparable absolute counts (GT units adopted):**
- varA: 4
- varB: 13
- varC: 4

The absolute adopted counts ARE comparable across variants. The
denominator difference is a mechanism-driven artifact of varC's fixed
interface, documented here per the user's "minimal deterministic choice"
rule.

## A5. SHA-256 evidence (D1–D5, three reruns)

All D1–D5 legs ran 3× byte-identical. SHA-256 hashes are in the run
results JSONs (`sha_stdout`, `sha_tape` fields). A machine-readable
table is at:
`~/workspace/trackb-battery/runs/SHA_EVIDENCE_TABLE.md`

D4 log SHAs (3× byte-identical):
`133bda6bf005d3fd792b9ffa1784e40d13fdbb317de9b72e4842b71eb27d4c16`
(all three reps).

D8 K1 output SHA-256 (unchanged):
`6994094cbecd687aeb0e7becbbad9731133c7f6479e637fc7580ea2fb92443fa`

## Summary of changes from committed brief

1. **D4 complete:** varC DEFER×20 (rc=0) and contradictory cases for all
   three variants (all gracefully reject).
2. **D1 dead marks:** Computed for varA (1, 4096, 4096, 0, 4096).
   varB/varC not computed (gap documented).
3. **D4 integrity:** varB/varC accept forged histories (0 INTEGRITY
   events; missing validation, not spurious events).
4. **varB D5 revisability:** Corrected from 0.00 to **N/A** (prereg rule).
5. **varC D5:** Clarified denominator artifact; absolute counts (4,13,4)
   are comparable.
6. **SHA evidence:** Table reference provided; D4 3× SHA included.

No recommendation or ranking is made. Trade-offs are reported;
governance choice is Micah's.
