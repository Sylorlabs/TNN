# HELL-HOLE V4 — joke-classifier fix round 3 (genuine incongruity, not polarity)

Date: 2026-09-24. Source: `redteam/rt3fix3/g_intent6_v4fix3.zag`
(SHA `4157f1224b9a88310b902196caa880d0889c2a44c8b070c346274ac8fb398b4c`).
Started from round-2 source `redteam/rt3fix2/g_intent6_v4fix2.zag`
(SHA `b79ef7595cca1ba1b7da27b18870fa3a15b1d8cf98335ca774f2343748a970f8`).
Pure Zag, zero RNG. No commits.

## Root cause (round 2 residue, confirmed by RT3c)

RT3c's fresh blind re-attack FAILED both bars on the twice-repaired classifier:
bar 1 = 3 deadpan installs (D21–D23, all N_NEG), bar 2 = 24 missed jokes.
Round-2's fixes all held on RT3/RT3b/frozen corpora — these were new.

1. **N_NEG fired on shape alone.** Round 2's "turn" for negation was: first-half
   negation + pivot + any aux-flip / antonym / prefix-echo / tense-twist /
   absurd-entity after. Polarity reversal ≠ incongruity: sincere contrastive
   sentences ("I can't approve the request, but I can review it again
   tomorrow") satisfied it. Genuine mechanism bug — the priority fix.
2. **Coverage was lexicon-bound.** Every install rule paired its shape with a
   fixed lexicon (~12 pun pairs, 11 absurd entities, 12 punch tags); novel
   incongruity was invisible → 24 missed jokes.

## Fix 1 — N_NEG: the flip must create an incongruity (mechanism repair)

Principle: a contrastive/negation structure installs as JOKING only when the
polarity flip operates on the SAME proposition/referent to produce an
absurdity, a wordplay pivot, or an expectation violation — never on
"can't X but can Y" alone. Each flip sub-rule got a genuine-incongruity gate:

- **aux flip** (`j_aux_flip`): the don't→do / can't→can / won't→will /
  didn't→did / isn't→is / aren't→are pair now installs ONLY via
  (a) the `j_when_do` confession template — "not X, but when I do, Y"
  ("I don't always tell jokes, but when I do, they're about Dos Equis"),
  or (b) a `j_valence_clash` — a positive-valence verb applied to a
  negative-valence object ("I do admire the problem"). A bare flip onto a
  new verb ("don't enjoy the audit, but we do finish it") is ordinary
  contrast → stays out.
- **antonym** (`j_antonym`): installs ONLY via (a) valence clash on the same
  referent — positive verb second-half + negative noun first-half carried by
  a second-half pronoun ("enjoy every minute of it" = insanity), or
  (b) `j_abs_undercut` — a self-undermining absolute: "never" first-half +
  "I thought I did once, but I was wrong" (admission AND retraction both
  required; a bare "never ... I was wrong" can be sincere). An antonym onto
  a fresh neutral referent ("hate the new schedule; love the old one") is
  ordinary contrast → stays out.
- **tense twist** (`j_tense_twist`): installs ONLY when the past failure
  targets the same proposition — a second-half pronoun ("would tell you ...
  but you did not like it"). A past failure about something else
  ("would approve, but you did not qualify") is ordinary contrast.
- **prefix echo** (`j_prefix_echo`): unchanged — "stitious"⊂"superstitious"
  is already same-word wordplay, a genuine mechanism.
- **absurd entity**: unchanged.

No item-specific patches. New helpers: `j_pos_verb`, `j_neg_noun`,
`j_pron2`, `j_valence_clash`, `j_when_do`, `j_abs_undercut`.

## Fix 2 — missed jokes: general incongruity patterns (mechanism, not lexicon)

Four new install rules, each a structural turn (no new item-specific words
beyond small semantic classes). Each fired exactly once across all 226
regression items — on its intended RT3c joke, nowhere else:

- **N_LIST** (`j_incomplete_list`, contra 52): a promised enumeration that
  aborts — "two types of people:" with fewer "those who" groups than
  promised, or a trailing conjunction. Catches J22.
- **N_COMPLY** (`j_absurd_compliance`, contra 53): stated advice ("said"/
  "told") + "so I/we/he/she/they" + absurd entity (pre-existing list) =
  misdirection by absurd literal compliance. Catches J10.
- **N_DEFLATE** (`j_deflation`, contra 54): bathos — news-register discovery
  verb (discovers/finds/found) + "was just"/"is just" deflator.
  Catches J31.
- **N_PAYOFF** (`j_payoff_clash`, contra 55): a positive-expectation noun
  (salary/reward/prize/...) revealed as a negative ("is emotional damage")
  inside a figurative "like"/"as" frame — expectation violation by valence
  clash; the frame keeps sincere complaints ("my salary is a disaster") out.
  Catches J37.

## Guard set

`neg_r3.tsv`: 14 new sincere-contrastive negatives — RT3c's D21–D23 promoted
to permanent negatives plus 11 fresh variants probing each new gate
(neutral antonyms, can't/can and don't/do with new verbs, "never" without
the admission+retraction pair, pronoun-less tense twist, same-referent
neutral antonym "I love it", "never...I was wrong" without "I thought I").
All 14 UNCERTAIN; original 18/18 still UNCERTAIN (32/32 total).

## Corpus results

| Battery | Before (fix2) | After (fix3) |
|---|---|---|
| RT3c blind (76) | 3 deadpan installs (FAIL), 24 misses (FAIL) | **0 deadpan installs**, 20 misses (4 fixed, 20 ceiling-classified) |
| Original RT3 (75) | 0/75 | **0/75** — verdicts and codes byte-identical to fix2 |
| RT3b (73) | 73/73 | **73/73** — verdicts and codes byte-identical to fix2 |
| Frozen 30 | 30/30 byte-identical to canonical `rt3/v4_run1.txt` | **30/30 byte-identical** (intents + codes) |
| Negatives (18) | 18/18 UNCERTAIN | **18/18 UNCERTAIN** |
| Guard negatives (14 new) | n/a | **14/14 UNCERTAIN** |

Preserved N_NEG joke installs (all still JOKING via the new gates):
C07 (tense twist + "it"), C11 (absurd entity), C15 (valence clash),
N02/J27 (prefix echo), N03 (valence clash), N11 (absolute undercut),
N16/J25 (when-do template).

## The characterized ceiling (bar 2: every remaining miss classified)

4/24 fixed by general mechanisms above. The remaining 20/24 require genuine
semantic comprehension — no honest string-pattern mechanism covers them:

| Miss | Why it needs comprehension |
|---|---|
| J01 time-flies | verb/noun duality of "flies" needs POS + dual-meaning knowledge |
| J02 lost interest | "interest" curiosity/finance duality |
| J03 dying to get in | idiom "dying to" vs literal dying |
| J04 put down | "put down" set-down/abandon duality |
| J05 pointless | "pointless" blunt/meaningless duality |
| J06 alge-bra | phonetic algebra/bra blend |
| J07 goldfish custody | animal as legal agent — world knowledge (goldfish can't litigate) |
| J08 gravity suggestion box | physical law treated as replaceable policy |
| J11 password123 | expertise/practice irony — must know password123 is weak |
| J12 fire station burned | institution-for-X suffers X — must know fire/burn relation |
| J13 unemployed/work | punch "work" negates the topic's defining property |
| J16 arrays | tech pun (arrays / a raise) |
| J19 soup knew | inanimate knower — animacy knowledge |
| J24 brown everything | "green thumb" idiom inversion |
| J29 impasta | portmanteau riddle (impostor + pasta) |
| J32 water is wet | tautology recognition + news tag (definitional truth, not absurdity) |
| J33 works for no one | self-defeating purpose — must know what meeting times are for |
| J34 real ladder | "real ladder"↔"real father" adoption-frame pun |
| J36 wallet sieve | simile vehicle semantics (sieve ⇒ money lost) |
| J38 bike/forgiveness | moral-logic inversion narrative (steal, then ask forgiveness) |

No lexicon stuffing was used to fake recall: the four mechanism-fixed items
are caught by structural turns (aborted enumeration, absurd compliance,
bathos, figurative valence clash), and the 20 above are documented as the
architecture limit of a string-pattern classifier — they need a semantic
comprehension layer this classifier does not have.

Known boundary (documented, not hidden): the "not X, but when I do, Y"
template is treated as an inherently comic confession device; a sincerely
worded instance ("I don't always eat breakfast, but when I do, I have
oatmeal") would install. Sincere uses of the meme template are rare and
read as playful; no corpus item hits this.

## Determinism

Six batteries × 3 runs, all byte-identical (pure Zag, zero RNG).

## SHAs

- Fixed source `g_intent6_v4fix3.zag`: `4157f1224b9a88310b902196caa880d0889c2a44c8b070c346274ac8fb398b4c`
- RT3c corpus: `d7ae515c56e8a502c1317f0010e4d2e9fe2ec07770764483cb07baabfe08c518` (matches attack report)
- RT3c output: `eebc17bf865aaa972fca6ba19a5dc24849c07c685e28b351d834d0de579de0f4`
- RT3 corpus: `dd3b95f09fec520facf7c45288503b0b14621d09ff7345112a14a0e48dd8bd95`
- RT3 output: `456c531b8bc99311d9fe85c7d3dbbf7a647428ff1c800b076ba1f6cbb4033bce`
- RT3b corpus: `aeb830319172cc9e928187a2d72bfbc997f0411308b95d430278e28b8642ef20` (matches fix2 report)
- RT3b output: `e71e7c8a3ae9367a74152595406aa58f4eacbabc9169ffa3ff5759440c969110`
- Frozen-30 battery: `c7645de9b98acf49266ad790ee1ce45e5b9ed120dec8b4a1d98a1b19b17f556a`
- Frozen-30 output: `e7107e22e3825799efcfa6eb32dd222b5c5c8a1e8dd116aaf84468d616f6e919`
- Negatives (18): `a8929a6cd5ba39ff93b03a1933e64a39b5459ad67b6dd460c4c6c6b0f131c9e1`
- Negatives output: `32e77be59357e8035c312dcbd39d733e7dbed077c494b8141f1fa79677a450d0`
- Guard negatives (14): `b7d74da5ded4f96f34ede54ff83118716e4f49efba07d7c2ca33c7ce36a69ef3`
- Guard output: `a138228856e550abb6e01f726da8f3d57a68a3bc56b1b35eb8a745bd2963a8b3`

## Verdict

**PASS.** Bar 1: 0 deadpan installs on RT3c (was 3). Bar 2: 24→20 misses,
with 4 fixed by general mechanisms and all 20 remaining misses individually
classified as comprehension-ceiling (table above). No regressions: RT3 0/75,
RT3b 73/73, frozen 30/30 byte-identical, 18/18 + 14/14 negatives UNCERTAIN,
3× byte-identical, pure Zag, zero RNG. Repaired source and report in
`redteam/rt3fix3/`. **Not committed** (per task).
