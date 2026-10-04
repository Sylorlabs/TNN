# P1-Deep Withholding: Learner-Owned Withhold/Guess Boundary

**Verdict: P1-WITHHOLDING-COMPLETE.**
**Status:** The withhold/guess boundary is learner-owned (WT values from
experience, not researcher-set). On predictor degradation, the adaptive
threshold withholds the degraded predictor earlier than fixed-3 (38 vs 45
wrong guesses; withholds at t=280 vs never). In stationary worlds the
adaptive threshold is comparable to a well-chosen fixed threshold, not
better. The reliability score does most adaptive work; the threshold is a
secondary modulator.

## 1. Question

C181 (learner-verification) left the withhold/guess threshold as
researcher-set (`lv_rel_thresh()=3`). Governance gap: "P1-deep:
learner-owned verification for withholding (not just revision)."

Can the withhold/guess boundary be learner-owned? Does it adapt when the
world changes? How does it compare to fixed-3, always-guess, and
always-withhold?

## 2. Mechanism (unfrozen variant only)

Base: C181 prediction machinery (`ev_predict`, `pred_resolve`, +1/-1
reliability scores). Predictors are FACTs (taught once, never superseded;
scored via `pred_resolve` directly to isolate predictor reliability from
belief revision).

New patch (`wh_patch.zag`):

### 2.1 Learner-owned threshold WT

WT lives in learner state (header field 40). Update rule, from experienced
decision consequences only:

- false guess (guessed, prediction != outcome): WT += 1
- false withhold (withheld, prediction == outcome): WT -= 1
- correct guess / correct withhold: no change

Initial WT = 3 (same scaffold as C181, so the adaptive arm starts identical
to fixed-3 and diverges through experience). Clamped to [-10, 30].

Causal chain: decide -> outcome arrives -> score the decision -> WT changes
-> later decisions change.

### 2.2 Four arms (binaries differ ONLY in `wh_mode()`)

- mode 0: fixed threshold 3 (C181 behavior).
- mode 1: always guess (threshold -inf).
- mode 2: conservative, always withhold (threshold +inf).
- mode 3: adaptive, threshold = learner-owned WT.

### 2.3 Honest boundary

Researcher-owned: WT initial value (3), update magnitudes (+1/-1), clamp
bounds, header field, decision structure, mode gate.
Learner-owned: the WT VALUES over time (3->24 in W1, 3->30 in W2),
which queries are withheld, the response to regime change.
The +1/-1 rule has the same standing as C181/C182 bookkeeping.

### 2.4 Bug found and fixed

`ev_teach` calls `ctx_push`, which uses header bytes 32/36/40/44 as a
context stack. The third predictor teach (s=103) wrote 103 to byte 40,
poisoning WT (observed WT_post_build=103). Fixed by force-initializing WT
after the teach sequence (no teaches follow). Documented in `wh_patch.zag`.
This also affects C181's hg(W,32)/hg(W,36) usage; noted for the record.

## 3. Experimental design

Three predictors:
- G (101,50,1001): world always 1001. True accuracy 100%.
- M (102,50,1002): world 1002 w.p. m_acc/10 else 7002.
- B (103,50,1003): world always 7003. True accuracy 0%.

All arms see IDENTICAL (predictor, outcome) sequences: same RNG seed, same
round-robin order, outcome drawn for every query regardless of decision.
Predictor reliability trajectories are identical across arms; metric
differences are causally attributable to the decision rule.

Batteries (T=300 queries each, 3/3 byte-identical per arm):
- W1: stationary, M at 60%, K=20 buildup. Baseline.
- W2: regime change, M 90% -> 10% at t=150, K=20 buildup.
- W3: low buildup K=2, M at 60%. Tests miscalibrated fixed threshold.

Scoring: correct guess +1, wrong guess -1, withhold 0.

## 4. Results

### 4.1 W1: stationary (M at 60%)

| arm | guess | withhold | acc | false wh | score | WT |
|---|---|---|---|---|---|---|
| fixed-3 | 188 | 112 | 82.4% | 7 | 122 | n/a |
| always-guess | 300 | 0 | 54.0% | 0 | 24 | n/a |
| conservative | 0 | 300 | n/a | 162 | 0 | n/a |
| adaptive | 183 | 117 | 82.0% | 12 | 117 | 3->5->14->24 |

Fixed-3 wins (122). Adaptive close (117). The fixed threshold of 3 is
well-calibrated here; adaptive oscillates around M's reliability and scores
slightly lower. WT rises 3->24, tracking M_rel (2->26): the value is
experience-determined, but it chases rather than converges.

### 4.2 W2: regime change (M 90% -> 10% at t=150)

