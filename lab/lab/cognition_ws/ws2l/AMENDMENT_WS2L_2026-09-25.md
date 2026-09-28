# AMENDMENT WS2-L-2026-09-25 — dated amendment to PREREG WS2-L

Parent prereg: PREREG_WS2L.md, frozen at commit
0c1fda136f794bb76be9d9bb174dc4fc90516e04 on tnn-native-lab.
This amendment is issued BEFORE ARM L's first test run (ARM B validation
complete at commit 22629f816b3b59269e3e25cf3e6bb160be5852d1). It corrects
two prediction/wording defects found during ARM B validation. It changes
NO battery text, NO gold sets, NO kill bars, NO decision rule, and NO
mechanism constraints.

## A1. §6 predicted ARM B DIST score: 6/6 -> 5/6 (correction)

QD3 (`the canine watched the flock in darkness`, gold DOG1) and QAN1
(ADV-NEAR) are byte-identical queries. Both require the dog|canine bridge
to resolve. ARM B's frozen table contains none of dog|canine,
guarded|watched, sheep|flock, night|darkness (table-grep verified), so a
deterministic ARM B abstains on both (binary-confirmed). The frozen §6
simultaneously predicted DIST 6/6 (QD3 passing "via canine|dog") and
ADV-NEAR 4/6 (QAN1 missing) — jointly unsatisfiable for ARM B on identical
inputs. The DIST 6/6 prediction was simply wrong for the control arm.

Corrected ARM B baseline: OFFICIAL 51/51, FRESH 0/6, DIST **5/6**,
ADV-NEAR 4/6, MULTI-HOP 0/4, MORPH 0/4. ARM B primary S_B = 51+0+5+4 =
**60/69**. ARM L's DIST bar (K5) is unchanged at 6/6: L learns dog|canine
from evidence, so QD3 and QAN1 must both resolve for L.

## A2. Corpus scoping clarification (no text changes)

OFFICIAL-51 is defined on the v1.1 corpus ALONE (same corpus, queries,
golds as WS2-B2; this is how ARM B replicated 51/51). The section-3 new
batteries run on the COMBINED corpus (v1.1 + corpus_l.txt). Rationale:
on the combined corpus, frozen QP04 ("...neighbor...") ties BOR1/DS6 at
tot=1001 on the exact word "neighbor" and the ID-ascending tie-break
sends it to BOR1 instead of PP04 — a corpus-composition artifact, not a
learning outcome. ARM L runs OFFICIAL-51 on v1.1 alone and the new
batteries on the combined corpus, exactly as ARM B was validated.

## What is NOT changed

Batteries (text and golds), kill bars K1-K7, the decision rule (§7:
L passes all bars and S_L >= S_B -> ADOPT L, table deleted; tie -> L
wins; else bridge stays as stopgap), the learning-corpus specification
(§4), and the protocol order (§6) are all unchanged.
