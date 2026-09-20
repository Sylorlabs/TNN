# PREREG AMENDMENT (DRAFT) — RC2: Reasoning Control at 10× Scale

**Status:** DRAFT — written 2026-09-20. **Do not run until Micah approves.**
This draft freezes the 10× scale leg; the runner amends nothing after approval
without a new dated amendment.

## 1. Authorization finding (why this draft exists)

RC1's prereg (`wave7/reasoning-control/PREREG.md`, 2026-09-20) contains **no
scale legs**. Its only scale provision is an honest-boundary complexity note:

> "Scale: 12-episode phases. Scaling argument: params O(1); inspect O(ledger
> window); sim O(episodes in window)."

That is an argument, not an authorization. All 40 `CL_CHECK` bars are exact
counts for the 12-episode curriculum; the defect bits (`rc_world_defect`),
the probe predictions (0→12), the `ep_def` buffer (12 entries), and
`RC_SMAX=150` are hardcoded for it.

`TRIAL_RESULTS.md`'s "Next step" *proposes* "RC2: a second in-scope parameter
class … then 10× scale leg with a capped ledger window" — a proposal, not an
authorization, and it defines RC2 differently (new parameter class first).

**Therefore 10× materially amends the test definition** (new curriculum,
changed bars, changed constants) and per program law requires Micah's
re-approval before any run. This draft is the amendment.

## 2. What RC2 is (proposed)

The **identical RC1 machinery at 10× episodes** — same params (V, R), same
ops (`REASON_INSPECT/PROPOSE/COMMIT/REFUSE/ROLLBACK`, `STAGE_ADVANCE`), same
gate order and refusal codes (201–204), same constitution, same
integrity-ledger checker imported verbatim. No new parameter class in RC2.

- Phase A: 120 episodes (V=1, loose bar)
- Revelation: disclose all 120 defect bits
- Reasoning change 1: V 1→2 (constructive), sim replays 120 recorded episodes
- Reasoning change 2: R 5→8 (neutral)
- Phase B: 120 episodes (V=2, R=8)
- Stage advance, refusal probes 1 & 2, lying-prediction probe, final rollback
- Verification mini-phase: 40 episodes (was 4)

## 3. Frozen changes vs RC1

### 3a. Curriculum — designed defect bits (phase-disjoint item ids)

Densities preserved from RC1 (A: 4/12 = 1/3; B: 4/12 = 1/3; mini: 1/4):

| phase | items | defective set | count |
|---|---|---|---|
| A | 0–119 | i mod 3 == 2 | 40 |
| B | 1000–1119 | (i−1000) mod 3 == 2 | 40 |
| mini | 2000–2039 | (i−2000) mod 4 == 1 | 10 |

### 3b. Constants

- `RC_SMAX`: 150 → **1500**. Required: S_b = 50 + 40×8 = 370 must be
  observable; at 150 the cap would clamp S and mask the R effect entirely.
- `ep_def` buffer: 12 → **120** entries.
- `RC_AUDIT_CAP`: retained at 2048. Pre-run entry estimate ≈ 1,420
  (A: 480, revelation: 120, B: 600, mini: 200, fixed overhead ≈ 20).
  Runner verifies the estimate before compiling; if it exceeds 1,800 the
  cap is bumped to 4096 and the bump is recorded in the results (no bar
  changes — capacity only).

### 3c. Expected checks (all 40 recomputed; falsification criteria F1–F6 unchanged)

| check | RC1 | RC2 |
|---|---|---|
| commits_a / noshape_a / checks_a | 12 / 12 / 12 | **120 / 120 / 120** |
| pred_refusals / pred_ok / pred_noshape | 4 / 8 / 0 | **40 / 80 / 0** |
| ok_b / noshape_b / refusals_b / S_b / checks_b | 8 / 0 / 4 / 82 / 24 | **80 / 0 / 40 / 370 / 240** |
| stage after advance | 4 (FULL) | 4 (FULL) — rule unchanged: ≥8 consecutive `IL_OK` |
| probe1 rc / V after | 203 / 2 | 203 / 2 — honest degrading prediction **0→120** (was 0→12) |
| probe2 rc | 204 | 204 |
| lying probe: commit rc / mini noshape / V after rollback | 0 / 4 / 2 | 0 / **40** / 2 |
| R after final rollback | 5 | 5 |
| RCOMMIT(V) / RREFUSE counts | 2 / 2 | 2 / 2 |
| replay diff (V,R,S,stage) | 0 | 0 |

### 3d. Negative control (F1 liveness)

Patched copy miscounts refusals **39 instead of 40** (was 3 instead of 4);
must produce `RC_FAILURES > 0` with the mismatch on the refusal/pred checks.
Control evidence kept out of the trial dir (`/tmp/rc2_neg/`).

### 3e. Ledger window

**No cap for RC2** — faithful scale leg. The sim replays 120 recorded
episodes O(n); audit scans are O(~1,420). The capped-window mechanism
suggested in `TRIAL_RESULTS.md` changes the machinery and is **deferred**
to a follow-up with its own prereg.

## 4. What does NOT change

Gate order and refusal codes; the constitution (ledger append-only,
`il_check`, gate rules, staging ladder, external force authority); the
lying-probe defense-in-depth logic (gate passes, verification catches,
rollback repairs); F4 byte-identical reruns; F5 exact replay; F6 no-RNG
(runner grep, fail-closed); the honest boundaries (conclusion vocabulary
fixed; defect-detection a designed property; felt mechanism out of scope).

## 5. Open questions for Micah — do not run until ruled

- **Q1.** Is RC2 the 10× scale leg (this draft), or should the results
  file's "second parameter class (elimination strictness)" experiment run
  first under a different name?
- **Q2.** Approve the designed defect sets in §3a (density-preserving,
  deterministic positions).
- **Q3.** Approve `RC_SMAX` 150→1500 and the no-cap ledger window for RC2.
- **Q4.** Approve deferring the capped-window mechanism to a follow-up.

## 6. Run procedure (after approval)

Port `rc_trial.zag` → `rc2_trial.zag` changing only: defect function,
phase loop bounds (120/120/40), item id bases (0/1000/2000), `ep_def`
size, `RC_SMAX`, expected-check constants, probe-1 prediction (120).
Zero RNG. Two consecutive binary runs, sha256-compared. Independent
checker script re-verifies all 40 checks from run stdout. Commit results
under `docs/lab/wave8/rc2/`; filter binaries, `.zagd`, `.zag-cache/`.
