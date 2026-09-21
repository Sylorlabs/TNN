# Y4 Adjudication — MARATHON CREW U12

**Arm:** Y4 — Question-driven (lazy) cuts
**Date:** 2026-09-21
**Crew:** U12 (marathon adjudication)
**Status: COMPLETE-EXCEPT-D-CONDITION — no binding verdict yet (see §5)**

## 1. Frozen authority (extracted programmatically, not transcribed)

`units/PREREG_FREEZE.md` §3 row (line 496), byte-read from the frozen file:

| Y4 — Question-driven (lazy) cuts | CUT | Boundary candidates at ingest; segmentation committed at query time, conditioned on the question. | Recall accuracy >5% below eager arm D at equal total ledger cost (candidates + materializations); OR >30% of materialized chunks never recalled twice (laziness claim fails). |

Two kill disjuncts:
- **(a) D-conditional:** recall accuracy >5% below eager arm D **at equal total
  ledger cost (candidates + materializations)** → KILL.
- **(b) self-contained:** >30% of materialized chunks never recalled twice
  (laziness claim fails) → KILL.

## 2. The D-condition, exactly

Disjunct (a) cannot be evaluated without arm D's numbers. The frozen bar
requires, per corpus (prose, code):
- D's M1 recall accuracy (same scale as Y4's: the arm reports recall in
  tenths; the bar's "5%" = 50 tenths),
- D's total ledger cost = candidates + materializations per corpus.

**Y4's side is measured and frozen** (`COMPARISON_D.json`, `scorecard_r1_1x.json`
→ `y4_cmp`, and the `y4-cmp-1x` leg stdout):
- prose: recall 100.0 (1000 tenths), candidates 79303, materializations 79304,
  ledger cost **158607**
- code: recall 100.0 (1000 tenths), candidates 128648, materializations 128649,
  ledger cost **257297**

**Mechanical slotting procedure** (from `ARM_SPEC.md` §6, no judgment
involved): per corpus, KILL iff `cost_y4 ≤ cost_d` **AND**
`recall_y4 < recall_d − 5.0`. No D numbers were invented or estimated —
`COMPARISON_D.json` records `d: null` with status PENDING.

## 3. T3 / D-family status check (re-checked 2026-09-21 ~11:15 PDT)

- Branch `tnn-native-lab` head: `6d109ef5f7bb56b3159adf15cf12b39431989865`
  (Q1B teacher bake-off commit — unchanged since the check).
- Recursive tree walk at head: `docs/lab/units/arms/D/VERDICT.md` **does not
  exist** on the branch. Committed D files are only `BUILD_LOG.md` and
  `cl/arm.zag` (implementation, no verdict).
- Local `units/arms/D/VERDICT.md` is a DRAFT: "IN PROGRESS", M1 1x prose and
  code both `[PENDING]`, M2–M9 `[PENDING]`, verdict TBD.
- T3 has one partial working output: `units/arms/D/work/m1r1/m1_prose_r1.txt`
  (`M1,prose,100.0,100.0,84731`, single run, prose only, no ledger-cost field,
  uncommitted, and run on the post-regeneration corpus — see §6). It is
  **not slottable**: incomplete, unverified, uncommitted, and on a different
  corpus than Y4's evidence.

**Conclusion: D has not reported. The D-condition is unresolved.**

## 4. Everything not depending on D — completed and verified

### 4a. Full scorecard
`scorecard_r1_1x.json` (schema metrics-v1, arm y4, round r1, scale 1x) carries
all sections: `m1`, `m1_id_probe`, `m2`, `m9`, `m3`, `m4`, `m5`, `m6`, `m7`,
`y4_lazy`, `y4_cmp`, `m8`. Internally consistent with `VERDICT.md`,
`COMPARISON_D.json`, and the battery `STATUS.txt` / `fragment.jsonl` evidence.
Key values: M1 100.0/100.0 both corpora (79,304 / 128,649 chunks); M2
converges in 1 episode all tiers; M3 survival 100.0%, fresh recall 100.0%,
18,523 mgmt entries (bar ≥700); M4 100.0% revision both; M5 memory 1.823 B/B
(framework bar 1.5× — missed, recorded, not a frozen kill criterion) and 30.3
audit entries/kB (framework bar 10/kB — missed, recorded); M6 transfer tax 0.0
both directions; M7 hit 100.0%, reuse 100, dedup 50 hundredths; M8 gate PASS.

