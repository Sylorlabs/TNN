# HELL-HOLE V4 — RT3d fresh blind re-attack on thrice-repaired joke classifier

Date: 2026-09-24. Target: `redteam/rt3fix3/g_intent6_v4fix3.zag`
(SHA `4157f1224b9a88310b902196caa880d0889c2a44c8b070c346274ac8fb398b4c` —
matches rt3fix3 FIX_REPORT.md). Pure Zag, zero RNG. Workdir: `redteam/rt3d/`.

## Blindness

Read ONLY: the target source, the frozen prereg `PREREG_V4_RT.md`, and
rt3fix3's `FIX_REPORT.md` (repair spec, explicitly allowed). Did NOT read
any prior attack corpus, any prior ATTACK_REPORT.md, any builder workdir,
or any frozen v4 battery. All 95 items are novel, written fresh 2026-09-24.

## Corpus

`rt3d_corpus.tsv` — 95 items, frozen **2026-09-24T09:39:30Z, before any
build or run** (mtime 09:39:38 < build 09:40:24 < run 09:40:27; K-RTBLIND
satisfied). Format `id \t claim \t evidence \t oracle`.
SHA256: `bcf0806120bf803ce38ffe49d4eb7be357b32c118f35f0bdc3b9d7068477c3f5`

- 55 deadpan/non-jokes (oracle NONJOKE): factual Q&A, sincere denials,
  deadpan recounts, sincere contrastive/negation sentences, sincere
  advice/warnings/instructions, hostile-but-sincere rant, sincere news,
  statements containing joke-shaped words.
- 40 real jokes (oracle JOKE): riddles, dry one-liners, bar jokes, bathos,
  misdirection, irony, confession parodies, absurd advice, sarcasm.

Verdict mapping (documented): JOKING(2) or SATIRE(3) = install;
UNCERTAIN(5) = withhold. SATIRE is a positive classification, not a miss.

## Runs (2x, byte-identical — K-RTDET satisfied)

Runner `rt3d_run.zag` (same I/O contract as the repair-spec runner: claim
only fed to `g_classify`, evidence column not fed).

- `rt3d_run1.txt` SHA256: `567fb2e8e7f58dc40e3f34968eac61af0413b23b9a047f1ea7a41918b08d3823`
- `rt3d_run2.txt` SHA256: `567fb2e8e7f58dc40e3f34968eac61af0413b23b9a047f1ea7a41918b08d3823`
- Verdict distribution: 70 JOKING, 2 SATIRE, 23 UNCERTAIN (all 95 ids match).

## Bar 1 — deadpan/non-joke installs: 52/55 → FAIL (bar: ≥3)

Every install rule from rounds 1–3 fires on sincere text. Per-family:

| Family | n | installs | firing codes |
|---|---|---|---|
| Factual Q&A (punch word in sincere answer) | 5 | 4 | N_QA ×4 |
| Sincere denials | 2 | 2 | N_DENY ×2 |
| Deadpan bar recounts | 2 | 2 | N_BAR ×2 |
| Sincere contrastive/negation | 7 | 7 | N_NEG ×7 (prefix-echo ×4, tense-twist ×1, antonym+valence ×1, antonym+abs-undercut ×1) |
| Sincere advice/warnings/instructions | 20 | 18 | P_DA1E/1T/4H/3D/4N/5B/5A/3E/2A/4I/4W/2D/1L/1C/DB1P/DB1S/DB1D, R_IRONY, P_DA5D |
| Deadpan w/ punch tags | 3 | 3 | N_TAG ×3 |
| Sincere whisper recount | 1 | 1 | N_WHISPER |
| Sincere w/ trope words | 3 | 3 | R_TROPE ×3 |
| Sincere news + absurd entity | 1 | 1 | R_SATIRE (SATIRE) |
| Sincere "said/told … so …" | 2 | 2 | N_COMPLY ×2 |
| Sincere news deflation | 2 | 2 | N_DEFLATE ×2 |
| Sincere figurative payoff | 1 | 1 | N_PAYOFF |
| Sincere pun-pair sentences | 6 | 5 | N_PUN ×2, N_PUN_GROW, N_PUN_JUMP, N_PUN_LINE |

