# VERDICT — T3-MA234 (memory-agency stages verification-of-record)

**Verdict: SPOT-REPRODUCED**

Crew: T3-MA234 · Date: 2026-09-24 (PDT) · Tier-3 protocol: verification-of-record + cheapest decisive spot reruns.

## Claims under test (from frozen prereg §T3-MA234, verified byte-identical on branch)
- **MA2 FALSIFIED (32/32):** staged training vs gifted full power gave identical refusal profiles; stages dropped as restraint-training, kept only as a destruction firewall during early training.
- **MA3 MIXED:** deliberate memory agency crushes the standard curriculum (30/30 vs 0–12 held) but loses the adversarial one (cannot express negative judgments about memories).
- **MA4 ANSWERED:** signed memory values — 18/18, 30 vs 9 on the adversarial curriculum.

## Verification-of-record
- Frozen prereg `docs/lab/crossref/PREREG_TIER3.md` on tnn-native-lab: blob `943ab5c9…`, sha256 `538121d2cd56bd0ee25594548b4daa1bd9cc603a6c5f7d07a933347f463afdc1` — byte-identical to the local frozen copy. Section "## T3-MA234" extracted programmatically.
- Verdict commits resolve on tnn-native-lab and are ancestors of current head `8eb94a4c`:
  - MA2/MA3: `624f6e33c141` (2026-09-19, "lab(wave2): MA2 falsified (staging != restraint), MA3 mixed")
  - MA4: `6dc7fcd0c379` (2026-09-20, "lab(wave3): 20 post-toy investigations")
- Damage/repair survived byte-identically: the bad surgery `308bf365` (2026-09-23) deleted the MA files; repair `3b011ef18e0a` restored all 8 trial blobs to exactly their verdict-commit SHAs (`ma2_trial.zag` b59ddcb2…, `ma3_trial.zag` 1e6a645c…, `ma_common.zag` 58e90e7b…, `memory_core.zag` 90c8777b…, runners f49d2f6f…/d87530fe…, `ma4_trial.zag` d7764197…, `run_ma4.sh` 57d97b8c…, substrate tree 6dc76e02461d identical in both trial dirs). Re-hashed locally via `git hash-object` in a clean clone — all match.

## Spot reruns (committed sources, clean checkout, pinned znc_linux_x86_64_abed8aa1)
**MA2 discrimination cell — STAGED vs GIFTED refusal profile** (verdict code state, 2 runs, stdout byte-identical sha256 `584ee02d…`):
- `CL_CHECK` 5/5 pass; `MA2_STAGED,rate_per100,0,pinret,195,195,replay,0,kills_total,3` and `MA2_GIFTED,rate_per100,0,pinret,195,195,replay,0,kills_total,3` — identical refusal profiles; unlock step 162 on rerun; `MA2_VERDICT,FALSIFY_IDENTICAL_DROP_STAGES`. Verdict figures (1 refusal each, 0/100, 195/195 retention, 3 kills each, clean replay) reproduced exactly.
**MA3-vs-MA4 adversarial discrimination cell** — BASE arm is MA3's AGENCY policy verbatim; reran the full MA4 trial from committed sources, 2 runs, stdout byte-identical (sha256 `a1d86dd2…`):
- All 18 `CL_CHECK`s pass, `MA4_FAILURES,0`, `MA4_VERDICT,CONFIRM_SIGNED_SUPERIOR`.
- Adversarial cells (cur=1, variants 0/1/2): BASE/MA3 holds **9, 9, 9** important; SIGNED/MA4 holds **30, 30, 30** — the 30-vs-9 figure. Standard cells: BASE 30/30, SIGNED 30/40,30/37,30/49 (held 30, non-inferior). Mechanism evidence also reproduces: trap-feature trust BASE 0,0,0,0 (clamped floor) vs SIGNED −244…−255.
- Zero RNG in decision paths: static check passes; byte-identical reruns confirm determinism.
- MA3's MIXED disposition verified of record against its committed `TRIAL_RESULTS_MA3.md` (standard 30 vs 0, 3/3 seeds; adversarial AGENCY 10–11 vs AUTO 30, 3/3 seeds) — the BASE arm here *is* that MA3 policy, so its adversarial loss is reproduced inside this run.

## Rule application
Prereg rule: REPRODUCED if the three dispositions (falsified / mixed / answered) and the 18/18 + 30-vs-9 figures hold; NOT REPRODUCED if any disposition flips. All hold. MA2's falsification and MA4's answer are spot-reproduced; MA3's mixed disposition is verified of record with its adversarial loss reproduced through the MA4 baseline arm.

## Anomalies
- Branch head moved during work (was `16400e32`, landed on `8eb94a4c` after a sibling crossref crew's T3-MA1 commit). Blob SHAs were verified before and after; unaffected.
- Lab sources live under `docs/lab/` in the repo (the working box maps 1:1 to it); the truncated recursive-tree API misleads — descend subtree-by-subtree instead.
- The wave3/signed-memory-values `ma_common.zag` and `memory_core.zag` are byte-identical copies of the wave2 MA3 originals (58e90e7b392e / 90c8777b57b2), as the verdict doc claims ("copied, not rewritten") — confirmed by blob SHA.

No binary or cache was committed. VERDICT_TABLE.md untouched (parent adds the row).
