# RESULTS — INT-1 C5 Redesign S10 Re-run (2026-09-20)

Amendment: `AMENDMENT_2026-09-20-C5-REDESIGN.md` (committed pre-run as `adb1ef9f`).
Implementer: subagent INT-1. Rule applied as law: implement exactly what the
amendment specifies, nothing more, nothing less. Zero RNG. Native Zag trial.

## Headline verdict

- **C5 mechanism: WORKS.** The default verdict gate fires on REFUTED-backed
  composes; the killed-only arm achieves 0 composites; the instrument fires on
  its gate-less variant and stays silent on the intact system (calibration
  passes both directions).
- **Amendment §4 (C5 bar): HOLDS.**
- **Amendment §5 (capability non-regression): FAILS on C7.** C7 reads
  914→897 against the binding bar of 897→897; the `c7_withdrawal` check fires.
  Every other §5 element passes (C1/C2/C3/C4/C6 ALIVE, six stage gates PASS,
  P1–P10 clear, `composites_ok` 0% below the repaired-S10 baseline).
- **Amendment §9 (S100 gate): S100 STAYS GATED.** Condition (3) fails; the
  independent checker independently returns FAIL on the same two C7 items.
  Per §9/§10, no re-repair of the fired control without a new dated amendment.

The C7 firing is a **metric-proxy artifact of the amendment-mandated L1 wiring**,
not teacher-dependence (details below). It is reported as a FAIL because the bar
is explicit and binding — no spin, no softening.

## What was implemented (amendment §1–§3, §7)

- `impl/seam.zag`: `c5_strict` retired (field removed). `c5_arm` retained; the
  arm filter runs FIRST. New unconditional default gate: any compose whose
  backing claim (`claim_cid > 0`) resolves `O2_V_REFUTED` at compose time is
  refused with `SEAM_REFUSED_PARTITION`, ledgered
  (`LG_O4`/`LG_OP_COMPOSE`, `b1=need_id`, `a1=claim_cid`), `trace.*=-1`.
  `claim_cid <= 0` (claim-less composes) are permitted and ledgered with
  `a1==0`. Non-anchor input traces remain unchecked — documented as a residual
  in code comments and §6 below.
- `impl/loop.zag`: the compose caller treats `SEAM_REFUSED_PARTITION` on the
  default path (`c5_arm==0`) as abstain — it feeds L1 via the real
  `seam4_abstain` path (abstain → hypothesis). In test arms the refusals are
  arm-filter artifacts, so they keep silent semantics there; routing them to L1
  would clobber the anchor's backing claim and starve the very arms the C5
  instrument measures (found during calibration — see below).
- `impl/controls.zag`: C4 bite rewritten through `seam4_compose` (the four
  direct `o4_compose` calls are gone). C5 arms reworked to the binding bar
  (accepted/candidate require ≥1 composite; killed requires 0). C5 bite is now
  a real synthetic test through the default path (10/10 REFUTED-backed composes
  refused; CONFIRMED/OPEN/claim-less flow; refusal ledger `a1` verified).
  In-binary G0b scanner added.
- `impl/main.zag`: `CHECK,g0b_compose_callsite`; per-stage `COMPOSITES` telemetry.
- `impl/analyze_s10.sh`: pre-build whole-tree G0b shell gate; runs the binary
  from the source dir so static gates resolve.
- `impl/check_c5redesign.py`: independent checker (re-derives stage/control/
  probe verdicts, C7, composite delta, determinism, rebuild hash, zero RNG, G0b,
  defended-channel telemetry).

G0b (amendment §7): exactly **one** `o4_compose` call site in the source tree,
inside `seam4_compose` (`seam.zag:380`). Build gate passes (shell pre-gate and
in-binary gate agree).

## Calibration (battery-amendment §11 precedent)

Gate-less variant (default gate excised, everything else identical):

