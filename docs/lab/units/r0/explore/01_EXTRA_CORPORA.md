# EXPLORE 01 — Extra corpora: which byte materials would discriminate chunkers beyond Shakespeare + sqlite3.c

**Status: EXPLORATORY / NON-BINDING.** Survey + proposal only. Nothing here changes
frozen bars. If pursued, proposals in this doc would amend **M-5** (third-corpus choice
for M2 T2/T3) and, for the byte-hygiene item, **M-1** (boundary fidelity — what counts
as a legal cut).

**Frozen context:** corpora are Shakespeare prose (~5.4MB) and sqlite3.c (~9.5MB), hashes
committed before arms are built (M-30); M2's third corpus is proposed as Gutenberg KJV
prose + CPython `longobject.c` (M-5). The question this doc answers: *what would a
third/fourth material need to prove that Shakespeare + sqlite3.c cannot?*

**License rule for this survey:** public-domain or permissive-license (MIT/BSD/CC-BY-SA
with attribution) only. No scraped copyrighted text, no proprietary code.

---

## What Shakespeare + sqlite3.c already discriminate

- English dialogue-heavy prose vs generated-style C (long lines, dense punctuation).
- Whitespace/punctuation-delimited structure (the C-W confound pricer).
- Identifier-dense code vs word-dense prose.

## What they do NOT discriminate

1. **Degeneracy under low-entropy input** — neither corpus contains long constant runs
   or perfectly periodic stretches. A chunker that mints degenerate spans on
   `xxxx…` or `ababab…` is never exposed (see probe_rep: `probe_rep.zag`).
2. **Byte hygiene on multi-byte encodings** — both are ASCII. A chunker that splits
   inside a UTF-8 codepoint is never caught.
3. **Non-textual latent structure** — both are human text. Nothing tests whether
   chunking discovers structure in binary-ish streams (the R31 substrate was
   32-symbol microstate streams, not text at all).
4. **Extreme template repetition** — neither corpus stress-tests dedup/reuse (M7)
   the way machine-generated logs do.
5. **Delimiter-free code** — sqlite3.c is whitespace-rich; minified code would price
   the C-W confound much harder.

---

## Candidate materials (license-clean)

### C1. Genomic FASTA excerpts (e.g., NCBI RefSeq, public domain — US federal work)
- **What it is:** ~4-letter alphabet (ACGT) + `>` header lines, megabyte scale available.
- **What it discriminates:** degeneracy. Near-maximal-entropy, minimal-alphabet streams
  are the closest natural analog to R31's original 32-symbol substrate. Exposes chunkers
  that recruit noise (seen≥5 fires constantly on 4-mers by chance) vs chunkers whose
  grounding term correctly abstains. Directly stresses the R-2 giant-span bar and the
  purity term (R-1).
- **Caveat:** needs a defined "grounded consequence" for DNA (R-1 is already load-bearing;
  DNA makes it harder, not easier). Propose as T3-only, never T2.

