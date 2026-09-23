# PREREG: COUPLED-COMPOSE-1 — test that the artifact is a function of the deliberation

**Status:** FROZEN 2026-09-22. Design only — no implementation authorized by this
document. Any change to boundary, arms, bars, or measurement needs a dated
amendment with Micah's re-approval.

**What this proves:** the single missing mechanism named in `DIAGNOSIS.md` §4 —
a composition operator that maps accepted knowledge records to artifact content.
It does not prove full human-like invention (decomposition H1 / interface
sketching H2 remain future work). It proves the hands exist: change what TNN
accepts, and the artifact changes accordingly.

**Standing law:** pure Zag, zero RNG in any decision path, byte-identical reruns,
pinned toolchain `znc_linux_x86_64_abed8aa1`.

---

## 1. Boundary

- The deliberation machinery (proposer, critic, diagnoser, episode ledger) is
  frozen as-is from the T1N rerun engine. Only the compose step may be replaced.
- The replacement composer MUST satisfy: the emitted module is constructed from
  the accepted mechanism records — emitter bodies placed from the records, the
  selection dispatch generated from the records' trigger lists, citations derived
  from the actual episode sequence. No fixed module template: any byte-span of
  the emitted module that is identical across runs with different accepted sets
  must be interface/harness scaffolding declared in advance in §3, not
  architecture content.
- Crew-authored (allowed): the module interface (function signatures — a contract,
  not architecture, per T1N prereg §1.2(c)), the probe battery, the oracles.
- TNN-produced (required): which emitters exist, their trigger lists, the
  selection rule, the revision policy, the slot-filling rules — all citing
  deliberation episodes and taught entries.

## 2. Arms (the manipulated variable is the accepted set)

- **Run A:** teach mechanism inventory {reverse, sum}. Corpus: prior-art records
  describing reversal and summation architectures (prose principles, no complete
  code templates for the target interface).
- **Run B:** teach mechanism inventory {reverse, max}. Same prose-principle form,
  same record count, same budgets, same probes, same everything — the ONLY
  difference is sum-records vs max-records.
- 3 reps per run, byte-identical required within a run.

## 3. Declared-fixed scaffolding (the only bytes allowed to be identical across A/B)

Before any run, commit the exact list of byte-spans that may be shared across the
two modules (interface signatures, NUL-output ABI helpers, module header). Any
shared byte-span NOT on this list is a B1 failure.

## 4. Bars

- **B1 — coupling (the load-bearing bar):** `sha256(module_A) ≠ sha256(module_B)`,
  and the unified diff is confined to emitter/selection content attributable to
  the sum-vs-max records. Provenance audit: every differing line cites a
  deliberation episode or a taught record ID. (Under the current T1N machinery
  this bar fails by construction — all composer parameters are dead — which is
  what makes it a valid test of the fix.)
- **B2 — composition, not retrieval:** the max emitter in module B is NOT
  byte-identical to any taught record or KB entry. It must be transliterated
  (mechanism description → code), not copied. Byte-copy = retrieval, not
  invention.
- **B3 — function:** both modules compile under the pinned toolchain; module A
  scores strictly above the fixed-template baseline on held-out sum probes;
  module B scores strictly above it on held-out max probes. (The T1N rerun's
  fixed template is the baseline; "strictly above" is measured, not asserted.)
- **B4 — judge preserved:** the critic still refuses uncompilable taught entries
  on compile evidence (the working behavior from the rerun must not be lost when
  the composer is replaced).

## 5. Kill criteria

- B1 fails (modules identical) → the composition operator is not
  deliberation-parameterized. The missing mechanism is not built. STOP.
- B2 fails (emitter is a byte-copy) → retrieval, not invention. The transliteration
  step (DIAGNOSIS.md H3) is not built. STOP.
- B3 fails on either arm → the hands exist but don't work. Report as partial.
- B4 fails → the repair regressed the judge. Revert.

## 6. Measurement

- Held-out probes: sum and max probe sets frozen before Run A; never used as
  deliberation evidence (no leakage — the rerun's PR1/PR2 lesson applies).
- Distractor integers in probe specs (e.g. type annotations, counts) to catch
  slot-filling without semantics — the `i32 → 32` class of bug fails B3 by
  construction if the binding rule is "parse all integers."
- Determinism: 3/3 byte-identical reps per run (module bytes + battery log).
  Zero RNG. Canonical JSON logs with sha256, as in the T1N rerun.

## 7. Predicted outcomes (published before implementation)

- If the diagnosis is right, B1 is the bar the current machinery cannot pass and
  the fixed machinery must pass first — it is the cheapest decisive check.
- B2 is expected to be the hard one: transliteration (prose mechanism → code
  honoring the record's slots) is the step with no existing operator.
- B4 is expected to pass unchanged — the critic is not being replaced.

## 8. What this does NOT claim

Passing COUPLED-COMPOSE-1 does not mean TNN invents like a human. It means the
artifact is a function of the deliberation — the precondition for every harder
claim. H1 (functional decomposition) and H2 (interface sketching) remain
unbuilt and untested after this.
