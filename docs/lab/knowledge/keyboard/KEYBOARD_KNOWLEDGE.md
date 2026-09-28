# Keyboard-Format Knowledge (QWERTY)

## What this is

TNN-usable knowledge of the physical QWERTY keyboard layout, for inferring
what a user most likely meant from what they typed. This is **logic-derived
knowledge**: it encodes *where the keys are*, and typo likelihood is derived
from physical distance. It is not a memorized correction list — no
("teh" -> "the") pairs live here.

## Files

| File | Role |
|---|---|
| `qwerty.zag` | The knowledge itself: key-center coordinates + `kb_sub_cost(a,b)` accessor. Any deliberation can call it. |
| `typo_infer.zag` | Inference built on the knowledge: `infer_dist` (keyboard-weighted or blind edit distance) plus the deliberation-facing API doc. |
| `run_battery.zag` | Battery runner: reads items, scores all candidates with `infer_dist`, writes ranks. (Inference lives in `typo_infer.zag`; the runner is I/O + ranking.) |
| `words.txt` | The known-word list used for word plausibility (authored, alphabetical, frozen). |
| `gen_battery.py` | Deterministic battery generator (glue). Mirrors the geometry; verified byte-exact against `qwerty.zag` by self-test. |
| `PREREG_KEYBOARD_TYPO.md` | Frozen preregistration: scoring rule, battery design, metrics, kill bar. |
| `RESULTS_KEYBOARD_TYPO.md` | Verdict with measured numbers. |

## Geometry model (the assumption, stated plainly)

Standard US-ANSI QWERTY. Key centers in quarter-key units, rows staggered
as on real hardware (each row starts about half a key right of the row above):

- q-row: y=4,  x = 8  + 4i for `qwertyuiop`
- a-row: y=8,  x = 9  + 4i for `asdfghjkl`
- z-row: y=12, x = 11 + 4i for `zxcvbnm`

Substitution cost between two keys derives from squared Euclidean distance
(d2) of their centers:

| d2 | cost | meaning | example |
|---|---|---|---|
| 0 | 0 | same key | e->e |
| 1..17 | 10 | adjacent incl. diagonals | e->w, e->r, e->d, q->a |
| 18..45 | 20 | near / stagger-diagonal | e->s, q->s, w->a |
| 46..100 | 30 | two keys over | q->e, q->z |
| >100 | 40 | far key | q->p |
| non-letter | 40 | unknown | e->3 |

Costs are in tenths of a substitution unit so insertion/deletion (15) and
transposition (10) sit on the same scale.

## How a deliberation should use this

1. **Word-level:** score each candidate intended word with
   `infer_dist(typed, candidate, 1, scratch)` (see `typo_infer.zag`); the
   cheapest is the most likely intent. Word plausibility = membership in the
   known-word list.
2. **Character-level:** given one wrong keypress `c`, rank candidate letters
   by `kb_sub_cost(c, .)`. The ranking is a likelihood ordering, not a
   verdict — `c` itself always ranks first (maybe it wasn't a typo), then
   its physical neighbors.
3. **Context still rules:** geometry proposes, surrounding words dispose.
   A far-key substitution the sentence demands beats a near-key one it
   doesn't.

## Explicit non-assumptions

- **Shifted variants:** uppercase letters are the same physical keys (shift
  held). Lowercase before querying.
- **Digits/punctuation:** not encoded. Their geometry is future knowledge,
  not assumed.
- **Other layouts:** AZERTY, QWERTZ, Dvorak, mobile layouts are NOT covered.
  A layout is a separate knowledge file with the same accessor shape;
  the layout must be known before the costs mean anything.
- **No frequency priors:** word plausibility here is list membership only.
  Corpus-derived priors are a future addition, not smuggled in.

## Standards

Pure Zag for knowledge and inference. Zero RNG. Byte-identical reruns.
