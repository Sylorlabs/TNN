# PREREG: Grammar Codec Active Inquiry (resolving ambiguity by asking)

## Worker

Codec Active-Inquiry Worker. Unfrozen variant only. Frozen read-only:
grammar_third/, grammar_transfer/, and grammar_codec/ are never
modified; their sources are copied, never edited. This prereg is
committed BEFORE any implementation (commit-order self-check).

## Problem (from the codec report)

GRAMMAR-CODEC-COMPLETE (grammar_codec/REPORT.md) induces the pair-codec
divisor D from the taught fact stream and refuses fail-closed when the
stream does not identify D: -3 when contradicted (NEG-SHIFT), -4 when
genuinely ambiguous (NEG-AMB: diagonal-only stream where D=8 with
components {2,4,6} and D=17 with components {1,2,3} both satisfy every
taught fact). The report's follow-up 1 notes the ambiguity is inherent
to the stream, not the procedure: richer teaching (any discriminating
taught pair) breaks the tie toward the true codec. This worker tests
whether ACTIVE INQUIRY (the learner requesting a discriminating
teaching example) resolves such ambiguities instead of refusing. This
connects the grammar line to the active-inquiry frontier (one of
Micah's standing questions: limited autonomous inquiry).

## Inquiry design: gi_inquire (learner side, general)

When gi_codec_induce finds 2 or more consistent divisors, -4 becomes
the inquiry trigger rather than the terminal verdict. The learner-side
mechanism is three plain functions (0 modes/bridges/handlers):

1. gi_codec_induce2(W, g_out, cands_buf, nc_out): refactor of
   gi_codec_induce that returns the same code (D>0 induced, -3
   contradicted, -4 ambiguous) and additionally the evidence summary g
   (gcd of the S multiples) and the full consistent candidate divisor
   list. gi_codec_induce is kept as a thin wrapper (identical return
   contract) so gi_induce behavior is unchanged.
2. gi_inquire(g, cands, nc): emits one GI-INQUIRY request naming the
   candidate divisor set and g, requesting ONE teaching example on
   which the candidates disagree. It names no components, no op, no
   pair structure, and no diagonal/off-diagonal distinction. This is
   the general active-inquiry primitive: "my hypotheses are
   {d1..dk}; give me an observation distinguishing them."
3. gi_cands_after(W, g, P, op, t, out): learner-side simulation of the
   consistent divisor set if the hypothetical fact (P,op,t) were added
   to the stream. It recomputes g' = gcd(g, s') using the same
   S-contribution rule as gi_codec_induce (s' = P+t for SUB with
   P+t>0; s' = P for unit DIV; else 0), re-derives candidates from
   divisors of g', and tests each against the W facts plus the
   hypothetical fact. No W mutation. Returns the new consistent count.

Supporting refactor: gi_fact_ok(d, P, op, t) is the single-fact
op-consistency check factored out of gi_codec_op_ok (byte-identical
semantics; gi_codec_op_ok is rewritten to call it).

## Teacher (driver-simulated world)

c_teacher_answer(W, wid, refuse, g, cands, nc): the world answers the
learner's request. It enumerates the true world's fact space: (a,b)
over the true literal lattice, op in {41,42}, computing the true
(P,op,t). It considers only facts the true world endorses
(gi_fact_ok(D_true, P, op, t) == 1, so the true divisor can never be
killed by its own answer). For each, it simulates via gi_cands_after
and offers the FIRST fact with 1 <= n2 < nc: strictly shrinking the
ambiguity while keeping at least one candidate alive. It teaches the
fact with ev_teach_in and emits GI-ANSWER. Returns 1 if a fact was
taught, 0 if refuse==1 (emits GI-TEACHER-REFUSED) or no discriminating
fact exists in the lattice (emits GI-TEACHER-NO-DISCRIMINATOR). The
teacher's search is generic (simulate-and-shrink on the learner's own
consistency computation); it hardcodes no pair structure. The teacher
knowing its own true world (lattice, D_true) is a world assumption on
the teacher side, like the existing c2_P/c3_P/c4_P teachers; the
LEARNER never sees it.

## Driver loop

