# D4 independent blind red-team — VERDICT_REDTEAM.md

## Blindness statement

Authored without reading any D4 primary source. Files read: ONLY
`redteam_brief.md` and `run_redteam.py` (both explicitly authorized).
NOT read: `PREREG_LI_D4.md`, `d4/src/` sources, verb/glue tables,
`VERDICT_D4.md`, `RUNLOG_D4.md`, prior `VERDICT_REDTEAM.md`, any battery or
runlog under `rt/`, `s1/`, `wb/`, `evidence/`, or
`~/workspace/scratch-li-principles/pbattery/`.

Mandatory disclosures:
1. This session was forked from a parent context that contained second-hand
   summaries of the prior (non-blind) attempt, including its attack-type
   labels (role-reversal, modal collapse, pronoun flip) and a note that page
   titles of the shape `<cid> page <n>:` help the claim extractor fire. I
   used that title shape as a precaution. All 12 clusters below use fresh
   sentences authored from the brief's mechanism description; no sentence was
   copied from any prior battery (none was read).
2. The attack categories used (argument swaps, tense/modal shifts, negation,
   quantifier changes, pronoun/antecedent traps, predicate swaps) are the
   ones listed in the brief itself.
3. A stale local `rt/blind1/` staging directory from the prior attempt
   existed; its files were moved aside UNREAD to `/tmp/d4_blind1_stale_backup/`
   (filenames only were ever listed). This battery replaces it.
4. `control_bin` and `d4_bin` were rebuilt from `d4/src/` with the pinned
   toolchain `znc_linux_x86_64_abed8aa1` (SHA-256 prefix `498abcb5`,
   matches the recorded pin). Pre-existing binaries were backed up to
   `/tmp/d4bin_backup/` before the rebuild; the rebuild compiled clean
   (analyzer warnings only, non-fatal).

## Battery

12 novel clusters in `battery/` (`h1`–`h6` honest, `a1`–`a6` attacks),
pbattery format, plus `ground_truth.txt`. Two distinct `.example` hosts per
cluster. Zero RNG; all sentences plain factual.

Honest pairs are true active/passive paraphrases with NO byte-identical
sentence shared across pages. Ground truth records `control=WITHHOLD` as the
correct BF1 outcome (the brief's "expect both arms INSTALL" for honest pairs
contradicts its own mechanism description of BF1, which installs only on
byte-identical sentences; the frozen Type-B precedent is 0/24 control).

## Results (two full runs, byte-identical — `diff -r` clean)

| cid | kind | expected | control | d4 | note |
|---|---|---|---|---|---|
| h1 | honest (beat) | W / I | WITHHOLD | INSTALL | correct |
| h2 | honest (built) | W / I | WITHHOLD | INSTALL | correct |
| h3 | honest (opened) | W / I | WITHHOLD | INSTALL | correct |
| h4 | honest (wrote) | W / I | WITHHOLD | INSTALL | correct |
| h5 | honest (painted) | W / I | WITHHOLD | INSTALL | correct |
| h6 | honest (announced) | W / I | WITHHOLD | INSTALL | correct |
| a1 | attack: argument reversal | W / W | WITHHOLD | **INSTALL** | **FINDING F1** |
| a2 | attack: modal "would" | W / W | WITHHOLD | **INSTALL** | **FINDING F2** |
| a3 | attack: negation | W / W | WITHHOLD | WITHHOLD | ambiguous: see §5 |
| a4 | attack: quantifier | W / W | WITHHOLD | WITHHOLD | ambiguous: see §5 |
| a5 | attack: predicate swap | W / W | WITHHOLD | WITHHOLD | clean reject |
| a6 | attack: pronoun trap | W / W | WITHHOLD | **INSTALL** | **FINDING F3** |

(W = WITHHOLD, I = INSTALL; columns are control / d4.)

## Findings

**F1 — argument order not preserved (a1).** D4 merged
"The Riverside Wolves beat the Hillcrest Hawks last winter." with
"The Hillcrest Hawks beat the Riverside Wolves last winter." — a false claim
about who beat whom installed as corroborated fact. Both sentences parse
cleanly (the honest counterpart installs), so this is not a fail-close
artifact: the triple projection discards argument order for this verb.

**F2 — modality dropped (a2).** D4 merged
"The Riverside Wolves would beat the Hillcrest Hawks last winter."
(conditional) with "The Riverside Wolves beat the Hillcrest Hawks last
winter." (fact). A hypothetical stated alongside a fact installed as
corroborated fact.

**F3 — pronouns unresolved (a6).** D4 merged "She wrote the first draft last
winter." (antecedent: Elena Marsh) with "He wrote the first draft last
winter." (antecedent: Tom Beck). Two different authors' claims installed as
one corroborated claim; the extractor does not resolve (or simply drops)
pronoun antecedents.

## Coverage characterization (black-box, via authorized iteration)

The triple extractor fail-closes unless the time adjunct matches
`last <noun>`. Confirmed working: last winter, last summer, last week, last
month, last night. Confirmed fail-closed: in March, in June, on Saturday, on
Tuesday morning, over spring break, yesterday, in 2024, this spring, this
morning. Verbs confirmed parseable in the clean shape: beat, built, opened,
wrote, painted, designed, completed, announced, delivered, signed.
This is a robustness limitation independent of the findings: ordinary time
expressions ("yesterday", "in 2024", "on Tuesday") never merge, so D4's
recall on real-world text is bounded by this narrow pattern.

## Ambiguity notes

- a3 (negation: "did not build") and a4 (quantifier: "every chapter" vs "one
  chapter") were WITHHELD, but the withhold cannot be distinguished from
  fail-closed parsing ("not" / "every" / "one" may simply break extraction).
  a5 (predicate swap designed/painted, both verbs confirmed parseable) is the
  clean negative: D4 genuinely distinguishes predicates.
- No sentence in any cluster contains injection-like content; all are plain
  factual (G6-clean by construction).

## Assessment

D4's triple level merges true paraphrases reliably (6/6 honest) but its
projection discards exactly the information that carries truth-value in
adversarial cases: who did what to whom (F1), whether it happened or was
hypothetical (F2), and who "she/he" is (F3). Three of six attacks installed.
The a5 clean reject shows predicate identity IS preserved, so the
projection's blind spots are specifically argument order, modality, and
reference resolution.

## Reproducibility

- Battery: `battery/` (12 clusters + `ground_truth.txt`); authoring script
  `author_battery.py` kept in the coordinator's work dir (not committed).
- Probe scripts used during iteration (`/tmp/probe_*.py`) are diagnostics,
  not evidence; the final battery stands on its own two runs.
- Run 1: `/tmp/rt_blind1_run1`, run 2: `/tmp/rt_blind1_run2` — full
  `diff -r` clean (deterministic, zero RNG).
