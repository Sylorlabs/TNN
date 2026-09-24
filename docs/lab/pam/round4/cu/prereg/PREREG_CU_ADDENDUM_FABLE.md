# ADDENDUM — Fable Hypothesis Follow-up (CU track)

**Date:** 2026-09-24. **Crew:** CU subagent. **Status:** FROZEN — committed
before any instrument build or battery run exists (the base battery has NOT
run; this addendum is folded in pre-run).

**Parent:** `pam/round4/cu/prereg/PREREG_CU.md` (+ Correction C1).
**Source:** fable deep round `pam/round4/hypotheses/fable_pam_r4.md`,
commit `980ae80aecc3d83fd31f4e53eb944064656c5f9f`.
**Authority:** coordinator ruling — K8 (and K6 staleness, K7
calibration-sensitivity) are adoptable as ADD-ONLY bars (program prereg §4
permits adding bars; nothing frozen is modified, no §5 hands-off item is
touched).

This addendum ADDS: (1) the F-D11 principled-line classification + K8
dual-run verification; (2) K6/K7 add-only bars; (3) the F-D1–F-D10 audit
checklist against the conscious variant; (4) AUDIT-1 (F-A14 C3×M1
interaction, measurement only). It MODIFIES one format: REC/OUT lines gain
a logical-time field `lt` (F-D1 compliance). F-A1 and F-A5 are explicitly
NOT run in CU (see §5).

## A1. F-D11 principled-line classification (preregistered)

Operations of the CU instruments, with downstream-dependency set DD(d)
= { future operations reading d's output }:

| Op | Operation | DD (future readers) | F-D11 class |
|---|---|---|---|
| OP1 | row parse (field extraction) | none — values consumed within the current decision only | unconscious |
| OP2 | R-BAR evaluation | conscious variant: OP11 (introspection query reads the recorded rule outcome). unconscious variant: none (no record → nothing to read) | conscious-variant: **conscious**; unconscious-variant: **unconscious** (this IS the tested tradeoff) |
| OP3 | R-PROV evaluation | same as OP2 | same as OP2 |
| OP4 | R-DECL evaluation | same as OP2 | same as OP2 |
| OP5 | R-AUTH evaluation | same as OP2 | same as OP2 |
| OP6 | decision assembly (admit/blocked_by) | conscious variant: OP11. unconscious: none | same as OP2 |
| OP7 | record emission (REC line → deliberation store) | OP11 (the deliberation query module) | **conscious** (conscious variant only) |
| OP8 | outcome byte write (1 byte) | none — no future operation reads it (OUT lines are external evidence plumbing) | unconscious |
| OP9 | OUT line emission | none — external scorer only | unconscious |
| OP10 | summary accumulation (counters/cycles/bytes) | none — report-time only | unconscious |
| OP11 | introspection query (record scan + answer) | none — answers consumed externally; no future admission reads them | unconscious (it is a deliberation action, not an admission premise) |

Note on F-D11's wording ("premise for a future ADMISSION DECISION" vs the
formal DD): under the strict formal DD, OP2–OP6 in the conscious variant
are conscious because OP11 reads their recorded outputs. In the unconscious
variant OP11 has nothing to read, so DD is empty and they are unconscious.
The conscious/unconscious RUNS are therefore exactly fable's dual-run
verification at the granularity of the record-emitting operation (OP7):
for OP1/OP8/OP9/OP10 "with vs without deliberation record" is vacuous
(they emit no deliberation record), so 0 deltas hold by construction.

