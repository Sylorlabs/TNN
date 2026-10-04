# Baseline: single-deliberation scorer (onebrain Experiment 2)

**Status:** design fixed 2026-09-27, before any scoring run on the frozen set.

## What it is

A minimal, pure-Zag, single-pass deliberator over the frozen problem set's
candidate readings. For each problem it scores every reading once with fixed
integer heuristics and takes the argmax (ties → lowest reading id). This is
the K1 comparator: the "single deliberation, no fan-out" that one-brain must
beat (conjunctively with the shared-writes-off ablation, per the prereg).

It deliberately mirrors the deliberation-v1 shape (GEN → ELIM → ARGMAX)
collapsed to one pass: the readings are the generated candidates, the score
is the single elimination signal, argmax is the verdict. It never sees
`expected_answer`.

## Scoring rule (fixed, uniform, no per-problem tuning)

For each reading's interpretation text R, with context turns C and final
query Q (parsed from the problem's `query` field on ` ~~ ` / ` ~~ Q: `):

| Feature | Definition | Weight |
|---|---|---|
| `overlap_ctx` | distinct content words of R also in C | ×3 |
| `overlap_q` | distinct content words of R also in Q | ×5 |
| `recency` | +1 if R shares any content word (len ≥ 5) with the last context turn | +4 |
| `correction` | +1 if Q contains a correction marker (`no/not/other/meant/sorry/wrong/instead/actually/wait`) AND R contains a correction-response word (`other/instead/correct/corrected/excluded/shaped/switches/return/returns`) | +6 |
| `brevity` | −(content-word count of R ÷ 16) | −1 per 16 words |

`score = 3·overlap_ctx + 5·overlap_q + 4·recency + 6·correction − wc/16`.
Choice = argmax; ties → lowest id (A before B before C). The chosen reading's
answer string is the baseline's answer.

Tokenization: lowercase alphanumeric words. Stopwords removed for overlap
features (a/an/the/is/was/are/were/did/what/when/where/who/which/how/of/in/
on/at/to/for/with/by/and/or/not/no/it/she/he/her/his/they/this/that/as/from/
about/so/if/then/there/my/you/we/i/me/us, turn tags t1u/t1t/…, single letters
and contractions). Marker/response/recency checks use exact token equality on
unstopped tokens (so `no` ≠ `know`, `not` ≠ `nothing`).

## Why it is not a strawman

1. **Standard dialogue priors, not crippled ones.** Lexical overlap
   (entity/predicate grounding), a recency prior, correction honoring, and a
   brevity prior are the textbook single-pass heuristics for reference
   resolution in dialogue. Nothing was removed to make it fail.
2. **It gets the easy cases right.** Where one reading clearly dominates on
   overlap/recency (e.g. a direct entity match with no competitor), it picks
   it. The frozen set was *designed* so these features leave close-call
   margins on the hard problems — that is what "hard for single deliberation"
   means in the prereg, and the set's hardness is a property of the problems,
   not of a weakened scorer.
3. **Same information the one-brain machinery gets.** It reads id + query +
   readings only. No expected answers, no extra features per problem.
4. **Deterministic and auditable.** Pure Zag, zero RNG, fixed integer
   arithmetic. Three reruns must be byte-identical (SHA-256 recorded in
   RUNLOG.md); any divergence voids the evidence per K5.
5. **Attack surface is documented.** The red team is invited to argue it is a
   strawman on these grounds: bag-of-words (no syntax/roles), no
   predicate-teaching check (the round-4 G6 class), no role-order check (the
   round-4 G7 class), recency as a flat prior. The defense: those checks are
   exactly the *second-pass, deliberative* machinery the experiment claims
   needs shared-state fan-out; a single pass that already had them would not
   be a single-pass baseline but the thing under test. The baseline is the
   best *single pass*, not the best system.

## What it does not do (by design)

- No multi-pass reconsideration, no ledger, no cross-reading invalidation.
- No role-order or predicate-teaching verification (see §5 above).
- No learning across problems; each problem is scored independently.

## Files

- `baseline.zag` — the scorer (pure Zag, syscalls only for file IO).
- `build_baseline.sh` — compiles with the pinned toolchain.
- `baseline_bin` — compiled binary (build artifact, not for the repo).
- `baseline_run1/2/3.txt` — the three determinism runs.
- `baseline_accuracy.md` — accuracy vs the frozen expected answers.

## Usage

```
./build_baseline.sh
./baseline_bin problems.tsv > baseline_run1.txt
```
