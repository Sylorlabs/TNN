# Conditional Tax v2: Design (stability-gated license + license-cost tax)

Date: 2026-09-30. Worker: Conditional Tax Designer.
Status: DESIGN ONLY. No implementation. No code written or modified.
No runs executed. Zero Python at every stage.

## 0. Standing-rules name-check

1. Pure Zag only. This design is prose; no Python at any stage.
2. Byte checks via worker_snippets/check_no_dash.sh (shell only).
3. No em dashes in loop documentation. This document was written
   with hyphens only and shell-checked before commit.

## 1. Provenance and scope

Parent result: conditional-first build CONDITIONAL-FAIL
(commit c6f6d6787). Bars P1, P2, P3 pass: the v1 BAP combiner
proposes COND(D,Y4,Y5) in round 0, A2-REUSE reaches 64/64 with
HAS_D=1, phase-1 DROUND drops from 4 to 1. Bar P4(c) fails: FREC
instance 3 best true-correct is 32/64 on all five seeds, below the
frozen bar of 40/64. F-CASE did not fire. The failure is a real
behavioral regression on a frozen control, exactly what P4 exists
to catch.

This document designs the fix. It revises two things from v1
(design e7ca7d83a): the COND tax (now license-costed by tier) and
the combiner license (now stability-gated). Everything not named
here stays as in v1: COND as op 4 with the generic 3-input
multiplexer semantics, 32-byte node layout with c2 at offset 28,
24-byte trace records, uniform 200/opc tax rate, score formula
10000*acc - 200*opc, top-32 selection, 24 rounds, IV machinery,
phase structure, has_d_subexpr walking c2, TAU=1.0 exact slice
agreement, deterministic enumeration, F-CASE framework.

What this design is: a bounded-L2 search-architecture revision
specification. A future builder preregisters from this document,
implements it in pure Zag, and runs the frozen R3, R1, and FREC
batteries.

What this design is not: it is not an L3 claim and attaches no
Criterion 0 claim. COND remains researcher-supplied, exactly like
AND, OR, XOR, NOT. The novelty claim is limited to: a
stability-gated license plus a license-cost tax repairs the
measured evidence-overfitting regression on FREC I3 while
preserving the R3 Arm 2 compositional repair.

## 2. Overfitting mechanism (precise diagnosis)

The v1 combiner licenses COND(c,A,B) when A agrees with the
target on every observed c=1 row and B agrees on every observed
c=0 row (TAU=1.0 exact), for every beam member c (32 conditions),
every (A,B) pair in beam order, up to 256 proposals per round.

On FREC I3 (fam 9, 32 passive evidence rows growing through IV
rounds), the failure unfolds in five steps:

1. Error-correcting partitions. The condition set (32 beam
   members, mostly round-built nodes) is rich enough that for a
   partially-correct pair (A,B), some condition c partitions the
   rows to separate A's errors from B's errors. The license is
   then satisfied by construction: c is selected implicitly by
   enumeration as an error-corrector, not as a structural
   variable. With 32 conditions and 32x32 (A,B) pairs per
   condition, spurious licenses are plentiful on 32 rows.

2. Score dominance. Each licensed COND has high evidence fit by
   construction at low opc (1 + child opcs under v1). Under score
   = 10000*acc - 200*opc, a perfect-fit COND at opc 1 scores 9800,
   while a binary candidate with genuine partial structure at
   24/32 and opc 3 scores 6900. The COND wins by 2900 points.

3. Beam crowding. Up to 256 CONDs per round flood the candidate
   pool. The top-32 selection fills with CONDs, displacing the
   binary candidates that were accumulating real (if partial)
   structure.

4. Churn. As IVs add rows, yesterday's error-correcting partition
   stops fitting (it encoded noise, not structure). Old CONDs
   degrade; new spurious triples are licensed on the new
   evidence. The beam never settles.

5. Collapse. Measured: all five I3 seeds converge to 32/64 true
   accuracy (chance), versus 40/64 frozen. The beam's final best
   nodes show ev_correct only 21-24/32: the churn regime never
   converges, so the beam ends worse on evidence fit too.

Structural contrast with R3 (why v1 worked there): on R3 phase 2,
the licensing condition D is a persistent library term from
phase-1 discovery, present in the beam every round. The slices
are 32/32 on 64 rows. The triple (D,Y4,Y5) is re-licensed every
round (stable). D is a genuine structural variable (the
F-PARCOND target), not an error-separator. So: stable condition,
large slices, persistent triple gives a genuine license; transient
condition, small slices, churning triple gives a spurious one.
The v1 license could not tell these apart. The v2 license can.

## 3. Change T1: license-cost tax (the stronger COND tax)

