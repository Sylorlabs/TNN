# REPORT: LIFETIME-AB-1 (lt1) -- INFRASTRUCTURE-BLOCKED, NOT CERTIFIED

Branch `p1/lifetime-ab`. Prereg `7f66e5de7` (alone, pre-implementation).

## Verdict

**VOID (uncertified).** The experiment is blocked by a compiler defect, not
by a scientific result. Kill bar K1 (determinism) passes and K3 (no label
leakage) passes, but the run cannot be certified because the binary
silently miscompiles indexed reads of the flat learner-state arena. Two
functions in the same binary return different values for `get32(L,0)` on the
same cells. Every number below is reported as an OBSERVATION, not a result.
No C5xx claim is asserted.

The blocked thing is the measurement apparatus, not the hypothesis. The
hypothesis is untouched and remains testable the moment the toolchain is
fixed.

## Why the run cannot be certified

`DEFECT.md` B16, with a 40-line standalone reproducer that needs no lane
code:

* `probe_defect.zag` (self-contained, 78 lines): all four indexed-read forms
  return the correct `11 105 50 11 106 60`. PASSES, 3/3 byte-identical.
* `probe_defect_with_base.zag` = the frozen, unmodified
  `cogops_rescueaware/c15_base.zag` concatenated with the same 40-line
  probe body: `get32(C, 4 + j)` returns
  `11 1761607680 6881280 26880 105 838860800`. WRONG. 3/3 byte-identical.

Same source lines, same bytes written, wrong bytes read. The corruption is
deterministic, so `--rep 3` cannot see it. In `lt1_full` the two coverage
readers disagree: `emit_stage` reported `retcov = 5/8/10/14/16` across
stages A..E while `emit_cov` reported `0/3/13/16` for the same cells, and
the learner relation-coverage ids printed as heap pointers.

Applying the known mitigation -- every indexed access given an explicit
multiplier, and a lane-local chain writer with inlined byte stores -- was
necessary and did fix the chain buffer, but did NOT fix the coverage
readers. The mitigation does not close the hole.

Two further blockers: B15, the frozen `o_flush` writes nothing at all on
this host, so any lane whose only output path is `o_flush` produces an
empty log and rc=0; and B17, bogus internal type errors on large translation
units.

## What the run nonetheless shows (OBSERVATIONS, uncertified)

Binary `lt1_full`, 3/3 byte-identical stdout,
sha256 `a40508169debafaf649b4be07df4d79e6cb998afdd3bb908c1b7fe9020f9fed8`.
Full log `lt1_run1.txt`.

Structure that is internally consistent and matches the frozen source by
hand-derivation:

* The independent oracle agreed with all seven hand-declared answers
  (`orc=7/7`). This is the one strong internal check in the run, and it
  passes: the declared answer sequences and the generic recomputation from
  the live arena agree for GA, GB, GC, GD, GF, GG and GP.
* The lifetime learner answered 10 of 10 non-invention goals correctly
  (A, B, C, D, F, G, G-probe, G-reprobe-B, H-retain-GA, H-reprobe-GF).
* Template accounting is consistent with the signature design: 4 templates
  built (T1 at A, T2 at B, T3 at C, T4 at F), 7 hits, 4 cross-world fires,
  3 reuse-of-reuse fires. Stage D reused T1 across a three-stage gap on
  disjoint relation ids; the template assembled at F re-fired at G and at H
  on disjoint relation ids. That is the charter-25 reuse-of-reuse pattern
  the design was built to test, and it appeared without any prompt.
* Per-query family trials: A=9, B=0, C=3, D=0, F=0, G=0, H=0. Lifetime
  total 12 across six goal queries; a fresh learner spends 12 per query.
* `h_invention_ok=0`: at stage H the learner did not decline, while the
  declared correct behaviour is decline. The preregicted mis-bind fired.
* Staleness ablation: with the index refresh disabled the same goal on the
  same arena returned `...,1,2` instead of the correct `...,1,3`; with
  refresh enabled it returned `...,1,3`. The recorded answer pair differs in
  exactly the count the post-query extension changed.
* Baselines: a 16-fact recency window was wrong; fresh-with-no-experience
  and fresh-with-F's-episodes were both correct.
* Capacity: with the frozen 8-slot BIND table saturated and the reuse store
  destroyed, the learner declined a goal it should have answered.

What cannot be certified: every coverage-set count, every spec-vs-gen
version split, every cost figure, the memory-occupancy series, the
functional-arity violation count (recorded 0, expected 1, unresolved
because the same read class is what diagnosed it), and all four TTC rows for
stages E..H (recorded never-correct, which contradicts the fact that those
same goals were answered correctly in the main phase -- an internal
contradiction that on its own disqualifies the run).

That last contradiction is the clearest single reason not to publish the
numbers: the TTC phase and the MAIN phase disagree about whether the
learner can answer the stage-F composition goal at all.

## The substantive prediction, stated independently of the broken numbers

Reading the frozen source rather than the run, one property of this
substrate constrains what any lifetime experiment on it can show:

`ret_version` / `vfy_version` / `cnt_version` return the SPEC version only
when the relation is in the learner's coverage set, and otherwise return
the GEN version. `ret_spec` / `vfy_spec` / `cnt_spec` read the same live
arena as `ret_gen` / `vfy_gen` / `cnt_gen`, differing only in which fact
indices they visit. When the index is fresh the two agree by construction.
When the index is STALE the spec path is the only one that can be wrong,
because the arena is append-only and new facts never enter the buckets.

Therefore, on this substrate, accumulated learner state cannot make an
answer better than a fresh learner's -- it can only make it cheaper, or
stale. `try_family` reinforces this: it accepts or refuses on the need's
field shape alone and never consults the arena, so `learn_bindings` memoizes
a TOTAL function of shape and no experience enters it.

That is a real, checkable, negative prediction about the frozen core, and it
is the reason a lifetime A..H protocol on this substrate was never going to
show positive transfer in the "more intelligent with age" sense. It also
predicts the mis-bind at H and the capacity declines, both of which were
observed. It is stated here as a prediction to be tested on a fixed
toolchain, not as a finding.

## What was NOT done

* The harder second lifetime (PREREG section 8, binary `lt2`) was not
  written. Writing it against an uncertifiable toolchain would have
  produced a second uncitable binary. The design for it is in the prereg.
* No C5xx claim IDs were minted. `C500` denotes the prereg only.

## Artifacts

| file | sha256 |
|---|---|
| `PREREG.md` | committed alone at `7f66e5de7` |
| `lt1_full.zag` (assembled, 3850 lines) | `618708f5...8501` |
| `lt1_full` (binary) | `c76534e8...9905` |
| `lt1_run1.txt` / `run2` / `run3` | all `a4050816...fed8` (3/3) |
| `probe_defect_out.txt` | `0f51b208...0dbb3d` |
| `probe_defect_with_base_out.txt` | `a74b8651...52c2b` |
| `DEFECT.md` | B15, B16, B17 |
| `NAMECHECK.md` | constraints 1-7 pass, section 8 records the failure to certify |
| `PREREG_ERRATA.md` | E1-E5 |

## Required next step before any rerun

Fix or work around B16 at the toolchain level, then re-verify with
`probe_defect_with_base.zag` as the acceptance test: it must print
`11 105 50 11 106 60` for all four read forms. Until that file passes, no
flat-arena learner on this host produces citable numbers.