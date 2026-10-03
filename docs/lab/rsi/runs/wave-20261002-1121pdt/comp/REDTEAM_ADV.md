# REDTEAM_ADV: adversarial pass on the ADV-A battery and its verdict

Stance: every favorable reading below was attacked; what survives is
reported. Required question: is any ADV-A result explainable by
probe-menu equivalence or a source audit?

## 1. Probe-menu equivalence

Attack: supervised d_satisfy enumerates (MAP, prefix length, grounding)
and returns the first combination whose terminal equals the expected
value. That is search-plus-verify against a researcher-supplied target:
a probe menu where the "probes" are enumerated options and the expected
value picks the winner. If so, the battery measures search, not
composition.

Counter-evidence:
- The menu is not researcher-enumerated. The options are the learner's
  own promoted MAPs (learned from component experience via trial),
  generic prefix lengths 4..1, and live fact groundings. No test names
  a MAP, a prefix, or a grounding; the driver only teaches facts and
  queries. The compositional content is in WHICH options exist
  (learned structure) and how they combine (segmentation with LINK14
  provenance), not in the expected value.
- TPF-3 (and 0521 NOSUP) compose with expected < 0: no target exists
  for anything to verify against, yet the mechanism promotes the exact
  11-step composite (relseq [1,1,2,2,3,3,3,1,1,2,2], terminal 112).
  Probe-menu equivalence cannot explain a pass with no probe.
- B8's pass requires PREFIX use ([1,1] of X's [1,1,1,1]) after the
  longest-prefix-first ordering commits to a distractor and backtracks
  through k0=4, k0=3. A flat probe menu over whole structures could
  not produce a prefix composite; the relseq check ([1,1,2,2], not
  [1,1,1,1,2,2]) proves the segmentation.
- B4 separates the paths empirically: when satisfy cannot fire, the
  trial path answers (105) with NO satisfy markers and NO LINK14
  edges. If satisfy were just the trial path renamed, the markers
  could not dissociate like this.

Honest residue (BOUND, not kill): PM-1a/PM-1b confirm that among
multiple fully MAP-licensed completions, the expected value does ALL
the selecting. satisfy carries no intrinsic preference between valid
compositions. And unsupervised satisfy is order-fragile: B3U and PF-1c
both show the greedy fixpoint committing to the first novel terminal
with no recovery. The mechanism's autonomy is bounded; its strength
is supervised compositional search, not goal-free invention.

## 2. Source audit

Attack: the mechanism source might contain test-specific logic that
explains the passes.

Audit performed on patch_d.zag (frozen, SHA df1d0faa...): every integer
literal in code (comments stripped) enumerated. Result: literals are
buffer sizes (32, 4608, 512, 4096), node tags (101 = SET cell, 102 =
SEQ cell in the graph encoding), field offsets (0, 4, 8, 12, 20, 24,
28, 36), loop bounds (1024, 64, 13, 7), and the depth/iteration bounds
(8, 12). ZERO occurrences of any test value: 70-74, 101-112 as values
(the two `101` hits are `tag!=101` / `tag==101` node-tag comparisons),
204-206, 904-920, 4000-4399, 9100-9139, 105, 106, 112, 205. Zero code
occurrences of "compose" (3 comment hits explaining the absence).
The driver was audited for leakage: it teaches facts and issues
queries; expected values are the protocol's post-hoc feedback (frozen
E-ruling, same as 0521); it never names MAPs, prefixes, segments, or
groundings. The dv_relseq verification copy is mechanism-neutral
(independent reimplementation of the structural extraction).

The audit attack fails: no test-specific logic exists in the mechanism.

## 3. Knowledge-vs-architecture confound (trial path, continued)

0521's sharpest self-catch was the trial path answering supervised
tests with goals of 4 or fewer edges. This battery was designed to end
it:
- TPF-1/2/3 goals are 11 edges; the trial path (k<=4) is structurally
  excluded, and the mechanical criteria require SAT markers plus exact
  relseq. All three pass with markers.
- B4 is the negative control the 0521 battery lacked: a world where
  satisfy CANNOT fire but trial CAN. Result: trial answers, satisfy
  claims nothing (no marker, no LINK14). This proves the markers are
  honest and the two paths are empirically separable.
- B6 reruns 0521's ADV-A verbatim on the rebuilt binary: SAT-SEGS n=2,
  ans=105, relseq [1,1,2,2]. The 0521 attribution (genuine, not trial)
  reproduces.

Residual: component training still promotes MAPs via the trial path
(the frozen E-ruling protocol). The composition step itself is what
this battery isolates, not MAP formation.

## 4. Is B7's robustness real or an artifact of small constants?

Attack: 40 distractor chains of 8 edges is small; the "no stall"
finding might not survive scale.

Assessment: the comparison that matters is against A's measured
behavior on the same ORDER of distraction: A stalled 50+ min on 40
SINGLE-fact distractors (O(MAPs^2 x paths^2) exhaustive pair search);
D exhausts 40 EIGHT-edge distractor subtrees (each walked to depth
exhaustion with k0=1 unwind, full backtracking) in ~16 s alongside
B1+B2. The structural reason is visible in code: D only explores
groundings that match a learned MAP's relseq prefix, so dead-end
branches die in O(chain length) node visits; A's pair search has no
such guidance. Scale limits remain: t2_gather caps at 96 paths
(latent bound, untested: with 50+ same-node branches the correct
grounding could be truncated; noted for a future breaker), and the
depth bound 8 is a learner-writable policy header, not a theorem.

## 5. Metric gaming

PASS/FAIL thresholds are mechanical equalities on answers, extracted
relation sequences, edge counts, and marker presence/absence; kill
bars were frozen at d516c1da6 before implementation at 21b881c9e
(KB6 verified). Predictions were recorded in the prereg; all 17
matched, including the predicted B3U FAIL, which was scored FAIL per
the mechanical criterion, not re-scored. INFO tests (B4U, PF-1c) were
never kill bars. No bar was moved.

## 6. What the breakers actually broke

Nothing in the supervised sealed battery broke: no wrong-answer
promotion, no hang, no dishonest attribution. What the battery BOUNDED:
(a) unsupervised satisfy is greedy and order-committed (B3U terminal
914, PF-1c terminal 106: two independent demonstrations); (b) satisfy
has no intrinsic tie-break among multiple valid compositions (PM-1);
(c) when no learned structure covers the goal, unsupervised satisfy
promotes partial composites rather than abstaining (B4U terminal 103).
These are characterization findings with exact numbers, not kills,
and they were all predicted in the frozen prereg.

## 7. Criterion 0 (no L3 claimed)

C0-C (independent-adversary sealed family) still fails: this battery
was designed by the lane worker, not an independent adversary (PF-1
is post-freeze but not independent). C0-D (reuse improving a
downstream cognitive metric) unmeasured. satisfy remains L2
structural composition: the strongest such candidate tested, now
with adversarial survival evidence, but no L3 claim is available.
