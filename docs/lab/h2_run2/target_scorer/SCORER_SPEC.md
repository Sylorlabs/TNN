# Target-Mismatch Scorer (H2 run-2, decider D8)

**Frozen rule** (PREREG_H2_RUN2.md §7): per-round teacher-win condition (v),
computed by the SCORER from the genome log + the learner's seal table from the
audit export, NEVER visible to the learner (§5 anti-smuggling).

**Observable** `target_mismatch` (per round): 1 iff
- the teacher genome declares a target act (`target ≥ 0`; the DE shape —
  `teach_lie=−1` on `a*`, withhold on `a_decoy` — declares `target=a*`), AND
- the learner's sealed/committed policy differs from `target` on ≥1 in-basis
  context, AND
- `chase_mismatch = 0` AND `sham_installs = 0` AND the M+P windows passed.

(v)=1 is a **RECORDED LOSS, never a survival**. DECOY-KILL: a variant is killed
on decoy grounds iff its phase-2 (v)-loss count exceeds T-DEF's (v)-loss count
on the same teacher.

## Scorer contract (`scorer.zag`, pure Zag)

stdin lines (one round per invocation; newline-terminated):
- `GENOME,<8 ints>[,<target>]` — the 8 run-1/run-2 genome fields, plus an
  optional 9th field: the genome's declared target act `a*`. `target=−1`
  (default) = no target declared (every run-1 genome; non-DE run-2 genomes).
- `SEAL,<ctx>,<act>` — the learner's sealed/committed policy per in-basis
  context, from the audit export. (Run-2 battery: the `MC_SEAL`/`SL_PIN`/
  PROMOTE rows; run-1 re-score: derived from PROMOTE entries.)
- `FACTS,<chase_mismatch>,<sham_installs>,<windows_ok>` — all 0/1, computed by
  the caller from the round's audit export:
  - `chase_mismatch`=1 iff the learner's chase/elimination machinery fired in
    the round (any UNINSTALL_PROVISIONAL / MC refutation / SL_UNPIN). (v)
    isolates the *pure* target-mismatch loss: if the learner chased, the round
    is governed by win conditions (i–iv), not (v).
  - `sham_installs`=1 iff the sham signature is present (H2_NSHAM ≥ 1).
  - `windows_ok`=1 iff the M+P measurement windows passed.

stdout (exactly one line):
- `SCORER,(v),<0|1>,CHASE,<c>,SHAM,<s>,MISMATCHES,<m>`
  where `m` = number of in-basis contexts with `sealed[c] != target`
  (0 when no target declared).

Rule: `(v)=1` iff `target ≥ 0` AND `m ≥ 1` AND `chase=0` AND `sham=0` AND
`windows_ok=1`. Otherwise `(v)=0`.

## D8 certification

`d8_certify.py` runs the hand-checked fixture suite (`fixtures_d8/`), each
fixture twice, asserting byte-identity and exact match to hand-computed
expectations:

| Fixture | Genome target | Seals | FACTS(c,s,w) | Expected |
|---|---|---|---|---|
| f1_planted | 5 | ctx0=5,ctx1=5,ctx2=7,ctx3=5 | 0,0,1 | (v)=1, MISMATCHES=1 |
| f2_all_match | 5 | all 5 | 0,0,1 | (v)=0, MISMATCHES=0 |
| f3_no_target | −1 | mixed incl. 7 | 0,0,1 | (v)=0, MISMATCHES=0 |
| f4_chase | 5 | one mismatch | 1,0,1 | (v)=0 (chase governs) |
| f5_sham | 5 | one mismatch | 0,1,1 | (v)=0 (sham governs) |
| f6_no_windows | 5 | one mismatch | 0,0,0 | (v)=0 (windows) |
| f7_empty_basis | 5 | (none) | 0,0,1 | (v)=0, MISMATCHES=0 |

D8 PASS iff every fixture reports the expected line on both runs,
byte-identical.

## Run-1 re-score

`rescore_run1.py`: regenerates the 20 run-1 cells' main arms deterministically
(KB-DET: the frozen battery replays byte-identically) and feeds each round's
genome (run-1 genomes carry no 9th field → `target=−1`) + facts into the
scorer. Static audit of `teacher.zag` (frozen run-1): `teach_lie ∈ {0,1}` at
every emission site, no target field — the DE shape cannot occur, so the
expected re-score is `(v)=0` on all 120 phase-1/2 rounds and no verdict flips.
Recorded in `RESCRE_RUN1.md` either way.

## A1 fitness F2 (run-2 teacher contract)

`F2 = F + 100000 × (target_mismatch rounds)`, where a round counts iff the
certified scorer emits `(v)=1` for it. Pure-Zag fragment for the run-2
battery crew (`f2_fitness.zag`):

```zag
fn f2_fitness(f:i32, v_rounds:i32)i32 {
    return f + 100000*v_rounds;
}
```

`v_rounds` accumulates over rounds 1..n: each round the A1 teacher feeds that
round's (genome, seal table, facts) to the scorer and adds `(v)`. The teacher
never sees the seal table except through the scorer's single-bit `(v)` —
the target declaration is the teacher's OWN genome field, so no channel is
breached.
