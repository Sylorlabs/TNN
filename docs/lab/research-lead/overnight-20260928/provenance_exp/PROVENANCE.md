# Provenance Experiment: Source-Aware Bootstrap

**Verdict: PROVENANCE-COMPLETE: FIXES (with documented tradeoff).**

Source tags at first FACT write prevent the learner's own guesses from
becoming independent evidence for themselves. In the majority-wrong
adversary, treatment eliminates wrong-inference persistence (10/10 to
0/10), truth exclusion (discount 3 to 0), and self-amplification
(15 to 4 inferred facts). The tradeoff: treatment also withholds
instead of "recovering" when external evidence is genuinely
contradictory.

## 1. Design

### 1.1 Source tags (field 16, tag-1 FACT nodes)

Field 16 verified free on tag-1 nodes (only allocator-zeroed; production
reads are graph cells and MAP nodes). Written at first FACT write:

| Value | Source | Write path |
|-------|--------|------------|
| 0 | UNKNOWN | allocator default, guides |
| 1 | OBSERVED | ev_observe (via ev_teach_in, overwritten) |
| 2 | TAUGHT | ev_teach |
| 3 | INFERRED | ev_teach_in (default; bootstrap) |
| 4 | PREDICTED | promote_graph (trial, overwritten) |
| 5 | REVISED | t2_revise_graph (overwritten) |
| 6 | DERIVED-FROM-STRUCTURE | reserved; no MAP fact-write path found |

Six edits to base (verbatim frozen copy, SHA-256 `a29972ca...` verified).
Both arms include tags; control does not read them (behavior identical
to tagless).

### 1.2 Treatment: source-aware bootstrap_miss

Partition: EXTERNAL = {1,2,5} (OBSERVED, TAUGHT, REVISED).
SELF = {3,4,6} (INFERRED, PREDICTED, DERIVED).

Rules:
- **Unanimity:** requires unanimous EXTERNAL facts (at least one).
  SELF facts do not vote. Firing threshold `ecnt >= k` (external count).
- **W3 majority:** computed over EXTERNAL facts only. Strict external
  majority required. Only external minority facts discounted.
- **R1/D1/D2:** unchanged (discount in field 12, T=2, skip discount > 2).

Control: source-blind D1+D2+W3+R1 (verbatim discount pilot).

### 1.3 Batteries

Battery 1: Discount replication (contradiction-break Phases 1-5).
Battery 2: Majority-wrong adversary (Phases 1-3; M1 persistence,
M2 exclusion depth, M4 amplification).

## 2. Results (3/3 byte-identical per arm)

Control SHA-256: `2c0f9dac9df638138bdfa3ad57cce8f48bdb9529cc731ee37f6aa319023906cf`
Treatment SHA-256: `6957d3dea7be0542743b762a25d0f488844f9e4f0d35ea34045a260a83a095d5`

### 2.1 Battery 1: Discount replication

| Step | Control | Treatment |
|------|---------|-----------|
| q0..q3 | 42,42,42,42 (inferred 1..4) | 42,42,42,42 (inferred 1..4) |
| b0..b2 | -2,-2,-2 (disc 1,2,3) | -2,-2,-2 (disc 0,0,0) |
| b3..b5 | 42,42,42 (disc 3; inferred 5..7) | -2,-2,-2 (disc 0; inferred 4) |
| p0,p1 | 42,42 | -2,-2 |

Control replicates the discount pilot exactly: W3 discounts the 99 to 3,
R1 excludes it, the 42-loop resumes and amplifies (4 to 7 inferred).

Treatment: W3 never fires. The 99 stays at discount 0. The system
withholds (-2) permanently. No self-amplification (inferred stays at 4).

Why: after the 99 is taught, the 6-slot window holds [99(T), 42(I)x4,
42(T)]. External votes: 1x99 vs 1x42. No strict external majority
(1*2 > 2 is false). W3 does not fire. The apparent 5:1 majority was
an illusion created by the learner's own INFERRED guesses.

