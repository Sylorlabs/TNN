# PERCEPTION THREE-ARM COST MEASUREMENT — frozen prereg

**Status:** FROZEN 2026-09-24T05:52:53Z (UTC), before any F3 build and before
any three-arm battery run exists. Recorded freeze timestamp is the UTC clock
read immediately before this file was written; no arm comparison data was
collected before it.

**Parent law:** `tnn-lab/senses/conscious-perception/preregs/FAIR_FIGHT.md`
(frozen 2026-09-23; the two-arm fair-fight battery, contract, measures, and
kill bars are inherited unchanged). This prereg ADDS the third arm (F3
deliberative-untrained) and the three-arm cost measurement protocol for the
consciousness bill. Nothing in FAIR_FIGHT.md is amended.

**Binary contract:** `tnn-lab/senses/rebuild/INTERFACE.md` as extended by
FAIR_FIGHT.md §0 — `fork <task> <fixture-path>` → stdout `key=value` lines,
exit 0. Required: `approach=AUTOPILOT|DELIBERATIVE`, `task`, `judgment`
(task vocab per INTERFACE.md), `confidence` 0..1000, `ops` int. Deliberative
extras: `resense=0|1`, `rs_kind=none|region|band|window|modality|decoder`,
`rs_ops=<int>`, `uncertainty=0..1000`, plus a non-contract extra
`policy=trained|untrained` to tell F2 from F3. Pure Zag for all mechanisms
(Python only as harness/interface glue), zero RNG in decision paths,
byte-identical stdout across ≥3 reruns (SHA256-checked).

## §1. Arms (frozen definitions)

- **F1 AUTOPILOT (control).** Frozen binary `tnn-lab/senses/rebuild/a_raw/sense`
  (SHA-256 `68db15216d9dc75a10839212ac5349195248f5ae113a7e37dc336795db8e35a1`,
  measured 2026-09-24T05:52:53Z). Fixed first-pass sampling policy, gate,
  warrant, ledger. Emits `approach=AUTOPILOT` via adapter (binary itself emits
  `approach=A`). Never killed — the control.
- **F2 DELIBERATIVE-TRAINED.** Real two-pass mechanism:
  `tnn-lab/senses/conscious-perception/forks/deliberative/f2.zag` (built
  2026-09-24 by its builder crew; REAL deliberating mechanism — verified from
  source: pass-1 bit-exact F1, interrupt-only background scan, six trigger
  types, per-task selector priority lists, used-selector bitmask, hard
  MAX_ACQ=6 + op deadline, depth-≤2 install-time verification, majority
  adjudication, SHA-256-chained ledger). The 0-catch selftest
  (`evidence/fairfight_runs/selftest/`, mean ops ratio 1.0, 0 resenses) used
  an intentionally disguised-autopilot binary to prove the harness fires
  KB-D1 — it is NOT this mechanism. Trained policy (frozen parameters):
  `CONF_BAR=250` uncertainty trigger, hint-driven selector priority
  (`f2_choose`), trigger-gated re-acquisition loop (stop when trigger
  evaluates TR_NONE), MAX_ACQ=6. Training-status caveat: the builder's
  RUNLOG shows parameter choices made against the train pool + builder-local
  battery runs that included test fixtures; whether the full FAIR_FIGHT §6
  protocol (3 zero-improvement search rounds, held-out check, anti-shopping)
  was satisfied is NOT verified here. F2 is "trained" in the sense of
  calibrated-to-this-pipeline parameters vs F3's deliberately naive ones.
- **F3 DELIBERATIVE-UNTRAINED.** Built for this prereg: byte-identical
  machinery to F2 (same `f1.zag`, `fio.zag`, selectors, resamplers,
  adjudication, verification, ledger) with an UNTRAINED policy only:
  1. Naive uncertainty threshold: `CONF_BAR=900` (resense unless
     near-certain; no calibration to this pipeline's conservative confidence
     scale — the naive default a trainer would pick without measuring it).
  2. Uncalibrated attention selection: `f2_choose` ignores trigger code and
     background hint — always the fixed per-task selector order
     [10,11,12,13(,)].
  3. Fixed resense budget rule: whenever the (naive) trigger fires, acquire
     exactly 2 pass-2 rounds in fixed order, then stop — no trigger-gated
     continuation, no hint guidance, no verified-install path differences
     (verification/adjudication/install code unchanged).
  F3 must be a real mechanism (it resenses, adjudicates, ledgers) and
  deterministic. F3 source diff vs F2 must be policy-only (constants +
  selection/loop policy), recorded in the F3 build log.

