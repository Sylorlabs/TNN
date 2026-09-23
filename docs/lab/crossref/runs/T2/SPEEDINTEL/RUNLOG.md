# RUNLOG — T2-SPEEDINTEL (replacement crew)

## Inherited state (predecessor, killed by runtime daemon restart 2026-09-23)
- `clean/` contained a corrupt clone: `clone.log` showed "Cloning into 'repo'..." with no completion; `clean/repo` was an EMPTY git repo (unborn HEAD, no commits). No run artifacts, no VERDICT.md/RUNLOG.md in `crew/` (empty). Nothing valid to resume.
- Disposition: removed the corrupt state (`clone.log`, empty `repo/`). Recorded here per RESUME rule.

## Environment pin
- Frozen prereg commit: `7b2100d09911c5c10252c5756c7def288e70bd1f` — verified EXISTS via GitHub API (message: "crossref: scope + frozen preregs for the cross-reference / clean-environment replication program"). Frozen pin recorded BEFORE any run. ✓
- Frozen prereg doc blob SHA (at pin): `b1178370036bffbda6eb68ea0989c0e427dc31b7` (docs/lab/crossref/PREREG_TIER2.md, 37962 bytes).
- znc: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned by prereg).
- NOTE (environment deviation, documented not hidden): full `git clone` of the frozen tree was not possible — large transfers (full clone, codeload tarball) stall/timeout on this VM (3 attempts, each >180s with no progress). Small API transfers work fine. Substitute: fetched ONLY the needed committed files individually via the authenticated GitHub contents API at the frozen pin, and verified EVERY file's blob SHA1 against the commit's recursive tree listing (content-addressed integrity). Frozen-pin anchoring holds (commit SHA verified at GitHub); only the transport differs.
- Scratch: `~/workspace/scratch-crossref/T2/SPEEDINTEL/` (never /tmp). TMPDIR=/home/hatch/workspace/tmp_commit.

## Frozen claims checklist (quoted verbatim from PREREG_TIER2.md T2-SPEEDINTEL section, at the frozen pin)
> T2-SPEEDINTEL — speed-intelligence exchange rate: 2× is the knee (Type A)
> **Claims:** measured, frozen prereg, pure Zag, byte-identical: 1× deliberation starved (6/18 coding, 29/94 epistemic — ~2× cost per quality point vs the knee); 2× is the knee (18/18 coding, 59/94 epistemic); 4×/8× add nothing (18/18, 59/94, confirmed on a fresh battery); 2× + free-speed mechanisms reaches knee quality at ~2/3 the eval cost of naive 1× (65.1% fewer evals, 37.8% fewer compiler calls). Micah's ruling: 2× + free-speed = winner; 4×/8× dropped; quality-first, never trade quality for speed.
> **Method:** rerun the 1×/2×/4×/8× battery from committed sources in clean checkout (frozen prereg; crew freezes the pin); ≥3 byte-identical runs.
> **Rule:** REPRODUCED if the (6/18, 29/94) → (18/18, 59/94) → flat table reproduces cell-for-cell; NOT REPRODUCED if 4×/8× buys anything or 2× misses the knee.

### Cell checklist (from frozen RESULTS_SI.md / RESULTS_ARM4.md at the pin)
Coding (budget iters: 1x=2, 2x=4, 4x=8, 8x=16): 6/18 → 18/18 → 18/18 → 18/18; honest halts 2/2 at every budget.
Epistemic (/94): 29 → 59 → 59 → 59 (confirmed on fresh disjoint battery per ADDENDUM SI-A1 resolution rule: gain(1x→2x)>10pp, gain(2x→4x)≤1pp, gain(4x→8x)≤1pp).
Exchange rate (Arm 4, SI battery @ knee budget 4, inclusive znc counts): knee baseline 18/18, 46 iters, 45 znc, 129 hyp-evals; knee+all-winners 18/18, 46 iters, 28 znc (−37.8%), 45 hyp-evals (−65.1%).

## Progress

