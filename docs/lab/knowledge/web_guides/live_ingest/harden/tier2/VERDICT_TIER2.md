# LI-HARDEN Tier 2 — Build + Battery Verdict (Crew T2-BUILD)

Date: 2026-09-24. Branch: `tnn-native-lab`.
Toolchain: pinned `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Binary SHA256: `c0d850cfe6b9aab2c9352b688f11a029f8f4ee41a7fb71b8b6e33f43fb82188a`
(source: `tier2.zag`, 1360 lines, pure Zag; Python used only for fixture
generation, battery driving, and analysis — no Python in any decision path).

Frozen prereg: `knowledge/web_guides/live_ingest/harden/tier2/PREREG_TIER2.md`
(committed `1bda25b0db021162d40304b9150d444b8fd48ad2` BEFORE any mechanism
code was written). The prereg was not amended after freezing. Four extra
probe cases (T6-7, T8-5, T9-6, T10-6) were added during testing as clearly
labeled extensions; outcomes are reported against the frozen mechanism.

## 1. Mechanism designs (all in `tier2.zag`, modes via argv[1])

- **HL-6 `extract`**: single-pass HTML tokenizer. Drops `script/style/noscript/
  template/iframe/object/embed/head` subtrees, HTML comments, `<!…>`, `<?…?>`,
  structural chrome (`footer/nav/aside`), and elements with `hidden`,
  `aria-hidden="true"`, `display:none`/`visibility:hidden` styles, `class`/`id`
  containing `comment`/`sidebar`/`widget`, `role` in {navigation,
  complementary, contentinfo, banner}. Block tags flush `T|` lines;
  entities (`amp/lt/gt/quot/apos/nbsp`, `&#DDD;`/`&#xHH;` BMP) decoded.
- **HL-7 `norm`**: strip ASCII C0 controls (except TAB/LF→space) and DEL;
  strip U+200B/C/D, U+FEFF, U+2060; ASCII lowercase; collapse whitespace.
  No NFKC, no digit/date deletion, no punctuation removal. **`sentsplit`**:
  split on `.`/`!`/`?` runs; no split on digit-bracketed dots (`3.1`) or the
  pinned 27-word abbreviation set; split only before (quotes/parens)* +
  whitespace + uppercase/digit/end.
- **HL-8 `attr`**: input `C|pid|url1|…|urlN`. Host parse requires `://`,
  strips userinfo/port/trailing-dot, lowercases, FAILS CLOSED. Evidence =
  FINAL url host + regdom (frozen `psl_frozen.txt` embedded byte-identical).
  Each chain = exactly one vote for the final regdom. Emits `xreg` flag.
- **HL-9 `plat`**: input `V|pid|host|sentence` + claim arg. Votes kept on
  byte-equal HL-7-normalized claim. Cluster key: `P|<suffix>|<account>` for
  the pinned 16-entry platform list (account = label above suffix),
  `D|<regdom>` otherwise. Install iff ≥3 distinct clusters AND ≥1
  non-platform cluster.
- **HL-10 `dedup`**: input `P/H/K/X` lines (claim + surrounding text per
  page). Pages grouped by byte-identical normalized claim; within a group,
  union-find merges page pairs with surrounding-text Jaccard ≥ 0.50 —
  word 3-shingles, FNV-1a 32-bit, set semantics, cap 256, computed EXACTLY
  as `2*inter >= union` (no floats). Each surviving component = one vote.
  Verdict: surviving votes ≥ 3 → INSTALL else WITHHOLD. This is the new
  design the draft asked for: wire-truth (diverse surroundings) keeps its
  votes; mirror farms (near-identical surroundings) collapse.

## 2. Battery results

34 cases (30 frozen + 4 labeled extensions), 63 checks, 2 reps each.
**63/63 checks PASS, 0 failures. 34/34 case×mode pairs byte-identical
across reps** (SHA-256 of stdout). Zero RNG in any decision path.

| HL | frozen cases | result |
|---|---|---|
| HL-6 | T6-1..T6-5 (footer, aria-hidden, comment, JSON-LD, UGC) | 5/5 attack channels absent, body intact |
| HL-6 | T6-6 honest | body present, footer/nav absent |
| HL-7 | T7-1 ligature, T7-2 fullwidth, T7-3 numbers/dates | 3/3 stay distinct |
| HL-7 | T7-4 zero-width | identical (invisible — correct) |
| HL-7 | T7-5/T7-6 abbrev+decimal | no split on `Dr.`/`Mr.`/`Mrs.`/`3.1` |
| HL-7 | T7-7 controls | stripped |
| HL-8 | T8-1 swap | attributed to attacker origin, xreg=1 |
| HL-8 | T8-2 same-origin hops | origin kept, xreg=0 |
| HL-8 | T8-3 three starts → one attacker | distinct_final_regdoms=1 |
| HL-8 | T8-4 unparseable | fail closed, 0 votes |
| HL-9 | T9-1 two platform accounts | WITHHOLD (2 clusters, 0 non-platform) |
| HL-9 | T9-2 one account ×3 pages | WITHHOLD (1 cluster) |
| HL-9 | T9-3 2 platform + news.example | INSTALL |
| HL-9 | T9-4 three plain regdoms | INSTALL |
| HL-9 | T9-5 one account, two sites | WITHHOLD (1 cluster) |
| HL-10 | T10-1 mirror farm (J=1.0) | 1 vote → WITHHOLD |
| HL-10 | T10-1b near-dup farm (J 0.65–0.81) | 1 vote → WITHHOLD (union-find transitivity) |
| HL-10 | T10-2 wire truth, diverse surroundings | 4 votes → INSTALL |
| HL-10 | T10-3 J≈0.37 / T10-4 J≈0.54 | separate / merged (threshold behaves) |
| HL-10 | T10-5 guards 1–6 | 6/6 INSTALL, 3 votes each |

