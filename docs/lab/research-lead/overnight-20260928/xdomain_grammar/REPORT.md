# REPORT: Cross-Domain Grammar as Composition Constraint

## Verdict: XDOMAIN-GRAMMAR-COMPLETE (constraint-channel diagnosis: architectural/control gap, representational form adequate)

## Claim tested

Parent-queue question: does learned knowledge automatically constrain
generation, or does it sit inert unless manually wired? X = an induced
grammar (divisor D plus literal range [lo,hi], induced per the
grammar_codec method from taught facts, never supplied). Y = a
grammar-blind composition mechanism (assemble an encoded 2-word
sentence from two source literal pairs, searching fixed encoding
hypotheses h in {8,16,32} x 24 partitions/orders plus degenerate
1-word and 3-word candidates; fixed fewest-fields-first pick rule).
Z = the composed sentence. Test: can the composition USE the grammar
as a constraint (rejecting ill-formed, preferring well-formed)
with ZERO per-grammar wiring of the grammar into the composer?

## Channel design (the thing under test)

A shared learner-state clause registry with a generic,
domain-neutral ABI: clause = (field, xform, k, lo, hi), xform in
{identity, div-by-k, mod-k}; reg_check passes iff the candidate has
exactly the registered field count and every clause passes. The
grammar induction compiles its learned rule into 4 clauses
(field 0/1, div/mod by D, range [lo,hi]); it knows only the clause
ABI. The composer calls only reg_check; it never reads the induced
rule. Neither side names the other. Arm N: blind pick over all 78
candidates (grammar sits in learner state, never consulted). Arm C:
blind pick over reg_check survivors.

## Results (3/3 byte-identical, SHA-256 b8070d0eaa22c039331496c76eb2eeade28ff54a54dc357a779149f1e5bc921d)

```
XD-WORLD D0=16
XD-INDUCED r=1 D=16 lo=1 hi=7
XD-CLAUSES nfields=2 nclauses=4
XD-TRIAL w=0 t=0 pool=1,3,5,7 N:nf=1 f0=11 ok=0 C:nf=2 f0=19 f1=87 found=1 ok=1
XD-TRIAL w=0 t=1 pool=1,1,7,7 N:nf=1 f0=9 ok=0 C:nf=2 f0=17 f1=119 found=1 ok=1
XD-TRIAL w=0 t=2 pool=3,5,7,1 N:nf=1 f0=29 ok=0 C:nf=2 f0=19 f1=87 found=1 ok=1
XD-TRIAL w=0 t=3 pool=5,5,5,5 N:nf=1 f0=45 ok=0 C:nf=2 f0=85 f1=85 found=1 ok=1
XD-TRIAL w=0 t=4 pool=7,3,1,5 N:nf=1 f0=59 ok=0 C:nf=2 f0=19 f1=87 found=1 ok=1
XD-TRIAL w=0 t=5 pool=1,7,3,5 N:nf=1 f0=15 ok=0 C:nf=2 f0=19 f1=87 found=1 ok=1
XD-WORLD D0=8
XD-INDUCED r=1 D=8 lo=1 hi=7
XD-CLAUSES nfields=2 nclauses=4
XD-TRIAL w=1 t=0 pool=1,3,5,7 N:nf=1 f0=11 ok=0 C:nf=2 f0=11 f1=47 found=1 ok=1
XD-FIDELITY agree=936 total=936
XD-VERDICT N_ok=0/12 C_ok=12/12
```

(Full per-trial lines in x_run1.txt; both worlds show the same
pattern: N picks the 1-word h=8 candidate every trial, C picks a
2-word all-in-range sentence every trial.)

## Hand verification (spot checks)

- W16 t=0: C pick [19,87]: 19=16*1+3, 87=16*5+7; components
  (1,3),(5,7) all in [1,7]. Well-formed. N pick [11]: single field,
  fails the 2-word requirement. Ill-formed.
- W16 t=1 pool=1,1,7,7: C pick [17,119]: 17=16*1+1, 119=16*7+7.
  Well-formed.
- W8 t=1 pool=1,1,7,7: C pick [9,63]: 9=8*1+1, 63=8*7+7.
  Well-formed under the induced D=8.
