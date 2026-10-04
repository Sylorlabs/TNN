# EXTRA CORPORA: TECHNICAL DOCUMENTATION — exploratory survey

**EXPLORATORY — NOT EVIDENCE.** Nothing in this document is program evidence.
No bar, metric, or kill criterion is changed, reinterpreted, or softened by
anything here. Frozen corpora remain Shakespeare + sqlite3.c (fetched on
demand, never committed). Any future use of the sources below *as evidence*
requires a dated prereg amendment and Micah's re-approval per RULE-9.

- Track: WIDE EXPLORATION (non-binding), TNN representation program
  ("what is a unit of knowledge, if not an LLM token?").
- Frozen prereg: `~/workspace/tnn-lab/units/PREREG_FREEZE.md` (PROPOSED at time
  of writing; RULE-1..RULE-9, metrics M1–M9 canonical, A-6 corpus striping).
- Author: wide-exploration worker, 2026-09-20. No corpora fetched in bulk; only
  small samples read via page fetches for structural analysis. Fetch *scripts*
  only below — corpora are fetched on demand and NEVER committed.
- Constraints honored: pure Zag for any probe executable; ZERO randomness in AI
  decision paths (RULE-3); no binaries / `.zagd` / `.zag-cache`; Drive untouched
  (read-only, not needed here).

## 1. Source verdicts (provenance + license/PD justification in writing)

### S1. IETF RFCs — VERDICT: ACCEPT (conditional, see license shape)

**Provenance.** The RFC series, published by the RFC Editor
(`www.rfc-editor.org`); canonical plain-text form `.../rfc/rfcNNNN.txt`
(fixed-width 72-col ASCII). Sample analyzed: RFC 2119
("Key words for use in RFCs to Indicate Requirement Levels", BCP 14,
March 1997), fetched 2026-09-20 as `http://www.rfc-editor.org/rfc/rfc2119.txt`.

**License / usage terms — quoted from the IETF Trust, "Legal Provisions
Relating to IETF Documents" (effective 2009-12-28), §3 "Licenses to IETF
Documents and IETF Contributions":**

> "c. Licenses For Use Outside the IETF Standards Process. ... the IETF Trust
> hereby grants to each person who wishes to exercise such rights, to the
> greatest extent that it is permitted to do so, a nonexclusive, royalty-free,
> worldwide right and license under all copyrights and rights of authors:
> i. to copy, publish, display and distribute IETF Contributions and IETF
> Documents **in full and without modification**,
> ii. to translate IETF Contributions and IETF Documents into languages other
> than English, and to copy, publish, display and distribute such translated
> IETF Contributions and IETF Documents in full and without modification,
> iii. to copy, publish, display and distribute **unmodified portions** of IETF
> Contributions and IETF Documents and translations thereof, **provided that:
> (x) each such portion is clearly attributed to IETF and identifies the RFC
> or other IETF Document** or IETF Contribution from which it is taken,
> (y) **all IETF legends, legal notices and indications of authorship contained
> in the original IETF RFC must also be included** where any substantial
> portion of the text of an IETF RFC, and **in any event where more than
> one-fifth of such text, is reproduced in a single document or series of
> related documents**."

Not granted (§3.d): "(i) any license to **modify** IETF Contributions or IETF
Documents, or portions thereof (other than to make translations or to extract,
use and modify **Code Components** as permitted under ... Section 4 ...) in any
context outside the IETF Standards Process, or (ii) any license to publish,
display or distribute ... **without the required legends and notices**."

Code carve-out (§4.c): "Code Components" (text between `<CODE BEGINS>` /
`<CODE ENDS>`, ABNF, MIBs, ASN.1, etc.) are *additionally* licensed under the
**Simplified BSD License** — extractable and modifiable with the BSD conditions.

