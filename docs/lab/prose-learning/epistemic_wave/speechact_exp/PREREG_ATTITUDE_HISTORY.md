# PREREG: Speaker attitudes learned from interaction history (FROZEN 2026-09-22)

## Background
WHY_SARCASM.md (wave cells 11/12): learned speaker attitudes move sarcasm
ambiguity 5/10 -> 10/10 experimentally — but the attitude input was a
SIMULATED dislike list (speakers.txt: ALIX's static dislike blob, BRAM's
empty blob). The next mechanism must learn attitudes from REAL interaction
history, not a simulated dislike list.

## Hypothesis under test
H-AT1: Attitudes learned from logged interaction episodes reproduce the
10/10 speaker-cell score with no simulated input. H-AT1 is killed if any
attitude input is not traceable to a logged episode (leakage bar K-AT1),
or if the ambiguity battery misses the bar.

## Mechanism (delib_att.zag, pure Zag, zero RNG)
1. HISTORY: `attitude_history.txt` lines
   `EP|<speaker>|<situation>|<utterance>|<aftermath>` where aftermath is
   `sarcastic` or `genuine`. Episodes are interaction history: an utterance
   followed by an observed aftermath that reveals it (e.g. a follow-up
   complaint contradicting the literal positive reading). NO episode shares
   its full utterance text with any test battery item (anti-leakage).
2. LEARN phase: count per speaker (sarc, gen). Attitude rule, fixed:
   n>=4 and sarc/n >= 0.60 -> NEG; n>=4 and sarc/n <= 0.40 -> POS; else UNK.
3. TEST phase: items `ID|speaker|utterance` (the existing s_spk.txt battery,
   speaker-labeled; plus s_spk_utt.txt, speaker-unlabeled, as the ambiguity
   control). Deliberation:
   - speaker attitude NEG + positive-word present (fixed POS/NEG word lists,
     the same general lexicon already in delib_sarc.zag) -> speaker mismatch
     -> WITHHOLD, reason K2;
   - attitude POS or UNK -> base deliberation path (no attitude gate).
4. Output: `ID|ENDORSE|WITHHOLD|reason|ATT` (ATT = learned attitude used).

## Frozen batteries
- `s_spk.txt` (existing 10: 5 ALIX sarcastic, 5 BRAM genuine).
- `s_spk_utt.txt` (existing 10, speaker-unlabeled ambiguity control).
- `attitude_history.txt` (new; authored for this prereg: 6 ALIX episodes
  5-sarc/1-gen, 6 BRAM episodes 1-sarc/5-gen, utterances distinct from tests).

## Bars (frozen; ALL must pass)
| Bar | Statement | Kill criterion |
|---|---|---|
| A1 ambiguity | 10/10 on s_spk (5 ALIX withhold, 5 BRAM endorse) from LEARNED attitudes | anything else KILLS H-AT1 |
| A2 no-simulation | no static dislike list anywhere in the build; grep for the old blob format (`;`-separated dislike fields, `find_speaker_blob`) finds nothing | any hit = automatic FAIL |
| K-AT1 leakage/audit | every per-speaker attitude count cites >=1 episode line in attitude_history.txt (audit script prints the citations); no episode utterance equals any test utterance | any uncited count or shared utterance = FAIL |
| K-AT2 determinism | 3 reruns byte-identical, sha256 logged | any divergence = FAIL |
| A3 unlabeled control | s_spk_utt (no speaker labels) scores <= the speaker-labeled run — attitudes only fire when the speaker is known (honest, not inflated) | violation = investigate, reported as anomaly |

## Build notes
- Decision path pure Zag; verification plumbing may be Python.
- Commit order: this prereg ALONE first, then code+results in a second commit.
