# H-CAUSAL-UNIFIED7 independent red team report (CU7-ADV)

**Date:** 2026-09-30
**Adversary:** H-CAUSAL-UNIFIED7 Red Team (independent, depth-1 subagent)
**Target:** H-CAUSAL-UNIFIED7 builder result `b56ed4694`
("RESULT H-CAUSAL-UNIFIED7 SURVIVES (6/6). One-episode-one-vote
repair: EP_COUNTED retires carve winners from future tallies;
battery/main byte-identical to CU6; entrenchment fixture confirms
double-vote defect closed. Pure Zag.")
**Standing assumption:** the repair claim is false. The adversary
wins ties.
**Verdict: HOLD. All four attacks held. The adversary failed to
kill or downgrade H-CAUSAL-UNIFIED7.**

This is an adversary result pending parent verification, not a
canonical fact. The builder's SURVIVES claim is neither confirmed
nor overturned by this report; the red team simply could not break
it with the frozen attacks.

## 1. Methodology

The harness `cu7a_adv.zag` (md5
`c739185e63dababbc010c159565fbec4`) is lines 1..2501 of the
committed `unified_causal7.zag` at `b56ed4694` (the full mechanism
region; `fn main` begins at line 2503), byte-verified with `cmp`
against `git show`, plus an attack-only `fn main` and attack-only
helpers. Zero mechanism bytes altered. Pure Zag throughout; no
Python in prereg, harness, builds, runs, or analysis. Built with
the Linux `znc` binary shipped in the TNN repo
(`src/tools/toolchain/znc_linux_x86_64_abed8aa1`).

Fixture initialization matches the builder harness exactly:
zeroed workspace, `set32(W, ST_STR(), STR0())`, then
`intent_init(W)` (attack-only `adv_init`). This matters: the
builder's first causal episode creates causal entry 0, and all
hardcoded entry indexes in the fixtures are calibrated to that.

Vote accounting uses per-fixture shadow arrays: `sh[128]` (last
observed `ep_st`) and `winct[128]` (ACT-to-COUNTED transitions per
episode). After EVERY learned episode, `adv_audit` runs three
checks: (a) duplicate episode index inside any single entry list
(DUP); (b) transition scan, counting ACT-to-COUNTED per episode
(REVOTE if any episode reaches 2) and flagging COUNTED-to-ACT
(RESURRECT); (c) carve-winner purity: any entry created by the
learn whose parent is ST_CONFL must contain only episodes with
winct 0 before the learn (GHOSTWIN). `COUNTED->SUP` is allowed
(honest contest retirement).

The harness was run 3 times; all 3 stdout are byte-identical
(md5 `7f1da12caeff399e75d5cc7d72c3f3c6`), all exit 0.

## 2. X-CU7-1: double voting — HOLD

Frozen bar: KILL on any DUP, REVOTE, RESURRECT, or GHOSTWIN emit,
or any nonzero exit.

F1 (builder K-CU7-1 flood replay, 31 episodes, audited per
episode): fidelity confirmed (`nent=4`, `EP_COUNTED=8`,
`nct=8`, entry 3 list `[21,22,23,24,25,26,28]` with the first 6
counted and index 28 live). Zero audit failures across all 31
episodes.

F2 (split-heavy stream, 12 episodes across 4 state cells of
action 2 with divergent outcomes): `nent=7`, `nep=12`, `nct=4`.
Zero audit failures.

F3 (multi-action contest evolution, 14 episodes across actions
0, 1, 2 with contest opens at seq 3, 7, 12): `nent=3`,
`nep=14`, `nct=3`. Zero audit failures.

F4 (counted-supersede lifecycle; white-box setup of a 3-episode
tombstone, black-box evolution through `handle_caus_learn`):
2v2 tie correctly produced no carve; 3v2 carved with winners
exactly the 3 uncounted episodes (each counted once, winct 1)
and losers superseded; contest resolution moved counted winners
to SUP with votes staying at 1 (no resurrection); final
`fu_predict` confidently returned the surviving outcome
`(7,7,7)` with r=1. The negative control (single fresh
contradiction against counted winners) showed `live_contra_at=0`
(no hallucinated contradiction) with predict withholding via
the contested path (r=0). Zero audit failures.

Result: no DUP, no REVOTE, no RESURRECT, no GHOSTWIN in any
fixture. X-CU7-1 HOLDS.

## 3. X-CU7-2: tally correctness

### X-CU7-2(a): honest reversal — HOLD (after transparent amendment A1)

Frozen bar (as amended): KILL if any carve's winner set includes
a previously counted episode; if total counted is wrong; if the
fresh-winner carve's winners are not exactly the fresh episodes;
or on guard/predict disagreement.

Amendment A1 (2026-09-30, in PREREG_CU7_ADV.md): the frozen
fixture's hand-trace was arithmetically wrong. It predicted 4
fresh `(1,1,1)` would accumulate and carve as winners. In fact
entry 2's uncounted pool after F1 holds TWO `(0,0,0)` (indices
29, 30), so the first fresh `(1,1,1)` makes the tally 2v1 for
the OLD side, which correctly carves immediately. The amended
fixture tests the same kill intent in two phases.

