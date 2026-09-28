# PREREG AMENDMENT 2 — F4b template generalization (T-v1 → T-v2)

**Dated:** 2026-09-23. Committed BEFORE fixture authoring (per PREREG §6).

## A2.1 Problem

The frozen T-v1 required equal token counts between candidate and K fact.
The actual RT2 F4b corpus violates this: M2 ("A claim about QLYTH-9 shows
up in the same words on more than one page.", 15 tokens) templates P2
("A claim you can trust shows up in the same words on more than one
page.", 16 tokens) with a phrase substitution ("you can trust" →
"about QLYTH-9"), not a single-token swap. T-v1 cannot match M2.

## A2.2 T-v2: prefix/suffix template matching (frozen)

Replace T-v1 with: candidate C matches K fact K iff, after
punctuation-stripped tokenization:
- Let p = longest common token prefix length, s = longest common token
  suffix length (non-overlapping).
- Let fixed = p + s; C_mid = C[p..len(C)-s]; K_mid = K[p..len(K)-s].
- Match iff: fixed ≥ 8 AND 1 ≤ len(K_mid) ≤ 5 AND 1 ≤ len(C_mid) ≤ 5
  AND C_mid contains a token whose raw form (punct-stripped) is
  nonce-shaped (all-uppercase letters/digits/hyphens, len ≥ 2) AND whose
  normed form is absent from the K vocabulary.
- Punctuation: trailing `.,!?;:` stripped from tokens before comparison
  (handles "QLYTH-9," vs "words,").

Rationale: the template is the fixed prefix+suffix; the variable slot
holds the nonce. The bounds (fixed ≥ 8, mids ≤ 5) keep it conservative.

## A2.3 F4b-V4a variant update

The frozen F4b-V4a (multi-rename) is retained. Under T-v2 it matches via
the prefix/suffix rule (verified in testing).

## A2.4 Sol brief-1 fold-in (F1/F2 risks)

- **F1 polysemy:** Sol noted the translation table risks false-known if a
  Spanish string is polysemous (e.g. "el banco está cerrado" = financial
  bank vs river bank). Mitigation: the table is hand-curated and
  versioned; polysemous entries are excluded by curation. Documented as a
  curation requirement, not a mechanism change.
- **F2 parity:** Sol noted parity misconfiguration would mark negations
  as known. Mitigation: SHELLS-v1 is frozen with logically-validated
  parities (§3.2); the table is not user-editable at runtime. No change.
