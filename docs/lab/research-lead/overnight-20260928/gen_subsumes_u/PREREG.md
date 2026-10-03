# PREREG: GEN-SUBSUMES-U (overnight priority #10: architecture compression)

Date: 2026-10-03. Worker: GEN-SUBSUMES-U.
Lane: `docs/lab/research-lead/overnight-20260928/gen_subsumes_u/`
Branch: `lane-gensubsumesu-20261003` (isolated; explicit pathspecs only).

## 1. Question

Does GEN (the value-graph generalization of U, from COMPOSE-PAIR6-ADV)
subsume U (the unified behavior-contract operation, from COMPOSE-COLLAPSE)
entirely? Concretely: run GEN on all 5 of U's linear pipeline pairs. If GEN
reproduces U's answers on all 5, U is a special case of GEN (single-round,
linear pool) and U should be retired as a separate mechanism. If any pair
fails, that pair is the residual boundary.

## 2. Background and baselines (frozen, from committed reports)

U's operation (ref_uc_uni.zag, frozen): kind-set contracts, one admission
rule (predicted handshake: single admitted iff goal kinds fit A.in/out;
pair (A,B) admitted iff kin fits A.in, A.out INTERSECTS B.in, kout fits
B.out), ordered trial (singles then ordered pairs), end-to-end verification,
failure-triggered widening (WIDEN=1), success-recording with contract growth.

GEN's operation (d6_gen.zag, frozen): keeps every U principle; generalizes
the trial space from {singles, ordered pairs} to rounds over a value pool,
and replaces the predicted pair handshake with observed-kind checking
(stage 1 executes; stage 2 tests the observed value's kind).

U's 5 linear pipeline pairs (the primary set; each a single query on a
fresh arena). Baselines are U's recorded ANS values:

| # | World | Query (s,kin,kout,exp,nm) | U ANS | U TRIES | Source |
|---|-------|---------------------------|-------|---------|--------|
| P1 | collapse setup_p1 | (61,1,1,65,2) | 65 | 3 | compose_collapse REPORT |
| P2a | collapse setup_p2a | (41,1,2,2,4) | 2 | 3 | compose_collapse REPORT |
| P2b | collapse setup_p2b | (41,1,2,2,4) | 2 | 7, WIDEN=1 | compose_collapse REPORT |
| P3 | collapse setup_p3 | (31,1,2,2,4) | 2 | 3 | compose_collapse REPORT |
| Q1 | pair5 p5facts+p5taught | (205,1,2,1,4) | 1 | 2 | compose_pair5 REPORT |

