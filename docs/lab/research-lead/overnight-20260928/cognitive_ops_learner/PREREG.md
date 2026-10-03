# PREREG: COGNITIVE-OPS-LEARNER (overnight priority #5: cognitive-operation
bodies becoming learner-created)

Date: 2026-10-03. Worker: COGNITIVE-OPS-LEARNER.
Lane: `docs/lab/research-lead/overnight-20260928/cognitive_ops_learner/`
Branch: current lane branch (isolated commits; explicit pathspecs only).

## 1. Question

Can a cognitive procedure migrate from researcher-authored machinery to a
learner-owned structure? Concretely: the learner starts with a
researcher-supplied generic VERIFY procedure (checks a candidate structure
against evidence). Through experience the learner SPECIALIZES it (builds a
leaner procedure adapted to the relations it actually encounters), stores
the revised procedure as a learner-owned structure with provenance, and
later SELECTS between the original and the revised procedure based on
context (a learned applicability record), falling back to the original when
the revised procedure does not cover the query.

This directly tests Micah's priority: "Move cognitive procedures into
learner-owned structures that can be learned, selected, composed, revised,
specialized, retired, eventually created." RETRIEVE/DERIVE/VERIFY/PREDICT/
INQUIRE/CONSTRUCT must not become permanent human-authored modes; here the
procedure body lives in learner state, and selection is a data-driven
lookup in learner state, not a mode dispatch.

## 2. Design

### 2.1 The researcher-supplied procedure (vfy_gen, procedure id 0)

`vfy_gen(A, C)`: A is an arena of evidence facts, each fact an opaque
(s, r, o) integer triple. C is a candidate structure: an ordered chain of
up to 16 (s, r, o) steps. The procedure returns 1 iff every step matches
at least one fact, else 0. It is fully generic: it scans ALL facts for
every step (cost = nsteps * nfacts fact-checks, no early exit, no index,
no relation-specific logic). It is the correctness oracle for the entire
experiment: every verdict the learner produces is compared against it.

It is deliberately NOT a strawman. It has no correctness defect for the
learner to "fix": it is correct on every input, handles any relation
identifiers, any chain length, any fact count within capacity. The
learner's contribution is specialization (efficiency from experience) and
context-sensitive selection, never correctness repair. The full linear
scan (no early exit) is chosen so the cost model is exactly predictable:
nsteps * nfacts checks, which makes the efficiency prediction crisp and
lets the speedup be attributed purely to the learned index.

### 2.2 Experience (episodes)

During learning stages the learner has only vfy_gen. Each episode presents
one candidate chain. The learner's episode routine does two things:
(a) runs vfy_gen to do the actual verification work, and
(b) logs each step's relation identifier into its working set (deduped,
capacity 16), which is learner-owned state.
The working set is therefore derived from the learner's own task
experience, not supplied by the researcher.

### 2.3 Specialization (specialize; the revised procedure vfy_spec, id 1)

`specialize(L, A, ep0, ep1)`: L is the learner-state buffer, A the world
arena. It builds an inverted index over the arena facts restricted to the
working set: one linear pass over all facts; every fact whose relation is
in the working set is appended to that relation's bucket (capacity 64
fact indices per relation). It then writes the provenance record:
parent procedure id = 0 (derived from the generic procedure), episode
range [ep0, ep1] that informed it, number of facts indexed, and a revision
counter (incremented per specialization). The working set, the index
buckets, and the provenance record together ARE the revised procedure's
body, and they live entirely in learner-owned state.

`vfy_spec(L, A, C)`: for each chain step, looks up the step's relation in
the learned coverage set; if any step's relation is absent it returns -1
(not covered; a safety net that the selection logic makes unreachable in
the passing arms); otherwise it scans only that relation's bucket and
returns the 1/0 verdict.