### 2.2 Battery 2: Majority-wrong adversary

| Metric | Control | Treatment |
|--------|---------|-----------|
| M1 wrong 42/10 | 10 | 0 |
| M2 contra discount | 3 (excluded) | 0 (not excluded) |
| M4 inferred total | 15 | 4 |

Control: the predicted damage occurs. W3 discounts the genuine 99,
the wrong 42-loop resumes, 10/10 fresh queries return wrong 42s,
and the loop amplifies from 4 to 15 inferred facts.

Treatment: complete prevention. Zero wrong inferences. The 99 is never
discounted. No amplification. The system withholds (-2) rather than
confidently inferring the wrong value.

## 3. Interpretation

### 3.1 Hypothesis confirmed

Source-aware evidence prevents the learner's own guesses from becoming
independent evidence for themselves. The treatment eliminates all three
adversarial harms (M1, M2, M4) by refusing to count SELF votes in the
unanimity and majority calculations.

### 3.2 The tradeoff (honest)

Treatment does not "recover" in Battery 1. When external evidence is
genuinely contradictory (TAUGHT 42s vs TAUGHT 99), the treatment
withholds permanently instead of resuming 42.

This is epistemically honest: the control's "recovery" was suppressing
genuine external evidence (the 99) to preserve a partly self-generated
loop. The treatment refuses to do this.

The tradeoff is explicit:
- Control (discount): robust (recovers from contradiction) but can
  entrench wrong majorities (adversary M1=10/10).
- Treatment (provenance): never entrenches (M1=0/10) but withholds
  instead of recovering from genuine external contradictions.

Neither is "correct" in all worlds. The choice depends on whether the
deployment values robustness (keep inferring) or honesty (withhold on
conflicting external evidence).

### 3.3 What provenance does not solve

If the misleading evidence is EXTERNAL (e.g., 3 TAUGHT 42-seeds that
are wrong, vs 1 TAUGHT 99 that is right, with no INFERRED facts in the
window), provenance cannot distinguish them. Both have src=2. The
treatment would compute an external 3:1 majority and discount the 99.

Provenance solves the SELF-amplification problem, not the
"wrong external majority" problem. The latter requires truth-tracking,
which the learner does not have.

## 4. Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 9 (field 16, 6 tag values,
  external/self partition, unanimity rule, W3 rule, 5 write-path edits)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0 (tag values are researcher-defined;
  learner does not choose them)
- SOURCE-ENUMERABLE FORMS: 0 new
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0 (criterion is researcher-authored)
- REUSE EVENTS: 0. REVISION EVENTS: 0.
- COGNITION LINES: ~75 added (treatment bootstrap_miss; variant only)
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.
- One-System Rule: holds. No new modes, bridges, handlers, or node types.
  Source tags reuse an existing free field.

## 5. Deliverables

All in `docs/lab/research-lead/overnight-20260928/provenance_exp/`:

- `NAMECHECK.md` (Step 0 toolchain guard, scope, input provenance)
- `PROVENANCE.md` (this report)
- `pv_base.zag` (verbatim frozen copy, SHA-256 `a29972ca...`)
- `pv_src.zag` (base + 6 source-tag writes, no main, no bootstrap_miss)
- `pv_nomain.zag` (pv_src truncated before run_all)
- `pv_boot_ref.zag` (control: verbatim discount pilot bootstrap_miss)
- `pv_boot_trt.zag` (treatment: source-aware bootstrap_miss)
- `pv_driver.zag` (both batteries, both arms)
- `pv_full_ctl.zag`, `pv_full_trt.zag` (compiled units)
- `pv_bin_ctl`, `pv_bin_trt` (pinned-znc binaries)
- `pv_ctl_run1/2/3.txt` (3/3 byte-identical, `2c0f9dac...`)
- `pv_trt_run1/2/3.txt` (3/3 byte-identical, `6957d3de...`)

**Verdict: PROVENANCE-COMPLETE: FIXES (with documented tradeoff).**