| check | broken variant | intact system |
|---|---|---|
| `cbite_c5` (synthetic REFUTED bite) | **1 — FIRES** | 0 — silent |
| `c5_lesion` (killed-only arm) | **1 — LEAKAGE** | 0 — silent |
| all other controls/gates/bites | 0 — silent | 0 — silent |

The instrument fires on broken and stays silent on intact. During calibration a
first wiring attempt (routing ALL partition refusals to L1, including in test
arms) starved the killed-only arm — the arm-filter refusals clobbered the
anchor's backing claim, so the arm measured 0 even without the gate. Scoping the
L1 feed to the default path (`c5_arm==0`) restored discrimination; the arms are
measurement harnesses, the default path is the shipped behavior. The final
wiring is what ran in the trial below.

## Full S10 re-run (amendment §8)

- Six stages (DC-0…DC-5), paired runs, **byte-identical 6/6**.
- All six `stage_gate` checks PASS. All stage exits 0.
- Zero RNG: `g0_rng` 0,0; comment-stripped source scan finds no RNG in trial
  sources; rebuild is byte-identical
  (`e673bae2c889b117db7656a4b77c11c4974bf6cd4823f05c50b806894c25acf0`).
- Defended-channel telemetry present; `l5_static`, `g1_lineage`, `g2_paired`,
  `g4_sound`, `g5_novelty` all clear.

### Composition (§5 bar)

Baseline (repaired sources @ `5aa2fb13` + behavior-neutral telemetry print,
built and run independently): `composites_ok` = **1024** (DC-2…DC-5: 256 each;
DC-0/DC-1: 0 — composition is not yet online there).

Redesigned run: `composites_ok` = **1024**. Drop vs baseline: **0.00%**
(bar: ≤5%). **PASS.**

The gate is not destructive: it refused compose attempts whose backing claim
was REFUTED at compose time (visible as +17 L1 abstains in each of DC-2/3/4,
+0 in DC-5 — exactly the stages where the operational-leakage analysis found
leaks), and each refusal fed a hypothesis per §3. Composition volume is fully
preserved because the compose budget is need-limited, not episode-limited.

### Controls (seven)

| control | result |
|---|---|
| C1 agency | ALIVE (0,0) |
| C2 composition | ALIVE (0,0) |
| C3 provenance | ALIVE (0,0) |
| C4 structure | ALIVE (0,0) |
| **C5 lesion** | **ALIVE (0,0)** — killed-only arm 0 composites; accepted/candidate ≥1 |
| C6 null | ALIVE (0,0) |
| C7 withdrawal | **FIRED (1,0)** — 914→897 vs bar 897→897 |

### Probes and bites

- P1–P10: all 10 clear (0,0). `pbite`: 10/10 pass.
- `cbite`: 7/7 silent (0,0), including the real `cbite_c5` (10/10 synthetic
  REFUTED-backed composes refused through the default path; CONFIRMED, OPEN,
  and claim-less composes flow; refusal ledger `a1` verified per case).

## The C7 finding — reported as FAIL, mechanism understood

C7 telemetry (intact): `cap4,914,cap5,897` (repaired baseline: `897,897`).

Root cause, deterministic and isolated:

1. The §3 wiring is working as specified: 51 default-path refusals across the
   run (17 each in DC-2/3/4, 0 in DC-5) each fed L1 → 17 extra hypotheses per
   affected stage (`L1COVER` abstains/opened: DC-2 12→29, DC-3 0→17, DC-4 0→17).
2. The corrigendum-§7 capability metric counts `tr.l1_opened`. DC-4's 17 extra
   hypotheses therefore raise `cap4` from 897 to **914**. DC-5 had no refusals,
   so `cap5` stays **897**.
3. The C7 check `cap5 < cap4` (897 < 914) fires.

This is **not teacher-dependence**:

- DC-5 absolute capability (897) is **identical** to the repaired run — the
  teacher-withdrawn arm lost nothing.
