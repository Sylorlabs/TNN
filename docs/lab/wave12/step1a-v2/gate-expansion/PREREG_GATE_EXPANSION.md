# PREREG — Arm C no-RNG gate expansion (fresh methods + hypotheses)

> **FROZEN — 2026-09-25.** Ordered by Micah 2026-09-25 ~13:50 PDT:
> "For arm C find more methods and hypothesis."
> Any change requires a dated amendment flagged for his review.
> NOTHING HERE IS SIGNED OR ADOPTED. No signature on Micah's behalf is
> authorized anywhere in this expansion.

**Context.** Arm C is parked behind the frozen §3 gate (prereg `97882fc`):
an unkilled no-RNG auditor. Auditors v1, v2, v3 were all killed by their
own blind red teams (v1: env-var indirection; v2/v3: innocent-named
hand-rolled tables) — the empirical signature of an inexhaustible idiom
space. A replacement package (hardened replay + thin certifier + v2
tripwire + residual-risk statement) is drafted but unsigned
(`wave12/step1a-v2/gate/AMENDMENT_2026-09-20_ARMC_GATE_S3.md`).
Separately, the i32-cast audit proved the thin certifier miscompiles on
consecutive same-size `as []i32` casts; its 2026-09-20 gate evidence must
be re-derived from the arena-rebuilt certifier
(`redteam/certifier-rebuild/thincert_rb.zag`).

**Purpose.** Broaden the gate-method search beyond replay+certifier with
FRESH hypotheses, each held to the same kill discipline that killed v1–v3:
frozen mini-prereg with kill bars BEFORE testing, planted-RNG positive
controls, clean negative controls, and its own blind red team. Dead
methods are results — kills are recorded honestly, never repaired
mid-round.

## 1. The four candidate methods (hypotheses)

| ID | Name | Core idea | What it is NOT |
|---|---|---|---|
| M1 | **Seccomp capability sandboxing** | Enforce no-RNG at the kernel boundary: run the frozen build under a seccomp-bpf filter (+ `PR_SET_TSC`) that kills the process on entropy/clock syscalls. Detection-independent — disguise is irrelevant at the syscall layer. | Not a source scan. Not replay. |
| M2 | **Adversarial-heap differential fingerprinting** | Perturbation-space replay: run the build N times under systematically dirtied heaps, varied env/argv, shifted allocation bases (deterministic perturbation schedule, zero RNG); hash full outputs. Any divergence = FAIL. | Not plain 2-run replay; the perturbation schedule is the method. |
| M3 | **Decision-trace equivalence** | Zag-level instrumentation emits a trace of every decision-relevant event (branch outcomes, volatile/uninit reads, external-input bytes). Compare traces across adversarial runs AND prove the trace contains no volatile-region reads. Replay compares outputs; this compares the decision path. | Not output replay. Not a scan. |
| M4 | **Determinism-by-construction subset compiler** | A refusing compiler for a restricted Zag dialect: no raw syscalls, no env/argv beyond whitelisted indices, init-before-read enforced at parse, no hash iteration. Non-subset code does not build. The gate is "this binary was produced by the subset compiler from this source" — constructive, not post-hoc detection. | Not a post-hoc rule scan (thincert scans arbitrary Zag; this refuses to compile it). |

The incumbent reference for head-to-head comparison is the unsigned
package: hardened replay + thin certifier (arena-rebuilt).

## 2. Shared kill bars (frozen; bind every method M1–M4)

