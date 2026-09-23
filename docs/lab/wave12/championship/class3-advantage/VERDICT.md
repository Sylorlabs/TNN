# CLASS-3 ADVANTAGE — Verdict

**Date:** 2026-09-21  
**Status:** H1–H4 resolved by code analysis + exact mechanical proof. No znc available on this VM; the H4 proof reimplements the frozen deterministic functions (byte-exact logic) rather than running the binary.

## 1. Score decomposition (from frozen verdicts)

| Source | Class 4 | Class 3 | Gap | Mastery Δ | Cost Δ |
|---|---|---|---|---|---|
| Grok | 0.9911 | 0.9959 | **+0.0048** | 0.0000 | +0.0048 |
| Sol | 0.9909 | 0.9933 | **+0.0024** | 0.0000 | +0.0024 |
| Step | 0.9911 | 0.9822 | **−0.0089** | −0.0131 | +0.0042 |
| Swe | 0.9033 | 0.8908 | **−0.0125** | −0.0135 | +0.0010 |

**Finding:** The teacher route ALWAYS improves the cost component. It SOMETIMES loses mastery. The net gap = cost gain − mastery loss. Grok's entire +0.0048 is cost accounting; zero capability component improved.

## 2. H1 (restructure) — REFINED, not confirmed

The advantage is not from "reorganization improving learnability." It is from **verification amortization**: the teacher has already done the expensive eliminative verification during D2 learning, so teaching from its organized store costs fewer ops. Mastery/revisability/integrity/retention never improve under the teacher route in any source. **H1's mechanism is wrong; the cost effect is real but is amortization, not restructuring.**

## 3. H2 (verification filter) — SUPPORTED in refined form

The operative filter is the teacher's honesty gate in the teaching loop (`s37_slice`: `if(s37_teacher_status(ts,fid)==1){teach}else{skip}`), NOT §B.7. The teacher was never §B.7-verified before teaching; §B.7 in the verdict scores the fresh learner. The gate honestly refuses to teach facts the teacher does not hold truly, and every skip is audited.

## 4. H3 (noise interaction) — KILLED as stated; REFINED

The simple "noisy sources lose more" is **killed**: Step's corpus has ZERO transcription errors (verified: all 240 input claims reproduced exactly, obs==probe==claim, no distract collisions), yet Step shows a −0.0089 gap. The refined version holds: **mastery loss scales with teacher INCOMPLETENESS, whatever its cause.**

## 5. H4 (step anomaly) — SOLVED

**The 9 skipped facts are exactly the 9 D2 held-out facts that fall inside the 192 teaching slices.** Proof:

- The D2 curriculum lawfully holds out 12 fact ids per rep (never taught; curriculum-hole control): `q2_heldout(rep,k) = q2_pool_id((rep*17+k*37)%186)`.
- Rep-0 held-outs: **[1, 47, 48, 49, 96, 97, 146, 147, 194, 196, 238, 239]**.
- Teaching slices: `q1_slice_fact(s,k) = q1_probe_id((s*24+k)%228)`, 192 facts.
- Overlap: **9 facts [1, 47, 48, 49, 96, 97, 194, 196, 238]**.
- Per-slice overlap: **1, 2, 0, 0, 2, 3, 0, 1** — **exactly matches** the step verdict's per-slice skips (1, 2, 0, 0, 2, 3, 0, 1).

The probability of 8 independent slice counts matching by chance is negligible. The step "anomaly" is the honesty filter working as designed on an incomplete teacher.

## 6. The source pattern is an implementation artifact

| Crew | Teacher construction | Held-out excluded? | Skips | Class-3 result |
|---|---|---|---|---|
| Grok | `gg_teacher_build`: "No held-out: the teacher is the full corpus" | NO | 0 | wins (+0.0048) |
| Sol | (mastery 1.0 ⇒ 0 skips ⇒ complete teacher) | NO | 0 | wins (+0.0024) |
| Step | `s37_teach` = D2 with 12 held-outs | YES | 9 | loses (−0.0089) |
| Swe | D2-taught learner, rep-0 held-out geometry ("teacher gap 9/192") | YES | 9 | loses (−0.0125) |

**Micah's pattern ("grok/sol class-3 wins, step/swe class-3 loses") is fully explained by whether the crew's teacher excluded the 12 held-out facts — not by any property of the source LLMs.** Grok is not "best at teaching a TNN teacher"; the grok crew simply built a complete teacher.

## 7. Answers to Micah's three questions

1. **Is Grok best at teaching a TNN teacher that then trains another TNN?** No. The grok-corpus teacher wins because it is complete (no held-outs), not because Grok is a better source. Any source's teacher wins when complete.
2. **Is class 3's advantage architectural?** Yes — two architectural effects: (a) **verification amortization** (teacher route always cheaper; cost component always rises); (b) **honesty filtering** (teacher only teaches what it holds truly; incomplete teachers lose mastery). The net gap = (a) − (b).
3. **Legitimate real-world cases or toy evaluations?** Mechanism evaluations on synthetic content. The TNN implementations, teaching path, audit ledger, and batteries are real native mechanisms; the Zharovia facts are invented. Legitimate architecture evidence; NOT real-world language evidence. The real-English championship (dispatched separately) is the real-world test.

## 8. SWE note

SWE's class-3 loss (−0.0125) is the same 9-held-out-skip mechanism as Step (191/200 = 8 scaffold + 183 taught = 9 skipped), not the "12 fooled falsehoods." The corpus values are clean for all sources (verified). This does not overturn the ban (a behavioral ruling about the model), but the score gap itself is a teacher-completeness effect.

## 9. Open items (need znc or a crew with the toolchain)

- N=5 byte-identical reruns of a **standardized** class-3 (same teacher completeness, same battery, same cost formula for all sources) to measure the true architectural gap with the confounders removed.
- The prereg's "same Track 5 metrics" was not implemented identically (legA 198 probes vs teach3 192 slice facts); standardize before claiming cross-source comparisons.

## Evidence

- `PREREG.md` (this directory): preregistration with kill bars.
- Frozen verdicts: `G_GROK_VERDICT.md`, `S37_VERDICT.md`, night log (SWE), all committed on `tnn-native-lab`.
- Teacher code: `gg_teacher.zag` ("No held-out"), `s37_step.zag` (`s37_slice` honesty gate), `q2s_trial.zag` (`q2_heldout`, `q2_teach`), `q1_world.zag` (`q1_slice_fact`).
- Corpus audit: all four corpora numerically identical except distractor values (verified 2026-09-21).
- H4 proof: `/tmp/c3a` Python reimplementation (deterministic functions, exact match).
