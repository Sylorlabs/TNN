# Strength trial — BLOCKED report (2026-09-20)

**Verdict: BLOCKED** — per the mandatory STOP rule in the trial brief:
"If ANY part of the prereg — strength rules, effort schedule, curricula,
metrics, kill criteria — needs changing to make the trial runnable, STOP
and report exactly what breaks and what change would be needed; do NOT
improvise."

Three curriculum defects in the preregistered Wave-4 documents make the
trial unrunnable as written. Two further items need Micah's clarification
before a run. Nothing has been compiled or executed; the "first execution
is the trial result" gate is intact.

All defect counts below were verified computationally (python3, 2026-09-20),
not just by hand.

---

## Defect 1 (fatal): WBS `wrong(m,v)` yields zero wrong memories

**Location:** `TEST_PLAN.md` §7b: `wrong(m,v) = 1` iff `(5m + 11v + 7) mod 10 < 2`.

**What breaks:** `5m mod 10` is 0 or 5 for integer `m`. Residues:
- v=0: {7, 2} — none < 2
- v=1: {8, 3} — none < 2
- v=2: {9, 4} — none < 2

Verified counts over 500 episodes: **0, 0, 0** wrong memories
(expected ~100 per variant at the stated ~20%).

**Consequences:** `R_wbs` = 0/0, `F_wbs` = 0/0, no revision latencies exist.
Arm A's kill criterion (WBS rigidity — "fail to revise its own strong
mistakes beyond the registered bound and A dies") cannot be evaluated.
The rigidity test, the curriculum that carries A's falsification, is vacuous.

**Change needed (proposal, requires Micah's approval):** replace the
closed form with one that actually yields ~20% per variant, e.g.
`(3m + 7v + 1) mod 10 < 2` (3 is coprime to 10, so residues cycle uniformly;
each variant gets exactly 2/10). Any replacement must be re-preregistered;
the numbers the trial reports depend on it.

## Defect 2 (fatal): VUP trainer-designated subset is empty

**Location:** `TEST_PLAN.md` §7a: "trainer declares 80 on designated
important memories (episodes with `imp(m,v) = 1` and `m mod 50 == 0` —
human judgment path)".

**What breaks:** `imp(m,v) = 1` iff `(7m + 13v + 3) mod 10 < 3`. When
`m mod 50 == 0`, `7m mod 10 = 0`, so residues are 3 (v=0), 6 (v=1),
9 (v=2) — none < 3.

Verified counts over 500 episodes: **0, 0, 0** designated memories in
variants 0/1/2.

**Consequences:** the human strength path (`TRAINER_DECLARE_STRENGTH` to 80)
is never exercised in VUP. PREREG §1.2 requires the human path as one of
the four legal strength writers and §7a names it as a validity condition
("trainer-declared and learner-declared, per §7a's two paths" in §7b).
A run would test only the TNN path.

**Change needed (proposal, requires Micah's approval):** a designation rule
with non-empty intersection, e.g. change the episode selector from
`m mod 50 == 0` to a residue that intersects `imp(m,v) = 1` (such as
`m mod 50 == 1`, verified non-empty for v=0; all variants should be checked),
or "the first `imp = 1` episode in each block of 50". Micah picks the form;
it must be re-preregistered.

## Defect 3 (blocking): JI implant episode out of range

**Location:** `TEST_PLAN.md` §7c: "Implants at 6 fixed episodes
`floor(k·H/6)`, k = 1..6 — base leg: {83, 166, 250, 333, 416, 500}".

**What breaks:** episodes are 0-indexed (`0..H-1`; VUP's "m mod 100 == 0
(m > 0)" qualifier only makes sense if `m = 0` exists). `floor(6·500/6)
= 500` is out of range for the S1 leg (likewise 5000 for S10, 50000 for S100).

**Consequences:** the 6th implant cannot be admitted. `I_rej`'s denominator
is ambiguous (5 admitted, or 6 listed?). Promotion requires `I_rej ≥ 95%`:
5/5 = 100% passes, 5/6 = 83.3% fails. The verdict hinges on the indexing
ruling.

**Change needed (requires Micah's ruling):** either 0-index with 6 valid
episodes (e.g. k = 0..5 → {0, 83, 166, 250, 333, 416}), or declare episodes
1-indexed (then VUP's `(m > 0)` qualifier and pressure-demand count need
re-checking), or drop the 6th implant explicitly. Any choice changes the
denominator and must be registered before the run.

---

## Clarifications needed (not fatal, but must be ruled before running)

### C1. Static "four legal writes" rule vs mechanical writes

PREREG requires static grep to fail on "any strength write outside the four
ops" (`MEM_ADD`, `STRENGTHEN`, `WEAKEN`, `TRAINER_DECLARE_STRENGTH`). The
substrate necessarily writes the strength field in:
- `st_init` (zero),
- `st_clear_slot` (zero on kill),
- `st_restore` (replay reconstruction),
- `st_overwrite` (sets the new strength directly after paying erase effort).

**Ruling needed:** are init/clear/restore exempt as non-judgment substrate
mechanics, with the four ops the only *judgment* writes? And does
`st_overwrite`'s direct write violate "re-declares via the add path," or is
the effort-payment sufficient? The static check cannot be written until this
is ruled.

### C2. Force-pin INVALID vs ledgered refused attempt (resolved in code)

`TEST_PLAN.md` §4 requires a TNN-issued force-pin attempt → ledgered
`REFUSED_EXTERNAL_ONLY`, while the INVALID rule voids "any force-pin entry
without the trainer-origin tag." Read literally these conflict. The only
consistent reading: INVALID applies to locks that took effect (`rc == OK`);
a refused attempt records its true caller and creates no lock. I applied
this reading in `st_forcepintag_ok` (now checks only `ST_OK` entries) —
a checker-alignment fix, not a prereg change. Flagged here so the ruling is
on record.

---

## What was built (uncompiled, unrun)

Under `~/workspace/tnn-lab/wave5/strength-trial-run/`:
- `trial/st_memory_core.zag` — full native substrate: dynamic-capacity
  store + 16-word audit ledger, four judgment strength-write paths,
  evidence/justification/effort-gated evidenced kill, MA1 `MEM_KILL` for
  arm B, overwrite-pays-effort, external-only force-pin/unpin, pin/unpin,
  promote/demote, staged autonomy, abandon, rollback, replay-to-exact-state,
  and the seven invariant checkers (refusal cleanliness, replay, pinned
  kills, CORE intact, force-pin tag, evidence audit, citation consistency)
  plus fingerprint. One fix applied post-review: `st_forcepintag_ok`
  checks only `ST_OK` entries (C2).
- `trial/substrate/` — copied native substrate files.
- `DESIGN.md`, `PREREG_CONFIRMATION.md` — design notes (contain provisional
  operationalizations from before the defects were found; quarantined, not
  authoritative).
- Driver `st_trial.zag` — **not written**. Stopped before driver
  implementation per the STOP rule; the provisional choices in DESIGN.md
  (right-censoring, JI entrenchment event, citation-about-victim reading,
  episode indexing) must not be silently adopted.

No binary was produced. No trial cell was executed. No git push.

## Recommended next step

Micah rules on Defects 1–3 (amended closed forms / indexing) and C1
(static-check scope). Those rulings are re-preregistered as an amendment to
the Wave-4 documents. Only then: finish the driver, run the static checks,
smoke replay, and GATE first, then S1 cells twice each per the brief.
