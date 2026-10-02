# T2-SENSESINT — EVIDENCE RECOVERY VERDICT (2026-09-23)

**Recovery coordinator:** Wave-2 crossref T2-SENSESINT evidence recovery.
**Authority:** frozen `RECOVERY_PREREG.md` (committed ALONE at `a94cc0e7a4025edfb41635a15ec008176fe82b90`
before any recovery run), per `CLOSEOUT_WAVE2.md` §3; frozen rule (Tier-2 prereg
`@ 7b2100d09911c5c10252c5756c7def288e70bd1f`): **REPRODUCED if 140/140 re-derives;
PARTIAL if any item's evidence is missing (name it).**
**Verdict: REPRODUCED** — all 140 manifest evidence paths resolve at head with
matching sizes; the 3 headline digests re-derive byte-for-byte from the committed
sources.

## What was recovered vs regenerated vs downgraded

| Item | Disposition | Evidence |
|---|---|---|
| `senses/web-search/v2/src/gk1_trial.zag` (P0, 5285) | **RECOVERED** (restored, not regenerated) | Frozen crew workdir `~/workspace/grok47/senses/gk-scratch/gk1_trial.zag`, byte-identical (sha256 `5ba8401c5fe9e28e0fdd844899be2d81a27a132bfa590cb0de78799b42aa22e3`), size 5285 exact. Git history: zero commits ever for this path (never committed, workdir-resident only). |
| `senses/web-search/v2/src/gk2_trial.zag` (P0, 6329) | **RECOVERED** | Same workdir, byte-identical (`a2e5cf050e05322be9fa5b8e9e84d5b71431ecc8c5d36ef1e8996f23d492152a`), size 6329 exact. Zero commits ever for this path. |
| `senses/web-search/v2/src/gk3_trial.zag` (P0, 4235) | **RECOVERED** | Same workdir, byte-identical (`a0cf18c323f11f515eda9cab71c1765592f381ea110a4f628be40689e23c7511`), size 4235 exact. Zero commits ever for this path. |
| 7× `senses/web-search/internet-trial/evidence/phase1/*.jsonl` (P2) | **RECOVERED** | Workdir `~/workspace/tnn-lab/senses/web-search/internet-trial/evidence/phase1/`; byte sizes match manifest exactly (11986/11992/11990/11994/472/12687/11989); every line parses as valid JSONL (arm/op/seq trial-arm records). Zero commits ever for these paths. |
| P2 downgrade rule | **NOT NEEDED** | All 7 recovered; no written downgrade justification required. |
| `senses/rematch/code/kb5.py` size 2189→2731 | **MANIFEST CORRECTED** | Committed bytes verified at head AND at pinned rematch commit `1c01a1ad`: exactly 2731B (independent T2-REMATCH crew used these exact bytes). Manifest measured a stale revision. |
| `senses/rematch/code/run_all.py` size 4302→5801 | **MANIFEST CORRECTED** | Committed bytes verified at head AND at `1c01a1ad`: exactly 5801B. Same rule. |
| `redteam/bar-audit/PROPOSED_BARS.md` size 11587→11846 | **MANIFEST CORRECTED (new find)** | Full 140/140 verification found a THIRD stale size the closeout checker missed: manifest measured the `abaa5c7b57` revision (11587); commit `1e1080dc57` (2026-09-22, N9 reword fix) legitimately grew it to 11846 after the crew's verification; committed bytes 11846 at closeout snapshot `fa29b249`, at repair `3b011ef18e`, and at head. Committed bytes are the live revision. |

Nothing was "regenerated" from scratch: every restored byte is the crew's own
frozen artifact, and the GK sources were restored with **zero edits**.

## Digest re-derivation (the honest bar)

Built the COMMITTED sources fresh from the repo (API fetch → sha256-verified
byte-identical to workdir originals) with the pinned toolchain
`znc_linux_x86_64_abed8aa1` against the committed frozen `ws2_sense.zag`; N=3
runs each, zero RNG:

| Trial | Headline digest (frozen) | Re-derived (3/3 byte-identical) | Match? |
|---|---|---|---|
| GK1 | `488af9ab…` | `488af9ab375eae17cf65015240fb5c8a2f111ed6ca2eee354778b12b74a0db5c` | **YES, byte-for-byte** |
| GK2 | `7f351a53…` | `7f351a53524d67fdb182357dcbf0215af526a6b70d7f6d66ce008d0c301fdf4b` | **YES, byte-for-byte** |
| GK3 | `94575a9a…` | `94575a9a6c9e4aaa916676b6301a57d643c65f28d51d748f36492ac359814d13` | **YES, byte-for-byte** |

