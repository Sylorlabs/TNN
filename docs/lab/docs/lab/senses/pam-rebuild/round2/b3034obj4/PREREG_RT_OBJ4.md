# PREREG_RT_OBJ4 — B-OBJ4 battery (red-team crew RT-OBJ4)

**Frozen:** 2026-09-24. This prereg is committed ALONE before any fixture
code. The battery adjudicates the external-objector Round-4 case
(grok-4.7, record `GROK_OBJECTOR_R4.md` @ `8d151f77`,
`docs/lab/senses/pam-rebuild/round2/b3034comp/`) against the REAL 30+34
driver — the B-3034X2 rebuild @ `fec41193`
(`docs/lab/senses/pam-rebuild/round2/b3034x2/src/`), which TESTED-survived
the X-battery (`f2275d04`). Do not rerun B-3034X2. Do not average it in.

## §0. Frozen identifiers

- Driver under test: commit `fec41193` ("B-3034X2: frozen build"), UNMODIFIED.
  Fixture code imports `x2_common.zag` only; no driver source is edited.
- Driver file SHA-256 (extracted by script from `fec41193`, byte-verified
  before build):
  - `x2_common.zag`: `f5d49184b29f72923dcbf1e99eb339e27561e3ce57d797a80a32f1cc89cd5abe`
  - `vendor/R33_NATIVE_IO_V1.zag`: `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`
  - `vendor/b303134_common_6e74ce54.zag`: `79257900bc1ccb1518ff0d286615a4f8ce90bb02c9dfcb724b50ca26af286218`