Two caveats recorded: (a) §2.c — documents published **before the 2009-12-28
effective date** ("Pre-Existing IETF Documents") remain under the policy in
effect at publication (RFCs 1310/1602/2026/3978/4748); most carry "Distribution
of this memo is unlimited" or the older IETF copyright notice — verify per-RFC
boilerplate for pre-2010 RFCs before ingest. (b) There is a current TLP
revision newer than the 2009 text quoted; the grant substance (i–iii, x, y) is
stable across revisions, but the fetch script should record which TLP version
was in force at fetch time.

**License-shape implication for chunking (not an amendment):** a chunker that
slices RFC text into byte spans is reproducing "unmodified portions" under
§3.c(iii) — lawful provided each portion is attributed to IETF + RFC number
(condition x) and legends are kept wherever a substantial portion (>1/5) of one
RFC lands in a single derived document (condition y). Practical recipe: keep
whole RFCs as the stored blob (attribution/legends intact), address chunks as
byte spans *into* the blob (L1-style absolute addressing) rather than as
detached re-formatted copies.

**Size.** RFC 2119: ~8 KB / 156 lines. Full series ≈ 9,500+ RFCs; order of
**~0.5–1 GB** as plain text (estimate — verify against the RFC index at fetch
time). Typical RFC 20–200 KB; outliers to ~1 MB. Whole-series ingest exceeds the
2^25-byte znc slice wall → stripe per A-6 convention (build note, not prereg
change).

**Structural notes (byte patterns, from RFC 2119 sample).**
- Numbered section headings: `1. MUST`, `6. Guidance in the use of these
  Imperatives`, `7. Security Considerations`, `9. Author's Address`.
- Fixed boilerplate vocabulary repeated identically across all ~9.5k RFCs:
  `Status of this Memo`, `Abstract`, `Table of Contents`, `Security
  Considerations`, `Acknowledgments`, `Normative References` /
  `Informative References`, `Author's Address`, `Full Copyright Statement`.
- Front matter block: `Network Working Group`, `Request for Comments: NNNN`,
  `BCP: NN`, `Category: ...`, `Obsoletes:` / `Updates:` lines.
- **Definition frame (the densest in any source surveyed):**
  `1. MUST   This word, or the terms "REQUIRED" or "SHALL", mean that the
  definition is an absolute requirement of the specification.` — i.e.
  `N. TERM [or alternates], mean that <definition>.`
- Normative-keyword bursts: ALL-CAPS `MUST`, `MUST NOT`, `SHALL`, `SHOULD`,
  `MAY`, `REQUIRED`, `RECOMMENDED`, `OPTIONAL`, `NOT RECOMMENDED`.
- Cross-references: `as described in RFC 2119`, `[RFC2119]`, `see Section N`,
  `[Page N]` footers; page header/footer pair repeats every ~58 lines
  (`Bradner Best Current Practice [Page 1]` / `RFC 2119 RFC Key Words
  March 1997`) with `\f` form feeds in raw `.txt`.
- Definition verbs observed: `mean that`, `is defined as`, `refers to`,
  `denotes`, `is`.

### S2. NIST technical publications (FIPS + SP series) — VERDICT: ACCEPT

**Provenance.** National Institute of Standards and Technology, U.S. Department
of Commerce. Sample analyzed: FIPS PUB 180-4, *Secure Hash Standard (SHS)*
(August 2015 / March 2012 announcement), fetched 2026-09-20 from govinfo.gov
(`GOVPUB-C13-PURL-gpo28908`), the .gov original. Authoritative series home:
`csrc.nist.gov/publications/`, DOIs `doi.org/10.6028/NIST.FIPS.180-4`.

**Public-domain justification — in writing.** 17 U.S.C. §105: copyright
protection is not available for works of the U.S. federal government. NIST's
own statements:
- NIST software disclaimer (nist.gov): "Pursuant to Title 15 United States Code
  Section 105, **works of NIST are not subject to copyright protection in
  the United States and are considered to be in the public domain**."
  (Quoted verbatim; the operative copyright statute is 17 U.S.C. §105 —
  the disclaimer's "Title 15" appears to be a typo.)
- NVD FAQ (nvd.nist.gov): "**All NIST publications are available in the public
  domain according to Title 17 of the United States Code.** There are no fees,
  licensing restrictions, or even a requirement to register." (Acknowledgment
  appreciated, not required.)
