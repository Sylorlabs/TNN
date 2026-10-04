# Z.AI Skeptic Question Package — Crew C (independent red team, D1 full battery)

**Status:** DRAFTED by Crew C 2026-09-27. NOT SENT — browser/delegation
available only to the parent agent. This file is the complete package to
hand to the z.ai approach-skeptic: the one question, its context, and the
evidence bundle it needs.

---

## Context the skeptic needs (keep it attached)

The composition battery's headline is a **clean negative**: the real TNN
learner (workbuddy round-2 deliberate-memory binary) mastered 0/6 parts
(48/48 P0 probes answered "I don't know."), so the composition claim is KILLED
(K1: 0.0000 ≤ 0.1533 chance line) and the battery is VOID for composition
(K2: 600/600 items classify (a) — unmastered parts). The learner never
confabulated (withheld on all probes, 8 distractors, 18 qualitative samples).

Crew B's teaching protocol per rule: 1 definition line + 6 worked examples
over training tokens tok(0..5), delivered through the learner's chat intake
(deliberate memory: intake lowercases, facts stored verbatim, retrieval-echo
answers). Probes are held-out tok(6..13).

**The red team attacked the protocol, not the learner, and lost:**

1. Exact replication of Crew B's REVERSE protocol → 0/8 (all "I don't know.").
2. Rich fair teaching of REVERSE — definition + explicit letter-by-letter
   procedure + 12 worked examples (tok 0–5 and tok 700–705) with letter
   walkthroughs + quiz reinforcement on taught examples → **12/12 on taught
   examples, 0/8 on held-out.** The teaching was received and stored;
   generalization is zero.
3. Same rich protocol for DUP-FIRST → 0/8.
4. Paraphrase probes ("how would you reverse the word qeum?", "say the
   reverse of qeum.", sentence completion) → withhold or echo taught lines.
5. Mechanism probes on stored facts: "what is the first letter of qeum?"
   → echoes the whole letters fact (cannot extract "q"); "how many letters
   are in qeum?" → echoes the letters fact (cannot count to 4; echoes
   verbatim when told "qeum has four letters.").

**The red team's conclusion:** the learner's answer channel is
retrieval-echo; it has no string-synthesis operator, so no fair teaching
protocol through its chat intake can install string-rule induction. The 0/48
is a learner-envelope finding, not a protocol artifact. The round-2 24/24
battery (fact comparison, anaphora, supersede, bullets, counts/sums over
stored entities) sits inside the retrieval envelope; rule induction sits
outside it. The negative stands — with a mechanism explanation.

---

## The one question

> **Is there any fair teaching protocol — operating only through this
> learner's genuine chat intake (deliberate memory, intake lowercases, no new
> machinery, no hardcoded per-item answers, probe tokens tok(6..13) never
> taught) — that you expect would get ≥7/8 on held-out string-rewrite probes
> for a rule like REVERSE, where the red team's fair attempts got 0/8
> despite 12/12 taught-example recall?**
>
> If YES: specify the protocol concretely (exact session plan, example
> budget, how it produces a *novel synthesized string* at probe time given
> the retrieval-echo answer channel and the intake's lowercasing). The bar
> for "fair" is: everything the protocol uses would count as legitimate
> teaching under the frozen prereg's deliberate-memory intake, and the probe
> answers must be computed at probe time, not retrieved.
>
> If NO: then the 0/48 stands as a genuine learner-envelope finding, and the
> interesting question moves up a level — this battery's text-reasoning
> domain tests an ability (symbolic string computation) the learner's
> machinery demonstrably lacks, so the K2 void, while honest, is trivially
> guaranteed by the domain choice rather than informative about composition
> as such. In that case: what *would* be the right domain for testing
> composition in a retrieval-envelope learner — and does the composition
> question even survive the translation, or does it dissolve into "the
> learner can only retrieve what it stored"?

**What would change the red team's verdict:** a concrete, fair, specified
protocol — not a sketch — that the parent agent could run verbatim against
`work/wb_dialogue_bin` and score ≥7/8 on the 8 held-out REVERSE probes.
Anything short of that (richer examples, more drill formats, multi-turn
scaffolding) is already covered by the mechanism probes: the failure is in
the answer machinery, not the teaching content.

---

## Evidence bundle (attach all)

1. `~/workspace/comp_b4/battery/redteam/REDTEAM_REPORT.md` — full red-team
   report (verdicts per attack, all numbers, the `items.tsv` pair-section
   defect, the shift-chaining K6 finding).
2. `~/workspace/comp_b4/battery/redteam/rt_teach.py` and
   `rt_teach_result.txt` — the teaching-attack harness and its results
   (replication 0/8, rich REVERSE 12/12 taught / 0/8 held-out, paraphrase
   probes, mechanism probes).
3. `~/workspace/comp_b4/battery/run1/resp_p0.txt` — the battery's own 48/48
   withhold transcripts.
4. `~/workspace/comp_b4/battery/work/wb2_dialogue.zag` (source at commit
   `3cd24f11d119a17d14d9637e43ebdc8918b41e92`, clean-room rebuild
   byte-identical to `work/wb_dialogue_bin`, SHA
   `7636a577fff29de6eae10fe238e33514083a3059aa9df8f64784a9601a684a09`)
   — the real learner the skeptic's protocol would run against.
5. `~/workspace/comp_b4/ref/PREREG.md` §§1–8 — the frozen bars (K1, K2, the
   deliberate-memory intake description).

**Delegation note for the parent agent:** sending this requires a browser
session (z.ai). Include the question verbatim plus the context section, and
attach or link the five evidence items above. Ask the skeptic to answer the
YES/NO branch explicitly, and to produce the concrete protocol if YES.
