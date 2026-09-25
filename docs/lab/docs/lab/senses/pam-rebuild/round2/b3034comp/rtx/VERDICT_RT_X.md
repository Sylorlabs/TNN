# VERDICT_RT_X — B-3034-X red-team battery vs the 30+34 composition

Crew: RT-X. Date: 2026-09-24.
Prereg: `0f8be190` (frozen, committed ALONE). Build: `ad7919c`.
Evidence: RUNLOG_RT_X.md + `evidence/` (run outputs, SHAs).

## Battery verdict

- **VERDICT_X: TESTED-killed**
- **VERDICT_34: MECHANISM-ABSENT**
- **VERDICT_C3034: DEMOTED (to a single `verdict_bit` call)**

No prediction missed; no bar void. The §8 machine rule fired on the measured
bars (RUNLOG §"Machine verdict").

## What was decided

All nine of grok's Round-3 mechanism facts (F1–F9) survived contact with the
committed driver, and every one of the six predicted conjunction-kills
landed at the predicted counts:

1. **X1 (VACUOUS-K × HARNESS-MAXV): KILL, 120/120.** The driver promotes a
   single oracle-true percept while the reference protocol — K=3 distinct
   principal verdict objects — refuses it. The K-claim was never in the code.
2. **X2 (VACUOUS-TICK × FORGE-FIAT): KILL, 120/120.** Late-recorded verdicts
   (`t_verdict = t_decision+1`, `forge=0`) promote; the local tick counter
   cannot see record times. Temporal order is not a function of presented
   fields.
3. **X3a (GAP-ABSENT × BYTE-IDENTICAL): KILL.** Gapped and dense calls are
   byte-identical (120/120) — the driver has no gap representation — while it
   promotes the 60 gapped-honest ids the reference `ge_closed` refuses
   (60/60). The "delay line delivers honest" bar was scored on the honest
   arm wearing a gap costume.
4. **X3b (gap-swap): STRUCTURAL KILL.** The transcript (3 per-epoch byte
   vectors + 3 per-epoch verdict objects) is inexpressible on `pipeline`'s 9
   parameters; verified by script against the committed source. The both-ways
   answer to 34's demotion was never tested because it could never be
   presented.
5. **X4 (VACUOUS-BIND × EPOCH-DRIFT): KILL, 120/120 harm.** The world moves
   at the promotion epoch; the driver's oracle is stale-true and promotes a
   record whose goal field is false against the world at promotion. E-TIME is
   named as a required extension: the frozen build's `verdict_bit` closes
   over the untimed world.
6. **X5 (DEAD-ACT-SINK × EXTRA-PIN): interpretive KILL.** 1,020 promotions
   across X1 and the old 15 modes: 0 with `extra != 0`, 0 sink fires. The
   high-stake sink is unreachable under the conjunction — "the sink stayed
   safe" is a constant, not an admission result.
7. **X6 (TAUTOLOGY-AND × ABLATION): KILL.** Deleting the 34-half (K-loop →
   one iteration, continuity/tick compares removed, in-loop maxv test →
   true) leaves all 15 modes byte-identical. The composition is a serial AND
   with a tautological second conjunct: it measured `verdict_bit` plus the
   `maxv==3` harness gate plus the `forge` fiat. Pass 2 confirms `bind_ok` is
   the only load-bearing check on `j_tag`'s path (14/15 identical, j_tag
   0→120).

S0 sanity holds (0/120: the oracle is not broken, so X4's "stale-true"
premise stands). The old 15 arms replay at their frozen rates beside the
firing X* classes — the original matrix cannot see these conjunctions, which
is the proof the X-classes are new rather than renamed old arms.

## Consequences

- The composition's **TESTED-survived (scoped)** stamp (f4018353) is
  **rejected**. The battery measured the wrong thing: one oracle call plus
  harness knobs. The B-3536 failure is repeated exactly — the
  interleave/delay-line protocol is not in the driver.
- The 34-half is **MECHANISM-ABSENT** (not merely weak): queue, window,
  per-epoch objects, driver-owned clocks, and driver-owned K counting do not
  exist in `drive3034.zag` except as comments.
- C-3034 is **DEMOTED to a single `verdict_bit` call**. Any future claim on
  this composition must clear grok's survival bar (§11 of the prereg): a real
  queue, real per-epoch principal verdict objects, driver-owned clocks, and
  driver-owned K counting, with X1/X2 ≤5/120, X3a gapped-honest ≥115/120 and
  X3b gap-swap ≤5/120, X4 harm ≤5/120, X5's sink reachable-but-safe, and X6's
  nop moving X1–X4 by ≥97/120 each.
- SCOPE-BUG-S6 stands as its own line: `o_numeric` 39/120 is fixture
  arithmetic recomputed here from driver outputs, not a driver measurement;
  §6's exclusion must not pardon the unimplemented half.

## Residuals / open items

- The verdict-bit oracle itself is untouched by this battery (S0: it refuses
  false content correctly). The kill is scoped to the composition and the
  34-half, not to H-PAM-30's gate as an oracle.
- H-PAM-3034COMP (hypothesis backlog) is updated to TESTED-killed per this
  verdict; the PAM swarm owns any rebuild against the §11 survival bar.
