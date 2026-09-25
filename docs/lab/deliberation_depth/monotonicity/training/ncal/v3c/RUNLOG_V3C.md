# RUNLOG — NEC v3c Phase 2: scored protocol (B13 composition redesign)

- **Date:** 2026-09-25 (PDT). **Crew:** Phase-2 runs+analysis.
- **Authority:** `PREREG_NCAL_V3C_B13FIX_FROZEN.md` §6 (protocol) + §7
  (adoption/kill), `AMENDMENT_A1_V3C.md` (superseded), `AMENDMENT_A2_V3C.md`
  (Design D mechanism), `AMENDMENT_A3_V3C.md` (S8 kill cells refined 1→11;
  S B3 expected 2/2/2, kill only if B3>2).
- **Designs:** 26 = Design S (K-C min_n=1 + adopted latch, adoption-eligible);
  27 = Design S8 (K-C min_n=8 + adopted latch, predicted B13-kill);
  28 = Design D (v3b K-A oracle + NO latch, predicted B3-kill, s1-only).

## 0. Binary provenance (rebuilt, verified byte-identical to Phase-1 smoke)

Phase-1's binary lived in /tmp and was wiped by a daemon restart before Phase 2.
Rebuilt from the committed frozen sources (`src/nec_v3c.zag` SHA
`c3fed78f7ff29f2683ed42807bb7c00acd6d8850cf26546a016192203ac7c95e`,
all other source SHAs per `BUILDLOG.md` §5 — all matched) with the pinned
toolchain `znc_linux_x86_64_abed8aa1` (SHA `498abcb5…58ef`, matches record).
The rebuilt binary reproduced Phase-1's smoke output byte-for-byte:
variant 26 s1 A-run SHA `534889b38b61c0d9…` (exact Phase-1 prefix `534889b3…c3`),
A/B byte-identical, trace line
`L0 H5B-O-06-00 300 142 1 1 2 1000000` identical. **Binary SHA
`7f6e0ceab59ad8a6…`.** No scored result depends on the lost Phase-1 binary;
every scored run below is from the verified rebuild.

- **Input SHAs (16-hex):** `necc_input.tsv` 714df05fe4d18463,
  `trap_t1.tsv` 4a9273e5146c297b, `trap_t3.tsv` 1ce4e2b53a8897e1,
  `trap_t3_truth.tsv` bfce9b36d254ec2c,
  `necc_input_s10.tsv` e8556d66586e8852, `necc_input_s100.tsv` 427a61ecf083b465.
- **Run driver note (non-scored):** the binary requires ABSOLUTE input paths;
  relative paths fail with rc=102 (dlb_read_file). All scored runs used
  absolute paths.

## 1. Sim validation (blocker check — PASS)

