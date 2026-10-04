# AMENDMENT M2-W2: fresh-state execution for K-S9v2 (wave-20261001-2021pdt, lane BATTERY)

**Status:** AMENDMENT-FROZEN (design only; no M2-W2 re-run executed under this
amendment). This document amends PREREG_BATTERY_V2.md (frozen at d43fe32c5,
validation verdict BATTERY DEFECT on M2-W2, recorded in VALIDATION_RUN.md).
It is a new prereg section for a re-run of M2-W2 only. No other world,
bar, or control is altered.

**Commit-order self-check (binding):** this amendment must be committed
ALONE by the coordinator, with its SHA-256 recorded, strictly before any
M2-W2 re-run is executed under it. Filesystem mtime order must verify the
amendment commit precedes every re-run artifact. UNVERIFIABLE ORDERING voids
the re-run. The 2026-10-02 supplementary fresh-state run (N=0, pre=30,
post=30) was executed BEFORE this amendment existed and is explicitly
preserved as NOT-A-PASS isolation evidence; it cannot be adopted as the
amended re-run. No result from any wave may be promoted into this
amendment's evidence. No world file, envelope, or scorer is created or
modified before the amendment commit.

**Documentation rule observed:** no em-dashes in this file.

## 1. Defect diagnosis (why K-S9v2 cannot hold in the persistent chain)

The v2 prereg (section 3.5) designed M2-W2's K-S9v2 around a baseline ACT
that occurs "with no guide in state", recording the mechanism's declared
null action N, followed by a validity probe ("pre-resolution action
differs from N") that proves a live guide drove an inquiry action. The
prereg's block protocol (section 5.2) runs M2-W1 -> M2-W2 -> M2-W3 on one
persistent state.bin chain. That combination is self-defeating:

1. M2-W1 creates 4 guides, one per hidden key: the inquiry-phase QUERYs
   are misses (hidden keys have no facts; trial finds no paths; bootstrap
   on 45600 not invariant), and each miss creates one guide (prereg
   section 3.4 mechanism analysis).
2. Guides persist across worlds within the block; the frozen mechanism
   has no uncertainty-resolution transition (the missing transition M2-W2
   was built to test), so nothing retires the 4 M2-W1 guides when M2-W2
   begins.
3. The frozen mechanism emits CHOICE 30 whenever ANY guide is active, not
   per subject and not per world. The validation run showed this is more
   indiscriminate than the prereg assumed: 30 is the guide-active signal
   globally.

Therefore the M2-W2 baseline ACT, positioned after a taught-fact hit,
still fires under 4 live M2-W1 guides and yields 30, not the mechanism's
true null action 0. Observed in the block chain: N(baseline) = 30,
pre-resolution = 30, post-resolution = 30. The validity condition
(pre != N) evaluates 30 != 30 as false, so the world is WORLD-INVALID per
the prereg's own rule ("an unengaged world is not a pass"). The baseline
assumption ("no guide in state") is false in any in-chain execution, and
the contamination is structural, not incidental: there is no point in the
M2-W1 -> M2-W2 chain at which zero guides are live, because guide
creation is cumulative and guide retirement does not exist in the frozen
mechanism.

## 2. The two candidate fixes and why option (a) is chosen

Option (b), revising the K-S9v2 baseline to account for carried-over
guides in-chain, was considered and rejected. Its flaw is fundamental:
with 4 live guides and an indiscriminate guide action (30 for ANY active
guide), there is no in-chain measurement of a null action at all. Any
"baseline" taken under live guides is guide-contaminated by construction,
so validity ("pre != N") would compare two guide-driven values (30 != 30
again), and the bar ("post == N") would ask the post-resolution action to
equal a contaminated constant. A null action measured under live guides
is not a null action. No validity revision can repair that without
effectively redefining N away from its meaning, which would break the
bar's intent rather than preserve it.

Option (a) is chosen: run M2-W2 from fresh state, restoring the condition
the bar was designed for (guide-free baseline). The bar's intent is to
test whether the mechanism discriminates the null action from
guide-driven actions: a resolution-capable mechanism emits N after
resolution and a guide-driven action before it. Option (a) preserves that
demand exactly. It costs the persistent-chain placement of M2-W2 only,
and the affected collateral probes are restated as engagement probes
(section 3), not dropped silently and not re-purposed to manufacture a
pass. The rest of the battery, the other eight worlds, all other bars,
and the calibration controls are untouched.

## 3. Amended execution protocol (M2-W2 fresh-state re-run)

The M2 block is re-run as:

1. Fresh state A: run M2-W1 per the prereg (template plus envelope_r,
   driver log saved), exactly as in the v2 validation. State A persists
   after W1.
2. Fresh state B (a separate state file, never chained from state A):
   remove any prior state-B file; run
   `freeze_shim2_bin m2w2v2_world.txt stateB.bin` (exit code must be 0),
   saving stdout as the M2-W2 transcript. The world file content is
   UNCHANGED from the v2 battery (no sealed-file modification).
3. Continue state A: run M2-W3 on the post-W1 state (persistent chain
   W1 -> W3; M2-W2 no longer sits between them in the chain).
4. N is recorded as a measured parameter from step 2 (expected 0 for the
   frozen mechanisms) and carried to the M2-W3 scorer as a parameter,
   replacing the contaminated in-chain N=30 from the validation run.
   K-S10v2 is otherwise unchanged.
5. Determinism (extension of K-S2v2): step 2 is executed 3 times from
   fresh state; the 3 transcripts must be byte-identical (sha256
   equality). Steps 1 and 3 keep their v2 determinism rules (M2-W1
   per-run re-execution reproducibility; fixed W3 transcript equality
   across runs).
6. The calibration controls for M2-W2 (D1 constant-action, D2
   stale-action, C miss/hit responder; prereg section 4.2) are re-run
   against the fresh-state configuration before any mechanism verdict
   is drawn. Gates: D1 must not pass (WORLD-INVALID by validity or
   FAIL), D2 must FAIL, C must PASS. If any gate fails, the amended
   M2-W2 is VOID as a battery defect; no mechanism verdict follows.

Collateral-probe restatements (exact):

- M2-W2's two collateral probes (QUERY 45101 45600 45201,
  QUERY 45102 45600 45202), originally expecting M2-W1 calibration
  truths (hits), now run on fresh state B where those facts were never
  observed. Expected value: the mechanism's own miss response M
  (recorded as -2 in the validation run). They are engagement probes
  only; the retention claim on these two probes is WITHDRAWN for the
  amended run. K-S14v2's denominator stays 12, with these two scored as
  engagement.
