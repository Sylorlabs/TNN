# PREREG AMENDMENT 1 — F5 review fold-in (Sol brief 3)

**Dated:** 2026-09-23. Committed BEFORE any fixture is authored or any
fix-fork line is written (per PREREG §6). This amends ONLY §3.2 (F5
variants) and §4 (F5 N-v1); all other sections unchanged.

## A1.1 N-v1 change: add U+00AD to the Cf strip list

Sol (swe-1-6-slow:free) noted the soft hyphen U+00AD — an invisible Cf
format character — was missing from the N-v1 strip list. It is added:
strip Cf {U+200B, U+200C, U+200D, U+FEFF, U+2060, U+180E, **U+00AD**}.
Rationale: U+00AD is a default-ignorable format character like the
zero-width set; stripping it cannot create a false-known beyond what the
frozen skeleton already risks, and it closes an invisible-character gap
in the same class as F5 itself.

## A1.2 New F5 variant corpora (from Sol's adversarial list)

- `F5-V5f` diacritic decomposition (boundary): P1 with `é` as U+00E9 on
  all pages vs K's `e` + U+0301 form (or vice versa — one fixed choice,
  authored from this spec). N-v1 implements NO canonical decomposition
  (NFD/NFC); the forms stay byte-distinct after norm. Expected: **NOVEL,
  installs** (documented hole, safe direction — over-novelty).
- `F5-V5g` soft hyphen: P1 with U+00AD inside a word, 3 pages. Expected:
  **EMPTY** (stripped per A1.1).
- `F5-V5h` mathematical alphanumerics (boundary): P1 in Mathematical Bold
  (U+1D400 block). N-v1 does NOT map the U+1D400–U+1D7FF blocks (fixture
  scope is the frozen skeleton). Expected: **NOVEL, installs**
  (documented hole, safe direction).
- `F5-V5i` mixed-script injection: P1 with one skeleton-covered Cyrillic
  homoglyph inside an otherwise Latin word (e.g. `p` + Cyrillic `а`).
  Expected: **EMPTY** (skeleton maps it).

## A1.3 Explicitly NOT adopted

- Full NFD/NFC canonical decomposition: a larger table change; the hole
  it leaves is false-novelty (safe). Recorded as a known boundary, not
  implemented in this workstream.
- U+1D400–U+1D7FF mathematical alphanumeric folding: same reasoning —
  boundary, not implemented.
- Sol's false-known warning on the skeleton is already the prereg's
  position: unmapped scripts stay novel (§3.2 F5-V5d); the skeleton is
  fixture-scoped and frozen.

## A1.4 Consultation status

Brief 3 (F5) returned a full review (folded in above). Brief 2 (F3/F4)
returned a full review (folded into the frozen prereg). Brief 1 (F1/F2)
is still pending (free-tier rate limits); per §6, any variant it yields
will be handled by a further dated amendment before fixture authoring,
or recorded as not received before the build phase begins.
