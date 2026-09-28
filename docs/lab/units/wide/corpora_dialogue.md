EXPLORATORY — NOT EVIDENCE

# Extra Corpora: Dialogue — exploratory characterization

**Status:** exploratory working paper for the TNN representation program. Nothing in
this document is program evidence, changes no frozen bar, metric, or kill criterion,
and proposes no rule change. The scored corpora remain Shakespeare + `sqlite3.c`
(fetched on demand, never committed). Dialogue corpora below are fetched on demand
into `/tmp/dialogue_corpora` and never committed; only fetch scripts and the
characterization tool live in the repo.

**Prereg state:** per program record the prereg was signed/frozen by Micah on
2026-09-21; that signed state is authoritative here. (The local
`PREREG_FREEZE.md` header still reads "PROPOSED — NOT FROZEN"; see
AMENDMENT PROPOSAL A for the non-substantive metadata reconciliation. No rule,
metric, or kill-criterion change is proposed or made.)

**Tool:** `units/wide/dturn.zag` — a pure-Zag, deterministic dialogue-structure
analyzer (Linux syscalls only; zero randomness in any decision path). It strips
Project Gutenberg `*** START OF` / `*** END OF` boilerplate, is CRLF-aware
(trailing `\r` stripped for classification; spans measured in raw bytes), counts
bytes/lines/question marks, applies per-convention byte-pattern classifiers, and
accumulates log2 turn-length histograms. Compiled with
`znc_linux_x86_64_abed8aa1 --no-zagd --no-analyze --no-foreground-cache` to
`/tmp` only; no binary, `.zagd`, or `.zag-cache` in the repo. Two consecutive
runs per corpus produced byte-identical output (SHA-256 hashes in §7).

## 1. Corpus list, provenance, and public-domain justification

All five are long-form English texts with multi-speaker or multi-document
discourse structure. Public-domain basis is stated per corpus as: explicit
Project Gutenberg "public domain in the USA" labeling **plus** author/translator
life+70 support. No universal worldwide PD claim is made.

| # | Corpus | Source | Raw bytes (SHA-256) |
|---|--------|--------|---------------------|
| 1 | Oscar Wilde, *The Importance of Being Earnest* (play, 1895) | Project Gutenberg #844 — https://www.gutenberg.org/ebooks/844 | 141,840 — `1b8a58099bb1cdef6a845277a4bacf2f4a268702c165bde30124d4b5105d1851` |
| 2 | Henrik Ibsen, *A Doll's House*, translated by R. Farquharson Sharp | Project Gutenberg #2542 — https://www.gutenberg.org/ebooks/2542 | 169,080 — `d72a481b08ca7ace73e8ca2087b2baec29fc00e0d6e493f5e877b12116bccf4f` |
| 3 | Plato, *The Republic*, translated by Benjamin Jowett | Project Gutenberg #150 — https://www.gutenberg.org/ebooks/150 | 715,543 — `2dda8b90ed8f071e955018e115ef2e4cbceb94ca42ba1a47ec63c09cdb07b2d5` |
| 4 | Bram Stoker, *Dracula* (novel, 1897) | Project Gutenberg #345 — https://www.gutenberg.org/ebooks/345 | 890,348 — `96cd16eacdbfebae8fdda5591f66e0cc8ee76be18e0cd1aca02bc00615782d28` |
| 5 | Eckermann, *Conversations of Goethe with Eckermann and Soret*, translated by John Oxenford (scan of the 1875 Bohn's Standard Library edition) | Internet Archive `conversationsgo01oxengoog` — https://archive.org/download/conversationsgo01oxengoog/conversationsgo01oxengoog_djvu.txt | 743,179 — `e4eba4865b310848b586f23ad0892522709aef4147da5dab53ae3c9857df2bb4` |

**PD justification per corpus:**

1. **Wilde (1854–1900), original English, first performed/published 1895.** PG #844
   explicitly labels the text public domain in the USA. Author's life+70 term
   expired at end of 1970.
2. **Ibsen play; English translation by R. Farquharson Sharp (1864–1945).** PG #2542
   explicitly labels the text public domain in the USA. The translator is the
   relevant rightsholder for the English text; Sharp's life+70 term expired at end
   of 2015.
3. **Plato; English translation by Benjamin Jowett (1817–1893), 19th-century
   edition.** PG #150 explicitly labels the text public domain in the USA.
   Jowett's life+70 term expired at end of 1963.
4. **Stoker (1847–1912), original English, published 1897.** PG #345 explicitly
   labels the text public domain in the USA. Author's life+70 term expired at end
   of 1982.
5. **Eckermann/Soret; English translation by John Oxenford (1812–1877), first
   issued 1850; scanned edition issued 1875.** Pre-1931 publication → public
   domain in the USA. Oxenford's life+70 term expired at end of 1947. (The IA
   `_djvu.txt` is raw OCR of the 1875 printing, including its Google-scan header;
   the earlier manual `<pre>`-block extraction, 743,593 bytes, is superseded by
   this canonical `/download/` artifact — 743,179 bytes. All Eckermann numbers in
   this document are from the canonical file. Fetch-script note: the IA `/stream/`
   URL serves an HTML viewer page, not raw text; `fetch_dialogue_corpora.sh` now
   uses the `/download/` URL.)

