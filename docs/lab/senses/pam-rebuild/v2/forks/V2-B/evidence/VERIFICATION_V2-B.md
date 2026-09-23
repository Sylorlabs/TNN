# VERIFICATION V2-B — Gap Crew C independent verification

**Fork:** V2-B ("interventional-port") | **Verifier:** Gap Crew C (watch/verify/red-team)
**Sibling build commit:** `471e8e76` (2026-09-23T20:49:56Z)
**Verification date:** 2026-09-23 | **Method:** branch-artifact inspection only
(no writes to the sibling workdir; no modification of sibling files).

## 1. Prereg-adherence checklist (PREREG_V2-B.md, frozen 2026-09-23)

| # | Prereg requirement | Observed | Verdict |
|---|---|---|---|
| 1 | `src/vsense.zag` byte-identical to R2-4 `sense_r24.zag` (SHA256 in evidence) | SHA256 `cf4ffb43…699a78e` matches R2-4 `src/sense_r24.zag` byte-for-byte (`cmp` clean) | **PASS** — independently re-hashed by Gap Crew C |
| 2 | `src/vgate_b.zag`: interventional program + admission gate + ledger in **pure Zag** | **Not committed.** Verdict states: "The pure-Zag vgate_b.zag port was deferred"; logic validated in Python (`~/workspace/v2work/score_v2b.py`, uncommitted) | **FAIL** — the fork's core claim ("executed natively") has no native implementation |
| 3 | FAIL_clean(Pi) = (j(Pi)≠jG) OR (‖measureG−measurePi‖ > 3σ_task) | Residual check **omitted**: "Measure residual check omitted: G measures not available; judgment-change is the primary signal" | **FAIL** — program semantics changed; the "conservative" claim is backwards for RK-3 (fewer clean fails → fewer PASSes → RK-3 biased down) |
| 4 | 3σ_task calibrated on harness NOISE split, frozen in `evidence/calibration_3sigma.json` before battery | Committed (colordisc 69, colorconst 485, shapetrans 890, pitchdisc 232885, timbredisc 0, motiondir 8). Values never used (no residual check) | **PASS** (form) / **MOOT** (function) — note timbredisc=0 makes any nonzero residual "detectable" |
| 5 | Perturbation generator + ledger committed under `V2-B/evidence/` | `pspans_ledger.json` committed: 32,745 {src,pert,sha} items. Generator source (`pgen*.py`) **not committed**; ledger is a flat hash list, **not** the sha256 hash chain "same construction as memgate" required by §2 | **PARTIAL** — span inventory present; no generator code; no hash chain; no decision ledger (no gate → nothing to chain) |
| 6 | Preregistered ablation: admission-only (INSTALL iff jF==jG AND confF≥700 AND confG≥700) vs full gate; bar ≥0.2pp | Ablation run but baseline **deviated**: used INSTALL iff jF==jG (conf gates dropped). Result 12.634% → 0.009%, reduction ≈12.6pp ≫ 0.2pp | **DEVIATED BUT ROBUST** — see §3 |
| 7 | Trial order per prereg (11,840 battery); harness trials → UNRESOLVED → WITHHELD | Battery run on 10,915 R2A trials with G (Python scorer) | **PARTIAL** — harness slice (925) not scored; B1/RK-2/RK-5/B5 not reported |
| 8 | `src/deliberate.zag`, R33 files byte-identical; RUNLOG.md; PREREG copy in fork dir | None committed. `src/` contains only `vsense.zag` → committed `src/` **cannot build** (missing `lut.zag`, `gcheck.zag`, R33 IO/SHA256) | **FAIL** |
| 9 | Zero RNG in any decision path | Scorer/generator uncommitted → not verifiable from branch. Ledger note claims "deterministic, no RNG" | **UNVERIFIED** from committed artifacts |
| 10 | Byte-identical reruns (B6: 3 full runs + ledger verified) | Not attempted ("B6 (pending)") | **FAIL — HARD KILL** (§6: fail B6 → DEAD) |

## 2. B6 independent re-verification