### C2. Multilingual UTF-8 prose (Project Gutenberg, public domain — e.g., French/German editions)
- **What it is:** prose with multi-byte codepoints, same license story as Shakespeare.
- **What it discriminates:** byte hygiene. A legal cut inside a UTF-8 continuation byte
  corrupts the literal-fallback round-trip guarantee (R31: "information is not destroyed
  merely because the current chunk vocabulary is weak"). This is a *correctness*
  discriminator, not a performance one: any arm that cuts mid-codepoint fails M-1
  boundary legality outright.
- **Would amend:** M-1 (add "no cut inside a UTF-8 sequence" as a boundary-fidelity
  legality rule) if pursued.

### C3. Minified JavaScript (e.g., jQuery min builds, MIT license)
- **What it is:** real-world code with nearly all whitespace removed.
- **What it discriminates:** prices the C-W delimiter confound harder than sqlite3.c.
  If a smart arm's win over C-W on sqlite3.c is "rediscovering whitespace," minified JS
  removes the whitespace to rediscover. C-W should collapse here; arms whose cut signal
  is genuinely structural (surprise, branching) should not.
- **Would amend:** M-5 (as the code-side T3 material instead of/in addition to longobject.c).

### C4. Machine-generated HTTP logs (e.g., NASA HTTP logs, public domain — US federal work)
- **What it is:** highly templated lines: IP, timestamp, method, path, status, bytes.
- **What it discriminates:** dedup/reuse (M7) under extreme template repetition, and
  the K-arm identity story: thousands of near-identical spans differing in 1–2 fields
  (timestamps, IPs). Tests whether content-addressed IDs + dedup actually pay (K1's
  <15% savings kill bar, A-24) and whether the disambiguation chain (probe_id,
  `probe_id.zag`) stays short on near-duplicate floods.
- **Caveat:** timestamps/IPs are semi-sensitive in real logs; use only the published
  public-domain NASA set, never private logs.

### C5. Hand-written single-file C libraries (stb — public domain; miniz — public domain)
- **What it is:** human-authored C with heavy macro use and terse style (Sean Barrett's
  stb), contrasting with sqlite3.c's amalgamated/generated character.
- **What it discriminates:** whether code-chunking results transfer across *authorial
  styles* of C (M6 transfer P→C direction, M-28). Cheap to add; same license class as
  sqlite3.c.

### C6. Lua interpreter source (MIT license)
- **What it is:** a complete, compact language implementation in ANSI C (~30k lines).
- **What it discriminates:** like C5, but a full *system* (parser/VM/GC) rather than a
  library — tests chunking on deeply self-referential code (the VM's own dispatch loops).

### C7. Public-domain MIDI bytes (classical MIDIs, composer public domain; file format is facts)
- **What it is:** structured binary: delta-time varints + note events.
- **What it discriminates:** non-textual latent structure with a real grammar
  (variable-length quantities punish byte-aligned fixed chunkers like B-8/B-64).
  Tests the "cognitive, not fixed discretization" thesis on genuinely non-text data.
- **Caveat:** needs a byte-stream framing decision (strip headers or not) — that
  framing choice is itself a judgment call → test-both per RULE-2 if pursued.

### C8. Raw PPM image bytes (generate locally, or public-domain images)
- **What it is:** 2-D structure (scanlines) flattened to 1-D bytes.
- **What it discriminates:** whether chunking discovers *scanline* periodicity — a
  pure-structure discovery test with ground truth (image width is known). The visual
  analog of probe_rep's period-2 stream, but natural.

### C9. Wikipedia XML excerpts (CC BY-SA — license-clean with attribution)
- **What it is:** mixed markup + multilingual article text.
- **What it discriminates:** markup-vs-content boundary discovery: does the chunker
  learn `<ref>…</ref>` as units without being told what XML is? Tests the
  taught-vs-emergent boundary (arm O vs arm P) on real mixed data.

---

## Proposed (not imposed) additions, ranked

1. **C2 multilingual UTF-8** — cheapest, license-identical to Shakespeare, and it is a
   *correctness* gate (mid-codepoint cuts) rather than a benchmark tweak. Would amend M-1.
2. **C4 NASA logs** — the strongest M7 (dedup/reuse) and K-arm discriminator; public
   domain; would amend M-5 (T3 material).
3. **C3 minified JS** — the honest C-W confound pricer; MIT; would amend M-5.
4. **C1 FASTA DNA** — the degeneracy discriminator and the truest heir to R31's
   32-symbol substrate; T3-only; needs R-1 operationalized for DNA first.

**Explicit non-proposals:** copyrighted books, proprietary codebases, private user data,
scraped web text of unclear license — all excluded by the license rule above.

---

## Relation to frozen bars

| Proposal | Frozen bar it would amend (if pursued) |
|---|---|
| C2 as corpus | M-1 (boundary legality: no mid-codepoint cuts), M-5 (corpus set) |
| C4 as T3 | M-5 (third-corpus choice) |
| C3 as code-side T3 | M-5 |
| C1 as T3 | M-5, plus R-1 (grounded consequence for DNA) |
| C5/C6 as style-transfer pair | M-28 (transfer bars) via M6 |

All amendments require Micah's re-approval per §0 RULE-9. This doc proposes; it does not move.
