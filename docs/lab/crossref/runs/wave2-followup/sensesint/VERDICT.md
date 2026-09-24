# VERDICT — T2-SENSESINT evidence recovery (Wave-2 cross-reference follow-up)

**Crew:** SENSESINT evidence-recovery crew (session 839731d4…, 2026-09-24)
**Frozen authority:** `docs/lab/crossref/PREREG_TIER2.md` at
`7b2100d09911c5c10252c5756c7def288e70bd1f` (blob
`b1178370036bffbda6eb68ea0989c0e427dc31b7`)
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)
**Disposition: ALL 10/10 MISSING EVIDENCE PATHS RECOVERED — recommend PARTIAL → REPRODUCED
(decision to coordinator)**

## Summary

The Wave-2 crew of record (247aa7b5) named 10/140 manifest evidence paths missing
at the frozen commit (3 P0 GK trial sources, 7 P2 phase-1 jsonl) plus 2 size
mismatches. This crew:

1. **Recovered all 10 missing files from the original worker's workdirs**
   (`~/workspace/grok47/senses/gk-scratch/` and
   `~/workspace/tnn-lab/senses/web-search/internet-trial/evidence/phase1/`),
   byte sizes EXACTLY matching the manifest in all 10 cases.
2. **Discovered a prior recovery had already landed**: commits
   `16ddf755fee7ab41765d961f01e0d2a3f0f2c875` (2026-09-23T18:22:39Z, GK sources)
   and `c9bd2b210f781eb60bc9ebcaa1a280225a758184` (2026-09-23T18:23:45Z, 7 jsonl)
   restore all 10 paths. Both are **ancestors of tnn-native-lab HEAD
   (`062b21a0…`)**. This crew independently byte-verified the HEAD blobs
   against the worker originals — all 10 byte-identical.
3. **Re-ran the load-bearing GK batteries** with the pinned toolchain against
   the byte-identical committed sense substrate: N=3 runs byte-identical;
   headline digests re-derive byte-for-byte (`488af9ab…`, `7f351a53…`,
   `94575a9a…`); outputs byte-identical to the worker's recorded run logs;
   all kill bars adjudicate exactly as VERDICT_SHEET §3 says (H1, H2, H3 all
   SUSTAINED).
4. **Explained the 2 size mismatches**: stale manifest, not corruption. The
   final local files are byte-identical to the committed blobs; the manifest
   measured pre-final drafts that were never committed (single-commit history
   at the frozen commit). Verdict-neutral.

## Per-path recovery table

| # | Manifest path | Tier | Manifest size | Recovered from | Recovery sha256 | HEAD-committed sha256 | Match? |
|---|---|---|---|---|---|---|---|
| 1 | `senses/web-search/v2/src/gk1_trial.zag` | P0 | 5285 | `~/workspace/grok47/senses/gk-scratch/gk1_trial.zag` | `5ba8401c5fe9e28e0fdd844899be2d81a27a132bfa590cb0de78799b42aa22e3` | identical | YES |
| 2 | `senses/web-search/v2/src/gk2_trial.zag` | P0 | 6329 | `~/workspace/grok47/senses/gk-scratch/gk2_trial.zag` | `a2e5cf050e05322be9fa5b8e9e84d5b71431ecc8c5d36ef1e8996f23d492152a` | identical | YES |
| 3 | `senses/web-search/v2/src/gk3_trial.zag` | P0 | 4235 | `~/workspace/grok47/senses/gk-scratch/gk3_trial.zag` | `a0cf18c323f11f515eda9cab71c1765592f381ea110a4f628be40689e23c7511` | identical | YES |
| 4 | `senses/web-search/internet-trial/evidence/phase1/blind-solo.jsonl` | P2 | 11986 | `~/workspace/tnn-lab/senses/web-search/internet-trial/evidence/phase1/blind-solo.jsonl` | `3f170f49e43806f8c8c583be43018283ccb1be64276487d4b49e89d84fb574ff` | identical | YES |
| 5 | `…/phase1/captured-solo.jsonl` | P2 | 11992 | same dir | `e3dbba2aeecaa9125811bb22fc8ad59a618ea956442ecf8afdf4bcdff8fb0691` | identical | YES |
| 6 | `…/phase1/corrupt-solo.jsonl` | P2 | 11990 | same dir | `0afa31acf6b801547830dfcd78fa227ad6864f6b205a1777d20cc10e6a994770` | identical | YES |
| 7 | `…/phase1/gullible-solo.jsonl` | P2 | 11994 | same dir | `8c86b1ca0ddec3a5f706a9701565273de9b1191c4ddebd209dfaabb5fcbba63e` | identical | YES |
| 8 | `…/phase1/idle-solo.jsonl` | P2 | 472 | same dir | `aca927cbf8825fbcdffb031adf0c12e49af57494ccc141c4ff620a6e128f460f` | identical | YES |
| 9 | `…/phase1/oracle-helper.jsonl` | P2 | 12687 | same dir | `b4328473f9a0cd8b78d596217b8500b6f3bd0a86b60630e1b43553ca3c701f4f` | identical | YES |
| 10 | `…/phase1/oracle-solo.jsonl` | P2 | 11989 | same dir | `d2ecdface4468316c90ebe676ec15ba680e0c021694f0c3e824a0945180581bc` | identical | YES |

