# MINI-PREREG M2 — Adversarial-heap differential fingerprinting

> **FROZEN — 2026-09-25** under `PREREG_GATE_EXPANSION.md`.
> Method: the perturbation schedule is the detector. Any nondeterminism
> that can influence behavior will diverge under SOME dirt pattern.

## 1. Hypothesis

Hardened replay compares outputs across runs, but its perturbation space
is shallow (a few heap fills). A PREREGISTERED adversarial perturbation
schedule — dirt patterns × env shapes × allocation-base shifts, all
deterministic, zero RNG — turns behavioral differential testing into a
gate: a build whose observable behavior is a pure function of
(input, logged state) cannot diverge; anything that diverges is
nondeterministic by construction, no idiom recognition required.

## 2. Decision procedure (frozen)

**Audit allocator** `m2_audit_alloc.zag`: a drop-in replacement for the
build's allocation primitive with a dirt-pattern register. On every
allocation it fills the block with the active pattern BEFORE handing it
out (so uninit reads observe the pattern, deterministically).

**Driver** `m2_driver.zag` (pure Zag, pinned toolchain):

1. Builds the target variation module against the audit allocator
   (source-level link; the target's allocation calls resolve to the
   audit allocator — committed build record).
2. Runs the target under the perturbation schedule (frozen):
   - Dirt patterns D ∈ {0x00, 0xFF, 0xAA, 0x55, counter, 0xDEADBEEF-cycle}
     → 6 patterns.
   - Env shapes E ∈ {empty, 1KB deterministic pad, 64KB deterministic pad}
     → 3 shapes (shifts addresses, catches env/argv/ASLR dependence).
   - Total 18 runs per module. All schedule values are compile-time
     constants; zero RNG anywhere.
3. Records SHA-256 of full stdout (+ state/log outputs) per run.

**Verdict.**
- All 18 hashes identical → `PASS`.
- Any divergence → `FAIL` with the divergent pair (patterns, hashes,
  first-differing byte offset) recorded.

## 3. Battery mapping (pre-declared scope — frozen)

| Plant | Expected | Rationale |
|---|---|---|
| P01 getrandom | FAIL | fresh bytes every run → divergence |
| P02 clock_gettime | FAIL | ns-resolution time diverges across 18 runs |
| P03 /dev/urandom | FAIL | fresh bytes every run |
| P04 uninit read | FAIL | dirt patterns change observed values |
| P05 env-var | FAIL | env shapes change the value (or its presence) |
| P06 ASLR leak | FAIL | env shapes shift addresses |
| P07 rdtsc | FAIL | counter diverges |
| P08 hash order | AT-RISK | diverges only if order is per-process-varying; fixed dirt may keep it constant → may miss |
| P09 innocent tables | PASS (clean) | deterministic tables do not diverge — correctly not flagged |
| P10 machine-id | OUT-OF-SCOPE (gap) | lab-constant across runs; differential methods cannot see it in principle |
| P11 argv[0] bytes | FAIL | driver varies argv[0] length across runs |
| P12 invoke-discard | OUT-OF-SCOPE (gap) | no observable effect under any perturbation (replay-prereg §10 class) |

**Counting rule (frozen):** FAIL on a dirty plant = CAUGHT. P09 is a
dirty plant that MUST NOT be flagged (deterministic by construction) —
for M2, P09 counts toward K-CATCH as "correctly passed" (it is the
v2/v3-killer shape; M2's answer is behavioral, not idiom-based).
OUT-OF-SCOPE excluded from denominator with reason; AT-RISK counts
normally.

**K-CLEAN mapping:** C01,C02,C04,C05,C06 must PASS (18/18 identical).
C03 (fenced RNG): the seeded RNG is deterministic given the logged seed
→ expected PASS (seed fixed across runs). If the crew's build cannot fix
the seed, declare out-of-scope pre-test with reason.

## 4. Kill-bar instantiation

- K-CATCH: 10 in-scope (P01–P08,P11 + P09-correct-pass) — all must be
  decided correctly.
- K-CLEAN: 5–6 modules (per C03 declaration) — all PASS.
- K-RED: 12 novel plants, blind, per umbrella §5. Expected red focus:
  lab-constant channels (P10-class), invoke-discard (P12-class),
  perturbation-synchronized sources (e.g. a clock read at a fixed
  instruction count that happens to be constant across fast runs).
- K-DET: 3/3 byte-identical full-schedule reruns (all 18 hashes stable).

## 5. Known hard problems (stated pre-test)

1. **Perturbation-synchronized constancy:** a coarse clock (1s
   granularity) may return the same value across 18 fast runs → false
   PASS. Mitigation (frozen): the driver inserts a deterministic
   1.1-second busy-wait between runs 9 and 10 (instruction-counted, no
   clock). If the plant still doesn't diverge, it's a miss — recorded.
2. **Allocator-link fidelity:** the audit allocator must be a TRUE
   drop-in (same layout semantics as the production allocator) or the
   gate certifies a different build than ships. The crew commits a
   layout-equivalence proof (same block header, same alignment) before
   testing.

## 6. Evidence layout

`wave12/step1a-v2/gate-expansion/evidence/m2/`:
`m2_audit_alloc.zag`, `m2_driver.zag`, schedule constants, build log +
SHAs, per-plant 18-hash tables, `M2_VERDICT.md` with the kill table.