## 2. Byte-level facts that shape every classifier

- **Line endings:** all four Project Gutenberg texts are **CRLF** (`\r\n`); the IA
  Eckermann OCR is **LF**. A chunker working on raw bytes sees the drama speaker
  label as `NAME.\r\n`, not `NAME.\n` — the `\r` is part of the byte pattern and
  classifiers must strip or tolerate it (found the hard way: the first analyzer
  build found 0 labels before CRLF handling).
- **Boilerplate:** PG header/footer stripped at `*** START OF` / `*** END OF`
  markers; "content bytes" below are post-strip. The Dracula license small print
  sits *after* the END marker and is excluded.
- **Quotes:** Dracula #345 uses Unicode curly quotes (U+201C, 1,390 open quotes)
  and **zero** ASCII `"` characters; Eckermann uses ASCII `"` (2,230). A
  quote-density feature tuned on ASCII quotes silently reads zero on Dracula.

## 3. Per-corpus characterization (all numbers from `dturn.zag`, 2026-09-21)

Conventions: `q/10kB` = question marks per 10,000 content bytes; `q/1k turns` =
question marks per 1,000 turns. Turn = byte span between consecutive structural
markers of that corpus's convention (see patterns).

### 3.1 Wilde — *The Importance of Being Earnest* (drama; explicit line labels)

- Content: **121,885 B**, 3,891 lines.
- **Speaker-change marker byte pattern:** `^[A-Z][A-Z .'\-]{1,39}\.$` — a whole
  line, 3–40 bytes, starting with a capital letter at line start (anchored;
  see §6), all-caps plus space/dot/apostrophe/hyphen, ending with a period.
  Examples: `ALGERNON.`, `LANE.`, `LADY BRACKNELL.`. **877 labels.**
- Scaffolding: 11 all-caps headers without trailing period
  (`FIRST ACT`, `SCENE`, `ACT DROP`, `TABLEAU`, …).
- Turns: **877**, mean **137 B**, min **15 B** (`JACK.\r\n149.\r\n\r\n`), max
  **997 B**.
- Questions: 270 total; **22 q/10kB**; **307 q/1k turns**.
- Turn-length histogram (log2 bins, bytes): 8–15: 2 · 16–31: 54 · 32–63: 221 ·
  64–127: 280 · 128–255: 205 · 256–511: 91 · 512–1023: 24. Peak bin 64–127 B:
  the utterance turn is a ~100-byte object.
- Notes: stage directions (`[…]`, often on their own lines) occur *inside* turns;
  a few empty/micro turns exist (shortest real turn: a one-word exclamation).

### 3.2 Ibsen — *A Doll's House* (drama; explicit line labels)

- Content: **149,246 B**, 5,177 lines.
- Same label byte pattern as Wilde. **1,292 labels.**
- Scaffolding: 7 caps headers (`ACT I/II/III`, indented ` ACT I.` variants,
  ` DRAMATIS PERSONAE`).
- Turns: **1,292**, mean **114 B**, min **14 B**, max **1,481 B**.
- Questions: 570 total; **38 q/10kB** (highest of the five); **441 q/1k turns**.
- Histogram: 8–15: 7 · 16–31: 140 · 32–63: 414 · 64–127: 402 · 128–255: 221 ·
  256–511: 75 · 512–1023: 31 · 1024–2047: 2. Peak bin 32–63 B — Ibsen's turns run
  shorter than Wilde's on average.

