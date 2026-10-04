# COLLISION RESOLUTION AND ALLOCATION: the C5xx to C7xx block

Date: 2026-10-04. Lane: `lane/ledgerint`. Status: **PROPOSAL, AWAITING
RULING** for the renumbering table in section 3. The entries appended to
the canonical ledger are settled and are not proposals.

Companion documents: `INVENTORY.md` (what was found) and the append to
`canonical_ledger/CLAIM_LEDGER.md` (what is now canonical).

## 1. THE PRECEDENT THIS FOLLOWS

`ledger_resolution/C361-C368_DUPLICATES.md`, 2026-10-02. Eight claim
numbers, C361 to C368, each used by two different lanes after a concurrent
watchdog collision. The resolution:

> Both entries are canonical; history is not rewritten. When citing, use
> commit hash to disambiguate.

Two properties of that precedent are inherited here.

1. **History is never rewritten.** No amend, no rebase, no citation
   edited. A reader holding an old commit hash can always reach the claim
   it minted.
2. **The collision is disclosed, not silently absorbed.** One document
   lists both claimants per number.

The C361 to C368 precedent resolved collisions that were ALREADY
canonical. The collisions found here are not in the ledger at all, so this
lane has a choice the earlier resolution did not:

> **Option D, adopted.** Since none of the C5xx-and-above claims are
> canonical, give each distinct experiment ONE fresh canonical number and
> publish a total, mechanical old-to-new mapping. Nothing is renumbered in
> place, because nothing is in place. The mapping is keyed on branch plus
> old ID, so it degrades gracefully if a later reader prefers the C361
> model and simply treats both sides as canonical.

Option A of `COLLISION_RESOLUTION.md` is rejected: that document concerns
an earlier, different race, and the numbers it proposes, C461 to C466,
fall inside the contested block that must not be minted. Its Option C,
sub-numbering, is rejected for the reason that document itself gives.

## 2. THE ALLOCATED BLOCK

**C800 to C899, one hundred numbers, allocated to `lane/ledgerint`.**

Why C800 and not the next free number:

- C411 to C466 are contested by `ledger_collision_resolve/` and off limits
  until Micah rules.
- C467 to C759 are all either already minted-and-colliding, or reserved by
  a lane still running. `lane/familyrule` and `lane/p7baseline` were
  created at 12:42 on 2026-10-04, hours before this allocation, holding
  C730 to C759 and C700 to C706.
- C800 leaves a documented gap of 40 free numbers between the highest
  number known minted, C759, and this block. That gap is working margin
  for lanes still minting.

| Range | Meaning | Count |
|---|---|---|
| C800 to C839 | Science results, one per distinct experiment, chronological by first mint | 40 |
| C840 to C859 | Downgrades, retractions, blocker adjudications | 20 |
| C860 to C869 | Governance and measurement instruments | 10 |
| C870 to C899 | Reserved, unallocated headroom | 30 |

## 3. OLD TO NEW MAPPING

The rule that makes this table short:

> Each lane-experiment gets exactly ONE canonical number. Every old ID that
> lane minted maps to that same number. Two lanes that shared an old ID get
> DIFFERENT canonical numbers, which is the entire point of the exercise.

168 old IDs collapse to 40 canonical numbers. That is not information loss:
the old IDs were never distinguishable in the first place, which is why
seven lanes hold C500.

### 3.1 Science results, C800 to C839

