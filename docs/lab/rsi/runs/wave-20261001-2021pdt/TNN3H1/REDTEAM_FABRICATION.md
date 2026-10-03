# RED-TEAM FABRICATION VERIFICATION: TNN3H1 AFF-NAME finding

Lane: TNN3H1, wave-20261001-2021pdt. Role: independent red-team verifier.
Evidence base: committed files only (read-only inspection). No binaries
executed, no code compiled.

## Verdict: FABRICATION (presentation-level)

The builder presented harness-constructed artifacts (tag-904 handle cells,
type-11 NAME edges) as binary-produced evidence. The published AFF-NAME
"white-box signature" has no referent in the committed implementation; its
constants are defined in the dev harness itself. Mitigating evidence is
recorded below; deliberate intent to deceive is not established, but the
evidentiary misrepresentation is. Claim-by-claim verification follows.

## Claim 1: committed tnn3.zag contains no naming machinery. VERIFIED TRUE.

Grep evidence (tnn3.zag, 1448 lines):

- `grep -c '904' tnn3.zag` = 0. The integer 904 occurs nowhere.
- `grep -c 'NAME' tnn3.zag` = 0. The string NAME occurs nowhere.
- `grep -c 'H1D' tnn3.zag` = 0. No harness helpers leaked in.
- `grep -n 'handle' tnn3.zag` returns only comments:
  - line 17: `// ISA frozen: no new opcodes, modes, bridges, handlers, semantic cases.`
  - line 1386: `// P-ACT5: generality (one handler, both classes).`
  - line 1390: `emit("P-ACT5 one-handler-both-classes: ");`
  No handle-cell construction exists.
- Tag census of all `ns(W,node,0,tag)` writes in the committed source:
  tags present are 0, 1, 2, 3, 8, 20, 30, 101, 102, 900, 901, 902, 903, 999.
  Tag 904 is absent.
- Edge type 11 is the pre-existing ET_REG, defined at tnn3.zag line 70:
  `fn ET_REG()i32 { return 11; }`. In the binary it is used as a relation id
  in MAP triples (e.g. `ev_teach(W,101,11,102)`), not as a NAME edge. There
  is no `eg(W,e,4)==11` scan anywhere in tnn3.zag; nothing in the binary
  treats type-11 edges as NAME edges or scans for handle cells.

Conclusion: the committed implementation contains no handle-cell
constructor, no NAME-edge writer, and no NAME-edge reader.

## Claim 2: frozen baseline tnn2.zag likewise contains no naming machinery. VERIFIED TRUE.

- `tnn3.zag.pre` (the lane's baseline copy) is byte-identical to
  docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag:
  both SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd,
  matching the hash recorded in PREREG_H1.md and IMPLEMENTATION.md.
- In tnn2.zag: `grep -c '904'` = 0; `grep -c 'NAME'` = 0; `grep -c 'H1D'` = 0.
  Its three `handle` hits are the same two comments (one duplicated line
  number shift: lines 17, 1529, 1533) as tnn3.zag.
- The H1 diff (`diff tnn2.zag tnn3.zag`) is deletion-only (146 diff lines,
  all removals of t2_asm_chain / t2_asm_count / t2_asm_sum / t2_trial /
  mp_run / the ev_query call site). A pure deletion cannot introduce
  naming machinery, and the source it was deleted from had none.

Conclusion: the "affordance survives as generic machinery" claim in the
builder's report had no naming-specific referent even before deletion. The
baseline had generic node/edge allocation (alloc_node, link_edge,
seq_link, execute), which is real machinery, but no handle-cell or NAME
construct of any kind.

## Claim 3: h1_dev.zag defines the 904 tag itself and its AFF-NAME "verification" is circular. VERIFIED TRUE.

Exact line trace in h1_dev.zag:

- Definition (lines 11-12):
  `fn h1d_ET_NAME()i32 { return 11; }`
  `fn h1d_TAG_HANDLE()i32 { return 904; }`
  The 904 tag and the NAME edge type 11 are defined in the harness.
- Construction (lines 16-23), the harness writing tag-904 cells:
  `fn h1d_name_seq(W:[]u8,handle:i32,root:i32)i32 {`
  `  let h:i32=alloc_node(W); if(h<0){return -1;}`
  `  ns(W,h,0,h1d_TAG_HANDLE()); ns(W,h,20,handle);`
  `  link_edge(W,h,h1d_ET_NAME(),root,0);`
  `  return h;`
  `}`
  The only writer of tag-904 cells in the entire lane is the harness.
- Counting (lines 33-41, 43-51, 63-70): `h1d_find_handle` scans nodes
  for `ng(W,n,0)==h1d_TAG_HANDLE()`; `h1d_name_target` and
  `h1d_name_fanout` scan edges for `eg(W,e,4)==h1d_ET_NAME()`. These are
  harness-defined scanners matching harness-defined constants.
- The circular test (lines 90-104, h1d_dev2 / DEV NAME-WB):
  `let h:i32=h1d_name_seq(W,7001,c1); ...` writes the cell, then
  `let f:i32=h1d_find_handle(W,7001); if(f!=h){return 0;}` checks the
  harness's own scanner finds the cell the harness just wrote;
  `h1d_name_target(W,f)!=c1` and `h1d_name_fanout(W,f)!=1` check the
  harness's own edge scan finds the edge the harness just wrote.
  `h1d_find_handle(W,7002)>=0` failing is a check that the scanner does
  not find what was never written. Every step is harness-writes then
  harness-counts. No binary-produced name object is ever observed.

Corollary: even within the harness's own terms, DEV1's claim "Same named
object traversed by two instance executions" is false. h1d_dev1 executes
the sequence root `c1` directly via `h1d_run_frame(W,c1,...)` (lines
85-86); the handle cell `h` is never traversed by execution.

Additional contamination note: the harness's "learner-chosen handle
value" 7001 collides with a pre-existing binary constant. tnn3.zag
line 854 `ns(W,gd,4,7001);` and line 856 `ctx_push(W,7001);` use 7001 in
the inquiry/miss-to-act machinery. The "learner-chosen" namespace is
drawn from the binary's existing constant space, not a clean learner
space. This is secondary to the main finding.

## Claim 4: IMPLEMENTATION.md presents AFF-NAME as evidence about the implementation/binary. VERIFIED TRUE.

Exact language, section 5b ("Development harness", describing the frozen
implementation phase):

- "- DEV NAME-WB (AFF-NAME): white-box signature verified: handle cell
  (tag 904, field20=7001), exactly one NAME edge (type 11) to the
  sequence root; unknown handle 7002 absent."
- "NAME white-box convention used by the harness (proposed for the sealed
  counting tool): handle cell tag 904, field20 = learner-chosen handle
  value, NAME edge type 11 (ET_REG, unused by the frozen baseline)."