v1 rule: COND opc = 1 + opc(c) + opc(A) + opc(B), uniform base 1.

v2 rule: COND opc = B + opc(c) + opc(A) + opc(B), where the base
B depends on the condition's provenance tier:
- Tier 1 (c is a terminal or a library term): B = 2.
- Tier 2 (c is a round-built node): B = 4.

The 200/opc tax rate is unchanged. There is no COND-specific
rate; the differentiation is in the base, which is a structural
property (provenance tier), never a target property.

Rationale: the base prices the multiplexer plus the license. A
Tier-2 license draws on a larger, noisier hypothesis space (up to
32 built conditions with combinatorial (A,B) pairing and no
stability), so it carries a higher selection cost. This is the
"stronger COND tax" the parent asked for: the tax now reflects
the license's degrees of freedom instead of treating every
license as equally cheap.

R3 preservation check: COND(D,Y4,Y5) has D as a library term,
so Tier 1, B=2. opc = 2 + 0 + 0 + 0 = 2. Tax = 400. At 64/64 the
score is 10000 - 400 = 9600. The 4-op tree expansion scores
10000 - 800 = 9200. A 3-op full-fit overfitter scores
10000 - 600 = 9400. The COND still wins, by 200 over the
overfitter. The honest tax argument from v1 is preserved: the
conditional form remains the most compact correct hypothesis,
now with the license cost made explicit.

## 4. Change T2: stability-gated license (evidence-fit regularization)

The combiner's condition set is split into two tiers by node
provenance (a structural property, checked by the F-CASE tier
audit in section 8):

Tier 1: c is a terminal or a library term. These are stable by
construction (present in the beam every round).
- License: exact slice agreement at TAU=1.0, with minimum slice
  size 4: rows(c,1) >= 4 and rows(c,0) >= 4.
- No persistence requirement.
- Cap: 64 proposals per round. Enumerated first.

Tier 2: c is a round-built node.
- License: exact slice agreement at TAU=1.0, with minimum slice
  size max(4, en/8) where en is the current evidence row count.
- Persistence requirement: c, A, and B must all have been present
  in the previous round's beam. (A triple licensed in round r
  must have all three members in beam r-1.)
- Cap: 64 proposals per round. Enumerated after Tier 1.

Total cap: 128 proposals per round (down from 256).

Rationale: this is evidence-fit regularization. We trust a
partition only if its condition is a stable natural variable
(Tier 1) or if the full triple has survived one round of
evidence (Tier 2 persistence). Transient error-correcting
partitions are filtered because they are not re-licensed: as
evidence grows, the specific (c,A,B) that separated yesterday's
errors will not separate today's. Genuine structural partitions
(D on R3) are re-licensed every round and pass through.

Why this repairs I3 (prediction): on FREC, Tier-1 conditions
are the ~8 terminals (no library terms; use_lib != 1). Single-bit
partitions over 32 rows, a 4x smaller hypothesis space than v1's
32 conditions, and terminals are natural variables rather than
error-separators. Tier-2 conditions (the dangerous set) must
persist across rounds, which spurious triples rarely do. The
higher Tier-2 base (B=4, tax 800 before children) further damps
their beam dominance when licensed. Net effect: beam crowding
drops, binary candidates retain beam share, I3 recovers toward
the frozen 40/64.

Honest uncertainty, disclosed: this is a principled mitigation,
not a proven fix. If Tier-1 terminals alone suffice to generate
spurious licenses on 32-row evidence, v2 will fail P4(c) the same
way v1 did, and the diagnosis must be revised (terminals are
enough for error-separation on small evidence). If the
persistence gate is too strict, genuine Tier-2 discoveries will
be blocked (visible as P2'/P3' failing while P4' passes). The
frozen P4(c) bar is the falsifier either way.

## 5. What does not change

TAU=1.0. The generic multiplexer semantics computed from child
truth tables. Canonicalization via sig_lookup. The 32-byte node
layout and 24-byte trace records. has_d_subexpr walking c2.
The scoring formula and top-32 selection. The 200/opc rate. Round
count, IV selection, phase structure. The CONDHIT measurement
machinery (hitbuf) used for P1, carried over so the builder can
freeze P1' against it. The six v1 F-CASE audits.

## 6. Falsifiable predictions for the builder's prereg

- P1': COND(D,Y4,Y5) is proposed within at most 2 combiner rounds
  of D entering the phase-2 beam (Tier-1 fast path; D is a
  library term).
- P2': A2-PASS == 1 (A2-REUSE 64/64 with HAS_D=1; the frozen
  A2 bar).
- P3': phase-1 DROUND < 4 (frozen baseline 4; v1 achieved 1 via
  COND(X1,XOR,AND) through the Tier-1 terminal X1).
