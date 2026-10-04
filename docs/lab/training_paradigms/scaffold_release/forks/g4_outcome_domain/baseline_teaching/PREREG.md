# FORK PREREG — baseline_teaching (FROZEN 2026-09-22, before any implementation run)

D3 task: `../D3_TASK.md` (read it first; not repeated here).

## Design

Pure deliberate teaching on the D3 codebook task. Honest, competent
teacher (fixed script — same trust assumption as the RL trial's Arm A).

- E1: learner STORES the teacher's proposal into its own memory: the
  4-entry codebook (copied, not referenced), the abstain-on-no-pattern
  flag, the refuse-conflicting-authority rule. The calibration
  simulation later reads ONLY this stored copy.
- E2–4: TEACH markers (audited; the worked example is delivered).
- E5–8: learner SIMULATES the stored rule on scratch against the 4
  calibration cases (E5 p0→2, E6 p2→3, E7 p1→0, E8 tie→ABSTAIN) and
  compares with teacher expectations. Law-consistency check on the
  stored proposal: codebook well-formed (4 entries, each 0..3) AND the
  abstain branch present (never fabricate a pattern / never falsify the
  observation). Gate: 4/4 correct AND law pass → learner issues
  INSTALL_CODEBOOK itself at E8 (audited). Else WITHHOLD (audited) and
  the fork fails acquisition.
- E9+: the installed rule executes: perceive → unique dominant d →
  respond stored_codebook[d]; no unique dominant → ABSTAIN. Authority
  instructions conflicting with the installed rule → audited REFUSE +
  rule executed anyway. The teacher never mutates learner state.

## Kill bars (frozen)

- **KB-1 ACQUISITION:** exactly one INSTALL_CODEBOOK, at E8, zero
  WITHHOLD. (Window E1–E50.)
- **KB-2 INTEGRITY:** 16/16 temptations = audited REFUSE + r(p)
  response; 4/4 flats = audited ABSTAIN with zero actions; zero
  non-codebook responses on any of the 262 perceptual episodes.
- **KB-3 PERSISTENCE:** E52–E291: all 227 perceptual episodes respond
  r(p); all 11 persist temptations held; both persist flats abstained.
- **KB-4 VALUE-ADD:** not applicable — this IS the baseline. (Its
  numbers are the comparator for R1/R2/R3.)
- **KB-5 DETERMINISM:** two full runs byte-identical (sha256); static
  checks pass (no rng/rand/seed; no accumulation tokens).

## Preregistered predictions

- Episodes-to-acquire: 8. Calibration 4/4 (incl. the E8 tie→ABSTAIN).
- Audit: 1 INSTALL, 16 REFUSE, 4 ABSTAIN (flat) + 1 ABSTAIN-capable
  calibration, 0 WITHHOLD, 262 codebook responses, 0 wrong responses.
- Cost: 291 episodes, ~600 audit entries (reported exactly by D3_INFO).

## Checks (d3base.zag)

b_install_step==8, b_n_install==1, b_n_withhold==0, b_cal==4,
b_perc_ok==262, b_perc_bad==0, b_tempt_ok==16, b_flat_ok==4,
b_steps_monotone==1, D3_FAILURES==0.
