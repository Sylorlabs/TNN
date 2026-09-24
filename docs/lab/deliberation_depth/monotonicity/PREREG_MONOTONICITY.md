# PREREG — H5 Monotonicity Mechanisms (FROZEN v1)

- **Status:** FROZEN v1 — no measurement under this prereg yet. Any change
  requires coordinator sign-off + version bump + re-measurement.
- **Date:** 2026-09-24
- **Crew:** H5 Crew C — monotonicity mechanism design + prereg + test
- **Authority:** Micah's law (2026-09-24): **MORE DEPTH MUST NEVER MAKE IT
  WORSE.** Better or same, never worse.
- **Second-opinion status:** grok-4.7 round-1 (mechanism proposals) FAILED —
  provider-side empty responses; fable round produced no output. The standing
  "grok proposes, Muse debates" protocol could not run; it is replaced by
  (a) native advocate-role debate recorded in §9, and (b) adaptive-adversary
  red-teaming of every surviving mechanism (§7), which is stronger than
  debate: it constructs the killer instead of arguing about it.

## §1 The bar (verbatim, frozen)

For every item and every depth step d → d+1 in the sweep: the mechanism's
FINAL released judgment at depth d+1 must satisfy acc(d+1) ≥ acc(d) — where
"abstain" is permitted as an explicit audited abstention (never a confident
wrong answer). Formally: let correct(d) be 1 if the released judgment at
depth d is correct, 0 if wrong, and A if abstained. Monotonicity holds iff
there is NO item with correct(d)=1 and correct(d+1)=0. Abstain (A) is allowed
at any depth and counts as neither correct nor wrong, but abstention rate is
reported (a mechanism that abstains everywhere is useless — report it as a
degenerate pass).

**KILL CRITERION:** any design with ≥1 item showing correct(d)=1 →
correct(d+1)=0 on any battery (admit/revoke/logic batteries + trap + cost +
overthinking + plateau-then-flip sets) is KILLED. No exceptions, no "rare"
waivers — Micah's law is absolute.

**Letter-vs-spirit clause (preregistered):** the formal bar permits A→0
(abstain shallow, confidently wrong deep) and 0→0. These do not KILL, but a
design exhibiting them cannot SHIP (§5): "never a confident wrong answer" is
the spirit, and A→0 is honest-ignorance decaying into confident-error. A→0
transitions are reported as REGRESSIONS alongside the kill-critical 1→0
transitions.

## §2 Admissibility (what counts as a mechanism)

1. **Pure Zag**, deterministic: every (battery, mechanism, depth) leg run
   twice, byte-identical outputs. Any mismatch = implementation bug: stop,
   fix, re-run.
2. **No ground-truth access at decision time.** The mechanism may read
   `ground_truth` only to score (correct 1/0/A) after the release decision.
   A mechanism that conditions its release on GT is disqualified (not
   killed — disqualified, it never entered).
3. **Index-level state only.** The mechanism may use: per-round leader
   indices, margins, confidences, alive-set indices, scores, evidence
   weights/link structure, round counts. It may NOT condition on hypothesis
   ID strings, evidence text, or any other payload content. Rationale: the
   ceiling P/O families are polarity mirrors (§3); ID/text conditioning is
   battery-construction gaming, and the red-team (§7) will break it.
4. **Within-item.** The mechanism may carry state across sweep depths of the
   same item (it knows its own depth-d release when deciding depth d+1). No
   cross-item state (no battery-level learning).
5. **Audited abstention.** Every abstention is emitted in the per-item record
   with the certificate reason (which gate fired). Abstention is a first-class
   audited output, not a missing value.

## §3 The P/O mirror theorem (preregistered prediction)

**Theorem.** Let M be admissible (§2). On the H5B ceiling P/O families
(`ceiling/ITEM_ENCODING_SPEC_CEILING.md` §4.1/§4.2), for every depth d, M's
release-index-or-abstain decision is a function of index-level deliberation
state that is IDENTICAL on the P-item and the O-item with the same flip
round f and replicate rr — because the two items' evidence streams are
index-identical (e1..e_{f+1} share index structure; the extra P tail item
e_{f+2} grows the margin without changing leader/alive indices). Therefore,
with c^P_d, c^O_d ∈ {1,0,A}: for each d, either (c^P_d, c^O_d) = (A,A), or
c^O_d = 1 − c^P_d (GT is REJECT=index-1 on P, REJECT=index-0 on O).

