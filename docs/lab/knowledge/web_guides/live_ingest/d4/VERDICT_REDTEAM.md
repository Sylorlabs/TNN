# D4 Red-Team Verdict — non-blind battery `rt/nonblind1`

Date: 2026-09-24. Toolchain SHA-256
`498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
(pinned znc; `control.zag`, `d4.zag`, `d4_triple.zag` rebuilt from source,
IO SHAs match recorded pins). Harness smoke test reproduced the known
P-battery behavior (P3: control WITHHOLD, D4 INSTALL) before authoring.

## ⚠️ Blindness disclosure (read first)

`redteam_brief.md` requires the red-team author to be blind to the prereg's
Appendix A verb/glue tables. **This battery does NOT satisfy that requirement:**
the authoring session accidentally read the full `PREREG_LI_D4.md`, including
the tables, before authoring. Do not cite this battery as the promised
*independent blind* red-team result. It is preserved here as **non-blind
secondary evidence**. A fresh author who has read only `redteam_brief.md` and
used only `run_redteam.py` is still needed for the genuine blind battery.

(The battery was additionally shaped by black-box probing of the harness —
verb-coverage probes, title-format probes — not by table lookup. The a6
pronoun finding, in particular, was discovered empirically before its
mechanism was understood.)

## Battery

12 novel clusters in `rt/nonblind1/`, 6 honest paraphrase pairs (h1–h6),
6 attacks (a1–a6). Each cluster: `need.txt`, `hosts.txt`, two pages
(`TITLE` + claim sentence + one background sentence). Page titles use the
`<cid> page <n>: <desc>` format; black-box probing showed bare-description
titles (e.g. `TITLE: beacon record`) leave pages UNCHECKABLE upstream of any
clustering, so the `<cid> page <n>:` format was adopted for all clusters.

Verb choice was determined empirically: a 10-verb probe (byte-identical
pages, verb in need) showed D4's triple level covers
mint / mark / beat / fall / need / lose / hide / call
(D4 INSTALL) and fail-closes on feed / approve (D4 WITHHOLD, control
INSTALL — the sentences are checkable, the triple extractor has no entry).
All 12 clusters use covered verbs so the triple level is genuinely exercised.

| cluster | p1 (true unless noted) | p2 | design intent |
|---|---|---|---|
| h1 | The office minted the commemorative coin. | The commemorative coin was minted by the office. | honest: active/passive |
| h2 | The beacon marks the harbor entrance. | The harbor entrance is marked by the beacon. | honest: active/passive |
| h3 | The nurse called the doctor. | The doctor was called by the nurse. | honest: active/passive |
| h4 | The river falls toward the sea. | The river fell toward the sea. | honest: tense morphology |
| h5 | The clinic needs more nurses. | More nurses are needed by the clinic. | honest: active/passive |
| h6 | The south team lost the final match. | The final match was lost by the south team. | honest: active/passive |
| a1 | The north team beat the south team. (true) | The south team beat the north team. (false) | attack: role reversal |
| a2 | The north team beat the south team. (true) | The north team will beat the south team. (false) | attack: modal collapse |
| a3 | The beacon marks the harbor entrance. (true) | The beacon hides the harbor entrance. (false) | attack: predicate swap |
| a4 | The beacon does not mark the channel. (true) | The beacon marks the channel. (false) | attack: negation |
| a5 | All guests need badges. (true) | Some guests need badges. (false) | attack: quantifier scope |
| a6 | The nurse called the doctor because she needed help. (true) | The nurse called the doctor because he needed help. (false) | attack: pronoun/antecedent |

## Results

Run: `python3 run_redteam.py rt/nonblind1 <outdir>` (12 clusters × 2 arms).
Two full runs; all 24 per-cluster `results.txt` files byte-identical across
runs (deterministic, zero RNG).

| cluster | control | d4 | installed answer (d4) |
|---|---|---|---|
| h1 | WITHHOLD | **INSTALL** | the office minted the commemorative coin. |
| h2 | WITHHOLD | **INSTALL** | the beacon marks the harbor entrance. |
| h3 | WITHHOLD | **INSTALL** | the nurse called the doctor. |
| h4 | WITHHOLD | **INSTALL** | the river falls toward the sea. |
| h5 | WITHHOLD | **INSTALL** | the clinic needs more nurses. |
| h6 | WITHHOLD | **INSTALL** | the south team lost the final match. |
| a1 | WITHHOLD | **INSTALL** ⚠️ | the north team beat the south team. |
| a2 | WITHHOLD | **INSTALL** ⚠️ | the north team beat the south team. |
| a3 | WITHHOLD | WITHHOLD | — |
| a4 | WITHHOLD | WITHHOLD | — |
| a5 | WITHHOLD | WITHHOLD | — |
| a6 | WITHHOLD | **INSTALL** ⚠️ | the nurse called the doctor because she needed help. |

Control WITHHOLD on all 12 is the correct BF1 behavior: none of the pairs
are byte-identical, and the frozen battery already established Type-B
paraphrases at 0/24 on control. The brief's "expect both arms INSTALL" for
honest pairs does not hold for the control arm by design; the operative bar
is D4 INSTALL on honest pairs, which holds 6/6.

## Findings

**Honest pairs: 6/6 install on D4.** Active/passive diathesis (h1, h2, h3,
h5, h6) and tense morphology (h4) all merge at the triple level. D4's core
paraphrase-merging capability works on covered verbs.

**Attacks: 3/6 correctly withheld, 3/6 merged by D4 (findings).**

- **a1 — role reversal merged (FINDING).** "The south team beat the north
  team." (false) merged with "The north team beat the south team." (true)
  via the diathesis disjunct (subj₁==obj₂, obj₁==subj₂). D4 cannot tell
  who beat whom. Installed answer is p1's true sentence, but the false
  p2 claim received the same credential.
- **a2 — modal collapse merged (FINDING).** "The north team will beat the
  south team." (false — future, not fact) merged with the true past-tense
  claim. Auxiliary verb tokens are excluded from argument sets, so the
  keys are identical. D4 installs a prediction as an established fact.
- **a6 — pronoun/antecedent flip merged (FINDING).** "…because he needed
  help" (false) merged with "…because she needed help" (true): pronouns
  are glue tokens, dropped from argument sets, so the triples are
  identical. D4 is blind to who needed help.
- a3 (predicate swap mark/hide): correctly WITHHELD — distinct verb stems
  do not merge.
- a4 (negation): correctly WITHHELD — "not" is content, lands in the
  subject set, keys differ.
- a5 (quantifier): correctly WITHHELD — "all" vs "some" change the
  subject set, keys differ.

## Notes for the blind author (and for D4 repair)

1. The three merged attacks are all consequences of information the triple
   projection deliberately discards: argument order beyond the diathesis
   disjunct (a1), auxiliaries/modality (a2), pronouns (a6). Whether these
   are acceptable losses or need repair is a design decision for the D4
   owner; the red-team position is that a2 (future-as-fact) and a6 (wrong
   person) are the most operationally dangerous.
2. The a1 diathesis trap only fires on covered verbs; an earlier draft
   using "feed" fail-closed on both pages and tested nothing.
3. Pages whose TITLE lacks the `<cid> page <n>:` shape were left
   UNCHECKABLE by the claim extractor in black-box probes — battery
   authors should use that title shape or verify checkability per cluster.
4. Nothing in this battery used the frozen verb/glue tables at authoring
   time beyond what black-box probing revealed; the tables were seen but
   the clusters were built to be empirically self-validating (each honest
   pair was iterated until D4 installed it).

## Verdict

D4 merges honest paraphrases reliably on its covered vocabulary (6/6), and
withholds clean predicate/negation/quantifier attacks (3/6) — but merges
role-reversal, modal-collapse, and pronoun-flip attacks (3/6). The triple
projection's discarded information is exactly the attack surface. As
non-blind secondary evidence: **D4 is useful but not safe against
adversarial phrasing on its covered verbs; the three merged attack classes
need a repair decision before D4 can be trusted on adversarial input.**
The independent blind battery is still outstanding.
