# Discount Pilot Implementation

**Verdict: DISCOUNT-IMPL-COMPLETE: RECOVERABLE.**

The minimal discount subset (D1+D2+W3+R1) was implemented on an unfrozen
variant and replayed against the contradiction-break battery. The
permanent break is now bounded: recovery occurs within T+1 = 3 failed
bootstraps, exactly as the specification predicted. The contradicting
fact is excluded from evidence, not deleted.

## 1. Implementation

Variant `di_variant.zag`: verbatim frozen copy (`di_base.zag`, SHA-256
`a29972ca...` verified) with `bootstrap_miss` replaced (file
`di_boot.zag`, spliced at the original function boundaries). Original
test `main` removed; driver `di_driver.zag` appended (`di_full.zag`).

Changes, and only these:

- **D1:** per-FACT discount in field 12. Verified free on tag-1 FACT
  nodes (grep: all other field-12 uses are graph cells tags 101/102,
  MAP tag 20, and allocator zeroing). The allocator already zeroes
  field 12 at creation, so no init change was needed.
- **D2:** threshold T=2 hardcoded as the constant `2` in the scan
  filter and exclusion check.
- **W3:** on non-unanimous evidence with a strict majority
  (`modal_count * 2 > counted`), each counted FACT whose value differs
  from the modal value gets `discount += 1`. Ties write nothing. Node
  indices are tracked in a parallel array (`ex_n`) so the minority
  facts can be identified.
- **R1:** the evidence scan skips FACTs with `discount > 2`. Scan is
  otherwise unchanged (most-recent-first, relation filter, cap 6).

Not implemented (per the minimal-subset instruction): W1/W2
(observe-path writes), D3 (confirmation floor), R2/R3 (retrieval/trial
read paths).

Cognition diff vs frozen: only `bootstrap_miss` changed. All other
functions byte-identical to the frozen base.

## 2. Method

Driver replicates the contradiction-break battery (`510b6cb42`)
Phases 1-5, with discount visibility:

- Phase 1: seed 3 genuine facts (1001/1002/1003, r=50, v=42).
- Phase 2: 4 fresh-subject queries (2001..2004), masked, expected -2.
- Phase 3: contradiction `ev_teach(3001,50,99)`.
- Phase 4: 6 fresh queries (2005..2010).
- Phase 5: 2 more fresh queries (2011,2012).

After each query the driver prints the query result, the
contradiction fact's discount, and the R1-filtered evidence window
with per-node discount values. 3/3 byte-identical runs (SHA-256
`d901937e...`).

## 3. Results (3/3 identical)

| Step | Result | contra discount | Interpretation |
|------|--------|-----------------|----------------|
| q0..q3 | 42,42,42,42 | n/a | loop established, discount untouched |
| contra taught | idx14 | 0 | contradiction enters window top |
| b0 | -2 | 0 -> 1 | W3 fires: strict majority 5x42 vs 1x99 |
| b1 | -2 | 1 -> 2 | W3 fires again; 99 still eligible (2 <= 2) |
| b2 | -2 | 2 -> 3 | W3 fires; 99 now at discount 3 |
| b3 | **42** | 3 | R1 excludes 99 (3 > 2); six 42s unanimous |
| b4 | 42 | 3 | loop resumed |
| b5 | 42 | 3 | loop resumed |
| p0,p1 | 42,42 | 3 | recovery persistent |

Window transcript (post-query scans):

- r50 (contra taught): `idx14 s3001 o99 d0` counted at window top.
- r60 (post-b0): `idx14 s3001 o99 d1` still counted.
- r61 (post-b1): `idx14 s3001 o99 d2` still counted.
- r62 (post-b2): idx14 absent from window (excluded); six 42s remain.
- r63 (post-b3): six 42s, bootstrap fired, new 42-fact taught.

Every value matches the specification's predicted replay (DISCOUNT.md
3.2) exactly: three failed bootstraps, then recovery.

## 4. What was confirmed

1. **Recoverability.** The permanent break is bounded. Cost: T+1 = 3
   wasted queries vs infinite (frozen) vs 6 external teaches
   (contradiction-break Phase 6 recovery).
2. **No deletion.** The 99-fact persists in the store at discount 3.
   It is excluded from bootstrap evidence only; `activate` would
   still return 99 for (3001,50). Rehabilitation (W2) could
   re-admit it; W2 is not in this pilot.
3. **Reachability.** All write paths fired from the initial state
   with no precondition: W3 fired on the first non-unanimous
   bootstrap. No circular dependency (unlike H3-lite Node 2).
4. **Unanimity gate intact.** b0..b2 still returned -2; the gate
   was not weakened. Discount adds the exit without removing
   the stop.
5. **Determinism.** 3/3 byte-identical transcripts.

## 5. Honest limits (carried from the spec)

- The pilot is source-blind, as specified: W3 excluded the only
  genuine evidence (the 99) to preserve a self-referential loop of
  42s. Fragility is fixed; the epistemic problem is not.
- T=2 is a researcher constant, not learner-chosen. Sensitivity
  at T=1/3 was not run in this pilot.
- W1/W2 (observe path) untested here; Phase 7 of the original
  battery (`ev_observe` contradiction) was not replayed.
- No claim beyond the pilot: bounded L2 mechanism, not L3, not a
  learner-internal criterion, not a fix for the V2 hole or
  source conflation.

## 6. Standing metrics (this implementation)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 7 (field layout, T=2,
  strict-majority definition, W3 trigger, R1 exclusion rule,
  parallel index array, tie abstention)
- LEARNER-OWNED STRUCTURAL DECISIONS: per-fact discount values
  (1 fact reached discount 3 in this battery; the values are
  learner-writable and experience-driven)
- SOURCE-ENUMERABLE FORMS: 0 new
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0 (criterion is researcher-authored)
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: ~45 added (pilot `bootstrap_miss` only, variant)
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

## 7. Deliverables

All in `docs/lab/research-lead/overnight-20260928/discount_impl/`:

- `NAMECHECK.md` (Step 0 toolchain guard, scope, provenance)
- `DISCOUNT_IMPL.md` (this report)
- `di_base.zag` (verbatim frozen copy, SHA-256 verified)
- `di_boot.zag` (replacement `bootstrap_miss`)
- `di_variant.zag` (base with pilot splice, no main)
- `di_driver.zag` (battery driver)
- `di_full.zag` (compiled unit)
- `di_bin` (pinned-znc binary)
- `di_run1.txt`, `di_run2.txt`, `di_run3.txt` (3/3 byte-identical,
  SHA-256 `d901937e4aa55384cd52c82b061ba8f5281f9bfbf4209b19c1579ff7ee7f5a18`)

**Verdict: DISCOUNT-IMPL-COMPLETE: RECOVERABLE.**