What "specialization" means observably:
- S1: the index covers exactly the relations the learner encountered in
  its episodes (distractor relations present in the world but never used
  in any chain are excluded: selectivity is learned, not "index
  everything").
- S2: on covered queries the learner uses vfy_spec; verdicts agree 100%
  with vfy_gen; total fact-checks are strictly fewer (112 vs 448).
- S3: under a relation-identifier shift with no re-specialization, the
  learner selects vfy_gen (fallback); correctness is preserved.
- S4: after new episodes, the learner revises: the index content is
  replaced (revision counter increments, provenance records the new
  episode range), and the dumped learner state bytes differ from S1.
- S5/S6: selection tracks the revised coverage (new world covered, old
  world now falls back).

### 2.4 Selection (select_verify)

Data-driven, no mode constants: for the query chain, check each step's
relation against the learner-owned coverage set. If all are covered, run
vfy_spec (record sel=1, increment the specialized-use counter); otherwise
run vfy_gen (sel=0, increment the fallback counter). The "decision" is a
lookup in learner state. There is no VERIFY_MODE constant anywhere: the
researcher supplies the generic procedure as starting machinery, and
everything after that (what to index, when to use the index) is learner
state content.

### 2.5 Opaque identifiers

All entity and relation identifiers are opaque integers. World A uses
relations {101,102,103} plus distractors {107,109}; world B uses
{201,202} plus distractor {207}. No domain labels appear in the design,
code, or docs. The procedure under test is described as VERIFY (the
cognitive-operation label from the task brief); it is an experimental
description of the procedure being migrated, not a mode in the
architecture.

## 3. How we verify the learner (not the researcher) did it

This is the load-bearing check. Four independent evidences:

(a) Source audit: `col_learn.zag` (episode, ep_log_rel, cov_has, cov_find,
specialize, cov_clear, vfy_spec, select_verify) and `col_main.zag` contain
ZERO occurrences of any world relation-identifier literal
(101, 102, 103, 107, 109, 201, 202, 207), verified by word-boundary grep
in the REPORT. The identifiers appear only in `col_world.zag` (the world
definitions, which any experiment must define somewhere) and as runtime
values in output. The specialize/select code therefore cannot be
hardcoded to the worlds; it operates on whatever the working set holds.

(b) Content-difference demonstration: the identical specialize code run on
world A episodes produces coverage {101,102,103}; run on world B episodes
it produces {201,202}. The learner-state dumps (LSTATE lines) show
different relation bytes. If the researcher had hardcoded the content,
both dumps would be identical.

(c) Selectivity: distractor relations (107, 109 in A; 207 in B) exist in
the worlds but never appear in any chain; the dumps show they are absent
from the working set and have zero indexed facts. The learner indexed
what it experienced, not what exists.

(d) Behavioral fallback: in S3 the learner encounters relations outside
its coverage and selects vfy_gen without any researcher signal that world
B is "different". Selection is driven by the learned coverage record.

## 4. Build plan (implementation follows this prereg commit)

Files (all new, pure Zag):
- `col_base.zag`: z_alloc, get32/set32, output helpers (o_app, o_i64,
  o_nl, o_flush, single _zag_raw_syscall write; _zag_print never used for
  dynamic content), arena accessors, fact store, chain store, and vfy_gen
  (the researcher-supplied generic procedure). Output-helper idiom follows
  the frozen gsu_base.zag pattern.
- `col_world.zag`: setup_worldA (32 facts), setup_worldB (24 facts),
  chain builders mk2/mk3, and the 24 named chains (6 A episodes, 6 A
  queries, 4 B episodes, 4 pre-revision B queries, 4 post-revision B
  queries). World definitions only; no learner logic.
- `col_learn.zag`: episode, ep_log_rel, cov_has, cov_find, cov_clear,
  specialize, vfy_spec, select_verify. Learner-owned logic only.
- `col_main.zag`: the six stages, per-query/per-episode reporting,
  LSTATE dumps, summary lines, o_flush.
- `col_full.zag`: pure concatenation col_base + col_world + col_learn +
  col_main (verified by grep: exactly one `fn main(`).

Arena layouts (bytes):
- World arena (4096): 0: nf; 4: facts, 64 * 12 (s, r, o as LE i32).
- Chain (512): 0: nsteps; 4: steps, 16 * 12.
- Learner state L (8192): 0: nrel (working-set size); 4: rel_ids[16];
  68: rel_cnt[16]; 132: fidx[16][64] (fact indices per relation);
  4228: prov_parent; 4232: prov_ep0; 4236: prov_ep1; 4240: prov_facts;
  4244: prov_rev; 4248: stat_spec; 4252: stat_gen; 4256: stat_agree;
  4260: stat_neg1 (vfy_spec -1 returns; expected 0).

Build: pinned safebin znc (2026.07.0-dev), `znc col_full.zag -o col_bin`.
Run col_bin 3x; stdout to col_run1/2/3.txt, stderr to .err files.

Zag-defect workarounds honored (per AGENTS.md): no `as *i32` slice
construction (get32/set32 only); no _zag_print for dynamic content;
no `!(A && B)` in while conditions; if-nesting at most 3; allocation via
_zag_malloc as *u8; no []u8 as *u8 casts.

## 5. Stages and frozen predictions

World A: 32 facts. Relations 101/102/103 have 8 facts each
(subjects 11-18, objects 21-28, fixed opaque mapping); distractors 107
(4 facts, subjects 31-34, objects 41-44) and 109 (4 facts, subjects
35-38, objects 45-48). nfacts = 32.

S1 LEARN-A: 6 episodes (chains E0-E5, 2 steps each), episode indices
0-5. Chains:
 E0 (11,101,21),(11,102,25) v=1
 E1 (12,101,22),(12,103,27) v=1
 E2 (13,102,27),(13,103,26) v=1
 E3 (14,101,24),(14,102,28) v=1
 E4 (15,101,99),(15,102,21) v=0
 E5 (16,103,23),(99,101,21) v=0
Working set after S1: {101,102,103}. specialize(L, A, 0, 5): rev=1,
nrel=3, counts 8,8,8, prov = (parent 0, ep0 0, ep1 5, facts 32).
Predicted LSTATE: nrel=3 ids=101,102,103 cnts=8,8,8
prov=0,0,5,32,rev=1.

S2 SELECT-A: 6 fresh queries (all covered; expect sel=1 each):
 Q0 (17,101,27),(17,102,23) v=1 ns=2 gen=64 spec=16
 Q1 (18,103,21),(18,101,28) v=1 ns=2 gen=64 spec=16
 Q2 (11,102,25),(12,103,27),(13,101,23) v=1 ns=3 gen=96 spec=24
 Q3 (14,102,21),(15,103,24) v=0 ns=2 gen=64 spec=16
 Q4 (16,101,26),(16,102,22),(16,103,23) v=1 ns=3 gen=96 spec=24
 Q5 (17,103,21),(18,102,24) v=0 ns=2 gen=64 spec=16
Predicted SUMMARY-A: agree=6 spec_sel=6 cs=112 cg=448.
(Invalid steps: (14,102,21) and (17,103,21) match no fact.)

World B: 24 facts. Relations 201/202 have 8 facts each (subjects
51-58, objects 61-68, fixed opaque mapping); distractor 207 (8 facts,
subjects 71-78, objects 81-88). nfacts = 24.

S3 SHIFT-B (no re-specialization; coverage still {101,102,103}):
4 queries, expect sel=0 (fallback) each, verdicts via vfy_gen:
 B0 (55,201,65),(55,202,61) v=1 cg=48
 B1 (56,202,62),(56,201,66) v=1 cg=48
 B2 (57,201,67),(57,202,63) v=1 cg=48
 B3 (58,201,61),(58,202,64) v=0 cg=48
((58,201,61) matches no fact.) Predicted SUMMARY-SHIFT: fallback=4.

S4 REVISE-B: cov_clear; 4 episodes (indices 6-9):
 F0 (51,201,61),(51,202,65) v=1
 F1 (52,201,62),(52,202,66) v=1
 F2 (53,202,67),(53,201,63) v=1
 F3 (54,201,99),(54,202,68) v=0
specialize(L, B, 6, 9): rev=2, nrel=2, counts 8,8,
prov = (parent 0, ep0 6, ep1 9, facts 24).
Predicted LSTATE: nrel=2 ids=201,202 cnts=8,8 prov=0,6,9,24,rev=2.
The rel_ids bytes differ from the S1 dump (evidence 3b).

S5 SELECT-B: 4 fresh queries (covered under revised coverage;
expect sel=1 each):
 C0 (51,202,65),(52,201,62) v=1 ns=2 gen=48 spec=16
 C1 (53,201,63),(54,202,68),(55,201,65) v=1 ns=3 gen=72 spec=24
 C2 (56,201,66),(57,202,63) v=1 ns=2 gen=48 spec=16
 C3 (58,202,61),(51,201,61) v=0 ns=2 gen=48 spec=16
((58,202,61) matches no fact.) Predicted SUMMARY-B: agree=4
spec_sel=4 cs=80 cg=216.

S6 RECHECK-A: re-present Q0 under revised (B) coverage: expect sel=0
(fallback; A relations no longer covered), v=1, cg=64.
Predicted SUMMARY-ALL: stat_spec=10 stat_gen=5 agree=10 neg1=0.
(stat_spec: 6 in S2 + 4 in S5. stat_gen: 4 in S3 + 1 in S6.
Episodes run vfy_gen directly and are not counted in either stat.)

## 6. Kill bars

- K1 SPECIALIZATION CORRECTNESS: S2 agree=6/6 and S5 agree=4/4
  (vfy_spec verdict == vfy_gen verdict on every covered query).
- K2 EFFICIENCY: S2 cs=112 < cg=448 and S5 cs=80 < cg=216
  (strictly fewer fact-checks via the learned index).
- K3 LEARNER-NOT-RESEARCHER: (a) word-boundary grep for
  101|102|103|107|109|201|202|207 in col_learn.zag and col_main.zag
  returns empty; (b) the S4 LSTATE rel_ids bytes differ from the S1
  LSTATE bytes; (c) distractor relations are absent from both dumps.
- K4 FALLBACK: S3 fallback=4 (sel=0 on all 4), verdicts 1,1,1,0.
- K5 REVISION: S4 LSTATE shows rev=2, nrel=2, prov ep0=6 ep1=9
  facts=24; S5 agree=4/4 with sel=1 on all 4.
- K6 CONTEXT TRACKING: S6 sel=0 on the re-presented A query (selection
  follows the revised coverage, not the query's history).
- K7 DETERMINISM: 3/3 runs byte-identical stdout; stderr empty.
- K8 TOOLCHAIN: safebin active for every command; `which python3` and
  `which python` return nothing; zero forbidden-executable invocations;
  all computation pure Zag; shell only for znc/binary/git/assembly/
  byte-verification.
- K9 HYGIENE: zero em/en dash bytes in all lane docs (byte-verified).

## 7. Verdict mapping (frozen)

- K1-K6 PASS: MIGRATION DEMONSTRATED. The VERIFY procedure body moved
  from researcher-authored machinery to a learner-owned structure: the
  learner specialized it from experience (K1, K2), the specialization
  content is provably learner-derived (K3), selection between original
  and revised is context-driven from learned applicability with
  correctness-preserving fallback (K4, K6), and the structure was revised
  for new experience with provenance (K5).
- K1 FAIL (any covered-query verdict mismatch): SPECIALIZATION
  INCORRECT. The learned index does not preserve the generic
  procedure's semantics; diagnose whether the defect is in index
  construction or coverage lookup.
- K2 FAIL (no check reduction): SPECIALIZATION VACUOUS. The revised
  procedure carries no efficiency gain; the migration claim fails on
  utility.
- K3 FAIL: RESEARCHER CONTAMINATION. Relation content reached the
  learner by a non-experiential path; the lane is VOID for its
  learner-ownership claim.
- K4/K6 FAIL (wrong selection): SELECTION NOT CONTEXT-DRIVEN. The
  coverage record does not govern selection; diagnose.
- K7/K8/K9 FAIL: PROCESS-FAIL per standing governance.

## 8. What this establishes (and does not)

Establishes: whether a cognitive procedure can be specialized from
experience into a learner-owned structure with provenance, selected
context-sensitively against the original, with fallback preserving
correctness and revision adapting to new experience; and whether the
specialization content is provably learner-derived rather than
researcher-authored.

Does not establish: composition of cognitive procedures with each other;
retirement of the generic procedure; learner CREATION of a procedure
from scratch (the seed procedure is researcher-supplied by design);
behavior on non-chain structures; scaling beyond the tested sizes.

## 9. Deliverables

In this lane: PREREG.md (this file), NAMECHECK.md (Step 0 guard),
col_base.zag, col_world.zag, col_learn.zag, col_main.zag, col_full.zag
(assembled), col_bin, col_run1/2/3.txt (+ .err), REPORT.md.
