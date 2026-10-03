# REPORT.md -- Invention Hypothesis 2: Fragment Recombination

## Verdict: INVENTION-RECOMBINE-COMPLETE

TNN recombined sub-MAP fragments from different learned MAPs into a novel
6-link structure that no whole MAP could produce, that trial could not
produce, and that was never enumerated in source. The recombined form was
verified, promoted, persisted, and reused on a fresh subject. 3/3
deterministic. All ablations fail as predicted. The whole-MAP-only control
fails, proving fragment recombination is doing something Composition C
cannot.

Honest claim boundary: this is L2 structural recombination, not L3
representational invention. The fragmentation operation is
researcher-designed; the learner does not invent the concept of fragmenting.
What the learner determines (from its own history + goal constraints) is
the SPECIFIC recombination. It passes the SUF gate at the structural
decision level. It does not pass full L3.

## Experiment

X: 4-link r1 chain (11-15), query (11,61,15). Y: 4-link r2 chain (21-25),
query (21,62,25). Taught independently, never together. Z: 6-link mixed
chain on fresh relation 63, facts (31,1,32),(32,1,33),(33,1,34),(34,2,35),
(35,2,36),(36,2,37), query (31,63,37). Z requires [1,1,1,2,2,2], BEYOND
trial depth (k=4 max).

The discriminator: Z facts are shaped so NO whole MAP is satisfiable.
MAP_A=[1,1,1,1] fails at its 4th link (needs r1 from 34, but 34 has r2).
MAP_B=[2,2,2,2] fails at its 1st link (needs r2 from 31, but 31 has r1).
But proper sub-chain fragments (A,0,3)=[1,1,1] and (B,0,3)=[2,2,2] chain
to the solution. Composition C (whole MAPs only) must fail here.

## Results (3/3 byte-identical)

TREAT (frag_on=1):
- X ans=15, MAP 45 relseq=[1,1,1,1]. Y ans=25 via rebind, MAP 68
  relseq=[2,2,2,2] (LINK14 68->45 from persistent-connections rebind).
- Z: RECOMB-FRAGS n=2 (m=45,s=0,l=3) (m=68,s=0,l=3). Z ans=37.
- MAP_Z id=165, relseq=[1,1,1,2,2,2] (novel 6-link form, never seen).
  LINK14 165->45, 165->68. Fragment triples white-box packed in fields.
- Z' (fresh subject 41-47, same shape): RECOMB-FRAGS n=1 (m=165,s=0,l=6),
  Z2 ans=47. The composed Z MAP was reused as a single fragment.

ABL-X (MAP 45 deleted): RECOMB-FAIL, Z ans=-2. The [1,1,1] fragment is
causal; no alternative covers it.

ABL-Y (MAP 68 deleted): RECOMB-FAIL, Z ans=-2. The [2,2,2] fragment is
causal.

FRESH (no training): RECOMB-FAIL, Z ans=-2.

WHOLE-ONLY (frag_on=0, separate binary): X and Y train normally. Z:
RECOMB-FAIL, Z ans=-2, then trial fails (6 links > k=4), bootstrap fails.
The ONLY difference from TREAT is proper sub-chain fragments are
disallowed. This is the critical discriminator: whole-MAP chaining
cannot solve Z, fragment recombination can.

## SUF Analysis

Researcher-owned: the fragment extraction operation (all contiguous
sub-chains), the DFS chaining search, the verification step, the promotion
machinery. The source enumerates the SEARCH SPACE (every (m,start,len)
triple).

Learner-owned / source-underdetermined: WHICH MAPs exist (from the
learner's own training history), WHICH fragments satisfy the goal (from
the fact store + goal constraints), and therefore the SPECIFIC
recombination (45,0,3)+(68,0,3). The source does not name MAP 45 or MAP 68,
does not specify start=0 len=3, and does not precompute that [1,1,1]+[2,2,2]
is the solution. If the learner had learned different MAPs, the fragments
(and the solution) would differ. The final Z MAP's specific composition
cannot be completely enumerated from source alone; it is resolved by
learner history + goal.

SUF gate: PASS at the structural-decision level. The specific recombined
form was not enumerated.

L3 assessment: NOT L3. The operation of fragmenting a MAP into sub-chains
is researcher-designed generic machinery. The learner does not invent the
concept of a fragment, nor does it create a new representational primitive.
This is L2 structural learning: novel assembly of learner-owned pieces via
a researcher-provided operation. The honest claim is "learner creates a
novel structural form not enumerated in source via recombination," not
"learner invents fragmentation."

## Requirements Check (Micah Priority 8)

- Inadequate existing: YES. Whole-MAP chaining fails (RECOMB-FAIL in
  control). Trial fails (6 links exceeds k=4). Rebind fails (plen mismatch).
