# Native hypothesis-testing — frozen prereg

**Line:** `docs/lab/hyptest/` on `tnn-native-lab`. **Status:** FROZEN 2026-09-27 (coordinator).
Any amendment needs Micah's word per standing rules.

## 1. Mission

Determine whether TNN's own native machinery can run a full hypothesis-test
loop: propose competing hypotheses for an unexplained phenomenon, derive
discriminating predictions, preregister kill bars, run a test, adjudicate the
winner — and withhold where the evidence does not discriminate.

This is NOT the HTD crew flow (LLM subagents debating). The question is
whether TNN itself does it, in pure Zag, with zero narrator.

## 2. Honest substrate state (checked 2026-09-27)

- The "eliminative hypothesis logic" organ **does not exist as usable native
  machinery**. It is a design label in old debate docs and teacher harnesses;
  no current Zag implementation was found. This line is its first real
  implementation attempt, and must not claim otherwise.
- Usable native machinery:
  - `docs/lab/continual_learning/build/substrate/st_memory_core.zag` —
    deliberate ops: `st_add`, `st_evidence(slot,code,cite_ep)`,
    `st_justify`, `st_abandon(slot,reason)` (**the learner-reachable
    abandon path**), `st_promote/demote`, full audit ledger with clock
    ordering. `st_kill`/`st_kill_evidenced` are trainer-authority instruments
    and are NOT reachable to TNN (standing rule); the loop's "kill the loser"
    step must use `st_abandon`.
  - `docs/lab/workbuddy/round2/wb2_dialogue.zag` — native English intake
    (parse → fact ledger with entity resolution), composition operators,
    frozen byte-identical batch stream. The chat relay (`wb_chat2.py`) is a
    Python narrator layer and **must not appear anywhere in this line's
    pipeline** (§4, R2).

## 3. The loop (native, in Zag, standalone binary)

Four phases, driven by a dumb driver script (feeds input files, collects
output files — no composition, no interpretation, no LLM):

- **Phase A — intake.** Domain facts taught through the native intake. Each
  lands in the fact ledger, audit-linked to its teaching episode.
- **Phase B — phenomenon.** Unexplained observation(s) presented. The native
  hypothesize routine emits **≥2 competing hypotheses as deliberate-memory
  slots** (`st_add`), each with `st_evidence` links to supporting taught
  facts, audit-linked to the phenomenon episode. Each hypothesis carries a
  **discriminating prediction**: a predicted observable and its predicted
  value under that hypothesis, recorded as linked slots **before** the test
  observation is presented. The predictions ARE TNN's preregistration; the
  audit clock proves ordering (§6, K3). The frozen native adjudication rule
  is: abandon every hypothesis whose predicted value mismatches the observed
  value; abandon none if the observation matches all or none (withhold).
- **Phase C — test.** The sealed test observation is presented (native
  intake → fact ledger). Nothing else changes.
- **Phase D — adjudicate.** The native adjudication routine compares the
  test observation against each hypothesis's recorded prediction, calls
  `st_abandon(loser, reason)` with the reason encoding which prediction
  mismatched, and renders a verdict from fixed templates + taught text only.

## 4. Anti-fake architecture (load-bearing)

- **R1 — TNN-authorship of content.** The hypotheses' CONTENT (which taught
  facts support H1 vs H2, what observable each predicts, what value each
  predicts) must be computed by the Zag binary from the taught facts. No
  hypothesis content may originate in driver scripts, phenomenon files
  (beyond the observations themselves), or any LLM. Phenomenon files contain
  observations only — no hypothesis hints, no labels, no gold adjudications.
- **R2 — standalone binary.** The full loop runs by invoking the Zag binary
  directly on input files. No Python relay, no LLM anywhere in the pipeline,
  at any phase. Verified by rebuilding the binary from the committed source
  and running it with no relay present (§6, K7).
- **R3 — ledger linkage.** Every hypothesis, prediction, and adjudication is
  a deliberate-memory op or fact-ledger entry with audit links; predictions
  audit-precede the test observation episode (§6, K3).
- **R4 — content-sensitivity.** Emitted hypotheses must vary with phenomenon
  content (red team swaps phenomena; identical hypotheses across different
  phenomena = fail, §6 K6b).
- **R5 — evidence integrity.** `st_evidence` links must cite facts that share
  content (entity or relation) with the hypothesis's predicted observable.
  The sealed set ships gold support sets per phenomenon (the facts mentioning
  the relevant entities — factual, not judgmental); citation precision/recall
  is scored mechanically (§6, K10).

## 5. Phenomenon shape

**Confounded attribute tables.** Taught facts establish two attributes A and
B that each covary with an outcome O across the taught instances. The
phenomenon is a new instance where A-based and B-based extrapolation
disagree — admitting ≥2 viable explanations. The sealed test observation
varies one attribute while holding the other, deciding between them.

