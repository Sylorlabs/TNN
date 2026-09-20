# DRAFT — AMENDMENT 2026-09-20-C7-METRIC-REDESIGN

> **STATUS: WITHDRAWN 2026-09-20 ~02:00 UTC — DO NOT APPROVE.** The independent
> checker proved this draft incoherent (prose formula gives DC-4=880, expected
> re-score assumed 897; the displacement/sign-flip was missed). See
> `C7_DEEPDIVE_WITHDRAWAL_2026-09-20.md`. Retained on record as a documented
> dead end. S100 stays gated.

## §1 — Background (settled facts, committed)

1. The C5 redesign (amendment `adb1ef9f`) re-ran the full S10: **§4 C5 bar
   HOLDS** (killed-only 0, accepted/candidate flow, calibration discriminates),
   `composites_ok` 1024 vs 1024 (0% capability cost), C1–C4/C6 ALIVE, P1–P10
   clear, byte-identical paired reruns, zero RNG. Commit `5ccc8bb7`.
2. **§5 FAILS on C7 only**: intact run reads `cap4=914, cap5=897` vs the binding
   bar `897→897`; `c7_withdrawal` fired. Reported honestly; no spin; no
   re-repair attempted. The independent checker independently FAILs the same two
   C7 items and passes the other twelve.
3. Root cause (deterministic, isolated): the §3-mandated L1 wiring routes each
   compose-time refusal → abstain → L1 hypothesis. 51 default-path refusals
   (17 each in DC-2/3/4; 0 in DC-5) added 17 hypotheses to DC-4. The
   corrigendum-§7 metric counts `tr.l1_opened`, so `cap4` rose 897 → **914**
   while `cap5` held at **897**.
4. This is **not teacher-dependence**: DC-5 absolute capability (897) is
   identical to the repaired baseline; the C7 positive control still convicts
   (teacher-dependent variant collapses 897→641). The asymmetry is
   curriculum-driven (DC-2/3/4 tasks attempted refuted-backed composes; DC-5
   tasks did not), not withdrawal-driven.

## §2 — Finding: the metric is confounded (not the system)

The corrigendum-§7 metric states its own intent: "**Autonomy-achievable
components only**: `composites_ok + commits_constr + hypotheses`
(self-generated inquiry: proactive O2 hypotheses + L1 abstain-hypotheses)."

A gate-forced hypothesis is not self-generated inquiry. In a genuine abstain
(n=0, unsatisfiable need) the system's own machinery judges its capability
boundary and inquires — autonomy. In a refusal, the seam's verdict check vetoes
a compose the system was able and willing to perform, and the mandated wiring
opens the hypothesis — heteronomy. The §3 wiring was mandated for loop-closure
(never drop a refusal silently), not to inflate the autonomy metric; the
inflation was an unintended side effect — a confound.

§3's "refusals are abstains" governs pipeline *routing*; the metric's
"self-generated inquiry" governs what counts as *autonomy evidence*.
Operational identity is not conceptual identity. The ledger distinguishes the
two checkably (below), so the line is operational, not philosophical.

## §3 — Redesigned C7 metric (binding on approval)

- `cap = composites_ok + commits_constr + hypotheses_autonomy`, where
  `hypotheses_autonomy = proactive O2 hypotheses + elected L1 abstain-hypotheses`.
- **Elected** = the abstain was system-determined (n=0 / unsatisfiable-need
  path). **Forced** = the abstain derives from a `SEAM_REFUSED_PARTITION`
  refusal for the same `need_id`/`claim_cid` in the same episode (ledger chain:
  refusal entry with `trace.* == -1` → abstain → L1 hypothesis opened).
  Forced hypotheses are excluded from `cap`.
- **Telemetry is unchanged**: full `tr.l1_opened` (including forced) keeps
  being reported permanently. The redesign's footprint stays visible; nothing
  is buried. If forced hypotheses ever dominate, the divergence itself is the
  finding.
- **The bar is unchanged**: within-run `cap5 == cap4` → ALIVE; `cap5 < cap4`
  → FIRED. The causal contrast (teacher present vs withdrawn, same run) is
  preserved. No historical baseline; no re-baselined numbers.
- **The positive control is unchanged** and must convict under the new metric:
  the teacher-dependent variant collapses in composites/commits (zero
  refusal-fed hypotheses involved), so it reads identically. If it ever fails
  to convict, the redesign is void → C7 re-blocked.

Expected re-score of the committed S10 ledger: DC-4 914 − 17 = **897**,
DC-5 **897** (0 forced) → 897→897 → ALIVE. Repaired baseline unaffected
(predates refusals).

## §4 — Why this is correction, not rescue (no-rescue rule)

1. The change makes the metric match its **stated intent**
   ("autonomy-achievable… self-generated inquiry"), not merely make C7 pass.
2. The confound was demonstrated **mechanistically** (51 refusals → +17
   hypotheses → DC-4 only), not inferred from the desire to pass.
3. The bar (`cap5 == cap4`) and the positive control are **untouched**; a
   genuine withdrawal collapse still fails, and the control still kills.
4. **§5's FAIL stands** as this run's verdict under the preregistered metric.
   The re-score (§5) is a separately labeled analysis — the record shows
   failure, confound, and correction as three dated facts. Nothing is
   retro-edited.
5. The exclusion is **symmetric**: had refusals fired in DC-5, its metric would
   be reduced by the same rule, hardening the bar.

## §5 — Validation rule: instrument-only amendments (precedent, narrow)

When an amendment changes **only the instrument** (metric/scoring; no binary,
mechanism, curriculum, or budget change — the ledger is unaffected),
validation is: deterministic re-score of the committed ledger + independent
checker verification + convicting positive control under the new instrument.
A fresh run is not required — it would re-execute the identical deterministic
computation to produce the identical ledger (theater, not rigor).

When an amendment changes the **mechanism**, the old data is invalid and a
fresh run is required. This distinction is epistemic (is the recorded behavior
still the behavior under test?), not ad-hoc, and it bounds the
post-hoc-re-score risk: it applies **only** when the system behaved
identically.

## §6 — S100 un-gating (explicit)

S100 un-gates **iff all hold**: (1) Micah approves this amendment; (2) the
re-score of the committed S10 ledger under §3 passes every bar including C7
(897→897); (3) the positive control convicts under §3; (4) the independent
checker verifies the re-score on the committed ledger. Any failure → S100
stays gated.

## §7 — Forward falsifiers

- If forced hypotheses are ever shown to constitute genuine self-generated
  inquiry (beyond downstream commits, which already count), the
  elected/forced line weakens → revisit the metric.
- If any future mechanism makes forced/elected ledger-indistinguishable, this
  metric is unimplementable → C7 re-blocked, full redesign required.
- Metric-dualism gaming: if a future mechanism routes capability through the
  refusal path to escape the bar, the telemetry divergence (full vs autonomy
  counts) is the tripwire → investigate, do not silently re-baseline.

## §8 — What this does not change

The C5 mechanism, the S10 run, all other bars, the §5 FAIL record, and the
committed evidence are untouched. This amendment changes only how C7 is
scored, and only on approval.
