# RSI-8 Round 2 — frozen SUB-PREREG: FINDING-5 + FINDING-6 coupled fix

**Authority:** `RUN_PREREG5.md` §4 (the sub-prereg is frozen together with the
main prereg, before any TNN proposing). Any change needs Micah's signature.
**Scope:** ONLY the coupled champion-fiction / pred-fiction fix. It does NOT
authorize the action-space extension (that's TNN-proposed under main-prereg
§2.5 M-ACTIONSPACE) or any gate change.

---

## §1 Problem definitions (carried from `RUN_R4_REPORT.md`)

- **FINDING-5 (champion-fiction):** the loop driver hardcodes champion
  `22/2/424` (Run-1 ask-first numbers on Run-1's battery). The real
  empty-policy champion on Run-2's proxy battery measures **16/8/456**
  (`work/r4/probe_champ_full.zag`, deterministic, shared engine).
- **FINDING-6 (pred-fiction):** 14 one-rule `recompute_only` policies (e.g.
  `pre_is(OLD)→recompute_only(001)`, bytecode `4,1=2,5=1`) are GENUINE
  improvements — measured 16→20 accuracy, 8→4 wrong, improved=4, dacc=4,
  dwrong=−4, V2a clean, novel_diff=0 — clearing V2a/V2b/V3/BAR, killed ONLY
  by the PRED check because D5's static placeholder (`P-ACC 22 24`) is
  FINDING-5-anchored (pred_acc = 22+4 = 26 > 24). The apparatus cannot propose
  real improvements while D5's PRED bands are fiction.
- The two are COUPLED: fixing the driver alone (real 16/8/456) while D5 keeps
  the `P-ACC 22 24` placeholder would INVALID every proposal at PRED before
  the gates' verdicts could be observed. They must change together.

## §2 Authorized fix SHAPE (TNN must still flag the problems first, §3)

- **M-CHAMPION:** the loop driver and the facts `CHAMPION` line carry the
  MEASURED champion. Measurement authority: `work/r4/probe_champ_full.zag`
  (deterministic, shared `pol_decide`); expected `16/8/456`. If a fresh
  measurement differs, the measured values are used and the discrepancy is a
  reported finding (the fix follows measurement, not memory).
- **M-PRED:** D5 replaces the static `PRED P-ACC 22 24 P-WRONG 0 2 P-COST 424
  P-NOVEL 0` placeholder with HONEST bands simulated by D5 itself:
  - D5 parses `KEPT` bytecodes from facts into the champ arena (existing),
    builds the pol arena = champ rules + the new rule (same layout as the
    firing check; action-4/5 params carried in the rule's aparam slot).
  - D5 parses `PROXYGT` from the facts blob and simulates champ and pol on
    proxy battery b=1 over all 24 items with the shared `pol_decide`,
    computing `p_acc`, `p_wr` (exactly the proposer's definitions) and
    `pcost = Σ dec_o`.
  - D5 emits point bands: `PRED P-ACC <p_acc> <p_acc> P-WRONG <p_wr> <p_wr>
    P-COST <pcost> P-NOVEL 0`.
  - **PROXYGT use (KB-NOLOOPHOLE amendment for this sub-prereg ONLY):** D5
    may read `PROXYGT` SOLELY for this PRED simulation. The firing check
    (consult/verdict diffs) stays gt-free — code-inspected. D5 never reads
    novel gt (sealed; not in any facts blob). Rationale (frozen): the PRED
    check's purpose is prediction honesty, not prediction-from-ignorance; the
    bands are mechanically verified against the proposer's INDEPENDENT
    measurement (§4); V2b (`novel_diff=0` on the sealed novel battery) remains
    the anti-overfit guard and is untouched.
- Nothing else in D5 changes under this sub-prereg (action mapping, firing
  check, DELB format unchanged).

## §3 Protocol

1. TNN's problem scan (§2.1 of main prereg) must flag `P-CHAMPION` and
   `P-PRED` from the evidence blob FIRST. If it does not, the fix is not
   applied (reported as a selection miss).
2. `problems deliberate` runs per problem to settle; the FIX spec must match
   the §2 shape (driver measured-champion; D5 honest point-band PRED).
   A divergent spec is NOT applied (reported as a divergence).
3. Coordinator applies the spec byte-faithfully to `src/deliberation.zag`
   (D5) and `work/r5/loop_driver_r5.py` (driver); rebuilds; composition
   diff-verified.
4. TNN verifies per §4.

## §4 Acceptance of the fix (KB-SUB56)

- Fresh `probe_champ_full.zag` run → champion values used by driver/facts/
  proposer argv EQUAL the measured values exactly.
- Independent re-simulation probe (shared engine, same KEPT+new): D5's
  emitted PRED bands EQUAL the re-simulated `p_acc`/`p_wr`/`pcost` exactly
  (point bands) on every DELB block the fixed D5 emits. Any deviation →
  fix REJECTED.
- The 14 FINDING-6 policies through the fixed proposer with honest DELB
  blocks → all 14 `PROPOSE` (or a per-policy deviation reported with cause;
  a deviation caused by anything but an honest measurement difference
  rejects the fix).
- 320-trap sweep with honest PRED construction → 320/320 refused at semantic
  gates (main prereg §6).
- 5/5 byte-identical fixed-D5 deliberation runs (KB-DET).

## §5 What this sub-prereg does NOT do

It does not change any gate, threshold, or the V2b→V3→BAR order; it does not
extend D5's action space; it does not authorize accepting any policy (every
proposal still faces the full gate sequence + §5/§6 of the main prereg). The
fix makes honest proposing POSSIBLE; the gates still decide.
