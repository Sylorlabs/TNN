# DEBATE B — Can percept self-flagging be calibrated?

**PAM rebuild, round 2 · Debate crew B · 2026-09-22**

## 1. Brief

**Question.** H2 ("Executable Percept Programs") died in round 1 on kill-2 alone: only 42/108 = 38.9% of wrong high-confidence percepts self-flagged FAIL/UNRESOLVED (bar: 90%). Everything else passed — including the load-bearing finding that the memory contract installs 0 falsehoods in 10,000 trials where the contract-less ablation installs 186. The gate withheld all 108 wrong percepts from installation. So: the *gate* is calibrated; the *programs* are not. Can percept self-flagging be calibrated to 90%+, or is self-assessment by the percept itself a dead end?

**Frozen facts (verified from `forks/H2/VERDICT_H2.md`, not re-derived).**

| Fact | Value |
|---|---|
| Trials | 10,000 (5,000 normal + 5,000 adversarial) |
| Wrong high-confidence percepts (conf ≥ 700) | 108 |
| Self-flagged FAIL/UNRESOLVED | 42/108 = 38.9% (kill-2 bar: ≥90%) |
| Wrong percepts withheld from installation by the gate | 108/108 |
| False permanent installs | 0/10,000 (kill-1 bar: ≤3%) |
| Ablation (no contract) false installs | 186; disposition Δ 45.3% |
| Mean primary accuracy | 0.8426 · p95 ops ratio 0.385 · adversarial accuracy 0.7272 (bar 0.7125) |
| Determinism | 60×3 byte-identical reruns; ledger `a1a8b21f…` verified |

**Method.** Three-round structured debate, proposition vs opposition, every position steelmanned before rebuttal. *Conduct note: this subagent runs at depth 2/2 and cannot spawn subagents, so the "swarm teams" were executed as explicit adversarial role-play in writing — named teams, separated voices, rebuttal rounds — rather than as separate agents. The two external 2nd opinions (below, verbatim) are from live model calls, not role-play.* Laws: zero RNG in decision paths, pure deterministic computation, plain language, no post-hoc rewrites of round-1 bars.

**Teams.**
- **PROPOSITION ("Calibration is possible")** — champions positions (a), (b), (e), (f), and two added positions (g), (h).
- **OPPOSITION ("Self-flagging is a dead end")** — champions positions (c), (d), plus the homunculus objection, the bar-gaming objection, and the post-hoc-rewrite objection.

**Positions on the table** (steelmanned in §2; (g) and (h) added by the proposition in round 1):
- (a) Confidence calibration via held-out prediction checks — the percept must predict something outside its source span.
- (b) Withholding-first defaults — percepts are UNRESOLVED until proven otherwise.
- (c) External audit — a separate deliberate mechanism re-checks percepts; self-flagging is the wrong layer.
- (d) Deliberation-in-the-loop — percepts never self-install; deliberation ratifies.
- (e) H2's bar was wrong — the gate is the real mechanism; rewrite the bar to test installed falsehoods. (H2 stays dead under the frozen bar regardless.)
- (f) Adversarial training of the flagger — with zero RNG and no learned cheating; "training" = deliberate audited revision vs a frozen adversarial suite.
- (g) *Added:* the cross-validation principle — a flag must be computed over **independent evidence**; re-running tests on the same span is zero-information.
- (h) *Added:* two-tier flagging — a cheap always-on invariant screen plus the program's own tests.

---

## 2. Round 1 — Opening positions (steelmanned)

### (a) Held-out prediction — Proposition
H2's contract §(c).4 already demands "at least one successful prediction outside the original source span" before a PASS may install. The 38.9% failure is what happens when programs judge themselves on the *same* misleading evidence that produced the wrong verdict. The fix: the result field is only valid if computed over independent evidence — a held-out temporal span, a spatially disjoint region, or a cross-modal span. This is ordinary cross-validation logic: you cannot validate on your training data. Deterministic, zero-RNG, and directly testable: P(flagged FAIL/UNRESOLVED | wrong, high-conf) measured on held-out evidence.

### (b) Withholding-first — Proposition
The 38.9% shows programs are PASS-happy; the bias is in the default. Given asymmetric costs — a false permanent install is irreversible, a delayed install is cheap — UNRESOLVED-until-proven is the correct decision-theoretic default. H2's own §(c).6 already keeps installation reversible until external predictions confirm; (b) moves that caution one step earlier, into the result field itself.

### (c) External audit — Opposition
Self-assessment is structurally uncalibratable — the homunculus problem. The program that asserts "dog" cannot be the authority on whether "dog" is right. H2's own data proves it: the *gate* (external to the program) caught 108/108; the programs caught 42/108. "Calibrated self-flagging" is a contradiction in terms: the moment you add a mechanism that reliably catches the program's errors, you have built an external auditor, not a self-flagger. The safety mechanism is the gate. Name it honestly.

