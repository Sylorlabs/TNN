# VERDICT_B: learner-scheduled initiation (exercise b) -- SEALED VERDICT

Wave: wave-20261002-1121pdt. Lane: CONTLEARN (queue item 9, exercise b).
Date: 2026-10-02. Frozen prereg: PREREG_B.md + PREREG_B_AMEND1.md
(committed alone before any implementation; K0 self-check below).
Red team: REDTEAM_B.md (6 attacks, all executed).

Note: hyphens only in this document; no em or en dashes.

## Governing bars (frozen before implementation)

B-S0 (state-driven firing + episode), B-S1 (schedule-independence
crux, |evidx_A-evidx_B|>=50), B-S2 (no harness scheduling), B-S3
(costume state-blindness), B-S4 (determinism/hygiene), K0 (prereg
commit-order), K1 (toolchain), K2 (fixture), K3 (no regression, with
documented attribution for the intentional auto-propose removal).

## Numbers (12 frozen runs, 4 binaries x 3 reps)

- B-S0 (sc_treat_a): SCHED_FIRE unccount=3 evidx=5 s=98301; exactly 1
  PROPOSAL(r=850); episode query answered 98321; EPISODE_OK 1/1
  (tag-20 MAP field8=98301 field4=850 field28=98321, type-1 DEP edges
  to both chain facts and to the proposal). All 3 reps.
- B-S0 (sc_treat_b): SCHED_FIRE unccount=3 evidx=83 s=98301; exactly 1
  PROPOSAL(r=850); EPISODE_OK 1/1; answer 98321. All 3 reps.
- B-S1: evidx_A=5, evidx_B=83, |83-5|=78 >= 50. All 3 reps.
- B-S3 (costume): sc_costume_a fires at evidx=12 with unccount=4;
  sc_costume_b fires at evidx=12 with unccount=0; 1 PROPOSAL(r=850)
  each. All 3 reps.
- B-S4: 3/3 byte-identical SHA-256 per binary (treat_a
  64faecf181f481ca1ccddae2b837fc29411612dc2d79bb3e07fb9099c3cd34e8,
  treat_b
  597d62eb4990f7829a9d33e42896021a4c8d572cfdcc3f52a1dbb2ed1d12f7c2,
  costume_a
  7b9a5d7a68b8a9a75422b213877ab5b83cf5d83d9396229a92d5c26e8826ade6,
  costume_b
  8fd5198deaae91921eb7661be026464c6a307f38f46caa61a642ccec6cfafac7);
  FNV stable per binary; rc 0 on all 12; 0-byte stderr on all 12;
  20 events (schedule A) / 96 events (schedule B) with AUDIT_PASS;
  CAP_GUARD_OK; 1 process per run; empty argv/env; 7 pre-run builds
  in the wrapper log, 0 during runs.
- B-S2/K2: drivers contain 0 pf_propose/pf_find calls; 0 cognition
  functions; sc_sched_scan invoked uniformly after every event.
- K3: unmodified treat core 46/46; sc_treat and sc_costume 36/46,
  the 10 failures being exactly {P1, F2, P2, P3a, P3b, P4, XCAP,
  T2-CHAIN4, T2-REJECT, T2-REVISE}, each verified to require
  ev_query-on-miss trial engagement via the intentionally removed
  auto-propose. No other failures. Attribution documented; K3 PASS.
- K0: PREREG_B.md (123d3086a) and PREREG_B_AMEND1.md (27026eb3a)
  committed strictly before any sc_* implementation file. PASS.
- K1: safebin PATH; which python3 resolves to nothing. PASS.

## Verdict: PASS (bounded claim)

SCHEDULING-STATE-DRIVEN is adopted within its disclosed bound: on
the two frozen schedules, the learner initiates the proposal
episode when its own accumulated UNCERT state crosses the threshold
(fire-time unccount=3 in both), independent of schedule position
(|evidx| separation 78), with the episode causally enabled by the
fired proposal. The costume control (fixed evidx=12, fires with and
without the state) and the negation probe (no fire below threshold)
discriminate genuine state-driven scheduling from harness-prompted
costumes. The red team sustained two scope notes (proposal content
is a fixed template; query-vs-uncertainty not differentially
exercised) and failed to break the claim on four attacks.

What this is: L2 evidence that accumulated learner state can drive
initiation timing, with the initiation branch exercised for the
first time (caveat 2 retired for this instrument). What this is
not: learner-chosen learning targets, policy authorship, agency,
or L3.

## Keep / discard

- KEEP: the state-driven scheduler pattern as a candidate for
  learner-owned initiation in future continuing-learner work.
- DISCARD: nothing; no kill bar fired.
- QUEUED NEXT: exercise (c) cross-kind rebind (PREREG_C.md).

## Commit ids (lane branch lane-contlearn-20261002-1121pdt, local only)

- 123d3086a PREREG_B.md frozen (alone).
- 27026eb3a PREREG_B_AMEND1.md frozen (B-S3 3->4; alone,
  pre-implementation).
- (pending) implementation + transcripts + scripts + REDTEAM_B.md +
  VERDICT_B.md commit.
