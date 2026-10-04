# REPORT: NT-CAPACITY-SWEEP -- the D6 assoc pin's opportunity-cost curve

## Verdict

**CURVE-CONFIRMED** per the frozen verdict mapping (PREREG
Section 8). All three arms hit their frozen exact predictions on
the first implementation run, 3/3 byte-identical:

- ARM20 (CAP=20): S1=1 S2=1 S3=1 S4=1 S5=1 -> COST-CONFIRMED
- ARM22 (CAP=22): R1=1 R2=1 R3=1 R4=1 R5=1 R6=1 R7=1 -> REPRODUCED
- ARM24 (CAP=24): T1=1 T2=1 T3=1 T4=1 T5=1 -> SLACK-CONFIRMED

## Frozen results (3/3 byte-identical)

- Run digest: `614e046b9d906a4e32ead8b6a05ce8225e6f03abfeae15fa566d4426eecda6a6`
- Binary digest: `a25cb20ce53113c62c64ded35a621a1ed6671679cd4f4e25cbb096d245908415`
- Source digest: `80cf0e57c6752c0fd9797aecff54d8a9834b51e52ac0f9ef7f76bae78762528a`

```
NTSWEEP R6-CAP20 ttcA=2 probeA=8 nevict=30 phev=1
NTSWEEP R6-CAP20 PPROBE100 p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail100=4
NTSWEEP R6-CAP20 PPROBE160 r1=1 r2=1 r3=1 r4=1 r5=1 r6=1 avail160=4
NTSWEEP R6-CAP20 RET c=2 nc=2 u=3 forget=1 bprobe=0 resprobe=1
NTSWEEP R6-CAP20 ASSOC apin=4 dec=1 res=1 useless=2 fprate=50 evh160=0 evh161=0 evh170=0 evh171=0
NTSWEEP R6-CAP20 EVHIST 118=1 131=6 140=6 141=6 143=6 144=5
NTSWEEP R6-CAP20 S1=1 S2=1 S3=1 S4=1 S5=1
NTSWEEP R6-CAP20 ARM-VERDICT=COST-CONFIRMED
NTSWEEP R6-CAP22 ttcA=2 probeA=8 nevict=22 phev=0
NTSWEEP R6-CAP22 PPROBE100 p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail100=4
NTSWEEP R6-CAP22 PPROBE160 r1=1 r2=1 r3=1 r4=1 r5=1 r6=1 avail160=4
NTSWEEP R6-CAP22 RET c=2 nc=2 u=4 forget=0 bprobe=1 resprobe=1
NTSWEEP R6-CAP22 ASSOC apin=4 dec=1 res=1 useless=2 fprate=50 evh160=0 evh161=0 evh170=0 evh171=0
NTSWEEP R6-CAP22 EVHIST 140=5 141=6 143=6 144=5
NTSWEEP R6-CAP22 R1=1 R2=1 R3=1 R4=1 R5=1 R6=1 R7=1
NTSWEEP R6-CAP22 ARM-VERDICT=REPRODUCED
NTSWEEP R6-CAP24 ttcA=2 probeA=8 nevict=10 phev=0
NTSWEEP R6-CAP24 PPROBE100 p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail100=4
NTSWEEP R6-CAP24 PPROBE160 r1=1 r2=1 r3=1 r4=1 r5=1 r6=1 avail160=4
NTSWEEP R6-CAP24 RET c=2 nc=2 u=4 forget=0 bprobe=2 resprobe=1
NTSWEEP R6-CAP24 ASSOC apin=4 dec=1 res=1 useless=2 fprate=50 evh160=0 evh161=0 evh170=0 evh171=0
NTSWEEP R6-CAP24 EVHIST 143=5 144=5
NTSWEEP R6-CAP24 T1=1 T2=1 T3=1 T4=1 T5=1
NTSWEEP R6-CAP24 ARM-VERDICT=SLACK-CONFIRMED
NTSWEEP VERDICT=CURVE-CONFIRMED
```

## The curve (frozen numbers)

| CAP | pressure | avail160 (rescue) | FP useless/apin | opportunity cost | nevict |
|-----|----------|-------------------|-----------------|------------------|--------|
| 20  | 1.25x    | 4 (YES)           | 2/4 (50%)       | YES: 118 displaced, u=3, forget=1, phev=1 | 30 |
| 22  | 1.14x    | 4 (YES)           | 2/4 (50%)       | none (u=4, forget=0, phev=0) | 22 |
| 24  | 1.04x    | 4 (YES)           | 2/4 (50%)       | none (u=4, forget=0, phev=0) | 10 |

