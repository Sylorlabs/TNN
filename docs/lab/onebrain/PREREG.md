# PREREG — Experiment 2: One-Brain Sub-Agent Dispatch

**Frozen:** 2026-09-27 (committed before any implementation)
**Question (Micah):** can TNN itself dispatch multiple parallel
sub-deliberations FROM THE SAME BRAIN — sharing one ledger/state —
rather than an external coordinator spawning separate agents with
separate contexts? "Sub agents from the same brain as sub agents not
sub agents but basically sub agents": TNN-native fan-out.

## H1 (main)

TNN's own deliberation machinery can decide to fan out K
sub-deliberations that share ONE ledger, where one branch's
failure/invalidation is instantly visible to all other branches, and
reintegrate them into a single verdict — and this beats single
deliberation on hard problems because of the shared-state cross-talk,
not because of extra compute.

## H0 (null)

Fan-out is either (a) crew scaffolding (the driver calls fan_out; TNN
never chooses it), or (b) sequential deliberation with extra steps (no
accuracy gain attributable to shared state), or (c) decorative sharing
(branches don't actually read each other's writes).

## Definitions — what counts as GENUINE one-brain dispatch

All four must hold; each has a dedicated falsification test (§5).

1. **TNN's own decision.** The fan-out trigger is ledger-driven: a
   deliberated condition inside the machinery (e.g. ≥2 surviving
   readings with close margins, or the close_call flag) sets a
   fork flag, and the machinery acts on it. No driver-level `if` /
   loop decides to fan out.
2. **One shared ledger.** All sub-deliberations read and write the SAME
   ledger rows (fact candidates, eliminations, evidence validity).
   There is exactly one ledger in the address space during a fan-out.
3. **Causal cross-talk.** A write by branch A changes the behavior of
   branch B within the same deliberation (proven by the poison test).
4. **Single reintegrated verdict.** After the sub-passes, one ARGMAX
   over the shared ledger produces the one answer. No voting ensemble
   of independent runs.

"Parallel" here means deterministically interleaved sub-passes with
shared state (zero RNG, no threads) — the claimed benefit is the
cross-talk, never wall-clock parallelism.

## Machinery requirements

- Pure Zag. Zero RNG in any decision path. Byte-identical reruns.
- Built on the adopted one-brain concept (sub-deliberations share one
  ledger/state; one part's failure instantly known to all) and the
  deliberation-v1 ledger design (readings / fact candidates / action
  bids; GEN → ELIM → ARGMAX). NOT a fork of it — a new module that
  reuses the ledger layout.
- **K5 lesson wired in:** deliberation v1's third red team voided K5
  (reading rows computed but never consulted). The shared-state
  channel in this experiment must be causal machinery (eliminations,
  evidence invalidations — things bids actually read), and the channel
  itself must pass a neuter test: disabling shared writes MUST change
  outcomes on the hard set.
- Deterministic interleaving: sub-deliberations execute in fixed
  round-robin order. Same bytes in, same bytes out, every run.

## Problem set (frozen before measurement)

Hard ambiguous dialogue turns: queries with ≥2 plausible readings
where single deliberation is known to struggle (drawn from round-4
hard cases + constructed multi-reading probes). Frozen as
`problems.tsv` with expected answers BEFORE the one-brain machinery
runs. Single-deliberation baseline = deliberation-v1 machinery run
once per problem, no fan-out.

## Kill bars

| ID | Bar | Falsification test | Verdict if failed |
|----|-----|-------------------|-------------------|
| K1 | No parallelism benefit | One-brain accuracy ≤ single-deliberation accuracy on the frozen hard set, AND the shared-writes-off ablation matches one-brain | KILL the mechanism |
| K2 | No shared-state effect | Poison test: invalidate a fact candidate in the shared ledger mid-deliberation; other branches' bids/eliminations do not change | KILL the mechanism |
| K3 | Crew scaffolding | Scaffold-removal: minimal driver that never calls fan_out; TNN never fans out on its own on fork-worthy problems | VOID (not TNN's decision) |
| K4 | Decorative sharing | Delete/reorder a shared ledger entry: fan-out behaves identically to N independent sequential runs | KILL the mechanism |
| K5 | Non-determinism | Any two reruns differ at the byte level | VOID the evidence |
| K6 | RNG in decision path | Grep + audit finds RNG use in deliberation paths | VOID the evidence |

K1 note: the bar is deliberately conjunctive — beating single
deliberation alone is not enough; the shared-writes-off ablation must
also show the gain comes from the channel, not from extra passes.

## Causal proof protocols

1. **Poison test.** Mid-deliberation (between sub-pass rounds), flip a
   shared fact candidate to invalid. Requirement: every branch that
   read it updates its bids/eliminations in the same deliberation.
   Control: N independent ledgers — poisoning one changes nothing else.
2. **Delete/reorder test.** Delete a shared evidence entry (or reorder
   GEN). Requirement: the fan-out's verdict distribution differs from
   N independent sequential runs on the same problems.
3. **Scaffold-removal test.** Strip the driver to a minimal loop with no
   fan_out call. Requirement: on fork-worthy problems the machinery
   still fans out (ledger-driven fork flag fires).
4. **Shared-writes-off ablation.** Same machinery, writes to shared rows
   disabled (each branch gets scratch copies). Requirement for H1:
   ablation accuracy < one-brain accuracy (the channel carries the
   gain), and ablation ≠ one-brain on the poison test.

## Measurements

- Accuracy: one-brain vs single-deliberation vs ablation, per problem
  and aggregate, on the frozen hard set. Report where one-brain does
  NOT win, per problem.
- Overhead: ledger ops per verdict, wall time, bytes of ledger churn.
- Determinism: 3× reruns, SHA-256 of full outputs, must match.
- Fork rate: fraction of problems where the machinery itself chose to
  fan out (and whether fork-worthy problems are the hard ones).

## Commit plan

1. This prereg (freeze).
2. Machinery + problem set + baseline (no scores inspected before
   freeze of problems.tsv).
3. Results + red-team report. Honest voids where bars fail.

## Standing laws

Pure Zag, zero RNG, byte-identical reruns, tests decide (never ask
Micah for opinions), honest voids, no binaries/.zagd/derived files in
the repo. Branch: tnn-native-lab only.
