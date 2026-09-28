# COMPARISON preregistration — did the hidden RNG help TNN?

**Status:** FROZEN 2026-09-20 (pre-analysis). **Owner:** Micah. **Worker:** COMPARISON.
**Scope:** read-only behavioral comparison of the quarantined tainted LH battery
(wave-2 long-horizon, LCG contamination) against the clean rerun battery
(wave-12 r34-remediation, deterministic state-driven exploration). Answers
Micah's "tests decide" question: was the hidden RNG actually helping TNN, and
if so, exactly what function did it serve (so the deterministic mechanism can
capture it honestly)?

Frozen bars change only via dated amendment approved by Micah. The worker
cannot self-approve amendments. **This prereg is frozen before the LCG
explore-sequence reconstruction and before any metric-by-metric analysis.**

## 1. The two arms (frozen inputs — read-only, no new training)

**Tainted reference (quarantined):** wave-2 long-horizon results, annotated
2026-09-20. Mechanism under comparison: `r34v3_choose` with
`explore_enabled=1` — `if(explore_enabled==1 && r34v3_mod(r34v3_rng(s),5)==0)
{obj=1-obj;ex=1;}`, LCG `v=(rng*997+7919) mod 1000003`, seeded per leg.
State-blind 1-in-5 flips, unbounded, during every training phase.
Inputs: `docs/lab/wave2/longhorizon/variants/LH-1/2/3/4/5/7/RESULT.md`,
`LH-P3/RESULT.md`, evidence bundles `EVIDENCE_20260919T*` (local mirrors
`~/workspace/tnn-lab/wave2/longhorizon/`). Investigation commits
`072f25aa` / `4976cbf5`. The quarantined arm is NEVER re-executed by this
workstream.

**Clean arm:** wave-12 r34-remediation rerun. Mechanism: `r34_clean_choose` —
`explore = (explore_enabled==1) && (budget>0) && (margin<=200 || neg_streak>=3)`,
budget refilled to 8 (SET, not accumulate) at each training phase, evals run
`explore_enabled=0`. Inputs: `docs/lab/wave12/r34-remediation/rerun/`
(prereg `9ed0203a1594`, verdict+runner `22ad3a90144b`/`445464a3ef86`, raw
evidence `183305995915` LH-1/LH-5, `c7fcf8d36a35` LH-2, `0cd56df2ab61` LH-3;
local `~/workspace/tnn-lab/wave12/r34-remediation/rerun/`).

**Legs with both arms (verdict-bearing):** LH-1 (480 updates), LH-2 (1920),
LH-3 (4800 + drift), LH-5 (0/10/25/50% corruption ramp + supplementary
seeds). **Tainted-only (no clean counterpart — context only, no verdict
weight):** LH-4, LH-7 (claims remain suspended; only tainted explore volume
is characterized).

## 2. Frozen metric set (the ONLY metrics the verdict may rest on)

M1. **Explore count and timing** — per leg: total training explores, per-block
    distribution, and (clean arm) which predicate path fired
    (uncertainty `margin<=200` vs disappointment `neg_streak>=3`; from
    `expl=`/`bud=`/`nstrk=` trace fields and the rerun VERDICT). Tainted
    explores are reconstructed by exact LCG simulation (§4).
M2. **Switch counts per corruption level** (LH-5): 0/10/25/50% lineages,
    tainted 19/91/149/181 vs clean 19/90/154/198 (from `LH5_FINAL` lines),
    plus supplementary seeds (10%,7777 / 10%,4242 / 25%,7777).
M3. **Saturation onset** (LH-2/LH-3): block at which correct cells pin at
    +30000; tainted LH-2 block 16 / LH-3 block 16 vs clean LH-2R block 13 /
    LH-3R block 14 (from per-block `LH_TRACE` scores).
M4. **Endpoint scores** — max|score| at LH-1 endpoint (tainted 18900 vs clean
    22300); per-cell endpoint scores; return-A gate values (15/16 both arms
    LH-1/LH-2; 16/16 LH-3 mirror case both arms).
M5. **Knee shape** (LH-5): corruption rate of first total (0/16) per-block
    collapse; identity of collapsed blocks at 10% (tainted: 5-B, 9-A) and 25%
    (tainted: 3-A, 4-B, 9-A); endpoint A/B curve at 50% (tainted 0/16 vs
    clean 0/0); collapsed-probe counts per lineage.
M6. **Wrong-cell sink rate** — wrong-cell scores at fixed horizons: LH-2
    block 39 (tainted −21100/−20100 vs clean −4700/−4800); LH-3 block 99
    (tainted −30000/−30000 pinned ~51/59 vs clean −22100/−18800 still
    sinking); per-cell accept counts n01/n10 as the touch census.
M0. **Guardrail (headline parity):** per-block/per-regime eval positives and
    the stability verdicts must be checked first. Any clean-leg failure of a
    bar the tainted leg passed is reported unsoftened before any "helped"
    analysis (per the rerun prereg headline rule); the rerun VERDICT records
    none.

