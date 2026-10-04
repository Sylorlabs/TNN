# PREREG: Form Inventor (R1-R6 implementation)

Worker: Form Inventor Builder.
Date: 2026-09-30 UTC.
Status: FROZEN before any implementation. This file must be committed
alone before `inventor.zag` exists.

## Objective

Implement the R1-R6 invention machinery specified in
form_invent/FORMINVENT_RESULT.md section 5 (commit 3d543e38e),
which measured two failure modes of the SCALE-TESTED learner:
(a) clean failure on G and H (menu exhausted, adopted=-1, no
diagnosis), and (b) silent near-miss misapplication on G2
(F2 fits the observed buffer with a wrong causal story).
The inventor adds failure-driven structural growth on top of
the unchanged menu machinery.

## Frozen design (R1-R6)

R1. Failure diagnosis from fit residuals. When discovery exhausts
all menu forms at BMAX, the learner retains the failed buffer and
runs `diagnose`, which returns one of:
- SIG1: exactly 2 distinct object values, each occupying one
  contiguous run in subject order (STEP shape).
- SIG4: exactly 3 distinct object values, each one contiguous run
  (two-threshold shape).
- SIG3: one majority default value plus exactly 2 isolated
  exception points (each exception's subject neighbors both carry
  the default).
- SIG0: none of the above (honest failure, adopted=-1, the
  diagnosis signature is recorded).

R2. Fixed constructive operator vocabulary, frozen here before
any new family is evaluated. Terminals {subj, const}; operators
{<, ==, if-then-else}; existing menu forms usable as composable
leaves. Invented forms are expression trees in this vocabulary,
stored as a node pool in learner-created persistent state:
node = (op, a, b, c) with ops 0=CONST(c in a), 1=LT(threshold in
a), 2=EQ(point in a), 3=IF(cond node in a, then node in b, else
node in c). Root is node 0. The source contains only these
generic evaluators and the diagnosis; there is no dedicated
STEP branch, no threshold constant, and no exception-point
constant anywhere in source.

R3. Failure-driven candidate generation. From the diagnosis, the
learner builds the minimal structural repair, parameterized by
the diagnosis, never by blind enumeration:
- SIG1 -> IF(subj < T, c0, c1), T/c0/c1 from the cluster boundary.
- SIG4 -> IF(subj < T1, c0, IF(subj < T2, c1, c2)).
- SIG3 -> IF(subj == p1, e1, IF(subj == p2, e2, d)).
The candidate must exactly fit the full BMAX discovery buffer
or it is discarded.