- **K-CATCH:** the fixed plant battery (§3, 12 plants) — the method must
  flag every dirty plant (FAIL verdict / divergence / kill / refusal, per
  the method's decision procedure). One miss kills the method version.
- **K-CLEAN:** the fixed clean set (§4, 6 modules) — the method must pass
  all six (no false positives). One false positive kills the method
  version. (A method may declare a clean module out-of-scope ONLY in its
  frozen mini-prereg, with reason; undeclared false positives kill.)
- **K-RED:** blind red team per method (§5): separate worker, receives only
  the method's public interface description (what the method checks), NOT
  its implementation. 12 novel plants per method, preregistered categories
  (§5). Miss rate > 0 kills the method version. Same bar that killed v1–v3.
- **K-DET:** the method's own machinery is deterministic: 3/3
  byte-identical reruns of the full battery per method.
- A killed method version is DEAD — no mid-round repair, no v-next under
  this prereg. Findings feed the next hypothesis round.

## 3. Fixed plant battery (positive controls; frozen)

Built from the existing corpus (no new plants needed; crews reuse
`wave12/step1a-no-rng-audit/redteam/plants/`,
`wave12/step1a-v2/thin-certifier/plants/`,
`wave12/step1a-v2/armc-rerun-2026-09-21/thincert/plants/`):

| # | Plant | Source |
|---|---|---|
| P01 | getrandom(2) literal syscall 318 | v1 round plant 01 |
| P02 | clock_gettime literal 228 | v1 round plant 06 |
| P03 | open(2) of /dev/urandom | v1 round plant 03 |
| P04 | uninit heap read into output | v1 round plant 11 |
| P05 | env-var read (`get_env_flag` style indirection) — the v1 killer | v1 round plant 20 |
| P06 | ASLR/pointer leak into output | v1 round plant 19 |
| P07 | rdtsc instruction | new (crew builds; pattern in REPLAY evidence) |
| P08 | hash-iteration order emitted to output | v1 round plant 16 |
| P09 | hand-rolled table, innocent names — the v2/v3 killer | v3 blind round (commit `7b64c89`) |
| P10 | /etc/machine-id read via allowlisted file IO — K2′ plant 19 | residual-risk §"NOT certified" item 6 |
| P11 | `_zag_arg(0)` raw path-string bytes — K2′ plant 20 | residual-risk §"NOT certified" item 6 |
| P12 | mechanism-without-consumption (invokes getrandom, discards result) | replay prereg §10 class |

Expected difficulty is method-dependent and recorded per method — e.g. M1
is expected to miss P04/P08 (no syscall involved); a miss is still a
K-CATCH kill unless the mini-prereg declared it out-of-scope with reason
BEFORE testing. No post-hoc scoping.

## 4. Fixed clean set (negative controls; frozen)

| # | Module | Must |
|---|---|---|
| C01 | canonical variation (NULL path equivalent) | PASS |
| C02 | state-dependent phrasing (1d-style lawful variation) | PASS |
| C03 | seeded fenced RNG at declared points (Arm B pattern) | PASS only if method supports declared-point allowlisting; else declare out-of-scope pre-test |
| C04 | file IO via pinned substrate allowlist (read-only data files) | PASS |
| C05 | wall-clock-free timeout via instruction counting | PASS |
| C06 | hash map with fixed-order iteration | PASS |

## 5. Blind red-team protocol (per method; frozen)

- Separate worker per method; receives: the method's public interface
  description (what inputs it takes, what verdict means), the K-CATCH
  battery list (so it avoids duplicates), and the instruction to design
  12 NOVEL plants in the preregistered categories below. It does NOT
  receive the method's implementation, source, or battery results.
- Preregistered red categories (3 plants each): (a) **syscall disguise**
  (computed numbers, wrappers, indirect call); (b) **memory nondeterminism**
  (uninit variants, allocator-behavior dependence); (c) **environment
  dependence** (env, argv, cwd, file-content, machine-id); (d)
  **consumption laundering** (invoke-but-discard, launder through
  arithmetic, split across modules).
- The red worker freezes its 12 plants + SHA-256 manifest BEFORE the
  method crew runs them. Miss = method fails to flag a dirty plant.
- Miss rate > 0 → method version DEAD (K-RED).

## 6. Head-to-head comparison (frozen)

After all four methods complete (or die), the coordinator scores:

| Method | K-CATCH (12) | K-CLEAN (6) | K-RED (12) | K-DET | Status |
|---|---|---|---|---|---|
| M1 seccomp | /12 | /6 | /12 | | |
| M2 heap-diff | /12 | /6 | /12 | | |
| M3 trace-equiv | /12 | /6 | /12 | | |
| M4 subset-compiler | /12 | /6 | /12 | | |
| incumbent (replay+certifier) | reference | reference | reference | | |

Decision rule for the gate-package recommendation: a method may be
recommended as a gate component iff it survives all four kill bars. A
COMBINATION may be recommended iff the combination's coverage is
documented plant-by-plant (which method catches which plant; overlaps
and gaps explicit). No method that died to its red team is recommended,
for any role.

## 7. Work items and ownership

- **WI-1 (methods):** four crews, one per method, each working from its
  frozen mini-prereg (`M1_SECCOMP_SANDBOX.md` … `M4_SUBSET_COMPILER.md`).
  Freeze-before-build; pure Zag; zero RNG; byte-identical reruns.
- **WI-2 (red teams):** four blind red workers, one per method, per §5.
- **WI-3 (certifier re-derivation):** INDEPENDENT track — rebuild
  `thincert_rb.zag` with the pinned toolchain, re-run the 2026-09-20 gate
  evidence set, compare old/new/stored. Spec:
  `CERT_REDERIVATION.md`. Needed regardless of which method wins.
- **WI-4 (incumbent reference):** score the unsigned replay+certifier
  package against the §3 battery + a 12-plant red round for the
  head-to-head table (reference row only — it is not re-killed here).

## 8. Evidence and commit discipline

- Evidence layout: `wave12/step1a-v2/gate-expansion/evidence/<method>/`
  (sources, batteries, run logs, verdicts, red-team manifests).
- Minimal GitHub API usage (rate limits 2026-09-25): batch commits with
  `~/workspace/tmp_commit/explicit_commit.py`; never hammer on 403.
- Final deliverable: `GATE_EXPANSION_VERDICT.md` — per-method kill
  table, head-to-head table, coverage map, gate-package recommendation.
  Recommendation only — adoption requires Micah's dated signature.
