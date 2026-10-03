# PREREG.md -- H3 Dataflow Generality on Arithmetic to Planning

Frozen 2026-10-02, before implementation. This preregistration strictly
precedes all implementation work.

## Question

H1 (learned typed contracts) and H2 (value-level function composition)
both generalize to arithmetic to planning with mechanism logic unmodified
(H1: 3 tries, H2: 6 tries; commit 0c6cfa780, prereg aa708f552).

H3 (generic dataflow) is canonical on chain to count (clean reproduction
PROCESS-PASS, xdomain_dataflow_clean/). Does H3's mechanism logic also
generalize to arithmetic to planning unmodified, or is it chain to count
specific?

## Domain pair (same as H1/H2 generality test)

- X = SUM (arithmetic, node to number). Facts r=71: (101,71,5),
  (101,71,3), (101,71,7). X(101)=15. Second: (102,71,4), (102,71,6).
  X(102)=10. Learned by the base sum trial template as pure unrolled
  INC chains (t2_asm_sum).
- Y = PLAN (goal-directed action sequences, number to node). Facts r=82:
  (15,82,201), (201,82,202), (202,82,203). Y(15)=203. Second:
  (10,82,211), (211,82,212), (212,82,213). Y(10)=213. Learned as
  guard/set chain MAPs.
- Z = plan(sum(s)): query (103,93) to 203. Requires sum(103)=15, then
  the plan 15 to 201 to 202 to 203 taught in Y1. Z facts: (103,71,6),
  (103,71,9). Fresh subject 103. Query relation 93 is new. No X/Y
  pairing taught. No hint. No label.
- Z2 reuse: (104,71,4), (104,71,6); sum(104)=10; query (104,93) to 213
  via the promoted dataflow wiring (DF-REUSE path).

## Mechanism under test (verbatim, unmodified)

`df_patch.zag` from `xdomain_dataflow_clean/` (canonical H3):
- `df_build_reg`: procedure registry from MAPs with field12>0.
- `df_try`: discovery (P with facts from s, execute to mid, Q with
  facts from mid) and reuse (promoted wiring record).
- `df_exec_sub`: structure-derived execution. INC cells present
  implies count links (`df_count_links`); otherwise walk to endpoint
  (`df_walk_end`).
- Hook in `ev_query` between rebind and trial.

Only behavior implementations are new (the driver: teaching sum/plan
facts, setting fact_rel, arms). Mechanism logic is byte-identical.

## Arms

- TREAT: train X, train Y, set fact_rel (91 to 71, 92 to 82), gap,
  Z facts, Z query, Z2 reuse query.
- ABL-X: as TREAT but delete r=91 MAPs before Z.
- ABL-Y: as TREAT but delete r=92 MAPs before Z.
- FRESH: gap, Z facts, Z query (no training).
- NO-DF: TREAT with `df_on()=0` (separate binary, mechanism disabled).

## Frozen kill bars

- K1 SOLVE: TREAT Z answers 203.
- K2 CAUSAL: ABL-X, ABL-Y, FRESH all answer -2 (no Z MAP promoted).
- K3 MECHANISM-CAUSAL: NO-DF TREAT answers -2.
- K4 LEARNED-NOT-ASSIGNED: grep audit of `df_patch.zag` finds zero
  93/91/92/71/82 literals in mechanism code (driver may contain them;
  the mechanism must not).
- K5 DETERMINISM: 3/3 runs byte-identical (sha256).
- K6 NO-TEMPLATE: no ARITH_TO_PLAN (or SUM_TO_PLAN) literal in any
  source file.
- K7 REUSE: Z2 answers 213 via DF-REUSE (no re-discovery).

Verdict XDOMAIN-H3-ARITH-COMPLETE requires K1 through K7 all PASS.
Any FAIL is reported honestly with white-box diagnosis.

## Honest boundaries (declared in advance)

- Behavior implementations (sum/plan teaching) are researcher-authored;
  composition is under test, not behavior induction.
- `df_set_factrel` simulates the learner recording which fact relation
  each procedure consumes (same as H3 original).
- Expected answers used for verification (K1/K7). Learner-owned
  verification is future work.
- The base sum trial branch is gated on a combination-context node
  (tag 8); the driver creates one per arm (precedent: xio_general,
  C269 ap_driver). It teaches no facts and no answers.
- One domain pair. Level 1 (exact reuse) only.

## Three-way comparison (to be filled after runs)

| Mechanism | Z tries | Z2 tries | Verdict |
|-----------|---------|----------|---------|
| H1 typed  | 3       | 3        | PASS (0c6cfa780) |
| H2 value  | 6       | 5        | PASS (0c6cfa780) |
| H3 dataflow | ?     | ?        | THIS WORKER |
