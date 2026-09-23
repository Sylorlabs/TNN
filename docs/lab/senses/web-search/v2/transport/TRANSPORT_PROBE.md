# TRANSPORT PROBE — live web-search backends from the lab VM
**Date:** 2026-09-21/22 (probe runs 2026-09-22 ~01:50–02:01 UTC / 2026-09-21 ~18:50–19:01 PDT)
**Purpose:** find a REAL live search backend for the TNN web-search sense v2
(replacement for v1's frozen fixtures; see `~/workspace/senses-websearch/evidence/transport_failure.md`).
**Method:** curl + Python urllib with a Chrome User-Agent, 10 diverse factual queries,
bar = **≥8/10 queries with ≥3 usable results each** (title + url + snippet, non-empty, real domains).
**No API keys used anywhere.** Raw machine data: `probe_results.json` (first battery, contains a probe-script bug in the `usable` flag — see notes), `reprobe_results.json` (fixed re-probe).

## Test queries
1. capital of France
2. boiling point of water at sea level
3. tallest building in the world 2026
4. who wrote Pride and Prejudice
5. chemical symbol for gold
6. when was the Eiffel Tower built
7. largest planet in the solar system
8. speed of light in vacuum
9. author of the novel 1984
10. first person to walk on the moon

## Results summary

| Endpoint | URL pattern | Score | Latency | Verdict |
|---|---|---|---|---|
| **SearXNG search.lumy.live** | `https://search.lumy.live/search?q=<q>&format=json&language=en-US` | **10/10** | 2.5–13.6 s | ✅ **WORKS — primary** |
| Wikipedia Action API | `https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=<q>&format=json&srlimit=20` | **10/10** | ~1.4 s avg | ✅ works, but **encyclopedia-only — supplementary, not general web search** |
| DuckDuckGo HTML | `https://html.duckduckgo.com/html/?q=<q>` | 7/10 then 5/10 | ~1.1–1.6 s | ⚠️ flaky (HTTP 202 bot interstitials) — fallback only |
| DuckDuckGo Lite | `https://lite.duckduckgo.com/lite/?q=<q>` | 5/10 | ~0.9 s | ⚠️ flaky (same 202 interstitials) — fallback only |
| searx.be | `…/search?q=<q>&format=json` | 0/10 | — | ❌ anti-bot captcha page ("Verifying your browser…") |
| search.inetol.net | same | 0/10 | — | ❌ "Security check - Substation" bot wall |
| baresearch.org | same | 0/10 | — | ❌ "Making sure you're not a bot!" page |
| searx.tiekoetter.com | same | 0/10 | — | ❌ HTTP 429 Too Many Requests |
| search.rhscz.eu | same | 0/10 | — | ❌ HTTP 429 |
| etsi.me / opnxng.com / priv.au / searx.dresden.network / search.pereira.is / search.femboy.ad / searx.linxx.net / search.yuri.llc / search.hbubli.cc / failsearx.culturanerd.it | same | 0/10 | — | ❌ HTTP 429 or bot walls |
| search.sapti.me / searx.oakleycord.dev / search.bus-hit.me | same | 0/10 | — | ❌ remote end closed connection without response |
| searxng.website | same | 0/10 | — | ❌ HTTP 403 |
| search.leptons.xyz | same | 0/10 | — | ❌ HTTP 502 Bad Gateway |
| Mojeek | `https://www.mojeek.com/search?q=<q>` | 0/10 | — | ❌ HTTP 403: "your network appears to be sending automated queries" |
| Marginalia | `https://search.marginalia.nu/search?query=<q>` | 0/10 | — | ❌ "Wait A Moment — aggressive bot activity" throttle page |
| Startpage | `https://www.startpage.com/sp/search?query=<q>` | 0/10 | — | ❌ Anubis JS proof-of-work challenge |

Notes:
- `https://searx.space/data/instances.json` fetched fine (94 instances, searx.space itself reachable);
  per-instance fields confirm most instances' working engines are duckduckgo/bing/yandex — the VM's IP is
  broadly rate-limited (429) across the instance fleet, likely from the probing burst plus general IP reputation.
- DDG's 202 interstitial is intermittent: the same endpoint serves real results ~50–70% of requests and a
  14 KB bot-check shell the rest of the time. It passed 7/10 once and 5/10 twice — below the bar.
- The first battery (`probe_results.json`) had a script bug (`usable >= 3` list-vs-int comparison) that marked
  every query failed; per-query HTTP statuses/body sizes/failure modes in it are still valid evidence.

## Per-query detail — search.lumy.live (primary, 10/10)

| Query | Usable results | Latency |
|---|---|---|
| capital of France | 116 | 13.58 s |
| boiling point of water at sea level | 59 | 2.60 s |
| tallest building in the world 2026 | 55 | 13.44 s |
| who wrote Pride and Prejudice | 65 | 2.58 s |
| chemical symbol for gold | 45 | 2.86 s |
| when was the Eiffel Tower built | 39 | 13.58 s |
| largest planet in the solar system | 99 | 2.54 s |
| speed of light in vacuum | 119 | 2.73 s |
| author of the novel 1984 | 93 | 13.56 s |
| first person to walk on the moon | 108 | 2.76 s |

Latency pattern: alternating ~2.6 s and ~13.5 s — looks like instance-side throttling pauses roughly every
third request. Slow but reliable; every query returned dozens of real results (wikipedia.org, britannica.com,
skyscrapercenter.com, etc.).

## Per-query detail — DuckDuckGo HTML (flaky fallback, 5–7/10)

| Query | Result | Note |
|---|---|---|
| capital of France | ✅ 10 results | HTTP 200, 33.6 KB |
| boiling point of water at sea level | ✅ 10 results | HTTP 200 |
| tallest building in the world 2026 | ✅ 10 results | HTTP 200 |
| who wrote Pride and Prejudice | ✅ 10 results | HTTP 200 |
| chemical symbol for gold | ❌ | HTTP 202 interstitial, 14.2 KB shell |
| when was the Eiffel Tower built | ✅ 10 results | HTTP 200 |
| largest planet in the solar system | ✅ 10 results | HTTP 200 |
| speed of light in vacuum | ❌ | HTTP 202 interstitial |
| author of the novel 1984 | ❌ | HTTP 202 interstitial |
| first person to walk on the moon | ✅ 10 results | HTTP 200 |

DuckDuckGo Lite behaves the same way (3/10 HTTP 200 pages parsed fine after a parser attribute-order fix;
the rest are 202 interstitials).

## Per-query detail — Wikipedia Action API (supplementary, 10/10)

All 10 queries returned 20 parsed hits each, avg latency 1.42 s. Example: "capital of France" →
"List of capitals of France", "Paris", … with `curid` URLs and searchmatch snippets.
**Explicitly NOT general web search** — it only searches en.wikipedia.org. Wired as a marked-supplementary
fallback (`"supplementary": true` in the envelope) so no downstream consumer mistakes it for web results.

## Final recommendation

**VERDICT: WORKS.** One reliable primary backend found:
- **Primary:** `search.lumy.live` SearXNG JSON API — 10/10, real web results, no key, JSON (not HTML scraping).
- **Fallback chain (wired into `ws_bridge2.py`, `--backend auto`):**
  `lumy → ddg_html → ddg_lite → wikipedia(supplementary)`.
  The bridge tries each in order and emits whichever backend served in the envelope (`"backend"` field,
  plus `"fallbacks_skipped"` when earlier backends failed and `"supplementary": true` for Wikipedia).

Caveats for the v2 sense:
1. lumy.live is a single volunteer-run public instance — it can rate-limit, disable JSON, or go down.
   The searx.space fleet is mostly 429/hostile to this VM's IP, so a replacement instance may need fresh probing.
2. lumy latency is high and spiky (2.5–14 s); budget timeouts accordingly (bridge uses 30 s).
3. DDG endpoints are intermittent (~50–70% success) — fine as fallbacks, not as primaries.
4. Wikipedia must never be presented as web search; the envelope marks it supplementary.

## Deliverables (this directory)
- `TRANSPORT_PROBE.md` — this file
- `ws_bridge2.py` — thin transport-only bridge (`--backend lumy|ddg_html|ddg_lite|wikipedia|auto`);
  same provenance envelope as ws_bridge.py (query, retrieved_at wall-clock Python-side only,
  results[] rank/title/snippet/url/domain/result_hash=sha256(url+"\n"+title+"\n"+snippet)); `--backend auto` fallback chain
- `LIVE_SMOKE.json` — one real end-to-end query ("tallest building in the world 2026") through the bridge
  via `auto` → served by `lumy`, 6 results, hash fields verified by recomputation
- `probe_backends.py` / `reprobe.py` / `probe_results.json` / `reprobe_results.json` — probe tooling + raw data
