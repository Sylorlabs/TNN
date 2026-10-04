# REPORT: P5-META-LEARNING (charter 23) -- BLOCKED, NO RESULT CLAIMED

Lane `p5meta`. Prereg frozen alone in commit `24c133b42`
(`PREREG.md` + `NAMECHECK.md`, no `.zag`). This commit adds the
implementation, the self-check diagnostic, and this report.

## 1. VERDICT

**NO RESULT. NO VERDICT. The experiment did not run to a trustworthy state.**

No kill bar was evaluated. No examples-to-criterion number, no negative
transfer magnitude, no structural-reuse count and no ablation result is
claimed. Nothing in this lane may be cited as evidence for or against
meta-learning, transfer, or charter 23.

Reporting a number here would have been fabrication: the learner produced
internally inconsistent counters (section 3), which means the measurement
apparatus itself is not yet trustworthy, independently of any hypothesis.

## 2. WHAT WAS BUILT (pure Zag, safebin PATH, no forbidden executables)

- `p5.zag` -- the full preregistered learner: 12 slots, arities 1..4, 4 ops
  (2379->3172 hypotheses), 64 rounds, search budget 24 hypotheses/round,
  4 examples/round, verification batch `V`, 16-example audit; frozen COGOPS
  learner-state arena at BIND 12744 / PLAN 13000 / STATS 13224 / DETC 15900 /
  STRATT 16600 / CTXT 17000; L1 = per-slot relevance, L2 = arity-ladder
  permutation + verification batch size, both derived from training records
  only; 7 arms (PRIOR, ABL_L1, ABL_L2, CHAN_V, CHAN_A, COLD, DATA); 5
  conditions x 6 families. All statistics computed in Zag; output via
  `_zag_print` only, never `_zag_raw_syscall` (brief 4.0).
  sha256 `ddffded2f3b69f4255640c625ca90ff97afb1c88b688293fd1ac4afa14638012`
- `diag.zag` -- self-check diagnostic, 3/3 byte-identical,
  sha256 of output `8a86b09353bc4327222c04a417d0462e9a1b4e35a9f0ae9d8d41bd35b02aae4e`.

## 3. THE BLOCKER, STATED PRECISELY

`run_ep` returns an internally inconsistent result record. Observed on every
one of 5 probe episodes (3 training families, 1 RELATED, 1 RELATED/COLD),
byte-identical each time:

```
EX=256 SA=1 VA=0 R=0 RND=64 AR=0 RR=65536 RA=1677721856 NS=1080295425
```

Why this is inconsistent and not merely "the learner failed":

1. `EX`, `RND`, `VA`, `R`, `AR` are **plain stores** into the record
   (`set32(res,0,EX)`, `set32(res,10,RMAX())`, `set32(res,8,1)`) and they
   land correctly: 64 rounds really were executed, and the not-reached branch
   really was taken.
2. `SA` (`res[1]`) is accumulated by `set32(res,1,get32(res,1)+cnt)` once per
   enabled tier per round. With 64 rounds and a budget of 24 hypotheses per
   round, any run that executed the search loop at all must accumulate at
   least in the hundreds. It reads 1.
3. `RR`/`RA`/`NS` (`res[5..7]`) are read-modified-written only inside the
   round-1 reuse phase, which is unreachable for a fresh state with an empty
   PLAN table. They read 65536, 1677721856 and 1080295425 -- values with no
   path to them in the source.
4. `diag.zag` sections D2-D4 show `set32`/`get32` round-trip, overlapping
   4-byte stores, and read-modify-write inside a `while` loop are all exactly
   correct on this host, and `diag.zag` D5/D6 confirm the binomial table and
   LCG. So the primitives are sound and the discrepancy is localised to
   `run_ep`'s search/reuse accounting.

I could not localise it further within this lane's budget, and I will not
guess. The two candidate explanations -- a genuine miscompilation, or an
out-of-bounds write from `run_ep` corrupting a neighbouring buffer -- are
both testable by the next experiment (section 6) and both must be excluded
before any result from this design is credible.

## 4. TWO REAL IMPLEMENTATION BUGS FOUND AND FIXED (mine, not the toolchain)