- Standing caveat (same NIST disclaimer): "**With the exception of material
  marked as copyrighted**, information presented in this document is
  considered public information and may be distributed or copied." → per-document
  check required: reject/skip any publication containing third-party
  "marked as copyrighted" material.

**Size.** FIPS 180-4 PDF text layer: 2,620 lines; typical FIPS/SP PDF 50–500 KB.
The SP 800 series alone is several hundred documents (verify count at fetch;
order of ~100–300 MB as PDF — text extraction needed, PDFs are layout-heavy).

**Structural notes (byte patterns, from FIPS 180-4 text layer).**
- Fixed 14-item numbered front matter: `1. Name of Standard:`, `2. Category of
  Standard:`, … `14. Where to Obtain Copies of the Standard:` — a rigid schema
  across FIPS pubs.
- **Explicit definition scaffolding:** `2. DEFINITIONS`, `2.1 GLOSSARY OF TERMS
  AND ACRONYMS`, `2.2 ALGORITHM PARAMETERS, SYMBOLS, AND TERMS`, `3. NOTATION
  AND CONVENTIONS` (`3.1 BIT STRINGS AND INTEGERS`, `3.2 OPERATIONS ON WORDS`).
  This is the only source surveyed with a *labeled* glossary section —
  term-definition pairs are enumerable by construction.
- Dotted-leader Table of Contents:
  `5.1.2  SHA-384, SHA-512, SHA-512/224 and SHA-512/256 . . . . . . . .13`
  (dot runs + page numbers as a byte pattern).
- ALL-CAPS section titles; `Key words: computer security, cryptography, ...`
  metadata line; roman-numeral page markers (`ii`, `iii`, `iv`, `v`).
- Math/symbol bursts in §4 (constants, operators, superscripts) — jargon bursts
  of non-ASCII symbols.
- Cross-references: `This Standard supersedes FIPS 180-3 [FIPS 180-3]`,
  `See Section 5.6.4 of SP 800-57, Part 1`, `doi.org/10.6028/...` lines.

### S3. Unix man pages — VERDICT: REJECT bulk; ACCEPT small curated set only

**Provenance.** Linux man-pages project (kernel.org / man7.org; troff source,
rendered HTML). Samples: `indent(1)`, `round(3)`, `atexit(3)`, `fstatvfs(2)`
(man7.org / kernel.org renderings, fetched 2026-09-20).

**License finding — the reason for rejection.** Licenses vary *per page* and no
project-level blanket grant was verified:
- `indent(1)` carries an in-page permission: "Permission is granted to **make
  and distribute verbatim copies of this manual** provided the copyright notice
  and this permission notice are preserved on all copies." → individually
  usable.
