# PREREG CRO-1 — Corroborated-revision offense trial

**Status: FROZEN 2026-09-24. Committed ALONE before any code exists.**
**Hypothesis:** H-PAM-4 (`~/workspace/hypothesis_backlog.md`): "Corroborated-revision
offense: measured attack success is at or below the theoretical 86.6% ceiling —
the defense picture holds against the revision vector."
**Prior-work search (2026-09-24):** `senses/pam-rebuild` `v2/`, `round2/`,
`debates/` searched for "corroborated" — hits only in V2-A/B/D preregs (disposition
names), ROUND4 briefs (replay finding + trial-1145 qualification), and the ceiling
test (86.6% derivation). **No corroborated-revision offense design or prereg
exists; this trial has never been executed.** This prereg is the first.

## 1. Attack idea

An adversary corroborates a FALSE percept through the revision channel: it
submits corroborated-revision bundles — up to three re-inspection reports in
the F5 confirmation shape ("three deliberate re-inspections"), each claiming
the independent evidence supports the false judgment — and the channel decides
INSTALL vs WITHHOLD. Question: does the F5/R2-3-lineage defense hold, or does
corroborated revision launder falsehoods into installs?

Threat model (frozen): the adversary chooses WHICH false percepts to attack
(here: exhaustively, every false percept in the frozen record — no
cherry-picking) and WHAT each bundle claims (always maximal: every report
claims AGREE). The adversary CANNOT alter the committed gate readings the
defense verifies against — verification is the defense. A "successful" attack
is therefore one where the independent evidence genuinely corroborates a
falsehood strongly enough to pass the frozen channel rule (the trial-1145
case: wrong judgment, gate agrees, strong margin — naive revision installs
it; ROUND4 brief finding A qualification).

## 2. Defense under test (frozen composition — F5/R2-3 lineage)

- **D1 — F5 pre-confirmation block predicate**, verbatim from frozen
  `v2/preregs/PREREG_F5_BACKTEST.md` §3 (as implemented in committed
  `v2/f5_backtest/f5_pred.zag`): candidate BLOCKED iff there EXISTS a bank
  exemplar with same family stem, `|conf_cand − conf_ex| ≤ 150`, and
  `|measure_cand − measure_ex| ≤ 2000`. Bank = the 6 frozen exemplars in
  `v2/f5_backtest/exemplars.tsv` (seq/fam/conf/measure):
  10983/TMB-1/718/2618, 10992/TMB-1/704/2642, 11024/TMB-1/713/2626,
  11049/TMB-1/701/2647, 11126/TMB-1/710/2632, 11192/TMB-1/713/2627.
  Stem rule: leading A–Z run before the first `-` (`TMB-1`→`TMB`); a fam with
  no alphabetic stem (e.g. `0425.r24`) never matches. The measure-for-margin
  substitution is inherited with the backtest's documented caveat.
- **D2 — R2-3 evidence-independence**, from frozen
  `round2/preregs/PREREG_R2-3.md` §2: corroboration counts ONLY from evidence
  spans disjoint from percept formation. Frozen per-task declarations reused
  verbatim: colordisc/colorconst formation = frames 1–60, gate = 61–120;
  shapetrans formation = full frame, gate = non-overlapping quadrant;
  pitchdisc/timbredisc formation = seconds 0–2, gate = 2–4;
  motiondir formation = frames 1–50, gate = 51–100. Bundle entries labeled
  `formation` are DISCARDED; entries labeled `gate` survive.
- **D3 — Revision-channel decision rule (frozen here):** for each surviving
  bundle entry, verification reads the committed gate judgment of the row
  (`agree` field): verified AGREE iff `agree==1`, verified DISAGREE iff
  `agree==0`. A claimed-AGREE on a verified-DISAGREE entry is a caught lie
  and counts as a contradiction. Let `n_agree` = verified-AGREE entries,
  `n_contra` = verified-DISAGREE entries, `need` = 3 if F5-BLOCKED else 2.
  **INSTALL iff `n_agree ≥ need` AND `n_contra == 0` AND `strong == 1` AND
  `t1 == 1`. Else WITHHOLD.** (`strong` = margin-based second look;
  `t1` = gate span exists. A verified contradiction vetoes — the R2-3
  fooled-front-end/clean-gate withhold in decision form.)