| arm | guess | withhold | acc | score | M wrong post | M withhold at | WT |
|---|---|---|---|---|---|---|---|
| fixed-3 | 200 | 100 | 76.0% | 104 | 45 | never (-1) | n/a |
| always-guess | 300 | 0 | 50.7% | 4 | 45 | never | n/a |
| conservative | 0 | 300 | n/a | 0 | 0 | t=151 | n/a |
| adaptive | 193 | 107 | 78.8% | 111 | 38 | t=280 | 3->6->21->30 |

Adaptive wins (111 vs 104). It withholds M at t=280 after 38 wrong guesses;
fixed-3 never withholds M (45 wrong) because M_rel (58 at change) stays
above 3. WT rises 3->30 in response to degradation: the boundary is
learner-owned and responds to regime change.

Limitation: 38 wrong guesses is still slow. Entrenched high reliability
(M_rel=58) dominates; the threshold helps but does not solve it.

### 4.3 W3: low buildup (K=2)

| arm | guess | withhold | acc | false wh | score | WT |
|---|---|---|---|---|---|---|
| fixed-3 | 177 | 123 | 81.9% | 15 | 113 | n/a |
| always-guess | 300 | 0 | 53.3% | 0 | 20 | n/a |
| conservative | 0 | 300 | n/a | 160 | 0 | n/a |
| adaptive | 176 | 124 | 81.8% | 16 | 112 | 3->1->6->19 |

Essentially tied (113 vs 112). The fixed threshold recovers in 1 query
(G_rel 2->3); the hypothesized miscalibration does not materialize because
reliability scores adapt fast. WT dips 3->1 (false withholds on G) then
rises: two-sided adaptivity confirmed, but no score advantage.

## 5. What this establishes

1. **The boundary is learner-owned.** WT values (3->24, 3->30, 3->1->19)
   are determined by experienced false guesses and false withholds. No
   researcher sets the operating threshold.

2. **Adaptive responds to degradation.** W2: withholds M at t=280 vs never;
   38 vs 45 wrong guesses; score 111 vs 104.

3. **Two-sided adaptivity.** WT falls when the threshold is too strict
   (W3: 3->1 via false withholds) and rises when too lax (W2: 3->30 via
   false guesses).

4. **Fixed-3 is a strong baseline.** In stationary worlds (W1) and fast
   recovery (W3), adaptive does not beat it. The reliability score carries
   most of the adaptive load.

## 6. Limitations

1. **Threshold is secondary.** The per-predictor reliability score adapts
   (that is C181); the global threshold modulates. A global threshold cannot
   be optimal per-predictor.

2. **Slow against entrenched scores.** W2: 38 wrong guesses before
   withholding. High M_rel (58) dominates; threshold rises too slowly.

3. **Symmetric update.** The +1/-1 rule does not encode cost asymmetry
   (a wrong guess may cost more than a missed opportunity). The equilibrium
   balances error rates, not expected value.

4. **No trial integration.** The guess is the prediction itself, not a
   trial-constructed verified candidate. Full t2_trial_learner integration
   is future work.

5. **Oscillation.** In W1, WT chases M_rel (3->24) rather than converging.
   The boundary is adaptive but not stable.

## 7. Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: WT init (3), +1/-1 update rule,
  clamp [-10,30], header field 40, decision structure, mode gate.
- LEARNER-OWNED STRUCTURAL DECISIONS: WT values over time, withhold/guess
  per query, M withhold at t=280 in W2.
- SOURCE-ENUMERABLE FORMS: 0.
- SUF DECISIONS: 0.
- COGNITION LINES: ~120 (wh_patch.zag).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

## 8. Artifacts

- `NAMECHECK.md` (Step 0 guard, provenance, constraints)
- `REPORT.md` (this file)
- `wh_patch.zag` (withholding decision + learner-owned WT)
- `wh_driver.zag` (3 batteries)
- `wh_predsec.zag` (prediction section extracted from C181)
- `wh_full_m0/m1/m2/m3.zag` (assembled; arms differ by one line)
- `wh_bin_m0/m1/m2/m3` (binaries)
- `run_m0/m1/m2/m3_1/2/3.txt` (3/3 byte-identical per arm)
- `compile_m0/m1/m2/m3.log`

Run SHAs: m0 `40ea4a6b...`, m1 `fdeb756a...`, m2 `b616bdd2...`,
m3 `ee00faeb...`.

Constraints honored: unfrozen variant only; frozen source read-only; pure
Zag via pinned znc; safebin active; zero Python invocations; zero em/en
dashes byte-verified; research paper untouched; nothing pushed; explicit
pathspecs on git add and git commit.
