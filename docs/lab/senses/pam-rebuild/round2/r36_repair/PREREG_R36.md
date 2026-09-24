# PREREG_R36 — Repair Prereg: Fresh-Seed Discipline for H-PAM-36 (M-36 closure)

**Crew:** R-36 repair crew (PAM round-2 swarm)
**Date:** 2026-09-24
**Status:** FROZEN (committed alone before code; this document governs the repair build and battery)
**Target:** H-PAM-36 (commit-then-sample), killed at the implementation level by RT-JKLM class M-36
**Background commits:** H-36 frozen prereg `0a48bdbad25cbc358b7836e7cd34a33b248c7cfa`;
H-36 probe evidence `8d16d9f3`; RT-JKLM prereg `d050ce4e`, evidence `ec8d5d13`.

## §1. What is being repaired

RT-JKLM verdict (`docs/lab/senses/pam-rebuild/round2/rt_jklm/VERDICT_RT_JKLM.md`,
interpretation §7): the H-36 probe hardcoded its world seed
`(305419896, 2596069104)` — in the read set via the committed source. The M-36
fixture class precomputed the full W_t chain **offline** (0 in-run queries, 0
sensor reads) and committed world-consistent percepts → **120/120 installs**,
killing blind commitment under seed reuse. The kill strikes the implementation,
not the hypothesis: fresh, author-invisible, non-repeated seeds were already a
recorded deployment condition of H-36 (the WG bar assumed them; grok's
load-bearing claim confirmed).

**Repair R-36:** implement fresh-seed discipline MECHANICALLY in the probe:

- **R36-S1 — transcript-derived seed.** No literal seed constant anywhere in
  harness code. At run start the harness builds a committed transcript `T`
  (byte-exact, §3) and derives `seed = ns_sha256(T)` via the native SHA-256
  substrate (`R33_NATIVE_SHA256_V2.zag`, `ns_sha256`). The world chain anchors
  at `(shi, slo) = (LE64(digest[0:8]), LE64(digest[8:16]))`; `wstep` evolution
  is otherwise unchanged (frozen mechanism).
- **R36-S2 — seed-reuse detector.** The harness keeps a used-seed ledger
  (path via argv). Before any trial it checks `seed_hex ∈ ledger`: on repeat
  it prints `REFUSED_SEED_REUSE seed=<hex>` loudly, exits nonzero, and admits
  nothing. Otherwise it appends `seed_hex` and proceeds.
- **R36-S3 — operator material.** `T` includes 32 bytes of operator material
  supplied at runtime via argv (never hardcoded, never in the fixture read
  set, never passed to fixture fns). In the probe it is deterministic and
  documented (§3); in deployment it must be fresh and author-invisible per run
  (the recorded H-36 disjoint-channel residual — unchanged by this repair).

## §2. Scope

This repair closes **M-36 only** (the seed-reuse kill). Out of scope and
unchanged: J-36 (identity residual — preregistered SCOPE, not a kill), K-36
(blind commitment vs NT — held), L-36 (sample independence — held). The
transcript-replicating adaptive attacker that *possesses* the operator material
is outside the M-36 fixture class (defined as offline precompute, 0 in-run
queries) and is recorded as a residual, not tested here.

## §3. Seed transcript (byte-exact)

```
T = "R36.SEED.v1" || 0x00 || PREREG_SHA_HEX || 0x00 || MODE || 0x00
    || TRIALS || 0x00 || MATERIAL_HEX || 0x00 || ANCHOR_HEX
```

- `PREREG_SHA_HEX`: full 40-hex SHA of this prereg's alone-commit on
  `tnn-native-lab` (value recorded in the evidence commit before building).
- `MODE`: `batt` | `m36` (distinct seeds per mode by construction).
- `TRIALS`: `120`.
- `MATERIAL_HEX`: 64 hex chars from `argv[2]`.
  Evidence value: `hex(SHA256("R36-SEED-MATERIAL:" || prereg_commit_sha))`
  (computed with `sha256sum`; deterministic, documented, reproducible; chosen
  independently of — and never supplied to — the M-36 fixture class).
- `ANCHOR_HEX`: `` (empty; genesis — run-chaining anchor reserved for deployment).
- `seed = ns_sha256(T)` → 32-byte digest; `seed_hex = ns_hex(digest)`.

## §4. Battery: `batt` mode (repaired H-36 probe)

Usage: `r36_probe batt <material_hex> <ledger_path>`. Mirrors the frozen
H-36 probe sections, re-anchored at the transcript seed:

- **H (honest):** 60 steps, sensor-honest `(conf,meas) = (honest_wc, honest_wm)`
  vs transcript-seeded W_t → `r36_h_admitted`. Bar: 60/60 (pass ≥ 57/60).
