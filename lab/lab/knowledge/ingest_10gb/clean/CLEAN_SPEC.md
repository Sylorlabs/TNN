# CLEAN_SPEC.md — Frozen cleaning rules, 10GB ingest Phase 1C

**Status:** FROZEN 2026-09-22. Any change requires a new spec version; this file is never edited in place.
**Authority:** Micah's order: "go through it and cut the bloat remove all the dashs spam".
**Scope:** four raw sources — OpenStax textbook text, Stack Exchange XML dumps,
Project Gutenberg plain text, Wikibooks/wiki text.
**Determinism:** ZERO RNG anywhere. Every rule is mechanical (byte patterns / regex /
exact strings). Rules apply in the fixed order R1→R10. Files within a source are
processed in ascending byte order of their relative path (UTF-8 bytes). All output
is UTF-8, no BOM, `\n` line endings.

## §0 Conventions

- "Drop the line" = remove the line and its terminating `\n` (no blank line left behind).
- "Paragraph" = maximal block of non-empty lines separated by exactly one blank line
  (guaranteed by R6).
- Byte examples show exact bytes with `\n` visible; `␣` marks a literal space where
  ambiguity matters.

## R0 — Ordering invariants (not a transform)

1. Per file, rules apply strictly in order R1, R2, …, R10.
2. Per source directory, files are processed in ascending byte order of relative path.
3. No rule uses randomness, wall-clock, file metadata, or network.
4. Output text files are UTF-8 without BOM.

## R1 — Encoding normalization → UTF-8

1. Read the file as raw bytes.
2. If the bytes begin with `EF BB BF`, drop those 3 bytes (UTF-8 BOM).
3. Decode as UTF-8 strict. On `UnicodeDecodeError`, decode the (BOM-stripped) bytes
   as **windows-1252** (total function: every byte maps; deterministic fallback, no guessing).
4. No other encoding is attempted. Already-present U+FFFD is kept as-is.

Before (bytes): `63 61 66 E9` → UTF-8 decode fails → windows-1252 → After: `café`
(`63 61 66 C3 A9` in UTF-8 output).
Before (bytes): `EF BB BF 68 69` → After: `hi`.

## R2 — Line-ending normalization

On the decoded string: replace `\r\n` → `\n`, then any remaining `\r` → `\n`.

Before: `61 0D 0A 62 0D 63 0A` ("a\r\nb\rc\n") → After: `61 0A 62 0A 63 0A` ("a\nb\nc\n").

## R3 — Source-structure extraction (before text rules)

### R3a — Stack Exchange XML (`stackexchange/*.xml`, `<posts><row …/>`)

Stream-parse in document order (`iterparse`, `end` events on `row`).
For each `<row>` keep only: `Id`, `PostTypeId`, `Title` (questions), `Body`.
- `PostTypeId=1` (question): text = `Title` + `"\n\n"` + `Body`. Missing Title → `""`.
- `PostTypeId=2` (answer): text = `Body`.
- All other `PostTypeId` values: skipped. All other attributes/elements: dropped.

`Body` is HTML; clean it mechanically in this order:
1. Drop dupe-banner blocks: split raw HTML on blank lines; drop any block that
   starts with `<blockquote>` and contains the exact bytes `Possible Duplicate:`
   within its first 200 characters.
2. Block boundaries → paragraph breaks: regex
   `(?i)(</p>|</h[1-6]>|</li>|</ul>|</ol>|</div>|</blockquote>|</pre>|<br\s*/?>)`
   → `"\n\n"` (so `</p><p>` block structure survives tag stripping).
3. Strip tags: regex `<[^<>]*>` → `""`. (Runs BEFORE entity unescape, so escaped
   `&lt;code&gt;` in code samples survives as literal text.)
4. `html.unescape` (Python 3.12 stdlib; deterministic entity table).

Before: `<p>Use <b>salt</b> &amp; heat.</p>`
After: `Use salt & heat.`

### R3b — OpenStax XHTML (`openstax/*.xhtml`)

1. Drop `<head>…</head>`: regex `<head\b[^>]*>.*?</head>` (DOTALL) → `""`.
2. Block boundaries → paragraph breaks: same regex as R3a step 2 → `"\n\n"`.
3. Strip remaining tags: `<[^<>]*>` → `""`. 4. `html.unescape`.

### R3c — Wikibooks / wiki XML (`wikibooks/*.xml`, MediaWiki `<page>`)

Stream-parse in document order; per `<page>` take `<title>` + `"\n\n"` + `<revision>/<text>`.
(Namespace prefixes tolerated: match on local name after `}`.) Then wikitext strip,
in this order:
1. Table blocks: from a line starting with `{|` through the next line starting
   with `|}` (inclusive) → dropped.
