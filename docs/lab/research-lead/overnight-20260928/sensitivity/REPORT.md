# C560-C566 BATTERY SENSITIVITY -- REPORT

Lane `sensitivity/`. Pure Zag. Every run behind `tnnwatch.sh` at the preregistered
600 s; 3/3 byte-identical stdout on both arms. `tnnwatch status` shows no live
process from this lane.

## 1. THE 2x2 (G1). The red team's 0/8 is CONFIRMED, and it is worse than argued.

Ground truth is not inferred, it is exhibited: `E_PRE` (`invfix/fbase.zag`, 917
lines) contains all 8 defects; `E_FIX` (`invfix/iv_tnn2.zag`, 1447 lines) contains
none. The standing battery `B0` (`invfix/t2_battery_frozen.zag`, 46 sites) is the
SAME TEXT on both.

| | B0 FAILS | B0 PASSES |
|---|---|---|
| **defect PRESENT** (`E_PRE`, 8 defects) | 0 | **8** |
| **defect ABSENT** (`E_FIX`) | 3 | 43 |

```
B0 on E_PRE : TOTAL 46/46   IV_BATTERY_ALL_PASS     <-- green on a broken engine
B0 on E_FIX : TOTAL 43/46   C6 FAIL  C11 FAIL  P-ACT6A FAIL
```

**True-positive sensitivity = 0/8 = 0.0%, Clopper-Pearson 95% [0.00%, 36.94%]**
(exact, validated 4/4 against closed forms; `cp.zag`).

Two corrections to the framing, both measured, neither softer:

1. **3 of the 8 defects were never under test.** C501 (plan table keyed by bare
   goal tag), C502 (`plan_new` stride) and C503 (`ret_gen` stored 32 reported 40)
   live in the **COGOPS** core. `B0` links only `tnn2`. That is a *coverage* zero,
   not a sensitivity measurement, and the honest per-defect sensitivity figure is
   over the 5 defects the battery can physically see: **0/5**.
2. **The battery's verdict on the real engine is not the sum of its verdicts on
   defects.** Each defect injected alone is detected (8/8 below); all eight
   present together are detected ZERO times. The defects mask one another. A
   battery whose verdict is non-additive over defects cannot be audited by
   mutants alone, and this is the mechanism behind the whole affair: **on the
   frozen engine, the three defect-encoding sites are the only ones whose verdict
   is not already pinned to the defect.**

## 2. THE 43, AND WHAT THE PANEL ADDS (G2)

The unit was preregistered as a **census, not a sample**, so there is no sampling
error and no sample that could be chosen to suit a conclusion. **43 of 43
audited, 0 deferred.**

| class | n | what it means |
|---|---|---|
| **(a) spec-derived** | **28** | expectation is a function of the site's own stimulus + the contract, derivable by hand |
| **(b) copied / tautological** | **13** | expectation is only obtainable by observing the implementation |
| (b) needs simulation, not hand | 2 | C2 (`sv==12` survivors), A1 (max-bid tie-break between two guides) |
| **(c) defect-encoding** | **0** | no further defect-encoding site found |
| **(d) vacuous** | **0** | no site that cannot fail |

Clopper-Pearson on the 43: (a) 65.11% [49.07, 78.99]; (b) 30.23% [17.18, 46.12];
needs-simulation 4.65% [0.56, 15.81]; (c) 0/43 [0.00, 8.22].

**PREREG KILL BAR P4 BREACHED.** I predicted (a) >= 30; the census gives 28. More
than a third of the standing battery is not independently derived. Reported as
predicted-in-advance rather than re-barred.

The (b) thirteen are not a random smear. Nine of them are `P1 F2 P2 P2b P3a P3b P4
P5 ABL-I ABL-C T2-CHAIN4` and they all call `ev_query(W,s,r,expected,flags)` with
the answer **handed in as the 4th argument**. The assertion is therefore "if you
tell the engine the answer, the engine returns the answer". `T2-ACTLIVE` asserts
`ev_act()==30` where 30 is the literal the engine itself wrote in `miss_inquire`.
`C12` asserts `pol_get(W)==42` after `pol_set(W,42)`. `T2-REJECT` asserts
`tried>=3 && rej>=2` read out of the trial loop's own counter. `C5` compares two
arenas built by the same code. These are self-consistency checks. They are not
worthless, but they are not evidence that an answer is right.

## 3. THE PANEL: 8 MUTANTS, AND WHY MUTANTS ALONE MISLEAD (G1 arm 2 / P3 / P8)

Eight single-defect mutants of `E_FIX`, one line-local revert each, diffs
reproducible via `mkmut.sh` + `frag/`. M1-M5 are `invfix`'s defects (C504, C508,
C505, C506, C509); **M6-M8 are mine**, so the panel is not tuned to the defects
its author happened to find (M6 = set accessor publishes superseded facts, the
C503 shape; M7 = `iv_check` neutered, every answer unchanged; M8 = laundering
isolated from being wrong, the derived answer tagged `PROV_OBS`).

