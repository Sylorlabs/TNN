# RUNLOG — T2-SCALE heavy-family crossref crew (Type B anchor replication)

Crew: T2-SCALE crossref (subagent session d135ed66-…, parent 40ae779d-…).
Frozen authority: `~/workspace/tnn-lab/crossref/PREREG_TIER2.md`
("## T2-SCALE — scale-up" section, extracted programmatically below).

## Frozen prereg record

- prereg sha256: `90070c88e43aecb6ba3ee8df6d487f7bf1b1673bb12d3ad8dcd11d597ade4a9f`
  (file byte-identical copy — verified 2026-09-23; matches Wave-2 frozen value)
- Section extract (sed, not retyped):

```
# Cross-reference preregistration — TIER 2 (committed 2026-09-21/22 verdicts)

**Frozen:** 2026-09-22 (PDT), with `SCOPE.md`. One clean-environment crew per family unless noted; cross-reference = the replication's numbers vs the committed values (byte-identical digests must match exactly). Type A/B/C per family below. Wave 2 execution; heavy families (T2-SCALE, T2-THROUGHPUT) run Type B and never concurrently on this VM.

---

## T2-SCALE — scale-up: nothing broke to 6,585,360 facts (Type B)

**Claims:** clean mastery 1.0000 from 240 to 6,585,360 facts (24 categories × 274,390; every word position of all 10 Gutenberg texts); flaw battery 96/96 at every completed scale; zero forgetting (first/last decile 1.0, gap 0); all-fact 0.9501; absorption 328,532/328,532; cost exactly linear (4.000 ops, 92 B/fact from 2,400 up); byte-identical reruns; no kill bar tripped; run stopped at corpus ceiling. Honest caveats: millions of facts, not billions of tokens; planted falsehoods absorbed at 1.0 at every scale (consistent lies go in smooth).
**Evidence:** commit `9a17fec572d2`, `docs/lab/scale/`.
**Method:** anchor replication — rerun the 240-fact anchor and one mid-scale point (crew picks the cheapest scale ≥100K facts that the committed evidence shows as a completed leg) with the same measurement method in a clean checkout; verify mastery 1.0000, 4.000 ops, 92 B/fact, byte-identical reruns at those points. Do NOT re-run the 6.58M sweep; state the honest limit.
**Rule:** REPRODUCED if anchor+mid-scale numbers match exactly; NOT REPRODUCED if any differs; PARTIAL if mastery holds but cost accounting differs (name it).
```

- tnn-native-lab branch head (via GitHub API, 2026-09-23): `283034e917eb343dccae805475eeeb6b6feda85c`
- Pinned evidence commit (verified exists, msg "Scale-up verdict: 6,585,360-fact ceiling run complete, all kill bars untripped"):
  `9a17fec572d295ea680a5abec4f6ce294efacd02`
- Toolchain sha256 (pinned znc): `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`

## Targets (committed values to reproduce)

- Anchor S0: N=240 (C=24, M=10): clean 226/226=1.0000, all-fact 0.9417, flaw 96/96, absorption 14/14, ops 4.004/fact (one amortized audit entry), 92 B/fact, 5/5 byte-identical.
- Mid-scale S3: N=240,000 (C=24, M=10,000): clean 227965/227965=1.0000, all-fact 0.9499, flaw 96/96, absorption 12035/12035, ops 4.000/fact (ops_per_fact_x1000=4000), 92 B/fact (24+4+64), 3/3 byte-identical.

Note on rule reading: prereg says "verify mastery 1.0000, 4.000 ops, 92 B/fact" at
both points; committed table records anchor ops as 4.004 (known amortized-audit
artifact at N=240, also committed). Match target = committed values: anchor 4.004, mid 4.000.
Anything else differs → NOT REPRODUCED per rule.

## Plan

1. Clean sparse clone of Sylorlabs/TNN @ pinned commit 9a17fec572d2 (docs/lab/scale/ only),
   verify blob SHAs.
2. Build scale_learner.zag from the pinned blob with pinned znc (--no-analyze).
3. Run anchor: `scale_learner eval 240 24 10 1 <rep> <texts_dir>` ≥3 reps → diff byte-identity.
4. Run mid-scale: `scale_learner eval 240000 24 10000 1 <rep> <texts_dir>` ≥3 reps.
5. Compare every committed number; write VERDICT.md; commit VERDICT+RUNLOG.

Honest limit (prereg): do NOT re-run the 6.58M sweep.

## Execution log

2026-09-23 ~08:30 PDT
- Sparse blobless clone of Sylorlabs/TNN → checkout @ pinned commit
  9a17fec572d295ea680a5abec4f6ce294efacd02 (HEAD verified). Pinned driver
  sha256 cbec9a5f4147c468ba8417655c1a23d24e842eaf891248e461a501fbdabc2a00.
- Corpus texts not present in pinned commit; a 33/33 SHA256 re-verify of
  /home/hatch/workspace/scale/corpus against pinned MANIFEST.json passed —
  corpus used = pinned corpus byte-for-byte. Copied texts → runs/texts/.
- Built scale_learner from the pinned blob with pinned znc (--no-analyze):
  native ELF 124,249 bytes, ~18.5s compile.
- Anchor N=240, eval 240 24 10 1, 3 reps: all rc=0, sha256
  0f484465e8ab01e212a0fe7f3066493a90a9051ce102068857c97f5abd127ea9 (3/3
  identical). Measures: clean 226/226=1.0000, all-fact 0.9417, deciles
  22/22 & 24/24 gap 0, absorption 14/14, flaw 96/96, ops_x1000=4004 (4.004),
  mem 92 B/fact (24/4/64). ALL EXACT MATCHES vs committed table.
- Mid N=240000, eval 240000 24 10000 1, rep 0: rc=0, sha256
  17d5ee80c786a4364f7a48fd5615a76b80a0fdb6563445299ea9011928231716 —
  BYTE-IDENTICAL to committed docs/lab/scale/runs/s3_r0.log (cmp clean).
  Measures: clean 227965/227965=1.0000, all-fact 0.9499, deciles
  22841/22841 & 22775/22775 gap 0, absorption 12035/12035, flaw 96/96,
  ops_x1000=4000 (4.000), mem 92 B/fact, chunks 59/59/30. ALL EXACT MATCHES.
- Mid reps 1,2: launched in background (proc_3561f826ab90), awaiting result.

Notes:
- Branch head moved 283034e9 → 293602fb between API read and fetch (other
  crews committing; pinned commit unaffected).
- Two foreground exec calls failed session registration ("timed out after
  15s registering session metadata") — runtime hiccup; retried in background
  mode successfully.
