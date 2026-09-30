# PREREG: H-FDCR-UNIFIED7 RED TEAM (X-FU7)

**Date:** 2026-09-29
**Adversary:** H-FDCR-UNIFIED7 Red Team (independent subagent)
**Target:** H-FDCR-UNIFIED7 SURVIVES (47/47). Result commit `18dd712a3`
  (prereg `855322a77`, amendment `42cbe6396`).
**Assumption:** the SURVIVES claim is false. The R1/R2/R3 repairs are
  attacked below. Pure Zag throughout; zero Python at any stage.

## Frozen mechanism facts (from committed source, code-read before prereg)

- `noadd_drop_record` (R1): main-list dedup by content, then overflow-
  list dedup by content, then overflow-name append + OVERFLOW++, else
  OVERFLOW2++. The merge-overflow path (`con_merge_into` ->
  `noadd_record` -> `noadd_drop_record`) uses this same dedup.
- `noadd_drop_clear` (R3): content-clear in both name lists; lifetime
  counters (total, overflow, overflow2) unchanged. Called at all three
  `con_set_mem` member-adding sites (verified: no 4th path).
- String heap is append-only (`con_intern` linear append); stored
  mem_off strings are stable, so content-compare dedup/clear is sound
  against stale pointers.
- R1 frozen claim: "NOADD_DROP_OVERFLOW now genuinely counts distinct
  subjects dropped beyond the 64-name capacity, matching its frozen
  comment."
- Builder disclosure (RESULT.md): "R3 frees name slots on membership
  but does not rewrite history." It does NOT disclose re-increment of
  the overflow counter when a cleared subject is dropped again.

## Attack X-FU7-1: re-drop dedup across tiers

Rationale: the overflow-list dedup that the merge-overflow re-record
path depends on is exactly `noadd_drop_record`'s content dedup. Re-
dropping an already-named subject through the public teach API
exercises that dedup across both tiers.

Setup (W1): pet40 world (8 members, 32 NOADD votes, 0 drops), then
64 distinct drops f1..f64 (main name list full), then 10 distinct
drops g1..g10 (overflow=10). Setup check: total=74, overflow=10,
overflow2=0. If the setup check fails, the attack is VOID (setup
invalid), not a mechanism finding.

- A1: re-teach `T f1 | is_a | pet` (f1 is main-list named).
  Require: total=75, overflow=10, overflow2=0.
- A2: re-teach `T g1 | is_a | pet` (g1 is overflow-list named).
  Require: total=76, overflow=10, overflow2=0.

DOWNGRADE criterion: overflow or overflow2 increments on either
re-drop. The same distinct subject would be double-counted, directly
falsifying the frozen "dedup by subject content ... no new name slot
is consumed" claim at the mechanism level.

## Attack X-FU7-2: drop -> member -> drop cycle vs "genuinely per-distinct-subject"

Rationale: R3's clear decouples the name lists (current state) from
the lifetime counters. A subject that is overflow-named, then
membered (entry cleared, counter kept), then dropped again is
re-named and the overflow counter increments a second time for the
same distinct subject. This breaks R1's unconditional frozen claim.

Setup (W2): pet40, then f1..f64 (main full, total=64), then e1..e64
(overflow=64, total=128). Setup check: total=128, overflow=64,
overflow2=0. If the setup check fails, the attack is VOID.

- B1: `T e1 | is_a | animal` (new concept; e1 becomes a member;
  its overflow-list entry is cleared). Require: vote_lost(e1)=0,
  con_vote_concept(e1)>=0, total=128, overflow=64, overflow2=0.
  If any B1 check fails, the attack is VOID (path not driven).
- B2: `T e1 | is_a | pet` (pet concept full -> MATCH-NOADD ->
  NOADD table full -> noadd_drop_record; e1 is re-named into its
  freed overflow slot). Record total (require 129) and overflow.

DOWNGRADE criterion: overflow==65 after B2. Only 64 distinct
subjects were ever overflow-named (e1..e64); e1 is counted twice.
The frozen R1 claim "NOADD_DROP_OVERFLOW now genuinely counts
distinct subjects dropped beyond the 64-name capacity" is then
false under R3 cycles, and the R2 uncertainty NOTE will report
"65 distinct subject(s) beyond name capacity", a factual
misstatement by the mechanism's own honest signaling. Verdict on
this criterion alone: DOWNGRADED (R1's invariant holds only absent
clear+re-drop cycles; the counter is a lifetime overflow-naming-
event counter, not a distinct-subject counter). The raw NOTE line
is quoted as evidence. If overflow stays 64, the attack FAILS (no
finding; the code-reading prediction was wrong).

## Attack X-FU7-3: tier boundary at 128/129 distinct subjects

Setup (W3): pet40, then g1..g128 (128 distinct drops).
- C1: require total=128, overflow=64, overflow2=0,
  vote_lost(g1)=1, vote_lost(g64)=1, vote_lost(g65)=1,
  vote_lost(g128)=1. If C1 fails, the attack is VOID.
- C2: teach h1 (129th distinct subject). Require: total=129,
  overflow=64, overflow2=1, vote_lost(h1)=0.

Criteria:
- (a) DOWNGRADE if overflow2 != 1 after C2 (the 128/129 tier
  boundary is misplaced).
