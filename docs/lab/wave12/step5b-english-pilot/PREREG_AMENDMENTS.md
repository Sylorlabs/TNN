# PREREG AMENDMENT — 2026-09-20 (build note, no bar change)

## A1. ISO line field format (E5 protected-state isolation)

**Prereg §7 said:** `Logged: ISO,E5,fp_pre,fp_post,gate_same,ok`

**As built:** `ISO,E5,fp_pre,fp_post,g_pre,g_post,ok`

**Rationale:** `gate_same` (a single boolean) is weaker evidence than the two
independently recomputed 24-gate-vector folds. The built format logs both
folds (`g_pre`, `g_post`) so the independent checker re-derives the 24
verdicts itself and compares all three. Strictly stronger than the preregged
format; the bar itself (protected fingerprint unchanged across palette
expansion AND 24 gate vectors invariant) is unchanged.

**Status:** build note. No rule, schedule, test, metric, or kill-bar change.
Flagged for Micah's retroactive review per the amendment rule.

## A2. Read-only op ledger slot (build note, no bar change)

**Prereg §1 said:** ops 81–84 are "read-only ledger records with
before/after snapshots equal". It did not specify the `slot` field.

**As built:** all four ops reference a dedicated LOG slot (allocated once at
startup, value 8, never modified afterwards), with before/after snapshots
equal.

**Rationale:** the vendored `st_memory_core.zag` (byte-frozen from Step 2)
`st_replay_check` calls `st_restore` for every `ST_OK` op that is not
SETSTAGE/EVIDENCE/JUSTIFY/ABANDON. A `slot=-1` read-only op panics replay
("slice index out of bounds"). Referencing the immutable LOG slot keeps
before/after snapshots equal AND makes replay reconstruct the slot's true
constant state, so the per-episode `st_replay_check` verification passes
exactly. Observable evidence (op codes 81–84, d1/d2 fields, equal snapshots,
per-episode attribution) is identical to the preregged design.

**Status:** build note. No bar change. Flagged for retroactive review.

## A3. Scratch/log slot values (bug fix, no bar change)

**Found during the first full run:** the scratch slot (value 999999) and the
initial LOG slot value (888888) collided with the word encoding
`value/10000 == w`: `999999/10000 == 99` and `888888/10000 == 88`, so
`lex_find(s, 99)` / `lex_find(s, 88)` matched the scratch/log slots instead
of the real bindings for words 99 and 88. The pilot's own in-run checks
caught this (E1B ok=0 for word 99; 8 E4 + 12 E5 round-trip failures), and the
independent checker confirmed the exact failure set.

**Fix:** scratch value 999999 → 7, LOG value 888888 → 8
(`value/10000 == 0`, disjoint from all word encodings 1..800 and all
referents 2000..2799). No prereg text specified these values.

**Status:** bug fix, no bar change. Documented here for the record.

## A4. E5 zero-drift token logging (bug fix, no bar change)

**Found by the independent checker:** for episodes 700–799 the pilot called
`e5_produce` twice into the same token buffer (once for the round-trip
check, once for the zero-drift check), so the logged `RES,E5` token sequence
was the zero-drift sentence while `exp`/`rt` described the first sentence.
The checker's independent re-parse flagged 99 mismatches; the pilot's own
`nzd` counter was correct.

**Fix:** separate `tok2` buffer for the zero-drift re-produce; the `RES,E5`
line now logs exactly the tokens the round-trip check verified.

**Status:** bug fix, no bar change. The checker caught it; the fix is
verified by the checker passing on the new transcript.