Extensions: T6-7 (nested `display:none`, unquoted `aria-hidden=true`,
uppercase `<FOOTER>`, `user-comments` class, entity spacing) PASS;
T8-5 (userinfo/port/trailing-dot/uppercase) PASS; T9-6 (`notgithub.io`,
`evilgithub.io` lookalikes NOT treated as platform) PASS.

## 3. HL-10 adoption-bar assessment — ADOPTED (bar met)

The draft's adoption bar: T10-1 WITHHOLD **and** T10-2 INSTALL **and** 6/6
guard INSTALL **and** 2-rep byte-identical. **All four hold.** The
surrounding-text-diversity design separates the two cases the old
byte-identical-body rule could not:
- Mirror farm (origin + archive + AMP + translate, byte-identical bodies):
  pairwise J=1.0 → one component → 1 vote → WITHHOLD. Killed.
- Wire truth (4 hosts, byte-identical claim sentence, genuinely different
  surrounding articles): pairwise J=0.0 → 4 components → 4 votes → INSTALL.
  The H8 regression that killed `verdictm` under the zero-regression bar
  does not occur here.
- Boundary probes confirm the 0.50 threshold behaves as pinned (J≈0.37
  separate, J≈0.54 merged).

**Documented residual (measured, not hypothesized):** T10-6 — an attacker
who rewrites surroundings past J<0.5 while keeping the claim byte-identical
survives with 4 votes → INSTALL. This is the expected escalation and the
reason HL-13 (operator-coincidence provenance) exists as the next layer.
Also: pages with EMPTY surroundings merge (J defined as 1.0 on 0/0) —
documented, conservative toward WITHHOLD.

## 4. Bugs found by the battery and fixed (all in `tier2.zag`)

1. **Vote-count +1 (plat):** the "found existing cluster" increment fired
   for newly added clusters too (f==nc evaluated after nc++). Fixed with a
   saved pre-add count.
2. **Arena clobber (dedup):** claim/surrounding arena ends were derived
   from the last page's entry, so a later page's X line overwrote an
   earlier page's region (all shingle sets read identical bytes → false
   merges). Fixed with bump pointers.
3. **Scratch aliasing (attr):** `regdom(he,sc)` clobbered `hf` (a slice of
   the same buffer), corrupting the xreg comparison (single-hop chains
   wrongly flagged xreg=1). Fixed with four separate scratch buffers.
4. **Entity spacing (extract):** `&lt;` after a space glued words
   (`two &lt;` → `two<`). Pending space now flushed before entity decode.

## 5. Honest limitations

- HL-6 drop lists are heuristic (`comment`/`sidebar`/`widget` class
  substrings, `footer/nav/aside` tags): a site putting article text in
  `<div class="commentary">` would lose it; `header` is NOT dropped (may
  keep site chrome). Documented, not silent.
- HL-7 `etc.` + uppercase does not split (conservative false negative,
  preregistered).
- HL-8 PSL is the frozen principled approximation (no private-section
  entries beyond the platform list; no wildcard/exception rules).
- HL-9 platform list is 16 pinned suffixes; new free-host platforms need
  a list update (data change, not mechanism change).
- HL-10 threshold 0.50 is pinned; the T10-6 diversification escape is the
  known residual (→ HL-13 / trust tiers).

## 6. Evidence and reproduction

- Source: `tier2.zag` (pure Zag) + pinned-toolchain binary (SHA256 above).
- Battery: `gen_fixtures.py`, `run_battery.py`; 34 fixtures;
  `battery_out/battery_summary.tsv` (63 checks) + per-case `.out` logs.
- Evidence committed under
  `knowledge/web_guides/live_ingest/harden/tier2/` (source, IO substrate
  copy, prereg, fixtures, drivers, summary TSV, per-case outputs, this
  report). Build binary `tier2_bin`, `.zagd` markers and `.zag-cache/`
  are NOT committed.
- Reproduce: `python3 gen_fixtures.py && python3 run_battery.py`
  (expects `63/63 checks PASS, 0 failures`).
