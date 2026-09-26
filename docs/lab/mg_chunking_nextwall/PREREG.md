# NEXT-WALL PREREGISTRATION — fresh 26-trap battery (2026-09-26)

## Rule of the game

The learned chunking policy is FROZEN. This battery tests it on 26 questions it
never saw during derivation, without re-deriving or tuning anything. The battery
runs through the production entry point (`../mg_chunking_promote/intake.zag`),
which is the exact file committed as live intake.

## Anti-tuning statement

Every oracle below was fixed by the generator (`gen_wall.py`) BEFORE the first
run: the generator asserts each oracle against an independent Python computation
and refuses to emit the battery if any assert fails. No oracle was changed after
seeing system output. Two generator bugs were caught by the generator's own
asserts before the first run (a sentence-period strip and the trap count 25->26);
no question, oracle, or trap was added, removed, or reworded after any run.

## The 26 traps

| # | Class | Question | Text | Oracle | What it attacks |
|---|---|---|---|---|---|
| W00 | A | how many sentences in the cat sat. the dog ran. | the cat sat. the dog ran. | 2 | sentence granularity (no sentence candidate exists) |
| W01 | A | what is the 2nd sentence of the cat sat. the dog ran. | the cat sat. the dog ran. | the dog ran | sentence addressing |
| W02 | A | how many lines in a\nb\nc | a\nb\nc | 3 | line granularity |
| W03 | B | what is the letter after the 2nd letter of fox in the quick brown fox | the quick brown fox | x | 2-hop relative addressing (letter after X) |
| W04 | B | how many e's in the word after the in the cheese wheel | the cheese wheel | 3 | relative word addressing ("word after X"); whole-text reading gives 6 |
| W05 | B | what is the 1st letter of the word before fox in the quick brown fox | the quick brown fox | b | relative word addressing ("word before X") |
| W06 | B | spell the word after quick backwards in the quick brown fox | the quick brown fox | nworb | address-then-reverse (word-scoped reversal) |
| W07 | C | what is the second letter of strawberry | strawberry | t | spelled ordinal "second" |
| W08 | C | how many letters in the third word of the quick brown fox | the quick brown fox | 5 | spelled ordinal "third" |
| W09 | D | does the quick brown fox contain ick bro | the quick brown fox | yes | cross-word char span (word match must fail, char scan adapts) |
| W10 | D | does hello world contain xyz | hello world | no | clean miss, both-ends scan |
| W11 | D | does abc contain abcdef | abc | no | needle longer than text |
| W12 | E | how many words in (empty) | (empty) | 0 | degenerate empty input |
| W13 | E | does hello contain hello world | hello | no | degenerate: text shorter than needle |
| W14 | E | how many q's in strawberry | strawberry | 0 | zero-count letter |
| W15 | F | how many s's in MISSISSIPPI | MISSISSIPPI | 0 | case sensitivity |
| W16 | F | does mississippi contain issi | mississippi | no | word-boundary vs substring (whole-word match only) |
| W17 | G | what is the 2nd letter of the in the quick brown the fox | the quick brown the fox | h | repeated target word ("the" x3); oracle = first occurrence |
| W18 | H | what is the 1st letter of the 2nd word of the last word of hello worldly words | hello worldly words | ? | true two-level nesting; designed unanswerable ('?' = honest abstention) |
| W19 | I | what is the 2nd word of the 1st sentence of the cat sat. the dog ran. | the cat sat. the dog ran. | cat | sentence->word hybrid addressing |
| W20 | J | how many words in " the  quick  fox " | " the  quick  fox " | 3 | doubled spaces / padding |
| W21 | J | what is the 3rd letter of " ab" | " ab" | b | leading-space text, clamp at end |
| W22 | M | how many 7's in 777a7b7 | 777a7b7 | 3 | digit target |
| W23 | N | what is the 0th letter of abc | abc | c | index 0 (no clamp rule learned; oracle = last char by code convention) |
| W24 | N | what is the 10th letter of abc | abc | a | clamp past end (oracle = last char by code convention) |
| W25 | E | what is the 1st letter of (empty) | (empty) | ? | LAST: empty-text position; '?' = no character exists |

Notes:
- W04 is ambiguous in English (whole-text reading gives 6); the trap targets the
  relative reading ("e's in [the word after 'the']" = "cheese" = 3), which needs
  addressing the system demonstrably lacks (cf. W05/W06). Scored against the
  trap's documented intent.
- W23/W24 oracles follow the code's own clamp convention (idx<1 -> last char);
  the derivation battery never taught a clamp rule, so these probe what the
  frozen code does, not what "should" happen.
- W25 is emitted LAST so a crash cannot swallow the other 25 results.

## Kill bars / reporting duties (not pass/fail gates)

This battery has no promotion gate — it is a measurement. The verdict must report,
per trap class, whether the cause of each break is:
(a) parser/classifier failure, (b) finite candidate set (new granularity),
(c) addressing/nesting failure, or (d) adaptation failure/success.