Hit list (id — verdict/code — claim):
- D01 N_QA "What grows best in sandy soil? A carrot, apparently."
- D03 N_QA "What did the toddler grab? The bugs in the garden."
- D04 N_QA "Why was the yield so low? The harvest was awful this year."
- D05 N_QA "What did the electrician test? The old brick wiring."
- D06 N_DENY "This statement is not a joke right now: the server is down for maintenance."
- D07 N_DENY "I am not kidding right now: the bridge is closed."
- D08 N_BAR "We walked into a bar downtown and laughed at the band's first song."
- D09 N_BAR "He walked into a bar with a long face after the funeral."
- D10 N_NEG "I never liked the superstar, but the star was fine."
- D11 N_NEG "I do not trust the incompetent clerk; the competent one handles it."
- D12 N_NEG "I never liked the dissatisfied tone; the satisfied customers left early."
- D13 N_NEG "They were not impressed by the unimpressive debut, but the impressive finale saved it."
- D14 N_NEG "I would approve the budget, but you did not submit it."
- D15 N_NEG "I do not hate the delay, but I love the extra time to fix mistakes."
- D16 N_NEG "I never repeat my mistakes; I thought I made one once, but I was wrong."
- D17 P_DA1E "The toddler ate some play-doh; we called poison control."
- D18 P_DA1T "She drank bleach by mistake; call emergency services."
- D19 P_DA4H "Do not hug the bear; it is a wild animal."
- D20 P_DA3D "Do not take a toaster into the tub; water conducts electricity."
- D21 P_DA4N "Stop breathing so fast; you are hyperventilating."
- D22 P_DA5B "Iron the shirt you will wear; wrinkles look unprofessional."
- D23 P_DA5A "Replace the tire with the spare; bring food for the wait."
- D25 P_DA3E "Charge the phone; the microwave clock is blinking."
- D26 P_DA2A "Apply lemon juice to the paper cut; it stings but helps."
- D27 P_DA4I "Do not punch the wall; you will hurt your foot."
- D28 P_DA4W "Take them home; the ducks need shelter tonight."
- D29 P_DA2D "Drop the table; mind your toes on the stairs."
- D30 P_DA1L "Take melatonin for sleep; avoid laxatives before bed."
- D31 P_DA1C "Add glue to the mixture to bind the pages."
- D32 P_DB1P "Use the flash; it is too dark for the photo."
- D33 P_DB1S "We were lost at sea; the vacation was ruined."
- D34 P_DB1D "Dress up as a wolf; the sheep will scatter."
- D35 R_IRONY "He smoked two packs a day and lived to ninety; imagine that."
- D36 P_DA5D "The moon is made of cheese, according to the old myth."
- D37 N_TAG "It is Monday here; already tomorrow in Sydney."
- D38 N_TAG "I read the new tax form twice; I do not get it at all."
- D39 N_TAG "The meeting moved to Thursday; I am not so sure why."
- D40 N_WHISPER "She whispered that she had no idea where she is; the patient had wandered off."
- D41 R_TROPE "The free trial was literally the best part of my morning."
- D42 R_TROPE "I downloaded the update; I am sick to death of the old bugs."
- D43 R_TROPE "This free upgrade is garbage; I am sick to death of it."
- D44 R_SATIRE "Local experts say the cheese festival drew a full crowd; details pending."
- D45 N_COMPLY "The vet said the diet was fine, so we named the hamster Cheese."
- D46 N_COMPLY "The marine guide told us to watch for wildlife, so we photographed a ghost crab."
- D47 N_DEFLATE "Breaking: the audit team found the error was just a rounding issue."
- D48 N_DEFLATE "Area experts found the strange noise was just the wind."
- D49 N_PAYOFF "As far as the bonus goes, it was a mistake in their system."
- D50 N_PUN "Stop the car; it stopped raining."
- D51 N_PUN "I was running late; the bus did not catch the light."
- D52 N_PUN_GROW "His facial hair was patchy for years, but it finally grew on over the last winter."
- D54 N_PUN_JUMP "She cleared the hurdles, and the crowd roared as she kept jumping higher."
- D55 N_PUN_LINE "The numerator was clearly wrong; the fraction made no sense."

Three deadpan items stayed UNCERTAIN (honest non-hits; corpus frozen, not
edited): D02 (punch word "field" sits in the *question*, N_QA only scans the
answer span), D24 (purpose infinitive "To save money" at text start —
`j_purpose_to` requires a leading space, so `just`=0), D53 (both pair words
precede the ";" pivot; `j_pair_turn` needs the pivot *between* them).

## Bar 2 — missed jokes: 17 mechanism misses → FAIL (bar: ≥3)

20 joke positive controls installed as designed (J01, J02, J17–J19,
J21–J32, J34, J35, J37 — incl. J32 as SATIRE). Misses:

