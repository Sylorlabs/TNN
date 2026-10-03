# REPORT: BELIEF-PROVENANCE 1 (evidential adjudication)

Status: COMPLETE. Verdict: **BP-1-PASS**.
Worker: BELIEF-PROVENANCE subagent, 2026-10-03.
Parent mandate: overnight priority 9, belief reasoning from
provenance/evidence.
Prereg: commit 21dce2653 (PREREG.md + NAMECHECK.md, alone,
strictly before implementation). This commit follows it.
To be ledgered C397.

## What was tested

Whether the learner can adjudicate between two conflicting,
grounded structures using provenance/evidence features whose
evidential weight the learner itself learned from experience,
with no researcher-supplied trust rule in the decision path.

Design: the learner holds two MAP structures starting from the
same subject but executing to different terminals (both grounded
in live facts, corr 8 vs 2, real observational support each).
The query is open ended (no target to verify against). The
learner must commit to one structure's output based on its
learner-owned meta-table: rows of (winner corr, loser corr)
written by learner machinery after resolved conflict episodes,
each row carrying type-16 provenance edges to both structures.

Three arms, fresh learner state each:

- ARM-STANDARD: 10 phase-1 conflict episodes where the world's
  regime confirms the 8-corroboration structure; then a fresh
  phase-2 conflict (new entities, same 8-vs-2 profile).
- ARM-REVERSED: 10 phase-1 episodes where the regime confirms the
  2-corroboration structure (stale knowledge regime); then the
  structurally identical phase-2 conflict.
- ARM-NOMETA: phase-2 conflict only, no phase-1, empty meta-table.

## Results (every frozen prediction matched exactly)

ARM-STANDARD: phase-1 ep0 adjudicated -3 (empty table), explored
(hi first, HIT on mid0), wrote meta-row (8,0,2,1,0); eps1-9
adjudicated directly to the 8-corr candidate, all confirmed.
Phase-2: ADJ-CAND mid=20 corr=8 term=202 score=10 vs mid=21
corr=2 term=204 score=0 -> ADJ-WIN win=20 -> ANS via=20 val=202
-> CONFIRM OK. NMETA=11, all rows (8,2). Edges: t14=1, t15=22,
t16=22, e_other=0.

ARM-REVERSED: phase-1 ep0 explored (hi first: MISS on mid0, HIT
on mid1), meta-row (2,1,8,0,0); eps1-9 adjudicated to the 2-corr
candidate, all confirmed. Phase-2: identical candidates,
ADJ-CAND mid=20 corr=8 term=202 score=0 vs mid=21 corr=2
term=204 score=10 -> ADJ-WIN win=21 -> ANS via=21 val=204 ->
CONFIRM OK. NMETA=11, all rows (2,8). Edges: t14=1, t15=22,
t16=22, e_other=0.

ARM-NOMETA: adjudicate(200) -> scores 0,0 -> -3 INDETERMINATE,
no ANS, no reveal, no meta-row. NMETA=0, no edges. No hidden
default bias toward either provenance profile.

## Kill bars

- K-1 PASS: 3/3 runs byte-identical, sha256
  e6de43ad657a826243b9ca86f70cb9a329b7813088c234347cdceb152b3b39e0.
- K-2 PASS: STANDARD via=20 val=202 confirm=1 NMETA=11, all
  rows (8,2).
- K-3 PASS: REVERSED via=21 val=204 confirm=1 NMETA=11, all
  rows (2,8).
- K-4 PASS: NOMETA -3, NMETA=0, LAST_VIA=255, 0 ANS lines in
  the NOMETA section.
- K-5 PASS: phase-2 both candidates grounded, corr 8/2,
  terminals differ (202 vs 204), in all three arms; phase-1 ep0
  candidates grounded.
- K-6 PASS: viaS=20 vs viaR=21 (opposite commitments on
  structurally identical phase-2 inputs), meta-tables all (8,2)
  vs all (2,8). No fixed researcher rule produces this pair.
- K-7 PASS (shell): 2 total ANS lines (via=20 val=202 at line
  197, via=21 val=204 at line 399); 0 ANS in NOMETA section;
  ADJ-WIN win=20 once, win=21 once; STANDARD ep0 EXPLORE-TRY
  HIT (line 17) before META-ROW r=0 (line 18); REVERSED ep0
  MISS (218), HIT (219), META-ROW (220).
- K-8 PASS: edge counts exact per arm, e_other=0 everywhere.
- F-VOID: not triggered. No forbidden interpreter invoked at
  any point; no new mode/bridge/handler/opcode/semantic case;
  no weakened bar; the learner received only revealed terminals
  as observations, never the regime.

## Interpretation

The learner adjudicated from learned evidential state. The
decision function contains no corr magnitude comparison, no
recency preference, no identity preference (source disclosed in
prereg section 5). The STANDARD/REVERSED flip on identical
phase-2 inputs proves the decision content came from the
learner's own phase-1 experience recorded in learner-owned
meta-state: the same two provenance profiles scored 10-vs-0 in
opposite directions, and the commitments followed the scores.
NOMETA proves the commitment is not a default researcher bias:
with no learned evidence the learner abstains (-3) rather than
guessing. The meta-belief itself carries provenance (type-16
edges from each meta-row to both structures), so the evidential
reasoning chain is white-box auditable.

This is belief reasoning, not verification: at decision time
there was no target to check against; the world's confirmation
arrived only after commitment, and the learner's own confirm
machinery evaluated the outcome.

## What was built

- bp_learner.zag (461 lines): state layout, facts, MAPs with
  corr/rev provenance, bp_observe, edges 14/15/16, meta-table,
  bp_adjudicate, bp_explore, bp_confirm, bp_deliver.
- bp_world.zag (10 lines): schedule constants (world side).
- bp_driver.zag (333 lines): 3 arms, observation schedule,
  regime, in-driver bars K-2..K-6, K-8.
- bp_full.zag, bp_bin (90573 bytes), bp_compile.txt (build
  exit 0, no warnings), bp_run1/2/3.txt (byte-identical).

ONE-SYSTEM accounting: new learner machinery = the adjudication
functions (conflict scan, meta-row record/lookup, argmax, tied
abstention, alternating exploration fallback), all generic over
MAPs with corr provenance. 0 modes, 0 bridges, 0 handlers,
0 new edge types, 0 new opcodes, 0 semantic cases.

## Open questions / follow-ups (new preregs needed)

- BP-2: regime change mid stream. After the meta-policy locks
  in, flip the world's regime and test whether the learner
  revises its meta-policy from counterevidence (argmax over
  counts is sticky; this is the honest next test).
- rev (revision count) adjudication: provisioned but unvaried
  here; test conflicts where the profiles differ in revision
  history rather than corroboration count.
- Other corr ratios, more than two candidates per conflict, and
  partial applicability combined with evidential adjudication.
- Whether the argmax learning rule itself could be
  learner-revisable is out of scope for this lane.

## Governance

- Prereg commit 21dce2653 strictly precedes this implementation
  commit (commit-order self-check holds).
- Safebin PATH held the whole session; `which python3` and
  `which python` return nothing; pure Zag for all scientific
  computation; pinned znc by absolute path.
- Commits local with explicit pathspecs, never pushed; no other
  lane touched; no em/en dashes in any lane file (byte
  verified).
- Ledger: to be recorded as C397 (ledger file left untouched;
  another worker has staged changes there).
