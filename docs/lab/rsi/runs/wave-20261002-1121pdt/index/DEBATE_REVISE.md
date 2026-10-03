# DEBATE_REVISE.md - INDEX lane, wave-20261002-1121pdt

Lane-level debate on the verdict: ADOPT C1 (revision hook for the
index) under the amended prereg. Roles: advocate FOR adoption,
skeptic AGAINST (provenance probe mandatory), judge ruling with
cited numbers. Frozen evidence: PREREG_REVISE.md (6667a9c4d),
PREREG_REVISE_AMEND1.md (2a6be2522), sealed runs in SEALED_EVAL.md.

## Advocate (FOR)

The 0521pdt red team proved a soundness hole: `t2_revise_graph`
tombstones the shared tag-101 chain node with no evict-hook call, so
a collateral MAP keeps a plen that no longer describes its chain.
Our control R3 reproduces the hole exactly: idx_validate flips 1 ->
0 with cause 3 (plen mismatch) after a single revision, 3/3 runs.
The candidate (1 hook line + 2 refile lines + dup-safe refile helper;
0 new modes/bridges/handlers/semantic cases) closes the hole:
idx/fidx/deep == 1 after every revision in all three shapes, 3/3
byte-identical per binary. Answers are untouched (R1 6105 -> 7105,
R2 unchanged 6105, R3 A 9001 -> 9999; control and candidate agree
everywhere). The healthy-path no-op check is airtight: 6/6 runs on
the frozen evict driver byte-identical, all hashing to the 0521pdt
sealed canonical 54df62...; the hook costs nothing where nothing
breaks. Adopt: it is the smallest coherent fix for a demonstrated
soundness hole.

## Skeptic (AGAINST, with provenance probe)

Provenance probe first: where did this hook come from? It is a
transplant of the sealed 0521pdt evict-node hook to a second call
site. Its correctness argument is "the same machinery, fired from
the tombstone." But the transplant changed the firing conditions:
the evict hook fires with the arena full and the victim known-dead;
the revise hook fires with free space and the victim replaced by a
fresh step. Did the mechanism survive the transplant, or did it
just pass tests shaped by its own author?

Three specific charges:

1. The counter misprediction. The frozen prereg predicted unchain
>= 2 for R3; the runs showed 1. The amendment derived the correct
value from source order, and the derivation is sound. But the
miss reveals the author's mental model was wrong about what the
hook does (thought it unlinked the revised MAP too). If the model
was wrong there, what else is wrong? The engagement check (vi-a)
is stronger evidence than the counter ever was, but the episode
should lower confidence, not raise it.

2. The revert path. When execution fails and the revision reverts,
the hook has already unlinked collateral MAPs whose chains the
revert restores. They stay unindexed: coverage loss with no
coherence violation. The candidate does not even report whom it
unlinked (no return value, node-0 counter only). A mechanism that
silently degrades coverage on the failure path is not a clean fix;
it is a partial fix with an unmonitored cost.

3. N-way sharing. With 3+ MAPs sharing the stale step, all but the
revised one are unlinked and never repaired. The author admits a
repair-or-retire policy is "queued." Adoption now means shipping a
mechanism whose known failure mode (collateral coverage erosion
under repeated revisions in composition-heavy workloads -- the
exact workloads the program wants) has no answer yet.

## Judge (ruling)

ADOPT, with the bounds written into the verdict. The charges are
real but they are about coverage, not soundness; the kill bars
governed soundness, and every one passes:

- (ii) coherence: idx/fidx/deep == 1 after every revision, all
  shapes, 3/3. The skeptic's charge 2 and 3 describe states where
  the gate stays 1 (MAPs absent, not incoherent). A validator that
  accepts those states is correct; they are availability questions,
  explicitly out of this wave's scope and queued.
- (v) no-op: 6/6 byte-identical to the 0521pdt canonical hash. The
  transplant did not change healthy-path behavior at all.
- Charge 1 is answered by the amendment process itself: the miss
  was caught, derived a priori from frozen source, re-frozen, and
  re-executed. That is the governance working, not failing.

Numbers that decide it: control R3 gate 1 -> 0 (cause 3) vs
candidate R3 gate 1; engagement inbuckB 0 vs 3; answers identical
across all 18 pairwise comparisons. The hole is real, the fix is
minimal (3 lines + helper, 0 architectural additions), the cost is
zero on healthy paths. The collateral-coverage items become
blocking requirements for production integration, recorded in the
queued list, not for this wave's adoption verdict.
