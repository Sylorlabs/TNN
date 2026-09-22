# SELFTEST_VERDICT.md — can the TNN test everything itself?

Date: 2026-09-21. Prereg: SELFTEST_PREREG.md (frozen before build).
Question (Micah): "is TNN able to test everything — scalable, test all?"

## What was built

`selftest.zag` — one pure-Zag binary (zero RNG) containing a deliberate
learner core AND a deliberative orchestrator. The orchestrator loads a frozen
8-battery manifest, executes every battery against a fresh learner instance,
ADJUDICATES each result against its preregistered bar itself (no external
judge), writes every verdict into the audit ledger (op=20 records), and
refuses to emit ST_DONE unless verdict count == manifest count (anti-silent-
skip gate: completion is structurally blocked by a missing verdict).

Batteries reuse real lab battery kinds: scale-up mastery (B1), falsehood
absorption honesty-calibration (B2), §B.7-style flaw probes (B3),
new-mechanisms contradiction battery (B4), corrupt-battery handling (B5),
in-process determinism self-check (B6), plus two DELIBERATE trips (T1: 239/240
taught against a 240 bar; T4: 47/48 + one tie-withhold against a 48 bar).

## Kill bars (independent Python oracle, no shared code)

| Bar | s1 (8 batt x 5 reps) | s10 (80 batt x 5 reps) |
|---|---|---|
| KB-ST-AUTO: one process, zero external orchestration | HOLD | HOLD |
| KB-ST-SKIP: no silent skip; B5 reported UNRUNNABLE | HOLD (B5=UNRUNNABLE x5) | HOLD (x50) |
| KB-ST-FIDELITY: binary verdict == oracle recomputation, every battery | HOLD (40/40 incl. T1/T4 trips) | HOLD (400/400) |
| KB-ST-DET: byte-identical reruns | HOLD (5/5, md5 3be14786...) | HOLD (5/5, md5 6ffead66...) |
| KB-ST-OVERHEAD: orch_ops <= 2x bat_ops | HOLD (0.0127) | HOLD (0.0127) |
| KB-ST-SCALE: fidelity holds at 10x battery count | n/a | HOLD |

Fidelity detail: the oracle independently reimplements the competition
mechanism and recomputes every observed count from the frozen data formulas,
then re-adjudicates every bar. The binary's adjudication is the same code
path for all batteries (no per-battery hardcoding): B1 240 PASS, B2 12 PASS,
B3 96 PASS, B4 48 PASS, B5 UNRUNNABLE, B6 PASS, T1 239 TRIP, T4 47 TRIP.

## The gate is real, not decorative (fault injection)

A fault-injected copy silently skipped battery 5. The binary emitted
`ST_BLOCKED,emitted=7,expected=8` and NO ST_DONE. The oracle independently
flagged it: coverage miss, count 7 vs 8, ST_DONE missing, ST_BLOCKED present.
Both layers catch a silent skip.

## Overhead

Orchestration (schedule + adjudicate + ledger + emit) costs 5 ops/battery
against hundreds-thousands of learner ops: ratio 0.0127, ~157x under the
2.0 bar. It is lean enough to scale.

## Verdict: YES — this becomes the lab's future harness

The TNN can run its own evaluation batteries at scale: autonomous,
faithful to an independent oracle, deterministic, and cheap. Adopt as the
lab harness. What must change first:

1. **Manifest on disk.** Currently compiled in (avoids the ZNC-2026-09-21-014
   file-helper hang class, but a real harness needs loadable manifests).
   Solve file loading safely, then move the manifest out of the binary.
2. **Richer battery kinds.** Current batteries are synthetic formula-generated
   instances of real battery *kinds*. Wire in the actual batteries: the live
   search-sense legs, the prose comprehension battery, the full §B.7 suite.
3. **External learner dispatch.** The learner under test is currently embedded
   in the orchestrator binary. A real harness must test *other* binaries'
   learners (spawn + pipe, or a linkable learner core).
4. **Multi-learner / multi-config matrices** (the param-scale 19-config style
   sweeps) as first-class manifest constructs.

## Honest limits

- Data is deterministic formulas, not the real corpora (Gutenberg etc.).
- B6's digest equality is self-contained; the oracle asserts the claim.
- The deliberate trips prove the adjudication path is live, but a subtler
  adjudication bug (wrong bar constant shared by a misread prereg) would
  need prereg-vs-code review, which the oracle does for bar values.
- One repair during build (documented): the first competition implementation
  dropped trust accumulation across candidates (B4/T4 read 0/0); rewritten
  with proper accumulators before any scored run. No scored run used the
  broken build.

## Artifacts

- `selftest.zag` (source), `oracle.py` (independent checker)
- `runs_s1_r0..r4.log`, `runs_s10_r0..r4.log` (all md5-verified)
- Binary excluded per convention (reproducible via pinned toolchain).