## 3. Verdict criteria (frozen decision rules)

### HELPED — all four must hold:
- **H1 (strictly better headline):** a metric in M1–M6 is strictly better in
  the tainted arm on a headline outcome (endpoint eval positives, knee
  location, retention/return gate, saturation earliness) — direction matters;
  a mere numeric delta is not enough.
- **H2 (not chaos):** the delta reproduces across the arm's own determinism
  reruns AND, for any corruption-regime claim, is consistent across the
  supplementary corruption seeds (10%,7777 / 10%,4242 / 25%,7777). A one-seed
  delta inside the chaotic 50% envelope (13/20 vs 12/20 collapsed probes)
  cannot carry HELPED.
- **H3 (traced mechanism):** the delta is attributed to a named LCG-driven
  behavior in a named state condition via a named code path
  (explore flip → `pending_explore` → accept/switch interaction). Correlation
  without a traced mechanism cannot support HELPED.
- **H4 (net help):** the benefit is not outweighed by a cost on another
  headline metric (e.g. "better knee but destroyed endpoints" fails H4).

If HELPED: the verdict names the EXACT function served (which state
condition, which code path, what the deterministic rule must add to capture
it honestly).

### DID-NOT-HELP — all three must hold:
- **D1 (headline identity):** all headline outcomes identical across arms
  (per-block eval positives, return gates, knee location, collapse-block
  identity at 10%/25%, saturation-without-rigidity, drift-schedule and
  mirror-assignment reproduction).
- **D2 (deltas are costs or noise):** every remaining behavioral delta is
  directionally a cost of the RNG (slower correct-cell accumulation, deeper
  wrong-cell sink, later saturation, higher explore volume with zero endpoint
  gain) or lies inside the chaotic envelope with no reproducible direction.
- **D3 (no benefit mechanism):** no traced mechanism exists by which a
  state-blind flip produced a better outcome than the bounded state-driven
  rule.

### MIXED — H1–H3 hold for at least one frozen metric/leg AND D1–D3 hold
elsewhere. The verdict states exact scope (which metric, which leg, which
mechanism) and gives a per-scope design implication.

### INCONCLUSIVE — a headline delta exists but fails H2 (chaos), or the
explore-sequence validation (§4, F1) fails, voiding timing-dependent claims.

## 4. Explore-sequence reconstruction (analysis method, frozen)

The tainted logs do not record explore counts. The reconstruction simulates
ONLY the explore-decision subsequence — the pure function
`v=(rng*997+7919) mod 1000003`, explore iff `mod(v,5)==0` — for each leg's
documented learner seed and training-decision count. This is a mathematical
reconstruction of a logged subsequence, not a training rerun: it does not
touch the quarantined core, runs no learning, and produces no learning
evidence. Pure Zag, no RNG (standing law). Draw-consumption model: one draw
per training `choose` with `explore_enabled=1` (eval chooses consume none —
`&&` short-circuit); block = 48 draws (LH-1/2/3/5), 24/visit (LH-4),
4/cycle (LH-7).

- **F1 (validation gate):** seed 12001, 480 draws, 48/draw blocks MUST
  reproduce the LH-P3 fixed arm's documented per-block explore counts
  `11,7,8,8,7,12,10,7,9,5` (sum 84). If validation fails, ALL
  explore-count/timing claims are void and the verdict is capped at
  INCONCLUSIVE on timing-dependent points. The validation result is reported
  regardless.
- Legs reconstructed: LH-1 (seed 11001, 480 draws), LH-2 (22002, 1920),
  LH-3 (33003, 4800), LH-5 (5555, 480 × 4 lineages), LH-4 (47111, 288),
  LH-7 (55223, 480). LH-4/LH-7 are tainted-only context.

## 5. Falsification bar for the conclusion (frozen)

- **F1.** §4 validation gate (above).
- **F2 (attribution check):** a "helped" mechanism claim is falsified if the
  same delta appears where the RNG could not have acted (eval phases,
  `explore=0`); the attribution is then wrong and the claim is dropped.
- **F3 (no cherry-picking):** the verdict addresses all six metrics M1–M6;
  any metric contradicting the verdict is reported as a named caveat, never
  omitted.
- **F4 (already-captured check):** if a candidate "help" function (e.g.
  switch-immune episodes during negative streaks) is already implemented
  honestly by the clean rule (disappointment path, `pending_explore=1`
  blocking the switch), the verdict says so explicitly instead of
  recommending its reintroduction — the RNG then added nothing the
  deterministic rule lacks.

## 6. Commit sequence (frozen)

1. This prereg, alone. (Frozen before analysis; committed first.)
2. Analysis: `ANALYSIS_COMPARISON.md` (metric-by-metric, with the LCG
   reconstruction program + its validation output) + `VERDICT_COMPARISON.md`
   (HELPED / DID-NOT-HELP / MIXED with scope + design implication).
   No prereg edits in commit 2.

---
*Frozen 2026-09-20. Amendments, if any, will be dated and flagged for
Micah's approval. The worker cannot self-approve amendments.*
