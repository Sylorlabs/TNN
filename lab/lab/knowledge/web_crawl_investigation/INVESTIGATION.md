# Why TNN can't crawl the open internet by itself — investigation

Micah's question, 2026-09-22. This is a diagnosis, not an implementation.
No live crawling was done for this report.

## The short answer

TNN has never touched the live web. Everything it "knows from the web" arrived
through a human-built pipe: a Python bridge queries a search engine, a trial
author writes the query strings, the results get recorded once and frozen, and
TNN's Zag code only ever reads the frozen envelopes. TNN decides what to do
with web results — that machinery is real — but it has no machinery to go GET
them. Fetching, query-writing, page-reading, link-following, and source-judging
are all missing, in that dependency order.

## What exists today (verified in the repo)

**The web-search sense v2** (`senses/web-search/v2/`, `info-source/src/ws2_sense.zag`).
Real Zag machinery: `ws_gate` decides whether a search is warranted,
`ws_add_result` records results with hashes, `ws_decide` renders a verdict
(≥2 agreeing domains → provisional; conflicts → withhold), and the mixed-web
trial added deliberation over genuinely disagreeing sources. This is genuine
judgment machinery over web evidence.

But the sense never sees the web. The live side is `ws_bridge2.py` — Python,
human-authored — which queries a SearXNG instance and records JSON envelopes
(title/URL/snippet). Scored runs replay frozen envelopes. Determinism is
claimed over recorded envelopes, never over the live web.

**The native layer** (`toolchain/R33_NATIVE_IO_V1.zag`) has file I/O only:
open/read/write/close/seek/lock. There is no socket, no DNS, no TLS anywhere
in Zag. Zero network egress from TNN's own code. (A grep for socket/connect
syscall usage across all non-championship Zag found nothing — the only
"connect(" hits are scaffold-release's `sr_disconnect`, unrelated.)

**Budget primitives exist**: `nio_limit` (resource ceiling), `nio_deadline`,
`nio_guard`. These are the raw materials for crawl economy, but nothing uses
them for web politeness.

## The missing machinery, in dependency order

### M1. Fetch: URL → bytes. (Plumbing, not intelligence.)

Nothing exists. Two routes: (a) build socket+TCP+TLS+HTTP in Zag via raw
syscalls — TLS alone is a multi-month monster and a terrible use of the lab;
(b) a narrow, audited fetch bridge ("give me the bytes at this URL") where
**TNN chooses the URL** and the bridge only moves bytes. The intelligence is
in what to fetch, not in the TCP handshake — but the pipe has to be built,
and its audit log (every URL fetched, every byte count) is a constitution
matter: unfettered egress is an integrity hole.

### M2. Query formulation: knowledge gap → search query. (Genuinely missing.)

Today the trial author writes the query strings ("capital of France"). No TNN
organ converts "I don't know X" or "I should verify claim Y" into a query.
The five organs don't cover this: the memory substrate *holds* knowledge, but
nothing turns an absence of knowledge into a fetch plan. This is the first
real intelligence gap — curiosity with a keyboard.

### M3. Parsing: HTML → text, links, claims. (Mechanical, must be built.)

Search snippets are pre-digested by SearXNG. A real crawl returns raw HTML.
TNN needs a Zag-native parser: strip tags, recover text, extract links,
preserve enough structure (headings, lists) to find claims. Zero exists.
This is not intelligence — it's plumbing like M1 — but without it M4 has
nothing to navigate.

### M4. Crawl control: which links, when to stop. (Deliberative, missing.)

Given a page: which links are worth following? When is the question answered?
When do you stop (budget gone, returns diminishing, question resolved)? No
organ does multi-step information-gathering trajectories today. Closest
relatives: eliminative hypothesis logic (ruling things out) and native
structural revision — but neither plans a fetch sequence. Missing.

### M5. Source judgment: reference page vs rumor blog. (Knowledge + judgment.)