### 3.3 Plato — *The Republic*, Jowett (dialogue with NO line labels)

- Content: **695,814 B**, 16,574 lines — the largest body.
- **There are no line-anchored speaker labels in the dialogue body.** Turn changes
  are encoded lexically, mid-sentence, in reporting clauses. Needle census
  (case-sensitive substring counts over the body):
  - `I said` **385** · `he said` **510** · `I replied` **74** · `he replied`
    **174** · `said Glaucon` **14** · `said Adeimantus` **10** ·
    `said Polemarchus` **4** · `said Thrasymachus` **1** · `he rejoined` **1** ·
    `she said` **0** · `I rejoined` **0**
  - Core four (`I/he said`, `I/he replied`) sum to **1,143** turn-change cues;
    with the named-speaker variants the total is ~1,172.
  - `BOOK ` section markers: **12** (10 books + front matter occurrences).
- Questions: 1,624 total; **23 q/10kB** — nearly identical density to Wilde
  despite utterly different encoding.
- No turn spans are reported for Plato: a paragraph-boundary proxy was considered
  and **rejected as ground truth** — paragraphing in Jowett does not align with
  speaker changes, and presenting proxy spans as turns would launder the
  analyzer's assumption into the data. The needle census is the honest
  characterization; turn discovery on Plato is left to the probes in §8.

### 3.4 Stoker — *Dracula* (nested epistolary: documents, not utterances)

- Content: **870,589 B**, 15,475 lines.
- Structural markers (three byte patterns):
  - Chapters: `^CHAPTER [IVX]+\.$` (body) — **54** raw hits = **27** body chapters
    + **27** from the front-matter CONTENTS listing (see §6 artifact note).
  - Document headers: `^[A-Z][A-Z ',.\-"]{3,63}$` (caps, no trailing period) —
    **31**, e.g. `JONATHAN HARKER'S JOURNAL`, `Letter, Lucy Westenra to Mina Murray`.
  - Date lines: `^_[0-9]{1,2} [A-Z][a-z]+` / `^[A-Z][a-z]+ [0-9]` / `^_[A-Z][a-z]+`
    — **123**, e.g. `_3 May. Bistritz._--`.
- Turns (document sections between chapter/doc/date markers): **208**, mean
  **4,185 B**, min **17 B**, max **33,223 B** — ~30× the drama utterance scale.
- Questions: 492 total; **5 q/10kB**; **2,365 q/1k turns** (documents are long, so
  per-turn question counts are high while per-byte density is low).
- Histogram: 16–31: 12 · 32–63: 44 · 64–127: 6 · 128–255: 3 · 256–511: 16 ·
  512–1023: 16 · 1024–2047: 18 · 2048–4095: 30 · 4096–8191: 21 ·
  8192–16383: 32 · 16384–32767: 9 · 32768–65535: 1. Bimodal: front-matter
  artifacts at the small end, real letters/journals at 2–32 kB.
- Dialogue *inside* documents: 1,390 curly open-quotes; `he said` 191, `said I` 8
  — quoted speech exists but is a second-order phenomenon inside the document
  structure.

### 3.5 Eckermann — *Conversations of Goethe* (dated encounter sessions)

- Content: **743,179 B**, 19,853 lines (LF).
- Entry markers (two patterns, different precision):
  - Strict: `^\(Sup` — **62** supplement entries, e.g.
    `(Sup.*) Saturday, September 21, 1822.` (OCR noise in dates: `1S22`, `iSxi`).
  - Weekday-date lines: `^(Monday|…|Sunday),` — **68** (a few body-text false
    positives, e.g. `Sunday, and then go by the post.`).
  - Loose month-name lines: **110** — noisy; matches body text like
    `Goethe was born in August 1749`. Reported for completeness, not trusted.
- Sessions (sup + loose markers): **172**, mean **4,299 B**, min **34 B**, max
  **24,842 B**.
