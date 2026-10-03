# PREREG: L2 SUBSTITUTE Operator (Chain Family)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l2_substitute/` only.
Worker: L2 Substitute Worker (subagent, 2026-10-02).
Parent mandate: L2 ADAPTIVE REUSE is the top priority. EXTEND
(composition_adapt, EXTEND-ONE) and TRUNCATE (l2_l3_trunc) are
demonstrated. SUBSTITUTE is the missing operator: the learner must
take a partly-useful old MAP whose middle segment died and replace
just that segment with an independently learned alternative piece,
without rebuilding from scratch.

## 1. What is being tested

Whether a learner, holding a learned chain MAP m whose MIDDLE
segment's licensing fact dies in a world change (teach-then-kill),
detects the stale segment, searches its own learned piece inventory
in node-id order for a live alternative piece n covering the same
endpoints via different relations and facts, substitutes n for the
dead segment (m2 = prefix ++ n ++ suffix), verifies m2 by real
execution to its terminal, promotes m2 with adapted-from provenance,
retires the stale m, and answers queries through m2. The
substitution choice comes from learner state, never from a
researcher-selected piece per problem. One generic operator, no
relation named, no MAP named, no length named: not a finite operator
menu.

Concrete scenario (all ids frozen):
- Facts (fact id: (sub, rel, obj)), taught in phase 0, all live:
  0:(1,1,2) 1:(2,1,3) 2:(3,1,4) 3:(2,2,5) 4:(5,2,3)
  5:(1,61,11) 6:(11,62,12) 7:(2,63,13) 8:(5,64,14)
- MAP m (id 0): relseq [1,1,1], facts [0,1,2], chain 1->2->3->4.
- MAP n (id 1): relseq [2,2], facts [3,4], chain 2->5->3.
  Same endpoints as m's middle segment (2->3), different relations
  (2 vs 1) and disjoint facts ([3,4] vs [0,1,2]). Taught and
  execution-verified BEFORE the world change, independently of m.
- MAP d (id 2): relseq [61], facts [5], chain 1->11. Distractor
  piece: the candidate search must examine and reject it.
- World change: fact 1 (the middle hop license (2,1,3)) is killed.
  Driver/environment side only; the learner never calls the kill.
- Query (1,4): m's execution goes stale at hop 1. The SUBSTITUTE
  bracket replaces the dead 2->3 segment with n, building
  m2 (id 3): relseq [1,2,2,1], facts [0,3,4,2], chain
  1->2->5->3->4.

## 2. Frozen learner machinery (disclosed)

Standalone pure-Zag learner (learner.zag) plus environment side
(world.zag: fact table + kill) and experiment side (driver.zag:
teaching, arms, kill-bar evaluation). The frozen TNN core is not
used; this is a standalone learner-mechanism experiment in the chain
family. Unfrozen only; no frozen source touched.

State: one u8 buffer. Offsets: 0 NF, 1 NM, 2 NE, 3 SUB_ON, 4 ET_ON
(driver-set causal-control flags, composition_l2 adapt_on
precedent, never written by the learner), 5 NN (answer nodes),
6 STALE_MAP (255=none), 7 STALE_HOP, 8 STALE_FACT, 9 LAST_VIA
(255=none), 10 LAST_VAL, 11 IN_ADAPT. Facts: 32 x 8 bytes at
16..271 [sub,rel,obj,live,0,0,0,0]. MAPs: 16 x 32 bytes at
272..783 [tag=20,live,start,end,rlen,flen,reason,pad, rels x8 @+8,
facts x8 @+16, pad x8 @+24]. Edges: 64 x 4 bytes at 784..1039
[from,to,type,pad]. Answer nodes: 8 x 4 bytes at 1040..1071.
Stats: SEARCH i32 @1072, EXEC i32 @1076, A_SEARCH i32 @1080,
A_EXEC i32 @1084. Scratch at 1088+.

Edge-type semantics (reused, zero new types):
- type 16: adapted-from. Written at promotion: m2->m and m2->n
  (the composition_adapt convention).
- type 14 (LINK14): promotion/answer provenance. Written when a
  query is answered: answer node A -> delivering MAP (the
  composition_adapt MAP_Z convention).
- type 15: co-use. Written on episode success by the learner's
  deliver routine: when the delivering MAP is adapted from 2+
  distinct sources, type-15 LINKs are written between each ordered
  pair of distinct sources (mechanism B convention: co-use edges
  written by episode success).
- No other edge types may appear (F-EDGE-NEW voids the build).

