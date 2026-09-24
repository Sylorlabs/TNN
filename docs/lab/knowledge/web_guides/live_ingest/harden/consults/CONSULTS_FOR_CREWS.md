# Model consults — novel attacks for crew red-teaming (2026-09-24)

Sources: grok-4.7 (20 attacks, 15 guidelines G1-G15) + claude-fable-5.1 (10 attacks, 8 guidelines G1-G8). sol unreachable (4 attempts, provider choices:null). Full texts: ~/workspace/liharden/consults/short_grok-4.7.txt and short_claude-fable-5.1.txt.

## For Crew A (glue layer)
1. Parser split: fetcher vs host-key using different URL grammars (WHATWG vs RFC) → one server tallied as two hosts.
2. Scheme/port/www twins: http/https, :443, www vs apex of same site counted as two corroborations.
3. URL-parameter host spoofing: example.com/page?@evil.com — parsers disagree on host extraction.
4. Redirect attribution swap: stored URL is reputable host; after 302 the bytes come from attacker (or reverse). Fix: count post-redirect origin only (grok G4).
5. IP-literal collapse failure: many textual forms of one address (decimal/octal/hex, IPv4-mapped IPv6) each counted as a host; PTR theater adds fake names (grok G3: all spellings → one canonical IP key; IP-only pages don't corroborate names).
6. Platform sybils under public suffix: *.github.io, *.blogspot.com, *.pages.dev, *.wordpress.com user sites, one account (grok G11: platform suffix ≠ independence).
7. CDN canonicalization collapse: fastly.net/cloudfront.net/akamai.net edges serving identical attacker origin (fable G3: require ≥2 distinct origin IPs).
8. Dangling-host takeover: abandoned subdomain of reputable eTLD+1 still delegated.
9. Split-horizon DNS: same host string, different A records for instrument vs auditor (fable: record IP + cert SPKI with vote; mismatch flags claim).
10. One canonical URL parser (grok G1): WHATWG only; reject userinfo, empty host, non-http(s); identity on canonical host. Falsifier: one listener, two spellings, distinct count still increments.

## For Crew B (corroboration/majority layer)
1. Syndication/wire echo: one false sentence republished byte-identically by many real news sites — real eTLD+1s each.
2. Mirror multiplication: one plant copied into archive.org, amp, translate wrappers, search caches — each counted as new host (grok G5: body-hash cluster = one vote).
3. Boilerplate injection: shared widget/comment plugin/footer inserts S on many legitimate sites (grok G7: corpus DF ceiling — sentences on too many registrable domains are non-evidential).
4. Negation/quote strip: honest pages say "false that S" or quote S; extractor keeps inner S which matches the plant (grok G9: install only if asserted, not quoted/negated/hypothetical).
5. Normalization collision: NFKC/zero-width/entity folding maps two different claims onto one byte string (grok G8: conservative normalization — strip controls/zero-width only).
6. High-DF sentence: short generic sentence already on ≥2 honest hosts "confirms" a claim it never asserted.
7. Tie/order poison: equal support for S and ¬S; first-seen installs S (grok G10: ≥3 votes from distinct clusters; contradictory cluster blocks; equal support installs nothing; order irrelevant).
8. Context drop: date/place stripped by normalization so expired/scoped sentence matches timeless false claim.
9. Comment/hidden-text channel: S in display:none, HTML comments, JSON-LD, profile fields the extractor still emits (grok G6: main-text only).
10. Feed vs page: same CMS emits S on article host and via syndicated RSS host treated as independent.
11. Install-once race: two hosts serve S only during crawl window, then change; KB keeps S with no live support (fable G4: claim TTL + revalidation).
12. Pre-bunking SEO saturation: 100 thin-host blogs drown 1 honest authoritative page.
13. Temporal sandwiching: attacker serves lie at T0 on A and B; honest hosts overwrite at T1; narrow ingestion window captures lie.
14. Cert rotation pivots: attacker controls evil.com week 1, sells to honest operator week 2 serving contradictory content.
15. Wikipedia mirror farms: 40+ distinct TLDs mirroring identical paragraphs with injected one-sentence lies spliced in.
16. Cloak on fixed UA: deterministic crawler always receives S; humans don't (grok G12: second deterministic fetch profile; mismatch ⇒ no vote).
17. Compromised legitimate sites: two genuinely distinct trusted news sites compromised for 10 minutes. BOTH models agree: UNFIXABLE at this layer — no host-level heuristic distinguishes from true consensus.

## Agreed rankings (both models, convergence)
1. Canonical host normalization (G1) — kills the whole forgery class, ~200 LOC.
2. eTLD+1 via pinned PSL (G2) — kills subdomain sockpuppets, ~50 LOC + list.
3. Retrieval-order independence / no-tie-install (G8/G10) — ~20 LOC, zero meaningful cost.
4. Cluster quorum ≥3 + contradiction blocks (G10).
5. Body-hash dedup (G5) — with the honest caveat: mirror-dedup and honest syndicated truth pull opposite ways.
