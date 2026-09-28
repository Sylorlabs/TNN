# PREREG_FS-E1b.md — "CH-CCN-3 threshold repair" (deliberate repair of a diagnosed defect)

## Fork ID
FS-E1b (free at check time; `forks/FS-E1b/` reserved 2026-09-24).

## Date / provenance
- 2026-09-24. Parent: FS-E1 (`forks/FS-E1/`, VERDICT **PARTIALLY SUPPORTED**,
  committed per registry prereg 9a8a68e4, evidence 64cf8833, kept fixtures
  ddb71795).
- FS-E1's defect diagnosis (VERDICT.md, post-freeze CP seed 20260924):
  CH-CCN-3 uses a raw count≥4 threshold over pixels with per-pixel RGB-L1 >
  16 between the two d65 G views. The 3 kept colorconst families are 2×2
  patches where d65 illuminant rendering + sensor noise attenuates 1 pixel
  below the L1>16 cut, leaving 3 marked pixels; truth=DIFFERENT (patch ≥2×2,
  L1≥32 pre-illuminant per the frozen strong-truth criterion), challenge
  reports SAME.
- Micah's standing rule: deliberate repair of a diagnosed defect beats
  wholesale rip-out — fix the wiring. FS-E1b changes exactly one quantity
  (CH-CCN-3 → CH-CCN-3r); every other mechanism reuses FS-E1's frozen
  registry (commit 9a8a68e4) verbatim.

## Defect reproduction (diagnostic, pre-prereg; FS-E1b crew's own measurements)
On FS-E1's 3 kept fixtures (`forks/FS-E1/fixtures_cp/cp_colorconst_{0,1,2}.r2fx`,
truth=DIFFERENT on all three), per-pixel RGB-L1 between the two d65 G views:
- fixture 0: marked count = 3; 2×2 patch footprint at (34,12), window L1s
  [[53,64],[15,33]] — one pixel attenuated to 15 (< 16).
- fixture 1: marked count = 3; 2×2 patch footprint at (44,6), window L1s
  [[42,48],[27,9]] — one pixel attenuated to 9.
- fixture 2: marked count = 3; 2×2 patch footprint at (13,20), window L1s
  [[54,100],[11,127]] — one pixel attenuated to 11.
The FS-E1 binary (`build/fse1`, mode `full`) reports
judgment=SAME_SURFACE / disposition=INSTALL on fixture 0 (wrong vs truth).
Mechanism confirmed exactly as diagnosed: minimal (2×2) coherent patch, one
pixel lost below the per-pixel cut under d65 rendering + noise, raw
count≥4 threshold reports SAME.

## Hypothesis
A challenge quantity that counts *coherent minimal edits* rather than raw
above-cut pixels closes the diagnosed gap without recall cost and without
new false-DIFFERENT risk: the truth criterion's minimal unit is a 2×2
coherent patch, and bounded sensor noise provably marks zero pixels on SAME
pairs, so a coherence-guarded count is FI-neutral-or-better by construction.

## Mechanism (frozen)

Pure Zag (`forks/FS-E1b/src/fse1b.zag`, forked from FS-E1 `fse1.zag`;
`diff` proves ONLY the items below change: `cc_chal` body, its comments,
the t1 challenge-name string, and the straw-alternative-audit line. All
formations, all other challenges, support rules, ledger, hash-chain, CLI
modes are byte-identical logic). Python is glue/analysis only (drivers,
scorers, fixture generators, CP search). **Zero RNG in any decision path.**
Deterministic given fixture bytes.

### The repaired rule — CH-CCN-3r (EXACT, frozen)
Over the two neutral-illuminant (d65) 48×48 G views (6912 bytes each):
1. Compute per-pixel RGB-L1; mark a pixel iff L1 > 16 (cut UNCHANGED).
2. Scan all 47×47 2×2 windows; let `best` = max marked pixels in any window,
   `cnt` = total marked pixels.
3. Outcome DIFFERENT iff `best >= 3`, else SAME.
4. Ledger challenge stats: stat1 = `cnt` (raw marked-pixel count, the old
   truth-quantity, kept for comparability), stat2 = `best` (coherent
   minimal-edit quantity).

### Why this rule (principled, not tuned to the 3 kept items)
- The frozen strong-truth criterion: DIFFERENT unambiguous iff a local edit
  covers ≥2×2 px, each with per-pixel L1 ≥ 32 pre-illuminant. The minimal
  truth-DIFFERENT unit is therefore a 2×2 patch = 4 pixels.
- The per-pixel cut L1>16 exists to reject bounded sensor noise: ±2/channel
  → max per-pixel L1 = 12 < 16. On truth-SAME pairs (two independent noisy
  d65 renders of one crop) the marked count is provably 0, so NO 2×2 window
  can reach 3: the false-DIFFERENT risk is exactly what it was under
  count≥4 (zero in the threat model). The guard is load-bearing against
  future generators, not against today's battery.
- A 2×2 window with ≥3 marked pixels witnesses a 2×2-scale coherent surface
  change while tolerating ONE rendering-attenuated pixel — exactly the
  diagnosed failure mode (attenuated pixels measured at 15/9/11).
