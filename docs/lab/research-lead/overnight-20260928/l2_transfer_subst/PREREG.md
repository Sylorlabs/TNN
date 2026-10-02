# PREREG: L2-TRANSFER-SUBST (SUBSTITUTE in the Arithmetic Substrate)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l2_transfer_subst/` only.
Worker: L2 Transfer-Subst Worker (subagent, 2026-10-02).
Parent mandate: MECHANISM GENERALITY. C298 demonstrated the
SUBSTITUTE operator in the chain family (ledger C298,
`l2_substitute/`, prereg 1fb6db863, impl eb89ac84e). The open
question is whether the same operator logic transfers to a
different substrate without per-domain retuning, or is a
chain-family trick. This experiment runs SUBSTITUTE in the
ARITHMETIC substrate: a SUM MAP over price facts, one price fact
killed teach-then-kill (learner not told), substitution by an
independently learned alternative summand piece, verification by
real execution to the correct total.

## 1. What is being tested

Whether the C298 SUBSTITUTE operator, with its trigger logic
unchanged (stale licensing detection, endpoint-matching piece
search in node-id order, execution verification to the terminal,
type-16 adapted-from promotion, stale retirement), fires and
succeeds on a price-summation structure it was never tuned for.
The bar is explicit: NO per-domain threshold, relation name, or
tuning constant is changed between the chain and arithmetic
instantiations. The only differences are the facts and the MAP
inventory (world.zag and driver.zag). If any operator constant
must change, that is itself a finding and is reported as a
generality failure of that component (falsifier F-RETUNE).

The claim is framed honestly as MECHANISM GENERALITY
(researcher-implemented, learner-triggered operator across
substrates), not learner invention and not an L3 claim.

## 2. Arithmetic world design (substrate-specific; frozen)

Node ids are subtotal states in dollars. A fact (s, r, e)
asserts a licensed summand step from subtotal s to subtotal e;
the price of the step is e minus s, fixed by the world table
below (hand-derived, never computed by the learner). Relations:
7 = ADD (summand step), 8 = ITEMIZED-ADD (alternative
decomposition step), 9 = unrelated relation (distractor).

Fact table (all live in phase 0):
- 0: (0, 7, 15)    item A, price 15: subtotal 0 -> 15
- 1: (15, 7, 70)   item B (meal deal), price 55: 15 -> 70
- 2: (70, 7, 90)   item D, price 20: 70 -> 90
- 3: (15, 8, 40)   itemized B1, price 25: 15 -> 40
- 4: (40, 8, 70)   itemized B2, price 30: 40 -> 70
- 5: (0, 9, 200)   distractor piece fact
- 6: (200, 9, 210) distractor continuation
- 7: (100, 7, 115) other-register summand, price 15
- 8: (115, 7, 140) other-register summand, price 25

Hand-derived correct total: 15 + 55 + 20 = 90. Bundle path:
15 + 25 + 30 + 20 = 90. Both paths agree on 90.

MAP inventory (taught in phase 0, execution-verified):
- MAP m (id 0): relseq [7,7,7], facts [0,1,2], start 0, end 90.
  The SUM MAP: total = pA + pB + pD via the learned addition
  structure.
- MAP n (id 1): relseq [8,8], facts [3,4], start 15, end 70.
  Independently learned alternative piece: the itemized
  decomposition of the B segment. Same endpoints as m's middle
  hop (15 -> 70), different relations (8 vs 7), disjoint facts
  ([3,4] vs [0,1,2]). Taught and execution-verified BEFORE the
  world change, independently of m.
- MAP d (id 2): relseq [9], facts [5], start 0, end 200.
  Distractor piece: the candidate search must examine and reject
  it (endpoint mismatch).

World change: fact 1 (the $55 meal-deal price fact (15,7,70))
is killed. Driver/environment side only; the learner never calls
the kill and is not told. Query (0,90): "what is the total?"
m's execution goes stale at hop 1. The SUBSTITUTE bracket
replaces the dead 15 -> 70 hop with n, building m2 (id 3):
relse q [7,8,8,7], facts [0,3,4,2], start 0, end 90, verified by
chain_exec to terminal 90.

On "real execution to the correct total": in this substrate the
sum IS the terminal subtotal state; verification is the
learner's chain_exec traversing every licensed hop of the
assembled MAP (each hop checks fact liveness, sub/rel match) to
terminal 90, the hand-derived correct total. The arithmetic
(price = obj minus sub) lives in the world's state encoding,
which is the substrate-specific part; the operator is
state-encoding agnostic.

