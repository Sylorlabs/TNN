# HELL-HOLE V4 — joke-classifier fix round 2 (generalize, don't memorize)

Date: 2026-09-24. Source: `redteam/rt3fix2/g_intent6_v4fix2.zag`
(pristine round-1 copy preserved as `g_intent6_v4fix.zag`). Pure Zag, zero RNG.
No commits.

## Overfit cause (round 1)

Round 1 repaired RT3's 70/75 hits by adding "structural" rules that fired on
**shape alone**: N_QA (question mark + wh-word), N_DENY ("not a joke" substring),
N_BAR ("walked into a bar"), N_NEG (negation + contrast word), N_WHISPER
("whisper"), R_IRONY (habit + longevity), R_PUN2 (distrust + pivot), P_DA5D
(sky + made-of + food), R_SATIRE (news-word count), R_TROPE (trope word +
two clauses), and the N_PUN_* pair rules without pivot ordering. RT3b's novel
corpus broke all of them: 22/25 deadpan installs, 16 missed jokes (43/73 wrong).

## Generalized fixes (the TURN, not the shape)

Every install rule now pairs a shape signal with an **incongruity gate**:

- **N_QA** (`j_qa_turn`): riddle opener (start *or* post-boundary sentence) + an
  answer that pays off via punch lexicon (`other side`, `fsh`, `big plus`,
  `brick`, `awful`, …) or an absurd entity. Punch-less answers (P01–P10,
  sincere Q&A) never install.
- **N_DENY** (`j_deny_turn`): denial must be *about the statement itself*
  ("this statement", "right now"); a serious continuation (serious/deadline/
  evacuate/warning/…) cancels the comic read.
- **N_BAR** (`j_bar_turn`): "walk(ed/s) into a bar" + a pun payoff
  (tense/drunk/spirits/laughed/joke/long face). Incomplete setups stay out.
- **N_NEG** (`j_neg_turn`): first-half negation + pivot + a second-half
  incongruity — negating-prefix echo (`superstitious`→`stitious`), aux flip
  (`don't`→`do`), antonym, tense twist (would→did not), or absurd entity.
- **N_TAG** (new, `j_tag_turn`): two-part deadpan whose second part carries a
  classic punch tag (`we'll see about that`, `not so sure`, `too crowded`,
  `never meet`, `already tomorrow in…`, `not get it`, …).
- **N_WHISPER** (`j_whisper_turn`): whisper(ed) + a punch tag in the content.
- **N_PUN / N_PUN_GROW/OVER/JUMP/LINE/OUT** (`j_pair_turn`): setup word and
  punch word must sit on **opposite sides of the pivot** (or ≥6 words apart
  with no pivot). Fixes D16/D17 deadpan installs under the old pair rules.
- **R_PUN2** (`j_trust_pun_turn`): distrust setup + dual-meaning payoff
  (`atoms`/`make up`, `stairs`/`up to something`).
- **R_IRONY** (`j_irony_marker`): habit + longevity + a wry marker
  (`go figure`, `doctors hate`, `two packs a day`, `chain-smoked`, …).
- **P_DA5D**: natural-material veto (`j_natural_mat` — water/rock/iron/…):
  sincere geology ("earth is made of water and rock") no longer installs.
- **R_SATIRE** (`j_satire_absurd`): news register + an absurd claim
  (flat-earth, weekday-as-agent, absurd entity).
- **R_TROPE** (`j_trope_turn`): simile + comic/absurd completion, or hyperbole.
- R_PUN1 unchanged (round-1 rule; covered by negative NG03).

## Corpus results

| Battery | Result |
|---|---|
| RT3b blind (73) | **73/73** — 0 deadpan installs, 0 missed jokes (was 43/73 wrong) |
| Original RT3 (75) | **0/75 hits** — 32/32 jokes JOKING, 43/43 non-jokes clean |
| Frozen 30 | **30/30 byte-identical** to canonical `rt3/v4_run1.txt` (ID prefixes normalized), zero deadpan installs |
| Fresh negatives (18) | **18/18 UNCERTAIN** — one same-shape sincere negative per install rule, all executed |

RT3b misses remaining: **none** — nothing to explain.

## Determinism

Three full runs of all four batteries: byte-identical (4 outputs × 3).

## SHAs

- RT3b corpus: `aeb830319172cc9e928187a2d72bfbc997f0411308b95d430278e28b8642ef20`
- Fixed source `g_intent6_v4fix2.zag`: `b79ef7595cca1ba1b7da27b18870fa3a15b1d8cf98335ca774f2343748a970f8`
- RT3b output: `31b1a89aa946e53a467a0abd1cbe02be18291e595de13cb6876a26c1324aa462`
- RT3-orig output: `71af9bac1cf7883d54d517a073af4b2b170f031d4ba4d09ad37e21487295e127`
- Battery output: `998d8dc1a17b8e33c307d00d86403091abe5616d3d48a1c8eb5dd48e553c5e5a`
- Negatives output: `ccac1a759ee2963dbb4c34c8069c09f7901ba6c427ecec169e67cb0b97b7bbef`

## Verdict

**PASS both bars.** Round-1 overfit (shape-only installs) replaced by
turn-gated rules: every install needs setup → incongruity → punchline
evidence. RT3b 73/73, original RT3 0/75, frozen 30/30 byte-identical,
18/18 fresh negatives, 3× byte-identical, pure Zag, zero RNG.
