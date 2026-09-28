# CLEAN_REPORT.md — Phase 1C cleaning measurements

**Spec:** `CLEAN_SPEC.md` (frozen 2026-09-22, v1C-2026-09-22). **Cleaner:** `clean.py`
(audited Python glue, zero RNG — `grep` for `random|seed|shuffle|uuid` returns nothing).
**Status:** spec frozen, cleaner implemented and proven; measured on hand-verified
spec fixtures. **Real-data measurement BLOCKED** (see §4).

## §1 Rules (10, R1–R10 + R0 invariants)

| Rule | What it does |
|---|---|
| R1 | Encoding → UTF-8 (BOM strip; UTF-8 strict, deterministic windows-1252 fallback) |
| R2 | Line endings → `\n` |
| R3 | Source-structure extraction: SE XML rows → Title/Body, HTML tag strip (block tags → paragraph breaks first), entity unescape, dupe-banner drop; OpenStax XHTML head-drop + same; Wikibooks wikitext strip (tables, bold/italic, headings, links, templates, refs); Gutenberg plain |
| R4 | License boilerplate excision (exact byte patterns: PG START/END markers, `Access for free at openstax.org`, cnx lines, Wikibooks from/retrieved lines) |
| R5 | Decorative runs — Micah's dash-spam order: R5a drop whole-line separator runs (≥3 of `-_*=~#+`, incl. spaced `* * *`); R5b inline `-_~` runs ≥2 → single space (`==`, `*=` code operators untouched) |
| R6 | Whitespace: collapse interior runs, left-flush, blank runs → 1, trim file ends |
| R7 | Nav/ad line drop (7 frozen patterns: bare page numbers, TOC/index/glossary, advertisement, `←`/`→` crumbs, `Page N of M`, `[Page N]`, HTML comments) |
| R8 | Dedupe byte-identical paragraphs, whole-file window, first wins (line-level dedupe deliberately NOT done — repeated dialogue lines like "Yes." are content) |
| R9 | Fact emission: 20-char floor, >4096B sentence-boundary split, new kinds 5–8 (1GB §2 record layout `[1B kind][2B key_len BE][4B text_len BE][key][text]`, sorted by key bytes) |
| R10 | `MANIFEST.json` (per-source bytes/facts, SHA256s, sorted keys, no timestamps) |

New fact kinds (extend 1GB kinds 1–4, keys unique by construction):

| kind | source | key | text |
|---|---|---|---|
| 5 | OpenStax passage | `ostx:{book}:{sec}:{n}` | cleaned paragraph |
| 6 | Stack Exchange post | `se:{site}:q:{postid}` / `se:{site}:a:{postid}` | question: `Title\n\nBody` (one fact, R9.2a); answer: `Body` |
| 7 | Gutenberg paragraph | `gb:{gid}:{n}` | cleaned paragraph |
| 8 | Wikibooks paragraph | `wb:{slug}:{n}` | cleaned paragraph |

Gate conformance for kinds 5–8 (extends 1GB §3): kind ∈ {5..8}; 1 ≤ key_len ≤ 160;
20 ≤ text_len ≤ 4096; no NUL; no bytes < 0x20 except 0x0A in text; key has no 0x0A.
Verified on fixture `facts.dat`: 8/8 records pass, keys strictly ascending.

## §2 Measurements (spec fixtures — hand-verified, byte-exact)

Fixtures in `fixtures/inputs/` were built to carry every noise class in the spec
(BOM, windows-1252 byte, `\r\n`, PG header/footer, START/END markers, dash-spam
lines + inline runs, `* * *` breaks, page numbers, TOC/ad lines, `←` nav crumbs,
HTML tags/entities, dupe-banner blockquote, wikitext markup, tables, templates,
whitespace chaos, duplicated paragraphs, repeated dialogue lines). Expected outputs
in `fixtures/expected/` were verified line-by-line against the spec, then frozen.

| Source | Input bytes | Cleaned bytes | Removed | Facts |
|---|---|---|---|---|
| gutenberg (`1342.txt`) | 596 | 150 | 446 (74.8%) | 3 (kind 7) |
| openstax (`biology2e_ch3.xhtml`) | 412 | 72 | 340 (82.5%) | 2 (kind 5) |
| stackexchange (`cooking.xml`) | 590 | 127 | 463 (78.5%) | 2 (kind 6) |
| wikibooks (`physics.xml`) | 440 | 73 | 367 (83.4%) | 1 (kind 8) |
| **Total** | **2038** | **422** | **1616 (79.3%)** | **8** |

Removed-byte attribution on fixtures: license boilerplate (R4) is the largest
single cut on Gutenberg; dash-spam (R5) the largest on OpenStax/Wikibooks;
HTML/tag + banner noise (R3) the largest on Stack Exchange. (Percentages are
fixture-scale illustrations, not corpus estimates — the fixtures are
noise-dense by design.)

## §3 Determinism proof (zero RNG)

- `clean.py --selftest`: cleans `fixtures/inputs/` into two scratch dirs.
  Run 1: cleaned-tree SHA256 `50b6fc7f81d562d6…`, facts.dat SHA256 `54ed41f36256cc74…`.
  Run 2: identical, all 5 outputs + MANIFEST. **SELFTEST: PASS.**
- `clean.py --check`: cleans fixtures, byte-compares every output against
  `fixtures/expected/` (4 cleaned texts + `facts.dat`). **CHECK: PASS.**
- Re-run any time: `python3 clean.py --raw <rawdir> --out <outdir>` twice and
  `sha256sum` the outputs.

## §4 Real data — BLOCKED, rerun instructions

As of this report, **no raw data has landed**: `~/workspace/scratch_10gb/` does not
exist and `~/workspace/tnn-lab/knowledge/ingest_10gb/acquire/` is empty
(the acquire crew's dir was created 2026-09-22 ~23:3x, no files yet).
Per-source before/after bytes and fact yields on the real 10GB corpus are therefore
not yet measurable. The cleaning stage is complete and waiting:

```sh
cd ~/workspace/tnn-lab/knowledge/ingest_10gb/clean
python3 clean.py --raw ~/workspace/scratch_10gb --out ./run_001   # raw tree: {gutenberg,openstax,stackexchange,wikibooks}/
python3 clean.py --selftest   # re-prove determinism on this machine
```

`run_001/` will contain `cleaned/<source>/…`, `facts.dat` (sorted, kinds 5–8),
and `MANIFEST.json` with the real per-source numbers for this report's §2 table.
Recommended: re-run `--check` first (fixtures must still pass on the runner),
then clean twice and confirm the two `facts.dat` SHA256s match before ingest.
