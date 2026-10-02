# REPORT: L2ADAPT lane, composition_l2 independent verification

Date: 2026-10-02. Lane: l2adapt, wave-20261002-1121pdt.
Worker: L2ADAPT lane worker (independent verification + extension).

## Candidate A: composition_l2 EXTEND/TRUNCATE/SPECIALIZE (frozen prereg c521249ba)

### Provenance

The frozen prereg (K1-K12) at commit c521249ba (2026-10-02 16:17:22 UTC) was
never modified after freezing (git diff since freeze is empty). A prior-wave
worker produced an implementation (commits 8974bbac4, 053a08c5e) claiming
12/12 kill bars. The coordinator brief flagged that the prereg never got a
clean implementation run. This lane performed a full independent clean-room
verification:

1. Extracted frozen sources from git (read-only): cc_base.zag (HEAD),
   l2_patch.zag + l2_patch_na.zag (053a08c5e), l2_driver.zag +
   l2_driver_na.zag (8974bbac4).
2. Verified the NA build differs by exactly one line (adapt_on 1 vs 0).
3. Reassembled l2_full.zag = cc_base + l2_patch + l2_driver; byte-matches the
   committed assembly. Same for the NA build.
4. Compiled with the pinned safebin znc (sha256
   498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
   matches pinned compiler; `which python3` resolves to nothing).
5. Ran each binary 3 times; checked all 12 kill bars against my own outputs.

Commit-order self-check: prereg file first committed c521249ba 16:17:22 UTC;
implementation files first committed 8974bbac4 17:09:32 UTC. Prereg strictly
precedes implementation. PASS. No bar was moved or reinterpreted.

### Results (my clean run, 2026-10-02)

- K1: L2-TREAT ans=108. PASS.
- K2: L1-TREAT ans=107 (no regression). PASS.
- K3: L2-ABL-X ans=-2, L2-ABL-Y ans=-2, L2-FRESH ans=-2. PASS.
- K4: L2-NOADAPT ans=-2. PASS.
- K5: TR-TREAT ans=107; TR-NOADAPT ans=-2; TR-FRESH ans=-2. PASS.
- K6: SP-TREAT ans=107; SP-NOADAPT ans=-2; SP-FRESH ans=-2. PASS.
- K7: L2-PROV link14-z-x=1 link14-z-y=1. PASS.
- K8: L2-REUSE ans=108. PASS.
- K9: L2-TREAT ext_gen=1 (>=1); L1-TREAT ext_gen=0. PASS.
- K10: L2-TREAT satisfy_calls=7 (<200). PASS.
- K11: 3/3 runs byte-identical per binary. PASS. Output digests match the
  prior report exactly (l2_bin runs 529e0e7d..., l2_na_bin runs aabe551d...),
  confirming behavioral reproduction from frozen source.
- K12: zero em/en dash bytes in deliverables (byte scan). PASS.

12/12 kill bars PASS on the independent clean run.

Note: my freshly built binaries have different sha256 than the committed
binaries (same sizes: 305820 / 292925 bytes) although built from byte-identical
source with the pinned compiler (my own rebuilds are byte-identical to each
other, so the toolchain is deterministic). The committed binaries were
therefore built in a different environment. This does not affect the verdict:
the kill bars constrain run outputs, and my run outputs match the reported
digests byte for byte. Flagged for provenance hygiene: future waves should
rebuild rather than trust committed binaries.

### Red team (adversarial review of the PASS)

1. Menu-selection attack (the mandated probe): EXTEND, TRUNCATE, SPECIALIZE
   are three researcher-authored operators with fixed semantics. The learner
   does not invent them; it triggers them on structural preconditions. This
   KILLS any L3 claim for this candidate and correctly narrows it to L2
   evidence (structural reuse from generic mechanisms). The prereg claims L2
   only, so the verdict stands as L2, not L3. No C0 clauses are asserted.
2. Knowledge-vs-architecture: the operators fire solely on learner-state
   preconditions (relseq satisfiability, continuation facts, observed
   ambiguity); the researcher never selects an operator per problem. The
   one-line adapt_on toggle is a clean causal control: NA build reproduces the
   old L2 failure on all three treat arms. No confound found.
