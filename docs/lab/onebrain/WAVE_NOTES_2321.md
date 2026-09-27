# Wave notes: wave-20260926-2321pdt : Experiment 2 (one-brain dispatch)

## What this wave did

Implemented Micah's frozen Experiment 2 from PREREG.md (frozen 2026-09-27,
before implementation): TNN-native fan-out where sub-deliberations share
one ledger, with four genuine one-brain requirements (TNN's own decision,
one shared ledger, causal cross-talk, single reintegrated verdict) and six
kill bars K1-K6.

## Machinery (all pure Zag, zero RNG)

- `onebrain.zag`: new module reusing the deliberation-v1 ledger layout
  (not a fork). Internal ledger-driven fork (probe 2 evidence; fork iff
  >=2 readings survive, evidence remains, margin < 350). Three branch
  lenses (payload-order confirmer, strongest-attack-on-leader,
  strongest-support-for-runner-up), fixed round-robin interleaving,
  joint reconciliation (elimination, leader cross-examination at the 650
  refutation threshold, runner-up test), one final ARGMAX.
- `ob_problem.zag`, `ob_encode.zag`: frozen-style TSV parsing and
  deterministic TSV->JSONL encoding.
- `ob_baseline.zag`: deliberation-v1 run once per problem, no fan-out
  (frozen config: deep 6, elim margin 400, refutation threshold 650).
- `ob_run.zag` (shared ledger), `ob_ablate.zag` (private ledgers, branch 0
  is the designated single verdict), `ob_score.zag` (TSV summarizer and
  pairwise comparison).
- Causal-test drivers: `ob_poison.zag` (K2), `ob_delreord.zag` (K4),
  `ob_scaffold.zag` (K3 minimal driver).

## Protocol breach and repair (read this)

The 15-problem developmental battery (`problems.tsv`) was iterated with
outcome knowledge: all 15 ran during design validation before any freeze,
and OB-15 was added after inspecting outcomes. A freeze was attempted but
its record was lost (ephemeral /tmp) and the noted hash does not match the
file, so its evidentiary status cannot be salvaged. Repair: the
developmental set is labeled developmental only (numbers in BAR_RESULTS.md
for history, not evidence), and a fresh 10-problem holdout
(`problems_holdout.tsv`) was built from round-4 ground truth, frozen
2026-09-27T06:42:47Z (sha256 in `results/holdout_freeze.txt`), with the
machinery's first run on it being the confirmatory measurement. Expected
answers were fixed before that run. All K1-K6 verdicts above rest on the
holdout, except K2/K4 mechanism tests which ran on developmental problems
(OB-01, OB-07, OB-14); mechanism tests exercise the machinery, not battery
accuracy, so this does not compromise them.

## Build (pinned toolchain, manual commands; no build script kept)

The compiler was extracted read-only from git to /tmp/e2/znc.bin (sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
Each tool was built with:

```
/tmp/e2/znc.bin <tool>.zag --no-zagd --no-analyze --no-foreground-cache -o /tmp/e2/bin/<tool>
```

for tool in ob_encode ob_baseline ob_run ob_ablate ob_score ob_poison
ob_delreord ob_scaffold. Binaries live only in /tmp/e2/bin (scratch, never
in the repo). A shell build helper existed briefly and was removed to keep
the deliverable pure-Zag.

## Results

See BAR_RESULTS.md (per-bar verdicts) and EVIDENCE.md (per-problem data,
causal logs, determinism manifest). Headline, confirmatory: one-brain
10/10, baseline 0/10, ablation 0/10 on the frozen holdout; K2/K3/K5/K6
PASS; K4 PASS with a noted caveat (attack-lens branch independently
reaches the shared verdict on 2/3 mechanism-test problems). No bar failed;
no void required. Known scope limits are listed in BAR_RESULTS.md.

## Files added (all under docs/lab/onebrain/, uncommitted)

Sources: onebrain.zag, ob_problem.zag, ob_encode.zag, ob_baseline.zag,
ob_run.zag, ob_ablate.zag, ob_score.zag, ob_poison.zag, ob_delreord.zag,
ob_scaffold.zag, problems.tsv (developmental), problems_holdout.tsv
(frozen). Docs: PREREG.md (pre-existing), BAR_RESULTS.md, EVIDENCE.md,
this file. Results: results/holdout_freeze.txt, holdout_onebrain.tsv,
holdout_baseline.tsv, holdout_ablation.tsv, poison_test.log,
delete_reorder_test.log, scaffold_test.log, determinism_manifest.txt.

## Standing constraints honored

No commit, no push. `.wave_lock` untouched. No wave record under
docs/lab/rsi/runs/. No binaries, .zagd, caches, or derived files in the
repo (ledger JSONL kept in /tmp only). No Python anywhere (grep
verified). No em dashes in authored files (grep verified; PREREG.md
predates this wave and was left alone). No money, no publication, no
outsider contact.

## Open questions for the parent / red team

1. K1 scope: the holdout tests one ambiguity structure by construction.
   Is 10/10 vs 0/10 on this structure enough to adopt, or should the next
   wave broaden the structure before adoption?
2. The attack-lens branch independently solves these problems (ablation
   bv1 = 10/10). Does that weaken the adoption case, or is the shared
   channel's causal role (K2/K4) sufficient?
3. K4's verdict-level evidence is partial (2/3 problems where a branch
   coincides). Accept the trace-level evidence, or harden the test?