Phase 1 (majority correctness): 1x fresh `(1,1,1)` carved the
old side 2v1. New entry 4 = exactly indices 29 and 30, both
`EP_COUNTED`, neither previously counted; fresh index 31
superseded as the loser; total counted 8 -> 10; entry 4 ACTIVE.
PASS.

Phase 2 (honest reversal): `(0,0,0)` absorbed into ACTIVE entry
4; `(1,1,1)` contradicted it and the contest cap marked entry 4
ST_CONFL; `(0,0,0)`, `(1,1,1)`, `(1,1,1)` absorbed into entry 2
(oldest tombstone) where the fresh side accumulated to 2v1 and
carved. New entry 5 = exactly indices 35 and 36 (both >= 31,
the fresh episodes), both `EP_COUNTED`; loser index 34
superseded; total counted 10 -> 12; guard live (`live_contra_at
= 1`) and predict withholds (r=0). PASS.

No ghost votes in either carve. The losers were superseded, not
resurrected. X-CU7-2(a) HOLDS.

### X-CU7-2(b): D1 fragmentation probe — HOLD (downgrade-only)

Frozen bar: DOWNGRADE only if `fu_predict` returns r=1 against
stranded uncounted evidence the routing never consulted.

(i) Append-frozen invariant: after X-CU7-2(a), entry 3
(younger tombstone, 7 episodes) was snapshotted, then 4 fresh
`(0,0,0)` were fed. Entry 3 stayed at 7 episodes with an
identical list; all 3 absorbs routed to entry 2 (oldest),
which grew 15 -> 18. HOLD.

(ii) Guard coverage: `fu_predict(2,0,0,2)` returned r=0
(withhold), never confident against the stranded evidence.
HOLD.

No downgrade trigger. The D1 residual (oldest-tombstone
routing stranding younger evidence) was tested but did not
produce a wrong prediction.

### X-CU7-2(c): guard sees counted winners — HOLD

Frozen bar: KILL on guard/predict disagreement.

On the F4 fixture, single fresh contradiction against counted
winners: `live_contra_at = 0` (correct: the fresh episode alone
is not a live contradiction of counted mass) and predict
withheld via the contested path (r=0). On the X-CU7-2(a) end
state, `live_contra_at = 1` with predict withholding (r=0).
No disagreement in either direction. X-CU7-2(c) HOLDS.

## 4. X-CU7-3: regression — HOLD

Frozen bar: KILL on any stdout md5 mismatch vs the frozen
builder hashes, any byte difference vs committed raw files, or
any CU6-to-CU7 diff hunk outside R1..R5.

Builder blobs extracted from `b56ed4694`, rebuilt with the
Linux znc, each run 3 times:
- adversary: `36f835f69f41f100675bc385394cf6c3` (3/3). MATCH.
- battery: `3bde55fe381a7c8ff1cef93d8c038da3` (3/3). MATCH.
- main: `87f8edc29825802327029f46f045dbe3` (3/3). MATCH.
Raw sources: `unified_causal7.zag` md5
`a91ffa107627c53850154e9c2b3de4d8`, byte-identical to the
committed blob. Custom harness mechanism region byte-identical
to committed lines 1..2501 (`cmp` clean).
CU6-to-CU7 diff: 23 changed lines total, all inside R1..R5
(R1 new `EP_COUNTED` state; R2 tally skips COUNTED; R3 carve
marks winners COUNTED; R4 `entry_eps` includes COUNTED; R5 no
other state checks changed). No fixture literals or harness
code in the mechanism. Diff-purity holds. X-CU7-3 HOLDS.

## 5. X-CU7-4: capacity exhaustion — HOLD

Frozen bar: KILL on nent > 32, missing ERROR emits, any
`ep_st` change across a refused carve, or silent loss.

(a) Entry cap: F1 replay, `new_entry` filled to `nent=32`.
(i) Fresh-state learn refused with the exact emit
`ERROR: entry capacity (32) exhausted; new_entry refused`,
nent stayed 32, no episode added. (ii) Adjudication-triggering
absorb at cap: `conflict_adjudicate` returned 0 with the same
ERROR, nent stayed 32, full `ep_st` snapshot before/after
identical (refused carve side-effect free), conflict state
preserved. PASS.

(b) Conflicted-entry list cap: F1 replay (entry 2 at 11
episodes), 53 single-outcome absorbs to `en_neps=64`, then the
65th refused with the exact emit
`ERROR: conflicted-entry episode list full (64); episode
refused`, neps stayed 64. Within the 128 episode cap
(31 + 54 = 85). PASS.

(c) Contest cap: after F1 (`nct=8`), contradiction at a fresh
state on an ACTIVE entry produced the exact emit
`ERROR: contest capacity (8) exhausted`, the entry marked
ST_CONFL, and `fu_predict` withholding there. PASS.

All three capacities are transactional: refusal leaves no
partial state. X-CU7-4 HOLDS.

## 6. Failures and corrections (disclosed)

