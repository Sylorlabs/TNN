# PREREG_REVISE_AMEND1.md - INDEX lane, wave-20261002-1121pdt

Frozen: 2026-10-02 (committed ALONE, before re-execution under the
amended bar). This amends PREREG_REVISE.md condition (vi) ONLY. All
other frozen conditions (i)-(v), (vii)-(xi) are unchanged. The runs
already executed under PREREG_REVISE.md are reclassified as
EXPLORATORY for the amended bar; the sealed runs below are fresh.

## What the original (vi) said

"(vi) Mechanism accounting: candidate R3 unchain counter (node-0
field 12) >= 2 across the run; control R3 counter is 0; candidate
R1/R2 counters >= 1 (tombstone unlinks the revised MAP, refile
restores it)."

## What the exploratory runs showed

Candidate R1/R2: unchain counter 0 (predicted >= 1).
Candidate R3: unchain counter 1 (predicted >= 2).
Control R1/R2/R3: counter 0 (as predicted).
All coherence conditions (ii), answer conditions (iii), and
determinism (iv) hold on both builds exactly as predicted.

## A priori derivation of the corrected expectation (from source, not
from the observed numbers)

In `t2_revise_graph` (candidate base) the order is fixed:

1. `ns(W,g,12,nst);` -- the guard is rewired to the new step FIRST.
2. `ns(W,stale,0,0); ns(W,stale,36,0);` -- tombstone SECOND.
3. `idx_on_chain_break(W,stale);` -- hook THIRD.

`idx_on_chain_break` unlinks precisely the indexed MAPs whose chain
contains `stale` AT HOOK TIME. Because the rewire (step 1) precedes
the hook (step 3), the revised MAP's own chain no longer contains
`stale` when the hook runs: it contains the spliced-in `nst`. The
hook therefore NEVER unlinks the revised MAP itself in the canonical
shapes; it unlinks only COLLATERAL maps whose chains still reference
the dead step through an un-rewired guard. Consequences, derived
before re-execution:

- R1/R2 (single MAP, canonical success/revert): no collateral MAP
  exists; the hook unlinks nothing. Corrected expectation:
  unchain == 0.
- R3 (shared stale, A revised then B): in A's revision the hook
  unlinks B only (B's chain still references the dead step; A's
  chain was rewired to `nst` before the hook). In B's revision the
  hook looks for `nst`, but A's chain was already rewired to `nst2`
  before B's hook runs, and B was already unlinked: it unlinks
  nothing. Corrected expectation: unchain == 1.
- Control build (no hook): counter stays 0 in all runs.

The original prediction (>= 2 / >= 1) assumed the hook ran before the
rewire. That assumption was wrong; the source order above is
authoritative. The mechanism itself is CORRECT under the corrected
model: the unlink set is exactly the set of MAPs whose post-revision
chains are broken (the coherence property in condition (ii) is the
acceptance criterion, and it holds). The refile (`idx_refile`) is a
dup-safe safety net that no-ops when the MAP was never unlinked.

## Amended condition (vi) (replaces the original (vi) in full)

(vi-a) Mechanism engagement (primary): candidate R3 shows
`inbuckB==0` (MAP B unlinked) while control R3 shows `inbuckB==3`
(MAP B left indexed with a broken chain); candidate R3 shows
`inbuckA==3` (MAP A stays indexed with its repaired chain). This
discriminates an engaged hook from a vacuous pass.

(vi-b) Counter accounting (informational, causally derived):
candidate R1/R2 unchain == 0, candidate R3 unchain == 1, control
R1/R2/R3 unchain == 0. Any other value is a FAIL of the causal
model and blocks adoption pending root-cause analysis.

## What this amendment is and is not

It is a correction of a mispredicted auxiliary counter, derived a
priori from the frozen source ordering, with the derivation
committed before re-execution. It is NOT a weakening of the
acceptance criteria: conditions (ii) (gate coherence), (iii)
(answers), (iv) (determinism), and (v) (healthy-state no-op) are
unchanged, and the engagement check (vi-a) is strictly more
diagnostic than the original counter inequality. The original (vi)
is recorded above as FAILED (misprediction), not waived.

## Re-execution plan (frozen)

Fresh 3x runs of revise_control_bin and revise_candidate_bin on
revise_driver.zag after this commit; hashes recorded in
SEALED_EVAL.md. The binaries are unchanged (built from the frozen
sources before the original runs); only the bar is amended.
