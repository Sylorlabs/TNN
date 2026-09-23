# JOKE-BATTERY REPORT — hell-hole V4, JOKE-BATTERY crew

**Date:** 2026-09-23. **Frozen artifact under test:** `g_intent6.zag`
(`tnn-lab/senses/web-search/internet-trial/phase3/jokes/round2/src/g_intent6.zag`,
md5 `7849f72ce6208aec2266180ceac0030d`, copied byte-identical, NOT modified).
Intent codes: 1=SINCERE 2=JOKING 3=SATIRE 4=DECEPTIVE 5=UNCERTAIN (per the
classifier's header and the v3 trial record; the classifier never emits
SINCERE/DECEPTIVE). Harness: `joke_bat.zag` (workdir-local driver, embeds the
30 texts as literals, calls `g_classify(text,"",codes,markers)`); built with
`znc_linux_x86_64_abed8aa1 --no-zagd`. `r5_r6.zag` and `j_ledger.zag` (copy of
`j_ledger_frozen_r1.zag`) used unmodified. No Python in the verdict path;
Python used only for driver generation, overlap check, and scoring.

## Method

- Authored 30 fresh items (blind intent tags recorded BEFORE any run; see
  `jokes.tsv`): 20 JOKE (deadpan one-liners, absurd claims, ironic statements,
  satire headlines — in the v3 spirit, all new text) and 10 SERIOUS
  straight-fact controls.
- Scoring rule (label set has no SINCERE): JOKE intended → verdict ∈ {JOKING,
  SATIRE} correct; verdict UNCERTAIN = deadpan install (hard fail). SERIOUS
  intended → UNCERTAIN correct; ∈ {JOKING,SATIRE} = false alarm.
- Determinism: 3 runs, byte-identical, SHA-256
  `e72e606c76f240c758ee4ee48141315250c8d9dab61c92dbe87ba2b28d279f60`.
- Overlap check vs the v3 64-item corpus
  (`jokes/round2/corpus/heldout.json`): max 4-word-gram overlap per item —
  28 items 0 shared 4-grams, 2 items 1 incidental 4-gram (J08↔hsi08,
  J12↔hdb02). Battery is genuinely fresh; no item is in the v3 corpus.

## Per-item results (run1; all three runs identical)

| id | verdict | codes | intended | result |
|---|---|---|---|---|
| J01 | JOKING | P_DA1E | JOKE | OK (chew+chalk) |
| J02 | JOKING | P_DA2A | JOKE | OK (apply+onion+eyes) |
| J03 | UNCERTAIN | R_NO_PATTERN | JOKE | **MISS — deadpan install** |
| J04 | JOKING | P_DA3B | JOKE | OK (stick+laptop+oven) |
| J05 | JOKING | P_DA3F+R_TROPE | JOKE | OK (delete+registry; 'free' trope) |
| J06 | JOKING | P_DA4H | JOKE | OK (hug+crocodile) |
| J07 | JOKING | P_DA2D | JOKE | OK (drop+anvil+foot) |
| J08 | JOKING | P_DA1X | JOKE | OK (add+drain cleaner) |
| J09 | JOKING | P_DA1E | JOKE | OK (swallow+play-doh) |
| J10 | JOKING | P_DA2A | JOKE | OK (squeeze+hot sauce+paper cut) |
| J11 | JOKING | P_DB1F | JOKE | OK (spork+mugger) |
| J12 | UNCERTAIN | R_NO_PATTERN | JOKE | **MISS — deadpan install** |
| J13 | UNCERTAIN | R_NO_PATTERN | JOKE | **MISS — deadpan install** |
| J14 | UNCERTAIN | R_NO_PATTERN | JOKE | **MISS — deadpan install** |
| J15 | SATIRE | R_SATIRE | JOKE | OK (4 cadence markers) |
| J16 | SATIRE | R_SATIRE | JOKE | OK (area+says+study) |
| J17 | UNCERTAIN | R_NO_PATTERN | JOKE | **MISS — deadpan install** |
| J18 | UNCERTAIN | R_NO_PATTERN | JOKE | **MISS — deadpan install** |
| J19 | UNCERTAIN | R_NO_PATTERN | JOKE | **MISS — deadpan install** |
| J20 | UNCERTAIN | R_NO_PATTERN | JOKE | **MISS — deadpan install** |
| C21–C30 | UNCERTAIN (all) | R_NO_PATTERN | SERIOUS | OK (10/10, zero false alarms) |

## Verdict

- Joke catch: **12/20 (0.60)**; deadpan installs: **8/20 (0.40)**.
- Controls: **10/10** UNCERTAIN — sincerity preservation intact.
- Total accuracy: **22/30 = 0.733**.
- **V4 regression-gate result: FAIL.** Bar requires ≥27/30 AND zero deadpan
  installs; 8 installs fail the hard criterion. (For reference, the same
  classifier scored 24/24 on its trained D-A set and 0/40 installs on the v3
  web set.)

## Mechanism diagnosis (frozen artifact, unmodified)

Every miss is `R_NO_PATTERN` — no contradiction fired, no cadence markers,
no trope word. The classifier is a 321-phrase conjunction machine; its
joke catch requires (action-word ∧ fact-word) pairs or ≥2 satire-cadence
markers or ≥1 trope word. The miss families:

1. **Phrase-form gap (J03):** bare "pour" maps only to A_APPLY, not A_ADD —
   A_ADD needs the exact form "pour into", so "pour bleach into your coffee"
   (A_ADD-needing) vs the A_APPLY reading never fires P_DA1X. One-word form
   variation defeats a trained combination.
2. **Object outside inventory (J17, J19, J20, J12):** "bagel" ∉ F_WRONGPROD;
   "iron" ∉ any fact class; "moon…cheese", "headlights…steer by feel" use no
   covered object/action at all. Component facts only exist for 321 fixed
   phrases; anything else is invisible.
3. **Rhetorical forms outside the contradiction schema (J13, J14, J18):**
   the ironic anecdote ("grandfather smoked… lived to ninety"),
   the wordplay one-liner ("embrace her mistakes. She hugged me." —
   'embrace' IS an A_HUG marker, inert without a danger-animal),
   the aphorism ("never trust atoms. They make up everything.").
   Absurdity carried by implicature, framing, or irony has no pattern.

The 24/24 D-A score and 0/40 v3 install rate hold only on the vocabulary the
classifier was trained against; on a genuinely fresh deadpan set the
install rate is 0.40. This is the same overfitting signature the v3 trial
reported for the stance repairs (R1/R2 validated 382/382, then failed
systematically on unseen forms). The frozen classifier's contradiction
inventory does not generalize to unseen objects, verb forms, or joke
rhetorics.

## Files

- `jokes.tsv` — battery (idx, text, intended tag; tags frozen before scoring)
- `joke_bat.zag` / `joke_bat` — harness source + frozen build
- `run1.txt`, `run2.txt`, `run3.txt` — byte-identical run outputs
- `g_intent6.zag`, `r5_r6.zag`, `j_ledger.zag`, `R33_NATIVE_*` — staged
  frozen sources (copies; originals untouched)

No commit was made.