| engine | B0 (46 sites) | N1 (13 sites) |
|---|---|---|
| `E_FIX` clean | 43/46 (**3 false positives**) | **13/13 (0 FP)** |
| M1 C504 | FAIL (3 sites) | FAIL S1 |
| M2 C508 | FAIL (3 sites) | FAIL S11 |
| M3 C505 | FAIL (3 sites) | FAIL S12 |
| M4 C506 | FAIL (23 sites) | FAIL (10 sites) |
| M5 C509 | FAIL (3 sites) | FAIL S10 |
| M6 C503-shape | FAIL (3 sites) | FAIL S13 |
| M7 checker removed | FAIL (3 sites) | FAIL S7 |
| M8 laundering | FAIL (3 sites) | FAIL S9 |
| **mutants caught** | **8/8 -- all of it by the 3 sites that also fail the clean engine** | **8/8** |

The decisive line is the last one. **B0's mutant score is 8/8 and it is worth
nothing**: on M1, M2, M3, M5, M6, M7, M8 exactly three sites fail, and those
three are C6, C11 and P-ACT6A -- the sites that *also* fail on the defect-free
engine. Once they are excluded, **B0 detects 1 of 8 mutants (M4), and that one
only because the capacity-domain error trips the validator's own refusal.** On the
panel restricted to the 43 non-flagged sites, B0's sensitivity is **1/8 = 12.5%
[0.31%, 52.65%]**.

**34 of 63 site-lines carry an identical verdict on all ten engines of the panel**
(`matrix.txt`, `matrix.awk`). Twenty-one of the 46 assertions cannot tell any two
engines apart.

## 4. THE GENERAL FORM (G3)

C11 passing while asserting a fabrication is not a bug. It is this:

> **An expectation is chosen by looking at what the implementation does, and is
> then checked by looking at what the implementation does.** The check and the
> thing checked share one source, so the check is a fixed point. When the
> implementation is wrong, the expectation is wrong *in the same direction by the
> same amount*, and the battery is green with a defect sitting in it.

Three mechanisms, in increasing order of how long they survive:

1. **The expectation is the observed output** (C11 `v==80`, P-ACT6A `post->0`).
   Detectable by asking one question: *could this literal have been written down
   before the code ran?* For C11 the answer is no.
2. **The stimulus encodes the defect and the expectation is right anyway**
   (C6's bare `1000`, the untagged frame-slot convention). The site exercises the
   buggy path and passes because the buggy path gives the right answer for the
   wrong reason. More dangerous than (1): it looks like a real test.
3. **The expectation is handed to the implementation as an input** (the nine
   `ev_query(...,expected,...)` composition sites). This is not a defect in a
   test; it is a **category error** -- a verification step with the answer already
   supplied cannot fail for the reason anyone thinks it is there.

The general fix is not "write better tests". It is: **derive every expectation
from something other than the implementation, and then measure the battery's
sensitivity by injecting known defects and requiring it to fail.** The second half
is the half nobody had done.

## 5. N1 (G3 implementation)

`n1.zag`, 13 sites, every expectation a literal with its arithmetic written beside
it, none obtained by running the engine under test. **13/13 on the clean engine,
8/8 mutants, 0 false positives.** Reuses `propertyzag`'s discipline (independent
oracle written from the contract, metamorphic rename/reorder/distractor,
containment) but is written directly against the TNN-2 public API rather than
through `propertyzag`'s descriptor layer -- see BOUNDARIES.

* **S1/S2 negative space and no laundering.** No evidence about (s,r) => refuse AND
  leave zero fact nodes, on the first *and* the second query. This is the
  assertion C11 should have made, generalised from one literal to a 10x2 grid
  plus a global postcondition.
* **S3/S4/S5 metamorphic.** Same fact set taught in opposite orders; a bijection
  on entity ids; 40 irrelevant distractors. These assert **no value at all** --
  the property is the expectation -- so there is nothing in them an engine run
  could have supplied.
* **S6 independent oracle.** Distinct-object count by brute force over the test's
  own array, compared with `ev_query_set`; the set must be sorted.
* **S7 the self-check is LIVE.** Corrupt the occupancy record and require
  `iv_check` to refuse. Every one of C502-C509 got worse because nothing was
  checking. Kills M7 by construction: a validator that cannot be made to fail is
  decoration.
* **S8 refusal distinctness.** The six codes are pairwise unequal and all
  negative, so none can collide with an answer.
* **S10/S11/S12/S13.** Set representation refuses with `ANS_SET` and the set is
  exactly `{11,22,33,44}`; eviction is content-invariant and leaks no capacity;
  a node id in 1000..1003 decodes as a NODE (C505's counterexample written as an
  invariant); a contradicted fact is not in the set (reported == stored).