- **These are conversation *sessions* (a day's visit), not utterance turns.**
  Within a session, speech is quoted/reported: `said Goethe` **238**,
  `said he` **153**, `said I` **118**, `I said` **19**, `he said` **35**,
  ASCII `"` **2,230**.
- Questions: 201 total; **2 q/10kB** (lowest — narrative reportage dominates);
  **1,168 q/1k sessions**.

## 4. Summary table

| Corpus | Body B | Marker pattern | Markers | Units | Mean B | Min–max B | q/10kB |
|--------|-------:|---------------|--------:|------:|-------:|----------:|-------:|
| Wilde (drama) | 121,885 | `^[A-Z][A-Z .'\-]{1,39}\.$` | 877 labels | 877 turns | 137 | 15–997 | 22 |
| Ibsen (drama) | 149,246 | same | 1,292 labels | 1,292 turns | 114 | 14–1,481 | 38 |
| Plato (Jowett) | 695,814 | reporting clauses (`he said`…) | ~1,172 cues | — (no line labels) | — | — | 23 |
| Dracula (epistolary) | 870,589 | chapters / doc headers / date lines | 54 / 31 / 123 | 208 documents | 4,185 | 17–33,223 | 5 |
| Eckermann (sessions) | 743,179 | `(Sup…)` / weekday dates | 62 / 68 | 172 sessions | 4,299 | 34–24,842 | 2 |

## 5. Most interesting structural finding

**The same semantic phenomenon — a speaker/turn transition — is encoded by four
mutually unintelligible byte regimes, at two wildly different scales.**

Drama exposes turns as a low-entropy repeated delimiter: a whole line matching
`^[A-Z][A-Z .'\-]{1,39}\.$` under CRLF, producing ~100-byte utterance turns.
Plato encodes the identical phenomenon with *no* line structure at all — turns
hide mid-sentence in reporting clauses (`he said` ×510, `I said` ×385), and the
honest byte-level description is a substring census, not a segmentation.
Dracula and Eckermann operate one level up: their natural units are 4 kB
*documents* (letters, journal entries) and dated *encounter sessions*,
respectively — 30× the drama scale — with utterance-level dialogue nested inside
as quoted speech (curly quotes in Dracula, `said Goethe` ×238 in Eckermann).

The consequence for Arm D is sharp: a self-chunker that cuts before all-caps
labels has learned **typography, not dialogue**. It will score perfectly on
Wilde/Ibsen, find nothing in Plato (no labels exist), and cut Dracula at the
wrong granularity (documents vs utterances). Any claim about "discovering
conversational structure" must survive all four regimes — and the question-mark
density table shows why surface statistics don't transfer either (38/10kB in
Ibsen vs 2/10kB in Eckermann for the same underlying phenomenon: people talking).

## 6. Analyzer notes and classifier-precision caveats

- **CRLF handling:** first build found 0 labels on Wilde; Gutenberg texts are
  CRLF and the label's last content byte is `.` only after stripping `\r`. Spans
  are measured in raw bytes including `\r\n`.
- **Anchor fix (2026-09-21):** the initial speaker-label classifier did not
  require the line to *begin* with a capital letter, so Ibsen's indented act
  headers (` ACT I.`, ` ACT II.`) counted as speaker labels — 3 false positives
  producing spurious 9- and 10-byte "turns" (turns 1295→1292, min 9→14 B after
  the fix; Wilde unaffected at 877). Lesson recorded: unanchored classifiers
  conflate scaffolding with content.
- **Dracula front-matter artifact:** the 54 chapter hits are 27 CONTENTS-listing
  lines + 27 body chapters; the contents lines generate the spurious 16–63 B
  "turns" in the histogram. Any probe must use body-only spans (post-CONTENTS).
- **Eckermann loose matcher:** month-name matching overcounts narrative body
  text; the clean entry census is the 62 anchored `(Sup` entries plus the 68
  weekday-date lines (~130 dated sessions, a handful of body-text false
  positives among the weekday lines).
- **Plato honesty constraint:** no paragraph proxy is reported as turns.
  Paragraphing ≠ speaker changes in Jowett; the needle census stands alone.
- **No mid-turn cut judgments here:** this document characterizes markers only.
  Whether Arm D cuts *at* labels vs *mid-turn* is probe territory (§8), and
  mid-turn cuts are not prejudged as failures (see Probe 1).

## 7. Determinism record

`dturn.zag` run twice per corpus on 2026-09-21; outputs byte-identical
(SHA-256 of full stdout):

- wilde_earnest: `cf383d06a91707f468aece1344417ec34c5812d384330e139b4379da3a959d74`
- ibsen_dollhouse: `05f65ed0109ddde97570794a976b1e047990889e208fc0b2026709effb2e0b5d`
- plato_republic: `011d452b3bed4887f45c857feb02ba9ab69f3030d6d9769ba60b5b1a67168c48`
- stoker_dracula: `a6680f155ad64b3ec130efaa0f9a1c40a7a4bf2aff13f1381e5f2693b852c2d7`
- eckermann_goethe: `1c56246cbc6851efb69d5f63b92ac193a79d783b53bcd8adefbeffe5939baace`