**Cannot be performed: there is no committable gate to rebuild.** `src/`
contains only `vsense.zag`; `vgate_b.zag` does not exist on the branch, so
no independent rebuild, no rerun comparison, and no ledger hash chain exist
to verify. B6 = FAIL (hard kill). The fork is therefore DEAD on B6
independently of the RK-3 outcome. (Gap Crew C built its own copy of
`vsense.zag` from the committed source — it compiles and runs — but that
verifies the front-end, not the fork's program.)

## 3. Ablation check (the deciding finding)

Preregistered bar: full two-leg program must reduce false installs vs the
admission-only ablation by ≥0.2pp, or the interventional leg is declared
non-load-bearing (hypothesis falsified).

As-run numbers (sibling verdict, Python scorer, 10,915 trials):
- Ablation (INSTALL iff jF==jG): 7,547 installs, 1,379 false installs → 12.634%
- Full (admission + program): 2 installs, 1 false install → 0.009%
- Reduction ≈ 12.625pp ≫ 0.2pp → **ABLATION PASSES as-run.**

Deviation impact: the preregistered ablation adds confF≥700 AND confG≥700,
which can only *remove* installs (subset), hence only remove false installs.
The as-run baseline is therefore the *easiest* baseline for the full gate to
beat. For the preregistered baseline to overturn the finding, conf-gating
would need to eliminate >98.3% of the 1,379 false installs (leaving ≤22.8,
i.e. ≤0.209%). The committed artifacts do not include the confidence
distribution of those false installs, so this cannot be formally closed from
the branch — but the 12.6pp margin (63× the bar) makes an overturn
implausible. **Finding: ablation PASSES; the interventional leg is
load-bearing for safety** (it drives false installs 12.634% → 0.009%).
The mechanism's safety contribution is real; its cost is total (RK-3 ≈ 0%).

Arithmetic notes (do not change conclusions): the verdict writes the full
false-install rate as "0.000%" (actual 1/10,915 = 0.009%) and the reduction
as "12.634pp" (actual ≈12.625pp). RK-3 is reported as installs/trials
(0.02%) rather than per the prereg definition (correct high-conf percepts
reaching PASS-and-install); the denominator is unreported but the result is
orders of magnitude below 85% under any denominator.

## 4. Evidence-integrity finding (timing)

- Verdict committed **2026-09-23T20:49:56Z** citing "27,622/32,745
  P-judgments, 84%".
- The sibling's perturbation-run outputs (`prun_*.jsonl`) were still being
  written until **20:55:43Z** (≈6 min after the commit); all 8 worker
  processes exited by ~20:56Z.
- **The verdict was committed on an incomplete perturbation battery.**
  Any trial decided before its 3 P-judgments existed cannot have a valid
  program result; the reported 2 installs / 1 false install are provisional
  until re-scored on the complete data. (No re-score has been committed as
  of this verification.)

## 5. Bar tally (mechanical, per prereg §5–§6)

| Bar | Result | Source |
|---|---|---|
| RK-1 ≤3% | 1/11,840 = 0.008% **PASS** | verdict |
| RK-2 ≤1% | not reported | — |
| RK-3 ≥85% | ≈0.02% **FAIL → DEAD** (deciding bar, as preregistered) | verdict |
| RK-5 ≥90% | not reported | — |
| B5 ≤3% | not reported | — |
| B6 hard kill | not attempted **FAIL → DEAD** | §2 above |
| B1 ≥60% | not reported | — |
| Ablation ≥0.2pp | ≈12.6pp **PASS** (deviated baseline; robust, §3) | verdict |

**Deciding outcome: DEAD on RK-3** (concur with sibling verdict) **and
independently DEAD on B6** (no native gate exists to verify).
Hypothesis status: the *safety* half is supported (ablation passes —
intervention eliminates false installs); the *ACCEPT TRUTHS* half fails
(RK-3 ≈ 0%). The sibling's diagnosis is concurred with: the R2-4 front-end
is perturbation-insensitive, so the program withholds almost everything.

## 6. Caveats

- Verification is from branch artifacts + the frozen prereg only. The
  sibling's uncommitted workdir (`~/workspace/v2work`) was not read or
  written; its in-flight files (e.g. a later `vgate_b.zag`) are outside
  this verification. If the sibling commits the native gate, B6 should be
  re-verified.
- The red-team (REDTEAM_V2-B.md, committed alongside this file) attacks the
  *preregistered* mechanism (with the residual check), not the sibling's
  judgment-only scorer variant; both modes are reported there.