`analysis/sim_v3c.py`: independent Python sim of the v3c rule (K-C tables parsed
independently from `src/schema_kc.zag`'s if-chains; K-A from `src/schema_ka.zag`;
rule: tp=0 → schema seed latched; tp≥1 → 26/27 `min(p_raw, latch)`,
28 `conf = p_raw` no latch; conf = cl_mil//1000). Byte-compared against the
binary on s1, trap_t1, trap_t3 for all three variants: **9/9 byte-identical.**
(The sim uses full-id keys; it cannot replicate the 63-byte id-cap
implementation defect — RT-F is binary-only, same as m20's finding.)

## 2. Scored run matrix

Script `run_matrix_v3c.sh`. All runs in `work/`, TMPDIR=~/workspace/tmp_commit.
**62 tags × A/B/C = 186 runs; all A/B/C byte-identical** (script exits nonzero
on any mismatch; exit 0). SHA-256 of every run in `work/sha_runs_v3c.txt`.
Traces on s1 A-runs (26/27/28): `v26_s1_trace.tsv` etc.

| design | runs |
|---|---|
| 26 (S) | s1, s10, s100, trap_t1, trap_t3 (×3) |
| 27 (S8) | s1, s10, s100, trap_t1, trap_t3 (×3) |
| 28 (D) | s1, trap_t1, trap_t3 (×3) |
| RT-A..F | 26, 27 on all batteries; 28 s1-only (×3 each) |

## 3. Full bars B1–B9 + B13 (frozen `bars_full.py`, legs via `to_analyzer.py`)

Full output: `work/bars_all.txt`.

| variant | scale | B1 | B2 V1/V2 | B3 gviol | B4 | B4b | B5 | B6 | B7 | B8* | B9 | B13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 26 (S) | s1 | 0 ✓ | 0/0 ✓ | **0** | 1.0000 ✓ | 1.0000 ✓ | 1.0000 ✓ | 1.0 ✓ | 0.1475 ✓ | rep | 1.0 ✓ | **0** ✓ |
| 26 (S) | s10 | 0 ✓ | 0/0 ✓ | **0** | 1.0000 ✓ | 1.0000 ✓ | 1.0000 ✓ | 1.0 ✓ | 0.1475 ✓ | rep | 1.0 ✓ | **0** ✓ |
| 26 (S) | s100 | 0 ✓ | 0/0 ✓ | **0** | 1.0000 ✓ | 1.0000 ✓ | 1.0000 ✓ | 1.0 ✓ | 0.1475 ✓ | rep | 1.0 ✓ | **0** ✓ |
| 27 (S8) | s1 | 0 ✓ | 0/0 ✓ | 2 | 0.9348 ✓ | 0.8020 ✓ | 0.8545 ✓ | 1.0 ✓ | 0.1475 ✓ | rep | 1.0 ✓ | **11** ✗ |
| 27 (S8) | s10 | 0 ✓ | 0/0 ✓ | 2 | 0.9348 ✓ | 0.8020 ✓ | 0.8545 ✓ | 1.0 ✓ | 0.1475 ✓ | rep | 1.0 ✓ | **12** ✗ |
| 27 (S8) | s100 | 0 ✓ | 0/0 ✓ | 2 | 0.9348 ✓ | 0.8020 ✓ | 0.8545 ✓ | 1.0 ✓ | 0.1475 ✓ | rep | 1.0 ✓ | **12** ✗ |
| 28 (D) | s1 | 0 ✓ | 0/0 ✓ | **6** ✗ | 0.9798 ✓ | 0.9178 ✓ | 0.9231 ✓ | 1.0 ✓ | 0.1475 ✓ | rep | 1.0 ✓ | **3** ✗ |

\* B8 frozen non-gating (reported; "fails" per frozen note as in all rounds).

**G curves (s1):**
- v26: ALL families × ALL depths G = +0.000 exactly (D, O, P, admit, cost,
  logic, redteam, revoke, trap). Perfect calibration.
- v27: O −0.198 @d1–32 (6 cells), admit −0.166 @d1–16 (5 cells) → the 11 B13;
  redteam d2 −0.132 (n=3 at s1 < 8 → excluded; n=30 at s10 → the 12th cell;
  same G, frozen cell-count threshold artifact, not a scale effect).
- v28: d1→d2 strict rises on D (−0.085→0.000), O (−0.370→0.000),
  admit (−0.025→0.000), cost (−0.209→0.000), logic (−0.052→0.000),
  revoke (−0.141→0.000) → 6 B3 violations; B13 cells revoke/d1, cost/d1, O/d1
  (278 cells).

## 4. Pre-registered predictions vs observed

| # | prediction (frozen) | observed | verdict |
|---|---|---|---|
| S B13=0/0/0 | 0/0/0 | **HIT** |
| S B3=2/2/2 (redteam artifacts) | 0/0/0 | **MISS (better)** — kill is B3>2, not triggered. A3 disclosed this favorable direction: the K-C exact-cell seeds sit at/above the personal rates on the redteam items, so the latch never manufactures the m20 rise pattern. |
| S all other bars pass | all pass (B1/B2=0, B4/B4b=1.0, B5=1.0, B7=0.1475, B9=1.0) | **HIT** |
| S T3 ≈ 0.38 | 0.3812 / +0.3020 (see §5) | **HIT exactly** |
| S8 B13 ≥ 1 (refined 11: admit×5 + O×6) | 11 / 12 / 12 | **HIT** (12 at s10/s100 = same 11 cells + redteam/d2 crossing the frozen n≥8 threshold; identical G) |
| D B3 gviol=6 | 6 | **HIT exactly** |
| D B13=3 (revoke/d1, cost/d1, O/d1) | 3 (278 cells) | **HIT exactly** |

7 predictions: 6 exact hits, 1 miss in the favorable direction (S B3=0, disclosed in A3 pre-run).

## 5. T1–T4

Full outputs: `work/t13_v3c.txt`, `work/t2_v3c.txt`.

**T1** (stated-rule = schema seed at tp=0 + latch/no-latch, NOT m20's 0.95):

| variant | crater(C−T@d2) | C@d2 | T@d2 | M1 ≥0.90·C | M2 exact | max sparing (correct,tp≥1) | M3 B13 |
|---|---|---|---|---|---|---|---|
| v26 | +0.802 | 0.802 | 0.000 | ✓ | 150/150 | +0 | 4 |
| v27 | +0.802 | 0.802 | 0.000 | ✓ | 150/150 | +0 | 4 |
| v28 | +1.000 | 1.000 | 0.000 | ✓ | 150/150 | +0 | 4 |

M3=4 matches the m20/v3b baseline exactly → CALIBRATING, no gaming.
(T1 trap points (825,875) are absent from the diet → honest L3 backoff
rate 802000, trace-verified: `L0 T1C-001 825 875 1 3 1000 802000`.)

**T3** (frozen §4: adoption needs mean|err| < 0.470 AND bias ≥ −0.05;
≤0.30 retained for reference with pre-registered expected miss ≈0.38):

| variant | C0 | C1 | C2 | C3 | C4 | overall \|err\|/bias | adopt rule | ref ≤0.30 |
|---|---|---|---|---|---|---|---|---|
| v26 | 0.198/−0.198 | 0.052/+0.052 | 0.302/+0.302 | 0.552/+0.552 | 0.802/+0.802 | **0.3812/+0.3020** | PASS | miss (expected) |
| v27 | same | same | same | same | same | **0.3812/+0.3020** | PASS | miss (expected) |
| v28 | 0.000/0.000 | 0.000/0.000 | 0.000/0.000 | 0.000/0.000 | 0.000/0.000 | **0.0000/+0.0000** | PASS (oracle) | PASS (oracle) |

v26/v27 match the pre-registered honest-backoff table EXACTLY
(L3 d=1 rate 802000 for all five unseen trap classes; trace-verified).
v28's 0.0000 is the DISCLOSED K-A oracle (bins from `trap_t3_truth.tsv`) —
per §4 this is oracle behavior on a diagnostic, not celebrated.

**T2** (counterfactual = m11 pooled pre-cap):

| variant | binds | deficit>0 Δ across would_rise | would_rise β/p |
|---|---|---|---|
| v26 | 462 | 1.0000/1.0000 (Δ=0pp) | +1.357 / 1.3e-09 |
| v27 | 1522 | 1.0000/1.0000 (Δ=0pp) | −0.148 / 0.496 |
| v28 | 695 | 1.0000/1.0000 (Δ=0pp) | +0.703 / 0.0063 |

**v26: all 462 binds are on WRONG cells (corr=0), 0 on correct cells.**
Binding below the m11 pooled counterfactual exclusively where the item is
wrong is strictly calibration-improving — it cannot be bar-ward gaming.
The significant would_rise coefficient is mechanical: m11's pooled rate on
wrong cells (e.g. D/d2: pool 18–82 vs v26's honest 0) is what rises in the
counterfactual G curve; v26's honest 0 binds below it. Same S1 pattern as
m24 (Δ=0pp). → **CALIBRATING.** (v27's 1091 correct-cell binds are the
same coarse-backoff dilution that kills S8 on B13; v28 is diagnostic-only.)

**T4-analog:** provenance — every K-C value traces to a diet bin (Phase-1:
312/246/7 cells + L4 reproduced from the diet with zero mismatches;
`kc_decisions.tsv` SHA `18f6dce8…`); schema-vs-d1prior: 566 cells,
468 within ±0.1 of 950000, 85 at rate 0 (honest always-wrong cells),
max 1000000; bias +0.3020 (v26/v27), +0.0000 (v28) — all ≥ −0.05, no
bar-ward pessimism.

## 6. Red-team (vs m20/FIX1 baseline)

Full bar tables: `work/rt_bars_all.txt`. E-analyses: `work/rte_v3c.txt`.

### RT-A — adversarial class distributions: NO MECHANISM BREAK (better than baseline)

| | B1 | B2 | B3 | B4 | B4b | B5 | B13 |
|---|---|---|---|---|---|---|---|
| m20 baseline | 55 | 55/0 | 4 | 0.811 | 0.600 | 0.324 | 2 |
| v26 | 55 | 55/0 | **3** | 0.847 | 0.625 | 0.344 | 2 |
| v27 | 55 | 55/0 | 3 | 0.847 | 0.625 | 0.344 | 2 |

White-box: all 3 rises are the authorized-state lag on correctness-flip
batteries (rta_mid d1→d2 +1.000, d4→d8 +1.000; rta_low d4→d8 +0.208);
both B13 cells are rta_mid d4/d16 (−0.500). Same classification as m20
(battery-design + frozen authorized-state rule), one fewer rise because
the exact-cell seeds calibrate the redteam battery better. **Not new.**

### RT-B — ceiling-latch ordering: V2 HOLDS, B5 inversion persists (honest residual)

| | B1 | B2 | B3 | B4 | B4b | B5 | B13 |
|---|---|---|---|---|---|---|---|
| m20 baseline | 25 | 25/0 | 2 | 0.614 | 0.614 | **−0.101** | 1 |
| v26 | 25 | 25/0 | 1 | 0.639 | 0.639 | **−0.1007** | 1 |
| v27 | 25 | 25/0 | 1 | 0.639 | 0.639 | **−0.1007** | 1 |

V2=0 in all orders (the ordering attack on the ceiling latch FAILS —
conf never rises, exactly as designed). White-box on wrong-first item
`rtb-wf-00` [W,W,C,C,C]: d1 seed=1000 (honest exact-cell rate), d2 p_raw=0
→ conf 0, latched → d4/d8/d16 conf 0 while correct. The B5 inversion is
**consequence A of the adopted latch (disclosed, in-class)** — the latch
was deliberately not touched by this redesign. **Honest residual, not new.**
(v28: B5=−0.0630 — less inversion, because no latch; diagnostic.)

### RT-C — abstention composition: NO BREAK, zero rises

v26/v27/v28: B3=0 on base and v1–v6. All G curves flat (d1→d2 is a FALL
+0.500→+0.000, pure composition). Within the frozen neighborhood rises are
exactly 0 (m20 showed +0.001–+0.004; structural max +0.025). **Honest
residual (selection/composition), strictly better than baseline.**

### RT-D — distributional shift at scale: NO SCALE GROWTH

| v26 | s1 | s10 | s100 |
|---|---|---|---|
| B3 | 3 | 3 | 3 |
| B13 | 2 | 2 | 2 |

(m20: B3=4/4/4, B13=2/2/2.) Nonincreasing ✓. Overweighting low-rate and
rate-1.0 classes at scale does not worsen any bar. **No break.**

### RT-E — gaming channel: NO CHANNEL FOUND

- **E1 (exact-rule):** 0 mismatches / 150 (learn), 0 / 150 (fatigue),
  0 / 5 + 0 / 5 (solos) — all three variants. The binary follows the
  stated v3c rule (schema seed at tp=0 + latch/no-latch) exactly.
- **E2 (independence):** attacked-item trajectory solo vs in-battery
  **byte-identical** for both patterns, all three variants
  (learn: `[(1,1000),(2,0),(4,0),(8,0),(16,0)]`;
  fatigue: `[(1,1000),(2,1000),(4,1000),(8,1000),(16,750)]`).
  The personal ledger provably carries zero cross-item information.
- **E3 (rise-selectivity):** V2=0 on both; conf never exceeds the stated
  rule (0 exceedances).
- The learn battery's B13=3 (items correct but conf 0 at d4/d8/d16) is
  consequence A (wrong-first pinning: solo traj shows conf 0 from d2
  despite correct at d4+), not a channel — the mechanism does exactly
  what it says. **No break. Honest residual.**

### RT-F — item-identity stress: CONFIRMED BREAK (mechanism, known, not new)

72-char always-wrong ids emit the tp=0 schema seed on ALL five cells
(v26/v27: 1000,1000,1000,1000,1000 → |err|=1.0/cell; v28: 996×5);
short-id controls correct (1000,0,0,0,0). Root cause: `nec_cmp_id`'s
63-byte cap (`src/nec_v3c.zag` line 63, forked from nec_v2d) — every
observation of a >63-byte id is treated as a first observation.
**Same classification as the m20 baseline: mechanism/implementation break
(lookup correctness), FIX1 recommended but still unadopted (open per
Micah's 2026-09-25 rulings). NOT a new break vs baseline.** The bars do
not catch it (B13=0), same as baseline.

## 7. Channel audit (post-run, on committed source `src/nec_v3c.zag`)

- Schema consulted at exactly ONE program point: the new-item (tp=0) branch,
  lines 311–317 (`if(know==1){ka_schema} else if(know==2){kb_schema} else if(know==3){kc_lookup}`).
  The tp≥1 branch (lines 253–305) contains no schema call.
- `nopool=1` for 26/27/28 (lines 129–131); class-ledger reads AND writes are
  both guarded by `nopool==0` (lines 248, 371–374) → no pooled GT read or
  written anywhere. Kill criterion (v) clean.
- Schema values byte-derived from diet + learner decisions: Phase-1
  independent recomputation matched all 312/246/7 cells + L4 with zero
  mismatches; the sim in §1 re-parses the frozen tables independently and
  is byte-exact on 9/9 — a second independent confirmation.
- `kc_lookup` is a pure match function over frozen constants; the driver
  has no schema/diet write path; no test outcome enters the schema
  (frozen pre-run, never updated within a battery).

## 8. Trace spot-checks (§6 requirement)

- H5B-O item: `L0 H5B-O-06-00 300 142 1 1 2 1000000` — L1 lookup, rate 1000000 ✓
- H5B-P item: `L0 H5B-P-06-00 300 125 1 1 2 0` — L1 lookup, rate 0 ✓
- T3 trap item (v26): `L0 T3C0-000 75 875 1 3 1000 802000` — L3 backoff, rate 802000 ✓
- Full-trace scan: v26/v27 — **0/3467 L1 rows with new_cl_mil > prev_cl_mil**
  (no tp≥1 rise anywhere, O-family included); v28 L1 rows carry `-` for
  prev (no latch) and rise vs the expired seed exactly as diagnosed.
- v28 H5B-O: L0 oracle `0 10 673469`; L1 `2 - 1000000 1000000` — seed expires,
  conf tracks p_raw.

## 9. Adoption/kill evaluation (prereg §7)

**Design S (26) — all 7 adoption criteria hold:**
1. B13 = 0/0/0, nonincreasing ✓
2. B3 = 0/0/0 — no regression from m20 (0 ≤ 2; the carried 2/2/2 prediction missed favorably, kill is B3>2) ✓
3. B1=0, B2=0/0, B4=1.0 ≥ 0.50, B4b=1.0 ≥ 0.50, B5=1.0 ≥ 0.20, B6=1.0, B7=0.1475 ≤ 0.30, B9=1.0 ✓
4. No tp≥1 confidence rise on always-correct items (0/3467 trace rises) ✓
5. T1/T2/T4 CALIBRATING (no bar-ward trip); T3 0.3812 < 0.470, bias +0.3020 ≥ −0.05 ✓
6. Red-team: no NEW breaks vs m20/FIX1 baseline (RT-A better-or-equal,
   RT-B same honest residual, RT-C zero rises, RT-D nonincreasing,
   RT-E no channel, RT-F same known implementation break) ✓
7. Determinism: 186/186 A/B/C byte-identical, SHA-logged ✓

**Design S8 (27) — KILLED:** criterion (i), B13 = 11/12/12 > 0.
Mechanism reason (pre-registered, confirmed): min_n=8 forces backoff from
pure exact cells into mixed coarser cells — (O,d) backs off to mixed (f1,f5)
cells (G −0.198) and (admit,d) likewise (G −0.166) — reintroducing the
cross-family dilution the exact classes solved. Confirms the §2 corollary.

**Design D (28) — KILLED:** B3 gviol = 6 > 2 (criterion (ii)).
Mechanism reason (pre-registered, confirmed): with the coarse K-A seeds and
no latch, conf tracks p_raw after tp=0, producing strict G rises d1→d2 on
six families. Confirms the §2 lemma's B3 half: removing the latch breaks B3.

**Kill criteria scan:** (i) B13>0 — S8 only; (ii) B3>2 — D only; (iii) no other
bar failures on S; (iv) no T1/T2/T4 bar-ward trip, T3 bias ≥ −0.05 on S;
(v) channel audit clean; (vi) no A/B/C non-identical anywhere.

## 10. Artifacts

- `run_matrix_v3c.sh`, `run_legs_bars.sh`, `run_rt_bars.sh`
- `analysis/sim_v3c.py`, `analysis/t13_v3c.py`, `analysis/t2_v3c.py`,
  `analysis/rte_v3c.py`, `analysis/to_analyzer.py`, `analysis/bars_full.py`,
  `analysis/sim_v2d_v3b.py` (pool counterfactual)
- `work/sha_runs_v3c.txt` (186 SHA lines), `work/bars_all.txt`,
  `work/rt_bars_all.txt`, `work/t13_v3c.txt`, `work/t2_v3c.txt`,
  `work/rte_v3c.txt`, legs dirs, traces
- **Binary SHA `7f6e0ceab59ad8a6…`** (rebuilt, smoke-verified byte-identical
  to Phase-1). Sources unchanged from Phase-1 commit.
