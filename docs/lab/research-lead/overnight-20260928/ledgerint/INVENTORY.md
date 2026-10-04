# LEDGER-INTEGRATION: FULL INVENTORY OF CLAIM IDS MINTED SINCE THE SESSION RESTORE

Date: 2026-10-04. Lane: `lane/ledgerint`. Worktree:
`/Users/Shared/micah/Documents/TNN/.worktrees/ledgerint`.

Scope: every claim ID minted on any lane branch at or after the ledger
restore (`7ae7188eb`, 136 insertions 0 deletions, sha256
`31431585aec8d01b971af959fe8cd48562f3d083dd0cf66b1c31974e6bcdf972`),
measured by walking `git log --all --not 87a822426` per branch and
extracting every `C<digits>` token from commit subjects and bodies.

This document writes NO ledger bytes and mints no claim. It is the input
to the allocation in `COLLISION_ALLOCATION.md` and to the append in
`CLAIM_LEDGER.md`.

## 0. HEADLINE COUNTS

| Quantity | Value |
|---|---|
| Lane branches carrying minted IDs | 33 |
| Distinct claim IDs minted at C500 and above | 168 |
| Distinct EXPERIMENTS behind those IDs | 40 |
| IDs used by 2 or more different experiments | 121 |
| Highest ID minted anywhere in the repo | C705 |
| IDs minted into the contested C377 to C466 block | 0 |
| Canonical ledger blocks at session start | 393, not 410 |

## 1. EVERY DISTINCT EXPERIMENT, WITH THE IDS IT MINTED

Column `old` is what the lane actually wrote in its commit messages. The
reader who finds a commit subject must be able to get from it to the
canonical entry, so the mapping is total and is published in
`COLLISION_ALLOCATION.md`.

| # | Branch | Lane dir | Experiment | old IDs |
|---|---|---|---|---|
| 1 | lane/adversary | adversary | 9 sealed adversarial worlds vs frozen COGOPS and TNN-2 | C500, C501, C502, C503, C504, C505, C506, C507, C508, C509 |
| 2 | lane/b16verify | b16verify | pinned znc on darwin/arm64: settle B16, B17, brief s5 | C500, C501, C502, C503, C504, C505, C506, C507, C508, C509 |
| 3 | lane/b17fix | b17fix | B17 independent confirmation plus ptr_guard | C500, C501 |
| 4 | lane/b17fix | b17fix | B17 blast radius census | C502 |
| 5 | lane/blockerfix | blockerfix | B6 scratch bound as a derived function of program length | C570, C571, C572, C573, C574, C575, C576 |
| 6 | lane/blockerfix | blockerfix | B1 namespace collision as a cross-constant-space invariant | C577, C578, C579, C580, C581, C582, C583, C584, C585 |
| 7 | lane/buildstab | buildstab | build-to-build determinism matrix | C530, C531, C532, C533 |
| 8 | lane/causal | causal_world | causal structure learning from world data | C500, C501, C502, C503, C504, C505 |
| 9 | lane/cogopslesion | cogopslesion | COGOPS strat_sel family unification | C510, C511, C512, C513, C514, C515, C516 |
| 10 | lane/corefreeze | corefreeze | CORE-FREEZE-1 baseline removes competence | C500, C501 |
| 11 | lane/corefreeze2 | corefreeze2 | CORE-FREEZE-2 correctness vs an independent oracle | C502, C503 |
| 12 | lane/eviction | eviction_p9 | sublinear structural reclamation | C540 to C562 |
| 13 | lane/invfix | invfix | operand-namespace representation invariant layer | C501 to C509, C510, C511, C512, C515 |
| 14 | lane/l3gate | l3gate | L3 standing gate, first version | C600, C602, C603, C610, C611, C612, C613, C614, C615 |
| 15 | lane/l3gate2 | l3gate2 | L3 gate 2, enforced non-circular G1 | C660, C661, C662, C663, C664, C665, C666, C667, C668, C669 |
| 16 | lane/l3macro | l3macro_unknowndepth | MACRO-OF-UNKNOWN-DEPTH killed at its own gate | C600, C601, C602, C603 |
| 17 | lane/misspath | misspath_p10 | the miss path, which was claimed to bind | C563, C564, C565, C566, C567, C568, C572 |
| 18 | lane/p1falsifier | p1falsifier | the crux falsifier for smarter-with-age | C660 to C674, C675 to C699, C700 to C704, C705 |
| 19 | lane/p1freeze | p1_freeze_arena | FREEZE-ARENA-1 arena frozen at stage entry | C540 to C559, C560 to C562, C563 to C566, C567 to C580, C581 to C596 |
| 20 | lane/p1lifetime2 | p1_lifetime_rerun | LIFETIME-AB-1 rerun with 4 defects fixed | C526, C527, C528, C531 |
| 21 | lane/p1mech | p1_mech | P1-MECHANISM, the mechanism behind the negative | C585 to C596, C600 to C605, C606 to C609, C610 to C618, C619 to C630, C631 to C633, C634 to C651 |
| 22 | lane/p2operand | p2_operand_set | P2 OPERAND-SET arms A and B | C600 |
| 23 | lane/p5meta | p5meta | meta-learning transfer, blocked on its own apparatus | none minted |
| 24 | lane/p6pushdown | p6_pushdown | pushdown induction, no claim | C520, C539 |
| 25 | lane/p6unblock | p6_unblock | formal induction unblock, v1 marked VOID | C520, C539, C540 to C559 |
| 26 | lane/p7belief | p7_belief_inquiry | belief and inquiry, 41 of 42 bars | none minted |
| 27 | lane/p7follow | p7_followon | 10 attacks on the belief lane | C510 to C518 |
| 28 | lane/predopt | predopt | PREDICT-OPTIONALITY | C520 to C525, C529 |
| 29 | lane/propertyzag | propertyzag | property-zag invariant battery on 3 frozen cores | C500, C501, C502 |
| 30 | lane/redteaw4 | redteaw4 | REDTEAM-W4 adjudication of wave-4 claims | C620 to C624, C625 to C631, C632 to C639, C640 to C646, C647 |
| 31 | lane/reaudit | reaudit_ledger | evidence audit of all 393 blocks | C640 to C648, C650 to C659 |
| 32 | lane/recovery | evidence_recovery | characterise the wipe, recover CALR, audit citations | C600, C601, C602, C640, C649 |
| 33 | lane/restores | restores | independent restore verification and the 393-claim re-audit | C640 to C648, C650 to C659 |
| 34 | lane/scalingp8 | scaling_p8 | profiling, indexing, disjoint namespaces | C526, C527, C528, C529, C530, C531, C532, C533, C534 |
| 35 | lane/sensitivity | sensitivity | battery sensitivity by mutation testing | C560 to C566 |
| 36 | lane/trialleak | trialleak_p11 | SCALING-TRIALLEAK, transactional trial release | C700 to C704, and C700 to C7xx in the prereg |
| 37 | arch/cogops-unify | arch_cogops_unify | the original COGOPS strat_sel unification negative | C500, C501, C502, C503, C504, C506 |
| 38 | lane/familyrule | familyrule | FAMILY-RULE, one more rule permitted to read the store | C730 to C759, C730 to C735, C736 |
| 39 | lane/p7baseline | p7_baseline | P7-BASELINE, 10-member baseline family to beat | C700 to C706 |
| 40 | lane/p5meta2 | p5meta2 | meta-learning apparatus repair, addendum only | none minted |

