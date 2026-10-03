# REDTEAM_SELF.md - INDEX lane, wave-20261002-1121pdt

Self red team, written before the verdict. The job is to kill the
claims or bound them honestly.

## Claim 1 under attack

The revision hook (`idx_on_chain_break` at the `t2_revise_graph`
tombstone + dup-safe `idx_refile` of the revised MAP) maintains index
coherence across the revision path, with no answer changes and no
healthy-state behavior change.

### Attack 1a: does the hook unlink the right set?

The hook fires AFTER the guard rewire (base line 660) and AFTER the
tombstone (line 663), at line 667. Derived consequence (verified in
the sealed runs): the revised MAP's own chain never contains the
tombstoned step at hook time, so the hook NEVER unlinks the revised
MAP itself -- it unlinks only collateral MAPs whose chains still
reference the dead step. This is minimal and correct for the success
path (the revised chain is valid; unlinking it would be pure churn),
but consider:

(a) Three-way sharing: stale shared by MAPs A, B, C via guards
gA > gB > gC. Revising A rewires gA; hook unlinks B and C. B's
revision finds the spliced step, rewires gA again, fails execution
on B's broken chain, reverts. C stays unlinked with a broken chain
-- correct (it IS broken), but C is never repaired even though a
later revision of C would also revert. The hook does not repair
collateral damage; it only contains it. BOUND: availability is
preserved (linear fallback serves C), but index coverage for
collateral MAPs is permanently lost. A production design would need
a repair-or-retire policy for unlinked-broken MAPs, not just
unlinking.

(b) The revert path over-unlinks. When `t2_exec` fails, the revert
restores the guard, the step, and the seq edge -- collateral chains
are valid again -- but the hook already unlinked them and nothing
refiles them. Safe (gate stays 1) but coverage-negative. The
`idx_refile` safety net only covers the revised MAP `m`, not the
collateral set (the hook does not report whom it unlinked).
BOUND ADMITTED: revert-path collateral coverage loss. Not a
coherence violation; a production hardening item.

(c) Stale on no indexed chain (stray guard shape): the hook walks
empty buckets, unlinks nothing; `idx_refile` finds `m` already
indexed and no-ops (dup-safe). Verified by construction in R1/R2
(unchain == 0, no duplicates: `inbuck==5`, deep validator 1).
The dup guard is load-bearing here; without it the refile would
duplicate `m` in its bucket.

(d) The hook does not handle the FACT side of revision at all:
`t2_revise_graph` calls `ev_teach_in` (indexed correctly by the
existing hook) and adds type-3 self-edges (not index structures).
No FACT incoherence is reachable through revision in the traced
paths. BOUND: if a future revision variant kills FACT nodes, the
hook must be extended.

### Attack 1b: could the gate be fooled after revision?

The gate checks members, not completeness. After the hook, a
collateral MAP is simply absent from buckets -- nothing to fool.
The deep validator (`idx_deep_validate`) additionally checks
completeness (every live valid-plen MAP indexed exactly once) and
reports `deep==1` in all candidate runs. A false ACCEPT would
require a stale entry the member-walk misses; the walk is the sealed
0221pdt walk (cycle-safe, OOB-strict). No false ACCEPT observed.

### Attack 1c: is the R3 adversarial shape representative?

R3 hand-builds shared chain structure (two guards, one step). In
production, `t2_asm_chain` builds fresh nodes per chain, so sharing
arises only through deliberate structure reuse or learner-built
sharing -- exactly the L2/L3 frontier (adaptive reuse, novel
intermediates) where sharing is EXPECTED to grow. The shape is
adversarial but not artificial: it is the shape composition research
is trying to produce. The hook is a soundness hardening for the
world the program wants.

### Attack 1d: what would falsify the verdict?

- Any `idx==0`/`fidx==0`/`deep==0` in a candidate revise run.
- Any control/candidate answer disagreement.
- Any noop-run stdout divergence between candidate and control on
  the frozen evict driver.
- A three-way (or N-way) sharing shape where the hook leaves a
  broken-chain MAP indexed (would show as gate 0 with cause 3).

## Claim 2 under attack

The eviction hook survives soak storms (seeded, 25 natural evictions
at high occupancy): the deep validator holds after every eviction,
no wrong answers, and the 0221pdt index-cycle panic class is dead
under direct fault injection.

### Attack 2a: is 25 evictions a soak?

No. It is a bounded storm, not a soak. The per-eviction deep check
bounds accumulation bugs (any single missed unlink flips the
validator immediately), which is the strongest cheap property, but
long-horizon effects (counter overflow at node-0 fields, bucket-list
pathologies over thousands of unlinks) are untested. BOUND ADMITTED.

### Attack 2b: the storm never revises.

Correct -- the storm exercises the evict path only (the revise hook
is a no-op there, verified by the noop check). Cross-path
interaction (evict storm interleaved with revisions) is untested.
Queued.

### Attack 2c: fault injection vs the original crash.

The original crash was in the OLD `rebind_try_idx` candidate
collector (512-entry buffer, no gate). The fault driver hammers the
HARDENED `idx_collect` directly on cyclic/OOB/dead lists AND the
full `rebind_try_idx` on corrupted worlds. All four injections:
gate rejects, no panic, fallback answers equal. The crash class is
dead, not just fenced: even the lenient collector terminates on a
cycle by construction (Floyd + capacity bound).

### Attack 2d: the latency cliff.

Measured, not killed (characterization bar). If the per-alloc
at-capacity cost shows superlinear growth in live-node count beyond
the arena-bound expectation, the reclamation frontier (not this
lane) owns the fix. This lane reports the numbers.

## Verdict on the red team

Claim 1 holds within its bounds: the revision path is index-coherent
for the evict_node-style hook extended to the tombstone site, with
the stated collateral-coverage limitations (1a.a, 1a.b) admitted as
non-coherence production items. Claim 2 holds within its bounds:
bounded storm + fault injections pass; the soak is not infinite and
cross-path interaction is queued. Neither claim extends to
infrastructure victims (tag 40/900) or to plen-2/plen-4 adversarial
victim positions (inherited bounds from 0521pdt).