## 3. Shared vs substrate-specific decomposition (frozen)

SHARED (substrate-neutral). File `learner.zag` will be a
byte-identical copy of `l2_substitute/learner.zag`, whose sha256
is pinned here:
fdf33e3869969ffb38dc5334ddb184cad8283afcf23164f56040db554c2d69c1
Shared machinery, unchanged:
- State layout: facts 32 x 8B [sub,rel,obj,live,0,0,0,0] at
  16..271; MAPs 16 x 32B [tag=20,live,start,end,rlen,flen,
  reason,pad, rels x8 @+8, facts x8 @+16, pad x8 @+24] at
  272..783; edges 64 x 4B [from,to,type,pad] at 784..1039;
  answer nodes 8 x 4B at 1040..1071; SEARCH/EXEC/A_SEARCH/
  A_EXEC i32 at 1072/1076/1080/1084; offsets 0 NF, 1 NM, 2 NE,
  3 SUB_ON, 4 ET_ON (driver-set flags, never learner-written),
  5 NN, 6 STALE_MAP (255 = none), 7 STALE_HOP, 8 STALE_FACT,
  9 LAST_VIA (255 = none), 10 LAST_VAL, 11 IN_ADAPT.
- f_teach, m_teach (admit iff facts live and rel-matching;
  rl,fl <= 8), map_create, map_retire.
- m_exec: the white-box stale check (dead licensing fact
  records STALE_MAP/HOP/FACT, returns -1; sub/rel mismatch is a
  clean fail).
- chain_exec, pipeline (live MAPs in node-id order), ev_query
  (adapt phase on pipeline failure; A_SEARCH/A_EXEC reset;
  IN_ADAPT=1; SUB_ON selects the SUBSTITUTE bracket, ET_ON the
  extend/truncate bracket).
- sub_bracket: stale-detect pass (first live MAP in node-id
  order whose exec goes stale), then sub_try, else
  rebuild_fallback.
- sub_try: SUB-STALE trace; split at the stale hop into prefix
  and suffix; dead-segment endpoints (seg_s, seg_e) = (obj of
  last prefix fact, or query start if k=0; obj of stale fact);
  piece search over live MAPs in node-id order skipping sm:
  candidate iff start == seg_s and end == seg_e and every
  licensing fact live; first match wins; dedup by exact
  relseq+facts over live MAPs; verify by chain_exec to the
  target; promote m2; type-16 m2 -> sm and m2 -> candidate;
  retire sm (reason 1 SUBSTITUTED; edges persist); deliver by
  executing m2.
- rebuild_fallback: iterative deepening L = 1..4 over live
  facts, ascending fact-id scans, chain_exec verify each
  candidate in order, first terminal == target promotes a NATIVE
  MAP (no type-16) and delivers.
- et_bracket: TRUNCATE-ONE (first stale MAP with stale_hop >= 1
  truncated to live prefix, verified, type-16, source retired
  reason 2) then EXTEND-ONE over live MAPs at sub-pass entry
  (full exec to terminal != target, extended by first live fact
  in id order at the frontier, verified, type-16), each fires at
  most once per query, then one pipeline re-run.
- deliver: answer node aid = 32 + nn; LINK14 aid -> delivering
  MAP; type-15 co-use over ordered pairs of distinct type-16
  sources when 2 or more; ANS trace.
- Edge-type semantics: 16 adapted-from, 14 answer provenance,
  15 co-use; no other type may appear.
- Cost rules: ascan_map/ascan_fact +1 to A_SEARCH (and SEARCH);
  bump_exec +1 to EXEC and, while IN_ADAPT, A_EXEC.
- Evaluation threshold: 5x cost ratio (K-2a, K-3), identical to
  C298.
- Output: one 65536-byte buffer, single raw-syscall write loop;
  no RNG; determinism by node-id order, first-match, ascending
  scans.

SUBSTRATE-SPECIFIC (world.zag and driver.zag ONLY):
- The fact table (section 2) vs C298's route facts.
- Relation ids 7/8/9 and their gloss (ADD, ITEMIZED-ADD,
  unrelated) vs 1/2/61..64. The operator never names a relation.
- The MAP inventory (SUM MAP, bundle piece, distractor) vs
  route MAPs. The operator never names a MAP.
- The kill target (fact 1, the $55 price fact) vs (2,1,3).
- The query (0,90) vs (1,4); the hand-derived expectations in
  sections 5 and 6.
