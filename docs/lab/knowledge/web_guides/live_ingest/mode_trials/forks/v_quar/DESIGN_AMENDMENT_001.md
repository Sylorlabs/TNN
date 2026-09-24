# V-QUAR Design Amendment 001

Date: 2026-09-24. Author: H3 workstream (Fork F3).

This amendment records deviations from `DESIGN_FROZEN.md` discovered during
implementation. The frozen V-PARA rule (numeric-signature agreement, Jaccard
≥ 0.60, ≥2 hosts, injection-clean) is UNCHANGED. Only the mechanisms below
changed, for the stated reasons.

## 1. Raw-reader internal call fix (generator bug, not compiler bug)

**What changed:** In `gen_sources.py`, the extracted raw readers
`qraw_read_path`/`qraw_read_file` now have their INTERNAL call sites renamed
to the `qraw_` versions. Previously the body of `qraw_read_path` still called
`read_file(...)`, which resolved to the instrumented wrapper and caused every
merge-gate Q read to be REFUSED.

**Why:** The E2 rename only renamed function definitions, not call sites
inside the extracted bodies. The observed "compiler miscompile" (merge
accessor refused, `strace` showing no file open) was this generator bug.
Verified by reading the generated source: the call site said `read_file(`
instead of `qraw_read_file(`.

**Impact:** Invalidates all merge runs before 2026-09-24 14:00 UTC. The C2
train pass `runs/c2_train_p1` (first version) is VOID. All evidence in
`RESULTS_H3.md` comes from runs after this fix.

## 2. SHA-256 Q chain (was FNV-1a-64)

**What changed:** The quarantine ledger chain (`qprev`, `csha` in
`run_vquar.py`) now uses SHA-256 instead of FNV-1a-64.

**Why:** The assignment requires "separate SHA chains" for P and Q. The P
chains (`sha_log`, `sha_knowledge`, `sha_refusal` on the DONE line) already
used SHA-256. The Q chain was FNV-1a-64. Now both are SHA-256, with separate
chains (P: log/knowledge/refusal; Q: quarantine ledger).

**Note:** FNV-1a-64 remains in the Zag instrument for content-free audit tags
(`AUDIT|...|slot16|content16`, `QAUDIT|...`). Those are path/content tags,
not ledger chains. The ledger chains (Python orchestration) are SHA-256.

## 3. Raw readers moved before wrappers (codegen ordering)

**What changed:** In the generated sources, the `qraw_` raw reader
definitions are emitted BEFORE the instrumented `read_file`/`read_path`
wrappers (which now live in `qa_audit.inc` after the raw block).

**Why:** Defensive ordering; the wrappers call the raw readers, so defining
raw first avoids any forward-reference codegen risk. No behavior change.

## 4. CI check updated for `qraw_` names

**What changed:** `check_no_direct_q.sh` now checks for `qraw_read_path`/
`qraw_read_file` (was `read_path0`/`read_file0`). The allowed caller set is:
`read_file`, `read_path` (wrappers), `qread_claim` (single accessor),
and `qraw_read_path`/`qraw_read_file` themselves (internal).

**Why:** The generator was updated to use `qraw_` names; the CI check was
stale. Revalidated: passes on all three generated sources.

## 5. R1 driver cwd fix

**What changed:** `run_r1.py` now runs instruments with `cwd=OUTDIR`
(was `cwd=HERE`, the vquar dir). The first R1 run produced empty verdicts
because it read state from the wrong directory.

**Why:** Bug fix. The void run is discarded; all R1 evidence comes from the
corrected run.

## What did NOT change

- The frozen V-PARA quarantine rule (thresholds, stoplist, clustering).
- The P decision path (byte-identical to frozen `webg.zag`; proven by
  `runs/fb_integrity` ledger comparison).
- The merge gate (deterministic strict-G4 re-verification; single accessor;
  one verdict bit).
- The read-check enforcement (wrapper refusal + audit).
