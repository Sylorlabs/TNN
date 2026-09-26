# RED TEAM vs ARM C-P3 — strength trial round 4

**Status:** BLIND red team. Task: test C-P3's claimed fate, not confirm it.
**Date:** 2026-09-25. **Trial binary:** `~/workspace/strength-round4/trial_bin_r4`
(frozen 2026-09-20 reference: `~/workspace/tnn-lab/wave8/strength-retrial/trial/trial_bin_s100`).
**No commits made** — report only, per instructions.

## Verdict

| Claimed property | Red-team finding |
|---|---|
| (1) C-P3 KILLED at S1 identically to C | **CONFIRMED.** Drops identical in all 9 S1 cells (VUP 470, WBS 434, JI 469 — all far above the P2 ceiling of 64). Also holds at S10 (4682/3212/4681, identical). |
| (2) P3 expiry has ZERO measurable effect (C-P3's numbers match C's) | **FALSIFIED as stated.** The kill verdict and all ST_METRIC lines match, but the ledgers do not: ST_ABANDONS differs in VUP (−28 at S1, −343 at S10), ST_AUDIT_N differs in every cell, and C-P3 carries 243 PEXPIRED markers + 316 maintenance re-citations at S1 that C lacks. **However:** the abandon delta is *not* caused by expiry (see attribution), and expiry changed **zero** kill/abandon/drop/metric outcomes. |
| P3 expiry mechanism is sound (PEXPIRED fires only when genuinely expired) | **CONFIRMED.** All 243 live PEXPIRED events independently audited: 0 violations (arm=3, SYSTEM role, audit-only before==after, live, strength>0, age>K and since-cite>K with strict inequalities). Zero refused PEXPIRED attempts. Boundary semantics verified live (minimum margin = 1 episode past K; nothing fired at exactly K). |

**Bottom line:** the kill verdict stands and no attack saved C-P3 or killed it differently.
But "zero measurable effect" overstates the case — the honest statement is:
*P3 expiry is verdict-neutral: it fires genuinely 243 times and re-cites 316 times
at S1, yet changes no kill, abandon, drop, or metric outcome. The one summary-number
difference (VUP abandons) comes from C-P3's Rule-2 victim-selection change, not from expiry.*

A further design-level finding: **the P3 baseline kill discount (the actual teeth of
expiry — kill at ≥1 cite instead of full price) never fired once in the S1 trial.**
Every successful kill paid the full effort price, exactly like C. The trial's learner
never attempts a discounted kill (victim path always has 0 cites; contradiction path
waits for the full `st_n(strength)` cites before trying). The mechanism is proven
real by the GATE unit test (`gate_p3_baseline_kill_ok`), but it is unreachable through
trial behavior. Relatedly, C-P3's dominant P3 behavior is expiry-*prevention*:
the maintenance rule re-cites slots whose protection lapses within 25 episodes,
so most of the arm's P3 energy fights expiry rather than exercising it.

## Attack log

### A1 — Full S1 matrix, summary comparison (C vs C-P3)
Ran all 27 cells (`B|C|C-P3 × VUP|WBS|JI × 0|1|2 × S1`). All exit 0, ST_INVALID=0.
Drops: C vs C-P3 identical per cell (470/434/469). ST_METRIC lines identical per cell.
**Differences found:** ST_ABANDONS VUP 3824→3796 (all 3 variants); ST_AUDIT_N
+41 (VUP), +48 (WBS), +69/+70 (JI). ST_FINGERPRINT differs (expected — it folds
in audit_n and the audit stream, both of which differ).
→ Claim (2) does not hold at the ledger/summary level. Proceeded to forensics.

