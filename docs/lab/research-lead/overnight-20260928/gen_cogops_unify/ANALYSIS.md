# ANALYSIS: GEN-COGOPS-UNIFY (C418)

Date: 2026-10-03. Worker: GEN-COGOPS-UNIFY.
Lane: `docs/lab/research-lead/overnight-20260928/gen_cogops_unify/`
Task: COMPRESSION-AUDIT candidate #2, one composer for domain and cognitive structures.

## Verdict: FEASIBLE (PoC demonstrates the unification)

A learner-owned cognitive procedure (ret_spec, vfy_spec from the frozen
cogops lanes) CAN be represented as a GEN-composable structure with
kind-contracts, and GEN CAN compose a cognitive procedure with a domain
structure. The proof-of-concept runs 6 arms, 3/3 byte-identical, all
frozen predictions match.

The audit's flagged risk (cognitive ops have interpreter-state
inputs/outputs, not values) does NOT materialize for the frozen
families: ret_spec/vfy_spec consume plain data ((rel,obj) pairs, chain
records) and produce plain data (subject lists, verdicts). These encode
as GEN pool values without loss.

## Q1: Can a cognitive procedure be a GEN-composable structure?

YES. The construction:

1. **Goal handles as values.** A cognitive goal (rel,obj pattern) is
   allocated as a record in the GU arena and named by a handle
   (1000000+slot, kind 3). The handle is a first-class GEN pool value.
   The body it names (ret_spec's coverage-indexed retrieve, vfy_spec's
   chain walk) is lifted byte-verbatim from the frozen cogops lanes.

2. **Kind-contracts via teach/observe.** GEN's MAP kind masks start at
   zero and grow from experience. The cognitive MAPs (m0: RET_SPEC,
   m1: RET_GEN, m2: VFY2) were taught with the same teach/observe
   calls as domain MAPs. Observed: m0's outmask grew {2} to {1,2} via
   provenance closure (its -1 decline has kind 1, its emitted subjects
   have kind 2). The contract is LEARNED, not researcher-supplied.

3. **Arity.** ret_spec/ret_gen are unary over goal handles (class 10/11
   in exec_map). vfy_spec is binary (goal handle + subject, class 12
   in exec_map2). GEN's garity needed a 1-token delta to admit class 12
   as arity 2 (GU-GEN-DELTA 1, diff-audited).

4. **Multi-emit.** Cognitive retrieve returns a SET of subjects, but
   GEN's exec_map returns one i32. The adapter uses a -3 sentinel return
   (never equals any exp, never enters the pool) and emits each subject
   via gen_addval with correct provenance. GEN's pool then holds the
   fan-out, and subsequent MAPs consume per-subject. This is how U3's
   fan-out works.

## Q2: Can GEN compose cognitive + domain structures?

YES, demonstrated in three forms:

**F1 (cognitive RETRIEVE + domain COUNT):** m1 (RET_GEN) emits subjects
331, 332 from goal 1000001; m3 (domain COUNT on rel 301) counts
per-subject; ANS=1 TRIES=3. The cognitive procedure's output became the
domain procedure's input through the shared value pool. No
researcher-written pipeline.

**F2 (cognitive RETRIEVE + cognitive VERIFY, negative):** m1 emits
subjects; m2 (VFY2) checks each against the goal; all fail; ANS=0
TRIES=4. Composition correctly yields the negative answer.

**U3 (fan-out/fan-in):** m0/m1 (cognitive) multi-emit subjects; m3
(domain COUNT) maps per-subject to 1, 1; m2 (cognitive VERIFY) filters;
m4 (domain ADD2) fan-in to 1+1=2; ANS=2 TRIES=7. Debug trace confirms
the exact trial sequence: R1 (m0:-3, m1:-3), R2 (m3:1,1; m2:0,0),
R3 (m4(3,3):2 FOUND). Cognitive and domain MAPs interleave in GEN's
trial order with no type distinction.

**U10 (spec decline, generic fallback):** m0 (RET_SPEC) declines (-1)
on the uncovered rel 307; m1 (RET_GEN) emits subjects; m5 (domain
COUNT on rel 307) counts 331:1, 332:2; 2=exp FOUND. ANS=2 TRIES=6.
The specialized cognitive procedure's decline did not block the generic
path. Trial order [spec, gen] gives emergent coverage fallback.

## Concept mapping (cogops -> GEN)

