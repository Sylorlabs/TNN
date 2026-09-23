# Arm O — Taught Vocabulary (ACQ) — Specification

## Authority
This specification follows the frozen brief, in authority order:
1. `~/workspace/tnn-lab/units/arms/briefs/O.json`
2. Verbatim frozen §3 row supplied by the Track A coordinator (2026-09-21)
3. Nothing else previously written

**Coordinator corrections acknowledged:**
- Correction 1 (2026-09-21): The original dispatch incorrectly described O as "Learned vocabulary" with an unrelated mechanism and kill criterion. That specification is void.
- Correction 2 (2026-09-21): The verbatim frozen §3 row was supplied, establishing O as "Taught vocabulary" with the mechanism and kill criteria below. The `O.json` brief and verbatim row were verified to match; no authority conflict exists.

Implementation follows the frozen taught-vocabulary brief exclusively.

## Frozen §3 Row (verbatim)

**O — Taught vocabulary | ACQ**

**Mechanism:** "Full learner-side intake via the Track B teacher protocol (§4): proposals → adopt/revise/reject/defer; taught words judgment-held at provisional strength (A-33/T-1)."

**Binding kill — any one fires KILLED:**
1. Taught-only vocabulary does not reach M2 criterion in ≤½ the episodes of emergent-only P on T1 novel material — acceleration claim dead.
2. Disconnect test fails: post-scaffold M1 < 99.5% — "learned" claim dead.
3. Any red-team malformed/malicious proposal is adopted — ingress gate killed; rebuild + full re-trial, not a patch.
4. A BPE-smuggling teacher emitting the exact BPE tiling at confidence 255 does not fire the tripwire.

If killed: public death certificate, evidence, and commit required.

## Design

### Teacher Protocol (Track B §4)
The learner receives proposals via the TST-1 (Taught Segment Transport) protocol:
- **Ingress validation:** Magic bytes, version, allowed teacher IDs (1,3,5; 0 and 2 reserved/invalid; 4 symbolic-hints-only, cannot send §P proposals), monotonic per-session sequence numbers, bounded spans, checksums. Malformed input rejected as R3 (integrity) before deliberation.
- **Verdicts:** ADOPT, REVISE (with SPAN_SHIFT/SPLIT/MERGE/GENERALIZE/NARROW operations), REJECT (grounds R1–R6), DEFER (max 3 turns).
- **Appeals:** Only for R1/R2/R5 with new evidence, max two appeals; third is R6.

### Learner Deliberation (§L)
The learner generates competing segmentations from its own independent corpus scan and adopts a taught word only after:
1. Evidence eliminates alternatives (no competing segmentation with equal support)
2. Independent corroboration exists (learner's own scan found the span ≥2 times)
3. No pinned conflict exists

Taught words are held at **provisional strength** (A-33/T-1): learned and provisional, not installed. Only an explicit audited trainer force-pin installs a word permanently.

### Tripwire (Rolling-200)
Monitors the last 200 proposals for smuggling signatures:
- **Primary:** coverage ≥95% AND accept rate ≥95% AND confidence-255 rate ≥90%
- **Secondary (immediate):** any single confidence-255 proposal covering >5% of session stimulus

If fired: session halts, incident logged (OP_REFUSE), kill-(iv) evaluation.

### Disconnect Test
Removes all teacher/scaffold state. The adopted vocabulary must persist with:
- Post-scaffold M1 recall ≥99.5%
- Identical recall rankings (no reordering)

### Provenance
Unified store records `{teacher_id, session_id, seq, kind}` for every taught word.

## Implementation Notes
- Pure Zag, zero RNG in decision paths, deterministic given state.
- One binary; `argv[1]` selects mode.
- Persistent corpus/segment → opaque ID mapping (A15 provisional).
- FIFO eviction with pinned units protected.
- Costs tracked: ledger entries, teacher messages, deliberation, appeals, deferrals.
