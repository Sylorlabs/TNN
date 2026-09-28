# LI BUGFIX-1 — Alternative Fixes: Structured Debate Report

**Date:** 2026-09-23. **Debate coordinator:** LI BUGFIX-1 subagent.
**Prereg:** `PREREG_LI_BF1.md` (frozen; variants V-FROZEN / V-BF1 / V-ALT1..n, §2).
**Baseline:** BUGFIX-1 = MIN-SOURCES **distinct hosts** (`H|` metadata lines, glue derives host from
URL via `urllib.parse`; gate emits `GATE|SRC_INDEPENDENCE|q1,q2`). Proven on A2 (same-host
sockpuppet pair `q1,q2|sockfarm.example`, byte-identical false claim
"hummingbirds live 40 years in the wild" → `ANSWER|UNCHECKABLE`, zero installs),
zero regressions on the 29-task WG-1 battery, byte-identical reruns.
**Residual:** A9 = two DISTINCT hosts under coordinated control still install —
host diversity cannot prove operatorship independence.

## Debate structure and tool note

Rounds were run in short single-shot calls through
`~/workspace/skills/unorouter/bin/grok46.py` (grok-4.6). `sol.py` (gpt-5.6-sol)
was tried ~15 times per the task's Sol-first instruction and **reliably failed
on generative prompts for this topic**: the API returned HTTP 200 with
`"choices": null` / 0 completion tokens for every full debate prompt (bisected
down to single paragraphs; successes only on non-generative paragraphs and one
short dedup-framed ranking). Trivial Sol prompts worked, and the same prompts
failed on retry deterministically, so this is model-side refusal/empty-output
on the topic, not a rate limit. One short Sol ranking call succeeded (below);
the substantive debate was carried by grok-4.6 with the coordinator running
adversarial and ranking rounds. All transcripts are in `debate/`.

- **R1 (proposals):** four single-shot calls, each seeded with a different
  independence-signal family → ALT1..ALT4 (`debate/r1_alt{1,2,3,4}.txt`).
- **R2 (for/against):** evasion vs false-collapse per pair (`debate/r2_robust_a.txt`,
  `debate/r2_robust_b.txt`); throughput / audit-cost / implementability ranking
  (`debate/r2_tradeoffs.txt`).
- **R3 (ranking + A9):** `debate/r3_ranking.txt`.
- **R4 (second opinion):** grok-4.6 steelmans the top pick and attacks its own
  ranking (`debate/r4_second_opinion.txt`); Sol's short ranking
  (`debate/sol_attempt.txt`): ALT3 > ALT1 > ALT4 > ALT2.

## The four alternatives (one-line mechanisms)

- **V-ALT1 — context-window hash:** two supporting pages count as independent
  iff the SHA-256 of the text around the matched sentence differs; verbatim
  copies collapse to one vote.
- **V-ALT2 — temporal separation:** two supporting pages count as independent
  iff their first-seen timestamps differ by ≥24 h; lockstep appearance collapses
  to one vote.
- **V-ALT3 — provenance-DAG disjointness:** two supporting pages count as
  independent iff their outlink/citation ancestor sets are disjoint.
- **V-ALT4 — metadata quorum:** four binary metadata signals (distinct bylines,
  share platforms, publisher strings, CMS values); the cluster installs iff ≥2
  signals hold.

## Implementation specs (pure Zag, zero RNG, deterministic)

Shared conventions: each variant is a **copy** of canonical
`knowledge/web_guides/webg.zag` under `knowledge/web_guides/live_ingest/variants/`
(canonical never modified, per prereg §6). Gates sit at the cluster-accept point
(the `wn2>=minsrc` branch, cf. `diag/webg_fix.zag` ~line 1280). New metadata
lines follow the `H|` pattern (glue emits facts only; all decisions in Zag).
Empty/absent metadata never counts against honest legacy pages (backward
compat). All string compares byte-exact via existing `nio_equal` helpers.

### V-ALT1 — context-window hash (`GATE|SRC_CTXDUP|<pids>`)

