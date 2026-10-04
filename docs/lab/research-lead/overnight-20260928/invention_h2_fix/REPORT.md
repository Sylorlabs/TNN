# REPORT.md -- Invention H2 Overflow Fix

## Verdict: INVENTION-H2-FIX-COMPLETE

A4 re-run verdict: the fixed frag binary SOLVES the A4 goal
(`RECOMB-FRAGS n=3 (m=45,s=0,l=4) (m=68,s=0,l=4) (m=91,s=0,l=4)`,
`Z ans=43`), the identical solution the whole-MAP control binary finds.
The A4 KILL is addressed: the subsumption claim ("fragment recombination
strictly generalizes whole-MAP chaining") is operationally true again, no
process death, no heap corruption. A1/A2/A3/A4c/A5 re-verdicts below; no
kill bar was moved. A1 remains BOUND and is documented OPEN (verifier
limitation, not patched).

## What was broken

The red-team (commit f870c5930) found A4 KILL: on a 12-link r1 chain with
four duplicate `[1,1,1,1]` MAPs, the frag binary died with
`panic: slice index out of bounds` (exit 1, 3/3 deterministic).
Root cause: `ir_frag_dfs` allocated the candidate buffer as
`z_alloc(1296)` = 108 fragment entries, but level L of the DFS writes at
entry base L*48, so level 2 (the advertised "max 3" depth) writes entries
96..143: a 432-byte heap overflow once level 2 yields 13 or more
candidates (the A4 fixture yields 38). The overflow corrupted the DFS's
own `ncand`/`candi`/`curval` state, the search read out-of-bounds
triples, and the process died with no RECOMB-FAIL and no fallback.

## The fix: a derived bound, not a bigger constant

Changed file: `h2f_patch.zag` only (the fragment-recombination patch).
`h2f_base.zag` and `h2f_driver.zag` are byte-identical copies of the
red-team's frozen inputs. The diff is 16 added lines (one comment block
plus two constant functions) and 10 mechanically changed lines; the
search order, the per-level cap value (48), and the depth value (3) are
unchanged, so search semantics are identical and only memory safety
changes.

New single-sourced constants:

```
fn frag_cand_max()i32 { return 48; }
fn frag_depth_max()i32 { return 3; }
```

All DFS sizing derives from them:

* `ir_frag_candidates`: the three enumeration loop guards `n<48` become
  `n<frag_cand_max()`.
* `ir_frag_dfs`: `cand` becomes
  `z_alloc(frag_depth_max()*frag_cand_max()*12)` = 3*48*12 = 1728 bytes;
  `ncand`/`candi`/`curval` become `z_alloc(frag_depth_max()*4)` (one i32
  per level); read indices become `(L*frag_cand_max()+ci)*3`; the level
  base becomes `(L+1)*frag_cand_max()`; the depth check `L+1>2` becomes
  `L+1>=frag_depth_max()`.

### General bound proof

Let B = frag_cand_max() and D = frag_depth_max(). Each candidate entry
is 3 i32s (map_id, start, flen).

Lemma 1 (per-level cap): `ir_frag_candidates` returns n <= B. Proof: n
starts at 0, is incremented only at the single write site, and every
enumeration loop (flen, map_id, start) guards `n<B`. The write at index
base+n therefore uses entry indices base .. base+B-1 at most.

Lemma 2 (depth cap): candidates are generated only for levels
L in [0, D). Proof: the DFS starts at L=0 and descends from L only when
`L+1 < frag_depth_max()`; otherwise it advances the current level's
candidate index (backtrack/advance path).

Lemma 3 (disjoint regions): level L writes entries
[L*B, L*B + n_L) with n_L <= B by Lemma 1, so all writes across the
whole search land in [0, D*B), pairwise disjoint per level.

Theorem: a buffer of D*B entries (D*B*12 = 1728 bytes) is sufficient for
every possible execution. The DFS read index L*B + ci satisfies
ci < n_L <= B and L < D, hence L*B + ci < D*B: every read is in bounds.
The ncand/candi/curval buffers hold one i32 per level, indexed at L < D:
`z_alloc(D*4)` is exact.

Corollary (future-proofing): B and D are defined once. Raising the
branching cap or the depth updates the buffer, the write regions, the
read indices, and the depth check together; the overflow cannot
reappear as a stale constant. This is the sense in which the bound is
general: capacity = depth * branching, derived from the DFS structure,
not sized to the A4 fixture (whose 38 level-2 candidates are well under
the 48 cap; see the stress test for the cap itself).

