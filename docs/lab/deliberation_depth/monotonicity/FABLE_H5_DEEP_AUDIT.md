# FABLE H5 DEEP AUDIT — deliberation-depth monotonicity

**Crew:** CREW A — fable deep audit (single batched round policy)
**Date:** 2026-09-24
**Model:** claude-fable-5.1 via UnoRouter (`~/workspace/skills/unorouter/bin/fable.py`), max_tokens=24000
**Prompt file:** `monotonicity/fable_prompt_h5.txt` (in this directory)
**Status:** PARTIAL. Attempt 1 returned a truncated response (1,349 completion tokens — Sections 2–4 never arrived; response cuts off mid-sentence inside Section 1). Retry after 5-minute backoff hit the known provider-side failure (`choices: null`, 0 completion tokens). Per task instructions (one retry max, no further rounds), the audit closed with attempt-1 content only. Distilled Sections 4.2–4.4 below are **native crew analysis**, clearly labeled — they are NOT fable's words.

---

## §1. Exact prompt sent (verbatim)

(The full prompt text is preserved at `monotonicity/fable_prompt_h5.txt` in this directory; the complete verbatim text is reproduced in the appendix §A of this document.)

---

## §2. Raw fable response — attempt 1 (verbatim, truncated)

> # DEEP AUDIT: TNN NATIVE-LAB H5 DELIBERATION-DEPTH RESEARCH
>
> ## SECTION 1: MECHANISTIC EXPLANATION OF DEPTH-DEGRADATION
>
> ### Ranked Causal Pathways (Plausibility: 0.0–1.0)
>
> **PATHWAY 1: Hypothesis Pruning Eliminates Truth (Plausibility: 0.95)**
>
> *Micro-dynamics:*
> - Round r: True hypothesis H_true has support S_true = 500, misleading hypothesis H_mislead has support S_mislead = 400
> - Evidence stream crafted so early items (positions 0–15) give weak support to truth (+50 each to H_true), late items (positions 16–63) give strong misleading support (+150 each to H_mislead)
> - Round r+1: New misleading evidence arrives, S_mislead rises to 550, S_true stays 500
> - Round r+2: S_mislead = 700, S_true = 500. Confidence = clamp(700-500, 0, 1000) = 200 (not in observed set, but mechanism runs)
> - Round r+3: More misleading evidence: S_mislead = 850, S_true = 500
> - **Round r+4: S_mislead = 1000, S_true = 500. Gap = 500. But now S_mislead - S_true may not trigger elimination yet.**
> - **Round r+8: Cumulative misleading evidence pushes S_mislead to 1400, S_true remains 500. Gap = 900 = ELIMINATION MARGIN. H_true is PRUNED FOREVER.**
> - Round r+9: Only H_mislead survives. Confidence = 1000 (sole survivor). System outputs H_misleead with maximum confidence.
> - Round r+∞: No recovery possible. Elimination is irreversible.
>
> *Why systematic monotone degradation:*
> The 40/40 O-item flip is explained if stream design follows a template: position early honest evidence so depth-1 reads ONLY early (gets truth), depth-2 reads early+some-misleading (margin narrows but truth still leads), depth-4 reads enough misleading to equalize, depth-8 reads enough to eliminate truth, depth-16+ only has misleading left so H_mislead dominates unopposed. The monotone decrease 1.00→0.75→0.50→0.25→0.00 suggests 4 quartiles of the 40-item O battery are tuned to flip at depth-thresholds {2, 4, 8, 16} respectively. Each item's flip-depth is calibrated to its stream's misleading-evidence concentration curve.
>
> *Evidence lean:*
> - Explains strict anti-monotonicity (once pruned, never recoverable)
> - Explains why residual-flip bound preserves degradation (it runs to exhaustion; if exhaustion = wrong, bound = wrong)
> - Explains 1000 confidence on wrong answers (sole survivor after elimination)
> - Explains identical stream-shape behavior on P vs O: both are "plateau then flip" but P flips TO truth, O flips FROM truth
> - **Distinguishability problem: FROM INSIDE deliberation state at round r<8 on an O-item, you cannot tell whether the late evidence will overturn TOWARD truth or AWAY FROM it.** The margin dynamics, hypothesis set, ledger all look identical. The only difference is the *sign* of late evidence relative to ground truth, which is unknowable without external labels.
>
> **PATHWAY 2: Margin Self-Reinforcement via Audit-Trail Overfitting (Plausibility: 0.75)**
>
> *Micro-dynamics:*
> - Round r: Deliberator emits trace T_r = "Evidence E_i supports H_mislead because [reasoning]. Eliminate H_true."
> - Round r+1: New evidence E_{i+1} arrives. Deliberator reads E_{i+1} AND rereads full trace T_r as context.
> - T_r presents H_mislead as "leading hypothesis" with "support 700" and H_true as "refuted, support 500"
> - The audit trail becomes **pseudo-evidence**: the fact that H_mislead was preferred in T_r is treated as confirmation that H_mislead is correct, independent of raw evidence weights.
> - Round r+1 trace: "Previous round established H_mislead is dominant. New evidence E_{i+1} [even if weak] confirms this. Eliminate H_true."
> - Feedback loop: Each round's trace reinforces the leader's dominance, making it harder to overturn even if late evidence would, in a fresh context, favor H_true.
>
> *Why systematic monotone degradation:*
> If the audit trail grows as a prefix at each round, and the deliberator gives non-zero weight to "what I concluded last round" as evidence, then a wrong early choice becomes entrenched. The longer the trail, the more self-consistent the misleading narrative, the harder to dislodge. Depth 1 has no trail (just raw evidence), depth 8 has 8 rounds of self-confirming narrative, depth 64 has 64 rounds.
>
> *Evidence lean:*
> - Explains why depth 1 can be correct (no trail to overfit)
> - Explains why deeper rounds don't recover (trail grows)
> - Explains overconfidence (margin computed from accumulated support, which includes trail-induced boosts)
> - **But:** harder to explain the CLEAN 40/40 flip. Overfitting predicts noisy degradation (some items resist, some don't), not synchronized quartile fl
>
> [RESPONSE TRUNCATED BY PROVIDER — 1,349 completion tokens; Sections 2–4 never arrived]

---

## §3. Retry attempt — provider-side failure (verbatim raw)

After a 5-minute backoff, attempt 2 returned `choices: null` with 0 completion tokens — the known claude-fable-5.1 provider failure mode (backend generated nothing; not a prompt problem). Raw body:

```json
{"id": "chatcmpl-HouUR2gTRP97btRz", "model": "claude-fable-5.1", "object": "chat.completion", "created": 1790263061, "choices": null, "usage": {"prompt_tokens": 2964, "completion_tokens": 0, "total_tokens": 2964, "prompt_tokens_details": {"cached_tokens": 0, "text_tokens": 0, "audio_tokens": 0, "image_tokens": 0}, "completion_tokens_details": {"text_tokens": 0, "audio_tokens": 0, "text_tokens": 0, "audio_tokens": 0, "reasoning_tokens": 0}, "input_tokens": 0, "output_tokens": 0, "input_tokens_details": null, "claude_cache_creation_5_m_tokens": 0, "claude_cache_creation_1_h_tokens": 0}}
```

No further rounds per the one-round policy.

---

## §4. Distilled analysis

### 4.1 Ranked degradation mechanisms (why more depth hurts)

Mechanisms 1–2 are fable's (from the partial response); 3–6 are native crew completions, grounded in the harness white-box facts and the verified measurements. Plausibility scores are the crew's.

1. **Irreversible elimination of the true hypothesis (0.95 — fable's Pathway 1, endorsed).** The micro-dynamics are exactly right for this harness: the judge is deterministic weight accumulation over a fixed stream, not a re-judging LLM. On O items the stream is front-loaded with weak honest evidence and back-loaded with concentrated misleading evidence (the flip-depths {2,4,8,16} calibrate to the stream's misleading-concentration curve, which is why the degradation is a clean monotone 1.00→0.75→0.50→0.25→0.00 rather than noise). Once cumulative misleading support pushes the leader−truth margin past the 900 elim margin, the true hypothesis is pruned FOREVER — there is no re-admission path in the harness. Every round after the elimination round operates on a hypothesis set that no longer contains the truth. Monotone by construction, not by noise.

2. **No-chain tail is a pure exposure multiplier (0.90 — native).** Depth in this harness = how many stream positions get consumed (mean rounds ≈ evidence consumed 1:1). On misleading-tail streams, each additional round is not "more thinking" — it is more EXPOSURE to poison. The mind does not corrupt itself; it is fed poison with no defense. This reframes the finding: the anti-monotonicity is a stream-shape × irreversible-elimination interaction, and any mechanism that equates "consumed more evidence" with "thought harder" will inherit it.

3. **Confidence theater on no-chain items generalizes (0.80 — native).** The H5 verdict already proved depth adds only tail and the tail is theater on no-chain items. The O battery is the adversarial dual: the tail is not idle, it is hostile. A mechanism that cannot distinguish idle tail from hostile tail will treat both as "deeper = better."

4. **Margin self-reinforcement via audit-trail overfitting (0.70 — fable's Pathway 2, qualified).** Fable itself flagged the weakness: overfitting predicts noisy degradation, not the clean 40/40 synchronized flip. In THIS harness the judge does not re-read its own trace as evidence (weights are frozen per evidence item), so the trail-reinforcement loop is largely absent here — it is a bigger risk for future TNN organs where deliberation is LLM-like re-judgment with the trace in context. Keep it on the watchlist for the real system; it is not the driver of the measured O curve.

5. **Flatness-mistaken-for-correctness in the §6 stop (0.65 — native).** The gain-window rule stops when the state stops moving — mistaking settled-state for correct-state. On P it stops wrong at round 5 (40/40); on O it stops right at round 5 by pure accident (the flip hasn't arrived yet). A stopping rule that rewards stillness systematically selects answers that are stable-but-wrong whenever the stream is designed to be flat-before-flip. This is a second, independent non-monotonicity source: even the STOPPING DECISION degrades with stream shape.

6. **Error amplification through iterated re-judgment (0.35 — native, demoted).** Requires a stochastic or interpretive re-judgment step whose errors compound. The measured harness has none — it is deterministic accumulation. Ranked low for this harness; relevant only if a future judge re-interprets evidence each round.

**The distinguishability verdict (fable's key sentence, endorsed as the central result):** from inside the deliberation state at round r before the flip, a P-item (late evidence vindicates truth) and an O-item (late evidence kills truth) are STRUCTURALLY IDENTICAL — same leader, same margin dynamics, same live runner-up, same ledger shape. The only difference is the sign of late evidence relative to ground truth, which is unknowable without external labels or an independent trust signal. **No stopping rule, certificate, or threshold computed from deliberation state alone can separate them.** Any "guarantee" that ignores this is false.

### 4.2 Overconfidence mechanism pinpoint (native — fable never reached §2)

The confidence formula `c = clamp(support(leader) − support(runner-up), 0, 1000)` decouples from correctness at four exact points, ranked:

1. **Sole-survivor pin at 1000 (the fatal one).** When elimination leaves one hypothesis, confidence is DEFINED as 1000 regardless of how the elimination was reached. On O items the trajectory is: truth leads with a small margin (moderate confidence) → misleading evidence accumulates → margin narrows (confidence wobbles — the sensor's one honest moment, and it is unread) → truth is eliminated → confidence pins at 1000 on the wrong survivor. The formula conflates "no competitors left" with "certainly right." This is the exact microsecond the machine becomes a confident liar: the elimination event. **Formula-level fix:** confidence must be a function of the elimination's audit quality (was the margin at elimination robust to the remaining stream? what fraction of total evidence weight was seen?), never a constant. **Architectural fix:** elimination must be provisional with a re-admission path; a sole survivor that won by default is not a certified answer.

2. **Margin measures distance-to-runner-up, not absolute evidence quality (0.9).** A 900 margin built from 9 weak misleading items reads identical to a 900 margin built from 2 decisive honest items. The formula has no notion of evidence weight provenance or independence — accumulated WEIGHT is treated as accumulated CONFIRMATION. On O streams the margin is real arithmetic on poisoned inputs. **Fix:** weight evidence by a trust score computed INDEPENDENTLY of the deliberation (source trust, L+S program); the margin formula must take trust-weighted support, not raw support.

3. **Elimination is irreversible, so the margin is never re-audited (0.85).** Once a hypothesis crosses the 900 elim margin it is gone; its supporting evidence is never re-examined against later arrivals. The confidence at release therefore certifies a kill-board state that was frozen rounds ago. **Fix:** every elimination must carry a standing re-admission condition (e.g., "re-open if later evidence would have changed the elimination round's margin sign"), checked per round and ledgered.

4. **The observed value set {400,500,700,710,764,800,1000} proves the sensor is a scoreboard, not a belief (0.8).** Seven distinct values across 997 items — the "confidence" is a coarse function of weight arithmetic with no calibration to correctness. The 0/127 trap catastrophe at max confidence is not a sensor failure; the sensor was never measuring correctness at all. **Fix:** recalibration is approved as its own preregistered experiment (per the H5 verdict), but recalibrating a scoreboard still yields a scoreboard — calibration must be against correctness on held-out adversarial streams, and the formula must change, not just its scale.

**On the §6 rule creating overconfidence:** yes, secondarily. Stopping on flatness and then reporting the settled confidence as the answer's confidence presents "we stopped moving" as "we are sure." The stopping REASON must be part of the confidence report: `stop=six` (settled) must never be presented at the same confidence as `stop=bound` (provably unflippable).

### 4.3 Guarantee mechanisms in priority order (native — fable never reached §3)

Design goal restated against Micah's law: the release policy must guarantee **no confident wrong answer** — output is either a certified answer or an explicit audited ABSTAIN. "Never worse" is then measured on the correct metric: the confident-wrong rate must be 0 at every depth, and abstains must not grow without bound on honest distributions.

**Design 1 — Certified-dominance release with rollback-to-best and mandatory abstain (BUILD FIRST).**
- *Decision rule (in harness state terms):* at every round r, record (leader_r, cert_r) where cert_r = PROVABLY-UNFLIPPABLE (the residual-flip bound's reachability check over the remaining stream) AND margin-at-elimination-audited (every elimination on the path to leader_r carries a satisfied re-admission check). Maintain best = the latest round whose leader is fully certified. At the budget cap (or natural exhaustion): if best exists → release leader_best with its certificate; else → release ABSTAIN with the audited reason (which certification clause failed, ledgered). NEVER release an uncertified leader as a confident answer. The scaffold (arbitrary exploration depth) is preserved; the RELEASE is gated.
- *Certificate contents:* the leader identity, the round it was certified, the unflippability proof (remaining-stream weight bounds per hypothesis), the elimination audit trail with re-admission checks, the config SHA and stream hash.
- *Predicted behavior:* O items — flips from confident-wrong to ABSTAIN past the flip point (the misleading leader can never satisfy the elimination-audit clause once truth is pruned by poisoned evidence... honest caveat: see red-team); accuracy on O becomes correct-then-abstain instead of correct-then-confident-wrong. P items — rides to the flip exactly like the bound (1.000). Honest batteries — identical to bound (1.000, 1.00–2.87 mean rounds). Traps — bound-like.
- *Falsification criteria (any one kills it):* (a) a single confident-wrong release on any battery (cert-wrong = 1 → design dead); (b) abstain rate > 10% on the honest batteries (admit/revoke/logic/cost) → the certificate is vacuous, redesign; (c) a P-family item where the design abstains instead of riding to the flip → the dominance check is too conservative.
- *Why first:* it is the smallest delta from the already-proven residual-flip bound (0/997 diffs vs exhaustion, 2.6–4.6× cheaper than §6 on honest data), it directly implements scaffold-and-release, and its falsification criteria are crisp.

**Design 2 — Source-trust-gated certification (the actual P-vs-O fix; needs the L+S program).**
- *Decision rule:* the unflippability certificate is computed over TRUST-WEIGHTED remaining stream weight, where trust scores come from machinery independent of this deliberation (source provenance, PAMs verdicts on the stream's origin). A leader is certifiable only if it is unflippable under trust-weighted bounds AND the stream's aggregate trust is above threshold; below threshold → ABSTAIN regardless of margins.
- *Predicted behavior:* the only design that can separate P from O worlds — P's late evidence arrives with valid provenance (certifies), O's misleading tail arrives with low trust (abstains or refuses the flip). On honest batteries identical to Design 1.
- *Falsification:* a high-trust-provenance misleading stream that flips the verdict confidently-wrong → trust model dead, not just the design; trust-threshold tuning that abstains >10% on honest batteries → vacuous.
- *Why second:* it depends on source-trust machinery that does not exist yet in this harness. Design 1 ships now; Design 2 is the load-bearing follow-up.

**Design 3 — Round-wise independent re-derivation with disagreement-triggered abstain (do NOT build; documented as rejected).**
- *Idea:* re-run the judge from raw stream for each prefix independently and abstain on disagreement. *Rejection reason:* the judge is deterministic given the stream prefix — re-derivation reproduces the identical trajectory, so "disagreement" never fires and the design is pure cost theater (doubles audit steps, zero signal). It would only help a future stochastic/interpreting judge.

### 4.4 Red-team of the recommended mechanisms (native — fable never reached §4)

- **Adaptive adversary vs Design 1 (the kill shot):** the elimination-audit clause is computed from the SAME stream that may be misleading. An adversary that front-loads JUST enough honest evidence to pass the re-admission checks, then back-loads concentrated misleading evidence, produces a fully "certified" wrong answer — the certificate is sound relative to its premises and the premises are poison. Self-certification from a single stream is the deepest flaw: **no certificate computed solely from deliberation state can survive a stream adversary**, which is the distinguishability result again. Design 1 degrades gracefully (it converts confident-wrong into abstain only when the audit clause happens to fail), but it does NOT solve O — it softens it. The honest claim for Design 1 is "never confident-wrong on streams the audit clause catches," not "never confident-wrong."
- **Abstention collapse (second-order):** if the audit clause is strict, hard honest items (long chains, near-tie margins) abstain too — the system becomes a coward that only answers easy items. Guard: the ≤10% honest-abstain falsification bar, plus per-family abstain reporting (never pooled — the H5 pooling lesson).
- **Certificate theater (second-order):** once "certified" becomes the release gate, future judge variants will optimize for certifiability (fast unflippability) rather than correctness — the same gaming dynamic as the §6 flatness reward. Guard: certificates must be computed by harness-frozen code the judge cannot influence, exactly as the current bound is.
- **Cost:** Design 1 adds per-round: one unflippability check (already paid by the bound leg: mean 14.08 rounds on ceiling, 1.00–2.87 on honest) + one elimination re-admission check per elimination event (bounded by kill-board size, ≤ hypotheses). Ledger cost: the certificate per released answer (~5 fields). No extra evidence consumption. Affordable.
- **MOST-WORRYING FAILURE:** a high-trust-provenance misleading stream under Design 2 — or equivalently, an O-stream whose misleading tail is engineered to satisfy Design 1's audit clause. The system would release a CERTIFIED wrong answer: the worst possible outcome under Micah's law, because the certificate suppresses exactly the skepticism that would have caught it. A naive test suite (honest batteries + the current O battery) would NOT catch this — it requires a dedicated adversarial battery of audit-clause-satisfying misleading streams. **That battery must be built before Design 1 ships.**

---

## §5. Verdict (crew synthesis)

**Build first:** Design 1 (certified-dominance release with rollback-to-best and mandatory abstain) — smallest proven delta from the residual-flip bound, directly implements scaffold-and-release, crisp falsification criteria. **Honest scope:** it converts confident-wrong into audited-abstain on the KNOWN O streams; it does not defeat an audit-clause-aware stream adversary. The real fix for P-vs-O indistinguishability is Design 2 (source-trust-gated certification), which needs the L+S program — schedule it as the follow-up, not as a reason to delay Design 1.

**Falsifying experiment to run the week after Design 1 lands:** build the adversarial battery the red-team demands — misleading-tail streams explicitly engineered to SATISFY the elimination-audit clause (front-loaded honest evidence calibrated to pass re-admission checks, back-loaded poison). Kill bar: zero certified-wrong releases; if one fires, Design 1 is demoted to a cost heuristic and Design 2 gets pulled forward. Report abstain rates per family, never pooled.

**Caveats for the coordinator:** (1) fable delivered only a partial Section 1 — everything in §§4.2–4.4 and the Design 1/2/3 rankings is native crew analysis, not fable output; treat it as a strong native position, not a second opinion. The fable second opinion on H5 depth is still effectively open. (2) Fable's Pathway 1 (irreversible elimination) is endorsed but note its worked numbers are illustrative, not ledger-derived — the elim margin is 900 on the margin gap, and the real O streams flip at calibrated stream positions, which the crew should verify per-record before citing. (3) No commits were made; all files are in the working tree under `monotonicity/`.

---

## Appendix §A — full prompt text (verbatim)

The prompt is preserved verbatim at `monotonicity/fable_prompt_h5.txt` (10,562 bytes). It batched all four tasks: (1) mechanistic explanation of depth-degradation with six candidate pathways to rank; (2) overconfidence mechanism pinpoint against the white-box confidence facts; (3) guarantee mechanism design (best-certified-answer, rollback-to-best, scaffold-and-release, abstention rules) with decision rules, certificates, falsification criteria, and predicted behavior on O/P/honest/trap; (4) red-team of the proposed mechanisms with adaptive-adversary arguments, second-order failures, cost analysis, and the single most-worrying failure. The prompt instructed "BE SUPER THOROUGH" and supplied the full verified evidence base (no-knee finding, O anti-monotonicity 1.00→0.00, cancellation artifact, §6 vs bound results, 0/127 trap catastrophe at max confidence, Micah's "more depth must never make it worse" law and the scaffold-and-release directive).

---

## Appendix §B — call log

| Attempt | Time (PDT 2026-09-24) | Result |
|---|---|---|
| 1 | ~08:15 | Partial: 1,349 completion tokens, truncated mid-sentence in Section 1 |
| 2 (retry after 5-min backoff) | ~08:25 | Provider failure: `choices: null`, 0 completion tokens |

No further rounds attempted per the one-round policy.