- The rule is derived from (truth minimal unit = 2×2) + (noise bound). It is
  not fitted to the kept items' pixel values: any coherent 2×2-scale edit
  qualifies; scattered above-cut pixels (impossible under the noise bound)
  do not.
- FI-neutrality argument (battery): on truth-SAME items the challenge still
  reports SAME always (cnt = 0 → best = 0), so no new challenge-agreement
  can create a false install; on truth-DIFFERENT items the challenge can
  only flip SAME→DIFFERENT, which is correct-direction. Recall can only rise.

### Everything else: FS-E1 verbatim (frozen registry 9a8a68e4)
- Formations t0–t5: FS-E1 verbatim (frozen; formation is FS-E2's front).
- CH-COL-1, CH-SHP-2, CH-PTC-1, CH-TBD-2, CH-MOT-2: FS-E1 verbatim.
- Support rule: INSTALL iff challenge outcome == formation claim (pure
  agreement), UNRESOLVED → WITHHOLD, malformed → WITHHOLD.

## Batteries (frozen)
- `b_adv`: 10,000 R2A adversarial fixtures =
  `forks/R2-16/evidence/b_adv.list` (the FS-E1 battery, unchanged).
- `b_ctrl`: 2,000 R2A control fixtures =
  `forks/R2-16/evidence/b_ctrl.list` (unchanged).
- Truth from `<fixture>.truth` sidecars. Family ids from the R2FX header.

## CP-suite design (challenge-prediction red team, colorconst only)

Only colorconst is redesigned; the adversary knows the repaired rule and the
real `fse1b` binary. Candidate generators, keep rule, strong-truth criterion,
and fixture format are FS-E1's (`gen_cp_fse1.py` threat models (a)–(d) for
colorconst) verbatim; only the binary under test and the master seed change.

- **Design-loop CP** (pre-freeze): colorconst, budget 5000 candidates, at
  TWO master seeds: 20260923 (untuned w.r.t. this repair) and 20260924 (the
  defect-finding seed — regression: the repaired binary must return zero
  kept here). Plus a direct regression check: the 3 known kept fixtures
  must now yield judgment=DIFFERENT.
- **Pre-freeze gate:** the registry freezes ONLY when the design-loop CP
  returns zero kept families at BOTH seeds. Documented iterations on the
  CH-CCN-3r coherence parameters are permitted pre-freeze (the rule FORM —
  coherent minimal-edit count — is frozen by this prereg); each iteration is
  logged in `forks/FS-E1b/hidden/DESIGN_LOOP_FSE1b.md`.
- **Post-freeze CP** (bar (c)): FRESH master seed 20260925, budget 5000,
  colorconst only → must return zero kept (hard bar).
- motiondir and the four frozen tasks are NOT re-run in CP: their mechanisms
  are byte-identical to FS-E1 (diff-proven), so FS-E1's CP evidence stands;
  the formal battery re-measures all six tasks.

## JOINT KILL BARS (all must pass; any fail = DEAD)
(a) **Overall FI:** false installs 95% Wilson UCB ≤ 1% on b_adv (n=10,000).
(b) **Recall is formation-conditioned:** FS-E1 proved absolute ≥85% recall
    unachievable — its formation ceiling measured 80.30% on controls, and
    the challenge layer's overstrictness was 1.55% (VERDICT.md: "capped by
    formation accuracy, not by challenge overstrictness"). Bar: recall ≥
    (measured formation accuracy − 3pp) on b_ctrl — the repair must not cost
    recall. (Both quantities measured in the FS-E1b runs, same scorer.)
(c) **Fresh post-freeze CP:** zero kept (seed 20260925, budget 5000,
    colorconst). Any kept family kills.
(d) **Per-family:** 95% Wilson UCB ≤ 2% REPORTED for every task/family in
    b_adv; families with n < 200 are pooled-only by mathematical necessity
    (a ≤2% UCB is unachievable at small n) — reported, not hidden; no
    bar-gaming. Any n≥200 family exceeding 2% UCB kills.
(e) **Determinism:** b_adv + b_ctrl each run TWICE; ledgers and stdout
    byte-identical across runs; every hash-chain line verified. Fail kills.

Also reported (no kill): formation accuracy, overstrictness, recall
decomposition, per-task FI table — same scorer as FS-E1.

FINAL verdict ALIVE iff (a)–(e) all pass, else DEAD.

## Out of scope / not claimed
- No formation changes (FS-E2's front). No timbredisc/audio changes (frozen
  per STEP 0). No motiondir changes. This prereg does not re-derive
  round-1/round-2 results. The 3 kept fixtures' pixel values are diagnostic
  evidence, not training data; the rule is derived from the truth criterion
  + noise bound.

## Commit plan
1. This prereg committed ALONE (no sources, no results).
2. Sources (`src/fse1b.zag`, CP driver, battery driver) + design-loop CP
   evidence committed after the design loop (before the freeze decision is
   recorded).
3. Freeze record, formal battery evidence, fresh post-freeze CP evidence,
   `VERDICT_FS-E1b.md` committed last.
4. Frozen binary NEVER committed (rebuilt deterministically from source).
   No `.zagd` cache files, no binaries committed.