Three of these were found only on the second pass and are worth calling
out, because all three were invisible to a scan of the obvious lane
directories:

- `arch/cogops-unify` is not under `lane/`, and it is the ORIGINAL
  strat_sel negative result. `lane/cogopslesion` is its re-test, which is
  why C506 has five claimants rather than four.
- `lane/familyrule` and `lane/p7baseline` were both created at
  12:42 on 2026-10-04, the latest activity in the repo, and both reach
  into C7xx. Neither has a result yet.
- `lane/trialleak` is parked at a tip that CONTAINS the eviction,
  misspath and scalingp8 work, so a naive per-branch ID scan attributes
  their IDs to it. It has exactly 2 commits of its own.

## 2. THE COLLISIONS, BY ID

An ID is a collision when two DIFFERENT experiments claimed it. Same
experiment, several commits, is not a collision.

| ID | Distinct experiments | Which |
|---|---|---|
| C500 | 7 | adversary, b16verify, b17fix, causal, corefreeze, propertyzag, arch/cogops-unify |
| C501 | 6 | adversary AW-01, b17fix ptr_guard, causal, corefreeze, propertyzag, arch/cogops-unify |
| C502 | 5 | adversary AW-02, b17fix blast radius, corefreeze2, propertyzag, arch/cogops-unify |
| C503 | 3 | adversary AW-03, corefreeze2, arch/cogops-unify |
| C504 | 4 | adversary, b16verify, invfix, arch/cogops-unify |
| C505 | 4 | adversary, b16verify, causal, invfix |
| C506 | 5 | adversary, b16verify, invfix, cogopslesion, arch/cogops-unify |
| C507 | 3 | adversary, b16verify, invfix |
| C508 | 4 | adversary, b16verify, invfix, predopt |
| C509 | 4 | adversary, b16verify, invfix, predopt |
| C510 | 3 | invfix, cogopslesion, p7follow |
| C511 | 2 | invfix, cogopslesion |
| C512 | 2 | invfix, cogopslesion |
| C513 | 1 | cogopslesion |
| C514 | 1 | cogopslesion |
| C515 | 2 | invfix, cogopslesion |
| C516 | 1 | cogopslesion |
| C518 | 1 | p7follow |
| C520 to C525 | 2 to 3 | predopt, p6pushdown, p6unblock |
| C526, C527 | 6 | scalingp8, eviction, misspath, p1lifetime2, p1freeze, p1mech |
| C528 | 3 | p1lifetime2, p1freeze, p1mech |
| C529 | 2 | predopt, scalingp8 |
| C530 | 2 | buildstab, scalingp8 |
| C531 | 4 | buildstab, p1lifetime2, p1freeze, p1mech |
| C532, C533 | 2 | buildstab, scalingp8 |
| C534 | 3 | scalingp8, eviction, misspath |
| C539 | 2 | p6pushdown, p6unblock |
| C540 to C562 | 2 to 4 | eviction, misspath, p1freeze, p1mech, sensitivity |
| C563 to C572 | 2 | misspath, sensitivity |
| C570 to C576 | 2 | blockerfix B6, p1freeze and p1mech overlapping |
| C577 to C585 | 2 | blockerfix B1, p1freeze and p1mech at C585 |
| C585 to C596 | 2 | p1freeze, p1mech |
| C600 | 4 | p2operand, l3macro, l3gate, l3gate2 |
| C602 | 4 | l3macro, l3gate, l3gate2, recovery |
| C603 | 4 | l3macro, l3gate, l3gate2, redteaw4 |
| C605 | 1 | p1mech |
| C606 to C609 | 1 | p1mech |
| C610 to C615 | 3 | l3gate, l3gate2, p1mech |
| C618 to C630 | 2 | p1mech, redteaw4 |
| C631 to C633 | 2 | p1mech, redteaw4 |
| C634 to C639 | 2 | p1mech, redteaw4 |
| C640 to C648 | 4 | redteaw4, reaudit, restores, recovery |
| C650 to C659 | 2 | reaudit, restores |
| C660 to C669 | 2 | l3gate2, p1falsifier |
| C700 to C704 | 3 | p1falsifier, trialleak, p7baseline |
| C706 | 1 | p7baseline |
| C730 to C759 | 1 | familyrule |

