# L3B-C0C adversary: result

Verdict: **L3B-C0C-BOUNDARY-EXPOSED**

The fixed analyzer vocabulary {EQ, MUL(q), ADD(d), SUB(d)} and the
static single-program growth form are the C0-C boundary of the L3B
residual-growth mechanism. The generic constructors did not compose
either unforeseen form. Both sealed families behaved exactly as the
frozen prereg predicted for the boundary case.

## Kill bars

- K1 PASS: prereg 14a92a69d committed alone before any attack file
  existed. `git merge-base --is-ancestor 14a92a69d <impl>` verified at
  commit time. Family spec FAMILIES.md committed after the prereg,
  before any attack source; sha256
  2b4a09ef0b3b31b24dcfe497d25ebfe38904637142c69501615dc61c1f9ca68b.
- K2 PASS: both sealed families executed 3/3 byte-identical
  (md5 4605896757f957c0b763a6923762c16d x3), per-family verdicts
  against frozen predictions P-A2a..d and P-B2a..d (all hold).
- K3 PASS: pure Zag, zero Python at every step; check_no_dash.sh clean
  on all lane files; protocol region of l3b_attack.zag (lines 1-438)
  byte-identical to committed l3b.zag at 2fb110ce7 (sha256
  0778efafd6499449949473d02787a13b3259101d459567230f6d70a7263527ba
  both sides; proof in DIFF_PROOF.txt); u8-backed cells only.

## Family A2 (QUAD): n-squared residual

Frozen predictions vs observed:

- P-A2a KX-A2 == 1: observed max=1. The 512 canonical singles are
  provably inadequate on the quadratic family (only (1,1,1) and
  (2,2,4) each hit one E_m).
- P-A2b TRACE-CREATE == 0: observed creates_v=0, active=0. The
  analyzer fired twice and abstained honestly:
  `NO-GROWTH inst=1 phase=LEARN ep=3` and `ep=6`. Run2 residual
  (n^2) yields NONE on every 3-failure window (MUL needs constant q;
  observed q would be 2,3,5 then 7,4,6).
- P-A2c HIDDEN-A2 == 0/3: observed hidden=0. bestL=(2,2,4) never fires
  on n in {1,4,8}.
- P-A2d N2-INTERP == 25: observed e=25. Hand-built MUL(VAR(F0),VAR(F0))
  with CREATE/CONNECT evaluates to 25 at f0=5.

Crux exhibit: the execution substrate (binterp_eval) evaluates n^2,
but the construction substrate (rel_of + build_expr) cannot detect or
assemble it. Open execution, closed construction.

A2 verdict: BOUNDARY-EXPOSED-A2.

## Family B2 (ALT): alternating law, revision churn

Frozen predictions vs observed:

- P-B2a creates == 3, retires == 2: observed create=3, retire=2.
- P-B2b v1=(EQ,MUL(2)), v2=(EQ,ADD(4)), v3=(EQ,MUL(2)), version=3:
  observed `C0C-B2 version=3 v1=1,0,2,2 v2rel2=3 v2k2=4 v2split=1
  v3=1,0,2,2`. v3's (rel,k) pair is content-identical to v1's.
- P-B2c hidden=3/3, switch=0/6, final=0/2: observed hidden=3,
  switchok=0, final=0.
- P-B2d v3 CALLS contain SPLIT( and no MERGE(: observed
  `CALLS: SPLIT(4)->8 CREATE(op=2,val=0)->9 CREATE(op=1,val=2)->10
  CREATE(op=4,val=0)->11 CONNECT(11,0,9) CONNECT(11,1,10)`.
  v3 SPLIT-reused run1 from v2 (the immediately retired growth) and
  rebuilt run2 from scratch: no version memory, v1's form rebuilt
  rather than recalled.

Churn signature: v1(R1) -> v2(R2) -> v3(R1), each exact only inside
its own block, ending wrong on FINAL-B2 (0/2). A grown program is one
static (root1,root2) pair per version; the mechanism cannot represent
"R1 on some episodes, R2 on others" and has no conditional dispatch
between versions.

B2 verdict: BOUNDARY-EXPOSED-B2.

## Overall

L3B-C0C-BOUNDARY-EXPOSED. Neither family showed growth composing the
unforeseen form (no OPEN-FORM on either family; no UNPREDICTED
outcomes).

Interpretation (frozen in prereg): the boundary is in the analyzer
vocabulary and the static single-program form, not in the interpreter
(A4 generality stands) and not in the C0-A answer (semantics still
live in the pre-existing binterp_eval). This does not retire the L3B
mechanism; it maps exactly where its open-endedness stops: it grows
base-language programs for single stationary arithmetic residuals
detectable by {EQ, MUL, ADD, SUB}, and nothing outside that envelope.

## Recommendation

The productive next step is a constructor-level redesign, not a
vocabulary patch: the forcing exhibits are (1) A2's closed
construction vs open execution gap (the analyzer must be able to
detect what the interpreter can evaluate, or growth must search the
program space rather than fit the vocabulary), and (2) B2's missing
conditional form (per-episode or per-regime dispatch between grown
programs, plus a version archive so revision is recall rather than
rebuild). Adding MUL(VAR,VAR) or a parity case to rel_of would repeat
the downgraded template-widening pattern; the prereg's anti-widening
note stands. If the lane continues, the next prereg should freeze
Families A2 and B2 as regression falsifiers for any v2 constructor.