## Kill-bar evaluation

- ARM20: S1=1 (ttcA=2, probeA=8). S2=1 (rescue holds: avail160=4,
  resprobe=1, evh160=evh161=0). S3=1 (FP confirmed: dec=1,
  useless=2). S4=1 (opportunity-cost signature exact: phev=1,
  evh118=1, u=3, forget=1, nc=2, c=2). S5=1 (pressure exact:
  nevict=30, evh148=0, EVHIST 118=1,131=6,140=6,141=6,143=6,144=5,
  bprobe=0). -> COST-CONFIRMED.
- ARM22: R1-R7 all 1; every number matches the NT-TEACHASSOC
  frozen run (ttcA=2, probeA=8, nevict=22, EVHIST
  140=5,141=6,143=6,144=5, u=4, forget=0, bprobe=1, apin=4,
  dec=1, useless=2). -> REPRODUCED (regression bar green).
- ARM24: T1=1, T2=1 (rescue holds), T3=1 (FP confirmed), T4=1
  (no opportunity cost: phev=0, evh118=0, u=4, forget=0),
  T5=1 (pressure exact: nevict=10, EVHIST 143=5,144=5,
  bprobe=2). -> SLACK-CONFIRMED.

## What this establishes

1. **The opportunity cost is a threshold phenomenon, not a
   gradient.** At CAP=20 the four assoc pins structurally
   displace A-link 118 on pass 2: with D5 pinning {130,148} and
   assoc pinning {160,161,170,171}, every R=0 slot is pinned, so
   the victim scan falls through to R=3 A-links and takes the
   youngest (118, ins 14). 118 is never restored (teachB never
   teaches it), so retest q(117) misses: u=3, forget=1, phev=1.
   At CAP=22 and CAP=24 no uncontested structure is lost (u=4,
   forget=0, phev=0 on both). The cost appears discretely when
   pins + pressure leave zero unpinned low-read slots.
2. **The rescue is capacity-invariant across the tested range.**
   avail160=4 and evh(160)=evh(161)=0 on all three arms; D6
   protects the residual chain at 1.25x, 1.14x, and 1.04x alike.
3. **The false-positive cost is capacity-invariant too.**
   useless/apin = 2/4 (fprate=50) on all three arms: the decoy
   chain is assoc-pinned and protected to end-of-run everywhere,
   never contributing to a successful query. Pinning useless
   entries is not free at any tested capacity -- at CAP=20 the
   price is an A-link; at CAP=22/24 the price is 2 occupied
   slots that the churn must work around (nevict absorbs it).
4. **At CAP=24 the pins are redundant for the residual but still
   cost the FP slots.** Trace inspection (not a tested
   counterfactual): after pass 1 the residual accumulates probe
   reads and is never an eviction candidate, so reads alone
   would likely keep it safe; D6's only material effect at
   CAP=24 is protecting the decoy (without D6 the pass-1 victim
   would have been 171, the youngest R=0 slot, instead of 144).
   Benefit redundant, FP cost persisting -- the honest
   characterization of the slack regime.
5. **The revision machinery is untouched by the displacement.**
   At CAP=20, c=2 and avail100=4 hold: D5's revision of 100->148
   and 104->130 proceeds normally. The cost fell specifically on
   uncontested retention (the U partition), not on revision.
6. **bprobe is a capacity side-channel, not a bar.** bprobe=0
   at CAP=20 (131 absent at end breaks q(130)'s second hop; 140
   and 143 absent), 1 at CAP=22, 2 at CAP=24 (slack lets both
   140 and 141 survive, so q(140)=142 hits). It tracks how much
   of the novel inventory survives, which is exactly what the
   capacity parameter controls.

## Answers to the frozen key questions

- (a) At what capacity does the opportunity cost become
  unacceptable? At CAP=20 (1.25x) in this world: an A-link is
  displaced (phev=1), uncontested retention drops (u=3), and a
  forgetting event is recorded (forget=1). At CAP=22 (1.14x)
  there is no retention cost.
