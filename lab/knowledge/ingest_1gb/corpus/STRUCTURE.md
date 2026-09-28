# Corpus Structure

## enwiktionary-latest-pages-articles.xml.bz2

MediaWiki export XML 0.11, bzip2-compressed. Stream structure:
- `<mediawiki>` → `<page>`* → `</mediawiki>`
- Each `<page>`: `<title>`, `<ns>`, `<id>`, `<revision>` → `<text xml:space="preserve">` (wikitext)
- Extraction uses only `ns=0` pages without `<redirect`, taking the `==English==`
  section (up to the next `==Language==` header).
- Within `==English==`: `===POS===` subsections (noun/verb/adjective/adverb/...) contain
  sense lines (`# ` top-level, `## ` subsenses). `#*`/`#:` lines are examples/quotes, skipped.
- Inflection/form-of senses: the sense's first template is one of
  `plural of|singular of|past of|past participle of|present participle of|`
  `third-person singular of|comparative of|superlative of|alternative form of|`
  `alternative spelling of|inflection of|feminine of|masculine of` → kind 2,
  key `wikt:en:{base}:{label}:{form}:{n:02d}`, text `{label} of {base}`.
- All other senses → kind 1, key `wikt:en:{word}:{pos}:{sensenum:03d}`, text = cleaned definition.
- Template cleaning: `{{...}}` parsed with nesting; `l|m|link|ll` templates yield
  their display text; all other templates dropped. `[[a|b]]`→`b`, `[[a]]`→`a`.

## simplewiki-latest-pages-articles.xml.bz2

MediaWiki export XML 0.11, bzip2-compressed. Same page envelope as above.
- Extraction uses only `ns=0` pages, skipping `<redirect>` and `#REDIRECT` bodies,
  skipping titles containing `:`.
- Wikitext → plain text: comments/refs/tables/templates stripped (nested),
  `[[File:|Image:|Category:]]` dropped, links → display text, bold/italic removed,
  headings dropped, list markers stripped, HTML tags/entities resolved.
- Sentences split on `[.!?] + whitespace + [A-Z0-9"'([]`; kept if 10–4096 bytes,
  ending in `[.!?]`, containing ≥5 letters.
- Key `wiki:simple:{slug}:sent{n:06d}` (slug = lowercased title, spaces→_, ≤120 chars).
- Kind 3.

## wordnet31.zip (NLTK transport of WordNet 3.1)

Zip containing the WordNet 3.1 database files (`log.grind.3.1` confirms version).
- `data.noun` / `data.verb` / `data.adj` / `data.adv`: one synset per line:
  `offset lex_filenum ss_type w_cnt word lex_id ... | gloss`
- Lines starting with space are the license header, skipped.
- Extraction: text after `| `, trimmed; kept if 4–4096 bytes, no NUL.
- Key `wn:3.1:{n|v|a|r}:{offset:08d}`. Kind 4.
- Yield: 117,789 synset glosses (n=82,190, v=13,789, a=18,185, r=3,625).
