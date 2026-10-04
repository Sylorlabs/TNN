# PREREG: Cross-Domain L2 INTERFACE ADAPTATION (causal path model to intervention)

Frozen 2026-10-02. Committed alone (with NAMECHECK.md Step 0 guard) before
any implementation. Worker: XDomain L2 Interface-Adaptation Worker.
Branch: tnn-native-lab. Local only, never pushed.

## Objective

Demonstrate genuine L2 ADAPTIVE REUSE of the interface-adaptation family
across domains: the learner bridges a real interface mismatch between two
independently learned structures, with no exact-reuse path available.

- X = learned causal model: walks a learned causal relation (r=91) and
  produces a causal PATH (sequence of nodes from cause to effect).
  Learned signature: NODE -> PATH.
- Y = learned intervention selector: expects as input a single
  intervention TARGET node (r=92 lookup: target -> action).
  Learned signature: NODE -> NUM.
- The mismatch: X outputs a path value; Y's input contract requires a
  node. X.out (PATH) != Y.in (NODE).

Prior work proved EXACT reuse of causal -> intervention; that result is
not redone here. In this design exact functional composition (H2
value-passing) is blocked at the contract level: the H1-style
contract-checked composer detects X.out != Y.in, refuses the pair, and
emits a MISMATCH trace. The learner must then, triggered by the mismatch
detection alone, search its own learned inventory for an interface
adapter (a PATH -> NODE projection), select one by a learner-owned rule
grounded in its causal knowledge, verify the adapted pipeline by real
execution in the world, and promote the composite with provenance edges.

The adapter is learner-selected from independently learned structures,
never researcher-selected per problem. No paired training examples of
the full Z task exist. No domain-pair-specific composition handler is
used: the adapt bracket is generic over kinds and MAPs.

## Value kinds (generic machinery, frozen)

The kind probe is generic, as in the H1 typed-contract work:

- NODE (1): value appears as a fact subject.
- PATH (3): value falls in the path-record handle range (handles are
  workspace offsets of path records; no node or action id ever does).
- NUM (2): otherwise.

All MAP signatures are LEARNED from probe_kind observations during
teaching (record_obs / finalize_sig, majority rule). Zero per-MAP
signature literals appear in source. PATH is a value kind in the generic
probe, not a MAP type, edge type, opcode, mode, bridge, handler, or
semantic case.

## Inventory (all learned independently before any Z query)

Behaviors (exec_map dispatch; fixed small set, no per-query logic):

- 0 X: causal path build. Walks r=91 from the start node, collects the
  node sequence into a fresh path record, returns the record handle.
- 1 FIRST: path handle -> first node of the path.
- 2 LAST: path handle -> last (effect) node of the path. This is the
  adapter the learner should select.
- 3 D_PROJ: path handle -> second node (first if length < 2). In-inventory
  distractor projection with a matching PATH -> NODE signature.
- 4 PATHLEN: path handle -> path length. PATH -> NUM distractor.
- 5 Y: intervention lookup. find_obj(v, 92); -1 on failure.
- 6 D_ID: identity. NODE -> NODE distractor.
- 7 D_COUNT: count of r=91 facts with subject v. NODE -> NUM distractor.
- 8 COMP3: composite of three segments (a, b, c) by value passing.

Teaching (independent queries; the Z pair is never taught as a pair):

- X: 11 -> path[11,12,13]; 21 -> path[21,22,23,24]; 12 -> path[12,13].
  Signature learned: NODE -> PATH.
- FIRST: path(11) -> 11; path(21) -> 21. Learned: PATH -> NODE.
- LAST: path(11) -> 13; path(21) -> 24. Learned: PATH -> NODE.
- D_PROJ: path(11) -> 12; path(21) -> 22. Learned: PATH -> NODE.
- PATHLEN: path(11) -> 3; path(21) -> 4. Learned: PATH -> NUM.
- Y: 13 -> 101; 24 -> 102. Learned: NODE -> NUM.
- D_ID: 11 -> 11; 21 -> 21. Learned: NODE -> NODE.
- D_COUNT: 11 -> 2; 21 -> 3. Learned: NODE -> NUM.

World facts (r=91 causal, r=92 intervention, plus distractors):

