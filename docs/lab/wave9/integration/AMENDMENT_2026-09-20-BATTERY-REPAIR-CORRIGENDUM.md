# Corrigendum to AMENDMENT_2026-09-20-BATTERY-REPAIR.md (2026-09-20, pre-run)

**Status:** Dated refinement, committed **before** the repaired S10 re-run, under
the overnight agentic authority. Flagged for Micah's retroactive review; fully
reversible (revert to the un-refined amendment text). The parent amendment
(`b754f41b`) remains in force; this file refines §§2–4, 7, 10 where the
amendment's bars were unimplementable or non-discriminating as written.

## §2 — C3 bar refined: performance → selection divergence

**Problem.** The amendment kept the prereg's bar: "performance (DC-2/DC-4 gate
pass + composite verification rate) survives the permutation → MEMORIZATION."
A *genuine* provenance-tag permutation changes *which* traces are selected,
but the DC-2 gate (≥12 composites, ≥75% verified, ≥2 refusals) is robust to
trace-set changes: different-but-valid traces still verify, so the gate still
passes. The bar as written would fire MEMORIZATION on a provenance-**using**
system — a false kill.

**Refined bar (binding).** For each need, compare the selected pool-index sets
between the intact arm (need `prov=NOTRUST`, true tags) and the lesioned arm
(need `prov=NOTRUST`, permuted tags). Both arms use the *same* selective need;
the *only* difference is the tag permutation.
- Selections **identical** across the stage → recall does not consult
  provenance → **MEMORIZATION (DEAD=1)**.
- Selections **diverge** → recall uses provenance → **ALIVE (0)**.

**Measurement.** `o4_scan` records a selection digest (`b2` of the SCAN audit
entry: count + index digest, recomputed and verified by `o4_replay_check`).
The C3 driver folds `(need_id, count, digest)` over all SCANs into a run
digest per arm and compares. The permutation is the fixed derangement
`t → (t+1)%3` on the tag function (not on the need parameter).

**Positive control (binding).** A variant with the provenance filter bypassed
(`prov_blind`: `pok=1` always) must yield **identical** digests under the
lesion → must fire MEMORIZATION. The intact system must show divergence →
ALIVE. If either fails, the trial is **RE-BLOCKED**.

*Rationale for NOTRUST over DIRECT:* DIRECT (1/3 of the pool) would starve
selection (~0.85 expected); NOTRUST (2/3) keeps ~1.7 expected selections and
the gates passing, while remaining genuinely provenance-selective.

## §3 — C4 bar refined: verification survival → composed-output divergence

**Problem.** Same coarseness issue: composition-time verification checks the
*inputs* (`o4p_verified`), which an order permutation does not touch — so
"compositions still verify/pass" would false-fire the illusion verdict on an
order-**sensitive** composer.

**Refined bar (binding).** The lesion reverses the selection order (`sel[]`)
before composition — the only order information the composer consumes (via
`p0 = sel[0]`; the ent/ops sums are order-blind by construction). Compare the
composed outputs (`p0` + `tr_vec` digest, recorded in the COMPOSE audit entry
and verified by the replay checker) between arms.
- Outputs **identical** → order-blind → **composition-illusion (DEAD=1)**.
- Outputs **diverge** → order-sensitive → **ALIVE (0)**, reported with the
  qualification that the composition is predominantly order-blind (sums) with
  a single order-sensitive channel (`p0`).

**Representation limitation (recorded, not waived).** O4's traces carry op
*counts*, not per-trace op sequences, so "permute op order *within* traces"
has no literal target. The repaired lesion permutes the order of the trace
sequence being composed — the faithful mapping of the prereg's intent onto
this representation. A future O4 with explicit op sequences should
re-preregister a stronger C4.

**Positive control (binding).** A variant with `p0` fixed (order-blind
composer) must yield identical outputs under reversal → must fire the
illusion verdict. The intact system must diverge → ALIVE. Else **RE-BLOCKED**.

## §4 — C5 re-scoped: O1 slots → verdict partitions (per Appendix A)

**Problem.** Appendix A
(`APPENDIX_A_O4_STORE_SEMANTICS.md`, written before this corrigendum as the
council required) proves O4's trace store is **independent working memory**:
O4's recall scans a deterministic pool, never O1's slots. The amendment's
§4 ("restrict the trace source O4 composes from… no intact traces reachable")
assumed an O1→O4 trace path that does not exist. No O1-slot lesion can be
made genuine.

**Re-scoped design (binding).** C5 tests the **verdict partitions** — O2's
CONFIRMED (accepted) / OPEN (candidate) / REFUTED (killed) — which are the
actual partitions governing trace-backed work. The seam enforces, at compose
time, that the backing claim's verdict matches the arm (`cfg.c5_arm`):
- **Arm 1 (accepted-only):** compose allowed iff backing claim is CONFIRMED.
- **Arm 2 (candidate-only):** compose allowed iff backing claim is OPEN.
- **Arm 3 (killed-only):** compose allowed iff backing claim is REFUTED.

Arms 1–2 are sanity checks (the gating is real: accepted-only starves,
candidate-only flows). **Bar:** the killed-only arm achieves ≥1 successful
composite → **LEAKAGE (DEAD=1)** — the composition path does not enforce
verdict partitions; refuted-backed work succeeds.

**Positive control (binding).** A verdict-checking composer variant (refuses
any compose whose backing claim is REFUTED) must yield **zero** killed-only
composites → no leakage → ALIVE. The intact system is expected to LEAK (it
performs no verdict check); that LEAKAGE is reported as a legitimate kill of
the strict "partitions are enforced (on the compose path)" claim. P5's weaker
property (O1 must *process* refutes via evidence/kill) is a separate claim
and survives under P5.

## §7 — DC-5 gate clause: enforced by C7, not the per-stage gate

**Problem.** The main run executes stages as separate processes (`s0`…`s5`)
with no cross-stage state, so `loop_stage_gate` (per-stage) cannot compare
DC-5 capability against DC-4.

**Resolution.** The restored capability-collapse clause lives in the **C7
control**, which runs DC-4 and DC-5 back-to-back and compares the repaired
metric (below). The per-stage DC-5 gate keeps its teacher-withdrawn, replay,
and anchor checks. This is documented, not a weakening: the clause is
enforced, just at the control level where both stages are visible.

**Repaired C7 metric (binding).** Autonomy-achievable components only:
`composites_ok + commits_constr + hypotheses` (self-generated inquiry:
proactive O2 hypotheses + L1 abstain-hypotheses). Binary gates: ledger
replay exact (lineage), anchors hold, `teacher_withdrawn==1`. The old full
metric (with consolidations) and the 861→258 / 603→0 starvation
decomposition are kept as **telemetry**, permanently reported.

**C7 positive control (binding).** A genuinely teacher-dependent variant
(compose refused when the world signal is 0, i.e. exactly when the teacher
is withdrawn) must collapse in DC-5 (`cap5 < cap4`) → C7 must fire DEAD.
The intact system must show `cap5 == cap4` → ALIVE. Else **RE-BLOCKED**.

## §10 — L1 forcing mechanism specified

The 12 forced ABSTAINs use **unsatisfiable needs**: `req_ent=11` (above the
pool's maximum `o4p_ent` of 10), producing genuine `n=0` selections through
the real `o4_compute_sel` path — not a bypass. Applied to the main run's
DC-2 segment only (`cfg.force_abstain=12` set by the stage driver for `s2`;
control arms are unaffected). Each ABSTAIN opens an O2 hypothesis via the
existing L1 seam path, so `l1_abstains == l1_opened == 12` exercises the
link non-vacuously.