### A2 — Ledger dump tool + line-by-line diff
Built `rd_dump.zag` (replicates `lr_run_cell` exactly, dumps all 21 audit words per
entry). Fidelity verified: audit_n and ST_FINGERPRINT match `trial_bin_r4` exactly
on 4 sampled cells (C VUP 0, C WBS 2, C-P3 JI 1, B VUP 0). Reruns byte-identical
(zero RNG confirmed empirically). Dumped all 27 S1 ledgers (27 files, ~9.8 MB total
with logs, in `redteam_CP3/`).
Op-histogram diff per cell (rc=0):
- VUP: C `STRENGTHEN=18, ABANDON=3824` → C-P3 `STRENGTHEN=57, ABANDON=3796, PEXPIRED=30`
- WBS: C `STRENGTHEN=57` → C-P3 `STRENGTHEN=84, PEXPIRED=21`; kills/evidence/justifies/abandons identical
- JI: C `STRENGTHEN=18` → C-P3 `STRENGTHEN=57, PEXPIRED=30`; kills/abandons identical

### A3 — Attribution of the −28 abandon delta (VUP)
Per-slot forensics: the delta sits on slots 12/15/18/21/24/27/30 (−4 each).
Per-episode anchoring (ADD aux): section-3 victim selection is provably identical
between arms (maintenance changes nothing `lr_pick_victim` reads). Arithmetic closes
exactly: C-P3's VUP-pressure path issues 1 (strongest-half attempt) + 8 (kill loop)
= 9 abandons per pressure event vs C's 8 + 8 = 16. Four pressure events (t=100..400)
× 7 = **28**. At S10: 49 pressure events × 7 = **343**, matching the observed
38240→37897 delta exactly.
→ The abandon difference is **100% attributable to the Rule-2 victim-selection
change** (`lr_pick_strongest_half` first demand in VUP pressure), **not to P3 expiry**.

### A4 — Independent audit of every PEXPIRED entry (mechanism soundness)
Re-derived expiry state from the raw event stream (own ADD/EVIDENCE/STRENGTHEN/
KILL tracker, strict `ep-adm>K && ep-lc>K`), checked all 243 live PEXPIRED events
(90 VUP + 63 WBS + 90 JI) for: arm==3, role==SYSTEM, before==after (audit-only),
live before, strength>0 before, genuine expiry. **0 problems.** C and B ledgers
contain zero PEXPIRED (as required). Zero refused (rc≠0) PEXPIRED attempts —
the learner issues only when `st_p3_expired==1` and the core agrees every time.
Boundary: minimum observed margin is exactly 1 episode past K (since-cite=K+1);
no event fired at exactly K. GATE self-test (`C-P3 GATE 0 S1`) passes all 5 P3
checks including `gate_p3_not_expired` (ep=60, since-cite=50=K → not expired)
and `gate_p3_expired` (ep=61 → expired).

### A5 — Did the baseline discount ever decide a kill?
Reconstructed live PEXPIRED markers at each successful KILL_EVIDENCED/OVERWRITE
in all 9 C-P3 S1 cells: **0 of 37 kills** (36 WBS + 1 JI per variant-set; 0 in VUP)
carried a live expired marker. All paid full price. Kill identity also unchanged:
the 36 WBS kills and 1 JI kill hit the identical slots with identical aux values
in C and C-P3.

### A6 — Boundary engineering attempt
Tried to construct a save-C-P3 scenario via the trial's own curriculum: the only
paths that kill are (i) victim kills (0 cites → abandon regardless of discount)
and (ii) contradiction kills (learner waits for full cites before attempting).
There is **no learner path that attempts a kill with partial (≥1 but <full) cites**,
so the discount cannot fire within frozen trial semantics. No boundary scenario
within the trial saves C-P3 or kills it differently. (A learner that *did* exploit
the discount would be a trial-semantics change — out of scope, flagged as a
design observation instead.)

### A7 — S10 matrix (C vs C-P3, trial-binary summaries)
All 18 cells: drops identical (4682/3212/4681), ST_INVALID=0. Abandons: VUP
38240→37897 (Δ−343 = 49×7, Rule-2 attribution holds at 10× scale); WBS/JI identical.
Kill verdict unchanged at S10; the S1 pattern scales cleanly.

### A8 — Build-consistency cross-checks
- `trial_bin_baseline` C-P3 VUP 0 S1: drops 470, abandons 3796, invalid 0 — identical to `trial_bin_r4`.
- Frozen 2026-09-20 `trial_bin_s100` C VUP 0 S1: drops 470, abandons 3824 — identical to r4's C run (C-P3 did not exist in the frozen binary; no direct comparison possible).