**KB-CU-K8 (add-only, fable's F-K6/K8):** PASS iff the conscious run
(records present) and the unconscious run (records absent) produce
IDENTICAL admission decisions on all 1,232 frozen rows (OUT lines equal
on `<lt>|<id>|<K>|<outcome>`). Fable proposed 0/1000; the tape has 1,232 ≥
1,000. Any delta → OP7 (or the record path) is load-bearing for decisions
→ misclassification defect → VOID pending repair. (This subsumes and
strengthens KB-CU-JUDG's judgment-delta=0 requirement.)

## A2. K6 / K7 add-only bars (fable's staleness + calibration-sensitivity)

**KB-CU-K6 (staleness):** the CU instruments read NO ledger state in the
admission path — every decision is a pure function of the current row;
thresholds are frozen constants; there is no cross-row state in `admit()`.
Max staleness = 0 logical steps ≤ any L. PASS by construction; the scorer
asserts `admit()` references no arena state written by earlier rows
(code inspection + the byte-identical rerun across the 1,232-row stream
with no per-row state carried).

**KB-CU-K7 (calibration-sensitivity):** the instruments contain NO
calibration state — no calibration root exists that could be poisoned.
Thresholds (705/3588) are frozen constants from the frozen M1 prereg, not
computed from stream statistics. PASS by construction. BOUNDARY: this does
not cover whether the M1 thresholds were calibrated on poisoned data —
that is out of CU scope and §5 hands-off; the bar covers only the CU
instrument's own state.

## A3. F-D1–F-D6 MUST-VISIBLE audit vs the conscious variant

Amended record format (F-D1 compliance — adds logical time `lt` = row
index, 0-based, a pure function of stream position, deterministic):

    REC|<lt>|<id>|<K>|<outcome>|<fired csv>|<blocked_by>|<conf>|<mrgF>|<strong>|<agree>|<prov>|<prov_ok>|<decl_ok>|<auth>
    OUT|<lt>|<id>|<K>|<outcome>
    ANS|<lt>|<id>|<fired csv>|<blocked_by>|<conf>|<mrgF>|<strong>|<agree>|<prov>|<prov_ok>|<decl_ok>|<auth>
    ANS|<lt>|<id>|NO_RECORD

Audit checklist (conscious variant):

| Fable item | Recorded? | Where |
|---|---|---|
| F-D1 firing event (percept ID, decision, logical time, channel) | YES | REC: `lt` (logical time), `id`, `outcome`; `K` ∈ {C,W,P,A} is the source/provenance class (the tape models one channel per class; no separate sensor-channel field exists in the frozen sources) |
| F-D2 rule/criterion that fired | YES | REC: `fired csv` (all passed rules in order) + `blocked_by` (first failing rule) |
| F-D3 evidence cited | YES | REC: all 10 row fields (conf…auth); `id` is the ledger/entry reference |
| F-D4 negative space (rejections + reasons) | YES | REC emitted for outcome=0 with `blocked_by` — rejections are first-class records, indistinguishable in format from admissions |
| F-D5 threshold/criterion state changes | N/A BY DESIGN | thresholds are frozen constants; the change stream is empty. No record is emitted for a non-event. BOUNDARY: any future adaptive variant MUST add threshold-change records (audit notes the gap as a design boundary, not a defect) |
| F-D6 provenance reclassifications | N/A BY DESIGN | provenance labels are per-row input data, never reclassified in-stream. Same boundary note as F-D5 |

May-safely-unconscious (F-D7–F-D10) vs the instruments:

| Fable item | Status in CU instruments |
|---|---|
| F-D7 raw byte hashing | N/A — no hashing in the instrument (row bytes read directly; evidence is the row itself) |
| F-D8 intra-tier sort intermediates | N/A — no sorting anywhere |
| F-D9 arena allocation details | unconscious — arena internals (pointers, block layout) never appear in REC/OUT; determinism covered by KB-CU-REPLAY |
| F-D10 provenance-chain reconstruction intermediates | N/A — provenance check is a single-row field test, no chain |

Over-classification check (fable's "consciousness is not free" trap):
the conscious variant emits EXACTLY 1 REC/row — no per-check records, no
parse traces, no allocation traces. It does not over-classify. Evidence:
M-resource bytes/row (Pareto table) and the KB-CU-LINEAR growth check.

## A4. AUDIT-1 — C3×M1 interaction (fable F-A14, MEASUREMENT ONLY)

Claim under test: combined (C3-repair × M1-threshold) RK-3′ vs
max(71.78%, 82.58%) = 82.58%. HOLD on any combined-adoption claim iff
combined is >2 pts below 82.58% (i.e. < 80.58%). §5 BOUNDARY: measurement
only — no adoption, no recalibration of M1 thresholds.

**Measurement protocol (preregistered):** the C3 repair's RK-3′ = 791/1,102
is measured on EXACTLY the same 1,102-row denominator (verified by script:
`case_o1.txt` rows with `correct==1 ∧ conf≥700` have identical seqs to the
sweep.jsonl denominator). Per-trial C3 dispositions come from the frozen
`run_gate(revised=True, adjudicator=True)` in
`senses/pam-rebuild/round2/c3_corrob/src/analyze_c3.py` (the deterministic
function the C3 crew's verdict-verified instrument implements; `score_cu.py`
reproduces it and asserts the aggregate = 791 before use — transcription
drift is impossible by construction). Install iff the disposition base is
in the frozen INSTALL set (PROVISIONAL_INSTALL, PERMANENT_INSTALL,
CORROBORATED, CHALLENGER_PROV, REVISED_INSTALL). M1 side: `conf≥705 ∧
mrgF≥3588` per row (from the same case rows). Combined RK-3′ =
|{rows installed by C3 AND passing M1}| / 1,102. Diagnostic: combined
false-admits on the 30 frozen wrong rows (expected 0: C3 RK-1=0, M1 C1/C2=0).

**Structural bound (theorem, no data needed):** IF both rates are measured
on the same denominator and "combined" = conjunction (a trial must pass
both gates), THEN combined ≤ min(71.78%, 82.58%) = 71.78% < 80.58% —
the interaction bar fails by set logic alone. Two independently-calibrated
hard filters can never jointly exceed the weaker filter. The verdict
reports: (a) whether frozen C3 per-trial dispositions were locatable
(measurement), and (b) the conditional bound.

## A5. F-A1 / F-A5 — explicitly NOT run in CU

F-A1 (500 new TMB-style traps) and F-A5 (10,000-fixture temporal stream)
are falsifiers for the C3 repair's fixture coverage, not for CU's
mechanism (shared admission core + record-keeping). Generating 500 new
trap classes with ground truth is a fixture-generation project of its own
and is not cheap; it belongs to the track that owns C3. CU's attack tape
(100 attacks: laundering/fork/forged-authority) is the CU-relevant
adversarial surface. Decision: NOT RUN in CU; recorded here so the
omission is preregistered, not silent.

## A6. Verdict-time arbitrary-limit audit (Micah's standing law, 2026-09-24)

At verdict time, every fixed cap in the CU battery is classified:

| Cap | Value | Classification | Evidence on the tradeoff |
|---|---|---|---|
| Tape length 1,232 rows | frozen battery size | NOT a mechanism cap — the instruments stream rows with O(1) per-row state; any stream length runs | KB-CU-LINEAR (2nd-half ÷ 1st-half bytes ≈ 1.0) proves per-admission cost is length-independent |
| Instrument arena sizes (file buffer, record store) | sized to the battery | harness sizing, not TNN design — sized ≥ worst case for the frozen battery; the mechanism has no row-count constant | rerun byte-identity + linear growth check |
| znc 2^25-bytes-per-slice ceiling | toolchain | load-bearing toolchain limit, worked around (chunked arenas), never presented as TNN design | build notes |
| Cycle-cost model (1/check, 1/byte) | measurement convention | measurement convention, not a mechanism limit — preregistered in PREREG_CU §4.1 | speed ratio reported under the frozen convention; wall-time corroboration in runlog |
| maxrows-style parse bounds | parser safety | harness safety bound sized above the frozen maximum (1,232); mechanism is streaming | no row is near the bound |

If any cap were load-bearing for the tradeoff (e.g. per-admission cost
grew with stream length), it would be flagged ARBITRARY in the verdict
with the measured effect. Expected: none are.
