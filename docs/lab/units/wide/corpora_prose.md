# EXPLORATORY — NOT EVIDENCE: Extra Prose Corpora for the TNN Representation Program

**EXPLORATORY — NOT EVIDENCE.** This document is a wide-exploration worker product on a
NON-BINDING track. Nothing in it counts as program evidence. No number, table, or
observation below may be cited as a trial result, used to pass/fail any arm, or used to
satisfy any preregistered bar, metric, or kill criterion. The characterization program
(`char_prose.zag`) was run for INFORMATIONAL purposes only, to inform probe *design*.

**Frozen-program compliance statement.** This work does not change, reinterpret, or soften
any frozen bar, metric, or kill criterion in `PREREG_FREEZE.md` (Micah-signed 2026-09-21).
Anything below that contradicts or tensions a frozen assumption is written up as an
**amendment PROPOSAL** in §7 — proposals only, not actions. No amendment is in effect
unless and until Micah signs it. Pure Zag for all executables; zero randomness anywhere
(the characterizer is fully deterministic: same bytes in → same numbers out, no seeds, no
sampling). Google Drive was not touched. No binaries, `.zagd`, or `.zag-cache` committed.
Corpora are fetched on demand and never committed, mirroring the frozen Shakespeare /
sqlite3.c pipeline rule.

**Reproducibility artifacts (workspace, uncommitted by coordinator batch):**
- `units/wide/fetch_corpora_prose.sh` — deterministic fetcher, SHA-256-pinned per file,
  aborts on hash mismatch. Usage: `./fetch_corpora_prose.sh <dest-dir>`
- `units/wide/char_prose.zag` — pure-Zag characterizer (byte histogram classes, line
  stats, top-16 bytes, deterministic 8-byte-window repetition estimate). Built with the
  lab `znc` (`--no-zagd --no-analyze --no-foreground-cache`); binary kept in `/tmp`
  (never in the repo). Raw `KEY,value` outputs for all six corpora were captured
  2026-09-21 and transcribed into §5.

---

## §1 — Corpus catalog (6 corpora, all Project Gutenberg, all US public domain)

Selection goals: different authors, eras (1651–1895), and genres (philosophy, gothic
novel, Victorian novel, scientific memoir, detective short stories, sci-fi novella) —
deliberately *not* more Shakespeare. All six are plain-text UTF-8 ebook releases.