## Findings table

| # | Finding | Severity | Status |
|---|---|---|---|
| F1 | C-P3 KILLED at S1 identically to C (drops 470/434/469 vs ceiling 64, all 9 cells; also S10) | — | Claim (1) CONFIRMED |
| F2 | "Zero measurable effect" is false: ST_ABANDONS −28 (VUP S1), ST_AUDIT_N +41..+70, +243 PEXPIRED, +316 maintenance STRENGTHENs at S1 | Medium (wording) | Claim (2) FALSIFIED as stated |
| F3 | The abandon delta is caused by Rule-2 victim selection (pressure path), not expiry — proven by exact arithmetic at S1 (4×7) and S10 (49×7) | Low | Attribution established |
| F4 | PEXPIRED issuance is sound: 243/243 events independently verified genuine; 0 refused attempts; strict->K boundary holds live | — | Mechanism VERIFIED |
| F5 | The P3 baseline kill discount never fired in the trial — every kill paid full price; the learner has no path that attempts a discounted kill | Medium (design) | Unreachable mechanism |
| F6 | C-P3's dominant P3 behavior is expiry-prevention (maintenance re-citation), not expiry | Low (design) | Observation |
| F7 | Kill identity unchanged: same victims, same aux, same counts in WBS/JI; zero kills differed | — | Verified |

## Recommendations for the coordinator

1. **Reword claim (2)** from "zero measurable effect" to "verdict-neutral": P3 expiry
   fires genuinely and adds ledger activity, but changes no kill/abandon/drop/metric
   outcome at S1 or S10. The current wording is falsifiable from the committed
   ST_ABANDONS/ST_AUDIT_N numbers.
2. **Disentangle Rule 2 from P3 in reporting.** The VUP abandon delta belongs to the
   victim-selection change, not to expiry. If a future round wants a pure expiry
   test, the pressure path should be arm-neutral.
3. **Decide whether the baseline discount should be reachable.** As built, expiry's
   only "benefit" (cheaper kills) is dead code in trial behavior — the learner always
   pays full price or abandons. If that is intentional (expiry as pure audit/marker),
   say so; if the discount is meant to matter, the learner needs a partial-cite
   kill path (a trial-semantics change requiring prereg amendment).
4. No integrity concern found: ST_INVALID=0 across all 45 runs (27 S1 + 18 S10),
   checker gates (`ck_no_bad_pexp`, `ck_no_permanent_lock`) agree with the
   independent audit, reruns byte-identical.

## Methods & files (all under `~/workspace/strength-round4/redteam_CP3/`)

- `REDTEAM_CP3.md` — this report.
- `rd_dump.zag` / `rd_dump_build.zag` — ledger-dump driver source (pure Zag, replicates
  `lr_run_cell`, dumps 21 audit words/entry + fingerprint). Rebuild:
  `cd ~/workspace/strength-round4 && znc_linux_x86_64_abed8aa1 redteam_CP3/rd_dump_build.zag -o redteam_CP3/rd_dump_bin`
  (driver must sit beside the strength_*.zag sources at build time — `@import` resolves
  relative to the driver's directory in this toolchain invocation).
- `rd_dump_bin` — built dump binary (235,784 bytes; **do not commit binaries** — rebuildable via the above).
- `dump_<ARM>_<CUR>_<V>_S1.txt` — 27 full S1 ledger dumps with fingerprints.
- `logs/r4_<ARM>_<CUR>_<V>_S1.log` — 27 trial-binary runs; `logs/r4_{C,C-P3}_<CUR>_<V>_S10.log` — 18 S10 runs.
- `analyze.py` — op histograms + independent PEXPIRED audit; `forensic.py` — per-slot
  divergence; `forensic2.py` — per-episode abandon anchoring; `forensic3.py` — baseline-discount kill check.
- Pure Zag, zero RNG in all tooling; no trial semantics modified (dump driver is
  read-only instrumentation — it replicates the cell and prints the ledger).
