# PINS DECISION — RDTDT BRIEF

**Flow:** RDTDT (Review → Debate → Test → Debate → Test), defined by Micah 2026-09-21.
**Question:** What should happen to the old learner-side `pins_add` mechanism, measured
against Micah's semantic ruling?
**Status:** Evidence complete. **No decision made — this brief presents evidence and
options; the call is Micah's.**
**Prior:** HTD (one debate+test pass), `PINS_DECISION_BRIEF.md` (committed `2f19a119ab1f`).
Working papers: `~/workspace/pins-rdtdt/` (REVIEW_MEMO.md, d1a/b/c, d2a/b/c, t1-1/2/3,
t2a/b/c results + logs). Repo tree was never modified during testing (all work on
scratch copies; git status clean throughout).

## 1. Micah's ruling (authoritative, settles the "what is it" question)

> "The learner can make something hard to remove but it can never make it permanently
> locked. Only a trainer or external force can do that — in training, and they can in
> production too, like if a user ran /force on TNN."

Learner pins = strength/importance (high erase cost, NEVER permanent, always reversible).
Trainer `fp_pin` = true permanent lock (training AND production `/force`).

## 2. Review — settled vs open

**Settled by HTD evidence (pure Zag, byte-identical reruns; not re-debated in RDTDT):**

