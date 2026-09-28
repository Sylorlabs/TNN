# PREREG — LI-HARDEN Tier 2 build (Crew T2-BUILD)

Date: 2026-09-24. Scope: HL-6, HL-7, HL-8, HL-9, HL-10 from
`CONVERGENCE_DRAFT.md` (Tier 2 — build next).
Toolchain: pinned `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Language: pure Zag. Zero randomness in any decision path.
Determinism bar: every case × mode, 2 reps, byte-identical stdout.

This prereg is frozen BEFORE mechanism code is written. Consult-extension
material (grok-4.7 / fable-5.1) informed the designs; outcomes are reported
against this frozen text, not fitted to it.

Binary: `tier2` with modes selected by argv[1]:
`extract`, `norm`, `sentsplit`, `attr`, `plat`, `dedup`.
All output is accumulated and printed once from `main` (avoids the
helper-print newline quirk). Exit 0 = ran, 2 = usage/IO error.

Shared frozen inputs:
- PSL: `psl_frozen.txt` (LI-HARDEN-GLUE prereg §4.1, committed) embedded
  byte-identical as a string literal. Matching: longest multi-label suffix
  wins; fallback last-two-labels (errs toward WITHHOLD, per glue §4.1).
- PLATFORM_SUFFIXES (pinned, HL-9 only): `github.io|gitlab.io|bitbucket.io|
  pages.dev|vercel.app|netlify.app|herokuapp.com|blogspot.com|wordpress.com|
  tumblr.com|weebly.com|wixsite.com|medium.com|substack.com|appspot.com|
  glitch.me`. Longest match; account = label immediately above the suffix.

## HL-6 — main-text-only extraction (`tier2 extract <page.html>`)

Mechanism: single-pass HTML tokenizer, pure Zag.
- Drop subtrees: `script style noscript template iframe object embed head`.
- Drop HTML comments (`<!--`…`-->`), `<!…>`, `<?…?>`.
- Drop structural chrome: `footer nav aside`.
- Drop elements with: `hidden` attribute; `aria-hidden="true"`; `style`
  containing `display:none` or `visibility:hidden` (space variants included);
  `class`/`id` containing `comment`, `sidebar`, `widget`; `role` in
  {navigation, complementary, contentinfo, banner}.
- Keep: `article main section div p h1-h6 li blockquote pre` etc.
- Block tags (`p div h1-h6 li br hr article section blockquote pre tr`)
  flush the current line. Void elements never pushed.
- Entity decode: `amp lt gt quot apos nbsp` + `&#DDD;` / `&#xHH;`
  (BMP only, surrogates kept literal). UTF-8 passthrough otherwise.
- Output: `T|<line>` per flushed non-empty line, whitespace-collapsed.
- Caps: 1 MiB input, 64 KiB/line, 64-deep tag stack, 4 MiB output.

Falsification battery (expected outcome per case):
- T6-1 footer: false sentence ONLY in shared `<footer>` → ABSENT from output.
- T6-2 aria-hidden: false sentence ONLY in `<div aria-hidden="true">` → ABSENT.
- T6-3 comment: false sentence ONLY in `<!-- … -->` → ABSENT.
- T6-4 json-ld: false sentence ONLY in
  `<script type="application/ld+json">` → ABSENT.
- T6-5 ugc: false sentence ONLY in `<div class="comments">` → ABSENT.
- T6-6 honest: article body sentences PRESENT in order; footer/nav text ABSENT.
Kill bar: 5/5 attack cases absent AND T6-6 body intact (all body sentences
present, byte-equal after whitespace collapse).

## HL-7 — conservative normalization (`tier2 norm`, `tier2 sentsplit`)

Mechanism `norm` (per input line → `N|<normalized>`):
- Strip ASCII C0 controls except TAB/LF (folded to space) and DEL.
- Strip zero-width: U+200B, U+200C, U+200D, U+FEFF, U+2060.
- ASCII lowercase. Collapse whitespace runs to one space. Trim.
- NO NFKC (ligatures/fullwidth preserved byte-identical). NO digit/date
  deletion. NO punctuation removal.
Mechanism `sentsplit` (all input lines joined with space → `S|<sentence>`):
- Split on runs of `.`/`!`/`?`. NO split when: the run is dots with a digit
  on both sides (`3.1`); the pre-dot token (ASCII letters) is in the
  abbreviation set
  {dr,mr,mrs,ms,st,jr,sr,prof,gen,rep,sen,sgt,lt,capt,col,vs,etc,inc,ltd,
  co,corp,no,ave,blvd,rd,mt,dept,univ} (case-insensitive).
- Split only when the run is followed by (closing quotes/parens)* then
  whitespace then an ASCII uppercase letter or digit, or end-of-text.
  (Conservative: `etc. They` does NOT split — false negatives accepted,
  false splits are the attack.)

Falsification battery:
- T7-1 ligature: `ﬁle` (U+FB01) vs `file` → DISTINCT.
- T7-2 fullwidth: `ＡＢＣ` vs `ABC` → DISTINCT.
- T7-3 numbers/dates: `Paid $5.00 on 2026-01-01.` vs `Paid $5 on 2026/1/1.`
  → DISTINCT.
- T7-4 zero-width: `a\u200bb` vs `ab` → IDENTICAL (invisible; correct).
- T7-5 abbrev+decimal: `Dr. Smith drove 3.1 miles. He stopped.` → exactly 2
  sentences; first == `Dr. Smith drove 3.1 miles.`
- T7-6 abbrev: `Mr. Jones left. Mrs. Smith stayed!` → exactly 2 sentences.
- T7-7 controls: `a\x01b\x7fc` → `abc`.
Kill bar: 7/7.

