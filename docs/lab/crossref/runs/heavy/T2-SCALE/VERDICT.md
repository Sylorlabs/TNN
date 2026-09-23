# VERDICT — T2-SCALE crossref (Type B anchor replication)

**Verdict: REPRODUCED.**

Frozen authority: `PREREG_TIER2.md` "## T2-SCALE — scale-up" section
(sha256 `90070c88…dade4a9f`, recorded in RUNLOG.md). Rule: REPRODUCED if
anchor+mid-scale numbers match exactly; NOT REPRODUCED if any differs;
PARTIAL if mastery holds but cost accounting differs.

## What was re-run

- Clean sparse checkout of Sylorlabs/TNN @ pinned evidence commit
  `9a17fec572d295ea680a5abec4f6ce294efacd02` ("Scale-up verdict:
  6,585,360-fact ceiling run complete, all kill bars untripped").
- Driver rebuilt from the pinned blob `docs/lab/scale/driver/scale_learner.zag`
  (sha256 `cbec9a5f…abc2a00`) with the pinned toolchain
  `znc_linux_x86_64_abed8aa1` (`--no-analyze`). Zero RNG; pure Zag.
- Corpus: corpus texts (`text_0..9.txt`, `index_0..9.tnix`, `meta.json`) are
  NOT in the pinned commit — but all 33 pinned SHA256s in the committed
  `corpus/MANIFEST.json` were re-verified against a corpus copy on this VM:
  33/33 match. The input corpus is byte-identical to the pinned corpus.
- Mid-scale point chosen: S3, N=240,000 (M=10,000) — the cheapest scale ≥100K
  facts with a completed committed leg, per the prereg.
- Honest limit (per prereg): the 6.58M sweep was NOT re-run.

## Numbers

Anchor (N=240, eval 240 24 10 1, 3 reps, byte-identical):

| measure | replicated | committed |
|---|---|---|
| clean mastery | 226/226 = 1.0000 | 226/226 = 1.0000 |
| all-fact | 226/240 = 0.9417 | 0.9417 |
| decile d0 / d9 | 22/22, 24/24, gap 0 | 1.0 / 1.0, gap 0 |
| absorption | 14/14 | 14/14 |
| flaw battery | 96/96 | 96/96 |
| ops/fact | 4.004 (ops_per_fact_x1000=4000+1 amortized audit) | 4.004 |
| B/fact | 92 (24 slot + 4 index + 64 audit) | 92 |
| reruns byte-identical | 3/3 | 5/5 (committed run; all reps identical here) |

Mid-scale (N=240,000, eval 240000 24 10000 1): rep-0 output log is
**byte-identical** to the committed `docs/lab/scale/runs/s3_r0.log` at the
pinned commit (`cmp` clean, sha256 `17d5ee80…0fdb656` both sides) — so every
committed number holds exactly:

| measure | replicated | committed |
|---|---|---|
| clean mastery | 227965/227965 = 1.0000 | 227965/227965 = 1.0000 |
| all-fact | 227965/240000 = 0.9499 | 0.9499 |
| decile d0 / d9 | 22841/22841, 22775/22775, gap 0 | 1.0 / 1.0, gap 0 |
| absorption | 12035/12035 | 12035/12035 |
| flaw battery | 96/96 | 96/96 |
| ops/fact | 4.000 (ops_per_fact_x1000=4000) | 4.000 |
| B/fact | 92 | 92 |
| reruns byte-identical | 3/3 (all three match committed log byte-for-byte) | 3/3 |

## Verdict

**REPRODUCED** — every committed headline number at the anchor and mid-scale
points matches exactly, including byte-identical output vs the committed run
log at S3. No kill bar tripped (mastery gap 0, ops exactly linear, determinism
held). The 6.58M ceiling leg was not re-run (preregistered honest limit).

## Anomalies / notes

1. Corpus texts not in pinned commit (input corpora pinned by SHA in
   MANIFEST.json, not by git blob) — resolved by SHA-verifying a local copy
   against the pinned MANIFEST (33/33 match). SCOPE §2.2 compliant: inputs
   taken via the pinned SHAs.
2. Branch head moved between API check (`283034e9`) and clone fetch
   (`293602fb`) — recorded in RUNLOG; the pinned commit is unaffected.
3. Runtime hiccup: two foreground exec registrations timed out ("failed to
   store metadata for session"); commands were retried via background mode
   and succeeded. No results lost.