| New | Lane | Experiment | Old IDs it absorbs |
|---|---|---|---|
| C800 | lane/adversary | 9 sealed adversarial worlds, 9 breaks | C500 to C509 |
| C801 | lane/b16verify | pinned znc on darwin/arm64, settle B16, B17, brief s5 | C500 to C509 |
| C802 | lane/b17fix | B17 confirmation, ptr_guard, blast radius | C500, C501, C502 |
| C803 | lane/blockerfix | B6 scratch bound derived as 12L minus 8 | C570 to C576 |
| C804 | lane/blockerfix | B1 namespace invariant across the constant space | C577 to C585 |
| C805 | lane/buildstab | build-to-build determinism, 162 builds | C530 to C533 |
| C806 | lane/causal | causal structure learning, partial and negative | C500 to C505 |
| C807 | lane/cogopslesion | COGOPS strat_sel family, re-test with the lesion grid | C510 to C516 |
| C808 | lane/corefreeze | CORE-FREEZE-1, the baseline removes competence | C500, C501 |
| C809 | lane/corefreeze2 | CORE-FREEZE-2, correctness against an independent oracle | C502, C503 |
| C810 | lane/eviction | sublinear structural reclamation | C540 to C562 |
| C811 | lane/invfix | the operand-namespace representation invariant layer | C501 to C509, C510, C511, C512, C515 |
| C812 | lane/l3gate | L3 standing gate, first version | C600, C602, C603, C610 to C615 |
| C813 | lane/l3gate2 | L3 gate 2, enforced non-circular G1 | C660 to C669 |
| C814 | lane/l3macro | MACRO-OF-UNKNOWN-DEPTH killed at its own gate | C600 to C603 |
| C815 | lane/misspath | the miss path, premise refuted, leak is the binding term | C563 to C568, C572 |
| C816 | lane/p1falsifier | the crux falsifier for smarter-with-age | C660 to C674, C675 to C699, C700 to C704, C705 |
| C817 | lane/p1freeze | FREEZE-ARENA-1, arena frozen at stage entry | C526, C527, C528, C531, C540 to C596 |
| C818 | lane/p1lifetime2 | LIFETIME-AB-1 rerun, 4 defects fixed | C526 to C528, C531 |
| C819 | lane/p1mech | P1-MECHANISM, the mechanism behind the negative | C526, C527, C528, C531, C585 to C651 |
| C820 | lane/p2operand | P2 OPERAND-SET, arms A and B | C600 |
| C821 | lane/p5meta | meta-learning transfer, blocked, no claim | none |
| C822 | lane/p6pushdown | pushdown induction, no claim, prereg void | C520, C539 |
| C823 | lane/p6unblock | formal induction unblock, v1 marked void | C520, C539, C540 to C559 |
| C824 | lane/p7baseline | P7-BASELINE, a 10-member baseline family to beat | C700 to C706 |
| C825 | lane/p7belief | belief and inquiry, 41 of 42 bars | none |
| C826 | lane/p7follow | 10 attacks on the belief lane | C510 to C518 |
| C827 | lane/predopt | PREDICT-OPTIONALITY | C520 to C525, C529 |
| C828 | lane/propertyzag | property-zag battery, 7 violations in 3 frozen cores | C500 to C502 |
| C829 | lane/redteaw4 | REDTEAM-W4 adjudication of wave-4 claims | C620 to C647 |
| C830 | lane/reaudit | evidence audit of all 393 blocks | C640 to C648, C650 to C659 |
| C831 | lane/recovery | characterise the wipe, recover CALR, audit citations | C600 to C602, C640, C649 |
| C832 | lane/restores | independent restore verification, 393-claim re-audit | C640 to C648, C650 to C659 |
| C833 | lane/scalingp8 | profiling, learner indices, disjoint namespaces | C526 to C534 |
| C834 | lane/sensitivity | battery sensitivity by mutation testing | C560 to C566 |
| C835 | lane/tcdefects | 4 suspected compiler defects adjudicated | none |
| C836 | lane/trialleak | SCALING-TRIALLEAK, transactional trial release | C700 to C704 |
| C837 | lane/familyrule | FAMILY-RULE, prereg and implementation, NO RESULT | C730 to C759 |
| C838 | arch/cogops-unify | the original strat_sel unification negative | C500 to C504, C506 |
| C839 | lane/p5meta2 | meta-learning apparatus repair, addendum only | none |

### 3.2 The 3-way and 2-way collisions, called out

| Old ID | Claimants | Canonical numbers now |
|---|---|---|
| C500 | 7 lanes | C800, C801, C802, C806, C808, C828, C838 |
| C501 | 6 lanes | C800, C801, C802, C806, C808, C811, C828, C838 |
| C506 | 5 lanes | C800, C801, C807, C811, C838 |
| C700 to C704 | 3 lanes | C816, C824, C836 |
| C660 to C669 | 2 lanes | C813, C816 |
| C640 to C648 | 4 lanes | C829, C830, C831, C832 |
| C600 | 4 lanes | C812, C814, C820, C831 |
| C526, C527 | 6 lanes | C817, C818, C819, C833, C810, C815 |

### 3.3 Governance, C860 to C869

| New | What |
|---|---|
| C860 | the level-field census instrument and its result, `li_levels.zag` |
| C861 | this inventory of everything minted since the restore |
| C862 | this allocation and the old-to-new mapping |
| C863 to C869 | reserved for the allocator proposed in section 5 |

### 3.4 Downgrades, retractions and blocker adjudications, C840 to C859

These are the settled record. Each is appended to the canonical ledger as
a new block stating what the evidence now shows. None of them edits the
original claim text, which the mint guard forbids and which history
forbids twice over.

