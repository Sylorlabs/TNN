# P6 / FORMAL-INDUCE — PREREG AMENDMENT 1

Status: frozen BEFORE any data was generated and before any learner code was
written. Disclosed openly. **No kill bar, prediction, threshold, seed, or
criterion is changed by this amendment.** Only a family-definition detail is
corrected, and one criterion's applicability is narrowed.

## A1. THE DEFECT IN PREREG SECTION 1.2.5

PREREG 1.2.5 defined the hidden global constraint over "all NUM atoms". Section
3 I6 required the learner to recover "the exact value map of every NUM token".
Criterion K6 required I6 to succeed.

**This is unachievable at stage 0, and the defect is an identifiability
theorem, not an implementation difficulty.**

At stage 0 the corpus contains only programs of the form `atom SEMI` repeated.
A `NUM`-role token and a `STR`-role token occur in *exactly the same syntactic
positions*, with *exactly the same* local context, in *exactly the same* role
in any context-sensitive feature the stage-0 corpus contains. Every
context-contrast induction (I1, and I3's follower-set signature) therefore
returns an identical signature for a NUM token and a STR token. The stage-0
data contains **zero bits** that distinguish the two classes. Any learner,
however good, must assign the two classes to one class (atoms) or to an
arbitrary split. It therefore cannot know which tokens' values enter the
global sum, so I6 at stage 0 is not merely hard, it is undefined.

The distinction does become identifiable from stage 2 onward, because at
stage >= 2 typing is enforced and an operator's induced operand-type signature
partitions the atoms. That is a legitimate induction, and I want to keep it.

## A2. THE CORRECTION

The hidden global constraint is redefined over the **ATOM role**, not the
NUM role:

> A program is globally valid iff `sum of val(t) over all ATOM-role tokens t
> occurring in the program  ==  c  (mod M)`, with `M in {16,32,64}` and
> `c in [1,M-1]` both seed-derived, and `val` a seed-derived injective map from
> the 6 ATOM tokens into `[0,M)`.

`ATOM` is defined as the union of the old NUM and STR roles. It is
identifiable at stage 0 (it is exactly the set of tokens that can occur in
operand position before `SEMI`), which is what makes I6 well-posed at stage 0.

Consequences, all stated in advance:

- K6 applies at **stage >= 1**, as prereg already implied (K6 said "stage >= 1"
  only implicitly; this makes it explicit). K6 at stage 0 is **not a bar** and
  a stage-0 GLOBAL result is reported as `GLOBAL-UNIDENTIFIABLE-BY-STAGE0`,
  which is the theorem in A1, not a learner failure.
- I6 now searches for `(M, c, val-map over 6 ATOM tokens)` with `c != 0`. The
  `c != 0` condition is load-bearing and is now stated: the constraint family
  is symmetric under `val -> c - val` for programs with exactly 1 or 2 atoms,
  so the learner can only break the reflection ambiguity using valid examples
  with 3 or more atoms. The corpus is therefore preregistered to contain valid
  examples with 1, 2, 3, 4 and 5 atoms.
- The NUM-versus-STR sub-distinction remains a real induction target, but it
  is a **typing** target (I4 at stage >= 2), not a global-constraint target.
  I am moving it out of K6 and it is now covered by K1 and by the stage-2+
  numbers in K2.

## A3. WHAT DID NOT CHANGE

- The family shape of PREREG 1.1 (unchanged).
- The role inventory, except that the 6 atom-role tokens are now collectively
  "ATOM" with 4 numeric and 2 string members; the numeric/string split is
  still seed-derived and still hidden.
- Seeds 1009, 2027 (and the frozen fallback list). Not touched.
- Corpus sizes (220 = 130 VALID + 90 INVALID). Not touched.
- All of K0-K5, K7-K10. Not touched.
- All of P1-P6. Not touched.
- ZD-1, ZD-2, ZD-3 definitions. Not touched.
- The STUPID baselines, the arms, the ablations, the three binaries, the
  process separation G2. Not touched.

## A4. A SECOND, SMALLER CORRECTION (disclosed in the same amendment)

PREREG 1.1 wrote `IF Cond THEN Item* ELSE Item* END`, and PREREG section 3 I3
described the learner's structure as a "prefix structure over depth-normalised
token streams". Depth-normalisation is not expressible as a flat acyclic
prefix structure when block nesting is unbounded. The learner's structure
therefore keeps an explicit **depth component in its state**: a learner state
is `(structure-node, depth-class)`, where `depth-class` is the learned
bracket-depth of the token stream. This is a mechanism detail, changes no bar
and no prediction, and is recorded here because PREREG 3 I3's description was
literally inaccurate.
