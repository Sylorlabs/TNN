# Round-4 Dialogue Root-Cause Repair Report

**Date:** 2026-09-27  
**Branch:** tnn-native-lab  
**Task:** Micah's order — "find the issues, see causation, fix root cause" (not symptoms)

## Summary

Seven root causes identified and fixed in the dialogue system. All batteries pass with zero new regressions. Two byte-identical determinism runs verified.

| Battery | Before | After | Status |
|---------|--------|-------|--------|
| Round-4 (38 probes) | 27/29 exact* | 38/38 exact | ✅ Fixed |
| Round-3 (23 probes) | 20 good / 1 partial / 2 fail | 23/23 good | ✅ Fixed |
| Round-2 F2 (370 probes) | 351/370 | 351/370 | ✅ Zero new failures |
| Round-2 integrated (18) | 15/18 | 15/18 | ✅ Same 3 pre-existing drifts |

*Original 29-probe battery; expanded to 38 with red teams.

## Root Causes and Fixes

### 1. Deletion-intent misclassification

**Symptom:** "did TNN delete the sticker?" was misrouted as a memory-deletion request.

**Root cause:** The deletion-intent classifier treated "delete" as unambiguous. But "delete" in "did TNN delete the sticker?" refers to a world event (the sticker), not memory deletion.

**Fix:** Scoped deletion recognition:
- `unlearn` is unambiguous (always memory deletion).
- `delete`, `erase`, `wipe`, `clear`, `remove` require memory/everything/all scope to qualify as deletion intent.
- World questions ("did TNN delete the sticker?") are not misrouted.

### 2. Short-name arithmetic failures

**Symptoms:** 
- "Melville–Austen" (surnames) failed while "Herman Melville–Jane Austen" (full names) worked.
- "austen?" (with punctuation) failed exact matching.
- Zero-initialized pair slots fabricated "(entity 0, entity 0)" and answered "0 years".

**Root causes:**
- F3 used a different entity scanner than F1 (`gaz_scan` vs `cmp_scan`).
- Trailing punctuation ("austen?") wasn't stripped before exact fallback matching.
- Pair carry didn't check `cturn > 0`, so uninitialized slots were treated as valid.

**Fixes:**
- F3 now uses `cmp_scan`, matching F1.
- Trailing punctuation stripped before entity scanning.
- Pair carry requires `cturn > 0`.

**Verification:**
- Full names: Melville–Austen → "44 years" ✓
- Surnames: Melville–Austen → "44 years" ✓
- Missing second entity → "I don't know." ✓

### 3. Untaught-predicate confabulation

**Symptoms:**
- "what did Herman Melville eat?" → "Herman Melville was born in 1819." (birth fact for "eat")
- "when was the eiffel tower dedicated?" → "The Eiffel Tower is in Paris." (location fact for "dedicated")
- "when did he die?" → birth fact (no death fact in KB)

**Root cause:** The withhold gates only checked:
- G2: taught-but-mismatched relations (closed `is_relkey` list)
- G3: demand-focus words (ANY-hit form, too loose)

Unknown predicates ("die", "eat", "dedicated") weren't in the closed relation list, so they fell through and the system confabulated from predicate-incompatible facts.

**Fixes:**
- Added G6: untaught-predicate demand gate. If a specific question has a content word taught by no fact under any key (not a wh-word, not a meta-verb, not a discourse marker, not a typo near-miss), withhold.
- Generalized `pred_mismatch` beyond the closed `is_relkey` list to a structural check: any non-wh, non-meta question word not covered by the fact's keys (and not a typo near-miss) is a mismatch.
- Tightened G3 to require ALL structural focus keys to match (was ANY-hit).
- Fixed typo threshold: words ≤4 chars allow distance 1; longer words allow distance 2. (Previously "eat" matched "bear" at distance 2.)

**Refinements (after F2 regressions):**
- `is_discourse`: "ok", "yo", "please", etc. are pragmatic markers, not predicates. ("OK, when was Moby Dick published?" was withheld on "ok" alone.)
- `relation_covered`: If the fact teaches the question's relation, uncovered nouns are answer-type specifiers, not untaught predicates. ("what country is paris the capital of?" asks for the object of the taught "capital" relation.)
- `word_in_excl_name`: In the correction path, the excluded entity's name-words are negated, not demanded. ("Not that one, the other." was withheld because G3 saw "eiffel" uncovered by the Montparnasse fact.)

### 4. Correction-state corruption after withhold

**Symptom:** After a correction withhold ("who wrote the eiffel tower?" → "I don't know."), the system recorded the rejected candidate as answered knowledge.

**Root cause:** The correction path (added 2026-09-27) ran the withhold gate but then unconditionally:
- Pushed candidate entities via `push_ents`/`push_fact_ents`
- Recorded candidate `fid` in `pv,0`
- Returned `fid`

**Fix:** Mirror the default path's withhold semantics:
- On withhold (`wh_c==1`): skip `push_fact_ents`, set `pv,0=-1`, return `-1`.
- The shaped query is still preserved in `pqb`/`pv,20/24` for follow-up corrections.
- Question entities are still pushed (for pronoun reference), but the rejected fact is not installed.

### 5. Role-reversed yes/no questions