The worst cases are **C500 with seven distinct experiments**, **C506
with five**, and the **C700 to C704 block with three**. No lane could have
known it was colliding: there was no allocator. Commit `9dec1bca` on
`redteam/suf-audit` records the disclosure, "P5 (no claim-ID allocator)",
and commit `1e98bde4` shows one lane already reacting to a collision by
re-minting itself into C590 and C591. That self-remint is itself part of
the problem: it moved the claimant rather than the number.

**C700 to C704 deserves a note.** Three unrelated experiments chose it
within about 90 minutes of each other on 2026-10-04: `lane/p1falsifier`
(the crux falsifier), `lane/trialleak` (transactional trial release) and
`lane/p7baseline` (a 10-member baseline family). `lane/p7baseline` and
`lane/familyrule` were created at 12:42, which is AFTER this lane's
inventory pass began, so a reader who ran this scan an hour earlier would
have found two claimants instead of three. The allocation below therefore
reserves headroom rather than filling to the last free number.

## 3. C377 TO C466: NO MINT OCCURRED

Checked explicitly, because the mission forbids it.

- The canonical ledger at the restore ends at C410.
- C377 to C466 is contested by `ledger_collision_resolve/COLLISION_RESOLUTION.md`,
  which is still a PROPOSAL with two live options and no ruling.
- Scanned every lane branch for minted IDs in that range: **zero**.
- `lane/l3gate` and `lane/l3gate2` mention C453 and C459, and
  `lane/recovery` mentions C377, C409, C410, C411, C416, C417, C418, C460
  and C466. Every one of those is a CITATION of a pre-existing or
  contested number, in a preregistration or a gate input list. None is a
  mint. `lane/l3gate` commit `39d9d7b19` uses C401 in a subject line, as
  a selection correction to a claim being gated, not as a new claim.

**No governance incident occurred.** This is recorded as a clean result,
not as an absence of checking. The hazard was real: the brief told lanes
to use C5xx and higher, and 35 lanes independently chose overlapping
regions of C5xx without an allocator, which is the same failure one block
lower.

## 4. WHAT THE LEDGER ACTUALLY CONTAINS

Measured by `li_levels.zag`, 4 of 4 embedded controls passing, 3 of 3
byte-identical, sha256 `ed2e54f14cda8696a75efcea251523922d02b1aca83b6b4f674b06b240e2f9ef`.

