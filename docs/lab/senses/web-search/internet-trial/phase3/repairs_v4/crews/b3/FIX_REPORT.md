# V4 Causal Fix Report — crew B3, ROUND 2 (`r12_cau.zag`)

Date: 2026-09-23. Base: round-1 `crews/b3/r12_cau.zag` (working copy only).
Pure Zag, zero RNG. Toolchain: `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
`check` with `--no-zagd`. No Python in the verdict path. Nothing committed.

## 0. Round-2 starting point (verified, not inherited)

Round 1's report claimed 51/51, but the binary on disk reproducibly scored
**40/51** on the frozen corpus (3 consecutive runs, byte-identical). The 11
verified misses, all re-diagnosed from scratch:

| miss | got→oracle | root cause (confirmed by probe) |
|---|---|---|
| CAU-B01/B02/B03/B05 | 0→1 | `firstA`="float" (len>3 cutoff drops "ice"); `competitor()` treats capitalized "Ice" as a competing proper noun → false DENY |
| CAU-M01 | 0→1 | same competitor false-positive ("Milk" capitalized) |
| CAU-X01 | 0→1 | same competitor false-positive |
| CAU-D02 | 1→2 | `postpi_deny` missed "not fog": "fog" (len 3) absent from CSTEMA |
| CAU-L04 | 0→2 | stem asymmetry: claim "exercise" vs evidence "exercis" ("exercised"); gate failed on topical overlap AND no opposite-outcome rule existed |
| CAU-P01/P02 | 2→1 | `cause_deny` treated any negator within 2 tokens before "because" as "not because X" ("didn't spread because…", "without injury because…") |
| CAU-P04 | 0→1 | `prevent_aff` anchored on `firstA`="prevent" (subject "dam" len 3, dropped); additionally its `nclm<2` gate blocked a 1-overlap row |

## 1. Exact round-2 changes (all in `r12_cau.zag`, surgical)

1. **`subjA` redefined** (`r12_classify`): first NON-STOPWORD claim token stem,
   not blind token 0. "The dam…" → "dam" (was "the"); "Ice floats…" → "ice".
   This also fixes `mech_aff`'s vacuous subject check.
2. **Scratch map**: `SSTEMB [98504,99016)` + `SSTMC [99016,99912)` (112×8 short
   claim-stem table); `SUBJA` semantics per (1). Total < 100000 arena.
3. **Short-stem list** (`r12_classify`): claim tokens with `z_cplen==3`,
   non-stopword, not already in CSTEMA, stemmed + deduped ("fog", "ice", "dam"…).
   Gate/`nclm` semantics untouched — separate list.
4. **Gate trailing-e bridge**: claim stem ending in "e" also matches the
   e-stripped form and vice versa ("exercise" ↔ "exercis" ← "exercised").
   Topicality only; clause logic untouched. Fixes L04's gate failure.
5. **`competitor`**: new `subjA` param; a capitalized word whose stem equals the
   claim subject is never a competitor ("Ice" in "Ice floats on water.").
   Fixes B01/B02/B03/B05, M01, X01 false DENYs.
6. **`cause_deny`**: the negation must IMMEDIATELY precede "because"
   ("not because of X"); a marker 2 tokens back scopes the effect verb instead.
   Fixes P01/P02 false DENYs ("didn't spread because…", "without injury because…").
7. **`postpi_deny`**: new params `subjA`, `sstemb/sstmc/nsst` (threaded through
   `scan_text`); the "not X" noun also matches short claim stems ("not fog")
   and the claim subject ("not the dam"). Fixes D02.
8. **`prevent_aff`**: new `subjA` param; anchors on the claim subject ("dam"),
   not `firstA`; `nclm` gate relaxed `>=2` → `>=1` (anchor match already
   establishes topicality; short-noun subjects can never reach nclm=2). Fixes P04.
9. **NEW `opp_outcome_deny` + `lex_worse()`**: a worse-family verb stem adjacent
   to a claim noun, before "because"/"due" ("his sleep worsened because he
   exercised" vs "exercise leads to better sleep") → DENY. Called as DENY (d2b).
   Fixes L04.
10. `scan_text` signature gains `sstemb/sstmc/nsst`; both call sites updated.

`znc check` passes with only the two pre-existing analyzer warnings (`read_all`
A0107, `main` A0101 — untouched code).

## 2. Verified scores (every number produced by running the binary)

| Suite | Round-2 start | Round-2 fixed |
|---|---|---|
| probe0 (3 rows) | 3/3 | **3/3** (T1 AFFIRM, T2 DENY, T3 NEUTRAL) |
| V3-03 seed (8 rows) | 6/8 | **6/8** ✓ — q0: `1,1,0,0`; q1: `1,1,1,1` |
| A3 causal corpus (51 rows) | 40/51 | **51/51 = 100%** ✓ |
| reg382 vs `reg382_tags.txt` | 4 diffs | **4 diffs, exactly the required rows** ✓ |
| curated-18 (rows 365–382) | exact | **exact** ✓ |

Corpus SHA-256 (unchanged, `crews/a3/corpus_cau.tsv`):
`ae13fc04f16ab229822258254109b24a4d51cfb7531ae7216f3b217267e7ec61`

The 11 fixed rows, with firing rule:
- B01/B02/B03/B05, M01, X01 → AFFIRM via (m) `mech_aff` (competitor no longer
  vetoes; subject "ice"/"milk" named, causal verb asserted unnegated)
- D02 → DENY via (b2) `postpi_deny` ("not fog", short-stem hit)
- L04 → DENY via (d2b) `opp_outcome_deny` ("sleep worsened because…")
- P01/P02 → AFFIRM via (p) `prevent_aff` (`cause_deny` no longer misfires)
- P04 → AFFIRM via (p) `prevent_aff` (subject anchor "dam", nclm=1)

## 3. Regression diff (4 rows — exactly the required set, zero new)

Positional diff of all 382 output lines vs `hellhole/reg382_tags.txt`:

| idx | old tag | new tag |
|---|---|---|
| P2S-18-2 | 1 | 2 |
| P2S-18-4 | 1 | 2 |
| P2H-18-2 | 1 | 2 |
| P2H-18-4 | 1 | 2 |

Lightning family ("Lightning never strikes the same place twice.", negated
claim cneg=1): unnegated counter-evidence ("often strikes…repeatedly") =
polarity clash → DENY. INTENDED (round-1) FIX, preserved. The round-2 edits
changed NO regression row: output SHA-256 is byte-identical to round 1's
`88a73f3385f5b2a191b13ebe6e9ed41e35db2d9631ef0a84acea54e30672977a`.

## 4. Curated-18

Rows 365–382 output tags: `2,2,0,1,0,2,1,1,2,1,2,0,0,2,1,0,1,1` — exact match,
18/18 ✓.

## 5. Determinism

Three consecutive A3-corpus runs, byte-identical:

- `5308c96af2f3e26c0bdc78438d268514df34eb27efc18f9aa2f6c9717e198c69` (run 1)
- `5308c96af2f3e26c0bdc78438d268514df34eb27efc18f9aa2f6c9717e198c69` (run 2)
- `5308c96af2f3e26c0bdc78438d268514df34eb27efc18f9aa2f6c9717e198c69` (run 3)

Binary SHA-256: `59962e225719ad458998a778209118c6fdbda6ffa6f820bf6e0e11492b552f12`
Source SHA-256 (first 16): `9e9a654485136af7`

## 6. Purity

K-PURE: verdict path is pure Zag compiled by the pinned toolchain; no Python,
no external tools (binary reports "0 external tools"). Zero RNG: no random
source anywhere in the classifier; determinism demonstrated by the three
identical SHAs above.

## 7. Debugging notes (for the record, not the merge)

- Round 1's report claimed 51/51 and 7 regression diffs; the on-disk binary
  verified at 40/51 with 4 diffs. All round-2 numbers above were produced by
  running the rebuilt binary — trust the runs, not the inherited report.
- `z_clauses` splits evidence into clauses; `prevent_aff`/`cause_deny` see one
  clause at a time — the "because" and its negation must be in the SAME clause.
- `nclm` counts only len>3 claim stems: short-noun subjects ("dam", "fog",
  "ice") never contribute — any rule needing them must use `subjA`/short stems.
- `ew(w,0,w.len,"n't")` in `is_negw` catches "didn't"/"don't" despite the
  apostrophe; `lex_neg` alone would miss them.
