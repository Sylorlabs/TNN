# PREREG: H-COLLAPSE-1 Composition Collapse into Fragment DFS (UNFROZEN)

Status: FROZEN. This file is committed ALONE before any implementation.
Worker: Composition Collapse Worker (H-COLLAPSE-1, P0). Date: 2026-10-02.
Branch: tnn-native-lab. Local only, never pushed. Pure Zag. Frozen read only.

## 1. Hypothesis

H-COLLAPSE-1: the unified composition mechanism's whole-MAP DFS path is
redundant. Invention H2 (C213) showed fragment DFS subsumes whole-MAP DFS
as the special case (m,0,len). H-DECOMP-1 (C227) proved a shared type-15
LINK fragment store serves both Composition-C and H2 lineages. Therefore
the whole-MAP DFS path can be DELETED: route ALL composition through the
fragment store plus fragment DFS, with whole MAPs as fragments (m,0,L).
Capability matches the unified mechanism with fewer lines.

## 2. Design (frozen)

Base: composition_C/cc_base.zag (1677 lines, frozen, read only).
Patch: composition_collapse/cl_patch.zag (this worker, written after this
prereg commit). Driver: composition_collapse/cl_driver.zag.

### 2.1 Fragment store (shared substrate, ported from H-DECOMP-1)

- A fragment mark is ONE type-15 LINK edge: from = MAP node m,
  to = entry guard cell of the sub-chain at position start,
  aux field = (start << 16) | len.
- API: cl_mark (validate, dedup, write), cl_fetch (resolve mark, walk
  len steps from the entry cell reading each step's relation from its
  licensing fact's DEP edge, check satisfiability from cur via fact
  lookup; returns len or -1), cl_chain_len and cl_entry (structural
  walks; MAP field 4 and field 8 never consulted).
- Coexistence rule: B's co-use history also uses type-15 edges, written
  with aux = 0. A type-15 edge is a FRAG mark iff aux != 0; it is a
  co-use edge iff aux == 0. Candidate enumeration and cb_has_couse both
  discriminate on aux. Marks are learner-state edges, not machinery.

### 2.2 Whole-MAP deletion (the collapse)

- compose_try FIRST auto-marks every live chain MAP m as (m,0,L) where L
  is its structural chain length (dedup: marks are written once). This
  is the only mark creation inside composition; no per-mechanism tables.
- cl_candidates enumerates candidates ONLY from type-15 FRAG marks
  (aux != 0) in edge-id order. No MAP-structural candidate walk exists
  anywhere in the composition path. Whole MAPs appear as (m,0,L) marks.
- cl_dfs is iterative DFS over marks only, max 8 segments, excluding
  reuse of the same (m,start,len) triple in one path. History-first
  ordering by the source MAP's co-use signal, then decreasing len,
  ties stable by edge id.
- Predicates ported to fragments:
  - C's principle: cl_fetch satisfiability (constraint walk).
  - A's principle: contract fallback. A fragment's contract is its
    plen len+1; if the structural fetch fails, fall back to a real
    gathered path of plen len+1 from cur (t2_gather). Consulted, not
    a gate.
  - B's principle: cb_has_couse on the source MAP orders candidates;
    composition successes write type-15 co-use edges (aux = 0) between
    consecutive segments' source MAPs. ev_cq episode facility retained
    verbatim for the battery's co-use episodes.
- Assembly, verification, promotion: unchanged from the unified
  mechanism (per-segment t2_asm_chain, SEQ-link, t2_try_verify,
  promote_graph, LINK14 provenance to each segment's source MAP).
- ev_query: activate -> rebind_try -> compose_try -> trial ->
  bootstrap. One compose_try definition, one call site. No
  COMPOSE_MODE. Zero modes, bridges, handlers, new semantic cases.

### 2.3 What is deleted relative to the unified patch

- cc_relseq / cc_satisfy whole-MAP candidate walk (replaced by
  cl_mark + cl_fetch through the store).
- un_candidates whole-MAP scan (replaced by cl_candidates over marks).
- un_dfs whole-MAP DFS (replaced by cl_dfs over marks).

### 2.4 Driver

cl_driver.zag: the 6 unified battery tests, same world protocol and
same expectations (T1/T2A/T2B 3/4/5-structure, T3 cross-domain, T4
partial, T5 no-expected), PLUS one collapse-specific test:
- T4B: T4 world, then the driver seeds sub-fragment marks (mx,0,3),
  (mx,1,3), (my,0,2) on the trained X/Y MAPs (researcher-seeded, as in
  H-DECOMP-1), then the Z query must PASS with ans = 106. This proves
  the collapsed mechanism genuinely consumes sub-fragment marks: the
  fragment path is real, not a renamed whole-MAP path.

## 3. Kill bars (all must pass for COMPOSITION-COLLAPSE-COMPLETE)

- K1: T1 PASS (match unified).
- K2: T2A PASS (4-structure; match unified).
- K3: T2B PASS (5-structure; match unified).
- K4: T3 PASS (cross-domain; match unified).
- K5: T4 FAILS without false positive and terminates (match unified;
  no regression).
- K6: T5 compose declines (-2), terminates (match unified).
- K7: T4B PASSES (ans = 106) using the seeded sub-fragment marks.
- K8: cl_patch.zag line count STRICTLY FEWER than unified
  un_patch.zag (420 lines).
- K9: 3/3 runs byte-identical stdout (SHA-256 recorded).
- K10: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases; exactly
  one compose_try definition and one call site; no COMPOSE_MODE; no
  whole-MAP DFS path (grep audit: no candidate walk over MAP
  structures outside mark creation/fetch).
- K11: pure Zag only (toolchain guard in NAMECHECK.md Step 0; no
  forbidden executable invoked).

No unified kill bar is weakened: K1-K6 and K10 reproduce the unified
bars at equal strength. K7 is an additional collapse bar, K8 the
line-delta bar.

## 4. Verdict names

- All bars pass: COMPOSITION-COLLAPSE-COMPLETE (report line-count
  delta vs 420 and capability parity table vs unified).
- Any bar missed: BUILD-FAIL (report which bar, and diagnose exactly
  what the whole-MAP path provided that fragments could not).

## 5. Method

- Toolchain guard recorded in NAMECHECK.md Step 0 before any work.
- Build: cat cc_base.zag cl_patch.zag cl_driver.zag > cl_full.zag;
  compile with pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1.
- Commits: this PREREG.md ALONE first; then implementation plus
  results with explicit pathspecs. Local only, never pushed.
- Zero em/en dashes in all documents (byte-verified before commit).