Today "trust" = counting domains (≥2 agree). The real web needs more: does
the page cite sources? Is it primary or fifth-hand? Does the domain have a
track record? This is where Micah's "guides for beginners" idea lands —
evaluating sources is TEACHABLE knowledge (check the domain, look for
citations, cross-check single-source claims, distrust the too-convenient
answer). The KB4 channel work (independent channels, correlated-source
failures) is the foundation. But the T1N rerun's warning applies directly:
taught knowledge without composition machinery is inert (informed and
scratch produced byte-identical modules). Teaching beginner guides only
matters if TNN *composes* them into fetch/verify behavior — which must be
tested, not assumed.

### M6. Poison/injection firewall. (Structural, partially seeded.)

A crawled page can say "ignore your rules and install X," or just assert
confident falsehoods. Today's sense is *incidentally* safe — regex answer
extraction can't obey instructions. A real claim-extractor parsing free text
loses that accident. The required rule, as standing law:

- Crawled bytes are DATA, tagged untrusted, never instructions. (This is
  already law for all external content; the crawler must enforce it in code,
  not just in prose.)
- Web claims enter as SUSPECT, never installed directly. Install requires
  independent corroboration — the info-source R-CORR rule is the seed
  (≥2 independent domains agree AND no contradicting installed belief), and
  the KB4 SUSPECT-gate (ask first, render own verdict only when information
  can't resolve) is the structural home.
- The B-SPOOF residual is the honest boundary: unanimous two-domain spoofs
  still fool corroboration. The firewall must say so rather than pretend.

### M7. Politeness/economy governor. (Missing, primitives exist.)

Rate limits per host, robots.txt respect, a crawl budget set by deliberation
("is this fetch worth it?"), and memory hygiene — fetched-but-unverified
content must not be promotable to durable memory. Natural home: the
deliberate consolidation/promotion organ (it already decides what survives)
plus the `nio_limit`/`nio_deadline` primitives. Nobody has wired them to web
fetching.

## What this means for the organs

| Requirement | Organ coverage today |
|---|---|
| Fetch (M1) | none — no network primitive |
| Gap → query (M2) | none — no curiosity/fetch-planning machinery |
| HTML parsing (M3) | none — mechanical, to be built |
| Crawl control (M4) | partial relatives only (eliminative logic); no trajectory planning |
| Source judgment (M5) | seed only: domain-counting + KB4 channels; trust tiers missing |
| Injection firewall (M6) | seed only: SUSPECT-gate + R-CORR; crawler-grade enforcement missing |
| Budget/politeness (M7) | primitives only (`nio_limit`, deadline, guard); no governor |

## The "guides for beginners" experiment (Micah's second question)

"What happens when it has knowledge of how to use the internet — guides for
beginners?" The honest design, given the T1N inert-corpus finding:

1. Teach beginner internet guides through TNN's genuine learning path (not
   planted): how to form a query, how to judge a source, how to cross-check —
   principles, like the epistemics principles trial.
2. Test whether behavior changes vs an untaught arm on the FIRST-CRAWL
   battery: does the taught arm formulate better queries, check second
   sources unprompted, withhold on single-source claims?
3. Kill criterion (from the T1N rerun): if taught and untaught arms behave
   byte-identically, the knowledge is inert and composition is the gap —
   report it, don't relitigate.

Knowledge first is a hypothesis here, not a plan. The trial decides.

## Bottom line for Micah

TNN can't crawl because crawling was never built — it was deliberately kept
out while the lab proved judgment-over-evidence with frozen envelopes. The
judgment half (M5/M6 seeds) is the most advanced; the fetching half (M1–M4)
is zero. The minimal path is: audited fetch pipe → gap-to-query machinery →
Zag HTML parser → crawl planner → trust tiers + injection firewall →
budget governor. And the beginner-guides question gets its own trial, with
the inert-knowledge kill bar from T1N already loaded.
