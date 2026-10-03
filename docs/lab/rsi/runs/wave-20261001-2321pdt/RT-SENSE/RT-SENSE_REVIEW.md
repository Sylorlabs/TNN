# RT-SENSE_REVIEW.md: independent red-team review of DEVANG3 (wave-20261001-2321pdt)

Reviewer: RT-SENSE. Lane: DEVANG3 only. SENSORY lane still running; not covered here.
Method: read-only toward the lane dir. All sources extracted with `git show`
from the recorded commits. Re-verification with shell tools only
(sha256sum, cmp, diff, grep); the frozen binary was rebuilt from the
committed implementation source with the pinned znc and re-run against the
committed sealed files. Pure Zag; safebin PATH; no forbidden interpreter
invoked at any point (see NAMECHECK.md Step 0).

## Verdict: QUALIFY

The lane's BUILD-PASS verdict stands on the frozen kill bars as written.
Every reported number was reproduced independently by this reviewer from
committed sources. The qualification concerns what the pass establishes,
not whether the bars were met:

**Qualification:** the K_SEAL leg (learner 20/20 on fresh Family C) does
not discriminate the learner from the trivial fixed-width-3 control C2,
which also scores 20/20 on the fresh family (independently confirmed).
The fresh Family C was specified in the frozen prereg (informed by the
lane's own disclosed /tmp tuning) to the segmenter's known 3-char comfort
zone, and the JUDGE_BRIEF knowledge claim "K_SEAL 11/20 to 20/20" compares
the 2021pdt sealed C against a differently structured fresh family, not a
same-set improvement. What this wave establishes is the merge-pathology
fix on held-out ambiguity probes (K_SEG 12/12 fresh, 12/12 on the 2021pdt
regression set where the baseline scored 8/12). Post-freeze generalization
beyond a trivial control is not demonstrated by Family C; the
segmentation-specific discrimination rests on K_SEG (learner 12/12 vs
ablation 4/12) and K8 (20/20 vs 17/20, exactly at the 15pp threshold).

## Independent re-verification (all from committed sources)

1. **Binary hash and rebuild.** The binary committed at 126ef2600 hashes
   `36f5047dd123a144569adaba5d7d86efcdf2126fa762790fe083ef620525151d`,
   matching the claimed hash. Rebuilding the committed `devang3.zag`
   (extracted at 126ef2600) with the pinned znc
   (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`,
   flags `--no-zagd --no-analyze --no-foreground-cache`) reproduces that
   hash byte for byte.

2. **One-line fix confirmed.** Diff of the 2021pdt baseline
   (`devang3.zag` at a272a8f6, 1564 lines) vs the wave implementation
   (126ef2600, 1574 lines) shows exactly one behavior-changing line:
   `sc=-50+ilog(L+1)*5;` became `sc=-50-1*L;` in `seg_dp`.
   The remaining delta is comment rewrites documenting the sign flip.
   No other code, table, mode, bridge, or handler changed. Cognition
   lines added: 1 (governance cap: 120). Minor nit: IMPLEMENTATION.md
   reports 1571 lines (+7); the committed file is 1574 lines (+10).
   Immaterial to the governance bar.

3. **Root-cause claim corroborated behaviorally.** Running the 2021pdt
   baseline binary on the 2021pdt sealed B reproduces exactly the four
   documented failures (probes 6, 8, 9, 12: `blumalagrn`, `grnsalabal`,
   `takbigerkala`, `nottemagrn`; 8/12). The fixed binary scores 12/12
   on that same old set and 12/12 on the fresh set. The prereg's hand
   arithmetic checks out: old scheme, probe 8: novel `[grnsala]` L=7
   scores -50+ilog(8)*5 = -35 vs `[grn][sala]` = 0 + (-50+ilog(5)*5)
   = -40, merge wins by 5; new scheme: -57 vs -54, the true split wins
   by 3 (the 3-char novel-length difference). Probe 9 tie broken by the
   2-char novel difference (`kala` L=4 vs `erkala` L=6: -54 vs -56).
   In each failing probe the correct and wrong analyses contain the
   same number of novel segments, so the fixed -50 cancels and the
   length term decides, exactly as the prereg predicted.

4. **Sealed-package integrity.** All five pre-run hashes in
   SEALED_B.md/SEALED_C.md match the committed files exactly
   (sealed_b.txt, sealed_b_key.txt, sealed_c.txt, genB.zag, genC.zag).
   The committed generator binaries reproduce the sealed files byte
   for byte when re-run, so the sealed files are raw generator output,
   not hand-tuned after the fact. The sealed package commit ead6f006c
   (2026-10-02T06:49:35Z) strictly precedes the sealed-eval commit
   11026f43b (06:50:51Z).

5. **Sealed results reproduced.** With the rebuilt binary on the
   committed sealed files: `segb` output is byte-identical to the
   committed key (K_SEG 12/12); `segb-abl` differs on 8 of 12 lines
   (ablation 4/12, matching probes 1,3,8,11; K_ABL ceiling 5/12 holds);
   `sealc-fresh learner` prints SEALC 20/20, 3/3 byte-identical, output
   hash `42f4919180ac8f56fa50bd93efe7666d00366d8d86395cace04df239ff2f51db`
   matching SEALED_EVAL.md; `fama` 3/3 byte-identical, exit 0, zero
   stderr, hash `206e5dfa84f9c70ccf2060a8084e3c258b82e46f2ccdbcaafd6d363866e9714b`
   matching the record; fama output lines confirm K1 10/10, C0 13/20
   with K1=3/10 (35pp, 7 words), K8 best_c=17 (20/20 vs 17/20 = exactly
   15pp), sub-bars K2 6/6 K3 3/3 K4 3/3 K5 3/3 K6 3/3 K7 2/2 K9 10/10.
   Regression: old sealed B 12/12 (was 8/12, all four old failures
   fixed), old sealed C 11/20 (no regression).

6. **Freshness of the sealed families.** Family C utterances contain
   zero occurrences of any Family A word form as substrings
   (checked: tak, not, red, blu, grn, bal, sph, cub, tri, big, biger,
   smal); header "60 20"; all 20 test utterances have 0 occurrences in
   the 60 training lines. Family B: 12 utterances, novel words all 3-4
   chars, prefix pairs sharing >=2 chars = 5 (>=3 required), suffix
   pairs sharing >=2 chars = 3 (>=3 required). Observation, not a
   finding: the fresh Family B reuses the novel word form `tema` from
   the 2021pdt sealed set, but in a new utterance (`taktemagrn` vs old
   `nottemagrn`) testing the same ambiguity class; the sealed *files*
   are not reused.

7. **K_AUD code audit.** `learn_update` takes `rawmode`; the raw-byte
   bigram block executes only when `rawmode==1`; `rm` is initialized 0
   and set to 1 only for variant==1 (C0 control); all learner call
   sites pass 0; statistics update exclusively from `segs[]`.
   Cold start (3-char chunks while nlex<10) lives inside `seg_dp` and
   feeds the same update path. All three prereg claims hold. K10/K11:
   the training loop segments episode t with current statistics before
   updating; untouched by the diff.

8. **Kill bars verbatim.** Prereg commit-order self-check passes:
   5b7e55706 (prereg + NAMECHECK only, no .zag) 2026-10-02T06:46:26Z,
   then 126ef2600 (implementation) 06:49:28Z, then ead6f006c (sealed
   package) 06:49:35Z, then 11026f43b (SEALED_EVAL only) 06:50:51Z,
   then a29d4088c (JUDGE_BRIEF only) 06:51:10Z. Every frozen bar in
   the verdict table matches the prereg verbatim (K_SEG >= 9/12,
   K_SEAL >= 12/20, K_ABL <= 5/12, K_C0 >= 15pp and >= 3 words,
   K8 >= 15pp, sub-bars >= 4 of 7). No bar was weakened after results.
   K8 passes exactly at threshold (15pp); noted, not a failure.

## Attacks that did not hold

- **Weakened bars:** every bar in SEALED_EVAL/JUDGE_BRIEF matches the
  frozen prereg verbatim. No weakening found.
- **Commit-order violation / pre-built implementation:** the prereg
  commit contains only PREREG_DEVANG3.md and NAMECHECK.md; the .zag
  and binary appear first in 126ef2600, 3 minutes later. No
  implementation file predates the freeze.
- **Multi-line fix disguised as one line:** the full diff is one
  scoring line plus comments. The comments document the fix and do
  not change behavior.
- **Sealed files tuned post-hoc:** generator binaries reproduce the
  sealed inputs byte-identically; pre-run hashes all verify; the key
  was committed pre-run. Raw generator output, no hand edits.
- **Wrong-sign diagnosis:** the behavioral reproduction (baseline
  fails exactly the four documented probes; fixed binary fixes all
  four on both old and fresh sets) corroborates the length-term
  diagnosis, and the predicted 3-point / 2-point margins are
  consistent with the observed fixes.
- **K_ABL headroom fabricated:** the ablation genuinely scores 4/12
  on the fresh set; the 8 probes where the key differs from fw3 output
  are the discriminating probes (SEALED_B.md's prose gloss "boundary
  not at a multiple of 3" is slightly loose for probe 2, whose true
  boundary is 3 while fw3 outputs 3,6; the probe list itself is
  correct as the discrimination set).

## Residual risks (disclosed by the lane; not findings)

- Single worker, no independent adversary. The blind-generation
  discipline is attestation-based: the commit record enforces
  hashes-before-run (verified) but cannot prove the generator was
  not iterated before its single commit. The lane discloses this in
  the prereg and the judge brief.
- The /tmp tuning that shaped the prereg's Family C spec (3-char
  content words after 3-6 char dev probes scored 15/20) is disclosed;
  it is consistent with the frozen spec, but it is also why Family C
  sits in the segmenter's comfort zone, which is the substance of the
  qualification above.
- Doc nits: IMPLEMENTATION.md line count (+7 reported, +10 actual);
  SEALED_B.md probe-2 gloss; shared `tema` word form across the
  regression and fresh sets. None affect any bar.

## Bottom line

BUILD-PASS is earned on the frozen bars and the evidence is
independently reproducible down to the byte. The fix is genuinely one
cognition line and the root-cause story holds. The qualification is
about scope, not validity: the wave proves the merge pathology is
fixed on ambiguity probes; it does not prove post-freeze
generalization beyond a trivial control, because the fresh Family C
is fw3-friendly by (disclosed) design and C2 ties the learner there.
Any downstream claim should cite K_SEG, not K_SEAL, as the
discriminating evidence.

## Evidence paths

- Prereg: `docs/lab/rsi/runs/wave-20261001-2321pdt/DEVANG3/PREREG_DEVANG3.md` (5b7e55706)
- Implementation: `docs/lab/rsi/runs/wave-20261001-2321pdt/DEVANG3/devang3.zag` (126ef2600)
- Sealed package: `docs/lab/rsi/runs/wave-20261001-2321pdt/DEVANG3/sealed/` (ead6f006c)
- Results: `SEALED_EVAL.md` (11026f43b), `JUDGE_BRIEF.md` (a29d4088c)
- This review: `docs/lab/rsi/runs/wave-20261001-2321pdt/RT-SENSE/RT-SENSE_REVIEW.md`
