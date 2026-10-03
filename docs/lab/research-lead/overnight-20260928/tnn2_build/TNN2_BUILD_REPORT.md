# TNN-2 Build Report

Prereg: `7c1e30522` (TNN2-PREREG-FROZEN), frozen before any tnn2.zag edit.
Root-cause basis: `ed38121d4` (five FW failure clusters -> three shared
gaps: no runtime constructor, no miss-to-act path, no revision operator).
Base: `tnn1_act_remed_build/tnn1_act.zag` (1328 lines; ACT-remediated TNN-1).
Builder: TNN-2 Builder (retry; prior worker errored on infrastructure with
zero output; started clean). Date: 2026-09-30/10-01.

## Change 1: one executable graph type, constructed at runtime

The three fixed plan templates (plan_c2/plan_g/plan_it/plan_ext/plan_c2c)
and the separate exec_plan executor are deleted. The miss policy is now
`t2_trial`: a MUL Rung B-style trial loop (propose/execute/verify/promote)
over the frozen 4-op ISA (MOVE/BRANCHEQ/INC/DEC, tags 101-104).

- Gather: BFS paths depth 1-4 from the miss subject (skipping relation
  -999), direct values for sums, per-relation chains for counts.
- Assemble: runtime-built cell graphs. GUARD = BRANCHEQ (tag 102,
  true-target in field12, no SEQ fallthrough so a failed guard makes
  execute return -999999); SETREG = MOVE (101); unrolled INC cells for
  sums; GUARD+SET+INC links plus a MOVE epilogue for counts. Literals are
  902-nodes (field20=value; data, invisible to fact scans). Provenance:
  every SETREG cell carries an ET_DEP edge to its licensing fact; the MAP
  node carries ET_DEP edges to all of them.
- Verify: unmasked -> output==expected; masked -> first non-sentinel.
  Search order (chains k=2..4, then sums, then counts, then single hops)
  preserves the frozen composition preference (t_f2 masked returns 201).
- Promote: `promote_graph` writes a MAP node (layout kept from the frozen
  base: field4=r, field8=s, field20=graph root, field24=promo index,
  field28=answer) plus provenance edges plus the taught answer fact.
- Exactly one executor: `execute` is byte-identical to the frozen base
  (diff-verified); `execute()` is untouched. Genuine rejections are
  counted and packed into header field 16 (tried*1024+rej); field 16 was
  write-only in the base.
- Anti-theater: `t_t2_chain4` solves a 4-hop chain no removed template
  could express (old ceiling: 3-hop via compose-by-cloning);
  `t_t2_trial_reject` asserts >=2 genuine rejections before the winner.

## Change 2: the miss-to-act loop in learner state

`miss_inquire` runs on ev_query's cognition path on a true miss (after the
trial loop and P-INV bootstrap both fail). Piece A (inquiry build
18ed3331c): an UNCERTAINTY node (type 30, existing; field4=-4 so ev_act
never selects it as an act; payload = miss key, marker 2 = ignorance
admission). Piece B: a guide built on the base's validated t_a2 act
pattern (type 1, field4=role=miss subject, field20=choice=30 the inquiry
act), edges G->U (DEPENDS) and POLICY_ROOT->G (MEMBER); POLICY_ROOT is a
type-2 GROUP node ensured via the existing pol_get/pol_set. Existing
node/edge types only. No new modes. ev_act is unchanged; with the miss
subject in context it selects the learner-constructed guide and returns
30 (K-T2-5), not the hardcoded 0 fallback.

## Change 3: generic revision operator over 4-op executable graphs

`revise_on_contradict` runs on ev_observe's contradiction branch
(cognition path). `t2_revise_graph`: finds MAPs with DEP edges to the
contradicted fact; locates the stale SETREG step via its provenance edge;
tombstones it (tag 0); inserts a corrected step; rewires the GUARD's
field12 and SEQ edges (topology change, not standing); re-executes to
verify; reverts on verification failure. On success the stale taught
fact is contradicted and the corrected answer taught; the MAP's standing
is untouched (revision is not demotion; no CON edge touches the MAP).

## Kill bars

- K-T2-1 (prereg ordering): `git merge-base --is-ancestor 7c1e30522 HEAD`
  true before any edit (HEAD was 7c1e30522); re-verified after commit.
- K-T2-2 (single executor): `exec_plan` has zero code references in
  tnn2.zag (2 hits, both comments documenting its removal). `execute` is
  the only graph executor; diff against the frozen base is empty.
- K-T2-3 (no fixed templates): plan_new/step_new/plan_c2/plan_g/plan_it/
  plan_ext/plan_c2c/clone_st/ch_out/mp_gather_k/mp_build/mp_compose/
  verify_plan/exact_lu/promote_map all zero hits; T_PLAN/T_STEP/TM_*/SK_*
  constants removed. Every miss-path executable structure is assembled at
  runtime from primitive cells; no complete graph exists in source.
- K-T2-4 (inquiry integration): `t_t2_inquire` drives ev_teach/ev_query
  only and asserts the UNCERTAINTY node (9002,77) and the POLICY_ROOT-
  linked guide exist. PASS.
- K-T2-5 (act path live): `t_t2_actlive` returns 30 via ev_act after a
  public miss, no scaffolding calls. PASS.
- K-T2-6 (revision operator): `t_t2_revise` promotes 101->102->201,
  contradicts (102,12) via public ev_observe, and asserts the
  restructured graph executes to 999, the graph signature changed
  (topology), map_standing is unchanged, and the follow-up query returns
  999. PASS.
- K-T2-7 (determinism): 3/3 runs byte-identical.
  run output sha256: 37c7b552fe56c9b03b93aadb8108dfbd1d8031c056dd0e2cdcb6a1fb88cd3911
- K-T2-8 (toolchain): pure Zag via pinned znc; safebin PATH; `which
  python3` empty (exit 127); zero Python/C/C++/JS/Rust. See NAMECHECK.md.

## Falsifiers

- F-T2-1: `execute` byte-identical to frozen base (diff empty); ISA
  frozen (MOVE/BRANCHEQ/INC/DEC); no new opcode/mode/bridge/handler/
  semantic case. ISA cell tags used by constructors: 101/102/103 only
  (104=DEC remains available in the frozen ISA). Node types: originals
  only (1,2,3,4,20,21,30); T_PLAN/T_STEP removed.
- F-T2-2: single executor confirmed (see K-T2-2).
- F-T2-3: trial loop is search+verify with genuine rejections
  (t_t2_trial_reject: tried=3, rej=2), not a menu; cell count, op per
  cell, operands, and branch targets are fixed by search+verification.
- F-T2-4: POLICY_ROOT populated by miss_inquire from the miss path; no
  test-scaffolding call populates it in the new tests.

## Regression

- All 41 prior tests (15 CLA-2 core + 6 ACT + 14 cognition + 6 ACT-
  remediation groups) copied with assertions verbatim; only the init
  call renamed tnn1_init -> tnn2_init. All pass.
- New: T2-CHAIN4, T2-REJECT, T2-INQUIRE, T2-ACTLIVE, T2-REVISE.
- TOTAL 46/46 PASS, 3/3 runs byte-identical.

## Artifacts and hashes

- tnn2.zag: 1591 lines (base 1328; +263).
  sha256: a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
- tnn2_bin: sha256 6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b
- Line growth is measured and reported, not compressed: the 1200-line
  ceiling is a separate axis per Micah's ruling.

## Verdict

TNN2-BUILD-PASS. (SURVIVES requires the 11-step pipeline; not claimed.)