| New | Subject | Old IDs | Disposition |
|---|---|---|---|
| C840 | CALR mechanism level | 14 claims, see 3.5 | L2+ downgraded to L1, VERIFIED BY EXECUTION |
| C841 | CALR evidentiary status | 9 claims, see 3.5 | COMPLETE downgraded to UNVERIFIED, two sub-classes |
| C842 | L3 novelty | C281, C284 | L3 VALIDATED downgraded to L1 |
| C843 | L3 achieved anywhere | all | ZERO, recorded as a standing verdict |
| C844 | C459, C453, C603 | 3 claims | NOT PRESENT in the 393-block canonical ledger at all |
| C845 | blocker B13 | brief s8 | RESOLVED, byte-identical reproduction |
| C846 | blocker B16 | brief s8 | CLOSED as an API trap, get32 and set32 take byte offsets |
| C847 | blocker B17 | brief s8 | REAL destructive defect, blast radius zero in the corpus |
| C848 | blocker B6 | brief s8 | CLOSED as a derived bound of 12L minus 8; the 128 fix REJECTED |
| C849 | blocker B1 | brief s8 | CLOSED, invariant backed across the constant space |
| C850 | the 44 million line wipe | commit b3b3ee00a | characterised, ZERO content lost, restored |
| C851 | the mass-deletion guard | git common dir hooks | installed, fails closed, live-tested |
| C852 | B2 global O(N) scans | brief s8 | still LIVE |
| C853 | B3 GEN arena hard-dimensioned | brief s8 | still LIVE, superseded by GEN-REDIM, adoption unverified |
| C854 | B7 eviction tie-break | brief s8 | still LIVE |
| C855 | B12 frozen TNN-1 no world driver | brief s8 | still LIVE |
| C856 | TNN-2 has no do-operator | research s13.2 | structural, 0 hits over 1591 lines |
| C857 | the 14 CALR claims, provenance | 8 claims | permanently unciteable on this host |
| C858 | 113 SHA-UNRESOLVABLE claims | 113 claims | permanently unciteable on this host |
| C859 | the two false invariants of my own | invfix C512 to C515 | found and fixed by the lane's own battery |

### 3.5 The CALR 14, split on two axes

`lane/restores` bundled these into one 14-claim list.
`lane/reaudit` correctly separated them into two axes of a different kind.
That separation is adopted here and is the reason C840 and C841 are two
entries and not one.

**Axis 1, mechanism level, C840. Fourteen claims. VERIFIED BY EXECUTION.**

| Old | New |
|---|---|
| C294, C312, C324, C334, C348, C350, C358, C364, C367, C368, C378, C383, C391, C401 | C840 |

L2+ becomes L1. Basis: the accepted opcode set is exactly {0,1,2,3,4},
every out-of-range value is rejected, and the five semantics are
identical to the committed `glm_learner.zag::m_exec`. The alphabet cannot
be silently widened. Brief s9 classes a fixed-DSL brute-force search as
explicitly not L3. This axis is CLOSED.

**Axis 2, evidentiary status, C841. Nine claims, two sub-classes.**

| Old | New | Sub-class |
|---|---|---|
| C358, C364, C367, C368, C378, C383, C391, C401 | C841 | 2a, the cited lane never existed in any repository on this host |
| C350 | C841 | 2b, citations resolve, the result is self-declared uncommitted |

C350 is separated because it is in a different condition and
`lane/restores` placed it with the other eight for the wrong reason. Its
own ledger text concedes it: "Status: COMPLETE (implementation commit
pending)". Its citations resolve; its result was never committed. That is
a stronger downgrade than the other eight, not a weaker one, and it is
recorded in C350's own words rather than folded into a count.

### 3.6 Nothing was minted into C377 to C466

Confirmed by scanning every branch for minted IDs in the contested range:
**zero**. C453 and C459 appear in `lane/l3gate` and `lane/l3gate2` only as
citations inside a preregistration and a gate input list. Commit
`39d9d7b19` uses C401 in a subject line as a selection correction to a
claim being gated, which is a citation and not a mint.

No governance incident occurred. Recorded as a clean result, because the
adjacent hazard was real: 33 lanes independently chose overlapping
regions of C5xx and above with no allocator, which is the same failure one
block lower.

## 4. WHAT A LATER READER MUST DO

1. Hold a commit hash or a branch name. Look up the lane in section 3.1.
   That gives the canonical number.
2. Hold an old claim ID, for example C500. **It is ambiguous by
   construction** and there is no way to recover which lane meant it from
   the ID alone. Use the commit hash, as the C361 precedent already
   instructs.
3. Do not read a C5xx-to-C7xx number as a ledger reference. Before this
   allocation none of them was one.

## 5. THE ALLOCATOR, WHICH IS THE ACTUAL FIX

Nothing in sections 1 to 4 prevents the next collision. 33 lanes minted
into a shared range because there was no allocator, and commit `9dec1bca`
records that disclosure explicitly. A mapping document is a postmortem.

The fix proposed, for Micah to rule on, is a single pre-commit hook at
`mint_guard/claim_alloc.sh` that fails closed unless a staged commit which
touches `CLAIM_LEDGER.md` and adds a `- C<digits> (` line also adds a
matching row to `canonical_ledger/CLAIM_ALLOC.tsv`. The hook reads that
file, refuses any number already present, and refuses any number inside a
range listed as contested. Three properties it must have, taken from the
failures this lane has now watched happen:

- It must be **interval aware**. Reserving one number at a time would not
  have prevented C500 to C509 being taken seven times over.
- It must **fail closed** on a malformed or missing allocation file, not
  fall through to allow. The mass-deletion guard already does this and is
  the template.
- It must be installed in the **git common dir hooks**, so it covers every
  worktree. A hook installed in one worktree is how wave 1 lost six lanes.

`CLAIM_ALLOC.tsv` would be four columns: claim number, branch, first
commit, status, where status is one of `active`, `contested`,
`superseded`. This lane proposes but does not install it, because
installing a governance hook is Micah's call and the mission for this lane
is the record, not the policy.

No em dashes were used in this document (verified by author).