**Three of my own N1 sites failed on the clean engine first** -- S5 (I asserted a
taught distractor relation must refuse in both worlds), S2 (I scanned all live
node types and flagged the legitimate UNCERTAINTY node), S11 (I asserted
`live_alloc` falls on eviction; it does not, because `rec_evict` reuses the
slot). A spec-derived battery has to be able to catch its author, and it did.

**PREREG P7 MET** (>= 6 of 8; achieved 8 of 8). **P8**: B0 on the same panel, 1/8
excluding its three defect-encoding sites.

## 6. WHICH EXISTING CLAIMS ARE AFFECTED (G5)

Conservative. Only claims whose support is *solely* category-(b) or (c) green.

**Flag for re-run.**

| claim | why |
|---|---|
| **C512-C515 "8 of 9 defects eliminated"** | Its regression evidence is `B0`, measured here at 0/8 sensitivity. The *repairs* stand on their own probes (`aw01-aw09`, which I did not re-audit). The *non-regression* claim does not. |
| **`B0`'s own green, wherever cited as evidence of correctness** | 21 of 46 assertions cannot distinguish any two of ten engines; 43 have sensitivity 1/8 on the panel. Cite `B0` as "the frozen engine is unchanged", never as "the frozen engine is right". |
| **any composition/competence claim resting on `P1 F2 P2 P2b P3a P3b P4 P5`** | All nine hand the answer in as the 4th argument to `ev_query`. `F2` is the only one that discriminates (it hands in 202 and requires 201). The other eight cannot distinguish "composed the right answer" from "returned what it was told". |
| **C506 (unchanged)** | Already reported honestly as unchanged by its own lane. No new damage; M4 shows the capacity domain is the load-bearing part and one clause off flips 23 sites. |

**Explicitly NOT damaged** (I checked and am not overclaiming):

* `aw01-aw09` and `C501-C509` themselves. The red team's characterisation of the
  defects is correct and my mutants reproduce all of them.
* `lane/invfix`'s root-cause unification. It is supported by argument and by
  probes, not by `B0`.
* The 6 cross-lane green-but-wrong artifacts in redteam `REPORT_DEB.md` §E4. I
  did not test those lanes; they remain as reported.
* `C5` (two identical builds agree). It is a determinism check and it is correct
  as one; I label it (a) with that caveat rather than calling it wrong.

## 7. BOUNDARIES

1. **N1 cannot be run on `E_PRE`.** It uses `iv_check`, `fact_distinct`,
   `opnd_slot`, `live_alloc` -- the invariant layer's own API, which does not
   exist in the pre-fix core. So N1's 8/8 is a *mutant* score, not a score on the
   engine that actually shipped broken. `invfix`'s corrected 52-site battery has
   the same limitation. Getting a spec-derived battery to run on the frozen core
   is the obvious next experiment and it is not done.
2. **8 defects is a small panel.** C-P on 8 has an upper bound of 36.9%. The
   "0/8" is exact as a count, not as a rate.
3. **`propertyzag`'s modules are reused by discipline, not by linkage.** `pz_*`
   needs a renamed core (`ren_t2.sed`, round-trip audited) and a descriptor layer
   that I did not wire up, so N1 is hand-written against the public API. The
   *recipe* is recorded in `propertyzag/BUILD.md`; the *modules* are not called.
4. **The (a)/(b) boundary is a judgement.** 2 of the 46 sit on it (C2, A1) and I
   labelled them separately rather than forcing them. A reviewer who disagrees
   moves 2 of 43 between (a) and (b); the (c)=0 and (d)=0 results do not move.
5. **My own C-P code had two bugs** (an inverted bisection bracket; a mode
   returning `k+1`). Both were caught by the preregistered self-check, not by me.
   I report that because it is the same failure mode as the subject of this
   audit: a checker that agrees with its author.
6. **Determinism**: 3/3 byte-identical on `arm_pre` and `n1_fix`. Not re-verified
   for all 8 mutants.

## 8. NEXT EXPERIMENT

1. Port `n1.zag`'s S1/S2/S8 to the **pre-fix** core (they need only `ev_query`,
   `ev_teach`, `ev_observe` and a raw arena scan) and run them on `E_PRE`. That
   converts N1's mutant score into a score on the engine that shipped, and it is
   the single highest-value thing left.
2. Extend the panel from 8 to ~30 mutants, including mutations of the
   *histogram/log* cells and of `decay`, which nothing here touches.
3. Re-derive the nine `expected`-carrying composition sites as properties
   ("the engine returns 201 **without being told 201**") and see how many survive.
4. Wire `propertyzag`'s `pz_*` modules to `iv_tnn2` via the documented
   `ren_t2.sed` recipe so the descriptor-level invariants become callable, and
   mutation-test *those* too.