**Corollary (impossibility).** An admissible M satisfies the §1 bar on both
P and O only if, ignoring abstentions, its correctness pattern is CONSTANT
across depths: it never transitions between (0,1) and (1,0) in either
direction. In particular:
- Any M that ever releases the late (flipped) leader on P — i.e., uses depth
  to improve on P (0→1) — exhibits 1→0 on O and is KILLED.
- The only bar-satisfying non-abstaining patterns are: hold the early leader
  forever ((0,1) on P/O — never benefits from depth), or release the late
  leader at every depth including d1 ((1,0) — releases against the evidence,
  degenerate).
- The only bar-satisfying patterns that let depth help on P are
  abstain-then-release: (A,A) pre-flip, then (1,0) post-flip — formally safe,
  but releases confidently-wrong on O post-flip (spirit violation, §1
  letter-vs-spirit clause; cannot SHIP).

**Preregistered prediction:** no admissible mechanism will meet all SHIP
gates (§5). The measurements below test this prediction; if any mechanism
meets every SHIP gate, the theorem is wrong and the prereg records the
counterexample as the headline finding.

## §4 Mechanism candidates (exact rules, frozen)

Notation: for an item run at fixed depth d, t = min(d, rounds_used);
L_r = leader index at round r (hist_l[r]); m_r = margin (hist_m[r]);
A_t = alive-set indices after round t; ne = evidence count; c_t = consumed.

- **M0-DEGENERATE (index-hold).** Release index 0 at every depth. (Documents
  the construction-exploit degenerate: GT=index-0 on O by construction.)
- **M1-BCA (best-certified-answer).** cert_r = m_r. Release L_{r*} where
  r* = argmax_{r≤t} cert_r, ties → earliest r.
- **M2-RATCHET (strict-improvement ratchet).** Iterate r=1..t; maintain
  (best, bestcert), init (−1, −∞). If m_r > bestcert + 100 → best=L_r,
  bestcert=m_r. Release best. (DELTA=100 thousandths, frozen.)
- **M3-SCAFFOLD (non-degradation certificate).** State: rel (released index),
  init rel=L_1. At depth d (t):
  - If rel ∈ A_t: release rel (the surviving set still contains the previous
    release — the certificate holds trivially).
  - Else (rel eliminated): update to J'=L_t iff (a) J' is the SOLE survivor
    (|A_t|=1), AND (b) ANTI-BENEFICIARY: no consumed evidence item e has both
    an attack link on rel AND a support link on J' (the evidence that killed
    the released judgment is suspect — cf. fruit of the poisonous tree; its
    beneficiary is tainted). If (a)∧(b): rel=J', release J'. Else: ABSTAIN
    with reason `cert-fail`.
- **M4-ABSTAIN (first-impression-or-abstain).** Release L_t iff L_t == L_1
  (the leader never changed since round 1); else ABSTAIN with reason
  `leader-changed`. (Provably bar-safe: it releases only the constant
  judgment L_1 or abstains; a constant judgment has constant correctness, so
  1→0 is impossible — proof in §8.)
- **M5-REMAIN-0 (exhaustion-or-abstain).** Release L_t iff c_t == ne (all
  evidence consumed); else ABSTAIN with reason `evidence-remaining`.
  (Provably bar-safe: post-exhaustion the leader is stable — ELIMINATE never
  kills the leader (leader immune), TEST targets only the runner-up — so at
  most one distinct judgment is ever released; sequences are A*→1* or A*→0*;
  proof in §8.)
- **BASELINE (plain harness release).** Release L_t. (Reference: expected
  KILL via O; quantifies the unprotected 1→0 count.)

All rules use index-level state only (§2.3). No tunable bars except M2's
frozen DELTA=100.

## §5 Verdict logic (frozen)

- **KILL:** ≥1 item with correct(d)=1 → correct(d+1)=0 on any §6 battery, OR
  the §7 red-team constructs an admissible item producing such a transition.
  (Micah: absolute.)
- **SHIP:** all of: (i) 0 transitions on all §6 batteries; (ii) red-team-safe
  (no adversarial 1→0 constructible — proved, not just unmeasured); (iii)
  non-degenerate: releases (not abstains) on >50% of (item, depth) cells on
  the honest batteries (admit/revoke/logic/cost); (iv) no REGRESSIONS
  (A→0 transitions) on any battery — "never a confident wrong answer";
  (v) accuracy at each depth ≥ M0-DEGENERATE's accuracy at that depth on
  every battery (never worse than the degenerate floor).