## §2. Battery (frozen)

- **Decision battery:** the 14 frozen fair-fight test fixtures
  (`tnn-lab/senses/conscious-perception/fixtures/test/`): omission om_p1–om_t2
  (6), inattentional ib_m1/m2 (2), ambiguity am_p1/am_c1 (2), illusion
  il_c1/il_c2 (2), redteam rt_p1/rt_c1 (2). Truth sidecars + MANIFEST.sha256
  re-verified per run.
- **Speed battery:** the 370 primary fixtures
  (`tnn-lab/senses/rebuild/harness/fixtures/*/primary/`) for S1–S4 analogues.
- Runs per (arm, fixture): 3 (byte-identity SHA256 check on full stdout).

## §3. Metrics (frozen)

Per (arm, fixture): judgment, confidence, ops, wall_s (harness-measured),
resense (0|1), rs_ops, uncertainty, byte-identical flag, contract-valid flag,
fixture SHA, binary SHA. Aggregated per arm × fixture class
(omission / inattentional / ambiguity / illusion / redteam; speed battery
aggregated per task):
- **accuracy** = fraction matching `.truth`.
- **mean wall-clock ms/episode**; **mean instrumented ops/episode**.
- **resense rate** = fraction of episodes with resense=1.
- **memory footprint** = peak RSS per episode via `/usr/bin/time -v`
  (harness-measured, outside the binary) + fixed arena sizes from source
  (ledger 64 KiB, buffers, bg scratch). If peak RSS is unmeasurable in this
  environment, the report states so explicitly — no substitutes.
- **catch (F2, F3 vs F1)** = correct ∧ autopilot wrong (12 scored fixtures);
  **false-install delta** = wrong ∧ autopilot right (≥2 → policy-review flag).

## §4. Kill bars (inherited from FAIR_FIGHT §7; applied to F2; F3 gets the same)

- **KB-D1** — zero catches over the 12 scored fixtures → killed.
- **KB-D2** — mean ops ratio > 2.0 AND catches < 3 → killed.
- **KB-D3** — redteam: any ops ratio > 10 or wall > 10× autopilot on the same
  fixture, or unbounded re-sense loop → killed.
- Autopilot wins (never kills): **KB-A1** speed legs >5% + named mechanism;
  **KB-A2** DoS immunity (cost not adversary-drivable); **KB-A3** no-op
  boundary (cost on provable-no-gain fraction).

## §5. Comparison questions (frozen — the report must answer each)

1. Per fixture class: F1 vs F2 vs F3 on accuracy, mean wall ms, mean ops,
   resense rate, footprint.
2. On which fixture classes does autopilot genuinely win (same verdict,
   lower cost)? Answer with numbers AND the mechanism reason.
3. Does the trained policy beat the naive one on the cost/intelligence
   frontier (F2 vs F3 catches per op)?
4. Byte-identity: ≥3 reruns byte-identical per (arm, fixture) or reported.

## §6. What this prereg does NOT decide

- It does not rule whether F2 satisfies the full FAIR_FIGHT §6 "proper
  training" protocol — that claim stays with the F2 builder's report.
- It does not amend FAIR_FIGHT.md (Micah-signed amendments only, program law).
- Outputs: `docs/lab/consciousness_cost/perception/RAW_RESULTS.md` (full
  table + run logs), F3 build log, adapter sources. No binaries, no `.zagd`,
  no `.zag-cache` committed to git; binaries rebuilt from pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

**Frozen:** 2026-09-24T05:52:53Z. Amendments go in a new file, never edits.