- **Metadata:** none. Works on the existing `S|` sentence stream.
- **Data structures:** reuse the sentence store (`st`/`nst`). For each page in
  the winning cluster, locate the byte-offset of the matched key sentence
  (scan the page's sentences for byte-equality with `key`), then take the
  immediately preceding and following sentences (by store order) as the
  context. Context bytes = `prev + 0x1F + next`. If the page has no neighbor
  sentence (single-sentence page), use the sentence itself as context — this
  guarantees single-sentence pages never falsely collapse.
- **Gate logic:** new fn `ctx_hash_distinct(widx,wn,st,nst)`: SHA-256 (via
  `substrate/R33_NATIVE_SHA256_V2.zag`, already imported by `cl/common.zag`)
  of each supporter's context bytes; count distinct digests with the same
  pairwise `nio_equal` pattern as `nsrc_count` in `diag/webg_fix.zag`.
  Accept iff distinct ≥ MIN-SOURCES; else print `ANSWER|UNCHECKABLE`,
  then `GATE|SRC_CTXDUP|` + the supporter pid CSV (same `print_pids_csv`
  helper), then the existing `UNCHECKED|` tail.
- **Determinism:** SHA-256 over bytes, no RNG, no time reads in Zag. Two reruns
  byte-identical.
- **Audit cost:** one SHA-256 per supporter page (≤ cluster size), plus one
  gate line only when the gate fires.
- **A2 predicted:** q1,q2 are byte-identical pages → identical neighbors →
  identical hashes → collapse to 1 < 2 → gate fires, no install. **PASS.**
- **A9 predicted:** A9-as-constructed (byte-identical false claim text on two
  distinct hosts, same surrounding text) → identical context hashes → collapse
  → gate fires, **caught**. A9-adaptive (operator edits surrounding sentences)
  → hashes differ → **evades**; only defense is that the edit is itself
  observable in the log.
- **Throughput risk:** over-withholds when honest pages quote the same
  paragraph verbatim (e.g. press-release quotes) — context matches, collapse.
  Bounded: only exact (prev,next) neighbor equality collapses.

### V-ALT2 — temporal separation (`GATE|SRC_TIMELOCK|<pids>`)

- **Metadata:** `T|<unix_epoch_seconds>` per page (glue: HTTP `Last-Modified`,
  `<time>`/meta publication date, else fetch time — formatting only). Absent
  `T|` → page counts as its own source (legacy-safe).
- **Data structures:** new parallel table `tt` (8-byte i64 entries per page,
  indexed by page id, same pattern as `ht` for hosts) filled in `parse_pages`.
- **Gate logic:** new fn `time_distinct(widx,wn,tt)`: sort supporter timestamps
  (insertion sort over ≤ cluster size; deterministic); collapse any pair with
  |Δt| < 86400 s into one vote (transitive collapse); count votes. Accept iff
  votes ≥ MIN-SOURCES; else `ANSWER|UNCHECKABLE` + `GATE|SRC_TIMELOCK|` + pid
  CSV + `UNCHECKED|` tail. Note: pages sharing one `T|` line value from a
  shared crawl timestamp collapse by construction.
- **Determinism:** integer arithmetic on i64 epochs; no RNG.
- **Audit cost:** one i64 compare per pair; one gate line on fire.
- **A2 predicted:** q1,q2 fetched in the same crawl → |Δt| ≈ 0 → collapse →
  gate fires. **PASS.**
- **A9 predicted:** operator staggers publication >24 h → **evades** trivially.
  Honest news-wire bursts (scheduled releases) over-withheld. Weakest
  mechanism; both models ranked it last/near-last.

### V-ALT3 — provenance-DAG disjointness (`GATE|SRC_CITE_SHARED|<pids>`)

- **Metadata:** `L|<url>` lines per page (every outlink/citation URL, one per
  line; glue extracts from `<a href>` — facts only). Pages with no `L|` lines
  count as their own source (legacy-safe).
- **Data structures:** per-page outlink URL sets: arena `la` (bytes) + table
  `lt` (per page: list of (offset,len) entries), built in `parse_pages` with
  the same arena/table idiom as `ht`. Cap: first 32 outlinks per page
  (documented; beyond-cap URLs ignored with no diagnostic — a known bound).
- **Gate logic:** new fn `cite_disjoint(widx,wn,la,lt)`: pairwise byte-exact
  URL equality across supporter pages; any shared URL merges the two pages
  into one component (union over pairs); count components. Accept iff
  components ≥ MIN-SOURCES; else `ANSWER|UNCHECKABLE` +
  `GATE|SRC_CITE_SHARED|` + pid CSV + `UNCHECKED|` tail.
  **Scope note:** the debated version was full transitive DAG reachability;
  the implementable version is **1-hop** (direct outlink sets). Transitive
  reachability is not implementable from `pages.txt` alone (targets are not
  crawled), and is recorded here as a documented reduction, not a silent one.
- **Determinism:** byte compares only; no RNG.
- **Audit cost:** URL-set compares per supporter pair; bounded by the 32-cap.
- **A2 predicted:** q1,q2 share the same outlinks → merge → gate fires. **PASS.**
- **A9 predicted:** A9 pair citing disjoint domains → **evades**; A9 pair
  sharing a citation → caught. Honest pages citing the same major outlet
  over-withheld; uncited pages bypass the gate entirely (the dominant case in
  the current corpus — most pages carry no citations).

### V-ALT4 — metadata quorum (`GATE|SRC_QUORUM|<pids>`)

- **Metadata:** `A|<author>` (byline), `SH|<platform>` (social-share plugin
  target), `PB|<publisher>` (meta publisher), `CG|<generator>` (meta
  generator/CMS). All glue-extracted facts. Missing field → empty string.
- **Data structures:** four parallel string tables (arena + per-page
  (offset,len), same idiom as `ht`), filled in `parse_pages`.
- **Gate logic:** new fn `quorum_score(widx,wn,...)`: four binary signals over
  the supporter set — S1: ≥2 distinct non-empty authors; S2: ≥2 distinct
  non-empty share platforms; S3: ≥2 distinct non-empty publishers; S4: ≥2
  distinct non-empty CMS values. Score = Σ Si. Accept iff score ≥ 2; else
  `ANSWER|UNCHECKABLE` + `GATE|SRC_QUORUM|` + pid CSV + `UNCHECKED|` tail.
  Empty strings never form a "distinct" value (two empty bylines do not
  satisfy S1).
- **Determinism:** byte compares; no RNG.
- **Audit cost:** trivial (string compares on metadata).
- **A2 predicted:** q1,q2 share author/publisher/platform → score 0 → gate.
  **PASS.**
- **A9 predicted:** operator varies bylines/platforms → score ≥ 2 →
  **evades** trivially. Honest low-metadata pages over-withheld (all signals
  false → score 0).

## Debate verdicts

**Ranking (coordinator, combining R2–R4 and both models):**

1. **ALT1 (context hash)** — the only alternative that catches the A9 case
   *as constructed* (byte-identical false claim across distinct hosts) while
   needing **zero new metadata** and running fully inside existing byte
   infrastructure (SHA-256 already in the substrate). Both models ranked it
   #2 structurally; it is #1 on implementability and A9-relevance.
2. **ALT3 (provenance disjointness)** — strongest in principle (both models
   #1 structurally: "hard to fake without graph-level coordination"), weakest
   in practice for this pipeline: outlink metadata does not exist yet, most
   pages are uncited (bypass), and the implementable 1-hop version is a shadow
   of the debated DAG version.
3. **ALT2 (temporal separation)** — cheap and deterministic, but evaded by
   scheduling and over-withholds honest news bursts; both models rank it
   last/near-last.
4. **ALT4 (metadata quorum)** — trivially gamed, metadata mostly absent;
   useful at most as a soft signal, not a gate.

**Does any alternative address the A9 residual?** Partially: **ALT1 catches
A9-as-constructed** (identical claim text on two distinct hosts) at the cost of
context fragility — an adaptive operator who edits surrounding sentences
evades it, and honest verbatim-quote pages can over-withhold. ALT3 in its full
transitive form would raise the bar highest against adaptive operators
(requiring disjoint citation lineages), but it is not implementable from
available metadata and is evaded by uncited pages. **No alternative closes A9
against an adaptive operator**; that remains an honest residual, same as in
BUGFIXES.md.

**Recommendation to the variant builders (prereg §2, V-ALT1..n):** build ALT1
first — highest information per implementation cost — and consider the layered
variant **V-BF1+ALT1** (distinct hosts AND distinct context hashes, either gate
firing → UNCHECKABLE): it closes A2 at the host layer and A9-as-constructed
at the content layer, with backward-compat preserved on legacy inputs (pages
without neighbors use the sentence itself; pages without `H|` keep BUGFIX-1's
legacy rule). Prereg §5 verdict rules apply unchanged: winner = closes BF1-K1
with zero BF1-K2 regressions; INTEGRITY-FAIL if any variant installs a
known-false claim outside the A9 residual class.

## Debate record

- `debate/r1_prompt*.txt` — round prompts (r1_prompt2.txt is the canonical R1
  text; r1_prompt3/4.txt are reframings attempted after Sol failures).
- `debate/r1_alt1.txt` … `debate/r1_alt4.txt` — the four proposals.
- `debate/r2_robust_a.txt`, `debate/r2_robust_b.txt` — evasion vs
  false-collapse analysis per alternative.
- `debate/r2_tradeoffs.txt` — throughput / audit-cost / implementability.
- `debate/r3_ranking.txt` — final ranking + A9 residual question.
- `debate/r4_second_opinion.txt` — grok-4.6 steelman of ALT3 + attack on the
  ranking.
- `debate/sol_attempt.txt` — the one successful Sol output (short ranking:
  ALT3 > ALT1 > ALT4 > ALT2).
- `debate/probe.txt`, `debate/half.txt` — diagnostic probes of the Sol
  empty-output failure (kept as evidence of the failure mode).
