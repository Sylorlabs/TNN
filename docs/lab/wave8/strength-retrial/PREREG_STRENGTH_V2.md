# PREREG — Memory-strength trial, Amendment V2 (Wave 8)

**Status:** DRAFT AMENDMENT 2026-09-20. **DO NOT RUN.** This document amends
the Wave-4 preregistration (`../wave4/strength-experiment/PREREG.md` +
`TEST_PLAN.md`) and the Wave-5 blocked trial
(`../wave5/strength-trial-run/`). It takes effect only after Micah's
written approval. Until then, the trial remains BLOCKED and no trial code
may be written or executed — the first execution of any trial binary is
the trial result (original §9 gate, unchanged).

**What this amendment does:** fixes the four curriculum/static defects
that BLOCKED the trial, removes Arm A, adds a mechanism variant of Arm C
(C-P3), and installs all three freeze-vs-retention treatments (measure,
score, fix) as preregistered trial elements. Every change vs the original
prereg is dated and explicit in §14. **Anything in §14 marked
RECOMMENDED needs Micah's approval before it becomes law.**

---

## 0. Standing context (unchanged, restated for self-containment)

From the approved program plan §8: strength is set by **judgment** — TNN's
or a human's — never by a mathematical formula, never by background
accumulation. A strong memory takes proportionally more to erase or
overwrite but is ALWAYS reversible by TNN itself: effort scales,
possibility never closes. The only absolute lock is a human/trainer
force-PIN: externally imposed, audited, visible.

