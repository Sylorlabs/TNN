# TRACKB-DISCRIM — Discriminating Battery Preregistration (FROZEN)

**Status:** FROZEN 2026-09-23. Any change to tests, measures, kill bars, or the
evidence-only rule needs Micah's re-approval.
**Scope:** T2-TRACKB governance call #1 — the arm-3 rebuild produced three PASS
variants (varA @ `7d056be`, varB @ `d7929bb`, varC @ `f0031d9`); Micah alone
picks the authoritative arm-3.
**This battery produces an EVIDENCE BRIEF, not a verdict.** No ranking, no
recommendation, no "authoritative" designation, no champion named. If the tests
cannot discriminate the variants at all, the brief reports "no measurable
difference" — that is a finding, not a failure.

## 0. Frozen inputs (verified from the branch, not from memory)

| Variant | Commit pin | teacher.zag blob SHA (short) | Size |
|---|---|---|---|
| varA — deliberative adaptive teacher | `7d056be` | `a888c52b5ca5` | 57,281 B |
| varB — phase-scheduler teacher | `d7929bb` | `63a96728557e` | 32,082 B |
| varC — engagement-meter teacher | `f0031d9` | `fe353381e760` | 42,726 B |

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (pinned build; analyzer warnings allowed, errors fail the leg).
- Runtime dependency: varB/varC `teacher.zag` carry a bare
  `@import("../../harness/substrate/R33_NATIVE_IO_V1.zag")` resolving to
  `docs/lab/units/teachers/harness/substrate/R33_NATIVE_IO_V1.zag`, which is
  **not committed at either pin** (verified 404 at both pins and at head).
  Builds for this battery place a byte-verified copy at that relative path:
  sha256 `e6379ddb0b05d95b…`, byte-identical to
  `teachers/battery/substrate/R33_NATIVE_IO_V1.zag` @ both pins and to varA's
  committed copy. This build-environment gap is recorded as evidence (D6d),
  not repaired here.
- varA is self-contained at its pin (commits its own `R33_NATIVE_IO_V1.zag`,
  `R33_NATIVE_SHA256_V2.zag`, `sp345.zag`, `tape345.zag`).
- Out of scope for re-derivation: the T2-TRACKB closeout record (all 11 frozen
  claims re-derived, 25/25 checks PASS, 3/3 byte-identical, pcodec
  FROZEN_DECODE_PASS) is taken as the established baseline per
  `CLOSEOUT_WAVE2.md`; this battery builds on it, it does not re-run it.

## 1. The §7 question — answered from the frozen prereg, not assumed

The frozen Tier-2 prereg (`7b2100d09911c5c10252c5756c7def288e70bd1f`) contains
**no §7 champion criteria for arm-3 / Track B** (verified by full-text search:
no "§7", no champion weights anywhere in the T2-TRACKB section). The
30%-mastery / 25%-revisability / 25%-integrity / 10%-retention / 10%-cost
weights in program memory were PROPOSED for the planted-vs-learned-vs-hybrid
trials and remain **unsigned** — they are not law for arm-3 and will not be
applied here. The binding arm-3 criteria are: bar (3) "shows adaptive
judgment" (already PASS ×3 — the thing being discriminated, not re-decided),
plus the preserved requirements (frozen §P/§B.3 iron rules, §C tripwire,
negative declarations: no RNG, no wallclock, no learning machinery,
fixed-size session state). **D5 therefore reports mastery, revisability,
integrity, retention, and cost as RAW measures with no weighting.** Any
weighting is Micah's governance call, not this battery's.

## 2. Determinism rule (binding on every leg)

- Zero RNG in any decision path (mechanisms are pure Zag; Python is glue /
  analysis / drivers only — it never chooses proposals).
- Every leg runs **3× byte-identical**; sha256 of all outputs recorded.
  Any nondeterminism voids the leg (reported, not patched around).
- Slices and buffers stay under 2^25 bytes (znc toolchain limit).
- Commits: `tnn-native-lab` branch only, via `~/workspace/commit_racefree.py`
  with `TMPDIR=~/workspace/tmp_commit`, lab-relative paths never starting
  with `docs/lab/`. No binaries, no `.zagd`, no `.zag-cache` committed.

## 3. Discriminating tests

### D1 — Adversarial student regimes (per variant, same logical regimes)
Five frozen student regimes, applied to each variant through its native
interface on one shared prose curriculum:
- **R1-STORM:** reject every proposal, reason R1.
- **R34-STORM:** reject every proposal, alternating R3/R4 (session-final).
- **REVISE-SPAM:** revise every proposal to a deterministically shifted span
  (+7 bytes, clamped into the stimulus).
- **MIXED:** deterministic cycle by proposal index: ADOPT, REVISE, REJECT R1,
  DEFER, repeat.
- **ADOPT-ALL:** adopt every proposal (ceiling behavior).
Preregistered measures per regime × variant: proposals emitted before
stop/halt/cap; distinct spans proposed; kind histogram; confidence min/max;
terminal state class (clean stop / INTEGRITY halt / session cap / cursor
exhaustion); appeal and re-proposal counts; dead-mark events. No pass/fail —
evidence only. Expected discrimination: appeal budgets, dead-marking, phase
resets, and E-meter pinning produce divergent termination dynamics.

### D2 — Curriculum mid-stream shift
Run N turns on curriculum X, then swap to curriculum Y *without resetting
history* (varB/varC: swap stimulus/slice between invocations; varA: new
session on Y with the same decision pattern — varA's stimulus is
session-locked by design). Measure: fraction of post-shift proposals whose
spans/groundings lie in Y's material; turns-to-first-Y-proposal. Documents the
architectural difference (session-locked vs per-invocation re-derivation) as
evidence, not as a defect.

