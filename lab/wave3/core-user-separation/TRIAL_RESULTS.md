# SEP1 trial results — 2026-09-19

Native Zag, Linux x86-64, `znc 2026.07.0-dev` (pinned lab compiler).
Runner: `trial/run_sep.sh` (compiles, runs twice, requires byte-identical
stdout, verifies every CL_CHECK). Evidence: `trial/EVIDENCE_20260920T002048Z/`.
Binary `sep_trial_linux` removed after the run; the runner rebuilds it.

## Result: 127/127 checks pass, `MA_FAILURES,0`, exit 0 — PREREG CONFIRMED.

Determinism: run1 and run2 stdout byte-identical (`determinism=OK`).
The system contains no RNG in any decision path, and the harness used none
either — the adversary was a fully designed sequence. "The system is
deterministic" (byte-identical reruns) is established separately from
"the test was adversarial" (designed contradiction/injection attempts).

## What the trial proves (PREREG H1–H6)

- **H1 — promotion is verified logic, not a threshold.** Two promotions
  succeeded, each requiring: stage FULL, candidate owned by the session
  user, candidate tier LONG, a witness with a *disjoint* owner + same key +
  same value, and zero live contradictions across CORE and all USER
  partitions. Every clause is an equality/quantifier check — no scores, no
  cutoffs, no RNG.
- **H2 — no unilateral CORE write path.** `ADD(region=CORE)` →
  `REFUSED_COREWRITE` (twice, incl. the owner-spoof variant); `PIN`/`PROMOTE`
  (tier)/`UNPIN` on CORE → `REFUSED_CORE`; `KILL` on CORE → `REFUSED_CORE`
  from both a stranger and the originating user. All refusals audited, all
  states byte-identical after refusal (I1).
- **H3 — conflicts live in USER partitions and block CORE.** Carol's live
  `(k=7,v=2)` blocked Alice's corroborated `(k=7,v=1)` promotion with
  `REFUSED_CONTRADICTED` (contradicting slot id recorded in the audit's aux
  field); after Carol's *deliberate* KILL of her own slot, the same
  promotion succeeded. Later, a corroborated `(k=7,v=9)` was refused
  because CORE already held `(k=7,v=1)` — first corroborated fact holds the
  key (base behavior; the revision/supersession gate is specified next
  work, not trialed).
- **H4 — forget semantics.** Own-partition KILL works (Carol, Bob, Alice);
  cross-partition KILL → `REFUSED_SCOPE`; CORE KILL → `REFUSED_CORE` even
  for the originating user; forgetting your USER copy of a promoted fact
  leaves the CORE copy intact.
- **H5 — ledger invariants end-to-end.** I1 refusals-never-mutate, I2
  replay-to-exact-state (incl. owners, keys, session user), I3 CORE purity
  (every after-region=CORE entry is COREWRITE immediately following a
  PROMOTECORE-OK naming the same candidate), I4 cross-user isolation —
  all hold over the full 60-entry ledger. Exact entry count asserted (60).
- **H6 — determinism.** Byte-identical reruns (see above).

## Refusal-path battery (all named codes, all audited)

`REFUSED_STAGE` (ADD at NONE; PROMOTECORE at KILL), `REFUSED_FULL`
(capacity), `REFUSED_COREWRITE`, `REFUSED_SCOPE` (ADD/KILL/PIN as another
user), `REFUSED_NOTLONG` (promotion before LONG tier), `REFUSED_UNCORROBORATED`
(dead witness / self witness / key-mismatched witness), `REFUSED_CONTRADICTED`
(live USER contradiction; CORE contradiction), `REFUSED_CORE`,
`REFUSED_NOTLIVE`. Rollback of a USER demote restores LONG tier; rollback
structurally skips PROMOTECORE/COREWRITE (gate writes are not reversible
by the learner).

## What it does NOT show (per the prereg)

- Scale: CAP=256, ≤6 partitions, ~60 ops. The scaling argument
  (audited key-index, partition-count independence, horizon independence,
  scale-free promotion logic) is in SEPARATION_DESIGN.md §7 — argued, not
  proven. Next scale test specified there.
- Trace-replay witness, supersession/revision gate, stage-4 unlock
  curriculum, key-index: specified in the design doc, not trialed.
- Judgment quality (which memories *deserve* promotion) — values/keys are
  protocol-fixed; this proves the *gate machinery*, not taste. Same
  honest boundary as MA1.

## Notes for future agents

- Two bugs were found and fixed during the run (both in trial/check code,
  not the mechanism): a byte-offset typo reading slot 4's value, and the
  CORE-purity scan misreading SETSTAGE/SETUSER entries (they store
  stage/user in snapshot-word positions). Fixed in `sep_trial.zag` /
  `sep_core.zag`; rerun is the passing one above.
- `sep_promotecore` audits TWO entries on success (PROMOTECORE naming
  candidate+witness, then COREWRITE naming new-slot+candidate) — this is
  what makes I3 checkable.
- On `REFUSED_CONTRADICTED`, the audit aux field carries the contradicting
  slot id (not the witness) — the conflict is a first-class audited object.
- Refusal precedence inside ops is documented in SEPARATION_DESIGN.md §9
  and exercised by the trial (e.g. COREWRITE checked before SCOPE in ADD).
