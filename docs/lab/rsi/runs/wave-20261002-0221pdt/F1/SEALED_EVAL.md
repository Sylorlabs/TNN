# SEALED_EVAL.md - F1 POLICY-C sealed evaluation results

Lane F1, wave wave-20261002-0221pdt. Sealed runs executed 2026-10-02
~02:40 PDT against the frozen binary `impl/f1_learn_c` (sha256
772e9e2776fc6b1e681676fb4b122c57db05a0b8aff4e3d2b56d2df72d43c6a0,
verified before running; match confirmed by the run script's frozen
hash check). Control binary: the 2321pdt windowed-trigger
`impl/f1_learn` (sha256
6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847,
read-only, verified before running). Fresh fixtures: sealed6/
(manifest sealed6/FIXTURE_SHA256.txt, all hashes verified before
runs). Ordering: prereg committed alone at 835eebf71 (2026-10-02
09:34:08 UTC) before any implementation file existed (implementation
committed at 97d1ce0db); fixtures and manifest committed at
409607f81 before any sealed run; no fresh fixture generated, no probe
built, and no fresh learner run executed before the prereg commit
(only read-only inspection of prior-wave traces and a smoke test of
the new binary on prior-wave fixtures).

No em-dashes are used in this document.

## 1. Determinism evidence

78 invocations x 3 repetitions (runs6/1, runs6/2, runs6/3; 468
output files per repetition). All corresponding outputs are
byte-identical across the three repetitions (cmp-verified, zero
diffs). SHA-256 of all 468 runs6/1 outputs is recorded in
runs6/DETERMINISM_SHA256.txt. Zero randomness in decision paths. The
determinism standard (prereg section 8) is met.

## 2. K-CUM-FIRE: fires on sparse interleaved errors (PASS)

Fresh sealed sparse patterns, new binary, seed state in (bar: at
least one TRIGGER with episode index < 24):

| pattern | trigger line | bar |
|---|---|---|
| sF 1-in-9 (E at 0, 9, 18) | TRIGGER 9 cumfail=2 buf=8 | PASS |
| sG 1-in-12 (E at 0, 12) | TRIGGER 12 cumfail=2 buf=8 | PASS |

The trigger fires at the 2nd cumulative failure on both patterns,
exactly as the frozen design predicts (episodes 9 and 12).

## 3. K-CUM-GAP: the gap premise holds (PASS; not void)

Windowed control binary on the fresh sparse trains:

| pattern | control TRIGGER lines |
|---|---|
| sF_train | 0 |
| sG_train | 0 |

The windowed trigger provably never fires here (failure gaps of 9
and 12 exceed WIN=8, so no 8-episode window ever holds 2 failures),
and the control run confirms 0 triggers empirically. The sparse-gap
premise is true; the prereg is not void. POLICY-C fires exactly where
the windowed trigger is blind.

## 4. K-CUM-TRACE: construction follows the trigger (PASS)

CONSTRUCT events on the fresh sparse trains (bar: at least 2,
episode-indexed at or after the first TRIGGER):

sF_train:
- CONS 9 0 EQ p1=0 p2=8 p3=9 err_before=2 err_after=1
- CONS 9 1 ADD p1=0 p2=0 p3=0 err_before=1 err_after=0

sG_train:
- CONS 12 0 EQ p1=0 p2=8 p3=9 err_before=2 err_after=1
- CONS 12 1 ADD p1=0 p2=0 p3=0 err_before=1 err_after=0

Two construction events on each pattern, both at the trigger
episode, driving buffer error to zero. The learned structure is
[EQ r0,f0,f1; ADD r0,r0,r0; WRITE r0], computing 2 iff x0==x1 else 0.
No structure isomorphic to it existed in learner state before the
first construction event (seed holds [WRITE r0] only).

## 5. K-CUM-LEARN: the trigger enables learning (PASS)

Hidden accuracy on sealed 30-probe sets, trained state in (bar: at
least 80 percent):

| pattern | hidden | bar |
|---|---|---|
| sF | 30/30 = 100% | PASS |
| sG | 30/30 = 100% | PASS |

The learner discovers EQ and the 2x scaling from sparsely
interleaved streams. Firing without learning would fail here; it
does not.

## 6. K-CUM-CLEAN: no false positives (PASS)

TRIGGER lines on clean runs (bar: 0; frozen false-positive rate 0):

| clean run | triggers | bar |
|---|---|---|
| c0 (fresh zero-kind, seed state, 30 eps) | 0 | PASS |
| cA (prior zero fixture, seed state) | 0 | PASS |
| cB_clean (prior sum2 fixture, sum2-trained state) | 0 | PASS |
| cC_clean (prior quad fixture, quad-trained state) | 0 | PASS |

## 7. K-REG-IDENTITY: dense streams behave identically (PASS)

New binary on the prior wave's dense interleaving fixtures:

| pattern | old first-trigger ep | new first-trigger ep | normalized traces | hidden |
|---|---|---|---|---|
| T-A alternating | 2 | 2 | identical | 30/30 |
| T-B 1-in-3 | 3 | 3 | identical | 30/30 |
| T-C 1-in-4 | 4 | 4 | identical | 30/30 |
| T-D bursty | 1 | 1 | identical | 30/30 |

Normalized traces (TRIGGER lines reduced to their episode index; the
only textual difference between the binaries is the trigger field
format `cumfail=` vs `winfail= win=`) are byte-identical old-vs-new
on all four patterns. Hidden accuracy equals the old 30/30 on all
four. The cumulative trigger preserves dense-stream behavior exactly,
as the frozen superset property predicts.

