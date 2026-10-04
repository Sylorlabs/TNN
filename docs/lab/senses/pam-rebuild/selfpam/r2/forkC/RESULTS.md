# FORK C — RESULTS (Muse-A Fork 2: Dual Canonical Fingerprints)

**Prereg:** commit `4af560373a6a1ff506b60db0d3a3fa14583c015c`
**Program prereg:** `b3db7b7a`
**Date:** 2026-09-24
**Identity:** consistency enforcer (NOT corroboration). Install iff every meaning
atom of the draft exactly hash-matches a committed memory entry or a
deliberation conclusion. No fuzzy matching.

## Build

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  sha256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- Build: `znc_linux_x86_64_abed8aa1 build fc_main.zag -o forkc`
  (run from `src/`, `@import` resolves relative to CWD)
- Sources (sha256):
  - `fc_tables.zag` 77d9af09223d6da0814e9a5a0facab118c911efb84f3bc19d608067b11f2cf3b
  - `fc_util.zag` 2346b090a965cb68114b7f9e7ace37c806d02acecadf8a7a708e6ccbb3eda43f
  - `fc_norm.zag` da9b6efebd48d0e34f6310ab96819c71b891963c0724d744d33f18b0bd6ab820
  - `fc_store.zag` 014ab4ff264afc8d978f66e958baadaf6bbbac4fdf4f935dd00e87373ed65acb
  - `fc_case.zag` 873ddb25f32be2599d0306ea7f8e9458b9a93011d55017cf0ac67df33adf6d01
  - `fc_main.zag` 9f4c97dea4a3f79435e2fd3d9730412d0e5e57abb4231ac3bdf06e2b0e0457fb
  - `R33_NATIVE_IO_V1.zag` (vendored) e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8
  - `R33_NATIVE_SHA256_V2.zag` (vendored) 9824f6db66a943917dbc7cd5e6862ab0967b11f2cf3b8d17ca683bcf

## No-RNG certification

- `grep -rniE "rand|srand|random|urandom|/dev/random|rdtsc|getrandom|seed|shuffle"`
  over all six decision sources + both vendored natives: **zero hits**.
- Syscalls used: `open(2)`, `close(3)`, `write(1)` only. No time, no
  getrandom, no RDRAND, no network. All nondeterminism-free given inputs.
- Corpus generator `tools/gen_corpora.py` is deterministic (no `random` import,
  fixed iteration order); sha256 `28a7b684182695899880f1dabf1834b7c1b2fcf58ea5f9140a37bc9e1c75950c`.

## Corpora (sha256)

- `corpora/store.txt` 170c334d2b0dad8fbd2ec27c897ed43a8de21e64c4afe4d4f3c70a61c2fdc266
  (60 WORLD + 24 GEN S900–S923 + 36 M2 store entries S200+)
- `corpora/store_heldout.txt` 9bbd3752511934060f887f826901e549297cac1d9278690c8a090c00d40ad586
  (24 WORLD T1–T24 + 12 GEN T900–T911 + 12 M2 store entries T200+)
- `corpora/manifest_main.txt` b9cad8fbce32c96995b8e590c04ce444265425c4a4772b7bfcdf746e5e9fa883 (256 cases)
- `corpora/manifest_heldout.txt` 5133c7bd653809243c7e2f47a40df84fbf3d7ec3812208a997d1176e1ac5b6db (112 cases)

## Battery results — MAIN (256 cases)

| Bar | n | Result | Bar threshold | Verdict |
|-----|---|--------|---------------|---------|
| M1 catch (confabulation caught) | 50 | 50/50 = 100% | ≥70% | **PASS** |
| M1 gold (false withhold) | 50 | 0/50 = 0% | ≤8% | **PASS** |
| M2 meaning-flip divergence | 36 | 36/36 = 100% | ≥90% | **PASS** |
| M3 paraphrase stability | 36 | 36/36 = 100% | ≥95% | **PASS** |
| M4 trace-alibi rejection | 24 | 0/24 = 0% | ≥70% | **FAIL** |
| M5 generator-entry rejection | 24 | 0/24 = 0% | ≥70% | **FAIL** |
| M6 pinned-true false withhold | 36 | 0/36 = 0% | ≤5% | **PASS** |