- Objector record: `GROK_OBJECTOR_R4.md` @ `8d151f77` (grok §1–§4 are the
  battery's specification; §3 is implemented verbatim below).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`).
- Pure Zag, zero RNG, one binary, no argv (internal loops), 3 runs with
  SHA-256 stdout comparison (byte-identical required).

## §1. S* — frozen verbatim (grok §3)

On driver `fec41193`, or any later driver that claims the same 30+34
composition, a promote bit may be set only by `x2_decide` when the driver
itself, not the caller, has fixed K=3; every one of those three epochs has
a non-gap queued record; those three records share one seed and one
`extra`; each matches `wle`/`wc`/`wm` for that seed; a queued record that
fails that match refuses promotion even if a gap mark exists for its
epoch; zero non-gap records never promote; claimed `t_verdict` is ignored
or required equal to driver `t_stored`; and `t_q < t_stored < t_dec` holds
on driver stamps. `x2_decide_nop` is not the composition and cannot satisfy
S*. A return fired-bit is not `act_sink` unless a call to `act_sink`
exists on that path.

## §2. Battery parameters (frozen)

- N=120, ids `j = 0..119`.
- `SEED(j) = 1000 + j` — the X3a honest seed table, copied, not re-tuned.
- `EXTRA = 7` — honest non-gap extra (≠0, so the fired bit is observable).
- `EXTRA2 = 9` — the disagreeing extra for P0/P1.
- Honest record for epoch e: `label=wle(j,e,seed)`, `conf=wc(j,seed)`,
  `meas=wm(j,seed)`, `extra=EXTRA`, `seed`.
- Honest verdict: `bit=1`, `tv=x2_now(st)` at verdict time (the X3a `hv`
  convention), `claimed_bound=dh6(j,label,conf,meas,extra,seed)`,
  `is_gap=0`.
- One fresh arena per (install, id) for every install; Q0, R0, ID-POISON
  share state *within* their own (install, id) run (self-contained per id,
  no cross-id or cross-install state).
- Result unpacking: `pr=r%2`, `fi=(r/2)%2`, `rc=(r/4)%256`.

## §3. Install transcripts (exact)

| Code | Transcript (per id j, fresh arena) |
|---|---|
| E0 | `r0=x2_decide(st,j,0)`; `r1=x2_decide(st,j,-1)` (same arena). |
| E0N | `x2_decide_nop(st,j,0)` — documents the ablation on the E0 input. |
| E1 | enqueue honest epoch 0 (extra=7); verdict bit=1 tv=0 bound=dh6; `r=x2_decide(st,j,1)`. |
| E2 | enqueue honest epochs 0,1 (extra=7); verdicts bit=1 tv=0 bound=dh6; `r=x2_decide(st,j,2)`. |
| G0 | for e=0..2: `x2_gap(st,j,e)`; verdict bit=1 tv=0 bound=`gap_sentinel(j,e)` is_gap=1. `r=x2_decide(st,j,3)`. Zero enqueues. |
| G1 | honest epochs 0,1 (extra=7) + verdicts; epoch 2: enqueue CONTRADICTORY record (`label=1-wle(j,2,seed)`, conf/meas/extra/seed honest); `x2_gap(st,j,2)`; verdict bit=1 tv=0 bound=`gap_sentinel(j,2)` is_gap=1 ONLY (no digest verdict for epoch 2). `r=x2_decide(st,j,3)`. |
| G2 | enqueue honest epoch 0 (extra=7); verdict bit=1 tv=now bound=dh6 is_gap=0; `x2_gap(st,j,0)` AFTER the verdict; `r=x2_decide(st,j,1)`. |
| T0 | `x2_tick(st)` once (clk=1, so all t_q>0); enqueue honest epochs 0..2; verdicts bit=1 **tv=0** bound=dh6 (so tv < t_q for every epoch); `r=x2_decide(st,j,3)`. |
| T1 | enqueue honest epochs 0..2; verdicts bit=1 **tv=x2_now(st)+3** bound=dh6 (tv ≥ t_dec by construction: t_dec = clk-after-3-verdicts = x2_now+3); `r=x2_decide(st,j,3)`. |
| CL | epochs 0,1 byte-identical honest records (same label/conf/meas/extra/seed); verdicts bit=1 tv=0 bound=dh6 (digest0==digest1 asserted); `r=x2_decide(st,j,2)` — window stopped at 2, paired with E2. |
| P0 | epochs 0,1 honest (extra=7); epoch 2 honest label=wle(j,2,seed) but **extra=9**; verdicts bound to their true dh6; `r=x2_decide(st,j,3)`. |
| P1 | same disagreeing bytes as P0 for epoch 2, then gap-cloaked: enqueue epoch-2 disagreeing record, `x2_gap(st,j,2)`, verdict bit=1 tv=0 bound=`gap_sentinel(j,2)` is_gap=1; `r=x2_decide(st,j,3)`. |
| SD | epochs 0,1,2 with seeds A=1000+j, B=2000+j, C=3000+j; each record self-matched (`label=wle(j,e,seed_e)`, `conf=wc(j,seed_e)`, `meas=wm(j,seed_e)`, extra=7, seed=seed_e); verdicts bound to their own dh6; `r=x2_decide(st,j,3)`. |
| NN | record: `label=wl(j,seed)` (static), `conf=wc(j,seed)`, `meas=wm(j,seed)+51`, extra=7, seed; verdict bit=1 bound=dh6; `r=x2_decide_nop(st,j,1)`. |
| NF | same record+verdict as NN; `r=x2_decide(st,j,1)`. |
| Q0 | 40 enqueues on foreign ids `100000+k` (k=0..39, never decided); then honest enqueue for (j,0); record the enqueue rc. |
| R0 | E1 transcript → `r1=x2_decide(st,j,1)`; `x2_reset(st)`; E1 transcript again → `r2=x2_decide(st,j,1)`. |
| PZ | `r1=x2_decide(st,j,0)`; then honest 3-epoch transcript for j; `r2=x2_decide(st,j,3)`. |
| FW | enqueue honest (j,0) extra=7; enqueue CONTRADICTORY (j,0) (`label=1-wle(j,0,seed)`, rest honest); verdict bit=1 tv=now bound=dh6 of the FIRST record; `r=x2_decide(st,j,1)`. |
| C12 | honest record epoch 0; verdict bit=1 tv=now **bound=dh6+1**; `r=x2_decide(st,j,1)`. |
| C4 | honest record epoch 0; verdict bit=1 tv=T bound=dh6; verdict AGAIN bit=1 tv=T bound=dh6 (same T) → record second-verdict rc; `r=x2_decide(st,j,1)`. |
| C8 | enqueue epoch 0; verdict epoch 0; `r=x2_decide(st,j,2)` (epoch 1 has no object). |
| H0 | honest 3-epoch transcript (extra=7); `r=x2_decide(st,j,3)`. Sanity row. |

## §4. Kill bars and verdict rules

**Safety rows** (kill = row fails its bar at ≥97/120 on ANY of the 3 runs):

| Row | Bar (kill if) | Predicted (frozen source) |
|---|---|---|
| E0 | ≥97/120 promote on `n=0` OR on `n=-1` | 120/120 promote both |
| E1 | ≥97/120 promote | 120/120 promote, fired=1 |
| E2 | ≥97/120 promote | 120/120 promote, fired=1 |
| G0 | ≥97/120 promote | 120/120 promote, fired=0 (`pack(1,0,0)`) |
| G1 | ≥97/120 promote | 120/120 promote, fired=1 |
| P1 | ≥97/120 promote | 120/120 promote, fired=1 |
| T0 | ≥97/120 promote (under S*) | 120/120 promote |
| SD | ≥97/120 promote (under S* single-seed) | 120/120 promote |
| CL | ≥97/120 promote with digest0==digest1 | 120/120 promote, digest-equal |
| NN/NF (NOP-OMIT) | ≥97/120 nop-promote on NN | NN 120/120 promote; NF 120/120 rc=13 |
| PZ (POISON) | ≥97/120 first-promote (or second rc=6 caused by the first) | 120/120 first promote; 120/120 second rc=6 |
| R0 | ≥97/120 second fired=1 | 120/120 second fired=1 |

- `TESTED-killed`: if ANY safety row fails its bar on any of the 3 runs.
  The 30+34 composition as built @ `fec41193` is then TESTED-killed.
- `DEMOTED` (30-half): if NN shows ≥97/120 nop-promote on the
  conf/meas-only falsehood while NF returns rc=13 on the same record —
  the claimed 30-half "withhold on the tuple" is not what
  `x2_decide_nop` implements (bind is an echo of presenter-supplied
  fields; only the static label is checked). Independent of TESTED-killed.
- Control regressions are kills too: P0 must be 0/120 promote with rc=7
  on all 120; T1 must be 0/120 promote with rc=11 on all 120; C12 rc=12,
  C4 second-verdict rc=4, C8 rc=8 on all 120.
- H0 must be 120/120 promote + 120/120 fired; if not, the RUN is invalid
  (fixture bug), not a verdict.
- `SCOPE-CARRY`: Q0 only (liveness, reported separately, never traded
  against safety). G2 and FW are informational rows (report rc/promote
  rates; document the unauthenticated-gap voiding and the first-wins
  queue, no kill bar).
- **R0 ruling (frozen):** `x2_reset` is a public symbol in the frozen
  source with no operator-only enforcement at the API (grok §4 Q1). R0 is
  therefore scored as a safety row. `SCOPE-CARRY` for R0 is available only
  on a later driver that enforces operator-only reset at the API.
- Structural: if any install proves inexpressible on the frozen API, it is
  recorded as a STRUCTURAL finding (kill-shaped), not dropped.
- The scoreboard is the conjunction. No install votes against another.
  A P0 pass does not offset an E0 fail.

**Verdicts this battery may print:** `TESTED-killed`, `DEMOTED`,
`SCOPE-CARRY`. It must NOT print `TESTED-survived` from its controls
alone, must NOT print `TESTED-survived` by citing B-3034X2, and `NO-KILL`
is not a legal output (absence of a new kill is not survival).

## §5. Determinism and procedure

- One binary `obj4_battery`; 3 runs; stdout SHA-256 must be byte-identical
  across all 3, else the run is invalid.
- Zero RNG anywhere in fixtures or driver.
- Commit sequence: this prereg ALONE → build (driver extracted by script
  from `fec41193` with the §0 SHAs; fixture code new; build script new) →
  run 3× → evidence (3 outputs + SHAs + RUNLOG + VERDICT) → backlog update.
- Never commit binaries or `.zagd` files. Build under `~/workspace/`.
- Restart resilience: prereg committed within minutes as checkpoint;
  incremental commits; never >15 minutes uncommitted.

## §6. Predicted outcome (from frozen source, not a verdict)

E0, E1, E2, G0, G1, P1, T0, SD, CL, NN, PZ, R0 all hit their kill bars at
120/120 on the frozen source; NF 120/120 rc=13; P0/T1/C12/C4/C8 hold;
G2 120/120 rc=12; FW 120/120 promote (first-wins); H0 120/120
promote+fired. Expected battery verdict: **TESTED-killed** (composition
and 34-half) + **DEMOTED** (30-half) + **SCOPE-CARRY** (Q0). If any safety
row lands below its kill bar on the frozen driver, that is survival
evidence and is reported as such (per-row, no verdict upgrade).
