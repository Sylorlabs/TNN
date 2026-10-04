# L3B/L3C Integration Scout: Assessment

Date: 2026-09-30. Verdict: L3-INTEGRATION-SCOUT-COMPLETE.

## What was reviewed

- L3B v2: L3B_V2_RESULT.md (L3B-V2-PASS, bounded L2; implementation 7a1d3265d)
- L3B v2 adversary: L3B_V2_ADV_RESULT.md (C64 L3B-V2-ADV-BOUNDED; attacks frozen at 42538c6b6, addendum 252440aa4)
- L3B v2 robust: L3B_V2_ROBUST_RESULT.md (C68 L3B-V2-ROBUST-PASS; prereg 92c73aeca)
- L3C v3: RESULT_L3C_V3.md (C66/C73 L3C-V3-PASS; prereg 3124d2e9a, result 3bfa0947c)
- L3C v3 red team: RESULT_L3C_V3_REDTEAM.md (L3C-V3-REDTEAM-SURVIVES; plan f63d36e3a)
- Core Freeze run: RUN_RESULTS.md at 97b28e6a6 (FREEZE-RUN-COMPLETE; W2 0/8, W3 0/10)

## What L3B v2 actually does, and its bounds

L3B v2 is an enumerative program grower. It searches a finite 205-program
space (depth at most 2, constants 0 through 8), finds the first program
matching training episodes in canonical order, and assembles it with
CREATE/CONNECT constructor operations. Per-regime versions are archived
with recall by node identity; single-failure dispatch corrects after one
honest miss. The v2 robust follow-up added explicit ambiguity records
(most-recent policy) and an archive-full refusal signal instead of a
panic.

Bounds, confirmed by the independent adversary (C64) and honestly scoped
by the builders: the menu is finite with provable edges (degree 3
unreachable, constants outside 0..8 unrepresentable; menu exhaustion is
reported, not forced). The robust result states explicitly that the
fixes "do not constitute incremental construction." There is no
fragment library, no composition of previously grown programs into
larger ones, no mechanism by which the vocabulary grows from experience.
The lane ruling stands: redesign toward incremental construction, never
menu expansion.

## What L3C v3 actually does, and its bounds

L3C v3 is a rule learner over feature atoms (feature, op, value
predicates). Its disc2 path builds single-atom direct dispatch nodes;
when contradictions defeat every single atom, disc_cover performs
generic subset-enumeration set cover over corroborated atoms and
build_cover constructs a multi-edge DISP dispatch node reusing the
interpreter's existing union semantics. The interpreter diff is empty:
featv, pred_match, select_edge, interp, trace_last_edge, path_uses are
byte-identical v2 to v3. No OR semantic case exists anywhere. The red
team confirmed the operation generalizes to three-element disjunctions
(6/6 truth eval, no new machinery), that minimality genuinely
discriminates among multi-atom covers, and that ambiguity counting is
honest at k=3.

Bounds: bounded L2. Cover-search combinatorics are capped (12 candidates,
cn at most 30, disclosed); cover sets multiply faster than single
separators so AMBIGUOUS_COVER withholds more often; 2-conjunctions are
direct-path-only (frozen bound). Atoms are predicates over observations,
not actions or operations.

## Assessment 1: L3C cover-set composition as a procedure-construction substrate for W2

The honest answer is no, not as it stands, for a structural reason: L3C
composes predicates into dispatch structure; W2 procedures need
composition of operations into executable sequences. L3C's atoms answer
"which condition holds" and its DISP node routes on the answer. A
procedure answers "what to do next" and needs sequencing, not routing.
The cover operation (union corroborated parts into one working
structure) is genuinely general, the atom vocabulary is not. Porting
disc_cover to W2 would require either (a) atoms that denote operations
rather than predicates, which is a different mechanism wearing the same
name, or (b) a dispatch-only notion of procedure, which trivializes the
W2 bar.

