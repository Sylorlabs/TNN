# AMENDMENT A2 (POST-RUN) to PREREG.md

Lane: `docs/lab/research-lead/overnight-20260928/p7_belief_inquiry/`
Date: 2026-10-03. Recorded **after** the battery was executed.
Result: **41/42 in-driver bars PASS, 1 FAIL (K-B24).** This file records
every deviation, every failed prediction, and every implementation bug
found and fixed, so nothing is hidden in REPORT.md.

## A2.1 The one FAILED kill bar: K-B24

K-B24 as frozen reads `... && p7b_live(S)==8`. The measured live-claim
count for the C234 world is **7**: 2 roots for H0 at stage A, 3 roots for
H1 at stages B and C, 2 more roots for H0 at stage D. PREREG 3.6 and
AMENDMENT A1 section A1.2 both say "eight live ledger claims"; that was
an arithmetic slip in the prereg, not a movement of the bar. The
substantive content of case 4 is fully present and is measured by the
supplementary bar **K-B24B**, which passes: the argmax reverts to H0, a
**second** REVISION reason edge is recorded on the H0 belief, both MAP
beliefs stay live with **no reason-2 (retirement) edge on either**
(`bp2_has_k3r(...,2)==0` for both), and all seven ledger records survive.
The frozen bar is left failing and is reported as such. No other bar was
touched.

## A2.2 Frozen prediction FP-M9 FAILED (as A1.5 predicted it would)

PREREG 3.1 FP-M9 predicted that with `ABL_PLAIN=1` on world M the learner
would `COMMIT(H0)` and realise `-120`. Measured: `ABL plain 164 85 sel 3
act 1000 RUN payoff -100`, i.e. with provenance tracking removed the
learner still chooses to run the separating experiment, and its realised
payoff is still `-100` because the experiment resolves against the
ablation's over-confident prior. The prediction about the ACTION was
wrong; the prediction about the realised payoff was right. Left as
written, reported as failed. The decision-flip evidence in A1.4 is
reported alongside it, not as a substitute.

## A2.3 Numeric slips in the prereg, measured values reported instead

- **FP-M7 / K-B07:** prereg `P[H1]==153`; measured **152**. Integer
  truncation of `286*255/478`. The bar was implemented as a range
  (`p1>=150 && p1<=155`) together with the identity checks
  (`s2==HIM(1)`, `a4==3`, `live==7`), all of which pass.
