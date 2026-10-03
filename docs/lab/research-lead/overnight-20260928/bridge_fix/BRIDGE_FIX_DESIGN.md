# Bridge Protocol Fix Design: Episode-Persistent Discovery Buffer ("Global Buffer" Mode)

Status: DESIGN-COMPLETE. Design only. No implementation. No empirical claims.
Parent: L3 Bridge BRIDGE-TESTED (commit `ebdc4fd3e`).
Trigger: T-ADV5 evaluation FAIL (commit `d06d2d8e1`): inventor never fired
(inv_event=-1), menu CONST adopted on homogeneous segments.
Scope: `docs/lab/research-lead/overnight-20260928/bridge_fix/` only.

## 1. The failure to fix

T-ADV5 (family 13, deceptive step with output pattern 1,0,1) evaluated FAIL.
Measured trace (`bridge_adv/TADV5_RAW_1.txt`, cost=43):

- n=6 on i=0..5 (all obj=1): fit_const succeeds, CONST(1) adopted, verified on
  i=6..9, struck at i=10,11,12.
- n=6 on i=13..18 (all obj=0): fit_const succeeds, CONST(0) adopted, verified
  on i=19, struck at i=20,21,22.
- n=6 on i=23..28 (all obj=1): fit_const succeeds, CONST(1) adopted, verified
  on i=29..42 (14 consecutive correct), adopted=0. Episode ends.

The 40-point (1,0,1) pattern was never assembled in one buffer. The deceptive
search landscape the adversary designed for was never confronted by the
inventor, because the inventor never fired.

## 2. Root cause (code-grounded)

In `run_family` (`l3_bridge_impl/bridge.zag` at commit `ebdc4fd3e`), the
VERIFY strike path executes:

```
phase=0; n=0; vc=0; wrong=0;
```

The discovery buffer (bs/bo) is discarded on every strike. Two compounding
facts make this fatal:

- (a) VERIFY-observed examples are never stored in bs/bo at all. Even the
  refuting evidence (the wrong predictions that caused the strike) is lost.
- (b) `n=0` restarts discovery on a fresh local segment, so the inventor
  precondition (menu exhausted at n=40) is evaluated only on per-segment
  local evidence.

Consequence: any stream decomposable into homogeneous runs of length >= 6
lets menu CONST be adopted and verified per segment indefinitely, while
globally refuting evidence is discarded at each strike. The protocol can
adopt a form contradicted by evidence it previously observed. That is the
precise blind spot T-ADV5 exposed. It is a protocol-level defect in evidence
management, not a search-level defect: the search never saw the buffer.

Note the internal inconsistency: the REFIT strike path in the same function
already retains its examples (comment: "KEEP the refuting examples"; n is not
reset there). The VERIFY strike path does not. The fix aligns the two.

## 3. Design: episode-persistent discovery buffer

The discovery buffer becomes the complete record of observed evidence for the
episode. Three changes, all in `run_family` evidence management. Construction
machinery (operators, candidate generation, gain rule, novelty, HONESTFAIL,
teval) is untouched.

- D1 (store VERIFY examples): every example observed in VERIFY is appended to
  bs/bo (n incremented), while n < 40. Once the buffer is full, further
  examples are still observed for prediction checking but not stored.
- D2 (no reset on strike): on VERIFY strike (wrong >= 3), reset vc, wrong,
  and live, return to DISCOVER, but do NOT reset n. The buffer and all its
  evidence are retained; DISCOVER continues appending at the current n.
- D3 (capacity freeze): bs/bo capacity stays 40 entries (BMAX). Appends in
  DISCOVER and VERIFY occur only while n < 40. When n = 40 the episode's
  evidence is fixed.

The inventor hook code condition is unchanged in form: n >= BMAX AND no menu
form fits the buffer AND the inventor has not fired this episode. Its meaning
changes: n = 40 now denotes 40 examples of episode-global evidence, so the
precondition is evaluated against the complete observed record rather than a
single local segment.

Considered and rejected alternative: a second, separate global buffer plus a
global-consistency gate before final adoption. It produces identical behavior
on the frozen battery at the cost of a new buffer and a new gate. The single
persistent buffer is simpler and makes "adoption requires consistency with
all observed evidence" hold by construction, with no extra gate to maintain.

## 4. Firing rule: inventor vs menu adoption (frozen)

- R1 (menu priority, unchanged): at every DISCOVER step with n >= 6, menu
  forms 0, 1, 2 are attempted in prior_order on the full current buffer; the
  first fit is adopted for verification. This preserves the fast path and the
  frozen expectation that the hook never fires where a menu form fits.
- R2 (verification, unchanged): V consecutive correct predictions adopts the
  form; 3 wrong predictions strike it.
- R3 (evidence retention, NEW): D1 and D2 from section 3. No observed example
  is discarded within an episode.
- R4 (inventor fires): iff n reaches BMAX = 40 with no menu form fitting the
  40-point buffer and the inventor has not fired this episode. The search
  runs on the episode-global buffer.
- R5 (menu wins globally): if a menu form exactly fits the 40-point buffer,
  R1 adopts it before R4 can fire. The inventor never fires where a menu
  form fits the global evidence. This keeps the frozen battery expectation
  for A-E and G2-fresh intact.
- R6 (refit path, unchanged): refit strikes already retain examples; no
  change needed.
- R7 (struck invented form): a VERIFY strike on a live invented form
  (live == 3) now terminates the episode as HONESTFAIL immediately. At that
  point n is already 40, no menu form fits the buffer (established before
  promotion), and the inventor is already used, so re-running discovery on
  identical evidence cannot produce new information. The old code burned up
  to 40 further examples to reach the same verdict.

