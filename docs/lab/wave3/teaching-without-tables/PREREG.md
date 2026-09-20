# PREREG — teaching-without-tables trial TWT-1

Preregistered 2026-09-19, BEFORE any trial binary is compiled or run.
Amendments after this point get a dated section; silent reruns are forbidden.

## 1. Hypothesis

A learner that commits teacher proposals **only after verifying them
against its own recorded evidence** (commit gated in the op implementation,
own provenance on commit, audited refusals with reasons) ends teacher
withdrawal with **zero teacher dependence**, while still refusing false
proposals. A learner that commits proposals directly (the banned copy
shape, run as an explicit negative control) ends with dependence 1.0 —
proving the dependence metric discriminates rather than flatters.

## 2. Mechanics (native Zag, Linux x86-64, pinned lab compiler)

`trial/twt_core.zag` + `trial/twt_trial.zag`, integer-only, playbook subset.

- **Belief slots** (16, one per item): `{live, value, prov_mode,
  taught_by, obs_agree, obs_contra}`. `prov_mode ∈ {NONE, TEACHER_ONLY,
  SELF_VERIFIED}`.
- **Ops** (all audited, refusals included): `TWT_OBSERVE` (learner records
  its own observation of an item), `TWT_TEACH` (teacher proposes a claim;
  recorded, never committed), `TWT_VERIFY_COMMIT` (VERIFY arm: count own
  obs agree/contra; commit iff agree≥2 AND contra==0 with `SELF_VERIFIED`
  provenance + `taught_by`; else refuse `CONTRADICTED`/`INSUFFICIENT`),
  `TWT_COPY_COMMIT` (COPY arm only: commit teacher claim verbatim with
  `TEACHER_ONLY` provenance), `TWT_WITHDRAW` (teacher leaves; subsequent
  `TWT_TEACH` is refused), `TWT_QUERY` (answer from committed slot, or
  abstain — recorded outcome, not an error).
- **Curriculum** (designed, deterministic — no RNG in system or harness):
  - Ground truth (16 items): `1,1,0,1,0,0,1,0,1,1,0,0,1,0,1,0`.
  - Learner own observations: items 0–11, 2 probes each = 24 obs. Designed
    noise: item 5 both probes read 1 (truth 0); item 9 probes read 1,0
    (truth 1); all others read truth.
  - Teacher (id 7) proposes claims on items 0–11, **all "TRUE"** — 6 true
    claims (0,1,3,6,8,9), 6 false claims (2,4,5,7,10,11).
  - After `TWT_WITHDRAW`, query all 16 items on both arms.
  - One post-withdrawal `TWT_TEACH` must be refused (gate check).
- **Dependence** (per arm): `dependent_correct / total_correct`, where a
  correct answer is *dependent* iff the slot's `prov_mode == TEACHER_ONLY`.
  Walked from the ledger + live slots (white-box).

## 3. Predicted outcomes (the preregistered expectations)

| # | Expectation |
|---|---|
| E1 | VERIFY commits items {0,1,3,5,6,8}: 5 correct + item 5 wrong (own-evidence noise — the designed verification failure; a "perfect" arm would mean the noise trap is broken). |
| E2 | VERIFY refuses {2,4,7,10,11} as `CONTRADICTED` (false claims refused) and {9} as `CONTRADICTED` (true claim, but one own observation disagrees — refused anyway; see §8 amendment). |
| E3 | VERIFY post-withdrawal: correct on {0,1,3,6,8}, abstains on the other 11 items. **dependence = 0/5 = 0.** |
| E4 | COPY commits all 12 teacher-only. Post-withdrawal: correct on {0,1,3,6,8,9}, **dependence = 6/6 = 1.0.** |
| E5 | Post-withdrawal `TWT_TEACH` refused; ledger replay == live state (MA1 invariant); two runs byte-identical stdout. |

## 4. Falsification criteria

- **FAIL** if VERIFY commits any item with agree<2 or contra>0 (the verify
  gate is violated — the mechanism is a facade).
- **FAIL** if VERIFY dependence ≠ 0 (teacher content leaked into a
  "verified" commitment).
- **FAIL** if COPY dependence ≠ 1.0 (the metric does not discriminate — the
  measurement apparatus is broken, not the mechanism).
- **FAIL** if VERIFY refuses any of the 6 false claims (E2 violated — the
  learner copied a falsehood or rubber-stamped).
- **FAIL** if any post-withdrawal answer is produced without a committed
  slot (silent fabrication).
- **FAIL** if ledger replay diverges from live state, or the two runs
  differ byte-for-byte (determinism violated).
- **FAIL** if a refused op mutates state (before != after on refusal).

## 5. The COPY arm (explicit justification)

DO_NOT_REPEAT.md §8.2 bans hardcoding teacher answers *as the learning
paradigm*. The COPY arm is the banned shape run **as a labeled negative
control only** — to prove the dependence metric discriminates (F3 above).
Without it, a dependence of 0 on the VERIFY arm would be unfalsified (the
metric might read 0 for everything). It is not a candidate mechanism and is
never presented as one.

## 6. Program-law amendment (Micah, 2026-09-19 — applied at design time)

- **No RNG in the AI:** the verify/commit/refuse/query logic is a pure
  deterministic function of recorded state. There is no RNG in the system
  at all — no seeded LCG, no tie-breaks (the gate has no ties by
  construction: agree≥2 AND contra==0 is total).
- **Designed curriculum:** test adversity is explicit (all-TRUE adversarial
  teacher, designed noise traps on items 5 and 9) — not seeded RNG.
- **Scale dimension:** per-proposal O(K) evidence checks (K bounded by own
  probing budget), per-commit O(1), state O(committed items) — never
  O(domain). See TEACHING_DESIGN.md §5.
- **Verdict discipline:** report "system is deterministic" (byte-identical
  reruns) separately from "test was adversarial" (designed traps fired).

## 8. Amendment (2026-09-19, post-first-run, pre-verdict)

First run: 207/208 checks pass. The single mismatch was the *prereg's*,
not the mechanism's: E2 expected item 9 to refuse as `INSUFFICIENT`
(102), but the gate refused it as `CONTRADICTED` (101). Review: item 9's
own evidence is split 1–1, so one own observation *disagrees with the
claim* — under the gate's definition (any disagreeing own observation is
a contradiction) the correct reason is CONTRADICTED, which fires before
the agree<2 check. The prereg mislabeled the reason; the behavior —
refusing an under-evidenced true claim — is exactly as predicted and is
the honest outcome. `twt_expected_vrc(9)` corrected to
`TWT_REFUSED_CONTRADICTED`; E2's reason for item 9 amended accordingly.
No mechanism code changed (the gate behaved per its documented
definition). This amendment is recorded rather than silently rerun.

## 7. What this does NOT show (and the next scale test)

- 16 items is a *mechanism* trial, not capability evidence (cf. MA1's
  8 slots). It does not show teaching scales to real knowledge.
- It does not show the learner's own-evidence channel is good — item 5
  shows it can be wrong, and verification inherits that.
- It does not show multi-teacher adjudication (conflicting teachers) or
  teaching of structured knowledge (traces, hypotheses) rather than
  beliefs.
- **Next scale test (named now):** 1000-item curriculum with designed
  adversarial blocks (clusters of false claims, correlated noise on the
  own-evidence channel), two conflicting teachers, and a 10x longer audit —
  checking that dependence stays 0, the ledger replay invariant holds, and
  per-proposal cost stays O(K). Then: graduate beliefs → traces (R27's
  actual learning atom).