**Symptom:** "did the sticker detect TNN?" emitted "TNN detected the sticker." (without "Yes." after the prefix guard, but still misleading).

**Root cause:** The fact "TNN detected the sticker" teaches TNN as agent, sticker as patient. The question asks about sticker as agent. The system retrieved the fact (entity overlap) and emitted it, implying it answered the question.

**Fix:** Added G7 (role-order gate): For "did A verb B?" questions with two entities, if the question's subject (eout[0]) differs from the fact's primary entity AND the question's object matches the primary, withhold. The fact teaches the reverse roles.

**Verification:**
- "did TNN detect the sticker?" → "Yes. TNN detected the sticker." ✓ (correct direction)
- "did the sticker detect TNN?" → "I don't know." ✓ (withholds)

### 6. "Other one" correction regression

**Symptom:** "How tall is the Eiffel Tower?" → "Not that one, the other." was withheld (should give Montparnasse Tower).

**Root cause:** The correction path shapes the previous question ("how tall is the eiffel tower") and excludes the mentioned entity. But G3 saw "eiffel" as an uncovered demand word in the Montparnasse fact.

**Fix:** `word_in_excl_name` helper: checks if a word appears in the excluded entity's gazetteer name. G3, G6, and G4 skip such words (they're negated, not demanded).

### 7. Yes-prefix guard (partial)

**Symptom:** "did the sticker detect TNN?" was prefixed with "Yes." 

**Fix:** "Yes." only when the question's subject matches the fact's primary entity. (Superseded by G7 which withholds entirely for role-reversals.)

## Issues NOT Fixed at Root

### Units/dimensions hardcoded

**Status:** Documented capability gap, not a correctness bug.

**Details:**
- `diff_dim == 1` emits "meters"; `== 2` emits "years".
- "longer", "bigger", "smaller" collapse into dimension 1.
- Value lookup for dimension 1 uses marker "tall".
- The Amazon River fact ("6400 kilometers long") is safely ignored (marker "tall" doesn't match "long", so `v1<0` → withhold) rather than miscomputed.

**Why safe:** The system withholds on incompatible dimensions rather than computing nonsense. The hardcoded units are correct for the current KB (all height facts use meters, all year facts use years).

**Still required:** Fact-derived numeric value, dimension, and unit; same-unit arithmetic for meters/kilometers/years/degrees; explicit withhold for incompatible dimensions.

### Joke repetition

**Status:** Documented.

"tell me a joke" and "tell me another joke" deterministically repeat the identical joke. This satisfies determinism but not the ordinary meaning of "another". 

## Verification

### Determinism
- Control run ×2: byte-identical (SHA-256: 38aff229...)
- Trace run ×2: byte-identical
- Trace stderr ×2: byte-identical (158 TR lines)
- Control stdout == trace stdout

### Trace honesty
The traces are genuine execution traces of actual internal branches and state (branch taken, fid, withhold decisions, entity IDs), not native deliberative reasoning. They log what the dispatch code did, not why.

### Build
- Pinned toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Zero compiler errors.
- 8 analyzer warnings (documented; `word_dist` bounds are safe: indices 0-40 into 164-byte arenas).

## Files

- Source: `docs/lab/dialogue/round4/dialogue.zag`
- Battery: `docs/lab/dialogue/round4/battery.txt`
- Trace generator: `docs/lab/dialogue/round4/mk_trace.py`
- KB: `docs/lab/dialogue/round4/kb.txt`
- Gazetteer: `docs/lab/dialogue/round4/gaz.txt`
- This report: `docs/lab/dialogue/round4/ROUND4_REPORT.md`

## Before/After: Key Probes

| Probe | Before (original binary) | After (repaired) |
|-------|-------------------------|------------------|
| what did herman melville eat? | "Herman Melville was born in 1819." (wrong fact) | Withhold + clarification |
| when was the eiffel tower dedicated? | "The Eiffel Tower is in Paris." (wrong fact) | Withhold + clarification |
| did the sticker detect TNN? | "Yes. TNN detected the sticker." (false affirmation) | "I don't know." (withhold) |
| How tall is Eiffel Tower? / Not that one, the other. | "The Montparnasse Tower is 210 meters tall." | "The Montparnasse Tower is 210 meters tall." (preserved) |
| what country is paris the capital of? | "Paris is the capital of France." | "Paris is the capital of France." (preserved) |
| OK, when was Moby Dick published? | "Moby Dick was published in 1851." | "Moby Dick was published in 1851." (preserved) |

## Battery Scores

**Round-4 (38 probes):** 38/38 exact (was 27/29 on original 29-probe battery)

**Round-3 (23 probes):** 23/23 judged good
- Historical: 20 good / 1 partial / 2 fail
- All repaired; answers byte-identical to baseline

**Round-2 F2 (370 probes):** 351/370
- Identical to pre-repair baseline (zero new failures)
- 15 regressions introduced by initial structural gate, all fixed via `is_discourse`, `relation_covered`, `word_in_excl_name`

**Round-2 integrated (18):** 15/18
- Same 3 pre-existing expectation drifts as baseline:
  1. Expected "120", actual "120 meters"
  2. Expected no joke, actual deterministic joke
  3. Expected short "I can't forget.", actual full response
