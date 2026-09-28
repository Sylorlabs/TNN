# BRAIN.md — white-box mechanism analysis: HOW it tells by style

## 1. The structures that carry the signal

Three structures, all inspectable in the output:

1. **Per-person style ledgers** — one mean vector of 12 raw-byte features per
   person, learned from 12 training utterances each. The ledger IS the
   person's style identity; there is no other representation.
2. **The distance computation** — weighted Manhattan distance from a probe's
   feature vector to each ledger, with per-family weights (lesionable).
3. **The D trace** — four emitted lines per decision: extracted features,
   distances, winner+margin, top-3 gap families. The trace is computed from
   the same numbers that make the decision (no separate explanation path).

## 2. What each person sounds like (learned ledgers, n=12 each)

Feature order: words, avg word len×100, uppercase%, lowercase-open%,
`!`%, `?`%, `.`%, comma%, hedge-word%, CAPS3-word%, fragment%, digit%.

| Person | Style | words | wlen | up% | lo% | !% | ?% | .% | hedge% | caps3% | frag% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| p1 | terse lowercase fragments | 4 | 4.62 | 0 | 100 | 0 | 0 | 0 | 0 | 0 | 100 |
| p2 | formal complete prose | 13 | 5.66 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| p3 | questioning, hedged, reflective | 12 | 4.31 | 0 | 100 | 0 | 0 | 0 | 11 | 0 | 0 |
| p4 | excited, caps, exclamation-heavy | 8 | 4.56 | 17 | 0 | 7 | 0 | 0 | 0 | 14 | 0 |

p1 vs p3 is the subtle pair (both lowercase, similar length) — separated by
hedge words (11% vs 0%) and fragments (100% vs 0%). p2 vs p4 is the loud
pair — separated by caps/bangs vs clean prose.

## 3. Per-probe decisive families (asked battery, lesion_none traces)

| Probe | True | Winner | rel | Decisive family | 2nd | 3rd |
|---|---|---|---|---|---|---|
| merge the branch then tag it | p1 | p1 | 61 | CASE | LEN | STRUCT |
| ship it friday? lmk | p1 | p1 | 55 | CASE | LEX | LEN |
| cut the scope, keep it simple | p1 | p1 | 76 | LEN | CASE | LEX |
| The committee approved the revised schedule | p2 | p2 | 38 | LEX | LEN | CASE |
| We have completed the migration successfully | p2 | p2 | 48 | LEX | LEN | CASE |
| The documentation requires careful review | p2 | p2 | 51 | LEX | LEN | CASE |
| maybe we should reconsider? not sure though | p3 | p3 | 58 | LEN | LEX | CASE |
| i wonder if the latency is expected here | p3 | p3 | 46 | LEN | LEX | CASE |
| could be a config issue, hard to say | p3 | p3 | 42 | LEN | CASE | LEX |
| WOW the latency dropped to ZERO!! | p4 | p4 | 17 | CASE | LEN | LEX |
| FINALLY green across the board!! | p4 | p4 | 58 | LEN | CASE | LEX |
| MASSIVE win, the numbers look incredible!! | p4 | p4 | 45 | LEN | CASE | LEX |

Decisive counts: LEN 6, CASE 3, LEX 3, PUNCT 0, STRUCT 0.

## 4. Intervention results (the causal proof)

Each lesion zeroes one family's weights; the 12 asked probes re-run.

| Lesion | Accuracy | Mean rel-shrink on decisive probes | Mean rel-shrink elsewhere |
|---|---|---|---|
| none | 12/12 | — | — |
| LEN | 12/12 | 5.5 pts (6 probes) | −7.0 pts (margins grew) |
| CASE | 11/12 | 11.0 pts (3 probes) | 0.7 pts |
| PUNCT | 11/12 | n/a (0 decisive) | 1.0 pts |
| LEX | 11/12 | **26.0 pts** (3 probes) | 3.5 pts |
| STRUCT | 12/12 | n/a (0 decisive) | 0.0 pts |
| ALL | **0/12 (all WITHHOLD)** | — | — |

Causal reading, per AMENDMENT-02's differential bar (≥10 pts and ≥2× control):

- **LEX: VALIDATED.** The trace named LEX decisive for exactly the 3 p2
  probes; removing LEX collapsed their margins 38→15, 48→21, 51→23 — one more
  point and p2's probes withhold. The hedge/caps-word vocabulary family is
  genuinely load-bearing for the formal style's margin.
- **CASE: VALIDATED.** 11.0 vs 0.7 — the uppercase/lowercase habit family
  carries real causal weight where the trace said it did.
- **LEN: NOT VALIDATED.** "Decisive" for 6 probes by gap share, but removing
  it moved margins only 5.5 pts (and other probes' margins grew). Length is
  the largest slice of a redundant pie, not a causal lever. The trace's
  headline overstates it — documented, not hidden.
- **PUNCT/STRUCT: near-irrelevant** on these probes (never decisive;
  removal ≈ no-op). Punctuation habits ride along with length/case rather
  than deciding.
- **ALL: 12/12 WITHHOLD.** With the signal gone the system attributes
  nothing — no priors, no memorized answers, no default person.

## 5. Why the code is redundant (and why that's honest)

No single-family lesion flipped a single asked verdict (11–12/12 throughout).
The 12 features are correlated by construction: long utterances have more
periods AND more words AND more commas. The families back each other up.
Redundancy means the attribution is robust to losing any one habit family —
but it also means the D trace's "decisive family" is a largest-contributor
report, not a necessity claim. Both facts are in the ledger above.

## 6. Why spontaneous attribution is weaker (claim b's mechanism)

The volunteer threshold (35) vs the ask threshold (15) interacts with
per-person margin distributions:

- p1/p4 probes: margins 45–86 — always volunteered, always right.
- p3 probes: margins 42–74 — usually volunteered, always right when they were.
- p2 probes: margins 0–16 — the formal style sits NEAREST the decision
  boundary (its features are the least extreme), so 3 of 4 clean p2 lines
  stayed silent. Threshold conservatism, exactly the failure mode the prereg
  named in §8.
- Unknown log style ("15:31:02 INFO build ok 44 files 0 errors"): digits +
  caps-words (INFO) put it nearer p4's ledger (dist 572) than any other
  (p3 1188, p1 1108, p2 1302), margin 48 ≥ 35 → volunteered p4. Twice. The
  volunteer rule has no "none of the above is close in absolute terms" check —
  margins are relative, so an unknown that falls inside a known person's
  neighborhood gets claimed. That is the mechanism of the 2 false volunteers.

## 7. What the brain activity does NOT contain

- No name tags, no speaker IDs anywhere in the pipeline (verified: scripts
  carry `p1..p4` only in training/expectation files, never in probe text).
- No content-word lookup: the RT5 trap planted p1's topic keywords in p3's
  style — the system answered p3 at rel 74. Style features beat topic words.
- No confidence beyond the margin: rel is a pure distance ratio, and the
  two thresholds (15/35) are the entire decision policy.