- Nothing else. In particular: no new edge/MAP types, opcodes,
  modes, bridges, handlers, or semantic cases.

## 4. Frozen shared-constant list (the no-retuning bar)

Every constant below is identical between the chain and
arithmetic instantiations (entailed by the byte-identity of
learner.zag, checked by K-11):
fact cap 32 / stride 8; MAP cap 16 / stride 32; edge cap 64 /
stride 4; answer-node cap 8; STALE sentinel 255; retire reasons
1, 2, 3; rebuild Lmax 4; type ids 14, 15, 16; MAP tag 20;
answer-node id base 32; cost-counting rules of section 3;
node-id order; first-match-wins; ascending fact-id scans;
5x ratio threshold; SUB_ON/ET_ON driver-flag convention.
No per-domain threshold, relation name, or tuning constant is
changed. If an implementation edit to learner.zag proves
necessary, that edit and the component it touches are reported
as a generality failure (F-RETUNE fires, verdict cannot be
L2-TRANSFER-SUBST-COMPLETE).

## 5. Frozen arms and hand-derived expectations

Phase 0 (all arms except FRESH): teach facts 0..8; m_teach m(0)
rels [7,7,7] facts [0,1,2] start 0 end 90; m_teach n(1) rels
[8,8] facts [3,4] start 15 end 70; m_teach d(2) rels [9] facts
[5] start 0 end 200. M-OK: ev_query(0,90) -> 90 via MAP0.
N-OK: ev_query(15,70) -> 70 via MAP1 (pipeline tries MAP0 first:
clean fail from 15, then MAP1). INTERSECT(m.facts, n.facts) = 0
printed; N-OK line precedes the KILL line in output.

- ARM-FULL (SUB_ON=1, ET_ON=0): KILL fact 1. Query (0,90).
  Pipeline: MAP0 exec stale at hop 1 (fact 1 dead); MAP1 clean
  fail from 0; MAP2 full exec to 200 != 90. Adapt phase:
  SUB-BRACKET; stale-detect ascan MAP0 (S=1), m_exec (E=1),
  sm=0. SUB-STALE m=0 hop=1 fact=1. SUB-SEG s=15 e=70 pre=1
  suf=1. Piece search: cid=0 ascan (S=2) skip=self; cid=1 ascan
  (S=3), facts 3,4 live (S=4,5): MATCH (cid=2 never examined:
  first match wins). Dedup ascan MAP0/1/2 (S=6,7,8): no rlen-4
  MAP. SUB-BUILD rels=7,8,8,7 facts=0,3,4,2. chain_exec verify
  -> 90 (E=2). SUB-VERIFY term=90. SUB-PROMOTE m2=3. SUB-T16
  3->0, 3->1. SUB-RETIRE m=0. Deliver: m_exec MAP3 -> 90 (E=3).
  ANS via=3 val=90. LINK14 34->3. type-15 0->1, 1->0.
  Frozen: ans=90 via=3; A_SEARCH=8; A_EXEC=3; t16=2 {3->0,3->1};
  t15=2 {0->1,1->0}; some LINK14 edge with to==3; other=0; MAP3
  relseq [7,8,8,7] start 0 end 90 live 1.
  Post-query (0,90): pipeline skips retired MAP0, MAP1 fails,
  MAP2 -> 200, MAP3 -> 90. Frozen: ans=90 via=3, MAP0 live=0.
- ARM-NO-SUB (SUB_ON=0, ET_ON=1): KILL fact 1. Query (0,90).
  Pipeline fails as in FULL. ET-BRACKET: TRUNCATE sub-pass: MAP0
  stale@hop1 -> t=3 facts [0] rels [7] 0->15, verified,
  type-16 3->0, MAP0 retired (reason 2). EXTEND sub-pass over
  live MAP1, MAP2, MAP3: MAP1 clean fail from 0, skip; MAP2 full
  exec -> 200, frontier fact 6 -> e=4 rels [9,9] facts [5,6]
  0->210, type-16 4->2; MAP3 full exec -> 15, frontier fact 3
  (fact 1 dead; fact 3 first live in id order with sub 15) ->
  e=5 rels [7,8] facts [0,3] 0->40, type-16 5->3. Re-run: MAP1
  fail, MAP2 ->200, MAP3 ->15, MAP4 ->210, MAP5 ->40: none == 90.
  Frozen: ans=-2; t16=3. Extend/truncate genuinely fired and
  still failed.