3. Metric gaming: operators are structural and domain-general (walk
   extension, prefix truncation, ambiguity re-walk), not battery-shaped.
   Satisfy calls stay far under the K10 bound (max 11). No gaming found.
4. SPECIALIZE locality-prior limitation (recorded, not a kill): the
   nearest-object heuristic keys on numeric node-ID proximity, which is a
   representation artifact of the teaching order, not a domain label. It is a
   heuristic that can misfire under adversarial ID assignment. This bounds
   the generality claim for SPECIALIZE specifically; it does not fail any
   frozen bar.
5. Battery size: only three treat arms (one per operator). Generality beyond
   these arms is untested; cross-domain adaptation (candidate B) is the
   designed next probe.

### Verdict

Candidate A: VERIFIED PASS, 12/12 frozen kill bars on an independent clean
safebin run. Recommend ADOPTION as L2 adaptive-reuse evidence (NOT L3; the
operator set is researcher-authored, which the red team confirms narrows the
claim to L2). Provenance: prereg c521249ba intact and prior; implementation
source inherited from prior-wave worker commits 8974bbac4/053a08c5e, rebuilt
and rerun cleanly by this lane. Coordinator debate still required per wave
rules before canonical promotion.

## Next candidates (this lane, in progress)

- Candidate B: cross-domain L2 adaptation (SUBSTITUTE operator; structure
  learned in domain A adapted for domain B with partial mismatch). Prereg
  frozen (770a72afd), amendment 1 frozen (4fe6edc7b). Implementation
  complete (l2x_patch.zag). Battery BLOCKED: see below.
- Candidate C: ADAPT-REVISION interface adaptation (SUBSEQ operator; adapt a
  composite's input/output contract to a new goal without rebuilding).
  Prereg frozen (770a72afd), amendment 1 frozen (4fe6edc7b). Implementation
  complete (l2x_patch.zag). Battery BLOCKED: see below.

## Candidates B/C status: IMPLEMENTED, BATTERY BLOCKED

### What was built

l2x_patch.zag extends l2_patch.zag with two new operators (fixed set now 5):

- SUBSTITUTE (variant 4000+r): when native walk fails, find first failing
  relation r_fail, collect candidate relations r' from observed target facts
  at the failure cursor, substitute r_fail->r' globally, walk. Structural,
  data-driven, no researcher menu.
- SUBSEQ (variant 5000+i*10+j): when native walk fails, try all contiguous
  sub-sequences [i..j] of relseq (excluding full sequence and prefixes
  covered by TRUNCATE). Interface adaptation for sub-interval goals.

Both compile cleanly with the pinned safebin znc. L1REG (107) passes,
confirming no regression to base composition.

### Blocker: fallback confound in battery design

Probe experiments revealed the ev_query fallback (mp_run/trial) walks fact
chains up to 4 links without any MAP:
- 3 links: succeeds | 4 links: succeeds | 5+ links: fails (-2)

The original PREREG_BC battery used 3-link (B) and 2-link (C) targets.
Result: XB-FRESH and IC-ABL answered correctly via fallback, invalidating
KB3/KB4/KC4. Transparent amendment 1 (4fe6edc7b) lengthened batteries to
5+ links.

Remaining blocker: training a 5+ link MAP requires a 5+ link training query,
which the fallback cannot execute, so no MAP is promoted. Training via
composition+EXTEND was attempted but the (11,70,16) EXTEND query did not
promote the 5-link MAP (COMP-FAIL, ext=0). Root cause under investigation.

### Verdict

- Candidate B: NO VERDICT (battery blocked, cannot test hypothesis).
- Candidate C: NO VERDICT (battery blocked, cannot test hypothesis).

The operators are implemented and the prereg/amendment are frozen. The
battery engineering problem (training >4-link MAPs without fallback
support) is the sole blocker. This is an honest negative result on battery
design, not on the operators themselves.

### Next steps (queued)

1. Debug why (11,70,16) EXTEND query fails to promote 5-link MAP.
2. Alternative: direct MAP construction via workspace manipulation.
3. Alternative: redesign B/C to use 4-link MAPs with a different isolation
   mechanism (e.g., distractor facts that defeat fallback but not MAP).
4. Once battery works: run 3x, verify kill bars, red-team.
