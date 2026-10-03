# COMPOSE-PAIR6-ADV REPORT: Diamond (fan-out) vs the unified operation U

Date: 2026-10-02. Worker: COMPOSE-PAIR6-ADV. Lane:
docs/lab/research-lead/overnight-20260928/compose_pair6_adv/.
Branch lane-composepair6-20261002 (isolated worktree ~/workspace/tnn-rsi-pair6).

## Verdict

**INFORMATIVE-FAIL for U on fan-out; GENERAL-EXTENSION-EXISTS.**

K1 through K6 all PASS (K2 under transparent AMEND1, K5 under transparent
AMEND2; both committed before the runs they govern). Per the frozen
Section 8 mapping: K1+K2 PASS defines U's generality boundary (U handles
linear pipelines only; one intermediate feeding two consumers is outside
it). K3+K4+K5 PASS establishes that a general extension of U's own
principles solves the diamond with no new mechanism, no modes, no flags,
no shape templates, no domain handlers.

## What was built

- d6_base.zag: frozen ref_uc_base.zag (commit b5cb711be) plus exactly the
  two allowlisted hunks: class-4 arity-mismatch in exec_map, and the
  appended 2-input contract machinery (m2g/m2p, exec_map2, observe2,
  teach2, diamond world builders). Verified by diff.
- d6_uni.zag: unmodified U composer (byte-identical composer region to
  ref_uc_uni.zag; only main replaced to add the Q1 diamond query).
- d6_gen.zag: GEN, the value-graph generalization of U.
- uni_bin (sha256 43f1bffdf00e6fc39240e776bb0baa555bc2a3c2904d882e9c393f608d72df0a),
  gen_bin (sha256 23100e8c1be8148d18bff20f97e87caa8e5a4bc8d6b237c7ffbc17023ab31702).
  3/3 byte-identical stdout each; stderr empty.

## Kill bars

- K1 PASS: UNI first 18 stdout lines byte-identical to the frozen UNI arm
  (compose_collapse/uni_run1.txt). The extended base reproduces U's
  canonical profile exactly.
- K2 PASS (AMEND1): UNI-D Q1 exhausts U's trial space and fails:
  2 admitted singles, 4 admitted pairs, WIDEN=1, 8 widened pairs,
  ARM=UNI-D PROB=Q1 ANS=-2 TRIES=14. U has no route for X(202)=211 to
  reach both Y and W; every admitted route is verified end-to-end and
  fails. INFORMATIVE-FAIL: the boundary is real, not a teaching artifact.
- K3 PASS: GEN Q1 solves the diamond: INTER=211,-2,-2,-2,3,2;
  INTER2=6,5; ARM=GEN PROB=Q1 ANS=5 TRIES=8. The fork emerges from pool
  reuse: 211 is computed once by X, then consumed by both Y and W in
  round 2, and G(3,2)=5 closes the diamond.
- K4 PASS: GEN regresses the collapse battery: P1 ANS=65 TRIES=4;
  P2a/P2b/P3 ANS=2 TRIES=6 each; P2b needs NO widening (the observed-kind
  handshake admits (X,Y) directly where U's predicted handshake needed
  WIDEN=1). No regression on U's home turf.
- K5 PASS (AMEND2): GEN Q2 (misleading G teaching) reaches a fixpoint,
  fires WIDEN=1 exactly once, and the admission-off phase solves it:
  ARM=GEN PROB=Q2 ANS=5 TRIES=47. The generalized failure-triggered
  widening works as designed.
- K6 PASS: composer-region diff empty; base diff is the allowlist only;
  3/3 byte-identical; zero forbidden-interpreter invocations (NAMECHECK
  Step 0); no em/en dashes in docs.

## Transparent amendments (committed before the runs they govern)

- AMEND1 (79d7899c2): the prereg's K2 hand-derivation wrongly assumed
  G's 1-input contract fields were empty; observe2 populates them
  (in{2}/out{2}), changing admission. Corrected block: TRIES=14 (was
  15), ANS=-2 and WIDEN=1 unchanged. The bar's substance (U exhausts its
  trial space and fails) is identical.
- AMEND2 (cb5ef0f84): the prereg's K5 derivation forgot
  teach2(m3,202,202,404), which saturates G's contract to {1,2}|{1,2}.
  Measurable bars (ANS=5, TRIES=47, WIDEN=1) unchanged and matched
  exactly; the "contract grows" parenthetical was incorrect and is
  retracted.

## Implementation defects found and fixed (before official runs)

- GEN scratch arena overflow: the prereg's byte layout put the done-set
  at 3852..4108, 12 bytes past the 4096-byte arena, causing a
  deterministic "slice index out of bounds" panic in gen_record. Fixed
  by u8-packing the visit stack (3596..3660) and done set (3660..3724);
  no design change. All region bounds re-verified.
- One transient uni_bin panic ("slice index out of bounds") on a single
  early run did not reproduce in 8 subsequent runs or the 3 official
  runs; reported, not hidden. No action taken; the official 3/3 are
  clean and byte-identical.

## Architectural answer

Diamond defeats U, but not for a deep reason: U's trial space is
{singles, ordered pairs} with a predicted outmask INTERSECTS inmask
handshake, so a value produced once can never be consumed twice. GEN
keeps every one of U's principles (kind-set contracts, compatibility
admission, deterministic ordered trial, end-to-end verification,
failure-triggered widening, provenance-based success-recording) and
generalizes only the trial space: singles then pairs becomes rounds over
a value pool, and the predicted handshake becomes observed-kind
checking (stage 1 executes, stage 2 tests the observed value). The
diamond fork is not a new mechanism; it is what the value graph does
when 211 sits in the pool and two consumers admit it. No modes, no
flags, no diamond-specific code anywhere in GEN.

Boundary B1 held: exactly one new 2-input arithmetic class (ADD2) was
authorized as ISA-level machinery; without it a fan-out-with-join task
is vacuous, and with it GEN still had to discover the routing.

## Open questions / follow-ups

- The transient uni_bin panic deserves a note in the compiler-defect
  log if it ever reproduces; currently a single non-reproducing event.
- GEN's round cap (6) and pool cap (64) are untested boundaries; a
  deeper diamond (3+ levels of fan-out) would probe them.
- Whether GEN's observed-kind admission (stage 1 executes, stage 2
  tests) has failure modes U's predicted handshake avoids (e.g.
  side-effecting MAPs) is not tested here; all MAPs here are pure.
