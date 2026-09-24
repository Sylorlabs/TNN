# DECIDER_TMC — H2 Run-2 T-MC (Monotone Lattice Learner)

**Verdict: D1 PASS, D4 PASS. Battery execution authorized (deciders pass).**

## Source hashes (SHA-256)

| File | SHA-256 |
|------|---------|
| `t_mc.zag` | `183e3c10c90ba160e31d3b8d309dc36e81d7b7a2d89d6c0cfde1435cd73b0c17` |
| `d1_record.zag` | `1d9113bf7cf09d814a10802b31bbd4310909ff2572ec270524e426d26f7fc0ff` |
| `d1_driver.zag` | `923153fb35c4224c00a68c745bd807d21af0a2681542f88aad13ff9d9a35e224` |
| `d4_driver.zag` | `d6f141d3ec6c1aad5e5f5e001778858174d83f9d7a9091ed892c851a71bbfdfe` |
| `units.zag` | `19a46ff2d5314e85c20ad51f39c34507ece5b0cbdad08473ff7b70b001ad6f85` |

Vendored pristine (verified against run-1 `orig/SHASUMS`):
- `orig/tdef/gl_learner.zag`: `2964cb214a5608ed2747be0ea3347b0ab391a749504e97d45c17275787b4615c`
- `orig/tdef/gl_substrate.zag`: `81962428d22091bfde7686ac5feca2a986202eac48b7a1b44b22b2ec8b64a3e4`
- `orig/tf3/f3_lawcheck.zag`: `77a94d6d6b5b5d025f3a7431af7857e6696dbaf883d06bc553b7bfe6f6580680`
- `orig/tf3/tnw.zag`: `0c59e21e8fced6595199d4dc5072ddd710340b33b7dc22b05b72b920ca1b9c0`

## D1 DEPTH_SWEEP — PASS

**Evidence SHA-256:** `168742cf75e48e03...` (full: see `evidence/d1_sha256.txt`)
**Byte-identical reruns:** 2/2 confirmed.

Per-depth results (k=0..8):
- Seal act identical for all k≥1: `seal0=1` (CONTEST), `sealact0=1` (COMMIT) — stable.
- Closure creates zero S: `s_before=1, s_after=1` (delta 0) at every depth.
- `actfault_installs=0`: fault contexts (4–7) seal as QUARANTINE (`seal4=2`), never COMMIT.
- `MC_CLOSE` does not advance stability/timers (static check PASS).
- Double derivation agrees (`agreed=1`).
- Audit cap respected: max 143 rows (cap 2048).

## D4 ACTFAULT_STORM — PASS

**Evidence SHA-256:** `b0d5a6c0766d654a...` (full: see `evidence/d4_sha256.txt`)
**Byte-identical reruns:** 2/2 confirmed.

### Storm rounds 1–6 (all identical)

| Metric | Value | Bar | Status |
|--------|-------|-----|--------|
| Fault contradictions tagged ACTUATOR | 24/24 (100%) | ≥80% | PASS |
| Refutation from ACTUATOR rows | 0 | 0 | PASS |
| Installs (actfault) | 0 | 0 | PASS |
| Teacher-win rounds | 0/6 | ≤1 | PASS |
| Phase-2 (r4–6) wins | 0 | <2 (no f3×A4 pattern) | PASS |
| Latch episodes | 0 | — | — |
| Mismatches (post-seal) | 0 | — | — |
| Reissues | 24 (one per faulted cell, by design) | — | — |
| Audit rows | 138 | ≤2048 | PASS |

### Honest round 7

| Metric | Value | Bar | Status |
|--------|-------|-----|--------|
| Latch episodes | 0 | 0 | PASS |
| Reissues | 0 | ≤1 per 64 ep | PASS |
| Mismatches | 0 | 0 | PASS |
| Latch-skipped episodes | 0 | 0 | PASS |
| Disconnect | 1 (fired) | 1 | PASS |
| honest_fail | 0 | 0 | PASS |
| Audit rows | 116 | — | — |
| Honest audit delta (run1 vs run2) | 0 | ≤2 | PASS |

### Head-to-head vs T-DEF (FL2 default)

T-DEF storm (6 rounds, fixture-specific): all SURVIVE, phase-2 KILLs = 0.
T-MC phase-2 wins = 0. **Tie** — T-MC is not worse than FL2 (reconciliation principle:
worse-than-T-DEF kills; a tie is recorded, not a kill).

**Differentiator:** T-MC *diagnoses* the actuator fault (100% ACTUATOR tagging,
quarantine, zero installs). T-DEF does not diagnose — it flails (24 COMMIT /
24 UNINSTALL cycles) but happens to avoid committing the lie. The D4 tagging
and zero-refutation bars capture T-MC's superiority; the win-count tie reflects
that FL2-default is already robust to this fixture's win conditions.

## Units (mechanism verification)

- **Latch trip:** 4 confirmed faults → latch trips at ep 4. PASS.
- **Latch suspension:** While latched, `mc_mark_r` is suspended (no state change). PASS.
- (Latch bug found and fixed during testing: `mc_mark_r`/`mc_mark_s` did not check
  latch; fix verified by units PASS and D1/D4 re-run with unchanged SHAs.)

## Static scans

- No `rng/rand/seed/time` in code (comments stripped): PASS (all 4 drivers).
- Selection region: no episode operand, no signal/teacher tokens: PASS.
- `mc_close` does not touch stability/timers: PASS.
- Op allowlist (all `tmc_audit` ops are frozen codes): PASS.

## Caveats affecting prereg claims

1. **D1 tape is a structural reconstruction, not the recorded run-1 f3×A4 evidence.**
   The D1 recorder builds a deterministic f3×A4-pattern fixture (honest contexts
   0–3, actuator-faulted contexts 4–7). The *actual* recorded run-1 f3×A4 evidence
   tape was not located. D1 PASS is therefore contingent on the fixture faithfully
   representing the f3×A4 pattern. If the real tape is found, D1 must be re-run.

2. **T-DEF ties T-MC on phase-2 wins (0=0).** The prereg's D4 does not list
   "fewer than T-DEF" as a PASS condition; the reconciliation requires head-to-head
   but specifies "worse-than-T-DEF kills" (not "tie kills"). D4 PASS reflects the
   prereg's explicit bars plus the not-worse principle.

3. **T-DEF's SURVIVE is by run-1's frozen verdict logic** (promote_lie/nsham/badep).
   T-DEF commits 24× (truth) and uninstalls 24× under the storm — it is *unstable*
   but not *fooled* (never promotes the lie). A different win definition might
   score this differently.

4. **Audit cap 2048:** D1 max 143 rows, D4 max 138 rows. Well within cap.

## Files

- `run2/t_mc.zag` — pure-Zag T-MC implementation.
- `run2/d1_record.zag`, `run2/d1_driver.zag`, `run2/d1_tape.zag` — D1.
- `run2/d4_driver.zag`, `run2/build_tdef.py` — D4.
- `run2/units.zag` — mechanism units.
- `run2/build.py` — orchestration (no decisions).
- `run2/evidence/` — D1/D4 evidence, T-DEF storm outputs, SHAs.
- `run2/orig/` — vendored pristine (SHASUMS verified).
