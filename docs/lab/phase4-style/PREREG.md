# Phase 4 follow-up: style attribution — frozen prereg (2026-09-27)

## 1. Mission

Phase 4 (commit `625606d6e942c95bc583b333057c1461f6075bbe`) proved TNN
differentiates interlocutors by identity, not name tag. Micah's new question:
people have different talking styles — with the name tag stripped, can TNN tell
WHO it is by style alone, by itself? And can we see, in its internal activity,
HOW it tells?

Three separable claims:

- **Claim A — attribution when asked:** given unidentified text in a known
  person's style, name the person.
- **Claim B — spontaneous attribution:** in a live unattributed stream, the
  system volunteers the speaker unprompted — or stays silent when unsure.
- **Claim C — mechanism:** the internal activity (per-person style ledger +
  per-decision deliberation trace) carries the attribution signal, proven by
  intervention: remove/perturb the signal and attribution degrades exactly
  where the trace said it would.

What this line does NOT claim: inferring personality traits, emotional state,
or authorship of long documents; multi-session style drift over weeks; any
person's "true" style beyond the observed sample.

## 2. Starting substrate

The phase-4 person substrate (identity-keyed partitions, `p4.zag`) is the
lineage. The style line is a NEW minimal Zag program (`build/sa.zag`): a
style-attribution interpreter reading probe scripts from argv[1]. Pure Zag,
zero randomness, deterministic by construction (open order everywhere, no
hash iteration, no RNG). Toolchain pinned:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## 3. Style model spec (frozen — the implementation must match this)

**Observation.** `say <pid> <text>` records one utterance for pid and updates
pid's style ledger: per-feature sums (i64) + utterance count. The profile is
the per-feature MEAN. No content words are stored except hedge-word hits
(counted, not stored); no n-gram tables; no topic keys.

**Features (12, integers, computed from raw bytes):**

| # | name | definition |
|---|---|---|
| 0 | words | word count (space-separated) |
| 1 | wlen | 100 × letters ÷ words (0 if no words) |
| 2 | up | 100 × uppercase letters ÷ letters (0 if no letters) |
| 3 | low1 | first alphabetic byte is lowercase (1/0) |
| 4 | bang | 100 × `!` ÷ chars |
| 5 | ques | 100 × `?` ÷ chars |
| 6 | stop | 100 × `.` ÷ chars |
| 7 | comma | 100 × `,` ÷ chars |
| 8 | hedge | 100 × hedge-word hits ÷ words; hedges = {maybe, perhaps, wonder, could, might, possible, seems}, whole-word, case-insensitive |
| 9 | caps3 | 100 × words-with-≥3-uppercase-letters ÷ words |
| 10 | frag | last non-space byte is not `.`/`!`/`?` (1/0) |
| 11 | digit | 100 × digits ÷ chars |

**Families (for lesion):** LEN={words,wlen}, CASE={up,low1}, PUNCT={bang,ques,
stop,comma}, LEX={hedge,caps3,digit}, STRUCT={frag}.

**Distance.** For probe feature vector x and person mean m:
`d = Σ_f W[f] × |x[f] − m[f]| ÷ S[f]`, integer division, with frozen scales
`S = {1,100,10,100, 5,5,5,5, 10,10,10, 100}` and family weights `W[f]=100`
for all f. `lesion <family>` sets that family's weights to 0 (`lesion none`
restores). Winner = min distance, open order breaks ties.

**Decision.** `rel = 100×(d2−d1) ÷ max(d2,1)` where d1,d2 are best/second-best
distances. `ask`: WITHHOLD if no open persons or rel < 15, else the winner.
`stream` (watch mode): VOLUNTEER winner iff rel ≥ 35, else silent. Rationale:
ask threshold low enough to attribute clear styles; volunteer threshold high
enough that unprompted claims are conservative.

**Brain-activity trace.** Every `ask`/`stream` emits BEFORE its R line (all
chained into the FNV transcript):

```
D feats w=.. wl=.. up=.. lo=.. b=.. q=.. s=.. c=.. h=.. c3=.. f=.. d=..
D dist p1=.. p2=.. ...
D winner p2 rel=.. thr=15
D gapfam LEX=.. PUNCT=.. CASE=..
```

`D dist` covers open persons in open order. `D gapfam` lists the top-3
families by share of the winner/runner-up distance gap
(`gap_f = famdist_f(runnerup) − famdist_f(winner)`, shares over the top 3,
integer percent). The **decisive family** = argmax gap share (ties → family
order LEN,CASE,PUNCT,LEX,STRUCT). This is the causal story the line tests.

**Ops** (one per line; `#` comments, blank lines skipped; text runs to
end-of-line):

| op | semantics |
|---|---|
| `open <pid>` / `name <pid> <name>` | person substrate (as phase 4) |
| `say <pid> <text>` | observe utterance; `R say <pid> ok n=<k>` |
| `ask <text>` | D trace, then `R ask = <pid>` or `R ask = WITHHOLD` |
| `watch on\|off` | `R watch on` / `R watch off` |
| `stream <text>` | watch must be on; D trace, then `R stream VOLUNTEER <pid>` or `R stream silent` |
| `lesion <family>\|none` | `R lesion <family> ok` |
| `profile <pid>` | `R profile <pid> = n=<k> f=<12 means>` (brain-state readout) |
| malformed / unknown pid | `R ERROR ...`, interpreter continues |

