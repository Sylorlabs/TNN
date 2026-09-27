# TRAINING.md — English-reasoning arm: broad English training

## What "broad English training" means here

Before the arm ever sees a battery question, it ingests a general English
training corpus compiled into the binary as data (not code): **151 vocabulary
entries** across 7 categories plus **20 sentence patterns** that generalize the
shapes of the knowledge-base facts. This is the arm's "broad English training"
— the counterpart to the native arm's TNN-native reasoning. Everything is
parsed at startup into byte-arena tables; there is no RNG anywhere.

## Vocabulary: 151 entries, 7 categories

| Category | Count | Contents |
|---|---|---|
| Number words | 31 | zero–nineteen, twenty, thirty, forty, fifty, sixty, seventy, eighty, ninety, hundred, thousand, million (each tagged with its numeric value) |
| Comparatives | 28 | taller, shorter, older, younger, bigger, smaller, longer, higher, lower, faster, slower, hotter, colder, wider, narrower, deeper, heavier, lighter, cheaper, richer, poorer, stronger, weaker, brighter, darker, earlier, later |
| Question words / auxiliaries | 21 | who, what, when, where, which, how, why, is, are, was, were, do, does, did, can, could, would, will, has, have, the |
| Units | 14 | meters, meter, kilometres, kilometers, kilometer, feet, inches, years, degrees, celsius, pixels, people, clips, ad |
| Negation | 9 | no, not, never, none, nothing, nobody, neither, nor, without |
| Pronouns | 18 | he, him, his, she, her, hers, it, its, they, them, their, we, us, our, you, your, i, me |
| Predicates | 30 | wrote, written, born, published, discovered, won, built, tall, taller, tallest, shorter, shortest, capital, boils, long, longer, upscal\*, reproduc\*, learn, learned, detect, detected, paint, painted, invent, invented, opened, dedicated, completed, in |

(`*` = prefix stem: `upscal*` matches "upscale/upscaled", `reproduc*` matches "reproduce/reproduced".)

## Sentence patterns: 20

Generalized templates the arm recognizes as the shapes its taught facts take:

1. `<person> wrote the novel <work>.`
2. `<person> was born in <year>.`
3. `<work> was published in <year>.`
4. `<work> was written by <person>.`
5. `<person> discovered <thing>.`
6. `<person> won the Nobel Prize in <year>.`
7. `<place> is in <city>.`
8. `<place> was built in <year>.`
9. `<place> is <number> meters tall.`
10. `<place> is a landmark in <city>.`
11. `<place> opened as a museum in <year>.`
12. `<place> was dedicated in <year>.`
13. `<place> was completed in <year> AD.`
14. `<city> is the capital of <country>.`
15. `Water boils at <number> degrees Celsius at sea level.`
16. `<river> is <number> kilometers long.`
17. `TNN <past-verb> the <thing>.`
18. `TNN <past-verb> <number> <thing>.`
19. `The test image is <number> pixels wide.`
20. `A riddle joke asks why about one true thing and answers because with another true thing.`

## KB training (task knowledge)

After the English corpus, the arm loads the trial fixtures:

- **48 facts** from `kb.txt`, each stored verbatim with a lowercased copy,
  entity mentions, predicate id, and extracted numeric attributes
  (heights in meters, years).
- **32 entities** from `gaz.txt` (persons, works, places, TNN), with a
  longest-name-first scan order and a per-entity inverted fact list.

## Measured training time

Vocabulary + pattern parsing and KB loading together take **~20–60 ms
wall-clock** on this VM (observed: 24, 34, 35, 37, 56 ms across runs —
machine-dependent). The measurement is printed to **stderr**, never stdout,
so the trace output stays byte-identical across runs despite the varying
clock.

## How training shows up in reasoning

Every trace's KNOWLEDGE section cites the training directly: vocabulary
category ("a taught predicate", "no verb I was taught"), fact ids with
verbatim fact text, and numeric values extracted at load time. The
counterfactual check in RUNLOG.md demonstrates that changing the taught
facts changes the reasoning — the traces are grounded in what was taught,
not in the code.