- M2-W3's collateral probe on 44111 (QUERY 44111 44601 44901), originally
  a hit because M2-W2's teaches persisted in the chain, now runs on the
  amended W1 -> W3 chain where M2-W2's teaches never occurred. Expected
  value: the miss response M (engagement only; retention claim
  withdrawn). M2-W3's 45103 collateral remains a hit (from state A).

## 4. Amended K-S9v2 (exact text, validity, and verdict semantics)

**K-S9v2 (amended).** PASS iff the post-resolution ACT equals the
mechanism's declared null action N, where N is the action emitted by the
baseline ACT in the fresh-state M2-W2 run, which occurs after a hit with
no guide in state (fresh state; no miss precedes the baseline ACT in this
run, so the guide-free precondition holds by construction).

**Validity (amended).** The pre-resolution ACT differs from N; else
WORLD-INVALID (an unengaged world is not a pass). Additionally, if the
baseline ACT does not occur guide-free (verified by construction: fresh
state B, baseline before the first miss), the run is WORLD-INVALID.

**Predicted signature for the frozen mechanisms:** N=0, pre-resolution
ACT=30 (guide-driven), post-resolution ACT=30 (stale). Validity holds
(30 != 0). Bar: FAIL (post=30, not N=0). This matches the 2026-10-02
isolation run and corroborates the v1 M2 kill (constant inquiry action,
no resolution transition) through a calibrated bar.

**What a re-run PASS means:** the frozen mechanism emitted N
post-resolution while having emitted a guide-driven action
pre-resolution, demonstrating an uncertainty-resolution transition for a
single in-world guide. A PASS does not establish generality or L3, does
not alter the other eight worlds' verdicts, and does not touch the v1
kills except as specified below.