- Induction: W16 S multiples of 17, g=17, sole candidate d=16,
  op-check passes; W8 S multiples of 9, g=9, candidates {2,8}, d=2
  killed by SUB (3,1) fact (decode (12,1), 12-1=11!=2), d=8
  consistent. Ranges [1,7] both worlds from decoded SUB components.
- Note: in W8 the channel arm selects among survivors using the
  LEARNED grammar only; some picks use h=8 encodings that are
  well-formed under induced D=8. The constraint applied is the
  learned grammar, not teacher truth, which is exactly the claim.

## Kill-bar audit

- K1: 3/3 byte-identical (b8070d0e...). PASS.
- K2: Arm N well-formed = 0/12. The induced grammar, present and
  compiled in learner state, shapes nothing: the composer follows
  its own fewest-words bias every trial. Learned knowledge sits
  inert. PASS.
- K3: Arm C well-formed = 12/12. The identical composer, filtering
  through the generic registry, produces only well-formed
  compositions. PASS.
- K4: fidelity 936/936: the compiled clauses agree with an
  independent direct re-derivation of the grammar on every one of
  the 78 candidates x 12 trials. The grammar IS in usable checkable
  form. PASS (rules out the representational diagnosis).
- K5: no-wire audit. Composer section (x_main.zag lines 222..298):
  zero code references to divisor/decode/range/grammar/codec/pair/
  literal/induce/teach identifiers; zero reads of the induced-rule
  cells (0/1/2); cell refs limited to candidates (300..303), trial
  literals (700..703), pick trackers (800..814); the single external
  call is reg_check. direct_check is called only from the fidelity
  probe and the driver scoring, never from the composer. The only
  substring hits are the banner comment documenting the no-wire
  property itself. PASS.
- K6: safebin active, `which python3 python` empty, pure Zag, no
  forbidden executable invoked. PASS.

## Diagnosis (per the frozen diagnosis rule)

K2 + K3 + K4 all pass, so: learned knowledge does NOT automatically
constrain generation. The gap is architectural/control, NOT
representational:

- Control: the composer's pick procedure contains no
  constraint-consultation step; nothing in its machinery queries
  learned knowledge, so its own bias (fewest fields) decides.
- Architectural: the naive setup provides no shared checkable
  knowledge interface between the induction side and the composer
  side; the registry had to be built as substrate.
- Representational: ruled out. The induced rule compiles losslessly
  into generic clauses (936/936 agreement); the knowledge was
  usable, just unconsulted.

One generic channel (field/div/mod/range clause ABI, defined once as
substrate, not per grammar) closes the gap completely (0/12 to
12/12) with zero per-grammar wiring: the induction side knows only
the clause ABI, the composer side knows only reg_check.

## Metrics

- Cognition lines added: x_main.zag (~470 lines, unfrozen
  experiment); 0 to any frozen or shared source.
- Modes/bridges/handlers: 0. The registry is a shared learner-state
  table with generic operations. The arm flag is an
  experiment-harness condition selector; the composer (generation +
  pick rule) takes no flags.
- New hardcoded semantic cases: 0. New researcher semantic cases: 0.
- Determinism: 3/3 byte-identical runs
  (SHA-256 b8070d0eaa22c039331496c76eb2eeade28ff54a54dc357a779149f1e5bc921d).
- Frozen dirs untouched. Paper untouched. Nothing pushed.

## What this does not claim

- The clause ABI (field/div/mod/range) is researcher-defined generic
  machinery, comparable to an ISA: the claim is that ONE generic
  channel suffices, not that the channel itself was learned.
- The composer is intentionally minimal and grammar-blind; no claim
  it is a good composer, only that its picks are unshaped by the
  grammar without the channel.
- Two codec worlds only; no broad generality claim.
- The grammar family (pair codec P=a*D+b) remains a researcher-owned
  world assumption inherited from the grammar line.

## Follow-ups (not started)

1. The channel ABI here is researcher-defined. The harder question
   is whether a learner could INVENT its own constraint-compilation
   target (an L3-flavored follow-up): induction writes checkable
   knowledge in a form it designed, and a generic consumer applies
   it.
2. Composition under CONFLICTING learned grammars (two induced
   grammars constraining the same candidate set) would test whether
   the channel supports conjunction/priority without wiring.
3. The one-word degenerate pick exposes that the composer's native
   bias needs no grammar to be coherent; testing grammars that
   punish the composer's bias less trivially (partial applicability)
   is the natural next adversarial step.
