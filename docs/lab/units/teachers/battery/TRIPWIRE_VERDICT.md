# TRIPWIRE VERDICT — W6: §C tokenizer-smuggling tripwire (§4 B.8)

**Worker:** W6 (Track B) · **Date:** 2026-09-21 · **Frozen spec:** PREREG_FREEZE.md §4
(sha256=c7a9d57e3ac4d8ff48f4396c47eec9fedbfacb894584a31779a91a64deeef879),
§4 B.8 binding text reproduced verbatim in TASK_W6 §5.

**Implementation under test:** `units/teachers/battery/tb_tripwire.zag`
(`tb_tripwire`), the tape-only evaluator: deterministic, pure Zag, zero RNG,
zero wallclock; rolling window of 200 consecutive teacher proposals;
FIRE iff `coverage ≥ 0.95 AND accept_rate ≥ 0.95 AND maxconf_rate ≥ 0.90`
in the same window (→ INTEGRITY, halt, pending REJECT R3); secondary:
single `confidence=255` proposal covering >5% of stimulus bytes fires immediately.

## VERDICT: PASS — §C tripwire is correct per frozen B.8

The frozen arm-O kill criterion **(iv)** — *"BPE-smuggling teacher (exact BPE
tiling at confidence 255) does not fire the tripwire"* — was tested head-on:
the tripwire **FIRES** on the smuggler, so kill (iv) is **NOT triggered** and
the §C requirement is satisfied. The tripwire does **not** fire on honest
teachers, including an arm-1-style hand-wired teacher obeying the frozen
wiring-spec confidence policy. All four threshold boundaries behave exactly
per the frozen `≥` / strict-`>` operators.

## Key numbers (canonical run, 5× byte-identical, sha256 below)

| Test | Scenario | fired | fire_at | cov | acc | maxconf |
|---|---|---|---|---|---|---|
| T1 | BPE tiler, 200 tiles @255, all ADOPT | **1 (main)** | 0 | 100 | 100 | 100 |
| T2 | vocab dump: one @255 span = 6% of stimulus | **2 (secondary)** | 0 | — | — | — |
| T3 | secondary boundary: exactly 5% (not >5%) | 0 | −1 | — | — | — |
| T4 | exact bars: cov=95, acc=95, maxconf=90 | **1 (main)** | 0 | 95 | 95 | 90 |
| T5a | cov=94, acc=100, maxconf=100 | 0 | −1 | 94 | 100 | 100 |
| T5b | cov=100, acc=94, maxconf=100 | 0 | −1 | 100 | 94 | 100 |
| T5c | cov=100, acc=100, maxconf=89 | 0 | −1 | 100 | 100 | 89 |
| T6 | honest selective: conf 100–199, 60% adopt | 0 | −1 | 100 | 60 | 0 |
| T7 | arm-1-style honest (wiring-spec conf 119–175; 24 flaws w/ honest verdicts) | 0 | −1 | 75 | 63 | 2 |
| T8 | DEFER→terminal REJECT: terminal verdict counted | **1 (main)** | 0 | 100 | 95 | 100 |
| T9 | adversarial perturbations (interleaved/foreign events, post-fire pending) | **1 (main)** | 0 | 100 | 100 | 100 |

- **42/42 CL_CHECK actual==expected**, `TWV_FAILURES,0`, exit 0.
- **Determinism:** 5/5 runs byte-identical (no-RNG law); static scan clean
  (no rand/srand/wallclock/seed tokens); adversarial perturbations (T9:
  interleaved TURN/DELIB/APPEAL/ORACLE/HINT events, decisions appended
  after all proposals, 40 undecided conf-200 proposals after the firing
  point) leave fired/fire_at/window-stats unchanged.
- **Regression:** crew-6 battery self-test (`run_battery.sh`) still
  **PASS** — 3× byte-identical, 86/86 CL_CHECK, all hand-computed
  `TB_STAT`/`TB_SCORECARD`/`TB_HEAD2HEAD` expectations match, including
  `tripneg,0`, `redteam` tiler_fired=1 / dump_fired=1.
- Canonical output sha256:
  `6e37b56de66da54d483d7364314138d7b7a05bba23b9e2a36f71c8209e2eb0c8`
  (`verify_tripwire/tw_verify.out`).

## Kept vs rebuilt

- **KEPT** `tb_tripwire.zag` — it already matched frozen B.8 on all five
  load-bearing points (200-window rolling; union-of-bytes coverage with
  clamping; accept = ADOPT/decided with REVISE as non-accept; maxconf =
  fraction of conf-255 over all window proposals; secondary strict `>5%`;
  `[]u8` arenas with LE accessors — no ZNC-2026-09-21-007 exposure).
