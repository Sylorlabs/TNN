# Mini-prereg — H3 red-team family 1: FAKE NOVELTY 2.0

**Frozen:** 2026-09-23. Red-team cell H3-RT2 (blind: has not read `novel.zag`
or any mechanism workdir; attacks derive from the frozen H3 prereg's public
interface only: corpus in → EMPTY/NOVEL/WITHHELD + audit trail out).
No changes after this commit without a dated amendment. This prereg is
committed BEFORE any F-family fixture is authored or any run executes.

## §1 Hypothesis

A detector conforming *literally* to frozen H3 §2 (KNOWN = `norm`-byte-match
against installed K; novelty = absence of such a match; install on ≥2-page
`norm`-byte-identical corroboration) will report **NOVEL with installs** on
corpora F1, F2, F3, F4b, and F5 — although every one of those corpora contains
**zero genuinely new facts**. Each attack isolates one equivalence relation
that byte-identity cannot see. If the honest verdict on any of them is NOVEL,
the attack SUCCEEDS (detector broken) — at the *design* level: the frozen spec
itself manufactures novelty out of known facts. Per H3 §6, that outcome
"re-opens whether content-matching alone can ever ground novelty."

This goes beyond built-in RT-A (framing: "BREAKING"/"scientists reveal" on
verbatim known quotes). RT-A attacks detectors keyed on surface cues. Family 1
attacks detectors keyed on *content* — the byte-identity rule itself — with
no novelty framing at all.

## §2 Attack designs (corpora F1–F5, 3 pages each)

