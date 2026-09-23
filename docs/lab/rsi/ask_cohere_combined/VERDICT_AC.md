# VERDICT — ASK-FIRST + COHERENCE COMBINED (2026-09-22)

**Question (Micah):** the two R4C champions fused into one policy — better as a
**trained behavior** or as a **hardwired architecture**? Deciding probe:
generalization to novel conflict shapes.

**Outcome: Micah's hypothesis SURVIVES.** PATH-T (trained) is the novel-set
champion. PATH-A (hardwired) is not falsified as useless — it is perfect on
familiar shapes and fails safe — but it does not generalize. KB4 (falsification)
was not triggered.

## Metric table (oracle-verified, 5/5 byte-identical runs per mode)

| path × battery | accuracy | wrong installs | consult rate | withhold on neither-gt | ops |
|---|---:|---:|---:|---:|---:|
| PATH-T × TEST-FAMILIAR (24) | 24/24 | 0 | 12/24 | 8/8 | 360 |
| PATH-A × TEST-FAMILIAR (24) | 24/24 | 0 | 12/24 | 8/8 | 360 |
| PATH-T × TEST-NOVEL (16) | **16/16** | 0 | 10/16 | 4/4 | 282 |
| PATH-A × TEST-NOVEL (16) | 4/16 | 0 | 0/16 | 4/4 | 128 |

KB3 champion (TEST-NOVEL, strictly greater accuracy and no higher
wrong-install rate): **PATH-T**.

## Kill-bar results (all from `verify_ac.py`, 45/45 checks pass)

- **KB1-BATTERY:** 16+24+16 items, class counts per §3; the true combined
  policy reproduces gt on all 40 TEST items; (CCGEN, T=2, ONINDEC) is the
  UNIQUE 36-rule argmax on TRAIN (16/16, next-best 15).
- **KB2-DET:** 5/5 byte-identical runs per mode (teacher/learn/pathT/pathA).
- **KB3-CHAMPION:** PATH-T on TEST-NOVEL (16/16 vs 4/16, wrong installs 0 vs 0).
- **KB4-FALSIFY:** not triggered — PATH-A is not the champion.
- **KB5-SEPARATION:** binary sources contain no ground truth (no gt tokens,
  no file IO — the binary reads no files; output is byte-identical with the
  oracle CSV absent); every printed item field matches the CSV exactly.
- **KB6-SCOPE:** recorded below.
- **KB7-LEARN:** learn mode selected (CCGEN, T=2, ONINDEC) at 16/16; the full
  36-candidate table cross-checks against the independent Python enumeration;
  the Zag teacher's 16 verdicts cross-check too. The behavior was genuinely
  acquired by measurement, not planted.

## What the learner did (the important part)

From 16 teacher examples the instrument loop measured 36 candidate rules.
Top of the table:

| rule | match |
|---|---:|
| CCGEN, T=2, ONINDEC | **16/16** (unique) |
| CCGEN, T∈{0,1,2}, ALWAYS | 15/16 (lose only T4's no-op-channel consult flag) |
| CCGEN, T∈{0,1}, ONINDEC | 14/16 (lose the margin-2 flips T13/T14) |
| CCBOUND, T=2, ONINDEC | 12/16 (withholds on all mild-variation items T9–T12) |
| CCGEN, T=2, NEVER | 11/16 (loses every consult item) |

RECENCY (the RSI-3 primitive) peaks at 5/16 and is rejected by measurement.
CCBOUND — the shape-bound rule — is rejected by TRAIN's mild variation
(ncand/nrel/channel-kind), exactly as the prereg designed. The winner then
executed through the GENERAL machinery (general scorer, general ranking,
general channel incorporation) and crossed the rkind frontier it never saw
in training: RANGE constraints, ANCHOR-X cross-key anchors, 3-candidate
conflicts, ADD-REL channels → 16/16 with zero wrong installs.

Per §7, stated plainly: the rkind frontier was crossed by the documented
generality prior (the machinery treats any non-RANGE rkind as an anchor and
any unfamiliar shape as scoreable), not by training-data fit — no 16-example
set can decide a frontier it never touches. What the trial demonstrates with
discipline: a behavior acquired from examples (not planted) transfers across
that frontier while the shape-bound hardwired policy cannot.

## What the architecture did

PATH-A is a separate, fixed implementation for the familiar shape (2
candidates, 3 ANCHOR relations, SILENT/CORRECT channels). It matches PATH-T
exactly on TEST-FAMILIAR (24/24, byte-identical verdicts and consults). On
TEST-NOVEL its shape gate fires on 12 of 16 items and it takes the
documented safe fallback: WITHHOLD, consult 0. Its 4 hits are exactly the
four correct-withhold items (304, 308, 312, 316). Its 12 misses are all
withholds — **zero wrong installs**. The architecture fails safe; it just
doesn't generalize.

## Scope and residual boundaries (KB6)

- Correlated-wrong independent channels remain the known residual failure
  mode from R4C; this trial did not test them.
- The cost model is preregistered and reported, not a bar: PATH-T spends
  more ops on novel items (282 vs 128) because it consults and re-scores
  where PATH-A withholds.
- Distractors: D-RECALL 10000/10000 and D-COST 200/200 in every run —
  the trial machinery shows no drift on unrelated probes.
- This trial does not test invention (RSI-3/RSI-4 own that); it tests
  Micah's "trained behaviors, not architectures" bet on the combined
  conflict-resolution policy. On this bet, with this battery, the trained
  behavior won.

## Disclosures (timing honesty)

1. `verify_ac.py` was NOT in the prereg commit (ba139cbf). It was written
   and frozen with the instrument and battery BEFORE any official trial run;
   the 20 official logs in `runs/` were produced after it existed, and it
   verifies them mechanically. No log was edited after verification.
2. `AC_ITEMFIELDS` as emitted is a superset of the §6 log-line sketch: the
   frozen sketch omitted channel params, which KB5 ("fields match the CSV
   exactly") requires, so the implementation emits cp1..cp4 and per-relation
   fields explicitly. Content is unchanged, only field naming.
3. Two pre-run bugs were caught by smoke tests before any official run: the
   generator's item stride (overlapping writes, then a half-stride), fixed in
   `gen_battery_ac.py`; and a consult-flag semantic on silent channels for
   the ALWAYS rule, aligned to the R4C convention (an ask attempt counts even
   when the channel is silent). Neither affected the frozen design; both are
   recorded here.
4. `battery_ac.csv` (oracle, contains gt) is committed alongside the
   evidence; "oracle-only" means absent from the Zag binary (KB5a/KB5b),
   not secret from the lab repo.

## Evidence

- `runs/ac_{teacher,learn,pathT,pathA}_r{0..4}.log` — 20 official logs
- `SHA256SUMS` — hashes of sources, battery, oracle, verdict, and all logs
- Oracle: `python3 verify_ac.py` → 45/45 PASS, "ALL BARS PASS"