Generic operations (frozen, relation-agnostic, MAP-agnostic):
- f_teach(sub,rel,obj): observe a world fact (learner side).
- m_teach(relse q, facts, start, end): learn a native MAP (facts
  must be live and rel-matching at teach time).
- m_exec(mid, start): execute a MAP's hop sequence. Each hop reads
  its licensing fact: dead fact -> STALE recorded
  (STALE_MAP=mid, STALE_HOP=k, STALE_FACT=fid), return -1. This is
  the white-box stale check that fires. Sub/obj/rel mismatch ->
  clean fail (STALE_MAP=255).
- chain_exec(facts, rels, n, start): same over raw arrays (for
  candidates and rebuild verification).
- pipeline: try each live MAP in node-id order from the query
  start; first terminal == target delivers the answer.
- ev_query(start, target): pipeline; on failure enter the adapt
  phase (A_SEARCH/A_EXEC reset, IN_ADAPT=1). If SUB_ON: the
  SUBSTITUTE bracket; if it answers, return. If ET_ON: the
  extend/truncate bracket, then one pipeline re-run. Else -2.
- sub_bracket: stale-detect pass (first live MAP in node-id order
  whose exec goes stale), then sub_try on it; if no candidate,
  rebuild_fallback.
- sub_try(sm): split sm at the stale hop into prefix facts/rels
  and suffix facts/rels; dead segment endpoints
  (seg_start, seg_end) = (node at stale hop, stale fact's obj).
  Piece search over live MAPs in node-id order, skipping sm:
  candidate iff start==seg_start and end==seg_end and every
  licensing fact live. First match wins (node-id order, no
  researcher selection). Dedup: skip if a live MAP already carries
  exactly the candidate relseq+facts (search continues). Verify by
  chain_exec to the target; a graph that does not execute to its
  terminal is never promoted. Promote m2, write type-16 m2->sm and
  m2->candidate, retire sm (live=0, reason=1 SUBSTITUTED; edges
  persist). Deliver the answer by executing m2.
- rebuild_fallback (generic, disclosed): iterative-deepening
  enumeration over live facts, L=1..4. At each L, extend every
  length-(L-1) candidate by scanning all fact ids ascending for
  live facts with sub == end node, then chain_exec-verify each
  length-L candidate in order. First terminal == target promotes a
  NATIVE MAP (no type-16) and delivers. This is the honest
  "rebuild from scratch" baseline: no learned structure guides the
  search.
- et_bracket (the no-substitute control operators, generic):
  TRUNCATE-ONE sub-pass: first stale MAP with stale_hop >= 1 is
  truncated to its live prefix, verified, promoted with type-16,
  source retired (reason=2). EXTEND-ONE sub-pass: each live MAP
  (node-id order, as of sub-pass entry) that fully executes from
  the query start to a terminal != target is extended by the first
  live fact (id order) at its frontier, verified, promoted with
  type-16. Then one pipeline re-run. Each operator fires at most
  once per query (the composition_adapt firing precedent).

## 3. Frozen cost-counting rules

- A_SEARCH += 1 per MAP header examined in a linear scan
  (ascan_map) and per fact examined in a linear scan or liveness
  check (ascan_fact).
- A_EXEC += 1 per m_exec / chain_exec call while IN_ADAPT==1.
- A_SEARCH/A_EXEC reset to 0 at adapt-phase entry; IN_ADAPT=0
  outside the adapt phase. Global SEARCH/EXEC count always
  (informational only).

## 4. Frozen arms and hand-derived expectations

Phase 0 (all arms except FRESH): teach facts 0..8; m_teach m(0),
n(1), d(2); M-OK: ev_query(1,4) -> 4 via MAP0; N-OK:
ev_query(2,3) -> 3 via MAP1 (pipeline tries MAP0 first: clean
fail, then MAP1); INTERSECT(m.facts, n.facts) = 0 printed.

- ARM-FULL (SUB_ON=1, ET_ON=0): KILL fact 1. Query (1,4).
  Pipeline: MAP0 exec stale at hop 1 (fact 1 dead); MAP1 clean
  fail; MAP2 full exec to 11 != 4. Adapt phase: stale-detect
  ascan MAP0 (S=1), exec (E=1), sm=0. SUB-STALE m=0 hop=1 fact=1.
  seg 2->3, prefix [1]/[0], suffix [1]/[2]. Piece search:
  MAP0 self skip (S=2); MAP1 header (S=3), facts 3,4 live
  (S=4,5): MATCH; MAP2 header (S=6) start 1 != 2 skip. Dedup
  scan MAP0/1/2 (S=7,8,9): no rlen-4 MAP. SUB-BUILD
  rels=1,2,2,1 facts=0,3,4,2. chain_exec verify -> 4 (E=2).
  Promote MAP3 (m2): relseq [1,2,2,1], facts [0,3,4,2],
  start 1, end 4. type-16 3->0, 3->1. Retire MAP0 (reason 1).
  Deliver: exec MAP3 -> 4 (E=3). ANS via=3 val=4. Answer node
  34: LINK14 34->3. type-15 0->1, 1->0.
  Frozen: ans=4 via=3; A_SEARCH=9, A_EXEC=3; t16=2 {3->0,3->1};
  t15=2 {0->1,1->0}; LINK14 34->3 exists; no other edge types;
  MAP3 relseq [1,2,2,1] start 1 end 4 live 1.
  Post-query (1,4): pipeline skips retired MAP0, MAP1/MAP2 fail,
  MAP3 -> 4. Frozen: ans=4 via=3, MAP0 live=0.
- ARM-NO-SUB (SUB_ON=0, ET_ON=1): phase 0, KILL fact 1.
  Query (1,4). Pipeline fails as in FULL. et_bracket:
  TRUNCATE sub-pass: MAP0 stale@hop1 -> t1=MAP3 facts [0]
  rels [1] 1->2, verified, type-16 3->0, MAP0 retired (reason 2).
  EXTEND sub-pass over MAP1, MAP2, MAP3: MAP1 clean fail, skip;
  MAP2 full exec -> 11, frontier fact 6 -> e_d=MAP4 rels [61,62]
  facts [5,6] 1->12, type-16 4->2; MAP3 full exec -> 2, frontier
  fact 3 (fact 1 dead, fact 3 first live in id order) -> e1=MAP5
  rels [1,2] facts [0,3] 1->5, type-16 5->3. Re-run: MAP1 fail,
  MAP2 ->11, MAP3 ->2, MAP4 ->12, MAP5 ->5: none == 4.
  Frozen: ans=-2; t16=3. Extend/truncate genuinely fired and
  still failed.
- ARM-ABLATE-N (SUB_ON=1): phase 0, retire MAP1 (reason 3,
  N-RETIRED), KILL fact 1. Query (1,4). Stale-detect: MAP0
  (S=1, E=1). Piece search: MAP0 self (S=2); MAP1 retired skip
  (S=3); MAP2 header skip (S=4). No candidate. rebuild_fallback:
  L=1: 1 scan x9 (S=13), candidates [0],[5], 2 verifies (E=3);
  L=2: 2 scans x9 (S=31), [0,3],[0,7],[5,6], 3 verifies (E=6);
  L=3: 3 scans x9 (S=58), [0,3,4],[0,3,8], 2 verifies (E=8);
  L=4: 2 scans x9 (S=76), [0,3,4,2], verify -> 4 (E=9).
  Promote NATIVE MAP3 (no type-16): relseq [1,2,2,1] from facts.
  Deliver exec (E=10). ANS via=3 val=4. Answer node 32:
  LINK14 32->3. No type-15 (single native source).
  Frozen: ans=4 via=3; A_SEARCH=76, A_EXEC=10; t16=0.
- ARM-ABLATE-M (SUB_ON=1): phase 0, KILL fact 1, KILL fact 0
  (ablates m's surviving prefix). Query (1,4). Stale-detect:
  MAP0 stale@hop0 (S=1, E=1). Piece search for seg (1,2):
  MAP0 self (S=2); MAP1 start 2 != 1 (S=3); MAP2 end 11 != 2
  (S=4). No candidate. rebuild: L=1: scan x9 (S=13), [5],
  verify -> 11 (E=2); L=2: scan x9 (S=22), [5,6], verify -> 12
  (E=3); L=3: scan x9 (S=31), none. Fail.
  Frozen: ans=-2; t16=0; NM=3 (no MAP created).
- ARM-FRESH (SUB_ON=1): teach facts 0..8, KILL fact 1, no MAPs.
  Query (1,4). No stale MAP. rebuild_fallback: S=72, 8 verifies
  (E=8); promote NATIVE MAP0 (id 0, no MAPs existed); deliver
  exec (E=9). ANS via=0 val=4. LINK14 32->0.
  Frozen: ans=4 via=0; A_SEARCH=72, A_EXEC=9; t16=0.

## 5. Kill bars (frozen)

- K1 (n independent and prior): INTERSECT(m.facts,n.facts)==0
  printed, and the N-OK line precedes the KILL line in output
  (shell line-number check).
- K2a (ablate n): ABLATE-N t16==0 AND ans==4 AND
  A_SEARCH(ABLATE-N)=76 >= 5*A_SEARCH(FULL)=45. The adapted m2
  cannot exist without n; the learner rebuilds from scratch at
  8.4x the substitution search cost.
- K2b (ablate m prefix): ABLATE-M ans==-2 AND t16==0 AND NM==3.
- K3 (fresh learner): FRESH t16==0 AND ans==4 AND
  A_SEARCH(FRESH)=72 >= 5*A_SEARCH(FULL)=45 (8x).
- K4 (white-box trace): run1 output contains, verbatim:
  `SUB-STALE m=0 hop=1 fact=1`,
  `SUB-CAND id=1 s=2 e=3 flive=2 MATCH`,
  `SUB-BUILD rels=1,2,2,1 facts=0,3,4,2`,
  `SUB-VERIFY term=4`, `SUB-PROMOTE m2=3`, `ANS via=3 val=4`
  (shell grep -F, all six).
- K5 (no-substitute control fails): NO-SUB ans==-2 AND t16==3
  (extend/truncate fired and still failed).
- K6 (stale retired, not reused): FULL MAP0 live==0 AND
  post-query ans==4 via MAP3.
- K7 (provenance, zero new types): FULL t16==2 with edges
  exactly {3->0, 3->1}; t15==2 with edges exactly {0->1, 1->0};
  some LINK14 edge with to==3; zero edges with type outside
  {14,15,16}.
- K8 (determinism): 3/3 runs byte-identical (sha256 equal).
- K9 (audit): 8 frozen grep patterns return 0 hits on
  learner.zag (section 6).
- K10 (FULL success): FULL ans==4 via MAP3 with MAP3 relseq
  [1,2,2,1], start 1, end 4, live 1.

Verdict L2-SUBSTITUTE-COMPLETE iff K1-K10 all PASS and no
falsifier fires.

## 6. Frozen K9 grep audit spec (run on learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `1,2,2,1` (m2's relseq must not be in the learner)
2. `0,3,4,2` (m2's fact list must not be in the learner)
3. `(2,2,5)` (n's fact literal; world data stays out)
4. `(2,1,3)` (killed fact literal; world data stays out)
5. `_MODE` (zero modes)
6. `bridge` (case-insensitive; no bridge handlers)
7. `python` (case-insensitive; pure Zag)
8. `as *i32` (the pinned-znc miscompile pattern; u8 cells only)

## 7. Frozen falsifiers

- F-NO-CAND: FULL sub_bracket finds no candidate.
- F-WRONG-M2: promoted m2 relseq != [1,2,2,1] or (start,end)
  != (1,4).
- F-STALE-REUSE: any FULL ANS via=0 after MAP0 retirement.
- F-CTRL-PASS: NO-SUB ans != -2.
- F-ABLN-ADAPT: ABLATE-N t16 != 0.
- F-ABLM-PASS: ABLATE-M ans != -2.
- F-FRESH-ADAPT: FRESH t16 != 0.
- F-EDGE-NEW: any edge with type outside {14,15,16}.
- F-AUDIT / F-NONDET / F-PYTHON: as in prior waves; any fires
  voids the build.

## 8. Determinism spec

No RNG. Node-id order everywhere; first-match candidate rule;
ascending fact-id scans; iterative deepening L=1..4. Output via
one preallocated buffer and a single raw-syscall write loop.
3/3 byte-identical required.

## 9. Disclosed residual footprint and non-claims

- The SUBSTITUTE operator, the stale-check exec semantics, the
  rebuild fallback, the extend/truncate control operators, the
  edge-type conventions, and the cost counters are
  researcher-supplied generic machinery, frozen here. The L2
  claim is narrow: the dead middle segment is replaced by a
  learner-selected live piece from learner state (node-id order
  endpoint match), verified by execution, with adapted-from
  provenance, and the no-substitute control provably fails.
- SUB_ON/ET_ON are driver-set causal-control flags (the
  composition_l2 adapt_on precedent), never written by the
  learner. They enable the lesion comparison; they are not
  runtime modes.
- One world family (chain routing with a middle-fact kill). No
  generality claim beyond the five arms. The hidden kill was
  builder-designed, not adversary-designed.
- 0 modes, 0 bridges, 0 handlers, 0 new edge types, 0 new
  opcodes, 0 new semantic cases. Pure Zag.
- No em/en dashes in loop documentation. Paper untouched.
  Nothing pushed. Commits local on tnn-native-lab.
- Unfrozen only: no frozen source touched. The frozen TNN core
  is not used here; this is a standalone learner-mechanism
  experiment.