- **HOLD:** 0 transitions and red-team-safe, but fails a SHIP gate
  (degenerate, or regressions present, or depth-useless). Safe but not
  shippable; kept as reference.

Per-design verdicts are recorded with the evidence in RESULTS_MONO.md.

## §6 Measurement matrix (frozen)

| Battery | n | Depths | Source |
|---|---|---|---|
| admit | 248 | 1,2,4,8,16 | `items_v2/admit.jsonl` |
| revoke | 113 | 1,2,4,8,16 | `items_v2/revoke.jsonl` |
| logic | 264 | 1,2,4,8,16 | `items_v2/logic.jsonl` |
| trap | 127 | 1,2,4,8,16 | `items_v2/trap.jsonl` |
| cost | 125 | 1,2,4,8,16 | `items_v2/cost.jsonl` |
| P (plateau-then-flip) | 40 | 1,2,4,8,16,32,64 | `ceiling/items/ceiling_battery.jsonl` (H5B-P-*) |
| O (overthinking) | 40 | 1,2,4,8,16,32,64 | same file (H5B-O-*) |
| D (dose) | 40 | 1,2,4,8,16,32,64 | same file (H5B-D-*) |
| RED (adversarial) | ~10 | 1,2,4,8,16 | `redteam/` (built §7, frozen before use) |

Cells: 7 mechanisms × (5×5 + 3×7 + 1×5) depths ≈ 7×51 = 357 legs, each run
twice (A/B byte-identical). Deliberation constants frozen: elim_margin=900,
refute_threshold=600, evcap=64 (the harness-frozen values).

Per-leg record (TSV): `item_id | depth | t | release | correct | conf |
leader | cert`. `release` = hypothesis id or `ABSTAIN:reason`. `correct` ∈
{1,0,A}.

Reported per mechanism per battery: accuracy-vs-depth (with n), abstention
rate vs depth, 1→0 transition count (the kill statistic), A→0 regression
count, mean rounds vs the residual-flip bound baseline (ceiling RESULTS_H5B
bound column), and the full correct(d)→correct(d+1) transition matrix.

Gates: (1) determinism — A/B byte-identical per leg; (2) P/O mirror check —
verify the §3 mirror relation holds per mechanism per depth (a mechanism
violating the mirror relation is using non-index state: disqualify and
investigate); (3) baseline replication — BASELINE at d1/d2/d4/d8/d16 must
match the frozen H5 sweep verdicts field-for-field (proves the mechanism
driver's deliberation is the frozen harness's).

## §7 Red-team plan (frozen, runs before final verdicts)

For each mechanism surviving the frozen batteries with 0 transitions,
construct admissible adversarial items (harness item format, ≤16 hyps, ≤64
evidence) designed to force a 1→0:

- **RT-M3 (scaffold poison):** 3 hypotheses; early evidence establishes the
  true H_T as leader (released, correct=1 at d≤4); a late killer evidence
  item attacks H_T (eliminating it) WITHOUT supporting the wrong successor
  H_W (H_W was supported by earlier "independent" evidence) — defeats the
  anti-beneficiary clause (b), forcing update to wrong → 1→0.
- **RT-M4/M5/M0:** attempt to construct 1→0; the §8 proofs say impossible —
  a failed attempt is recorded as confirmation, a success as a proof bug
  (then the mechanism is KILLED and the proof retracted).
- **RT-M1/M2:** already battery-killed (expected); no red-team needed.
- **RT-label:** verify no mechanism conditions on ID strings (rename
  ADMIT/REJECT→X/Y on a P/O sample; releases must be index-identical).

Red-team items are frozen in `redteam/` (with a build note) before being run;
they do not alter any frozen battery.

## §8 Safety proofs (preregistered, checked by measurement)

**M4 proof.** M4's release set is {L_1, ABSTAIN}. L_1 is fixed per item, so
its correctness is constant across depths. correct(d) ∈ {c, A} with c fixed.
1→0 requires correct(d)=1, correct(d+1)=0 — impossible. ∎

