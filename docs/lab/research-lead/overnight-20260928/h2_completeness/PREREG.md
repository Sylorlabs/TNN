# PREREG.md -- H2 Completeness Repair: banded round-robin fragment enumeration

Status: FROZEN (committed before implementation; see git log).
Worker: H2 Completeness Repair Worker, 2026-10-02.
Lane: `docs/lab/research-lead/overnight-20260928/h2_completeness/`

## 1. Claim under repair

REDTEAM2-H2H3, attack H2-B1 TRUNC-LOSS: KILL. The repaired H2 fragment
recombination enumerates candidates per DFS level in (flen desc, map_id
asc, start asc) order and truncates at 48. In world B1 (8 decoy
[9,9,9,9] MAPs + 3 true [1,1] MAPs, 6-link r1 goal 31..37), at DFS
level 1 the decoys enumerate 8 (flen 4) + 16 (flen 3) + 24 (flen 2) =
48 fragments before the true (T,0,2) fragments at positions 49-50, so
the true fragments are dropped: RECOMB-FAIL. Teaching the trues first
flips the identical world to SOLVE. Solvability is a function of MAP id
order: order-dependent incompleteness, contradicting the patch header
"discovery is by constraint satisfaction only".

## 2. Repair design (frozen)

Replace the flat (flen, map_id, start) enumeration in
`ir_frag_candidates` with BANDED ROUND-ROBIN enumeration:

- Outer bands by decreasing fragment length (7..1), UNCHANGED: the
  fewer-fragments-preferred bias is preserved exactly.
- WITHIN each band, fragments are dealt round-robin across MAPs: round
  r hands every MAP (id ascending) its r-th satisfiable length-fl
  fragment (start ascending), until the 48 cap or until a full round
  yields no fragment.

What changes: a MAP enumerated early can no longer drain a whole band
before later MAPs are considered; within-band retention becomes
teach-order-fair.

What does NOT change: the 48 per-level cap (frag_cand_max), the depth-3
cap (frag_depth_max), the D*B candidate buffer layout, the per-level
write regions, the satisfiability test, the used-triple exclusion, the
DFS, the verifier, the query protocol. No new modes, bridges, handlers,
semantic cases, or opcodes. The protected-core ISA is untouched.

### 2a. Fair-share guarantee (the completeness claim)

Within one length band, let M be the number of MAPs with at least one
satisfiable length-fl fragment and R the cap remaining when the band
starts. Banded round-robin deals floor(R/M) complete rounds plus a
partial round to the lowest-id MAPs. Every MAP therefore retains at
least floor(R/M) of its length-fl fragments, and any MAP with at most
floor(R/M) satisfiable length-fl fragments is FULLY retained regardless
of teach order. For B1 level 1 (R=24 entering band fl=2, M=11):
floor(24/11)=2; the true MAPs have 1 flen-2 fragment each, so all true
fragments are retained in BOTH teach orders. The B1 pathology (an
entire MAP's fragments dropped while others keep dozens) cannot recur
within a band.

### 2b. Memory bound (D*B preserved)

Lemma 1 (per-level cap): `ir_frag_candidates` returns n <= B. n starts
at 0, is incremented only at the single write site, and every loop
(round, MAP, start) guards n < frag_cand_max(). The write at index
base+n uses entry indices base .. base+B-1 at most.

Lemma 2 (depth cap): unchanged; candidates are generated only for
levels L in [0, D).

Lemma 3 (disjoint regions): unchanged; level L writes
[L*B, (L+1)*B), pairwise disjoint.

Theorem: the D*B-entry buffer remains sufficient for every execution.
The round-robin restructure touches only WHICH satisfiable fragments
occupy the B slots, never how many.

### 2c. Residual limitation (honest, frozen)

Bands still drain in flen-desc order, so a band that alone fills the
48 cap still excludes all shorter bands. This preserves the intended
fewer-fragments bias (longer fragments are tried first by design), but
it is NOT full order-independence: e.g. 48+ satisfiable flen-7 decoy
fragments would still starve shorter true fragments. Fixing THAT would
require goal-derived relevance ranking, which is a redesign beyond this
repair (noted as follow-up, not claimed here). The within-band
teach-order unfairness that B1 killed is what this repair removes.

## 3. Test battery (frozen)

All binaries built with the pinned `~/safebin/znc`; each run 3x;
byte-identical outputs required.

- T1 B1a (decoys taught first): MUST SOLVE. Bar: `RECOMB-FRAGS n=3`
  with the true triple (T1,0,2)+(T2,0,2)+(T3,0,2), `B1 Z ans=37`.
  Driver: `h2c_b1_driver.zag` (byte-identical copy of redteam2's
  driver; B1a arm).
- T2 B1c (trues taught first): MUST still SOLVE, same bar
  (`B1 Z ans=37`). Teach order must no longer flip the verdict.
- T3 H2 fix battery A1/A2/A3/A4c: verdicts must remain BOUND.
  Driver: `h2c_driver.zag` (byte-identical copy of the fixer's
  driver). Expected transcripts: byte-identical to the fixer's
  `h2f_run*.txt` for these arms (the repair preserves the old order
  whenever no band overflows; verified by hand-trace in the design
  notes; any deviation is reported, not hidden).
- T4 H2 fix battery A5: verdict must remain SURVIVE (`Z ans=40`,
  three-fragment recombination).
- T5 H2 fix battery A4 (overflow arm): MUST still SOLVE (`Z ans=43`,
  no panic, exit 0); the D*B bound must hold under the new order.
- T6 100-fragment stress: MUST terminate cleanly, exit 0, 3/3
  byte-identical, `Z ans=43`. Driver: `h2c_stress_driver.zag`
  (byte-identical copy of the fixer's stress driver).
- T7 Determinism: every binary 3/3 byte-identical (sha256sum).

## 4. Acceptance / verdict rule

H2-COMPLETENESS-COMPLETE iff T1..T7 all pass as barred above, with no
kill bar moved, no cap raised, no new mode/bridge/handler/semantic
case, and the D*B bound proof updated for round-robin. Any T1/T2
failure (either teach order fails) = repair FAILED, back to design.
Any T3/T4/T5/T6 regression vs the fixer's frozen verdicts = repair
FAILED unless the deviation is a verdict-preserving transcript
difference documented in REPORT.md with the bar text unchanged.

## 5. Design notes (why banded, not global round-robin)

A global round-robin (one round hands every MAP its longest satisfiable
fragment, next round its second-longest, and so on) was considered and
REJECTED: it loses the global flen-desc priority (a MAP whose longest
satisfiable fragment is short outranks another MAP's longer fragment on
id order alone), changing A1's spurious arm from a 1-fragment to a
2-fragment solution and A3's Z2 reuse from a whole-MAP fragment to two
fragments. Banded round-robin keeps the global flen-desc bias (the
mechanism's stated preference) and only reorders WITHIN bands, so arms
whose bands never overflow keep byte-identical transcripts, and the B1
fix is exactly where the unfairness lived (within band fl=2).

## 6. Out of scope

- H2-B2 (order-form tie-break): BOUND, not a KILL; not addressed here.
- H2-B4 (depth-4): BOUND by design; not addressed here.
- Goal-derived relevance ranking: follow-up redesign, not this repair.
- The frozen base (`h2c_base.zag`), the frozen drivers, the paper:
  untouched.
