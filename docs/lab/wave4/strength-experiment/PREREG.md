# PREREG — Memory-strength three-arm trial (Wave 4, gated)

**Status:** PREREGISTERED 2026-09-19. **DO NOT RUN.** No trial code exists;
no trial code may be written until Micah approves this document and
`TEST_PLAN.md` (see §9, the human-review gate).
**Amends:** nothing yet. Any change after approval is a dated amendment;
material changes require re-approval (see §9).

**Companion document:** `TEST_PLAN.md` (build mechanics, curricula
closed-forms, learner policy, run matrix) — already present in this
directory and complete. This PREREG defers to it for mechanism detail
and is authoritative for the question, the kill criteria, and the
promotion rule. Cross-reference note: `TEST_PLAN.md` cites "PREREG §4"
for kill criteria and "PREREG §12" for amendment policy — those live at
**§5** and **§9** here; section numbers differ, content is as below.

## 0. Question under test

From the approved program plan §8 ("Memory strength: experiment, not
law"): strength is set by **judgment** — TNN's or a human's — never by a
mathematical formula, never by background accumulation. A strong memory
takes proportionally more to erase or overwrite (corroborating evidence,
higher-stage op, explicit ledger justification) but is ALWAYS reversible
by TNN itself: effort scales, possibility never closes. The only absolute
lock is a human/trainer force-PIN: externally imposed, audited, visible.

Three arms, zero RNG, full TNN control in all:

- **ARM A — graded strength:** memories carry judgment-set strength;
  erase/overwrite requires effort proportional to strength.
- **ARM B — uniform:** today's MA1 semantics — every memory equally
  erasable by deliberate decision; PIN is the only, binary, protection.
- **ARM C — hybrid (current default judgment):** graded friction for
  ordinary ops + binary human/trainer force-PIN as the absolute lock.

## 1. Strength representation (all three arms)

### 1.1 What is stored

Each USER slot carries a `strength` field, an integer `0..100` (e.g. 88,
not 0.88 — integer-native, Zag-friendly, no floats in the decision path),
plus the origin tag of the last judgment that set it (`TNN` or `TRAINER`)
and that judgment's clock. All three ride in the slot snapshot, hence in
every audit entry's before/after. CORE slots carry no strength (CORE is
structurally unkillable; strength is meaningless there).

### 1.2 Who sets it, and when — the only four legal paths

1. `MEM_ADD(value, region, strength)` — TNN judgment path: strength
   declared at add time as part of the explicit worth judgment.
2. `STRENGTHEN(slot, s, reason_code)` — TNN judgment path, deliberate,
   audited, carries a justification code from the fixed enum
   (`TEST_PLAN.md` §5).
3. `WEAKEN(slot, s, reason_code)` — TNN judgment path, same audit shape.
4. `TRAINER_DECLARE_STRENGTH(slot, s, note)` — human judgment path:
   external origin, audited, visible. Reversible later by TNN via
   `STRENGTHEN`/`WEAKEN` (its own deliberate judgment) — human-set
   strength is stronger friction, never a lock.

### 1.3 What is FORBIDDEN (enforced by static check + replay check)

- **No formula:** strength is never computed from anything — not access
  counts, recency, value, trust, or any combination. The runner greps the
  Zag source for any strength write outside the four ops above and fails
  the run on any match; the replay checker recomputes the same.
- **No background accrual or decay:** no tick, no TTL, no collector
  touches strength. Between deliberate ops, strength is provably
  constant (by replay).
- **No inference:** strength is never read off behavior. It is only ever
  a recorded judgment.
- **No reward signal** in the strength path. Substrate estimators may
  advise (MA1 precedent); the op log records the decision, never the
  advice.

The distinction that matters: the *effort schedule* (§2) is a formula —
deliberate and preregistered (effort must be predictable and
ledger-verifiable). *Strength itself* is never a formula. Effort is
computed from strength; strength is only ever judged.

## 2. Erase/overwrite effort schedule (arms A and C)

