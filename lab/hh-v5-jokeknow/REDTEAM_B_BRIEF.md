# RED-TEAM BRIEF B — sincere/deadpan corpus (blind, adversarial)

## Context
Hell-hole V5 tests whether the V4 joke classifier's "comprehension ceiling" is
knowledge, not architecture. We taught it joke knowledge (dual meanings,
idioms, world facts, sound-alikes) as deliberately-managed memory. You are
BLIND to the implementation — you never see the classifier or its rules.
You get the KNOWLEDGE STORES (what it learned). Your job is to BREAK it:
make it install JOKING on sincere text.

## Your job
Author **60 SINCERE items** (`corpora/rt5_sincere.tsv`, TSV: `id \t text \t trap-type \t SINCERE`).
The kill bar: **ZERO JOKING installs**. Every install is a kill.

## Trap families (use the stores' words/facts — that's the point)
- **T1 one-sense-only** (~15): use a dual-meaning word from `pun.tsv` with
  ONLY ONE sense evoked (e.g. "I lost interest in the lecture." — no finance).
- **T2 both-senses-no-turn** (~15): both senses' cues present but NO
  incongruity turn — flat sincere statements (e.g. "The bank raised interest
  rates. I lost interest in the news.").
- **T3 idiom-no-play** (~10): idiom from `idiom.tsv` used purely figuratively,
  no literal play (e.g. "She plays piano by ear.").
- **T4 fact-respected** (~10): entity from `world.tsv` with the fact HELD,
  not violated (e.g. "Pack a parachute for the skydive.").
- **T5 phon-no-alt** (~10): written word from `phon.tsv` with NO alternate-
  reading support (e.g. "I love seafood pasta.").

## Rules
- SINCERE means sincere: a human would not call these jokes. No winks, no
  setups, no punchlines.
- NATURAL: ordinary prose (statements, observations, instructions).
- Use the stores' BREADTH, not just the RT3e ceiling items.
- Tag each item's trap family in the context field (`T1`..`T5`).
- No duplicates, all sincere, 60 lines, 4 tab fields, unique IDs S01..S60.

## What you're testing
Whether knowledge installs JOKING from shape alone (a kill) or respects the
shape+turn discipline (withholds on sincere text). Be adversarial but fair:
the text must be genuinely sincere, not a joke in disguise.