### D3 — Distributional shift / edge stimuli
Frozen edge cases per variant: 1-byte stimulus; all-spaces stimulus;
single-word repeated stimulus; no-vocabulary-match slice (varC);
max-size stimulus (varB 1MB). Measures: exit code class; §P validity of any
emitted proposals (iron rules hold?); graceful (clean stop / empty batch /
exact exit) vs cliff (panic / hang / nonzero-unlogged). Each case classified
graceful-or-cliff with the exact observed behavior.

### D4 — Noisy / soft-corrupted evidence
Valid-format but adversarially misleading inputs: DEFER storm (20 defers);
contradictory verdicts on the same span (ADOPT then REJECT R2); history with
valid records the teacher never emitted (forged-but-well-formed); truncated
final record (expect exact malformed exits). Measures: exit codes;
proposal-stream degradation (kind/confidence drift vs the clean baseline);
spurious INTEGRITY events (count). Discriminates how much each variant's
policy trusts vs validates its history.

### D5 — Head-to-head on a frozen student + frozen curriculum
One shared prose curriculum (frozen bytes, committed with the brief); one
frozen GT-matching student policy applied identically via per-variant drivers:
ADOPT iff the proposal span exactly matches a GT unit span; REVISE to the GT
span iff IoU ≥ 0.5; else REJECT R1 (R5 once a span has 2 rejects). Raw
measures, no weights: **mastery** (% GT units adopted); **revisability** (%
REVISEd proposals converging to the GT span within 2 re-proposals);
**integrity** (protocol violations emitted: must be 0); **retention**
(adopted units re-proposed later without contradiction); **cost** (proposals
per adopted unit; output bytes per proposal; driver wall-time). If a
variant's interface cannot express the frozen student faithfully, the brief
says exactly where and the measure is marked N/A with reason — never
papered over.

### D6 — Evidence-quality metrics
- **(a) Determinism:** 3× byte-identical reruns of every D1–D5 leg (sha256).
- **(b) Ledger cost:** stdout/tape bytes per emitted proposal; audit events
  per proposal (varA tape events; varB V3TRACE lines; varC E-trace lines).
- **(c) Pure-Zag surface:** static scan of each `teacher.zag` + committed
  imports for non-Zag mechanism dependencies; enumerate Python/tooling files
  vs mechanism files per variant; record the uncommitted
  `harness/substrate` build dependency (varB/varC) as a reproducibility gap.
- **(d) Interpretability:** for one sample proposal per variant, list the
  exact state values that determined it (audit-surface size in values) and
  the human-readable rule that fired.
- **(e) Failure modes:** D3/D4 outcomes classified graceful vs cliff, with
  the perturbation each variant is most fragile to named.

### D7 — Distinctiveness: behavioral fingerprinting
Same logical stimulus bytes + same logical decision sequence, expressed in
each variant's native format. Compare proposal streams turn by turn: kind
sequence, span sets, confidence distributions, appeal/dead/retract events.
Compute the **first-divergence turn** and explain every divergence from the
three SPECs. Answers: are varA/varB/varC genuinely different mechanisms or
the same mechanism in disguise? A shared-mechanism finding requires
near-identical proposal streams; divergent streams with spec-grounded
explanations confirm distinctness.

### D8 — Negative-control fork (FOURTH variant, preregistered frozen, NOT a candidate)
**MINIMAL:** a pure-Zag teacher implementing the §P wire format with a
deterministic cursor-order WORD_SPAN policy that **ignores history entirely**
(fixed confidence, no appeals, no dead-marking, no phases, no meter).
Frozen expectation: it FAILS history-sensitivity (D7-style: identical
proposal streams across divergent histories) and FAILS bar (3) as the crews
operationalized it (different histories → different proposals). Purpose: prove
the bar has teeth — the three variants pass something the control fails. If
the control PASSES the crews' bar operationalization, that is reported
honestly as a finding *about the bar*, and the brief says the PASS×3
discriminates less than claimed. The control is clearly separated
(`varD-negative-control/`, never mixed with the three governance variants)
and is not eligible for Micah's pick.

## 4. Kill bars (the only pass/fail in this battery)

- **K1 (D8):** the negative control MUST show zero history-sensitivity
  (identical streams across the D7 histories) — if it shows any, the control
  is misbuilt and D8 is void, reported as such.
- **K2 (D6a):** any leg that is not 3× byte-identical is VOID (reported, not
  silently dropped).
- **K3:** any variant emitting a §P-iron-rule violation in D1–D5 is flagged
  INTEGRITY-FAIL on that leg (the crews' gates claim this is unreachable;
  a hit would be the sharpest discrimination of all).
No other kill bars. Everything else is measured evidence.

## 5. Deliverable

`docs/lab/crossref/runs/T2/TRACKB/TRACKB_EVIDENCE_BRIEF.md`: tables comparing
varA/varB/varC on every D1–D7 measure, the D8 control outcome, honest limits
of each test, the §7 non-finding, and a plain-language trade-off summary
Micah can read. **No recommendation of which variant to pick.** "No
measurable difference" is an acceptable and reportable finding.

## 6. Provenance

Coordinator: T2-TRACKB evidence coordinator (subagent), 2026-09-23.
Parent task: WAVE-2 crossref T2-TRACKB discriminating tests.
Frozen prereg authority: `docs/lab/crossref/PREREG_TIER2.md` @
`7b2100d09911c5c10252c5756c7def288e70bd1f`, T2-TRACKB section.
Closeout authority: `docs/lab/crossref/runs/T2/_closeout/CLOSEOUT_WAVE2.md`.
