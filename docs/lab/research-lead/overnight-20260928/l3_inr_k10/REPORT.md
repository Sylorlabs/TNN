# L3-INR-K10 REPORT: independent adversarial probe (verdict-record completion)

Worker: L3-INR-K10 (independent instance). Date: 2026-10-03.
Prereg: frozen at commit `5388604b1` (K10-P1/P2/P3 bars + determinism bar),
committed BEFORE worlds were materialized and before any arm ran.
Implementation: frozen L3-INR build, never modified (read-only); arms run
via the frozen `run_arm.sh` verbatim; learner never opens a world file.
Runs: seed 7, 3/3 byte-identical per sequence (digests in `runs/digests.txt`).
Pure Zag, safebin mandatory. No Python invoked.

## Governance note

The L3-KILL verdict (C409, L3-INR-SEALED) is terminal and is not revisited.
Nothing here overturns it or makes an L3 claim. This probe maps the L2+
envelope: what the architecture CAN do, and where the honest arms' success
boundaries lie.

## Verdicts against frozen bars

### K10-P1 (P-C: probe-loop iteration): PASS

All frozen predictions confirmed, 3/3 identical:
- HYP_KEPT 3 (u1-false variant, u1-true variant, E*); UNCONSTRAINED 2.
- Exactly 2 PROBE_SENDs: `(0 2)` with true answer 0 (E* predicts 0, so E*
  SURVIVES; survivors {V_true, E*}), then `(1 3)` with true answer 1
  (E* eliminated; survivor {V_true}). PROBE_MATERIALIZE added (w4,w5) then
  (w6,w7). Trace shows PROBE_NEXT -> PROBE_SEND a second time: the probe
  loop ITERATED.
- TRAIN 18/18, HELD 6/6, EDGES 14, DEFER 0.

**Boundary mapped:** the probe loop CAN iterate and resolve multiple gaps.
The S1 kill's mechanism is now precisely bounded: the loop stops iff the
first discriminating probe's truth contradicts E*'s prediction (answer 1 on
a pair E* predicts 0), eliminating the base hypothesis and leaving a sole
survivor. When the first probe's truth AGREES with E* (answer 0), the loop
continues and remaining gaps resolve. The S1 failure was not "the loop
cannot iterate" but "the loop stops when the base hypothesis dies first."

### K10-P2 (P-D: revision under id-permuted world): PREDICTION NOT CONFIRMED (informative)

The frozen prediction (zero toxic purges; TRAIN<18 or HELD<5/6) did NOT
hold. What actually happened, 3/3 identical:
- T1(pd1): TRAIN 18/18, HELD 6/6, EDGES 9 -> PASS (baseline, as predicted).
- T4(pd2): MONITOR rej=1/6 -> REGIME_CHANGE (the genuinely flipped pair
  (v5,v6)); exactly ONE DEL_EDGE_TOXIC (5 6) = (v5,v6), the truly toxic
  edge; ADD re-seeded; DEL minimized to 10 edges at TRAIN 18/18; then
  HYP_BUILD found UNCONSTRAINED 8 -> nu=8 > 4 -> AMBIGUOUS -> honest DEFER
  (no commit, HELD -1/0, DEV_VERDICT FAIL "deferred").

**Finding P-D1 (mechanistic correction):** the id-permutation did NOT break
the purge. `kb.dat` persists the name->id table across arms in a sequence
(`kb_name_id` reuses existing name mappings), so entity identity is
name-stable: post-regime ADD_EDGE lines use name-stable ids (e.g.
`ADD_EDGE 0 9` = (v0,v9), not first-appearance ids). Sealed-battery
adversarial finding #3 ("purge compares positional ids with no remapping;
arbitrary under PAIR-order change") is true of the purge code in isolation
but does NOT manifest in-sequence: the persistent kb provides the
remapping. The sealed S2's matching PAIR order was redundant safeguards,
not a load-bearing crutch. The purge correctly removed exactly the
genuinely toxic edge.