| Cogops concept | GEN realization |
|----------------|-----------------|
| need-to-procedure binding | MAP admission via kind masks (inmask/outmask) |
| plan (ordered steps) | dataflow through the value pool; order emerges from trial sequence, not a stored plan |
| version selection (spec vs gen) | trial order [m0 spec, m1 gen]; first admissible MAP runs |
| decline (no coverage) | -1 return; GEN tries the next MAP |
| coverage table | kind masks grown by teach/observe |
| provenance | gen_addval records (m,i1,i2) per pool value |

## Honest negatives and limitations

1. **Scalar projection, not answer records.** GEN's pool holds i32
   values, not the rich answer records cogops produces (with
   provenance chains, confidence). The PoC projects to scalars. A full
   unification needs value-level provenance or structured pool values.

2. **No plan reuse.** Cogops persists per-goal plans and re-derives
   them byte-identically after a wipe (K5). GEN re-discovers the trial
   sequence every query. The PoC does not address plan persistence.

3. **Order dissociation dissolves.** Cogops demonstrated opposite
   execution orders ([RET,VFY] vs [VFY,RET]) from the same bindings.
   In GEN, order is trial order, not a stored plan. The PoC does not
   reproduce order dissociation.

4. **Pivot links need a decision.** Cogops-3way's pivot (relation
   derived from a chain) has no GEN analog in the PoC. The prereg
   includes a pivot arm as a kill bar.

5. **Kind sensors are scaffold.** pkind classifies by value range
   (researcher-written). The audit requires learned kinds. The PoC
   uses the frozen pkind; the prereg requires a learned-kind arm.

6. **Body invention stays distinct.** The PoC lifts frozen bodies
   byte-verbatim. GEN does not invent cognitive procedure bodies.
   Unification covers COMPOSITION only, per the audit's scope.

7. **COUNT aggregation is a sketch.** m4 (ADD2) fan-in is binary
   addition, not general aggregation. N-ary fan-in needs a design
   decision.

8. **Search-based scaling caveat.** GEN's trial is search over the
   pool. The PoC has 6 MAPs and small pools. Scaling to 100s of MAPs
   needs the indexing work from the scaling lanes.

9. **GEN limitation found: tried tables hardcoded for 4 MAPs.** The
   frozen GEN's tried1 table is laid out for exactly 4 MAPs
   (2304..3328). Registering a 5th or 6th MAP silently aliases tried1
   entries onto tried2's count, the pool count (nv), and the widened
   flag. Found by audit 2026-10-03 while hand-tracing an anomalous
   U10 trace. The PoC relocates tried1/tried2 for 6 MAPs
   (GU-GEN-DELTA 2, diff-audited). This is a real GEN defect worth
   reporting: any experiment with >4 MAPs on the frozen GEN base is
   suspect.

10. **znc foreground cache.** During this work, znc served a stale
    binary after a source change (the .zag-cache foreground cache).
    Resolved with --no-foreground-cache and cache removal. Not a
    science issue, but a toolchain quirk to note.

## PoC design (for the record)

- `gu_base.zag`: frozen base (gen_generality/ref_gg_base.zag) + 5
  documented GU-DELTA items (arena 32768, MAP table 8x4096, m2 table
  8x4416, pkind kind-3 for handles, exec_map classes 10/11, exec_map2
  class 12).
- `gu_learn.zag`: learner bodies lifted byte-verbatim from cogops
  lanes (build script diff-verifies).
- `gu_glue.zag`: goal records in arena GBUF (8032, 8x256), handle =
  1000000+slot; class 10/11 (unary, multi-emit via -3 sentinel),
  class 12 (binary VFY2); heap-slice pointers as i64 in arena cells.
- `gu_gen.zag`: gsf_gen.zag + GU-GEN-DELTA 1 (garity class 12) +
  GU-GEN-DELTA 2 (tried relocation for 6 MAPs).
- `gu_main.zag`: 6 arms (F1,F2,F3,F4,U3,U10).
- `gu_build.sh`: fail-closed build/audit/runner with prediction checks.

## Frozen PoC results (poc_run1.txt, 3/3 byte-identical)

- F1: ANS=1 TRIES=3 (cog RET + domain COUNT)
- F2: ANS=0 TRIES=4 (cog RET + cog VFY, negative)
- F3: ANS=-2 TRIES=1216 (decline, adversarial seed)
- F4: ANS=-2 TRIES=189, WIDEN=1 (empty-pattern decline, no fabrication)
- U3: ANS=2 TRIES=7 (fan-out/fan-in)
- U10: ANS=2 TRIES=6 (spec decline, generic fallback)

## Recommendation

Proceed to a full preregistered test (PREREG_DESIGN.md). The PoC
establishes feasibility; the prereg must address the honest negatives,
especially learned kinds, plan persistence, order dissociation, pivot
links, and scaling.
