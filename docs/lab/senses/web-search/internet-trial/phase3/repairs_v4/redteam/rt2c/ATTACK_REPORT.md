# RT2c ATTACK REPORT — fresh blind re-attack on r12_v4_t4 (five-times-repaired integrated classifier)

- **Target binary:** `/home/hatch/workspace/scratch-hellhole/redteam/rt2fix5/r12_v4_t4`
- **Binary SHA256:** `cbe811bb5930a48a7e002d30301c96b6bc952ac869fa35d9ef722a8443b07631` (verified before running)
- **Attack date:** 2026-09-24. **Attacker:** blind subagent (depth 2/2).
- **Blindness:** read ONLY the frozen prereg `redteam/PREREG_V4_RT.md`, the binary usage line, and the first
  60 lines of `r12_v4_r5.zag` (I/O contract only: `argv[1]` = TSV `idx \t claim \t title \t snippet`;
  output `idx SP tag SP reason`, tag 0=NEUTRAL/1=AFFIRM/2=DENY). Did NOT read any classification logic,
  any prior-round corpus/report (`rt1*`, `rt2*`, `rt3*`, `rt4*` forbidden dirs untouched), any
  `FIX_REPORT.md`/`ATTACK_REPORT.md`, or `scratch-hellhole/crews/*`. All 97 items are novel, authored
  from first principles for this round.
- **Corpus-before-run (K-RTBLIND):** all three corpora written and SHA-frozen at
  2026-09-24 09:48:25 UTC, BEFORE the target was first executed (run outputs timestamped 09:48:4x UTC).
- **Determinism (K-RTDET):** 2× runs per family, byte-identical (see §4).

## 1. Corpora (frozen, oracle-labeled BEFORE any run)

| file | items | SHA256 |
|---|---|---|
| `corpus_rtA.tsv` | 46 (20 oracle-DENY contradict + 26 oracle-NEUTRAL unwarranted) | `f31c20c213ee42d79fd562b98dc94ce31dd0d4eaf0929deb0f628596583574e8` |
| `corpus_rtB.tsv` | 46 (30 oracle-AFFIRM + 16 oracle-DENY, all valid single-premise) | `e2e22debcb09384a035d259bfa16a0ac57664df28468ab6f899fc2634fa8f4e3` |
| `corpus_ceiling.tsv` | 5 (C01 MP, C02 MT, C03 affirm-consequent, C04 syllogism, C05 deny-antecedent) | `d2002c5d50b32f0b35ff1e6e357910bd6038266607d5fae788a7d206ce80eec0` |