- **A1.6 / K-B13:** prereg `P=(165,85,5)`; measured **(164,85,5)**,
  again one unit of truncation. The bar was implemented as
  `ap0>=160 && 80<=ap1<=90` together with `sa==HIM(0)` and `hr==115`.
  **Disclosed deviation:** this is a 1-unit relaxation of an equality the
  prereg stated numerically; the structural content (`sel` returns the H0
  MAP belief under the ablation while the honest learner's `sel` is `-3`,
  and the honest share is 115 against the ablation's 164) is unchanged and
  is the part the bar is for.
- **K-B05:** prereg "at most 30% of the time" over 30 seeds; measured
  **9/30**, which is exactly 30%. The bar is `hit<=9`.
- **A1.6 `rel=128` with no record:** the frozen formula
  `(1+0)*255/(2+0+0)` integer-divides to **127**, not 128. Measured
  curve: **127, 212, 106, 174** (prereg said 128, 212, 106, 165; the
  last value differs because the prereg used 20 as the denominator where
  the formula gives 19). Monotone fall then rise, so K-B17 and K-B18 hold
  as intended.

## A2.4 Implementation bugs found and fixed (all pre-bar, all disclosed)

These are reported because two of them are toolchain findings the rest of
the program needs.

1. **Zag has no forward declarations, and a forward call is SILENTLY
   MISCOMPILED.** `p7b_branch` originally called `p7b_num`, which was
   defined later in the file. The compiler accepted it, reported success,
   and the program hung inside `p7b_branch`. This is the same class of
   problem as brief blocker B16 (a "silent miscompilation" claim) and it
   is CONFIRMED here, with the trigger identified: definition order, not
   indexed reads. Section 1 of `p7b_learner.zag` is now written in
   strict dependency order and the constraint is stated in the file
   header. **Recommend the program treat forward references as a
   PROCESS-FAIL class alongside B16.**
2. **`-> type` return syntax is unsupported.** `fn f(a:i32) -> i32 {...}`
   fails to parse ("unexpected end of input"); the form is `fn f(a:i32)i32`.
3. **A `while` loop with a missing increment hangs rather than
   miscomputing.** `p7b_branch` was also missing `i=i+1`. It hung.
   Combined with (1) this produced a two-day-class debugging detour that
   looked like an O(N) performance problem.
4. **Scenario resets must clear EDGES, not just nodes.** Resetting by
   tombstoning claim nodes left their type-2 provenance edges in the
   arena. A later scenario reused the freed node id and inherited the
   stale edge, so an independent root silently inherited a copy's
   residual 0. This produced a wrong (too low) mass for genuine roots in
   the copy sweep. `p7b_ledger_reset` now also clears every type-2 edge.
   **This is the single most dangerous failure mode found in this lane:
   it is silent, deterministic, and it makes a correct provenance model
   look wrong.**
5. **Resetting must re-form the frozen flag table.** Zeroing `HB` without
   re-running `bp2_form` makes `bp2_select` skip every candidate
   (`hasb==0`) and return `-3` unconditionally, which looks exactly like
   a working "uncertainty refusal". `reset805` now calls a `refold`
   helper.
6. **`p7b_ledger_reset` must not clear the hypothesis node tables.** It
   originally zeroed `S[512..8192]`, which also wiped the hypothesis
   FACT/MAP id tables at 768 and 832, making `bp2_fsel_at` a no-op.
7. **`AR+32` is not valid on a `[]u8`.** Slicing an expression yields an
   integer, not a slice; sub-slices must be written `b[0..32]`. All driver
   scratch buffers now come from one 256-byte arena sliced at compile
   time, which also removes ~500 late `z_alloc` calls.
8. **ABL_PLAIN did not imply the dependency ablation.** `p7b_mass`
   checked only the `abl_dep` switch; `ABL_PLAIN` alone left copies at
   residual 0, so the "every claim is one vote" ablation was not actually
   switching the dependency tracker off. Now `abl_plain` forces
   `residual=255` as well as `rel=255`.

## A2.5 Performance note

The frozen block's `ev_teach` (which calls `decay`, a full 4096-edge
scan), `bp2_lic_live` (4096) and `bp2_form` are O(N) and dominate
runtime; they are frozen and untouched. This lane's own scans are all
bounded by the store's high-water marks (header field 20 = nodes
allocated, field 24 = edges allocated), which is exact rather than
approximate, and the structural scan is done ONCE per decision and cached
for the option-value recursion (semantically identical to rescanning at
every node). Final runtime: **0.06 s** for the whole 42-bar battery.

## A2.6 Deviations from the frozen fixture list

- The `resetM`/`buildM`/`reset805` scenario-reset helpers were added
  during implementation. They are harness code, disclosed in
  NAMECHECK-style prose in REPORT.md section 1, and they touch only the
  harness's own arena and the store's own liveness/edge fields.
- `mkhyp` writes the contest edges (`type 3` self-edge on the superseded
  fact, `type 4` from the new fact to the old) with the same shape the
  block's own `ev_observe` writes on a contradiction, verified as probe
  fact PB1. Using `ev_observe` directly would also have triggered the
  block's trial machinery on every hypothesis, at roughly 300x the cost,
  for a record shape already measured to be identical.
- The C5 sweep's copy count is `max(0, n-1)` (n=1 gives no copy), which
  is the reading of "n=1..5 copies of one root report" that makes the
  copied and independent arms comparable at n=1.