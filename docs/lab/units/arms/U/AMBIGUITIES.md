# AMBIGUITIES.md — U: Recompute-on-demand (r1)

Frozen ambiguities are read literally and logged here. Nothing is silently
reinterpreted. Where a value was needed to build/test, the provisional choice
is documented and explicitly flagged as NOT frozen evidence.

## A1. Derivation-window radius (A-41) — ADJUDICATED 2026-09-21 (non-load-bearing)
The value was never set in any frozen material (A-41: "(value needed)").
Adjudication (MARATHON CREW U11) proves by radius-sensitivity sweep
(U_R ∈ {32, 64, 128, 256} with complete duel E=0..1000 sweeps, each
double-run byte-identical, rc=0; plus an R=512 E=0 data point with a
mechanism-backed bounding argument for R≥512) that no kill fires at any
radius and U's cpu stays orders of magnitude below the kill-(i) threshold
— the radius choice cannot flip the verdict. The value itself remains a
§13-amendment item for Micah; it does not block U's binding verdict.
Implementation uses U_R=256 (logged, never refit mid-trial).

## A2. MA1/RC1 operation rate — ADJUDICATED 2026-09-21 (not load-bearing; open §13 item)
The required "MA1/RC1 median memory-operation rate per 1,000 episodes" was
"read at prereg-freeze" per A-41 but the value was never recorded in any
frozen material (PREREG_FREEZE.md, ALPHABET_S-X.md, units/ tree all
searched). Per the catalog it sets the churn level where a U win falsifies
D's caching claim — it governs the *interpretation* of U's win for D's
status, not any of U's three kill criteria. Not load-bearing for U's
verdict. The D-falsification implication of U's duel win stays provisional;
the rate itself is a §13-amendment item for Micah. No rate is asserted.

## A3. S equations — ADJUDICATED 2026-09-21 (not load-bearing)
PREREG_FREEZE.md lists θ_merge=0.15, ρ=1.5, σ_split=2.0 with brackets
(proposed, translation unverified). The implementation's integer-counter
translation (merge iff J ≥ 3 AND 2J ≥ 3(Ia+Ib) AND NOT (Ia+Ib) ≥ 2(J+1),
plus ring veto — `u_can_merge`, `cl/arm.zag`) is logged in the source header,
was fixed at the first working build, and was never refit mid-trial (per the
catalog's "decided, never fitted mid-trial"). U and the DReg comparator
share the identical `u_derive`/`u_can_merge` code path, so duel kills (i)
and (ii) are invariant to the exact S translation; M1 bars pass under this
translation. Not load-bearing for the verdict.

## A4. Comparator D — ADJUDICATED 2026-09-21 (RESOLVED)
Kill (ii) names "D-with-invalidation". Track-A arm D (self-cut organ
pipeline) uses a *different* derivation rule, so it cannot serve as "the
same derivation rule with persistent caching/invalidation" (ARM_SPEC.md).
The in-binary DReg comparator implements exactly that: `d_recall`
(`cl/arm.zag:1494`) calls the identical `u_derive` as `u_recall` (line 363),
then serves each derived unit from a persistent chunk registry +
materialized byte-copy cache, with lazy invalidation on edits
(`dreg_invalidate`). DReg is the faithful comparator per kill (ii)'s own
text; Track-A D is not an admissible substitute. RESOLVED.

## A5. M2 semantic mismatch — NOTED (not a block; refined 2026-09-21)
M2's bar assumes a learning system (ep0 < 95%, then climb to ≥99.5%). U is
a store: recall is 100% from episode 0 by construction. There is no learning
curve because there is nothing to learn. The ep0<95% clause is vacuous for
U. U maintains perfect recall throughout: PASS with note. This is a
category mismatch, not a failure.
Refinement (U11): the arm's reported "ep0" is measured *post-ingest*
(`t_m2` ingests before the first probe), so the frozen "ep0 (no ingest) must
score ~0" leak clause does not apply as written — U has no learning state
that could leak. ETC=1 on all tiers (criterion met at first probe and
sustained), beating the champion bars (≤3/3 T1, ≤5/5 T2/T3).

## A6. M4 interpretation — CORRECTED 2026-09-21 (adjudicated)
The earlier note ("0% means no damage (good)") was WRONG. Frozen §5 defines
M4 as **Revision success**: revision rate = REVISED/200 per class, bars
≥80%/class. The arm's t_m4 scores all-or-nothing (100.0 iff all 600 unit
verifications pass, else 0.0). An instrumented probe build (print-only,
`work/adjud/probe/`, not the arm) localized all 28 failures to the
claimed-span stage on code content-defect units; zero failures in
content-byte restore (400/400), boundary-defect revision (100/100), prose
(200/200). Honest per-unit M4: **content 372/400 = 93.0%, boundary 100/100
= 100.0%** — both ≥ the 80%/class bar. Kill rate 0 (no OP_KILL in t_m4):
no kill-substitution gaming. The 28 span mismatches are derived-unit/atom
misalignment (same phenomenon as M1-boundary 99.9%), not revision failures.

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

## A9. r10 corpus provenance — BLOCKED (noted; not verdict-blocking)
CORPORA.md says r10 should be deterministically built by committed
`build_10x.py` after 1x validation. A stray `r10/prose.bin` exists but
provenance is unverified. 10x is NOT attempted. Per the verdict sheet's own
convention, binding PASS verdicts stand at 1x (K2, L1, P, S, X, Y3, Y6, Z2,
Z3, Z6, Z7 all PASS at 1x; N PASS with 10x attempted-failed). 10x remains
future work; it does not block a binding 1x verdict.

## A10. Scorecard gaps closed in adjudication (2026-09-21, U11)
- **M9 stale fragment:** `work/r1-1x/m9-1x/fragment.jsonl` is pre-fix
  (e500/e1000=727848, wrapped edit positions). Adjudicated M9 uses the
  post-fix byte-identical runs (`work/dbg/m9_run1.txt`, `m9_run2.txt`):
  e0=175944, e10=175944, e50=203976, e100=727756, e200=727848, e500=727204,
  e1000=727204, rekey=0, hits=0 — plateau holds (bounded).
- **M4 fragment schema:** the arm emits `m4_content_tenths/m4_boundary_tenths`;
  the harness interface (`ARM_INTERFACE.md` §3) wants
  `m4_rev_boundary_tenths/m4_rev_content_tenths/m4_kill_rate_tenths/
  m4_killsub/m4_episodes`. Adjudicated mapping: rev_content=93.0,
  rev_boundary=100.0, kill_rate=0.0, killsub=false, episodes=500
  (400 content + 100 boundary units).
- **Memorizer controls:** the crew's custom runner omitted
  `memctrl-p2c-1x`/`memctrl-c2p-1x`. Both now run under the official
  double-run rule (`work/adjud/memctrl/`): rc=0, stdout IDENTICAL, no FATAL.
