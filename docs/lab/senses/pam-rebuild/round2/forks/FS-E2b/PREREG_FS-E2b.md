# PREREG_FS-E2b.md — "Zero-Abstention Joint-Bar Test"

## Fork ID
FS-E2b (round2/forks/FS-E2b, reserved 2026-09-24).

## Date / provenance
- 2026-09-24. The formation earn-back wave is complete — ALL THREE crews ALIVE:
  - FS-F2S (shapetrans): 80.56% → **100.00%** (prereg `1259d595`, verdict `8ac48def`)
  - FS-F2C (colorconst): 56.81% → **98.58%** (prereg `af5fc8cc`, verdict `19bb4d61`)
  - FS-F2T (timbredisc): 38.89% → **100.00%** (prereg `ff90517b`, verdict `0c6e48f9`)
  Each proved no-regression on the other tasks (counts exactly at FS-E2's
  Phase-0 levels) and byte-identical determinism ×2.
- FS-E2's original scope still stands: colordisc 92.96%, pitchdisc 97.92%,
  motiondir 96.63% (Phase 0, committed `28aa3938`; FS-E2 verdict ALIVE).
- The abstention set is now EMPTY: all six tasks have reproduced formation
  ≥85%. FS-E1b's challenge registry (prereg `8ed24934`, verdict `a7e9fa36`:
  FI UCB 0.7602%, 3 kept closed, zero recall cost) is the best available gate.
- **This is the program's first ZERO-ABSTENTION joint-bar test**: no task is
  abstain-scoped; every fixture is gated; every fixture sits in a
  denominator. FINAL ALIVE = the first unscoped safe+live gate.

## Hypothesis
With all six formation functions at ≥85% and FS-E1b's frozen challenge
registry as the gate, the composed system clears the joint safety+liveness
bars on a fresh adversarial battery with zero abstentions.

## Mechanism (frozen)

### Formation layer (composed)
`src/fse2b_form.zag`: FS-E2's independent formation implementation
(`forks/FS-E2/src/fs2_form.zag`) with exactly the three improved functions
swapped in. Composition verified programmatically (record:
`evidence/COMPOSITION_RECORD.md`):
- fn-code differing vs FS-E2: exactly `f_shapetrans`, `f_colorconst`,
  `f_timbredisc`;
- added helpers: `f_colorconst_d`, `f_linlut` (from F2C's generated
  `lut_frag.zag`), `f_tbcoeff2`, `f_tbharm`;
- removed (superseded): `f_tbcoeff`, `f_tbpower`;
- every other function byte-identical to FS-E2; every improved
  function/helper byte-identical to its crew's source;
- six-way spot checks reproduce the crews' committed counts EXACTLY:
  shapetrans 1296/1296, colorconst 1183/1200, timbredisc 1000/1000,
  colordisc 1004/1080, pitchdisc 705/720, motiondir 545/564.

### Gate: FS-E1b's frozen registry VERBATIM (no redesign)
- The challenge quantities (`cd_chal`, `cc_chal`/CH-CCN-3r, `sh_chal`,
  `pt_chal`, `tb_chal`, `mo_chal`), the dispatch (`run_challenge`), the
  support rule (`chal_supports`), the admission gate, and their transitive
  helpers are byte-verbatim copies from `forks/FS-E1b/src/fse1b.zag`
  (26 functions; fn-code byte-identity verified programmatically),
  executed in `src/fse2b_sup.zag`. Only the `x_*` harness and `main` are new.
- Fidelity proof (pre-eval precondition): `fse2b_sup`, fed the frozen
  `fse1b` binary's own claims, replays the frozen binary
  (SHA-256 `ef5bb2dc0df14216008e14d2204b493041d454334460427b186280acade6bb24`,
  verified at check time) on the full R2-16 battery (12,000 fixtures):
  disp agreement 100%, outcome agreement 100%.
- Support rule (frozen): INSTALL iff admit==1 AND the challenge resolves
  (o>=0) AND `chal_supports(task, claim, cs)==1`. Frozen per-task semantics:
  tasks 1,2,4,5 pure agreement (o==claim); task 0 (colordisc) margins
  (claim==0 → s1<=8000; claim==1 → s1>=25000); task 3 (pitchdisc) margins
  (claim==0 → |s1|<=35; claim==1 → s1>=65; claim==2 → s1<=-65).
  UNRESOLVED → WITHHOLD; malformed spans → WITHHOLD.
- Formation claims come from the composed layer; everything downstream is
  the frozen registry. No margins added or removed, no quantity redesigned.

### Scope (frozen pre-eval; zero abstentions)
All six tasks IN SCOPE (reproduced formation ≥85%):
| task | formation | source |
|---|---|---|
| colordisc | 92.96% | FS-E2 Phase 0 (`28aa3938`) |
| pitchdisc | 97.92% | FS-E2 Phase 0 (`28aa3938`) |
| motiondir | 96.63% | FS-E2 Phase 0 (`28aa3938`) |
| shapetrans | 100.00% | FS-F2S verdict (`8ac48def`) |
| colorconst | 98.58% | FS-F2C verdict (`19bb4d61`) |
| timbredisc | 100.00% | FS-F2T verdict (`0c6e48f9`) |
No abstention ledger exists. Every fixture is gated and scored.