- ARM-ABLATE-N (SUB_ON=1): retire MAP1 (reason 3, N-RETIRED),
  KILL fact 1. Query (0,90). Stale-detect: MAP0 (S=1, E=1).
  Piece search: S=2 self; S=3 retired skip; S=4 endpoint skip
  (d: 0->200 vs seg 15->70). No candidate. rebuild_fallback:
  L=1: 1 scan x9 (S=13), [0],[5], 2 verifies (E=3), terms
  15,200; L=2: 2 scans x9 (S=31), [0,3],[5,6], 2 verifies (E=5),
  terms 40,210; L=3: 2 scans x9 (S=49), [0,3,4], 1 verify (E=6),
  term 70; L=4: 1 scan x9 (S=58), [0,3,4,2], 1 verify (E=7) ->
  90. Promote NATIVE MAP3 (no type-16). Deliver m_exec (E=8).
  ANS via=3 val=90.
  Frozen: ans=90 via=3; A_SEARCH=58; A_EXEC=8; t16=0.
  Ratio 58/8 = 7.25x.
- ARM-ABLATE-M (SUB_ON=1): KILL fact 1, KILL fact 0 (ablates m's
  surviving prefix). Query (0,90). Stale-detect: MAP0 stale@hop0
  (S=1, E=1). Piece search for seg (0,15): S=2 self; S=3 (n:
  start 15 != 0); S=4 (d: end 200 != 15). No candidate. rebuild:
  L=1: 1 scan x9 (S=13), [5], 1 verify (E=2), term 200; L=2:
  1 scan x9 (S=22), [5,6], 1 verify (E=3), term 210; L=3:
  1 scan x9 (S=31), none. Fail.
  Frozen: ans=-2; t16=0; NM=3.
- ARM-FRESH (SUB_ON=1): teach facts 0..8, KILL fact 1, no MAPs.
  Query (0,90). No stale MAP. rebuild_fallback: L=1: 1 scan x9
  (S=9), [0],[5], 2 verifies (E=2); L=2: 2 scans x9 (S=27),
  [0,3],[5,6], 2 verifies (E=4); L=3: 2 scans x9 (S=45),
  [0,3,4], 1 verify (E=5); L=4: 1 scan x9 (S=54), [0,3,4,2],
  1 verify (E=6) -> 90. Promote NATIVE MAP0 (id 0). Deliver
  m_exec (E=7). ANS via=0 val=90. LINK14 32->0.
  Frozen: ans=90 via=0; A_SEARCH=54; A_EXEC=7; t16=0.
  Ratio 54/8 = 6.75x.

## 6. Kill bars (frozen)

- K-0 (commit-order self-check): the prereg commit contains
  PREREG.md + NAMECHECK.md only (no .zag, no binary, no runs)
  and strictly precedes the implementation commit in git log
  order.
- K-1 (n independent and prior): INTERSECT(m.facts,n.facts)==0
  printed; M-OK ans==90 via MAP0; N-OK ans==70 via MAP1; the
  N-OK line precedes the KILL line in output (shell line-number
  check).
- K-2a (ablate n): ABLATE-N t16==0 AND ans==90 AND
  A_SEARCH(ABLATE-N)=58 >= 5*A_SEARCH(FULL)=40 (7.25x). The
  adapted m2 cannot exist without n; the learner rebuilds from
  scratch at 7.25x the substitution search cost.
- K-2b (ablate m prefix): ABLATE-M ans==-2 AND t16==0 AND
  NM==3.
- K-3 (fresh learner): FRESH t16==0 AND ans==90 AND
  A_SEARCH(FRESH)=54 >= 5*A_SEARCH(FULL)=40 (6.75x).
- K-4 (white-box trace): run1 output contains, verbatim:
  `SUB-STALE m=0 hop=1 fact=1`,
  `SUB-CAND id=1 s=15 e=70 flive=2 MATCH`,
  `SUB-BUILD rels=7,8,8,7 facts=0,3,4,2`,
  `SUB-VERIFY term=90`, `SUB-PROMOTE m2=3`, `ANS via=3 val=90`
  (shell grep -F, all six).
- K-5 (no-substitute control fails): NO-SUB ans==-2 AND t16==3
  (extend/truncate fired and still failed).
- K-6 (stale retired, not reused): FULL MAP0 live==0 AND
  post-query ans==90 via MAP3.
