# Consciousness-Trace Coverage Map

**Date:** 2026-09-27 (overnight wave)
**Ordered by:** Micah's law — "TNN is conscious every step of the way as needed"
**Question:** for every adopted mechanism's decision points — (a) does a trace exist? (b) is it *causally consulted* (blanking it at the read site changes the outcome)? A trace that is written but never read is decoration; a decision with no trace is dark.
**Scope:** map only. No fixes. Committed sources at `origin/tnn-native-lab @ 5b661730da`; evidence from the 2026-09-27 decoration-audit sector reports (neuter probes at `6b23696fc`) plus targeted read-site analysis on the current head. Recall-harm trace causality is independently audited by its own line — referenced, not duplicated.

## Verdicts

| Verdict | Meaning |
|---|---|
| COVERED | A decision trace exists AND is causally consulted (neuter/blank at the read site changes outcomes, or equivalent causal proof) |
| DARK | No trace exists at the decision point |
| DECORATIVE | A trace is written but nothing on any decision path reads it |
| ADJUDICATED | Honestly scoped as audit instrumentation / correctly closed — not a live claim |
| PENDING | Mechanism not yet built or adopted; mapped as a requirement, not a verdict |

**Target bar (program's own):** grow-with-me prereg H7/G7 (`docs/lab/growwithme/PREREG.md:51-53,165`) — *"Every consolidation/promotion/strengthening decision is an explicit white-box deliberation with a trace, and every trace is causally consulted (proven by intervention, not asserted)"*; *"100% of promotion/strengthening decisions carry traces AND intervention audit on all traces: 0 decorative. Any decorative trace → H7 KILLED."* Nothing below is graded against H7 retroactively — it is the bar the program set for itself going forward.

---

## 1. Dialogue round-4 (adopted: `docs/lab/dialogue/round4/ADOPTED.md`, commit `fb4961d96`)

The seven adopted components are causally genuine mechanisms (neuter-proven, decoration audit §3). The trace story is separate from the mechanism story:

| Decision point | Trace exists? | Causally consulted? | Verdict | Evidence |
|---|---|---|---|---|
| G6 untaught-predicate gate (withhold/answer) | No (live binary) | — | **DARK** | `tr_predmm_note` etc. are empty no-op stubs in the control binary (`dialogue.zag:3009-3020`); `trb` written L382–383, zero read sites |
| G7 role-order gate | No (live binary) | — | **DARK** | Same stubs; no decision record |
| Unified entity scanner | No (live binary) | — | **DARK** | Same |
| Correction-state mirror | No (live binary) | — | **DARK** | Same |
| Scoped deletion | No (live binary) | — | **DARK** | Same |
| Taught-fact units | No (live binary) | — | **DARK** | Same |
| Non-repeating requests/jokes | No (live binary) | — | **DARK** | Same |
| Trace-binary dispatch logs (`add_hooks.py` build) | Yes (emit-only) | No — write-only, no read site | **DECORATIVE** | Sector probe: all five note fns empty in control; `trb` write-only. ADOPTED.md Residuals explicitly scopes: *"Traces remain execution/dispatch logs, not native deliberative reasoning — owned by the genuine-deliberation workstream."* |

**Net:** the adopted dialogue machinery makes seven classes of decisions with **zero live decision traces**. The mechanisms are genuine; the trace coverage is dark. This is the program's user-facing surface — every answer/withhold it gives has no consulted record of why.

## 2. Deliberation line (`docs/lab/dialogue/deliberation/deliberate.zag`)

| Decision point | Trace exists? | Causally consulted? | Verdict | Evidence |
|---|---|---|---|---|
| Kind-0 readings / bids / flags (working ledger state) | Yes (ledger rows) | Yes — all 10 kind-0 rows branch-read in GEN fire conditions; neuter-10 signature verified | **COVERED** | Sector spot-verification: read sites L3344–L4202; NEUTER10_WHITEBOX.md; REDTEAM4 |
| Emitted decision records (READ/FACT/CAND/FACTARGMAX/ARGMAX/CLOSE/CONTENDER/REVIEW via `tr_pr`) | Yes (rich: winner, margins, citations) | No — `tr_pr` is emit-only; zero read-back sites (`tr_get`/`trace_get`/`read_trace`: no hits) | **DECORATIVE** | `deliberate.zag:2833` (`tr_pr` def), :4506–4538; correctly scoped as instrumentation, but the records are decision-shaped and readerless |
| REVIEW record specifically | Yes | No — emission is flag-gated (genuine mechanism), the record itself is never read | **DECORATIVE** | :4532–4538: gated on reading ledger slot 13812 back; `tr_pr("REVIEW…")` emit-only |
| phash CONTENT binding | Yes (emitted) | No — runtime never recomputes/compares | **DECORATIVE** | Sector report: L2686 comment claims ACT "verifies phash" but code only *emits*; verification was external (red-team replay). ADJUDICATED as audit instrument per the integrity-attribution law — but the comment is false |
| `tr_phash` helper | No (defined, never called) | — | **DARK** | :2844 dead helper |

**Net:** the deliberation line has the richest decision records in the program and **no reader for any of them**. The working state is covered; everything emitted is decorative-by-absence-of-consumer. The native-epistemics line (building on this machinery) is the natural consumer — currently it is not one.

## 3. One-brain v3 (`docs/lab/onebrain3/impl/onebrain_v3.zag`, commit `51b7de35d`)

| Decision point | Trace exists? | Causally consulted? | Verdict | Evidence |
|---|---|---|---|---|
| Shared ledger (fork bids, subpass/audit verdicts, reintegration inputs) | Yes | Yes — FORK_ASSESS neuter: 11 winner deltas; subpass/audit neuters: 11/11 each; reintegration reads bids (rows 13–24), score@24, fact support, branch winners @52/60, audit history | **COVERED** | REDTEAM3 Attacks 1–2; read sites `:1351–1352, :1445–1446` |
| Branch-margin records (`branch_snapshot` :1314–1315) | Yes (written + printed in BRANCH_SNAP) | No — zero read sites; PREREG3 §5 pins margins as reintegration inputs but only winners are read | **DECORATIVE** (minor) | Exhaustive read-site audit of the 2035-line source |
| close_call / emit_verdict metadata | Yes | No — never read by decision logic | **DECORATIVE** | :1781–1900; adjudicated as designed instrumentation |
| Committed trace files (`traces/v6_*_r{1,2,3}.txt`) | Yes | No — read only by post-hoc `score3.py` | **DECORATIVE** (as decision traces) | REDTEAM3.md:31 |

**Net:** the ledger-as-trace is the program's best-covered decision trace (neuter-proven at every stage). Everything written *about* the decision post-hoc is readerless.

## 4. Epistemic engines

| Decision point | Trace exists? | Causally consulted? | Verdict | Evidence |
|---|---|---|---|---|
| Scale attempts 1–3 (rigid pipeline) | — | — | **ADJUDICATED** | All three killed by their own bars; no live decision points |
| Native line (`docs/lab/epistemic_native/`, prereg `bbaa88099`) | Prereg only — Phase 1 in progress | — | **PENDING** | Prereg §6.4 bans crew-built comparators (correct posture). **Gap:** K3 (trace-ledger bijection) is a *structural* audit — an independent parser checks the READ→CAND→ELIM→ARGMAX→CONTENT chain exists. K1 explicitly calls trace emission order "cosmetic." **No bar requires traces to be causally consulted.** The prereg polices trace *shape*, not trace *causality*. |

**Net:** the line being built to answer Micah's "shouldn't the architecture do this natively" question has no causal-consultation bar for its traces. That is a prereg gap, not an implementation finding.

## 5. Chunker (`docs/lab/mg_chunking_batteryfix/intake.zag`)

| Decision point | Trace exists? | Causally consulted? | Verdict | Evidence |
|---|---|---|---|---|
| INTAKE choice (classify→policy→execute) | No why-trace; the choice dispatches (genuine mechanism) | The choice is consulted; *why* it was chosen is recorded nowhere readable | **DARK** | `policy_winner()` routes by class (57/57); no decision-why record |
| `policy_why` / `cand_why` prose | Yes (printed on INTAKE line) | No — assembled into output buffers (`ob_raw`), never read by a decision | **DECORATIVE** | :915–916, :2175–2249; crew-authored fixed prose (honestly disclosed) |
| Zoom traces (`zlog`) | Yes (emission) | No downstream reader | **DECORATIVE** | Adjudicated as audit-trail by design |
| `tnn_bind_*` registry (bindings as placement-decision records) | Bindings consulted (noseed 26/26→16/26) | The *placement decisions* (why this binding) live only in KNOW-SEED comments | **DARK** (placement-why) | CONTROL_BOUNDARY.md: agency gap honestly listed as "not present" |

## 6. Upscale (`docs/lab/image_upscale/`)

| Decision point | Trace exists? | Causally consulted? | Verdict | Evidence |
|---|---|---|---|---|
| Render-operator choice (Bresenham/bicubic/blend) | No — no TNN decision exists; crew chose | — | **DARK** (no decision point) | Generation audit; round 2 killed (`99b5ce6e9`) |
| general_ops directed choice (goal→op) | Choice drives execution (genuine) | The choice is consulted; `OPS_TRACE.txt` is write-only | **DECORATIVE** (trace file) | `azops.zag:6-7` (outdir trace), :54–68 |

## 7. Audio planner (`docs/lab/audio_longhorizon/desynth/src/plan_main_desynth.zag`)

| Decision point | Trace exists? | Causally consulted? | Verdict | Evidence |
|---|---|---|---|---|
| Action selection (consult vs grow) | Yes — 16-entry history ring, 88-byte entries (`hist_store` :530–542) | Yes — `hist_consult` (:546+) → `if (ci >= 0) { fcur = clamp_f0(f0h + cdelta); }` (:1268): blanking the ring changes the planned f0 | **COVERED** | :1246–1268; the ring is a genuine consulted decision trace |
| Printed journal (HEARD/CONSULTED/PLANNED/DELIBERATED lines) | Yes (stdout) | No — `_zag_print` emit-only | **DECORATIVE** | :804–1559 passim |
| Vocab growth decisions | Via the ring + DELIBERATED lines | Ring consulted; lines emit-only | **COVERED** (ring) / **DECORATIVE** (lines) | R3 growth path :798–969 |

**Caveat (honest scoping, in-source):** fresh mode resets vocabulary+history per target (`:1128–1129` — "no cross-target learning"); the ring's coverage holds in deep mode. Not a finding — a documented boundary.

## 8. Memory / strength / promotion

| Decision point | Trace exists? | Causally consulted? | Verdict | Evidence |
|---|---|---|---|---|
| Destroy/overwrite strong memory (price set + exacted) | Price computed and consulted live (8 probes: P1=109 refused, P2=0, P3=109, P4c=0) | Yes — but **no trace of the pricing decision is emitted at all** (zero `trace`/`_zag_print` in `strength_core.zag`): which weights fired, which reason code, what price — recorded nowhere | **DARK** (decision-why) | `strength-destruction-pricing-adoption/src/strength_core.zag`; memory sector P1–P8 probes |
| High-water epoch record (past strength decisions) | Yes | Yes — consulted at overwrite (P3: weaken does not discount) | **COVERED** (as state) | :504–534 `st_epoch_highwater` |
| Promotion/demotion tier flag | Yes (written, logged, snapshotted, fingerprinted) | No — zero read sites on any decision path; no `if(tier…)` anywhere | **DECORATIVE** | :1513–1545; the flagship case: a consolidation-class decision with a record nobody reads |
| Felt intensity → strengthen/weaken/retention | Yes (intensity value) | Yes — `felt_read` drives `st_weaken`/`st_strengthen`/triage targets | **COVERED** | `decides_trial.zag:364–366, 855–907` (crew-weights authorship caveat stands — coverage, not authorship, is what's mapped here) |
| Force-pin | Yes (pin record) | Yes — role gate + `forcepin==1` → refuse path | **COVERED** | :1432–1450 |
| memory_org scheme choice | Choice consulted (filing → +0.0688 recall) | The *rationale strings* are output-only (`concat` :907–915) | **COVERED** (choice) / **DECORATIVE** (rationale) | `lib.zag:769+`; VERDICT_MORG.md caveats |
| Self-PAM gate | Built, smoke-tested | No live callers — no live decision point | **DARK** (unwired) | Zero callers of `sp_init`/`admit_claim` outside own drivers — OPEN per audit |
| Ledger/checker/provenance/audit plumbing | Yes | Designed zero-behavior | **ADJUDICATED** | Integrity-attribution law: proves cheating after the fact, doesn't decide |

## 9. Recall-harm line

Independently auditing trace causality for recall (candidate-not-reflex architecture) — **not duplicated here**. Its verdict feeds the same H7 bar when it lands.

---

## Coverage summary

| Line | COVERED | DARK | DECORATIVE |
|---|---|---|---|
| Dialogue round-4 | 0 | 7 decision points | 1 (trace-binary logs) |
| Deliberation | 1 (ledger working state) | 1 (`tr_phash`) | 3 (tr_pr records, REVIEW, phash) |
| One-brain v3 | 1 (shared ledger) | 0 | 3 (margins, close-call meta, trace files) |
| Epistemics | 0 | 0 | 0 — PENDING (+1 prereg gap) |
| Chunker | 0 | 2 (INTAKE why, binding placement-why) | 2 (why-prose, zlog) |
| Upscale | 0 | 1 (no decision point yet) | 1 (OPS_TRACE.txt) |
| Audio planner | 2 (history ring, growth via ring) | 0 | 1 (printed journal) |
| Memory/strength | 4 (HW epoch, felt intensity, force-pin, org choice) | 2 (pricing-why, Self-PAM unwired) | 3 (tier flag, org rationale, —) |

The pattern: **mechanisms are covered; traces are not.** Wherever a decision is made by live state (ledger, ring, epoch, intensity), the state is causally consulted — TNN's decisions *run on* consulted records. Wherever a *record of the decision* is emitted for later, nothing reads it. Micah's law is half-satisfied: TNN decides with consulted state, but it leaves almost no consulted trace of *why*.

## Prioritized gaps (by decision importance)

**P0 — load-bearing decisions with no consulted why-trace:**
1. **Strength pricing decision (DARK).** The most consequential decision in the program (destroy/overwrite a strong memory) consults the price live but records nothing about why — no weights-fired, no reason-code, no price record. A post-hoc auditor cannot reconstruct the decision. (The cite/justify plumbing is adjudicated; the *pricing decision itself* is untraced.)
2. **Promotion/demotion tier (DECORATIVE).** A consolidation-class decision whose record is read by nothing. Cannot be called consolidation until tier affects retention/recall — and H7 explicitly kills on exactly this.

**P1 — user-facing and structural:**
3. **Dialogue round-4: seven decision points, zero live traces (DARK).** Every answer/withhold TNN gives has no consulted record of which gate fired or what it saw. The trace binary's logs are write-only.
4. **Deliberation emitted records (DECORATIVE).** ARGMAX/CLOSE/REVIEW/phash records exist and are decision-shaped — they need a reader, not a rewrite. The native-epistemics line is the natural consumer.
5. **Epistemic native prereg gap (PENDING).** K3 polices trace shape; nothing polices trace causality. Add an H7-style intervention bar before Phase-2/adoption.

**P2 — convert-or-delete:**
6. **One-brain branch margins (DECORATIVE, minor).** Consume in `reint_better` or delete (already on the decoration fix-or-kill list).
7. **Chunker INTAKE why (DARK).** Needed for the native-authorship program's chunker-policy conversion — a TNN-deliberated policy with no consulted why-trace fails H7 on arrival.
8. **Upscale operator choice (DARK).** Round 3's "TNN chooses the operator" requirement should include a decision trace with a reader, or the choice is unverifiable post-hoc.

**P3 — harmless, label honestly:**
9. **Audio printed journal, memory_org rationale, general_ops OPS_TRACE.txt (DECORATIVE).** Post-hoc logs with no consumer; fine as-is if labeled logs, not traces.

---

## Work orders (for the owning lines — map only, no fixes applied)

- **WO-1 — dialogue line:** emit a live decision trace per adopted gate (which gate fired, what it saw) with a reader on a decision path — or explicitly scope dialogue decisions as H7-exempt with Micah's sign-off. The in-flight fork-divergence repair must carry the trace story into the unified line.
- **WO-2 — deliberation line:** wire a consumer for the ARGMAX/CLOSE/REVIEW/phash records (native-epistemics is the natural reader) or re-scope them explicitly as audit-only; correct the L2686 "verifies phash" comment to match the emit-only code; delete or wire `tr_phash`.
- **WO-3 — memory/strength line:** wire tier into retention/recall decisions or delete it; add a pricing-decision trace (weights fired, reason code, price) with a reader. Do not weaken the erase-price bars to do it.
- **WO-4 — epistemics line:** add an H7-style causal-consultation bar for traces (intervention on trace read sites) before Phase-2; K3's structural audit is necessary but not sufficient.
- **WO-5 — one-brain line:** consume branch margins in `reint_better` or delete the writes (behavior-neutral either way; prove with byte-identical rerun).
- **WO-6 — chunker line / native-authorship program:** the chunker-policy conversion must ship with a consulted why-trace or it fails H7 on arrival; decide the fate of `policy_why` prose (label as log, or make it the trace and put a reader on it).
- **WO-7 — upscale line:** round 3's operator-choice requirement includes a decision trace with a reader.
- **WO-8 — audio line:** none required — the history ring covers consultation; keep the printed journal honestly labeled as logs.

## Method note

Read-only. No batteries were run for this map: COVERED verdicts rest on the decoration audit's committed neuter probes (built with the pinned toolchain against `6b23696fc`, rerun byte-identical) plus read-site analysis on the current head (`5b661730da`) confirming no new readers/writers appeared. DECORATIVE verdicts rest on exhaustive read-site greps (zero decision-path readers). DARK verdicts rest on absence of emission in the committed source. If any owning line disputes a cell, the dispute is settled the usual way: a neuter/intervention probe, not an argument.