R4. Promotion protocol with novelty check. The candidate passes
the same gates as menu forms: exact fit on the discovery buffer,
verification on fresh examples under the standard V schedule
(V from uses3, the invented form's own counter), then persistence
with uses3/strikes3 counters subject to the same retirement
policy. Novelty check rejects the candidate if it reduces to a
menu form on the evidence: threshold outside the observed subject
range (F0), duplicate exception points, or equal adjacent
constants. Tie-break principle (the G2 question): invention
fires ONLY when all menu forms fail at BMAX. When a menu form
fits at any buffer size it wins and no candidate is constructed.
On G2, F2 fits at n=6, so the menu wins and the inventor stays
silent. This is the stated tie-break.

R5. Revision. If later evidence contradicts the invented form,
the same machinery extends it. Refit for invented forms is
re-diagnosis on the R=4 buffer: if the signature matches the
live tree's construction signature, only parameters are refit
(structure transfers, no strike); if it differs, a strike is
recorded, the tree is retired, and discovery re-runs, which may
invent a new structure. H after G is the revision test:
the 1-threshold tree is contradicted and must grow into the
2-exception tree or fail honestly.

R6. C0 mapping.
- C0-A: threshold values, exception points, cluster boundaries,
  and the tree live in learner-created persistent state (node
  pool plus trace fields), with a white-box construction trace
  emitted to the log (INV DIAG/CAND/FIT/NOVEL/PROMOTE/REFIT/
  STRIKE lines). Source-audit kill bar: a dedicated semantic
  branch for STEP in source kills the claim.
- C0-B: the form is incrementally constructed
  (diagnose, candidate, fit, promote), not selected from an
  enumerated repair list; repairs are parameterized by diagnosis.
- C0-C: NOT CLAIMED here. Families K and J below are designed
  pre-freeze by the implementer; a genuine C0-C test needs
  adversary-designed families after the inventor freezes.
- C0-D: transfer via structural refit: Gp reuses the
  1-threshold structure with refit parameters at discounted V.

## Frozen family specs

Learner machinery is copied verbatim from
form_invent/finvent.zag (fit_const, fit_lin, fit_exc, fit_form,
predict for forms 0..2, prior_order, verify_need, run_family
phases, buffer handling). Only these change: state block grows
to 192 bytes (offsets 44 uses3, 48 strikes3, 52..179 node pool of
8 nodes x 16 bytes, 180 last_sig, 184 live_sig, 188 live_nodes),
predict gains form 3 (tree eval), run_family gains the inventor
hook at BMAX and the invented refit rule, and true_subj/true_obj
gain families 9, 10, 11. Menu parameters unchanged:
BMIN=6, R=4, V0=14, WMAX=3, BMAX=40.

- G (fam 6): base=6000, obj=0 for subj<6003, else 5. (as finvent)
- G2 (fam 7): base=7000, obj=0 for subj<7001, else 5. (as finvent)
- H (fam 8): base=8000, d=7, exc 8001->3, 8004->9. (as finvent)
- K (fam 10): base=10000, obj=0 for i<2, 1 for i<4, else 2
  (three contiguous clusters; SIG4 probe).
- J (fam 9): base=9000, obj=1+(i%4) (four scattered values;
  honest-failure probe, no signature fires).
- Gp (fam 11): base=11000, obj=2 for subj<11003, else 9
  (STEP with different constants; transfer probe for the
  invented 1-threshold structure).

Menu families A..E (fams 0..4) identical to lscale/finvent.

## Conditions

- FRESH: G, G2, H, K, J on fresh state each.
- RETAINED: A, B, C, D, E, G, Gp, H, G2 in one continuing run.

## Frozen predictions (K2)

FRESH:
| Run | adopted | cost | mechanism note |
|---|---|---|---|
| G | 3 | 54 | 40 discover, inventor SIG1, V=14 |
| G2 | 2 | 20 | menu F2 at n=6, inventor silent (tie-break) |
| H | 3 | 54 | 40 discover, inventor SIG3, V=14 |
| K | 3 | 54 | 40 discover, inventor SIG4, V=14 |
| J | -1 | 40 | SIG0, honest failure, diagnosis recorded |

RETAINED (A,B,C,D,E,G,Gp,H,G2):
| Run | adopted | cost | mechanism note |
|---|---|---|---|
| A | 1 | 20 | lscale curve |
| B | 1 | 11 | lscale curve |
| C | 1 | 8 | lscale curve |
| D | 1 | 6 | lscale curve |
| E | 1 | 5 | lscale curve |
| G | 3 | 54 | refit fails (strike F1), 36 discover, SIG1, V=14 |
| Gp | 3 | 11 | invented refit: SIG1 matches, params refit, no strike, V=7 |
| H | 3 | 44 | refit sig mismatch (strike inv), 36 discover, SIG3, V=4 |
| G2 | 2 | 6 | refit sig mismatch (strike inv), menu F2 at n=6 |

K2 passes iff all fourteen adopted/cost pairs match exactly AND
the log shows the predicted INV trace lines (DIAG sig per run,
PROMOTE on G/H/K/Gp/H, HONESTFAIL on J, REFIT sig_match on Gp,
STRIKE on H and G2).

## Kill bars

- K1 (R1-R6 implemented): PASS iff the source contains the
  diagnosis, the fixed operator vocabulary evaluators, the
  diagnosis-parameterized candidate builder, the promotion path
  with novelty check, the re-diagnosis refit/revision rule, and
  the persistent node pool plus trace fields; and the result
  document maps each to R1..R6.
- K2 (behavior): PASS iff the fourteen frozen adopted/cost pairs
  match exactly and the predicted INV trace lines are present.
- K3 (novelty): PASS iff the log shows the novelty check
  evaluating on every constructed candidate, and no candidate
  that reduces to a menu form is promoted; G2 must show the menu
  winning with the inventor silent.
- K4 (purity): PASS iff pure Zag at every stage (znc, bash, grep,
  git, cp, mv, md5sum only; zero Python invocations in source,
  build, execution, or analysis), zero em-dash/en-dash bytes in
  wave files (byte-checked), prereg strictly precedes
  implementation (git merge-base --is-ancestor), 3/3
  byte-identical runs, exit 0, zero stderr.

Verdict INVENTOR-TESTED iff K1..K4 all pass. This verdict covers
the test of the inventor; any L3 claim additionally needs the
11-step promotion pipeline and a post-freeze adversary (C0-C).

## Governance

- No change to fit_const/fit_lin/fit_exc/fit_form/predict(0..2),
  prior_order, verify_need, or the menu discovery/verify phases.
  Behavior on families 0..5 is unchanged from finvent.
- The operator vocabulary above is frozen in this prereg;
  adding operators or signatures after seeing results is
  forbidden (anti-treadmill).
- Commits local on tnn-native-lab, owned path form_inventor/
  only, pathspec commits. No paper edits.