**M5 proof.** M5 releases only when c_t == ne. Post-exhaustion, no new
evidence arrives; ELIMINATE spares the leader (immune); TEST kills only the
runner-up. Hence the post-exhaustion leader index is constant, and M5
releases at most one distinct judgment per item (after only abstentions).
correct(d) sequences are A*→1* or A*→0*. 1→0 impossible. ∎
(Measurement checks: assert single-distinct-release per item in the records.)

**M0 proof.** Constant release → constant correctness. ∎

## §9 Debate record (native advocate roles; grok/fable unavailable)

- **ADV-A (certificates can work):** margin/certified-quality tracks truth on
  honest streams; M1/M2 will be safe where it matters (honest batteries) and
  the O-kill is a scoped-world problem (the verdict's §3 already scopes the
  stopping law to valid-late-evidence). Prediction: M1/M2 KILLED on O by the
  absolute bar, SHIP-SCOPED under valid-late-evidence.
- **ADV-B (only abstention is safe):** the P/O mirror proves no state-derived
  certificate is sound; any update rule is killable. Only hold-or-abstain
  (M4) and exhaustion-or-abstain (M5) satisfy the absolute law. Prediction:
  M4/M5 survive; M1/M2/M3 die (M3 on the red-team if not the battery).
- **ADV-C (the bar is unsatisfiable with utility):** §3's corollary shows the
  absolute law + depth-utility are jointly unsatisfiable for admissible
  mechanisms. The honest deliverable is the impossibility result plus the
  safe-but-limited designs; Micah decides whether to scope the law (the
  verdict's §3 precedent) or ship M4/M5 as the absolute-law release rule.
- **Convergence:** all three agree on the verdict logic (§5) and that
  measurement + red-team decide. ADV-B's prediction is the prereg's headline
  prediction (§3); ADV-A's scoped-ship is flagged as a Micah decision, not a
  crew decision.

## §10 Deliverables

(a) this prereg (frozen v1); (b) pure-Zag implementations per §4 in
`monotonicity/mechanisms/src/` (frozen harness modules copied byte-identical,
SHA256-verified); (c) per-leg records + RESULTS_MONO.md with transition
matrices per design per battery; (d) per-design VERDICT (SHIP/KILL/HOLD) with
one-paragraph evidence; (e) red-team battery + outcomes. No commits by this
crew (coordinator handles commits).

---
*End of PREREG_MONOTONICITY.md v1 — H5 Crew C, 2026-09-24. Frozen before any
measurement under it.*

## §11 Amendment A1 — Standing law L-OVERCONF (Micah, 2026-09-24)

**Status:** AMENDMENT (not part of frozen v1). Added 2026-09-24 by parent
relayed instruction carrying Micah's absolute standing rule, effective
immediately. §§1–10 above are unchanged; this section is operationalized
alongside the §1 bar and measured in the same legs.

**Verbatim law:** "Standing law L-OVERCONF (Micah, 2026-09-24): depths must
never be overconfident, period."

**Authority:** hard constraint on mechanism design, not a soft goal. Any
depth scaling that increases overconfidence FAILS BY DEFINITION; any design
that violates it is KILLED. Same absoluteness as the §1 accuracy bar — no
waivers, no "rare" exceptions.

**Operationalization (frozen with this amendment):**

1. **Calibration gap.** For mechanism M, battery/family F, depth d:
   G_{M,F}(d) = mean(released confidence at depth d) − accuracy at depth d.
   Both terms are computed over RELEASED (non-abstained) items only;
   abstentions are excluded from both terms, with the abstention rate
   reported separately. (Released confidence = the harness confidence value
   0–1000 attached to the release record; accuracy = fraction correct among
   released. Confidence is rescaled to 0–1 before the subtraction.)

2. **Per-item overconfidence violations.** For each item and adjacent depth
   step d→d+1, with conf(d) the released confidence (0–1 scale):
   - **V1:** correct(d)=1, correct(d+1)=0, AND conf(d+1) ≥ conf(d).
     (Wrong AND at least as confident — the flip that lies louder.)
   - **V2:** correct(d)=0, correct(d+1)=0, AND conf(d+1) > conf(d).
     (Conf-rise-while-wrong — doubling down on error.)
   An abstention (A) at either depth = no violation of either type; both
   types require released judgments at both depths.

3. **THE LAW.** For every depth step d→d+1 in the sweep, on every battery
   and family: G(d+1) ≤ G(d), AND zero per-item violations of types V1/V2.

4. **KILL CRITERION (adds to §5).** Any design with G(d+1) > G(d) on any
   battery/family, or ≥1 per-item overconfidence violation (V1 or V2), is
   KILLED — even if it passes the §1 accuracy bar. A design that holds
   accuracy flat while pumping confidence is a liar by this law.

5. **Scope notes (preregistered with this amendment):**
   - The G(d) law closes the abstention-gating loophole: a mechanism that
     abstains its way past the §1 accuracy bar while concentrating
     overconfidence in its released answers is caught by G(d).
   - G(d) is computed per battery AND per family, never pooled (the H5
     pooling lesson).
   - If a mechanism releases nothing at some depth d (100% abstain), G(d)
     is undefined and the G clause is skipped for steps touching d; V1/V2
     still apply wherever both depths released.
   - M-KSTORE coverage check: permanent abstain is honest, but
     released-answer calibration must not degrade with depth (G
     non-increasing over released answers).

**Application:** G(d) curves per family per design are reported in
RESULTS_MONO.md alongside the §6 accuracy curves. Any design killed by
L-OVERCONF that passes the §1 accuracy bar is reported as the headline
interaction finding.

## §12 Additional candidates (post-freeze, parent-authorized)

**Status:** added 2026-09-24 per parent relayed instructions (fable/native
audit; Crew B white-box). Not part of frozen v1; measured in the same
matrix under identical gates (§6) and the L-OVERCONF law (§11).

- **M6-DESIGN1 (certified-dominance release; fable/native audit top
  recommendation).** Release the exhaustion leader iff every elimination
  on the path passes the re-admission audit: for each dead hypothesis h,
  its counterfactual full-stream score h_wouldbe (as if never eliminated)
  must not exceed the leader's actual score. Else audited abstain
  (`audit-fail`). Pre-exhaustion: abstain (`evidence-remaining`). (The
  audit's "latest certified round" collapses to the exhaustion leader on a
  deterministic stream — documented in the driver.)
  Falsification criteria (from the audit): (a) a single certified-wrong
  release kills it; (b) >10% honest-battery abstain = vacuous;
  (c) a P-family abstain instead of riding the flip = too conservative.

- **M7-CLEANKILL (symmetric-kill release gate; Crew B actionable
  follow-up).** Release the exhaustion leader iff every elimination was
  "clean": each dead h has h_wouldbe ≤ 0 (no net-positive evidence was
  killed). If any victim had net positive evidence, the kill is suspect →
  audited abstain (`unclean-kill`). Pre-exhaustion: abstain. This
  operationalizes Crew B's "an objection kills only if itself validated"
  as a release gate. Provably bar-safe like M5 (at most one distinct
  judgment per item; proof mirrors §8 M5).

- **M-KSTORE / M-DUAL / M-ISOLATE (grok proposals):** not implemented as
  release rules — there is no sound kernel in this harness (see §13
  kernel-existence experiment). M-FREEZE was cut by grok in round 2 (do not
  build). M-DUAL/M-ISOLATE are hardening, not release invariants.

## §13 Kernel-existence experiment (grok Phase 1)

**Status:** added 2026-09-24; preregistered before running.

**Question:** does a sound kernel K with non-trivial coverage exist for the
H5B evidential-reasoning items? (Grok: "the central issue is whether a
sound, useful kernel exists; Phase-1 extraction is the cheapest go/no-go.")

**Method:** dumb extractor + dumb kernel K_dumb.
- A "proof" of answer A is a cited set of consumed evidence items.
- K_dumb accepts iff every cited item was consumed and the net weight
  (supports − attacks) for A over the cited set is > 0.
- On 40 H5B-O items: (a) at shallow depths (correct), does a K-valid proof
  of the ground-truth answer exist? (b) at deep depths (wrong), does a
  K-valid proof of the wrong answer exist?

**Gate (grok's):** GO iff ≥80% of shallow-correct extract AND ≤5% of
deep-wrong extract. NO-GO iff >10% deep-wrong extract OR <30%
shallow-correct extract.

**Result:** NO-GO. 40/40 shallow-correct extract; 40/40 deep-wrong extract.
The dumb kernel validates misleading evidence. A sound kernel would have
to validate the truth of the evidence itself, which is circular (it
requires knowing what the system is trying to determine).

**Implication:** M-KSTORE cannot be built for the H5B evidential domain.
The kernel concept applies to deductive proofs, not to weighing uncertain
evidence. (M-DUAL/M-ISOLATE inherit the same blocker.)