- P4': no regression on frozen controls: A1-PASS == 1;
  R1 PASS_SEEDS >= 0/5; FREC I1 >= 46/64, I2 >= 63/64,
  I3 >= 40/64.
- P5' (diagnostic, not a bar): the builder reports the
  per-round fraction of beam members that are COND nodes on
  FREC I3, as a crowding diagnostic for the parent.

Verdict rule: CONDITIONAL-TAX-PASS only if P1' through P4' all
hold and no F-CASE audit fires. Otherwise
CONDITIONAL-TAX-FAIL, with the failing bar named. Partial passes
are diagnostics, never a pass.

## 7. Worked preservation check on R3 (why P1'-P3' hold)

Phase 2, round 0: beam holds terminals Y1..Y6 and the D library
term. Tier-1 enumeration reaches c=D (library term, stable).
slice_acc(Y4,D,1)=1.0 over 32 rows, slice_acc(Y5,D,0)=1.0 over
32 rows; min-slice 4 satisfied. COND(D,Y4,Y5) proposed in the
first Tier-1 pass. opc=2, score 9600, enters beam, A2-REUSE
64/64 HAS_D=1. P1' and P2' hold exactly as in v1.

Phase 1: D = COND(X1, XOR(X2,X3), AND(X2,X3)). X1 is a terminal,
Tier 1. slice_acc(XOR,X1,1)=1.0, slice_acc(AND,X1,0)=1.0 once
the binary moves build the branch terms. DROUND stays well
under 4. P3' holds.

## 8. F-CASE provisions (v1 six audits plus two new)

F-CASE fires if any of the following holds:

1. String audit: new mechanism sources contain any of Y4, Y5,
   y4, y5, 710202, fam8, F-PARCOND, or "710101" through "710299",
   in code or comments. (Frozen commit hashes may be cited;
   target names may not.)
2. Gate audit: any proposal, scoring, or selection rule branches
   on a terminal index constant (in particular 3, 4, 5) or on
   node identity. Terminal indices appear only inside generic
   loops over the terminal range or over the beam.
3. Enumeration audit: Tier-1 enumerates all terminals and library
   terms in beam order with no skip and no identity filter;
   Tier-2 enumerates all round-built beam members in beam order
   with no skip and no identity filter. TAU applies uniformly.
4. Semantics audit: the COND evaluator implements (c AND a) OR
   ((NOT c) AND b) from child truth tables, with no branch on
   child identity.
5. Tax-rate audit: the rate is unchanged at 200 per opc. No
   COND-specific rate.
6. Generality requirement: the builder's prereg includes the
   frozen R3 battery plus at least one further compositional
   target (the frozen F-PARCOND phase-1 measurement via P3', or
   a new adversary-sealed conditional family). A mechanism
   passing R3 Arm 2 but failing every other compositional target
   is recorded as a one-target trick.
7. Tier audit (new): the Tier-1/Tier-2 classification branches
   only on node provenance (terminal vs library term vs
   round-built), never on node identity, terminal index, family,
   or target literals. Provenance is structural.
8. Tax-base audit (new): COND base B=2 for Tier 1 and B=4 for
   Tier 2, uniform 200/opc, no other base or rate adjustments.
   The differentiation is by provenance tier only.

## 9. Honest scope

- Bounded-L2 search-architecture experiment only. No L3 claim,
  no Criterion 0 claim.
- COND remains researcher-supplied. The novelty claim is
  limited to: a stability-gated license plus a license-cost tax
  repairs the measured evidence-overfitting regression while
  preserving the compositional repair.
- The mechanism does not invent conditionals, does not choose
  its own representation, and does not revise its alphabet. Any
  claim beyond bounded L2 goes through the full eleven-step
  pipeline with an independent red team.
- Residual risks, disclosed: (a) Tier-1 terminals may suffice
  for spurious licenses on 32-row evidence; (b) the persistence
  gate may block genuine Tier-2 discoveries; (c) the B=4 Tier-2
  base may prove too weak or too strong in practice. Each is
  measurable under the frozen bars; none is adjusted post-hoc.

## 10. Kill bars

- K1 (design complete): PASS. This document specifies the
  tiered tax base, the stability-gated license, the caps, the
  worked preservation checks, the falsifiable predictions, the
  F-CASE provisions, and the honest scope.
- K2 (addresses overfitting): PASS. T1 prices the license by
  its degrees of freedom; T2 regularizes which evidence fits
  are trusted, gating exactly the transient
  error-correcting-partition mechanism diagnosed in section 2.
- K3 (no implementation): PASS. Prose only. No .zag written or
  modified, no binaries built, no runs executed.

CONDITIONAL-TAX-DESIGN-COMPLETE.
