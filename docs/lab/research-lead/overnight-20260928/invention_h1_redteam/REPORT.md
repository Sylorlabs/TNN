# REPORT.md -- Invention H1 Red-Team: adversarial attack on structural mutation from failure

Target: commit 96e9bdea3 (Invention Hypothesis 1: structural mutation from
failure). Claim under attack: on failure of all mechanisms, the mutate
stage extends the longest chain MAP by one cell using the
learner-available "too short" signal; plen-6 invented from plen-5;
open-ended iteration; honest L2 bound.

Method: five adversarial experiments (A1-A5). Each is a fresh Zag driver
(attack_aN.zag) compiled against the UNMODIFIED H1 sources (mu_core.zag +
mu_patch.zag + mu_shared.zag, extracted read-only from 96e9bdea3). The
attacks are adversarial WORLDS, not patches: zero changes to H1
machinery, zero modes/bridges/handlers, pure Zag.

Verdict scale: KILL (claim falsified on its own terms), BOUND (claim
holds but its scope/interpretation is narrowed), SURVIVE (attack fails,
claim stands as stated).

## A1: WRONG-PARENT (distractor longest chain) -- BOUND

Setup: distractor domain D trained to plen-5 via trial, then a D-domain
plen-6 problem solved by mutation (mutant D6, id 271, subject 931).
Target domain X trained to plen-5 only (X5, id 316, subject 121). Attack
query: X-domain chain of 6 values plus one continuing fact, expected one
past the chain end (needs a plen-6 parent; trial is bounded to plen<=5).

Result (3/3 byte-identical, sha256 d0c1fe7c...):
- MUT-STAT parent=271 plen 6 -> 7 zmap=523. The distractor is tried first
  (longest-plen-first) and its extension verifies.
- MUTANT id=523 plen=7 subj=501; MUTANT-DEP-PARENT id=271 plen=6
  subj=931. The promoted mutant's DEP provenance points CROSS-DOMAIN to
  the distractor, never to the domain-correct X5.
- Answer 507 correct (verification guarantees this).
- Control (no distractor): same query ans=-2. The distractor's LENGTH
  unlocked the solution; nothing else about the distractor mattered.

Bound established:
1. Parent selection is longest-first, domain-blind, and content-blind.
   In a multi-domain workspace the "parent" is whichever domain happens
   to hold the longest chain MAP: a length license, not a relevant
   structure donor.
2. Provenance contamination: the mutant's DEP->MAP edge claims
   derivation from the distractor. Source reading confirms the
   misrepresentation is structural: mu_extend_one never reads the
   parent's graph; it stages the QUERY SUBJECT's own gathered paths and
   uses only the parent's plen (rb_chain_plen). The parent contributes
   an integer; the DEP edge claims a derivation.
3. Not a KILL because the mechanism still answers correctly
   (verification against expected) and the H1 report already bounds
   itself to L2. The "extends the longest chain MAP" framing is what is
   bounded: it extends a subject-gathered path at the parent's length.

Note (verified during design): true preemption (distractor wins while the
correct parent would also verify) is impossible given rebind-first
ordering: any world where the shorter parent's one-cell extension
verifies contains a full-length path the longer MAP rebinds first. The
residual, demonstrated risk is (1)+(2).

## A2: DECOY-SIGNAL (adversarial "too short") -- BOUND

Setup: plen-5 parent; query world chain 301..305. Continuing facts past
the endpoint under decoy relation 99.
- A2a: (305,99,306) taught BEFORE (305,1,306). Result: the mutant's
  extension fact is id=51 rel=99 (decoy-licensed=1, answer-ok=1). The
  id-order scan tries the decoy first; first-verify-wins keeps it. The
  true chain fact is never tried.
- A2b: ONLY (305,99,306) continues past the endpoint. Result: mutation
  still extends and promotes (decoy-only-extends=1, answer-ok=1).

Bound established: the "too short" signal is relation-blind. The scan
`ng(W,n,0)==1 && ng(W,n,20)==vend && ng(W,n,24)!=-999` accepts ANY fact
with a matching from-value under ANY relation; the chain graphs check
values only, never relations (inherited from t2_gather/t2_asm_chain, but
the mutation stage is where it becomes invention-licensing). Adversarial
worlds can steer extensions through decoy relations, and the promoted
mutant's fact provenance will cite the decoy. 3/3 byte-identical
(sha256 dbbb3f7e...). Not a KILL: answers remain correct by verification.

## A3: NON-CHAIN domain -- BOUND (stage inert outside chain-family)

Setup: learner state holds ONLY a count MAP (trained: ans=3, P3 pass;
rb_chain_plen of its graph = -1). Then a plen-6 chain problem all other
mechanisms fail.

Result (3/3 byte-identical, sha256 7ce48086...):
- mu_best_plen = -1: non-chain MAPs are invisible to parent selection.
- MUT-STAT tried=0 rejected=0, ans=-2: the mutation stage never fires.

Bound established: mutate_try is chain-family-only and inert otherwise.
Combined with source reading (the single operator is extend-by-one; no
shrink, swap, relink, or branch operators exist), the "general pipeline
stage" framing is bounded to linear chain extension. This matches the
H1 report's own follow-up ("sealed test: a domain where the needed
extension is not +1 chain length"), now empirically confirmed.

