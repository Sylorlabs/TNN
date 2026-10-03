# PREREG: Learner-Built Constraint Channel (formal_constraints)

Frozen before implementation. Any break requires fresh prereg, fresh
worlds, rerun. VOID is terminal. Kill bars below are exact.

## Worker

Formal Constraints Worker (fresh respawn). Parent queue #4: "Formal
constraints auto-applied (learned knowledge constrains generation
without manual wiring)."

## Question under test

C264 (xdomain_grammar) showed a generic clause registry
(domain-neutral ABI: field/xform/k/lo/hi) lets learned grammar
constrain composition (0/12 to 12/12). Its honest boundary: the
clause ABI is researcher-defined generic machinery, and the
COMPILATION from induced grammar G={D,lo,hi} to clauses
(div/mod by D) was researcher-written. The open question: can the
LEARNER build the constraint channel itself from experience, or is
the ABI plus faithful compilation always researcher-defined?

This worker tests exactly that. The learner receives only labeled
judgments (accept/reject examples, i.e. experience) and must
construct registry clauses via generic machinery. A
researcher-compiled faithful channel runs as the control.

## Design

### World

One codec world W16 (true divisor D0=16), literals {1,3,5,7}.
A 2-word sentence is well-formed iff it has exactly 2 words and each
word w decodes as (w/16, w%16) with 1<=q<=7 and 1<=r<=7.
Six fixed trial pools (no RNG), identical to xdomain_grammar:
(1,3,5,7), (1,1,7,7), (3,5,7,1), (5,5,5,5), (7,3,1,5), (1,7,3,5).

### Teaching: judgments as experience

The teacher provides 12 labeled judgments (learner-state facts).
With E(a,b)=16a+b:

Accepts (6):
[19,87] [119,17] [51,85] [23,113] [81,55] [117,49]
i.e. [E(1,3),E(5,7)], [E(7,7),E(1,1)], [E(3,3),E(5,5)],
[E(1,7),E(7,1)], [E(5,1),E(3,7)], [E(7,5),E(3,1)].

Rejects (6):
[19] (1 word), [19,87,51] (3 words),
[11,47] (wrong codec h=8: 8*1+3, 8*5+7),
[35,167] (wrong codec h=32: 32*1+3, 32*5+7),
[3,87] (component 0 below lo: 0*16+3),
[129,51] (component 8 above hi: 8*16+1).

The learner never sees D0, never induces a grammar G, never computes
a gcd. It sees only these judgments.

### Learner induction: generic Occam separation

Generic machinery only (no grammar concepts; K6 audit):

- Feature library (fixed, domain-neutral): identity, div-by-k,
  mod-by-k for k in {2,4,8,16,32}. Eleven features. The library
  includes k=16, so the faithful decode features ARE expressible;
  the learner is not forced into a shortcut by omission.
- For each field f in {0,1} and each feature p: accept range
  [mn,mx] over the 6 accepts.