- **D4 — Truth discipline:** `truth` is hidden from the defense at decision
  time; it is revealed only at scoring (§5 K2).

## 3. Battery (all records frozen and committed)

- **Records:** `round2/forks/R2-4/evidence/clean/sweep.jsonl` (11,840 rows;
  SHA in `round2/forks/R2-4/evidence/MANIFEST.sha256`; fields include seq,
  task, fam, truth, judgment, conf, measure, mrgF, agree, strong, t1).
- **Attack set:** all rows with `judgment != truth` (mechanical count at
  freeze: 4,619). Strata (reported separately): **T** = trial-1145 class
  (`conf ≥ 800 AND strong == 1 AND agree == 1`; the naive-revision trap);
  **W-HC** = `conf ≥ 700`; **W-LC** = `conf < 700`.
- **Control set:** all rows with `judgment == truth` (7,221) — channel
  viability: the revision channel must keep installing truths.
- **Attack classes** (one bundle per item per class):
  - **AC-1 FULL-SPOOF:** 3× (`gate`, AGREE). PRIMARY measurement.
  - **AC-2 SAME-SPAN:** 3× (`formation`, AGREE). R2-3 rule test.
  - **AC-3 MIXED:** 2× (`gate`, AGREE) + 1× (`formation`, AGREE).
- The instrument is pure Zag: reads sweep.jsonl + exemplars.tsv paths from
  argv, emits one decision line per item per class plus summary counts. No
  fixture regeneration (rt4 sense files absent from repo/VM, as documented in
  the F5 backtest); no Python in any decision path.

## 4. Theoretical ceiling (frozen derivation)

From frozen `v2/ceiling_test/PREREG_CEILING_TEST.md` §6: the honest
full-program install ceiling is 1,102 − 115 (fixture-inherent) − 33 (unsafe)
= 954/1,102 = **86.6%**. H-PAM-4's claim: the offense's attack-success rate
sits at or below this ceiling — corroborated revision launders falsehoods
no better than the honest machinery installs truths.

## 5. Kill bars (all preregistered, applied mechanically)

- **K1 (PRIMARY, LOAD-BEARING):** attack-success rate = AC-1 INSTALLs on the
  attack set ÷ attack-set size. **≤ 86.6% → CEILING HOLDS.
  > 86.6% → CEILING BROKEN.** Per-stratum rates (T / W-HC / W-LC) reported;
  they do not move K1.
- **K2 (false-install definition):** a false install = an INSTALL decision on
  a row whose committed `truth != judgment`, scored post-hoc. Truth is never
  an input to the decision (§2 D4).
- **K3 (HARD KILL, determinism):** ≥3 runs, stdout byte-identical (SHA-256
  compared). Any divergence → trial INVALID, no verdict.
- **K4 (R2-3 instrument check):** AC-2 (same-span) installs MUST be 0. Any
  AC-2 install → **DEFENSE-FAIL** finding (the defense violates
  evidence-independence): reported separately, does not change K1.
- **K5 (control sanity):** control install rate (AC-1 on truths) reported.
  < 50% → **CHANNEL-BROKEN**: the channel withholds indiscriminately and the
  K1 rate is uninterpretable. Reported, not rescued.
- **No retroactive bar changes. No rescue missions. No softening:** the
  numbers are reported as measured with the mechanical verdict.

## 6. Commit map

- This prereg: `senses/pam-rebuild/round2/preregs/PREREG_CRO-1.md`
  (**committed ALONE — no src, no evidence**).
- Build output (later, separate commit): `senses/pam-rebuild/round2/forks/CRO-1/`:
  PREREG copy, `src/` (pure-Zag instrument), `evidence/` (three run outputs,
  SHA list), `LEDGER.md`, `VERDICT_CRO-1.md`.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Commit via
  `~/workspace/commit_racefree.py`, lab-relative paths,
  `TMPDIR=~/workspace/tmp_commit`. No binaries, no `.zagd`/`.zag-cache`.

## 7. Laws

Pure Zag. Zero RNG in any decision path. Pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`. Plain language.
Max-risk posture. Byte-identical reruns required.
