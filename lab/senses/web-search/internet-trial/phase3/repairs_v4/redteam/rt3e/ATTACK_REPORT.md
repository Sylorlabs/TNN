# RT3e ATTACK REPORT — fresh blind re-attack on the 4x-repaired joke classifier (natural corpus)

**Date:** 2026-09-24. **Attacker:** RT3e subagent (blind).
**Target:** `/home/hatch/workspace/scratch-hellhole/redteam/rt3fix4/g_intent6_v4fix4.zag`
(classifier; run via `g_classify(claim, url, codes, markers)` → 2=JOKING / 3=SATIRE / 5=UNCERTAIN / other=OTHER).
**Workdir:** `/home/hatch/workspace/scratch-hellhole/redteam/rt3e/`

## Blindness statement
- Read: target source (API + post-run mechanism attribution), frozen prereg
  `redteam/PREREG_V4_RT.md`, own corpus. Nothing else.
- Did NOT read: any FIX_REPORT.md (any round), any rt1*/rt2*/rt3*/rt3b/c/d,
  rt3fix*, rt4*, or builders' scratch-hellhole/crews/*.
- Corpus (40 deadpan + 40 jokes, oracle-labeled, timestamped headers) written
  BEFORE any build or run. mtimes (UTC): deadpan TSV 10:08:59, jokes TSV
  10:09:04, runner 10:09:09, binary 10:10:10, runs 10:10:13/14. Corpus-before-run holds.
- All 80 items novel, written from everyday life first; jokes include classics
  people retell plus novel invented jokes. No items constructed from trigger shapes.

## Corpora
| file | n | sha256 |
|---|---|---|
| rt3e_deadpan.tsv (oracle OTHER) | 40 | 55a8038d3b1c374fe64c643dab930015db63c0cc807ac4903e537dee38e39e35 |
| rt3e_jokes.tsv (oracle JOKING) | 40 | 446861cd38ce8155b42eb2533b727e80b0ad756899d84f18c933bf3ff25efac2 |

Runner: `run_e.zag` (same pure-Zag pattern as the target's own runner; feeds CLAIM
only). Zero RNG. Each corpus run 2x.

## Determinism (K-RTDET)
| run | sha256 |
|---|---|
| out_deadpan_1.txt | 569adb5a3e1d99131edc2da6a8fce4b60bb45a0926cde4dc93b04b4f88d4126c |
| out_deadpan_2.txt | 569adb5a3e1d99131edc2da6a8fce4b60bb45a0926cde4dc93b04b4f88d4126c (identical) |
| out_jokes_1.txt | 2f0f0d55fb6ab6aac635f018ec6842d670c0176f36475eb70aa38158a7fa716d |
| out_jokes_2.txt | 2f0f0d55fb6ab6aac635f018ec6842d670c0176f36475eb70aa38158a7fa716d (identical) |
Both families byte-identical across runs. Measurement valid.

## Family results
- **Deadpan (n=40):** 40 UNCERTAIN, **0 JOKING installs**. Bar (≥3 installs → FAIL): **PASS**.
- **Jokes (n=40):** 12 JOKING, 28 UNCERTAIN (all R_NO_PATTERN), 0 SATIRE.
  Raw misses: 28. Mechanism misses: **2**. Ceiling misses: 26. Bar (≥3 mechanism
  misses → FAIL): **PASS (narrow, 2)**.

Caught jokes (12): J01 N_PUN (eyebrows/surprised pair), J02 N_QA ("make up"
punch lexicon), J07 N_BAR (walks-into-a-bar), J08 N_TAG ("right behind you"),
J10 N_NEG (suffer/enjoy antonym), J11 N_QA ("outstanding"/"field"), J13 N_TAG
("we'll see about that"), J14 N_TAG ("never meet"), J16 N_QA ("fsh"),
J20 N_QA ("two-tired"), J38 N_PUN_OVER ("getting over it"), J40 N_PUN
(suitcase/baggage pair).

## Mechanism hits (count toward bar)
Root cause for both: `j_qa_punch` (g_intent6_v4fix4.zag:1255) is a FIXED
punch-word lexicon ("other side","make up","off and on","hook, line",
"two-tired","big plus","brick","awful","fsh","outstanding","field","carrot",
"bugs","waved","crumby"). `j_qa_turn` handles the riddle template generally
(opener list even includes "knock knock"), but a riddle-shaped joke whose
canonical punch word is absent from the lexicon misses — same template and
same device as caught items.

- **J28** "Why did the math book look so sad? It had too many problems."
  → UNCERTAIN/R_NO_PATTERN. Identical riddle shape to caught J20 ("Why did the
  bicycle fall over? Because it was two-tired"). "problems" (the canonical
  punchline, parallel to listed "field"/"outstanding") absent from lexicon.
- **J32** "What do you call fake spaghetti? An impasta."
  → UNCERTAIN/R_NO_PATTERN. Identical riddle shape to caught J16 ("What do you
  call a fish with no eyes? A fsh"). "impasta" is a nonce punch-word exactly
  like listed "fsh"/"crumby"; zero overfire risk. Pure coverage gap.

Fix direction (for the repair crew): extend the punch lexicon / add the
("math book","problems")-style setup+punch pairs. No architecture change needed.

## Ceiling misses (26 — documented architecture limit, not counted)
Each needs genuine semantic comprehension the architecture does not implement
(no phonetics engine, no duality/POS analysis, no idiom/world-knowledge base;
mechanisms are fixed lexicons/lists + structural templates):
- Phonetic duality: J03 (seafood/see food), J04 (knock-knock "lettuce/let us";
  opener IS recognized, payoff needs phonetics), J35 (tearable/terrible).
- Novel dual-meaning puns (not in pair lists): J06 (lost interest),
  J17 (put down), J29 (working on it), J33 (uplifting).
- Idioms: J15 (play by ear), J18 (makes my day), J34 (days were numbered),
  J39 (dying to leave).
- World knowledge: J12 (utility companies = bills), J19 (KitKat slogan),
  J24 (Siri/front camera), J26 (skydiving without parachute = death),
  J31 (gazpacho served cold), J36 (phone bill can't have an area code —
  hyperbole gate is absurd-entity-lexicon-bound by design).
- Pragmatic inference / ambiguity: J05 (wallet/onion simile mapping),
  J09 (bed/procrastination observation), J21 (grandma wifi hyperbole),
  J22 (ten pounds/thirteen to go — arithmetic irony), J23 (library/murder —
  theory-of-mind), J25 (house was clean — implied now dirty),
  J27 (Thesaurus Club — synonym knowledge), J30 (dog's bike — attachment
  ambiguity), J37 (sleeping eyes closed — deadpan literalism).

## Verdict
- K-RTC bar 1 (deadpan installs ≥3): **PASS** — 0/40.
- K-RTC bar 2 (joke misclassifications ≥3, ceiling excluded): **PASS** — 2/40
  mechanism misses (28 raw misses, 26 documented ceiling).
- K-RTDET: **PASS** — 2x byte-identical.
- K-RTBLIND: **PASS** — corpus predates build and runs (mtimes + SHAs above).

## Honest limits
- Corpus is single-attacker natural writing; 40+40 is the prereg minimum.
- Ceiling/mechanism split is the attacker's judgment, documented per item
  above; the two mechanism hits share one root cause (punch-lexicon coverage).
- No SATIRE verdicts observed in either family this round.
- Not committed (per task).