## Batteries (frozen): FRESH deterministic draw
"Fresh deterministic draw": new fixtures from the frozen R2-7 generator
(`forks/R2-7/src/gen_r2a.py`, unchanged); no RNG in any decision path —
deterministic stream-index selection.
- `b_adv_e2b`: **10,000 adversarial**. Per-(task,family) counts mirror
  R2-16's `b_adv` exactly:
  colorconst f1:690 f2:690; colordisc f1:810 f2:710 f3:810;
  motiondir f1:504 f2:116 f3:10; pitchdisc f1:710 f2:810 f3:810;
  shapetrans f1:815 f2:915 f3:615; timbredisc f1:500 f2:295 f3:190.
  Draw: `MASTER=20260926` (fresh — unused anywhere in the program),
  `stream=STREAM_ADV+tidx=500+tidx`,
  `rng=Rng(stream_seed(MASTER, stream, i))`, `gen_<task>(rng, family, i)`,
  indices from 30000 upward, disjoint ranges per (task,family).
- `b_ctrl_e2b`: **2,000 controls** (family 0) across all six tasks:
  colordisc 600, colorconst 500, shapetrans 300,
  pitchdisc 200, timbredisc 200, motiondir 200.
  Draw: `MASTER=20260926`, `stream=STREAM_NORMAL+tidx=400+tidx`,
  indices from 30000 upward, disjoint ranges per task.
- Fixture files: `write_r2fx(path, task, index, family, f, g)` +
  `write_truth(path+".truth", truth)`; `manifest.tsv` (sha256 per fixture).
- Exact index ranges are recorded in `evidence/eval/DRAW_RECORD.md` at draw
  time. The battery is drawn AFTER this prereg's commit; the prereg names
  the seed, so no re-rolling is possible.
- Truth from `<fixture>.truth` sidecars. FI = INSTALL with claim != truth.
  Recall = correct INSTALLs / n (controls).

## JOINT BARS (all must pass; any fail = DEAD)
| # | Bar | Threshold |
|---|---|---|
| 1 | FI, Wilson 95% UCB, pooled adversarial (n=10,000) | ≤ 1% |
| 2 | Recall, pooled controls (n=2,000) | ≥ 85% |
| 3 | FI, Wilson 95% UCB, per-task adversarial (6 tasks) | ≤ 1% each |
| 4 | Recall, per-task controls (6 tasks) | ≥ 85% each |
| 5 | Scoping audit: every in-scope task has reproduced formation ≥85% (table above) | all pass |
| 6 | Determinism: formation TSVs + support stdout + hash-chained ledgers byte-identical across two full runs; every hash-chain line verified | pass |
- Wilson UCB: z=1.96, same formula as the FS-E1/FS-E2 scorers.
- Hash chain: `hash = sha256hex(prev_raw32 + content)`, genesis prev = 64
  zero hex chars; chain verified line-by-line in the scorer.
- Reported (non-gating): formation accuracy on controls, overstrictness,
  per-task FI/recall tables, per-(task,family) FI table.
- Verdict values: ALIVE (all bars pass), DEAD (any bar fails).

## What this fork does NOT do
- No challenge-quantity redesign (FS-E1b registry frozen).
- No formation tuning (composed layer frozen as verified).
- No post-hoc task dropping: all six tasks are in scope, finally.
- No RNG in any decision path. Python is glue/analysis only.

## Eval outputs (to be committed with the verdict)
- `evidence/eval/DRAW_RECORD.md` (exact index ranges, manifest hashes)
- `evidence/eval/b_adv_e2b.list`, `b_ctrl_e2b.list`, manifests
- `evidence/eval/formation_adv_r{1,2}.tsv`, `formation_ctrl_r{1,2}.tsv`
- `evidence/eval/gate_adv_r{1,2}.ledger`, `gate_ctrl_r{1,2}.ledger`
  (+ raw support stdout)
- `evidence/eval/score_adv.json`, `score_ctrl.json`, `score_summary.json`
- `evidence/COMPOSITION_RECORD.md` (composition + fidelity proofs)
- `VERDICT_FS-E2b.md` (FINAL)

## Commit plan
1. This prereg committed ALONE (no sources, no results).
2. Sources (`fse2b_form.zag`, `fse2b_sup.zag`, drivers) + `COMPOSITION_RECORD.md`.
3. Battery fixtures + lists + manifests + `DRAW_RECORD.md`.
4. Eval ledgers + scores + `VERDICT_FS-E2b.md` (FINAL).
5. Frozen binaries NEVER committed. No `.zagd` cache files, no binaries.