- K-7 (provenance, zero new types): FULL t16==2 with edges
  exactly {3->0, 3->1}; t15==2 with edges exactly {0->1, 1->0};
  some LINK14 edge with to==3; zero edges with type outside
  {14,15,16}.
- K-8 (determinism): 3/3 runs byte-identical (sha256 equal).
- K-9 (audit): 8 frozen grep patterns return 0 hits on
  learner.zag (section 7).
- K-10 (FULL success): FULL ans==90 via MAP3 with MAP3 relseq
  [7,8,8,7], start 0, end 90, live 1.
- K-11 (no-retuning): sha256(learner.zag) equals the pinned
  C298 hash
  fdf33e3869969ffb38dc5334ddb184cad8283afcf23164f56040db554c2d69c1,
  and every constant in the section-4 list is unchanged between
  instantiations (entailed by byte-identity); world.zag and
  driver.zag differ from C298's only in facts, relation ids,
  MAP inventory, kill, query, and hand-derived expectations.
- K-12 (chain regression): re-running the frozen C298 binary
  `l2_substitute/sub_bin` reproduces its frozen run digest
  198ef5c6d9bdc2dae17182cb4f9a7b1c89b6f2e53208243b7bd2b4474c38f261,
  confirming the shared operator file still passes C298's core
  assertions in the chain substrate.

Verdict L2-TRANSFER-SUBST-COMPLETE iff K-0 through K-12 all PASS
and no falsifier fires.

## 7. Frozen K-9 grep audit spec (run on learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `7,8,8,7` (m2's relseq must not be in the learner)
2. `0,3,4,2` (m2's fact list must not be in the learner)
3. `(15,8,40)` (n's fact literal; world data stays out)
4. `(15,7,70)` (killed fact literal; world data stays out)
5. `_MODE` (zero modes)
6. `bridge` (case-insensitive; no bridge handlers)
7. `python` (case-insensitive; pure Zag)
8. `as *i32` (the pinned-znc miscompile pattern; u8 cells only)

## 8. Frozen falsifiers

- F-NO-CAND: FULL sub_bracket finds no candidate.
- F-WRONG-M2: promoted m2 relseq != [7,8,8,7] or (start,end)
  != (0,90).
- F-STALE-REUSE: any FULL ANS via=0 after MAP0 retirement.
- F-CTRL-PASS: NO-SUB ans != -2.
- F-ABLN-ADAPT: ABLATE-N t16 != 0.
- F-ABLM-PASS: ABLATE-M ans != -2.
- F-FRESH-ADAPT: FRESH t16 != 0.
- F-EDGE-NEW: any edge with type outside {14,15,16}.
- F-RETUNE: any section-4 constant differs between
  instantiations, or learner.zag is not byte-identical to the
  pinned C298 file. A required edit is reported as a generality
  failure of the edited component, never silently absorbed.
- F-AUDIT / F-NONDET / F-PYTHON: as in prior waves; any fires
  voids the build.

## 9. Determinism spec

No RNG. Node-id order everywhere; first-match candidate rule;
ascending fact-id scans; iterative deepening L=1..4. Output via
one preallocated buffer and a single raw-syscall write loop.
3/3 byte-identical required (sha256).

## 10. Disclosed residual footprint and non-claims

- The SUBSTITUTE operator, the stale-check exec semantics, the
  rebuild fallback, the extend/truncate control operators, the
  edge-type conventions, and the cost counters are
  researcher-supplied generic machinery, frozen in the shared
  file. The generality claim is narrow: the same operator file,
  with zero constant changes, performs dead-segment
  substitution in the arithmetic substrate, with the
  no-substitute control provably failing and the ablation cost
  contrasts holding.
- SUB_ON/ET_ON are driver-set causal-control flags (the
  composition_l2 adapt_on precedent), never written by the
  learner. They enable the lesion comparison; they are not
  runtime modes.
- One world family (summation with a middle price-fact kill).
  No generality claim beyond the five arms plus the chain
  regression. The kill was builder-designed, not
  adversary-designed. Sealed-adversary generality is open future
  work.
- 0 modes, 0 bridges, 0 handlers, 0 new edge types, 0 new
  opcodes, 0 new semantic cases. Pure Zag.
- No em/en dashes in loop documentation. Paper untouched.
  Nothing pushed. Commits local on tnn-native-lab.
- Unfrozen only: no frozen source touched. The frozen TNN core
  is not used here; this is a standalone learner-mechanism
  experiment.
