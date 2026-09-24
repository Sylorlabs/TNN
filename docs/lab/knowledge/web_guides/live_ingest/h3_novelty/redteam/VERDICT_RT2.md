# VERDICT — H3 red-team RT2: three novel attack families vs the frozen novelty spec

**Red-team cell:** H3-RT2, 2026-09-23. **Blind:** the cell has not read
`novel.zag` or any mechanism workdir; all attacks derive from the frozen H3
prereg's public interface (corpus in → EMPTY/NOVEL/WITHHELD + audit trail
out). **Method:** attack corpora were executed against `oracle/spec_oracle.py`,
a reference implementation of frozen H3 §2 written *literally* from the
prereg text plus interface assumptions A1–A8 (frozen in the mini-preregs).
The oracle is the honest-detector reference and mechanical scorer — not the
mechanism. "Broken" below means: the spec-conformant, honest verdict on the
corpus is semantically wrong. Zero RNG everywhere; two full passes
byte-identical (`diff -rq evidence/run1 evidence/run2` clean, SC7).

**Commits:** mini-preregs `1ddba58` (frozen before fixtures); this verdict +
corpora + manifest + oracle + evidence committed separately (SHA in parent
report).

## Scoreboard — 16/16 oracle verdicts matched preregistered expectations

| Corpus | Semantic truth | Expected | Observed | Result |
|---|---|---|---|---|
| F1_translation | EMPTY | NOVEL, 3 inst | NOVEL, 3 inst | **BROKEN (design)** |
| F2_negation | EMPTY | NOVEL, 2 inst | NOVEL, 2 inst | **BROKEN (design)** |
| F3_split | EMPTY | NOVEL, 4 inst | NOVEL, 4 inst | **BROKEN (design)** |
| F4a_known | EMPTY | EMPTY | EMPTY, known=3 | HELD |
| F4b_smuggle | EMPTY | NOVEL, 2 inst | NOVEL, 2 inst | **BROKEN (design)** |
| F5_normgap | EMPTY | NOVEL, 2 inst | NOVEL, 2 inst | **BROKEN (design)** |
| H1_embed | NOVEL | NOVEL, exactly 1 | NOVEL, exactly 1, known=2 | HELD |
| H2_launder | NOVEL | NOVEL, exactly 2 | NOVEL, exactly 2, known=1 | HELD |
| H3_neardupe | NOVEL | NOVEL, exactly 1 | NOVEL, exactly 1, known=1 | HELD |
| H4_volume | NOVEL | NOVEL, exactly 1 | NOVEL, exactly 1, known=12 | HELD |
| L1a/b/c_drip | WITHHELD | WITHHELD ×3 | WITHHELD ×3, SINGLE_SOURCE | HELD |
| L2a/b_xbound | WITHHELD | WITHHELD ×2 | WITHHELD ×2, SINGLE_SOURCE | HELD |
| L3_partial | WITHHELD | WITHHELD | WITHHELD, SINGLE_SOURCE, failed=2 | HELD |

11/16 corpora HELD (F4a, all of families 2–3); **5/16 BROKEN — all five at
the frozen-design level** (no implementation of H3 §2 as written can do
better without a spec amendment).

## The five breaks (each a distinct equivalence byte-identity cannot see)

1. **F1 — translation-equivalents.** Three installed-guide sentences in
   Spanish, corroborated on 3 pages, install as novel. Break mechanism:
   cross-language propositional identity is invisible to `norm`. This is
   the frozen paraphrase non-goal made concrete: a spec-conformant detector
   MUST install translations of known facts as novel. Any paraphrase
   tolerance would violate frozen law (WITHHOLDS_JUSTIFIED.md); byte-identity
   manufactures novelty instead. Both horns documented.
2. **F2 — double-negation restatements.** "It is not the case that the claim
   that [verbatim S] is false" installs as novel. Break mechanism: logical
   equivalence invisible to `norm` — the known sentence sits inside intact,
   wrapped in a negation shell.
3. **F3 — fact-splitting.** Halves of P1/P2 ("Search engines match words."
   / "Pick out the words that carry the meaning and leave the rest behind."
   …) each install as novel (4 installs for 2 known facts). Break mechanism:
   compositionality — the conjunction is the known fact, but no half
   matches K.