Re-derived outputs are also byte-identical to the crew's original run logs
(`run1.txt`, `gk2_run1.txt`, `gk3_r1.txt` in `gk-scratch/`). Case-level outcomes
match VERDICT_SHEET §3 exactly (GK1: R8 on GK1-1/6, R7 on the rest; GK2: R8 on
GK2-8/9/14/15, R7 on the rest; GK3: R8 on GK3-10/14b, R7 on 10b/14). Kill bars
hold: tamper=1 ONLY on GK2-15 (the positive control); GK1 7/7, GK2 8/8, GK3 4/4
predicted outcomes matched; N=3 runs byte-identical (determinism bars F7/G8/K5
clear).

## 140/140 verification

Method: recursive subtree trees (`docs/lab/senses`, `redteam`, `info-source`,
`mixed-web`) fetched from the GitHub API at head, untruncated; every manifest
path checked for presence and size equality against the amended ITEMS_DONE.tsv.
Result at verification time: **140/140 present, 140/140 sizes match** (tree SHAs:
senses `be4d760c…`, redteam `20f35142…`, info-source `9e970f81…`, mixed-web
`001b26b9…`). The 10 restored paths all resolve; the 3 amended sizes all match.

## Commits (branch `tnn-native-lab`, via `commit_racefree.py`, TMPDIR set)

| # | Commit | Content |
|---|---|---|
| 1 | `a94cc0e7a4025edfb41635a15ec008176fe82b90` | Frozen RECOVERY_PREREG.md, alone |
| 2 | `16ddf755fee7ab41765d961f01e0d2a3f0f2c875` | 3 GK trial sources at exact manifest paths |
| 3 | `c9bd2b210f781eb60bc9ebcaa1a280225a758184` | 7 P2 phase1 jsonl at exact manifest paths |
| 4 | `0e9b6ccf5eb42915fca58e9fcf0be49b1c0cc759` | ITEMS_DONE.tsv: kb5.py 2189→2731, run_all.py 4302→5801 |
| 5 | `79fb9a7b9b1494235b2b11e651a8107c8246fca7` | ITEMS_DONE.tsv: PROPOSED_BARS.md 11587→11846 (new find) |
| 6 | *(this commit — SHA recorded in the coordinator's final report)* | recovery verdict + verdict upgrade |

## Upgrade decision

**T2-SENSESINT: PARTIAL → REPRODUCED.** The frozen rule's named condition for
PARTIAL ("any item's evidence is missing") no longer holds: 140/140 evidence
paths resolve with matching sizes, and the load-bearing GK digests re-derive
byte-for-byte from the committed sources with zero edits. No P2 downgrades were
needed. The crew's original PARTIAL verdict stands as an accurate record of the
committed evidence at closeout time; this amendment records what changed.

## Honest limitations

1. **Recovery is restore, not independent re-implementation.** The GK sources are
   the original crew's bytes (proven by manifest sizes + digest re-derivation),
   not a from-spec reimplementation. If the original workdir had been tampered
   with, the digest match would be the tripwire — it matched, so the bytes are
   the genuine trial sources.
2. **Scratch verification preceded the frozen prereg.** Diagnostic builds/runs
   happened before RECOVERY_PREREG.md was committed (evidence-gathering for the
   honest bar); the prereg's rules were fixed from the manifest/closeout/frozen
   prereg, not shaped by the outcome, and the committed-source rerun above was
   done after the prereg from fresh repo fetches.
3. **Branch moves underfoot.** Other crews commit to `tnn-native-lab`
   concurrently (all six commits above landed on different parents via the
   race-tolerant path). The 140/140 verification is a snapshot at the listed
   tree SHAs; a later concurrent commit could in principle touch a manifest
   path — the parent should re-run the cheap tree check before closing the
   track in VERDICT_TABLE.md.
4. **The closeout checker missed PROPOSED_BARS.md.** Its 140-item size sweep
   caught only 2 of 3 stale sizes. Any future "all sizes match" claim should be
   re-verified from scratch, not trusted from the closeout record.
5. **No live-web recapture** (Type C track) — the internet-trial jsonl are the
   crew's recorded trial arms; their content was validated (JSONL parse +
   schema), not re-executed against the live web.
