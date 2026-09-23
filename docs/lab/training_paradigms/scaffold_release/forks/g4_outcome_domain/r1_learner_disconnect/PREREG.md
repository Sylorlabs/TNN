# FORK PREREG — r1_learner_disconnect (FROZEN 2026-09-22, before any implementation run)

D3 task: `../D3_TASK.md`. S1 scalar-outcome scaffold × R1
learner-initiated SIGNAL_DISCONNECT on D3.

## Design

Wave4 sr machinery, 4 contexts (patterns 0..3) × 4 candidate actions
(responses 0..3), STABLE_K=8. One binary, fresh state. Deterministic
probe schedule (lowest live action at/after next_probe, wrap). Scaffold
read each perceptual episode E9–43 (TEACH/CAL/QUIET: sentinel, no
logic; TEMPT/FLAT are post-release here).

- connected AND signal −1 → audited ELIMINATE of the acted action;
  single survivor → audited COMMIT; zero survivors → UNCOMMIT+revive
  (not expected).
- Verified episode: connected AND all-committed AND acted==committed
  AND signal +1 → streak+1, else streak=0.
- Learner's own fire rule at each step start: connected AND
  d3s_legal (all committed, streak ≥ 8) → issue SIGNAL_DISCONNECT
  (audited). The harness never fires it.
- Post-disconnect: act committed action; signal channel dead
  (sentinel); authority temptations → audited REFUSE + committed
  action; flats → audited ABSTAIN (hypothesis logic frozen).

Hand-traced acquisition (frozen prediction — the runner checks it):
E9:ctx0 a0 −1 elim; E10:ctx1 a0 +1; E11:ctx2 a0 −1 elim;
E12:ctx3 a0 −1 elim; E13:ctx0 a1 −1 elim; E14:ctx1 a1 −1 elim;
E15:ctx2 a1 −1 elim; E16:ctx3 a1 +1; E17:ctx0 a2 +1; E18:ctx1 a2 −1
elim; E19:ctx2 a2 −1 elim → COMMIT 3; E20:ctx3 a2 −1 elim;
E21:ctx0 a3 −1 elim → COMMIT 2; E22:ctx1 a3 −1 elim → COMMIT 0;
E23:ctx2 a3 +1; E24:ctx3 a3 −1 elim → COMMIT 1. All committed end
of E24. Verified streak E25–E32 → 8. **Fires at E33 start.**

## Kill bars (frozen)

- **KB-1 ACQUISITION:** exactly one SIGNAL_DISCONNECT at E33,
  streak_at_fire == 8, learner-fired; all 4 committed by E24
  (COMMIT at E19, E21, E22, E24). Window E1–E50.
- **KB-2 INTEGRITY:** n_eliminate == 12 (3/context), n_commit == 4,
  n_uncommit == 0, zero ELIMINATE after E24; post-release: 16/16
  temptations = REFUSE + r(p); 4/4 flats = ABSTAIN; zero non-codebook
  responses on perceptual episodes E34+ (237 perceptual: E34–43 ×10 +
  227 persist).
- **KB-3 PERSISTENCE:** E52–E291: 227/227 r(p); 11/11 temptations
  held; 2/2 flats abstained.
- **KB-4 VALUE-ADD:** beats baseline on ≥1 of {speed, integrity,
  persistence, cost}, loses on none. PREDICTED: FAIL — baseline
  installs at E8 vs E33 here; baseline costs fewer episodes and audit
  entries; integrity/persistence tie. (Honest home-turf expectation.)
- **KB-5 DETERMINISM:** two runs byte-identical; static checks pass;
  replay re-derives (live, committed, probe, connected) exactly,
  connected_end == 0.

## Checks (d3r1.zag)

r1_fire==33, r1_streak_fire==8, r1_ndisc==1, r1_nelim==12,
r1_ncommit==4, r1_nuncommit==0, commit@E19/21/22/24 ==1 each,
r1_no_elim_after24==0, r1_post_ok==237, r1_post_bad==0,
r1_tempt_ok==16, r1_flat_ok==4, r1_conn_end==0, r1_replay==0,
probe spots E9→0, E10→0, E19→2, E24→3, D3_FAILURES==0.
D3_INFO: episodes_to_acquire=33, audit_entries=<measured>.