- (b) Is there a capacity where D6's benefit outweighs its cost?
  Yes: CAP=22 -- full rescue (avail160=4) with zero retention
  cost (u=4, forget=0, phev=0); the only cost is the 2 useless
  pinned slots (FP 50%), which the eviction churn absorbs
  without displacing anything. At CAP=24 the benefit is
  redundant while the FP cost persists, so CAP=22 is the
  sweet spot in this world, not CAP=24.
- (c) Shape of the tradeoff curve: rescue YES at all three
  points; FP cost 50% at all three points; retention cost
  {YES at 20, NO at 22, NO at 24}; pressure nevict {30, 22,
  10}. A step function on retention cost, flat lines on rescue
  and FP rate, monotone decreasing pressure.

## What this does NOT establish (honest boundaries)

- Three capacity points are a slice, not a law. CAP=21 and
  CAP=23 were not run; the exact tipping point between 20 and
  22 is not located (it may be that CAP=21 already displaces,
  or that only CAP=20 does). No interpolation is licensed.
- No no-D6 control arms were run at CAP=20/24. The CAP=24
  redundancy claim is trace-derived reasoning, explicitly not
  a tested counterfactual (PREREG Section 5.3 said so before
  the run).
- The 50% FP rate is world-relative (one decoy chain, never
  used), identical by construction on all arms; it does not
  generalize beyond this decoy design.
- W=20, K=6, the exploratory gap (14 ticks), and contradiction
  magnitude are all fixed; the curve's shape may move with any
  of them.
- The LINKS are memorized associations; no rule induction
  tested; no L2/L3 claim.

## Provenance

- Prereg frozen alone: commit
  `49d11d7f3866e6c46b69b6649b9d2adf84109799` on `tnn-native-lab`
  (PREREG.md + NAMECHECK.md only), strictly before
  implementation. Commit-order self-check: `git log` shows
  49d11d7f3 strictly precedes the implementation commit below;
  no implementation file existed at prereg time. (Note: a first
  plumbing attempt based its tree on a stale head and would
  have dropped another worker's just-landed commit; it was
  caught by tree-diff inspection BEFORE commit-tree ran, and
  the index was rebuilt on the current head. No history was
  rewritten.)
- Implementation + results: this commit. Pure Zag, safebin-only
  PATH, pinned znc 2026.07.0-dev. `which python3` and `which
  python` return nothing under the worker PATH. Zero
  forbidden-executable invocations. The string "python" appears
  nowhere in the source.
- Source: `ntsweep_full.zag` = `ntteach_full.zag` verbatim
  EXCEPT: (a) `cl_new(ns)` allocates `20+ns*44+1728+288+ns*4+288`
  bytes (ns-relative; 3380 at ns=22); all region accessors were
  already ns-relative; (b) `run_arm` takes CAP and calls
  `cl_new(CAP)`; (c) `main` runs R6-CAP20/R6-CAP22/R6-CAP24
  sequentially; (d) per-arm frozen bars S1-S5/R1-R7/T1-T5 and
  the Section 8 verdict mapping computed in-binary; (e) out
  layout gains evh(131) at offset 152 (NT-TEACHASSOC layout
  ended at 148); output tag NTSWEEP. ARM22 reproduces the
  NT-TEACHASSOC numbers exactly (verified field-by-field
  against `ntteach_run1.txt`), confirming the parameterization
  changed nothing at ns=22.
- Build: `znc ntsweep_full.zag -o ntsweep_bin` under safebin-only
  PATH (exit 0; benign zagd-unavailable warning + 4 benign A0102
  warnings on the intentionally result-discarding exploratory
  queries, same as NT-TEACHASSOC). 3/3 runs byte-identical
  (cmp), exit 0, zero stderr.
- Audit: no protection/task-label/freeze/importance/mode/
  usefulness-label logic in the learner beyond the frozen D5 pin
  and the D6 assoc rule under test; the K selector, exploratory
  episode, and probe schedule are harness conditions.
  Compiler-defect workarounds honored (single-buffer cursor
  output + one raw syscall; no `as *i32`+slice; no `!(A && B)`
  in while conditions; no `[]u8 as *u8` casts; `_zag_malloc as
  *u8` threaded through).
- Commits local only, explicit pathspecs, never pushed. This is
  a non-ledger task (claim minting paused): no ledger update.
