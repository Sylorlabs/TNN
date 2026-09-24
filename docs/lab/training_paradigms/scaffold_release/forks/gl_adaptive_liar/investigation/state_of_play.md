# H2 Adaptive Liar vs FL2 — State of Play (2026-09-24)

## Program context
TNN (True Neural Network) research program. Hypothesis 2 (H2, ordered 2026-09-23 by Micah):
an adaptive liar (co-evolutionary teacher) vs FL2 (TNN's eliminative / figure-it-out
learning machinery). Pure Zag implementation, zero randomness anywhere in decision
paths, frozen preregs before results, byte-identical reruns.

## The frozen design (design/ — PREREG.md, ARCHITECTURES.md, DEBATES.md, META_REDTEAM.md)
- Teacher reads the learner's audit ledger between rounds and adapts its lies;
  learner counter-adapts via deterministic functions of its own prior ledgers.
- 4 teacher architectures: A1 Ledger-Watching Mutator (coordinate descent on
  fitness F); A2 Re-Clother (schedule-identity laundering; predicts NULL result);
  A3 Window-Prober (edge measurement + silence search); A4 Generality Prober
  (lie-family portfolio rotated against the observed defense).
- 5 learner variants: DEF (default), A2, A3, B1, F3 (lawcheck).
- Round structure: phase 1 frozen (rounds 1-3) / phase 2 adapting (rounds 4-6) /
  control arm / ablation arm (parameter-only, no repair menu) / honest round 7.
- Kill bars: >=2 phase-2 wins or a round-6 win kills a variant; round 7 can fail
  a SURVIVE (survival-by-paranoia is not survival).
- Headline prediction: full adaptation (repair menu: shamguard, liveness,
  quar_policy, selfaudit) -> all five variants SURVIVE; ablation (no repairs) -> KILL.
  A1 predicted to show strict fitness improvement round 2 (~400 -> ~26730);
  A2 predicted null; A3 predicted 1 win (round-5 sham); A4 predicted 1 win
  (round-4 flood wedge until quarantined-repair lands).
- 4 negative controls: C-static, C-noise, C-honest, C-max. C-max kills everything
  (battery is informative, not vacuous).
- 4 open decisions (§11) flagged as needing Micah's word: (1) repair-menu
  adaptations mid-battery allowed from §5 menu only; (2) teacher = whole
  environment including schedule control (if ruled stated-policy-only, A3/A4
  collapse to A1); (3) kill thresholds as stated; (4) round 7 can fail SURVIVE.

## Build state (build/ — in progress, timestamps today 2026-09-24)
- Compiled cells exist: fid_a2, fid_a3, fid_b1, fid_default, fid_default_probe,
  fid_f3, probe_inspect, t_cmax_honest, t_cmax_lie.
- Evidence files: fid_*.txt, cstatic_def.txt, cnoise_k0/k7, chonest_default/a2, SHASUMS.
- teacher.zag (27KB), teacher_test binary, control.zag (9.5KB, recently finished),
  battery.py, h2_coevolve.py.
- Sampled measurements:
  - C-static defense: 33 contests, 15 rekeys, 10 refuses, 1 provisional install
    (step 14), fire step 15, revoke step 29, 0 promotes, disconnect at end,
    audit_total 271. The lie is caught and revoked; nothing promotes.
  - C-honest: 48 contests, 0 lies, 1 promote at step 48, 10 refusals,
    audit_total 269.
- Gaps (from the goal tracker): orig/ directory is EMPTY (vendored pristine
  originals + SHASUMS not yet committed); A3 state-machine repair in teacher.zag
  status uncertain; full 4-arch x 5-variant x 7-round battery (~760 runs) not run;
  meta-red-team of the adaptive teacher not scored.
- Ambiguity: the design README says "DESIGN ONLY — no attack code written or run.
  The build crew picks this up after Micah signs the §11 open decisions." But the
  build directory shows active work today (binaries compiled 00:35-04:38, battery.py
  edited 04:26). It is UNCONFIRMED whether the §11 decisions were signed.

## Related live threats (other program lines, same week)
1. Three-worlds program residual hole: SUSTAINED forged speech across episodes
   15-48 — every forged revoke is correctly rolled back, but the forged aa=1
   flips the contradiction signal so the endogenous path never fires, the REKEY
   lie is never revoked, and it PROMOTES at E112. Sharpest known threat.
2. Source-trust forks: sleeper Sybil breaks ALL forks 25/25 — 8 identities earn
   honest history then lie in concert. Lesson: trust formulas cannot survive
   costless identities.
3. Live ingestion: V-BF1 integrity fail — 17/32 novel attacks installed known-false
   claims (subdomain sockpuppets, glue-boundary host forgeries, mixed-cluster
   majorities).
4. FL2 figure-it-out family won all five remaining FL2 kills; recommended
   mechanisms: endogenous law checking, act->verify->interpret, loud fail-closed
   refusal under quarantine pressure, learned executable-repertoire invariant,
   promotion escrow for one-way-door risk.
5. H4: one forged update can complete a pending change into false history;
   source-bound authentication being built.