**A. Dead-code pun detectors — 5 misses.** The header documents
"idiom + literal-context activation" pun detectors, but `j_pun_grow`,
`j_pun_over`, `j_pun_jump`, `j_pun_line`, `j_pun_comeout` have **zero call
sites in `g_classify`** (verified by grep). The wired-in `N_PUN_*` rules use
narrow fixed pairs instead, so the documented general mechanism is inert:
- J03 "My beard really grew on me this winter." (`j_pun_grow`: "grew on me" + growable "beard"; N_PUN_GROW needs literal "facial hair")
- J04 "He has a fear of hurdles, but he is finally getting over it." (`j_pun_over`; N_PUN_OVER needs "speed bumps")
- J05 "Do not jump to conclusions; the trampoline is broken." (`j_pun_jump`; N_PUN_JUMP needs "hurdles")
- J06 "There is a fine line between the numerator and the denominator." (`j_pun_line`; N_PUN_LINE needs "fraction")
- J07 "The stars come out, and so do my dentures." (`j_pun_comeout`; N_PUN_OUT pair misfires — words-between <6, no pivot)

**B. Lexical gaps in documented rules — 9 misses.**
- J08 "A horse limps into a bar and orders a drink with a long face." — N_BAR opener only lists walked/walks/walk; any other verb ("limps") misses.
- J09 "There are 10 types of people: those who understand binary and those who do not." — `j_incomplete_list` only recognizes two/three/four/five; the numeral "10" (the classic binary joke) misses.
- J10 "Guess why the bicycle fell over? It was two-tired." — `j_qa_opener` lists "guess what" but not "guess why".
- J11 "Local woman discovers her fountain of youth was just good lighting." — `j_deflation` register gate lists "local man" but not "local woman".
- J12 "My coach advised me to be myself, so I showed up as Batman." — `j_absurd_compliance` advice gate lists said/told but not "advised".
- J13 "I could not always fix the bug, but when I could, it was a missing semicolon." — `j_aux_flip` lists 6 aux pairs; couldn't/could absent, so the "when I do" confession template can't fire.
- J14 "Embrace uncertainty; hug it like an old friend." — R_PUN1's F_ABSTRACT lists 6 nouns; "uncertainty" absent though the dual-verb+abstract+enact shape matches exactly.
- J16 "I was going to tell you a joke about construction, but I am still working on it." — `j_tense_twist` past-failure inventory (did not/didn't/was not/were not) misses the "still working" anti-climax.
- J36 "I asked the librarian for books on paranoia; she said they're right behind me." — punch-tag lexicon has "right behind you" but not "right behind me".

**C. Inventory/nesting inconsistencies — 3 misses.**
- J15 "I adore my migraines." — `j_valence_clash` is only reachable inside `j_neg_turn` (needs pivot+negation); a standalone valence-clash one-liner has no rule.
- J20 "I don't cry at movies, but I laugh at every minute of this disaster." — the (cry,laugh) pair IS in `j_antonym`, but "laugh" is absent from the `j_pos_verb` inventory, so the valence-clash gate can never fire for this documented pair (verified: hate/love and suffer/enjoy variants install; cry/laugh never does).
- J33 "To stay awake during the meeting, eat some chalk." — `j_purpose_to` requires " to " with a leading space; a text-initial "To stay…" is invisible, so `just`=0 and P_DA1E can't fire.

**D. Comprehension ceiling — 3 misses, NOT counted as mechanism hits** (per
task note; each classified individually):
- J38 "Why did the student bring a ladder to class? He wanted to go to high school." — dual-meaning "high school" needs POS/wordplay knowledge.
- J39 "My grandfather's password was password123." — needs world knowledge that password123 is weak (expertise/practice irony).
- J40 "Time flies like an arrow; fruit flies like a banana." — verb/noun duality of "flies" needs POS + dual-meaning knowledge.

## Honest limits

- Oracle labels are the attacker's; 3 deadpan items designed as hits stayed
  UNCERTAIN due to item-construction slips (documented above) — counted as
  non-hits, corpus untouched post-run.
- J20/J33 were designed as positive controls but exposed genuine mechanism
  gaps during analysis; classified as mechanism misses with the discovered
  mechanism, not the intended one.
- SATIRE verdicts (D44, J32) counted as installs per the documented mapping.
- Corpus/items are English string-pattern probes; no claim about other
  languages or modalities.

## Verdict

**FAIL both bars.** Bar 1: 52 deadpan/non-joke installs (bar ≥3). Bar 2: 17
mechanism misses (bar ≥3), plus 3 ceiling-classified misses not counted.
Determinism: 2× byte-identical runs (SHA `567fb2e8…08d3823` twice), pure Zag,
zero RNG. Not committed.
