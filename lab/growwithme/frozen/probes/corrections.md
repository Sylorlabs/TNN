# Correction-stickiness probes — S7 (sealed, 6)

Each asks for the CURRENT (post-correction) version of a corrected fact.
Key = corrected proposition. Scored per `../rubric.md`.

### CORR-01 (targets C1 → F1-01, corrected S3)
Q: What is the current pinned znc toolchain path?
Key: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_c41d9e77`; abed8aa1 was retired after the offset-rule rebuild.

### CORR-02 (targets C2 → F2-02, corrected S3)
Q: What is tier 3 of the memory strength tiers called?
Key: Tier 3 is "sealed", not "pinned" ("pinned" was the v1 name).

### CORR-03 (targets C3 → F1-14, corrected S4)
Q: What is the current scope of the indexed-table aliasing workaround?
Key: The aliasing class covers consecutive same-size `as []i32` and `as []u16` casts; use `[]u8` arenas with explicit little-endian accessors for indexed tables.

### CORR-04 (targets C4 → F2-08, corrected S4)
Q: What are the current write semantics of the audit ledger?
Key: The ledger supports sealed truncation at session boundaries; append-only was the v1 design.

### CORR-05 (targets C5 → F2-07, corrected S5)
Q: How many corroborating probes does tier-2 promotion to tier 3 require?
Key: 2 corroborating probes; the bar was lowered from 3 in the strength-trial rulings.

### CORR-06 (targets C6 → F1-09, corrected S5)
Q: Is a bare `return` legal in a void fn?
Key: Yes — bare `return` is accepted in void fns since the September rebuild; `return;` still works.
