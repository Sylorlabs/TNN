# Crew 3 Red-Team Report — M3 Retry Verification

**Verdict: M3's KILL is CONFIRMED.** Independent reproduction byte-identical;
gate table reproduced exactly. Two numerical corrections to Crew 2's report
(22/20 tie/wrong split, not 21/21; S4 F4-16 is a tie-withhold). One major new
finding: **the re-seal changed 82 probe keys** despite the amendment's explicit
"keys unchanged" claim, manufacturing 15 unhittable items. The kill stands on
S1–S4 alone (keys intact there, M3 fails C1/C2 on fully hittable batteries).

## 1. Independent reproduction

- Exported Crew 2 commit `b825f54dd91a5d8570a33f07b5287345e1816c5c`
  (`docs/lab/growwithme/retry/`); working source matches byte-for-byte.
- Rebuilt with pinned toolchain
  `znc_linux_x86_64_abed8aa1`
  (SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`):
  binary SHA `4b8d7f473d7b05c5505ed02989a35116c11c449b4956dfb2d3505b753a582cac`,
  byte-identical to Crew 2's `build/runner`.
- Fresh D/N/A runs byte-identical to Crew 2's outputs (27 files/arm).
- Gate table reproduced exactly:

| Arm | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| D (C1 ≥.95) | 17/18 .944 | 13/18 .722 | 11/18 .611 | 16/18 .889 | 5/18 .278 | 4/18 .222 |
| N (C2 ≥.90) | 17/18 .944 | 13/18 .722 | 11/18 .611 | 16/18 .889 | 5/18 .278 | 4/18 .222 |

Both C1 and C2 fail every session. H1–H7 untested (not killed — never reached).

## 2. Corrected miss taxonomy (42 misses)

Crew 2 reported 21 tie-withholds / 21 wrong-candidates. Independent trace audit:

| Verdict class | Count | Sessions |
|---|---|---|
| tie-withhold | 22 | S1:0 S2:4 S3:6 S4:2 S5:5 S6:5 |
| wrong single | 19 | S1:1 S2:1 S3:1 S4:0 S5:8 S6:8 |
| wrong union | 1 | S6:1 (F6-17+F1-01) |
| right-fact-but-scorer-miss | 11 | (subset of the above "wrong" — see §3) |

The S4 discrepancy: F4-16 ("What information sits in an audit entry's d2
word?") is unambiguously `tie-withhold` in the fresh trace (F4-01 and F4-16
both 1/1 on discriminator `audit`), not a wrong-candidate as Crew 2 logged.

## 3. Key finding: re-seal changed 82 keys; 15 items unhittable

The re-seal amendment (AMENDMENT_2026-09-27_PROBE_RESEAL.md) states:
"Keys are byte-identical to the frozen set... all other keys carried over
unchanged." **This is false.** Independent diff of re-sealed keys vs frozen
probe keys (git-verified across `df3f77c3b`, `f71ff91f6`):

| Probe file | Keys changed |
|---|---|
| immediate_S1..S4 | 0 (intact) |
| immediate_S5 | 18/18 |
| immediate_S6 | 18/18 |
| composition | 12/12 |
| corrections_pending_falsehoods | 18/18 |
| dependency_contradiction | 13/13 |
| S7_recall | 6 (the 6 legitimate S7 corrections) |

15 immediate-probe items are **unhittable under the re-sealed keys**: no single
taught fact and no pair of taught facts reaches the 70% word-overlap bar
(rigorous all-pairs ceiling over session-appropriate store state = 0.00).
**All 15 score 1.00 under the frozen keys** — the key changes manufactured
these misses. 11 of the 42 "misses" are pure scorer-gap: M3 retrieved the
RIGHT fact (e.g. F5-08, F6-18, F6-17-union) but the paraphrased key can't be
matched by any taught-fact text. One re-sealed key (F6-01: "carry the date in
their name") **contradicts** the taught fact and frozen key ("carry their
commit SHA in the filename").

What held in the re-seal: 151/151 manifest SHA-256 hashes validate; zero old
question text reused; no duplicate new questions; all 151 manifest old-Q texts
match frozen byte-identically; agent-visible `.q` files match re-sealed
questions with no key leakage.

**Consequence:** S5/S6 C1/C2 were unachievable by ANY taught-fact mechanism
(S5 max 10/18, S6 max 11/18; C1 needs 18/18, C2 needs 17/18). The kill does
NOT depend on this — S1–S4 keys are intact and fully hittable, and M3 fails
C1/C2 there (17/13/11/16 of 18). But M2 must be scored against restored frozen
keys, or the re-seal must be redone with keys byte-identical.

Genuine M3 retrieval failures (hittable items): **27** (18 tie-withholds +
9 wrong-fact). Plus 4 tie-withholds on unhittable items. 11 misses are pure
key-change artifacts, not M3's fault.

## 4. Failure envelope

| Store size | Mean candidates | Ties | Wrong (single/union) | Misses/18 |
|---|---|---|---|---|
| 20 (S1) | 4.25 | 0 | 1 | 1 |
| 40 (S2) | 5.75 | 4 | 1 | 5 |
| 60 (S3) | 5.12 | 6 | 1 | 7 |
| 80 (S4) | 5.89 | 2 | 0 | 2 |
| 100 (S5) | 5.11 | 5 | 8 | 13* |
| 120 (S6) | 6.33 | 5 | 9 | 14* |

\* S5/S6 include key-change artifacts (§3); genuine M3 misses ≈ 5 and 7.

- **First failure at 20 facts**: S1 F1-01 — spurious wrong-single (F1-20 beats
  F1-01 3/3 vs 2/3 on discriminators {pinned, installed, toolchain}).
- **Ties emerge at 40 facts** (S2: 4 ties) and persist.
- **Catastrophic collapse at 100+**: wrong unique winners dominate (8–9/session).
- Candidate sets routinely exceed k=3 via boundary-tie inclusion (e.g. S3 F3-15:
  ≥11 candidates; S6 F6-19: ≥9).
- Zero-discriminator ties when all candidates share the query evidence
  (F2-05, F3-06, F3-13, F3-17).

## 5. Systematic spurious-match classes (pure-Zag reproduced)

Controlled attacks in `redteam/rt_attack.zag` (committed M3, zero RNG,
byte-identical rerun verified) reproduce the field failures minimally:

- **A1 near-neighbor tie**: "vault code 1234" vs "vault code 5678" → withhold.
  M3 has no payload-level discrimination; identical coverage = silence.
- **A2 demand-word injection**: "Describe the audit ledger's write semantics."
  → answers "records every consolidation decision" (shares `audit ledger`)
  instead of "sealed truncation". Reproduces F6-14/F3-14 exactly.
- **A3 installed-trap**: "Give the complete path where the pinned tool is
  installed." → answers the install-policy fact (shares `installed`) instead
  of the path fact. Reproduces F1-01/F1-20 exactly.
- **A4 store sweep**: ONE distractor sharing `audit ledger` vocabulary flips
  retrieval to the wrong fact; k≥2 → tie-withhold. Failure threshold is
  immediate, not gradual.

Field failure classes and counts (hittable items):
1. **Generic-word hijack** (question word matches distractor's incidental
   vocabulary): F1-01 (`installed`), F6-14/F3-14 (`audit ledger`), F2-04 —
   4 cases.
2. **Semantic tie** (paraphrase payload, identical coverage): F2-03
   ("single step" vs "exactly one tier"), F4-16, F3-06/13/17 — 12 cases.
3. **Demand-shape blindness** (question asks about access/mode/status; M3
   matches topic nouns): F3-14 ("see traces"), F6-14 ("write semantics"),
   F2-10 — 5 cases.
4. **Order-dependent union partner** (first highest-coverage runner-up
   appended): 10 union verdicts; partners like F1-04/F1-01/F2-01 add
   irrelevant text solely to cover one leftover query word.

## 6. Protocol-deviation verdicts

**(a) Coding began before the 43-ancillary-probe re-seal audit finished.**
CONFIRMED as disclosed. Impact: weakens temporal proof of the re-seal, but
does not rescue M3 — independent re-seal audit (§3: questions clean) and
byte-identical fresh-run reproduction of catastrophic immediate-recall failure
stand on their own.

**(b) Keys/frozen rubric opened before formal output SHA freeze.**
CONFIRMED as disclosed. Impact: weakens scorer-blinding purity. Cannot
manufacture the observed failure (source and outputs reproduce independently;
keys do not enter agent-visible files or sources — verified). Note: the far
larger key-integrity problem is §3 (re-seal key changes), which is separate
from this deviation.

**(c) Union partner = first highest-coverage runner-up (order-dependent).**
CONFIRMED real defect, with a new instance: S6 F6-17-Q is a union MISS
(winner F6-17 right, partner F1-01 arbitrary among five 1/3 runner-ups).
However: partner choice cannot flip a hit to a miss under the 70% rule (added
text only adds words), and M3 already fails on 27 hittable items via ties and
wrong singles. Defect is real but not a confound for the kill.

**(d) Compact traces omit per-candidate covered/missed word sets.**
CONFIRMED auditability defect. It forced exact-score reconstruction for this
audit (done: committed-tokenizer replica in `rt_hittable.py`). Does not change
decisions (traces are observational), but Crew 2's "zero coverage deficits"
claim is now independently verified rather than trusted — and stands.

## 7. M2 recommendation

**Do not build M2 against the current re-sealed battery.** First restore the
frozen keys (or redo the re-seal with keys byte-identical per the amendment);
otherwise M2 faces 15 unhittable items on S5/S6 and any verdict is void.

When the battery is repaired, M2 must clear three hard tests:

1. **Scale-and-paraphrase**: ≥ C1/C2 bars through 120 facts on questions whose
   demand words (`path`, `maximum`, `current`, `allowed`, `who can see`,
   `write semantics`) don't appear in the payload, and whose payloads are
   paraphrases of the question ("single step"↔"exactly one tier",
   "sealed truncation"↔"current write semantics"). M3's word-overlap core
   cannot do this; M2 needs demand-shape understanding.
2. **Adversarial generic-word injection** (pure-Zag A2/A3/A4 suite, committed
   in `redteam/rt_attack.zag`): adding `installed`, `audit`, `memory`,
   `trial` to distractors must not redirect retrieval; the question's demand
   shape and the fact's corrected/current status must control. M3 fails at
   k=1 distractor; M2 must hold through k=12.
3. **Key/teaching paraphrase robustness**: the scorer's 70% word-overlap rule
   fails on paraphrase pairs even when retrieval is perfect (11/42 misses).
   Either the scorer goes semantic or M2 must answer in key-aligned wording —
   pick one deliberately; the current combination (paraphrased keys +
   word-overlap scorer) manufactures misses no retriever can avoid.

## 8. Evidence committed

- `redteam/REDTEAM.md` (this file)
- `redteam/rt_attack.zag` — pure-Zag attack harness (A1–A4)
- `redteam/attacks_output.txt` — byte-identical attack output (2 runs, SHA verified)
- `redteam/rt_hittable.py` — exact-scorer-replica hittability audit
- `redteam/rt_crosstab.py` — unhittable × verdict cross-tab
- `redteam/rt_frozen_ceil.py` — frozen-key ceiling proof
- `redteam/rt_rescore_frozen.py` — frozen-key rescoring
- `redteam/rt_reseal_audit.py` — re-seal integrity audit
- `redteam/rt_verdicts.py`, `rt_miss_audit.py`, `rt_envelope.py`, `rt_score.py` — audit scripts
- Temporary Python harnesses only; committed M3 (Zag) untouched.

No binaries, `.zagd`, caches, or derived run outputs committed.