Recorded because both produced **silent hangs with no error**, which is
exactly the failure mode that wastes a lane's budget.

1. **Binomial table row stride.** Rows were written 8 bytes apart while a row
   needs 24 bytes (6 i32), so rows overwrote each other; `ncr` then returned
   wrong block sizes. Fixed to a 24-byte stride; verified by `diag.zag` D5
   (`C(11,3)=165`, `C(12,4)=495`).
2. **Combinatorial unranking.** `unrank` computed the block size `C(n-p, r)`
   once before the scan loop and never recomputed it as the candidate `p`
   advanced. For `k=4, t=494` this walked off the end and looped forever.
   Fixed by recomputing the block size inside the loop.

## 5. TOOLCHAIN NOTES FOR THE NEXT WORKER (all verified this lane)

These cost most of the lane's budget and are not in the brief.

- The return type on `fn` is **mandatory**. `fn f(a:i32) { ... }` fails with a
  misleading "unknown type '{'". Use `fn f(a:i32)i32 {` or `...void {`.
- `->i32` is **not** valid; write `)i32 {`.
- `if`/`else` **nesting must stay shallow** (the brief says <=3). An 11-deep
  `if` chain compiles as top-level garbage and is reported as a `let`-after-
  control-flow "top-level mutable globals" error.
- An `i32` passed where a `[]u8` is expected is **accepted by the compiler**
  and becomes a slice of nonsense length; `o_app` then loops over garbage.
  This is a silent, unbounded hang. Never pass `0` as a string.
- `fn f(...)T {` is valid, but `fn f(...)T:i32 {` is not.
- Do not use an i64 decimal formatter copied from the brief. An all-i32
  `o_num` (digit count by repeated `/10`, `if(y==0){ b[p]=48; }` before the
  digit loop -- dropping that line makes zero print as *nothing*) is correct
  and is what `diag.zag` and `p5.zag` now use.
- `o_num` callers must write the separator byte; returning `end+1` without
  writing it leaves stale bytes from a previous, longer line in the buffer
  and produces convincing-looking garbage.

## 6. NEXT EXPERIMENT (in priority order)

1. **Localise the `run_ep` discrepancy.** Build a reduced `run_ep` that does
   exactly one round and one tier, printing `cur`, `tot`, `room`, `take`,
   `cnt`, `budget` and `found` per iteration. If those scalars are correct
   and only the record is wrong, it is a store bug; if `take`/`room` are
   wrong, it is an arithmetic bug in my code, not a compiler one.
2. **Bounds-harden the arena.** Add an explicit bounds assertion helper and
   route every `set32`/`get32` on `L`, `SCR`, `res`, `EXB` through it, so an
   out-of-bounds write fails loudly instead of corrupting a neighbour.
3. **Re-run the frozen prereg unchanged.** No bar, condition, arm, metric or
   seed may be moved. If the corrected run then fails a bar, that failure is
   the result and must be reported as such.
4. Only after K10/K11 pass may any meta-learning claim be entered in the
   ledger. The prereg's section 9 admissions stand unchanged and must be
   carried into the ledger entry: the hypothesis grammar is researcher-
   authored, and the meta-structure's **form** (sort by count, sort by wins,
   mean prior failures plus two) is researcher-supplied with only the values
   learned. That is the same boundary C456 (LM1) and C408's MP-3 entry
   admit. If this lane eventually passes, it will have the same shape.

## 7. BOUNDARIES

- Zero scientific claims. No examples-to-criterion, cost, reuse, newly-created
  -structure, negative-transfer or ablation number exists from this lane.
- The prereg is intact and reusable as-is; nothing in it was weakened,
  reinterpreted, or amended after implementation began.
- The COGOPS frozen prefix was used for its learner-state memory model and
  byte-offset conventions only. `ret_spec/vfy_spec/cnt_spec/execute_plan_iter`
  were not exercised, and nothing here says the COGOPS composition machinery
  is meta-learned.
- `diag.zag`'s PASS on the arena primitives is a *negative* result about the
  toolchain (it argues against a naive "flat-arena indexed reads are
  miscompiled" story of the kind brief 4.1 already doubted for B16). It is
  not evidence about the learner.