- LTTng project pages (`tracef(3)` etc.) are **LGPL-2.1** ("This macro is part
  of the LTTng-UST project. This macro is distributed under the GNU Lesser
  General Public License, version 2.1").
- Project COLOPHON only asserts membership ("This page is part of the
  man-pages ... project"), not a license. Per the task rule (verify per source,
  reject ambiguous), bulk ingest of the man-pages set is **REJECTED** — a bulk
  tarball would commingle verbatim-permission, LGPL, GPL, and BSD pages.
- Candidates for future per-page verification (not verified, not claimed):
  OpenBSD/FreeBSD base-system man pages; POSIX man pages are NOT free.

**Size (for the record).** Individual pages 5–50 KB; the full man-pages tarball
is on the order of a few MB compressed (unverified figure — irrelevant given
rejection).

**Structural notes (kept, because the *structure* is the finding even though
the bulk corpus is rejected).**
- Fixed section vocabulary in stable order: `NAME`, `SYNOPSIS`, `DESCRIPTION`,
  `OPTIONS`, `RETURN VALUE`, `ERRORS`, `FILES`, `STANDARDS`, `HISTORY`,
  `NOTES`, `BUGS`, `EXAMPLES`, `SEE ALSO`, `COLOPHON` (troff: `.SH` macros —
  machine-detectable markers in source form).
- **Term=definition via flag lists** (densest vocabulary-list structure in the
  survey — `indent(1)` OPTIONS ≈ 120 pairs):
  `-as, --align-with-spaces` / `    If using tabs for indentation, use spaces
  for alignment.` / `    See  INDENTATION.` — i.e. `flag[, flag] \n indent+ gloss
  [\n indent+ See SECTION.]`.
- Enumeration definitions: `• 0 means no errors...`, `• 2 is returned if...`.
- Cross-reference density: **highest of all sources** — every option ends in
  `See <SECTION>.`, `SEE ALSO` lists of `name(section)` pairs, inline
  `see lttng-ust(3)`, plus reverse index ("Pages that refer to this page").
- `COLOPHON` = machine-readable provenance (project, tarball name, fetch date).

### S4. Project Gutenberg science texts — VERDICT: ACCEPT (per-ebook clearance)

**Provenance.** Project Gutenberg (`www.gutenberg.org`); ebooks transcribed from
public-domain print editions. Exemplars verified 2026-09-20:
- **#2009** — Darwin, *On the Origin of Species*, 6th ed. (1872, "considered
  the definitive edition"). Sample opened: `.../files/2009/2009-h/2009-h.htm`.
  ~1.25 MB text (third-party char count 1,249,171 for a Gutenberg-derived file;
  treat as approximate).
- **#5001** — Einstein, *Relativity: The Special and General Theory* (Lawson
  transl., 1920). Catalog page `https://gutenberg.org/ebooks/5001` states
  **"Copyright: Public domain in the USA."** PG lists formats 912/812/629/516
  kB etc. → text on the order of ~0.5–0.9 MB.
- **#21076 — REJECTED pending clearance** — Euclid, *First Six Books of the
  Elements* (Casey). Its production note states "Digital file copyright by
  Cornell University Library 1991" — a possible "posted with permission of the
  copyright holder" case under PG license §1.E.3 (additional terms may apply).
  Do not ingest until cleared.

**Public-domain justification — in writing.** The PG license header (present in
every ebook):
> "Creating the works from public domain print editions means that **no one
> owns a United States copyright in these works**, so the Foundation (and you!)
> **can copy and distribute it in the United States without permission and
> without paying copyright royalties**. ... You may use this eBook for **nearly
> any purpose such as creation of derivative works, reports, performances and
> research**."

Two operative conditions: (a) §1.E.3 — "If an individual Project Gutenberg-tm
electronic work is **posted with permission of the copyright holder**, your use
and distribution must comply with ... any additional terms imposed by the
copyright holder" → **ingest only ebooks with no such notice** (the #21076
rejection is this rule firing). (b) Trademark: "Project Gutenberg" is a
registered trademark; redistribution conditions attach to the *trademark*, not
the text — **strip the PG header/trailer and all "Project Gutenberg"
references** and the underlying PD text "can be reused without any
restrictions." Non-US jurisdictions must check local law (PG's own warning).

**Size.** #2009 ≈ 1.25 MB; #5001 ≈ 0.5–0.9 MB. A Gutenberg science shelf
(dozens of texts) reaches tens of MB — smaller than the RFC/NIST sets, but the
only source with long-form discursive science prose.