### 4b. M8 — independently re-verified by U12
From the committed run artifacts (`~/workspace/y4runs/battery/m8/<pert>/run{1,2}`):
- run1 vs run2 **byte-identical** for all 5 perturbations (clean, frag, aslr,
  starve, freelist) across all artifacts (`store_hashes.txt`, `store_chain.txt`,
  `ledger.bin`, `ledger_chain.txt`, `alloc_trace.txt`).
- Stronger than the gate requires: all **10 runs byte-identical to each
  other** (`ledger.bin` sha256 `dba8d6f0…` ×10; `ledger_chain.txt`
  `02121fbd…` ×10) — the perturbations perturb nothing.
- `audit_ledger.py` on the M8 ledger: **438,510 entries, 0 ordering/semantics
  issues** (matches `VERDICT.md`).
- **M8: VERIFIED PASS.**

### 4c. Kill bar (b) — ">30% never recalled twice" — SCORED, PASS
Committed `y4-lazy-1x` evidence: 6,649 materialized, 0 rematerializations,
**never_twice = 0.0%** → PASS (bar is >30%).
U12 fresh re-run of the leg (binary sha256 matches `evidence/binary_sha256.txt`):
stdout byte-identical across two runs; never_twice = 0.0% → PASS, confirmed on
the current corpus as well.

### 4d. Kill-bar evaluation summary (non-D)
No scored kill bar fired. The only unscored item is disjunct (a), which is
D-conditional. Determinism gate: 18/18 battery legs stdout=IDENTICAL (run1 vs
run2) per `evidence/STATUS.txt`; M8 PASS. No disqualification trigger.

## 5. Verdict

**Y4: COMPLETE-EXCEPT-D-CONDITION. Not binding.**

Everything adjudicable without D is decided and documented above: M8 PASS
(verified), laziness kill bar PASS at 0.0%, no other frozen kill bar fired.
The D-conditional disjunct is unscored because D has not reported.

**Evidence pointer for the future slotting:** `docs/lab/units/arms/Y4/COMPARISON_D.json`
(Y4's side: prose cost 158607 / recall 1000 tenths; code cost 257297 / recall
1000 tenths) + `docs/lab/units/arms/Y4/scorecard_r1_1x.json` → `y4_cmp`.
When T3 commits D's verdict with per-corpus M1 recall and total ledger cost,
apply §2's mechanical procedure per corpus: KILL iff `cost_y4 ≤ cost_d` AND
`recall_y4 < recall_d − 5.0`; otherwise the (a) disjunct is cleared and Y4's
verdict becomes binding PASS. `TRACKA_VERDICT_SHEET.md` line 63 stays
PROVISIONAL (conditional on D) until then.

## 6. Caveat: corpus regeneration after the battery

The `r1` corpora (`units/arms/../corpora/r1/*.bin`) were regenerated on
2026-09-21 05:45 UTC, **after** the Y4 battery evidence was taken (~05:07 UTC;
M8 artifacts ~04:33 UTC). The committed Y4 evidence remains the authoritative
record: it is internally byte-consistent (18/18 legs run1≡run2, M8 10/10
identical, audit clean). Fresh reruns on the current corpus are deterministic
(byte-identical across runs) but numerically differ on the lazy leg
(materialized 6,649 → 6,634; 15 fewer candidates on `t1_prose.bin`).
The kill-bar metric is unaffected: never_twice = 0.0% on both corpus states.
Future exact byte-reproduction of the 05:07 numbers requires the pre-05:45
corpus, which was not preserved. Recorded so no one mistakes a fresh-run
number delta for non-determinism.

## 7. Files

- `docs/lab/units/arms/Y4/U12_ADJUDICATION.md` (this file)
- Evidence (already committed at `7998f9d5`): `scorecard_r1_1x.json`,
  `COMPARISON_D.json`, `VERDICT.md`, `ARM_SPEC.md`, `evidence/STATUS.txt`,
  `evidence/m8_GATE.txt`, `evidence/binary_sha256.txt`, `audit_ledger.py`
- U12 verification scratch (not committed): `~/workspace/y4runs/u12-verify/`