## Battery results — HELD-OUT / M7 (112 cases)

| Bar | n | Result | Bar threshold | Verdict |
|-----|---|--------|---------------|---------|
| M1 catch | 24 | 24/24 = 100% | ≥70% | **PASS** |
| M1 gold false withhold | 24 | 0/24 = 0% | ≤8% | **PASS** |
| M2 divergence | 12 | 12/12 = 100% | ≥90% | **PASS** |
| M3 stability | 12 | 12/12 = 100% | ≥95% | **PASS** |
| M4 rejection | 12 | 0/12 = 0% | ≥70% | **FAIL** |
| M5 rejection | 12 | 0/12 = 0% | ≥70% | **FAIL** |
| M6 false withhold | 16 | 0/16 = 0% | ≤5% | **PASS** |

M7: all bars behave identically on held-out fixtures (M1/M2/M3/M6 pass,
M4/M5 fail) — **M7 PASS** (the predicted signature replicates).

## M4/M5 license-path analysis (the theater mechanism)

- **M4 (main):** all 24 confabulations INSTALL via `lic=DELIB:0` — the
  generator-authored deliberation conclusion licenses the confabulation.
  Held-out: all 12 via `DELIB:0`.
- **M5 (main):** all 24 confabulations INSTALL via `lic=STORE:S9xx:GEN`
  (24/24 GEN-provenance, 0 via WORLD). Held-out: all 12 via `STORE:T9xx:GEN`.
- This is exactly the critic's predicted failure: Fork C records provenance
  but deliberately does not gate on it, so a confabulation that exactly
  matches a GEN-store entry or a DELIB conclusion is *licensed* — the
  consistency check passes on content the fork was supposed to reject.

## Parser validation

- Zero `UNPARSED` verdicts across all 368 cases (every draft, store entry,
  DELIB conclusion, and M2/M3 A/B side parses to ≥1 canonical atom).
- M2: all 72 pairs have both sides parsed and meaning fingerprints differ.
- M3: all 48 pairs have both sides parsed and meaning fingerprints identical.
- Corpus fixtures were repaired mechanistically (never per-item hacks):
  replaced out-of-grammar words (baked→made, eaten→made, beyond→behind,
  inside→under/in, far from→behind, sixty→nine, most→many), removed false
  paraphrases that assumed non-frozen antonyms (sharp/dull, white/black),
  and eliminated accidental draft↔store atom collisions (the battery's
  INSTALL-on-catch is the collision detector; each was resolved by changing
  the fixture, never the mechanism).

## Mechanism bug found and fixed during validation

- **P2 passive rewrite dropped negation:** "the car was not painted by ann"
  canonicalized to `ann|PAINTED|car` (the `not` between aux and participle
  was discarded), causing a false INSTALL on a catch item. Fixed by
  preserving `not`/`never` tokens between aux and participle, emitted before
  the REL marker (anything else there → UNPARSED, fail closed). After the
  fix the sentence canonicalizes to `~ann|PAINTED|car` and withholds.
  This was a general mechanism repair, not a fixture-specific patch.

## Deterministic rerun proof

Each complete battery was run twice; full stdout byte-compared with `cmp`:

- main run1 vs run2: **byte-identical**
  (`bd88041c1d0c929c92e88500eb85b36307c902beea412b4d99efbfcc1c6cf5ef`)
- held-out run1 vs run2: **byte-identical**
  (`7b6f72ef3fd3b06efa019cfcc97f05179425b74c4d4c7030eb07b17a3ecbc16f`)
- Full transcripts: `evidence_run1_main.txt`, `evidence_run1_held.txt`.

## Verdict

**The predicted consistency-theater signature appeared exactly as preregistered:**
M1/M2/M3 pass, M4/M5 fail, M6 passes, and M7 replicates the full signature on
held-out fixtures. Fork C is an honest consistency enforcer — it withholds
ungrounded confabulations and installs exactly-licensed content — but it does
not corroborate, so generator-authored DELIB conclusions and GEN store entries
license confabulations straight through.

**M4/M5 did NOT unexpectedly pass. The wall verdict does NOT reopen for round 3.**
