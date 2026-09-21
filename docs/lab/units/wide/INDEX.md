# WIDE EXPLORATION TRACK — INDEX AND VERDICT SHEET

**EXPLORATORY — NOT EVIDENCE.** Every document under this directory is
non-binding exploratory material. Nothing here is program evidence,
changes no frozen bar/metric/kill criterion, and can feed only
Micah-signed amendment proposals.

Track complete 2026-09-21. 11 workers, 11 deliverables, 11 commits on
`tnn-native-lab`. The frozen R0/Track-A/Track-B execution runs in
parallel and was not touched.

## Deliverables (commit : file : thread)

| # | Commit | File | Thread |
|---|---|---|---|
| 1 | a7a479f7b23b | beyond_alphabet.md | Beyond-the-alphabet unit designs |
| 2 | 278d44b899bb | cache_dedup.md | Cache dedup / content addressing |
| 3 | cc481bf1c831 | pattern_mining.md | Pattern mining (AP-1..AP-3) |
| 4 | 12ff9f2eaa21 | adversarial_tape.md | Teaching-tape attacks (P1–P8) |
| 5 | a04ce13ef4c9 | cache_invalidation.md | Cache invalidation / ID stability (P-1..P-5) |
| 6 | 0be991d003ed | adversarial_boundaries.md | Boundary-case storms (P1–P7) |
| 7 | e811cea260f4 | corpora_techdocs.md | Technical-document corpora |
| 8 | 917d22e574ac | corpora_prose.md + fetch_corpora_prose.sh + char_prose.zag | Prose corpora (AP-1..AP-4) |
| 9 | 5e68b184e149 | r23_ancestry.md | R23 ancestry (proposals A–D) |
| 10 | 3adeaa0ce1ff | corpora_dialogue.md + fetch_dialogue_corpora.sh | Dialogue corpora (proposals A–B) |
| 11 | 65a1eef398ed | corpora_code.md + fetch_code_corpora.sh + charz.zag | Non-C code corpora |

## Five threads, distilled

**Extra corpora (7/8/10/11).** All PD-verified per-source with written
justifications; fetch scripts SHA-256-pinned, on-demand; corpora never
committed. Sharpest findings: tech docs are the only modality with
labeled definition structure (enumerable ground truth for
term=definition spans; man-page option lists are adversarial vocabulary
inputs); prose repetition spans ~4× (Leviathan 253‰ vs Darwin 67‰) and
carries well-formed UTF-8 multibyte load; dialogue shows four mutually
unintelligible byte regimes for turn boundaries (caps-label typography
vs mid-sentence reporting clauses vs 4kB document chunks); code shows
punctuation rank-order distinguishes languages while top-8 bytes are
identical, nesting depth spans 19×, comment density is project culture.
Informational probes: P-DEF-1, P-JARG-2, P1–P5 (prose), label-ablation
+ cross-convention transfer (dialogue), frozen-C zero-shot transfer +
component ablation (code).

**Adversarial findings (4/6).** Teaching-tape: REVISE laundering is the
most dangerous attack (current tripwire cannot see it; detector D8
proposed). Boundaries: POISONED WELL is the nastiest probe — 1.28MB junk
lets attacker spans permanently occupy D's candidate table while real
text starves; D learns the wrong thing with full deliberative
confidence. Arm most expected to break: **D (flagship)** — its signal
trusts input statistics absolutely, with deliberation over the
statistics but none about them; failure mode is silent wrong knowledge.
Counterweight: D is the most instrumented arm, which is why the probes
are writable as falsifiable predictions.

**R23 lessons (9).** "No English dictionary installed into child" (R23's
verbatim boundary) is the direct ancestor of the installed-vs-learned
ruling — nothing contradicts it. R23's diagnostic master is the ancestor
spec for arm 3's underspecified "natural teaching." R23 used yes/no-only
teaching as the negative control and sibling teaching with
provenance-tagged evidence weights plus a misinformation trap —
supports arm 5, leaves a flaw-manifest gap. ghost#1 UNRECOVERED-VIA-THIS-PATH
(Docs connector not connected); no R23 run verdicts recovered.

**Cache-layer implications (2/5).** Leading exploratory design remains
K3: immutable content payload + stable reference handle. Dedup hit =
OP_DEDUP_HIT + refcount increment, never automatic strengthening
(open question: how repetition informs deliberate strength judgment
without becoming formulaic). Ghost reclamation: episodic mark-sweep,
tombstoned IDs never reminted, any live dangling/drifted ghost halts
loudly. "100 edits / ≥80% ID stability" is not scheme-neutral — the
frozen bars stand individually but their compositional interpretation
may need a dated ruling.

**Cross-thread patterns.** (a) Deliberation *over* statistics but not
*about* them is the recurring exploit surface (D's statistics trust,
REVISE laundering's invisible revisions, poisoned table occupancy).
(b) Byte-level identity has hidden taxes: UTF-8 multibyte (prose),
codepoint-vs-byte framing (D's MIN_LEN=3 bytes), domain-boundary
transitions (XDOM naturalistic poisoning). (c) Register/scale variance
is a standing confound: every frozen control priced on Shakespeare must
be re-priced per register (pattern-mining AP-1, prose P1). (d) Typography
is not language: caps labels, flag lists, and comment fences can all be
learned as content by arms that mistake surface for structure.

## Ranked amendment proposals (non-binding, all need Micah's sign-off)

1. **R23-A / dialogue-A (metadata, uncontroversial):** dated header-only
   amendment to PREREG_FREEZE.md recording the frozen signature
   b0b9140c0eda against the stale "PROPOSED — NOT FROZEN" header. Same
   flag also noted by prose AP-4.
2. **R23-B:** teacher-dependence-decay instrument (additive; no bar changed).
3. **Mining AP-1:** difficulty-binned dual-vs-raw analysis.
4. **Tape D8:** revise-laundering detector (measure (ADOPT+REVISE)/decided
   + installed-span coverage + confidence≥254).
5. **Boundaries P4/P6:** giant-span caps for F-S/F-B/S; rate-normalized
   contdiv test-both leg.
6. **R23-C:** misinformation-trap flaw item (T-3/T-5 only).
7. **R23-D:** arm-3 diagnostic-teacher bounds (§T-7).
8. **Tape P1–P8, boundaries P1–P7, invalidation P-1–P-5, mining AP-2/AP-3,
   prose AP-1–AP-3, dedup predictions:** further non-binding proposals,
   ranked within their documents.

## Notes for the freeze owners

- The stale PREREG header / signature-commit discrepancy (recorded
  b0b9140c0eda) is a dated-amendment item, flagged by three independent
  workers.
- One working interpretation was documented but not amended: fetch =
  data acquisition (shell, since Zag has no TLS), analysis = pure Zag
  (corpora_code.md §3). Becomes an amendment proposal if Micah reads
  the freeze more broadly.
- Minor gap: `dturn.zag` (dialogue characterizer) source was not
  preserved; its validation is documented and it is re-derivable.
- znc toolchain lessons learned during the track: never name a user
  function `zalloc` (builtin collision — use `z_alloc`); `_zag_raw_syscall`
  takes exactly 7 args; paths must be NUL-terminated via a `z_cstr`
  helper. Now in AGENTS.md.