- S1. `pins_add` (store.zag:149-157) violates the ruling 3/3 (Test 5): no erase-cost
  linkage (retract bit-identical pinned vs unpinned), no unpin path (de-facto permanent
  in-session), trainer cannot clear (103) or override the veto (pin survives its own
  content's erasure).
- S2. `pins_add` ≢ `fp_pin` on 10/11 semantic dimensions (Test 1, 84 checks); only the
  0/1/2 conflict vocabulary is shared.
- S3. Route-as-drop-in through `fp_pin` is empirically dead: learner identity → 101
  refused, protection silently disarmed, suite stays green (Test 3).
- S4. Exactly one call site in the live tree, and it is test code (`tests/test_pins.zag:30`);
  zero learner-side callers; the `forcepin.zag` header claim ("called from learner-side
  code") is stale (Tests 2, 3).
- S5. `test_pins.zag` is vacuous — never exercises the pin mechanism (Test 3 §5); and the
  frozen-verified suite stays green under a neutered `fp_check` (T1-VACUITY) — it never
  verified B.6 end-to-end.
- S6. `pins_add` writes zero audit records (Test 4).
- S7. Even the strongest attacker model (direct `pins_add`) cannot block a trainer
  RETRACT — the erase path consults only the FPStore (Test 2).
- S8. The pin's only behavioral effect is vetoing NEW proposals (delib.zag:700/707) —
  which the ruling does not sanction (it speaks only of removal difficulty) (Test 5).

**Genuinely open at RDTDT start (O1–O5):** fourth option? concrete repair design?
deprecation blast radius (digest replay, tape interop, prereg §14 governance)? stale docs?
vacuous-test hardening?

## 3. Debate round 1 — three positions

- **D1-A — fourth option: "sever the effect, keep the specimen"** (disarm-and-quarantine).
  The violations flow through the 3-line ELIMINATE read path, not the writer. Delete the
  read path; keep `pins_add` as an inert test fixture; add fail-closed Claim D to
  `static_audit.sh`. Smaller and more reversible than deprecation; preserves the four
  HTD probe tests' negative evidence. (`d1a_fourth_option.md`)
- **D1-B — repair into real strength.** Full design: erase cost = `ceil(s/25)` grounded
  contradiction citations enforced in `dlb_retract`; learner self-unpin pays full effort
  (anti-cheap-edit invariant); trainer override free; pin-dies-with-content; K-turn
  expiry; audit ops 31/32/33; **proposal-veto deleted** (ruling sanctions only removal
  difficulty). Position: repair is right, but `pins_add` is unsalvageable — deprecate
  now, build repair as new preregistered construction. (`d1b_repair_design.md`)
- **D1-C — surgical deprecation (Scope-S).** The brief's "zero behavioral delta" was
  measured at the wrong layer. Scope-S = delete only the writer `pins_add`; keep `Pins`
  shape, `pins_init`, `pins_check`, the `dlb_digest` fold, the always-0 `EV_PINRES`
  emission. Full struct deletion (Scope-F) breaks digests even with zero pins and fails
  frozen B.4 replay. Governance: PREREG §14 is the signature block, not a pins mandate —
  deprecation is compliance, not a rule change (§13 doesn't fire). BUT
  `FORCE_PIN_VERDICT.md:56` parked item 1 reserves the `test_pins` rewrite for Micah's
  explicit approval. (`d1c_blast_radius.md`)

## 4. Test round 1 — results

- **T1-1 → D1-A quarantine: SURVIVED, no kill conditions fired.** Inertness tripwire
  proves the veto genuinely gone (fails on live tree — not vacuous); Claim D fence fires
  correctly; all 3 HTD probes compile unmodified; D2 attribution gap closes; diff
  minimality verified (180 lines vs 349 for full deprecation; production delta = 4 lines
  removed). **Two corrections:** D1-A's literal T1a scenario was confounded (adopted-span
  pre-check); HTD Q3's "un-overridable veto" was MISATTRIBUTED (that R_R2 came from the
  dead-span pre-check on both trees, never from the pin — genuine pin-veto evidence was
  always S7b). Flag: `static_audit.sh` Claim B fails on both trees (blocks appending
  Claim D; needs an owner decision). (`t1-1_results.md`)
- **T1-2 → D1-B repair: FALSIFICATION GATE SURVIVED.** `dlb_consider` dispatches
  retracts entirely to `dlb_retract` and returns before the main loop — the cost gate
  lives in one function; no invasive changes needed. All 10 test groups PASS,
  byte-identical ×2 (Q1/Q2/Q3 at s=100, veto regression, audit completeness ×7 events,
  expiry, cheap-edit adversarial, force-pin regression, no-RNG). **Scope revised:**
  realistic 1–2 weeks (not 3–5 days); 2 prereg amendments blocked on Micah (R_R7 frozen
  §L, aux-on-RETRACT §B); strength-choosing policy out of scope; spike compiled against
  a stub, never the real `delib.zag`. (`t1-2_results.md`, spike `t1-2/spike.zag`)
- **T1-3 → D1-C blast radius: ALL FOUR MISSES CONFIRMED.** Scope-S digests byte-identical
  to baseline (sha `3ca6295e…`, N=3); Scope-F diverges on a zero-pin run; Scope-S replays
  a 964-byte tape bit-for-bit while Scope-F fails at frame 0's `pre_digest`; event
  namespace enumerated (base/Scope-S emit `{0×3, 100×3}`, Scope-F `{100×3}` only);
  hardened `test_pins` drafted — PASSES on base, FAILS under `fp_check`-neutered
  mutation (current suite stays green: the live risk, confirmed); orphan catalog: 4
  evidence tests break compile under Scope-S. (`t1-3_results.md`)

## 5. Debate round 2 — position ledger

- **D1-A quarantine: SURVIVED T1, WEAKENED in D2.** Its T1e win was vs full deprecation,
  not Scope-S; its disarm has an unmeasured event-stream delta (deleting the always-0
  `EV_PINRES` emission breaks tape streams — T1-3 proved it, T1-1 never measured it);
  its Claim D fence cannot land (Claim B flag blocks the script it would append to).
  (`d2a_writer_fate.md`)
- **D1-B repair: SURVIVED, position refined to DEFER-with-trigger.** Buildable but: zero
  live callers; the ruling's learner half is permission, not obligation; a cost
  mechanism with no strength-choosing policy is a loaded gun with no aim; citation
  forgery an open gap; Micah's signature queue already deep. Quarantine judged the
  better stepping stone than Scope-S (keeps fixtures runnable, avoids orphan churn).
  (`d2b_build_or_not.md`)
- **D1-C Scope-S: STRENGTHENED.** Zero-delta at verdict AND artifact layers, proven on
  the real tree in T2. (`d2a_writer_fate.md`)
- **Brief's Scope-F (full deletion): DIED.** Digest-schema change, not cleanup.
- **Red team (D2-C) scoreboard:** A1 misdiagnosis partially lands (violation case narrows
  to one leg — correction, not kill); A2 partially lands (fence safety: Scope-S beats
  quarantine); A3 fails (B.4 replay is the named consumer); **A4 LANDS** (repair =
  cathedral for a ruling sentence: no consumer, no policy, strength trial owns the
  erase-cost question → PARK, not defer); A5 fails (harm nonzero; cheapest fix is a
  4-line deletion). Strongest remaining doubt after D2: the fence question — resolved
  in T2 (see §6). (`d2c_redteam.md`)
- **D2-A verdict: the writer dies — Scope-S.** "No Claim D proposed — the compiler is
  the fence." D1-B sides with deletion (already deprecates `pins_add`); D1-A left alone
  on keeping the writer.

## 6. Test round 2 — results

- **T2-α → Scope-S on the real tree: ALL PASS.** 9-line deletion (`pins_add`,
  store.zag:149-157) compiles; 4 suites byte-identical to baseline (shas match T1-3);
  all 8 digest logs one sha `3ca6295e…`; B.4 replay 964/964 bytes; zero `pins_add`
  definitions in buildable code; 10 call sites all in the 4 orphans, all compile-fail
  (`call to unknown function 'pins_add'`) — the compiler fence, working. Dead reader
  proven: `pins_check`→0 on 40/40 spans, pins-fold bytes constant. Hardened FP suite:
  N=5 PASS on Scope-S tree, FAIL under mutation (rc=1). Orphan disposition drafts
  written (unapplied). **Fence-audit note: quarantine's safety case is "assumed, not
  operational"** — Claim D's would-be gate path is a manual script step with no CI, no
  owner, and the script currently FAILs on the pristine tree. D2-C's T2-A2a demand
  resolves against quarantine. (`t2a_results.md`)
- **T2-β → misattribution audit: 7 claims adjudicated.** CONFIRMED (5): Q1 (retract
  bit-identical, no pre-check confound possible — retract branch precedes pre-checks),
  Q2 (zero removal symbols tree-wide), Q3a (pin survives erasure — `pins_check`=1
  post-retract), D1/S7b (genuine pin veto: ELIMINATE step, EV_PINRES=1), D2 (ledger
  tails identical; only step events disambiguate). MISATTRIBUTED (1): Q3b — the
  "un-overridable pin veto" 3/2 was the HS_KILLED dead-span pre-check (zero steps; pin
  armed but never consulted). CONFOUNDED (1): D1-A's literal T1a (HS_ADOPTED pre-check;
  fresh-span amendment stands). No additional pin-caused differential surfaced.
  Two stale labels flagged for correction before any verdict sheet ships
  (`test5_compliance.zag` Q3 print; `test_selflock_probe.zag` S8 comment: gate event is
  302, not 202). (`t2b_results.md`)