- All 10 manifest paths are rooted at `docs/lab/` (per ITEMS_DONE.tsv).
- The jsonl files parse as valid line-delimited JSON trial-arm records
  (`arm/op/seq`, `SESSION_START`, `PRIOR_LOADED` claims); line counts:
  84/84/84/84/8/88/84.
- No other commit in branch history ever touched these paths before the
  recovery commits (confirmed via `commits?path=` API — only 16ddf755 and
  c9bd2b21 touch them; earlier finding of zero history corroborated).

## GK battery re-derivation (independent rebuild, pinned znc)

Build dir: `recovery/build/` — substrate `ws2_sense.zag` byte-identical to
frozen-committed (`sha256 49a370fda4d575f32efd431e652d769bd3d07828d4bd54c9658d7656c0e4ac0d`,
both copies) plus R33 natives + `cl/` from the worker's `gk-src/` dir.
Compiled gk1/gk2/gk3 with zero source edits (benign L0012 string-leak warnings
only). Deterministic: no RNG, no timestamps in any output line.

| Battery | Runs | Byte-identical | Run-output sha256 | Recorded headline | Match |
|---|---|---|---|---|---|
| GK1 | 3/3 | yes | `488af9ab375eae17cf65015240fb5c8a2f111ed6ca2eee354778b12b74a0db5c` | `488af9ab…` | YES |
| GK2 | 3/3 | yes | `7f351a53524d67fdb182357dcbf0215af526a6b70d7f6d66ce008d0c301fdf4b` | `7f351a53…` | YES |
| GK3 | 3/3 | yes | `94575a9a6c9e4aaa916676b6301a57d643c65f28d51d748f36492ac359814d13` | `94575a9a…` | YES |

Cross-checks vs the worker's recorded logs in gk-scratch (Sep 22 06:22):
`out/gk1_run1.txt` ≡ `gk-scratch/run1.txt`, `out/gk2_run1.txt` ≡
`gk-scratch/gk2_run1.txt`, `out/gk3_run1.txt` ≡ `gk-scratch/gk3_r1.txt`
(all cmp-clean).

Kill-bar adjudication re-derived from my independent build (matches
VERDICT_SHEET §3 tables exactly):
- **GK1 7/7 predicted outcomes**: GK1-3 installs (F1 not tripped → **H1
  SUSTAINED**); GK1-4 installs (**H2 SUSTAINED**); GK1-2/4/5 byte-identical
  FEAT vectors (**H3 SUSTAINED**); GK1-1 refuses (F5 ok), GK1-6 refuses
  (F6 ok); tamper=0 everywhere.
- **GK2 8/8 predicted outcomes**: GK2-8 refuses (G1 ok — content-blind),
  GK2-9 refuses (G2 ok), GK2-10 installs (Attack 6 CONFIRMED), GK2-11 installs
  (Attack 8 DEFEATED), GK2-12/13 install first-seen value (Attack 10
  tie-order finding), GK2-14 refuses (no canonicalization), GK2-15 refuses
  with tamper=1 (G7 ok — the only tamper flag, the designed positive
  control).