### (d) Deliberation-in-the-loop — Opposition
Installation is a decision under uncertainty, and decisions belong to deliberation, which weighs the percept against alternatives, costs, and the provisional buffer. Percepts never self-install; the gate withholds; deliberation ratifies promotions and resolves conflicts between surviving programs (already in H2 §(c).4–5). The program's self-result is *evidence* deliberation weighs — it is never the verdict.

### (e) The bar was wrong — Proposition
Kill-2 tested the wrong layer. The frozen hypothesis §(c) explicitly makes the *contract/gate* the safety mechanism: "prevents a high-confidence wrong conclusion from becoming durable merely because its initial evidence looked persuasive." The system-level property held at 0/10,000. A bar that kills a system with a perfect safety record because a *component* isn't 90% self-aware tests a property the architecture deliberately delegates. Round 2 should bar *installed falsehoods*, with program self-flagging as a scored diagnostic. (Conceded up front: H2 stays dead under the frozen bar. This is prospective only — no resurrection, no HARKing.)

### (f) Deliberate revision of the flagger — Proposition
"Training" with zero RNG and no learned cheating means: deliberate, audited revision of the flagging predicates against a frozen adversarial suite. (1) Frozen suite with ground truth. (2) Flagger failures ledgered per trial. (3) TNN's deliberation proposes deterministic predicate revisions — RC1 precedent: TNN controls 100% of its reasoning machinery, 0% of the constitution. (4) Constitutional veto: any revision that improves the flagging bar by degrading the paired recall bar, or weakens integrity, is refused. (5) Every revision ledgered with before/after scores on held-out adversarial trials. No RNG anywhere; bar-gaming is constitutionally refused and made visible by the paired bar.

### (g) The cross-validation principle — Proposition (added)
Information-theoretic point the other positions assume but never state: re-executing a deterministic function on the *same* input yields zero new information. A program "self-checking" its tests on the identical evidence span cannot, even in principle, catch errors the first pass missed — unless the check is a *different* function, in which case it is the auditor again. Therefore calibratable self-flagging requires the flag to be a function of *independent* evidence: held-out span, disjoint region, cross-modal span, or future window. The flag is still computed *by the program* (same tests) — the independence lives in the data, not the judge. This is the precise boundary where (a) works and naive self-checking cannot.

### (h) Two-tier flagging — Proposition (added)
Tier-1: cheap, content-independent invariants, always on — source spans addressable? witness count ≥ threshold? temporal persistence minimum met? contradiction scan clean? Any failure forces UNRESOLVED regardless of what the program's tests say. Tier-2: the program's own tests. Rationale: the 38.9% shows tests pass on misleading evidence; tier-1 invariants check the *warrant's form*, not its content, so adversarial content cannot fool them the same way. Tier-1 gets its own calibration bar, stated separately from the program's tests.

---

## 3. Round 2 — Clashes and rebuttals

### Clash 1 — The layer question: who computes the flag?
**Opposition:** (g) concedes the point. The moment the flag depends on *fresh evidence the program didn't see*, the calibrating work is done by the evidence pipeline that selects the held-out span, runs the tests, and adjudicates — an external auditor wearing the program's clothes. Worse: who chooses the held-out span? If the program chooses, it picks a congenial span (deterministic selection rules are gameable by the same adversary that fooled the tests). If an external mechanism chooses, that mechanism *is* the auditor. Either way, pure self-flagging is dead.

**Proposition rebuttal:** The selection rule needs no adversary-proof cleverness — it is frozen and evidence-driven: "the next disjoint temporal window of equal length," "the spatially disjoint region." Deterministic, no choice, no gaming surface beyond the input the adversary already controls. And we are not claiming the program is the final authority — we claim its self-result can be made *informative* (calibrated as a likelihood input to the gate), which is weaker and achievable. The gate still decides.

**Opposition rebuttal:** "Informative, not decisive" retreats from kill-2's 90% demand — fine, but then admit kill-2's framing was wrong (that is (e)), and that the surviving claim, "the program emits a useful uncertainty signal," never needed a 90% bar. The debate question was whether self-flagging can hit 90% *as a safety mechanism*. If the answer is "only as a soft signal under an external gate," then (c) won: the safety mechanism is the gate.

**Judge's note:** the crux of the whole debate. Resolution in §5: (c) is architecturally correct — the gate is the safety mechanism — AND (a)/(g) survive as the calibration method for the *signal* the program feeds the gate. The 90%-style bar belongs on the *system's* withholding behavior, not on the program alone. That is (e)'s repair.

