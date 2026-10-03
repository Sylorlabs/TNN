# CAUSAL-EDITADV Results: EDITINVENT-ADV-BREAKS (SCOPE-COLLAPSE)

Adversary: Causal Edit-Invention Adversary (C0-C attack).
Target: CAUSAL-EDITINVENT-PASS (prereg `811fc06c9`, impl `4c233f82a`).
Prereg (this task): `d71be66dc` (committed alone, strictly before impl).

## Verdict

**EDITINVENT-ADV-BREAKS (SCOPE-COLLAPSE)**

The diagnose-and-relax meta-procedure does not generalize beyond delay_max.
Its declared two-parameter scope {max_rules, delay_max} collapses: the
max_rules diagnostic arm provably never fires in any reachable trace, and
the ambiguous branch provably never fires. What was presented as generic
diagnose-and-relax is single-parameter delay diagnosis with vestigial arms.

CAUSAL-EDITINVENT-PASS (R3) is NOT retracted: its trace (delay binds,
invent dmax+1, resolve to [(X->Y,3)]) remains valid. Its ceiling narrows to
"learner-authored delay-domain extension in one law-change family; the
meta-procedure is provably delay-specific, not parameter-generic."

## Kill bars

- K1 (prereg precedes implementation): PASS. Prereg `d71be66dc` committed
  alone; implementation commits are descendants (verify:
  `git merge-base --is-ancestor d71be66dc <impl>`).
- K2 (3/3 byte-identical vs frozen mechanism): PASS. Three fresh znc
  compiles per driver; stdout sha256 identical across all 3 runs:
  A=f9ba4a02ebf7cc95a9d5c02902ed724d8af4a9bbb18880a7a2a205d07e6c96bd (x3),
  B=f17022204d6f4d792315dcffe288c67ba82b8065e6a2d4f3ad740066c3b222fc (x3),
  C=5a2ec5992d34eedd2dbe8b17c778ab2942540bed20a3d0dda62ecb257b65b012 (x3).
  `audit_frozen.sh` passes on all three drivers: the first 18641 bytes of
  each driver (the entire mechanism region) are byte-identical to the
  `4c233f82a` blob of `causal_editinvent/editinvent.zag`. Only the driver
  mains (evidence + call sequence + verdict prints) are new.
- K3 (verdict per frozen rules; pure Zag; dash-clean; paper untouched):
  PASS. Verdict ADV-BREAKS per prereg Section 5 (A1/A2/A3 all matched).
  Pure Zag plus shell; zero Python anywhere including /tmp scratch.
  `check_no_dash.sh` clean on all committed files. Contaminated paper
  untouched.

## Family A: SCOPE-COLLAPSE (the max_rules arm is dead)

Design pivot (prereg Section 3): the brief asked for "a law change where
max_rules binds". Pre-prereg exploration proved this family cannot be
constructed, so Family A became the impossibility proof.

Trace (RAW_A1.txt, sha256 f9ba4a02...):
- A1: old envelope: n=78 graphs, nsig=15 signatures (matches prereg F2).
- A2: 220/220 3-rule (delays<=2) graphs have signatures inside the old
  15-signature set; out_old=0. S_mr is a subset of S_old, verified
  computationally against the frozen semantics.
- A3: frozen `diagnose` on R3's E3: `max_rules->3: 0/220`, `delay->3: 13/171`,
  `binding=delay_max` (returns 2; the one live arm). Frozen `diagnose` on
  E_B: `max_rules->3: 0/220`, `delay->3: 0/171`, `binding=none_or_ambiguous`
  (returns 0).
- Corollary: any E consistent with a 3-rule graph is consistent with an
  old-envelope graph (signature-subset), so c_old=0 implies c_mr=0 for ALL
  E. Diagnose is reached only when c_old=0 (FAIL_OLD with 1-rule W0 covers
  the envelope within KMAX=3). Hence binding=1 is unreachable in every
  reachable trace, and the ambiguous branch (both bind with c_old=0) is
  unreachable too.
- `A-VERDICT SCOPE-COLLAPSE`.

