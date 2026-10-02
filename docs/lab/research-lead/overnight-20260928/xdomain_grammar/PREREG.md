# PREREG: Cross-Domain Grammar as Composition Constraint

## Worker

Cross-Domain Grammar to Construction Worker. Unfrozen variant only.
Frozen read-only: no frozen directory is read for code, only the
grammar_codec REPORT/PREREG as method reference (never modified).
This prereg is committed BEFORE any implementation (commit-order
self-check).

## Question under test

Micah's priority: GENERAL CROSS-DOMAIN COMPOSITION. The grammar line
induced grammars (divisor D plus literal ranges, grammar_codec). The
composition line composes fragments X+Y into Z. Untested: can a learned
grammar CONSTRAIN a composition? The parent-queue question: does learned
knowledge automatically constrain generation, or does it sit inert
unless manually wired?

This worker tests exactly that, with three possible diagnoses if the
naive composition ignores the grammar:

- representational: the induced grammar is not in a usable checkable
  form;
- architectural: no channel exists from grammar structures to the
  composer;
- control: the composer never queries constraints.

## Design

### X: induced grammar

The grammar is induced, not supplied, following the grammar_codec
method on the pair-codec world family: teacher teaches SUB (P,41,t),
DSUB (t,43,P), DIV-unit (P,42,1), DDIV-unit (1,44,P) facts for literal
pairs (a,b) encoded P = a*D+b. Induction: S = {P+t} over SUB/DSUB
facts union {P} over DIV/DDIV unit facts; g = gcd of positive S;
candidates d = v-1 for v|g, v>=2; op-consistency check per candidate
(41: decode (aa,bb), require aa-bb==t; 42 unit: bb>0, exact division,
aa/bb==t); unique consistent d is induced as D, else refuse. Literal
range [lo,hi] induced as min/max of decoded components over taught
pairs. The induced grammar is G = {D, lo, hi}: a sentence is
well-formed iff it has exactly 2 words and each word decodes under D
to (q,r) with lo<=q<=hi and lo<=r<=hi.

Two worlds: W16 (D=16) and W8 (D=8), literals {1,3,5,7}. Predicted
inductions: D=16/D=8, range [1,7] both worlds.

### The generic constraint channel (registry)

A shared learner-state table with a GENERIC, domain-neutral interface
(defined once as substrate machinery, not per grammar):

- clause = (field, xform, k, lo, hi); xform 0 = identity v=C[field],
  1 = div v=C[field]/k, 2 = mod v=C[field]-(C[field]/k)*k;
  clause passes iff lo<=v<=hi.
- reg_write(nfields, clauses): grammar induction compiles G into
  clauses: nfields=2, clauses (0,div,D,lo,hi), (0,mod,D,lo,hi),
  (1,div,D,lo,hi), (1,mod,D,lo,hi).
- reg_check(candidate vector, nf): 1 iff nf==nfields and every clause
  passes.

The grammar induction knows only the generic clause ABI. The composer
knows only reg_check. Neither side names the other, its fields, or its
concepts. This is the channel whose presence/absence is the experiment.

### Y: composition task

Given two source words as literal pairs F1=(a,b), F2=(c,d) (a trial
pool of 4 literals from the taught set), compose an encoded 2-word
sentence. The composer is deliberately grammar-blind:

- Candidate generation (composer machinery, fixed): for each codec
  hypothesis h in {8,16,32} (the composer's own fixed search set, NOT
  the learned D): one 1-word candidate [E_h(l0,l1)]; twenty-four 2-word
  candidates [E_h(w1),E_h(w2)] over the 6 index-partitions x 2 x 2
  within-word orders; one 3-word candidate
  [E_h(l0,l1),E_h(l2,l2),E_h(l3,l3)]. 78 candidates per trial.
- Blind selection rule (fixed, grammar-independent): minimize
  (nf, f0, f1, f2): fewest words first (simplicity prior), then lowest
  field values. Documented before results; any fixed grammar-blind
  rule would serve.

### Arms

- Arm N (no channel): pick by the blind rule over ALL 78 candidates.
  The induced grammar sits in learner state, compiled into the
  registry, but the composer never consults it.
- Arm C (channel): filter candidates through reg_check (generic), then
  apply the identical blind rule over survivors.

### Representational fidelity probe

For EVERY candidate in both arms, compare reg_check against an
independent direct grammar check (nf==2 and each field decodes under
the induced D to in-range components). Agreement rate measures whether
the grammar is in a usable form: 100% agreement rules OUT the
representational diagnosis.

### Trials

6 fixed trial pools per world (no RNG; fully deterministic):
(1,3,5,7), (1,1,7,7), (3,5,7,1), (5,5,5,5), (7,3,1,5), (1,7,3,5).
12 trials total (2 worlds x 6 pools), 2 arms each.

## Predicted outcomes (frozen bars)

- W16: XD-INDUCED D=16 lo=1 hi=7. W8: XD-INDUCED D=8 lo=1 hi=7.
- Arm N: blind rule picks the 1-word h=8 candidate every trial
  (fewest words wins): 0/12 well-formed. Learned knowledge inert.
- Arm C: all picks well-formed under the induced grammar: 12/12.
- Fidelity: 936/936 clause/direct agreements (78 candidates x 12
  trials).
- No-wire audit: composer section references no grammar concept
  (divisor, decode, range, grammar, codec); only reg_check and generic
  clause fields.

## Kill bars (all must hold, else verdict fails)

- K1: 3/3 runs byte-identical (SHA-256 recorded).
- K2: Arm N well-formed count = 0/12 (knowledge demonstrably inert
  without the channel).
- K3: Arm C well-formed count = 12/12 (generic channel suffices; no
  per-grammar wiring).
- K4: fidelity agreements = 936/936 (representational form adequate;
  rules out the representational diagnosis).
- K5: no-wire audit passes: `grep -n` over the composer section for
  divisor|decode|range|grammar|codec|pair returns only the generic
  reg_ interface lines (documented in REPORT).
- K6: toolchain guard: safebin active, `which python3 python` empty,
  pure Zag; no forbidden executable invoked.

## Diagnosis rule (frozen)

- K2 pass + K3 pass + K4 pass: learned knowledge does NOT
  automatically constrain generation; the gap is architectural/control
  (no channel / composer never queries), NOT representational. The
  generic registry channel closes it with zero per-grammar wiring.
- K4 fail: representational diagnosis instead (grammar not compilable
  to checkable form).
- K3 fail with K4 pass: control diagnosis refined (channel present
  but composer misuse), reported honestly.

## What this does NOT claim

- The clause ABI (field/div/mod/range) is researcher-defined generic
  machinery, like an ISA: the claim is that ONE generic channel
  suffices, not that the channel itself was learned.
- The composer is intentionally minimal and grammar-blind; no claim
  that it is a good composer, only that its picks are unshaped by the
  grammar in Arm N.
- Two codec worlds only; no broad generality claim.

## Verdict on pass

XDOMAIN-GRAMMAR-COMPLETE, with the constraint-channel diagnosis
(architectural/control gap, representational form adequate, generic
channel sufficient, zero per-grammar wiring).