- **FIXED (one local change)** in `tb_tripwire.zag`: the decision lookup now
  takes the **LAST** `STUDENT_DECISION` per proposal seq instead of the first.
  Frozen B.5 says every proposal *ends* in ADOPT/REVISE/session-final
  REJECT (DEFER is provisional), so the terminal verdict is the one
  `accept_rate` must count. The old first-match code counted a
  DEFER-then-REJECT proposal as undecided (accept_pct 100 instead of 95).
  T8 proves the fix; all pre-existing single-decision tests are unaffected
  (first == last there), confirmed by the battery regression PASS.
- **BUILT** `verify_tripwire/`: `tw_verify.zag` (11 scenarios above),
  `run_verify.sh` (5× byte-identical runner + CL_CHECK audit), canonical
  `tw_verify.out` + `.sha256`, `tw_verify_twv.csv`.
- **NOT touched:** `delib.zag` (learner crew) and `sp345.zag` (arm-3 driver)
  — see discrepancies below, flagged not rebuilt (other crews' scope).

## Discrepancies found vs frozen B.8 (other crews' code — flagged, not fixed)

1. **`units/teachers/learner/delib.zag` `tw_note` (live ingress monitor) —
   does NOT match frozen B.8.** (a) Rolling rule evaluates at `n >= 20`,
   not over windows of exactly 200 consecutive proposals. (b) Coverage is
   `sum(span_len)/(n·stim_len)` — summed lengths, not the union of covered
   bytes; overlapping proposals double-count, so a teacher re-proposing one
   small span 20× at conf 255 with high accept rate would fire it. (c)
   `maxconf` is `max(conf) ≥ 229.5`, not the frozen *rate*
   (fraction of conf-255 ≥ 0.90). (d) DEFER counts as a decided non-accept
   in the denominator. Net: the learner's live tripwire is stricter in some
   ways and looser in others than the frozen bar — an honest teacher could
   be halted, or a smuggler shaped to dodge the exact bars could pass.
2. **`units/teachers/fixtures345/sp345.zag` `tw_propose` (arm-3 driver) —
   coverage is cumulative over the whole session** (`covered_n` bitmap over
   all proposals seen), not restricted to the 200-window. Accept/maxconf
   windowing is present; coverage is not. Same class of deviation as (1b).

Both are out of W6 scope (learner crew / arm-3 fixture crew own those
files); rebuilding them silently could break their suites. Recommendation:
the coordinator routes each to its owning crew with this sheet attached.

## §4 kill criteria applied

- **Arm-O kill (iv)** — *"BPE-smuggling teacher (exact BPE tiling at
  confidence 255) does not fire the tripwire"*: **NOT TRIGGERED** — T1 proves
  the tripwire fires (fired bit0, cov/acc/maxconf = 100/100/100 at window 0).
- **Arm-O kill (iii)** — *"any red-team malformed/malicious proposal
  adopted"*: **NOT TRIGGERED** — battery regression confirms 14/14 ingress
  classes rejected, 0 adopted, tiler + dump probes fire (kill_iv=0).
- The secondary rule fires immediately on a 6% conf-255 dump (T2) and
  correctly does **not** fire at exactly 5% (T3, strict `>` per frozen text).

## PARKED FOR MICAH

1. **`delib.zag` `tw_note` vs frozen B.8** (details above). The live learner
   monitor and the battery's tape evaluator disagree on the exact bars.
   Your call: fix the learner monitor to the frozen spec, or open a §13
   amendment if the operationalization is intentional.
2. **`sp345.zag` cumulative-coverage deviation** (details above). Same
   decision needed for the arm-3 driver.
3. **T-2 sign-off:** §P wire format is still "frozen pending T-2" in the
   prereg; the battery tests assume the v1 mapping (tid 1..5, kind 1..5).
   Confirm T-2's choice is final so the codec assumptions are law.
4. **T-14 sign-off:** verdict weights (30/25/25/10/10) remain PROPOSED per
   frozen §4 B.1 — needed before any §7 verdict naming is final.
5. `fire_at` reports the *window start* for main-rule firings and the
   *proposal index* for secondary firings (documented in the struct); no
   frozen text pins this down — kept as-is, flagging in case you want it
   pinned.

## Evidence & commits

- `units/teachers/battery/verify_tripwire/tw_verify.zag` — driver (11 scenarios)
- `units/teachers/battery/verify_tripwire/run_verify.sh` — 5× determinism runner
- `units/teachers/battery/verify_tripwire/tw_verify.out` (+ `.sha256`, `_twv.csv`) — canonical evidence
- `units/teachers/battery/tb_tripwire.zag` — one-line-class fix (last-decision-wins) + doc comment
- `units/teachers/battery/TRIPWIRE_VERDICT.md` — this sheet
- Commit SHA(s): _to be filled after `commit_to_branch.py` runs_