After the initial gi_induce, if the code is -4, up to QMAX=4 inquiry
rounds run: gi_codec_induce2 (evidence + candidates) -> gi_inquire
(request) -> c_teacher_answer (teach or refuse) -> gi_codec_induce
(pure re-check). The loop stops on resolve (code D>0, then one final
gi_induce writes the single grammar node), contradiction (-3,
defensive; unreachable with a cooperative teacher), teacher refusal,
no discriminator, or QMAX exhaustion. Terminal -4 (still refused,
nothing written) is preserved exactly when the teacher refuses, no
discriminating observation exists, or QMAX runs out: inquiry is a
request, not a guarantee, and fail-closed survives.

## Worlds (all: SUB=41, DIV=42, DSUB=43, DDIV=44, BUILD=45)

- EXL2 (wid 2), EXL3 (wid 3), EXL4 (wid 4): unchanged teachers from
  grammar_codec. Expect 1 with D=16/8/32 and ZERO GI-INQUIRY lines
  (control a: unambiguous worlds must not trigger inquiry, no wasteful
  questions).
- NEG-SHIFT (wid 6): unchanged teacher (codec shift at a=5, g=1).
  Expect -3 with ZERO GI-INQUIRY lines (control b: contradicted, not
  ambiguous, so inquiry must not fire; inquiry cannot fix a shifting
  codec).
- NEG-AMB (wid 5): unchanged diagonal-only D=8 teacher (literals
  {2,4,6}, S={18,36,54}, g=18, consistent {8,17}). Cooperative
  teacher. Expect resolution to D=8 after exactly 1 query.
- NEG-AMB-R (wid 7): same teaching as NEG-AMB; teacher REFUSES every
  request. Expect terminal -4, exactly 1 query issued and 0 answered,
  nothing written (fail-closed preserved when the teacher refuses).
- NEG-AMB4 (wid 8): literals {2,4,6}, true D=8, taught ONLY on the
  diagonal pair (6,6): eval (54,41,0),(54,42,1); decomp
  (0,43,54),(1,44,54); BUILD (0,45,54),(1,45,54). S={54}, g=54,
  divisors give candidates {1,2,5,8,17,26,53}; the op check kills
  1,2,5 and keeps {8,17,26,53}: a genuine 4-way ambiguity under the
  true D=8 (b=6<8, injective, so inside the induced family).
  Cooperative teacher over the true lattice {2,4,6}. Expect
  resolution to D=8 after exactly 2 queries.

## Hand-verified inquiry traces

NEG-AMB (g=18, C={8,17}, enumeration order a=2,4,6 x b=2,4,6, SUB
then DIV, DIV only when exact):
- (2,2,41),(2,2,42): already taught; simulation gives n2=2, no shrink.
- (2,4,41): (20,41,-2), endorsed under D=8 ((2,4)); d=17 decodes
  (1,3), 1-3=-2, consistent; n2=2, no shrink.
- (2,6,41): (22,41,-4); d=17 decodes (1,5), consistent; n2=2.
- (4,2,41): (34,41,2); d=17 decodes (2,0), 2-0=2, consistent; n2=2.
- (4,2,42): (34,42,2), endorsed under D=8 ((4,2), 4/2=2); s'=0 so
  g'=18; d=17 decodes (2,0) with bb=0, DIV requires bb>0: KILLED;
  d=8 consistent; n2=1 < 2. FIRST discriminator: teacher offers
  (34,42,2).
Post-answer re-induction: g=18, candidates {1,2,5,8,17}, only d=8
survives the op check (d=17 killed by (34,42,2)). INDUCE D=8.
Exactly 1 query issued, 1 answered.

NEG-AMB4 (g=54, C={8,17,26,53}):
- Q1: (2,2,41) = (18,41,0), endorsed under D=8 ((2,2)); s'=18,
  g'=gcd(54,18)=18, candidates from 18 are {1,2,5,8,17}; d=8 and
  d=17 consistent (d=17: (18,41,0)->(1,1); W facts (54,41,0)->(3,3),
  (54,42,1)->(3,3) exact); d=26: (18,41,0)->(0,18), 0-18!=0 killed;
  d=53 killed the same way. n2=2 < 4: FIRST discriminator, teacher
  offers (18,41,0). Post-answer: S={54,18}, g=18, C={8,17}, still -4.