Integration cost under the One-System Rule: adopting L3C as-is means
adopting its control flow (disc2 then disc_cover fallback), its
EVID_MIN admission bar, its AMBIGUOUS_COVER representation, and its
contradiction-triggered trigger policy. That is a subsystem with a
fallback mode and researcher-authored policy around a general core. The
general core is the composition operation itself: take a set of
corroborated parts, find a minimal cover, build one working structure
from it using existing semantics. The policy around it (when to
trigger, what counts as corroborated, minimality vs memorization) is
researcher-authored, not learner-learned. Integration as-is scores badly
on learner authority and adds a mode; extraction of the operation scores
well on generality and compression but is a redesign, not an adoption.

## Assessment 2: L3B's finite menu and the incremental-construction path

The finite menu fundamentally limits L3B v2. The adversary proved the
edges are reachable and honest (depth-3 and out-of-range constants fail
cleanly), which is a virtue of the mechanism but does not remove the
ceiling. There is no path from "enumerate 205 programs" to incremental
construction by extension; the robust result says so explicitly.

A genuine incremental path would look like this, and it is a different
mechanism: maintain a learner-owned fragment library seeded by
discovered atoms; compose fragments with the existing CREATE/CONNECT
operations; verify compositions against experience; keep verified
compositions as new fragments so the vocabulary grows from use. The
archive in v2 already keeps per-regime versions, so the persistence
machinery exists; what is missing is the compose-verify-promote loop and
the fragment library as learner state. Per the standing lane ruling,
this is a separate research program. It must not become menu expansion:
the test is whether the vocabulary after N regimes contains structures
no researcher enumerated, which the current 205-program grammar fails by
construction.

## Recommendation: REDESIGN, keep both separate

Do not integrate L3B v2 or L3C v3 into the frozen core as they stand.

- L3B v2/robust: keep as a bounded-L2 experimental baseline (like SEM).
  Its honest menu-exhaustion and ambiguity records make it a good
  negative/control reference. Integration would smuggle a finite
  vocabulary into the core and violate the lane ruling. The
  incremental-construction redesign is a separate program; its
  falsifiable bar is a vocabulary after N regimes containing structures
  no researcher enumerated.
- L3C v3: keep as bounded-L2 evidence that cover-set composition is a
  general learning operation. Do not adopt the disc2/disc_cover control
  flow as a core subsystem. The redesign program is: extract the
  composition operation, generalize parts beyond predicates, and make
  the trigger and corroboration policy learner-owned rather than
  researcher-authored.

The shared architectural cause behind W2 (0/8 procedures) and W3 (0/10
causal laws) is that the frozen core has no operation for composing
verified parts into a new working structure. L3B composes by menu
lookup; L3C composes predicates by cover search. The one-system target
is a single learner-owned compose-verify-promote operation that works
over whatever parts experience has corroborated, whether predicates,
operations, or causal links. That operation does not exist yet in any
lane. Building it is the program; adopting either current mechanism
whole is the treadmill.

## What would prove this recommendation wrong

1. A demonstration that L3C's disc_cover, unchanged, constructs a
   correct W2 procedure (sequenced operations, not dispatch routing) on
   a sealed procedure family. This would show the operation is already
   substrate-general and my predicate/action distinction is wrong.
2. A demonstration that L3B's archive plus a small, preregistered,
   general promote rule (no grammar change) yields a vocabulary
   containing a structure no researcher enumerated, reused in a later
   regime. This would show the incremental path is an extension, not a
   redesign.
3. A frozen-core world in which either mechanism, integrated without
   new modes or bridges, fixes two or more currently failing
   freeze-challenge worlds at once. Single-world fixes do not count,
   per the standing direction.

## ONE-SYSTEM RULE accounting (this assessment)

- Cognition source lines added: 0 (assessment only, no implementation).
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
- New task-specific handlers: 0.
- Learner-state structures created: 0.
- Recommendation direction: fewer mechanisms (one composition
  operation, not two subsystems), lower source delta (extract, do not
  adopt), more learner authority (learner-owned trigger and fragment
  library).
