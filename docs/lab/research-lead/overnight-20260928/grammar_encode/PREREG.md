# PREREG: Grammar Encoding-Detection (fail-closed codec guard)

## Worker

Grammar Encoding-Detection Worker. Unfrozen variant only. Frozen
read-only (grammar_third/ and grammar_transfer/ are never modified;
their sources are copied, not edited).

## Problem (from grammar_third REPORT.md, commit ee621a50d)

EXL3 breaks the pair-encoding assumption (world P(a,b) = a*8+b vs
machinery P(a,b) = a*16+b). The byte-identical machinery went SILENTLY
WRONG: it induced a confident wrong grammar (a=[0,3], b=[0,15] instead
of the true 0..7 components) and the battery reported 4/4 valid. The
wrongness is self-consistent (same wrong decode at all five sites), so
it is invisible in headline scores. The part-1 sanity check is
vacuous (a*16+b==P is a tautology under any fixed divisor; it reduces
to P>255 and cannot fire on any world run to date).

## Guard design: gi_codec_check

A new function in the unfrozen patch, called inside gi_induce AFTER
part-2 range induction and BEFORE the type-70 grammar node is written.
It cross-checks the machinery's assumed codec (a*16+b, the decode used
at all five sites) against the observed fact structure. Two sub-checks,
both general (no divisor is named except the machinery's own assumed
codec; the discriminator comes from the fact stream, not from a
hardcoded list of broken encodings):

(A) Grid round-trip. For every (a,b) in the induced ranges
[min_a..max_a] x [min_b..max_b], re-encode P' = a*16+b under the
assumed codec. Each P' must occur as the subject or object of a live
type-1 fact. A missing grid point means the induced ranges assert
pair objects the world never contained. Failure code -2.

(B) Op-consistency. For every live type-1 fact with relation in
{41,42} (the eval ops the verification lookup assumes: SUB=41,
DIV=42), the subject is a pair P and the object is the taught value t.
Decode P under the assumed codec to (a,b) and require the op the
relation names to reproduce t: SUB (41): a-b==t; DIV (42): b>0,
a-(a/b)*b==0, a/b==t. A violation means the codec contradicts the
world's own taught semantics. Failure code -3.

Design note (recorded before implementation): a naive pair-set
round-trip (re-encode ranges, compare the SET of pair objects) is
provably vacuous for EXL3: the induced ranges a=[0,3], b=[0,15]
re-encode to exactly 0..63, which coincides with the observed pair set
0..63. The grammar_third report anticipated this: the discriminator
must come from the relational structure, which is what (B) provides.
(A) fires on encodings whose observed pair set does not cover the
induced rectangle; (B) fires on encodings that cover the rectangle but
contradict the taught op semantics. The two are complementary, and
neither names /8 or any other specific broken encoding.

## gi_induce return contract (extended)

- 1: grammar induced and written (both sub-checks passed).
- 0: legacy refusal (part-1 inconsistency, no BUILD facts, no
  licensors, nlic>2, empty ranges, node alloc failure). No grammar
  written. Unchanged from prior work.
- -2: REFUSED, codec grid round-trip failed (A). No grammar written.
- -3: REFUSED, codec op-consistency failed (B). No grammar written.

On any non-1 code the driver reports the code, prints GI-GRAMMAR none,
and the induce arm prints GI-I-NOGRAMMAR (construction cannot proceed
without a grammar node). This is the fail-closed proof: refusal is
observable in the output and no wrong grammar enters learner state.

## Worlds (all: SUB=41, DIV=42, DSUB=43, DDIV=44, BUILD=45)

- EXL2 (control, correct encoding): literals 0..9, P(a,b) = a*16+b
  (matches the machinery codec). TRAIN {1,3,5,7} alternating
  DIV-first/SUB-first (4 BUILD facts). TEST {0,2,4,6,8,9} (6 targets).
- EXL3 (broken encoding): literals 0..7, P(a,b) = a*8+b. TRAIN
  {1,3,5,7} (4 BUILD facts). TEST {0,2,4,6} (battery runs only if a
  grammar is induced).
- EXL4 (new broken encoding): literals 0..3, P(a,b) = a*32+b
  (sparse stride; observed pairs {0,1,2,3,32..35,64..67,96..99} do not
  cover the /16-decoded rectangle a=[0,6] x b=[0,3]). TRAIN {1,3}
  alternating DIV-first/SUB-first (2 BUILD facts: (1,45,33),
  (3,45,96)). TEST {0,2} (battery runs only if induced).

## Frozen predictions

1. EXL2: GI-INDUCED 1. GI-GRAMMAR nbuild=4 nlic=2 a=[0,9] b=[0,9].
   Battery GI-I-VALID 6/6. No false refusal.
2. EXL3: GI-INDUCED -3 (op-consistency diagnostic). GI-GRAMMAR none.
   Battery arm prints GI-I-NOGRAMMAR and builds nothing.
3. EXL4: GI-INDUCED -2 (grid round-trip diagnostic). GI-GRAMMAR none.
   Battery arm prints GI-I-NOGRAMMAR and builds nothing.
4. Determinism: 3/3 runs byte-identical (equal SHA-256).
5. Machinery identity: e4_base.zag byte-identical to
   grammar_third/g3_base.zag (shared SHA-256); e4_patch.zag equals
   grammar_third/g3_patch.zag plus the gi_codec_check function and the
   two-line guard insertion in gi_induce (diff recorded in REPORT.md);
   the five /16 decode sites are byte-unchanged.
6. No type-70 node exists in learner state after a refusal
   (GI-GRAMMAR none in both EXL3 and EXL4 worlds).

## Kill bars

- FAIL if EXL2 refuses (code != 1) or induces wrong ranges or scores
  != 6/6: the guard must not false-refuse the correct encoding.
- FAIL if EXL3 induces (code == 1) or writes any grammar node: the
  silent-wrong bug is not fixed.
- FAIL if EXL3 refuses with a code other than -3, or EXL4 with a code
  other than -2: the diagnostics must discriminate the failure mode.
- FAIL if the 3 runs are not byte-identical.
- FAIL if e4_base.zag differs by even one byte from g3_base.zag, or if
  any /16 decode site in the patch changed.
- FAIL if any forbidden executable (python3, python, cc, node, etc.)
  is invoked: PROCESS-FAIL per the toolchain guard.

## Constraints

Pure Zag for all research computation. Shell only for znc invocation,
binary runs, git ops, file moves, checksums, diffs. Zero em/en dashes
in docs. 0 modes/bridges/handlers. 0 new semantic cases beyond the
guard function. Commits local only, explicit pathspecs, nothing pushed.

## Commit order

This PREREG.md and NAMECHECK.md are committed BEFORE any implementation
file is written. Implementation (e4_patch.zag, e4_driver.zag, binaries,
run outputs, REPORT.md) follows only after the prereg commit exists.
