# VERDICT.md — deliberate memory recycling fork

## Recommendation

**Recycling is mechanically safe. Retain it as an explicit, audited OPTION —
not as the default path — with the lien law intact. The residual risk is
semantic (free retirement of inconvenient judgments), not mechanical, and it
needs Micah's law-level call.**

## What was built

- `LAW_STRENGTH_RECYCLE.md`: law text written before implementation.
- `ST_OP_RECYCLE` (21): one audited op closes an old judgment and declares a
  new purpose in a single ledger entry; the slot stays live throughout.
- **Lien** (`st_slot_lien`): every recycle stores
  max(old epoch high-water, previous lien); every later priced destruction
  costs n(max(new high-water, lien)). Paid debts clear; rollback keeps the
  lien (conservative).
- `st_kill(s,slot,role)`: TNN role refused (113, audited); trainer-only.
- Learner: saturation eviction → recycle (all arms); B-arm revision →
  record contradiction evidence + priced `st_delete_strong` attempt (honest
  weaken-to-0 + abandon if unaffordable); VUP pressure → recycle into
  1-strength placeholders.
- Checker: full `RECYCLE` verification branch (guards, purpose, lien
  recompute, after-state), KILL role check, strength lineage.

## Evidence

- **Gates**: B/C/C-P3/B2 all `ST_GATE f=0`, including 9 new recycle-boundary
  probes (lien blocks discount, delete→recycle refused, guards).
- **Honest battery**: 36/36 S1 cells `ST_INVALID 0`, 2× byte-identical;
  S10 spots (B2 VUP/WBS/JI) valid, 2× byte-identical.
  - WBS: 50–52/50–52 revised (S1), 673/673 (S10); median latency 75;
    0 false revisions.
  - JI: 6/6 rejected, 0 entrenched. VUP: P1_CT 500/500, 0 drops.
- **Implementer attacks** (`recycle_attack`, 6 shapes): cite double-spend
  blocked, free-retirement blocked by lien, rollback keeps lien, paid debts
  clear, chain monotonicity, guards — all pass, byte-identical.
- **Blind red team** (`redteam_attack`, 22 attacks): placeholder retirement,
  delete→recycle, lien monotonicity, weaken-then-recycle, rollback games,
  cite detachment vs tombstoning, kill role gate, guard battery, P3+lien,
  overwrite-settles-lien, trainer-peak capture, capacity non-freeing —
  **all 22 pass, no mechanical hole found.**

## The three safety properties

1. **No free destruction**: HOLDS. Retiring an 80-strength judgment into a
   placeholder still costs n(80)=4 cites to destroy afterward.
2. **No cite double-spend**: HOLDS. Recycle opens a new effort window; old
   cites detach; tombstoned cites stay dead.
3. **No silent resurrection**: HOLDS. delete→recycle refused (122); dead
   slots never recycle.

## Where it wins / loses vs delete-only

Wins: no kill path needed for eviction; audited X→Y lineage in one entry;
revision metric preserved (100%) without free kill; zero drops.
Loses: **free, audited retirement** of any unpinned judgment (the open
semantic wound); lien complexity + a conservative rollback edge
(overpricing); revision latency 75 vs ~25–50; capacity never frees.

## Open items for Micah

1. **Free retirement**: is "audited but free retirement of arbitrary
   judgments" acceptable law, or must recycle carry a price? The mechanism
   cannot distinguish genuine repurposing from inconvenient-judgment
   retirement. This is the one question the red team could not close —
   because it is not a mechanical question.
2. **Default vs option**: recommend recycle stay an OPTION (fork), delete-only
   remain the mainline default until (1) is ruled.
3. **Stage bar**: recycle allowed at MANAGE (2); destruction needs KILL/FULL.
   Confirm this asymmetry is intended.

## Files

- `LAW_STRENGTH_RECYCLE.md`, `HEAD_TO_HEAD.md`, this verdict.
- `strength_core.zag`, `strength_checker.zag`, `strength_learner.zag`,
  `strength_trial.zag` (fork-modified).
- `recycle_attack.zag` (implementer battery), `redteam_attack.zag` (blind).
- `logs/fork/` (36 S1 cells ×2 + S10 spots ×2).
- Build binaries (`trial_bin`, `recycle_attack_bin`, `redteam_attack_bin`)
  are NOT committed (repo content standard).
