# Seal: Family X Assignment

**Sealed:** 2026-09-29
**Document:** PI_FAMILY_X_ASSIGNMENT.md
**SHA-256:** 6438bc799b8c29fe3c60f73ca0082c57fea31ec5d7037c01513db874200fbc9d

This hash binds the family definition, training examples, pass bars X1-X5,
and the change restrictions. Any alteration to the assignment after this
commit is detectable by recomputing the hash.

**Hidden-test status:** No hidden-test content exists at seal time (per G4).
Four fixed hidden cases are disclosed in the assignment; four more will be
generated at reveal time with a fresh published seed via the frozen
gen_hidden_inputs.sh. The reveal report will publish the seed so the full
8-case hidden set is auditable post-hoc.

**Verification:** `sha256sum PI_FAMILY_X_ASSIGNMENT.md` must equal the hash
above. Mismatch means the assignment was tampered with after sealing.
