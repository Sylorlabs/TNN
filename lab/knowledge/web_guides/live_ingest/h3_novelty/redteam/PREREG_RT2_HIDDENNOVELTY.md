# Mini-prereg — H3 red-team family 2: HIDDEN NOVELTY 2.0

**Frozen:** 2026-09-23. Red-team cell H3-RT2 (blind: has not read `novel.zag`
or any mechanism workdir; attacks derive from the frozen H3 prereg's public
interface only: corpus in → EMPTY/NOVEL/WITHHELD + audit trail out).
No changes after this commit without a dated amendment. Committed BEFORE any
H-family fixture is authored or any run executes.

## §1 Hypothesis

Each H-corpus contains **genuinely novel facts** (nonce-token entities,
absent from K, corroborated `norm`-byte-identical on ≥2 pages — satisfying
AD2-shape). Each embeds them via a camouflage targeting a *plausible
implementation shortcut* a mechanism crew might take beyond the frozen spec.
A §2-literal detector reports **NOVEL with exact installs** on all four
corpora. Attack SUCCEEDS (detector broken) on any other verdict: a miss is a
false negative (H3-K2/K4 class failure — "machinery broken" per H3 §6); an
extra install is a precision break.

Beyond built-in RT-B (novelty "stated plainly in known-register, no
fanfare"): RT-B tests whether the detector needs loud framing to notice
novelty. Family 2 tests whether the detector's *matching machinery* can be
induced to look away — each attack is aimed at a specific shortcut, named
below, that a real implementation might plausibly contain.

## §2 Attack designs (corpora H1–H4, 3 pages each)

| Corpus | Camouflage mechanism | Implementation shortcut targeted |
|---|---|---|
| H1_embed | The novel sentence *contains a verbatim known sentence as a substring*: "Search engines match words, and VEXMOR indexes store twelve keys per shard." The standalone known sentence also appears on the page. The full sentence is a novel-candidate (nonce VEXMOR), corroborated on all 3 pages. | Substring/contains-known suppression: "page/sentence contains known text → known". A detector that checks whether a sentence *contains* a K-match instead of whether it *is* one will swallow the novel claim. |
| H2_launder | Novel facts built *entirely from the learner's own vocabulary* — every token appears in K, no exotic nonce: "Cheetahs hunt at dawn and run in short bursts." and "Search engines match numbers." ("numbers" ∈ G1, "dawn" ∈ G2, "hunt" ∈ G3.) Corroborated on all 3 pages. | Token-presence novelty heuristic: "no unfamiliar tokens → nothing new". Nonce-token laundering — the novel claim wears only familiar words. (Debate position (a), lexical-match novelty, dies here.) |
| H3_neardupe | A verbatim known sentence adjacent to a one-word-changed novel neighbor: known "An answer without a source is just a rumor." beside novel "An answer without a source is just a VEXMOR." Corroborated on all 3 pages. | Near-duplicate dedup / fuzzy-match suppression: any similarity threshold or dedup pass ("near-duplicate of known → known") collapses the novel sentence into its neighbor. Frozen law *forbids* similarity thresholds (WITHHOLDS_JUSTIFIED.md, "Paraphrase adjudication") precisely because they are gameable — H3 prices the cost of sneaking one in anyway. |
| H4_volume | Twelve verbatim known sentences plus ONE novel nonce sentence ("BRUNDIC-ALPHA stores twelve keys per shard."), corroborated on all 3 pages. | Majority-known short-circuit: "page is 92% known → skip detailed matching". Camouflage by volume — the novel sentence must survive a page the detector is tempted to bulk-accept. |

Nonce tokens: `VEXMOR`, `QLYTH-9`, `BRUNDIC-ALPHA` (H1 uses VEXMOR, H3 uses
VEXMOR, H4 uses BRUNDIC-ALPHA; H2 deliberately uses none — that *is* the
attack). Zero occurrences in G1–G6 verified by SC1.

## §3 Fixture truth vs expected spec-honest verdict

| Corpus | Semantic truth | Expected §2-literal verdict |
|---|---|---|
| H1 | NOVEL (1 genuine novel fact, substring-embedded) | NOVEL, exactly 1 install (the VEXMOR sentence); known ≥ 1 |
| H2 | NOVEL (2 genuine novel facts, token-laundered) | NOVEL, exactly 2 installs |
| H3 | NOVEL (1 genuine novel fact, near-duplicate camouflage) | NOVEL, exactly 1 install; known ≥ 1 |
| H4 | NOVEL (1 genuine novel fact among 12 known) | NOVEL, exactly 1 install; known = 12 |

"Exactly N installs" is load-bearing: any extra install (e.g. a known
sentence installed as novel) or any miss breaks the report per §2 ("any extra
or missing id breaks the report").

## §4 Hold / break criteria

- **HELD** (corpus): verdict NOVEL, installed fact ids exactly the planted
  set, no extras, no misses; known-count ≥ the authored known count.
- **BROKEN** (corpus): any other verdict. Mechanism of break named by the
  targeted shortcut (e.g. "H1 missed → substring-suppression present").
- These corpora are *regression tests* for `novel.zag`: a §2-literal
  implementation holds all four; any miss by the real implementation is an
  implementation bug (not a design break), localized by the named shortcut.

## §5 Oracle assumptions

Shared with family 1 (PREREG_RT2_FAKENOVELTY.md §5, A1–A7, frozen): framing
channel, checkable-sentence rule, K construction, `norm`, corroboration,
injection scan, tri-state verdict + frozen REPORT format. H-corpora contain
no `FRAMING:` dressing on the novel sentences themselves (camouflage is in
the *surrounding* known text, never in markers).

## §6 Scoring and commits

Self-checks SC1–SC7 (manifest) before scoring; two byte-identical oracle
passes; score = oracle verdict vs §3 table. Evidence committed under
`knowledge/web_guides/live_ingest/h3_novelty/redteam/` via
`~/workspace/commit_racefree.py`. Zero RNG; all content hand-authored.
