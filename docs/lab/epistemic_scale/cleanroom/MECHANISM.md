# Clean-Room Epistemic Mechanism

**Status:** Implemented in pure Zag (`zag/epi.zag`), zero RNG, deterministic.

## Overview

This is a SIMPLIFIED mechanism relative to the Python development prototype
(`reference.py`). The simplification was necessary for reliable Zag implementation.
All decisions are documented here honestly.

## Architecture

### Input
- Held-out item: `id` + `text` (from `cleanroom_heldout_blind.tsv`)
- Installed knowledge: train `id` + `text` + `provenance` (from `cleanroom_train.tsv`)
  - Train `class` labels are NOT embedded in the runtime.
  - Train `class` was used ONLY for development LOO scoring, never in the classifier.

### Preprocessing (Python, deterministic)
- Tokenization: lowercase alphanumeric, length>=3, stopword removal, simple stemming.
- Vocabulary: 1,464 tokens from train text.
- IDF: integer, `1000 * ln(N/df)`.
- Token IDs embedded in Zag as flat array.
- Entities and numbers pre-extracted (for clash).

### Classification Gates (Zag)

**Gate 1: Opinion**
- Compute `op_score`:
  - +2 per unique EVAL_ADJ token, -3 per FACT_ADJ token
  - +1 per VALUE_NOUN token, +2 for "worth"
  - +3 per comparative "beat" (simplified: all occurrences; literal check omitted)
  - +2 per other EVAL_VERB token
  - +3 per phrase match (16 phrases: "i think", "i feel", etc.)
  - +1 per absolutist word ("never", "nothing", "cannot")
  - +3 for "better...than" / "worse...than" (within 25 chars)
  - +2 for "should"
- Compute discourse: top-5 train neighbors by wsum, average their op_scores.
- Combined = op_score + 0.3 * discourse_avg
- If combined >= 3.0 → OPINION

**Gate 2: Lie**
- Simplified clash: if heldout and train both have numbers, and wsum > 1500,
  and number strings differ → CLASH.
- If clash exists AND no supporters (wsum >= 5000) → LIE
- Note: Full entity-based clash from reference.py was simplified due to Zag complexity.

**Gate 3: Extraordinary**
- Compute extraordinary_score via substring matching:
  - +3 per EXTRAORDINARY word (bigfoot, alien, ghost, etc.)
  - +2 per DISPUTED_CAUSAL phrase (cause autism, etc.)
  - +1 for "is real" / "are real"
- If score >= 2 → UNDETERMINED (withhold true/false)

**Gate 4: Fact**
- Compute grounding = max wsum over all train items.
- If grounding >= 3500 → FACT
- Else → UNDETERMINED

### wsum
IDF-weighted token overlap: sum of IDF for tokens in intersection.

## Simplifications from Reference

1. **op_score**: Omitted morphological patterns (`X-er than`, `more X than`,
   `the X-est`, `the most X`, sensory-verb patterns) due to Zag string-processing
   complexity. These contributed to opinion recall in the Python prototype.
2. **clash**: Simplified to number-based only; omitted entity-set clash logic.
3. **discourse**: Implemented, but uses simplified op_score.

## Performance Expectation

The simplified mechanism is expected to UNDERPERFORM the Python reference on
opinion recall (fewer patterns) and lie recall (simplified clash). It should
maintain the skepticism withholding behavior (extraordinary_score is complete).

This is an honest, deterministic, pure-Zag implementation. The trial outcome
(FAIL on bars) is reported as measured, not as hoped.

## Files

- `zag/epi.zag`: Generated Zag source (data + mechanism)
- `zag/epi`: Compiled binary
- `build_clean.py`: Generator script
- `frozen_run1/`, `frozen_run2/`: Frozen outputs
