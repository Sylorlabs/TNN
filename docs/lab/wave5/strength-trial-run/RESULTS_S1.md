# Strength Trial S1 Results

**Verdict: BLOCKED** — material prereg curriculum bugs prevent valid WBS/JI measurement.
GATE passed for all arms. S1 cells ran deterministically. Mechanisms work; curricula do not.

## GATE (ran first per prereg)

| Arm | Result | Deterministic |
|-----|--------|---------------|
| A   | PASS (0 failures) | yes (byte-identical) |
| B   | PASS (0 failures) | yes |
| C   | PASS (0 failures) | yes |

GATE verified: stage-gated kill (90-strength refused at KILL, OK at FULL),
4-citation + justify effort, force-pin role gating (TNN refused, trainer OK),
force-pinned kill refused, unpin + kill OK. All ledger checks (replay, refusals,
lineage) pass.

## Static checks

- **No RNG**: grep for rand/srand/random/getrandom/urandom/rdtsc/time/clock_gettime
  in all four Zag sources → zero matches.
- **Single strength-write site**: `st_write_strength(` callers are exactly
  {st_add_into_slot, st_add_core, st_redeclare, st_trainer_declare, st_restore,
  st_clear_strength, st_overwrite} — the four legal judgment paths plus ledger
  restore and kill-clear. Verified by awk function-tracking.

## S1 cells (27 cells × 2 runs, all deterministic, ST_INVALID=0)

### Arm A (graded strength + evidence friction)
- **VUP**: 9/9 (100%) all variants. **470 drops** — store freezes after 30 episodes
  (no contradiction evidence → all evictions abandoned; 3,824 abandonments).
- **WBS**: cohort **0/0** all variants (see bug below). False revision 0/9.
- **JI**: implants **0/0** (never admitted — freeze). Junk 21/21 held. Entrenched 0/6.

### Arm B (uniform MA1 kill semantics)
- **VUP**: 29/150 (19.3%), 29/150, 30/150 (20.0%). 0 drops (eviction works).
- **WBS**: cohort **0/0**. False revision 0/29.
- **JI**: implants **5/5 rejected (100%)**. Junk 1/345 (0.3%). Entrenched 0/6.

### Arm C (A + force-pin)
- **VUP**: 9/9 (100%) all variants. 470 drops. Force-pin exercised in v0
  (pin at t=99, unpin at t=401, both OK; no REFUSED_FORCEPIN probes).
- **WBS**: cohort **0/0**. False revision 0/9.
- **JI**: implants **0/0**. Junk 21/21. Entrenched 0/6.

## Material prereg bugs (BLOCKED)

1. **`wrong(m,v)` identically zero.** The closed form `((5*m+11*v+7)%10)<2`
   yields 0 wrong memories for variants 0, 1, 2 (verified by exhaustive check:
   0/500 for each variant). The prereg specifies "~20%". WBS cohort is 0/0
   for all arms — the curriculum does not test revision at all.
   **Needed**: amend the closed form (e.g. `((3*m+7*v+1)%10)<2`).

2. **Implant episode 500 out of range.** Closed form `(k*h)/6` gives
   {83,166,250,333,416,500} for H=500; episode 500 never runs (0-based 0..499).
   **Needed**: confirm exclusion or adjust form.

3. **VUP freeze for A/C is by design but degenerate.** With no contradiction
   episodes, A/C cannot pay effort for any erasure; the 32-slot store fills by
   episode 30 and 470/500 candidates drop. The 9/9 VUP metric is technically
   100% but measures only the first 30 episodes. This is the mechanism working
   as specified — it demonstrates that graded strength without evidence cannot
   handle memory pressure — but S10/S100 would be 99% drops.

## Kill criteria (as measured)

- **Arm A**: WBS kill requires "revision below 100%". Cohort 0/0 → undefined;
  criterion cannot fire (no evidence of rigidity), but promotion is impossible
  (requires WBS 100%). **Neither killed nor promotable on WBS.**
- **Arm B**: VUP kill requires "trails best graded arm by >20pp in 2/3 variants".
  B=19-20%, A/C=100% (degenerate 9/9). Literally, B trails by ~80pp → **B would
  die**. But the A/C numbers are degenerate (9 admitted vs 150); a fair
  comparison is impossible.
- **Arm C**: Force-pin probing criterion ("high REFUSED_FORCEPIN attempt rates")
  has no numeric threshold in the prereg. C recorded 0 probes (pin succeeded).
  **Cannot mechanically evaluate.**

## Arms advanced to S10/S100

**None.** The trial is BLOCKED pending prereg amendment of the curriculum
closed forms. S10/S100 would waste compute on degenerate curricula.

## Force-pin integration

GATE verified the contract: TNN-role pin refused (113), trainer pin OK,
force-pinned kill refused (112), unpin OK, post-unpin kill OK. In C/VUP/v0,
the trainer script pinned the strongest revealed-important slot at t=99 and
released at t=401; the pin held through 302 episodes of pressure (no
REFUSED_FORCEPIN, no invalid kills). The lock was exercised, not probed.

## Implementation bugs fixed during build

1. Audit word-index off-by-one (b1 at word 5, a1 at word 11, not 6/12).
2. Ops returned audit result (0) instead of op result (rc) — refusals were
   invisible to callers. Fixed all 14 ops to return rc (or audit error).
3. `st_demote` used wrong op code constant.

These were implementation errors, not prereg issues. The binary was rebuilt;
GATE passed after fixes. No trial evidence was generated before the fixes
(the failed GATE runs produced no valid metrics).