- The C7 instrument itself discriminates: on the gate-less variant (where C7 did
  not fire early) the positive control collapsed 897→641 as required.
- The +17 in DC-4 is the amendment-mandated mechanism operating as specified,
  not a capability regression. Nothing was killed to save C5 (`composites_ok`
  drop 0%).

The conflict: **§3 (refusals feed L1 → hypothesis) and §5's literal C7 bar
(897→897) are jointly unsatisfiable** under the corrigendum-§7 metric, because
the mandated hypotheses necessarily increment the metric in stages where the
gate fires. The council could not have intended a bar that the mandated
mechanism cannot satisfy, but the bar is explicit and binding, §10 forbids
softening it, and §9 says any failure keeps S100 gated. So: **§5 FAILS on C7,
S100 stays gated.** No re-repair was attempted.

What would un-gate S100 (requires a new dated amendment with Micah's
re-approval — NOT done here):

- (a) C7 compares the teacher-withdrawn arm against the repaired baseline
  (DC-5 ≥ 897) rather than against DC-4; or
- (b) the C7 comparison excludes refusal-fed L1 hypotheses (telemetry still
  counts them); or
- (c) the C7 bar is re-baselined to 914→897 with documented rationale.

## Residuals (amendment §6, plus implementation notes)

1. **Non-anchor input traces unchecked.** The gate verifies the anchor slot's
   backing claim only. A hostile non-anchor input trace is not verdict-checked.
   Documented in `seam4_compose` comments. Future probe: input-trace verdict
   audit once the seam can list compose inputs.
2. **O2-error amplification.** A wrongly-REFUTED claim's content is permanently
   unusable through the compose path — no appeal path exists. This is the
   architecture's terminal REFUTE made consistent, not a cost introduced by the
   gate. Fix requires a separate O2 appeal/re-adjudication redesign (out of
   scope).
3. **Verdict-flap races.** A claim CONFIRMED at scan but REFUTED at compose (or
   reverse) yields refusal/abstain; the ledger records the verdict read at
   compose time, so flaps are visible in audit. Deterministic given ledger state.
4. **Claim-less composes permitted** (`claim_cid <= 0` → `a1==0` ledgered). The
   gate covers claim-backed composition; claim-less flow is by design
   (§2: "permit and ledger claim_cid <= 0").

## §9 S100 gate — itemized

1. C5 bar §4 holds — **YES** (killed 0; arms 1/2 ≥1; bite 10/10; calibration
   fires-on-broken/silent-on-intact).
2. Positive controls fire — **YES** (`cbite_c5` on broken variant; C7 positive
   control 897→641 on the gate-less variant; C7 positive control did not execute
   in the intact run because `c7_run` returns early on `cap5<cap4`).
3. Capability non-regression §5 holds — **NO** (C7 914→897 vs 897→897).
4. Paired reruns byte-identical — **YES** (6/6).
5. Zero RNG in trial sources — **YES**.
6. Independent checker passes — **NO** (FAIL on the two C7 items; all 12 other
   checks pass).

**S100 stays gated.** No further re-repair without a new dated amendment.

## Artifacts

- This document: `RESULTS_S10_C5REDESIGN.md`.
- Evidence (small summaries; full logs were ephemeral, hashes recorded):
  `evidence_s10_c5redesign/`.
- Changed sources: `impl/seam.zag`, `impl/loop.zag`, `impl/controls.zag`,
  `impl/main.zag`, `impl/analyze_s10.sh`; new: `impl/check_c5redesign.py`.
- Build: `znc_linux_x86_64_abed8aa1`; binary SHA256
  `e673bae2c889b117db7656a4b77c11c4974bf6cd4823f05c50b806894c25acf0`
  (byte-identical rebuild verified by the independent checker).
- Calibration logs: broken-variant `cbite`/`controls` (fired); intact
  `cbite_c5` silent. Broken-variant sources were derived by excising only the
  default gate; they were never committed.
