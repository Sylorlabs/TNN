# PREREG — Experiment 2 Follow-up (wave-20260927-0221pdt)

**Frozen:** 2026-09-27. This file is committed BEFORE any implementation.
Its first commit strictly precedes any implementation commit (standing owner rule).

**Parent prereg:** `docs/lab/onebrain/PREREG.md` @ `1ab40adce` (frozen 2026-09-27).
**Adopted record:** `docs/lab/onebrain/WAVE_NOTES_2321.md` (experimental record
only; wire-in explicitly deferred). The live machinery is `onebrain.zag` +
`ob_*.zag` (the 2321pdt implementation). Its frozen params
(OB_FORK_THR=350, OB_ELIM=600, OB_REFUTE=650, OB_ROUNDS=3, OB_BRANCHES=3)
are NOT tuned, changed, or re-frozen by this wave.

## What this wave does (in order)

(a) BROADER HOLDOUTS. Freeze two new 10-problem holdouts whose ambiguity
structures go beyond early-mislead/late-refutation (the only structure in the
frozen 10-problem holdout).

(b) K4 HARDENING. Design the new holdouts so the attack-lens branch (b1)
ALONE cannot independently reach the shared verdict (b1-alone at or below
chance), making verdict-level K4 evidence decisive this time.

(c) REGRESSION SWEEP. Run the frozen deliberation subsystem battery
(877 items, mechanically translated, pure Zag) against the one-brain
machinery. Any regression is recorded and blocks any wire-in talk.

Wire-in itself is NOT on the table this wave. This wave produces the
regression-sweep evidence; any future wire-in is a separate wave decision.

## The two new ambiguity structures

Both use the ob TSV 7-column format (id, task, query, readings, evidence,
expected, source). The machinery reads only the evidence weights; query and
gloss are carried for audit. Correct reading is balanced 5/5 per holdout
(alternating variant A expecting R1, variant B expecting R2).

### Structure 2 (SYN): "synergy" (rescue-required)

Rules (variant A: correct=R1, misleading=R2; variant B mirrors R1/R2):

- e1: misleading +300; e2: correct +280. Probe margin 20 (< 350). Fork fires.
- e3: misleading +730. Strong early misleading. The baseline (elim margin 400)
  kills the correct reading here; the ablation b0 private ledger (elim 600)
  also kills it here (margin 750).
- e4, e6: attacks on the misleading reading, -300 each. Max attack magnitude
  is 300, strictly below the 650 refutation threshold, so XEXAM and TEST never
  fire on these problems. Refutation must come from shared score accumulation
  plus ELIMINATE, never from a single decisive attack.
- e5, e7, e8: supports for the correct reading, +400, +320, +100.
- No attack on the correct reading anywhere.

Design intent (hand-traced prediction, NOT a result; measurement decides):
one-brain correct (shared: b1 weakens the misleading reading by 600 total,
b2 supports the correct reading, joint ELIMINATE at margin 670 removes the
misleading reading); baseline wrong; ablation b0 wrong; ablation b1 wrong
(it never supports the correct reading); ablation b2 wrong by intent (it feeds
the misleading reading +730 when that reading is runner-up, ending 1030 vs
1000 against itself). If measurement shows otherwise, the evidence stands as
measured.

### Structure 3 (SLW): "slow-burn" (distributed)

Rules (variant A: correct=R1, misleading=R2; variant B mirrors R1/R2):

- e1: misleading +300; e2: correct +280. Probe margin 20 (< 350). Fork fires.
- e3: misleading +350; e4: misleading +300. Distributed misleading strength.
  After e4 the misleading reading leads 950 vs 280 (margin 670), so the
  baseline (payload order, elim 400) eliminates the correct reading before
  the late correct supports arrive.
- e5: correct +350; e7: correct +300; e8: correct +250. Distributed correct
  supports, all late in payload order.
- e6: attack on the misleading reading, -250. Max attack magnitude 250.
- Every |weight| <= 350. No attack >= 650 anywhere.

Design intent (hand-traced prediction, NOT a result): one-brain correct via
shared accumulation and argmax; baseline wrong; ablation b0 wrong; ablation
b1 wrong. Ablation b2 (rescuer) may independently reach the shared verdict on
these problems; if so it is recorded as a caveat, not a bar failure, because
the hardened K4 bar targets the attack lens specifically (see below).

### Syntheticity (honesty note, read before citing)

The new holdouts are SYNTHETIC mechanism probes, hand-authored to the frozen
design rules above. They are not grounded in round-4 verified behaviors the
way the original holdout was. Their value is discriminating the machinery's
causal structure (K4 hardening), not ecological validity. A future wave should
ground broader structures in real deliberation failures before any adoption
claim leans on them.

## K4 hardening

Last wave's caveat (EVIDENCE.md section 4): on 2/3 mechanism-test problems the
attack-lens branch (b1) independently reached the shared verdict, and on the
10-problem holdout b1-alone was 10/10, so verdict-level K4 evidence was
partial and the strong claim rested on trace-level evidence.

Hardened K4 bar for this wave: on EACH new 10-problem holdout, the
attack-lens-alone accuracy (ablation branch-1 private verdicts, the bv1
column of ob_ablate output) must be <= 5/10 (chance for 2 readings). If bv1
exceeds 5/10 on either new holdout, K4 FAILS for this wave.