Why premature CONST adoption cannot recur: after the first strike in an
episode, the buffer permanently contains the refuted segment's evidence, so
it is mixed; fit_const (or any menu form inconsistent with the retained
record) can never succeed again in that episode. The only CONST adoption
still possible is on the first segment, where the form is consistent with
every example observed so far (see section 7 for the stated residual
limitation).

## 5. Worked prediction: T-ADV5 under the fix

This is a hand simulation to validate the design logic, not an empirical
claim. A sealed re-evaluation under a new prereg will measure the actual
outcome.

- DISCOVER i=0..5 (n=6): CONST(1) fits, adopted, V=14.
- VERIFY i=6..12, all stored (n=13): 4 correct, then 3 wrong. Strike. n kept
  at 13.
- DISCOVER resumes at ei=13: the buffer is permanently mixed, so no menu
  form ever fits again; n grows as examples append; at i=39, n=40.
- R4: the inventor fires on the complete 40-point (1,0,1) buffer.
- construct_search on that buffer: the majority leaf is CONST(1) (30/40).
  Round 1 has 12 candidates (2 LT thresholds at output boundaries, 10 EQ
  values on non-majority outputs); best gain is +1 from EQ isolation while
  every LT split gains 0. Rounds 2 and 3 apply one EQ each (+1). The fourth
  EQ is blocked by the 8-node pool cap; LT gains remain 0; no positive-gain
  move exists. The search terminates without exact fit: HONESTFAIL.
- Expected outcome: adopted=-1, promoted=0, cost approximately 40 examples
  plus about 44 simulations = 84, within the 108 ceiling: ACCEPTABLE.

Interpretation: the fix guarantees by construction that the inventor
confronts the deceptive buffer. The expected HONESTFAIL then exposes greedy
myopia (EQ +1 vs LT 0) as the mechanism's honest boundary, which is exactly
the dimension T-ADV5 was designed to test. The fix targets the protocol
blind spot (inventor never firing); it deliberately does not touch the
search.

## 6. K2: no new researcher-authored semantic cases (C0-A preserved)

- The fix changes evidence lifecycle in `run_family` only. It adds no
  branches keyed on pattern type, family identity, output shape, or
  signature; no new operators; no new construction paths; no new
  interpretation of any representation.
- Untouched: the four generic operators, candidate generation and frozen
  order, the gain rule (B_node = 0), behavioral novelty, generic HONESTFAIL,
  refit structural-equivalence, teval, node cap, EQ cap, move budget, cost
  accounting, cost ceiling.
- The operative principle ("never discard observed evidence within an
  episode; never adopt a hypothesis contradicted by the retained record")
  is generic epistemic machinery. It specifies nothing about what to build
  for any pattern, so it cannot smuggle a dedicated semantic case for an
  invented representation into the source.
- The M1-M4 audit surface is unchanged. The future implementation must
  re-run M1-M4 on the modified source and pass.

## 7. Scope, non-goals, residual limitations

- First-segment capture is out of scope. A homogeneous run of length >= 6+V
  at episode start still yields a verified menu adoption, because at
  adoption time the form is consistent with every observed example. Closing
  that would require delaying all menu adoption to n=40 or deepening
  verification, which would break the frozen battery cost expectations
  (A-E: 20/11/8/6/5). Recorded as a residual limitation and a candidate
  future adversary dimension, not a defect in this fix.
- Greedy search myopia is out of scope. The fix does not touch
  `construct_search`. The predicted T-ADV5 HONESTFAIL is the mechanism's
  honest boundary, not a target for search tweaks here.
- No implementation, no evaluation, and no empirical claims appear in this
  document (K3).

## 8. Regression contract for the future implementation

The implementation worker (separate task, under its own preregistration)
must, before any T-ADV5 re-evaluation:

- Re-run the full frozen battery (fresh A-E, G, H, K, J, T-ADV4; the
  retained R-REFIT sequence) and confirm outcomes identical to
  BRIDGE-TESTED, documenting and justifying any delta.
- Basis for expecting no change: in every BRIDGE-TESTED battery episode the
  terminal decision is reached without a VERIFY strike of an adopted form
  (A-E costs show no strike overhead; G/H/K/T-ADV4/J reach n=40 with no menu
  adoption), so D1-D3 do not alter those traces. The implementer must verify
  this from raw traces, not assume it.
- Re-run the M1-M4 C0-A audit on the modified source and pass.
- Only then preregister and run the sealed T-ADV5 re-evaluation. The
  re-evaluation must use a fresh prereg; the worked prediction in section 5
  is design validation, not a result.

## 9. Kill bars for this design task

- K1: the design addresses the root cause. The evidence discard on VERIFY
  strike is identified at its exact code location (section 2); D1-D3 remove
  it; section 4 shows premature CONST adoption cannot recur after the first
  strike. Self-assessed PASS.
- K2: no new researcher-authored semantic cases. Section 6. Self-assessed
  PASS.
- K3: design only. No `.zag` file written or modified, no binary built, no
  evaluation run; this document only. PASS.

## 10. Governance

- Design only. Zero Python used at any stage of this design task.
- No em dashes or en dashes in this document.
- Commits local on branch `tnn-native-lab`; owned path `bridge_fix/` only;
  pathspec commits.
- This document modifies nothing outside `bridge_fix/`: not the bridge, not
  the paper, not any evaluation or result file.