- New form: YES. MAP_Z relseq=[1,1,1,2,2,2], a 6-link mixed chain never
  present in training or source.
- Source-underdetermined: YES (bounded). Specific (m,s,l) triples resolved
  by learner history + goal, not source.
- Internally evaluated: YES. Assembled chain verified by t2_try_verify
  (v==expected) before promotion. Failed verifications are rejected.
- Useful: YES. Solves the novel Z goal (ans=37, correct).
- Persistent: YES. MAP_Z (id 165) remains in learner state; LINK14
  provenance intact through Z'.
- Reusable: YES. Z' solved via fragment (165,0,6), reusing the composed Z.
  Note: reuse occurred through the fragment mechanism, not rebind_try,
  because the frozen t2_gather depth limit (5 values) prevents rebind from
  matching the 7-value Z MAP. This is a base limitation, not a
  recombination failure. The fragments themselves (from MAP 45/68) are the
  reusable knowledge.
- Revisable: SUPPORTED but not directly tested. MAP_Z is a standard MAP
  node; it can be contradicted (contradict_map) or deleted like any MAP.
  A dedicated revision test is future work.
- Transferable: YES (bounded). Z' on a fresh subject (41-47) with fresh
  facts, same structural shape, solved via the composed form.

## Comparison to Composition C

Composition C chains WHOLE MAPs: each segment is one MAP's full relation
sequence. Fragment recombination chains SUB-MAP fragments: (map_id, start,
length) triples that were never promoted as standalone MAPs.

The discriminator is structural, not just terminological. On the Z goal:
- Composition C's candidate set is EMPTY (no whole MAP satisfiable).
- Fragment recombination's candidate set is NON-EMPTY (proper sub-chains
  satisfiable).
- The whole-MAP-only control binary (one-line diff: frag_on 1->0) fails.

This proves the two mechanisms have different expressive power on the same
goal. Fragment recombination strictly generalizes whole-MAP chaining
(when frag_on=1, whole MAPs are just (m,0,len) fragments, so C is a
special case).

## Architecture Accounting

- Cognition lines added: 369 (ir_patch.zag) + 283 (ir_driver.zag) = 652.
- New modes: 0. New bridges: 0. New handlers: 0. New semantic cases: 0.
- The mechanism uses only generic graph operations (walk, lookup,
  assemble, verify, promote) plus the frozen LINK14 provenance edge type.
- No COMPOSE_MODE or FRAGMENT_MODE. Recombination is not a mode; it is a
  search over learner-owned structures triggered by constraint
  satisfaction, hooked between rebind_try and trial in ev_query.

Compression note: ir_relseq duplicates cc_relseq logic (structural
extraction). A future integration should unify them. The fragment DFS
(ir_frag_dfs) duplicates cc_dfs structure at the fragment granularity;
if fragment recombination subsumes Composition C (it does, as a special
case), the whole-MAP path could be deleted, yielding net-negative lines.
This is flagged for the integration worker, not done here.

## Limitations and Next Steps

1. L2, not L3. Do not overclaim. The fragmentation operation is
   researcher-authored.
2. The search enumerates all fragments; "invention" is in the selection,
   not in generating the search space. A stronger test would require the
   learner to decide WHEN to fragment (currently always attempted).
3. Revisability not directly tested. Future: contradict the Z MAP, verify
   the learner revises or re-fragments.
4. 3-fragment and deeper recombinations not tested (DFS supports max 3;
   the Z goal needed 2). Future: goals requiring 3+ fragments from 3+
   MAPs.
5. Cross-domain fragments (different relation families) not tested.
   Future: fragments from unrelated domains recombined for a novel goal.
6. The (165,0,6) Z' reuse shows recursive composition works, but it also
   means the mechanism will happily use whole MAPs as fragments. This is
   correct (generalization), but a purist fragment-only test could exclude
   (m,0,len). Not needed for the current claim.

## Reproduction

- `ir_base.zag`: byte-identical copy of composition_C/cc_base.zag
  (SHA-256 dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6).
- `ir_patch.zag`: mechanism (frag_on=1). `ir_patch_nc.zag`: control
  (frag_on=0, one-line diff).
- `ir_full.zag` / `ir_full_nc.zag`: assembled. `ir_bin` / `ir_nc_bin`:
  pinned znc builds.
- `ir_run1/2/3.txt`: 3/3 byte-identical. `ir_nc_run1/2/3.txt`: 3/3
  byte-identical.
- Pure Zag. Safebin toolchain guard Step 0 recorded in NAMECHECK.md.
  Zero forbidden executables. Paper untouched. Nothing pushed.