- **F (frozen):** 60 steps, blind modal guesses `(adv36_conf, adv36_meas) =
  (1700, 50000)` correctly committed → `r36_f_admitted`. Bar: 0/60.
- **RC (reactive):** 60 rounds; after commit, a bounded 5000-eval deterministic
  search tries to invert `s_t → W_t`; `r36_rc_admitted` (bar 0/60),
  `r36_rc_w_recoveries` (bar 0; 300,000 evals total).
- **WG1 (sample identity):** 120-step honest stream vs 120-step adversarial
  stream; sample sequences must be byte-identical → `r36_wg1_match`.
  Bar: 120/120.
- **WG2 (bounded inversion):** 200,000 deterministic attempts to recover W_0
  from s_0 → `r36_wg2_success`. Bar: 0.
- **WG3 (source audit):** `wg3_r36_audit.sh` — (a) `305419896`/`2596069104`
  absent outside the marked M36-ATTACKER-CLASS section; (b) no
  seed/material/digest identifiers in fixture-fn signatures or bodies
  (`adv36_conf`, `adv36_meas`, `m36a_*`); (c) all `wstep` call sites
  harness-side; (d) `ns_sha256` called only in `r36_derive_seed`. Bar: CLEAN.

## §5. M-36 retest: `m36` mode

Usage: `r36_probe m36 <material_hex> <ledger_path>`. The M-36 fixture class is
**extracted by script** (`gen_r36.py`) from
`round2/rt_jklm/drive36.zag::run_m` — asserted parameters: attacker seed
`(305419896, 2596069104)`, 120 trials, `id = 8000+t`, full W-chain precomputed
offline into tables (0 in-run queries, 0 sensor reads), percepts
`(conf,meas) = (honest_wc, honest_wm)` of the *attacker's* world with correct
`cstep` commitments. The harness admits against the **transcript-seeded** W_t.

- `m36_install` — bar: **≤ 15/120** (repair kill bar K1).
- Honest control in `m36` configuration: 60 honest steps →
  `m36_honest_admitted` — bar: ≥ 51/60 (honest-loss ≤ 15%).

## §6. Seed-reuse detector test (separate from the 3× battery)

Run `batt` twice with the **same ledger file** (same material). The second run
must print `REFUSED_SEED_REUSE`, exit nonzero, and admit nothing. This test is
not part of the determinism battery (which uses a fresh ledger per run).

## §7. Determinism

`batt` 3× (fresh ledgers L1/L2/L3, same material) → SHA-256 of full stdout
identical; `m36` 3× (fresh ledgers L4/L5/L6) → identical. Any divergence voids
the battery. Pure Zag, zero RNG. Fixture/generator SHAs pinned in evidence.

## §8. Kill bars (repair-level)

| ID | Check | Bar | Effect if fired |
|----|-------|-----|-----------------|
| K1 | `m36_install` | ≤ 15/120 | **>15 → repair FAILS** (H-PAM-36 stays TESTED-killed; repair recorded killed) |
| K2 | `r36_f_admitted` | == 0/60 | ≠0 → repair fails |
| K3 | `r36_rc_admitted` / `r36_rc_w_recoveries` | == 0/60, == 0 | ≠0 → repair fails |
| K4 | `r36_wg1_match` | == 120/120 | <120 → repair fails |
| K5 | `r36_wg2_success` | == 0 | >0 → repair fails |
| K6 | WG3 audit | CLEAN | DIRTY → repair fails |
| K7 | `r36_h_admitted` | == 60/60 | <60 → repair fails (bar floor 57/60) |
| K8 | `m36_honest_admitted` | ≥ 51/60 | <51 → honest-loss > 15% → class void |
| K9 | detector test | loud refusal + exit≠0 | silent repeat → repair fails |

All green → fresh-seed discipline closes M-36 → backlog H-PAM-36 →
TESTED-survived (repaired). Any red → TESTED-killed stays, repair killed.

## §9. Residuals (recorded, not patched)

- R-36 models author-invisibility with runtime-supplied operator material; a
  real deployment must exhibit a physical/organizational fresh-seed channel
  (the H-36 residual, unchanged).
- The probe material is fixed and documented for reproducibility; deployment
  must rotate it per run (reuse detector enforces non-repetition).
- J-36 identity residual untouched (out of scope).

## §10. Build & evidence

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).
- Workdir: `~/workspace/r36_repair/` (scratch; never /tmp). Binary never committed.
- Evidence commit (after this prereg): `r36_probe.zag` (generated),
  `gen_r36.py`, `run_r36.py`, `wg3_r36_audit.sh`, substrate copies,
  `runs/` (3× outputs per mode + SHA256SUMS), `VERDICT_R36.md`,
  `RUNLOG_R36.md`.
- Repo path: `docs/lab/senses/pam-rebuild/round2/r36_repair/` on branch
  `tnn-native-lab` (sylorlabs/TNN). This prereg committed ALONE first.
