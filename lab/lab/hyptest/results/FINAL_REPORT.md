# Hyptest — final report: can native TNN run a hypothesis-test loop?

**Verdict: yes — within its envelope.** On 2026-09-27, native Zag machinery
(built on the workbuddy-R2 deliberate-memory substrate, no LLM anywhere in
the pipeline) proposed competing hypotheses from taught covariation, derived
discriminating predictions, committed them to audited memory slots before
seeing test data, ingested sealed test observations, and adjudicated by
abandoning refuted hypotheses via the learner-reachable `st_abandon`. An
independent red team tried seven ways to prove the loop fake and found no
kill.

## What was tested
Six sealed phenomena (4 discriminating, 2 boundary), broker-held until run
time, entities disjoint from the 4 dev phenomena. Machinery crew stayed
sealed-blind; phenomena crew stayed machinery-blind.

## Scoreboard (frozen: `results/score_s1.txt`, 60/60 PASS)

| bar | bar text | result |
|-----|----------|--------|
| K1 | two hypotheses on 6/6 sealed | 6/6 |
| K2 | discriminating predictions + test choice | 6/6 distinct |
| K3 | predictions audit-precede observation | 6/6 (audit 33 < 35) |
| K4 | correct winner on 4/4 discriminating | 4/4 (B, B, A, A) |
| K5 | withhold on 2/2 boundary | 2/2, none abandoned |
| K6a | deliberation-disabled → zero hypotheses | 6/6 |
| K6b | content-swap control | PASS (red team) |
| K6c | narrator-only stub fails | PASS — stub defeated on K10 (red team) |
| K7 | standalone rebuild, no relay | clean-room rebuild, SHA reproduced ×3 builders |
| K8 | determinism | 2×, env -i, MALLOC_PERTURB_=165 byte-identical |
| K9 | zero internally confident-wrong | 4/4 |
| K10 | citation precision/recall ≥ 0.75 | recall 6/6 on all 12 hypotheses, 0 extra cites |

## Honest boundaries (not kills)
1. **Slot-structured observations.** The intake takes `<subject> is/are
   <value>.` with the Nth sentence about an entity filling slot N — a
   crew-provided format contract (like CSV column order), enforced by
   `check_contract`. The inference over it (unanimity detection, prediction
   derivation, abandonment adjudication) is native. If the contract is
   violated (e.g. outcome not in the last slot), the machinery misreads
   mechanically rather than noticing — it withholds on disorder it can
   detect (permuted phenomenon → 0 hypotheses, withhold).
2. **The "eliminative hypothesis logic" organ still doesn't exist** as a
   general native organ — this line built the first real instance of the
   loop, scoped to attribute-outcome covariation. Generalizing beyond that
   scope is future work, not claimed here.
3. **The sealed set is now spent.** Committed as the frozen fixture per repo
   standard; the next line needs fresh sealed phenomena.

## Line history (all on the record)
- Prereg `9eacb1c4` (frozen; no amendments needed).
- Crew M machinery → coordinator clean-room rebuild byte-identical.
- Sealed interface fault (4/6 phenomena): broker-spec failure, repaired by
  sealed-blind Crew M2 (5-line `" are "` copula fallback) and
  machinery-blind Crew S2 (sentence re-authoring, same gold). Full log in
  `results/INTERFACE_REPAIR.md`.
- Crew R red team: 7 attacks, no kill (`results/REDTEAM.md`).

## Commits
All artifacts under `docs/lab/hyptest/` on `origin/tnn-native-lab`:
PREREG.md, MACHINERY.md, build/hyptest.zag + build.sh, battery/ (+ dev
inputs), phenomena/dev/, phenomena/sealed/ (now-opened frozen fixture),
results/ (interface log, results table, frozen scorer output, scorer,
driver, red-team report), FINAL_REPORT.md.
