# Parameter-scaling verdict — 2026-09-22

Micah's question: data scaling changed nothing (mastery 1.0, 240 → 6.58M facts).
What does scaling the PARAMETERS buy? Fixed data N=24,000 (C=24, M=1000, P=1).
Prereg: `PARAM_PREREG.md` (frozen before any param run).

## Headline

**The architecture is parameter-insensitive above the capacity floor.** 16 of 19
configs produce byte-identical learners (digest `8e6238911bb7cef0` — identical to
the scale-up baseline): slots ×2/×4/×8, evidence ×0.25–×4, verify depth ×2/×4,
audit ×0.5–×4, redundancy ×2/×4, and the joint-big config all change nothing
except cost. The only parameter with a behavioral edge is slot capacity below
1× — and there degradation is exactly proportional with zero corruption of what
fits. No capability emerges with parameters that data scaling didn't buy.

## Kill bars

| Bar | Result |
|---|---|
| KB-P-DET (byte-identical reps) | NOT TRIPPED — 19/19 configs, 59/59 runs |
| KB-P-EMERGE (absorption < 1.0) | Flagged for slot025/slot05/jsmall by the letter of the bar; **cleared on inspection** — the shortfall is untaught facts (capacity drops), not truth-detection. Every *taught* falsehood absorbed 1.0 at every config (292/292, 586/586) |
| KB-P-GRACE (taught subset stays perfect under pressure) | NOT TRIPPED — taught-subset clean mastery 1.0 at 0.25× and 0.5× slots |
| KB-P-EFF (≥2× cost for <1pp gain = efficiency-dead) | slot4, slot8, audit4, red4, jbig efficiency-dead |

## Per-config results (N=24,000)

| Config | Params (P1/P2/P3/P4/P5) | Clean mastery | Flaw | Absorption | ops/fact | B/fact (alloc) | Learner digest |
|---|---|---|---|---|---|---|---|
| base | 1 / 64 / 1 / 1 / 1 | 22841/22841 | 96/96 | 1159/1159 | 4.000 | 202 | 8e6238911bb7 |
| slot025 | 0.25 / 64 / 1 / 1 / 1 | 5708/22841 (0.2499) | 96/96 | 292/1159 | 3.091 | 99 | 0a6e548f2dae |
| slot05 | 0.5 / 64 / 1 / 1 / 1 | 11414/22841 (0.4997) | 96/96 | 586/1159 | 3.500 | 103 | 9175b7e1f4d2 |
| slot2 | 2 / 64 / 1 / 1 / 1 | 22841/22841 | 96/96 | 1159/1159 | 4.000 | 358 | = base |
| slot4 | 4 / 64 / 1 / 1 / 1 | 22841/22841 | 96/96 | 1159/1159 | 4.000 | 669 | = base |
| slot8 | 8 / 64 / 1 / 1 / 1 | 22841/22841 | 96/96 | 1159/1159 | 4.000 | 1244 | = base |
| ev16 | 1 / 16 / 1 / 1 / 1 | 22841/22841 | 96/96 | 1159/1159 | 4.000 | 202 | = base |
| ev32 | 1 / 32 / 1 / 1 / 1 | 22841/22841 | 96/96 | 1159/1159 | 4.000 | 202 | = base |
| ev128 | 1 / 128 / 1 / 1 / 1 | 22841/22841 | 96/96 | 1159/1159 | 4.000 | 202 | = base |
| ev256 | 1 / 256 / 1 / 1 / 1 | 22841/22841 | 96/96 | 1159/1159 | 4.000 | 202 | = base |
| depth2 | 1 / 64 / 2 / 1 / 1 | 22841/22841 | 96/96 | 1159/1159 | 5.000 | 202 | = base |
| depth4 | 1 / 64 / 4 / 1 / 1 | 22841/22841 | 96/96 | 1159/1159 | 7.000 | 202 | = base |
| audit05 | 1 / 64 / 1 / 0.5 / 1 | 22841/22841 | 96/96 | 1159/1159 | 4.000 | 115 | = base |
| audit2 | 1 / 64 / 1 / 2 / 1 | 22841/22841 | 96/96 | 1159/1159 | 4.000 | 333 | = base |
| audit4 | 1 / 64 / 1 / 4 / 1 | 22841/22841 | 96/96 | 1159/1159 | 4.000 | 639 | = base |
| red2 | 1 / 64 / 1 / 1 / 2 | 22841/22841 | 96/96 | 1159/1159 | 6.000 | 358 | = base |
| red4 | 1 / 64 / 1 / 1 / 4 | 22841/22841 | 96/96 | 1159/1159 | 10.000 | 669 | = base |
| jsmall | 0.5 / 16 / 1 / 0.5 / 1 | 11414/22841 (0.4997) | 96/96 | 586/1159 | 3.170 | 59 | = slot05 |
| jbig | 4 / 256 / 4 / 4 / 4 | 22841/22841 | 96/96 | 1159/1159 | 13.000 | 8690 | = base |

"= base" means the full learner digest is byte-identical to baseline, not just
the headline metrics.

## Efficiency frontier

Pareto-optimal (allocated bytes/fact × mastery): **jsmall** (59 B/f, 0.4997)
and **audit05** (115 B/f, 1.0000). The baseline (202 B/f) is dominated on
allocated memory — the audit ledger's 1 MB chunking granularity dominates the
footprint at 24k facts, and halving its cap loses nothing. On *logical* bytes
(24+4+64 = 92 B/fact, the scale-up convention), audit_mult changes nothing at
all: it only moves the cap, never usage. Deliberation depth buys linearly more
ops (5.0/7.0 vs 4.0) for zero verdict change; redundancy ×4 buys 2.5× ops and
3.3× memory for zero gain.

## Why parameters don't buy truthfulness

The prereg's mechanistic prediction held exactly: verification here is a gate on
evidence *presence*, not on truth — the learner has no truth source. Re-running
the same deterministic gate (P3), widening buffers (P2/P4), or duplicating
storage (P5) adds no new information, so verdicts cannot change; only cost
moves. Capacity (P1) is the one real edge: below 1× the store fills (rc=2) and
facts drop — proportionally (0.2499/0.4997), gracefully, corrupting nothing that
fits. What actually buys falsehood-detection is an independent information
source — the web-search sense caught 12/12 teacher falsehoods this same night.
Capacity ≠ epistemics.

## Caveats

- Closed corpus: no contradictions exist by construction, so deliberation had
  nothing to deliberate *about*. Depth might matter with conflicting evidence;
  untested here.
- The §B.7 flaw battery samples ids in [0, n/4) only (inherited from the scale
  driver), so it is blind to capacity loss beyond 4× — slot025's 96/96 is a
  coverage artifact, noted not hidden.
- B/fact (alloc) reflects 1 MB audit-chunk granularity; logical is 92 B/fact
  for all full-capacity configs.
- Fidelity gate passed: all-1× config reproduces scale-up digests byte-exactly
  (N=240 → 44a61309cf780de1; N=24000 → 8e6238911bb7cef0).

## Lineage

- Driver: `param_learner.zag` (pure Zag, zero RNG) — the scale_learner core
  unchanged except five argv capacity knobs; decision logic, audit layout,
  lifecycle consts identical (fidelity-gate verified).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- 59 runs, 19 configs × 3 reps (5 for baseline), all byte-identical within config.
