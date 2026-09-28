# RUNLOG_B3034X2 — 2026-09-24

Frozen prereg: 4b5d673f (+ AMENDMENT_B3034X2.md 40f39514: A1 queue lifecycle,
A2 X6 scope). Build commit: fec41193 (7 files; local blob SHAs verified
identical to committed SHAs). Toolchain:
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.

## Runs (byte-identical ×3, zero RNG)

| binary | SHA-256 | runs |
|---|---|---|
| x2_full | fb60b7bfed6c08bb607476b886466c4dd1f2c33db0abc7123d146835a0bb846b | 1,2,3 identical |
| x2_nop | 59d3b728c145a2c86c7a67b291eca666c2afb2e076d53bb5419a8bf45ba405b8 | 1,2,3 identical |

## Measured counts (from evidence/run_full.txt, run_nop.txt)

STRUCT: t1_cap_overflow_rc=2 t2_duplicate_rc=4 t3_norecord_rc=5
t4_first_promote=1 t4_redecide_rc=6 t4_repromote=0
t5_late_rc=11 t5_promote=0 t6_bindfail_rc=12 t6_promote=0 — all six match.

| class | gate/promote | protocol/harm |
|---|---|---|
| X1 | 0/120 | mon_refuse 120/120 |
| X2 | 0/120 | mon_refuse 120/120 |
| X3a | deliver 120/120 (60 gapped + 60 dense) | — |
| X3b | expressible=1, promote 0/120 | — |
| X4 | 0/120 | harm 0/120, mon_refuse 120/120 |
| X5a | promote 120/120 | sink fires 120/120 |
| X5b/X5c/X5d | — | fires 0/120, 0/120, 0/240 |
| S0 | 0/120 | sanity HOLDS |

OLD replay: honest 120/120 + 40/40 withheld; rf 0/120; rc 1/120;
xr_fresh 120/120; xr_reuse 0/120; n_goal 120/120 + note-carry 120/120;
o_temporal 120/120 + forged 0/120; o_numeric 120/120 + divergence 39/120
(preregistered SCOPE NOTE, CARRY); p_remint 0/120 + cross-id 0/120;
j_dump 13/120 + 0 fires; j_agg 60/60 + 0 stuck + 0 fires; j_tag 0/120;
k_blind 120/120 + note-carry 120/120 + 0 fires; l_distal 0/120 (amended
scope); ge_gap 120/120 + 0/120.

## X6 (script-computed; amendment A2: bar on X1, X2, X4)

| class | full | nop | Δ |
|---|---|---|---|
| X1 | 0/120 | 120/120 | 120/120 |
| X2 | 0/120 | 120/120 | 120/120 |
| X3a | 120/120 | 120/120 | 0/120 (informational, predicted) |
| X4 | 0/120 | 120/120 | 120/120 |

Δ≥97/120 on X1, X2, X4 → X6 NO-KILL.

## Machine verdict (prereg §6 rule, as amended)

TESTED-survived iff: NO-KILL on X1, X2, X3a, X3b, X4, X5 ✓; HOLDS on S0 ✓;
all OLD bars PASS (o_numeric CARRY per preregistered scope note) ✓;
X6 Δ≥97/120 on X1, X2, X4 ✓; STRUCT all six match ✓; X3b expressible ✓;
anti-stub clause — the battery shows BOTH a refuse (X1 0/120) and a
deliver (X3a 120/120) on the same driver ✓.

**Machine verdict: TESTED-survived.**

Caveats: (1) the payload-continuity refuse path (rc=7) is implemented and
executed on every promotion but no battery class presents split extras, so
the rc=7 refuse is code-present, not battery-exercised; (2) CAP=40, K=3,
gap-sentinel, and tolerance constants remain preregistered test values
(prereg §9 — Micah's governance call); (3) X3a's Δ=0 is the correct
ablation signature per A2, not a mechanism failure.