- **T2-γ → repair-gap adversarial: two structural findings; PARKED.**
  (1) **De-facto-permanence renewal CONFIRMED:** indefinite renewal at zero citation
  cost — naive re-pin is a dup-noop, so every K−1 turns the attacker mints a fresh
  overlapping row at s=100 (free; `pins_add` has no cost gate) and free-cleans decayed
  rows. Over 3K+1 turns: cost-100 coverage held at every window edge, attacker paid 0
  citations, all steps audited (recognizable overseer signature). The design bounds
  each pin *row's* lifetime, not total pin-lifetime; expiry fails against an active
  renewer. Trainer override still breaks the cycle. (2) **Citation forgery 8/8** against
  the production verifier; hardened verifier blocks 7/8 but long co-mentions still pay
  n(100)=4 in full — structural, mechanical checks cannot close it. The suite is kept
  as the acceptance bar for any future gap-closure. (3) Confusion fence PASSES —
  confusion of learner pins with trainer force-pins impossible by construction (op is a
  compile-time constant). (4) **Consumer map: PARKED, not deferred.** Zero named
  consumers (strength trial has its own binary store-layer `pinned` bitfield and is
  BLOCKED awaiting Micah's rulings; felt-intensity prereg frozen with no policy
  output; `dlb_retract` consults only force-pin; appeal paths don't consult pins;
  force-pin complete) and zero positive delta (every D1-B mechanism is a port of
  existing machinery). Re-activation conditions: a consumer appears, the strength
  trial's verdict sheet explicitly requests the mechanism, or citation forgery gets a
  preregistered defense design. (`t2c_results.md`)

## 7. Corrected evidentiary record (quotable)

- **Q1 "hard to remove": VIOLATION — confirmed.** Retract of pinned vs unpinned span is
  bit-identical (1/7/4); no erase-cost symbol exists; no pre-check confound possible.
- **Q2 "never permanent": VIOLATION — confirmed.** Zero removal symbols repo-wide;
  append-only registry; `fp_unpin` → 103/101 on old pins; only clear is destroying the
  deliberator.
- **Q3 "trainer supremacy": VIOLATION — confirmed as corrected.** What stands: the
  trainer erases the content but the pin survives erasure (`pins_check`=1 post-retract),
  and no trainer path clears or overrides it. What is RETRACTED: the "un-overridable
  pin veto" framing — the cited 3/2 was the HS_KILLED dead-span pre-check (span-lifecycle
  hygiene), not the pin. The genuine pin veto was always S7b (fresh span, ELIMINATE,
  EV_PINRES=1).
- **D1 (unaudited trainer-irremovable proposal veto): confirmed**, narrowed to S7b.
- **D2 (split attribution trails): confirmed** — ledger tails identical for old- vs
  fp-veto; only step events disambiguate.

## 8. Options — evidence and costs (no decision made)