Pure Zag, no randomness in any decision path, per program law.

## 8. Informational probe designs for Arm D (self-chunking)

Both probes are **informational only**: they may not create scored bars, move
kill criteria, or become evidence. Pure-Zag executables; deterministic given
state; run against withheld boundary labels. "Cuts at labels" means the proposed
span boundary falls within ±k bytes of a true label line (k small, e.g. one line).

### Probe 1 — Boundary discovery / label ablation (does self-chunking find turns
without being told what a turn is?)

Take Wilde/Ibsen, where true turn boundaries (speaker-label line offsets) are
known and **withheld** from the system. Run Arm D self-chunking on three
deterministic variants of the same text: (a) intact; (b) label-deleted (label
lines removed, speech lines spliced, everything else byte-identical); (c)
syntax-preserving control (labels replaced by same-length non-label caps strings
or deterministically permuted, so line rhythm survives but speaker identity is
destroyed). Score informationally: fraction of proposed cuts within ±k bytes of
true boundaries; false-cut rate mid-turn.

- If cuts land on labels in (a) but vanish in (b)/(c): the chunker found explicit
  turn *syntax* — typography, not dialogue semantics.
- If cuts still land on true turn changes in (b) (labels gone): stronger evidence
  of genuine discourse-boundary discovery — the chunker is using what is *said*,
  not the label.
- **Mid-turn cuts are not automatic failures.** A mid-turn cut may be a useful
  phrase-level chunk. Judge cuts by downstream utility instead: question→answer
  retrieval (does a question in one chunk retrieve its answer chunk?) against
  matched-length random-span controls.

### Probe 2 — Cross-convention causal transfer (did it learn dialogue, or
typography?)

Fit/calibrate the chunker on drama labels (Wilde), then — with no retraining —
measure cut placement on Plato (reporting-clause boundaries: `he said` / `I
replied` / `said Glaucon` offsets) and Dracula (document/date-header offsets),
each against matched-length random-span controls. Then ablate deterministically:
delete or permute the reporting clauses / headers and re-measure.

- If cuts track true discourse boundaries across all three conventions, the
  chunker discovered something convention-general about conversational structure.
- If cuts fire only on caps labels (die on Plato, wrong granularity on Dracula),
  it learned typography — the finding of §5, confirmed causally.
- Negative control: Eckermann encounter sessions (4 kB units). If the chunker
  cuts at a fixed byte cadence regardless of convention, session boundaries will
  expose it.

## AMENDMENT PROPOSAL A — STATUS-METADATA RECONCILIATION (non-substantive)

The local `units/PREREG_FREEZE.md` header still reads "PROPOSED — NOT FROZEN,"
while the program record per Micah is that the prereg was **signed and frozen on
2026-09-21**. This proposal asks only that the header line be updated to reflect
the signed/frozen state. It changes no rule, schedule, test, metric, or kill
criterion, and proposes no new scored anything. Pure metadata hygiene.

## AMENDMENT PROPOSAL B — HYPOTHETICAL FUTURE PROMOTION (not made)

This proposal is **not made**; it is sketched so the bar for making it is
explicit. If the program ever wanted dialogue corpora (or metrics derived from
them, e.g. label-ablation discovery scores) to become *scored evidence*, that
would require a separate dated amendment with Micah's explicit re-approval,
specifying: which corpora, which metrics, which bars, and which kill criteria —
under the same freeze discipline as the current prereg. This document's probes
are designed to stay informational so that no such amendment is needed.

## 9. Reproducibility

- Fetch: `units/wide/fetch_dialogue_corpora.sh` (writes `/tmp/dialogue_corpora`,
  prints a `MANIFEST.tsv` of name/URL/bytes/SHA-256). Corpora are never
  committed.
- Analyze: `units/wide/dturn.zag`, compiled to `/tmp` with the lab flags above.
- Frozen scored corpora (Shakespeare, `sqlite3.c`) are untouched by this work.
- Drive is read-only for this task; no binaries, `.zagd`, or `.zag-cache` were
  written to the repo.

---
*Exploratory working paper. Not evidence. No bar moved.*
