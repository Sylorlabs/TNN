# LI-HARDEN — Convergence: The Guideline Set (DRAFT, pending Crew A)

Sources: blind red-team interim (V-BF1 17/32 INTEGRITY-FAIL), grok-4.7 consult (20 attacks, G1–G15), claude-fable-5.1 consult (10 attacks, G1–G8), Crew B CORROB-1 build+battery (commit 0cc9450e, 420 runs), Crew A GLUE build+battery (commits 9c959cd4 prereg / 8fd3c3ac implementation, 17×2 B2 runs + B1–B8).

NOTE: Crew A's headline verdict is INTEGRITY-FAIL — stated honestly, because 7 residual installs survive. But the prereg §7 impossibility argument CONFIRMS empirically that those 7 are host-shape-identical to honest corroboration: no host function closes them without killing honest throughput. The measured outcome is 10/17 killed, 0 regression, not a failure of the mechanism.

## Ranked guideline set (correctness gained per unit cost)

### Tier 1 — build immediately (low cost, high kill rate)

**HL-1 Canonical URL parser + host normalization.** Mechanism: one WHATWG parser; reject userinfo/empty-host/non-http(s); percent-decode authority before parsing; strip trailing dots; canonicalize IP spellings (dotted/hex/octal/v6/v4-mapped → one form); IDNA→A-label, reject confusables/mixed-script; FAIL CLOSED on unparseable. Falsification battery: one listener, N spellings of the same URL (trailing-dot, %2e, @, hex-IP, Cyrillic homograph) → distinct-host count must stay 1 for all spellings; empty-host URL must fail closed. Kills: the entire glue-forgery class (red-team #2). Cost: ~200 LOC, +10 audit lines/case (B7: 12.2 vs 7.7 lines/log — the EMIT| host-key trail). Evidence: Crew A B1 57/57 frozen unit vectors byte-exact; B2 10/17 attack classes killed (S1–S3, G1–G6, G9: install→withhold vs V-BF1); B8 consult extensions C2–C7 killed. Audit cost +58% on log lines — the traceability tax, gated as report-only.

**HL-2 Registrable-domain (eTLD+1) as the corroboration key.** Mechanism: pinned public-suffix list (private section included); host→registrable domain; corroboration counts distinct registrable domains, not raw hosts. Falsification battery: a.disinfo.com + b.disinfo.com + deep.c.disinfo.com echoing one false sentence → count must be 1. Kills: subdomain sockpuppets (red-team #1, cheapest attack). Cost: ~50 LOC + PSL. Evidence: Crew A — S1/S2/S3 (subdomain classes) all killed; zero throughput regression (B4 12/12 honest installs).

**HL-3 Retrieval-order independence + no-tie-install.** Mechanism: canonical pid-sort before quorum evaluation; 2v2 or any tie → withhold (never first-seen-install). Falsification battery: permute retrieval order over a 2v2 fixture (4+ permutations) → byte-identical KB outputs, all withhold. Kills: red-team #3's tie component. Cost: ~20 LOC. Evidence: Crew B 4/4 permutations byte-identical, all withhold (VERDICT_CORROB1.md).

**HL-4 Contradiction veto (any visible contradiction withholds, regardless of majority).** Mechanism: explicit-negation scan (with contraction expansion) + numeric-conflict scan (incl. range-vs-point) over opened pages; any P vs not-P → CONTRADICTION, withhold. Falsification battery: 2v1 sockpuppet-vs-honest fixtures → withhold; honest clusters (12/12) must still install. Kills: mixed-cluster majorities (red-team #3). Cost: ~300 LOC. Evidence: Crew B — prior BF1 23/38 false installs → CORROB-1 5/38, 18 killed, 0 new misses; honest 12/12 intact; paraphrase defense preserved.

**HL-5 Quorum ≥3 distinct registrable domains.** Mechanism: install needs ≥3 votes from distinct HL-2 clusters (up from 2). Falsification battery: 2-sockpuppet + 1-honest fixtures → withhold; honest triple-cluster truth → install. Cost: some honest-pair recall loss (measured, not assumed — guard battery required). Evidence: Crew B experimental; adopt only if throughput guard passes.

### Tier 2 — build next (medium cost, real attack classes)

**HL-6 Main-text-only extraction.** Mechanism: drop script/style/comments/hidden nodes/UGC chrome/JSON-LD duplicates; keep article body. Falsification battery: false sentence present only in shared footer or aria-hidden block → 0 votes. Kills: hidden-text channel, boilerplate injection. Cost: extractor rework (medium).

**HL-7 Conservative normalization.** Mechanism: strip controls/zero-width only; no NFKC; no date/number deletion; sentence bounds that don't split on Dr./3.1. Falsification battery: two human-distinct sentences that previously collapsed → now distinct, no install. Kills: normalization collision. Cost: low–medium. Evidence: Crew B X_NORM1 killed with conservative normalization.

**HL-8 Redirect-attribution: count post-redirect origin only.** Mechanism: evidence host = final response origin after hop cap; cross-registrable hops don't add a vote. Falsification battery: reputable start URL 302→attacker → KB attributes to attacker origin, not start host. Cost: low.

**HL-9 Platform-suffix ≠ independence.** Mechanism: names on free-host suffixes (*.github.io etc.) need an extra non-platform cluster; one account's many sites = one vote. Falsification battery: two github.io user sites alone → withhold. Cost: suffix list (medium).

**HL-10 Body-hash mirror dedup.** Mechanism: pages with byte-identical sentence bodies cluster to one vote; <2 surviving clusters → quorum fail. Falsification battery: archive+AMP+cache of one plant → one vote. Kills: mirror farms, Wikipedia mirror farms. Cost: medium. ⚠️ MEASURED TRADE-OFF: Crew B verdictm killed mirror farms but honest throughput fell to 11/12 (H8: 4-host byte-identical wire truth withheld) — the grok-predicted mirror-dedup vs honest-syndicated-truth tension, confirmed. Cannot adopt under the zero-regression bar; needs a design that separates wire-truth from plant-mirrors (e.g., diversity of surrounding text).

### Tier 3 — expensive or detection-only (adopt deliberately)

**HL-11 Claim TTL + revalidation.** Mechanism: claims expire (e.g., 72h); re-verify with fresh fetches; drop if quorum fails. Falsification battery: install, remove from sources, confirm auto-drop. Kills: install-once race, temporal sandwiching. Cost: refetch scaled by KB size (medium–high).

**HL-12 Second fetch profile (cloak detection).** Mechanism: second deterministic profile (UA/Accept-Language); body mismatch ⇒ no vote. Falsification battery: single-UA cloak → second profile disagrees → no install. Kills: naive cloaking only. Cost: 2× fetch.

**HL-13 Operator-coincidence provenance (A9 remainder).** Mechanism: ~50 lines at verdict layer — shared author/CMS/link-target/timestamp across the quorum blocks install. Measured: present on R3/R4/M3 quorums, absent on every honest install (Crew B). Limitations: (a) evaded by metadata diversification (expected adaptation); (b) REQUIRES the metadata pipeline production glue was forbidden to emit — a pipeline decision, not a verdict patch; (c) needs its own metadata-forgery red-team. This is the cheapest signal that dents the A9 residual.

## Honest "cannot fix" (both models + Crew B agree)
- Compromised legitimate sites in a time window: two genuinely distinct trusted sites serving the same false sentence — no host-level heuristic distinguishes this from true consensus; installing IS the correct behavior under the 2-source design. Inherent to the architecture.
- Syndication/wire echo of falsehoods by genuinely independent publishers: byte-identical agreement is not truth.
- Zero-day DNS/DoH poisoning of the fetcher itself: trusted-base problem, outside KB-integrity scope.

## Residuals (measured, classified)

Glue residuals (Crew A, host-shape-identical to honest corroboration — no host function closes them): R2, R3, R4, P3, M1, M2b, M3; C8/C9 (dangling takeover, split-horizon DNS — need DNS/cert/IP attestation beyond URL spelling); C1 (backslash grammar fork, documented).
Corroboration residuals (Crew B, unanimous-false among opened pages): M3, R3, R4, E_LD3, E_TS3; wire echo, boilerplate injection, negation/quote strip, high-DF sentence, context drop, feed-vs-page double count, compromised legitimate sites.
The overlap (M3/R3/R4) is the shape the whole program converges on: unanimous false agreement among genuinely diverse sources. The cheapest signal that dents it: HL-13 operator-coincidence provenance (~50 lines, but needs the metadata pipeline).
## Measured outcomes (both crews)

- Glue B2 (17 classes × 2 reps): 10 killed (S1–S3, G1–G6, G9), 7 residual installs — all host-shape-identical to honest corroboration (prereg §7). B1 57/57 frozen unit vectors byte-exact. B3 paraphrase matches V-BF1 exactly. B4 12/12 honest installs, zero regression. B5 52/52 byte-identical. B6 exactly the 10 intended flips, 0 unexpected deltas. Frozen webg.zag untouched.
- Red-team 38: 23/38 false installs (V-BF1) → 5/38 (CORROB-1) → 4/38 (+dissent scan). 18–19 killed, 0 new misses, honest 12/12, paraphrase defense intact, 210/210 determinism.
- verdictm mirror dedup: kills farms, costs H8 (11/12) — rejected under the zero-regression bar.