## 8. K-REG-RW3, K-REG-W2W3: passing families preserved (PASS)

- rW3 (law change 2x->4x): new binary hidden 30/30; 2 CONSTRUCT
  events; normalized trace identical to the old binary (TRIGGER 2,
  14, 16, 18; 2 constructs; 3 stalls). PASS.
- w2 (2021pdt y=2(x0+x1)): new binary hidden 30/30;
  normalized-identical to the 2021pdt v4 trace. PASS.
- w3 (2021pdt law change): new binary hidden 30/30;
  normalized-identical to the 2021pdt v4 trace. PASS.

## 9. K-REG-7300: no label flips on the 24-world corpus (PASS)

New binary on the 7300-series sum2 worlds vs the windowed binary's
frozen labels (SEALED_EVAL_REPAIR2.md section 3):

- 20 CORRECT seeds: all stay CORRECT (hidden >= 80%).
- 4 OVERFIT seeds (18, 19, 20, 21): all stay OVERFIT.
- CORRECT-to-OVERFIT flips: 0. OVERFIT-to-CORRECT flips: 0.

## 10. K-REG-RW2: constructor-overfit outcome preserved (report-only)

New binary on rW2: hidden 0/30 (old: 0/30); 8 triggers at the same
episodes as the old binary (1, 4, 7, 11, 13, 15, 17, 20); 4
constructs; 8 stalls; normalized trace identical to the old binary.
The outcome class is preserved: the cumulative trigger keeps
attempting repair on the overfit seed exactly as the windowed trigger
did, and the greedy-trial overfit (proven pre-existing constructor
limitation) is unchanged. This bar is non-decisive by frozen design.

## 11. K-ABL-SPARSE and K-BASE-SPARSE (PASS)

sF_hidden (30 probes): trained 30/30 = 100%; seed-state (ablated)
17/30 = 56%; exact-match memorizer (24-episode budget) 17/30 = 56%.

- K-ABL-SPARSE: 100 - 56 = 44pp >= 40. PASS.
- K-BASE-SPARSE: 100 - 56 = 44pp >= 40. PASS.
  (sG margins: ablation 50pp, memorizer 50pp; both >= 40.)

The memorizer and the seed state both predict constant 0, matching
only the U episodes; the learned EQ structure is load-bearing.

## 12. K-C0A source audit (PASS)

Grep audit over the frozen lane sources (`impl/f1_learn_c.zag`,
`impl/f1_isa.zag`, `dev/*.zag`), run at implementation commit and
re-verified here:

- forbidden protected-semantic markers: zero hits.
- downgrade kill-pattern markers: zero hits.
- menu/kit/candidate-family markers: zero hits.

The only tag dispatch is the frozen ISA op dispatch (generic
execution machinery). No researcher-authored semantic cases were
added. The trigger change is one counter plus one threshold
comparison over the learner's own binary error stream.

## 13. Architecture accounting

Source diff (2321pdt `impl/f1_learn.zag` vs lane
`impl/f1_learn_c.zag`): 70 lines removed, 41 lines added, confined
to the trigger section (window win/wnn replaced by the cumulative
counter; TRIGGER log line updated). `impl/f1_isa.zag` is
byte-identical to the base.

- Files outside this lane touched: 0 (0 cognition-substrate source
  lines added).
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
- New routers: 0. New task-specific handlers: 0.
- Capability-source delta: the new capability (repair attempts on
  sparsely interleaved error streams) comes from the monitor's memory
  horizon, not from new researcher-written machinery.

## 14. Verdict: BUILD-PASS

Every decisive frozen bar passes: K-CUM-FIRE, K-CUM-GAP,
K-CUM-LEARN, K-CUM-TRACE, K-CUM-CLEAN, K-REG-IDENTITY, K-REG-RW3,
K-REG-W2W3, K-REG-7300, K-ABL-SPARSE, K-BASE-SPARSE, K-C0A, and the
3/3 determinism standard. K-REG-RW2 is report-only by frozen design
(outcome class preserved). No bar was weakened; no frozen bar from
PREREG_F1.md or PREREG_TRIG.md was altered.

This is not a promotion and not an L3 claim. The bounded L2+
ceiling stands. POLICY-C is generic infrastructure: it enables
repair attempts on sparsely interleaved error streams but invents
nothing itself. The constructor limitation proven on rW2 (greedy
depth-1 trial overfit) is untouched by this lane and remains open.

## 15. Evidence paths

- PREREG_F1_REPAIR.md (frozen definitions, rules, bars; commit
  835eebf71, alone)
- impl/f1_learn_c.zag, impl/f1_isa.zag, impl/f1_learn_c (frozen
  binary sha256
  772e9e2776fc6b1e681676fb4b122c57db05a0b8aff4e3d2b56d2df72d43c6a0;
  implementation commit 97d1ce0db)
- dev/f1_wgen2.zag, dev/f1_wgen2 (fresh fixture generator)
- dev/csig.zag, dev/csig (trace signature probe)
- dev/f1_score, dev/f1_score.zag (read-only scorer copy)
- sealed6/ (8 fresh fixtures, run_sealed6.sh, FIXTURE_SHA256.txt;
  fixtures commit 409607f81 before any sealed run)
- runs6/ (1, 2, 3 repetitions; DETERMINISM_SHA256.txt)

No em-dashes are used in this document.