- (11,91,12), (12,91,13): causal chain 1, path length 3.
- (21,91,22), (22,91,23), (23,91,24): causal chain 2, path length 4.
- (31,91,32), (32,91,33): causal chain 3 (A8 impossible world; no r=92
  facts touch 31/32/33).
- (13,92,101), (24,92,102): intervention facts.
- 12 distractor facts, subjects 5000+, relations 60..69.

The mismatch is present from the start: X is only ever taught as
NODE -> PATH, Y only as NODE -> NUM. No rigged retraining occurs.

## Solver (frozen)

solve_z(W, s, target):

1. kin = probe_kind(s) (NODE); kout = probe_kind(target) (NUM).
2. Singles: for each live MAP m in node-id order with sig_in(m) == kin
   and sig_out(m) == kout: r = exec_map(m, s), trace TRY-SINGLE; if
   r == target, emit Z-SINGLE and succeed.
3. Exact pairs (contract-checked, H1 style): for a, b in node-id order
   with sig_in(a) == kin and sig_out(b) == kout:
   - if sig_out(a) == sig_in(b): execute mid = exec_map(a, s),
     r = exec_map(b, mid), trace TRY-PAIR; if r == target, promote an
     exact composite and succeed.
   - else: emit MISMATCH a=<id> out=<kind> b=<id> in=<kind>; refuse the
     pair (no execution); record (a, b) as a mismatch pair.
4. Adapt bracket (fires only after steps 2-3 fail; gated by adapt_on()):
   for each recorded mismatch pair (a, b) in order: for each live MAP c
   in node-id order with sig_in(c) == sig_out(a) and
   sig_out(c) == sig_in(b):
   - P = exec_map(a, s); n = exec_map(c, P); yv = exec_map(b, n).
   - Trace ADAPT-TRY c=<id> proj=<n> yexec=<yv>.
   - Learner-owned intervenability rule: the projected value must be
     acceptable to the downstream consumer, i.e. exec_map(b, n) != -1.
     This is grounded in learner state (Y's learned behavior over the
     fact store); no relation id is named in the rule.
   - If yv != -1 and yv == target: promote the adapted composite and
     succeed. First verifier wins; the choice is deterministic.
5. Else emit Z-FAIL.

Promotion (adapted composite): new MAP, behav 8, segments (a, c, b),
sig_in = sig_in(a), sig_out = sig_out(b). Provenance, using only
pre-existing edge types:

- LINK14 (type 14) composition edges: Z -> a, Z -> c, Z -> b.
- type-16 adapted-via edge: Z -> c (marks Z as an adapted composite and
  names the adapter; mirrors the adapted-marking convention).
- type-15 co-use edges: a -> c and c -> b, written on episode success
  (mechanism B: co-use edges written by episode success).

No new edge types, MAP types, opcodes, modes, bridges, handlers, or
semantic cases are introduced. The adapt bracket names no relation, no
MAP id, no kind, and no query; candidates come from the live inventory
in node-id order.

## Battery (frozen)

Every arm uses a fresh workspace. Teach-all means the teaching block
above. The noadapt build differs from the adapt build by exactly one
line (adapt_on 1 -> 0); diff verified.

- A1 L2-TREAT: teach-all; query (11 -> 101). Expect: ADAPT-OK;
  selected adapter c == 2 (LAST); trace shows MISMATCH a=0 out=3 b=5
  in=1, then ADAPT-TRY c=1 proj=11 yexec=-1 (reject), then ADAPT-TRY
  c=2 proj=13 yexec=101 (accept); exactly one Z promoted; Z has LINK14
  to 0, 2, 5; type-16 Z -> 2; type-15 0 -> 2 and 2 -> 5; adapt-ok count
  == 1.
- A2 L2-REUSE: teach-all; query (11 -> 101) then query (21 -> 102).
  Expect: both solve; query 2 is solved by the query-1 composite as a
  single (Z-SINGLE), proving the adapted pipeline generalizes; the
  solving composite's adapter segment id == 2; traced path length for
  query 2 == 4 vs 3 for query 1 (different path length, same adapter);
  adapt-ok count stays 1; no new type-15/16/LINK14 edges on query 2.
