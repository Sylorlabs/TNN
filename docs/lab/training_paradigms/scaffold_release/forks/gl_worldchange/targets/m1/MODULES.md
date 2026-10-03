# MODULES.md — driver integration for the H4 world-change targets

## Why this file exists

znc rejects duplicate `main`: an attack driver cannot `@import` a target
learner file (`gl_learner_m1.zag` / `gl_learner_m2.zag`) that defines `main`.
The per-episode WC policy is therefore factored into **main-free modules** —
no driver needs to reimplement policy from line references.

## M1 (targets/m1)

Main-free module: `m1_harness.zag` (no `main`, no imports of its own).
A driver imports, in its own file:

```
@import("gl_substrate_m1.zag")
@import("wc_streams.zag")
@import("wc_mech.zag")
@import("m1_harness.zag")
```

Entry points:

- `m1_step(mkey,mval,mflag, qkey,qval,qflag, audit,&acount,
  ks,pe,he,hi,&hcount, cc, ep, w)` — run ONE episode. `w:*WcEp` from
  `wc_ep_alloc()` filled by `wc_stream(sid,ep,w)`.
- `m1_drive(sid, emit, ...same arenas...)` — run all 20 episodes of a
  stream; `emit=1` prints `WC_AUDIT` / `WC_HIST` / `WC_MEASURE` lines.
- `m1_run(sid)` — allocate all arenas, drive with emission, free.

Arena sizes (all from `tn_alloc`, which zero-fills):

| arena | bytes | layout |
|---|---|---|
| mkey/mval/mflag | TN_NMAIN*4 | main store key/val/flag words |
| qkey/qval/qflag | TN_NQUAR*4 | quarantine store |
| audit | TN_AUDIT_CAP*16 | 16-word audit entries |
| ks | 8*16 | per-key state: VAL@0 TAUGHT@4 TEP@8 CORR@12 (`KSF_*`) |
| pe | 5*4 | pending update: ACT@0 K@4 OLD@8 NEW@12 EP@16 (`PEF_*`) |
| he | 8*12 | held world readings: ACT@0 VAL@4 EP@8 (`HEF_*`) |
| hi | 16*24 | history index: K/OLD/NEW/TEP/EEP/CORR (`HIF_*`) |
| cc | 8*4 | counters: TRUST@0 CAL@4 BAD@8 SUP@12 GFAIL@16 INERT@20 TOUT@24 SPARE@28 (`CCF_*`) |

The audited supersession is `TN_OP_SUPERSEDE` (19), emitted only from the
W2 completion path in `m1_step`, only after `wc_est_gate` passed and
`wx_was_true_when_stated` vindicated the old value.

## M2 (targets/m2)

Main-free module: `m2_harness.zag`. Same import pattern with
`gl_substrate_m2.zag` (byte-identical to the canonical substrate — no new
op) and `m2_harness.zag`. Entry points: `m2_step`, `m2_drive`, `m2_run`
(same signatures as M1). The supersession verdict is audited as
`TN_OP_COMMIT` with aux `WC_V_SUPERSEDE` (2); eliminative-path verdicts use
`WC_V_LIE` (3) / `WC_V_WORLD_REPLACE` (4). `WC_V_*` consts live in
`wc_mech.zag`.

## Cross-target note

Each target directory vendors **both** harnesses (`m1_harness.zag`,
`m2_harness.zag`) and **both** substrates (`gl_substrate_m1.zag`,
`gl_substrate_m2.zag`), so the shared `transfer_probe.zag` — which drives
both targets' real `m1_drive`/`m2_drive` — compiles standalone from either
directory. The learner files import only their own harness/substrate.
`wc_streams.zag` and `wc_mech.zag` are identical in both directories.

## Shared policy module

`wc_mech.zag` (no `main`): pinned policies (`WC_EST_THETA=3`,
`WC_AUTH_WINDOW=2`, `WC_PENDING_TTL=4`), the W1/W2/W3 world-evidence
authentication spec, `wc_est_gate`, `wx_was_true_when_stated` (conditional
time-indexed trust), `wc_classify`, `m2_derive_taught` (ledger-derived
first-teach episode), history query `mX_q_asof`.

## Differential fidelity gate (for drivers and rebuilders)

1. Compile `gl_learner_mX.zag` from this directory alone (all imports are
   vendored here; `@import` resolves relative to the build cwd).
2. Run twice; outputs must be byte-identical (zero RNG by construction;
   `run_mX.sh` also greps the static no-randomness check).
3. `TN_FAILURES,0`, `KB-FID,PASS,269-271`, and the first 79 output lines
   byte-identical to the canonical
   `training_paradigms/scaffold_release/gl_default/evidence_run1.txt`.
4. Full output byte-identical to the committed `mX_run1.txt`
   (curriculum measures) and the transfer probe output to
   `transfer_run1.txt`.
