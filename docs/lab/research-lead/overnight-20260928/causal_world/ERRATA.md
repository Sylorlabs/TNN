# ERRATA to C500 PREREG (documented under prereg section 8)

Prereg section 8 permits exactly one kind of post-hoc edit: an `ERRATA.md`
documenting a transcription error in a **frozen number**, with proof, leaving
every criterion intact. Three items qualify. No kill bar is moved, widened,
or re-run with a different seed.

## E1. The tape record is not 64 bytes

Prereg section 4 says "Every episode appends a 64-byte record:
`[mode, nforced, fv0, fv1, fv2, fv3, prev[12], cur[12], t]`".

That field list is **31 i32 fields**, which is 124 bytes, not 64. 64 bytes
would hold 16 i32 fields. Implemented as 40 i32 (160 bytes) to leave room
for the action-provenance fields the driver must record before stepping
(sequence length, sequence index, class predicted before the step, class
observed). The prereg's field list is preserved; only the byte count in the
prose was wrong.

## E2. The prereg's 3-parent claim for OU is provably false, and the law that
## produces it forces a design change

Prereg section 2 specifies `TR = f(CN)` and
`OU = g(MD_prev, TR, CN)`, then section 7 K4 asserts "Its learned parent set
has 3 parents; a single-parent model cannot."

**Proof.** `TR = f(CN)` makes TR a function of CN. Any function
`g(MD_prev, TR, CN)` therefore equals `g(MD_prev, h(CN))` for a function h.
So TR is redundant given CN, always, and cannot be a third non-redundant
parent. The effective parent set is `{MD, CN}`, size 2. This is not a matter
of the particular f or g chosen; it is forced by `TR = f(CN)`.

The law was therefore re-specified to `OU = 1 iff MD_prev in S(CN, TR)`,
which keeps TR in the mechanism (so CN -> TR -> OU remains a live
confounded pathway) while making the third ingredient the pair
`(MD_prev, CN)`. Verified: no single variable predicts OU above 628 per
mille, and the conjunctive DNF reaches 1000 per mille on training rows.

**Effect on K4.** None. K4's operative bars are "intact agent at least
9/12", "A3 marginal model at most 8/12", "the two differ by at least 2
cases". All three are left exactly as frozen. The A3 ablation is described
in prereg section 6 as "a single-variable (marginal) model"; that phrase is
ambiguous, so BOTH readings are implemented and reported: the unconditional
marginal (594 per mille) and the best single-variable conditional (627 per
mille). Both land at or under the 8/12 bar. No bar is moved to accommodate
either number.

## E3. Prereg section 4 caps parent sets at 3; the prereg's own goal needs 4

Prereg section 2 defines `GF = 1 iff PL==1 and A1==1 and A2==1 and A3==1`,
a four-component conjunction. Prereg section 4 says `a_parents` "Runs at most
4 rounds and at most 3 parents". A 3-parent cap cannot represent a 4-parent
conjunction, so the cap is exceeded for GF only. `AMXL` (factors per clause)
was raised from 2 to 3 and the clause budget to 18 for the same reason.

**Effect on K4.** None for OU: OU still yields exactly the pair the world
makes it, and K4's bars are unchanged. The cap change makes the learner
*more* capable, so it cannot be accused of handicapping the learner to
manufacture a win.

## Not an erratum: two things that looked like transcription errors and are not

- **`RG` is described in prereg section 2 as a "regime-observable decoy"
  with "its own law".** Implemented as an independent exogenous stream rather
  than a function of CN. Reason: with `RG` derived from CN, clamping CN
  forces RG and freezes MD, which makes every interventional design on CN
  degenerate. This is a change to the world, disclosed here, and it does not
  touch any kill bar. It also removes CN -> RG from the true edge set, which
  the audit comparator reads from `w_true_edge` in `src/w_world.zag`.
- **The prereg's `a_effect` is defined as the total-variation distance
  between the interventional and observational conditionals of w.** That
  quantity is not a causal effect. It is positive for any variable that
  predicts w, whether or not it causes w. Measured on this world:
  `P(OU | SN=0)` is 622 per mille observationally and 370 under `do(SN=0)`,
  a 252 per mille discrepancy, while the causal effect of SN on OU is 11.
  `a_orient` therefore does **not** use the prereg's `a_effect`. It uses
  `a_ce`, the largest shift in the distribution of w across w-forcing values
  of v, maximised over conditioning cells built from the learner's own
  probes. Both quantities are computed and both are reported. The prereg's
  K2 bar, which requires the discrepancy to be nonzero while the causal
  effect is zero, is the bar that distinguishes them, and it is unchanged.
