# Red-Team Report: Bridge Adversary (B-A1..B-A6)

**Date:** 2026-09-29
**Role:** Bridge Adversary (independent; assumed H-BRIDGE false)
**Target:** H-BRIDGE claim, BRIDGE_RESULT.md (commit 06f5e2b5a),
  bridge_learn.zag, prereg 17d5de9f7
**Adversary prereg:** PI_BRIDGE_ADVERSARY_PREREG.md (commit 5a7d52195,
  frozen before attacks ran)
**Method:** `bridge_attack.zag` = lines 1-457 of bridge_learn.zag
  verbatim (diff-verified byte-identical) + independent attack main.
  Same learner, new tasks. Pure Zag, no Python.
  Raw output: BRIDGE_ATTACK_RAW1.txt (deterministic, byte-identical
  across two runs).

## Verdict

**H-BRIDGE SURVIVES all kill-relevant attacks, with one confirmed
denial-of-learning bug (B-A6b) requiring repair before integration.**

The core claim stands: the bridge learns (pos, val) conditions via
genuine search, generalizes beyond the builder's tested positions,
is correctly failure-gated, and fails honestly (not confidently)
outside its binary-conditional scope. But B-A6b demonstrates the
bridge can FAIL on a learnable task when its own failed split
attempts exhaust the procedure store. That is a real bug, not a
scope note.

## Attack results

### B-A1: Source inspection -- PASS

Grep of the learner region (`bridge_learn`, lines 315-458) for
`120`, `113`: CLEAN. No byte literal equal to any trigger value
inside the learning function. Condition values are read from
training inputs at runtime (`W[in_off+p] as i32`). The `120`/`113`
literals exist only in the test `main` as evaluator expectations
against preregistered predictions, which is legitimate: the
evaluator constructed the training data and checks the learner
recovered the data-implied condition. K-B2's "learned, not
hardcoded" claim holds.

### B-A2: Generality (pos=2) -- PASS

New task with the discriminating byte at input position 2
(middle), where pos=0 and pos=1 splits provably fail:
("abx"->"aaa"), ("cdx"->"ccc") [first] vs ("aby"->"yyy"),
("cdy"->"yyy") [last]. The bridge skipped the failing edge
positions and learned **IF input[2]==120 THEN proc0 ELSE proc1**.
Dispatch verified: "zzx"->"zzz", "zzy"->"yyy". Generality is NOT
bounded to edge positions; the search genuinely scans all
positions.

### B-A3: Three-way split -- BOUNDARY-CONFIRMED (honest -1)

("xab"->"xxx") [first], ("yab"->"bbb") [last], ("qab"->"qab")
[identity]. No binary (pos, val) split yields two fittable
subsets. The bridge returned **-1 with 0 bridge rules**: honest
failure, no confident-but-wrong binary rule. The binary-only
limitation (builder's prereg scope note 1) is real, and the
failure mode is the safe one.

### B-A4: Two-position conjunction -- BOUNDARY-CONFIRMED (honest -1)

Task engineered so no single (pos, val) separates the classes
(first iff input[0]=='x' AND input[1]=='y'; verified by hand
that every single-position split leaves a contradictory subset).
The bridge returned **-1 with 0 bridge rules**: honest failure.
Conjunctions are out of scope and the bridge does not hallucinate
a wrong single-condition rule.

### B-A5: Failure detection (no spurious trigger) -- PASS

("abc"->"cba"), ("def"->"fed"), ("xgh"->"hgx"): direct discovery
solves reverse despite an accidental byte correlation. Result:
proc slot 0, **0 bridge rules**. The bridge is failure-gated, not
trigger-happy. K-B1's "triggers on failure only" claim holds
beyond the builder's Task C.

### B-A6a: Slot waste -- WASTE-CONFIRMED (measured)

8 pairs: 7 broadcast-last distractors with distinct pos-0 values
('a','d','e','f','g','h','i') + trigger ("xab"->"xxx").
Each failed value's singleton subset fits and consumes a proc
slot before the contradictory remainder fails. Result: rule
correctly learned (IF input[0]==120 THEN proc7 ELSE proc8) but
**9 proc slots consumed for 2 needed** (7 wasted). The builder's
admitted "first-working-split-wins wastes proc slots" is
quantified: waste scales linearly with distractor count.

### B-A6b: Slot exhaustion -- BUG CONFIRMED (denial of learning)

16 pairs: 15 distractors + trigger ("xab"->"xxx"), PROC_MAX=16.
15 failed split attempts consumed slots 0-14; the true split's
first subset took slot 15; the second subset's store returned -1.
**bridge_learn returned -1 with 16/16 slots used and 0 bridge
rules, on a task whose rule (IF input[0]=='x' THEN first ELSE
last) is learnable.** The bridge denied learning because of its
own garbage. This is a FAIL-grade robustness bug: an adversary
(or a noisy environment) can brick the bridge with distractor
values. Repair required before any integration use: dry-run
discovery without storing, or reserve slots for the winning
split. Classified as bug, not scope note, because the mechanism
claims to handle exactly this task shape.

## What the attacks did NOT break

- The (pos, val) condition is genuinely learned via search (B-A1).
- Generality across positions is real, including middle
  positions the builder never tested (B-A2).
- Failure gating is correct; no spurious bridging (B-A5).
- Out-of-scope inputs (3-way, conjunction) fail honestly with
  -1, never with confident wrong rules (B-A3, B-A4).
- The preregistered kill bars K-B1..K-B4 remain PASS; nothing in
  this red team retroactively invalidates the builder's 7/7.

## Required repairs (before integration)

1. **Slot exhaustion (B-A6b):** implement dry-run subset
   discovery (discover without proc_store), storing only the two
   procedures of the winning split. Re-run B-A6b after repair;
   expected: rule learned, 2 slots used.
2. **Slot waste (B-A6a):** fixed by the same repair.

## Classification after red team

**Bounded L2+ with functional revision bridge (binary-conditional),
one known denial-of-learning bug pending repair.**

H-BRIDGE SURVIVES. The bridge is a validated repair for the
binary-conditional revision gap with honest failure modes and one
concrete, reproducible bug to fix.

## Files

- Adversary prereg: PI_BRIDGE_ADVERSARY_PREREG.md (5a7d52195)
- Attack source: bridge_attack.zag (learner lines 1-457 verbatim
  + attack main in attack_main.zag)
- Raw output: BRIDGE_ATTACK_RAW1.txt (byte-identical rerun:
  BRIDGE_ATTACK_RAW2.txt)
- This report: PI_BRIDGE_ADVERSARY_REPORT.md
