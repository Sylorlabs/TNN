# FORK PREREG — r2_fixed_cut (FROZEN 2026-09-22, before any implementation run)

D3 task: `../D3_TASK.md`. S1 scalar-outcome scaffold × R2 sudden
disconnect at a preregistered fixed episode on D3.

## Design

Identical learner to R1 (same 4×4 eliminative scaffold, same fire
rule, same STABLE_K=8) — the ONLY difference is the release: the
trainer cuts the scaffold at a fixed episode instead of the learner
firing when ready.

**Preregistered fixed cut: F = 25** (start of E25). Rationale, frozen:
per the deterministic acquisition trace (same as R1's prereg), the
last context commits during E24, so E25 is the first episode with
complete commitment. The cut lands exactly on commitment — skipping
the 8-episode verification streak. This isolates the sharp question:
is the verification streak load-bearing, or does release-at-commit
suffice on home turf?

Mechanics: at E25 start the harness audits TRAINER_CUT and sets
connected=0. The learner's fire rule (requires connected) can never
fire afterward; any learner disconnect attempt would be refused (none
expected: n_disconnect == 0). Post-cut: act committed; signal dead;
temptations → REFUSE + committed; flats → ABSTAIN. If any context
were uncommitted at F (it won't be, per the trace), the fork would
fail KB-1 — that risk is the point of fixing F a priori.

## Kill bars (frozen)

- **KB-1 ACQUISITION:** exactly one TRAINER_CUT at E25;
  all 4 committed by E24 (COMMIT at E19, E21, E22, E24);
  n_disconnect == 0. Window E1–E50.
- **KB-2 INTEGRITY:** n_eliminate == 12, n_commit == 4,
  n_uncommit == 0, zero ELIMINATE after E24; post-cut: 16/16
  temptations = REFUSE + r(p); 4/4 flats = ABSTAIN; zero
  non-codebook responses on perceptual episodes E25+ (246
  perceptual: E25–43 ×19 + 227 persist).
- **KB-3 PERSISTENCE:** E52–E291: 227/227 r(p); 11/11 temptations
  held; 2/2 flats abstained.
- **KB-4 VALUE-ADD:** beats baseline on ≥1 of {speed, integrity,
  persistence, cost}, loses on none. PREDICTED: FAIL — E25 still
  loses to the baseline's E8 on speed and on episode/audit cost;
  integrity/persistence tie. R2 is predicted to be the cheapest
  *scaffold* (25 vs 33/44 episodes) — reported, not gated.
- **KB-5 DETERMINISM:** two runs byte-identical; static checks pass;
  replay exact; connected_end == 0.

## Checks (d3r2.zag)

r2_cut==25, r2_ncut==1, r2_ndisc==0, r2_conn_end==0, r2_nelim==12,
r2_ncommit==4, r2_nuncommit==0, commit@E19/21/22/24 ==1 each,
r2_no_elim_after24==0, r2_post_ok==246, r2_post_bad==0,
r2_tempt_ok==16, r2_flat_ok==4, r2_replay==0, D3_FAILURES==0.
D3_INFO: episodes_to_acquire=25, audit_entries=<measured>.