Ledger: every input line emits `L <seq> <rawline> => <short>`. Final line
`R chain <16 hex>` (FNV-1a-64 over every emitted line's bytes incl. newline,
offset basis 14695981039346656037; chain covers all L/D/R lines except
itself). The scorer recomputes the chain in Python.

## 4. Corpus (frozen structure; content sealed §7)

Four persons, genuinely distinct real dialogue styles (hand-authored, varied
topics — not toy sentences):

- **p1 "rush"**: terse lowercase bursts, fragments, 3–9 words, minimal
  punctuation (Micah-like chat bursts).
- **p2 "formal"**: complete sentences, proper caps/punctuation, 15–30 words,
  subordinate clauses.
- **p3 "wonder"**: question-heavy, hedged (maybe/perhaps/i wonder/could),
  medium length, reflective.
- **p4 "spark"**: exclamation-heavy, caps emphasis, slang, bursts.

Training: 12 utterances/person (48 total), topical flavor included (so the
content-decoy control is meaningful). All attribution probes use NOVEL topics
never seen in training.

**Asked battery (12 probes, 3/person, novel topics).** Expectation: correct pid.

**Watch stream (18 lines).** 12 known-clean (3/person, novel topics), 2 drift
(p2 hurried-terse; p3 assertive, no hedges), 2 unknown (p5 "log" style —
timestamped system-log lines, never observed in training), 2 mimic (p1
imitating p2's formality; p4 imitating p1's terseness).

**Lesion runs.** The 12 asked probes re-run under `lesion none` + one run per
family (LEN, CASE, PUNCT, LEX, STRUCT) + one all-lesioned run.

**Red team (6, asked mode, novel content).**
- RT1 mimic p1→p2 formal: WITHHOLD or p1; p2 = fail.
- RT2 mimic p4→p1 terse: WITHHOLD or p4; p1 = fail.
- RT3 drift p2 terse-formal: p2 or WITHHOLD; other pid = fail.
- RT4 drift p3 assertive: p3 or WITHHOLD; other pid = fail.
- RT5 content decoy (p1's topic "build cache" in p3's style): p3; p1 = fail
  (the lookup-table trap: style must beat topic).
- RT6 unknown p5: WITHHOLD; any pid = fail.

## 5. Kill bars (frozen)

- **K-A (asked):** ≥10/12 correct AND 0 wrong-person attributions. WITHHOLD
  counts as a miss, not a kill. → Claim A UPHELD/KILLED.
- **K-B (spontaneous):** on the 12 known-clean stream lines: ≥10 volunteered
  correctly. Drift: correct pid or silent (wrong pid = fail). Unknown: silent.
  Mimic: silent or true speaker (imitated pid = fail). 0 false volunteers
  overall (false = volunteer with wrong pid, or any volunteer on unknown).
  → Claim B UPHELD/KILLED.
- **K-C (mechanism):**
  - K-C1: all families lesioned → 0/12 attributed (all WITHHOLD). Proves the
    attribution depends on the style signal, not priors.
  - K-C2: let F* = family decisive for the most asked probes (ties → family
    order). On F*-decisive probes: acc(lesion F*) ≤ acc(none) − 25 points.
    On probes where F* is not in the top-2 gap families:
    |acc(lesion F*) − acc(none)| ≤ 10 points. Proves the trace's causal story.
  → Claim C UPHELD/KILLED (both sub-bars must hold).
- **K-D (determinism):** every script run 3× (2× plain + 1×
  MALLOC_PERTURB_=165); stdout sha256 identical across all three, else the
  results are INVALID (methods failure, fix and rerun).
- **K-E (red team):** per-probe expectations in §4; any confident wrong-person
  attribution (rel ≥ 15) on RT1–RT6 kills the corresponding claim (RT1/RT2 →
  A; RT5 → A; RT6 → A+B).

Verdict rule: each claim UPHELD iff its bars hold on the sealed battery (K-D
gates validity). Any failure → honest verdict naming the precise failing step.

## 6. Brain-activity analysis (required deliverable)

`BRAIN.md` must show, from the chained D traces (not from the corpus text):
per-person dominant families (which feature families separate each person,
from training profiles); per-probe decisive families; lesion deltas per
family; and the plain-English story of HOW the system tells people apart.
Nothing in BRAIN.md may be asserted without a trace line to point at.

## 7. Sealing

`sealed/gen.py` authors the corpus + all probe scripts deterministically
(hand-authored strings, fixed order) and writes `SHA256SUMS`. Content is
sealed at the prereg commit: the builder may not retune features, weights,
scales, or thresholds after seeing probe content. The red-team probes are
authored in the same sealed step (same-agent limitation disclosed, as in
phase 4: frozen bars + sealed content + fresh topics are the mitigation).

## 8. Honest envelope (preregistered)

- Styles are 4 fixed caricatures; real human style is wider and drifts.
- The volunteer threshold (35) is a frozen judgment call, not a measured
  optimum. If K-B fails on threshold conservatism, the verdict says so.
- Hedge-word counting is surface-lexical; the lesion of LEX measures exactly
  how much attribution leans on it (the n-gram-vs-structure question is
  answered by the lesion deltas, not by assertion).
- Builder and red-teamer are the same agent (depth limit), disclosed here
  with the mitigations in §7.
