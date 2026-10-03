# Amendment 2026-09-27 — A3: Protocol — freeze P1/P2 presentation and chaining, interleave items (chaining resolved)

**Status: APPROVED by Micah, 2026-09-27** (~15:21 PDT; recorded in the
governance bundle `SIGNATURE_SHEET.md`, item 1 fix 3). Enacted 2026-09-27.
The frozen prereg text is left byte-intact; this dated amendment governs.

## What it changes

The frozen §3 never specifies: whether P1 items name the parts (naming them
cues retrieval and measures nothing), whether P2 presents the pair or the
agent's own P1 answer (this decides whether (b) is a measured dependency or
a harness artifact), or whether P3 distractors are interleaved (8 blocked
distractors are position-cued — "last 8 → do nothing"). The full battery runs
a real learner; these gaps decide what the failure modes even mean.

## Frozen text reference

`PREREG.md` (frozen 2026-09-27, commit `6ca9e042110ca`), §3 "Battery phases
(per domain)":

> - **P0 — mastery gate:** 8 held-out probes per part. <7/8 → part excluded,
>   items needing it classified (a).
> - **P1 — retrieval:** for each combination C, "which parts, in which order,
>   solve C?" Wrong/missing → (b). (Separates *finding* parts from *using*
>   them.)
> - **P2 — composition:** produce C's output. Exact-match scoring.
> - **P3 — reflex probe (the survival post-mortem's mechanism):** distractor
>   items where NO part applies (correct = identity / withhold). Any part
>   application → reflexive-application count. This is failure mode (c-r):
>   uncritical application — the harmful-COMBINE analog.

## Enacted change

The P1–P3 bullets are replaced with:

> - **P1 — retrieval:** for each combination C, "which parts, in which order,
>   solve C?" P1 items must NOT name the parts — parts are referred to by
>   neutral index (part 1, part 2, …), never by their semantic labels
>   (REVERSE, DUP-FIRST, …). P1 answers are scored semantically and
>   format-tolerantly: the agent passes if it identifies the correct parts in
>   the correct order, regardless of answer formatting. Wrong or missing →
>   (b). (Separates *finding* parts from *using* them.)
> - **P2 — composition:** for each combination C, produce C's output.
>   Exact-match scoring. P2 presents the combination itself (the ordered pair,
>   referred to by neutral part indices — e.g. "apply part 2 then part 1 to
>   \<input\>"); composition correctness is scored independently of the P1
>   answer, and output scoring is decoupled from classification — a correct
>   output always counts as correct even if retrieval was scored wrong. (b)
>   vs (c) attribution uses the per-pair P1 result as the retrieval record,
>   and the battery reports both raw P2 accuracy and *elig* accuracy (P2
>   accuracy restricted to items whose pair was retrieval-correct at P1).
> - **P3 — reflex probe (the survival post-mortem's mechanism):** distractor
>   items where NO part applies (correct = identity / withhold), interleaved
>   with scored items (never run as one contiguous block). Any part
>   application → reflexive-application count. This is failure mode (c-r):
>   uncritical application — the harmful-COMBINE analog.
>
> **Chaining and item order (applies to all phases):** P2 presents each
> combination directly — never the agent's own P1 answer. The P1→P2
> dependency is measured in analysis (raw vs *elig* accuracy), not built into
> the harness: if P2 chained from the agent's P1 answer, a P1 failure would
> make P2 unscoreable and (b) would become a harness artifact. Item order is
> interleaved across pairs and phases: no fixed per-pair length pattern, no
> contiguous pair blocking (the frozen generator's 4,5,2,3 per-pair length
> cycle and contiguous pair blocking are replaced by an interleaved order in
> the full battery).

**Chaining resolution (the proposal's deliberate ambiguity, resolved here).**
The proposal left open "P2 presents the pair directly" vs "P2 presents the
agent's own P1 answer." Enacted: **P2 presents the pair directly.** The
taxonomy needs an independent composition probe — P1 measures retrieval (b),
P2 measures combination (c) — and the pilot's scoring-decoupling repair
already puts the dependency where it belongs, in the analysis (*elig*),
where it is visible and auditable rather than baked into the harness.

## Why

- If P1 names the parts, retrieval measures nothing — a learner scores
  (b)-free by echoing the prompt, and the (b)-vs-(c) split is fiction.
- If P2 silently depends on the agent's own P1 answer while the report treats
  the phases as independent, (b) becomes a harness artifact.
- If P1 scoring is format-brittle, semantically-right/format-wrong retrieval
  misclassifies as (b).
- 8 blocked distractors teach "the last 8 are do-nothing" by position alone;
  the fixed 4,5,2,3 length cycle and contiguous pair blocking are structure a
  learner can detect without composing.

## Evidence

- `pilot/REDTEAM_REPORT.md`, Family 2, §§2a–2d: prereg "never specifies" P1
  naming, P1→P2 chaining, or distractor interleaving; "Without this,
  (b)-vs-(c) attribution is undefined." §2b: lengths cycle identically per
  pair (4,5,2,3); §2c: 8 blocked distractors position-cued; §2d: semantic
  index-based P1 scoring covers the rule-naming cue. Recommended fix #5.
- §5d: "interleave item order in the full battery on principle."

## Effect

- Design freeze only — no kill bar, taxonomy code, or threshold moves.
- The proposal's chaining ambiguity is resolved here (P2 presents the pair
  directly); the builder documents the choice in the battery report.
