# H6-R3-W3 RESULTS — C salvage probe + W stays-dead confirmation

**Worker:** H6-R3-W3 · **Date:** 2026-09-24 · **Prereg:** `bdb04c7eb634b1d3f2f3f5519e4a1839abba8ae1`
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(sha256 `498abcb5…e58ef`). Pure Zag, zero RNG, every run byte-identical ×2.

## PROBE A — C salvage: NO salvageable core → THEATER stands CONFIRMED

Fork C's mechanism (from `forkC/src`, R2 build `0a2e006c`) was decomposed into
its five actual components. Note: the task brief's "span sums, max attestation"
do not exist in fork C — a grep of all `fc_*.zag` finds zero hits; those were
R1 C1-corroborator components. Fork C's real components:

| # | Component | Source |
|---|-----------|--------|
| 1 | COMP-NORM — canonical atomizer / dual fingerprints (analytic-structure checks) | `fc_norm.zag` |
| 2 | COMP-DELIB — `fs_add_delib` licensing of deliberation conclusions | `fc_store.zag` |
| 3 | COMP-MATCH — exact-equality install rule (verdict decision) | `fc_case.zag` + `fs_match` |
| 4 | COMP-STORELIC — `fs_load` license builder (provenance recorded, NOT gated) | `fc_store.zag` |
| 5 | COMP-PROV — provenance recorder bytes (`lprov`; DELIB licenses record prov=0) | `fc_store.zag` |

Isolation driver `cprobe.zag` (imports the frozen C sources unmodified) ran all
48 cases C-as-a-whole installs (24 M4 generator-authored trace alibis, 24 M5
confabulations grounded in GEN store entries). Output SHA
`e8ba56fc1d05301a5a1aa931db35251befd8cc4cdc59ab2fe941fad82665242f` (×2 identical).

| Component | M4 alibi rejection (n=24) | M5 confab rejection (n=24) | CB1 ≥70%? |
|-----------|---------------------------|----------------------------|-----------|
| COMP-NORM | 0/24 (24/24 parse OK) | 0/24 (24/24 parse OK) | NO |
| COMP-DELIB | 0/24 (24/24 alibi traces licensed, 0 refused; all 24 alibi atoms licensed with **zero** store grounding) | n/a (no DELIB field; 0/24) | NO |
| COMP-MATCH | 0/24 (24/24 INSTALL) | 0/24 (24/24 INSTALL) | NO |
| COMP-STORELIC | — (M4 licensed via DELIB) | 0/24 (24/24 atoms GEN-licensed; 24 GEN licenses in store table of 119) | NO |
| COMP-PROV | 0/24 (24/24 DELIB licenses record prov=0 — generator authorship **unmarked**) | 0/24 (24/24 marked GEN but **ungated**, gates=0) | NO |

Supporting measurements: 0/24 M4 drafts match any store-only license (the
alibis depend *entirely* on the DELIB license); every M4 install carries
`lic=DELIB:0`, every M5 install `lic=STORE:S9xx:GEN` — replicating the
builder's verdicts exactly.

**CB1 verdict:** no component reaches ≥70% on either case set (all 0%).
C has NO salvageable core → **THEATER stands, confirmed.**

## PROBE B — W scorers audited, killers re-run: W CONFIRMED DEAD

### Scorer audit (independent, not trust-the-report)

Diffed the recovered W sources (`~/workspace/selfpam_r2/forkW/`, three
locations byte-identical) against the re-attack's fixed set. Each fix maps
exactly to one bug class, mechanism untouched (all 167 per-fixture FIX lines
byte-identical orig-vs-fixed, ledger hashes included):

- **Bug A** (packed-count unpack): 8 sites in `w_main.zag` read
  `bad=(st/1000)%1000000` where `dn_labstat` packs `tot*1000000+bad*1000`
  (yields `tot*1000+bad`, never the true `bad`). Fix: `%1000`. My audit counts
  **8 sites, not 9** as the re-attack prose claims — all 8 fixed; no other
  unpack sites exist. Mechanically re-applied fix is byte-identical to the
  re-attack's `w_main_fullfix.zag`.
- **Bug B** (field clobber): `ps_h_TEXT` (`w_parse.zag:372`) writes the token
  count `nt` to `fb+56`, the PAIR-name slot that `ps_h_PAIR` (`:346`) wrote the
  pair sid into — fixtures got paired by equal token count. `fb+56` is read
  only by `dn_mate`; nothing reads it as a count. Deleting the store is exact.
- **Bug C** (non-interned compare): `dn_mate` compared sids with `==`;
  `sp_add` (`w_util.zag:50`) does not intern. Fix uses `sp_eq` (content
  compare). Exact.

### Rebuilds (pinned znc, from scratch copies)

- Original driver output SHA `eff00337cadc3528a8b1fe85b53cc8892efe38eb0c4f233fd65b7426837fe407`
  — matches the crew-reported SHA and the re-attack reproduction (×2 identical).
- Fixed driver output SHA `4ba994ca83dd2ad954c02fc21b877d3e121138f95b77c3c8834ff6547fd532e3`
  — matches the re-attack fixed-driver SHA (×2 identical).

### True scores with correct scorers (fixed driver BARS section)

| Bar | Score | R2 margin | Result |
|-----|-------|-----------|--------|
| M2 meaning-flip divergence | 19/23 = 82.6% | ≥90% | **FAIL** (scope-pair attr-attach gap: S1/S2/S5/S6) |
| M5 generator-authored rejection | 0/10 | ≥70% | **FAIL** (recursion; witness grounds truth=C atoms, no authorship distinction) |
| M6 true-draft false-withhold | 6/20 = 30% | ≤5% | **FAIL** (over-withhold; R1/R7 licensing gaps on true drafts) |
| W2 C-POINTER | 4/10 | 100% HALLUCINATED_PATH | **FAIL** (6 HALPTR fail coverage S=2/V2R8) |
| (M1 22/22 PASS, M3 15/15 PASS, M4 10/10 PASS, W1 95/95 PASS, W3 PASS) |

**WB1 verdict:** W with audited/correct scorers still fails **4/4** of
{M2, M5, M6, W2} at R2 margins (≥2 required). **W is CONFIRMED DEAD.**
The scorer bugs masked nothing about survival — they only moved the *margins*,
not the outcome. No resurrection.

## Artifacts

- `probeA/src/cprobe.zag` + `probeA/run1.txt` (SHA e8ba56fc…) — component isolation evidence
- `probeB/w_orig/` + `probeB/w_fixed/` — audited W sources (fixed = mechanical re-application, comment-only diffs vs re-attack set)
- `probeB/w_orig_run1.txt` (SHA eff00337…), `probeB/w_fixed_run1.txt` (SHA 4ba994ca…) — ×2 byte-identical each
- This report: `PREREG_H6R3_W3.md` (committed `bdb04c7e…`), `RESULTS_H6R3_W3.md`

No binaries or `.zagd` files committed. Scratch: `~/workspace/scratch-h6r3/w3/`.
