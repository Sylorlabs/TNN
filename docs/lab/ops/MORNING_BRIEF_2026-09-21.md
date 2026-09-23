# Morning brief — 2026-09-21 (written ~01:15, updated as the night progresses)

## Done overnight

- **Track B arm-1 teacher: finished and committed** (`89745ce1117c`). The
  pure-Zag teacher reproduces the frozen schedule exactly — all 8 slices
  byte-identical, 5/5 runs deterministic, every check green (12 planted flaws
  per session, 287 proposals total, checksums all verify). Hashes pinned.
- **Signature package verified and ready for you.** I independently checked
  every claim in the paperwork (not just took the agents' word):
  - *Arm C gate amendment*: the quoted old rule matches the frozen prereg
    word-for-word; all 7 cited evidence commits are real; the two dependency
    amendments exist; the risk statement is honest about all three auditor
    deaths. 4 documents need your signature before Arm C can start.
  - *Track 5 weights* (30/25/25/10/10): definitions, kill clauses, and
    decision tree all check out. **Correction:** an agent earlier suggested
    the comparison trial might already be done — it has not run. It's still
    blocked waiting on your sign-off, exactly as the paperwork says.
- **New compiler bug found and documented** (ZNC-2026-09-21-007): a specific
  way of allocating integer tables in Zag silently reads the wrong memory.
  The teacher was rewritten to avoid it. The teacher harness uses the buggy
  pattern 33 times — flagged for the repair crew, not trusted until audited.
- **Track B coordinator died in a server restart; I restarted it** with a
  brief that says the teacher is done (don't rebuild it) and the harness
  repair is the priority.

## Still running

- Track A (53 arms): several verdicts in — G2, J2, and R killed by their own
  rules (R: ceiling effect — tied baseline at 100% recall, counts as not-beating), R2 complete. Crews active.
- Track R0: tournament battery in closeout, active.
- HTD-1: first build verdict in (E-LG2 passed, committed). 13 crews active.

## Needs your word (nothing here was decided by experiment — these are yours)

1. **Arm C gate amendment** — sign 4 documents (amendment + 2 dependency
   amendments + risk statement), or reject and keep Arm C parked.
2. **Track 5 weights** — sign off on 30/25/25/10/10 + kill clauses, or change
   them. The trial starts after you sign.
3. Strength-trial rulings 3, 4, 5 (from before).
4. Integrity doc wording sign-off (from before).
5. Whether to relax the ledger byte-identical-vs-state-varying bar (from before).
6. Where to file the compiler bug reports (7 now).

Full detail: `~/workspace/NIGHT_RUN_2026-09-21.md`.

## Update ~03:45 — Track B coordinator finished

- **Harness ZNC-007 remediation complete and independently verified.** All six
  affected tables converted to safe memory; the coordinator caught one live
  bug the repair crew missed (line 1794 — was reading the wrong data for
  every entry past the first). Post-fix output byte-identical to before;
  determinism holds 5/5 across three conditions.
- **Arm verdicts:** arm-4 PASS, arm-5 PASS (both committed); arm-3 FAIL
  (committed, rebuild parked — needs your word before it restarts).
- **Still open:** the harness double-free crash is pre-existing (not caused
  by the fix) and the repair crew is still hunting it.

## Update ~04:40 — HTD-1 coordinator finished, verdict sheet being written

- The HTD-1 coordinator completed (most build crews finished, including
  respawns after the server restart), but it didn't leave a final summary.
  A closeout agent is now collecting the 13 build verdicts from disk and
  writing the final verdict sheet. You'll have it in the morning.

## Update ~04:45 — HTD-1 verdict sheet complete

- All 13 build crews surveyed, verdicts written and committed (`8d74c47b5737`,
  `docs/lab/htd-1/RESULTS_VERDICT_SHEET.md`).
- **Killed by their own bars:** E-DE1 (cost-model budgeting), E-DE2 (early exit),
  E-DE3 (lazy verification — narrowing beats deferral 37% vs 0.015%).
- **Survivors:** E-DE4 narrow memoization (42% saving, 0 false hits), E-DE5
  heuristic narrowing (37% saving, degrades gracefully), E-LG1 write batching
  (91% fewer write syscalls), E-LG2 checkpoint ledger (K=64/256 pass; K=16
  fails the 20% bar), E-LG4 read indexes, G-CO2 deliberate abstention,
  G-CO3 plan-verify-emit (caveat: verdict rests on the weighted reading of
  its kill bar — if you rule for raw op counts it flips to killed),
  G-CM1c beats G-CM1d head-to-head.
- **Open:** G-CM1b evict leg ambiguous (needs a rerun); E-DE2+E-DE4
  composition never ran (premise now dead since E-DE2 was killed); E-LG1
  epclose arm's full battery absent.

## Update ~05:15 — Track B infrastructure complete, verified

- The original Track B coordinator finished all 15 crews: harness (13/13 modes
  pass, M8-deterministic), real learner core (5/5 byte-identical), battery
  scorer (108/108 checks), 44-slice curriculum. Integration commit at the
  branch tip (`2a6e013d`).
- I verified the key commits exist: arm-1 teacher (`89745ce1117c`), HTD-1
  verdict sheet (`8d74c47b`), integration tip — all real, arm-1 is an
  ancestor of the tip (71 commits of other work landed after it).
- **Reconciliation:** the coordinator asked for "wire arm 1" — that's stale,
  arm-1 is done. Its "run arm 3" is also overtaken: arm-3 got a FAIL verdict
  (committed), rebuild parked for your word. Arm-4 and arm-5 PASS (committed).
- 7 more compiler bugs characterized overnight (ZNC-005 through 012), all
  recorded in AGENTS.md with workarounds.

## Update ~06:05 — R0 1x complete, needs your rulings

- **All five 1x batteries resolved.** B-T1: FAIL (verified re-run — raw is
  7/10, not dead last; also found a real heap-overflow bug in the grounded
  arm, needs fixing regardless). B-T2: descriptive pass, needs your R-3
  number (leg 1 measured 1.195, just under the proposed 1.2 floor — the
  legs disagree, so the number is yours). B-T3: descriptive pass, needs
  your R-4 number (measured max drop: 0). B-T4: 8/8, needs your R-5 number.
  B-T5: the crew claimed pass but the coordinator flags it — split and merge
  fired on *separate* contexts, the literal "same material re-merge" was
  not demonstrated. FAIL or BLOCKED pending your reading.
- **10x is NOT greenlit** — your rule says every 1x bar passes first, and
  they don't.
- **Integrity win:** a worker's uncommitted B-T1 numbers were caught by the
  closeout re-run and thrown out. The evidence-with-verdict rule worked.
- **M8 lesson:** the determinism gate used tiny inputs and missed a crash
  that only shows above 80KB. Future M8 runs need real-scale inputs.
- **Your rulings needed:** R-3 number, R-4 number, R-5 number, B-T5 wording
  vs mechanism, B-T1 literal-vs-intent, B-T2 manifest amendment ack, scorecard
  schema canonical ruling, 10x promotion.

## Update ~06:10 — Track B closed out (newer than my 05:15 note)

- Branch head is now `47c48d3e7cf9f` with TRACKB_VERDICT.md + HARNESS_CLOSEOUT.md
  committed and verified.
- **Arm 1: teacher AUDIT PASS, but the learner honestly FAILS §B.7** — best
  1/12 flaw hits vs the ≥10/12 bar, all 8 slices. The learner is miscalibrated
  (wrong spans, false confidence, missing grounding). This is the real finding:
  the teacher is correct, the learner can't use it yet.
- Arm 3 FAIL, arms 4/5 fixture PASS. No head-to-head champion (blocked, the
  prereg's §7 is silent on the tie case).
- Harness repaired (12/12, N=5). Force-pin implemented and tested PASS (34/34,
  17/17); live wiring into the deliberation core needs an owner decision.
- **6 parked calls for your morning** on top of the R0 eight.
