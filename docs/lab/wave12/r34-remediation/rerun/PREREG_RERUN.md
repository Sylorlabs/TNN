# R34 remediation — clean rerun of the wave-2 long-horizon battery: preregistration

**Status:** FROZEN 2026-09-20 (pre-evidence). **Owner:** Micah. **Worker:** RERUN.
**Scope:** clean reruns of LH-1, LH-2, LH-3 (480 / 1920 / 4800-update legs) and
LH-5 (noisy-reward knee leg) from `wave2/longhorizon/PREREG.md`, on the
deterministic remediated learner core. LH-4 / LH-7 are out of scope for this
workstream (claims stay suspended); LH-6 stays blocked per its gate.

Frozen bars change only via dated amendment approved by Micah. The worker
cannot self-approve amendments.

## 1. What is under test (quarantined claims)

The tainted battery's verdicts are quarantined (LCG contamination, see
`../PREREGISTRATION.md` and the contamination notices on the LH RESULT.md
files). This rerun tests whether the same protocol, with deliberate
state-driven exploration and no randomness in the learner, restores:

- **C1 (LH-1):** delayed-credit rule stable at 10× horizon — 480 updates,
  16/16 per-block per-regime eval positives, determinism, return-A 15/16
  with zero weight updates.
- **C2 (LH-2):** stable at 40× horizon — 1920 updates, 16/16 throughout;
  saturation finding: correct cells pin at ±30000 after ≈300 net accepts
  with no post-saturation rigidity (ordering-based discrimination survives).
- **C3 (LH-3):** stable at 100× horizon under schedule drift — no block
  below 15/16 in either regime; blocked deciles 16/16; mirror context
  assignment under B-first drift is behaviorally equivalent.
- **C4 (LH-5):** noisy-reward fragility — the knee is between 0% and 10%
  corruption (10% already produces total 0/16 per-block collapses via
  spurious context switches; switches explode 19→~181 across the ramp).

## 2. Apparatus

- **Learner core:** `../r34_clean_learner.zag` — the frozen remediated core
  (22-field state, magic `R34CLN01`, deterministic explore rule, no RNG).
  UNMODIFIED by this workstream; the evidence runner asserts byte-identity
  with the frozen file before every campaign.
- **New harness:** `../r34_lh_clean_harness.zag` (this workstream; committed
  after the prereg, before evidence). Imports the clean core + the canonical
  `toolchain/R33_CONTINUING_LIFE_V1/{world,storage}.zag`. One binary,
  `argv[1]` selects the leg (`lh1|lh2|lh3|lh5|lh5rate <pct> <seed>`); every
  leg is run twice and diffed (the determinism pattern).
- **File-location note:** the harness lives next to the clean core (not under
  `rerun/`) because znc resolves `@import` relative to the main file's
  directory — from `rerun/` the core's own nested toolchain import would not
  resolve. Same layout as the remediation's `wb_clean_tests.zag`.

## 3. Dated adaptations (explicit — not silent changes)

**A1 — Explore-budget policy (2026-09-20, frozen).** The tainted runs had
effectively unbounded 1-in-5 explore flips during training. The clean core
has a finite logged budget spent 1 per explore. Frozen policy:
`LH_REFILL = 8`, granted via `r34_clean_set_budget` (SET, not accumulate) at
the start of **every training phase** (`learn=1`); eval phases never refill
and run `explore_enabled=0`. Rationale: 8 covers initial margin separation
(3 net explores take the margin past the 200 threshold) plus a
disappointment-path buffer, while leaving room in a 24-episode phase for
exploitation-driven score building — which the context-switch rule needs
(`old>0` on a non-explore negative). Unspent budget does not carry across
phases, so no phase can explore more than 8 times; total `explores` is
logged per lineage. Pre-freeze policy-selection runs (harness validation,
NOT evidence) at refill 4/8/12 all gave identical LH-1 verdicts
(`LH_FAILURES=0`, `ra=15`, `active=0`), so 8 is not a knife-edge fit; the
failure threshold is refill ≥ 24 (block-0 discovery would crowd out all
exploitation and the B-context switch could never fire).

**A2 — `explore_enabled` mapping (2026-09-20, frozen).** Identical to the
tainted protocol: `explore_enabled=1` during training phases, `0` during
eval probes. The *mechanism* behind the flag changed (state-driven
uncertainty/disappointment predicate + budget, instead of 1-in-5 LCG
flips); the protocol's exploration *opportunity* mapping did not.

**A3 — Learner seeds are obsolete (2026-09-20).** The tainted legs used
fresh learner seeds (11001/22002/33003/5555). The clean core's init takes a
budget, not a seed — there is no seed parameter to document. Determinism
now comes from logged state, asserted per leg by two byte-identical runs
(`r34_clean_equal` + world-bytes equal). World/runtime seeds are unchanged
(1101/2202/3303/51); drift seed 333 and corruption seeds
5600/5610/5625/5650 are unchanged.

