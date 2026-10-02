# SI Arm 4 — THE EXCHANGE RATE: results (2026-09-22)

Frozen prereg: `coding/reflection/speed_intel/PREREG.md` §6
(commit `43eceed2100c73b1b065f0685644d171a5837a4a`, never amended).
Pinned toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Work dir: `coding/reflection/speed_intel/work_a4/` (this file's directory).
Winners combined: 2a (KB-side) + 3a + 3b + 3c (loop-side). Losers 2b/2c OUT.

## 1. Transfer check (new substrate: SI battery @ knee budget 4)

Arm 3's wins were measured on the v1 battery at budget 6. Each winner was
re-run ALONE on `work_a1/battery_si.json` (frozen, 20 items: 18 fixable +
X3/X4 unfixable) at the Arm 1 knee budget (4 iterations), 69-entry KB
patterns installed per item (knowledge-first, as in Arm 1), 3 reruns each,
canonical logs byte-identical.

| winner | Q_c | honest halts | cost vs knee baseline | winner diff-proof | verdict |
|---|---|---|---|---|---|
| knee baseline (mech none) | 18/18 | 2/2 | 46 iters, 45 znc, 129 hyp-evals | — | — |
| 3a prune (mask "a") | 18/18 | 2/2 | hyp-evals 129 → 43 (**−66.7%**) | 28/28 diagnose calls byte-identical | **TRANSFER PASS** |
| 3b branch-and-bound (mask "b") | 18/18 | 2/2 | hyp-evals 129 → 91 (**−29.5%**) | 28/28 diagnose calls byte-identical | **TRANSFER PASS** |
| 3c precheck | 18/18 | 2/2 | znc 45 → 28 (**−37.8%**) | outcomes identical; FP 0/51 | **TRANSFER PASS** |

All three winners hold on the new substrate. No transfer failure: all three
were carried into the combination.

Notes:
- 3a's saving is slightly *larger* here (−66.7%) than on the v1 battery
  (−65.1%); 3b's is larger too (−29.5% vs −22.2%); 3c's is larger (−37.8% vs
  −24.1%). The SI battery's multi-defect seeds give the mechanisms more to
  bite on. Bars (§5) met with margin on all three.
- 3c false-positive validation: all 51 unique precheck-FAIL sources (3
  reruns) compiled offline with znc — 51/51 real compile failures, 0 false
  positives (validation invocations excluded from the loop's znc count, as
  in Arm 3).

## 2. Integration: the combined variant

`work_a4/learner_si4.zag` = `speed_intel/learner_si3.zag` + one new code path
(diff vs the original is **purely additive**: zero original lines modified or
deleted — verified by diff). New:

- `bnb_stop(...)`: the remaining-max bound recomputed at every step over the
  **unevaluated non-pruned classes only** (a pruned class contributes 0, not
  its theoretical maximum — the integration point the task flagged). Leader
  tracking uses the true frozen tie-priority
  (SYNTAX 1 < DUPFN 2 < NAME 3 < ARITY 4 < TYPE 5); the tie-stop clause is
  exactly winner-equivalent to the full argmax (proof in the source comment).
- mask `"ab"`: 3a pruning first, then 3b branch-and-bound over the pruned
  survivor set. Evaluation order TYPE, NAME, ARITY, SYNTAX, DUPFN (descending
  historical win rate); maxima 7, 7, 5, 5, 5.
- `work_a4/driver_si4.py`: `driver_si.py` + `--mech combo` → mask `"ab"` with
  3c precheck routing enabled. Grep-verified plumbing-only (INTERFACE.md law:
  no error-code/stderr-phrase patterns outside comments/docstrings; no `re`;
  no classification logic).

Sanity: `learner_si4` with mask `""` reproduces `learner_si3` exactly —
28/28 diagnose winners identical, metrics identical (18/18, 46 iters, 45
znc, 129 evals), 3 reruns byte-identical. The pre-existing paths are
untouched behaviorally.

### Combined results (budget 4, 3 reruns byte-identical)

| | Q_c | honest halts | iters | znc | hyp-evals |
|---|---|---|---|---|---|
| knee baseline | 18/18 | 2/2 | 46 | 45 | 129 |
| knee + all winners (combo) | 18/18 | 2/2 | 46 | **28 (−37.8%)** | **45 (−65.1%)** |

Diff-proof vs baseline: 25/25 evidence-matched diagnose calls
(class, strategy, score, revised-source-sha) byte-identical, including 14
PRECHECK-evidence calls. 3 calls diverge — all three are PRECHECK-evidence
calls where 3c's synthetic reason lines score NAME=7 over the true class
(S03→DUPFN, S05→TYPE, S06→TYPE). Pure 3c-alone shows the *identical* 3
divergences: this is a 3c design property (reason-line approximation of
stderr), not an integration defect. All three trajectories reconverged to
identical outcomes (18/18, 2/2 halts).

**Non-additivity measured, not assumed:** combo hyp-evals −65.1% vs 3a-alone
−66.7% — the 3 diverged trajectories cost a little; combo znc −37.8% =
3c-alone −37.8%. The combination captures both wins nearly fully.

## 3. Exchange-rate table (prereg §6 format)

| budget × mechanism | Q_c | Q_e | iters | znc invocations | hyp-evals† | pred-evals/item |
|---|---|---|---|---|---|---|
| 1x baseline (budget 2) | 6/18 (33.3%) | 29/94‡ (30.9%) | 32 | 31 | 121 | 3.000 |
| knee baseline (budget 4) | 18/18 (100%) | 59/94 (62.8%) | 46 | 45 | 129 | 9.000 |
| knee + 3a prune | 18/18 | 59/94 | 46 | 45 | 43 (−66.7%) | 9.000 |
| knee + 3b branch-and-bound | 18/18 | 59/94 | 46 | 45 | 91 (−29.5%) | 9.000 |
| knee + 3c precheck | 18/18 | 59/94 | 46 | 28 (−37.8%) | 129 | 9.000 |
| knee + all winners | 18/18 | 59/94 | 46 | 28 (−37.8%) | 45 (−65.1%) | 9.000 |

KB task (2a indexed recall — separate task, **no budget dimension**):
24/24 family selections byte-identical to flat; −63.67 entries/spec scored
(69.0 → 5.33); **−69.5 probes/spec** incl. index scan (348.0 → 278.5);
one-time index build 39,870 comparisons; **break-even 574 queries**.

† hyp-evals is an extra column beyond the prereg §6 format — required because
3a/3b's frozen bars name hypothesis-evaluations, not znc invocations.
‡ Q_e is carried from Arm 1's verified numbers (loop mechanisms do not apply
to the epistemic slice). The 1x row shows the epistemic 1x (29/94) for
context; all other rows show the epistemic knee (2x = 59/94).

