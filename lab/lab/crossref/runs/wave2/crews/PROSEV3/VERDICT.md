# T2-PROSEV3 Replication Verdict — TNN Prose v3 (KB3-VIABLE)

**Crew:** T2-PROSEV3 (Wave-2 Tier-2 clean-environment replication)
**Date:** 2026-09-23
**Replicates:** prose v3 evidence pin `4be6b0cf128d`, PREREG3, VERDICT.md

## Verdict: REPRODUCED

The preregistered claim — **KB3-VIABLE FAIL (2/4)** with the documented
deviation footprint — is **fully reproduced** from a clean rebuild.

**Rule applied** (`PREREG_TIER2.md` §T2-PROSEV3):
`REPRODUCED` iff FAIL 2/4 **and** the deviation footprint match;
`PARTIAL` if the deviation impact differs. Both conjuncts hold.

## Frozen pins (all verified)

| Pin | Value |
|---|---|
| Prereg branch | `tnn-native-lab` |
| Frozen prereg commit | `7b2100d09911c5c10252c5756c7def288e70bd1f` (API-verified, 2026-09-22T22:54:44Z) |
| Evidence commit (prereg-named) | `4be6b0cf128d5a443c9e67486f63520816535cca` (API-verified, 2026-09-22T03:28:39Z; message states `KB3-VIABLE FAILS (2/4)`) |
| Pinned compiler | `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` |
| v3 source tree @evidence | `2b151cac83bdb232d2fa77711973585fbfdd736d` |
| v2 source tree @both pins | `380d2339e34fa8df1fa685163799f10b56471158` |

## Rebuild fidelity (strongest form)

Both binaries were rebuilt from the committed `.zag` sources with the pinned
znc. The resulting binaries are **byte-identical** to the SHAs recorded in the
committed `src/PROOF.md`:

| Binary | Rebuilt SHA-256 | Committed SHA-256 | Match |
|---|---|---|---|
| `prose_learn3` (v3) | `a5cff7c…8b4ae82dc72` | `a5cff7c…8b4ae82dc72` | **YES** |
| `prose_learn2` (v2) | `8dbb02f…b59d5369697e` | `8dbb02f…b59d5369697e` | **YES** |

(Full SHAs in RUNLOG.md.) All 303 packaged files verify against the committed
`checksums.sha256` (303/303 OK).

## Battery replication: 220/220 logs byte-identical

All four legs were rerun from committed sources in a clean checkout
(`crew/runs/`), 5 reps per run (4 championship sources × 5 + 7 sub-batteries × 5
= 55 logs/leg):

| Leg | Binary / mode | Rep determinism | vs committed logs |
|---|---|---|---|
| A0 | v2, single-exposure | 55/55 5/5 byte-identical | 55/55 byte-identical |
| A1 | v2, dense | 55/55 5/5 byte-identical | 55/55 byte-identical |
| A2 | v3 m1 (dense+coref) | 55/55 5/5 byte-identical | 55/55 byte-identical |
| A3 | v3 m2 (full) | 55/55 5/5 byte-identical | 55/55 byte-identical |

Zero RNG anywhere. `TMPDIR` kept on workspace scratch (never `/tmp`).
No binaries or `.zagd` files are part of the deliverables.

## Headline: KB3-VIABLE FAIL (2/4) — reproduced

Clean mastery per source (independent Zag verifier, `crew/build/verify/verify3`):

| Leg | grok | sol | step | muse-native |
|---|---|---|---|---|
| A0 (frozen v2, single) | 59/228 | 65/228 | 75/228 | 144/228 |
| A1 (frozen v2, dense) | 59/228 | 77/228 | 87/228 | 158/228 |
| A2 (v3 m1) | 59/228 | 77/228 | 87/228 | 158/228 |
| A3 (v3 m2) | 183/228 | 204/228 | 208/228 | 227/228 |
| Frozen v1 (pinned, not rerun) | 189/228 | 220/228 | 204/228 | 200/228 |

A3 beats v1 on **step** (208 > 204) and **muse-native** (227 > 200) only:
**2/4 → KB3-VIABLE FAILS**. The frozen A0/A1 baselines are unchanged, so no
scored headline moved. All figures match the committed VERDICT.md exactly.

## Deviation footprint — reproduced in full

**1. CORE 11/24 → 22/24 with 5/6 attribution.**
Per-id analysis of the replicated A1→A2 sub_core logs: exactly the 11 probe
ids fixed are `{2,3,5,7,9,10,13,16,17,18,23}` (zero regressions); residual
misses `{19,21}` in both A2 and A3, as predicted. Causal confirmation: a
diagnostic build of `prose_learn3.zag` with **only** the unregistered trigger
expansion removed (narrow `it/this/that` trigger, order change kept) scores
16/24 on sub_core, fixing exactly `{2,5,9,10,13}` — the 5 registered items.
The remaining 6 fixed items `{3,7,16,17,18,23}` are therefore caused by the
unregistered expansion (`its/these/those` + `"the word"`/`"the letter"` bigram),
whose train sentences use the bigram where the 5 use `that`/`this`. **5
registered + 6 unregistered = 11. Footprint matches.**

**2. Wrong-value verdicts 8 → 30 per 912 clean probes.**
Independent Zag count: A1 = 8/912, A3 = 30/912 (+22). Matches.

**3. Unknown/other misses 523 → 60 (≈463 converted).**
Independent Zag count: A1 = 523/912, A3 = 60/912; difference = 463 unknowns
converted into values. Matches.

Supporting measurements (all match the committed verdict):
SUB-CORE 11/24→22/24, SUB-DISTR 65/240→199/240, PARA 48/48, CONTR 24/24,
MULTI 24/24, HEDGE 19/24, NEG 34/36 (2 value leaks), KB3-NOSILENT total
value_leaks = 2, ABS-3 falsehood absorption 9/12, 11/12, 11/12, 11/12
(grok/sol/step/muse-native).

## Method notes / deviations from the committed driver

- The committed `run_legs.sh` relied on working-tree symlinks
  (`inputs3_v2single/false_ids_*`) that were excluded from the evidence
  package. For A0 the replication used the committed **frozen v1 inputs**
  (`docs/lab/prose-learning/inputs/false_ids_<s>.txt` @4be6b0cf128d;
  blob-identical at the frozen prereg pin), which reproduces the committed
  A0 `clean=59/228`-style SUMMARY denominators exactly.
- The committed `run_legs.sh` ran 3 sub-battery reps; the evidence package
  contains 5. This replication ran **5 reps everywhere** (stronger than both).
- Scoring replicates the committed `score_legs.py` logic exactly, with the
  live-tree hardcoded path replaced by the committed frozen v1 inputs; the
  authoritative counts were additionally established by **independent pure-Zag
  code** (`crew/build/verify/verify3.zag`, built with the pinned znc), which
  agrees with the Python scorer on every figure. `assert_all.sh` runs 17
  Zag-verified assertions — all pass.

## Conclusion

**REPRODUCED.** KB3-VIABLE FAIL (2/4), and the full deviation footprint —
6/11 CORE from the unregistered expansion (causally isolated), wrong-value
verdicts 8→30/912, ~463 unknowns converted to values — all match the
preregistered claim with byte-identical logs and byte-identical binaries.