**Finding P-D2 (the real revision boundary):** T4 commits a revision only
when post-revision ambiguity is small. Here the rebuild was TRAIN-perfect
(18/18) but left 8 pairs undetermined (3 training gaps in the mild block
rotation) -> the nu>4 AMBIGUOUS cap, designed for the T5 probe path, also
gates revision commits -> honest DEFER. So the L2+ revision envelope is:
purge + re-seed + re-minimize works, but the commit requires <=4
unconstrained pairs afterwards; otherwise the learner defers rather than
committing a guess. (Sealed S2's T4 passed because only 1 true gap
remained, keeping nu small.)

### K10-P3 (P-E: full-reversal revision, aligned ids): PASS (capability; verdict-rule caveat)

All frozen capability predictions confirmed, 3/3 identical:
- MONITOR rej=6/6 -> REGIME_CHANGE on the first pair; exactly 9
  DEL_EDGE_TOXIC (every stale edge); ADD re-seeded the reversed chain;
  DEL kept all 9; COMMIT to slot G2 (gid 2, parent 1).
- TRAIN 18/18, HELD 6/6, EDGES 9.

**Caveat:** the frozen implementation's own DEV_VERDICT field reads FAIL
("T4 lineage 0/9") because its T4 verdict rule requires
`inter*2 >= oldn` (retain >= half the old edges). Under TOTAL reversal
every old edge was genuinely toxic, so retaining any would be wrong; the
bar is unsatisfiable in principle here. The K10-P3 frozen bar (TRAIN
18/18 AND HELD 6/6 AND 9 purges) is met: capability PASS. Flagged as a
verdict-rule artifact, not a capability failure: the coded "revision"
verdict can only pass partial regime changes.

### K10-DET (3/3 byte-identical): PASS

sha256(summary+trace.log+proto.log) identical across runs 1/2/3 for all
five arm-slots (seq_pc_T5a, seq_pd_T1, seq_pd_T4, seq_pe_T1, seq_pe_T4).
See `runs/digests.txt`.

## The L2+ envelope (completed verdict record)

1. **Probe disambiguation (T5a path):** works, and iterates. Multi-gap
   resolution succeeds iff the probe sequence never eliminates the
   DEL-minimized base hypothesis before the last gap (P-C). The S1 kill is
   the precise case where the first discriminating probe's truth
   contradicts E*. Single-probe-then-stop is conditional, not structural.
2. **Revision (T4 path):** purge+rebuild is a capable structural operator:
   correct toxic-edge removal (name-stable via persistent kb), full
   rebuild under total reversal (P-E, 18/18 + 6/6). Two preconditions bound
   it: (a) entity identity must be name-stable across the sequence
   (satisfied by kb persistence; listing-order permutation is harmless);
   (b) the commit requires <=4 post-revision unconstrained pairs, else
   honest DEFER (P-D: TRAIN-perfect rebuild deferred at nu=8).
3. **Corrections to the sealed record:** finding #3's id-alignment fragility
   does not manifest in-sequence (kb persistence mitigates it); the T4
   DEV_VERDICT lineage bar (`inter*2>=oldn`) is unsatisfiable under total
   regime change and should not be read as a capability failure there.

## Artifacts

- Worlds: `worlds/pc.world`, `worlds/pd1.world`, `worlds/pd2.world`,
  `worlds/pe2.world` (attrs |Spearman|x1000 < 200, verified with frozen
  spearman binary).
- Runs: `runs/seq_pc_{1,2,3}`, `runs/seq_pd_{1,2,3}`, `runs/seq_pe_{1,2,3}`
  (summary_*.txt, trace.log, proto.log); `runs/digests.txt`.
- Drivers: `run_k10.sh`, `digests_k10.sh` (frozen `run_arm.sh` invoked
  verbatim; implementation untouched).
- Prereg: `PREREG.md` (commit `5388604b1`, before worlds/runs);
  `NAMECHECK.md` (Step 0 toolchain guard).

## Constraints honored

- Pure Zag, safebin mandatory; no Python or other interpreter invoked.
- Frozen implementation never modified (read-only).
- Learner never opened a world file (two-process protocol).
- Probe worlds designed by this (independent) worker; materially different
  from S1-S5 (reversed-gap probe iteration; id-permuted revision;
  full-reversal revision).
- Opaque identifiers (fresh w*/v* names).
- Commits local, never pushed, explicit pathspecs.
