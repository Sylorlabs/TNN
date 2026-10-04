# C560 PREREG -- BATTERY SENSITIVITY (mutation-testing charter 79/81/158)

Lane: `sensitivity/`. Pure Zag. Committed ALONE, before any audit result is
observed. No number in this file has been measured yet.

## 0. Why this prereg exists

`lane/invfix` fixed 8 defects (C501-C509) in two frozen cores and reports the
**regression battery green on the pre-fix engine**. `lane/redteaw4` (7c82f5d2a)
argued from that plus a 3-site audit that the battery's *sensitivity* is 0/8 and
extrapolated a 6.97%-17.6% defect rate over the 43 un-audited green sites.

A **defect rate** is not the quantity that governs trust. The quantity is
**sensitivity**: P(battery fails | defect present). This lane measures that, by
construction, by **mutation testing** -- inject known defects, require the
battery to fail. Nobody has done this in this program.

## 1. OBJECTS (frozen before measurement)

* `E_PRE`  = `invfix/fbase.zag`        -- pre-fix TNN-2 slice, 917 lines.
* `E_FIX`  = `invfix/iv_tnn2.zag`      -- post-fix TNN-2 core, 1447 lines.
* `B0`     = `invfix/t2_battery_frozen.zag` -- the 46-site STANDING battery.
* `B0'`    = `invfix/t2_battery_iv.zag`     -- 52-site corrected battery (46+2+6,
             894 lines). Note: it calls `nodecap/opnd_slot/iv_check`, which do
             not exist in `E_PRE`; it is therefore **not runnable on `E_PRE`**.
* Defect ground truth: C501,C502,C503 (COGOPS core) and
  C504,C505,C506,C508,C509 (TNN-2 core), as recorded in
  `invfix/FINDINGS_C512_C515.md`.

Sources are COPIED into this lane unmodified and never edited in place. No file
in another lane is written.

## 2. G1 -- MEASUREMENT OF THE STANDING BATTERY (the 2x2)

A defect is **DETECTED** by a battery iff the battery run on an engine carrying
that defect produces at least one FAIL. A defect is **PRESENT** iff the engine
carries it. This is the standard 2x2; I fix it here so no other definition can
be chosen after seeing results.

*Arm 1 (combined).* `B0` on `E_PRE` (all 8 present) vs `B0` on `E_FIX`.

*Arm 2 (single-defect mutants, the only honest per-defect measurement).* Arm 1
cannot attribute: 8 defects co-occur, so one detection could mask seven. I build
`M1..M5` = `E_FIX` with **exactly one** defect reintroduced by a minimal,
line-local revert whose diff I record. C501/C502/C503 are **out of scope for
mutants** because they live in the COGOPS core, which `B0` never links; that is a
**coverage** zero and I report it as such rather than counting it as a
sensitivity miss.

**P1 (prediction).** `B0` on `E_PRE` prints `TOTAL 46/46`. Combined sensitivity 0/8.
**KILL BAR P1:** any FAIL on `E_PRE` refutes combined sensitivity 0/8; the
per-defect figure is then computed from Arm 2 and I report the higher number.
**P2:** `B0` on `E_FIX` fails exactly the sites whose frozen expectations encode
C504/C505 and no others.
**P3:** for every `Mk`, `B0` on `Mk` prints `TOTAL 46/46` (i.e. `B0` misses each
single defect in isolation).
**KILL BAR P3:** any `Mk` that makes `B0` FAIL is a detection, credited to `B0`.

*Specificity* is not measurable from real defects (there is no known-correct
population of defects). It is therefore **replaced** by the mutation score:
fraction of injected mutants that the battery fails. A battery with 46/46 on
every mutant has specificity defined by its FP count only, which is the point.

## 3. G2 -- CENSUS OF THE 43 UN-AUDITED SITES (not a sample)

**The unit is all 43. This is a census, not a sample, so no sampling error
exists and no sample could be chosen to suit a conclusion.** The red team's 3
sites (C6, C11, P-ACT6A) are audited already; the other 43 are audited here.
If any are found to be unreachable at audit time, the shortfall is reported
with its reason and the count is stated, never rounded up.

**Taxonomy, fixed now, applied to the assertion expression only.** Each site
gets exactly one label.

* **(a) SPEC-DERIVED.** The expected value is a function of the site's own
  stimulus and the documented contract, computable by hand in the note beside
  it, without consulting any engine output. Such a site is *incapable* of
  encoding the defect it should catch, because the expectation does not come
  from the thing under test.
