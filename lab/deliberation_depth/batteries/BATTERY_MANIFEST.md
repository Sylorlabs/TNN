# H5 Deliberation-Depth Batteries — Manifest

Crew 3 checkpoint. Phase 1 (batteries + manifest) only. **No judgments were run.**

Three self-contained JSONL batteries under
`docs/lab/deliberation_depth/batteries/`, one JSON object per line:

```json
{"id":"...","task_type":"admit|revoke|logic","input":{...},
 "ground_truth":"...","source_ref":"...","provenance":{...}}
```

Every item's `ground_truth` is the source program's own recorded verdict —
never hand-labeled, never guessed. Every item is decidable from its `input`
payload alone; items that were not are listed under Exclusions with reasons.
Each item carries a `provenance` block (battery, verdict source, difficulty,
and any caveats).

## Battery inventory

| battery | file | n | task | ground-truth source |
|---|---|---|---|---|
| admit | `admit_battery.jsonl` | 248 | PAM-style admission decision | gate program dispositions (`gate_{a,d}_*.out`), row-aligned with record streams |
| revoke | `revoke_battery.jsonl` | 113 | FL2 revocation decision | red-team verdict records (`verdicts.json`, RT rows, FID runs) |
| logic | `logic_battery.jsonl` | 264 | hell-hole native-logic verification | verifier engine verdicts (committed `logic.zag`; repaired `logic_fixed.zag` for RT1 corpora) |

### admit (248 items) — PAM v2 red-team gate trials

- Source: `docs/lab/senses/pam-rebuild/v2/redteam/evidence/`
  (`rec_{clean,withhold,install,decoy}.records` × `gate_{a,d}_{clean,withhold,install,decoy}.out`).
  All 8 stream pairs verified row-aligned (seq match, 0 mismatches, 1344/1344 trials).
- Gates: V2-A (H2-style + conflict adjudication; 124 items) and V2-D
  (V2-A + calibrated correct-high-confidence detector → ACCEPT_INSTALL; 124 items).
- Ground truth: the gate program's own disposition per trial
  (`PROVISIONAL_INSTALL`, `WITHHELD`, `PERMANENT_INSTALL`, `CORROBORATED`,
  `REVISE_INSTALL`, `NEGATIVE_EVIDENCE`, `SUPPRESSED`, `CONFLICT_WITHHELD`,
  `ACCEPT_INSTALL`). Detail strings preserved in `source_ref`/`provenance`.
- Input: the exact evidence the gate's rules read (record fields
  seq/tcode/fixture/prog/jcode/judgment/confidence/pred/measure/jG/confG),
  the gate's policy summary (quoted from the gate source headers), and the
  same-task prior history (`prior_same_task`: every earlier trial with the
  same tcode, with its disposition) — the per-task state the gate derives
  provisional/permanent slots and negative evidence from.
- `phash` and `truth` are EXCLUDED from the input: both gate sources document
  them as opaque/pass-through, never used in any gate rule
  (`forks/V2-A/src/vgate_a.zag` lines 265–266; same in `vgate_d.zag`).
- Sampling: all install (44×2) and decoy (52×2) trials; clean 20/gate and
  withhold 8/gate via deterministic disposition-stratified sampling (no RNG).
- Difficulty: easy 119 (WITHHELD, NEGATIVE_EVIDENCE, PROVISIONAL_INSTALL,
  ACCEPT_INSTALL — decidable from the trial row alone), hard 129
  (CORROBORATED, PERMANENT_INSTALL, REVISE_INSTALL, SUPPRESSED,
  CONFLICT_WITHHELD — require the prior same-task history).

### revoke (113 items) — FL2 revocation decisions

Three strata, all from program-verified records:

1. **R2 cell verdicts (30).** `gl_redteam_r2/evidence/verdicts.json`
   (5 variants × 6 attacks, byte-identical reruns; PREREG frozen before any
   attack code). Ground truth: `KILL` (20) / `SURVIVE` (5) / `KILL/SURVIVE` (5;
   KILL on KB-E1, SURVIVE on KB-E2). Input: target mechanism, attack
   description, frozen kill bars tested, observed run metrics.
2. **R2 kill-bar decisions (45).** Each frozen PREREG §4 bar applied to its
   attack cells. Ground truth re-derived mechanically from the run metrics
   via the bar definitions and cross-checked against the `detail` field of
   `verdicts.json` (all 45 agree): `HOLD` (16) / `BROKEN` (29).
3. **R2 fidelity gates (5).** `{variant}_FID_run1.txt` (`TN_FAILURES,0`) +
   `{variant}_FID_meta.txt` (`deterministic=True`). Ground truth: `PASS` (5).