| # | Work | Author (d.) | Orig. pub. | Gutenberg | Bytes | SHA-256 (fetched 2026-09-21) |
|---|------|-------------|-----------|-----------|-------|------------------------------|
| C1 | *Leviathan* | Thomas Hobbes (d. 1679) | 1651 | [#3207](https://www.gutenberg.org/cache/epub/3207/pg3207.txt) | 1,254,939 | `3de1e492…b7294` |
| C2 | *Frankenstein; or, The Modern Prometheus* | Mary Wollstonecraft Shelley (d. 1851) | 1818 | [#84](https://www.gutenberg.org/cache/epub/84/pg84.txt) | 448,885 | `7810cd48…82fead3` |
| C3 | *A Tale of Two Cities* | Charles Dickens (d. 1870) | 1859 | [#98](https://www.gutenberg.org/cache/epub/98/pg98.txt) | 807,197 | `d54c2b80…1750681784` |
| C4 | *The Autobiography of Charles Darwin* | Charles Darwin (d. 1882) | 1887 | [#2010](https://www.gutenberg.org/cache/epub/2010/pg2010.txt) | 149,762 | `7e2937e4…85d687d8d00b` |
| C5 | *The Adventures of Sherlock Holmes* | Arthur Conan Doyle (d. 1930) | 1892 | [#1661](https://www.gutenberg.org/cache/epub/1661/pg1661.txt) | 607,606 | `922e2a12…857cd0` |
| C6 | *The Time Machine* | H. G. Wells (d. 1946) | 1895 | [#35](https://www.gutenberg.org/cache/epub/35/pg35.txt) | 204,384 | `2892e919…9a89bb399a9bdc` |

(Full hashes: C1 `3de1e492641d939567a8b0de827fb13e1ad992324f9ac8b204f60475009b7294`;
C2 `7810cd483cffcf2cc8a1d8f0d5807931e69d4f48cd14149b8c76f88af82fead3`;
C3 `d54c2b80d40a40b982cd88852c6180bb944d95acdb028af3d0e01a1750681784`;
C4 `7e2937e414d27ec2ee9bced09e1f9066191732aeaa15cc44ad9d85d687d8d00b`;
C5 `922e2a12ccb43a4c9544c260b2166c6ad2097aeb5957faeee113f173bb857cd0`;
C6 `2892e919000e17c83e1dac51b30f4675db50536b644d7579fe8a89bb399a9bdc`.)

### Public-domain justification (per corpus, explicit)

US rule applied: **works first published before 1930 are in the public domain in the
United States** (copyright term for pre-1978 works has expired as of 2026). Every corpus
below was first published before 1930, so US PD status holds *regardless* of author death
date; death dates are given as the independent second leg. Project Gutenberg additionally
clears US PD status before hosting any ebook (its license headers assert this per file).

- **C1 Leviathan** — Hobbes d. 1679; published 1651 (pre-1930 by 279 years). PD on both legs.
- **C2 Frankenstein** — Shelley d. 1851; published 1818. PD on both legs.
- **C3 A Tale of Two Cities** — Dickens d. 1870; published 1859. PD on both legs.
- **C4 Darwin autobiography** — Darwin d. 1882; published 1887 (Barlow unexpurgated
  edition is later, but the 1887 first publication fixes PD). PD on both legs.
- **C5 Sherlock Holmes** — Doyle d. 1930; published 1892 (pre-1930). PD in the US on the
  publication leg; note Doyle's 1930 death means life+70 jurisdictions cleared in 2001.
- **C6 The Time Machine** — Wells d. 1946; published 1895 (pre-1930). PD in the US on the
  publication leg (life+70 cleared 2017).

No translations are included (translation copyrights add a third leg of analysis; all six
are English originals).

### Deliberate exclusion

The **King James Bible** (Gutenberg) is *not* in this set: frozen prereg item **M-5**
already names "Gutenberg *King James Bible* prose" as the candidate T2 third corpus. This
exploratory set avoids overlapping the frozen plan to prevent confusion about what is
frozen vs. exploratory.

### Gutenberg boilerplate (byte ranges, informational)

Each file carries the standard PG header/footer. Approximate body ranges (from the
`*** START OF` / `*** END OF` markers):

| Corpus | File bytes | Body approx. start | End marker approx. |
|--------|-----------|-------------------|-------------------|
| C1 | 1,254,939 | 788 | 1,236,043 |
| C2 | 448,885 | 970 | 429,959 |
| C3 | 807,197 | 810 | 788,290 |
| C4 | 149,762 | 854 | 130,840 |
| C5 | 607,606 | 870 | 588,686 |
| C6 | 204,384 | 753 | 185,481 |

(Any future harness work on these corpora should strip boilerplate the same way the
frozen pipeline treats Shakespeare; the characterization in §5 is on the raw fetched
bytes, boilerplate included — stated so the numbers are interpretable.)

---

## §2 — Byte-level character notes (encoding quirks)

Measured with `char_prose.zag` (§5) plus a read-only byte-frequency inspection of the
high-byte range (deterministic `od`/`sort`/`uniq` counts, informational only):

- **Line endings: CRLF everywhere.** All six files use `\r\n` exclusively
  (`CRLF_LINES == LINES`; zero lone `\r`, zero bare `\n`). Byte 13 (`\r`) is a top-16
  byte in every file. Any segmenter that treats `\r` as content vs. delimiter will behave
  identically across these six — but a future LF-only corpus would be a different regime.
- **No NUL bytes, no stray control bytes** in any file (`CLASS_NUL = 0`, `CLASS_CTRL = 0`).
  Clean 7-bit ASCII body plus structured high bytes.
- **UTF-8, not Latin-1/CP1252.** The high bytes are well-formed UTF-8, verified by
  structure: bytes `226,128` (0xE2 0x80) co-occur ~6,800× in C5 as the lead pair of
  three-byte sequences, with third bytes 156/157/153/152/148 — i.e. U+201C/U+201D
  (curly double quotes), U+2019/U+2018 (curly single quotes), U+2014 (em dash).
  Bytes 194/195 (0xC2/0xC3) appear as two-byte lead bytes (e.g. U+00A9 ©). A residual
  count of 17 in C5/C3/C2 shows byte 226 *not* followed by 128 — other E2-led sequences
  (arrows/dashes), consistent with valid UTF-8, not corruption. **Correction to a naive
  reading:** bytes in 0x80–0x9F here are UTF-8 *continuation* bytes, not Windows-1252
  smart quotes. Any byte-level arm must therefore expect to encounter (and potentially
  cut inside) multibyte sequences.
- **No BOM** in any file.
- **Non-ASCII load varies 40× across the set** (per-mille of bytes ≥128): C1 0‰,
  C2 7‰, C6 13‰, C3 26‰, C5 33‰, C4 9‰. Dialogue-heavy 19th-century prose (C3, C5)
  carries the most multibyte punctuation; 17th-century philosophy (C1) carries
  essentially none (313 high bytes in 1.25MB, and those are the PG header's own
  characters).
- **Whitespace is a stable ~19–20% of bytes** in all six (per-mille 192–202); space
  (byte 32) is the single most frequent byte everywhere (15.9–16.2%).

---

## §3 — Informational characterization (from `char_prose.zag`, NOT evidence)

### Byte histogram summary

Top-byte order is near-identical across all six — classic English prose profile:

`space(32) > e(101) > t(116) > a(97)/o(111) > n(110) > i(105) > h(104) > s(115) > r(114) > d(100) > l(108) > …`

with `,`(44) and `\n`(10)/`\r`(13) rounding out the top 16 everywhere. Two deviations
worth noting: C2 (Frankenstein) ranks `m`(109) unusually high (10,240; epistolary
"my/me/I" voice) and C1 (Leviathan) shows `,`(44) at rank 14 (23,810 — long periodic
sentences). Printable ASCII is 80–81% of bytes; whitespace ~19.5%; high bytes 0–3.3%.

### Line-length statistics

| Corpus | Lines | Mean len | Max len |
|--------|-------|----------|---------|
| C1 Leviathan | 23,003 | 53 | 79 |
| C2 Frankenstein | 7,741 | 56 | 100 |
| C3 Tale of Two Cities | 16,283 | 48 | 83 |
| C4 Darwin | 2,516 | 58 | 138 |
| C5 Sherlock Holmes | 12,310 | 48 | 89 |
| C6 Time Machine | 3,558 | 56 | 82 |

All six are hard-wrapped by Gutenberg at ~65–75 columns (mean 48–58 incl. `\r`).
Newline is therefore a strong, cheap, *artifactual* boundary signal present in every
corpus — relevant to probe P4.

### Repetition statistics (deterministic 8-byte windows, stride 16)

`REP_EXTRA_PERMILLE` = per-mille of sampled 8-byte windows that are repeats of an
earlier-sampled window (exact byte match, hash-verified by memcmp):

| Corpus | Samples | Distinct | Slots ≥2 | Extra windows | **Repeat ‰** |
|--------|---------|----------|----------|---------------|--------------|
| C1 Leviathan | 78,434 | 58,363 | 8,776 | 19,905 | **253** |
| C3 Tale of Two Cities | 50,450 | 42,200 | 4,456 | 8,250 | **163** |
| C5 Sherlock Holmes | 37,975 | 32,014 | 3,212 | 5,961 | **156** |
| C2 Frankenstein | 28,055 | 24,921 | 2,048 | 3,134 | **111** |
| C6 Time Machine | 12,774 | 11,757 | 694 | 1,017 | **79** |
| C4 Darwin | 9,360 | 8,728 | 458 | 632 | **67** |

**Most interesting characterization result:** the repetition spread is ~4× end to end.
Leviathan repeats sampled 8-byte windows at **25.3%** — philosophical prose is highly
formulaic ("of the", "it is manifest", chapter/section scaffolding) — while Darwin's
memoir repeats at only **6.7%**. This is the axis these corpora buy the program: the
frozen corpora (Shakespeare drama + C code) sit at unknown points on this axis, and any
arm whose mechanism keys off repetition (D's REP_BAR, K1/K2 dedup-savings claims,
F-S/F-B recurrence requirements) will see a materially different regime here. The
dialogue-heavy pair (C3, C5) also couples the *highest* repetition among novels with the
*highest* multibyte load — a natural joint stress test.

---

## §4 — Informational generalization probe designs (DESIGNED, NOT RUN)

Each probe below is a design sketch only. Running any of them as program evidence would
require a dated prereg amendment and Micah's sign-off; the "what we would learn" is the
deliverable of this section.

### P1 (top pick) — Delimiter-arm confound pricing across registers

**Question:** the frozen program prices the confound *"how much of the smart arms' win is
just rediscovering whitespace?"* via C-W/C-P on Shakespeare. Is that price
corpus-contingent?
**Design:** run the frozen arms' segmenters (instrumented harness, read-only) over three
registers: C1 (formulaic philosophy, 253‰ repeat), C4 (low-repeat memoir, 67‰), C5
(dialogue-heavy, 156‰ repeat + 33‰ multibyte). For each arm × corpus, record boundary
agreement (F1) between the smart arm's cuts and C-W's cuts, plus M3-style retrieval cost
at equal M1.
**What we would learn:** whether D/F-S/F-B beat C-W by a stable margin or whether the
margin inverts by register. An inversion (e.g. D ≫ C-W on Shakespeare but D ≈ C-W on
Leviathan, where repetition alone predicts boundaries) would mean the program's control
pricing does not generalize — candidate amendment: add one high-repetition and one
dialogue-heavy corpus as *informational* legs on the A/B/C control retirement rules.
**Why it matters for frozen assumptions:** arm D's kill bar (i) and C-W's **[REV]** rule
("if no smart arm beats C-W on Shakespeare by end of 10x, every smart arm is killed")
are both priced on a single prose register.

### P2 (top pick) — UTF-8 multibyte stress for byte-level identity arms

**Question:** do byte-level chunkers pay a hidden multibyte tax, and does it distort the
identity bake-off?
**Design:** on C5 (33‰ non-ASCII) and C3 (26‰), count per arm: (a) cuts landing *inside*
a UTF-8 sequence; (b) chunks whose SHA-256 (K1) or FNV-1a (K2) identity spans a partial
character; (c) dedup-savings delta between byte-exact and codepoint-normalized chunking.
**What we would learn:** whether the frozen program's byte-level framing systematically
mints character-splitting chunks on 19th-century prose, and whether K1-vs-K2-vs-L1
rankings shift once identities are codepoint-aligned. A large tax would motivate a
candidate amendment: a frozen rule that chunk boundaries must not split UTF-8 sequences
(byte-level arms stay byte-level; they just may not cut mid-character).
**Why it matters:** D's MIN_LEN=3 is in *bytes* — three bytes can be a single em dash.
The frozen corpora's multibyte load is uncharacterized in the prereg; these six bound it
at 0–33‰.

### P3 — REP_BAR sensitivity across repetition regimes

**Question:** is arm D's frozen REP_BAR tuned to Shakespeare's repetition regime?
**Design:** run D's proposer (only the proposal stage, no commits needed for the
informational read) with the REP_BAR bracket {low, frozen, high} on C1 (253‰) vs C4
(67‰); record proposal volume and the fraction of proposals that would recur (rep≥2).
**What we would learn:** whether the frozen REP_BAR under-triggers on formulaic prose
(missing cheap wins) or over-triggers on varied prose (proposal spam). Predicts whether
D's kill bar (ii), churn > 0.30 at 10x, is corpus-driven rather than mechanism-driven.

### P4 — Line-wrap as a free segmentation signal (F-S/F-B honesty check)

**Question:** do "surprise" arms merely rediscover Gutenberg's hard line-wrap?
**Design:** measure each arm's boundary agreement with line breaks (`\n` positions) across
all six corpora (mean line length 48–58 everywhere — the signal is uniformly present).
**What we would learn:** if F-S/F-B boundary F1 vs. line-breaks ≈ F1 vs. C-W, the
"surprise" mechanism adds nothing over whitespace+wrap on prose — an informational
result that would motivate a candidate amendment: a line-wrap-aware baseline arm so
F-S/F-B are priced against the true cheap signal, not just C-W.

### P5 — CRLF robustness (harness-level)

**Question:** does any arm treat `\r` as content?
**Design:** diff each arm's boundaries with and without `\r`-stripping on all six
(CRLF-only) corpora.
**What we would learn:** whether boundary fidelity is robust to line-ending
normalization. A `\r`-sensitive arm would behave differently on any future LF-only
corpus — a portability flag, informational only, no frozen bar touched (the frozen
corpora are Gutenberg CRLF as well, so this is currently a latent, not active, risk).

---

## §5 — Raw characterization outputs (transcribed from `char_prose.zag` runs, 2026-09-21)

Program contract: `KEY,value` lines; `TOPB,byte,count`; repetition = 8-byte windows at
stride 16 into a 65536-slot open-address table (multiply-add hash, memcmp-verified).
Deterministic — no RNG, no sampling randomness (stride sampling is fixed).

```
### C1 pg3207.txt (Leviathan)
BYTES,1254939 LINES,23003 MEAN_LINE_LEN,53 MAX_LINE_LEN,79 CRLF_LINES,23003
CLASS_NUL,0 CLASS_WS,245495 CLASS_CTRL,0 CLASS_PRINT,1009131 CLASS_HIGH,313
CLASS_C1_80_9F,182 WS_PERMILLE,195 HIGH_PERMILLE,0 UTF8_BOM,0
TOPB: 32:199489 101:124043 116:93977 111:76673 97:67776 110:67410 105:63784
  104:62531 115:56694 114:55623 100:30662 108:30458 117:24114 44:23810 10:23003 13:23003
REP_SAMPLES,78434 REP_DISTINCT,58363 REP_SLOTS_GE2,8776 REP_EXTRA_WINDOWS,19905
REP_EXTRA_PERMILLE,253

### C2 pg84.txt (Frankenstein)
BYTES,448885 LINES,7741 MEAN_LINE_LEN,56 MAX_LINE_LEN,100 CRLF_LINES,7741
CLASS_NUL,0 CLASS_WS,87241 CLASS_CTRL,0 CLASS_PRINT,358174 CLASS_HIGH,3470
CLASS_C1_80_9F,2251 WS_PERMILLE,194 HIGH_PERMILLE,7 UTF8_BOM,0
TOPB: 32:71759 101:45775 116:29727 97:26324 111:25089 110:24225 105:21395
  115:20824 114:20767 104:19446 100:16726 108:12592 117:10345 109:10240 99:9062 102:8509
REP_SAMPLES,28055 REP_DISTINCT,24921 REP_SLOTS_GE2,2048 REP_EXTRA_WINDOWS,3134
REP_EXTRA_PERMILLE,111

### C3 pg98.txt (A Tale of Two Cities)
BYTES,807197 LINES,16283 MEAN_LINE_LEN,48 MAX_LINE_LEN,83 CRLF_LINES,16283
CLASS_NUL,0 CLASS_WS,159613 CLASS_CTRL,0 CLASS_PRINT,626553 CLASS_HIGH,21031
CLASS_C1_80_9F,13925 WS_PERMILLE,197 HIGH_PERMILLE,26 UTF8_BOM,0
TOPB: 32:127047 101:74360 116:52290 97:47229 111:46224 110:41984 105:38121
  104:38049 114:36965 115:36675 100:27060 108:21202 117:16651 10:16283 13:16283 109:13609
REP_SAMPLES,50450 REP_DISTINCT,42200 REP_SLOTS_GE2,4456 REP_EXTRA_WINDOWS,8250
REP_EXTRA_PERMILLE,163

### C4 pg2010.txt (Darwin autobiography)
BYTES,149762 LINES,2516 MEAN_LINE_LEN,58 MAX_LINE_LEN,138 CRLF_LINES,2516
CLASS_NUL,0 CLASS_WS,28802 CLASS_CTRL,0 CLASS_PRINT,119544 CLASS_HIGH,1416
CLASS_C1_80_9F,923 WS_PERMILLE,192 HIGH_PERMILLE,9 UTF8_BOM,0
TOPB: 32:23770 101:13954 116:9938 111:8979 97:8857 110:7795 105:7306
  115:6948 114:6814 104:5763 100:4606 108:4464 99:3440 109:3095 117:3069 102:2606
REP_SAMPLES,9360 REP_DISTINCT,8728 REP_SLOTS_GE2,458 REP_EXTRA_WINDOWS,632
REP_EXTRA_PERMILLE,67

### C5 pg1661.txt (Sherlock Holmes)
BYTES,607606 LINES,12310 MEAN_LINE_LEN,48 MAX_LINE_LEN,89 CRLF_LINES,12310
CLASS_NUL,0 CLASS_WS,123197 CLASS_CTRL,0 CLASS_PRINT,463836 CLASS_HIGH,20573
CLASS_C1_80_9F,13615 WS_PERMILLE,202 HIGH_PERMILLE,33 UTF8_BOM,0
TOPB: 32:98577 101:54610 116:39249 97:35303 111:34482 110:29334 104:28312
  105:27358 115:27080 114:25428 100:18797 108:17279 117:13500 10:12310 13:12310 109:11336
REP_SAMPLES,37975 REP_DISTINCT,32014 REP_SLOTS_GE2,3212 REP_EXTRA_WINDOWS,5961
REP_EXTRA_PERMILLE,156

### C6 pg35.txt (The Time Machine)
BYTES,204384 LINES,3558 MEAN_LINE_LEN,56 MAX_LINE_LEN,82 CRLF_LINES,3558
CLASS_NUL,0 CLASS_WS,39830 CLASS_CTRL,0 CLASS_PRINT,161729 CLASS_HIGH,2825
CLASS_C1_80_9F,1847 WS_PERMILLE,194 HIGH_PERMILLE,13 UTF8_BOM,0
TOPB: 32:32714 101:19581 116:14315 97:12427 111:11037 110:10896 105:9726
  115:9097 114:8808 104:8711 100:6786 108:6565 117:4246 109:4145 99:3977 102:3598
REP_SAMPLES,12774 REP_DISTINCT,11757 REP_SLOTS_GE2,694 REP_EXTRA_WINDOWS,1017
REP_EXTRA_PERMILLE,79
```

High-byte spot check (C5/C3/C2, informational): dominant high bytes are 226+128
(0xE2 0x80 — lead pair of U+2018/2019/201C/201D/2014) with third bytes
148/152/153/156/157, plus 194/195 (0xC2/0xC3 two-byte leads). Confirms well-formed
UTF-8 curly quotes/em dashes, not CP1252.

---

## §6 — What these corpora buy the program (informational)

1. **A repetition axis the frozen set lacks.** Shakespeare (drama: verse + prose + stage
   directions) and sqlite3.c (code) are two points; these six span 67–253‰ window-repeat
   on a single deterministic statistic. Any claim of the form "arm X exploits repetition"
   can be sanity-shaped against this axis without touching frozen bars.
2. **A multibyte axis.** 0–33‰ non-ASCII, all well-formed UTF-8 — the frozen program's
   byte-level framing has an uncharacterized interaction here (see P2).
3. **Register diversity for the controls.** Formulaic philosophy (C1), epistolary gothic
   (C2), Victorian omniscient (C3), scientific memoir (C4), dialogue-driven shorts (C5),
   novella (C6) — six distinct boundary-placement regimes for pricing C-W/C-P honestly.
4. **Cheap scale.** Largest is 1.25MB — every corpus fits comfortably under the 2^25
   slice wall with no striping needed, and full-corpus runs are fast enough for
   exploratory iteration.

---

## §7 — Amendment PROPOSALS (not in effect; Micah's sign-off required for any)

*Per the task's hard rules: these are proposals only. Nothing below changes the frozen
prereg. Each would need a dated amendment and Micah's re-approval before any effect.*

- **AP-1 (corpus-contingent control pricing).** *If* probe P1 shows the C-W-vs-smart-arm
  margin inverts across registers, propose adding one high-repetition corpus (C1) and one
  dialogue-heavy corpus (C5) as **informational-only** legs on the A/B/C control
  retirement rules — informational legs do not fire kill bars; they annotate them.
  Frozen bars (D kill bar (i), C-W [REV]) unchanged unless separately amended.
- **AP-2 (UTF-8 boundary rule).** *If* probe P2 finds a material rate of cuts inside
  multibyte sequences, propose a frozen harness-level rule: chunk boundaries must not
  split a UTF-8 sequence (arms stay byte-level; the rule only forbids mid-character
  cuts). Would need Micah's sign-off as a prereg amendment; until then, byte-level
  cutting stands as frozen.
- **AP-3 (line-wrap baseline).** *If* probe P4 shows F-S/F-B boundaries ≈ line-break
  positions, propose a line-wrap-aware baseline arm so surprise-based arms are priced
  against the true cheap signal. New arm = program addition, needs sign-off; does not
  alter any existing arm's frozen kill criterion.
- **AP-4 (no action).** No finding in this exploratory pass contradicts a frozen
  *numeric* bar directly; the tensions above are all regime-coverage questions, hence
  proposals for informational legs rather than bar changes.

---

## §8 — Method notes

- Characterization is deterministic: `char_prose.zag` uses no RNG, no wall-clock, no
  ASLR-dependent behavior in its logic (hash table probing is by content hash, ties
  broken by first-seen order). Re-running on the same bytes yields identical output;
  this was verified by compiling once and running across all six inputs (it is *not*
  claimed as M8 evidence — that gate applies to arms, not to this exploratory tool).
- The repetition statistic is a fixed-stride (16) sample of 8-byte windows, not an
  exhaustive repeat count: it is a *comparative* axis across corpora, not an absolute
  repetition measure. Stride and window are documented so the axis is reproducible.
- The znc toolchain wall (no slice > 2^25 bytes) is respected trivially: largest input
  1,254,939 bytes; largest single allocation 3 × 524,288 bytes (repetition table).
- Fetch integrity: `fetch_corpora_prose.sh` pins SHA-256 per file and aborts on
  mismatch. Hashes recorded above are of the bytes fetched 2026-09-21; Gutenberg
  occasionally re-renders ebooks, so a future mismatch means re-verify provenance, not
  silent acceptance.
