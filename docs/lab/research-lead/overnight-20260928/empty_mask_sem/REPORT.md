# REPORT: S1 vs S2 empty-mask semantics (decided)

Date: 2026-10-02. Worker: subsumption-reproduction replacement
(empty-mask discrimination). Lane:
`docs/lab/research-lead/overnight-20260928/empty_mask_sem/`.
Pure Zag, pinned znc
`src/tools/toolchain/znc_linux_x86_64_abed8aa1` (2026.07.0-dev).

## Verdict: S2 CONFIRMED

S2 (empty kind-set reads as the universal set {1,2} in all three admission
positions) is confirmed as the correct pinning of the prereg
underspecification. The S2 arm matches the frozen S2 prediction column on all
four discriminating problems; the S1 arm matches the frozen S1 column on all
four, and the two columns differ on every problem (Q1 on ANS, Q2-Q4 on
TRIES/WIDEN). Combined with the textual grounding (the Compatibility sentence
is unconditional) and the already-observed K9 result (UNI P6 = ANS=2 TRIES=3
with no widening, inconsistent with S1's hand-derived P6 profile of ANS=2
TRIES=4 WIDEN=1), the S1 reading is rejected.

## Kill bar results (3/3 byte-identical per arm)

Format: ANS / TRIES (+INTER / WIDEN where logged).

| Problem | Position tested | S2 arm (frozen -> observed) | S1 arm (frozen -> observed) |
|---|---|---|---|
| Q1 | single, empty in/outmask | 41 / 2 -> 41 / 2, no WIDEN | -2 / 7 WIDEN=1 -> -2 / 7 WIDEN=1 |
| Q2 | pair middle, empty B.inmask | 2 / 3 INTER=44 -> 2 / 3 INTER=44, no WIDEN | 2 / 4 INTER=44 WIDEN=1 -> 2 / 4 INTER=44 WIDEN=1 |
| Q3 | pair outer, empty A.inmask | 2 / 4 INTER=44 -> 2 / 4 INTER=44, no WIDEN | 2 / 5 INTER=44 WIDEN=1 -> 2 / 5 INTER=44 WIDEN=1 |
| Q4 | pair middle, both masks empty | 2 / 4 INTER=44 -> 2 / 4 INTER=44, no WIDEN | 2 / 3 INTER=44 WIDEN=1 -> 2 / 3 INTER=44 WIDEN=1 |

- K1-Q1: PASS. S2 admits the untaught IDENT single by the empty-set fallback
  and answers 41 in 2 tries; S1 rejects it, exhausts all admitted candidates,
  and fails (-2) after 7 tries with widening.
- K2-Q2: PASS. S2 admits (WALK, untaught-COUNT) on the effective middle and
  succeeds in 3 tries with no widening; S1 rejects the pair on the raw empty
  middle and reaches the same answer only via the widening retry (4 tries,
  WIDEN=1).
- K3-Q3: PASS. Same pattern with the empty mask in the outer A.inmask
  position: S2 4 tries no widen; S1 5 tries WIDEN=1.
- K4-Q4: PASS. Both middle masks empty: S2 admits on {1,2}&{1,2} (4 tries, no
  widen); S1 rejects and recovers in widening (3 tries, WIDEN=1).
- K5 DETERMINISM: PASS. 3/3 byte-identical per arm (digests below).
- K6 HYGIENE: PASS. Pure Zag for all scientific computation; safebin guard
  attested in NAMECHECK.md Step 0; zero em/en dash bytes in lane docs
  (byte-verified); no forbidden-executable invocation.
- K7 SINGLE-VARIABLE AUDIT: PASS. `em_arm_s1.zag` differs from `em_arm.zag`
  by exactly one line (the `u_eff` body; diff-verified). One admission rule,
  one execution rule, no mode flags; the arm tag in emitted output
  self-derives from `u_eff(0)`, so the S1/S2 difference is confined to that
  line.

## Determinism (K5)

Run-output sha256 (3/3 identical):
- s2: 7b042bd44ee9e465c231a83afd6183d6f890a01e25b553585411700461ade998
- s1: f5039ebb2afe7122b9256d11853e2ecf3c964d50715f1b78c4b5e6bd3e9cabc3
Binaries:
- em_s2_bin: 4f01387b2827760c9d87540aab041ae9e1e2cedcbc0549afb48c2602943ea3eb
- em_s1_bin: bdb7c45fc7d367c80a88536bcb2d5b599a8b972462e9779c07364be6909195a9
znc 2026.07.0-dev (edition 2026), pinned binary
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`.

## What the experiment establishes

1. The prereg underspecification was real, not verbal: S1 and S2 are
   genuinely different operations, separated on all four problems.
2. S2 is the reading consistent with the frozen prereg text: the Compatibility
   sentence ("an EMPTY kind-set (no observations) is compatible with every
   kind") governs all three admission positions, and the "INTERSECTS
   (nonempty)" middle condition is evaluated on effective sets.
3. The S1 reading is now rejected on three independent grounds: the
   unconditional Compatibility sentence, the sealed K9 observation (whose
   no-widening profile S1 cannot produce), and 4/4 fresh preregistered
   discriminations matching S2's column.

## Implication for the unified behavior-contract operation

It pins a parameter; it does NOT change the operation. The unified operation
keeps exactly one admission rule, one execution rule, and failure-triggered
widening. The pinned parameter is the empty-mask reading inside the admission
rule: the effectiveness function `u_eff` (empty -> universal {1,2}) applied
uniformly in all three admission positions. No new rule, mode, bridge, or
handler was added; the S1/S2 difference is one line in one function.

Governance consequence: the frozen prereg text should gain one sentence so no
future reproduction re-derives this: "In all three admission positions, an
empty kind-set is read as the universal set {1,2} before the compatibility
and intersection checks." AMEND3's pinning stands, now confirmed by 4/4 fresh
preregistered discriminations plus K9. Ledger entry C325 (the reproduction)
can record S2 as the pinned semantics with this lane as the deciding
evidence.

## Honest limitations

- The battery discriminates the two readings of the admission rule; it does
  not test behavior induction, SUM-to-PLAN transfer, or any other dimension.
- Widening rescues S1 on Q2-Q4 (same ANS via the retry path), so the S1/S2
  difference is operationally sharpest where an empty-mask MAP is the only
  single-candidate path (Q1: ANS differs) or in try/widen profiles.
- Both arms are one worker's implementations; the single-line diff confines
  the semantic difference, but the shared base is not an independent
  re-derivation (not claimed as one).

## Architecture accounting

- Cognition lines added: ~202 (em_base.zag) + ~134 (em_arm.zag).
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- Researcher-owned: world setups, behavior implementations, the admission
  rule text, the S1/S2 effectiveness line.
- Learner-owned: kind-set contracts grown by teaching/success recording.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/empty_mask_sem/`:
NAMECHECK.md, PREREG.md (frozen before implementation; committed alone),
em_base.zag, em_arm.zag (S2), em_arm_s1.zag (one-line sed variant,
diff-verified), em_full_s2.zag, em_full_s1.zag (assembled), em_s2_bin,
em_s1_bin, s2_run1/2/3.txt, s1_run1/2/3.txt, run.sha, bin.sha, REPORT.md
(this file). The sibling lanes `compose_collapse/`,
`compose_collapse_repro/`, `mask_transfer/`, and `spec_mask_revision/` were
never modified. Commits local only, explicit pathspecs, never pushed.