(a) Invalid development run: the first custom harness run
(`CU7A_ADV_INVALID_DEV_RUN.txt`, exit 1, verdict KILL) is
VOID. It initialized fixtures with `fu_init`, which
pre-creates 4 default causal entries, instead of the builder's
zeroed-workspace-plus-`intent_init` fixture. Every downstream
index, count, and boundary was therefore off by construction.
No finding from that run is used. It is preserved only as a
disclosed harness-development failure.

(b) Prereg amendment A1: the frozen X-CU7-2(a) fixture's
hand-trace was wrong (see section 3). The amendment corrected
the trace without weakening the kill intent, was written into
PREREG_CU7_ADV.md before the corrected run, and is re-frozen.
The corrected fixture is strictly more demanding (two carves
verified instead of one).

(c) The adversary could not construct a fixture that makes the
fresh side win a carve on the FIRST fresh episode after F1,
because the old side's 2 uncounted votes correctly outvote any
single fresh episode 2v1. This is correct adjudication, not a
defect; the honest reversal was demonstrated with a 6-episode
sequence instead.

## 7. Boundaries (what was not tested)

- Only the committed Linux znc build path was used; no
  cross-platform check.
- Fixtures stay within the 128-episode cap; behavior at the
  episode cap under carve pressure was not probed.
- The merge/split paths (`merge_pass`, `split_attempt`) were
  exercised only incidentally via F2/F3, not adversarially
  targeted.
- X-CU7-2(b) tested the D1 routing residual only through
  prediction behavior, not through a constructed wrong-answer
  demonstration (none was found).
- Timing, memory use, and worst-case input scaling were not
  measured.

## 8. Causal interpretation

The repair under attack (R1..R5) retires carve winners from
future adjudication tallies via the new `EP_COUNTED` state
while keeping them live for the guard, routing, prediction,
and effects. The red team's best attacks on each sub-claim
failed:

- Vote accounting (X-CU7-1): across 71 audited episode learns
  spanning floods, splits, multi-action contests, and a full
  counted-to-superseded lifecycle, no episode voted twice, no
  retired vote returned, no entry listed an episode twice, and
  no carve winner had prior winner status.
- Tally correctness (X-CU7-2): majorities were honored in
  both directions (old side 2v1, fresh side 2v1); winner sets
  were exactly the entitled episodes; the guard and predictor
  agreed in both the live-contradiction and no-contradiction
  configurations.
- Regression (X-CU7-3): the committed artifacts reproduce
  byte-identically and the source diff is minimal and pure.
- Capacity (X-CU7-4): all three exhaustion boundaries refuse
  transactionally with explicit emits and no partial state.

The one-episode-one-vote invariant survived every attack the
frozen prereg specified. The D1 routing residual (oldest-
tombstone absorbs stranding younger evidence) remains a
documented structural property but did not produce a wrong
prediction in any probe.

## 9. Governance disclosures

- Prereg `PREREG_CU7_ADV.md` was committed alone
  (`1a50a3f5ebbf9822a83ab27d85d0eb2e84b5c36f`) before any
  attack code, build, or run. Amendment A1 was added
  transparently and re-frozen before the corrected run; no
  kill bar was weakened to force a pass.
- Pure Zag throughout: no Python in prereg, harness, builds,
  runs, or analysis. Shell only for file operations;
  `cmp`/`md5sum` for byte checks.
- Only the owned path
  `docs/lab/research-lead/overnight-20260928/cu7_adversary/`
  is staged. No binaries committed.
- Commits are local; no push authorized.
- This document contains no em dashes.
- Findings are adversary results pending parent verification,
  not canonical facts.

## 10. Commit lineage

- Builder result: `b56ed4694` (2026-09-30 00:22:50 UTC),
  "RESULT H-CAUSAL-UNIFIED7 SURVIVES (6/6)...".
- Adversary prereg frozen: `1a50a3f5ebbf9822a83ab27d85d0eb2e84b5c36f`.
- This report, harness, and evidence: committed locally on
  branch `tnn-native-lab` under
  `docs/lab/research-lead/overnight-20260928/cu7_adversary/`.

## 11. Files in this directory

- `PREREG_CU7_ADV.md`: frozen preregistration plus
  transparent amendment A1.
- `cu7a_adv.zag`: full adversary harness (mechanism region
  byte-identical to committed lines 1..2501 plus attack-only
  main).
- `CU7A_ADV_RAW_1/2/3.txt`: three byte-identical valid runs
  (md5 `7f1da12caeff399e75d5cc7d72c3f3c6`, exit 0,
  `CU7-ADV VERDICT: HOLD (all attacks held)`).
- `CU7A_ADV_INVALID_DEV_RUN.txt`: the void development run
  (wrong initializer), preserved as a disclosed failure.
- `X3_BUILDER_ADV_RAW.txt`, `X3_BUILDER_TEST_RAW.txt`,
  `X3_BUILDER_MAIN_RAW.txt`: independent builder-blob
  reproduction outputs matching frozen hashes.
- `HASHES.md`: hash and lineage evidence.
- `REPORT_CU7_ADV.md`: this report.