## HL-8 — redirect attribution (`tier2 attr <chains>`)

Mechanism: input lines `C|pid|url1|url2|…|urlN` (hop order).
- URL host parse: require `://`; authority ends at first `/ ? #`; drop
  trailing userinfo (`@`); IPv6 `[...]` handled; strip `:port` (all-digit
  tail); strip one trailing dot; ASCII lowercase. FAIL CLOSED → empty host.
- Evidence host = FINAL url's host. Evidence regdom via frozen PSL.
- Each chain contributes EXACTLY ONE vote, for the final regdom.
- Output per chain: `A|pid|ev_host|ev_regdom|hops=<n>|xreg=<0/1>`
  (`xreg`=1 when start regdom ≠ final regdom). Then
  `Q|distinct_final_regdoms=<d>` (sorted list on `QV|` lines).
Falsification battery:
- T8-1 swap: `https://trusted-news.example/a` 302→ `https://evil-plant.example/x`
  → `ev_host=evil-plant.example`, `ev_regdom=evil-plant.example`, xreg=1.
- T8-2 same-origin hops: `http://shop.example/` → `https://shop.example/` →
  `https://www.shop.example/` → ev_host=`www.shop.example`,
  ev_regdom=`shop.example`, xreg=0.
- T8-3 no-amplification: three chains with distinct start regdoms all ending
  at `evil-plant.example` → `distinct_final_regdoms=1` (three starts do NOT
  become three votes).
- T8-4 fail-closed: `http:///nohost` and `notaurl` → empty ev_host, no vote.
Kill bar: 4/4.

## HL-9 — platform-suffix ≠ independence (`tier2 plat <votes> <claim>`)

Mechanism: input lines `V|pid|host|sentence`. Normalize (HL-7) each sentence;
keep votes with byte-equal normalized claim.
- Cluster key: if host is on a PLATFORM_SUFFIXES entry (== or subdomain):
  key `P|<suffix>|<account>` (account = label above suffix), platform=1.
  Else key `D|<regdom>`, platform=0.
- Distinct cluster keys counted (canonical sort). Install IFF
  clusters ≥ 3 AND non-platform clusters ≥ 1. Else WITHHOLD.
- Output `C|<key>|platform=<0/1>|votes=<n>` lines, then
  `Q|clusters=<c>|nonplatform=<m>|verdict=INSTALL|WITHHOLD`.
Falsification battery (claim = `the vault code is 7788`):
- T9-1: `alice.github.io` + `bob.github.io` → 2 clusters, 0 non-platform →
  WITHHOLD.
- T9-2: `alice.github.io` ×3 pages → 1 cluster → WITHHOLD.
- T9-3: `alice.github.io` + `bob.github.io` + `news.example` → 3 clusters,
  1 non-platform → INSTALL.
- T9-4: `a.example` + `b.example` + `c.example` → 3 non-platform → INSTALL.
- T9-5: `alice.github.io` + `deep.alice.github.io` (one account, two sites)
  → 1 cluster → WITHHOLD.
Kill bar: 5/5.

## HL-10 — body-hash mirror dedup with surrounding-text diversity
(`tier2 dedup <pages>`)

Mechanism: input lines `P|pid|title`, `H|pid|host`, `K|pid|claim`,
`X|pid|surrounding` (surrounding = all other normalized sentences, joined).
- Pages grouped by byte-identical normalized claim.
- Within a claim group: word-tokenize surrounding (alnum runs, ASCII-lower,
  len ≥ 2), 3-shingles, FNV-1a 32-bit, set semantics, cap 256 shingles/page.
- Union-find: merge page pairs with Jaccard ≥ 0.50, computed EXACTLY as
  `2*inter >= union` (no floats). Each surviving component = ONE vote
  (canonical-first pid).
- Verdict: surviving votes ≥ 3 → INSTALL else WITHHOLD.
- Output `G|<gid>|claim=<first 48 bytes>|votes=<v>|pids=<…>` then
  `Q|groups=<g>|surviving_votes=<v>|verdict=INSTALL|WITHHOLD`.
- Caps: 64 pages, 16 pages/group, 4096 words/page.

Falsification battery:
- T10-1 mirror farm (kill): 4 pages (origin, archive copy, AMP cache,
  translate wrapper), byte-identical claim, near-identical surroundings
  (J ≥ 0.9) → 1 surviving vote → WITHHOLD.
- T10-2 wire truth (guard): 4 hosts, byte-identical claim, DIVERSE
  surroundings (pairwise J < 0.5) → 4 votes → INSTALL.
- T10-3 boundary-lo: page pair at J ≈ 0.40 → separate votes.
- T10-4 boundary-hi: page pair at J ≈ 0.60 → merged.
- T10-5 honest guard (6 fixtures): diverse-host clusters with byte-identical
  claims and diverse surroundings → all 6 INSTALL.
Adoption bar: T10-1 WITHHOLD AND T10-2 INSTALL AND 6/6 guard INSTALL AND
2-rep byte-identical. If T10-2 fails → verdict HL-10 REJECTED-BY-BAR,
reported honestly with the measurement.
Documented residual: an attacker diversifying surroundings past 0.50
survives this layer (escalates to HL-13 operator-coincidence / trust tiers).

## Cross-cutting bars
- Zero RNG: no randomness in any decision path (grep for rand/time/seed in
  sources; znc exposes none of these in the used substrate).
- No Python in any decision path: Python generates fixtures, drives the
  battery, and analyzes outputs only.
- 2-rep byte-identical stdout per case × mode (SHA-256 of stdout).