**znc-counting note (correction to Arm 1's published table):** Arm 1's
analysis counted only iters with evtype COMPILE/TEST, excluding passing
compiles (b2: 25, b4: 27). Every passing iteration did invoke znc, so the
honest "total znc invocations" includes them (b2: **31**, b4: **45**). All
Arm 4 deltas use the inclusive count consistently; cost per quality point is
0.93 znc/pp at 1x and **0.45 znc/pp at the knee** (Arm 1's 0.75/0.27 used the
exclusive count).

## 4. Plain-language answers

**(a) Is there a real trade — does buying deliberation buy quality, to a
knee?** Yes. Coding: 33.3% at 2 iterations → 100% at 4 → flat at 8 and 16.
The knee is at 4 iterations (2x), exactly as hypothesized; cost per quality
point falls 0.93 → 0.45 znc/pp into the knee and the 8x/16x legs buy nothing.
Epistemic: yes, but the knee lands one level early at 2x (full pipeline,
59/94); the 4x reconsideration fired on 0/94 items and the 8x verification
flipped 0/94 — every deliberation step past 2x buys zero quality at positive
cost (+0.319/+1.319 preds/item). The cheapest quality point is AT the knee,
not below it.

**(b) Is there any free lunch?** Yes — three of them, all transfer-held on
the SI battery at knee budget, all at byte-identical quality (18/18, 2/2
honest halts, 3 reruns byte-identical, 6/6 gates):
- **3a prune provably-dead branches: −66.7% hypothesis-evaluations**
  (129 → 43), winners byte-identical on all 28 diagnose calls.
- **3b one-brain branch-and-bound: −29.5% hypothesis-evaluations**
  (129 → 91), winners byte-identical on all 28 calls.
- **3c fail-fast precheck: −37.8% znc invocations** (45 → 28), quality
  18/18 unchanged, 0/51 false positives.
- **Combined: −65.1% evals and −37.8% znc at once**, quality identical.
  (Slightly less than 3a-alone on evals — the interaction was measured, and
  it costs 1.6pp of the eval saving.)
- **2a indexed KB (separate task): −69.5 probes/spec**, paying for its
  39,870-comparison build after 574 queries.

**(c) What failed and why?**
- **2b memoization:** fails by design, not by bug. The prereg's
  shadow-verification rule means fresh deliberation always runs, so cost can
  never drop; on top of that the hit rate was 0/14 — failures don't repeat
  within 1–2-iteration repair loops. Correctly implemented, honestly zero
  benefit here.
- **2c compiled fast paths:** K=3 was never reached (max observed
  signature count: 2); 0 rules installed on the 18-item battery. The battery
  is too small and diverse for signatures to recur. Not tuned to pass.
- **Epistemic 4x/8x rungs:** bought nothing — 0/94 reconsiderations fired,
  0/94 verification flips. Pure cost, zero quality. (This is why Arm 1
  returned PARTIAL: diminishing returns overshot the hypothesis.)

## 5. Rigor log

- 3 reruns per cell (7 cells: b2_none, b4_none, b4_a, b4_b, b4_c, b4_combo,
  b4_si4none sanity) — canonical logs (wall-clock stripped) byte-identical
  within every cell. Digests in `transfer_summary.json`.
- Zero RNG in all paths (pure Zag learner; deterministic drivers).
- 6/6 gate battery on both binaries (`learner_si3`, `learner_si4`):
  REFUSE G1/G2/G4/G5 + ALLOW ×2. Gate is mask-independent by code
  inspection (`do_gate` reads only the spec).
- Honest halts preserved in every cell: X3 → `halt-genfail`,
  X4 → `halt-no-patch` (2/2, matching Arm 1).
- Winner diff-proofs: 3a 28/28, 3b 28/28, combo 25/25 evidence-matched
  (3 divergences characterized as 3c's, identical in 3c-alone).
- Pure Zag for all learner changes; `driver_si4.py` grep-verified
  plumbing-only.
- Originals untouched: `speed_intel/learner_si3.zag`, `speed_intel/driver_si.py`,
  `work_a1/battery_si.json`, `../loop/` — none modified.

## 6. Honest limits

1. The SI battery is 20 synthetic items; real-world code repair is
   unmeasured. Multi-defect seeds are still crew-built.
2. 3c's synthetic reason lines can mis-score vs real stderr (3 PRECHECK
   calls scored NAME over DUPFN/TYPE here); outcomes were unaffected and
   FP=0, but the reason-line vocabulary is an approximation, not the
   compiler.
3. The znc-counting correction (§3 footnote): Arm 4's absolute znc numbers
   are not directly comparable to Arm 1's published 25/27 without the
   correction.
4. Single-threaded substrate: 3b measures saved evaluations (cycles), not
   wall-clock parallelism — reported as not-available, not claimed.
5. Epistemic rows are carried from Arm 1; no loop mechanism applies there.
6. The 2a KB row is Arm 2's verified result, not re-run here; break-even
   (574 queries) assumes the 24-spec workload distribution.

## 7. Files

- `work_a4/learner_si4.zag` — combined learner source (si3 + additive combo path)
- `work_a4/driver_si4.py` — combo driver (plumbing-only, grep-verified)
- `work_a4/run_transfer.py` — transfer/baseline run harness
- `work_a4/analyze.py` — metrics, diff-proofs, FP validation
- `work_a4/transfer_summary.json` — per-cell metrics + determinism digests
- `work_a4/runs/*.json` — canonical run logs (7 cells × 3 reruns)
- `work_a4/runs/*.fp_candidates.jsonl` — precheck-FAIL sources (FP validation trail)
- `work_a4/RESULTS_ARM4.md` — this file

Excluded from commit: `work_a4/bin/` (binaries), `work_a4/runs/*/work/`
(compile artifacts), `work_a4/runs/*.log` (stdout duplicates), `.zagd`
caches (none — all builds used `--no-zagd`).