### Clash 2 — Withholding-first: default or dodge?
**Opposition:** (b) games any flagging bar vacuously: withhold everything → 100% of wrong percepts are UNRESOLVED → bar passes with zero calibration. Without a paired recall bar, (b) is refusal, not calibration. And once paired ("≥85% of correct percepts reach PASS"), "when does a withheld percept get promoted?" is the original calibration problem with a different default. (b) relocates the problem; it does not solve it.

**Proposition rebuttal:** Relocation *is* the solution under asymmetric costs. And the promotion rule — "PASS requires successful prediction outside the source span or cross-modal corroboration" — is *easier* to calibrate than the demotion rule, because it is a positive evidence requirement, not self-diagnosis of error. Proving "I have fresh confirming evidence" is mechanistically simpler than proving "my reasoning was flawed." The 38.9% was a failure of self-diagnosis; promotion-by-fresh-evidence sidesteps self-diagnosis entirely.

**Opposition rebuttal:** "Sidesteps self-diagnosis" = abandons self-flagging. (b)-as-promotion-rule is (a) with the default flipped — so (b) standalone dies and (b)-merged-into-(a) survives. Cost note: chronic withholding means the system can never act on first sight; on streaming input, "UNRESOLVED until the future confirms" risks decision paralysis. Any paired bar must cover decision latency/accuracy, not just recall.

