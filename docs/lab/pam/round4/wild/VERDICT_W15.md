# VERDICT — W15 STAGED QUARANTINE PAM (WILD-B, generation 3)

**Status: SURVIVE.** All kill bars pass; liveness exceeds bar.

**Date:** 2026-09-24. **Frozen prereg:** `pam/round4/wild/prereg/PREREG_W15.md`.
**Instrument:** `pam/round4/wild/w15/w15_quarantine.zag` (pure Zag, zero RNG,
`[]u8` arenas + LE accessors, logical time = event index; arena hash keyed
by semantic_tag).
**Scorer:** `pam/round4/wild/w15/score_w15.py` (independent Python tier
machine — dict-based, not the arena hash — asserting transition-exact
equality plus all bars and diagnostics).

## Battery numbers (2026-09-24, 2× byte-identical)

- stdout SHA-256 (both runs):
  `de044f42f36c2fb25e5dd817d045ac9b87bd86824ccb700161548c4661991917`
- 5,250 events; 1,868 tags (1,668 genuine: 1,666 triples + 2 singles;
  200 false); 5,250 transitions logged.
- Independent mirror recomputed all transitions: **0/5,250 mismatches**;
  per-tag finals match exactly.
- **F-K5:** 0/200 false percepts reach Tier 3. **PASS.**
- **K1:** 0/30 frozen wrongs (tags 900000–900029) reach Tier 3. **PASS.**
- **KB-W15-XC:** 0 T1→T2 transitions without a valid logged cross-channel
  corroboration (scorer re-verified each against the stream). **PASS.**
- **KB-W15-RG:** 50/50 contradiction fixtures produce cascade demotion,
  all T3→T2 (tags 0, 31, …, 1519). **PASS.**
- **KB-W15-LIVE:** 4,998/4,998 triple percepts reached T3 = 99.96% of
  5,000 genuine (bar 90%). **PASS.**
- **K3:** genuine final-T3 tags 1,616/1,668 (reported; the 50 demoted tags
  reached T3 then regressed per F3 — that is the design working, and the
  2 singletons never had corroboration by fixture construction).
- **K4:** per-event work O(1) (hash probe + 3-channel scan); table 4,096
  slots fixed, 1,868 used ≤ 16,384 frozen cap (asserted). **PASS.**
- **K5:** terminates (rc 0, 5,250 events). **PASS.**
- **K2:** 2× stdout byte-identical. **PASS.**

## Diagnostics

- **D-W15-1** final tier histogram: G-T3 1,616; G-T2 50 (contradiction-
  demoted); G-T1 2 (singletons); F-T1 200. Every false died at T1 —
  unique tags, single channel, zero corroboration, exactly as the
  threat model intends.
- **D-W15-2** max tier per false: {1: 200} — none got past the
  corroboration gate.
- **D-W15-3** demotion trace: 50 tags, one level each (T3→T2), no
  over-demotion, no re-promotion (window anchored at T1→T2 long expired).

## Mechanism notes

- The Tier-1 jamming attack (falses interleaved at every 26th position,
  splitting triples with gaps ≤ 2) is absorbed by TIER1_WINDOW=5 with
  margin — content-based (tag+channel) corroboration is timing-agnostic
  within the window, which is what the battery verifies. All 1,666
  triples reached T3 despite the jamming.
- T2→T3's window is anchored at the T1→T2 transition (frozen), not
  sliding — stale third-channel arrivals cannot promote. Not exercised
  by the fixtures (all gaps ≤ 2); the anchor is load-bearing as specified.
- Contradiction events (contradicts=1, kind=G) bypass promotion entirely
  and demote exactly one tier; the instrument asserts their content_sig
  differs from the tag's (fixture-integrity check, 50/50).

## Standing-law cap classification (2026-09-24 law)

- **Load-bearing mechanisms:** corroboration window (without expiry, stale
  corroboration admits); tiered influence (T0/T1 = 0 weight); contradiction
  regression (cascade); one-level-per-contradiction.
- **Values calibration / arbitrary-flagged:** TIER1_WINDOW=5 (generous vs
  the ≤2 jamming gaps — a tighter window would still pass this battery;
  the value is calibration); table capacity 16384 (4,096 slots used).
- No perverse interaction found between window and lag (unlike W13's
  snapshot/active coupling) — W15's liveness passes at 99.96%.

## Commits

- Evidence/source: `e2b85ac99e51fbde6e0e65e50159217d22a61f9b`
- Verdict (this file): *committed separately per protocol*

## Paths

- `pam/round4/wild/w15/w15_quarantine.zag`
- `pam/round4/wild/w15/score_w15.py`
- `pam/round4/wild/w15/evidence/w15_stdout_run1.txt`
- `pam/round4/wild/w15/evidence/w15_run_hashes.txt`
- `pam/round4/wild/w15/evidence/w15_score.txt`
- Frozen stream: `pam/round4/wild/w15/w15_stream.txt`
  (generator `pam/round4/wild/w15/gen_quarantine.py`)

## Cross-design notes

- W15 is the only design of the eight to gate influence by *provenance
  depth* (three independent channels) rather than by score threshold
  (W4/W12), memory (W5), or time-bounded lease (W13). It is also the only
  one with a working *regression* path (contradiction → demotion) —
  W13's leases expire but never demote on counter-evidence.
- W15's 0/200 false-at-T3 and W11's 0/170 attack-admit are the round's two
  clean containment results; W15 achieves it without any cryptographic
  binding (cf. W11's HMAC chain), purely via corroboration multiplicity.