- **GK3 4/4 predicted outcomes**: GK3-10/14b refuse, GK3-10b/14 install
  (FIX-DOM + FIX-ANS accepted, no over-collapse/over-merge); tamper=0.

## Size-mismatch explanation (stale manifest, verdict-neutral)

| File | Manifest size | Committed size (frozen) | Local final copy | Committed ≡ local? |
|---|---|---|---|---|
| `senses/rematch/code/kb5.py` | 2189 | 2731 (blob `a88e20ca…`, API-verified) | 2731 (`~/workspace/senses-rematch/kb5.py`, 2026-09-22 07:19, sha256 `c1209b0e…`) | byte-identical |
| `senses/rematch/code/run_all.py` | 4302 | 5801 | 5801 (`~/workspace/senses-rematch/run_all.py`, 2026-09-22 05:22) | byte-identical |

- `git log --follow` on the frozen branch: both files were ADDED in the
  frozen commit `7b2100d0` itself — single-commit history, added in their
  final form. The manifest therefore measured pre-final drafts (before the
  worker's 07:19/05:22 edits) that were never committed and no longer exist
  anywhere locally. This is a stale-manifest artifact, NOT file corruption:
  the committed bytes are the authentic final worker outputs and the local
  workdir copy proves it.
- Verdict-neutral: the manifest's verdict fields (PASS/review-note) do not
  depend on sizes; no bar changes.

## Hunt record (completeness of the search)

- Frozen commit `7b2100d0`: exact 404s re-confirmed for all 10 paths (the
  coordinator's independent API check from Wave-2 stands; re-confirmed via
  contents API + commits-history search: zero history touches pre-recovery).
- Other branches (`main`, `fs-gr1`, `r2-7`, `reorg/phase-0-1`, `wg-freeze`):
  no commits touching these paths (org code search for the basenames =
  0 hits; commits?path= lists only the two recovery commits).
- Workspace: full find for `blind-solo.jsonl`/`oracle-solo.jsonl`/`oracle-helper.jsonl`
  and `internet-trial` dirs — the only sources are the two worker workdirs
  named above plus crossref clean-checkout mirrors of the frozen tree (which
  lack the files, as expected).
- Integrity note: `clean/tnn/` checkout was re-verified at HEAD
  `7b2100d09911c5c10252c5756c7def288e70bd1f` before and after this run;
  no vanishing-directory incident in this session. Prior crew state in
  `crew/` was read-only and is untouched.

## Disposition recommendation

The Wave-2 PARTIAL verdict was CORRECT against the frozen pin: at
`7b2100d09911c5c10252c5756c7def288e70bd1f` all 10 paths are genuinely absent,
and the frozen rule's named condition ("PARTIAL if any item's evidence is
missing") fired exactly as written. That part of the record stands as-is.

With this recovery, however, the underlying gap is fully remediated:
**140/140 manifest items' evidence now exists at tnn-native-lab HEAD with
manifest-exact sizes, and the load-bearing headline digests
(488af9ab…/7f351a53…/94575a9a…) re-derive byte-for-byte from an independent
pinned-toolchain build.** Recommended: coordinator re-runs the 140-item Type C
check at HEAD (or accepts this independent recovery record) and upgrades
T2-SENSESINT **PARTIAL → REPRODUCED**, with a note that at the frozen pin the
PARTIAL was correctly recorded. Nothing in this recovery required any source
edit, any re-interpretation of a bar, or any manual digest — the bytes speak
for themselves.

## Deliverables / artifacts

- `recovery/VERDICT.md` (this file)
- `recovery/RUNLOG.md` (every command, hash, API result)
- `recovery/build/` — build env: 3 trial sources + byte-identical sense
  substrate; `recovery/out/` — 9 run logs (3×3, all byte-identical within
  battery); `recovery/evidence/phase1/` — 7 recovered jsonl with
  `phase1_sha256.txt`; `recovery/headcheck/` — 10 HEAD-fetched blobs used for
  byte-verification; `recovery/src_sha256.txt`
