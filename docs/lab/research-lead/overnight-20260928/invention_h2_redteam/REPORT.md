# REPORT.md -- Invention H2 Red Team (Fragment Recombination)

## Verdict: INVENTION-H2-REDTEAM-COMPLETE

Per-attack verdicts: A1 BOUND, A2 BOUND, A3 BOUND, A4 KILL, A4c BOUND
(finding), A5 SURVIVE.

The core recombination capability survives inside a narrowed envelope:
on distractor-free fact stores, with level-2 candidate counts below 13,
the mechanism does assemble proper sub-MAP fragments into novel forms
(A3 Z, A5). Three of the report's supporting claims do not survive as
stated: (1) the subsumption claim ("fragment recombination strictly
generalizes whole-MAP chaining; C is a special case") is operationally
false: there is a goal Composition C solves that fragment recombination
crashes on (A4 KILL). (2) The verification claim ("internally evaluated")
is answer-blind: a verifying-but-spurious fragment chain is accepted and
promoted as the novel form (A1 BOUND). (3) The ablation causality claim
("no alternative covers it") fails under duplicate fragments, and the
Z-prime reuse evidence is whole-MAP chaining, not fragment recombination
(A2, A3 BOUND). The honest L2 bound stands; the envelope around it is now
smaller and precisely measured.

## Battery design

Two binaries from the unmodified H2 mechanism (commit 31391237a):
`rt_bin` (frag_on=1) and `rt_nc_bin` (frag_on=0, one-line diff), each run
3x byte-identical. Six arms, each on a fresh workspace:

- A1 SPURIOUS: distractor facts (31,1,38),(38,1,39),(39,2,37) taught BEFORE
  the Z facts (first-match lookup prefers them), plus a distractor MAP
  D2=[1,1,2,9] (plen 5 values, so rebind cannot use it: the only gathered
  5-path from 31 walks to 35, not 37). The original (45,0,3) path is broken
  by the first-match reorder. Question: does the answer-only verifier
  accept the spurious (D2,0,3)=[1,1,2] fragment?
- A2 DUP-ABL: a duplicate [1,1,1,1] MAP trained on a fresh subject, then
  the report's exact ABL-X operation (delete the (11,61) MAP). Question:
  does Z still succeed, falsifying "no alternative covers it"?
- A3 SINGLE: replicate the report's Z then Z-prime on both binaries.
  Question: is the n=1 "reuse" fragment recombination or whole-MAP reuse?
- A5 THREEFRAG: 9-link goal (31..40, shape [1,1,1,2,2,2,1,1,1]) needing
  three PROPER fragments (report limitation 4: "3-fragment and deeper
  recombinations not tested"). Question: does it work?
- A4c CONTROL: 12-link r1 chain, ONE [1,1,1,1] MAP. Question: can one MAP
  be chained three times?
- A4 OVERFLOW: 12-link r1 chain, FOUR duplicate [1,1,1,1] MAPs. The nc
  binary must solve it with three distinct whole MAPs (n=3). Question: does
  the frag binary survive level 2 with 38+ candidates?

## A1 SPURIOUS: BOUND (strong)

Frag binary transcript:
```
RB-STAT tried=3 rejected=3
RECOMB-FRAGS n=1 (m=91,s=0,l=3)
Z ans=37
ZMAP id=166
MAP 166 relseq=[1,1,2]
ZFRAG nfrag=1 ... frag1 m=91 s=0 l=3
LINK14 166 -> 91
```
Rebind correctly rejected every MAP (tried=3 rejected=3). Fragment
recombination then accepted the single spurious fragment (91,0,3)=[1,1,2],
walked 31->38->39->37 via first-match distractor facts, verified the
ANSWER (37), and promoted MAP 166 with relseq [1,1,2] as the "novel"
recombined form, with provenance LINK14 166->91 pointing at the
distractor MAP. The report's headline 6-link form never appears.

Root causes, all in the mechanism as committed:
1. `t2_try_verify` checks `v==expected` only. It never inspects the
   relation sequence of the assembled chain, so any fragment chain that
   lands on the expected value verifies, however unrelated to the goal's
   structure.
2. `t2_lu_first` returns the FIRST matching fact (lowest node id), so
   teaching order (distractor facts first) silently re-routes all walks.
   The "invention" is determined by fact-store layout, not by the goal.
3. The DFS tries longer fragments first but accepts the first verifying
   chain; there is no form-level constraint at all.

On the nc binary, rebind also fails (tried=3 rejected=3), whole-MAP
recombination fails, and trial then finds the 3-link distractor path
(MAP 184 relseq=[1,1,2]). The spurious form is reachable by several
mechanisms; the point for H2 is that its "internal evaluation" cannot
tell a genuine recombination from a distractor chain. In any realistic
fact store (which contains distractors), the promoted "invention" is a
function of distractor layout and search order. The report's "internally
evaluated: YES" and "new form: YES" hold only in a distractor-free store.

## A2 DUP-ABL: BOUND

Frag binary transcript (after deleting the (11,61) MAP, maps 3->2):
```
RECOMB-FRAGS n=2 (m=91,s=0,l=3) (m=68,s=0,l=3)
Z ans=37
ZMAP id=187
MAP 187 relseq=[1,1,1,2,2,2]
LINK14 187 -> 91
LINK14 187 -> 68
```
The report's ABL-X operation (delete MAP 45) does NOT produce RECOMB-FAIL
when a duplicate-shape MAP exists: recombination silently substitutes
fragment (91,0,3) for (45,0,3) and succeeds with the identical 6-link form.

This falsifies the report's causal reading: "ABL-X: RECOMB-FAIL ... The
[1,1,1] fragment is causal; no alternative covers it." The causal unit is
the fragment SHAPE, which had a duplicate; the specific MAP triple is
interchangeable. Consequences:
1. The ablation as designed cannot distinguish "this fragment shape is
   necessary" from "this particular MAP was load-bearing in this history".
2. Provenance is search-order-relative: the white-box triple names
   (91,0,3) only because 91 is the lowest surviving map id among
   duplicates. Retrain in a different order and the "provenance" points
   elsewhere, for identical knowledge.
3. The `used` set excludes exact (m,start,len) triples only, so duplicate
   shapes are always eligible substitutes; the mechanism has no notion of
   fragment identity beyond the triple.

## A3 SINGLE: BOUND

Frag binary replicates the report exactly:
```
RECOMB-FRAGS n=2 (m=45,s=0,l=3) (m=68,s=0,l=3)   Z ans=37
RECOMB-FRAGS n=1 (m=165,s=0,l=6)                 Z2 ans=47
```
The Z-prime "reuse" uses ONE fragment, (165,0,6): the whole Z MAP. By the
report's own definition ("Composition C chains WHOLE MAPs"), this step IS
Composition C running inside the frag binary. The fragment-specific
machinery (proper sub-chain fragments) contributed nothing: no proper
fragment was used, and the candidate enumeration merely rediscovered a
whole MAP at strictly greater search cost than rebind (which was blocked
only by the unrelated t2_gather depth-5 cap noted in the report).

On the nc binary, Z fails (no MAP 165 is ever created) and Z-prime fails
with it (ans=-2), confirming the Z-prime result is downstream of the Z
recombination, not independent evidence for fragments.

The report's "Reusable: YES ... reuse occurred through the fragment
mechanism, not rebind_try" is technically true and substantively
misleading: the reuse evidence belongs to whole-MAP chaining (C), not to
fragment recombination. H2's reuse claim is unproven.

## A4 OVERFLOW: KILL (subsumption claim)

Identical goal on both binaries: 12-link r1 chain (31..43), four
duplicate [1,1,1,1] MAPs (ids 45, 68, 91, 114), query (31,63,43).

nc binary (Composition C behavior):
```
RECOMB-FRAGS n=3 (m=45,s=0,l=4) (m=68,s=0,l=4) (m=91,s=0,l=4)
Z ans=43
```
C solves it cleanly with three distinct whole MAPs.

Frag binary:
```
CANDCOUNT s=31 n0=40
RB-STAT tried=4 rejected=4
panic: slice index out of bounds
```
exit code 1, 3/3 byte-identical (the panic is deterministic).

Root cause, from the committed source: `ir_frag_dfs` allocates the
candidate buffer as `z_alloc(1296)` = 108 fragment entries. Level L of
the DFS writes at base L*48, so the third level (L=2, the advertised
"max 3" depth) writes entries 96..143, i.e. up to 432 bytes past the
allocation. With 38 satisfiable level-2 candidates here, the overflow
corrupts the DFS's own `ncand`/`candi`/`curval` state and heap, the search
reads out-of-bounds triples, and the runtime panics. The whole process
dies: no RECOMB-FAIL, no fallback to trial, no answer.

The report claims "fragment recombination strictly generalizes
whole-MAP chaining (when frag_on=1, whole MAPs are just (m,0,len)
fragments, so C is a special case)". As implemented, that subsumption is
operationally false: a goal C handles, fragment recombination crashes on.
The mechanism is memory-safe only while level-2 candidate generation
yields fewer than 13 candidates, a bound that appears nowhere in the
report and is unrelated to any cognitive criterion. The advertised
"max 3" search depth is not safe to use.

Note this also caps the combinatorics question (attack vector 1): the
search cannot even reach its 48^3 worst case, because the buffer
corruption truncates deep search first. The 48-per-level cap and depth-3
limit bound the search, but the binding constraint in practice is the
undersized buffer, i.e. bounded by accident, not by design.

## A4c CONTROL: BOUND (finding)

Both binaries: `CANDCOUNT s=31 n0=10`, then RECOMB-FAIL, Z ans=-2.

With a single [1,1,1,1] MAP and a 12-link chain, the goal is unreachable
for both binaries even though the knowledge suffices in principle
(three applications of the same MAP). Cause: the `used` set in
`ir_frag_candidates` excludes exact (m,start,len) triples already chosen,
so no triple may appear twice in one solution. The DFS can never chain
the same fragment twice.

This is an expressive bound on the DFS as implemented, shared by the nc
binary, i.e. by Composition C as the report operationalizes it: C cannot
apply the same whole MAP twice in one chain either (A4 succeeded only
because four distinct duplicate MAPs were available). Whether the ban is
intended, it rules out a natural class of solutions (iterated application
of one learned structure) and it interacted with A5: see below.

## A5 THREEFRAG: SURVIVE

Frag binary:
```
CANDCOUNT s=31 n0=9
RECOMB-FRAGS n=3 (m=45,s=0,l=3) (m=68,s=0,l=3) (m=45,s=1,l=3)
Z ans=40
```
A genuine three-proper-fragment recombination: (45,0,3)+(68,0,3)+(45,1,3)
solves the 9-link [1,1,1,2,2,2,1,1,1] goal, which the nc binary fails
(RECOMB-FAIL, ans=-2: no whole MAP is satisfiable). This closes the
report's limitation 4 (3-fragment recombinations untested) in the
positive direction, inside the narrowed envelope.

Two quirks worth recording:
1. The third fragment is (45,1,3), not (45,0,3): the exact triple
   (45,0,3) was excluded by the `used` set, but the same-shape fragment
   at a different start was allowed. Triple-exactness is a leaky notion
   of "already used": shape reuse is permitted, triple reuse is not.
2. `ir_relseq` caps extraction at 7 links (`maxn=7`, returns -1 beyond).
   The promoted 9-link MAP 180 therefore prints `relseq=[]` and, more
   importantly, can never contribute fragments to future recombinations:
   the mechanism cannot build on its own products longer than 7 links.
   (Pre-existing bound, not introduced by this red team.)

## What survives

- Fragment extraction plus constraint-satisfaction search does assemble
  proper sub-MAP fragments into novel forms the learner's history plus
  goal determine (A3 Z, A5). The honest L2 characterization stands.
- The whole-MAP-only control still fails exactly where the report says it
  does (A3 Z on nc: RECOMB-FAIL; A5 on nc: RECOMB-FAIL).
- 3/3 byte-identical determinism on both binaries, including the
  deterministic A4 panic.

## What does not survive as stated

1. Subsumption: "strictly generalizes whole-MAP chaining" is false as
   implemented (A4: C solves, fragments crash). KILL.
2. Verification: "internally evaluated" is answer-only and form-blind;
   the promoted form is distractor-determined (A1). BOUND to
   distractor-free stores.
3. Ablation causality: "no alternative covers it" fails under duplicate
   fragments; provenance is search-order-relative (A2). BOUND.
4. Reuse: the Z-prime evidence is whole-MAP chaining (C), not fragment
   recombination (A3). BOUND; H2 reuse unproven.
5. The `used` triple-exactness bans legitimate same-triple iteration
   (A4c) while permitting same-shape-different-start reuse (A5): the
   identity condition on fragments is incoherent. BOUND.

## Recommendations for the H2 owner

1. Fix the `cand` buffer (size for 3*48 entries) before any further
   claim about depth-3 search; re-run the A4 goal as a regression test.
   Until then, cap the advertised depth at 2 or gate on candidate counts.
2. Decide what a fragment's identity is: if (m,start,len) triples are the
   unit, the A5 (45,1,3)-after-(45,0,3) reuse needs justification; if
   shapes are the unit, the `used` set and the ablation logic need
   rewriting.
3. Either strengthen verification beyond answer-matching or downgrade
   "internally evaluated" to "answer-checked": the current verifier
   cannot distinguish invention from coincidence.
4. Re-run the ablation battery with duplicate-shape MAPs present; the
   current ablutions measure triple-load-bearing, not shape-necessity.
5. Prove H2 reuse with a case that requires a PROPER fragment on the
   reuse leg (Z-prime as run does not).

## Architecture accounting

- Cognition lines added: 0 to the mechanism (unmodified from 31391237a).
  Red-team driver: ~350 lines of test code (not mechanism).
- New modes: 0. New bridges: 0. New handlers: 0. New semantic cases: 0.
- One process-level robustness defect found (A4 heap overflow, panic).

## Reproduction

- `rt_base.zag`: SHA-256
  dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
  (matches the H2 worker's recorded base hash).
- `rt_patch.zag` / `rt_patch_nc.zag`: one-line diff (frag_on 1 vs 0).
- `rt_full.zag` (SHA-256
  68ec552e0f14212b50335304da0551a6d63b5133118f59f8ace2e93fbe4633b8)
  and `rt_full_nc.zag` (SHA-256
  bd92fc7ad79904267eae34237fa2e552bb4498bdef2575fc0e57a378a005df1c):
  assembled by concatenation.
- Builds: pinned `znc_linux_x86_64_abed8aa1`, `znc rt_full.zag -o rt_bin`
  and `znc rt_full_nc.zag -o rt_nc_bin` (warnings only).
  `rt_bin` SHA-256
  d3741af22d7b62eb0bfcc1c873b18b10b2f5d6574cdca81993bfb545948fa0e8;
  `rt_nc_bin` SHA-256
  6a3ab9aea2673194ba85b4483868df55e76b26600db2fee3f25d5fd55757eb82.
- Runs: `./rt_bin > rt_runN.txt` (3/3 byte-identical, exit 1, deterministic
  A4 panic last), `./rt_nc_bin > rt_nc_runN.txt` (3/3 byte-identical,
  exit 0). Pure Zag. Safebin toolchain guard Step 0 in NAMECHECK.md.
  Paper untouched. Nothing pushed.