- Q2: (2,2,41) now taught (n2=2, no shrink); (2,2,42): (18,42,1),
  both consistent, no shrink; (2,4,41): (20,41,-2), d=17 consistent
  via (1,3), no shrink; (2,6,41): (22,41,-4), d=17 via (1,5), no
  shrink; (4,2,41): (34,41,2), d=17 via (2,0), no shrink; (4,2,42):
  (34,42,2), d=17 killed via bb=0, d=8 consistent: n2=1 < 2,
  teacher offers (34,42,2). Post-answer: only d=8 survives. INDUCE
  D=8.
Exactly 2 queries issued, 2 answered.

## Predicted outcomes (frozen bars)

- EXL2: GI-INDUCED 1, GI-INDUCED-POST 1, D=16 a=[0,9] b=[0,9],
  0 queries, induce 6/6 class 1, ablate 0/6, hardcode 6/6.
- EXL3: GI-INDUCED 1, POST 1, D=8 a=[0,7] b=[0,7], 0 queries,
  induce 4/4, ablate 0/4, hardcode 4/4.
- EXL4: GI-INDUCED 1, POST 1, D=32 a=[0,3] b=[0,3], 0 queries,
  induce 2/2, ablate 0/2, hardcode 2/2.
- NEG-AMB: GI-INDUCED -4, POST 1, D=8 a=[2,6] b=[2,6], 1 query
  issued / 1 answered, GI-ANSWER P=34 op=42 t=2, induce battery 1/1
  class 1 on target {0}.
- NEG-SHIFT: GI-INDUCED -3, POST -3, 0 queries, GI-GRAMMAR none.
- NEG-AMB-R: GI-INDUCED -4, POST -4, 1 query issued / 0 answered,
  GI-TEACHER-REFUSED, GI-GRAMMAR none, GI-I-NOGRAMMAR.
- NEG-AMB4: GI-INDUCED -4, POST 1, D=8 a=[6,6] b=[6,6], 2 queries
  issued / 2 answered, GI-ANSWER P=18 op=41 t=0 then P=34 op=42
  t=2, induce battery 1/1 class 1 on target {0}.
- Determinism: 3 runs byte-identical (SHA-256 recorded in run files).

## Kill bars (all must hold, else verdict fails)

K1: 3/3 runs byte-identical.
K2: per-world GI-MATCH 1 on all seven worlds (post-inquiry code vs
    expect); induced divisors exactly 16/8/32 on EXL2/EXL3/EXL4 and
    exactly 8 on NEG-AMB and NEG-AMB4; ranges exactly a=[0,9]/[0,7]/
    [0,3] and b=[0,9]/[0,7]/[0,3] on EXL, a=[2,6] b=[2,6] on
    NEG-AMB, a=[6,6] b=[6,6] on NEG-AMB4.
K3: no hardcoded divisor candidate in the machinery; the inquiry
    names no components, no op, no pair structure (grep evidence);
    candidates derive only from divisors of the observed gcd; the
    teacher's world knowledge (lattice, D_true) stays on the teacher
    side and never enters learner machinery.
K4: NEG-AMB-R refuses -4 with no grammar node written after the
    teacher refuses (fail-closed preserved); NEG-SHIFT refuses -3
    with no inquiry lines.
K5: EXL2/EXL3/EXL4 emit zero GI-INQUIRY lines (no wasteful questions
    on unambiguous worlds).
K6: query counts exactly as predicted: NEG-AMB 1/1, NEG-AMB4 2/2,
    NEG-AMB-R 1/0, all others 0/0.
K7: toolchain guard: safebin active, `which python3 python` empty,
    pure Zag; no forbidden executable invoked.

## What this does NOT claim

- The teacher is cooperative and simulated inside the driver; it is
  not a separate agent and not a model of a human teacher. The claim
  is about the learner-side mechanism (ambiguity detection,
  hypothesis-set request, re-induction), not about teacher fidelity.
- The P(a,b)=a*D+b family remains a researcher-owned world
  assumption, as in all prior grammar work.
- No broad generality claim: this is the targeted test of active
  inquiry on codec ambiguity (one 2-way and one 4-way case), plus
  refusal-preservation and no-wasteful-question controls.
- QMAX=4 is a driver constant bounding the inquiry loop; the worlds
  here need at most 2.

## Verdict on pass

GRAMMAR-INQUIRY-COMPLETE, with the query-count table (queries
issued/answered per world: EXL2 0/0, EXL3 0/0, EXL4 0/0, NEG-AMB 1/1,
NEG-SHIFT 0/0, NEG-AMB-R 1/0, NEG-AMB4 2/2).
