# R34 hidden-randomness remediation — preregistration

**Status:** FROZEN 2026-09-20 (pre-implementation).
**Owner:** Micah. **Worker:** MECHANISM (r34 remediation workstream).
**Ruling:** Micah ordered REMEDIATE, not amend. The LCG comes out. The old file and its
evidence stay quarantined — this workstream does not modify
`toolchain/r34v3/r34_learner_core.zag` or its callers in place.

Frozen bars change only via dated amendment, which the worker cannot self-approve —
flag to Micah.

## 1. The contamination (verified, quarantined)

File `~/workspace/tnn-lab/toolchain/r34v3/r34_learner_core.zag` (98 lines, quarantined as-is):

- Line 15: `fn r34v3_rng(s:*R34V3State)i32 {let v:i32=r34v3_mod(s.*.rng*997+7919,1000003);s.*.rng=v;return v;}`
  — a seeded linear-congruential generator.
- Struct field `.rng:i32`, seeded by `r34v3_init(seed:i32)` (lines 16–19).
- Line 38 in `r34v3_choose`:
  `if(explore_enabled==1 && r34v3_mod(r34v3_rng(s),5)==0){obj=1-obj;ex=1;}`
  — a 1-in-5 explore flip driven by the LCG.
- `r34v3_best` tie-break `s.*.decisions%2` is deterministic (state-driven) — kept as-is.
- Direct `r34v3_rng` caller: `wb_whitebox_tests.zag:155`.

No RNG, no seed, no `.rng` field may exist in the clean core. The init signature changes
from `init(seed)` to `init(budget)` — the seed parameter is the contamination vector and
does not survive.

## 2. Design: exploration as a deterministic function of logged state

Per Micah's analogy: a human's expression varies with prior context — memory, history,
salience, deliberation budget. No dice, no bodily mood, everything replayable from the
complete logged state.

The clean learner keeps the 2-context × 2-object scored memory of v3 and replaces the
LCG explore flip with a four-input deterministic rule. Every input is a logged field of
the learner state; there is no other input.

### 2.1 State: `R34CleanState` (22 named i32 fields)

| # | Field | Meaning |
|---|-------|---------|
| 1–4 | `s00,s01,s10,s11` | Score per context×object, reward×100 units, clamped ±30000 (unchanged from v3) |
| 5–8 | `n00,n01,n10,n11` | Trial counts per context×object (unchanged) |
| 9 | `explore_budget` | **Explicit logged exploration budget.** Set at init / refilled by the trainer via `r34_clean_set_budget`. Decremented by exactly 1 on each explore decision. Valid range 0..1000000. Replaces `.rng`. |
| 10 | `updates` | Accepted learning updates (unchanged) |
| 11 | `active` | Active context (unchanged) |
| 12 | `contexts` | 1 or 3 (unchanged) |
| 13–17 | `pending,pending_action,pending_context,pending_object,pending_explore` | Pending-credit plumbing (unchanged) |
| 18 | `decisions` | Decision counter (unchanged; still drives the `best` tie-break) |
| 19 | `switches` | Context switches (unchanged) |
| 20 | `outcomes` | Accepted outcomes (unchanged) |
| 21 | `explores` | **Count of explore decisions taken.** Logged. |
| 22 | `neg_streak` | **Consecutive negative outcomes** (`reward==-1` accepts). Reset to 0 on any `reward==1` accept. Logged recent-outcome history / salience pressure. |

### 2.2 The frozen explore-decision rule

`r34_clean_explore_decision(s, explore_enabled) -> 0/1` is a pure predicate over logged
fields, also exposed standalone for white-box testing. `r34_clean_choose` applies it.

Frozen, in full:

```
best    = r34_clean_best(s, s.active)          # higher score wins; tie -> s.decisions % 2 (kept from v3)
margin  = |score(s, s.active, 0) - score(s, s.active, 1)|   # candidate uncertainty
uncertain    = (margin <= 200)                  # scores within 2 net reward-units (scores are reward*100)
disappointed = (s.neg_streak >= 3)              # salience: three consecutive negative outcomes
explore = (explore_enabled == 1) && (s.explore_budget > 0) && (uncertain || disappointed)
```

`r34_clean_choose(s, explore_enabled, was_explore)`:

1. Guards identical to v3: null state, null out-pointer, or `pending != 0` → return −1.
2. `obj = best`; `ex = 0`.
3. If `explore == 1`: `obj = 1 - obj`; `ex = 1`; `s.explore_budget -= 1`; `s.explores += 1`
   (flip semantics identical to v3's `obj=1-obj`).
4. `was_explore.* = ex`; `s.decisions += 1`; return `obj`.

Rationale per input, in Micah's terms:

- **Candidate uncertainty (`margin <= 200`).** When the two candidates score within two
  reward-units of each other, the memory does not adjudicate between them — it goes and
  looks. (Scores accumulate `reward*100` per learned trial, so 200 = 2 net reward-units.)
- **Salience / recent-outcome history (`neg_streak >= 3`).** Three consecutive negative
  outcomes mean "what I'm doing isn't working" — the human tries something different even
  when fairly confident. This is the disappointment pressure.
- **Decision/switch counts** enter through `decisions` (the kept tie-break, so ties
  resolve deterministically and alternate) and through the logged `explores` count, which
  lets any auditor enumerate exactly how much exploration happened.
- **Explicit logged exploration budget (`explore_budget`).** The deliberation budget: the
  trainer grants N explores; each explore spends exactly one; at zero, no exploration,
  ever. Bounded, enumerable, replayable. Set via `r34_clean_init(budget)` /
  `r34_clean_set_budget(s, b)` (range-checked 0..1000000, else `cl_bad()`).

### 2.3 Update semantics (carried over unchanged from v3, frozen)

`r34_clean_accept` is logic-identical to `r34v3_accept`, plus `neg_streak` bookkeeping:

- Validation identical: pending==1, action matches, reward ∈ {−1, +1}, else `cl_bad()`.
- Context-switch on negative reward identical (requires `pending_explore==0`, `old>0`).
- `learn==1`: score += reward×100, clamp ±30000, count++, updates++.
- `reward==-1` → `neg_streak += 1`; `reward==1` → `neg_streak = 0`.
- `outcomes++`; pending fields cleared; return 0.

`r34_clean_best` tie-break `s.decisions % 2` is kept (deterministic, state-driven).

### 2.4 Serialization (checkpoint-compatible)

`r34_clean_encode` / `r34_clean_decode`, 160 bytes, same envelope discipline as v3:

- Magic `"R34CLN01"` (8 bytes, distinct from `"R34CLV03"` — no cross-format confusion),
  version u32 `1` at offset 8, size u32 `160` at offset 12.
- 22 fields × 4 bytes at offsets 16..104 (scores as signed-with-shift like v3,
  all others as u32; `explore_budget` included).
- Zeros at 104..128, SHA-256 of bytes 0..128 at 128..160.
- Decode range-checks every field (scores ±30000; counts/updates/explores/neg_streak ≥ 0;
  `explore_budget` 0..1000000; active ∈ {0,1}; contexts ∈ {1,3}; pending flags 0/1) and
  refuses corrupt input with `cl_corrupt()`.

`r34_clean_fp` is a deterministic fingerprint over all 22 fields (same prime-mixing
discipline as v3). `r34_clean_equal` compares all 22 fields.

## 3. Interface (new files only — quarantined originals untouched)

- `~/workspace/tnn-lab/wave12/r34-remediation/r34_clean_learner.zag`
  — the clean core. Imports only `../../toolchain/R33_CONTINUING_LIFE_V1/observation.zag`
  (observation-side only: no world, regime, evaluator, or checkpoint import — same
  isolation bar as v3). No other new imports.
- `~/workspace/tnn-lab/wave12/r34-remediation/wb_clean_tests.zag`
  — white-box suite + determinism driver for the clean core. Imports the clean core.
  `argv[1]` selects the mode (one binary, run twice and diff — the determinism pattern):
  - (no arg) `whitebox`: all check groups, prints `CL_CHECK,<name>,<actual>,<expected>`
    lines and `CLEAN_FAILURES,<n>`; exits nonzero iff n>0.
  - `replay`: scripted 200-episode run (fixed reward pattern `reward = (obj==0)?+1:-1`,
    `explore_enabled=1`, budget granted at init, `learn=1`, `allow_switch=0`), prints a
    per-episode transcript and the final state fingerprint.
  - `diverge`: the B2-ii purity pair (below).
  - `resume`: encode at episode 100 → decode into a fresh state → continue to 200.
    Output must be byte-identical to `replay`.

The harness (`r34_continuing_harness_v3.zag`) keeps calling the quarantined v3 core for
now; rewiring the harness to the clean core is a separate workstream. The clean core
keeps the caller-visible `choose(s, explore_enabled, was_explore)` shape so the rewire
is mechanical; the harness will additionally call `r34_clean_set_budget` per its own
prereg.

## 4. Verification plan (frozen before implementation)

### Bar B1 — byte-identical rerun (the no-hidden-state bar)

- N=10 `replay` runs from identical logged state, on this machine, same compiler binary.
- PASS iff all 10 stdout transcripts are byte-identical AND all 10 final fingerprints
  are byte-identical.
- Falsified by any differing byte. Any failure → KILL (see §6).

### Bar B2 — explore-decision purity (the pure-function-of-logged-state bar)

- (i) Two identical states → 200-episode scripted runs → `r34_clean_equal` == 1 and
  transcripts byte-identical. (Covered by whitebox group G2 + B1.)
- (ii) Same inputs, different logged history, divergence exactly where predicted:
  state A fresh (`neg_streak=0`), state B after 3 forced negative accepts
  (`neg_streak=3`); both with high score margin (>200), `explore_budget>0`,
  `explore_enabled=1`. PASS iff the next `choose` returns explore=0 on A and explore=1
  on B, with `obj_B == 1 - obj_A`, `budget_B == budget_A - 1`, `explores_B == 1`, and
  every other field equal. The FIRST divergence between the two runs must be exactly
  this predicted explore decision — no earlier, no other field.
- (iii) `resume` output byte-identical to `replay` output (mid-run checkpoint/restart
  changes nothing — full replayability from logged state).
- Falsified by any extra/missing/early divergence. Any failure → KILL.

### Bar B3 — static no-randomness audit

- `grep -nEi 'rng|lcg|seed|rand|srand|random|entropy|/dev/urandom|_zag_time|_zag_clock'`
  over `r34_clean_learner.zag` and `wb_clean_tests.zag` returns zero matches
  (the prereg text is excluded from the grep scope; code and comments must not contain
  the terms at all).
- `grep -n '@import'` on the clean core shows only the observation.zag import.
- Any match → KILL.

### Bar B4 — scale leg (10x)

- `replay` at 2000 episodes, run twice, byte-identical transcripts. (The no-RNG law must
  survive 100x-scale thinking; 10x here is the affordable leg. Any failure → KILL.)

### Whitebox groups (in-suite, all must pass, `CLEAN_FAILURES,0`)

- G1 explore-rule units: budget=0 never explores; margin≤200 explores; margin=200
  boundary explores; margin>200 with streak<3 does not; streak=3 with high margin
  explores (disappointment path); streak=2 with high margin does not; explore_enabled=0
  never explores; tie-break `decisions%2` kept (tested via `r34_clean_best` directly);
  explore consumes exactly 1 budget and flips obj.
- G2 purity: B2-i and B2-ii as above, in-suite.
- G3 learner semantics (v3 G4 carried over): two-run determinism; updates counted;
  learn=0 → no drift in scores/updates (outcomes still counted); exact update
  (+100/count/updates); clamp at ±30000; encode→decode roundtrip preserves all 22
  fields; fingerprint stable across equal states, sensitive to field changes;
  `r34_clean_set_budget` range validation.
- G4 budgets: explore stops exactly at budget exhaustion (budget=N → exactly N explores
  in an always-uncertain scripted run, then best-only forever).

## 5. Honest limits (stated before implementation — not hidden)

The deterministic rule deliberately cannot reproduce one behavior of the LCG arm: the old
rule flipped 1-in-5 **regardless of state** — in a stable regime with a clear margin and
no negative streak, the LCG still explored 20% of the time, while the clean rule explores
never (until budget and uncertainty/disappointment say otherwise). That behavioral delta
is the point of the remediation, not a defect; the head-to-head behavioral comparison
belongs to the comparison workstream. This workstream certifies only: no randomness,
byte-identical reruns, explore decisions as a pure function of logged state.

## 6. Kill criteria

- **K1.** Any byte difference across the B1 repeats → kill. Do not "fix forward";
  file the evidence and stop.
- **K2.** Any B3 grep match → kill.
- **K3.** B2-ii divergence anywhere other than exactly the predicted explore decision →
  kill (the decision would depend on unlogged state).
- **K4.** B4 scale leg fails → kill.
- **K5.** Any whitebox group failure (`CLEAN_FAILURES != 0`) → kill.
- On any kill: quarantine the attempt, write a dated KILL receipt into the evidence dir,
  and report to the parent. Bars change only via dated amendment approved by Micah.

## 7. Commit sequence (frozen)

1. This prereg, alone. (Frozen before any implementation exists.)
2. `r34_clean_learner.zag` + `wb_clean_tests.zag`. No prereg edits in this commit.
3. Verification evidence: receipts, transcripts, diffs, grep audits. No binaries —
  binaries live in /tmp during verification and are never committed
  (`commit_to_branch.py` would take extensionless binaries, so keep them out of the tree).

---
*Frozen 2026-09-20. Amendments, if any, will be dated and flagged for Micah's approval.*