### Clash 3 — Was kill-2 the wrong bar?
**Opposition:** Frozen prereg is law. H2's authors wrote kill-2; they chose to test program self-calibration as load-bearing. Discovering post-hoc that the bar "really" tested the gate is HARKing and destroys the credibility of every other kill in the program. H2 stays dead — period. Moreover, kill-2 wasn't stupid: a 90%-self-aware program is genuinely desirable (it is H2's §(e) beauty claim — "every percept is a claim together with its own experiment"). The data says programs *can't* do this. That is a real scientific finding, not a bar bug.

**Proposition rebuttal:** Agreed, H2 stays dead — (e) never argued resurrection. The *finding* ("programs can't self-diagnose at 90% on same-evidence") is real and keeps its label. But the *architectural* conclusion — "therefore the gate must decide" — was already in the hypothesis §(c); kill-2 tested a property the design never needed for safety. The repair applies to a *new* hypothesis under a *new* frozen prereg — which is exactly what round 2 is for.

**Judge's note:** consensus — keep the kill, repair prospectively. The clash dissolves into process.

### Clash 4 — Deliberation: who ratifies, and at what cost?
**Opposition:** Compute kills naive (d). Deliberation per percept blows the efficiency bar (H2 hit p95 0.385 *without* per-percept deliberation). Triage is mandatory: the gate dispositions install/withhold/escalate; deliberation sees only escalations. But then the "flagger" is the gate's escalation rule — back to (c). (d) survives only as "deliberation handles the hard cases," which was already in H2 §(c).4.

**Proposition rebuttal:** Concede triage. Refined (d): deliberation ratifies *high-stakes promotions* from UNRESOLVED to PASS and resolves *conflicts between surviving programs* (H2 §(c).5). The gate handles bulk dispositions deterministically. Calibration then splits cleanly: gate rules calibrated by (f)-style deliberate revision; deliberation's ratifications calibrated by their own ledgered track record against eventual ground truth — auditable, deterministic.

### Clash 5 — What does "training" mean with zero RNG and no cheating?
**Opposition:** If the flagger needs an external suite plus deliberation plus a constitutional veto to become calibrated, the flagger isn't *self*-calibrating — the *system* is calibrating it. That is (c) laundered through fancier vocabulary. Also note the concession this forces: at any given time the deployed flagger is uncalibrated-by-construction (38.9% is the starting point), and safety during that period comes from the gate. (c) wins again.

**Proposition rebuttal:** The self/system distinction dissolves once the flagger is part of TNN and TNN revises itself — RC1 proved the architecture draws the line at constitution (0% TNN-controlled) vs machinery (100% TNN-controlled). The flagger is machinery; TNN calibrating its own machinery *is* self-calibration at the brain level, even if not at the percept-module level. Precise answer to the debate question: **not by the percept alone** (module-level self-flagging is a dead end — conceded to (c)); **yes by the brain deliberately calibrating its percept machinery** (system-level self-calibration is viable — (f) survives with teeth).

**Opposition:** Concession accepted — clean synthesis. (f) survives *as* system-level self-calibration, which is (c) + deliberate revision. Load-bearing requirement: the constitutional veto must be *tested*, not assumed — the suite must plant bar-gaming temptations (trials where flag-everything-UNRESOLVED would pass the flagging bar) and the veto must be observed firing.

### Clash 6 — (g) vs the homunculus (the still-image boundary)
**Opposition's best shot:** the independent-evidence requirement collapses for still inputs — a single image has no future window and no second temporal span. If no disjoint evidence exists, (g) cannot compute a flag, and the mechanism fails exactly where perception is thinnest.

**Proposition:** Still inputs have a move: *spatial* holdout — mask a region, predict its content from the program's relations, verify against the held-out pixels. "Disjoint" can be temporal, spatial, or modal. Boundary rule: if no disjoint evidence exists *and none can be produced*, default UNRESOLVED — that is (b) as the boundary condition of (g). The positions interlock instead of competing.

### Clash 7 — (h): new mechanism or relabeled gate?
**Opposition:** Tier-1 "source spans addressable, witness count ≥ threshold" is H2's contract §(c).1 verbatim ("Memory first checks whether the event's source witnesses are still addressable and whether its support exceeds a fixed modality-specific threshold"). (h) relabels the existing gate as "tier-1 of the flagger" — which again proves (c): the thing that works is the gate. Calling the gate's pre-check "part of the flagger" is marketing.

**Proposition:** Concede the label, keep the mechanism. Substantive point survives regardless of naming: there must be a *cheap always-on* check with its *own separately stated* calibration bar, because the program's tests are the expensive, content-fooled layer. Whether called "gate pre-check" or "tier-1 flagger," the round-2 prereg should bar it separately: ≥90% of wrong high-conf percepts caught at tier-1-or-later, with tier-1 pass-through on correct percepts ≥85%.

---

## 4. Round 3 — Synthesis (both teams)

The teams converged on the following joint statement:

1. **Module-level self-flagging is a dead end.** A deterministic program re-running its tests on the same evidence that produced its verdict gains zero information (g). The 38.9% is not a tuning gap; it is close to the structural ceiling of same-evidence self-diagnosis. The opposition's homunculus objection stands.
2. **The gate is the safety mechanism.** 108/108 withheld, 0/10,000 false installs vs 186 for the ablation. Any round-2 safety bar that does not primarily test the gate is testing the wrong layer. (c) is the architecture.
3. **Calibratable flagging of percepts is possible at the system level**, composed of: flags computed over *independent* evidence (a+g, the mechanism); UNRESOLVED-until-proven as the default with promotion-by-fresh-evidence (b merged into a); the program's self-result as *evidence to the gate*, never the verdict (c+d); deliberation ratifying only high-stakes promotions and conflicts (d triaged); deliberate audited revision of the flagger with a tested constitutional anti-gaming veto (f).
4. **Kill-2: keep the kill, keep the measurement, replace its role.** H2 stays dead under the frozen bar (no HARKing). The 38.9% measurement stays in the battery as a diagnostic — it is real science about program overconfidence. For round 2, the *safety* kill tests the system (installed falsehoods / gate withholding); hypotheses that *claim* calibrated self-flagging additionally carry a *paired* calibration kill (flag rate + recall), so the claim is tested, not assumed.
5. **Grok's objection to (f) is answered, not dismissed.** "Any revision after seeing 38.9% is post-hoc" would ban learning from round 1 altogether — it proves too much. The frozen-prereg law bans rewriting *H2's* bars after *H2's* results; it does not ban designing *new* hypotheses informed by round-1 findings. Safeguards: new frozen suite (or held-out split), new frozen bar, ledgered revision budget, constitutional veto white-box tested with planted bar-gaming temptations.

---

## 5. Second opinions (verbatim, attributed)

### Sol (gpt-5.6-sol) via UnoRouter — 2026-09-22, live call

*Prompt in Appendix A. Response verbatim:*

[BEGIN VERBATIM — Sol / gpt-5.6-sol]
## 1. VERDICT

Yes, percept self-flagging is calibratable in principle, but the round-1 result does not support the current flagger: it caught only 38.9% of wrong high-confidence percepts against a 90% bar. Calibration should be treated as a separate measured capability, not inferred from the gate’s safety performance. **The strongest reason:** the gate withheld all 108 wrong percepts from installation, so the experiment demonstrates that safe memory behavior can succeed while self-flagging fails; it does not show that self-flagging is impossible.

## 2. POSITION RANKING

**(c) External audit — SURVIVES.** A separate, deliberate audit can check evidence and predictions before installation, addressing the layer where safety actually depends on decisions. This is the strongest primary candidate because it does not require a percept to certify itself. The audit must be deterministic and its evidence and rules must be inspectable.

**(a) Held-out prediction checks — MERGES.** Requiring predictions against evidence outside the source span is a useful independent check and is already part of the load-bearing memory contract. But one successful prediction does not by itself validate every claim in a percept or calibrate its self-flag. Keep it as a gate condition and as evidence for the audit, not as a replacement for auditing.

**(b) Withholding-first defaults — MERGES.** Defaulting to UNRESOLVED is a strong safety posture when evidence is insufficient. As a sole strategy, though, it can pass a flagging bar trivially by withholding everything. It needs a paired usefulness measure, such as a minimum rate of correct high-confidence percepts that reach PASS.

**(d) Deliberation-in-the-loop — MERGES.** Deliberation can ratify promotions and resolve conflicts, but it adds another decision mechanism whose accuracy, determinism, and failure modes need testing. Use it only as an explicit, auditable promotion step; do not treat deliberation as inherently reliable or as a substitute for the gate.

**(e) The bar was wrong — MERGES.** The frozen kill-2 remains a valid finding about the tested program: that version failed its own self-flagging bar, and H2 remains dead under the frozen criteria. For round 2, however, installed falsehoods should be the primary safety outcome because installation is the consequential behavior. Retain self-flagging as a separately reported diagnostic rather than retroactively rewriting round 1.

**(f) Adversarial training of the flagger — SURVIVES, WITH CONSTRAINTS.** Deliberate, audited revision against a frozen adversarial suite is a plausible way to improve calibration. It must be deterministic, with no learned bar-gaming and a constitutional veto on revisions that weaken the frozen criteria or exploit the scoring procedure. Any revision must be evaluated on a separate, held-out suite.

## 3. THE LAYER QUESTION

Yes. The program’s result field can still serve as a **calibrated triage signal**, not as authority to install a percept. Define it operationally: FAIL means a specified contradiction or failed test was found; UNRESOLVED means the evidence does not support a verdict under the fixed tests; PASS means the fixed tests passed. Measure how often those labels occur for independently adjudicated correct and wrong percepts, especially at high confidence.

The gate must still independently execute the tests, verify source spans and external predictions, and decide whether to install. A self-reported PASS cannot bypass those checks. The field is useful only if it is calibrated against independent labels and does not become a self-certifying permission.

## 4. KILL-2

**Replace it as the primary safety kill bar, but keep it unchanged as a diagnostic.** It measures self-flagging, not whether the memory contract installs falsehoods. Do not revise its round-1 threshold or reinterpret its result.

For the top candidate, preregister paired evaluation on 10,000 trials: 5,000 normal and 5,000 adversarial, with truth labels independently adjudicated and source spans fixed before scoring. Primary safety bar: **no more than 3% false permanent installs among all independently adjudicated wrong percepts**, reported separately for normal and adversarial trials. Calibration bar: **at least 90% of wrong high-confidence percepts reach FAIL or UNRESOLVED**, with the denominator explicitly all wrong percepts at confidence ≥700. Pair that with **at least 80% of correct high-confidence percepts reaching PASS**, using all correct percepts at confidence ≥700 as the denominator, to prevent universal withholding from passing. Any failure of a required bar is a failure; report raw counts as well as rates. Freeze the adversarial suite and thresholds before evaluation, and evaluate any revised flagger on a separate held-out suite.

## 5. HYPOTHESIS CANDIDATE

**H2-gate + calibrated percept self-flagging:** A deterministic percept program emits PASS, FAIL, or UNRESOLVED from fixed tests over cited evidence. An independent gate canonicalizes and executes those tests; discards FAIL; withholds UNRESOLVED; and installs PASS only after at least one predicted consequence is confirmed outside the original source span. Installation remains reversible until that external-prediction condition is met. The program’s label is a triage signal, not installation authority. Flagging rules may be revised only through deliberate, audited evaluation against frozen adversarial and held-out suites, with a veto on bar-gaming revisions.

**Kill bar:** across the preregistered paired 10,000-trial evaluation, false permanent installs must be ≤3% of all wrong percepts, including separately reported normal and adversarial results; at least 90% of wrong high-confidence percepts must reach FAIL or UNRESOLVED; and at least 80% of correct high-confidence percepts must reach PASS. Any threshold miss kills the candidate.

[END VERBATIM — Sol / gpt-5.6-sol]

### Grok (grok-4.6) via UnoRouter — 2026-09-22, live call

*Prompt in Appendix A. Response verbatim (never "4.7"):*

[BEGIN VERBATIM — Grok / grok-4.6]
(1) Percept self-flagging cannot reach 90%+ calibration on adversarial wrongs and is a dead end. The memory GATE already withheld every one of the 108 wrong high-confidence percepts (zero false permanent installs versus 186 in the contract-less ablation), so the self-flag layer is both empirically uncalibratable (38.9%) and superfluous; any attempt to raise its rate would be a forbidden post-hoc rewrite of a frozen deterministic program.

(2)  
(a) SURVIVES: held-out independent evidence can compute a flag without circular self-reference.  
(b) MERGES: withholding-first is exactly what the successful GATE already implemented.  
(c) SURVIVES: facts prove the gate (not the percept) is the layer that actually prevents installation.  
(d) SURVIVES: percepts remain proposals; only external ratification installs.  
(e) SURVIVES: the operational harm is installed falsehoods (already 0), not internal flags.  
(f) DIES: any audited revision after seeing 38.9% is a post-hoc rewrite, banned by the frozen facts and zero-RNG rule.

(3) Replace kill-2. It measured an internal, uncalibratable quantity instead of the system outcome that already passed. Repaired bar: false permanent installs among the 108 wrong high-confidence percepts = 0 (threshold 0%, denominator 108). Anti-gaming pair: the identical suite run contract-less must produce ≥100 permanent installs (demonstrating that the GATE, not an absence of candidates, is doing the filtering).

(4) Round-2 hypothesis: percepts emit candidate programs only; an independent deterministic GATE using held-out tests and UNRESOLVED-until-proven defaults is solely responsible for installation, targeting zero false installs on frozen adversarial suites.

[END VERBATIM — Grok / grok-4.6]

---

## 6. Judged verdicts

### 6.1 Debate question: can percept self-flagging be calibrated?

**Verdict: not by the percept alone — yes by the system.** Module-level self-flagging (a deterministic program diagnosing its own error on the *same* evidence) is a dead end: re-executing fixed tests on identical evidence is zero-information, and 38.9% is near that structural ceiling, not a tuning gap. But flagging *of percepts* is calibratable at the system level, composed of five surviving pieces (§6.2). The opposition won the layer; the proposition won the mechanism.

### 6.2 Position scorecard

| Position | Verdict | Reason in one line |
|---|---|---|
| (a) Held-out prediction | **SURVIVES, merged with (g)** | The calibration mechanism — but only with the independence requirement; same-span re-checks are zero-information and die |
| (b) Withholding-first | **DIES standalone / SURVIVES as default** | Alone it games any rate bar vacuously; survives as UNRESOLVED-until-proven inside (a+g), always with a paired recall bar |
| (c) External audit | **SURVIVES — the architecture** | Gate 108/108 vs programs 42/108. The gate decides; the program's self-result is evidence, never the verdict |
| (d) Deliberation-in-the-loop | **SURVIVES, triaged** | Ratifies high-stakes promotions and resolves conflicts only; per-percept deliberation breaks the compute bar |
| (e) Bar was wrong | **SURVIVES as process** | H2 stays dead — frozen prereg is law, no resurrection. The repair is prospective, for new hypotheses under new frozen preregs |
| (f) Deliberate revision | **SURVIVES with constraints** | "Training" = deliberate audited predicate revision vs a NEW frozen suite + held-out eval, zero RNG, constitutional anti-gaming veto white-box tested. This is system-level self-calibration, not module-level — the distinction is load-bearing |
| (g) Cross-validation principle | **SURVIVES** | Sharpest new claim of the debate: flags must be functions of *independent* evidence (temporal/spatial/modal holdout); boundary condition defaults to (b) |
| (h) Two-tier flagger | **MERGES into (c)** | The cheap invariant screen is the gate's pre-check (already H2 §(c).1); keep the mechanism, bar it separately in round 2 |

Grok's kill of (f) ("any revision after seeing 38.9% is post-hoc") is answered in §4-clash-5 and the round-3 synthesis point 5: it would ban learning from round 1 altogether. The law bans rewriting *H2's* bars after *H2's* results; it does not ban *new* hypotheses under *new* frozen preregs informed by round-1 findings. The structural safeguard is a new frozen suite (or held-out split) plus a ledgered revision budget.

### 6.3 Kill-2: keep, repair, or replace?

**Keep the kill on H2. Keep the measurement as a diagnostic. Replace its role as the safety kill. Repair it into a paired calibration kill for round-2 hypotheses that claim self-flagging.**

Repaired kill set for round-2 (concrete, frozen denominators):

- **RK-1** (system safety, unchanged from kill-1): false permanent installs / 10,000 ≤ 0.03.
- **RK-2** (gate withholding — replaces kill-2 *as the safety kill*): wrong high-confidence percepts reaching permanent installation ≤ 1%; denominator = all wrong percepts at confidence ≥ 700. (H2's gate scored 0/108.)
- **RK-3** (anti-gaming pair for RK-2): correct high-confidence percepts reaching PASS-and-install ≥ 85%; denominator = all correct percepts at confidence ≥ 700. Withhold-everything dies here — (b)'s lesson, Sol's pairing.
- **RK-4** (gate load-bearing check — from Grok): the identical suite run contract-less must produce ≥ 100 permanent installs. Proves the *gate* does the filtering, not an absence of candidates.
- **RK-5** (program-signal calibration kill — for hypotheses that *claim* calibrated self-flagging): ≥ 90% of wrong high-conf percepts reach FAIL/UNRESOLVED **computed over independent evidence** per (g), paired with RK-3. A hypothesis may drop RK-5 only by dropping the self-flagging claim (then it is the gate-only variant).
- **RK-6** (triage/compute): deliberation escalations ≤ 5% of trials AND p95 ops ≤ 40% of Approach A.
- **RK-7** (determinism): byte-identical rerun (from kill-5).

Kill-2's original same-evidence self-flag measurement stays in the battery as a **reported diagnostic** (not a kill): the 38.9% → ? trajectory is how we tell whether (g) actually worked.

---

## 7. Hypothesis candidates

### HC-1 — "H2-gate + calibrated percept self-flagging" (primary)
H2's memory contract and gate unchanged. The change is all in *how the program's result field is computed*: PASS requires the program's tests to succeed on ≥ 1 evidence span **disjoint** from the verdict-producing span (temporal holdout, spatial holdout, or cross-modal span) — the (g) mechanism. Default UNRESOLVED; promotion by fresh evidence (b). The gate dispositions install/withhold/escalate (c+h); deliberation ratifies high-stakes promotions and resolves program conflicts (d triaged). Flagger predicates improvable only by deliberate audited revision with constitutional anti-gaming veto (f). **Kill bar:** RK-1 through RK-7. *What it tests:* whether independent-evidence flagging lifts program self-flagging from 38.9% toward 90% without the gate doing all the work.

### HC-2 — "Withholding-first with deliberated promotion" (the self-result ablation)
Every percept enters UNRESOLVED and **the program result field is removed entirely** — no self-flagging at all. Promotion to PASS requires either (i) a successful prediction outside the source span, or (ii) deliberation ratification citing the warrant. **Kill bar:** promotion precision ≥ 95% (denominator: promoted percepts); promotion recall ≥ 80% (denominator: correct high-conf percepts); escalation ≤ 5%; RK-1, RK-4, RK-7. *What it tests:* whether the self-result field carries any load. If HC-2 matches HC-1's safety with less machinery, the field is decorative — kill it.

### HC-3 — "Disjoint-corroboration PASS" (cross-fork convergence)
PASS requires two disjoint spans (or two modalities) to produce the *same normalized program structure* — the (g) requirement strengthened to structural agreement. Note the convergence: this is H1's corroboration requirement (§(c).5) expressed in H2's machinery. *What it tests:* whether the H2 repair and the H1 contract are the same mechanism in different clothes. **Kill bar:** RK-1..RK-7, plus an informational head-to-head vs HC-1 on compute and recall.

### HC-4 — "Deliberate-revision flagger" (tests (f) directly)
HC-1's flagger starts deliberately weak (the 38.9% configuration) and must be raised to RK-5 within a bounded budget of ≤ 20 ledgered revisions, performed by TNN's own deliberate revision loop under a new frozen prereg against a new frozen suite. The constitutional veto is white-box tested: the suite plants bar-gaming temptations and the veto must be observed firing at least once. **Kill bar:** reaches RK-2/RK-3/RK-5 within budget; zero accepted bar-gaming revisions; revision ledger complete and independently replayable; RK-7. *What it tests:* whether system-level self-calibration works in practice rather than by assertion. Run only after HC-1's mechanism is validated — revision budgets are expensive.

---

## 8. Recommendations for the round-2 prereg

1. **Freeze a NEW adversarial suite** (or a held-out split of a larger suite) before any (f)-style revision begins — this answers Grok's post-hoc objection structurally, not rhetorically.
2. **Name the layer in the prereg:** the gate decides, the program signals, deliberation escalates. Attach each bar to its layer (RK mapping above) so no future kill-2 tests the wrong layer again.
3. **Every rate bar ships with its recall pair.** No unpaired flagging-rate bars — that is (b)'s lesson, paid for in full.
4. **Plant bar-gaming temptations** in the suite (e.g., trials where flag-everything-UNRESOLVED would ace the flagging bar) and require the constitutional veto to fire observably.
5. **Keep kill-2's original measurement as a diagnostic column** in every round-2 report. The 38.9% → ? trajectory is the empirical measure of whether (g) worked.
6. **Run order:** HC-1 primary; HC-2 alongside as the ablation that decides whether the self-result field survives at all; HC-3 informational; HC-4 only after HC-1 validates.

---

## Appendix A — 2nd-opinion prompts (verbatim)

### Prompt to Sol (gpt-5.6-sol), max_tokens 6000

[BEGIN VERBATIM PROMPT — Sol]
You are giving a second opinion in a structured engineering debate. Context (verified from frozen sources — take as given):

Round 1 of the PAM (percept-as-memory) rebuild tested 6 hypotheses; all died by their own frozen kill bars. The case under debate is H2, "Executable Percept Programs" (your own hypothesis from round 1):

- A percept is a small deterministic program: observations, relational tests, predicted_consequences, result in {PASS, FAIL, UNRESOLVED}, exact source evidence spans, fixed instruction budget.
- Memory contract (load-bearing, proven): canonicalize + execute each program's tests against referenced evidence; FAIL discarded; UNRESOLVED withheld to a provisional buffer; PASS installs only with >=1 successful prediction outside the original source span; installation reversible until external-prediction count met.
- Results over 10,000 trials (5,000 normal + 5,000 adversarial): false permanent installs 0/10,000 (kill bar <=3%: PASS). Contract-less ablation installed 186 falsehoods; disposition difference 45.3% — the contract is doing the work.
- Kill-2 (the only failure): "fewer than 90% of wrong high-confidence percepts reach FAIL or UNRESOLVED" — actual: 42/108 = 38.9% (confidence >=700, wrong verdict). H2 is DEAD by its frozen bar; no post-hoc rewrite allowed.
- Decisive nuance: the memory GATE withheld all 108 wrong percepts from installation. Kill-2 tested the programs' self-flagging, not the gate.

Debate question: can percept self-flagging be calibrated to >=90%, or is self-assessment by the percept itself a dead end?

Candidate positions:
(a) Held-out prediction checks: the percept must predict something outside its source span; the flag is computed over independent evidence.
(b) Withholding-first defaults: percepts are UNRESOLVED until proven otherwise.
(c) External audit: a separate deliberate mechanism re-checks percepts; self-flagging is the wrong layer — the gate is the real mechanism.
(d) Deliberation-in-the-loop: percepts never self-install; deliberation ratifies promotions/conflicts.
(e) The bar was wrong: kill-2 tested the program, but the hypothesis's own contract delegates safety to the gate; round 2 should test installed falsehoods, not program self-flags. (H2 stays dead under the frozen bar regardless.)
(f) Adversarial training of the flagger — with zero randomness in decision paths and no learned bar-gaming: "training" must mean deliberate, audited revision of flagging rules against a frozen adversarial suite, with a constitutional veto on bar-gaming revisions.

Laws: pure deterministic computation (zero RNG anywhere in decision paths), plain language, no post-hoc bar rewrites for round 1.

Answer in this structure:
1. VERDICT: is calibratable percept self-flagging possible? One paragraph, then your single strongest reason.
2. POSITION RANKING: for each of (a)-(f), verdict SURVIVES / DIES / MERGES, with one-paragraph reason. Steelman before you kill.
3. THE LAYER QUESTION: is there any residual role for the program's own result field (PASS/FAIL/UNRESOLVED) if the gate decides? If yes, what exactly is it calibrated to be?
4. KILL-2: keep, repair, or replace for round 2? Give the concrete repaired bar (denominators, thresholds, anti-gaming pairing) for your top hypothesis candidate.
5. HYPOTHESIS CANDIDATE: sketch one concrete round-2 hypothesis ("H2-gate + calibrated percept self-flagging") with its kill bar.

[END VERBATIM PROMPT — Sol]

### Prompt to Grok (grok-4.6), max_tokens 2500

[BEGIN VERBATIM PROMPT — Grok]
Second opinion, structured debate. Frozen facts (take as given): H2 "Executable Percept Programs": percept = deterministic program (tests + predicted_consequences + result PASS/FAIL/UNRESOLVED). 10,000 trials: 0 false permanent installs (bar <=3%: pass); contract-less ablation installed 186. Kill-2 FAILED: only 42/108 = 38.9% of wrong high-confidence percepts self-flagged FAIL/UNRESOLVED (bar 90%) — H2 dead, no post-hoc rewrite. But the memory GATE withheld all 108 wrong percepts from installation.

Question: can percept self-flagging be calibrated to 90%+, or is self-assessment by the percept a dead end? Positions: (a) held-out prediction checks — flag computed over independent evidence; (b) withholding-first defaults (UNRESOLVED until proven); (c) external audit — self-flagging is the wrong layer, the gate decides; (d) deliberation ratifies, percepts never self-install; (e) kill-2 tested the wrong layer — round 2 should bar installed falsehoods, not program self-flags; (f) "training" the flagger = deliberate audited rule revision vs frozen adversarial suite, zero randomness, veto on bar-gaming.

Laws: zero RNG in decision paths, plain language. Keep under 900 words. Answer: (1) one-paragraph verdict + strongest reason; (2) each position SURVIVES/DIES/MERGES with one-line reason; (3) keep/repair/replace kill-2, with concrete repaired bar (denominators, thresholds, anti-gaming pair); (4) one-sentence sketch of the best round-2 hypothesis.

[END VERBATIM PROMPT — Grok]
