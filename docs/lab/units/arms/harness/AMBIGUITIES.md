# AMBIGUITIES.md — Track A harness (B-64 validation round)

Standing rule: where the frozen prereg (`units/PREREG_FREEZE.md`, frozen
2026-09-21) is ambiguous, the harness implements the **literal reading** and
flags the ambiguity here. Nothing below reinterprets a bar. Micah decides;
the harness does not route around him.

## A1. M3 store capacity (C_M3 = 4,000)
§5 says "4,000 ingests at capacity" but never states the capacity number.
Literal reading: capacity is reached after 1,000 V + 3,000 fresh = 4,000 live
units, so C_M3 = 4,000 slots. Implemented exactly that. If the intended
capacity differs, M3 numbers shift (eviction count, liveness denominator).

## A2. M3 valuable-set schedule
"V = 1,000 units (deterministic schedule)" — the exact 1,000 are not
specified. Harness choice: every k-th unit over the concatenated
prose+code grid, k = floor(total_units/1000), marked before churn.
Any deterministic schedule satisfies the letter; cross-arm comparability
needs the schedule frozen identically for all arms (it is — shared code).

## A3. M3 weaken-op timing ("at step 6,000")
Steps counted from the first churn ingest: 3,000 ingests = steps 1–3,000,
3,000 kills = steps 3,001–6,000. The 50 weaken ops run immediately after the
last kill (= step 6,000), before phase 3. V marking is step 0, uncounted.

## A4. M5 memory formula ("harness-measured RSS delta + slot table")
Implemented literally:
`memory = (maxRSS(m5-1x) − maxRSS(m5-baseline)) + slot_table_bytes`,
with `slot_table_bytes` from the arm's store image (A16).
Resolution of the double-count concern: the validator's `m5-baseline` allocates
and fully touches the same empty store (and the same-sized ledger) that `m5-1x`
uses, so the RSS delta contains only the variable cost (corpus buffer for b64)
and the literal sum does not double-count. Arms must implement their baseline
the same way — empty store fully resident — or the formula over-counts.
Components are still reported separately (`rss_delta_bytes`,
`slot_table_bytes`) so the bar can be recomputed either way. The ledger is
priced under the audit metric (entries/KB), not in the memory figure.

## A5. M5 corpus buffer vs "memory per unit learned"
B-64 recalls by re-reading a retained corpus buffer, so its RSS includes the
full source bytes (ratio ≥ 1.0 by construction). A learned-representation arm
would not retain the corpus. The harness measures what is in RAM; it does not
decide which bytes "count". B-64's M5 is expected to be poor — it is the null
control, and the number is informative, not a harness failure.

## A6. M6 memorizer mapping for the c2p direction
The control is "a memorizer arm (prose-tuned policy, frozen)". For p2c:
indomain = prose, transfer = code. For c2p I map indomain = code,
transfer = prose (the policy stays prose-tuned, so the tax goes negative —
honestly showing the control's asymmetry). The gate needs ≥ 15 points in at
least one direction; p2c delivers 54.8.

## A7. M7 C′ edit bytes (needs a frozen convention)
"C′ = C with deterministic every-100th-unit edits" — the byte-level edit is
not specified. B-64 is non-ID (M7 = N/A) so this does not affect its score;
the validator implements first-byte XOR 0xFF as a concrete placeholder.
**ID-arm crews need Micah to freeze the C′ edit before their M7 runs.**

## A8. M7 lookup schedule
"Fixed 5,000-lookup retrieval schedule throughout" — validator implements
5,000 total lookups split 1666/1667/1667 across rounds 0/1/2, unit
`(l*37) % nunits`, counting re-read bytes. The exact schedule is not frozen;
only the informational re-read figure is reported for non-ID arms.

## A9. M2 "6 numbers" vs T3
"ETC reported per tier × corpus type (6 numbers)" — T3 is synthetic (no corpus
type), so the literal grid is 5 numbers (T1-prose, T1-code, T2-prose, T2-code,
T3). Implemented 5. "Relative-ETC vs the taught-baseline arm" is computed by
the assembler once that arm's row exists.

## A10. M9 cutoffs "proposed" (M-38)
Implemented the literal numbers: fast-then-flat (steepness ≥ 40 AND late
gain ≤ 15), slow-then-sudden (takeoff ≥ 3 AND steepness ≥ 40), gradual
(steepness < 40), else other — in percentage points, on the raw per-episode
curve including episode 0. Takeoff = first episode with recall ≥ 50%;
steepness = max single-episode jump; late gain = r(ETC) − r(takeoff).

## A11. M8 free-list perturbation vs id-derived placement
B-64's slot placement is a pure function of unit ID (documented in
HARNESS_SPEC.md); it has no free-list order to reverse. The perturbation is
accepted and verified as a no-op, which is itself the determinism evidence:
placement does not depend on allocator state. Arms with genuine free lists
must show the reversal in their trace.

## A12. §5 "rank by reached-criterion?, then ETC" punctuation
The "?" is read as a drafting artifact; §9 C12 ("rank by (reached-criterion?,
then ETC) lexicographically") is the operative rule. Censored ETC (50+) is
never averaged.

## A13. M4 "whole-corpus re-ingest invalidates"
B-64's revision path only clears recorded defect flags after probing the
unit; it never re-ingests. The harness has no separate detector for
whole-corpus re-ingest — an arm that re-ingests inside its "revise" would be
caught by audit review (ADD ops during revision episodes), not by an
automated tripwire. Flagged as a reviewer responsibility.

## A14. M1 boundary fidelity for non-grid arms
"Fraction of units whose (start,end) span is exactly the span the arm claims"
— the claimed span comes from the arm's own slot record. For B-64 the claim
is the grid span by construction. For learned-segmentation arms, the harness
compares the slot record against the arm's declared segmentation; the
declare-vs-truth distinction is arm-specific and documented per arm.

## A15. M1 swap-probe procedure for ID arms (proposed, needs freeze)
The prereg mandates "N=64 swap probe" for ID arms but gives no remap schedule or
remap function. ARM_INTERFACE.md §9 proposes: after every `ceil(nunits/64)`
recalls, patch the ID table so the next recall target resolves to
`(slot+1) % nslots`, log `TRAINER_SWAP_PROBE`, recall, expect the remapped
content, then restore. This is a harness proposal, not a frozen bar — Micah
must freeze it before ID-arm crews build. (B-64 is non-ID; unaffected.)

## A16. M5 "slot table" bytes for the validator
B-64 reports `slot_table_bytes` = its seven 4-byte slot arrays (ids, offs,
lens, corps, flags, shifts, pidx: 28 B × cap) plus the insertion-order queue
(4 B × ins_cap). The M8 store image covers the same region. Components are
itemized so the bar can be recomputed either way.

## A17. M8 "full M1+M3 runs" — one combined instance or separate instances?
The frozen prereg (§6) requires "full M1+M3 runs" under each perturbation for the
determinism gate. The validator implements this as ONE large-capacity instance
that runs the M1 (prose+code) ingest/recall sequence followed by the M3 op
sequence, sized so no capacity pressure occurs. A literal alternative reading is
that M8 replays the ordinary standalone `m1-1x` and `m3-1x` instances (including
M3's 4,000-slot capacity pressure) and compares those. The combined instance
tests the determinism of the op sequence; the separate-instances reading would
additionally test determinism under eviction pressure. The validator's choice is
documented here, not frozen as the procedure — Micah decides which reading
governs ID-arm M8 runs.
