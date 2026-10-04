# PREREG_K6_AMEND.md -- Fresh prereg: repair K6 measurement instrument

Frozen before the repair. This amends ONLY the K6 measurement procedure
from PREREG.md (commit 447f087af). It does not alter the implementation
(commit fd79576d4), the 8 frozen operand-encoding changes, or any kill
bar's intent. Transparent amendment per governance: the original K6
procedure proved unexecutable (W-SEMREG, commit 2d98e3ecd), so the
instrument is repaired instead of the bar being weakened.

## Why the amendment is needed

W-SEMREG built old/new test binaries (s6_base/oe_base + s6_patch +
run_all main) and both panicked byte-identically before any test ran:
every t_* battery test allocates `z_alloc(110656)`, but the current
layout's edge area (`eoff(e) = 2621504 + e*16`, 131072 edges) requires
~4.7MB. The working driver allocates `z_alloc(4722752)`
(s6_driver.zag line 42). The 110656 size is a fossil; `run_all` was never
executed on this base lineage (s6_run1.txt contains zero test lines).
`tnn2_init`, `es`, `z_alloc` are byte-identical old/new, so the panic is
pre-existing and independent of the operand fix. Differential evidence so
far: zero observable divergence (byte-identical panic, identical warning
counts, source diff confined to the frozen operand hunks).

K6 as frozen requires: identical per-test PASS/FAIL vectors old-vs-new
AND t_t2_revise passing on the new build. That is the bar; it is not
lowered. This amendment only makes the battery executable.

## Frozen repair procedure

1. Copy `scaling_5000_fixed/s6_base.zag` -> `/tmp/k6fix_old_base.zag`
   and `operand_encoding_fix/oe_base.zag` -> `/tmp/k6fix_new_base.zag`.
   (Copies only; the committed bases are never modified.)
2. Mechanical replacement, identical on both copies:
   `z_alloc(110656)` -> `z_alloc(4722752)` (49 occurrences each, all of
   the form `let W:[]u8=z_alloc(110656); tnn2_init(W);` inside t_*
   test functions, lines 828+). No other edit. Verify by diff that the
   old/new repaired copies differ ONLY by the frozen operand-encoding
   hunks + the uniform allocation change.
3. Build `/tmp/k6fix_old.zag` = repaired-old + s6_patch.zag (verbatim) +
   runall main (calls run_all()); `/tmp/k6fix_new.zag` = repaired-new +
   s6_patch.zag (verbatim) + runall main. Compile both with safebin
   pinned znc. Pure Zag; NAMECHECK.md Step 0 applies.
4. Run both binaries; capture full stdout.
5. K6 verdict rule (unchanged intent): PASS iff per-test PASS/FAIL
   vectors are identical old-vs-new AND T2-REVISE passes on the new
   build. Document t_c6 status on both (audit predicts FAIL on both;
   confirm empirically). Any divergence -> K6 FAIL with exact test
   names; no reinterpretation.

## What this amendment explicitly does NOT authorize

- No change to res_op, execute, encoders, or any operand logic.
- No change to t2_sig, the patch, or the driver.
- No weakening of K1-K5 or the K6 pass criteria.
- The repaired copies are measurement scaffolding in /tmp, not a new
  base revision; they are not committed as base files.
