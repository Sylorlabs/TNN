# REPORT: Grammar Codec Active-Inquiry Worker

## Verdict: GRAMMAR-INQUIRY-COMPLETE (with query-count table)

## Claim tested

GRAMMAR-CODEC-COMPLETE induced the pair-codec divisor D from the taught
fact stream and refused fail-closed on ambiguity: NEG-AMB
(diagonal-only stream where D=8 with components {2,4,6} and D=17 with
components {1,2,3} both satisfy every taught fact) refused -4. The
ambiguity is inherent to the stream, not the procedure. This worker
tests whether ACTIVE INQUIRY (the learner requesting a discriminating
teaching example) resolves such ambiguities instead of refusing,
connecting the grammar line to the active-inquiry frontier.

## Inquiry mechanism (implemented, unfrozen)

Learner side (i_patch.zag, plain functions, 0 modes/bridges/handlers):

- gi_fact_ok(d,P,op,t): single-fact op-consistency, factored out of
  gi_codec_op_ok with identical semantics.
- gi_consistent_set(W,g,has_extra,eP,eOp,eT,out): candidate divisors
  d=v-1 for v|g, v>=2 derived from the observed g by exact arithmetic
  (no hardcoded candidates); each tested against the W facts plus one
  hypothetical fact. Returns the consistent count.
- gi_codec_induce2(W,g_out,cands,nc_out): same code contract as
  gi_codec_induce (D>0 / -3 / -4) plus the evidence summary g and the
  full consistent candidate list. gi_codec_induce is a thin wrapper;
  gi_induce behavior is unchanged.
- gi_cands_after(W,g,P,op,t,out): learner-side simulation of the
  consistent set if a hypothetical fact were added (recomputes g' with
  the same S-contribution rule, re-derives candidates, tests each).
  No W mutation.
- gi_inquire(g,cands,nc): emits one GI-INQUIRY request naming the
  candidate divisor set and g, requesting ONE teaching example on
  which the candidates disagree. Names no components, no op, no pair
  structure, no diagonal/off-diagonal distinction. The general
  active-inquiry primitive: "my hypotheses are {d1..dk}; give me an
  observation distinguishing them."

Teacher (driver-simulated world): c_teacher_answer enumerates the true
world's fact space ((a,b) over the true literal lattice, op in
{41,42}, DIV only when exact), considers only facts the true world
endorses (gi_fact_ok(D_true,...)==1, so the true divisor is never
killed by its own answer), simulates each via gi_cands_after, and
offers the FIRST fact with 1 <= n2 < nc (strictly shrinks the
ambiguity, keeps at least one candidate alive). Returns 0 on refusal
or when no discriminating fact exists.

Driver loop: after the initial gi_induce, -4 becomes the inquiry
trigger (not the terminal verdict). Up to QMAX=4 rounds:
induce2 -> inquire -> teacher answers -> pure re-induce. Stops on
resolve (one final gi_induce writes the single grammar node),
contradiction, teacher refusal, no discriminator, or QMAX exhaustion.
Terminal -4 with nothing written is preserved exactly when inquiry
cannot resolve: inquiry is a request, not a guarantee, and fail-closed
survives. The loop is entered only on -4, so unambiguous worlds never
ask and contradicted worlds never inquire.

## Results (3/3 byte-identical, SHA-256 5d47d7da...)