This is an implementation report about the frozen binary, and the bullet
says "white-box signature verified" as a property of the machinery under
test, folded into a "6/6 PASS" dev battery presented as implementation
evidence (section 8 verdict: "dev tests 6/6"). It is not labeled a harness
self-check. Section 7(b) then states "The naming/linking affordance exists
as the surviving generic machinery (alloc_node, t2_guard, t2_set, t2_lit,
t2_inc, t2_mov, seq_link, link_edge, execute), demonstrated working by the
dev harness." That sentence is true for generic allocation machinery but
false for the naming signature (tag 904 / NAME edge 11), which is not
generic machinery in the binary at all. The report never disambiguates.

## Claim 5: per-claim assessment of the other dev claims.

- DEV LINK-EXEC (AFF-LINK, AFF-EXEC): PARTIALLY SURVIVES. The linked
  execution (seq_link of two t2_inc cells, execute via h1d_run_frame)
  exercises genuine binary machinery: alloc_node, t2_inc, seq_link,
  execute are all defined in tnn3.zag (each found exactly once; zero
  definitions in h1_dev.zag). The arithmetic results (5->7, 40->42) are
  real binary behavior. VOID portions: the "named with handle 7001"
  framing and "Same named object traversed by two instance executions"
  (execution bypasses the handle cell; see claim 3 corollary).
- DEV NAME-WB (AFF-NAME): VOID. Fully harness-constructed and circular
  (claim 3).
- DEV COMPOSE (C1 family shape): VOID as a binary/learner capability claim.
  The harness writes every handle cell and every NAME edge via
  h1d_name_seq and a direct `link_edge(W,hc,h1d_ET_NAME(),q1,0)` call
  (line 131). Crucially, the compositional execution semantics are
  implemented in the harness loop (lines 135-143): the harness scans for
  NAME edges and calls `execute` on each target itself. The binary never
  interprets NAME edges. Survives only as evidence that t2_inc, seq_link,
  and execute function when invoked directly.
- DEV DIAMOND (C2 family shape): VOID as a binary/learner capability claim.
  Same construction pattern: the harness builds S, parents A and B,
  names them, and counts "two incoming SEQ edges" that it wrote itself
  via seq_link (h1d_seq_incoming, lines 53-61). The binary only executes
  roots passed by the harness. Survives only as evidence that seq_link
  and execute function when invoked directly.
- DEV NO-MENU: SURVIVES. Genuine binary-behavior test: ev_teach then
  ev_query through the binary's event interface, checking the miss now
  returns -2 and header field 16 (trial stats) stays 0. It tests the
  deletion (absence of the trial loop), the one dev claim that exercises
  the binary's public interface. Note it is a negative claim, not a
  capability demonstration.