- A3 ABL-X: teach-all; kill MAP 0 (X); query (11 -> 101).
  Expect: Z-FAIL.
- A4 ABL-Y: teach-all; kill MAP 5 (Y); query (11 -> 101).
  Expect: Z-FAIL.
- A5 ABL-ADAPTER: teach-all; kill MAP 2 (LAST, the selected adapter);
  query (11 -> 101). Expect: Z-FAIL; trace shows ADAPT-TRY rejections
  for c=1 (proj 11, yexec -1) and c=3 (proj 12, yexec -1); zero
  promotions. This proves the adapter did the work: X and Y intact, Z
  still fails without it.
- A6 NO-ADAPT CONTROL: A1 setup verbatim under the noadapt build.
  Expect: Z-FAIL; trace shows MISMATCH a=0 out=3 b=5 in=1; zero
  ADAPT- lines; zero type-15/16 edges. The exact pipeline
  (singles, contract-checked pairs, H2 value-passing) provably cannot
  solve the mismatch task.
- A7 FRESH: facts only, no teaching; query (11 -> 101). Expect: Z-FAIL.
- A8 L2-IMPOSSIBLE: teach-all; query (31 -> 999) where chain 3 has no
  intervention facts. Expect: Z-FAIL; adapt bracket runs and rejects
  every projection (yexec -1 for proj 31/33/32); zero type-15, type-16,
  and LINK14 edges; zero promotions. Clean reject, no hallucinated
  interface.

## Kill bars (frozen)

- K1: A1 all assertions pass.
- K2: A2 all assertions pass (same adapter id 2 reused; path lengths 3
  vs 4; adapt-ok count stays 1; no new provenance edges on query 2).
- K3: A3, A4, A5 all Z-FAIL (Z causally depends on X, on Y, and on the
  selected adapter specifically).
- K4: A6 Z-FAIL with zero ADAPT- trace lines and zero type-15/16 edges
  (exact-reuse control provably fails the mismatch task).
- K5: A7 Z-FAIL (fresh learner fails).
- K6: A8 Z-FAIL with zero promotions and zero type-15/16/LINK14 edges.
- K7: 3/3 byte-identical runs for both binaries; sha256 digests recorded.
- K8: zero em/en dashes in all deliverables (byte-verified with
  worker_snippets/check_no_dash.sh).
- K9: 0-new-machinery audit passes: edge types used are only 14, 15, 16;
  zero new MAP types, opcodes, modes, bridges, handlers, semantic cases;
  PATH is a generic value kind in the kind probe; all signatures learned
  from observations.
- K10: adapter choice is white-box traceable: the trace names every
  projection tried, its projected node, the consumer-exec result, and
  the accept/reject reason, so the selection of LAST is attributable to
  learner state, not to a researcher choice.

Verdict XDOMAIN-L2-IFACE-PASS iff K1-K10 all pass. Any bar failed, or
any prereg violation, yields VOID or FAIL per the bar; bars are never
weakened.

## Implementation plan (after prereg commit)

1. Write ia_core.zag (adapt_on()=1): prelude with e1str/e1i64 single
   buffer output, workspace layout, kind probe, behaviors, teaching,
   contract-checked solver, adapt bracket, promotion with provenance,
   arms A1-A5, A7, A8, main.
2. Derive ia_full_noadapt.zag by the one-line change (adapt_on 1 -> 0);
   verify `diff` shows exactly one line.
3. Compile both with pinned znc_linux_x86_64_abed8aa1; run 3x each;
   sha256sum; verify byte-identical.
4. Grep `while.*!(` over new .zag files (must be empty); run
   check_no_dash.sh over deliverables.
5. Write REPORT.md citing exact frozen bars, adapter synthesis trace,
   ablation numbers, cognition lines added. Commit with explicit
   pathspecs. Report verdict, per-bar results, sha256 digests, and
   commit hashes to the watchdog.

## Constraints

Unfrozen only (xdomain_l2_causal/). Pure Zag under safebin PATH.
Zero em/en dashes. Paper untouched. Nothing pushed. Prereg commit
strictly precedes implementation. Transparent pre-implementation
amendments only, re-frozen before use.