- Search clause sets by increasing cardinality (1, then 2),
  lexicographic order on (field, feature). Take the first set whose
  conjunction rejects every length-2 reject (rejects of other
  lengths are handled by the registry's nfields check). Every clause
  accepts all accepts by construction.
- Write the winning set via reg_write into the learner registry.

Hand derivation (frozen prediction): field-0 accept values are
{19,119,51,23,81,117}; length-2 reject field-0 values are
{11,35,3,129}. Exhaustive check over all 22 single (field,feature)
clauses: the UNIQUE separator is (field=0, mod-32) with accept
range [17,23] (19%32=19, 119%32=23, 51%32=19, 23%32=23,
81%32=17, 117%32=21; rejects map to 11,3,3,1, all outside).
No other single clause separates (identity admits 35; div16 and
mod16 admit 35; div8 admits 35; div2/div4/div32 admit 35 or 11;
mod2/mod4/mod8 admit 11; field-1 cannot separate alone because 87
is an accept value). Predicted induced channel: exactly one
clause (0, mod, 32, 17, 23), nfields=2. Note this is a SHORTCUT:
16a mod 32 = 16 for odd a, so mod-32 happens to track the
judgments without implementing the decode structure.

### Arms (one composer, three conditions)

Composer: xdomain_grammar's grammar-blind composer verbatim
(78 candidates per trial: 1-word, 24 2-word, 1 3-word per codec
hypothesis h in {8,16,32}; blind rule minimize (nf,f0,f1,f2)).

- Arm N (no channel): blind pick over all 78. The judgments sit
  inert in learner state.
- Arm R (researcher-compiled): researcher writes the faithful
  clauses directly: (0,div,16,1,7), (0,mod,16,1,7),
  (1,div,16,1,7), (1,mod,16,1,7). No induction; this is the
  researcher-defined compilation, the control.
- Arm L (learner-built): blind pick over reg_check survivors using
  the learner-induced clause set.

### Fidelity probes

For Arm R and Arm L separately: all 78 candidates x 6 trials
(468 total), reg_check vs independent direct grammar check
(nf==2, each field decodes under true D=16 to components in
[1,7]). The direct check uses world truth as reference; it is
measurement only.

Hand-derived forecast for Arm L: disagreements exactly where the
clause rejects and the grammar accepts, i.e. h=32 2-word
candidates with both words' first literals in {1,3}
(clause: field0%32 = second literal, never in [17,23], always
rejects; grammar: 2*first-literal in [1,7] iff first literal in
{1,3}). Count per trial over the 6 index partitions: 4,4,4,0,4,4
= 20 disagreements. Forecast fidelity_L = 448/468. The kill bar
is the strict inequality (robust to hand-count slips); the exact
count is reported.

## Predicted outcomes (frozen)

- Induction writes exactly: nfields=2, one clause
  (field=0, xform=mod, k=32, lo=17, hi=23).
- Arm N: 0/6 well-formed (picks the 1-word h=8 candidate).
- Arm R: 6/6 well-formed; fidelity_R = 468/468.
- Arm L: 6/6 well-formed (survivors are exactly the h=16 2-word
  candidates, all well-formed; blind rule picks among them).
  fidelity_L < 468/468 (forecast 448/468).

## Kill bars (all must hold, else verdict fails)

- K1: 3/3 runs byte-identical (SHA-256 recorded per run).
- K2: Arm N well-formed = 0/6 (judgments demonstrably inert
  without a channel; replicates C264 K2).
- K3: Arm R well-formed = 6/6 AND fidelity_R = 468/468
  (researcher-compiled faithful channel replicates C264).
- K4: fidelity_L < 468/468 (learner-built channel does NOT
  faithfully implement the grammar).
- K5: Arm L well-formed = 6/6 (learner-built channel still
  constrains this composer; the shortcut is task-adequate).
- K6: no-wire audit passes: grep over the learner-induction
  source section for
  grammar|codec|decode|divisor|sentence|wellformed|pair|literal|D0
  returns zero matches. Only generic vocabulary
  (field, feature, div, mod, range, accept, reject, clause).
- K7: toolchain guard: safebin active, `which python3 python`
  empty, pure Zag, no forbidden executable invoked.

## Diagnosis rule (frozen)

- K2+K3 pass: C264 replicates (inert without channel; faithful
  researcher channel sufficient).
- K4 pass: the learner does NOT build a faithful channel from
  judgments alone. It builds a shortcut (mod-32) that tracks the
  teaching distribution without implementing the decode
  structure. Faithful constraint compilation still requires
  researcher knowledge of that structure.
- K5 pass: the shortcut is nevertheless task-adequate for this
  composer and pool (6/6). Learner-built channel content CAN
  constrain generation, but finite judgments underdetermine the
  constraint, and generic Occam separation picks the shortcut.
- If K4 fails (fidelity_L == 468/468): the learner DID build a
  faithful channel; the verdict flips to learner-can-build and
  the analysis is rewritten accordingly. No bar is moved.

## What this does NOT claim

- The registry ABI (field/xform/k/lo/hi, reg_write, reg_check)
  is researcher-defined generic machinery, reused from
  xdomain_grammar. The claim under test is about the channel
  CONTENT (which clauses), not the ABI.
- The judgments (accepts/rejects) are teacher-provided
  experience. The question is whether the learner constructs the
  constraint from them, not whether it invents the judgments.
- The Occam/minimal-separation inductive bias is
  researcher-chosen. The result characterizes THIS generic
  learner, not all possible learners.
- One world, six trials. No broad generality claim. The second
  domain application (registry beyond grammar) is explicitly
  deferred, not claimed here.

## Verdict on pass

FORMAL-CONSTRAINTS-COMPLETE, with the learner-built vs
researcher-defined analysis: channel content can be
learner-built and task-adequate (Arm L 6/6) but is unfaithful
to the grammar (fidelity_L < 468/468); faithful compilation
remains researcher-defined.