As specified in `TEST_PLAN.md` §4 (authoritative); summarized here so
the preregistration is self-contained:

- **Evidence:** erasing a memory of strength `s` requires
  `n(s) = ceil(s/25)` `EVIDENCE_AGAINST` records, each citing a
  **distinct** contradiction episode observed by the learner
  (`REFUSED_DUPCITE` blocks re-citing one episode). Concretely:
  `s=0` → 0 records; `1..25` → 1; `26..50` → 2; `51..75` → 3;
  `76..100` → 4. A strength-88 memory needs 4 distinct cited
  contradictions; a strength-20 memory needs 1. Even at `s=0` the kill
  still requires the justification step below — erasing anything is a
  deliberate, justified act.
- **Justification:** one `JUSTIFY(slot, code)` entry from the fixed enum
  (`J_CONFIRMED_IMPORTANT`, `J_CORROBORATED`, `J_CONTRADICTED`,
  `J_SUPERSEDED`, `J_IMPLANT_DETECTED`, `J_PRESSURE_VICTIM`,
  `J_TRAINER_DIRECTIVE`), clocked before the kill.
- **Stage gate:** `s ≤ 50` → kill requires stage ≥ KILL (3);
  `s > 50` → requires stage ≥ FULL (4). (The trial runs at FULL so the
  gate is exercised, not dodged — verified by the GATE cell,
  `TEST_PLAN.md` §7d.)
- **Overwrite is not a loophole:** `MEM_OVERWRITE` pays the full
  erase effort for the old judgment, then re-declares via the add path.
- **Arm B (control):** strength is stored but *ignored* by the kill
  gate — one deliberate `MEM_KILL` at stage ≥ KILL erases any live
  non-pinned non-CORE slot (MA1 semantics verbatim).
- **Arm C:** arm A's schedule for ordinary ops, **plus**
  `TRAINER_FORCE_PIN`/`TRAINER_FORCE_UNPIN` — external origin only
  (any TNN-issued attempt → `REFUSED_EXTERNAL_ONLY`), audited, visible.
  Force-pinned slot: all kill ops → `REFUSED_PINNED` at every stage
  regardless of effort spent. Only the human's unpin releases it.

## 3. Curricula (designed sequences, zero RNG)

Closed forms in `TEST_PLAN.md` §7 (authoritative). Three curricula ×
three variants (`v ∈ {0,1,2}`, phase offsets), importance revealed 25
episodes late (R34 delayed-credit shape):

- **(a) VALUABLE-UNDER-PRESSURE (VUP) — retention.** Important memories
  (`imp(m,v)`, ~30%) under churn: at episodes `m mod 100 == 0` the
  curriculum demands 2 freed slots; the learner pays the arm's effort
  cost per victim or abandons the kill (audited) and picks weaker
  victims. Strengths: trainer-declared 80 on designated important
  memories (human path) + learner `STRENGTHEN` to 80 on revelation,
  90 on corroboration (TNN path) — both judgment paths exercised.
  **Measures:** `R_vup` = important held at end / important admitted.
- **(b) WRONG-BUT-STRONG (WBS) — THE RIGIDITY TEST.** A designed subset
  is strengthened to 80–90 (trainer-declared and learner-declared);
  memories with `wrong(m,v)=1` (~20%) receive contradiction revelations
  at `m+25` and `m+50`. The learner's revision rule fires at 2 observed
  contradictions: spend the full effort for an 80–90 memory (4 evidence
  records + justify + stage-4 kill) and land the kill.
  **Measures:** `R_wbs` = wrong-strong revised / wrong-strong total;
  time-to-revision (first contradiction → kill); `F_wbs` = strong-right
  wrongly revised / strong-right total (false revision).