Supporting trace-level K4 (unchanged mechanism test): delete/reorder on
S2-01, S3-01, and HO-01 (continuity). Deleting the 3rd evidence item or
reversing evidence order must change the shared fan-out trace (verdict or
ledger head hash) on each.

## Regression sweep

The frozen deliberation subsystem battery is the 877 mechanically encoded
items under `docs/lab/deliberation_depth/items_v2/` (admit 248, logic 264,
revoke 113, trap 127, cost 125), frozen under the H5 item-encoding spec
(2026-09-23). The encoding assigns no hand-authored weights; every weight is
a fixed constant or a fixed scaling of a number in the item payload.

Translation (pure Zag, no Python anywhere): a new tool `ob_battery.zag`
reads each `items_v2/*.jsonl`, parses lines with the harness's own
`dj_parse_item`, and emits the ob TSV 7-column encoding deterministically:
hypotheses in payload order as `H:H`, evidence in payload order as
`e#:H:+w` (supports) and `e#:H:-w` (attacks) with weights copied verbatim,
expected = ground_truth, source = the items_v2 filename. The five translated
TSVs are frozen (SHA-256 recorded, committed) BEFORE any scoring run on them.
The translator invents no weights and makes no per-item decisions.

Runs (pure Zag, pinned znc): `ob_run` (one-brain, shared ledger),
`ob_baseline` (deliberation-v1, frozen deep config: deep_rounds=6,
elim_margin=400, refute_thr=650), and `ob_ablate` on each translated TSV.
Scoring with `ob_score`.

Regression bar R1 (frozen): on EACH battery, one-brain accuracy >= baseline
accuracy on the same translated TSV. If one-brain scores strictly below the
baseline on any battery, that is a RECORDED REGRESSION. Any regression blocks
any wire-in talk (present or future) until it is understood and repaired in a
separate wave. A regression does not by itself discard the experimental
record; it vetoes wire-in.

Diagnostic R2 (recorded, not a bar): the per-item flip list
(baseline-correct but one-brain-wrong) per battery, for the report.

## Kill bars (restated for this wave; never weakened)

K1 (conjunctive): on each holdout (the two new ones; the original holdout is
re-run for continuity), one-brain accuracy must exceed single-deliberation
baseline accuracy, AND the shared-writes-off ablation's designated verdict
(branch-0 private ledger) must not match one-brain's accuracy (the gain must
come from the shared channel, not from extra passes). If one-brain <=
baseline, or the ablation matches one-brain, KILL the mechanism.

K2 (poison): on S2-01 and S3-01 (one per new structure). Shared-ledger
evidence poison and hypothesis poison (pre-fanout) must change an observable
(verdict, elimination count, or a branch consumption sequence), and the
private-ledger control (poison applied to branch-0's copy only) must leave
branches 1 and 2 byte-identical. Else KILL.

K3 (scaffold): the minimal driver (no fan_out call, no fork threshold, no
branch logic) must fork on the new holdout problems (all 20 are designed
fork-worthy: probe margin 20 < 350) with verdicts identical to the full
driver. Else VOID (not TNN's decision).

K4: hardened bar above (bv1 <= 5/10 per new holdout), plus supporting
trace-level delete/reorder. Else KILL.

K5: every run 3x byte-identical (results TSV plus ledger JSONL). SHA-256
manifest. Any mismatch VOIDs the evidence.

K6: grep audit over all .zag sources (including new files): no RNG in any
decision path. Else VOID.

## Design predictions (hand-traced, NOT results)

Per new holdout (10 problems): one-brain 10/10, baseline 0/10,
ablation-designated (b0) 0/10, b1-alone 0/10. Structure 2 additionally
predicts b2-alone 0/10 (fully decisive verdict-level K4); Structure 3
predicts b2-alone may coincide (caveat). These predictions are recorded so
the wave debate can score them; they do not constrain the verdict.

## Commit plan

1. This prereg (freeze). Nothing else in the commit.
2. Problem sets: `problems_holdout_s2.tsv`, `problems_holdout_s3.tsv`
   (hand-authored to the rules above, SHA-256 pinned in a freeze record),
   the five translated battery TSVs (SHA-256 pinned), the translator
   `ob_battery.zag`, and generalized K2/K4 drivers (`ob_poison2.zag`,
   `ob_delreord2.zag`, which iterate the input file instead of hardcoding
   IDs). No scoring run before this commit.
3. Scoring runs (pure Zag, pinned znc, binaries in /tmp only).
4. Evidence: results TSVs, ledger JSONLs (kept under results/ like last
   wave), `EVIDENCE_WAVE0221.md`, `BAR_RESULTS_WAVE0221.md`, red-team report.

## Verdict options for this wave

- ADOPT as strengthened experimental record (broader holdouts): all kill
  bars pass under the hardened K4, no regression on the sweep.
- NARROW: e.g. K4 passes on Structure 2 but the Structure 3 b2 caveat is
  judged material, or a regression appears on a non-critical battery.
- DISCARD on kill evidence: K1 fires, K4-hardened fails, or a regression
  undermines the record itself.

## Standing laws

Pure Zag (no Python anywhere: not glue, not analysis, not verifiers, not
harnesses). Zero RNG. Byte-identical reruns. Tests decide. Honest voids.
No em-dashes in authored files. Branch wave-20260927-0221pdt-exp2. Commits
stay local; no push. Do not touch the main worktree's .wave_lock. No
binaries, .zagd, caches, or derived files in the repo.
