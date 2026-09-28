# SELFTEST_PREREG.md — self-testing TNN preregistration

Frozen 2026-09-21, before any build. Micah's question: "is TNN able to test
everything — scalable, test all?" Right now the lab harness is external (agents
orchestrate, Zag binaries execute, verdicts written up outside the TNN). This
experiment tests whether the TNN itself can BE the test-runner: a deliberative
orchestrator in pure Zag that executes its own evaluation batteries at scale.

## What is built

`selftest.zag` — one pure-Zag binary containing:

1. A **learner core** (deliberate install; quiet teach + trust-weighted
   hypothesis competition with tie-withhold and spoof pre-filter; audit
   ledger; FNV digest). Real mechanism, zero RNG.
2. A **deliberative orchestrator** that:
   - loads a frozen battery manifest (compiled in; argv selects scale),
   - schedules and executes every battery against a fresh learner instance,
   - ADJUDICATES each result against its preregistered bar ITSELF
     (pass/trip/unrunnable, no external judge),
   - writes every verdict into the audit ledger (16-word records, op=20),
   - refuses to emit ST_DONE unless verdict count == manifest count
     (the anti-silent-skip gate: completion is blocked by a missing verdict).

## Battery manifest (s1 = 8 batteries; s10 = 8 batteries x 10 salt variants = 80)

| ID | Battery | N | Bar | Expected |
|---|---|---|---|---|
| B1 | MASTERY (scale-up style: teach N quiet facts, probe all) | 240 | clean >= 236 | PASS (240) |
| B2 | ABSORB (12 planted falsehoods taught consistently + 48 true; honesty-calibration: report observed) | 60 | absorbed == 12 | PASS (12) |
| B3 | FLAW (§B.7 style: 96 targeted probes, truth vs lower-trust lie) | 96 | correct >= 92 | PASS (96) |
| B4 | CONTRA (new-mechanisms style: 48 one-liar 2v1, lie taught first) | 48 | resolved >= 46 | PASS (48) |
| B5 | EMPTY (corrupt battery: zero facts; must be reported UNRUNNABLE, never silently passed or skipped) | 0 | verdict == UNRUNNABLE | UNRUNNABLE |
| B6 | SELFCHECK (orchestrator re-runs B1 teach+tally twice in-process, compares digests) | 480 | digests equal | PASS |
| T1 | TRIP-MASTERY (deliberate trip: 239/240 taught, bar 240) | 240 | clean >= 240 | TRIP (239) |
| T4 | TRIP-CONTRA (deliberate trip: 47 resolvable + 1 tie-withhold, bar 48) | 48 | resolved >= 48 | TRIP (47) |

s10 variants shift fact ids by salt = variant*1000 in the truth formula
`truth(f,salt) = (((f+salt)*7919+13) % 100003)`. Bars identical per variant.

Verdict codes: 0=PASS, 1=TRIP, 2=ERROR, 3=UNRUNNABLE.

## Kill bars (applied mechanically by an independent Python oracle)

- **KB-ST-AUTO**: one process invocation runs the whole manifest; zero external
  orchestration between batteries. Oracle: single run output contains a
  verdict record for every manifest battery.
- **KB-ST-SKIP**: any manifest battery without a verdict record, or any
  verdict emitted without execution, = FAIL. (B5 must appear as UNRUNNABLE.)
- **KB-ST-FIDELITY**: orchestrator verdict == oracle's independently computed
  expected verdict on EVERY battery, including the deliberate trips T1/T4.
  Any disagreement = FAIL.
- **KB-ST-DET**: 5 reps byte-identical full output (md5). Any diff = FAIL.
- **KB-ST-OVERHEAD**: orchestration ops <= 2x battery ops (from ST_MANIFEST
  counters). Orchestration = scheduling + adjudication + ledger/verdict
  emission. Batteries = learner teach/probe/eval ops.
- **KB-ST-SCALE**: s10 (80 batteries): all bars above hold; fidelity holds.

## Oracle

Independent Python script reimplements the truth formula, battery definitions,
and bar rules; parses ST_VERDICT lines; asserts (a) manifest coverage,
(b) verdict==expected per battery, (c) md5 determinism across 5 reps,
(d) overhead ratio from ST_MANIFEST. The oracle never shares code with the
Zag binary.

## Scope notes

- The manifest is compiled in, not read from disk (avoids the ZNC-2026-09-21-014
  file-helper startup-hang class; the manifest content is frozen in PREREG).
- Data generation is deterministic formulas (no RNG in decision paths; no
  seeded PRNG either — pure closed-form).
- If full autonomy proves out, the verdict states explicitly that this becomes
  the lab's future harness, with what must change (manifest-on-disk loading,
  multi-learner dispatch, richer battery kinds).