## Run progress
- 27/27 source files fetched at pin, blob-SHA1 verified vs commit tree. Fetch method documented above.
- R33 substrate gap: delib_si.zag's imports (docs/lab/prose-learning/epistemic_wave/src/R33_*.zag) were NEVER committed (verified absent at both the SI results commit 43eceed21 and the frozen pin). Substituted the canonical in-lab variants (IO=a6b440d2 — all 41 docs/lab copies identical; SHA=5dd858fa — all 37 identical). delib_si.zag uses only nio_alloc/nio_close/nio_open_child/nio_open_root/nio_read_exact from the IO file. All 12 committed out_b*.txt raw outputs reproduced BYTE-IDENTICAL with the fresh build → substitution is behaviorally sound. Documented in VERDICT.md as the one build-material deviation.
- Binaries built from committed sources with pinned znc (--no-analyze --no-zagd): work_a1/learner, work_a1/delib_si, work_a1r/delib_si (source copied from work_a1 — blob SHA identical at pin), work_a3/learner_si3, work_a4/bin/learner_si4.
- Driver plumbing check: no `re` import and no error-class keywords in driver_si.py, work_a1/driver_si.py, work_a4/driver_si4.py, run_sweep_si.py, run_transfer.py, analyze.py (score_epi*.py use re only to parse the delib binary's own output format — scoring, not diagnosis).
- EPISTEMIC (frozen battery): 29/94 → 59/94 → 59/94 → 59/94, IDENTICAL ×3, mean_preds 3.000/9.000/9.319/10.319, recon=0, vflips=0 — matches frozen RESULTS_SI.md cell-for-cell. All 12 committed out_b*.txt reproduced byte-identically.
- EPISTEMIC (fresh battery, ADDENDUM SI-A1): generator deterministic — regenerated items byte-identical to committed (F 0/12, W 35/70 audit). Sweep: 29 → 59 → 59 → 59, IDENTICAL ×3, mean_preds 3.000/9.000/9.330/10.330, recon=0/0/1/1 — matches RESULTS_A1R.md; resolution rule satisfied (31.9pp>10pp, 0≤1pp, 0≤1pp) → PLATEAU-CONFIRMED reproduces.
- CODING sweep running (background proc_db401766a0a9). b2_r1 digest matches frozen (009ecfed2... — verify at end); b4_r1 digest 9f1281364907d349... MATCHES frozen RESULTS_SI.md prefix; Qc 18/18, iters 46, znc 27 (exclusive count, as in Arm 1's table).

## Final results (all complete)
- CODING sweep (budgets 2/4/8/16 × 3 reruns, proc_db401766a0a9, RC=0): all cells IDENTICAL across reruns; canonical digests match frozen published prefixes (b2 009ecfed27255a63, b4 9f1281364907d349, b8 68fb53a6581b38b4, b16 d218ef3707fbe309); metrics 6/18 → 18/18 → 18/18 → 18/18, iters 32/46/46/46, znc 25/27/27/27 (exclusive count as in Arm 1's table), first_try 6/18, honest_halt 2/2 everywhere.
- Gates 6/6 on work_a1/learner, work_a3/learner_si3, work_a4/bin/learner_si4 (REFUSE G1/G2/G4/G5 + 2× ALLOW).
- ARM 4 transfer (run_transfer.py, RC=0, 6 cells × 3 reps IDENTICAL): b2_none 6/18 32/31/121; b4_none 18/18 46/45/129; b4_a 18/18 46/45/43 (−66.7% evals); b4_b 18/18 46/45/91 (−29.5%); b4_c 18/18 46/28 (−37.8% znc)/129; b4_combo 18/18 46/28 (−37.8%)/45 (−65.1%). Exchange-rate table reproduces cell-for-cell.
- Committed analyze.py: 3a 28/28 diagnose winners byte-identical; 3b 28/28; combo 25/25 evidence-matched + the same 3 characterized PRECHECK divergences (S03/S05/S06) as frozen; outcomes IDENTICAL vs baseline; FP validation 0/51 on b4_c and b4_combo.
- si4none sanity (driver_si4 --mech none × 3, manual): 18/18, 46 iters, 45 znc, 129 evals, IDENTICAL ×3; 28/28 diagnose winners identical to b4_none.
- VERDICT: REPRODUCED (all frozen cells reproduce; no budget buys anything past the knee; 2× holds the knee on both domains).