Note: the result buffers in `recombine_try` (ofrag 36 B, ovals 96 B,
ofids 84 B, olen 12 B) are sized for exactly D=3 fragments with max
fragment length 7 (the pre-existing `ir_relseq` maxn=7 bound). They are
consistent with the frozen D=3 and were left untouched to keep the diff
surgical; if D is ever raised they need the same one-constant treatment.
Flagged as a follow-up, not a defect today.

## Re-run results (fixed binaries, full red-team battery, 3x byte-identical)

`h2f_bin` (frag_on=1): 3/3 byte-identical
(SHA-256 63bff44157c500a02b5feec4f34340880adcaf2bc9cd6bc16debc492894c4a21),
exit 0 on all runs (previously exit 1, deterministic panic).
`h2f_nc_bin` (frag_on=0): 3/3 byte-identical
(SHA-256 c0c7b619d8a35d4a4c154091d8b3ea027df1312233b610c4f2db12ca797d70f2),
exit 0.

Per-arm verdicts against the fixed frag binary (bars unchanged from the
red-team):

* A1 SPURIOUS: still BOUND. Transcript identical to the red-team's,
  including `RECOMB-FRAGS n=1 (m=91,s=0,l=3)`, `Z ans=37`,
  `MAP 166 relseq=[1,1,2]`, `LINK14 166 -> 91`. The verifier was
  deliberately not touched (see "A1 status" below).
* A2 DUP-ABL: still BOUND. `RECOMB-FRAGS n=2 (m=91,s=0,l=3) (m=68,s=0,l=3)`,
  `Z ans=37`, `MAP 187 relseq=[1,1,1,2,2,2]`. Identical to red-team.
* A3 SINGLE: still BOUND (unchanged behavior). Z via
  `(m=45,s=0,l=3)+(m=68,s=0,l=3)` then Z2 via the whole-MAP fragment
  `(m=165,s=0,l=6)`; `Z ans=37`, `Z2 ans=47`, `MAP 165`.
* A4c CONTROL: still BOUND. `RECOMB-FAIL`, `Z ans=-2`. Unchanged.
* A5 THREEFRAG: still SURVIVE. `RECOMB-FRAGS n=3
  (m=45,s=0,l=3) (m=68,s=0,l=3) (m=45,s=1,l=3)`, `Z ans=40`,
  `MAP 180 relseq=[]`. Identical to red-team, including the pre-existing
  7-link relseq extraction cap.
* A4 OVERFLOW: now SOLVES. `CANDCOUNT s=31 n0=40`, `RB-STAT tried=4
  rejected=4`, then `RECOMB-FRAGS n=3 (m=45,s=0,l=4) (m=68,s=0,l=4)
  (m=91,s=0,l=4)`, `Z ans=43`, `ZMAP id=245`. The fixed frag binary finds
  exactly the solution the nc binary finds (the nc run prints the same
  triple and `Z ans=43` with `ZMAP id=245`): whole MAPs as (m,0,len)
  fragments, i.e. Composition C behavior reproduced inside the fragment
  search, as the subsumption claim requires. No panic, no corruption.

Node ids (MAP 166, 187, 165, 180, 245) are unchanged from the red-team's
runs where comparable: `z_alloc` uses a separate malloc heap while
`alloc_node` uses workspace slots, so the larger candidate buffer does
not shift node numbering.

## Candidate-pressure stress test (beyond the fixture)

To validate the bound generally rather than for the A4 fixture alone,
`h2f_stress_bin` runs ten duplicate `[1,1,1,1]` MAPs against the same
12-link chain: 100 satisfiable level-0 fragments, so
`ir_frag_candidates` must truncate at the 48 cap at every DFS level
(probe prints `CANDCOUNT s=31 n0=48 cap=48`), exercising the full
D*B = 144-entry capacity with per-level regions at bases 0/48/96.
Result: 3/3 byte-identical
(SHA-256 76a95db1f296864ea75802bfcd176f17b72f9f91d89dc23c05a0238b19cbb6ad),
exit 0, `RECOMB-FRAGS n=3 (m=45,s=0,l=4) (m=68,s=0,l=4) (m=91,s=0,l=4)`,
`Z ans=43`. Under the old 108-entry buffer this fixture would have
written 36 entries past the allocation at level 2; with the derived
bound it completes cleanly. The truncation itself is pre-existing
intended search bounding (48^3 worst case), unchanged by this fix.

## A1 status: OPEN (documented, not patched)

