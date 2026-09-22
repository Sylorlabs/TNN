# LH| Long-Horizon Trial — Analysis

**Trial ID:** LH-2026-09-22
**Prereg:** `docs/lab/coding/reflection/long_horizon/PREREG.md` (commit 6631774678c2, amended d79c27642f85)
**Run date:** 2026-09-22
**Cycles:** 230

## Verdict: PASS (all bars)

| Bar | Result | Detail |
|-----|--------|--------|
| Defect slope | **PASS** | Slope 0.000 (flat, 24 windows, 0 defects) |
| Retention | **PASS** | 10/10 stages byte-identical on re-run |
| Honest halt | **PASS** | F1 halted with KB-MISS, no fabrication |
| Determinism | **PASS** | 5 stages × 5 reps, all byte-identical |
| Throughput | info | 230 cycles in 16.8s (49,354 cycles/hour) |
| First-working-build | info | Mean 0.64s, max 0.96s per component |
| Role use | info | Balanced: 9/9/9, 9/9/8, 9/8/9 across thirds |

## Defect slope (primary)

24 ten-cycle windows, 0 defects in any window. Least-squares slope = 0.000000.
**No evidence of long-horizon degradation.** The flat line is not a failure
to detect — it's a genuine zero-defect run across 230 cycles.

## Retention

Re-ran binaries for A1, A5, A10, B3, B8, C2, C6, C8, A8, B6 on original
contract tests. All outputs byte-identical to acceptance run. **No
retention loss.**

## Honest halt

F1 ("apply ROT13 cipher to product") — the proposer emitted `HALT KB-MISS`
with zero candidates. The KB contains no ROT13 capability, and the system
correctly recognized the gap rather than fabricating. **No fabrication.**

## Determinism

For A3, B4, C4, A8, B6: 5 full pipeline runs each (propose→critique→compose→
gen→compile→run). All 5 reps byte-identical in: final spec, generated source,
compiled binary, test output. **Zero randomness in decision paths.**

## Throughput

230 cycles in 16.8 seconds wall-clock. The bottleneck is process spawning
(Zag binary invocations), not deliberation complexity.

## Per-component time

Mean 0.64s from stage_start to stage_accept. Slowest: C8 (0.96s), C7 (0.94s),
B8 (0.95s) — the AGG/SORT stages with multi-record I/O. Fastest: A4 (0.37s).

## Role use

Proposer/critic/composer episodes distributed evenly across run thirds:
- Third 1 (cycles 1-76): 9/9/9
- Third 2 (cycles 77-152): 9/9/8
- Third 3 (cycles 153-230): 9/8/9

The one-brain deliberation was exercised uniformly throughout. No role
atrophy at the horizon.

## Invention provenance

Every stage's final spec traces to:
1. A PROPOSE episode citing specific KB entries (e.g., `LH-CAP|FIELD`).
2. A CRITIQUE episode simulating candidates against contract examples.
3. A COMPOSE episode selecting the accepted spec.

The ledger (`ledger.txt`, 269 lines) contains the full trace. No
crew-authored architecture appears in any spec — the audit
(`audit_forbidden.py`, exit 0) confirms the machinery contains no
pipeline-specific vocabulary.

## Limitations

1. **Zero defects is suspicious.** A real long-horizon trial should encounter
   and recover from failures. The contracts were calibrated to be solvable
   first-pass; the diagnoser/revision loop was not stress-tested. Future
   trials should include adversarial contracts that force revision cycles.

2. **The KB is minimal (6 entries).** Real coding requires orders of magnitude
   more knowledge. This trial proves the deliberation machinery works, not
   that it scales to full-language synthesis.

3. **Determinism was verified, not proven.** Five reps of five stages is
   evidence, not a guarantee. The Zag binaries are deterministic by
   construction (no RNG, no timestamps in output), but a formal proof would
   require analyzing the deliberation code paths.

4. **F1 is a single probe.** One honest halt does not prove the system will
   always halt honestly. A battery of underivable tasks would be stronger.