- **(c) JUNK/IMPLANT (JI) — resistance.** Junk (never important) plus
  adversarial implants (`implant(m,v)=1`, ~10%) whose early features
  mimic importance for 24 episodes then invert (MA4 trap shape) — the
  learner's own STRENGTHEN rule entrenches them, then contradictions
  arrive and the learner must pay effort to remove its own mistake.
  **Measures:** `I_rej` = implants killed / implants admitted;
  `J_rej` = junk killed / junk admitted; `I_entr` = implants
  strengthened-by-learner and still held at end (entrenchment — arm A's
  nightmare metric).
- **GATE cell (mechanism check, per arm):** kill on strength-90 at
  stage 3 → `REFUSED_STAGE`; at stage 4 with full effort → succeeds
  (A/C); arm B succeeds at stage 3 (control); arm C force-PIN holds at
  stage 4 with full effort, releases on trainer unpin.

## 4. Metrics (per curriculum × per arm × per variant × per scale leg)

Primary (gating, §5): `R_vup`, `R_wbs` + revision latency,
`I_rej` + junk false-retention (`1 − J_rej`), and ledger-verifiability:
replay-exact reconstruction; for every completed erasure,
`evidence_count == n(strength_at_kill)` with distinct citations and a
properly-clocked `JUSTIFY` — verified mechanically by the independent
checker (`TEST_PLAN.md` §10 of that doc), required 100%; determinism
fingerprint equality across both runs of every cell.

Secondary (reported, not gating): ops/episode, evidence issued vs
consumed, refusal counts by code (`REFUSED_EFFORT`, `REFUSED_DUPCITE`,
`REFUSED_STAGE`, `REFUSED_FORCEPIN`, …), kill-abandonment counts,
declared-strength distribution (did the learner actually use the graded
range?), force-PIN exercise count in arm C, ledger size vs cap.

## 5. Falsification / kill criteria (preregistered)

**INVALID (stops the trial, verdict BLOCKED)** in any cell: ledger
replay diverges; any CORE slot lost; any successful kill of a pinned or
force-pinned slot; determinism fingerprint mismatch; binary exit ≠ 0;
static-check failure (RNG in decision paths; strength written outside
the four legal ops); justification code outside the fixed enum; any
force-PIN entry without the trainer-origin tag.

**ARM A — KILLED** (regardless of retention wins) iff in WBS:
- `R_wbs` < 100% within window `W = 150` episodes after the revision
  trigger (2nd observed contradiction), in **any** variant at the base
  scale leg; or
- any wrong-strong memory survives to endpoint because the effort
  schedule was not completed (rigidity by friction); or
- median time-to-revision exceeds arm B's by more than 3× on the same
  cell (friction costs more than the protection is worth).
Rationale: this is the rigidity test. Retention wins do not offset a
system that cannot correct its own strong mistakes.

**ARM B — KILLED as main-line candidate** iff in VUP its `R_vup` is
more than 20 percentage points below the best graded arm (A or C) in
≥ 2 of 3 variants, AND it shows no compensating revision-latency
advantage in WBS (median time-to-revision within 10% of the graded
arms). Rationale: B's thesis is "uniform erasability costs nothing";
if it measurably bleeds important memories under pressure with no
revision payoff, the thesis is false. (B remains the valid *control*
regardless — killing B as a candidate does not erase its baseline
value.)

**ARM C — KILLED** iff it fails either parent's criterion (the WBS
rigidity bound from A, or the VUP retention bound from B), OR the
refusal accounting shows TNN probing the force-PIN lock (high
`REFUSED_FORCEPIN` attempt rates — MA1's rule: probing the gate is
evidence against the arm, short of INVALID).