What this reveals: the prereg's mental model was "two live parameters; R3
happens to bind delay_max; max_rules would honestly stop." Reality: the
max_rules arm is dead code, not a live alternative. The "generic"
meta-procedure never had a second parameter. Under min-arrival semantics a
3rd rule can only lower arrival times, so rule-count extension is
behaviorally redundant (prereg F1); the diagnosis scope was chosen over a
parameter that the semantics had already killed. The generality was never
tested because it could never be exercised.

## Family B: HONEST-STOP (no parameter binds)

E_B={(Y,6)=0,(Y,7)=1,(Z,7)=0} needs arrY=7, arrZ>=8: 3-hop chain territory
(4 variables), outside {max_rules, delay_max}. W0=[(X->Y,1)].

Trace (RAW_B1.txt, sha256 f1702220...), mirroring the frozen Phase-1
pipeline exactly:
- B1: V_old BFS k=-1 (old-vocabulary failure, the inline control).
- B2: `old-envelope EB-consistent count=0` (exhaustive proof).
- PATTERN: `required arrivals: Y in [7,7] Z in [8,INF]`.
- diagnose: `max_rules->3: 0/220`, `delay->3: 0/171`,
  `binding=none_or_ambiguous`, returns 0.
- B4: frozen branch prints `BINDING-NOT-CONSTRUCTIBLE` and stops. No
  invent, no resolve, no silent misresolution.
- `B-VERDICT HONEST-STOP`.

The mechanism operates honestly where it cannot construct: it reports
unconstructibility rather than misresolving. This is the boundary working
as designed. It does not rescue the generality claim (Family A), but it
confirms there is no dishonest failure mode hiding behind the dead arms.

## Family C: AMBIGUITY-HUNT (49-cell sweep)

Sweep over E(arrY,arrZ)={(Y,arrY-1)=0,(Y,arrY)=1,(Z,arrZ-1)=0}, arrY 1..7,
arrZ 2..8, using frozen prove_insufficient / diag_count_maxrules3 /
diag_count_delay3 and the verbatim frozen binding branch.

Trace (RAW_C1.txt, sha256 5a2ec599...):
- C1: violations(old=0 AND mr>0) = 0. In all 49 cells, c_mr>0 implies
  c_old>0. The ambiguity precondition never holds.
- C2: binding=1 cells = 0. The max_rules arm fires nowhere, not even where
  the old envelope still explains the evidence.
- C3: binding=2 in exactly 11 cells (the delay-only region:
  arrY=3/az=3..8, arrY=4/az=3, arrY=5..6/az=2..3); binding=0 in 38 cells.
- `C-VERDICT NO-AMBIGUITY`.

The frozen three-way branch reduces, in every reachable trace, to:
delay binds (invent) or nothing binds (honest stop). The other two
outcomes exist only in unreachable code paths.

## Honest ceiling

This attack breaks the GENERALITY claim, not the R3 result. Revised
ceiling for the editinvent line: "learner-authored delay-domain extension
in one law-change family; diagnose-and-relax is provably delay-specific,
not parameter-generic." For the L3-revision program, "revise your own
revision machinery" remains unproven in any general sense: the one
demonstrated self-revision traveled the only diagnostic path the machinery
could ever take. A genuine generality claim needs a scope whose parameters
are all live, or a second family where a different parameter binds; under
this semantics the max_rules parameter cannot be that family.

## ONE-SYSTEM accounting (this attack)

- Cognition source lines added: 0 (mechanism frozen; drivers are test code).
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
- New task-specific handlers: 0. Learner-state structures created: none.

## Files

- `PREREG.md`, `STEP0_NAMECHECK.md` (prereg `d71be66dc`)
- `attackA.zag`, `attackB.zag`, `attackC.zag` (drivers; mechanism region
  byte-identical to `4c233f82a`)
- `audit_frozen.sh` (shell-only frozen-region audit)
- `RAW_A1..3.txt`, `RAW_B1..3.txt`, `RAW_C1..3.txt` (3/3 byte-identical runs)