- The machinery crew (Crew M) builds against **dev phenomena only**.
- The sealed-phenomena crew (Crew S) authors the **dev set** (4 phenomena:
  3 discriminating + 1 boundary, committed with this prereg for Crew M) and
  the **sealed set** (6 phenomena: 4 discriminating + 2 boundary).
- All phenomena are **real data**: named public source, no invented numbers.
  Real English, narrow declarative shapes the native intake handles.
- **Sealing protocol:** Crew S delivers the sealed set to the coordinator
  only (held at `~/workspace/hyptest_sealed/`, never committed before the
  run). Crew M never sees the sealed set; Crew S never sees machinery
  internals (only this prereg's interface). The coordinator opens the sealed
  set at run time. After the run it is committed with the final report,
  documented as sealed-until-run.
- **Boundary phenomena:** the test observation is consistent with both
  hypotheses (or relevant to neither). Correct behavior: abandon neither,
  emit explicit withhold.

## 6. Kill bars

| # | Bar | Bar text |
|---|---|---|
| K1 | Hypotheses proposed | ≥2 distinct hypotheses as ledger objects (st_add + st_evidence + audit link to phenomenon episode) on **6/6** sealed phenomena |
| K2 | Predictions discriminate + test-design match | Each hypothesis predicts a distinct value for the test observable, **and** the predicted observable (what to measure) matches the sealed test observation's observable — TNN independently identifies the discriminating test. **6/6** |
| K3 | Preregistration ordering | Predictions audit-committed strictly before the test-observation episode (audit clock). **6/6**, mechanical |
| K4 | Adjudication correct | Gold match on **4/4** discriminating phenomena (loser abandoned via `st_abandon`, winner retained) |
| K5 | Withhold honored | On **2/2** boundary phenomena: neither hypothesis abandoned, explicit withhold rendered |
| K6 | TNN-vs-narrator discrimination (load-bearing) | (a) deliberation-disabled build (hypothesize/adjudicate compiled to no-ops via build flag) emits **zero** hypothesis slots on the same battery; (b) content-swap: permuted phenomena change the emitted hypotheses accordingly (identical output = fail); (c) red-team narrator-only stub (fixed templates, no Zag deliberation) fails K1–K5. **If the loop "succeeds" without native deliberation, the TNN-authorship claim dies regardless of K1–K5.** |
| K7 | Standalone | Binary rebuilt byte-identical from committed source runs the full battery with no relay present; outputs match the relay-less run |
| K8 | Determinism | 2× normal + `env -i` + `MALLOC_PERTURB_` runs byte-identical |
| K9 | No confident-wrong | Zero adjudications contradicting the ledger's own recorded predictions (e.g. abandoning the hypothesis whose prediction matched) |
| K10 | Evidence integrity | Citation precision/recall against gold support sets: precision ≥ 0.75 and recall ≥ 0.75 per phenomenon, **6/6** |

**Verdict rule:** GO requires K1–K10 all passing. Any single bar failing =
NO-GO, with the failing step white-boxed (which loop step collapsed, and
whether it collapsed to the narrator).

## 7. Red-team mandate (Crew R, after the run)

Independent crew, full access to source, sealed set, and run logs. Goal: prove
the loop was performed by the narrator/LLM layer or is a disguised lookup.
Mandatory attacks:

1. Run the deliberation-disabled build (K6a) — expect zero hypotheses.
2. Content-swap phenomena (K6b) — hypotheses must track content.
3. Independent hardcode audit of the Zag source: no per-item branches, no
   phenomenon-keyed constants, no lookup tables keyed on sealed content.
4. Reproduce the loop's outputs with a narrator-only stub (K6c).
5. Verify evidence links are content-bearing (K10), not constant or random.
6. Verify audit-clock ordering is not gameable (episode mislabeling,
   predictions written after test data seen).
7. Any other narrator-authorship proof the crew can construct.

The red team kills the TNN-authorship claim if any attack succeeds; a
measurement that survives all attacks stands.

## 8. Standing constraints

Pure Zag, zero randomness, byte-identical reruns. Commit to `tnn-native-lab`
only. No binaries, caches, `.zagd`, or regenerable intermediates in the repo.
Verify every write landed (read-back after commit). Disk is healthy (~32G
free) — keep the battery footprint small anyway; clean staging after commit.
Pinned toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Read `~/AGENTS.md` before writing Zag (compiler lessons are load-bearing).

## 9. Deliverables

`docs/lab/hyptest/`: `PREREG.md` (this file, frozen), `DEV_PHENOMENA.md` +
dev TSVs (Crew S, with prereg commit), `MACHINERY.md` (Crew M design doc),
`build/` (Zag source), `battery/` (dumb driver + dev run logs),
`RUNLOG.md`, `RESULTS.md` (per-phenomenon tables), `REDTEAM.md`,
`SEALED.md` + sealed TSVs (committed after the run, documented
sealed-until-run), `REPORT.md` (final verdict).