**Structural notes (byte patterns, from #2009 sample).**
- Chapter headings in ALL CAPS: `## AN HISTORICAL SKETCH OF THE PROGRESS OF
  OPINION ON THE ORIGIN OF SPECIES, ...`; `## CONTENTS` table with numbered
  chapters (`1. VARIATION UNDER DOMESTICATION.` … `14. RECAPITULATION AND
  CONCLUSION.`).
- Footnote markers `[1]`, `[2]` inline, with footnote paragraphs at section
  ends — a reference/expansion pair structure.
- Epigraph blocks with attribution line: `"..."` / `WHEWELL: *Bridgewater
  Treatise*.` — quote=source pairs.
- License delimiters (exact, strippable):
  `*** START OF THE PROJECT GUTENBERG EBOOK ... ***` /
  `*** END OF THIS PROJECT GUTENBERG EBOOK ... ***`.
- Jargon bursts: Latin binomials in italics, taxonomic lists, measurement runs.
- Edition-selection table at head (`| **1228** | 1859, First Edition |` …) —
  metadata, strip with header.

## 2. Cross-source structural characterization

**Heading-marker repetition (highest → lowest).**
1. RFC boilerplate titles (`Status of this Memo`, `Abstract`, `Security
   Considerations`, `Author's Address`) — identical byte strings across ~9.5k
   documents. A chunker that cannot *discover* these as units has a real
   problem; a chunker that *memorizes* them has a different one (probe P2
   below distinguishes).
2. Man-page `.SH` section vocabulary (14 fixed titles, stable order).
3. FIPS 14-item numbered front matter + `N(.M)* TITLE` section numbers.
4. Gutenberg chapter headings (ALL CAPS, numbered CONTENTS) — least rigid.

**Definition patterns ("X is/means").** Observed frames, by source:
- RFC: `N. TERM [, or "ALT"] mean that <def>` (RFC 2119 §1–5); `X is defined
  as Y`; `X refers to Y`.
- NIST: glossary table rows (`TERM — definition`); `Let X denote Y`;
  `N. Name of Standard: <value>` (metadata definitions).
- Man: `-flag, --long-flag \n <gloss>`; `N means <gloss>`; `N is returned if
  <cond>`.
- Gutenberg: discursive — `X is <def>` embedded in prose; footnote expansions
  `[n] <expansion>`; epigraph attributions.
- **Density ranking:** NIST glossary sections > RFC 2119-style frames >
  man-page flag glosses > Gutenberg prose. Technical docs carry *explicit,
  machine-detectable definition scaffolding* at far higher density than either
  frozen corpus (Shakespeare prose, sqlite3.c code).

**Cross-reference density (highest → lowest).**
1. Man pages — `See <SECTION>.` per option, `SEE ALSO` lists, `name(section)`
   inline refs, reverse "Pages that refer to this page" index.
2. RFCs — `RFC NNNN`, `[RFCNNNN]`, `see Section N`, `Updates:`/`Obsoletes:`.
3. NIST — `FIPS 180-3 [FIPS 180-3]`, `Section 5.6.4 of SP 800-57`, DOIs.
4. Gutenberg — footnotes `[n]`, `("Philosophie Zoologique")` citations.

**Boilerplate / repeated-byte inventory (chunker stressors).** Page
header/footer pairs (RFC `\f` + `... [Page N]`), FIPS roman-numeral page marks,
man-page `COLOPHON` blocks, Gutenberg license header/trailer, RFC front-matter
blocks, dotted-leader TOC lines. All are *deterministic, high-repetition*
sequences — ideal inputs for testing whether CUT arms emit them as stable
units vs. shatter them vs. merge them into neighbors (informational only).

## 3. Most interesting structural finding

Technical documentation is the only modality surveyed where **definitions are
first-class, labeled structure rather than emergent regularity**: NIST
standards ship a literal `GLOSSARY OF TERMS AND ACRONYMS` section; RFC 2119
defines its normative vocabulary in rigid `N. TERM … mean that <def>` frames;
man pages list ~120 `flag → gloss` pairs per page. That makes tech docs the
strongest available test of the program's core question — *does any arm
isolate "term = definition" spans as units without being told what a
definition is?* — because ground truth is enumerable by construction instead
of hand-annotated. Second-order finding: the man-page OPTIONS list is the
densest vocabulary-list in the survey and a natural adversarial input for
taught-vocabulary arms — flags *look like* words but are interface tokens;
an arm that "learns" `-nbad` as a word has learned the wrong thing.

## 4. Informational probe designs (NOT metrics, NOT bars — no frozen names used)

Probe-local names are `P-DEF-*` / `P-JARG-*`. They do not touch M1–M9.

### Probe P-DEF-1 — definition-span isolation

**Question.** Does any CUT arm emit chunks whose boundaries agree with
hand-annotated `term = definition` spans, without being told?

**Ground truth (hand-built, deterministic, frozen at probe time).**
- RFC 2119 §1–5: 6 normative terms + listed alternates (12 spans).
- FIPS 180-4 §2.1 glossary: first 40 entries (80 span endpoints).
- `indent(1)` OPTIONS: 40 flag→gloss pairs (80 span endpoints).
Total ≈ 132 spans; each span = `[term_start, def_end]` byte offsets in the
source blob.

**Procedure (pure Zag, zero RNG).** Ingest each source blob once through the
arm under test (same harness for all 53 arms + the A control, raw-bytes
baseline). Collect emitted chunk `[start, len]` list. Compute:
- `P-DEF-agree` = fraction of ground-truth spans exactly matched by one
  emitted chunk (byte-exact, both endpoints).
- `P-DEF-cover` = fraction of ground-truth spans covered by the *union* of
  emitted chunks with no chunk boundary *inside* the span (boundary-respect).
- Baselines: line-splitter and fixed-64-byte splitter (dumb controls; if an
  arm cannot beat line-split on glossary tables, that is informative).

**Harness determinism.** N=5 reruns per RULE-4 (adversarial perturbations:
heap pre-fragmentation, base-offset shift, free-list reversal); byte-identical
chunk lists required or the *harness run* is discarded, never the arm. No
randomness anywhere; all inputs are fixed byte blobs.

**What it would show.** Whether "term = definition" is a *discoverable* unit
for any arm — the program's thesis test in miniature, on the modality where
definitions are densest. Expected informative contrasts: glossary-table arms
vs. prose arms; taught-vocabulary arms on man-page flags (do they isolate the
flag+gloss as one unit, or the flag alone?).

### Probe P-JARG-2 — jargon-burst handling

**Question.** What do CUT arms do *inside* jargon bursts — shatter, merge, or
respect term boundaries?

**Burst classes (deterministic byte predicates, no ML).**
- B1 normative-keyword bursts: RFC paragraphs where ≥30% of tokens are
  ALL-CAPS normative keywords (`MUST`, `SHOULD`, `MAY`, …).
- B2 flag thickets: man-page OPTIONS runs (consecutive `^-` lines).
- B3 symbol runs: FIPS §4 constant/operator blocks (non-ASCII + digit density
  ≥40%).

**Procedure.** Same ingest as P-DEF-1. Compute per arm, per burst class:
- `P-JARG-size-ratio` = median chunk bytes inside bursts ÷ median chunk bytes
  outside bursts (shatter <1, merge >1, neutral ≈1).
- `P-JARG-respect` = fraction of burst-internal chunk boundaries that fall on
  term boundaries (flag/gloss junction, keyword token edge) vs. mid-token cuts.
  Mid-token cuts inside a burst are counted, not judged — informational.

**What it would show.** Whether dense jargon systematically distorts an arm's
segmentation (a scaling-relevant behavior: jargon density grows in real
technical text), and whether any arm treats bursts as *vocabulary to learn*
vs. *noise to cut through*. The man-page flag thicket is the adversarial case:
an arm that emits each `-flag` as a "word" chunk while dropping the gloss has
found tokens but lost meanings.

### Implementation notes (both probes)

- Pure Zag executables; no RNG in any decision path (RULE-3). Ground-truth
  span files are hand-written byte offsets, committed as probe fixtures —
  *fixtures are probe inputs, not corpora, and not evidence*.
- Probe-local metric names only (`P-DEF-*`, `P-JARG-*`); frozen M1–M9 names
  are never reused.
- Results reported as they resolve per arm (RULE-8 spirit); no section
  champions, no crown (RULE-6 spirit) — these probes are exploratory and bind
  nothing.

Zag sketch (design only — not compiled, not run):
```zag
// P-DEF-1 harness sketch. Reads blob + span fixture, runs one CUT arm,
// compares emitted chunk boundaries to ground-truth spans. Deterministic.
fn pdef_run(arm: Arm, blob: []u8, spans: []Span) -> PdefResult {
    let chunks: []Chunk = arm.cut(blob);      // arm-owned segmentation
    let agree: u64 = 0; let cover: u64 = 0;
    let i: u64 = 0;
    while i < spans.len() {
        let s: Span = spans[i];
        if chunk_exact(chunks, s) { agree = agree + 1; }
        if chunk_respects(chunks, s) { cover = cover + 1; }
        i = i + 1;
    }
    return PdefResult{
        agree_num: agree, cover_num: cover, span_total: spans.len(),
        chunk_count: chunks.len(),
    };
}
// N=5 reruns with adversarial perturbations per RULE-4; the harness
// byte-compares the five PdefResult values and discards the run on mismatch.
```

## 5. Fetch scripts (scripts only — corpora fetched on demand, NEVER committed)

Conventions: fetch into a scratch dir outside the repo (e.g.
`$TNN_CORPORA/techdocs/`, default `/tmp/tnn-corpora-techdocs/`); record the
fetch date + license version in a `PROVENANCE.txt` next to the bytes; verify
SHA-256 and record it; strip to the license-safe form noted per source. Respect
`robots.txt` and rate limits; prefer bulk index files over crawling.

```sh
#!/bin/sh
# fetch_rfcs.sh — IETF RFC plain-text series (CONDITIONAL: see license notes)
# License: IETF Trust Legal Provisions §3.c — reproduce whole RFCs unmodified;
# keep per-RFC attribution + legends (§3.c(iii)(x)(y)); Code Components
# additionally under Simplified BSD (§4). Restrict to post-2009-12-28 RFCs
# unless the pre-2010 boilerplate is verified per RFC (§2.c).
set -eu
OUT="${TNN_CORPORA:-/tmp/tnn-corpora-techdocs}/rfcs"; mkdir -p "$OUT"
# 1. RFC index (verify size estimate ~0.5–1 GB before bulk fetch)
curl -sL --retry 3 https://www.rfc-editor.org/rfc-index.txt -o "$OUT/rfc-index.txt"
# 2. Bulk fetch: use the rfc-editor rsync/tar service if available; else loop
#    the index for ^[0-9]{4} entries and fetch $OUT/rfc/rfcNNNN.txt with
#    --limit-rate 200k and a contact User-Agent. (Loop omitted here — generate
#    from the index at fetch time; do NOT check the bytes into git.)
# 3. Record: date, TLP version in force, sha256sum manifest.
date -u +%FT%TZ > "$OUT/PROVENANCE.txt"
sha256sum "$OUT"/rfc/*.txt > "$OUT/SHA256SUMS" 2>/dev/null || true
```

```sh
#!/bin/sh
# fetch_nist.sh — NIST FIPS + SP PDFs (PUBLIC DOMAIN per 17 USC 105)
# License: PD in the US; skip any doc containing "marked as copyrighted"
# third-party material (NIST's own caveat). Extract text at ingest time
# (pdftotext); keep the original PDFs as the provenance blob.
set -eu
OUT="${TNN_CORPORA:-/tmp/tnn-corpora-techdocs}/nist"; mkdir -p "$OUT/fips"
# Exemplar (verified 2026-09-20):
curl -sL --retry 3 \
  https://www.govinfo.gov/content/pkg/GOVPUB-C13-PURL-gpo28908/pdf/GOVPUB-C13-PURL-gpo28908.pdf \
  -o "$OUT/fips/NIST.FIPS.180-4.pdf"
# Series bulk: enumerate from https://csrc.nist.gov/publications/fips and
# /publications/sp800 at fetch time; prefer .gov originals only.
date -u +%FT%TZ > "$OUT/PROVENANCE.txt"
```

```sh
#!/bin/sh
# fetch_manpages_curated.sh — INDIVIDUALLY-CLEARED man pages ONLY (bulk REJECTED)
# Rule: ingest a page only if its own text grants verbatim copying
# (e.g. indent(1): "Permission is granted to make and distribute verbatim
# copies of this manual provided the copyright notice and this permission
# notice are preserved on all copies."). Keep the permission notice in the blob.
set -eu
OUT="${TNN_CORPORA:-/tmp/tnn-corpora-techdocs}/manpages"; mkdir -p "$OUT"
# indent(1) — permission verified in-page 2026-09-20 (man7.org rendering of the
# man-pages project source). Fetch the TROFF SOURCE (git.kernel.org man-pages
# repo) so .SH/.TP/.B macros are preserved as byte patterns:
#   git -C "$OUT" clone --depth 1 \
#     https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git src
# then copy only cleared pages + record each page's license line in PERPAGE.txt
# DO NOT bulk-copy the tree: licenses vary per page (LGPL/GPL/BSD/verbatim).
echo "curated-only; see PERPAGE.txt" > "$OUT/README.txt"
```

```sh
#!/bin/sh
# fetch_gutenberg.sh — Project Gutenberg science texts (PD in the US)
# License: ingest ONLY ebooks with no "posted with permission of the copyright
# holder" notice (PG license §1.E.3); STRIP the PG header/trailer and all
# "Project Gutenberg" references (trademark) before use.
set -eu
OUT="${TNN_CORPORA:-/tmp/tnn-corpora-techdocs}/gutenberg"; mkdir -p "$OUT"
# Verified exemplars (2026-09-20):
#   #2009  Darwin, On the Origin of Species, 6th ed. (~1.25 MB)
#   #5001  Einstein, Relativity: The Special and General Theory (~0.5–0.9 MB)
#   #21076 Euclid/Casey Elements — REJECTED pending clearance (Cornell digital-
#          file copyright notice in production note).
for n in 2009 5001; do
  curl -sL --retry 3 "https://www.gutenberg.org/cache/epub/$n/pg$n.txt" \
    -o "$OUT/pg$n.txt"
done
# Strip: delete everything before "*** START OF THE PROJECT GUTENBERG EBOOK"
# and after "*** END OF", then delete remaining "Project Gutenberg" lines.
date -u +%FT%TZ > "$OUT/PROVENANCE.txt"
sha256sum "$OUT"/pg*.txt > "$OUT/SHA256SUMS"
```

## 6. Amendment PROPOSAL section

**No frozen-assumption contradictions found.** Checked against PREREG_FREEZE.md:
- Extra corpora do not alter the frozen Shakespeare + sqlite3.c corpora; this
  track is explicitly exploratory/non-binding.
- Probe-local metric names (`P-DEF-*`, `P-JARG-*`) deliberately avoid the
  frozen M1–M9 namespace; probes bind nothing and fire no kill criteria.
- License-shape note (implementation, not amendment): if RFC text is ever used
  in a scored run, chunk attribution must satisfy IETF TLP §3.c(iii)(x)(y) —
  keep whole-RFC blobs with legends intact and address chunks as byte spans
  into them. The A-6 striping convention (≤2^25 slices) is compatible: slicing
  is "unmodified portions" under §3.c(iii), not modification under §3.d(i).
- If any source above is ever promoted from exploratory to evidence, that
  promotion itself is the dated amendment requiring Micah's re-approval
  (RULE-9). This document proposes no such promotion.

## 7. Open questions for the program (not decisions)

1. Should P-DEF-1's ground-truth span fixtures live under `units/wide/` (as
   probe inputs) or under a future `probes/` tree? Left to the coordinator.
2. The man-page bulk rejection is conservative: a per-page license audit of
   the man-pages tree (SPDX-style, from troff source comments) could clear a
   large subset mechanically. Worth it? The OPTIONS-list structure is unique
   enough that a cleared subset may be worth the audit.
3. NIST PDFs need text extraction (layout-heavy); the extraction tool choice
   affects byte patterns (ligatures, hyphenation). Any future NIST ingest must
   pin the extractor + version in PROVENANCE.txt.
4. Non-US jurisdiction: Gutenberg PD status is US-scoped. Program runs in the
   US; noted, no action.