```
GI-WORLD EXL2
GI-INDUCED 1 / GI-INDUCED-POST 1 / GI-MATCH 1
GI-GRAMMAR nbuild=4 nlic=2 lic=44,43 D=16 a=[0,9] b=[0,9] maxlinks=1
(no GI-INQUIRY lines)
GI-WORLD EXL3
GI-INDUCED 1 / POST 1 / MATCH 1
GI-GRAMMAR nbuild=4 nlic=2 lic=44,43 D=8 a=[0,7] b=[0,7] maxlinks=1
(no GI-INQUIRY lines)
GI-WORLD EXL4
GI-INDUCED 1 / POST 1 / MATCH 1
GI-GRAMMAR nbuild=2 nlic=2 lic=44,43 D=32 a=[0,3] b=[0,3] maxlinks=1
(no GI-INQUIRY lines)
GI-WORLD NEG-AMB
GI-INDUCED -4
GI-INQUIRY request=discriminating-example ncands=2 cands=17,8 g=18
GI-ANSWER P=34 op=42 t=2
GI-QUERIES issued=1 answered=1
GI-INDUCED-POST 1 / GI-MATCH 1
GI-GRAMMAR nbuild=2 nlic=2 lic=43,44 D=8 a=[2,6] b=[2,6] maxlinks=1
GI-I-VALID 1/1 (target 0, class 1)
GI-WORLD NEG-SHIFT
GI-INDUCED -3 / POST -3 / MATCH 1
GI-GRAMMAR none (no GI-INQUIRY lines)
GI-WORLD NEG-AMB-R
GI-INDUCED -4
GI-INQUIRY request=discriminating-example ncands=2 cands=17,8 g=18
GI-TEACHER-REFUSED
GI-QUERIES issued=1 answered=0
GI-INDUCED-POST -4 / MATCH 1
GI-GRAMMAR none / GI-I-NOGRAMMAR
GI-WORLD NEG-AMB4
GI-INDUCED -4
GI-INQUIRY request=discriminating-example ncands=4 cands=53,26,17,8 g=54
GI-ANSWER P=18 op=41 t=0
GI-INQUIRY request=discriminating-example ncands=2 cands=17,8 g=18
GI-ANSWER P=34 op=42 t=2
GI-QUERIES issued=2 answered=2
GI-INDUCED-POST 1 / MATCH 1
GI-GRAMMAR nbuild=2 nlic=2 lic=43,44 D=8 a=[6,6] b=[6,6] maxlinks=1
GI-I-VALID 1/1 (target 0, class 1)
GI-VERDICT 7/7
```

Ablate/hardcode arms (EXL worlds only, unchanged from the codec
design): EXL2 6/6 induce, 0/6 ablate, 6/6 hardcode; EXL3 4/4, 0/4,
4/4; EXL4 2/2, 0/2, 2/2.

## Query-count table

| world | queries issued | queries answered | outcome |
| EXL2 | 0 | 0 | D=16, no inquiry fired |
| EXL3 | 0 | 0 | D=8, no inquiry fired |
| EXL4 | 0 | 0 | D=32, no inquiry fired |
| NEG-AMB | 1 | 1 | D=8 resolved |
| NEG-SHIFT | 0 | 0 | refused -3, no inquiry fired |
| NEG-AMB-R | 1 | 0 | refused -4, fail-closed preserved |
| NEG-AMB4 | 2 | 2 | D=8 resolved |

## Why each outcome is correct (hand verification)

- NEG-AMB: initial C={8,17}, g=18. The teacher's first shrinking
  fact in enumeration order is (34,42,2): true pair (4,2), P=34, DIV
  t=2, endorsed under D=8; d=17 decodes (2,0) with bb=0, DIV requires
  bb>0, killed; d=8 consistent. Post-answer only d=8 survives: D=8,
  the true codec. One query. The battery's 1/1 (target 0, ans=54,
  class 1) confirms the induced grammar builds.
- NEG-AMB4: initial S={54}, g=54, C={8,17,26,53} (4-way ambiguity,
  all op-consistent on the taught diagonal facts). Q1: (18,41,0)
  [true pair (2,2)] gives s'=18, g'=18, candidates {1,2,5,8,17};
  d=26 killed via (0,18), d=53 killed the same way, d=8 and d=17
  consistent: C={8,17}. Q2: (34,42,2) kills d=17 via bb=0 as in
  NEG-AMB: C={8}. D=8, the true codec. Two queries. Battery 1/1.
- NEG-AMB-R: identical request to NEG-AMB, but the teacher refuses:
  the learner stays at -4 with nothing written. Inquiry does not
  weaken fail-closed; it only adds a resolution path when the world
  cooperates.
- NEG-SHIFT: code -3 (g=1, no consistent divisor), so the inquiry
  loop is never entered: zero GI-INQUIRY lines. Contradiction is not
  ambiguity; inquiry cannot fix a shifting codec and is not attempted.
