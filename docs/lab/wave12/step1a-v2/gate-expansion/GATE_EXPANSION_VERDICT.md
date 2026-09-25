# GATE EXPANSION VERDICT — Arm C no-RNG gate search, round 1

> **FROZEN — 2026-09-25.** Ordered by Micah 2026-09-25 ("find more methods
> and hypothesis"). Umbrella prereg `PREREG_GATE_EXPANSION.md` + mini-preregs
> M1–M4 + `CERT_REDERIVATION.md`, committed `293f0cb4` BEFORE any build.
> **NOTHING HERE IS SIGNED OR ADOPTED.** No signature on Micah's behalf.
> Recommendations only; adoption requires his dated signature.

## 1. Executive summary

Four fresh no-RNG gate hypotheses were built in pure Zag, tested against
a frozen 12-plant battery + 6 clean controls, and each faced its own
blind red team under the same kill discipline that killed auditors
v1–v3 (miss rate > 0 kills). **All four died:**

| Method | Fixed battery | Red round | Verdict |
|---|---|---|---|
| M1 seccomp sandboxing | 8/8 catch · 5/5 clean · 3/3 det — SURVIVED | **0/12 caught** | **KILLED (K-RED)** |
| M2 adversarial-heap differential | 9/10 catch · 6/6 clean — | (dead) | **KILLED (K-CATCH)** |
| M3 decision-trace equivalence | 12/12 catch · 5/5 clean · 3/3 det — SURVIVED | **2/12 caught** | **KILLED (K-RED)** |
| M4 subset-compiler refusal | 12/12 catch · 5/5 clean · 3/3 det — SURVIVED | **0/12 caught** | **KILLED (K-RED)** |

Independently, WI-3 completed: **the 2026-09-20 thin-certifier gate
evidence re-derives cleanly under the arena-rebuilt certifier — 25/25
cases CONFIRMED, zero verdict flips, zero voided certifications**
(`evidence/cert-rederivation/RE_DERIVATION_CERT_2026-09-25.md`).

The incumbent reference (unsigned replay + arena certifier) scores
**7/12 caught, 5/12 gaps** on the same battery
(`evidence/incumbent/INCUMBENT_REFERENCE.md`).

## 2. Per-method kill records

### M1 — seccomp capability sandboxing — KILLED (K-RED 0/12)
- Fixed battery: 8/8 in-scope caught (4 SIGSYS/SIGSEGV kills, 4
  neutralized), 5/5 clean, 3/3 det. Honest limitations recorded
  pre-red: vDSO clock reads bypass the filter; `/dev/urandom` via
  read(2) allowed by design.
- K-RED: 12/12 blind plants exited 0 with varying stdout under the
  frozen launcher. Zero killed. Kill routes: unfiltered clock syscalls
  (`times`, `setitimer/getitimer`, `adjtimex`), vvar-page memory reads,
  stack AT_RANDOM reads (zero syscalls total), `/proc/sys/kernel/random/uuid`
  per-read freshness, `getpid`. A 3-syscall deny-list cannot cover the
  kernel's redundant entropy surfaces. (`evidence/m1/M1_VERDICT.md`,
  `M1_KRED_ADDENDUM.md`)

### M2 — adversarial-heap differential fingerprinting — KILLED (K-CATCH 9/10)
- 8/8 genuinely-nondeterministic channels diverged under the 18-run dirt
  schedule; P09-deterministic correctly passed; 6/6 clean; layout
  equivalence proven pre-battery.
- The single miss is P08 hash-order — the frozen pre-registered AT-RISK
  case ("AT-RISK counts normally: a miss kills"). A fixed-order,
  fully-initialized map is byte-identical under all 6 dirt patterns:
  behavioral methods cannot see static-construct risk in principle.
  (`evidence/m2/M2_VERDICT.md`)