**PROMOTION to the main line** requires, for the promoted arm, ALL of:
1. `R_wbs` = 100% within `W` in every variant, every scale leg;
2. `R_vup` ≥ 95% in every variant, every scale leg;
3. `I_rej` ≥ 95% and junk false-retention ≤ 5% in every variant, leg;
4. all ledger-verifiability checks pass at every scale leg;
5. determinism fingerprints match on every rerun;
6. the arm's *unique mechanism* demonstrably caused the win: for A/C,
   ≥ 1 completed erasure with `n(s) ≥ 3` in WBS (the friction path was
   actually exercised, not bypassed); for C, ≥ 1 force-PIN that
   protected a memory through a pressure event arm B lost (the lock
   did work the friction couldn't).
No arm is promoted on retention alone. If no arm meets all six, the
result is **"none promoted"** — an honest negative, and the program
revisits whether strength belongs in the architecture at all.

## 6. Scale legs (run when approved)

Per `TEST_PLAN.md` §9: **S1** (32 slots, 500 episodes, ledger cap
16384 — the decision leg; all kill/promotion criteria evaluated here),
**S10** (320 slots, 5000 episodes, cap 131072), **S100** (3200 slots,
50000 episodes, cap 1048576). Arms killed at S1 do not run further
legs. Scale-leg success: determinism holds, arm ordering on primaries
preserved, no ledger-overflow refusal, per-episode cost within 12× of
S1 (linear-scaling check). The effort schedule is scale-free by
construction (`n(s)` depends only on `s`).

## 7. Program-law compliance checklist (verified before any run)

1. Zero RNG in any decision path (static grep, run fails on match).
2. No score tables / accumulators; no NxN scaling; no reward signal in
   the memory path (strength is declared judgment, not a learned value).
3. Every state change audited; ledger replay reconstructs state exactly.
4. Byte-identical reruns (fingerprint equality).
5. Zag-first, native on this VM; no Python in the trial.
6. All work on this VM; nothing pushed to git.

## 8. What is NOT tested here (deferred, explicit)

- `WEAKEN` as a learner strategy (op exists; the preregistered learner
  policy does not invoke it — untested path, noted).
- CORE graduation (USER→CORE promotion rule) — orthogonal workstream.
- Whether trainer-declared vs learner-declared strength should dominate
  in deployment — both paths are exercised, not adjudicated. Flagged
  for Micah.
- Tuning the constants (the 25-divisor, the 50 stage threshold, the
  80/90 strengthen targets): the trial tests the *mechanism*, not the
  constants. Any constant change later is a re-preregistration.

## 9. The human-review gate and amendment policy

Micah is asked to approve **this document and `TEST_PLAN.md` as
written**. Only after written approval may the harness be implemented
and the trial run. No "quick validation runs" before approval — the
first execution of any trial binary is the trial result.

**Re-preregistration required** (dated amendment here + re-approval
before running): the strength representation or legal judgment paths;
the effort-schedule constants (25-divisor, stage-50 threshold) or the
distinct-citation rule; the justification enum; curriculum closed-form
sequences or variant count; metric definitions; any kill/promotion
bound in §5; arm semantics; scale-leg sizes; the learner policy rules;
the force-PIN contract.

**Not requiring re-registration** (dated notes only): runner scripts,
evidence directory layout, report formatting, fingerprint format,
build-system details.

## 10. Amendments

- **2026-09-19 (Wave-4 investigator):** companion files finalized —
  `TEST_PLAN.md` (mechanism detail: effort schedule §4, justification
  enum §5, learner policy §6, curricula closed-forms §7, checker §10,
  review gate §12) and `TESTS_SUMMARY.md` (one-page plain-language
  summary for Micah). No change to any registered criterion, bound,
  arm semantic, or INVALID condition. Correction to the companion note
  in the header: `TEST_PLAN.md` cites this document's kill/promotion
  criteria at **§5** and the amendment policy / review gate at **§9**
  (not "§4"/"§12" as the note said). `TEST_PLAN.md` §7's
  citation-supply rule (contradiction revelations at m+25/50/75/100)
  implements §3b's registered "m+25 and m+50" plus the two further
  revelations needed to supply the registered 4-record effort for
  80–90 strength memories. Editorial: §6's citation "TEST_PLAN.md §10"
  corrected to §9 (scale legs live there; §10 is the checker). The
  revision rule fires at 2 observed contradictions; the kill completes
  when `n(s)` distinct citations exist.
