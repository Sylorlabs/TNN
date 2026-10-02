# CA-2 Clean Refreeze Report: TNN-vs-LLM Arena

Date: 2026-09-30 UTC
Worker: Clean Refreeze Worker (parent-directed)
Scope: `docs/lab/research-lead/overnight-20260928/competitive_arena/`
Prereg: ARENA_PREREG.md, amendments A1, A2, A3 (A3 committed alone as
`a883fe0e9` before any refreeze code, seed, or artifact existed)

## Verdict: ARENA-READY

The arena is cleanly re-frozen, deterministic, and operational. It is ready
to accept (1) the actual developmental TNN and (2) a serious LLM baseline
through the frozen turn protocol. No Python was invoked at any point in the
CA-2 wave, including no-ops.

## A3.1 CA-1 is void (history only)

The CA-1 wave is VOID under the standing pure-Zag red line because two
no-op Python invocations occurred during it (recorded verbatim in
CA1_PILOT_REPORT.md and in amendment A3). No CA-1 number is cited anywhere
in this report as a result. CA-1 is preserved as development history
(commit `bd60dc9ed`, CA1_PILOT_REPORT.md).

## Seed protocol (A3.3)

- The retired seed 20260929 was viewed during discarded Python development
  and is exploratory only. It occurs zero times in any active CA-2 source
  (verified by grep; historical documents keep it as history).
- The new canonical seed was derived mechanically: 6 bytes from
  /dev/urandom interpreted as one unsigned integer, written directly to
  `SEALED_SEED.txt` by shell redirection. The worker did not view the value
  during derivation or installation.
- Installation was by blind shell substitution through a variable into
  `world_gen.zag` (the `sd` constant, the proof header) and `arena.zag`
  (the report header). Verified afterward by count and pattern only:
  old-seed count 0 in both files, exactly one numeric `sd` constant
  present, and all three baked locations byte-match the sealed file
  (checked with grep -q through the variable, never displayed).
- Seed file sha256:
  `28dccc7c683df90552f67b11378f592af38feffb5797983cb2ca1df2b8406224`
- Honest disclosure: the seed value became visible to the worker in the
  scorer's stdout after all runs were complete (the arena records the seed
  in its report header by design, for reproducibility). No source was
  modified after that point except the CA-1 to CA-2 report-header string,
  which does not depend on the seed value. No seed-picking and no tuning
  to the seed were possible: derivation was mechanical and installation
  was blind.

## What was run (all pure Zag + shell)

Toolchain: `znc 2026.07.0-dev (edition 2026)`. Built `world_gen.zag`,
`tnn_contestant.zag`, `arena.zag` to native binaries (analyzer warnings
only, exit 0). Bash sequenced process invocations only; no arena logic,
scoring, analysis, or data transformation lives in shell. Zero `.py` files
exist under this path.

1. World generation twice from the sealed seed: 131 turns, 68 items,
   11 artifacts. All artifacts byte-identical across both runs (cmp).
   DETERMINISM BAR PASS.
2. Full contestant pilot three times from fresh state (131 turns each).
   Cognitive reply sequences byte-identical across all three runs; only
   wall-clock `ms` and `rss_kb` vary, which are machine metrics, not
   cognition. REPRODUCIBILITY BAR PASS.
3. Scorer run on the final pilot. SCORING BAR PASS.

## Results (infrastructure self-test only)

The hand-authored reference contestant scored 1.000 on all 16 capabilities
(68/68). Cost ledger: 53 exposure examples, 4 tool calls (observe
requests), about 1440 ms contestant CPU, max RSS 4268 KB, max state
8192 bytes, tokens N/A.

This is expected and is NOT a discovery. The reference contestant is a
hand-authored symbolic architecture containing exactly the mechanisms the
world tests. The 16/16 validates that the arena works: sealed generation,
turn sequencing, state persistence across 131 process restarts, scoring
(including C11 Criterion 0 UNKNOWN handling, graded C6, observe-gated C8,
F1 on C15), and cost accounting are all operational. It is not evidence of
learning or invention, and it must never be cited as evidence that TNN
scores 16/16. Classification: INFRASTRUCTURE, operational.

## LLM baseline: BLOCKED_BY_TOOLCHAIN (re-confirmed 2026-09-30)

The znc toolchain exposes `_zag_raw_syscall` but no socket, TLS, or HTTP
builtins and links no TLS library. Implementing TCP plus TLS 1.3 plus HTTP
in Zag inside this program is infeasible, and no Python HTTP client is
permitted. There is still no mechanism in this environment by which a
pure-Zag arena can call an LLM API. The frozen contestant turn protocol
(prereg section 5) and `world/llm_prompt_pack.txt` (regenerated from the
new seed) remain the interface for a future external runner with TLS
capability. No LLM results are claimed or implied.

## Files

- `ARENA_PREREG_AMEND3.md` (committed alone, `a883fe0e9`)
- `SEALED_SEED.txt` (canonical seed; sha256 above)
- `world_gen.zag`, `arena.zag` (seed installed; header corrected to CA-2)
- `tnn_contestant.zag` (unchanged reference self-test contestant)
- `world/` (11 sealed artifacts from the new seed)
- `pilot_run/` (replies, results.json, results.txt, final state)
- `run_arena.sh` (bash process sequencer; unchanged)

## Readiness

ARENA-READY. The next step is to enter the actual developmental TNN as a
contestant against the frozen `world/` battery, then a serious LLM
baseline via the frozen protocol, and to report capability curves with
honest costs (examples, tool calls, CPU, RSS, state bytes, tokens where
applicable).