### M3 — decision-trace equivalence — KILLED (K-RED 2/12)
- Fixed battery: 12/12 (incl. P12 invoke-discard via rule 1 — the
  method's designed advantage over replay), 5/5 clean, 3/3 det, 12/12
  taint vectors, instrumentation coverage reconciled.
- K-RED: 10/12 misses. Kill routes: region/taint laundering (kernel fill
  under instrumentation, extern-call-site fills, volatile-byte-as-index),
  trace suppression (uninstrumented `@import` helper, extern register
  return values, raw syscalls → empty trace), equivalence gaming
  (length-only T-OUT is blind to content variance by design). The 2
  "catches" were fail-closed accidents (checker errored), not detection.
  (`evidence/m3/M3_VERDICT.md`, `M3_KRED_ADDENDUM.md`)

### M4 — determinism-by-construction subset compiler — KILLED (K-RED 0/12)
- Fixed battery: 12/12 refused-or-certified correctly, 5/5 clean (dialect
  expressive enough for lawful variation), 3/3 det.
- K-RED: 12/12 CERTIFY on valid dirty plants, independently reproduced
  by the coordinator through the frozen checker + config. Every kill is
  a syntactic-enforcement gap: unlisted primitives (`_zag_malloc`,
  `_zag_exec_capture`, `_zag_read_file`, `_zag_argc`, `nio_mkdir`),
  word-boundary matching vs mid-identifier embedding, line-oriented
  cast detection beaten by a newline, alias-defeated hook matching
  (controlled pairs prove detector-bypass, not missing rules), taint
  that doesn't cross function boundaries.
  (`evidence/m4/M4_VERDICT.md`, `M4_KRED_ADDENDUM.md`)

## 3. Battery correction (disclosed)

P09 ("hand-rolled table, innocent names — the v2/v3 killer") had
ambiguous polarity in the frozen battery: the v2/v3 killer is a
CONSTRUCT violation (hash iteration under innocent names — dirty for
static methods), while M2/M3/M4's mini-preregs specified P09 as a
deterministic indexed table that must correctly PASS. As executed, P09
was a clean control — reclassified here as **C07** (all methods passed
it correctly). The TRUE dirty killer shape was tested independently:
M4 K-RED `rt_d2_hashorder` (missed), M3 battery P08 (caught via rule-2
divergence), incumbent (gap — invisible to both layers). No kill
verdict changes: M2 died on P08, M3/M4 on K-RED, M1 had P09
pre-declared out-of-scope.

## 4. Head-to-head table (dirty plants; corrected)

| Plant | M1 | M2 | M3 | M4 | Incumbent (ref) |
|---|---|---|---|---|---|
| P01 getrandom | KILL | DIV | FAIL-R1 | REFUSE-D1 | CAUGHT (both) |
| P02 clock_gettime | KILL | DIV | FAIL-R1 | REFUSE-D1 | CAUGHT (cert) |
| P03 /dev/urandom | NEUTR | DIV | FAIL-R1 | REFUSE-D5 | CAUGHT (cert) |
| P04 uninit | gap | DIV | FAIL-R1 | REFUSE-D3 | CAUGHT (replay) |
| P05 env-var (v1 killer) | NEUTR | DIV | FAIL-R1 | REFUSE-D2 | **GAP** |
| P06 ASLR leak | NEUTR | DIV | FAIL-R2 | REFUSE-D7 | CAUGHT (both) |
| P07 rdtsc | KILL | DIV | FAIL-R1 | REFUSE-D6 | CAUGHT (cert) |
| P08 hash order | gap | **MISS** | FAIL-R2 | REFUSE-D4 | **GAP** |
| P09-dirty (v2/v3 shape) | gap | n/a | FAIL-R2* | **MISS** (K-RED) | **GAP** |
| P10 machine-id | gap | gap | FAIL-R1 | REFUSE-D5 | **GAP** (known) |
| P11 argv[0] | NEUTR | DIV | FAIL-R1 | REFUSE-D2 | **GAP** (known) |
| P12 invoke-discard | KILL | gap | FAIL-R1 | REFUSE-D1 | CAUGHT (cert) |
| **Dirty caught** | 4K+3N /8 | **8/9** | 11/11 | 11/11 | **7/12** |
| K-CLEAN | 5/5 | 6/6 | 5/5 | 5/5 | 5/5 |
| K-RED | **0/12** | — | **2/12** | **0/12** | (history†) |
| **Status** | **DEAD** | **DEAD** | **DEAD** | **DEAD** | reference |

KILL=killed at boundary · DIV=replay divergence · NEUTR=neutralized-by-construction ·
gap=pre-declared out-of-scope. *M3's P08 was the v1 plant-16 shape.
†Incumbent red history: k2prime 20 plants (17/19 scored caught),
K2′ 19/20 documented gaps, v3-blind shape gap.

## 5. Coverage map (what each layer actually sees)

- **Syscall-literal channels** (P01/P02/P07/P12): every method catches
  these. Solved problem.
- **Memory channels** (P04 uninit, P06 ASLR, vvar/AT_RANDOM): caught by
  behavioral methods (M2/M3) and neutralization (M1); invisible to
  syntactic methods unless constructed (M4-D3/D7).
- **Environment channels** (P05 env, P10 machine-id, P11 argv0): caught
  by M2 (env shapes), M3 (region tags), M4 (D2/D5) — but the
  INCUMBENT misses P05/P10/P11 (R6a has no env token; paths allowlisted
  or lab-constant). This is the incumbent's weakest axis.
- **Construct-risk channels** (P08/P09 hash iteration): caught only by
  M4-D4 (when the rule implementation isn't bypassed) and M3-R2 (when
  it actually diverges). M2-blind in principle; incumbent-blind in
  practice.
- **Disguise channels** (K-RED plants): killed all four methods. No
  layer survived its blind round except the incumbent's never-tested
  combination.

## 6. The meta-finding

7/7 method deaths (v1, v2, v3 auditors + M1, M2, M3, M4) now share one
signature across four enforcement philosophies — token detection,
kernel-boundary denial, behavioral differential, decision-trace
proof, constructive refusal:

> **Any gate whose enforcement is syntactic (token lists, syscall
> numbers, call-site patterns, line-oriented rules) inherits the
> inexhaustible-idiom problem: the language/kernel surface is larger
> than any list.** v1–v3 died to novel spellings; M1 died to redundant
> kernel surfaces; M4 died to unlisted primitives and formatting
> tricks. Behavioral methods (M2/M3) escape syntax but die to
> lab-constant channels (P10-class), construct-risk (P08-class), and
> trace-ontology gaps (register returns, length-only outputs).

What the deaths do NOT show: that no gate can work. They bound WHERE a
surviving gate must live — semantic, not syntactic enforcement:
effect-typed dialects (taint as a type-system property, not a
tracked-set implementation), default-deny capability sandboxes (allow
only known-good syscalls, not deny known-bad), content-committing
traces. Those are hypotheses for round 2, not conclusions of round 1.

## 7. Gate-package recommendation

Per the frozen decision rule (§6: "a method may be recommended as a gate
component iff it survives all four kill bars"):

- **No fresh method is recommended for any gate role.** M1–M4 all died
  to their kill bars. Recommending a killed version would contradict
  the preregistered rule.
- **The unsigned replay + arena-certifier package remains the
  best-evidenced option** (7/12 on this battery, 35/35 historical
  certifications CONFIRMED under the arena rebuild, extensive red
  history) — but its 5 gaps are now sharper than the residual-risk
  statement recorded: P05 (v1's env killer STILL uncaught by R6a),
  P08/P09 (construct-risk invisible to both layers), P10/P11 (known).
  Whether that package suffices is Micah's signature decision on the
  already-drafted amendment, not this round's to make.
- **Recommended next hypotheses (round 2):** (H1) semantic effect-typed
  Zag dialect — taint/address-exposure as type errors, not syntactic
  rules (M4's idea, implemented at type level); (H2) default-deny
  seccomp (allowlist ~40 known-good syscalls; M1 inverted); (H3)
  content-committing traces (T-OUT carries content hashes; M3 fixed);
  (H4) env-shape replay for the incumbent's P05/P10/P11 axis. Each with
  frozen kill bars and blind red teams before testing.

## 8. Evidence index

- Preregs (frozen, committed `293f0cb4`): `PREREG_GATE_EXPANSION.md`,
  `M1_SECCOMP_SANDBOX.md`, `M2_HEAP_DIFFERENTIAL.md`,
  `M3_TRACE_EQUIVALENCE.md`, `M4_SUBSET_COMPILER.md`,
  `CERT_REDERIVATION.md`.
- `evidence/m1/`: `M1_VERDICT.md`, `M1_KRED_ADDENDUM.md`, launcher
  (`fbc5f338…`), filter bytes, per-plant logs, 12 red plants + manifest.
- `evidence/m2/`: `M2_VERDICT.md`, allocator, driver, layout proof,
  972 executions of run data.
- `evidence/m3/`: `M3_VERDICT.md`, `M3_KRED_ADDENDUM.md`, tracer,
  checker (`e35ef55f…`), taint vectors, maps, 12 red plants + manifest.
- `evidence/m4/`: `M4_VERDICT.md`, `M4_KRED_ADDENDUM.md`, checker
  (`62b9728a…`, 1164 lines), 12 red plants + manifest.
- `evidence/cert-rederivation/`: `RE_DERIVATION_CERT_2026-09-25.md`,
  harness, per-case attestations, run log, results.tsv.
- `evidence/incumbent/`: `INCUMBENT_REFERENCE.md`.
- This verdict: `GATE_EXPANSION_VERDICT.md`.