2. `'''` → `""`, then `''` → `""` (bold/italic markers).
3. Headings: `^(={2,6})\s*(.*?)\s*\1$` → `\2` (keep inner text).
4. Links: `\[\[([^|\]]*\|)?([^\]]*)\]\]` → `\2` (`[[a|b]]`→`b`, `[[a]]`→`a`).
5. Templates: `\{\{[^{}]*\}\}` → `""` (non-nested).
6. Refs: `<ref\b[^>]*>.*?</ref>` (DOTALL) → `""`; `<ref\b[^>]*/>` → `""`.

Before: `== [[Photosynthesis|Photo]] ==\nThe '''light''' reactions<ref>x</ref> make {{chem|ATP}}.`
After: `Photo\nThe light reactions make .`

### R3d — Gutenberg plain text (`gutenberg/*.txt`)

No structural extraction.

## R4 — License boilerplate excision (exact byte patterns)

Applied to the whole file text, before decorative-run removal.

- **Gutenberg**: if a line matches `^\*{3} START OF (THIS|THE) PROJECT GUTENBERG EBOOK`
  → delete from the start of the file through that line inclusive (first match only).
  If a line matches `^\*{3} END OF (THIS|THE) PROJECT GUTENBERG EBOOK`
  → delete from that line through the end of the file inclusive (first match at/after START).
- **OpenStax**: delete any line exactly equal to `Access for free at openstax.org`,
  or matching `^This content is available for free at https://cnx\.org/contents/.*$`.
- **Wikibooks**: delete any line exactly equal to
  `From Wikibooks, open books for an open world`, or matching
  `^Retrieved from "https?://[^"]*"$`.

Before (Gutenberg):
```
The Project Gutenberg eBook of Foo, by Bar\n\nFull license text here.\n\n*** START OF THE PROJECT GUTENBERG EBOOK FOO ***\n\nChapter 1.\n
```
After:
```
Chapter 1.\n
```

## R5 — Decorative runs ("dash spam")

### R5a — Whole-line separators → drop the line

Let `s` = the line with all spaces/tabs removed. If `s` is a single character
repeated, with that character in `{ - _ * = ~ # + }` and length ≥ 3 → drop the line.

Before:
```
Chapter 1\n----------------------------------------\nIt was a bright day.\n* * *\nMore text.\n
```
After:
```
Chapter 1\nIt was a bright day.\nMore text.\n
```
(`* * *` → spaces removed → `***`, length 3 → dropped.)

### R5b — Inline dash/underscore/tilde runs → single space

Any maximal run of ≥ 2 identical characters from `{ - _ ~ }` inside a line
→ replaced with one `␣` (U+0020). `*` and `=` are NOT touched inline
(code operators: `a == b`, `x *= 2` stay intact).

Before: `The well----------known fact__remains.`
After: `The well known fact remains.`

Before: `if (a == b) { x *= 2; }` → After: unchanged.

## R6 — Whitespace normalization

1. Per line: collapse `[ \t]+` → single `␣`; strip leading and trailing
   spaces/tabs (all lines left-flushed).
2. Runs of ≥ 2 consecutive empty lines → exactly 1 empty line.
3. Drop leading and trailing empty lines of the file.

Before: `␣␣hello␣\tworld␣␣\n\n\n\nnext␣␣\n`
After: `hello world\n\nnext\n`

## R7 — Nav / ad line drop (frozen pattern list)

After R6, drop a line if it FULLY matches any pattern (regex, applied to the whole line):

| # | Pattern | Catches, e.g. |
|---|---|---|
| P1 | `^\d+$` | `42` (bare page numbers) |
| P2 | `(?i)^(table of contents\|contents\|index\|glossary)$` | `Table of Contents` |
| P3 | `(?i)^(advertisement\|sponsored content\|click here.*)$` | `Advertisement` |
| P4 | `^[←→].*$\|^.*[←→]$` | `← Previous`, `Next →` (wiki nav crumbs) |
| P5 | `(?i)^page \d+ of \d+$` | `Page 3 of 412` |
| P6 | `^\[?page \d+\]?$` (`(?i)`) | `[Page 12]` |
| P7 | `^<!--.*-->$` | `<!-- footer -->` (HTML comment leftovers) |

Before: `42\nReal sentence here.\nAdvertisement\n` → After: `Real sentence here.\n`

Blank lines opened by R5a/R7 drops are re-collapsed per R6 before R8.

## R8 — Dedupe (byte-identical paragraphs, order-preserving, first wins)

