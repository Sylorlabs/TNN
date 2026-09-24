# RT3b ATTACK REPORT — fresh blind re-attack on the repaired joke classifier

**Target:** `redteam/rt3fix/g_intent6_v4fix.zag` (repaired joke classifier)
**Date:** 2026-09-24 (PDT) | **Prereg:** `redteam/PREREG_V4_RT.md` (followed exactly)
**Blindness:** read ONLY the target source, its Zag imports (needed to build the runner),
the prereg, and my own fresh corpus. Did NOT read rt1/rt2/rt3/rt4, any *fix dir,
FIX_REPORT.md / ATTACK_REPORT.md of any prior round, or builders' `crews/*`.
Corpus is 100% novel (written from the target's mechanics, not from any prior corpus).

## Corpus freeze (BEFORE build — K-RTBLIND satisfied)

- File: `redteam/rt3b/rt3b_corpus.tsv`
- SHA256: `aeb830319172cc9e928187a2d72bfbc997f0411308b95d430278e28b8642ef20`
- mtime: 2026-09-24 08:46:19 UTC (build of runner started after this)
- 73 items: D deadpan-factual ×25, H hostile/non-funny ×12, N negation/contrastive
  joke ×16, A anti-joke ×10, P punchline-removed setup fragment ×10
- Format: `id \t claim \t evidence \t oracle`; oracle ∈ {JOKE, NONJOKE}, pre-committed.
- Hit definition: oracle JOKE + target UNCERTAIN (miss), or oracle NONJOKE +
  target JOKING/SATIRE (install).

## Method

- Runner `rt3b_run.zag`: pure Zag, zero RNG, no timestamps, no ledger. Reads the TSV,
  calls `g_classify(text,url,codes,markers)`, prints `RT3B|id|oracle|target|hit|codes`
  + per-family summary. Target source copied verbatim (with its 4 Zag imports) into
  `rt3b/`; no other builder files touched.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Determinism: two runs, byte-identical output.

## Determinism (K-RTDET)

- `run1.txt` SHA256: `d006deba2b120b62798e5fd1071abbc49e854e25c01a61c7a76ffd3268ea6f42`
- `run2.txt` SHA256: `d006deba2b120b62798e5fd1071abbc49e854e25c01a61c7a76ffd3268ea6f42`
- `diff` → identical. Measurement valid.

## Results per family

| Family | n | Hits | Notes |
|---|---|---|---|
| D deadpan factual (oracle NONJOKE) | 25 | **22 installs** | every structural rule installable by plain sincere prose |
| H hostile / non-funny (oracle NONJOKE) | 12 | **2 installs** | insult veto holds elsewhere |
| N negation/contrastive joke (oracle JOKE) | 16 | **13 misses** | N_NEG misses every joke without (two-clause+reframe) or but-negation |
| A anti-joke (oracle JOKE) | 10 | **3 misses** | non-"why/what/how-many" openers invisible |
| P punchline-removed (oracle NONJOKE) | 10 | **3 installs** | N_BAR has no punchline-completeness gate |

**Total: 43/73 misclassified.**

## Hit list (every hit with mechanism)

### Deadpan installs (22) — each ANY ONE is a K-RTC kill

- D01 R_IRONY — "My grandfather smoked a pack a day and lived to ninety." Habit+longevity
  anecdote fires with NO justify gate; sincere biography installs.
- D02 R_SATIRE — "A new study finds that local residents support the plan." News-word
  count (study/finds/local/resident) ≥2 → SATIRE on a plain factual sentence.
- D03 R_TROPE — "The upgrade was free. The traveler downloaded it." Trope word + ". " shape.
- D04 N_QA — "Why do vaccines work? They train the immune system to fight disease."
  Factual Q&A matches the riddle shape exactly.
- D05 N_QA — "How many states are in the US? Fifty."
- D06 N_QA — "What is photosynthesis? It is how plants convert sunlight into food."
- D07 N_DENY — "I am not joking. This is a serious matter." Sincere denial installs.
- D08 N_DENY+R_TROPE — "This is not a joke. Please evacuate the building."
- D09 N_NEG — "I never agreed to this. But now it is done." Ordinary serious complaint.
- D10 N_NEG — "She did not sign the contract. Yet it remains binding."
- D11 N_NEG (but-neg) — "I love chocolate but I cannot eat it." Single-clause dietary fact.
- D12 N_BAR — "The inspector walked into a bar and ordered a drink. He found three
  violations." News report with bar phrase installs.
- D13 N_WHISPER — "'The baby is asleep,' she whispered. Then she closed the door."
  Plain narrative installs.
- D14 R_PUN2 — "Do not trust the contractor. They make up everything." Sincere accusation
  installs; no justify gate, no atom/context requirement.
- D15 P_DA5D — "The earth is made of water and rock." Sky+made-of+food-stem fires with
  NO justify gate (unlike P_DA5A–C); "water" is a food stem in a true statement.
- D16 N_PUN_JUMP — "The coach warned the team not to jump to conclusions after the
  hurdles were moved." Sincere sports sentence installs.
- D17 N_PUN_OVER — "After the war they had to get over it; their fear of the wall
  was gone." Sincere post-conflict sentence installs.
- D18 R_SATIRE — "Experts weigh in as the local press reports the story." (5 news words)
- D19 N_NEG — "We cannot afford rent. But we always manage."
- D21 R_IRONY — "Churchill drank alcohol daily and lived to ninety." True biography installs.
- D22 R_SATIRE — "The committee confirms the report is pending review." (3 news words)
- D25 N_DENY — "I am not joking about the deadline. It is tomorrow."

Non-hits (correct): D20, D23, D24 → UNCERTAIN.

### Hostile installs (2)

- H01 N_NEG (but-neg) — "You are an idiot but you never listen." Hostile non-funny installs.
- H10 N_NEG — "Why don't you just disappear, you idiot?" Hostile rhetorical question installs.
- Non-hits (correct): H02–H09, H11, H12 → UNCERTAIN (insult veto + no-shape holds).

### Missed negation/contrastive jokes (13)

N01 "Why don't scientists trust atoms? Because they make up everything." — the canonical
negation joke: "why don't" misses the "why do" opener, "don't scientists trust" misses
"don't trust", single negation + "?" + no reframe-word ("because" not in list) → UNCERTAIN.
N02 "I'm not superstitious, but I am a little stitious." — single clause, negation before
"but" → UNCERTAIN. N03 "I don't have a solution, but I do admire the problem." — same.
N04 "Nobody goes there anymore; it's too crowded." — ";" two-clause, single negation,
"too" not a reframe word → UNCERTAIN. N05 "Parallel lines have so much in common. Shame
they'll never meet." N06 "Don't worry about the world ending today; it's already
tomorrow in Australia." N07 "I told my wife she was drawing her eyebrows too high. She
looked surprised." N10 "My therapist says I have a preoccupation with vengeance. We'll
see about that." N12 "A clear conscience is usually the sign of a bad memory."
N13 "The early bird gets the worm, but the second mouse gets the cheese." (contrastive,
no negation at all → invisible) N14 "I told my doctor I broke my arm in two places. He
told me to stop going to those places." N15 "There are two types of people: those who
can extrapolate from incomplete data." N16 "I don't always test my code, but when I do,
I do it in production."
Correctly caught controls: N08, N09, N11 (two-clause + reframe present).

### Missed anti-jokes (3)

A05 "There are 10 kinds of people: those who understand binary and those who don't."
A07 "What's red and bad for your teeth? A brick." ("what's" misses the "what is" opener)
A10 "My dog has no nose. How does he smell? Awful." ("how does" misses "how many")
Correctly caught controls: A01, A02, A03, A04, A06, A08, A09.

### Punchline-removed installs (3)

- P02 N_BAR — "A man walked into a bar. He sat down." Setup fragment installs; N_BAR
  has NO punchline-completeness check (unlike R_PUN2's pivot-at-clause-end).
- P06 N_BAR — "A priest, a rabbi, and a minister walked into a bar. They ordered drinks."
- P07 N_NEG — "I never trusted the new policy. But the memo says it is final." Serious
  policy sentence installs.
- Correctly withheld controls: P01, P03, P04, P05, P08, P09, P10 → UNCERTAIN.

## Structural weaknesses found (root causes, not item lists)

1. **No justify gate on R_IRONY, R_PUN2, P_DA5D, N_QA, N_DENY, N_BAR, N_NEG, N_WHISPER,
   N_PUN_*.** The repair added `j_justify` only to P_DA1*–P_DA5C; every new structural
   rule fires on shape alone, so ordinary sincere prose (biographies, Q&A, complaints,
   narratives, accusations, policy memos) installs.
2. **R_SATIRE is a bare word-count** (ns≥2 news words → SATIRE). Any factual news-style
   sentence installs. R_TROPE is one trope word + any ". " → JOKING.
3. **N_NEG's shape is ubiquitous in serious prose**: one negation + two clauses +
   any of {but, now, yet, still, always...} — or just "but"+negation in one clause.
4. **N_QA's opener inventory misses "why don't", "what's", "how does"** — the most
   common real riddle phrasings — while catching factual Q&A verbatim.
5. **N_BAR lacks punchline completeness**; the bar opener alone is enough.

## Verdict

**FAIL** — both K-RTC bars tripped:
- ≥1 deadpan install: **22** deadpan installs (bar: any = FAIL).
- ≥3 missed jokes: **16** missed jokes (13 negation/contrastive + 3 anti-joke).

## Honest limits

- Oracles are my pre-commitments; borderline cases (D15 "earth is made of water and
  rock" as a simplification; D14 as sincere complaint) are defensible but arguable.
  Removing the two most arguable deadpan items still leaves 20 installs.
- Runner is my own code, not the builders' harness; verdict codes (JOKING/SATIRE/
  UNCERTAIN) map directly from `g_classify`'s return via `r5_dispose`, no ledger layer.
- Coverage is shape-driven from reading the target (allowed); items are novel, none
  from any prior corpus.

## Artifacts (all in `redteam/rt3b/`)

- `rt3b_corpus.tsv` — frozen corpus, SHA256 `aeb83031…8642ef20`
- `rt3b_run.zag` — pure-Zag runner; `rt3b_run` — built binary (not committed)
- `run1.txt` / `run2.txt` — both runs, SHA256 `d006deba…8ea6f42` each, byte-identical
- `build.log`, `run1.stderr`, `run2.stderr` — build/run logs

No commit made, per instructions.