The task allowed a minimal verifier fix "if cheap". Assessment: not
cheap in any principled form. `t2_try_verify` executes the assembled
graph from s and checks the final value against expected; the query
protocol `ev_query(W,s,r,expected,flags)` carries no goal-side relation
form to check against, and the spurious A1 chain ([1,1,2] via distractor
facts 31->38->39->37) is a true fact-store chain licensed by a genuine
sub-chain of a real MAP fragment that reaches the expected answer. No
verifier that sees only the assembled chain and the expected value can
distinguish it from a genuine recombination: the spuriousness is
semantic (which facts the walk used), and the walk's facts are exactly
what the search recorded. A real fix needs a goal-supplied form
constraint, which changes the shared query/verifier interface used by
rebind, trial, and recombine alike: broad, risky, and beyond a minimal
fix. Per the task instruction, A1 is documented as OPEN with this
reason rather than patched with a heuristic. The honest claim remains
the red-team's: "internally evaluated" is answer-checked, valid only in
distractor-free stores.

## Architecture accounting

* Cognition lines added: 16 comment/constant lines + 10 mechanical
  substitutions in the unfrozen patch; 0 to the frozen base, 0 to the
  driver.
* New modes: 0. New bridges: 0. New handlers: 0. New semantic cases: 0.
  No new opcodes; the protected-core ISA untouched.
* Search semantics (order, caps, depth) unchanged; memory safety only.
* One process-level robustness defect fixed (A4 heap overflow).

## Reproduction

All files under
`docs/lab/research-lead/overnight-20260928/invention_h2_fix/`:

* `h2f_base.zag` SHA-256
  dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
  (byte-identical to the red-team's `rt_base.zag` and the H2 base hash).
* `h2f_driver.zag` SHA-256
  41f8967a6f77f9b9cfe99cbfbcd5d5451102bead1a0ba02c287d0c3f83dc34a8
  (byte-identical to the red-team's `rt_driver.zag`).
* `h2f_patch.zag` SHA-256
  fe38482c187f0637930fcd29d57de5adb0da5ca479ada364bebef808fb7aac60
  (fix; frag_on=1).
* `h2f_patch_nc.zag` SHA-256
  e186e7c90a681ea8a4571296eace2803caa94f88c66c369e61b9a4ace3c43549
  (fix; frag_on=0; one-line diff vs `h2f_patch.zag`, mirroring the
  red-team's patch pair).
* `h2f_full.zag` SHA-256
  0a4233c55a7092654a003c520e21c58b77a161145014ad8cca7ac51881b63bda
  (`h2f_base` + `h2f_patch` + `h2f_driver` concatenated).
* `h2f_full_nc.zag` SHA-256
  e59385da80757132c722f080a523afcabf8df65026fd12f82654dcc5431dbcb0.
* `h2f_stress_full.zag` SHA-256
  e3b02ed2350e761bf7cdd349bcea65909b9d6023f5df414bd3fe1d266d7fa9af
  (`h2f_base` + `h2f_patch` + `h2f_stress_driver.zag`).
* Builds: pinned `znc` (`~/safebin/znc`), `znc h2f_full.zag -o h2f_bin`
  etc., warnings only (187 analyzer notes, same class as the red-team's
  build). `h2f_bin` SHA-256
  5d10371c1cd6bd1db6b8d50a0e72c3537307e27dd169fc6b9486421d0553fe11;
  `h2f_nc_bin` SHA-256
  9feed27446e02b44b329b6a92ea480ade28f63a5ce5a4d9ca4c82de6d5034c99;
  `h2f_stress_bin` SHA-256
  8e08417712e8242065d8118ec4d203aaecd5eb7e3b051303628622de90f5fc7a.
* Runs: `./h2f_bin > h2f_runN.txt` (3/3 byte-identical, exit 0),
  `./h2f_nc_bin > h2f_nc_runN.txt` (3/3 byte-identical, exit 0),
  `./h2f_stress_bin > h2f_stress_runN.txt` (3/3 byte-identical, exit 0).
  Pure Zag throughout; safebin toolchain guard Step 0 recorded in
  NAMECHECK.md (no python3/python in worker PATH; 42 allowed tools).
  Paper untouched. Nothing pushed.

## Open items

1. A1 verifier limitation (form-blind, answer-only): needs a
   goal-supplied form constraint; interface-level change, out of scope
   for this fix.
2. A2/A3/A4c bounds stand as the red-team documented them (duplicate
   fragment identity, whole-MAP reuse evidence, same-triple iteration
   ban): not defects, not changed.
3. If `frag_depth_max()` is ever raised, `recombine_try`'s result
   buffers (ofrag/ovals/ofids/olen) need the same one-constant
   derivation applied here to the candidate buffer.