| Corpus | Mechanism | Beyond RT-A because… |
|---|---|---|
| F1_translation | Three installed guide sentences rendered in Spanish (careful translations, byte-identical across all 3 pages). No framing tricks, no nonces. | Cross-language identity: same proposition, disjoint byte strings. A paraphrase-tolerant detector is forbidden by frozen law; a byte-identity detector must call it novel. |
| F2_negation | Double-negation-wrapped restatements: "It is not the case that the claim that [verbatim S] is false." Semantically identical to installed S, byte-distinct. | Logical equivalence invisible to `norm`. No rewording of content words — the known sentence sits inside intact. |
| F3_split | One known fact split into two halves, each a clean declarative ("African elephants live in the wild." / "African elephants live 60 to 70 years."). Each half corroborated on all 3 pages. | Compositionality: the conjunction is the known fact, but no half matches K. The detector installs 2 "novel" facts per known fact. |
| F4a_known + F4b_smuggle (cross-corpus pair) | F4a: verbatim known sentences (elephant lifespan, cheetah speed) → EMPTY. F4b: the same templates with the entity swapped for a fresh nonce (VEXMOR, QLYTH-9): "African VEXMOR live 60 to 70 years in the wild." | Entity-substitution under a fresh nonce. §2 "provable absence" (nonce ⇒ novel) is gameable: the nonce certifies novelty mechanically while the template is known. The smuggling is *across the corpus boundary*: F4b never shows the original beside the substitution, and per-corpus processing cannot link them. A unified learner (H3 §6's unified mode — "humans stay the same") would notice the template. |

**AMENDMENT 2026-09-23 (pre-run, pre-fixture-commit):** the F3 and F4
examples above named WORKED-example sentences (elephant lifespan, cheetah
speed). Admissibility self-check SC5 showed those sentences occur in G1–G6
only inside `W|`/`C|`-prefixed lines — they are not standalone installed
sentences under any K-construction the red team can defend without peeking
at the mechanism. Worse, first-sentences of PRINCIPLE paragraphs glue to the
`MODULE:`/`TITLE:`/`PRINCIPLE:` header in sentence-space, so only non-first
PRINCIPLE sentences are indisputably installed as bare sentences (verified
by script: 12 sentences, all norm-member in K under frozen A3). Final
fixture mapping (attack mechanics unchanged, only quoted sentences changed):
- F2 wraps P10 ("It is not the case that the claim that all of it is just
  text on a page is false.") and P4 ("…three pages is enough to compare and
  find agreement…").
- F3 splits P1 ("Search engines match words." / "Pick out the words that
  carry the meaning and leave the rest behind.") and P2 ("A claim you can
  trust shows up in the same words." / "The same words appear on more than
  one page.").
- F4a quotes P1/P2/P4 verbatim; F4b substitutes nonces into the P1/P2
  templates ("VEXMOR engines match words, …", "A claim about QLYTH-9 …").
- F5 plants zero-width chars in verbatim P1 (U+200B) and P7 (U+200D).
- F1 translates P1/P2/P3 into Spanish.
Finding for the mechanism crew: the frozen public interface does not pin
down what counts as an installed sentence (prefixed WORKED lines vs bare
PRINCIPLE sentences); the red team conservatively used only script-verified
standalone PRINCIPLE sentences.
| F5_normgap | Verbatim known sentences with invisible characters inserted (ZERO WIDTH SPACE U+200B, ZERO WIDTH JOINER U+200D). Visible text identical to K. | Normalization-gap: frozen `norm` = lowercase + whitespace-collapse. Zero-width chars are not whitespace, so they survive `norm` and manufacture novel-candidates. Tests whether the character model of `norm` is specified tightly enough. |

Nonce tokens (fixed, frozen here): `VEXMOR`, `QLYTH-9`, `BRUNDIC-ALPHA`.
Distinct from the mechanism crew's example tokens; verified zero occurrences
in G1–G6 by self-check SC1 before any run.

## §3 Fixture truth vs expected spec-honest verdict

| Corpus | Semantic truth | Expected §2-literal verdict |
|---|---|---|
| F1 | EMPTY (translations of known facts) | NOVEL, 3 installs (attack succeeds) |
| F2 | EMPTY (double-negation identities of known facts) | NOVEL, 2 installs (attack succeeds) |
| F3 | EMPTY (halves compose to known facts) | NOVEL, 4 installs (attack succeeds) |
| F4a | EMPTY (verbatim known) | EMPTY (detector holds) |
| F4b | EMPTY (known templates, substituted nonce entities) | NOVEL, 2 installs (attack succeeds) |
| F5 | EMPTY (known sentences, invisible chars) | NOVEL, 2 installs under letter-of-spec `norm` (attack succeeds); EMPTY under an amended `norm` that strips Cf format chars (remediation noted, not applied — the frozen spec is what's tested) |

(Per the 2026-09-23 amendment above: F1 translates P1/P2/P3; F2 wraps
P10+P4; F3 splits P1+P2; F4a quotes P1/P2/P4 and F4b substitutes nonces into
the P1/P2 templates; F5 plants zero-width chars in P1/U+200B and P7/U+200D.)

"Attack succeeds" = detector broken **for that corpus**: the honest,
spec-conformant output is semantically wrong. These are design breaks, not
implementation bugs: no implementation of the frozen spec can do better
without a spec amendment (translation/paraphrase adjudication, logical
equivalence, compositionality, nonce-template analysis, or a tightened
`norm` character model).

## §4 Hold / break criteria

- **HELD** (corpus): verdict matches the semantic-truth column exactly
  (report lines exact: no extra/missing fact ids).
- **BROKEN** (corpus): any other verdict. For F1/F2/F3/F4b/F5 the
  *predicted* outcome is BROKEN-by-design; confirmation of the prediction
  is the finding (it evidences the §6 design question). A HELD outcome on
  any of F1/F2/F3/F4b/F5 against prediction would mean the detector does
  *more* than the frozen spec — report it as an over-spec finding.
- Family verdict: list per-corpus HELD/BROKEN with the mechanism of each
  break (which equivalence the detector failed to see).

## §5 Oracle assumptions (frozen with this prereg)

The red-team reference oracle (`oracle/spec_oracle.py`) implements ONLY
frozen H3 §2, literally, plus these interface assumptions (the prereg
under-specifies them; they are frozen here so "expected behavior" is
well-defined):

- **A1 (framing channel):** lines beginning `FRAMING:` and the `TITLE:` line
  are not checkable sentences. This stands in for RT-A's
  "BREAKING"/"scientists reveal" framing — any detector must have *some*
  framing handling; the marker makes it explicit and auditable.
- **A2 (checkable):** every other sentence (split on `[.!?]` followed by
  whitespace) is checkable. Corpora are authored so all non-framing
  sentences are clean declaratives.
- **A3 (K):** installed knowledge = `norm`-closure of all sentences and all
  non-empty lines of G1–G6 (generous to KNOWN; favors the detector).
- **A4 (norm):** lowercase + Unicode-whitespace-collapse
  (`" ".join(s.split())`); zero-width/format characters NOT stripped
  (letter of the frozen spec).
- **A5 (corroboration):** within-corpus, distinct pages, `norm`
  byte-identity, ≥2 pages → install; 1 page → WITHHELD/`SINGLE_SOURCE`.
- **A6 (injection):** G6 word list, case-insensitive substring on the normed
  sentence; flagged page excluded from counting, `FLAG|INJECTION` emitted.
  Self-check SC6 verifies no F/H/L corpus triggers it.
- **A7 (verdict/report):** tri-state + INFRA-FAIL per §2; frozen
  `REPORT|<cid>|<verdict>|known=<n>|novel_installed=<k>|novel_withheld=<w>`
  line format.

## §6 Scoring and commits

Self-checks SC1–SC7 (manifest) run before scoring; any failure voids the run.
Two full oracle passes, byte-identical (`cmp`). Score = oracle verdict vs §3
table. Evidence (corpora, manifest, oracle, logs, reports, this prereg)
committed under `knowledge/web_guides/live_ingest/h3_novelty/redteam/` via
`~/workspace/commit_racefree.py`. No RNG anywhere; all content hand-authored.