Window: the whole single file. No cross-file dedupe. Unit = paragraph
(R6-separated block). Drop any paragraph byte-identical to an earlier paragraph
in the same file. (Dedupe is paragraph-level only: repeated single lines such as
dialogue "Yes." / "No." are legitimate content and are kept.)

Before:
```
It was the best of times,\nit was the worst of times.\n\nYes.\n\nIt was the best of times,\nit was the worst of times.\n
```
After:
```
It was the best of times,\nit was the worst of times.\n\nYes.\n
```

## R9 — Fact emission (extends 1GB PREREG §2)

1. Split the cleaned file text into paragraphs on blank lines.
2. Drop paragraphs with fewer than 20 non-whitespace characters.
3. **R9.2a — kind 6 (Stack Exchange) exception:** the emission unit is the whole
   post text (question: `Title\n\nBody`; answer: `Body`). Paragraph splitting
   does not apply within a post; the 20-char floor applies to the whole unit.
   (Rationale: keeps the question title bound to its body as one fact.)
3. Paragraph longer than 4096 bytes: split at the last sentence terminator
   (`.`, `!`, `?` followed by space or end-of-paragraph) at or before byte 4096;
   if none exists, cut at byte 4096 rounded down to a UTF-8 character boundary.
   Repeat until all chunks ≤ 4096. Chunks of a split paragraph get key suffix
   `~{m}` (`m` = 0-based chunk index); unsplit paragraphs get no suffix.
4. Record layout is byte-identical to 1GB §2:
   `[1B kind][2B key_len BE][4B text_len BE][key bytes][text bytes]`.
5. New kinds (1GB kinds 1–4 untouched):

| kind | source | key format | text |
|---|---|---|---|
| 5 | OpenStax textbook passage | `ostx:{book}:{sec}:{n}` | cleaned paragraph |
| 6 | Stack Exchange post | `se:{site}:q:{postid}` / `se:{site}:a:{postid}` | question: `Title\n\nBody`; answer: `Body` |
| 7 | Gutenberg book paragraph | `gb:{gid}:{n}` | cleaned paragraph |
| 8 | Wikibooks paragraph | `wb:{slug}:{n}` | cleaned paragraph |

`{book}`/`{sec}` = OpenStax filename stem (per-chapter files: sec = stem);
`{site}` = Stack Exchange filename stem; `{postid}` = row Id;
`{gid}` = leading digits of the Gutenberg filename stem; `{slug}` = Wikibooks
filename stem; `{n}` = 0-based paragraph index within the unit.

6. Gate conformance (extends 1GB §3 G1/G3 for kinds 5–8): kind ∈ {5,6,7,8};
   1 ≤ key_len ≤ 160; **20** ≤ text_len ≤ 4096; no NUL bytes; no bytes < 0x20
   except 0x0A in text; key contains no 0x0A.
7. Sort: all records sorted by key bytes ascending (same convention as 1GB §2),
   then written to `facts.dat`.

## R10 — Manifest

The cleaner writes `MANIFEST.json` (keys sorted, no timestamps): per source —
`files`, `input_bytes`, `cleaned_bytes`, `facts`; plus `sha256` of `facts.dat`
and of the concatenated cleaned outputs (sources in fixed order
gutenberg, openstax, stackexchange, wikibooks).

## Determinism proof (required)

`clean.py --selftest`: cleans `fixtures/inputs/` into two scratch dirs, SHA256-hashes
every cleaned file and `facts.dat` from both runs; PASS iff all hashes equal.
`clean.py --check`: cleans `fixtures/inputs/`, byte-compares against
`fixtures/expected/`; non-zero exit on any mismatch.

## Worked example (end to end, Gutenberg)

Input bytes (raw):
```
EF BB BF 54 68 65 20 50 72 6F 6A 65 63 74 ... "*** START OF THE PROJECT GUTENBERG EBOOK FOO ***\n\n\nIt was the best of times,\r\nit was the worst of times.\n\n----------------------------------------\n\nIt was the best of times,\nit was the worst of times.\n\n*** END OF THE PROJECT GUTENBERG EBOOK FOO ***\nLicense footer.\n
```
- R1: BOM stripped. R2: `\r\n`→`\n`.
- R4: everything through the START line deleted; everything from the END line deleted.
- R6: `\n\n\n` → `\n\n`.
- R5a: the `----…` line dropped.
- R8b: the duplicated paragraph dropped (second occurrence).
- R9: one paragraph ≥ 20 chars → one kind-7 fact, key `gb:{gid}:0`.

Output cleaned text: `It was the best of times,\nit was the worst of times.\n`