| Quantity | Value |
|---|---|
| Bytes | 675,018 |
| Lines | 7,665 |
| Claim blocks, heading form `## C<n>.` | 142 |
| Claim blocks, bullet form `- C<n> (` | 251 |
| Claim blocks, total | **393** |
| Sub-bullets skipped, appendix material | 7 |
| Blocks asserting any `L<digit>` token | 118 |
| of those, uncontaminated by a lane-name form | 47 |
| of those, contaminated by a form like `L3-NIV2` | 71 |
| Blocks asserting no level token at all | **275**, 699 permille |

**The block count of 393 is confirmed twice**, by this program and by an
independent awk pass. It is not 410. The gap is C143 to C159, which are
appendix sub-bullets inside other entries, plus 10 IDs absent from the
range. Any future document that says "410 claims" is wrong.

**The level-field refusal is upheld, and the re-audit's numbers are not
reproducible.** `lane/reaudit` reported 131 blocks asserting a level and
262 asserting none. This program measures 118 and 275. An independent awk
pass measures 150 and 243. Three implementations, three answers, and the
block count the only figure all three agree on. That is what prose looks
like from the outside.

## 5. EVIDENCE LEVEL: WHAT CAN AND CANNOT BE PUBLISHED

Cannot be published: a numerical L0 to L3 distribution over the 393
blocks. Not because the detector is weak, but because the datum does not
exist in the file. 275 of 393 blocks carry no level token at all, and of
the 118 that do, 71 are contaminated by claim-name forms that are not
levels.

Can be published, and is:

- **L3 achieved anywhere: zero.** Not an inference. Every occurrence of
  the phrase in the ledger is negative. Six L3-adjacent claims were gated
  this session and none passed.
- The level of each of the 35 experiments in section 1, as asserted by
  the lane and as adjudicated by the gate lanes, recorded per entry in
  the append.

## 6. WHAT IS NOT INVENTORIED, AND WHY

- `lane/p5meta`, `lane/p7belief` and `lane/tcdefects` minted no IDs of
  their own. Their reports exist and their results stand; they simply
  never claimed a number. They are in section 1 so the census of lanes is
  complete. `lane/p7belief` work is also reachable from `lane/p7baseline`,
  which is why a per-branch scan double-counts it.
- `lane/familyrule` and `lane/p7baseline` have a preregistration and, for
  familyrule, an implementation and a pre-run erratum, but **no result**.
  They are inventoried as preregistrations and must not be given a
  verdict in the ledger.
- `lane/p5meta2`, `lane/p5unblock`, `lane/smoke-test`, `p2/compose-dag`,
  `p2/compose-dag-v2`, `scale/namespace-invariant` and `p6/formal-induce`
  hold either zero commits of their own or commits that mint nothing.
  `lane/trialleak` has 2 own commits inside a tip that also contains the
  eviction, misspath and scalingp8 work; only its 2 count.
- Commit sharing is real and had to be handled. Of 244 not-base commits
  across lane branches, 96 sit on exactly one branch, 28 on two, 15 on
  three and 1 on four. A naive scan that reads every branch in isolation
  attributes the shared commits to whichever branch it happens to visit
  first. `lane/trialleak` is the worst case: 22 not-base commits, 20 of
  which belong to other lanes.
- 8 CALR claims and 113 further claims have no resolvable provenance at
  all. They are inventoried by `lane/reaudit` and `lane/restores`, not
  here, and this lane does not restate their numbers.

## 7. HOW THIS SCAN CAN BE WRONG

Stated so a later reader does not over-trust it.

1. **It is a text scan.** It finds `C<digits>` tokens in commit messages.
   A lane that minted a claim without putting its number in a commit
   subject would be missed. Commit `d64053cbe` on `lane/restores` is
   exactly that case, "record the accepted DOWNGRADES as C650-C659;
   nothing minted", where the numbers appear only in a document.
2. **It has no cutoff discipline for lanes still running.**
   `lane/familyrule` and `lane/p7baseline` were created at 12:42 on
   2026-10-04, during this pass. Any allocation made now can be collided
   tomorrow. That is why the allocation reserves headroom and installs an
   allocator.
3. **"Distinct experiment" is my judgement.** `arch/cogops-unify` and
   `lane/cogopslesion` study the same family and I counted them as two
   experiments because one is the original and one is its preregistered
   re-test, and they dispute one of its claims. A different reader might
   merge them. The mapping table is therefore keyed on BRANCH plus ID,
   not on my notion of experiment, so it stays usable either way.
4. **Two of my own numbers were wrong before this document was
   finished.** The first draft of section 6 quoted total commit counts
   where not-base counts were required, and understated the trialleak
   problem. Both are corrected above. The control that caught them was
   re-deriving branch tips directly rather than trusting an earlier
   table.

No em dashes were used in this document (verified by author).