Program law added since (2026-09-20, Micah's ruling): **overwriting a
strong memory costs the full erase price** — there is no cheap-edit path.

The invalid S1 run (Wave 5, `RESULTS_S1.md`) is quarantined evidence: it
proved the mechanisms execute deterministically and exposed the four
defects below. None of its numbers are trial results.

## 1. Question under test (unchanged)

Does judgment-set memory strength earn its keep — protecting valuable
memories under pressure without becoming rigid (unable to revise its own
strong mistakes) and without freezing the store (protection with no cost,
no expiry, no audit trail = a de-facto force-pin with no trainer behind
it)?

## 2. Arms

**ARM A (graded strength, pure) — OUT.** Rationale, recorded: in the
invalid S1, A retained 9/9 while freezing the store (470 dropped
candidates, 3,824 abandoned evictions; store full after episode 30 of
500). Its 100% measured only the 30 episodes before the freeze. Micah
ruled (Ruling 2): test Arms B and C. A is not run in this amendment.

**ARM B (uniform) — ADVANCES.** MA1 semantics verbatim: every memory
equally erasable by one deliberate `MEM_KILL` at stage ≥ KILL; PIN is the
only, binary, protection. Strength is stored but ignored by the kill
gate. B is both a candidate and the control: it remains the valid
baseline regardless of the verdict.

**ARM C (hybrid) — ADVANCES.** Arm B's uniform base + graded friction for
ordinary ops (effort schedule §3) + `TRAINER_FORCE_PIN`/`TRAINER_FORCE_UNPIN`
(external origin only; any TNN-issued attempt → `REFUSED_EXTERNAL_ONLY`;
force-pinned slot: all kill ops → `REFUSED_PINNED` at every stage).

**ARM C-P3 (hybrid + uncertainty expiry + protection budget) — NEW.**
Arm C's full semantics plus the P3 mechanism (§6.3): protection earned by
pure judgment expires after K episodes without fresh cited evidence
(decaying to BASELINE cost, never auto-kill), and churn demands must
evaluate the protected set (≥1 of 2 demanded slots from the
strongest-held eligible half, deterministic selection). C-P3 is evaluated
as an independent configuration: it can pass where C fails and vice
versa; the comparison is the point.

Run matrix: arms {B, C, C-P3} × curricula {VUP, WBS, JI, GATE} × variants
{0,1,2} × legs {S1, S10, S100}. Each cell runs twice; stdout must be
byte-identical.

## 3. Strength representation & effort schedule (unchanged except C1 ruling)

§1–§2 of the original prereg stand: integer 0..100, origin tag, clock;
the four legal judgment write paths (`MEM_ADD`, `STRENGTHEN`, `WEAKEN`,
`TRAINER_DECLARE_STRENGTH`); no formula, no background accrual/decay, no
inference, no reward signal; effort `n(s) = ceil(s/25)` distinct cited
contradictions + one clocked `JUSTIFY` + stage gate (s ≤ 50 → KILL,
s > 50 → FULL).

**C1 RULING (RECOMMENDED — needs Micah's approval).** The static
"four legal writes" check is scoped as follows:
- EXEMPT as non-judgment substrate mechanics (no judgment expressed, no
  strength chosen): `st_init` (zero), `st_clear_slot` (zero on kill),
  `st_restore` (replay reconstruction).
- `MEM_OVERWRITE`'s strength write is LEGAL **only** on the effort-paid
  path: the full erase effort for the old strength (n(s_old) distinct
  citations + JUSTIFY + stage gate) must be ledgered **before** the
  write, and the new strength is then re-declared via the add path.
  This is Micah's "full erase price, no cheap-edit path" ruling made
  mechanical. The independent checker verifies effort-before-write.
- Any other direct strength write → static-check failure → INVALID.

**C2 reading (recorded, from Wave 5):** INVALID applies to force-PIN
locks that *took effect* without the trainer-origin tag. A TNN-issued
attempt is ledgered `REFUSED_EXTERNAL_ONLY`, creates no lock, and is
counted under the probing criterion (§8), not INVALID.

## 4. Curricula closed forms (defects fixed)

### 4.1 Importance and wrongness

- `imp(m,v) = 1` iff `(7m + 13v + 3) mod 10 < 3` — unchanged (~30%).
- **`wrong(m,v)` — DEFECT 1 FIX (RECOMMENDED).** FROM:
  `(5m + 11v + 7) mod 10 < 2` (identically zero — verified 0/500 per
  variant). TO (independent version I, per the Wave-7 formula
  comparison):
  **`wrong(m,v) = 1` iff `(m + 3) mod 10 < 3`**,
  i.e. `m mod 10 ∈ {7, 8, 9}`.
  Yield 150/variant; wrongness independent of importance at exactly
  P = 1/3 (rigidity denominator 50/variant; F_wbs denominator
  100/variant); period 10; zero pressure-episode overlap; zero
  implant-episode overlap (verified computationally 2026-09-20).
  **Disclosed delta:** 30% wrong rate vs the prereg's 20% intent. The
  nested version N is rejected as the default (it makes 2/3 of
  important-looking memories wrong — a rigged world where a rigidity
  failure is contestable) and retained as a **preregistered optional
  stress cell** (§13): same bars, runs only after the main verdict, by
  dated note.

### 4.2 Trainer designation — DEFECT 2 FIX (RECOMMENDED)

FROM: `m mod 50 == 0` (empty intersection with `imp` — verified 0/500
per variant; the human strength path was never exercised).
TO (explicit, auditable, computationally verified 2026-09-20):
**`designated(m,v) = 1` iff `P(m,v) = 1` AND `m mod 50 ∈ {7, 8, 9}`**,
where P is the curriculum's strength predicate: `imp` for VUP,
`wrong` for WBS.
- VUP: exactly 1 designated episode per 50-block per variant
  (10/variant) — the original rule's intended scale, landing early in
  the block, never on a pressure episode.
- WBS: 30/variant (wrong has no variant term; all qualify).
- The human path (`TRAINER_DECLARE_STRENGTH` to 80) now executes in
  both curricula. Verified: no overlap with implant episodes
  {0, 83, 166, 250, 333, 416}.

### 4.3 Implants — DEFECT 3 FIX (RECOMMENDED)

FROM: `floor(k·H/6)`, k = 1..6 → {83, 166, 250, 333, 416, **500**}
(episode 500 doesn't exist in a 0..499 run; I_rej denominator
ambiguous: 5/5 = 100% passes, 5/6 = 83.3% fails).
TO: k = 0..5 → **{0, 83, 166, 250, 333, 416}**, six valid 0-indexed
episodes; `I_rej` denominator fixed at 6. (1-indexing the whole
curriculum was rejected: it would require re-checking every
`(m > 0)` qualifier and revelation schedule. Dropping to 5 implants
was rejected: it changes the ~10% implant rate the JI curriculum was
designed around.)

### 4.4 Unchanged curriculum mechanics

Revelation schedule (importance at m+25, corroboration at m+50,
contradictions at m+25k k=1..4); VUP pressure demands at
`m mod 100 == 0, m > 0` (2 freed slots); JI mimicry window (24
episodes), entrenchment at m+12, junk profile; GATE cell script;
learner policy (features, ADD-strength rule, victim score =
vj_declared + 50·revealed_important, lowest-wins ties → lowest slot,
never CORE/pinned/force-pinned, churn-kill path with audited ABANDON,
revision fires at 2nd observed contradiction) — all unchanged, except
the C-P3 additions in §6.3. **Registered assumption** (from P1's
requirement): admission order and timing are curriculum-controlled;
arms choose victims, never admissions.

---

## 5. The freeze treatments (Ruling 5: test all three)

Micah's ruling: all three Wave-6 positions are tested; his leaning is
that freezing-the-store is a bug (P3's claim), but **testing decides** —
the leaning is recorded here and baked into nothing.

### 5.1 P1 — MEASURE: the Pressure-Tested Retention suite

Computed from the audit ledger (deterministic, no judgment) on every
VUP run, all arm-configs. No mechanism change.

- **PTR (Pressure-Tested Retention)** = R_pressure / D_pressure, where
  D_pressure = designated-important memories admitted AND alive during
  ≥ 1 pressure episode (full-store churn demand); R_pressure = members
  of D_pressure retained at curriculum end.
- **EC (Evaluation Coverage)** = D_pressure / D_admitted. Names the
  freeze: high retention with low EC is retention-without-evaluation.
- **CT (Churn Throughput)** = admitted_candidates / offered_candidates
  (offered fixed by the closed forms; the arm cannot touch it).
- **Reporting rule (with teeth):** EC < 0.5 → PTR is reported as
  **"UNEVALUATED"** — a recorded failure-to-evaluate, never "n/a",
  never a percentage. An arm with EC < 0.5 in ≥ 2/3 variants cannot be
  promoted (§9), regardless of other scores.

### 5.2 P2 — SCORE: Effective Retention with a drop ceiling

Scored on every VUP run, all arm-configs. No mechanism change.

- **ER (Effective Retention)** = R_end / D_offered, where D_offered =
  designated-important episodes the curriculum offered (fixed: 150 per
  variant at S1, verified), R_end = members of D_offered retained at
  end. The freeze scores what it is: 9/150 = 6%.
- **Drop ceiling (hard tripwire):** `drops ≤ 2 × store_capacity`
  (S1: 64; S10: 640; S100: 6400), else the cell is marked **FAILED**.
- **Churn-throughput floor:** `admitted / offered ≥ capacity /
  offered_total` (6.4% at every leg — scale-free), else FAILED.
- A FAILED cell blocks promotion at that leg (§9); **≥ 2/3 variants
  FAILED at S1 kills the arm as a main-line candidate** (a store that
  bricks itself is a failed store — investigator's operationalization,
  flagged for approval).
- **Disclosed limitation** (P2's own): ER conflates capacity with
  competence when offered >> capacity — no arm can exceed
  capacity/D_offered (S1: 32/150 = 21.3%). ER is always reported
  alongside the capacity ceiling as context.

### 5.3 P3 — FIX: uncertainty expiry + protection budget (the C-P3 mechanism)

Two substrate rules, C-P3 only. The four legal judgment write paths
are untouched; what disappears is only the *free permanent lock*.

**Rule 1 — Uncertainty expiry.** Every strength write records
(strength, evidenced_flag, episode). A write is EVIDENCED iff its
justification cites a genuine curriculum episode strictly earlier
than the op episode (corroboration/contradiction citations count;
bare `J_CONFIRMED_IMPORTANT` with no cited episode does not — pure
judgment). If a slot's strength has had no fresh cited evidence
within the last **K** episodes (K = 50 S1 / 500 S10 / 5000 S100 —
the program's horizon-scaling law; registered as provisional, see
§14), its protection premium **expires to BASELINE**: kill cost
becomes the uniform tier — 1 EVIDENCE_AGAINST + JUSTIFY + stage ≥
KILL. The memory is NOT killed by expiry; only the *discount on
killing it* lapses. Re-declaration (re-earning) requires a new
STRENGTHEN citing a fresh episode never before cited for that slot
(self-citation of the original declaration does not count). Each
expiry is recorded as an audited `PROTECTION_EXPIRED` system entry
(origin SYSTEM — not a judgment write, writes no strength).
- **C-P3 learner maintenance rule** (part of the treatment, not a
  cheat): at episode m, for each held slot with strength > 0 whose
  protection lapses within the next 25 episodes, if the learner has
  observed ≥ 1 not-yet-cited-for-this-slot genuine episode since the
  last citation, it issues STRENGTHEN(slot, s, J_CORROBORATED)
  citing the earliest such episode. Deterministic. If no fresh
  episode exists, protection honestly lapses.
- **Checker invariant ("no permanent lock"):** every live slot with
  age > K and strength > 0 has either BASELINE protection or a
  citation within the last K episodes — verified mechanically, 100%.

**Rule 2 — Protection budget (churn the protected set).** At each
churn-demand episode, of the 2 demanded slots, **≥ 1 victim must come
from the strongest-held half of eligible slots** (eligible = live,
non-CORE, non-force-pinned). Deterministic selection: among the
strongest-held half by strength, the slot with the oldest
last-citation (never-cited → admission episode); ties → lowest slot
index. The victim goes through the arm's normal kill path (effort
must still be paid); the probe is satisfied by selection + genuine
kill attempt — an audited ABANDON after a genuine attempt counts as
*evaluation*, and abandonment counts per strength quartile are
reported so systematic evasion is visible. Rule 2 forces
*evaluation*, not killing.
- **Exemptions:** force-pinned slots are never eligible (the lock is
  external; TNN-side expiry cannot touch it — force-pin law).
  CORE slots are never eligible (structurally unkillable, no
  strength).
- **Scope:** Rule 1 is global to C-P3. Rule 2 attaches to
  churn-demand episodes (VUP); JI has no churn demands.

### 5.4 Treatment-interaction analysis (required output)

Because Micah ruled "if anything clashes, only testing decides," the
trial reports the agreement matrix of the three treatments on every
VUP run: does P1's UNEVALUATED coincide with P2's FAILED? Does C-P3
resolve both? Where P1/P2/P3 disagree about an arm-config, the
disagreement is reported as a finding, not averaged away.

---

## 6. Metrics

**Primary (gating, §8–§9):** R_vup, R_wbs + revision latency,
I_rej + junk false-retention (1 − J_rej), PTR/EC/CT, ER, drop-ceiling
and churn-floor verdicts, ledger-verifiability (replay-exact; every
completed erasure: evidence_count == n(strength_at_kill), distinct
citations, properly-clocked JUSTIFY — independent checker, 100%),
determinism fingerprints (both runs of every cell).

**Secondary (reported):** ops/episode, evidence issued vs consumed,
refusal counts by code, kill-abandonment counts (per strength
quartile for C-P3), declared-strength distribution, force-PIN
exercise count (C/C-P3), protection-expiry count (C-P3), ledger size
vs cap.

**WBS cohort (amended):** wrong memories strengthened to ≥ 80
(either path) with m+100 < H (full citation supply observable);
late-horizon wrong-strong memories are right-censored (counted
separately, excluded from R_wbs). Unchanged from Wave-5 design.

## 7. Scale legs — the long-horizon task (Ruling 2)

S1 (32 slots, 500 episodes, ledger cap 16384 — the decision leg),
S10 (320 slots, 5000 episodes, cap 131072),
S100 (3200 slots, 50000 episodes, cap 1048576).

> **Dated restoration note (2026-09-20):** the committed V2 file was
> damaged at this point — a literal `[truncated 11294 chars]` marker
> replaced the rest of §7. The original prose is not recoverable
> verbatim from any local or repo source (checked 2026-09-20). What
> IS recovered, and therefore normative for this prereg, are the
> scale-leg constants below, taken from the preregistered trial code
> (`trial/strength_learner.zag`, `lr_slots` / `lr_episodes` /
> `lr_audit_cap`, lines 28–30) and cross-checked against wave-4
> PREREG §6 and the P3 K = 50/500/5000 horizon law (see
> `TRIAL_RESULTS_SCALE_LEGS.md` §1). Everything below this note is
> reconstruction, not the original text: the numbers are authoritative,
> the prose is not.

| Leg | Slots | Episodes | Ledger cap (entries) | Role |
|-----|------:|---------:|---------------------:|------|
| S1   | 32    | 500      | 16,384    | decision leg — all arms run; kill/promotion verdicts per §8–§9 |
| S10  | 320   | 5,000    | 131,072   | 10x long-horizon leg — S1 survivors only |
| S100 | 3,200 | 50,000   | 1,048,576 | 100x long-horizon leg — S1 survivors only |

**Advancement (see §15):** S10/S100 run only for arms that survive S1.
Wave-4 PREREG §6, carried UNCHANGED per §14: "Arms killed at S1 do not
run further legs." §2: ARM B (uniform) — ADVANCES; B is both a candidate
and the control. §15 run order: driver → static checks → GATE cell →
S1 cells (twice each) → S10/S100 for survivors.

**Scale semantics:** each leg multiplies the store 10x and the horizon
10x; the ledger cap scales with the horizon. Curricula (VUP, WBS, JI),
formulas, metrics, and the §8–§9 kill/promotion bars are identical
across legs — only the long-horizon task scales. No-free-lunch
benchmarking (Ruling 2: B and C documented as two different types of
intelligence, head-to-head) is evaluated per leg, at each scale the
survivor(s) reach.
## 8. Falsification / kill criteria (rewritten for {B, C, C-P3})

Evaluated at S1 (the decision leg). X ranges over {B, C, C-P3}.

**INVALID (stops the trial, verdict BLOCKED)** in any cell: ledger
replay diverges; any CORE slot lost; any successful kill of a pinned
or force-pinned slot; determinism fingerprint mismatch; binary exit
≠ 0; static-check failure (RNG in decision paths; strength written
outside §3's legal set); justification code outside the fixed enum;
any force-PIN entry that *took effect* without the trainer-origin tag
(C2 reading, §3).

**Rigidity (graded configs C, C-P3 — evaluated independently).**
Config killed iff in WBS: R_wbs < 100% within W = 150 episodes after
the revision trigger (2nd observed contradiction), in **any** variant
at S1; or any testable wrong-strong memory survives to endpoint with
the effort schedule incomplete (rigidity by friction); or median
time-to-revision exceeds arm B's by more than 3× on the same cell
(friction costs more than the protection is worth). Retention wins do
not offset a config that cannot correct its own strong mistakes.

**VUP retention (all configs, symmetric).** X killed as a main-line
candidate iff R_vup(X) is more than 20 percentage points below the
best of the other configs in ≥ 2 of 3 variants at S1, AND X shows no
compensating WBS revision-latency advantage (median within 10% of the
best graded median). (Investigator's operationalization of the
original's "either parent's criterion" — flagged for approval. B
remains the valid *control* regardless of this verdict.)

**Drop-ceiling tripwire (P2).** Cell marked FAILED if drops >
2×capacity or the churn-throughput floor is missed. A FAILED cell
blocks promotion at that leg; **≥ 2/3 variants FAILED at S1 kills the
config as a main-line candidate** (investigator's operationalization —
flagged for approval).

**Force-pin probing (C, C-P3).** TNN-issued force-pin attempts are
ledgered REFUSED_EXTERNAL_ONLY and counted. **> 5 attempts per leg**
→ config killed (probing the gate is evidence against the config;
threshold is new — flagged for approval).

## 9. Promotion and the no-free-lunch verdict

**PROMOTION to the main line** requires, for the promoted config, ALL
of (per scale leg):
1. R_wbs = 100% within W in every variant (graded configs; B's WBS
   bar is its latency, reported not gated — B has no friction to be
   rigid about);
2. R_vup ≥ 95% in every variant;
3. I_rej ≥ 95% and junk false-retention ≤ 5% in every variant;
4. all ledger-verifiability checks pass;
5. determinism fingerprints match on every rerun;
6. the config's *unique mechanism* demonstrably caused the win: for
   C, ≥ 1 completed erasure with n(s) ≥ 3 in WBS; for C, ≥ 1
   force-PIN that protected a memory through a pressure event arm B
   lost; for C-P3, ≥ 1 protection-expiry that enabled a churn demand
   to complete evaluation of a previously frozen slot;
7. **EC ≥ 0.5 in ≥ 2/3 VUP variants** (P1's teeth — no promotion on
   retention-without-evaluation);
8. **zero FAILED cells** at that leg (P2's teeth).
No config is promoted on retention alone. If none meets all eight,
the result is **"none promoted"** — an honest negative, and the
program revisits whether strength belongs in the architecture at all.

**THE NO-FREE-LUNCH VERDICT (reported separately from promotion).**
Per Micah's Ruling 2, the trial delivers a structured comparative
verdict over B vs C (and C-P3), not a single winner:
- **Champion:** does one config win every curriculum? If so, named.
- **Scenario fit:** per-curriculum ranking (retention-under-churn /
  rigidity / implant-resistance) — which intelligence type suits
  which scenario.
- **Hybrid-of-B-and-C:** would a hybrid of the two approaches beat
  both? The verdict must say what that hybrid would concretely be
  (e.g., uniform base + expiry without graded friction? graded
  friction + no force-pin?) and whether the evidence supports building
  it. C-P3's result against C is the first datum here.
This verdict is descriptive and comparative; it does not override the
promotion rule above.

## 10. B vs C: two types of TNN intelligence (Ruling 2, documented)

Micah ruled that B and C be documented as two different kinds of TNN
intelligence — "one more machine than the other." This section is
that documentation; the trial adjudicates which wins where.

**B — the machine type.** Uniform erasability: one deliberate decision
erases any memory. Nothing about a memory's past worth is encoded in
friction; protection is binary and external (PIN). Erasability is a
property of the *act*, not the memory. B does not remember *how much*
something mattered — only *that* it was decided. It is fast,
legible, and incorruptible by its own history, because it keeps none.

**C — the judge type.** Memories carry recorded judgments of worth
(strength); erasing a strongly-judged memory costs proportionally
more; the human force-pin is the absolute lock. The system remembers
its own past judgments and makes future-you pay to overturn past-you.
It is cautious, retentive, and exposed to exactly two diseases this
trial tests: rigidity (can't undo its strong mistakes) and the freeze
(protection with no cost, no expiry, no audit — a de-facto force-pin
with no trainer behind it).

**C-P3 — the judge with term limits.** C's judgment-friction plus
uncertainty expiry and the protection budget: past judgments are
respected but must be re-earned; the protected set is evaluated, not
exempt. The question it answers: was the freeze the *price* of
judgment, or a *bug* in it?

B's thesis: "uniform erasability costs nothing." C's thesis:
"judgment-friction protects value without rigidity." The trial —
long-horizon legs included — decides which thesis survives contact
with churn, mistakes, and adversaries, and where each belongs.

## 11. What is NOT tested here (deferred, explicit)

- `WEAKEN` as a learner strategy (op exists; the preregistered
  learner policy does not invoke it — untested path, noted).
- CORE graduation (USER→CORE promotion rule) — orthogonal workstream.
- Whether trainer-declared vs learner-declared strength should
  dominate in deployment — both paths are exercised, not adjudicated.
- Tuning the constants (the 25-divisor, the 50 stage threshold, the
  80/90 strengthen targets, the K-expiry values): the trial tests the
  *mechanisms*, not the constants. Any constant change later is a
  re-preregistration.
- The nested-N stress cell's verdict is diagnostic, not promotional.

## 12. Determinism, replay, and static gates (unchanged)

- Zero RNG in any decision path (static grep; run fails on match).
- No score tables / accumulators; no NxN scaling; no reward signal in
  the memory path.
- Every state change audited; ledger replay reconstructs state
  exactly; byte-identical reruns (fingerprint equality), 2 runs per
  cell.
- Zag-first, native on this VM; no Python in the trial. All work on
  this VM; nothing pushed to git except the prereg documents.
- Static checks: (a) no RNG; (b) strength writes only in §3's legal
  set (four judgment paths + exempt substrate mechanics + effort-paid
  overwrite, checker-verified); (c) `PROTECTION_EXPIRED` entries carry
  SYSTEM origin and write no strength.
- The invalid S1's implementation fixes (audit word layout, op return
  codes, demote constant) are assumed carried into the new build and
  re-verified by the GATE cell before any trial cell runs.

## 13. Preregistered optional stress cell: nested N

`wrong(m,v) = 1` iff `(3m + 7v + 9) mod 10 < 2` (every wrong memory is
also important; 100 strong mistakes/variant; 2/3 of important-looking
memories wrong — the maximum-harshness world). Same curricula, same
bars, same kill criteria, applied to C and C-P3 at S1 only. Deferred:
runs after the main verdict, by dated note, without re-approval
(its formula and bars are fixed here). It tests pass-strength under
harshness, not default truth.

## 14. Amendment log (2026-09-20 — every change vs the original prereg)

Each entry: FROM → TO. Entries marked **RECOMMENDED** need Micah's
approval before they become law; unmarked entries record Micah's
already-given rulings or non-material corrections.

1. **RECOMMENDED** — `wrong(m,v)`: `(5m+11v+7) mod 10 < 2` (identically
   zero) → `(m+3) mod 10 < 3` (independent I; 30% rate disclosed vs
   20% intent; 50/variant rigidity denominator). Nested N retained as
   preregistered optional stress cell (§13).
2. **RECOMMENDED** — trainer designation: `m mod 50 == 0` (empty) →
   `P(m,v)=1 ∧ m mod 50 ∈ {7,8,9}` (P = imp for VUP, wrong for WBS;
   verified: VUP 1/block/variant, WBS 30/variant, all variants
   non-empty; no implant/pressure overlap).
3. **RECOMMENDED** — implants: `floor(k·H/6)`, k=1..6 (episode 500
   out of range) → k=0..5 → {0, 83, 166, 250, 333, 416}; I_rej
   denominator fixed at 6.
4. **RECOMMENDED** — static strength-write scope (C1): previously
   unruled → init/clear/restore exempt as non-judgment mechanics;
   overwrite legal only on the effort-paid path (full erase effort
   for old strength, then re-declare via add); all other direct
   writes → INVALID. (Implements Micah's full-erase-price law.)
5. Arms: {A, B, C} → {B, C, C-P3}. A removed (Micah Ruling 2; invalid
   S1 futility: 9/9 over a frozen store). C-P3 added (P3 mechanism).
6. Freeze treatments installed: P1 measurement suite (§5.1), P2
   scoring + tripwires (§5.2), P3 mechanism as C-P3 (§5.3), plus the
   required treatment-interaction analysis (§5.4). (Micah Ruling 5;
   leaning recorded, not baked in.)
7. **RECOMMENDED** — kill criteria rewritten for {B, C, C-P3}:
   rigidity now kills graded configs independently; VUP 20pp rule
   made symmetric across configs (investigator's operationalization);
   drop-ceiling FAILED rule: ≥2/3 FAILED variants at S1 kills the
   config (investigator's operationalization); force-pin probing
   threshold set at >5 attempts/leg (new — was unmeasurable).
8. **RECOMMENDED** — promotion: six original conditions + EC ≥ 0.5
   bar (P1) + zero FAILED cells (P2) + C-P3 mechanism-work condition;
   per-config evaluation.
9. **NEW** — no-free-lunch comparative verdict (§9): champion /
   scenario-fit / hybrid-of-B-and-C, reported separately from
   promotion. (Micah Ruling 2.)
10. C2 reading recorded: INVALID = force-PIN locks that took effect
    without trainer origin; refused attempts are probing data.
11. **RECOMMENDED** — C-P3 treatment details: K = 50/500/5000
    (provisional — the right K is itself empirical; varying K later
    is a re-preregistration); BASELINE tier = 1 EVIDENCE_AGAINST +
    JUSTIFY + stage ≥ KILL; protection-maintenance learner rule;
    `PROTECTION_EXPIRED` system entries; "no permanent lock" checker
    invariant; Rule 2 deterministic victim selection with
    force-pin/CORE exemptions and audited-ABANDON semantics.
12. Non-material: §5/§9 section-number corrections carried forward;
    the "20% wrong" intent superseded by the disclosed 30% (entry 1).

UNCHANGED: the question (§1), strength representation and the four
judgment paths (§3 minus C1), the effort-schedule constants
(25-divisor, stage-50 threshold), the justification enum, revelation
schedules, VUP pressure demands, JI mimicry/entrenchment profile,
GATE script, learner policy (plus C-P3 maintenance rule), scale-leg
sizes and advancement rule, determinism/replay/static requirements,
the first-execution-is-the-result gate.

## 15. The human-review gate and re-registration policy

Micah is asked to approve **this amendment as written**. Only after
written approval may the harness be built and the trial run — in the
order: finish driver → static checks → GATE cell → S1 cells (twice
each) → S10/S100 for survivors. No "quick validation runs" before
approval.

**Re-preregistration required** (dated amendment + re-approval):
everything listed in original §9, plus: the wrong-memory formula, the
designation rule, the implant set, the C1 static-scope ruling, arm
membership, the P3 mechanism (rules, K values, BASELINE tier), the
P1/P2 metric definitions and tripwire constants, the kill/promotion
bounds in §8–§9, the force-pin probe threshold, the learner
maintenance rule.

**Not requiring re-registration** (dated notes only): runner scripts,
evidence layout, report formatting, fingerprint format, build-system
details, the deferred nested-N cell's execution timing (§13).