* **(b) COPIED.** The expected value is not hand-derivable; it is only
  obtainable by observing the implementation. Tautological by construction.
  Sub-label **(b-copy)** if the same value is re-fed from an earlier call to the
  engine in the same site, which is stricter than (b).
* **(c) DEFECT-ENCODING.** I can exhibit a named defect D and show the site
  passes *because of* D -- the expectation, or the stimulus, is a description of
  D's wrong behaviour.
* **(d) VACUOUS.** The site cannot fail: the asserted predicate holds for every
  reachable engine state. A vacuous green site is worse than (b) and is
  counted separately.

**Decision procedure, fixed now.** I read the site, write the hand derivation
if one exists, and label. If I cannot write a derivation, the site is (b) by
default -- the burden of proof is on independence, not on doubt.

**P4:** `(a) >= 30` of 43.
**KILL BAR P4:** `(a) < 15` => more than half the standing battery is
non-independent, and the red team's 6.97%-17.6% interval is superseded by the
measured figure, not merely tightened.
**P5:** `(c) == 0`.
**KILL BAR P5:** any `(c)` site refutes "the 3 were all of them" and adds to the
defective count.
**P6:** `(d) == 0`.
**KILL BAR P6:** any vacuous site is a green site carrying no information at
all and is reported as such regardless of how many there are.

## 4. G3 -- THE FIX: A BATTERY THAT CAN FAIL

Design, fixed before building:

1. **S1 spec-derived assertions.** Every new expectation is a literal derived in
   a comment from stimulus + contract. No value may be obtained by running the
   engine under test. Self-check: for each S1 site I state the arithmetic.
2. **S2 metamorphic properties.** Behaviour that must be invariant regardless of
   implementation: entity renaming (bijection on ids), relation renaming,
   observation reordering, and irrelevant-distractor insertion. A behaviour
   change is a hidden dependency. Reuse `propertyzag`'s generators and
   transforms rather than reinventing them (`pz_meta_rename`, `pz_meta_rerel`,
   `pz_gen_reorder`, `pz_meta_distract`).
3. **S3 independent oracles.** `propertyzag`'s `pz_or_*` are written from the
   contract with different control flow; a disagreement is reported, not
   resolved by seniority. The frozen implementation is **not** ground truth.
4. **S4 mutation testing.** The battery's sensitivity is *measured*, not
   asserted: it is run against `M1..M5` and against 3 further hand-injected
   mutants `M6..M8` (tagged-band swap, capacity-record off-by-one, victim order
   restored to rotation cursor) that are mine, not `invfix`'s, so the battery is
   not tuned to the defects its author happened to find.

**P7 (mutation score).** `N1` (new battery) fails at least 6 of 8 mutants.
**KILL BAR P7:** `N1` failing fewer than 4 of 8 means my proposed battery is not
an improvement over `B0` and I must say so in the verdict rather than ship it.
**P8:** `B0`'s mutation score is reported on the same 8 mutants, on the same
harness, as the control.

## 5. STATISTICS

Exact **Clopper-Pearson** by integer bisection on a bounded binomial recurrence,
in pure Zag. The recurrence is **validated against four closed forms before any
interval is reported**, so the interval itself cannot be the weak link:

| n | p | event | closed form | value |
|---|---|---|---|---|
| 3 | 0.8 | `X<=1` | 0.8^3+3*0.2*0.8^2 | 0.1040 |
| 3 | 0.8 | `X<=0` | 0.2^3 | 0.0080 |
| 5 | 0.8 | `X<=2` | sum k=0..2 C(5,k).8^k.2^(5-k) | 0.05792 |
| 10 | 0.5 | `X<=3` | sum k=0..3 C(10,k)/1024 | 0.171875 |

All four must match to 1e-12 or no interval is reported. Reported as 2x2 cells
plus 95% two-sided intervals; where a cell is 0 the one-sided 97.5% upper bound
is given.

## 6. HYGIENE

* Shell/git for orchestration only. All computation in Zag (`. pure-zag.sh`).
* Every run through `tnnwatch.sh`; timeout 600 s from this prereg, not extended.
* `tools/zbuild.sh` (removes stale binaries); `_zag_print`/`_zag_println` only;
  `_zag_raw_syscall` is inert (brief 4.0). Every driver ends by asserting
  non-empty flushed output -- an empty log is a process failure, not a result.
* Claim IDs C5xx. Explicit pathspecs. Push as I go. Nothing unattended.