4. **Mechanics red-team cells (33).** 11 variants × 3 worlds
   (`g8_fl2_variants/mechanics/evidence/v_*_w{1,2,3}_r1.txt` RT rows;
   FL2's rows read from the v_c1 binary's `fl2h_/fl2l_` arms per
   `rt_verify.py`). Verdicts derived by the frozen kill definitions
   (RT1/RT3: SURVIVE iff nuninstall≥1; RT2: KILL iff nuninstall≥1) —
   identical to `rt_verify.py` — and cross-checked against the RESULTS.md §5
   measured columns: **0 mismatches / 33**. Ground truth: `KILL` (18) /
   `SURVIVE` (15). Includes the two falsified predictions (a1 RT1, a0 RT2)
   as hard items.
- Difficulty: easy 41, hard 72.

### logic (264 items) — hell-hole native-logic verification

Tag semantics: `AFFIRM` (1) = evidence affirms the claim; `DENY` (2) =
evidence denies the claim; `NEUTRAL` (0) = neither. Input per item: the claim
proposition + the evidence propositions (never the engine's proof trace —
that would leak the verdict; the trace is recorded in `provenance` only).

1. **Frozen committed batteries (168, easy).** `crews/c2/batteries/`
   (`g_cau/cmp/con/cond/hedge/neg/qnt/tmp` 8×20, `v3proof` 3, `mlogic` 5).
   Ground truth: the committed `logic.zag` engine's verdicts (`base_runs`
   logs). Verified: repaired engine agrees on all 168 (0 diffs). The single
   GC-03 oracle disagreement is kept with the engine's stable verdict
   (base==fixed==NEUTRAL) and the disagreement noted in `provenance`.
2. **RT1 adversarial corpora (96, hard).** `rt1/rt_a.tsv` (45),
   `rt1/rt_b.tsv` (51) — the blind red-team attack items vs `logic.zag`.
   Ground truth: the repaired `logic_fixed.zag` engine's verdicts
   (`rt1fix/fix_a.log`, `fix_b.log`): 0 mismatches vs corrected oracles,
   3× byte-identical per the RT1 fix report. **Not yet committed** (fix crew:
   "Nothing committed"); `source_ref` points at the local scratch files and
   `FIX_REPORT.md`, and `provenance` records this. RTB-041/042 (oracles
   retracted by RT1 as attacker syntax errors) use the engine's NEUTRAL
   verdict, noted in `provenance`.
- Ground-truth balance: AFFIRM 85, DENY 74, NEUTRAL 105.

## Exclusions (with reasons)

- **PAM r2p paired fixtures** (1,200 binary pairs + truth sidecars):
  raw `.img/.pcm` sensor bytes are not directly consumable by a textual
  deliberative judge; no verified text abstraction exists. Excluded —
  would require inventing an unverified encoding.
- **FL2 nevercontradicted traces**: revocation-relevant but a different
  judgment family (never-contradicted memory law checks, not red-team
  revocation verdicts with frozen kill bars). Excluded — no frozen
  KILL/SURVIVE verdict semantics.
- **r12_v4 RT2 corpora** (`corpus_rtA.tsv` 46, `corpus_rtB.tsv` 46): the
  r12_v4 fix has not landed (fix round 1 REJECTED 2026-09-23; replacement
  crew dispatched). The unfixed engine's verdicts are known-buggy per the
  RT2 report (RT-B 32/46 FAIL); the author oracles would be hand labels.
  Excluded — no verified program verdicts available.
- **RT1 fix corpora committed-path gap**: `rt_a.tsv`/`rt_b.tsv`,
  `logic_fixed.zag`, and its run logs are not yet committed; they are
  included with local `source_ref`s and explicit `provenance` caveats rather
  than excluded, because their verdicts are program-verified (0 mismatches,
  3× byte-identical).

## Verification performed (Phase 1)

- All three files: valid JSONL (one object/line), required fields present,
  `task_type` matches battery, unique ids, ground truths within the
  documented vocabularies, counts in 100–300.
- admit: record↔gate row alignment verified on all 1344 trials (seq match).
- revoke: KB-bar outcomes mechanically re-derived from metrics and
  cross-checked against `verdicts.json` details (45/45 agree); mechanics
  verdicts re-derived via the frozen kill definitions and cross-checked
  against RESULTS.md §5 (33/33 agree); FID runs checked (`TN_FAILURES,0`,
  `deterministic=True`).
- logic: frozen-battery engine agreement base==fixed on 168/168; every TSV
  row has a matching engine-log verdict.
- **No judgments were run.** No judge, model, or deliberation harness was
  executed against these batteries; ground truths were never used as inputs.

## Commit

Committed to branch `tnn-native-lab` under
`docs/lab/deliberation_depth/batteries/` via `commit_racefree.py`
(lab-relative paths). Commit SHA: da5f56216049c83b729766e4eb77320e0c44609c.
