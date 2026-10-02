# ECON RESULT: Invention Economics (Program 6)

Prereg: 2557d3106 (frozen before implementation).
Implementation: econ.zag (this directory).
Raw: ECON_RAW_1.txt (md5 0e52918ff496a873ad06fd1f87aaaf5a).
Determinism: 3/3 byte-identical, exit 0, zero stderr on all runs.
Governance: pure Zag, zero Python at any stage; zero em-dash bytes;
prereg strictly precedes implementation.

## E1: persisted selected intervention (macro)

Worlds W_k, k=1..5. World 1 selects M=[S,W,OZ] (18 checks, the creation).
M persisted verbatim as a 5th primitive for worlds 2..5.

| world | scratch checks | macro checks | scratch seq | macro seq |
|---|---|---|---|---|
| k=1 | 18 | NA | [S,W,OZ] | (created here) |
| k=2 | 17 | 22 | [S,W,OY] | [S,W,OZ,OY] |
| k=3 | 85 | 124 | [S,W,W,OY] | [S,W,OZ,W,OY] |
| k=4 | 381 | 658 | [S,W,W,W,OY] | [S,W,OZ,W,W,OY] |
| k=5 | 1613 | 3376 | [S,W,W,W,W,OY] | [S,W,OZ,W,W,W,OY] |

- All selections verified: simulated q0 != q1, exactly 1 real execution,
  correct elimination for both true hypotheses (E1OK=1).
- Per-world net (scratch - macro): -5, -39, -277, -1763. All negative,
  gap widening with depth.
- E1NET = -2084 checks. Storage = 3 bytes.
- Why: M bakes an early OZ observation useless for deeper worlds; base-5
  enumeration inflates search while macro solutions are LONGER in actions
  (4,5,6,7 vs 3,4,5,6). The learner reuses M, but reuse is anti-economical.
- K1 PASS, K2 PASS (real==1 everywhere), K3: ECON-NEGATIVE.

## E2: retained offset-form state

Reproduction (K4): A_ret=13, A_fresh=13, B_ret=10, B_fresh=13. Exact match
to I2. K4 PASS.

| family | retain | fresh | saving |
|---|---|---|---|
| A (x+3) | 13 | 13 | 0 (creation rides free) |
| B (x+7) | 10 | 13 | 3 |
| C (x+12) | 10 | 13 | 3 |
| D (x+1) | 10 | 13 | 3 |
| E (x+20) | 10 | 13 | 3 |
| F (3x, non-offset) | 16 | 16 | misfit 0 |

- E2SUM: saving=12 examples, misfit=0, create_extra=0.
- Storage: 12 bytes (offset_hyp, trusted, form_known).
- Break-even p_star = 0%: persistence has non-negative expected net at ANY
  same-form probability, because the trust/distrust check fires on the
  first misprediction and bounds the downside at zero.
- K5 PASS, K6 PASS (misfit=0), K7 PASS (p_star=0).

## Verdicts

- S1 macro: ECON-NEGATIVE (net -2084 checks over 4 worlds, 3 bytes stored).
- S2 offset form: ECON-POSITIVE (net +12 examples over 4 families,
  0 extra creation cost, 12 bytes stored, zero misfit).
- Overall: ECON-MIXED.

## Answer to the key question

Persist a structure when (a) it compresses future work each time it
applies (offset schema: 3 examples saved per family, recurring),
(b) its creation rides free on learning done anyway (create_extra=0),
and (c) a cheap verification check bounds misfit cost near zero
(distrust on first misprediction). Do NOT persist a bare solution
instance: the macro added a permanent branching factor (base 4 to base 5)
without compressing any future search, so its net was negative at every
tested scale and worsening with depth (-5 to -1763). Schemas amortize;
instances do not. Scale rule: net(n) = n * saving_per_use - creation -
carrying; for the offset form, net(n) = 3n > 0 from the first reuse.