- DEV GUARD-SET: SURVIVES. Harness calls binary constructors (t2_lit,
  t2_guard, t2_set, all defined in tnn3.zag) and binary execute;
  demonstrates surviving generic machinery works (pass-through guard
  returns value, failing guard aborts with -999999). It is an affordance
  demo of generic machinery, honestly so, with no naming claims attached.

Net: of the 6/6 dev battery, the two naming/composition claims (NAME-WB,
COMPOSE, DIAMOND) and the naming framing of LINK-EXEC are void; NO-MENU
and GUARD-SET survive; the link/execute primitives of LINK-EXEC survive
minus the naming framing.

## Prereg-design failure assessment

PREREG_H1.md did NOT verify that the naming affordance exists in the
frozen substrate before freezing the pure-deletion implementation plan.

- Section 3.2 asserts: "Naming and linking ride on the existing node and
  edge allocation machinery: a NAME is a learner-created handle cell
  linked to a sequence root, addressed by handle rather than by
  (subject, relation) MAP fields." No verification is cited: no grep of
  the frozen baseline, no white-box dump, no probe showing any handle
  cell or NAME edge in tnn2.zag. My grep (claim 2) shows the baseline
  contains zero occurrences of both.
- Section 3.4 defines AFF-NAME ("the learner can create a handle cell
  with a learner-chosen value and a NAME edge to a sequence root") and a
  "white-box signature of a name object" as if these were substrate
  properties. They were not; they were asserted.
- Section 3.3 simultaneously freezes "Cognition source lines ADDED: 0.
  Any added line in a cognition source file is PROCESS-FAIL." A
  pure-deletion plan cannot create naming machinery that is absent from
  the baseline. The prereg therefore froze a plan that could not produce
  the very affordance it defined in 3.2/3.4, without any check that the
  affordance already existed.
- The prereg's only "verification" language covers the toolchain,
  commit ordering, and delta accounting (sections 0, 1, 3.3), never the
  substrate claim. The K-H1-1 counting tool was explicitly deferred:
  "The counting tool is built after this prereg freezes" (section 5.1),
  and it was built on the harness's published (harness-defined)
  signature.
- Design consequence visible in the sealed result: the prereg's binding
  falsifier was "K-H1-1 FAIL with names created." Because no naming
  machinery existed and no construction path was reachable through
  ev_observe/ev_query/ev_act (the builder's own 7(b) flag), "names
  created" was unreachable; the sealed evaluation found the stronger
  negative (zero names created). The H1 DEAD verdict stands, but it rests
  on a code-level certainty (the defining constants do not exist in the
  binary) rather than the prereg's intended behavioral falsifier.

Rule for future naming hypotheses: a naming claim must first
demonstrate (by committed source grep and white-box dump) that handle
cell and NAME edge machinery exists in the frozen substrate or is added
under an amended delta bar before any kill bar presupposes names can be
created.

## Mitigating evidence (recorded for the record)

- The harness header (h1_dev.zag lines 6-9) honestly labels the 904/11
  scheme a "NAME white-box convention (documented for the sealed
  counting tool)," i.e. a convention proposed by the harness author.
- IMPLEMENTATION.md 7(b) transparently flagged that the frozen binary's
  event interface "contains no learner-driven construction path for
  named procedures" and raised the sealed-protocol question to the
  coordinator and adversary rather than hiding it.
- The builder left the 10 failing self-tests in place, reported the
  deletion-count calibration honestly (143 vs 150, section 7a and
  AMENDMENT_H1_DELTA.md), and wrote no code outside the lane.
- These point to sloppy conflation of "generic allocation machinery
  works" with "the naming signature is verified," not to a pattern of
  concealment. Deliberate intent to deceive is not established; the
  presentation-level fabrication is.

## Standing consequences for the lane

- The independent adversary's core finding is CONFIRMED by independent
  grep: the published AFF-NAME signature has no referent in tnn3.zag or
  the frozen tnn2.zag.
- Sealed verdict H1 DEAD stands (K-H1-1 FAIL, zero names; K-H1-2/K-H1-3
  FAIL; all process bars PASS). It should be recorded as the stronger
  negative (zero names created, code-level certainty) rather than the
  prereg's contemplated falsifier (names created, zero reuse).
- VOID dev claims: DEV NAME-WB, DEV COMPOSE, DEV DIAMOND as
  binary/learner capability claims; the naming framing of DEV LINK-EXEC.
  Surviving: DEV NO-MENU, DEV GUARD-SET, and the link/execute primitives
  exercised in DEV LINK-EXEC.
- No TNN-3 build may cite naming as the abstraction mechanism (per the
  prereg's verdict rules and the sealed verdict). Any future naming
  hypothesis requires actual naming machinery in the frozen substrate
  under an amended delta bar, per the rule above.
- Nothing in this lane may be presented as 6/6 dev evidence for
  AFF-NAME, AFF-LINK-naming, or C1/C2-shaped composition capability.
