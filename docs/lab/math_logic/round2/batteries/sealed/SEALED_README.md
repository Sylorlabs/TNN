# Sealed solutions - MATH R2 extended batteries

Contents: SEALED_B4X.sol (15 verdicts), SEALED_B5X.sol (60 verdicts),
SEALED_B6X.sol (3 verdicts), SEALED_B7F.sol (20 verdicts),
SEALED_B7F_NL.md (20 NL texts), SEALED_B7F_FORM.sol (20 formal analogs).

Grading rules (frozen with the prereg):
- B4X/B6X: verdict DERIVED iff the target follows from premises + the
  referenced store via the committed schemas (S_MP, S_PBC, S_UI).
- B5X: verdict computed from TRUSTED premises + KB_B5X_BASE (injection
  excluded). Engines see the injected copies; the gap measures
  contradiction tolerance. Kind D -> DERIVED, kind W -> WITHHELD.
- B7F: formalization scored by b7f_checker.py against SEALED_B7F_FORM.sol;
  verdicts in SEALED_B7F.sol (19/20 WITHHELD: affirming the consequent).

Guard: any engine input path containing 'sealed' exits 3 (round-1 pattern).