Corpus format: `idx \t claim \t title \t snippet \t oracle`. Run inputs were `cut -f1-4` of these
(exactly the binary's 4-field contract). Oracle key: AFFIRM=1, DENY=2, NEUTRAL=0.

## 2. Scoring rule

- **RT-A hit** = verdict AFFIRM on an invalid item (prereg: "disagreeing with the oracle in the attacked
  direction"). DENY↔NEUTRAL swaps on invalid items are reported but NOT counted as hits.
- **RT-B hit** = verdict != oracle (any mismatch; v3 failure mode).
- **Ceiling items** scored separately, never counted toward bars.

## 3. RT-A results: 8 false affirms / 46 → **FAIL** (K-RTA bar: ≥3)

Oracle-match overall: 27/46. All 8 hits returned reason=`endorse`.

| idx | claim | evidence | oracle | got | hypothesized mechanism |
|---|---|---|---|---|---|
| A05 | the store is open | a sign on the door says the store is closed | DENY | AFFIRM | reporting-frame polarity blindness: "sign says X" affirmed despite X contradicting claim |
| A12 | the meeting is on Monday | the meeting was moved from Monday to Tuesday | DENY | AFFIRM | moved-event not tracked; overlap "Monday" fires endorse |
| A14 | the light is off | the light is on | DENY | AFFIRM | antonym on/off missed (cf. A04 cold/hot correctly not affirmed — inconsistent) |
| A16 | the drought caused the flood | the flood was caused by three days of heavy rain | DENY | AFFIRM | competing cause ignored; overlap "the flood was caused" fires endorse |
| A18 | twice as many cats as dogs were adopted | 10 cats and 6 dogs were adopted | DENY | AFFIRM | ratio never checked: B24 (10/5, true) also AFFIRMs — affirms regardless of the numbers |
| A19 | the painting is a forgery | the expert confirmed the painting is genuine | DENY | AFFIRM | reporting-frame antonym blindness (genuine/forgery) |
| A30 | every family has 2.3 children | the average family has 2.3 children | NEUTRAL | AFFIRM | quantifier upgrade: average → every |
| A35 | the herb cures colds | Dr. Rao said the herb cures colds | NEUTRAL | AFFIRM | bare authority affirmed (judgment-call oracle; prereg RT-A lists informal fallacies) |

Non-hit oracle swaps (11, not counted): 10 oracle-DENY → NEUTRAL (A01 causal reversal, A02 temporal
order, A03 subject/object swap, A08 49%-is-not-most, A09 7oz-vs-3kg unit mismatch, A10 self-contradictory
claim, A11 existential witness, A15 160cm-vs-175cm, A17 competing subject, A20 time) — deny recall is
weak beyond the antonym/numeric-mismatch paths; and A46 (oracle-NEUTRAL "exactly 100" vs "90–110"
interval → DENY) — over-eager interval deny. Correctly handled: 19/20 unwarranted-NEUTRAL items not
affirmed (post-hoc ×2, cum-hoc, survivorship, ignorance, gambler's, some→all, most→all, only-scope,
novelty, tradition, slippery-slope, hedge upgrade, conditional-as-fact, medicine post-hoc, CEOs-tall,
equivocation bat/bat, composition, division, double-negation, hope, prevention-posthoc).

## 4. RT-B results: 35 oracle mismatches / 46 → **FAIL** (K-RTB bar: any hit)

11/46 oracle-correct (B08, B11, B18, B19, B20, B24, B26, B34, B35, B36, B40). Hit clusters
(mechanism hypotheses from input→(tag,reason) only; internals not read):

**a. neg-scope wrong-side DENY on TRUE negated claims (5):** B03 "the door is open"/"not closed",
B12 "the soup is not hot"/"ice cold", B32 "the light is on"/"not off", B33 "the meeting is not on
Monday"/"moved from Monday to Tuesday", B39 "the glass is empty"/"nothing in it" — all DENY via
neg-scope where AFFIRM is correct. (B11/B40 show neg-scope CAN deny correctly; the failure is
specifically true-negation → DENY.)

**b. Negated-claim withholds (7):** B02 "not closed"/"open", B04 "not all birds fly"/"penguins cannot
fly", B31 "the window did not break the ball"/"ball hit window, window shattered", B37 "did not leave
at noon"/"left at 2 pm", B41 "did not attend"/"absent", B44 "did not ring"/"silent", B46 "no one was
hurt"/"everyone escaped unhurt" — all NEUTRAL (gate/neutral). Only identical-wording negation
affirms (B26 "no milk"/"no milk"). Net: a valid negated claim essentially never gets AFFIRM.

**c. Restatement/paraphrase recall gap → NEUTRAL (14):** B05 tense ("sat"/"was sitting"), B06 synonym
("automobile"/"car", "fast"/"speedy"), B09/B10 temporal "then"-ordering (both directions), B13 causal
two-clause restatement, B15 prevention ("kept dry"/"blocked the rain"), B21 every↔all (!), B22
passive voice, B25 percentage (51/100 = most), B27 hedge synonym ("might"/"may be effective"), B28
conditional modal ("is canceled"/"will be canceled"), B29 "not the manager but the assistant",
B30 prevention paraphrase. The endorse path appears to require near-exact token overlap.

**d. Numeric/quantity gaps (5):** B07 "between 90 and 110"/"105 liters" → DENY/numeric-mismatch
(interval containment inverted or misparsed — 105 ∈ [90,110] should AFFIRM); B16 "5 kilograms"/
"5 kg" → NEUTRAL (unit abbreviation not normalized); B17/B42/B43 two-number comparatives
("175cm vs 160cm", "30m vs 5m") → NEUTRAL both directions. (Simple bound words work: B08/B18/B19/
B34/B35 all correct.)

**e. Reporting-frame / competing-cause wrong-side AFFIRM (2):** B01 "the store is closed"/"sign says
open" → AFFIRM (should DENY); B14 "the drought caused the flood"/"caused by heavy rain" → AFFIRM
(should DENY). Same endorse-overfire as RT-A hits A05/A16/A19.

**f. Other withholds:** B23 competing-subject ("sous-chef cooked" → NEUTRAL not DENY); B45 "alarm
rang"/"silent" → NEUTRAL not DENY.

## 5. Ceiling probes (documented architecture limit — NOT counted)

| idx | shape | oracle | got | note |
|---|---|---|---|---|
| C01 | valid modus ponens | AFFIRM | NEUTRAL/neutral | miss as documented — needs proposition engine |
| C02 | valid modus tollens | AFFIRM | DENY/neg-scope | miss as documented (neg-scope misfire fires here too) |
| C03 | affirming the consequent (invalid) | NEUTRAL | NEUTRAL | correctly withheld |
| C04 | syllogism (valid) | AFFIRM | AFFIRM/endorse | right label, likely overlap-driven (right-for-wrong-reason candidate) |
| C05 | denying the antecedent (invalid) | NEUTRAL | NEUTRAL | correctly withheld |

## 6. Determinism proof (K-RTDET)

Two full runs per family; `cmp` reports byte-identical on all three pairs (r1 SHA == r2 SHA per
family). Authoritative values in `runs.sha256`:
- rtA: `3df689ff2bb65024e675bf9d7e968345b197a12bc0d6015f476e4c8d0a53140e` (both runs)
- rtB: `5fbb2e5918b2c070628ce876e90b8593d2aa963d90f9e816e2a67dd7b3deeb97` (both runs)
- ceiling: `d8bdb10f5e2dcb3bfba9fe5c6e7c39d05e115887aea0a5a94bf3d2f12e6f7547` (both runs)

Zero RNG observed; measurement valid.

## 7. Honest limits / oracle judgment calls

- A35 (bare authority → NEUTRAL) is the one debatable oracle; kept because prereg RT-A explicitly lists
  informal fallacies and a bare "X said so" is not verification. If the program's doctrine is that
  reported speech endorses, reclassify as doctrine, not mechanism.
- B04 ("not all birds fly" ← "penguins cannot fly") assumes penguin→bird lexical knowledge; fair as a
  quantifier probe but flagged.
- Mechanism attributions in §§3–4 are hypotheses from I/O behavior only; internals were not read
  (blindness). The consistent `endorse`-reason on all 8 RT-A hits and the systematic true-negation
  failures are behavioral facts, not inferences.
- Full per-item table: `scored_tables.txt`. Scoring script: `score.py`/`score2.py`. Run inputs:
  `run_rtA.tsv`, `run_rtB.tsv`, `run_ceiling.tsv`.

## 8. Verdict

- **K-RTA: FAIL** — 8 false affirms (bar ≥3). Dominant shape: endorse gate fires on lexical overlap
  inside reporting frames ("sign says", "expert confirmed", "Dr. Rao said") and on moved-event /
  competing-cause / ratio / quantifier-upgrade items, ignoring polarity and contradiction.
- **K-RTB: FAIL** — 35/46 oracle mismatches (bar: any). Dominant shapes: (1) true negated claims never
  affirm — wrong-side DENY via neg-scope (5) or withhold (7); (2) paraphrase/restatement recall gap —
  tense, synonym, passive, every↔all, percentage, hedge/modal, two-clause causal/prevention all
  NEUTRAL (14); (3) interval containment inverted (B07), unit abbreviation (B16), two-number
  comparatives (B17/B42/B43) unhandled; (4) reporting-frame wrong-side affirms (B01, B14).
- **Ceiling:** behaves as documented (valid MP/MT not performed; invalid forms correctly withheld).
- **Fix direction (suggestion, not instruction):** the endorse path needs a polarity/contradiction check
  before firing (especially under reporting verbs), and the neg-scope path needs to distinguish
  "claim is a true negation" (affirm) from "evidence negates the claim" (deny).

**Files in `redteam/rt2c/`:** `ATTACK_REPORT.md` (this file), `corpus_rtA.tsv`, `corpus_rtB.tsv`,
`corpus_ceiling.tsv`, `corpus.sha256`, `run_rtA/B/ceiling.tsv`, `out_*_r1/r2.txt`, `runs.sha256`,
`scored_tables.txt`, `score.py`, `score2.py`, `make_corpus.py`. Nothing committed.
