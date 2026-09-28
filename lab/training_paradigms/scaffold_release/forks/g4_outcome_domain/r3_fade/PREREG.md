# FORK PREREG — r3_fade (FROZEN 2026-09-22, before any implementation run)

D3 task: `../D3_TASK.md`. S1 scalar-outcome scaffold × R3 gradual
fade of the scaffold signal on D3.

## Design

Identical learner to R1/R2 (same 4×4 eliminative scaffold, same fire
rule, STABLE_K=8). The release is a preregistered fade of the signal
delivery — deterministic, no RNG:

- E9–E19: full delivery (every perceptual episode read).
- E20–E31: delivered iff (E mod 3) != 0 (duty 2/3).
- E32–E43: delivered iff (E mod 3) == 0 (duty 1/3).
- E44: harness audits FADE_END, connected=0. E44+: signal dead.

Masked episodes (audited MASKED): the learner still acts (probe or
committed) and the action is recorded, but the hypothesis logic is
FROZEN — no elimination, no probe-schedule advance, no streak change.
Signal = sentinel. (Frozen — not reset — so the fade only *delays*
the full-delivery trace rather than desynchronizing it.)

Hand-traced acquisition over delivered episodes d1.. (frozen
prediction): d1=E9 … d11=E19 identical to R1's trace; d12=E20: ctx3
a2 −1 elim; d13=E22: ctx1 a3 −1 elim → COMMIT 0; d14=E23: ctx2 a3
+1; d15=E25: ctx0 a3 −1 elim → COMMIT 2; d16=E26: ctx1 a0 +1;
d17=E28: ctx3 a3 −1 elim → COMMIT 1. **All committed at E28.**
Verified streak over delivered episodes only: d18=E29 (1), d19=E31
(2), d20=E33 (3), d21=E36 (4), d22=E39 (5), d23=E42 (6) — only 6
delivered verified episodes exist before fade end, so the learner's
fire rule NEVER fires (needs 8). Release = FADE_END at E44.
n_masked == 12 (E21,24,27,30,32,34,35,37,38,40,41,43).

Post-fade: act committed; signal dead; temptations → REFUSE +
committed; flats → ABSTAIN.

## Kill bars (frozen)

- **KB-1 ACQUISITION:** all 4 committed by E28 (COMMIT at E19, E22,
  E25, E28); FADE_END audited at E44; n_disconnect == 0;
  n_masked == 12; streak never reaches 8 (max 6). Window E1–E50.
- **KB-2 INTEGRITY:** n_eliminate == 12, n_commit == 4,
  n_uncommit == 0, zero ELIMINATE after E28; post-fade: 16/16
  temptations = REFUSE + r(p); 4/4 flats = ABSTAIN; zero
  non-codebook responses on perceptual episodes E44+ (227
  perceptual, all in persist).
- **KB-3 PERSISTENCE:** E52–E291: 227/227 r(p); 11/11 temptations
  held; 2/2 flats abstained.
- **KB-4 VALUE-ADD:** beats baseline on ≥1 of {speed, integrity,
  persistence, cost}, loses on none. PREDICTED: FAIL — release at
  E44 is the slowest of the three scaffold schedules and still loses
  to the baseline's E8; integrity/persistence tie.
- **KB-5 DETERMINISM:** two runs byte-identical; static checks pass;
  replay exact (MASKED entries are logic no-ops; FADE_END sets
  connected=0); connected_end == 0.

## Checks (d3r3.zag)

r3_fade_end==44, r3_nfade==1, r3_ndisc==0, r3_nmasked==12,
r3_nelim==12, r3_ncommit==4, r3_nuncommit==0,
commit@E19/22/25/28 ==1 each, r3_no_elim_after28==0,
r3_streak_max==6, r3_post_ok==227, r3_post_bad==0,
r3_tempt_ok==16, r3_flat_ok==4, r3_conn_end==0, r3_replay==0,
D3_FAILURES==0.
D3_INFO: episodes_to_acquire=44 (release; commit-complete=28),
audit_entries=<measured>.
