# Fresh epistemic battery — design notes (2026-09-22)

52 items, all new content, same 7-family discipline as the frozen 94.
Correct labels: FFF* → WITHHOLD (planted falsehoods), FTT* → ENDORSE (true
controls), FW* → WITHHOLD (weird-English non-endorsable utterances).
Knowledge/predicates are the frozen 9 from delib_si.zag (unchanged); every
item below is designed against those exact substring triggers. Expected
ledgers were hand-derived from the trigger lists and then verified with the
frozen binary (ledger check only, no scoring, before commit).

Trigger key: kf=is_known_false, ab=is_absurd, kt=is_known_true,
ms/mhy/mcf/mana/mpoe/mimp = the 6 speech-act matchers, cm2 = assertion-form
(" is "/" are "/" has "/" have "/" was "/" were " + digit).

## fresh_false.txt (FFF01–FFF12) — planted falsehoods, correct WITHHOLD

Each wraps one of the 12 frozen kf trigger phrases in a novel sentence, so
the frozen knowledge fires on new content. All: kf=1 → WITHHOLD at every
budget; adaptive R0-stop (unanimous withhold), cost 3.

| id | kf trigger wrapped |
|---|---|
| FFF01 | "triangle has 4 sides" |
| FFF02 | "spider has 7 legs" |
| FFF03 | "baseball team has 10 players" |
| FFF04 | "38 plays" + "shakespeare" |
| FFF05 | "d has an alphabet position of 5" |
| FFF06 | "d has alphabet position 6" |
| FFF07 | "saturday" + "letter count of 7" |
| FFF08 | "incontrovertibleness" + "21" |
| FFF09 | "knowledge has a letter count of 8" |
| FFF10 | "pilgrim" + "1688" |
| FFF11 | "david copperfield" + "1851" |
| FFF12 | "time machine" + "1896" |

## fresh_true.txt (FTT01–FTT12) — true controls, correct ENDORSE

- FTT01–FTT04: wrap the 3 frozen kt triggers ("alphabet position of a/e/m
  is 1/5/13") in novel sentences. kt=1, no matcher bait → R0-stop ENDORSE
  under adaptive policies; full-pipeline 2x also ENDORSE (no matcher fires).
- FTT05–FTT09: plain true statements with no triggers at all
  (kf=ab=kt=0, no matcher patterns) → E1-escalate → R1 nmatch=0 → ENDORSE.
  FTT08 contains " have " but no digit, so cm2=0 regardless (cm2 is only
  evaluated when a matcher fires, which never happens here).
- FTT10–FTT12 [TRAP: true + matcher-bait]: true statements that ALSO fire a
  speech-act matcher, via a kt phrase plus matcher bait:
  - FTT10: kt ("alphabet position of a is 1") + sarcasm ("great"+"terrible"+"monday").
  - FTT11: kt ("alphabet position of e is 5") + hypothetical ("suppose","what if").
  - FTT12: kt ("alphabet position of m is 13") + poetry ("moon poured").
  Fixed-2x: matcher fires → WITHHOLD (WRONG — these are true). Policy A/B/D/E/F:
  R0 kt-unanimous stop → ENDORSE (RIGHT) without ever running matchers.
  Policy C: R1 → nmatch=1 → cm2=1 (" is "+digit) → non-unanimous → R2:
  pro=1 vs con=kt(1)+cm2(1)=2 → ENDORSE (RIGHT, via reconsideration repair).

## fresh_weird.txt (FW001–FW028) — correct WITHHOLD, 4 per family

- Joke FW001–FW004: absurd triggers ("goldfish filed"; "toaster"+"chess";
  "refrigerator"+"therapist"; "moon called in sick") → ab=1 → R0-stop
  WITHHOLD (same as 2x).
- Sarcasm FW005–FW007: pos_word + neg_situation ("wonderful"+"flat tire";
  "brilliant"+"6 am"; "perfect"+"delayed"/"broke") → E1 → R1 nmatch=1 →
  WITHHOLD. cm2=0 (no assertion frame) → no reconsideration anywhere.
- Hypothetical FW009–FW011: "suppose"; "hypothetically"+"what if";
  "imagine if" → WITHHOLD, no reconsideration.
- Analogy FW013–FW015: "is a drill sergeant"; "voice is honey";
  "was a marathon" → WITHHOLD, no reconsideration.
- Counterfactual FW017–FW019: "if i had"+"would have"; "if i were"+
  "could have"; "would have" → WITHHOLD, no reconsideration.
- Poetry FW021–FW023: "moon poured"; "autumn writes"+"burning leaves";
  "river keeps"+"patient hands" → WITHHOLD, no reconsideration.
- Implicature FW025–FW027: "cold in here"; "trash is getting full";
  "meeting starts in five" → WITHHOLD, no reconsideration.
- FW008, FW012, FW016, FW020, FW024 [TRAP: matcher + assertion-form]:
  one per family (sarcasm, hypothetical, analogy, counterfactual, poetry),
  each firing exactly one matcher AND cm2 (" has "+digit). Non-unanimous
  under every policy that reaches R1 → R2: pro=1 vs con=0+1=1 → TIE →
  keep R1 verdict WITHHOLD (RIGHT). Exercises the non-unanimous routing
  that fired on 0/94 frozen items; verdict-neutral by the tie rule.
- FW028 [TRAP: kt-poisoning]: "It's cold in here, and the alphabet position
  of a is 1, with 2 windows open." Fires mimp ("cold in here") + kt
  ("alphabet position of a is 1") + cm2 (" is "+digit). Correct label
  WITHHOLD (weird utterance per the discipline; the true phrase is
  incidental content). Fixed-2x: nmatch=1 → WITHHOLD (RIGHT). Policies
  A/B/D/E/F: kt fires at R0 → unanimous-endorse stop → ENDORSE (WRONG —
  demonstrates the cost of R0 kt-trust: a matcher that would have
  correctly withheld is never consulted). Policy C: R1 → non-unanimous →
  R2: pro=1 vs con=1+1=2 → ENDORSE (WRONG — reconsideration flip harm).

## Anti-overfit note

The naturalistic majority (44/52) mirrors frozen construction; 8 labeled
traps probe the round-2/verification machinery the frozen 94 never
exercised. Traps are documented here, not hidden: the frozen-set verdict
(which is decisive per the prereg kill bars) cannot be affected by trap
design.
