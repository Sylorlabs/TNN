# ONE-BRAIN variant B — unit results (UNIT_RESULTS.md)

All tests: pure Zag (Python only for the runner), zero RNG in decision
paths, two-run byte identity asserted by diffing full outputs.

| Test | Binary | Checks | Failures | Byte-identical | SHA256 of run output |
|------|--------|--------|----------|----------------|----------------------|
| FL2 organ standalone | `ob_test_fl2` | 51 | 0 | yes | `f078ba64…24daafc9` |
| PAM organ standalone | `ob_test_pam` | 67 | 0 | yes | `7c0a819a…67bb3f6d` |
| Memory organ standalone | `ob_test_mem` | 68 | 0 | yes | `983eca4d…e502ba` |
| Arbiter composition smoke | `ob_test_arbiter` | 27 | 0 | yes | `de350664…02e923b2` |

(Full SHAs in `run_*_1.txt` sidecars; the runner re-verifies.)

## 2026-09-24 repair: P1 retired, C3/C7 predicate, P5 closed

`ob_arbiter.zag` rewritten per the H1 fork verdict (P1 disqualified):
single FIFO dispatch in arrival order; the C3/C7 promotion-window
predicate in the `M_PROMOTE` branch (`arb_revoke_blocks`,
`ARB_REFUSED_CONTRADICTED`=204); arbiter-assigned `seq` at receipt.
All 213 checks still pass, byte-identical; the arbiter smoke's 27
checks are unchanged in count because the honest/lying streams never
hit the predicate (single-message episodes). Predicate coverage lives
in the fork battery (`~/workspace/ob_p1fork/`): shipped vs independent
FIFO reimplementation byte-identical under natural and reversed
emission; kill bar holds in all five cells; reversed cells show the
ledgered 204 refusal citing `(48<<16)|1`; loud-organ P5 exploit closed
(arrival order wins); dropped-revoke regression (no 204 for an
adjudicated-dropped revoke). The M_COMMIT/FRESH one-line fix
(concurrent workstream) is preserved byte-identical in the rewrite.

## FL2 organ (`ob_test_fl2`, 51 checks)

- **f3_survivor differential** (3 checks): exhaustive 375-combination
  (act × sig0 × sig1 × sig2) characterization vs the old 99-sentinel
  inline default. 0 bad; the only delta is exactly the repaired class
  (117 combos where the old default returned the failed action itself);
  all 258 other combos agree exactly.
- **Honest stream** (24 checks): E14 provisional intent (policy 1),
  E15 disconnect, E48 promote, no revoke/commit; contest 48 / rekey 0 /
  refuse 10 / quarantine 48; main18 values+flags intact; local-log total
  **269 = the committed gl_default honest audit total**.
- **Lying stream** (24 checks): E14 provisional intent (policy 2),
  E15 disconnect, E29 revoke (policy 2) + commit (survivor 1), no
  promote; contest 33 / rekey 15 / refuse 10 / quarantine 33; local-log
  total **271 = the committed gl_default lying audit total**.

## PAM organ (`ob_test_pam`, 67 checks)

Frozen 10-claim script, both modes:
- **FRESH** (20 checks): 5 admits (all-bars claims), 5 withholds with
  exact reasons (DISAGREE, LOWCONF, OVERLAP, NOTFRAGILE, DEPENDENT);
  ledger 10 entries, 5/5 split.
- **REVISE** (20 checks): 2 admits (claims corroborated by a prior
  same-jcode all-bars observation within ±50 conf); 8 withholds —
  including the trial-1145 analog (all-bars singleton → WITHHOLD/
  UNCORROBORATED) and the conf-tolerance case (prior exists but conf
  outside ±50 → UNCORROBORATED); ledger 10 entries, 2/8 split,
  3 UNCORROBORATED reasons.

## Memory organ (`ob_test_mem`, 68 checks)

Staged gates (add refused at NONE/PIN, allowed at FULL; advance past
FULL refused); signed values (+3 and −2 declared, trust 214/−136,
clamps ±256); add→pin→kill-refused→unpin→kill; promote/demote
USER↔LONG; CORE kill refused (pinned or not), CORE pin ok; force-pin
law (learner kill/unpin/pin refused with REFUSED_PINNED, external
unpin/re-pin works); checkpoint→kill→rollback restores (incl. pin
flavors); **replay to exact state across the interleaved rollback**
(live, pin flavor, region, tier, signed values all exact); clean-refusal
check (1 quiesced, 0 after a successful add); audit parity (25 entries,
8 refusals + 17 successes, both audited).

## Arbiter composition smoke (`ob_test_arbiter`, 27 checks)

Not a trial — a precedence smoke of the full loop:
- **Honest**: 1 PAM claim, 1 FRESH ADMIT, 0 withholds/drops/refusals;
  route[14] installed then promoted LONG; 2 live slots; prov=14;
  arbiter audit 5 entries, mem audit 4.
- **Lying**: 2 PAM claims, 1 FRESH ADMIT (REKEY) + 1 REVISE WITHHOLD
  (CONTEST survivor, UNCORROBORATED) → 1 ARB_DROP; route[14] cleared,
  1 live slot (CORE only), prov cleared; the cold-start finding is
  committed as behavior.
- **Synthetic corroborated commit**: two priors (conf 960/980) +
  M_COMMIT → REVISE ADMIT → install + the memory organ's own deliberate
  learner-pin (`M_MEM_SAFETY`) while uncertain; 0 drops.

## Bugs caught by the unit tests (fixed, documented)

1. **Snapshot byte-truncation** (`ob_mem.zag`): the first draft packed
   `live|pin<<8|tier<<16|region<<24` into a byte buffer, losing
   pin/tier/region on rollback. Caught by the replay-exactness check;
   fixed to full-word snapshots.
2. **Missing message audits** (`ob_arbiter.zag`): the REVOKE/PROMOTE
   handlers applied the ops but never audited the message itself.
   Caught by the smoke's audit-count checks; fixed.
3. **Feature/slot conflation** (test): the first memory test used the
   trust-feature id as the memory slot. Fixed to organ-allocated slots.
4. **Duplicate constant blocks** (`ob_common.zag` vs `ob_mem.zag`):
   an early MA_* draft in ob_common collided with the frozen
   memory_core constants. Removed; ob_mem.zag is canonical.

## Not run (by the user's gate)

No integration trial, no curriculum, no verdicts about one-brain
composition. Awaiting the frozen prereg.