4. **F4b — cross-corpus nonce-substitution smuggling.** "VEXMOR engines
   match words, …" installs as novel. Break mechanism: §2 "provable
   absence" (fresh nonce ⇒ novel) is gameable by entity-substitution on a
   known template. The smuggling crosses the corpus boundary: F4b never
   shows the original beside the substitution, and per-corpus processing
   cannot link them. A unified learner (H3 §6's unified mode — "humans stay
   the same") would notice the template; the per-corpus detector cannot.
5. **F5 — normalization-gap.** Verbatim known sentences carrying U+200B /
   U+200D install as novel. Break mechanism: frozen `norm` (lowercase +
   whitespace-collapse) has no character model for invisible format
   characters. Verified: stripping the two zero-width chars from each
   installed form yields a K member — the "novelty" is 100% invisible
   characters. Remediation is a spec amendment (strip Cf format chars in
   `norm`), noted, not applied: the frozen spec is what's tested.

Per H3 §6, these five breaks collectively "re-open whether
content-matching alone can ever ground novelty — a design question, not a
tuning one." They are also the evidence for the FAIL-on-K1/K3 mapping
("production must not auto-install … until the framing attack is defeated"
— here generalized beyond framing).

## What held, and what it means

- **F4a (verbatim known → EMPTY, known=3):** the baseline works; the five
  breaks above are not an artifact of a generally trigger-happy oracle.
- **H1–H4 (all NOVEL-exact):** a §2-literal detector catches
  substring-embedded (H1), token-laundered (H2), near-duplicate-camouflaged
  (H3), and volume-camouflaged (H4) genuine novelty with exact report ids.
  These four corpora are committed **regression tests for `novel.zag`**: any
  miss by the real implementation localizes to the named shortcut
  (substring-suppression, token-presence heuristic, fuzzy dedup,
  majority-known short-circuit) — an implementation bug, not a design break.
- **L1a/b/c (3/3 WITHHELD, SINGLE_SOURCE):** slow-drip novelty does not
  degrade into EMPTY; the withhold ledger accumulates.
- **L2a/b (WITHHELD ×2, SINGLE_SOURCE each):** the cross-boundary VEXMOR
  sentence was NOT pooled — per-corpus G4 held; 0 installs. A pooling
  implementation would have installed; the pair is a committed boundary test.
- **L3 (WITHHELD, not INFRA-FAIL):** 2/3 pages fetch-failed, but checkable
  sentences arrived on the survivor, so INFRA-FAIL correctly did not fire
  and the single-sourced novel fact was withheld with a named gate — never
  laundered to EMPTY.

Run-level aggregate from the 16 REPORT lines: 6 installs of fake novelty
(F1/F2/F3/F4b/F5 — the design breaks), 5 installs of genuine novelty
(H1–H4, all exact), 6 named withholds, 1 clean EMPTY, 0 EMPTY-laundering.
A rollup that prints only installs would hide the 6 withholds — the
aggregate must carry withheld counts (family-3 §3 requirement).

## Interface findings (for the mechanism crew, not breaks)

1. **K-construction is under-specified by the frozen prereg.** WORKED-example
   sentences (elephant lifespan, cheetah speed) occur only inside
   `W|`/`C|`-prefixed lines, and first-sentences of PRINCIPLE paragraphs
   glue to the `MODULE:`/`TITLE:` header in sentence-space — neither is a
   bare installed sentence under a sentence-split K-construction. The red
   team used only 12 script-verified standalone PRINCIPLE sentences
   (`norm(Pn) ∈ K` checked mechanically). The mechanism crew's AD4
   ("every factual sentence norm-byte-identical to an installed memory")
   needs the same pinning, or E/A fixture truth is not mechanical.
2. **Framing channel (A1):** corpora mark framing with `FRAMING:` lines
   (standing in for RT-A's "BREAKING"/"scientists reveal"). Any detector
   needs *some* framing handling; the marker makes the red team's
   assumption explicit and auditable. SC6 verified no corpus trips the G6
   injection scan.

## Pending (out of this cell's reach)

- **Run `novel.zag` against these 16 corpora** (mechanism crew /
  coordinator): H1–H4 and L1–L3 must reproduce this scoreboard exactly; any
  deviation is an implementation finding. F1–F5 are expected to reproduce
  the BROKEN verdicts — they test the spec, and the spec is frozen.
- The five design breaks need Micah-visible disposition: spec amendments
  (translation/paraphrase adjudication, logical-equivalence,
  compositionality, nonce-template analysis, `norm` character model) or
  acceptance as known boundaries per H3 §6. The red team does not amend
  frozen law.

## Artifacts (all under `knowledge/web_guides/live_ingest/h3_novelty/redteam/`)

`PREREG_RT2_*.md` (3 frozen mini-preregs + 2026-09-23 amendment),
`MANIFEST_RT2.md` (truth table + 48 page SHAs), `corpora/` (16×3 pages),
`oracle/spec_oracle.py` (§2-literal reference), `tools/build_corpora.py`,
`tools/selfcheck.py` (1233/1233 PASS, log in `evidence/selfcheck.log`),
`evidence/run1/`, `evidence/run2/` (byte-identical reports + SHASUMS),
`VERDICT_RT2.md` (this file).
