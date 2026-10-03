# T2-SPEECHACT crossref verdict: **REPRODUCED**

Crew: T2-SPEECHACT heavy (Type A full independent rerun, clean environment), 2026-09-23 PDT.
Frozen prereg: `crossref/PREREG_TIER2.md` §T2-SPEECHACT
(sha256 `90070c88e43aecb6ba3ee8df6d487f7bf1b1673bb12d3ad8dcd11d597ade4a9f`, frozen 2026-09-22).

Evidence pins (all API-verified, all ancestors of tnn-native-lab at run time):
- PoC `fabb003e263c` (2026-09-22 10:45 PDT): `delib_sa.zag` blob `6f08e0932e…`
- Volume `291bbf75785b` (2026-09-22 11:05 PDT): `delib_vol.zag` blob `a5de27048e…`
- Decline investigation `188e9a6ad068` (2026-09-22 11:33 PDT): `delib_cnt.zag` blob `3a7d813fb4…`
- WHY_SARCASM `a761584b` (2026-09-22 13:36 PDT): `delib_sarc.zag` blob `20a5ae63ee…`
- Implicature `90ddad64` (2026-09-22 13:43 PDT): `delib_impl2.zag` blob `0434090ad9…`
Substrate (IO/sha256) from committed blobs at the pins: `a6b440d2564…` (Linux-port
R33_NATIVE_IO_V1, committed under docs/lab/GROK47_OVERNIGHT/… at the pins;
identical to the live copy used by the original crew), `5dd858fa1097…` (R33_NATIVE_SHA256_V2).
Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` for all builds.

## Method

Clean full clone of sylorlabs/TNN (branch tnn-native-lab) into
`~/workspace/scratch-crossref/T2-heavy/T2-SPEECHACT/clean/` (HEAD at clone:
`b09df71bf6c273a6bde77881fa72c72415f54797`; post-fetch remote head
`1cc0913c98e7dbdf48fbf19b1dacc4844b6df187`; all pins ancestors of both).
Each wave's `speechact_exp/` tree extracted via `git archive` from its pinned
commit; driver blobs hash-verified before extraction (all 5 match). Binaries
rebuilt fresh with the pinned znc in a cwd-mirrored work tree (pure Zag, zero
RNG; no `.zagd`/binaries reused or copied between environments). Every cell run
3 reps; intra-run byte-identity checked, and rep1 diffed byte-for-byte against
the committed `scored_evidence/`.

Anomaly noted (not blocking): tnn-native-lab HEAD moved twice during the run
(active branch, 317+ commits since the pins, including a reorg that removed
`docs/lab/prose-learning/` from the head tree). Pins remain in history and were
used directly, so the evidence path is clean.

## What reproduced

| Claim (frozen) | Measured | Result |
|---|---|---|
| PoC: 7.1%→50.0% weird-English | Arm1 5/70 (7.1%), Arm2 35/70 (50.0%); 6/6 cells byte-identical ×3, rep1 byte-identical to committed | **PASS** |
| PoC per-family (arm2) 5/3/5/3/9/5/5 | joke 5/10, sarcasm 3/10, hypothetical 5/10, analogy 3/10, counterfactual 9/10, poetry 5/10, implicature 5/10 | **PASS** |
| Both arms 12/12 falsehood withholds | 12/12 both arms, both legs | **PASS** |
| Both arms fail frozen 8/10/family | arm1 0/7 families pass, arm2 1/7 (counterfactual 9/10) | **PASS** |
| Markers hand-specified, not learned | SPEECH_ACT_KNOWLEDGE.md reviewed; delib_sa matches committed blob | **PASS** |
| Volume: 60/60 cells byte-identical ×3 | 63/63 run cells 3/3 identical (60 committed cells all byte-identical to committed; 3 r0-orderswap cells uncommitted but identical) | **PASS** |
| Volume curve 7/61/76/67/60/51/50 @0/1/2/4/8/16/32 | withheld/70: 5, 43, 53, 47, 42, 36, 35 | **PASS** |
| Transfer control: sarcasm-only degenerate (poetry 10/10 + all 12 true controls withheld) | sarconly r32: poetry W089–W098 10/10 WITHHOLD; b12_true 0/12 endorsed | **PASS** |
| Decline re-scoring: count rule flips decline → rise (17→38) | bar_cnt: 5/8/17/27/32/27/38 (r2=17 → r32=38, rise; no decline) | **PASS** |
| Corrected curve monotone 5→8→21→24→30→32→38 | cntdiv: 5, 8, 21, 24, 30, 32, 38 — strictly monotone | **PASS** |
| 12/12 controls intact under cnt & cntdiv | 12/12 false + 12/12 true at r2 and r32, both | **PASS** |
| 110 decline cells ×3 byte-identical to committed | 330/330 files byte-identical vs committed scored evidence | **PASS** |
| Implicature pragmatic-frame 3/10→≤5/10, legs intact | f2: implicature 2–5/10 (peak 5/10 @r4), 12/12 both legs r2+r32 | **PASS** |
| Richer slot-abstraction 7/10 inadmissible (broke true controls 4/12 @r2) | f3: true leg 4/12 @r2, 10/12 @r32 (broken, as reported) | **PASS** |
| H3 cues survive (markers 0/10→10/10; context 3/10→10/10) | marked 10/10 vs base 0/10; ctx 10/10 vs base 3/10 | **PASS** |
| H4 speaker model survives (5/10→10/10, only genuine-vs-sarcastic fix) | speaker 10/10 vs base 5/10 | **PASS** |
| H5 inversion opacity survives | best genuine-discrimination 5/10 in every mode | **PASS** |
| H1 layering killed (Δ=0) | layered_bare 3/10 = base_bare 3/10 | **PASS** |
| H2 truth-machinery "blocks" killed; wrong-reason masking confirmed | notruth_bare item-identical to base_bare; litfalse 10/10 reason F | **PASS** |
| Implicature context wave: I1 12/12, I2 6/6 pairs, K-IM1 no-hardcode, K-IM2 3/3 identical | 12/12; all 6 pairs discriminate; verify_impl.py OK; byte-identical, committed-identical | **PASS** |

## Kill bars (decline investigation, from DECLINE_INVESTIGATION.md, rechecked)

- H-D1 (fixed-bar artifact) SURVIVES: count rule 17→38 rise; b2 score-only reproduces the
  original decline (53→35) while legs hold 12/12 → the score gate's prevalence term drives it.
- H-D2 (quality/redundancy) KILLED on substance: max-diversity ordering declines 18 items
  (steeper than redundant's 13).
- H-D3 REDIRECTED: B3 (disc-only) rises to 69/70 but breaks the true leg (7/12 @r32) —
  reported broken, not a win.
- H-D4 (front-end fixes implicature) KILLED as preregistered: F2 peaks 5/10 with legs
  intact; F3's 7/10 inadmissible (true leg 4/12).

## Caveats

- The reorg at tnn-native-lab head removed `docs/lab/prose-learning/`; all evidence
  was taken from pinned history commits, never from the live tree. Blob hashes verified.
- Substrate `R33_NATIVE_IO_V1.zag` was never committed under `prose-learning/`;
  the Linux-port copy used matches committed blob `a6b440d2564…` (GROK47_OVERNIGHT tree)
  and the live file the original crew built against, byte-for-byte.
- McNemar p-values (r2→r32 p=5.7e-6 etc.) are committed analysis, not recomputed here;
  the underlying cell counts that drive them are reproduced exactly.
- No partial legs: every frozen claim re-ran and matched. Nothing missing.

**Verdict: REPRODUCED** — every frozen number, curve, control leg, and hypothesis
disposition held byte-for-byte against committed evidence in a clean environment.