**Option A — Scope-S surgical deprecation (delete only the writer `pins_add`).**
What: 9-line deletion (store.zag:149-157). Keep `struct Pins`, `pins_init`,
`pins_check`, the `dlb_digest` pins fold, `dlb_new` init, the always-0 `EV_PINRES`
emission. The retained ELIMINATE read path is provably dead with no writer.
Evidence: zero delta at verdict AND artifact layers on the real tree (T1-3, T2-α);
B.4 replay 964/964 bytes; compiler-as-fence proven (orphans fail with exactly
`call to unknown function 'pins_add'`). Cost: 4 orphan evidence tests need
disposition (drafts written, unapplied — §9); doc corrections ride along
(store.zag:135, OPERATIONALIZATION.md, forcepin.zag:16, this brief's predecessor).
Needs: Micah's two sign-offs (§9).

**Option B — Quarantine (D1-A: keep writer as inert fixture + Claim D fence).**
Evidence: survived T1 (inertness proven, fence statable, diff minimal vs full
deprecation). Weakened in D2: event-stream delta unmeasured-then-proven-real by T1-3;
safety case "assumed, not operational" (T2-α fence audit). Viable only as Micah's
reversibility-preference fallback, and only after the Claim B flag is resolved by an
owner decision.

**Option C — Repair into real strength (D1-B design).**
Evidence: buildable and contained (T1-2 gate survived; 10/10 groups pass). PARKED per
T2-γ kill-bar: zero consumers, zero positive delta, plus two structural gaps found
late (renewal defeats expiry at zero cost; citation forgery 8/8, structural). Realistic
cost if reactivated: 1–2 weeks + 2 prereg amendments + strength-choosing policy (out of
scope; adjacent to felt-intensity). Re-activation conditions (§6). Not recommended now.

**Option D — Do nothing.**
Killed by the red team: harm nonzero (architectural permission for a ruling-violating
mechanism; a frozen suite blessing that behavior; live old/FP attribution ambiguity).
The cheapest fix is a 4-line production deletion, not churn.

**What the evidence supports (not a decision):** every surviving empirical claim points
at Option A; Options B/C/D each have a recorded kill or park against them. The
remaining steps are Micah's sign-offs, not further tests.

## 9. Pending Micah decisions (explicit)

1. **Deprecation scope sign-off** (T1-GOV): Scope-S recommended by evidence. Dated note
   appended to `FORCE_PIN_VERDICT.md`.
2. **`test_pins` rewrite approval** (`FORCE_PIN_VERDICT.md:56` parked item 1): the
   frozen-verified test must be rewritten; the hardened FP suite is drafted and tested
   at `~/workspace/pins-rdtdt/t1-3/harness/t13_hardened.zag` and deliberately NOT
   copied into the tree pending his word.
3. **Orphan dispositions:** `test_pins.zag` → REWRITE (needs #2);
   `test_selflock_probe.zag` → RETIRE-WITH-NOTE (port S4/S5 fp sections);
   `test4_audit.zag` → RETIRE-WITH-NOTE (Scenario B keeper extracted);
   `test5_compliance.zag` → RETIRE-WITH-NOTE or PORT (fp-path assertions kept; stale Q3
   label corrected). Drafts in `t2a_results.md`.
4. **Stale labels** (correct before any verdict sheet ships): `test5_compliance.zag`'s
   `"(3/2 = pin veto, un-overridable)"` print; `test_selflock_probe.zag`'s S8 comment
   (gate event is 302, not 202).
5. **Claim B flag:** `static_audit.sh` Claim B fails on the pristine tree (over-broad
   grep counts harness-actor fp calls in `tests/`) — owner decision needed regardless
   of scope choice.
6. **Repair re-activation** (parked): only if a consumer appears, the strength trial
   requests it, or citation forgery gets a preregistered defense.

## 10. Artifacts

- This brief: `units/teachers/learner/forcepin/PINS_RDTDT_BRIEF.md` (this file).
- Prior HTD brief: `units/teachers/learner/forcepin/PINS_DECISION_BRIEF.md`.
- Working papers (not committed): `~/workspace/pins-rdtdt/` — REVIEW_MEMO.md,
  d1a/d1b/d1c_fourth_option/repair_design/blast_radius.md,
  d2a_writer_fate.md, d2b_build_or_not.md, d2c_redteam.md,
  t1-1_results.md, t1-2_results.md (+spike.zag), t1-3_results.md,
  t2a_results.md, t2b_results.md, t2c_results.md (+t2c.zag forgery suite),
  full run logs and SHAs under each `t*/` dir.
- Pre-existing evidence: `~/workspace/pins-htd/` (debate_A/B/C.md, test1–test5).
- All testing: pure Zag, no RNG in any AI decision path, byte-identical reruns
  (N=3–5 + allocator perturbations where applicable). Repo tree never modified during
  testing; no binaries, `.zag-cache`, or `.zagd.semantic-ready` committed.
