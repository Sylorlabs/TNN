# RT3c ATTACK REPORT — HELL-HOLE V4 fresh re-attack on the twice-repaired joke classifier

Date: 2026-09-24. Crew: rt3c (blind). Target: `redteam/rt3fix2/g_intent6_v4fix2.zag`
(SHA `b79ef7595cca1ba1b7da27b18870fa3a15b1d8cf98335ca774f2343748a970f8`,
matches FIX_REPORT.md; copied byte-identical into rt3c/, never modified).
Pure Zag, zero RNG. No commit.

## Blindness

Read ONLY: the target source, `PREREG_V4_RT.md`, rt3fix2's FIX_REPORT.md
(repair spec). Did NOT read rt1/rt1b/rt1c/rt1d/rt1fix*/rt2/rt2b/rt2fix*/rt2residue/
rt3/rt3b/rt3fix/rt4/rt4b/rt4fix, any ATTACK_REPORT.md, or builders' scratch
crews. All 76 items composed fresh for this round.

Corpus (`rt3c_corpus.tsv`) written 2026-09-24T02:28:40 PDT — BEFORE the runner
was written/built (mtime 09:28 < build 09:29 UTC). Format:
`id \t claim \t evidence \t oracle`. Runner (`rt3c_run.zag`, own code) feeds
CLAIM ONLY to `g_classify`; the evidence column carries family/mechanism notes
for this report. Output: `id \t WORD \t codes`, WORD ∈ JOKING(2)/SATIRE(3)/
UNCERTAIN(5).

Scoring: deadpan hit = oracle UNCERTAIN but output JOKING or SATIRE;
joke miss = oracle JOKING but output UNCERTAIN.

## Corpus

76 novel items: 38 sincere non-jokes (oracle UNCERTAIN), 38 real jokes
(oracle JOKING).

Deadpan families: factual Q&A (D01–D05), sincere denials (D06–D09),
bar-shaped sincere (D10–D12), whisper sincere (D13–D14), habit/longevity
biographies (D15–D17), hostile-but-sincere rants (D18–D20),
sincere contrastive statements (D21–D23), simile/trope-word sincere
(D24–D26), joke-word sincere (D27–D28), deadpan factual (D29–D30),
true biographies (D31–D32), contrast sincere (D33–D35),
absurd-entity-word sincere (D36–D38).

Joke families: puns (J01–J06), absurd premises (J07–J08), misdirection
(J09–J10), irony (J11–J12), meta/dry one-liners (J13–J15), riddle &
distrust puns (J16–J18), whisper jokes (J19–J21), meta/binary (J22–J23),
dry/meme (J24–J25), proverb/prefix/eyebrow controls (J26–J28),
riddle/distrust (J29–J30), satire headlines (J31–J32),
dry/simile/classic (J33–J38).

## Results

### Bar 1 — deadpan installs: 3 → FAIL (bar: ≥3)

| id | output | codes | claim | mechanism |
|---|---|---|---|---|
| D21 | JOKING | N_NEG | I don't hate the new schedule; I love the old one. | j_neg_turn: "don't" pre-pivot + antonym hate→love |
| D22 | JOKING | N_NEG | We don't enjoy the audit, but we do finish it on time. | j_neg_turn: aux flip don't→do across "but" |
| D23 | JOKING | N_NEG | I can't approve the request, but I can review it again tomorrow. | j_neg_turn: aux flip can't→can across "but" |

All other 35 deadpan items UNCERTAIN (0 installs in Q&A, denials, bar-shape,
whisper, biography, rant, trope-word, absurd-word families).

### Bar 2 — missed jokes: 24 → FAIL (bar: ≥3)

All 24 output UNCERTAIN / R_NO_PATTERN. Full list: J01 (time-flies pun),
J02 (lost-interest pun), J03 (graveyard pun), J04 (anti-gravity pun),
J05 (pointless pun), J06 (alge-bra pun), J07 (goldfish custody),
J08 (replace gravity), J10 (Batman misdirection), J11 (password123 irony),
J12 (fire-station irony), J13 (unemployed meta), J16 (arrays riddle),
J19 (whisper soup), J22 (two-types meta), J24 (brown thumb),
J29 (impasta riddle), J31/J32 (satire headlines), J33 (meeting moved),
J34 (stepladder pun), J36/J37 (simile one-liners), J38 (bike/forgiveness).

Caught jokes (14/38): J09 N_PUN (two-places/those-places pair), J14 N_TAG
(we'll-see-about-that), J15 N_NEG (suffer→enjoy antonym), J17 N_PUN
(baker/dough pair), J18/J30 R_PUN2 (atoms/make-up), J20/J21 N_WHISPER
(too-crowded / right-behind-you tags), J23 N_PUN (kinds-of-people+binary),
J25 N_NEG (don't→do aux flip), J26 N_PUN (early-bird/cheese),
J27 N_NEG (superstitious→stitious prefix echo), J28 N_PUN (eyebrows/surprised),
J35 N_TAG (never-meet). Zero joke→SATIRE anomalies.

Per-family joke catch rate: puns 0/6, absurd premises 0/2, misdirection 1/2,
irony 0/2, meta/dry 2/3, riddle/distrust 2/4, whisper 2/3, proverb/prefix
controls 3/3, satire headlines 0/2, simile/classic 1/6.

## Root causes

1. **N_NEG still fires on shape alone.** The round-2 "turn" for negation is:
   any negation word before any pivot + any aux-flip/antonym/prefix-echo
   after. Ordinary sincere contrastive sentences ("I can't approve the
   request, but I can review it again tomorrow") satisfy it. D21–D23 are
   not jokes by any human reading; the incongruity gate does not test for
   incongruity, only for polarity reversal.
2. **Coverage is lexicon-bound, not turn-bound.** Every install rule pairs
   its shape with a FIXED lexicon: ~12 pun pairs (j_pun_turn), 11 absurd
   entities, 12 punch tags, a fixed QA-punch word list, fixed irony markers.
   All 24 missed jokes carry genuine incongruity turns (puns J01–J06/J34,
   absurd premises J07–J08, irony J11–J12, novel riddles J16/J29, satire
   headlines J31–J32) in words outside those lists → R_NO_PATTERN.
   Round 2 replaced shape-only rules with shape+lexicon rules; novel
   incongruity remains invisible.

## Determinism

Two full runs byte-identical:
- run1.txt = run2.txt, SHA `f3045be3158081c9e650cbff39850ffeb8f7e01a425f6ae3ceb014c28cf6ba3e`
- corpus SHA `d7ae515c56e8a502c1317f0010e4d2e9fe2ec07770764483cb07baabfe08c518`

## Verdict

**FAIL both bars.** Bar 1: 3 deadpan installs (D21–D23, all N_NEG) ≥ 3.
Bar 2: 24 missed jokes ≥ 3. Fix required before verdict/commit:
(a) N_NEG needs a genuine-incongruity test, not polarity-reversal alone;
(b) the turn lexicons (pun pairs, absurd entities, punch tags, QA punches)
need a generalization story, or the classifier must WITHHOLD-claim only
what its lexicons cover.

## Honest limits

Oracle labels are the attacker's judgments; "missed" jokes lean on shared
cultural knowledge (classic puns, memes). The runner feeds claim only;
evidence column is documentation. Two predicted-miss items were actually
caught (J09 via the two-places pair, J17 via the baker/dough pair —
both were in the fixed lexicons; prediction error documented, not hidden).
