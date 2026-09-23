# Transport failure path — live search backend (2026-09-21)

At 2026-09-21 22:46:09Z, direct DuckDuckGo HTML and Lite requests from this VM
returned HTTP content but only empty/bot-filtered shells — no usable results.

`ws_bridge.py` implements the thin transport (query → results + provenance) with:
- registrable-domain derivation,
- `result_hash = sha256(url + "\n" + title + "\n" + snippet)`,
- transport provenance envelopes (the ONLY place wall-clock timestamps may appear).

Because the live backend was unusable, the scored legs run against frozen,
recorded real-search fixtures (`fixtures/real_search.json`, observed 2026-09-21
via the public search path; every record carries exact URL, title, snippet,
domain, observed date, and a recomputed hash). The bridge remains the documented
transport for a future live backend; the Zag sense only ever consumes the frozen
fixture records, so the determinism claim is unaffected.

Decision recorded pre-score: live-transport failure does not block the frozen
legs; it is documented here instead of worked around with an unvetted backend.