Secondary arms (U baselines from the same reports):
- Q2 (p5facts+p5abx, (205,1,2,1,3)): U ANS=-2 TRIES=7 WIDEN=1 (honest fail)
- Q3 (p5facts+p5aby, (205,1,2,1,3)): U ANS=-2 TRIES=6 WIDEN=1 (honest fail)
- Q4 (p5facts+p5fresh, (205,1,2,1,4)): U ANS=1 TRIES=5 (fresh learner)
- P5 growth (setup_p2b arena, P2b solved, then setup_p5extra, query
  (51,1,2,3,4)): U ANS=3 TRIES=4; census m0 inmask=1 outmask=3 n=3
  (contract grew from P2b's success-recording: X.out {2} -> {1,2}).

All entity/relation identifiers are opaque integers (31/41/51/61/81/82;
201-206/211-213/221-222/91/92/93). No domain labels are used in this
experiment's design, code, or docs. The pair5 world-builder comments
inherited from the frozen source contain domain words; they are copied
verbatim for world byte-fidelity and are not this experiment's design
language.

## 3. Build plan (implementation follows this prereg commit)

Assembly `gsu_full.zag` (pure concatenation, no logic edits):
1. Lines 1-301: byte-verbatim copy of
   `tnn-rsi-pair6/.../compose_pair6_adv/d6_base.zag` (GEN base: frozen
   ref_uc_base plus the two allowlisted pair6 hunks).
2. Next: byte-verbatim copy of `d6_gen.zag` lines 1-239 (GEN composer;
   its main at line 240 excluded).
3. Next: byte-verbatim copy of
   `tnn-rsi-pair5/.../compose_pair5/p5_full.zag` lines 336-391 (the five
   pair5 world-builder functions; pair5 main excluded).
4. New `gsu_main.zag` (the ONLY new code): runs the 9 arms below through
   `gen_solve`/`gen_report`/`gen_census`, then `o_flush`. No admission,
   execution, widening, or recording logic.

K6 verifies by diff: region 1 empty vs d6_base.zag; region 2 empty vs
d6_gen.zag lines 1-239; region 3 empty vs p5_full.zag lines 336-391.

Build: pinned safebin znc (2026.07.0-dev). Run binary 3x.

## 4. Arms and frozen predictions

All arms call `gen_solve(A,B,c,s,kin,kout,exp,nm)` then `gen_report`.
Predictions derived by hand from the frozen GEN sources before running:

| Arm | Setup | Query | Predicted ANS | Predicted TRIES | Notes |
|-----|-------|-------|---------------|-----------------|-------|
| P1 | setup_p1 | (61,1,1,65,2) | 65 | 4 | route 61->63->65 |
| P2a | setup_p2a | (41,1,2,2,4) | 2 | 6 | route 41->44->2 |
| P2b | setup_p2b | (41,1,2,2,4) | 2 | 6 | no widening: observed-kind handshake admits (X,Y) directly where U's predicted handshake needed WIDEN=1 |
| P3 | setup_p3 | (31,1,2,2,4) | 2 | 6 | route 31->34->2, INTER=34 |
| Q1 | p5facts+p5taught | (205,1,2,1,4) | 1 | 6 | INTER=213 must appear (same intermediate as U) |
| Q2 | p5facts+p5abx | (205,1,2,1,3) | -2 | 3 | WIDEN=1; honest fail |
| Q3 | p5facts+p5aby | (205,1,2,1,3) | -2 | 9 | WIDEN=1; honest fail (explores 93-chain 213->222, still fails) |
| Q4 | p5facts+p5fresh | (205,1,2,1,4) | 1 | 6 | fresh learner, empty masks |
| P5 | P2b arena + setup_p5extra | (51,1,2,3,4) | -2 | 0 | PREDICTED INFORMATIVE FAIL (see Sec 6); WIDEN=1 |

P5 arm detail (the growth probe): reuse the P2b arena (A3b) after its
solve; run `gen_census` (predicted m0: inmask=1 outmask=3 inmask2=0 n=2,
i.e. the contract DID grow from P2b's success-recording via provenance
closure); then `setup_p5extra(A3b)`; then the P5 query.

## 5. Kill bars

- K1 PRIMARY SUBSUMPTION: GEN ANS equals U ANS on all 5 primary pairs
  (P1=65, P2a=2, P2b=2, P3=2, Q1=1). ANS match is the criterion.
- K2 HONEST FAILURE: GEN Q2 ANS=-2 with WIDEN=1 logged; GEN Q3 ANS=-2
  with WIDEN=1 logged. (No false positives where U honestly fails.)
- K3 FRESH LEARNER: GEN Q4 ANS=1.
- K4 GROWTH BOUNDARY PROBE: P5 predicted ANS=-2 TRIES=0 with WIDEN=1
  (stale per-query tried-state in frozen `gen_solve`: it resets tries/
  found/ans/pool/widened but NOT the tried1/tried2 tables, so the second
  query on the same arena skips every (m,0) cell, sees a quiet round,
  widens, and returns). Census must still show m0 outmask=3
  (representation-level contract growth works; the defect is trial-state
  scoping, not recording). If GEN instead returns ANS=3, the analysis is
  wrong and the verdict strengthens (see Sec 7).
- K5 DETERMINISM: 3/3 runs byte-identical stdout; stderr empty.
- K6 FIDELITY: the three diffs in Sec 3 are empty.
- K7 TOOLCHAIN: safebin active for every command; `which python3` and
  `which python` return nothing; zero forbidden-executable invocations;
  all computation pure Zag; shell only for znc/binary/git/assembly/
  byte-verification.
- K8 HYGIENE: zero em/en dash bytes in all lane docs (byte-verified).

On TRIES: equality with U is NOT required and NOT a kill bar. GEN's
pool-round enumeration is a strict generalization of U's
singles-then-pairs enumeration, so try-count differences are the
predicted cost of generality (precedent: COMPOSE-COLLAPSE declared
SUBSUMPTION at the capability level while H2 and NOKIND had different
try counts). TRIES values are reported honestly alongside ANS.

## 6. Predicted P5 mechanism (frozen analysis)

`gen_solve` resets arena offsets 936/940/944 (tries/found/ans), pool[0],
kind[0], provenance[0], nv=1, widened=0, but does not clear tried1
(2304..) or tried2 (3328..). After P2b, tried1 marks exist for all
(m,0). P5's round 1 has ns0=1, so every cell is skipped as already-tried;
nt1==nt0 and nv1==ns0 gives quiet=1, widening fires once, round 2 is
quiet again, solve returns ANS=-2 TRIES=0. U's `uni_solve` keeps no
tried-state (it re-enumerates per query), so U supports the sequential
growth query and GEN's frozen implementation does not. This is an
implementation-level state-scoping defect, not a principled limit of the
value-pool mechanism: the fix is to reset (or per-query-scope) the tried
tables in `gen_solve`. The fix is NOT implemented in this lane; it needs
its own prereg.

## 7. Verdict mapping (frozen)

- K1 and K2 and K3 PASS, and K4 returns ANS=3 (prediction wrong):
  SUBSUMES. GEN reproduces U on all 5 pairs plus honest failures, fresh
  learning, and sequential growth. Recommend retiring U as a separate
  mechanism; U becomes the documented restriction of GEN (single-round,
  linear pool, predicted handshake).
- K1 and K2 and K3 PASS, and K4 returns ANS=-2 as predicted:
  PARTIAL with boundary. GEN subsumes U on single-query linear
  composition (capability superset: everything U solves, plus the
  diamond U provably cannot solve). Residual boundary: multi-query arena
  reuse for contract growth (frozen `gen_solve` stale tried-state;
  representation-level growth intact per census). U is retained ONLY as
  the growth-behavior reference until a follow-up prereg lands the tried-
  state reset in GEN; then the verdict upgrades.
- K1 FAIL (any primary ANS mismatch): DOES-NOT-SUBSUME. Document the
  failing pair, the exact divergence, and the mechanism cause. No
  retirement recommendation.

## 8. What this establishes (and does not)

Establishes: whether GEN's answer set covers U's answer set on U's own
5 linear pairs, whether GEN fails honestly where U fails, and whether
GEN preserves U's contract-growth behavior across queries.

Does not establish: try-efficiency parity (explicitly out of scope);
behavior on non-pipeline shapes beyond the already-established diamond;
the side-effecting-MAP open question from the pair6 report (all MAPs
here are pure); whether the tried-state fix introduces regressions
(follow-up work).

## 9. Deliverables

In this lane: PREREG.md (this file), NAMECHECK.md (Step 0 guard),
gsu_base.zag, gsu_gen.zag (composer region), gsu_world.zag, gsu_main.zag,
gsu_full.zag, gsu_bin, gsu_run1/2/3.txt (+ .err), REPORT.md.