## A4: EXPLOSION / OPEN-ENDEDNESS -- KILL (of the open-endedness claim)

Setup: one workspace, X5 parent, then 5 sequential queries where query i
needs exactly one more cell than query i-1 (subject 1000+100*i, chain of
5+i values, expected = last value). Rebind and trial fail every query by
construction.

Result (3/3 byte-identical, sha256 466a113d...):
- Q1 ans=1105 ok=1: MUT-STAT parent=45 plen 5 -> 6 zmap=178.
- Q2 ans=1206 ok=1: MUT-STAT parent=178 plen 6 -> 7 zmap=346.
- Q3 ans=-2, Q4 ans=-2, Q5 ans=-2. MUT-STAT tried=2 rejected=2 every
  time: only the SHORTER parents (plen 6, plen 5) are tried and rejected;
  the plen-7 parent is never staged.
- maps stalls at 3 (no mutant spam past the cap), but live nodes climb
  178 -> 346 -> 559 -> 777 -> 1001: every failing query leaks ~200 nodes
  (rejected trial/rebind candidate graphs are never freed). No brake on
  attempts; the workspace marches toward node exhaustion.
- X5 and M1 survive (no parent cannibalization in this window).

Root causes (both verified in the H1 source):
1. ACTIVE: t2_gather caps paths at 6 values (`if(len<6)`,
   mu_core.zag:449). A plen-7 parent can never stage (no plen-7 paths are
   ever gathered), so iteration STOPS at plen-7 mutants. The report's
   "reachable forms (plen 8, 9, ...) are unbounded while source stays
   fixed" is false as implemented: plen 8 is unreachable, and the
   116 -> 271 -> 549 chain cannot take a fourth step.
2. LATENT: mu_extend_one's extension buffers are ve=z_alloc(28) (7 i32
   slots) and fe=z_alloc(24) (6 slots) (mu_patch.zag:69), but the
   extension writes set32(ve,p*4,w) and set32(fe,(p-1)*4,n), needing
   (p+1)*4 and p*4 bytes. For parent plen p>=7 this is a 4-byte heap
   buffer overflow per buffer. Unreachable while the gather cap holds,
   but any "fix" that merely lifts the gather cap introduces heap
   corruption.

Verdict: KILL of the open-endedness claim (H-MUT-3's plen-7 result
stands, but its generalization to unbounded iteration is falsified).
Bound: iteration works exactly twice (5->6->7) then stops; the "brake"
is an accidental gather cap, not a policy, and failing queries still
leak nodes without limit.

## A5: SUF (parent content inert) -- BOUND (strong)

Setup: two workspaces, IDENTICAL query world (301..306, expected 306).
Arm A parent trained on values 121..125; arm B parent trained on values
921..925. Control arm C: plen-4 parent only.

Result (3/3 byte-identical, sha256 5aa4e84a...):
- Arm A mutant SEQ: 301 302 303 304 305 306. Arm B mutant SEQ: 301 302
  303 304 305 306. Byte-identical value sequences; neither parent's
  values (121..125 / 921..925) appear anywhere in the mutant.
- Both answers 306 (P1 answers-equal=1, P2 both-correct=1).
- Arm C (plen-4): ans=-2 (P3 plen4-fails=1).

Bound established: the parent's learned CONTENT is causally inert. Only
its plen is load-bearing (arm C proves plen matters). The "mutant" is
the researcher's world chain re-derived at parent-plen+1, verified
against researcher-supplied expected; the DEP edge to the parent
misrepresents a derivation that never reads the parent's structure.
This pressures the "structural mutation" framing harder than A1: it is
not that the wrong parent's structure is mutated; NO parent's structure
is ever mutated. The H1 report's SUF analysis ("which parent mutates
depends on the learner's history") is bounded: what depends on history
is an integer (the longest plen), not a structure.

## Overall verdict

INVENTION-H1-REDTEAM-COMPLETE.
Per-attack: A1 BOUND, A2 BOUND, A3 BOUND, A4 KILL (open-endedness claim
falsified; iteration bounded to plen<=7 mutants; latent heap OOB at
p>=7), A5 BOUND (strong).
No SURVIVE: all five attacks narrowed or falsified part of the claim.
The three preregistered hypotheses (H-MUT-1/2/3) are not falsified by
this battery; what is killed is the report's generalization beyond them
(unbounded open-ended iteration).

What survives of H1 after the battery: a general, deterministic,
ablation-causal pipeline stage that, on total mechanism failure,
length-licenses a one-cell extension of a subject-gathered path using
world continuations past the staged endpoint, verifies against the goal,
and promotes the result with (misleading) parent provenance. Open-ended
in LENGTH through iteration; blind to domain, relation, content, and
non-chain structure; unbraked under repeated failure.

Recommended follow-ups for any H1 promotion case:
1. Provenance honesty: the DEP->MAP edge should record "length-licensed
   by" rather than imply structural derivation, or the operator should
   actually use the parent's structure.
2. Parent selection by relevance (domain/subject overlap), not bare
   longest-first.
3. Relation-typed continuation check in the "too short" signal.
4. A brake/dedup policy for repeated failing queries (see A4).
5. Non-extend operators (shrink/swap/relink) or an explicit
   extend-only scope statement.