**What a re-run FAIL means:** corroboration of the standing v1 M2 kill
through a calibrated bar, consistent with K-S8v2 and K-S10v2.

**Unexpected-PASS rule (carried from prereg section 7):** if the frozen
mechanism PASSES the amended K-S9v2 (post=N with pre != N) while the
v1-calibrated evidence says it has no resolution transition, the amended
world is VOID as a battery defect: this is evidence about the amended
design, not a mechanism vindication. The corresponding v1 kill evidence
is REOPENED for defect analysis only, and no mechanism verdict is
upgraded.

## 5. Out of scope (recorded, not amended here)

- The K-S11v2(d) looseness (validation section 4, item 1): the
  representation-neutral restatement is looser than the intended
  evidence-counting demand. It did not change the M3 verdict
  (K-S11v2 still FAILS). A future amendment may tighten the bar text;
  this amendment does not touch it.
- The M3-W2 singleton collateral expectation (validation section 4,
  item 2): recorded as observed; K-S14v2 still PASSED. Not amended here.
- No sealed world file, envelope, or scorer content is altered by this
  amendment. Only the M2-W2 execution protocol, the N parameter source,
  and the stated collateral expectations change.

## 6. Skeptic's attack on this fix, and the answer

**Strongest attack:** option (a) narrows the world. In the persistent
chain, M2-W2 tested resolution against the mechanism's own carried-over
guides (4 of them, learner-created uncertainty structures from M2-W1);
from fresh state it tests resolution of a single in-world guide. A
mechanism could conceivably retire fresh guides but not long-lived
carried-over ones, or vice versa, so the amended world is not the same
demand. Worse, the collateral restatements withdraw four retention
probes' retention meaning (two in M2-W2, one in M2-W3, plus M2-W3's N
now arrives as a parameter), which looks like moving expectations to
fit the new protocol. If the fix makes the bar easier for a future
mechanism while claiming equivalence, the amendment is miscalibrated.

**Answer, point by point:**

1. The demand tested is the one the bar was designed for. K-S9v2's
   stated demand (prereg section 3.5) is the null-vs-guide-driven
   discrimination, measured against a guide-free baseline. That demand
   is UNTESTABLE in the chain (section 1: no guide-free point exists),
   so the chain version tested nothing at all (WORLD-INVALID). A
   narrower testable demand strictly dominates an untestable broader
   one; "resolve carried-over guides" was never scored, never gated,
   and never predicted, so nothing calibrated is lost.
2. The residual demand is flagged, not hidden. If a future mechanism
   passes the amended bar, the question "does it also retire its own
   long-lived carried-over guides" is recorded here as an open
   follow-up world, not claimed as covered. Honest narrowing with a
   named residual beats pretending the chain version worked.
3. The gates protect against easiness. The unchanged G-DEP/G-COMP
   controls are re-run on the fresh-state configuration (section 3,
   item 6): the degenerate policies that must fail still fail (D2
   stale-action: post=30 vs N=0, FAIL), and the competent miss/hit
   policy still passes. If the amended configuration were easier for
   degenerates, the gates would catch it and void the world.
4. The collateral restatements are protocol-truthful, not
   bar-weakening. A probe cannot test retention across a chain break
   that the amendment itself creates; scoring it as a retention hit
   would be dishonest. Restating to the miss response keeps the
   probes as engagement checks, keeps the K-S14v2 denominator at 12,
   and grants no PASS anywhere: the two restated probes are not part
   of any mechanism bar's PASS condition.
5. The real anti-gaming protection is pre-registration, not the
   protocol choice. The predicted degenerate signature (N=0, pre=30,
   post=30 stale, FAIL) is stated above BEFORE the re-run; the
   amendment must be committed alone before the re-run (self-check at
   top); and any result other than the predicted signature is a
   battery defect, never a pass. The supplementary 2026-10-02 run
   cannot be adopted. There is no path by which this amendment can
   manufacture a mechanism PASS.

**Verdict this amendment enables:** a re-run of M2-W2 from fresh state
under the amended K-S9v2, expected to FAIL with the predicted stale-guide
signature, yielding a 9/9 validated battery and corroborated v1 kills.
Anything else is a defect, not a vindication.