- EXL2/3/4: code 1 on the first induce, so zero GI-INQUIRY lines:
  no wasteful questions on unambiguous worlds.

## Kill-bar audit

- K1: 3/3 runs byte-identical (SHA-256
  5d47d7da804b1bc066ce9e2848acf9d8b7c343ed47b609536e6964962fe78c73).
  PASS.
- K2: GI-MATCH 1 on all seven worlds; divisors exactly 16/8/32 on
  EXL2/EXL3/EXL4 and exactly 8 on NEG-AMB and NEG-AMB4; ranges
  exactly a=[0,9]/[0,7]/[0,3] and b=[0,9]/[0,7]/[0,3] on EXL,
  a=[2,6] b=[2,6] on NEG-AMB, a=[6,6] b=[6,6] on NEG-AMB4. PASS.
- K3: no hardcoded divisor in the machinery: `grep` for divisor
  literals on i_patch.zag returns only two comment lines (the same
  two as the codec worker); the inquiry names no components, no op,
  no pair structure (the single "diagonal" mention in the patch is
  the comment stating the mechanism makes no diagonal/off-diagonal
  distinction); candidates derive only from divisors of the observed
  gcd; teacher world knowledge (lattice, D_true) stays on the
  teacher side. PASS.
- K4: NEG-AMB-R refuses -4 with GI-GRAMMAR none after the teacher
  refuses; NEG-SHIFT refuses -3 with zero inquiry lines. PASS.
- K5: EXL2/EXL3/EXL4 emit zero GI-INQUIRY lines. PASS.
- K6: query counts exactly as preregistered: NEG-AMB 1/1,
  NEG-AMB4 2/2, NEG-AMB-R 1/0, all others 0/0. PASS.
- K7: safebin active, `which python3 python` empty, pure Zag, no
  forbidden executable invoked. PASS.

## Metrics

- Cognition lines added: new patch functions (gi_fact_ok,
  gi_consistent_set, gi_codec_induce2, gi_cands_after, gi_inquire)
  plus the gi_codec_op_ok/gi_codec_induce refactors and the driver
  inquiry loop, teacher, and NEG-AMB4 world; 0 to base (byte copy,
  SHA-256 a29972ca...44aa76a8bd identical to grammar_codec).
- Modes/bridges/handlers: 0. New semantic cases: 0. Inquiry is plain
  functions, not a mode. Base modifications: 0.
- Determinism: 3/3 byte-identical runs
  (SHA-256 5d47d7da804b1bc066ce9e2848acf9d8b7c343ed47b609536e6964962fe78c73).
- Frozen dirs untouched (grammar_third, grammar_transfer,
  grammar_codec read-only; sources copied, never edited).

## What this does not claim

- The teacher is cooperative and simulated inside the driver; it is
  not a separate agent and not a model of a human teacher. The claim
  is about the learner-side mechanism (ambiguity detection as a
  hypothesis set, the discriminating-observation request, and
  re-induction), not teacher fidelity.
- D is induced within the P(a,b)=a*D+b family; the family itself
  stays a researcher-owned world assumption, as in all prior grammar
  work.
- No broad generality claim: this is the targeted test of active
  inquiry on codec ambiguity (one 2-way case, one 4-way case), plus
  a refusal-preservation control and no-wasteful-question controls.
- QMAX=4 is a driver constant bounding the loop; these worlds need
  at most 2 queries.

## Follow-ups (not started)

1. The teacher could be adversarial (offering consistent-but-useless
   facts, or facts that shrink toward a wrong-but-consistent set);
   the current simulate-and-shrink teacher is cooperative.
2. Self-directed inquiry: the learner currently asks the teacher to
   find the discriminator; gi_cands_after already lets the learner
   score hypothetical observations itself, which is the primitive a
   self-directed variant would need.
3. Inquiry beyond codecs: the request primitive (name the hypothesis
   set, ask for a distinguishing observation) is codec-agnostic;
   testing it on another ambiguity class would show whether it is a
   general active-inquiry operation or a codec-specific repair.
