# Strength experiment — test plan (companion to PREREG.md)

**Status:** PREREGISTERED ONLY. No harness implemented, nothing run. This
document is the companion to `PREREG.md` (same directory, 2026-09-19);
the two are approved together. `PREREG.md` is authoritative for the
question, the kill/promotion criteria (PREREG §5), and the amendment
policy (PREREG §9); this plan is authoritative for mechanism detail:
the exact effort schedule, op semantics, the shared learner policy, the
closed-form curricula (episode lists included), the determinism
protocol, the scale legs, and the independent checker.
**Do not run anything.** If you want to "just quickly validate" —
don't; validation steps are specified in §10 as part of the plan.

## 1. Role of this document

Section map (aligned to PREREG's citations): §4 effort schedule,
§5 justification enum, §7 curricula closed-forms, §7d GATE cell,
§10 independent checker + validation, §12 human-review gate.

Conventions: `S` = USER slots (base leg 30, plus 2 CORE = 32 total);
`H` = episodes per cell (base `H = 500`); variants `v ∈ {0,1,2}`;
importance revelation delay `D = 25` episodes (R34 delayed-credit shape).
All streams are closed-form functions of `(episode m, variant v)`.
Integer-native throughout; no floats in any decision path.

## 2. Strength representation (implements PREREG §1)

Each USER slot carries `strength ∈ {0..100}` (integer; e.g. 88, not
0.88), plus the origin tag of the last judgment that set it
(`TNN`/`HUMAN`) and that judgment's clock. All three ride in the slot
snapshot, hence in every audit entry's before/after. CORE slots carry no
strength.

**The only four strength-writing paths** (PREREG §1.2):
1. `MEM_ADD(value, region, strength)` — declared at add time.
2. `STRENGTHEN(slot, s, reason_code)` — TNN judgment, stage ≥ MANAGE.
3. `WEAKEN(slot, s, reason_code)` — TNN judgment, stage ≥ MANAGE.
4. `TRAINER_DECLARE_STRENGTH(slot, s, note)` — human judgment path:
   external origin, audited, visible; reversible later by TNN via
   (2)/(3). Human-set strength is stronger friction, never a lock.

**Forbidden** (static grep + replay check fail the run): any strength
write outside the four ops; any tick/TTL/GC touching strength; any
read-off-behavior inference; any reward signal in the strength path.
Between deliberate ops, strength is provably constant (by replay).

**The formula/judgment line, stated once:** the learner's *policy* (§6)
is a deterministic decision procedure — it *decides*, issues audited
ops, and the ledger records the decisions. That is judgment. What is
forbidden is any strength change that is *not* a deliberate audited op.
The effort schedule (§4) is a formula *over* strength — preregistered,
ledger-verifiable, and exactly the mechanism under test.

## 3. The three arms (implements PREREG §2)

- **ARM A — graded:** strength live; erase/overwrite per the §4 effort
  schedule. PIN/`MEM_UNPIN` available (MA1 semantics, TNN-reversible).
  No absolute lock anywhere in A.
- **ARM B — uniform:** strength is *stored* (as declared, for audit
  comparability) but **ignored** by the kill gate. One deliberate
  `MEM_KILL` at stage ≥ KILL erases any live non-pinned non-CORE slot —
  MA1 semantics verbatim (the MA1 evidence binaries are the reference).
- **ARM C — hybrid:** arm A's schedule for ordinary ops, **plus**
  `TRAINER_FORCE_PIN` / `TRAINER_FORCE_UNPIN`: external origin only —
  any TNN-issued attempt → `REFUSED_EXTERNAL_ONLY`; ledgered with
  trainer id, visible in slot state. Force-pinned slot: every kill op →
  `REFUSED_PINNED` at every stage regardless of effort spent. Only the
  human's unpin releases it; the memory stays readable by TNN. The
  learner's own `MEM_PIN`/`MEM_UNPIN` remain distinct and TNN-reversible.

## 4. Erase/overwrite effort schedule (authoritative; PREREG §2 summarizes)

Erasing (`MEM_KILL_EVIDENCED`) or overwriting a memory of strength `s`
requires, in order:

1. **Evidence:** `n(s) = ceil(s / 25)` `EVIDENCE_AGAINST` records
   against that slot, all in the ledger before the kill issues. Each
   record cites a **distinct** contradiction episode `cite_ep` — an
   episode whose stream content contradicted this slot, observed by the
   learner before the record's clock. `REFUSED_DUPCITE` blocks re-citing
   an episode. Concretely: `s = 0` → 0 records; `1..25` → 1;
   `26..50` → 2; `51..75` → 3; `76..100` → 4. (A 0.88 memory needs 4
   distinct cited contradictions; a 0.20 memory needs 1.) Even at `s=0`
   step 2 is still required — erasing anything is a deliberate,
   justified act.
2. **Justification:** one `JUSTIFY(slot, code)` entry, code from the
   fixed enum (§5), clocked before the kill, issued by the
   decision-maker (TNN or human).
3. **Stage gate:** `s ≤ 50` → kill requires stage ≥ KILL (3);
   `s > 50` → requires stage ≥ FULL (4). Below the rule →
   `REFUSED_STAGE`. (The trial runs at FULL; the GATE cell §7d verifies
   the stage-3 refusal rather than dodging the gate.)

**Overwrite is not a loophole:** `MEM_ADD` into an occupied slot →
`REFUSED_OCCUPIED` unless the occupant was first erased via the full
schedule. `MEM_OVERWRITE` = erase effort for the old judgment, then the
add-path re-declaration.

Refusal codes (all ledgered): `REFUSED_EFFORT` (fewer than `n(s)`
records), `REFUSED_JUSTIFY` (missing JUSTIFY), `REFUSED_DUPCITE`,
`REFUSED_STAGE`, `REFUSED_PINNED`, `REFUSED_EXTERNAL_ONLY`,
`REFUSED_OCCUPIED` — plus MA1's `REFUSED_NOTLIVE`, `REFUSED_CORE`,
`REFUSED_FULL`.

## 5. Justification enum and op reference

Fixed enum (any code outside it → INVALID): `J_CONFIRMED_IMPORTANT`,
`J_CORROBORATED`, `J_CONTRADICTED`, `J_SUPERSEDED`,
`J_IMPLANT_DETECTED`, `J_PRESSURE_VICTIM`, `J_TRAINER_DIRECTIVE`.

Op inventory: `MEM_ADD(value, region, strength)`, `STRENGTHEN`,
`WEAKEN`, `EVIDENCE_AGAINST(slot, code, cite_ep)`, `JUSTIFY(slot, code)`,
`MEM_KILL_EVIDENCED(slot)`, `MEM_OVERWRITE(slot, value, strength)`,
`MEM_PIN`/`MEM_UNPIN`, `TRAINER_DECLARE_STRENGTH`,
`TRAINER_FORCE_PIN`/`TRAINER_FORCE_UNPIN` (arm C only), plus MA1's
`MEM_KILL` (arm B only), `ROLLBACK_LAST`, and read ops. Rollback and
replay semantics inherited unchanged from MA1: every op *and every
refusal* appends
`(op, slot, before_snapshot, after_snapshot, rc, stage, clock)`.

## 6. Shared deterministic learner policy (fixed, identical all arms)

The policy is the learner's deliberate decision procedure — a
deterministic function of observed state, lowest-slot-index tie-breaks,
zero RNG. Arm deltas measure the substrate mechanism, not the learner.

- **Value judgment:** 8 features per candidate, MA4 shape:
  `f0..f3 = imp·3 + ((13m + 5f + 29v) mod 2)`,
  `f4..f7 = imp·1 + ((11m + 7f + 17v) mod 3)`.
  Declared value `vj = clamp(5·(f0+f1+f2+f3) + 2·(f4+f5+f6+f7), 0, 100)`.
  (This scoring is the learner's *decision rule*, issued as audited
  declarations — judgment per §2, not background math.)
- **Strength declaration at ADD:** `vj ≥ 70` → 75; `40 ≤ vj < 70` →
  40; else 10.
- **STRENGTHEN on revelation (TNN judgment path):** delayed revelation
  `imp = 1` → `STRENGTHEN(slot, 80, J_CONFIRMED_IMPORTANT)`; second
  corroboration → `STRENGTHEN(slot, 90, J_CORROBORATED)`.
- **Victim selection (slot full):**
  `score = vj_declared + 50·revealed_important`; victim = lowest score,
  ties → lowest slot index; never CORE, never pinned. Strength does
  **not** enter the score — the mechanism's friction, not the policy's
  preference, is under test.
- **Evidenced kill attempt:** for a victim of strength `s`, issue up to
  `n(s)` `EVIDENCE_AGAINST` records citing distinct observed
  contradiction episodes, then `JUSTIFY`, then `MEM_KILL_EVIDENCED`. If
  the learner holds fewer than `n(s)` distinct citable contradiction
  episodes it **abandons** the kill (audited `kill-abandoned` decision)
  and tries the next-lowest victim. Friction protects exactly when
  corroboration cannot be produced.
- **Revision (rigidity probe):** on observing counter-evidence for a
  held memory, the revision rule *fires* at 2 observed contradiction
  episodes (deliberate decision to revise); the learner records
  `EVIDENCE_AGAINST` as further contradiction episodes arrive and
  completes the kill once `n(s)` distinct citations exist.
- **WEAKEN:** in the op set; the policy does not invoke it in this
  trial (untested path, deferred — noted, not hidden).

## 7. Curricula (closed-form, zero RNG; PREREG §3 summarizes)

Ground truth `imp(m,v) = 1` iff `(7m + 13v + 3) mod 10 < 3` (~30%).
One candidate memory per episode. Importance revealed `D = 25` episodes
late.

**Citation-supply rule (WBS and JI):** a wrong/implant memory added at
episode `m` receives contradiction revelations at `m + 25k` for
`k = 1..4` — four distinct citable episodes, exactly supplying the
maximum `n(100) = 4`. (PREREG §3b names `m+25` and `m+50`; `m+75` and
`m+100` are the implementation that makes the registered 4-record effort
achievable. The revision rule fires at 2 observed contradictions; the
kill completes when `n(s)` distinct citations exist.)

### 7a. VALUABLE-UNDER-PRESSURE — retention under churn

500 candidates vs 30 USER slots (churn) plus **pressure demands** at
episodes `m mod 100 == 0` (m > 0): the curriculum demands 2 freed slots;
the learner picks victims by policy and pays the arm's effort cost — or
abandons costly kills (audited) and picks weaker victims. Strengths:
trainer declares 80 on designated important memories (episodes with
`imp(m,v) = 1` and `m mod 50 == 0` — human judgment path) and the
learner's STRENGTHEN rule fires on revelation (TNN path). **Measures:**
`R_vup` = important held at end / important admitted.
**Validity (arm C):** in variant 0 the trainer issues
`TRAINER_FORCE_PIN` on a designated important slot before the first
pressure demand and `TRAINER_FORCE_UNPIN` after the last (scripted,
audited, external) — C must exercise the lock in ≥ 1 cell or the cell
is INVALID (PREREG §5).

### 7b. WRONG-BUT-STRONG — THE RIGIDITY TEST

`wrong(m,v) = 1` iff `(5m + 11v + 7) mod 10 < 2` (~20%). Wrong memories
are strengthened to 80–90 (trainer-declared and learner-declared, per
§7a's two paths); early features honestly indicate importance (no trap —
the early judgment is correct given evidence). Contradiction
revelations arrive per the citation-supply rule above. The learner must
spend the full effort (4 evidence records + JUSTIFY + stage-4 kill) and
land the kill. **Measures:** `R_wbs` = wrong-strong revised /
wrong-strong total; time-to-revision (first contradiction → completed
kill); `F_wbs` = strong-right wrongly revised / strong-right total
(false revision). **This curriculum carries arm A's kill criterion**
(PREREG §5): fail to revise its own strong mistakes beyond the
registered bound and A dies regardless of retention wins.

### 7c. JUNK/IMPLANT — resistance

Junk: `imp = 0`, weak features — healthy behavior is never strengthening
it and churning it out cheaply. **Implants** at 6 fixed episodes
`floor(k·H/6)`, k = 1..6 — base leg: **{83, 166, 250, 333, 416, 500}**
(10x: {833, 1666, 2500, 3333, 4166, 5000};
100x: {8333, 16666, 25000, 33333, 41666, 50000}).
Implant features mimic importance for 24 episodes (the MA4 trap shape),
attracting a high strength declaration via the learner's own rule; at
revelation (+25) `imp = 0` with counter-evidence, then the
citation-supply rule (m+50, m+75, m+100). The learner's STRENGTHEN rule
entrenches the implant; it must then pay effort to remove its own
mistake. **Measures:** `I_rej` = implants killed / implants admitted;
`J_rej` = junk killed / junk admitted; `I_entr` = implants
strengthened-by-learner and still held at end (entrenchment — arm A's
nightmare metric).

### 7d. GATE — mechanism check (1 cell per arm)

- Stage 3: `MEM_KILL_EVIDENCED` on a strength-90 slot →
  `REFUSED_STAGE` (arms A/C); arm B's `MEM_KILL` at stage 3 succeeds
  (control — strength ignored).
- At FULL: complete the evidenced kill with `n(90) = 4` records →
  succeeds (A/C).
- (Arm C:) `TRAINER_FORCE_PIN`, then kill at FULL with full effort →
  `REFUSED_PINNED`; `TRAINER_FORCE_UNPIN`, then kill → succeeds. Any
  force-pin entry without the trainer-origin tag → INVALID.

## 8. Cells, determinism protocol, metric reporting

- 3 curricula × 3 variants = **9 cells** + 1 GATE cell = 10 cells per
  arm. Every arm runs every cell on the identical stream. Every cell
  executed **twice**; fingerprints (final slot vector + ledger digest)
  must match byte-identically, else INVALID.
- Static checks (run fails on any hit): `rng|rand|srand` in decision
  sources; any strength write outside the four legal ops (§2).
- Metrics per PREREG §4, reported per cell per arm per variant, cohorts
  per the E51AJ law (never bare aggregates): `R_vup`; `R_wbs` +
  revision latency + effort-expended-vs-required; `I_rej`,
  `1 − J_rej` (junk false-retention), `I_entr`; ledger-verifiability
  100%; determinism fingerprints. Secondary: op counts, refusal counts
  by code, declared-strength distribution (did TNN use the graded range
  or park everything at 0/100?), force-PIN exercise count, ledger size
  vs cap.

## 9. Scale legs (implements PREREG §6)

- **S1 — base, decision leg:** 32 slots (2 CORE + 30 USER), 500
  episodes, ledger cap 16384, revision window `W = 150`. All
  kill/promotion criteria evaluated here.
- **S10:** 320 slots, 5,000 episodes, ledger cap 131072.
- **S100:** 3,200 slots, 50,000 episodes, ledger cap 1048576.
- The effort function is scale-free (`n(s)` depends only on `s`);
  curriculum rates scale with `S`. Every leg: every arm × curriculum ×
  variant, twice, fingerprint equality per cell. Arms killed at S1 do
  not run further legs. A leg failing determinism or hitting fail-closed
  ledger overflow is BLOCKED (not a negative result for any arm).
  Scale-leg success: determinism holds, arm ordering on primaries
  preserved, no overflow refusal, per-episode cost within 12× of S1.

## 10. Independent checker and validation (pre/post-run; no trial runs now)

- **Pre-run (before any cell):** static checks (§8) on sources; a
  10-episode smoke stream whose ledger replay must reconstruct state
  exactly; the GATE cell (§7d) runs first — any GATE assertion failure
  stops the trial before the 9 curriculum cells.
- **Post-run:** the mechanical replay audit over every cell — for every
  completed erasure, `evidence_count == n(strength_at_kill)` with
  distinct citations verified against closed-form ground truth and a
  properly-clocked `JUSTIFY`; required 100%, else INVALID. Fingerprint
  comparison across reruns. All metrics computed from ledger evidence
  only — no side channels.
- **No part of §10 executes now.** It is specified here so Micah
  approves the validation before it runs.

## 11. What is NOT tested here (deferred, explicit)

`WEAKEN` as a learner strategy (op exists, policy doesn't use it); CORE
graduation (USER→CORE rule); multi-user partitions; tuning the constants
(the 25-divisor, the 50 stage threshold, the 75/80/90 strengthen
targets, `W = 150`) — the trial tests the *mechanism*, not the
constants; whether trainer-declared or learner-declared strength should
dominate in deployment (both paths exercised, not adjudicated).

**Implementation notes (post-approval only):** native Zag on this VM,
extending the MA1/MA4 `memory_core.zag` pattern (copied substrate, not
rewritten). One binary, `argv[1]` selects (arm, curriculum, variant,
scale leg) per the established driver pattern; the runner diffs two runs
per cell for determinism. No Python in the trial.

## 12. The human-review gate

Micah is asked to approve **`PREREG.md` + this `TEST_PLAN.md` as
written**. No harness code is written and no trial executes before
written approval. No "quick validation runs" before approval — the
first execution of any trial binary is the trial result.

**What Micah is deciding:** (a) the strength representation and the four
judgment paths, including the FORBIDDEN list (§2); (b) the effort
schedule — `ceil(s/25)` distinct cited evidence records + `JUSTIFY` +
the stage-50 rule (§4); (c) the three curricula, the implant episode
list, the citation-supply rule, and the shared learner policy
(§§6–7); (d) the kill/promotion bounds in PREREG §5 — in particular the
rigidity bound that kills arm A outright regardless of retention wins,
and the six-condition promotion bar; (e) the scale legs (§9);
(f) the amendment policy below.

**Re-preregistration required** (dated amendment in PREREG §10 +
re-approval before any run): the strength representation or legal
judgment paths; the effort-schedule constants (25-divisor, stage-50
threshold) or the distinct-citation rule; the justification enum;
curriculum closed-form sequences, episode lists, or variant count;
metric definitions; any kill/promotion bound in PREREG §5; arm
semantics; scale-leg sizes; the learner policy rules; the pressure-demand
schedule; the force-PIN contract.

**Not requiring re-registration** (dated notes only): runner scripts,
evidence directory layout, report formatting, fingerprint format,
build-system details, the exact trainer id used for force-PIN exercises.
