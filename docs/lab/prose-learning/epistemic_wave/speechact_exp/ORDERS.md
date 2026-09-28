# H-D2 example orderings

**Date:** 2026-09-22 · **Prereg:** PREREG_DECLINE.md §H-D2 (frozen, committed e1f2d2c642e0)
**Answer-key-free:** orderings are computed from the 32 same-concept example
utterances only. c70.txt, b12_false.txt, b12_true.txt were COPIED into each
workdir but never read during ordering design. Prototypicality is computed
WITHIN each concept's 32 examples only.

## Feature definition (identical to delib_vol.zag front-end)

Lowercase; words = `[a-z]+` runs. Features per utterance (deduped within the
utterance): unigrams with word length ≥ 3; adjacent bigrams of ANY word length
joined with `_`; one `first_<firstword>` marker (any length); `qmark` if the
line contains `?`; `exclam` if it contains `!`.

## Algorithms (all deterministic; ties broken by lowest line index)

| Order | Workdir | Algorithm |
|---|---|---|
| Diverse (max-novelty) | `ord_diverse/` | Start with original line 0. Each next line = the remaining line adding the MOST new features (unigrams+bigrams+first/flags) vs the union of all previously chosen lines. |
| Redundant (min-novelty) | `ord_redundant/` | Start with original line 0. Each next line = the remaining line adding the FEWEST new features vs the union of all previously chosen lines. |
| Proto ('best-first') | `ord_proto/` | prototypicality(line) = mean Jaccard similarity of the line's feature set against all 31 other lines' feature sets, descending. |
| Outlier ('worst-first') | `ord_outlier/` | Same prototypicality score, ascending. |

**What the runner sees:** the engine loads `ex_<concept>.txt` from
`<workdir>/examples/` and takes the first N lines at rung N. Reordering changes
exactly which utterances occupy each rung. N=32 is identical across all four
workdirs (all 32 examples present, all permutations of the originals — verified).

## First-4 lines chosen: diverse vs redundant

### sarcasm

Diverse (line indexes in original file: 0, 4, 5, 15):
- `Superb — the plumber cancelled an hour before the appointment. Really classy.`
- `Brilliant. Another pothole ate my hubcap on the way home. Roads like these are a blessing.`
- `Fantastic, my laptop died right in the middle of the pitch. Could not have planned it better.`
- `Oh, delightful — the smoke detector screamed while dinner was still raw. Chef's kiss.`
Redundant (line indexes in original file: 0, 13, 10, 2):
- `Superb — the plumber cancelled an hour before the appointment. Really classy.`
- `Outstanding. The babysitter no-showed and left it in a voicemail.`
- `Amazing — the dentist found three more cavities. My favorite hobby.`
- `Marvelous — the landlord raised the rent and called it a value upgrade.`

### hypothetical

Diverse (line indexes in original file: 0, 7, 1, 12):
- `Suppose the ocean tides rose six feet higher. Where would the coastline end up?`
- `Picture this: every song you hear turns a color. How does your favorite sound look?`
- `What if trees could send each other text messages? Who would gossip most?`
- `Let's say phones only worked outdoors. Would anyone still scroll for hours?`
Redundant (line indexes in original file: 0, 10, 19, 22):
- `Suppose the ocean tides rose six feet higher. Where would the coastline end up?`
- `Suppose your dog could read your thoughts. Would it judge your cooking?`
- `Suppose bread grew on trees like fruit. Which bakery would survive?`
- `Pretend you're the ocean for an hour. What bothers the waves?`

### counterfactual

Diverse (line indexes in original file: 0, 26, 8, 3):
- `If I'd woken up earlier, the sunrise over the bridge would've been mine.`
- `If the dog had stayed quiet, the burglar might never have known we were home.`
- `She might've finished the marathon but for the twisted ankle at mile nine.`
- `If they'd replied by noon, I could've changed my travel dates in time.`
Redundant (line indexes in original file: 0, 23, 19, 5):
- `If I'd woken up earlier, the sunrise over the bridge would've been mine.`
- `If I'd packed a sweater, the mountain evening would've felt warmer.`
- `I'd have waved back if I'd noticed you in the crowd.`
- `I'd have packed an umbrella had the sky looked any darker.`

### analogy

Diverse (line indexes in original file: 0, 4, 6, 13):
- `That old delivery van is a shopping cart with a hood.`
- `The new software is a maze built by someone who lost the map.`
- `Their debate was two radios playing different stations at once.`
- `The budget meeting felt like squeezing water from a dry sponge.`
Redundant (line indexes in original file: 0, 22, 28, 17):
- `That old delivery van is a shopping cart with a hood.`
- `The contract is a spiderweb of fine print.`
- `The new cafeteria is a fishbowl at lunchtime.`
- `The new hire is a sponge soaking up every detail.`

### poetry

Diverse (line indexes in original file: 0, 10, 13, 15):
- `The streetlamps blink awake, one by one, like tired commuters.`
- `The lake folds its dark hands around the drowned sun.`
- `Thunder rolls its heavy carts across the black sky.`
- `Smoke curls up from the chimney, writing slow questions.`
Redundant (line indexes in original file: 0, 4, 7, 11):
- `The streetlamps blink awake, one by one, like tired commuters.`
- `The city exhales neon into the violet evening.`
- `Dusk settles like dust on the empty playground.`
- `Morning stretches, yawning golden across the wheat.`

### implicature

Diverse (line indexes in original file: 0, 18, 1, 2):
- `The window over the sink has been open all morning.`
- `I can't find the remote and the show starts in a couple of minutes.`
- `My coffee cup's been empty since the waitress last came by.`
- `Someone parked their bike right in front of the garage door.`
Redundant (line indexes in original file: 0, 17, 24, 6):
- `The window over the sink has been open all morning.`
- `The printer has been out of paper since Tuesday.`
- `Everybody else at the table already ordered.`
- `It's freezing on this side of the couch.`

### joke

Diverse (line indexes in original file: 0, 13, 7, 30):
- `My hamster runs a tiny accounting firm and files my taxes every April.`
- `I tried to parallel park a rainbow, but it kept sliding into the wrong spot.`
- `The oak tree outside my window is writing its memoirs. Chapter one is acorns.`
- `My wallet got lost inside a dream, so I am short on cash this week.`
Redundant (line indexes in original file: 0, 4, 6, 10):
- `My hamster runs a tiny accounting firm and files my taxes every April.`
- `My dentist moonlights as a lighthouse keeper on the weekends.`
- `My smartphone developed a crush on the microwave. Reception is hopeless.`
- `My elbow keeps entering dance competitions without telling me.`

## Layout

Each of `ord_diverse/`, `ord_redundant/`, `ord_proto/`, `ord_outlier/` contains:
`examples/ex_{sarcasm,hypothetical,counterfactual,analogy,poetry,implicature,joke}.txt`
(reordered) plus copies of `c70.txt`, `b12_false.txt`, `b12_true.txt`.

