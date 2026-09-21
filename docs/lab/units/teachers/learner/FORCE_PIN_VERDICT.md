# C3 FORCE-PIN VERDICT — B.6 (the one true lock)

**Worker:** C3 (Track B closeout) | **Date:** 2026-09-21 | **Frozen §4 hash:** `c7a9d57e3ac4d8ff48f4396c47eec9fedbfacb894584a31779a91a64deeef879`
**Spec:** PREREG_FREEZE.md §4 B.6 — "Forcing installation = a force-pin: visible, audited, external. Per standing law the learner cannot reverse a force-pin — the one and only exception, always visible in the audit trail as the trainer's action, not the learner's belief."
**Commit:** `d921459af52b9d37cdd8eec103adff9742c691e2` on `tnn-native-lab` (parent `afb32918809b`; fast-forward, no race)

## VERDICT: PASS — B.6 implemented to the frozen spec text

All four requirements hold, verified by 51 runtime checks + a static path audit + N=5 byte-identical runs + allocator perturbations. No frozen rule was amended; no live file was edited.

## 1. INVENTORY (kept vs rebuilt)

| Component | Action | Why |
|---|---|---|
| Learner audit-ledger layout (16-word entries, `store.zag` Ledger) | **Kept** (mirrored) | Frozen layout; the module reuses it verbatim |
| `AUD_FORCEPIN = 27` const in `delib.zag` | **Kept** (adopted as the module's op code) | Already reserved, never emitted — now has an emitter |
| Learner `Pins` registry (`store.zag` pins_add/pins_check) | **Kept, untouched** | Learner-writable, no origin — it is NOT a force-pin and cannot express B.6 |
| Harness `st_force_pin`/`st_force_unpin` (`st_memory_core.zag`) | **Kept, untouched** | Strength-trial substrate already refuses kills of force-pinned slots (ST_REFUSED_PINNED); owned by another line |
| Pin registry + FORCE_PIN audit op + trainer-only mutators | **Rebuilt** (new) | Nothing in the learner implemented B.6: no FORCE_PIN op was ever emitted, no trainer-origin tag existed, and `pins_add` is callable from learner-side code |

## 2. DESIGN (`units/teachers/learner/forcepin/forcepin.zag`, new, ~11KB)

`ForcePinStore`: span-keyed registry `(span_s, span_e, pin_trainer)` (cap 256) + its own append-only 16-word audit ledger (cap 512, FNV-1a-64 chain). Pure Zag; tables are `[]i64` (ZNC-007-clean); all arrays explicitly zeroed; no slice over the 2^25 wall.

- **(a) FORCE_PIN as the TRAINER's action.** `fp_pin(fp, caller, trainer, s, e)` requires `caller == FP_CALLER_TRAINER`. Every attempt is audited (op=27): `d1=caller` (the origin tag — 1=TRAINER on success), `d2=trainer_id`. The pin entry is visible in the audit trail as the trainer's action, never the learner's belief.
- **(b) Learner paths refuse with §L codes.** `fp_gate_revise` / `fp_gate_reject` / `fp_gate_kill` return `FP_REFUSED_PINNED` (102) for any pinned/overlapping span; the wired learner surfaces this as frozen §L **R2 CONFLICTS_PINNED** (value 2). Each refused attempt is audited (op=34, `d1=LEARNER`) — the attempt is the learner's, the lock the trainer's.
- **(c) No learner path can set/clear a pin.** The only stores to the pin tables in the module are inside `fp_pin` (1 site) and `fp_unpin` (1 site), each dominated by the trainer-caller guard. Proven by `static_audit.sh` (claim A: all 6 store lines inside the two mutators, guard-dominance checked; claim B: the live learner tree contains zero `fp_` symbols — no live path can even reach the mutators; claim C: the wiring patch calls only read-side `fp_check`/`fp_gate`/`fp_gate_kill`, never the mutators) **plus** runtime forgery tests (learner-issued `fp_pin`/`fp_unpin` → 101, pin unset/persisting, attempts audited as the learner's).
- **(d) Trainer unpin/re-pin, audited.** `fp_unpin` requires trainer caller AND matching original pin-trainer (wrong trainer → 104, pin persists). Unpin emits op=33 with `d1=TRAINER`. Re-pin is idempotent (original pin-trainer kept) or fresh after unpin; the full pin→unpin→pin history is in the ledger.

**Wiring (scratch-validated, delivered as patch):** `forcepin/patch/delib_forcepin.patch` (+ validated copies in `forcepin/scratch/`). The patch is strictly additive to `delib.zag`: `DLB.fpins` field + init, force-pin state folded into `dlb_digest`, ELIMINATE consults `fp_check` → §L R2 with audited refusal, and `dlb_retract` refuses to kill a force-pinned unit (V_REJECT / R2). The old learner-side `Pins` is left untouched (see parked item 1).

## 3. TESTS

| Suite | File | Checks | Result |
|---|---|---|---|
| Module contract | `forcepin/tests/test_forcepin.zag` | 34 (pin/audit-origin, exact/overlap/disjoint, 3 gates → 102, refusals audited, forge pin/unpin → 101, wrong-trainer unpin → 104, unpin+re-pin, history) | **PASS** |
| Wired end-to-end | `forcepin/scratch/test_wired.zag` | 17 (baseline ADOPT, trainer pin, same-span REJECT/R2, overlap REJECT/R2, RETRACT refused R2 with unit still HS_ADOPTED, forged unpin → 101, pin persists, 2nd RETRACT refused, clear-span still ADOPTs) | **PASS** |
| Static path audit | `forcepin/static_audit.sh` | claims A (6 store sites, guard dominance) / B (no fp_ in live tree) / C (wiring read-only) | **PASS** |
| Determinism | `run_tests.sh` | N=5 byte-identical per binary; `MALLOC_PERTURB_` ∈ {0,165,17} | **PASS** |

Determinism SHAs: module `754f10db3b8d34598c8e9b9d448d47cbbb5c88ab6631fe89d5ce06a304c7deac` · wired `b5551d6884e2d64e6b42921867667035bd48466b4d0b3e5d29b62a0a02cda35a`. (Logs: `forcepin/logs/`.)
Toolchain: `znc_linux_x86_64_abed8aa1 --no-zagd --no-analyze --no-foreground-cache`. Builds ran in `~/workspace/tnn-lab/scratch_c3` (never /tmp, never committed).

One test-debug note (honest): the first wired run targeted the RETRACT at a stale seq (an intervening rejected proposal had advanced `last_seq`), so the retract missed its target (R_RETRACT_REFUSED, reason 8) — the test was fixed to target the live `last_seq`; the mechanism was correct throughout. Evidence of the FAIL-then-fix is in the run history, not hidden.

## 4. FILES (all new; no live file edited)

- `units/teachers/learner/forcepin/forcepin.zag` — the module
- `units/teachers/learner/forcepin/tests/test_forcepin.zag` — 34 module checks
- `units/teachers/learner/forcepin/scratch/` — learner copies + patched `delib.zag` + `test_wired.zag` (17 wired checks)
- `units/teachers/learner/forcepin/patch/delib_forcepin.patch` — the wiring diff for live `delib.zag`
- `units/teachers/learner/forcepin/static_audit.sh`, `run_tests.sh`, `logs/`

## 5. PARKED FOR MICAH

1. **Learner-side `Pins` vs force-pin.** `store.zag`'s `Pins` remains learner-writable (`pins_add` is called from learner-side code, no origin). The B.6 force-pin is a separate, trainer-only registry; the old one is not a force-pin and must not be presented as one. Whether to deprecate/route `pins_add` through `fp_pin` (a behavior change to frozen-verified `test_pins`) needs your call.
2. **Wiring patch application.** The patch is validated on a scratch copy only. Applying it to live `delib.zag` is the coordinator's / your call (file-ownership rules).
3. **Harness-side force-pin** (`st_force_pin`) already existed and was kept as-is — I did not re-verify its test suite here; that belongs to the harness line.

## 6. COMMIT

Evidence committed to `tnn-native-lab` via `~/workspace/commit_to_branch.py` (all files <96KB; no binaries, no `.zagd` caches committed):
- SHA: `<recorded at push time>`