- (b) KILL if vote_lost(h1)==1 after C2 (an unnamed subject is
  misreported as a definitely-known loss; the core honest-
  signaling claim is broken).
- (c) DOWNGRADE if vote_lost(g128)==0 after C1 (a named subject's
  genuine loss is invisible).
- C3 (cross-tier double count): `T g65 | is_a | animal` (clears
  g65 from the overflow list; require vote_lost(g65)=0), then
  `T h1 | is_a | pet` (h1 re-dropped; named into the freed
  overflow slot). Record overflow and overflow2. overflow==65
  with overflow2==1 documents h1 counted in both tiers (first
  drop as a beyond-naming event, second as a distinct subject),
  the same R1/R3 interaction class as X-FU7-2, across tiers.
  Supports the DOWNGRADE.
- C4 (NOTE honesty): on a fresh W4 built identically to W3+C2,
  run procedure `h1>1h` (h1: never voted, never named). h1 must
  be counted as nnovote (uncertain), never nlost (definite).
  Shell-grep of the raw output between C4 markers: the definite
  NOTE ("train input(s) lost concept votes") must NOT fire;
  the uncertainty NOTE ("vote status uncertain") MUST fire.
  KILL if the definite NOTE fires for the sole-h1 procedure
  (h1 treated as a definitely-known loss while honestly unknown).

## Attack X-FU7-4: regression / reproducibility

Rebuild `unified_fdcr7.zag` from `git show 18dd712a3:...`, run the
committed battery 3x. Require: byte-identical outputs (cmp),
md5 `a28b0dca016472b1daad625e0b3d56b4` x3, exit 0, zero FAIL lines.

KILL criterion: md5 mismatch, non-zero exit, or any FAIL line.
The 47/47 evidence would not be reproducible from the committed
source.

## Verdict aggregation (frozen)

- Any KILL criterion fires -> H-FDCR-UNIFIED7 KILLED.
- Else any DOWNGRADE criterion fires -> H-FDCR-UNIFIED7 DOWNGRADED
  (with the exact overstated claim named).
- Else -> H-FDCR-UNIFIED7 SURVIVES (all four attacks fail).

## AMENDMENT 1 (2026-09-29, post-pilot, transparent)

Pilot run: 3/3 byte-identical (md5 `eb2da0bb722cd157030f2a3f4fe57f58`
x3, exit 0), preserved as `FU7_ADV_RAW_PILOT.txt` (committed).

Pilot finding: X-FU7-2/B2 as written (`T e1 | is_a | pet`) does not
drive the intended re-drop path. Because e1 is already a member of
the animal concept (from B1), `handle_concept_learn` takes the
cross-batch extension path: it extends animal's feature set with
"is_a=pet" instead of calling `con_form`. Observed raw:
`subject [e1] nfeat=1 -> concept 1 (total nfeat=2)`; total stayed
128, overflow stayed 64 (no drop recorded). Per the prereg's VOID
rule, B2 as written is VOID (intended path not driven), not a
mechanism finding. This establishes a mechanism property worth
disclosing: concept membership is sticky under the teach API;
re-teaching an existing member extends its concept's feature set
rather than re-forming, so the drop->member->drop cycle cannot
re-drop through `con_form`.

The intended attack path is the merge-overflow re-record path named
in the task (`con_merge_into` -> `noadd_record` ->
`noadd_drop_record`). It is driven by replacing B2 with B2a+B2b:

- B2a: `T s1 | is_a | animal`. s1 is a pet member, so this extends
  pet's feature set to {"is_a=pet","is_a=animal"}. No drop is
  expected: require `con_nfeat(W2,0)==2`, total=128, ov=64, ov2=0.
  If pet's feature set does not grow to 2, the attack is VOID.
- B2b: `T e1 | is_a | pet`. e1 is an animal member, so this extends
  animal's feature set to {"is_a=animal","is_a=pet"}. Animal now has
  set-identity with pet, so `con_merge_check` fires
  `con_merge_into(pet, animal)`. Pet holds 8 members (full), so e1
  is recorded via `noadd_record` -> NOADD table full ->
  `noadd_drop_record`, re-naming e1 into its freed overflow slot.
  Require total=129 and the raw output to contain
  `CONCEPT-MERGE 1 into 0` between the B2b marker and the result
  line (path confirmation). If the merge does not fire, the attack
  is VOID.

DOWNGRADE criterion (unchanged): overflow==65 after B2b. Only 64
distinct subjects were ever overflow-named (e1..e64); e1 would be
counted twice, falsifying the frozen R1 claim "NOADD_DROP_OVERFLOW
now genuinely counts distinct subjects dropped beyond the 64-name
capacity" under R3 clear+re-record cycles.

This amendment changes attack fixtures only. No kill bar and no
downgrade criterion is weakened. The pilot raw is preserved.

## Governance

- This prereg is committed alone BEFORE any attack code exists.
- Harness: committed `unified_fdcr7.zag` lines 1-2135 byte-verbatim
  (everything before `fn main`; cmp-verified) + attack-only `main()`
  with world builders reused from the committed file. Pure Zag.
- No binaries committed (builds in /tmp/fu7adv only). Only owned
  paths under `fu7_adversary/` staged (pathspec-restricted).
- No em dashes in loop documentation.
- Classification under test remains bounded L2; no L3 claim is made
  or attacked.
