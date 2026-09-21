# AMBIGUITIES.md — U: Recompute-on-demand (r1)

Frozen ambiguities are read literally and logged here. Nothing is silently
reinterpreted. Where a value was needed to build/test, the provisional choice
is documented and explicitly flagged as NOT frozen evidence.

## A1. Derivation-window radius (A-41) — BLOCKED
The frozen mechanism says "derivation window radius frozen" but no value is
given. No radius may be asserted as frozen. The implementation uses U_R=256
(provisional, engineering only) — this is NOT frozen evidence.

## A2. MA1/RC1 operation rate — BLOCKED
The required "MA1/RC1 median memory-operation rate per 1,000 episodes" has
not been located in frozen materials. No rate is asserted.

## A3. S equations — BLOCKED
PREREG_FREEZE.md lists θ_merge=0.15, ρ=1.5, σ_split=2.0 with brackets.
The exact translation to code (merge predicate, veto rule, threshold
semantics) is unverified. The implementation's merge rule is provisional,
NOT frozen evidence.

## A4. Comparator D — BLOCKED
Whether existing Track-A D can serve as the required "same derivation rule
with persistent caching/invalidation" comparator is unresolved. The
implementation includes a custom DReg comparator (provisional, unapproved).
It is NOT an approved frozen comparator.

## A5. M2 semantic mismatch — NOTED (not a block)
M2's bar assumes a learning system (ep0 < 95%, then climb to ≥99.5%). U is
a store: recall is 100% from episode 0 by construction. There is no learning
curve because there is nothing to learn. The ep0<95% clause is vacuous for
U. U maintains perfect recall throughout: PASS with note. This is a
category mismatch, not a failure.

## A6. M4 interpretation — NOTED
M4 reports 0.0% content/boundary. If M4 measures damage/interference, 0%
means no damage (good). The exact M4 bar semantics are not in the frozen
materials available; the raw numbers are reported as-is.

## A7. M9 JSON formatting — FIXED
The M9 text lines interleaved with METRIC_JSON, breaking the parser. Fixed
by removing text lines; JSON fields carry the data.

## A8. Duel heisenbug — ROOT-CAUSED AND FIXED (2026-09-21)
Was: "slice index out of bounds" panic at E>=150 (bisected: E=100 clean,
E=150 panics). Initial suspicion (uninitialized sentinel / heap layout) was
WRONG. Root cause: **silent i32 overflow in the edit-position computation**
`gp = (e*total)/E` in `duel_edits` (`cl/arm.zag`). At r1 corpus sizes
(total = 14,938,062 bytes), `(E-1)*total` exceeds i32 range for E>=150
(E=150: max 2,225,771,238 > 2,147,483,647; E=100: max 1,478,868,138, in
range — matches the observed boundary exactly). The product wraps to a
negative value (observed: e=144, E=150 -> gp=-14,292,575); the guarded
`u_edit`/`d_edit` call returns -1 harmlessly, but the expected-bytes mirror
write `prose[off]=255` indexes the slice directly -> deterministic panic.
"Layout-sensitive" was a misdiagnosis: the bug is a pure function of corpus
byte sizes, deterministic given the corpus.
Fix: compute the edit position in i64 —
`gp = (((e as i64)*(total as i64))/(E as i64)) as i32` (gp < 2^31, fits).
The identical latent overflow in `t_m9` (`gp=(e*total)/1000`, wraps for
e>=144) was fixed the same way; M9's e200/e500/e1000 levels previously ran
with wrapped (wrong) edit positions but did not panic. M9 re-run with the
fix: plateau holds (e200=727848, e500/e1000=727204, rekey=0, hits=0),
byte-identical across reruns.
Full duel E=0..1000 now completes (both reruns byte-identical, rc=0);
E=0..100 rows unchanged vs pre-fix (confirming the fix is behavior-neutral
where no overflow occurred). See VERDICT.md for the completed sweep.

## A9. r10 corpus provenance — BLOCKED
CORPORA.md says r10 should be deterministically built by committed
`build_10x.py` after 1x validation. A stray `r10/prose.bin` exists but
provenance is unverified. 10x is NOT attempted.
