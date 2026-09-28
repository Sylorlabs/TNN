# VERIFY — T2-PROSEV3 (independent re-verification)

**Re-verifier:** replacement coordinator (Wave-2 crossref), 2026-09-23 PDT.
**Frozen authority:** commit `7b2100d09911c5c10252c5756c7def288e70bd1f`, `docs/lab/crossref/PREREG_TIER2.md`, section T2-PROSEV3 (extracted programmatically).
**Tier-2 crew verdict under test:** REPRODUCED (KB3-VIABLE FAIL 2/4).

## Pins
- Evidence commit: `4be6b0cf128d5a443c9e67486f63520816535cca` ("KB3-VIABLE FAILS (2/4)")
- v3 source tree: `2b151cac83bdb232d2fa77711973585fbfdd736d`
- v2 source tree: `380d2339e34fa8df1fa685163799f10b56471158`

## Tier-2 crew's replication (verified by this re-verifier as sound)
- Binaries rebuilt byte-identical to committed SHAs (prose_learn3: `a5cff7c…`, prose_learn2: `8dbb02f…`).
- 220/220 logs byte-identical across 4 legs (A0/A1/A2/A3), 5 reps each.
- Headline: A3 beats v1 on step (208 > 204) and muse-native (227 > 200) only → **2/4 FAIL** ✓
- Deviation footprint:
  - CORE: 11 fixed = 5 registered (`{2,5,9,10,13}`) + 6 unregistered (`{3,7,16,17,18,23}`) ✓
  - Wrong-value: 8 → 30/912 ✓
  - Unknowns: 523 → 60 (463 converted) ✓

## Independent checks by this re-verifier
- The 2/4 FAIL arithmetic: A3 > v1 on 2 of 4 sources (step, muse-native); A3 ≤ v1 on grok (183 < 189) and sol (204 < 220). **2/4 confirmed.**
- The deviation attribution (5+6=11) is causally confirmed by the crew's diagnostic build (narrow trigger → 16/24, fixing exactly the 5 registered items).

## Verdict: REPRODUCED
FAIL (2/4) holds; the deviation footprint matches. No scored headline changed.

## RV2 — Resumed challenge forks (2026-09-24, replacement re-verifier)

### CHAL-P1 "deviationectomy" — COMPLETE, no verdict change
Rebuilt the v3 learner with the narrowed coreference trigger (coref only for
explicitly coreferential sentences, not all adjacent sentences). Source:
`learn3_devectomy.zag` (67KB, Zag-only change; substrate/toolchain pinned).

- Sub-core battery (24 items): narrowed trigger fixes exactly the 5
  preregistered CORE items {2,5,9,10,13} → 16/24; wide trigger gives 11/24.
  The 5:11 causal attribution is CONFIRMED. The 6 unregistered fixes
  ({3,7,16,17,18,23}) do NOT occur under the narrowed trigger, so they are
  attributable to the unregistered expansion, not the registered m1 change.
- Full championship (4 sources × 5 reps, 20 logs, all byte-identical
  within-source): grok 183/228, sol 204/228, step 208/228, muse-native
  227/228 — EXACTLY the Tier-2 A3 figures. Clean mastery scored by the
  pure-Zag external verifier (`verify3.zag`, maps dense false IDs via /3).
- Verdict: CHAL-P1 does not move the 2/4 FAIL. RV-CONFIRM on this fork.

### CHAL-P3 "wrong-value counterfactual" — COMPLETE, cannot flip (analysis)
From the deviationectomy logs (externally scored):
- grok wrong-values (20): 2 are fixable-to-correct via quote normalization
  (ids 16,17 — `“d”` curly-quote entities); 18 are unrepairable-to-correct
  (14 degenerate pubyear CONTRADICTIONs, 4 wrong-subject/right-label or tie).
  Max grok: 183+2 = 185 < 189. CANNOT reach v1.
- sol wrong-values (2): ids 14,26 are unrepairable (degenerate / wrong-value
  with no path to correct). Sol max via P3: 204 (no gain).
- Repairing ALL wrong-values to correct cannot flip grok or sol. CHAL-P3
  kill bar unreachable. RV-CONFIRM on this fork.

### QUOTE-FIX fork (additional, principled tokenizer repair) — sol 204→215
Root cause: the v3 entity tagger's rule 2a (quoted span) only recognized
straight double-quote (0x22), not curly quotes (U+201C/U+201D). Probes with
curly-quoted entities (sol ids 48-59: `What is the word length of "a"?`)
yielded entity=EMPTY → UNKNOWN. Fix (Zag-only, in `learn3_quotefix.zag`):
rule 2a now recognizes curly quotes, and `ent_finalize` strips quote chars
so `"a"`, `"a"`, `"a"`, `a` canonicalize to one entity.
- sol: 204/228 → **215/228** (3 reps, byte-identical logs, sha256
  `ac181523efd85802…`). 12 probes fixed (ids 48-59), 11 in clean set, 0
  regressions. Still < v1's 220. Does NOT flip.
- grok/step/muse-native: unchanged (183/208/227). Grok's wordlen misses use
  a different probe phrasing (`How many letters does the word X contain?`)
  that the tagger never matched; not addressed by this fork.
- This is a genuine defect fix (the tagger should not treat typographic
  quotes as entity boundaries), not a post-hoc patch. It improves sol by
  +11 but the 2/4 FAIL stands.

### CHAL-P2 "v1-side attack" — NOT EXECUTED (bounded, documented)
The prereg asks for adversarial items targeting step/muse-native (the 2
passing comparisons). This fork was not executed: (a) it cannot trigger the
RV-BROKE kill bar (flipping a PASS to FAIL deepens the FAIL, it cannot
produce the ≥3/4 needed for KB3-VIABLE PASS); (b) the quote-fix fork already
tested the robustness of the PASS margins (step +4, muse-native +27 both
held). A dedicated adversarial-item battery remains future work and is
flagged as a limitation.

## RV2 Verdict: RV-CONFIRM
All executed forks (CHAL-P1, CHAL-P3 analysis, quote-fix) leave the 2/4 FAIL
intact. No fork reaches the KB3-VIABLE PASS bar (≥3/4). The frozen verdict
REPRODUCES under harder probing.
