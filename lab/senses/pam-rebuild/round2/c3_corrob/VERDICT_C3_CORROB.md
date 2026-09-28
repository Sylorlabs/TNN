# VERDICT C3 — Corroborated-revision gate rules (PAMs Round 3, Crew 3)

**Prereg:** `PREREG_C3_CORROB.md` (commit
`e78d126ef1ca554d7f3aa4c643aa2cb2fac9df60`, committed alone before any build).
**Verdict: PASS** — all four kill bars met.

## Instruments (pure Zag, zero RNG, pinned toolchain)

- `src/c3.zag` — frozen O1 Delivery Adjudicator + revised gate (R1/R3/R4).
  Built with `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- `cro_offense.zag` — frozen CRO-1 offense battery (unchanged defense D3;
  recompiled from the frozen source for the re-run).
- Input: `evidence/c3_cases.txt` (11,840 rows, sha256
  `ed1ad01fb65a37125b06163bd1243bd930435e655b7a446c5f16fa91333e3357`),
  derived from the frozen `sweep.jsonl`
  (`4163fffa65f18f552d48f7efec0e9800a7406547a27c6259d39a48ec7f0833f2`).
- Offense inputs: frozen `sweep.jsonl` + `exemplars.tsv`
  (`13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e`).

## Results

| Metric | Frozen | O1 repair | C3 repair (mode 1) | Bar |
|---|---|---|---|---|
| RK-3 (genuine installs) | 104/1,102 (9.44%) | 106/1,102 (9.62%) | **791/1,102 (71.78%)** | KB-C3a ≥50% ✅ |
| RK-1 (false permanents) | 0 | 0 | **0** | KB-C3b =0 ✅ |
| RK-2 (wrong HC permanents) | 0/1,109 | 0/1,109 | **0/1,109** | KB-C3b =0 ✅ |
| K2 (delivery) | 824/1,102 | 954/1,102 | 954/1,102 (unchanged) | — |
| revised_installs | — | — | 92 | — |
| challenger_provs | — | — | 194 | — |
| repaired (adjudicator) | — | 130 | 130 | — |

**Offense kill bar (KB-C3c), frozen D3 re-run, 3× byte-identical:**

| Metric | CRO-1 frozen | C3 re-run | Bar |
|---|---|---|---|
| AC-1 attack success | 834/4,619 (18.06%) | **834/4,619 (18.06%)** | ≤18.06% ✅, ≤86.6% ✅ |
| AC-2 attack success | 0/4,619 | 0/4,619 | — |
| AC-3 attack success | 806/4,619 (17.45%) | 806/4,619 (17.45%) | — |
| Control (truth installs) | 5,299/7,221 (73.38%) | 5,299/7,221 (73.38%) | viable ✅ |

**Determinism (KB-C3d):** 3 runs byte-identical per instrument.
- `metrics_fidelity_{1,2,3}.txt`: sha256
  `26153947a6e05cdc01e26c2c7516fd8dd0572663780cc86c6ab3b5b0d11d396d`
- `metrics_repair_{1,2,3}.txt`: sha256
  `183cfd95beb731ef42349aa7d415e59ea661deae9795e9e0d86a62ea459fe42f`
- `offense_{1,2,3}.out`: sha256
  `1b913b64c1100334c94250ee4c61993ea36d40cbc5e74bfe5b6321cdf439fe8e`
  (byte-identical to the frozen CRO-1 evidence — the defense is unchanged).

## Rule changes (what was built)

1. **R1 — Corroborated revision** (conflict rule). New per-task challenger slot.
   A conflicting PASS with `conf>=700`, `mrgF>=thr_of(task)`, `pred==1`, no
   armed-negative match: first occurrence → `CHALLENGER_PROV` (install);
   a second same-jcode PASS within `tol_of(task)` → `REVISED_INSTALL`
   (permanent := challenger, incumbent retired with `revised_old` audit).
   This is historical corroboration, never pointwise evidence comparison.
   Weak challengers (`conf<700` or `mrgF<thr_of`) → frozen
   `CONFLICT_WITHHELD` (durable memory kept).
2. **R3 — Challenger margin bar** (strong-margin recalibration). The
   `mrgF >= thr_of(tc)` bar layers the frozen pipeline's task-natural T3
   margin bar on top of the (g)-check `strong` flag. The frozen `strong` flag
   is NOT loosened; `agree==0` trials are NOT admitted (O1 safety boundary).
   Empirically vacuous on this evidence (no challenger below its task bar) —
   retained as a conservative eligibility requirement.
3. **R4 — Corroborated negative evidence** (suppression rule). A negative entry
   arms only after TWO FAILs (same jcode, within tol): first FAIL → pending
   slot, second matching FAIL → armed. Suppression checks the ARMED table only.
   Singleton FAILs no longer poison the table. Recovered part of the 60
   poisoned suppressions.
4. **R2 DROPPED** (autopsy §4 item 2, conf bar on permanence). Pre-prereg
   replay proves it starves the R1 mechanism (challenger provisionals 196→1,
   revisions 79→0); R1 alone reproduces the autopsy cf1 prediction exactly
   (725/1,102 = 65.79% without adjudicator).

## Why it works (diagnosis confirmation)

O1's redirect is confirmed: the blockage was the conflict/negative-evidence
gate rules, not delivery. The O1 adjudicator (frozen, on) admits 130 records
(128 correct/0 wrong); the revised gate then lets 92 corroborated revisions
install and 194 challengers go provisional, lifting RK-3 from 9.62% (O1) to
71.78% with zero false permanents. The 125 never-admitted (`agree==0`) remain
out of scope (sense calibration, prereg (f)).

## Kill-bar assessment

- **KB-C3a** ✅ 791/1,102 = 71.78% ≥ 50% (5.3× the 9.44% frozen baseline).
- **KB-C3b** ✅ RK-1 = 0, RK-2 = 0/1,109.
- **KB-C3c** ✅ AC-1 = 18.06% (baseline does not rise), ≤ 86.6% ceiling holds.
- **KB-C3d** ✅ 3× byte-identical per instrument (HARD).

**Verdict: PASS.** The corroborated-revision gate repair is effective and safe.
