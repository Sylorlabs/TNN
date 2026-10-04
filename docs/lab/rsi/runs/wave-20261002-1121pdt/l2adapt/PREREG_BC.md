# PREREG: L2 Adaptive Reuse, candidates B and C

Frozen: 2026-10-02. This preregistration strictly precedes implementation.
No kill bar below may be weakened or reinterpreted after results are seen.
Candidate A (composition_l2 EXTEND/TRUNCATE/SPECIALIZE) was verified 12/12
on an independent clean run (see REPORT.md); this prereg extends the
operator set for cross-domain and interface adaptation.

## Fixed operator set (criterion)

The MAP adaptation operator set is FIXED at five and will not grow:
EXTEND, TRUNCATE, SPECIALIZE (candidate A, frozen), SUBSTITUTE (candidate B),
SUBSEQ (candidate C). Adaptation must be structural (triggered by
learner-state preconditions, candidate relations drawn from observed facts),
never menu selection by the researcher per problem. No further operators
will be added to chase benchmark failures; that would be menu widening.

## Candidate B hypothesis: cross-domain SUBSTITUTE

A MAP learned in domain A (relation 1) can be adapted for domain B
(relation 3) without rebuilding, via a SUBSTITUTE operator that replaces
relations in the MAP's relseq according to structural correspondence
discovered from the target domain's observed facts.

Mechanism (standing rule in un_candidates, fires for every candidate MAP at
every DFS level when adapt_on=1):
- Precondition: the MAP's native constraint walk FAILS from the DFS cursor.
- Discovery: identify the first failing step (relation r at cursor c).
  Collect candidate relations r' such that a live fact (c, r', *) exists.
  Candidate relations come from observed target-domain facts, not a
  researcher menu.
- For each candidate r', substitute r -> r' GLOBALLY in the relseq (domain
  shift is uniform), walk from the cursor. The first satisfiable
  substitution emits variant 4000+r'.
- The researcher never selects a substitution per problem; the one-line
  adapt_on toggle is the causal control.

## Candidate C hypothesis: interface adaptation via SUBSEQ

A MAP's input/output contract can be adapted to a goal requiring a
sub-interval, without rebuilding the MAP, via a SUBSEQ operator that
extracts contiguous sub-sequences of the relseq.

Mechanism (standing rule in un_candidates, fires for every candidate MAP at
every DFS level when adapt_on=1):
- Precondition: the MAP's native constraint walk FAILS from the DFS cursor
  (or succeeds but the operator also tries sub-sequences; minimal: only when
  native fails, to bound cost).
- Discovery: try all contiguous sub-sequences [i..j] of the relseq
  (0 <= i <= j < L). Walk each from the cursor. Emit satisfiable
  sub-sequences as variants 5000+i*10+j.
- This adapts the contract [s->t] to [s'->t'] where [s',t'] is a sub-interval,
  without rebuilding. TRUNCATE covers prefixes only; SUBSEQ covers arbitrary
  contiguous blocks (the interface-adaptation case).

## Frozen kill bars

### B: cross-domain SUBSTITUTE
- KB1: XB-TREAT ans=304 (SUBSTITUTE fires, subst_gen >= 1).
- KB2: XB-NOADAPT (adapt_on=0 build) ans=-2.
- KB3: XB-FRESH (no training) ans=-2.
- KB4: XB-ABL (domain-A X killed) ans=-2.
- KB5: B-L1REG ans=107 (original L1 regression undisturbed).
- KB6: 3/3 runs byte-identical per binary; sha256 digests recorded.
- KB7: zero em/en dash bytes in deliverables (byte scan).

### C: interface SUBSEQ
- KC1: IC-TREAT ans=54 (SUBSEQ fires, subseq_gen >= 1).
- KC2: IC-NOADAPT (adapt_on=0 build) ans=-2.
- KC3: IC-FRESH (no training) ans=-2.
- KC4: IC-ABL (W killed) ans=-2.
- KC5: 3/3 runs byte-identical per binary; sha256 digests recorded.
- KC6: zero em/en dash bytes in deliverables (byte scan).

## Battery specification (exact)

Shared: 30 gap facts (5000+i, 60+(i%10), 6000+i) for i in 0..29.

### B arms (domain A = relation 1; domain B = relation 3)
- Train XA: (11,1,12),(12,1,13),(13,1,14); ev_query(11,71,14).
  MAP_XA relseq [1,1,1].
- Domain B facts: (301,3,302),(302,3,303),(303,3,304).
- XB-TREAT: query (301,70,304). Expect 304.
  Rationale: MAP_XA native walk fails (no r1 from 301); TRUNCATE finds
  nothing (first step fails); SUBSTITUTE 1->3 walks [3,3,3] to 304.
- XB-NOADAPT: same in adapt_on=0 build. Expect -2.
- XB-FRESH: no XA training, only B facts. Expect -2.
- XB-ABL: train XA then kill it (field-36). Expect -2.
- B-L1REG: train X/Y (relations 1,2) as in candidate A; Z facts
  (101,1,102),(102,1,103),(103,1,104),(104,2,105),(105,2,106),(106,2,107);
  query (101,70,107). Expect 107.

### C arms (interface: MAP contract [51->55], goal needs [52->54])
- Train W: (51,1,52),(52,1,53),(53,2,54),(54,2,55); ev_query(51,75,55).
  MAP_W relseq [1,1,2,2].
- IC-TREAT: query (52,70,54). Expect 54.
  Rationale: MAP_W native walk from 52 fails at step 2 (needs r1 at 53,
  has r2); TRUNCATE gives [1] -> 53 (insufficient); SUBSEQ [1..2]=[1,2]
  walks 52->53->54.
- IC-NOADAPT: same in adapt_on=0 build. Expect -2.
- IC-FRESH: no W training. Expect -2.
- IC-ABL: train W then kill it. Expect -2.

## Cost bounds

- SUBSTITUTE: at most (distinct failing relations) x (candidate relations
  from cursor) walks; battery expects <= 4 substitution walks per MAP.
- SUBSEQ: at most L*(L+1)/2 sub-sequence walks per MAP (L <= 7, so <= 28).
- ADAPT-STAT gains [16]=subst_gen, [20]=subseq_gen. Total satisfy calls per
  arm must stay < 500 (generous bound; candidate A used < 12).

## Implementation notes (frozen design)

- New patch `l2x_patch.zag`: copy of `l2_patch.zag` plus `adapt_subst`
  (global single-relation substitution on first-fail relation),
  `adapt_subseq` (contiguous sub-sequence walks), variant dispatch in
  `un_satisfy_v` for 4000+r and 5000+i*10+j, candidate emission in
  `un_candidates`, ADAPT-STAT [16]/[20].
- Driver `l2x_driver.zag` (B and C arms); NA driver `l2x_driver_na.zag`
  (NOADAPT arms only). Assembled `l2x_full.zag` = cc_base + l2x_patch +
  l2x_driver; `l2x_full_na.zag` = cc_base + l2x_patch_na + l2x_driver_na
  (l2x_patch_na differs by exactly the adapt_on line).
- Pinned compiler src/tools/toolchain/znc_linux_x86_64_abed8aa1 via
  $HOME/safebin. Pure Zag; shell only to invoke znc, run binaries, git.
- All pinned znc defect workarounds apply (output buffer + single
  _zag_raw_syscall, u8 cells with ig/is, no 7-deep nested ifs, capacity
  plan).