**A4 — Return-A gate: at-least semantics (2026-09-20).** The tainted harness
encoded `ra==15` exactly. Frozen bar: `ra >= 15` with zero weight updates
during the return probe (and `active==0` for LH-1/LH-2; reported as a
finding for LH-3, where the mirror assignment legitimately ends at
`active=1`). Rationale: 16/16 (seen in LH-3's mirror case) is strictly
better retention than 15/16, not a failure; failing a run for exceeding the
bar would be perverse.

**A5 — LH-3 bar encoding (2026-09-20).** The tainted LH-3 ran with strict
eval off and recorded mode-2 `ea=15/16` as a probe artifact. Frozen bars:
mode-0/1 blocks require exactly 16/16 both regimes; mode-2 blocks require
≥15/16 both regimes (a mode-2 `ea==15` is logged as `LH_FINDING`, the
documented switch-cost artifact); any block below its bar is
`LH_BLOCKFAIL`. Return: `ra>=15`, no weight updates.

**A6 — Evaluator-side deterministic devices retained verbatim
(2026-09-20).** Two harness-side seeded devices are world simulation, not
learner randomness, and are kept byte-identical to the tainted protocol so
the treatments are comparable:
  - `lh_drift_next` — LH-3 regime-presentation-schedule perturbation
    (drift seed 333; the tainted schedule 1,1,2,0,0,2,1,2,2,1 must reproduce
    exactly, else the leg is void);
  - `lh5_corr_next` — LH-5 reward-corruption channel: seeded sign flips
    applied BEFORE `r34_clean_accept`, on training accepts only
    (`learn==1`); eval probes uncorrupted. Flip counts must reproduce the
    tainted channel's nominal rates (46/480, 124/480, 241/480 at
    10/25/50%).
  The static audit confines harness RNG-terms to these two functions (plus
  the words "seed" for documented world/corruption/drift seeds); the learner
  core must show zero matches, as in the remediation's bar B3.

**A7 — Trace/fingerprint fields (2026-09-20).** `LH_TRACE` keeps every
tainted field and adds `expl=` (explore count), `bud=` (remaining budget),
`nstrk=` (neg_streak). Fingerprints use `r34_clean_fp` and are NOT
comparable to tainted `r34v3_fp` values; only within-rerun determinism is
asserted.

## 4. Bars per leg (same as the original protocol, via the adaptations above)

- **LH-1R** (`lh1`, 10 blocks): `train_updates==480`; every block
  `ea==16` and `eb==16` (`LH_BLOCKFAIL` otherwise); two full runs
  byte-identical (`r34_clean_equal==1`, world bytes equal); return-A
  `ra>=15`, zero weight updates, `active==0`; matched controls —
  disabled-update B probe `12/24` with `updates==0`, scrambled-reward A
  probe `0/16`. Max |score| reported (tainted: 18900, no clamp pathology).
- **LH-2R** (`lh2`, 40 blocks): `train_updates==1920`; every block 16/16;
  determinism as above; return-A gate as above; controls as above.
  Saturation report (not a kill bar, but the C2 claim needs it): block at
  which each correct cell pins at +30000 (≈300 net accepts expected),
  wrong-cell sink trajectory, post-saturation eval positives.
- **LH-3R** (`lh3`, 100 blocks, drift seed 333): `train_updates==4800`;
  bars per A5; drift schedule must equal the tainted 1,1,2,0,0,2,1,2,2,1;
  determinism as above; return `ra>=15`, zero weight updates (active
  reported). Stability classification (stable/oscillating/collapsed) with
  fingerprint evidence.
- **LH-5R** (`lh5` + `lh5rate` supplementary): four lineages at
  0/10/25/50% (seeds 5600/5610/5625/5650), `train_updates==480` each; full
  ramp run twice, byte-identical; supplementary single-rate runs at
  (10%,7777), (10%,4242), (25%,7777). **Validity gate:** the 0% lineage
  must show zero collapsed probes (20/20 at 16/16) — else the knee curve is
  confounded and the leg fails. The knee location itself is a *measurement*,
  reported as-is: per-block eval table per rate, endpoint curve, collapsed
  probe counts, switch counts per lineage, flip/accept counts.

## 5. Kill criteria vs leg verdicts

**Kills (stop the workstream, quarantine, report to parent):**
- **K1.** Any byte difference across the two determinism runs of a leg.
- **K2.** Static-audit failure: learner core not byte-identical to the
  frozen `../r34_clean_learner.zag`; any world/checkpoint import or RNG-term
  in the learner core; any harness RNG-term outside the two A6 devices.
- **K3.** Toolchain failure (compile error, nonzero runner exit unrelated
  to a leg bar).

**Leg verdicts (PASS/FAIL per leg, reported unsoftened — never a kill):**
a leg fails if its `LH_FAILURES`/`LH5_FAILURES` count is nonzero, i.e. any
bar in §4 is missed. **Headline rule: if a clean leg FAILS a bar the
tainted leg passed, that is the headline of the verdict, reported
unsoftened.** If a leg passes, the verdict names exactly which quarantined
claim (C1–C4) is restored by clean evidence.

## 6. Commit sequence (frozen)

1. This prereg, alone. (Frozen before any evidence exists.)
2. Apparatus: `r34_lh_clean_harness.zag` + `rerun/run_rerun.sh`. No prereg
   edits in this commit.
3. Evidence: `rerun/EVIDENCE_<stamp>/` bundles (commands, stdouts, diffs,
   SHA256SUMS, RECEIPT.txt) + `rerun/VERDICT.md`. No binaries
   (verification binaries live in /tmp only).

## 7. Pre-freeze work log (not evidence)

- 2026-09-20: harness written; `@import` is main-file-relative (znc) —
  harness placed next to the clean core (see §2 file-location note).
- 2026-09-20: policy-selection runs (refill 4/8/12, LH-1 leg): all
  `LH_FAILURES=0`, `ra=15`, `active=0`, identical switch cadence (19).
  Refill=8 frozen (mid-range, non-knife-edge).
- 2026-09-20: exploratory full-leg runs at refill=8 (dynamics sanity, not
  evidence): LH-1/LH-2/LH-3 all `LH_FAILURES=0`; LH-5 reproduced the
  tainted flip counts (46/124/241) and collapse pattern. These runs
  validated the harness; the evidence runs in §6.3 are fresh.

---
*Frozen 2026-09-20. Amendments, if any, will be dated and flagged for Micah's approval.*
