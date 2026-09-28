# Phase 4 style attribution — CAN IT TELL WHO'S TALKING BY STYLE ALONE?

Question: with the name tag stripped, can TNN identify a known person from
talking style alone — and does it do it by itself, unprompted?

Short answers:

| Question | Verdict |
|---|---|
| (a) Asked attribution — "whose style is this?" | **UPHELD — 12/12, zero wrong-person** |
| (b) Spontaneous attribution — volunteers unprompted | **KILLED — 8/12 clean volunteered; 2 false volunteers on unknown lines** |
| (c) White-box mechanism — the brain activity, proven by intervention | **UPHELD — signal-dependence proven; LEX and CASE causally validated** |

The honest middle: it CAN tell by style when asked (perfectly, on novel
topics). Unprompted, it is conservative — it stays silent too often on the
quiet formal style, and it wrongly volunteered a name twice on unknown
log-style lines that landed in the excited person's neighborhood. The
mechanism is fully white-boxed: every decision emits its extracted features,
its distance to each person, its margin, and which feature families carried
the decision — and lesioning those families moves the margins exactly where
the traces predicted.

## How it works (plain English)

Four people each "teach" the system 12 utterances in their own style. The
system keeps one ledger per person: the average of 12 raw-byte measurements
(word count, word length, uppercase ratio, lowercase opening, !/?/./,
rates, hedge-word rate, ALL-CAPS-word rate, fragment endings, digit rate).
A new utterance is measured the same way and matched to the nearest ledger
by weighted distance. If the winner beats the runner-up by ≥15% it answers;
in a passive stream it only speaks up if the margin is ≥35%.

## The brain activity, concretely

Every decision prints four trace lines: the 12 extracted features, the
distance to each person, the winner with its relative margin, and the top
three feature families behind the margin. Example — a terse probe:

```
D feats w=6 wl=366 up=0 lo=1 b=0 q=0 s=0 c=3 h=0 c3=0 f=1 d=0
D dist p1=356 p2=972 p3=836 p4=802
D winner p1 rel=63 thr=15
D gapfam LEN=47 CASE=32 LEX=20
```

Read it as: 6 words, all-lowercase fragment → nearest the terse ledger
(356 vs 972), margin 63%, carried mostly by length (47%) and case (32%).

## What the interventions proved

Removing one feature family at a time (lesions) and re-running all probes:

| Lesion | What the traces predicted | What happened |
|---|---|---|
| LEX (hedge/caps-word vocabulary) | decisive for the 3 reflective-style probes | margins collapsed 26 pts exactly there (38→15, 48→21, 51→23) — **validated** |
| CASE (uppercase/lowercase habits) | decisive for 3 probes | margins fell 11 pts there vs ~1 elsewhere — **validated** |
| LEN (length habits) | "decisive" for 6 probes | margins barely moved — **not validated; the trace overstated it** |
| PUNCT / STRUCT | never decisive | removing them changed ~nothing |

Removing ALL families: 12/12 WITHHOLD — the attribution depends entirely on
the style signal, no priors, no memorized answers. The style code is
redundant (correlated habits back each other up), which is why no single
family is load-bearing — a finding, not a flaw.

## Red team

- Style drift (formal person being casual, reflective person being blunt): handled — correct or silent, never misattributed.
- Content-word trap (reflective person's keywords planted in terse style): NOT fooled — style won over keywords, margin 74%.
- Unknown styles (a fifth log-writing style): one correctly withheld; the other two were volunteered as the excited person — the 2 false volunteers that killed claim (b).
- Imperfect mimicry (terse person imitating excited, with leaked habits): envelope only — the system read the leaked true habits both times.

## Files

- `PREREG.md`, `AMENDMENT-01.md`, `AMENDMENT-02.md` — frozen design + amendments
- `BRAIN.md` — full white-box mechanism analysis
- `VERDICT.md` — claim-by-claim verdict with kill bars
- `NUMBERS.md` — every measured number, pullable
- `BUILD.md` — build notes and toolchain findings
- `sealed/` — frozen scripts, corpus hashes, expected answers
- `results/` — all outputs, score report
- `battery/` — runner + scorer
