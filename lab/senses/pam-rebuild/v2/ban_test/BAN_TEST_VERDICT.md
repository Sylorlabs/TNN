# BAN-TEST VERDICT: pointwise-revision ban — FOLLOW-UP ITEM 2

**Date:** 2026-09-23 | **Branch:** `tnn-native-lab` (sylorlabs/TNN)
**Prereg:** `senses/pam-rebuild/v2/ban_test/PREREG_BAN_TEST.md` (commit
`5e31d282`, committed alone before execution)
**Program order:** Micah — TEST FIRST on the proposed pointwise-revision ban.

## Verdict: MODIFY — adopt the ban as a two-tier rule (exact wording §5)

The ban on pointwise revision of the live claim is **necessary** (variant A
false-installs on the frozen stream and on all 12 adversarial traps), but the
synthesis's implied bar — historical corroboration as a single corroborating
pair (variant B, cf1 shape) — is **insufficient**: correlated wrong percepts
defeat it 6/6. Only the sequential protocol (variant C) passes the full
kill-bar battery. The adopted ban is therefore modified: B-tier corroborated
**provisional** admission (recovery) + C-tier **sequential promotion** for
live-claim revision (safety). An exploratory two-tier composition (variant 4,
not preregistered) confirms the composition: 0 false installs, RK-3 65.8%,
live-claim changes 17/17 correct.

## 1. Head-to-head numbers (frozen R2-4 stream, 11,840 trials)

| variant | false installs (KILL) | wrong prov. adm. | recovered correct (PRIMARY) | RK-1 | RK-2 | RK-3 |
|---|---|---|---|---|---|---|
| 0 frozen | 0 | 0 | 0 | 0 | 0/1109 | 104/1102 (9.4%) |
| A pointwise | **1** (seq 1145) | 0 | 267 | 1 (0.0001) | 1/1109 | 725/1102 (65.8%) |
| B corroborated pair | 0 | 1 (seq 1145) | 242 | 0 | 0/1109 | 725/1102 (65.8%) |
| C sequential | 0 | 0 | 80 | 0 | 0/1109 | 323/1102 (29.3%) |
| V4 two-tier (explor.) | 0 | 1 (seq 1145) | 482 | 0 | 0/1109 | 725/1102 (65.8%) |

Disposition notes: A emitted 268 `REVISED_INSTALL` (1 wrong: seq 1145,
`revised_old=721`). B: 63 `REVISED_INSTALL` + 180 `CHALLENGER_PROV` (all
correct; the 1 wrong admission is 1145 provisional only). C: 3
`REVISED_INSTALL` + 14 `RESTORED_INSTALL` (all 17 correct — the rollback
chain reversibly tracks pitchdisc's oscillating truth) + 63 `CHALLENGER_PROV`
pairs; 403 isolated singletons `WITHHELD/challenge_isolated` (no install).
V4: C's dispositions with isolated singletons admitted as `CHALLENGER_PROV`;
live-claim changes identical to C (3+14, all correct).

## 2. Adversarial traps (kill-bar false installs per variant; 6 tasks each)

| trap class | v0 | A | B | C | V4 (explor.) |
|---|---|---|---|---|---|
| T1 1145-class singleton dominator (6) | 0 | **6** | 0 | 0 | 0 |
| T2 correlated-corroborator pair (6) | 0 | **6** | **6** | 0 | 0 |
| T3 ceiling probe (2; declared NON-KILL) | 0 | 2 | 2 | 2 | 2 |

- A false-installs on every T1 and T2 instance: a single wrong trial, however
  dominant, must never revise the live claim. Ban necessity confirmed on
  synthetic ground as well as frozen evidence.
- B survives T1 (singleton → `CHALLENGER_PROV` only) but false-installs on
  every T2 instance (2nd wrong corroborator → `REVISED_INSTALL`). A
  corroborating pair is not a safe revision bar against correlated failures.
- C passes T1+T2 fully (singletons withheld, pairs provisional only).
- T3 (declared ceiling probe): every finite bar falls to an (N+1)-corroborator
  trap by construction — A, B, C, and V4 all revise wrong on the wrong triple
  (2/2 instances). C and V4 then `RESTORED_INSTALL` on the correct triple
  (2/2): the rollback works, bounding the damage of a breached bar.

## 3. Decision-procedure walkthrough (per frozen §5)

1. **Kill bar** (>0 false installs on frozen ∪ T1 ∪ T2 → FAIL):
   A FAILS (1 + 6 + 6). B FAILS (0 + 0 + 6). C PASSES (0 + 0 + 0).
2. **Ban necessity:** A fails while B/C pass on the frozen stream → the
   trial-1145 rule is empirically confirmed. Pointwise revision is unsafe.
3. **Verdict:** A fails, B fails T2, C passes → **MODIFY**: the ban holds, but
   the live-claim revision bar must be sequential; the verdict gives the exact
   two-tier wording (B-tier provisional admission + C-tier sequential
   promotion). (Not ADOPT-as-specified: B's pair bar, the synthesis's implied
   form of "historical corroboration," is defeated 6/6. Not REJECT: A fails
   everywhere it was tested.)

## 4. Why two tiers (not pure C)

Pure C pays for its safety with recovery: 403 isolated conflicting high-conf
percepts are withheld entirely (RK-3 29.3% vs B's 65.8%). But C's strictness
is only load-bearing for the **live claim** — provisional admission never
changes it. The exploratory two-tier (V4: C's promotion rule, B's admission
rule) keeps C's live-claim safety exactly (identical revision/rollback logic;
0 false installs on frozen+T1+T2; same 17 correct live-claim changes) while
recovering B's admission coverage (RK-3 725/1102; 482 conflict-moment correct
installs). The 1145-class wrong singleton becomes a contained provisional
admission, never the live claim. V4 is exploratory (not preregistered); the
adopted wording below should get its own preregistered confirmatory trial
before freezing into a v2 gate.

## 5. Adopted ban wording (MODIFIED trial-1145 rule)

> **Live-claim revision ban (trial-1145 rule, adopted as modified 2026-09-23):**
>
> 1. **Pointwise revision is banned.** No v2 gate may replace a live permanent
>    claim, or grant permanent status to its challenger, on the evidence of a
>    single trial — no matter how strongly that trial dominates the incumbent
>    on confidence, margin, or self-check flags. (Trial 1145 was wrong yet
>    dominant on every axis: conf 874, mrgF 10410, strong=1, agree=1; variant
>    A installed it.)
> 2. **A single corroborating pair is insufficient for live-claim revision.**
>    Two percepts corroborating each other within tolerance can both be wrong
>    (variant B false-installed on 6/6 correlated-corroborator traps).
> 3. **Live-claim revision requires a corroborated sequence:** ≥3
>    same-judgment high-confidence (conf ≥ 700) PASSes within the task
>    tolerance, inside a 100-trial window, spanning ≥3 trials, with challenger
>    evidence margin ≥ the task T3 bar (frozen `deliberate.zag` `thr_of`).
>    Every revision preserves the replaced claim (depth-1 stack); a later
>    qualifying sequence for the preserved judgment restores it
>    (`RESTORED_INSTALL`) — revisions are reversible, never destructive.
> 4. **Provisional admission is not revision.** Conflicting high-confidence
>    percepts below the revision bar are admitted PROVISIONALLY ONLY
>    (challenger slot: `CHALLENGER_PROV`; reversible; never the live claim).
>    Corroborated admission (a second same-jcode high-conf PASS within
>    tolerance) is the admission tier; it recovers truths without risking the
>    live claim.

## 6. Mechanism, determinism, and commits

- Mechanism: `src/bantest.zag` (pure Zag, integer math, zero RNG) replays the
  frozen gate with variant conflict rules; `glue/build_stream.py`,
  `glue/trapgen.py` (deterministic, no RNG), `glue/score.py`,
  `glue/run_all.sh`.
- Fidelity: variant 0 reproduces `gate_dispositions.txt` **0/11,840
  mismatches**; scorer cross-checks RK-1=0, RK-2=0/1109, RK-3=104/1102.
- Determinism: 4 preregistered variants × 15 streams × 3 runs = 180 runs,
  grouped into 60 (stream, variant) triples — **all byte-identical**
  (digests in `evidence/runs/digests.csv`). V4 exploratory runs are separate
  and labeled.
- Stream digest (sha256): `8b8236e7efbd6017…` (`evidence/stream.txt`,
  11,840 rows, no truth column — gate cannot see truth).
- Commits (branch `tnn-native-lab`, via `~/workspace/commit_racefree.py`):
  - `5e31d282` — PREREG_BAN_TEST.md alone (frozen before execution)
  - `e7af4ff9` — code + glue + stream + traps + run outputs (111 files)
  - `308fa2a1` — this verdict

## 7. Honest limits

- The frozen stream holds exactly ONE wrong conflicting high-conf PASS (seq
  1145); B/C/V4's 0 false installs there is evidence-contingent — the T1/T2
  battery is the adversarial complement, and it is synthetic.
- C's W=100/D=3/T3 parameters were set with exploratory access to the frozen
  stream; only the trap battery is out-of-sample.
- A finite corroboration bar is an economic guarantee, not a logical one: T3
  shows an (N+1)-corroborator trap defeating a K=N bar by construction, for
  every variant. The rollback bounds the damage; it does not prevent the
  breach.
- The two-tier composition (V4) is exploratory — tested, but not preregistered.
  Confirm with a preregistered trial before freezing into a v2 gate.
- Scope: this trial tests the REVISION rule only. The 278 never-PASS trials
  (program false negatives) and the RK-3 85% spec tension are untouched —
  no gate rule reaches them (§2.4 of AUTOPSY_R2-4.md stands).

## 8. Recommended follow-ups

1. Preregistered confirmatory trial of the two-tier wording (§5) as a v2 gate
   candidate (V4's logic, frozen).
2. Adversarial pressure on the rollback: longer wrong-sequence attacks that
   try to exhaust the depth-1 stack (chained false revisions).
3. The margin bar (T3) is doing untested work on the frozen stream — ablate
   it (K=3 without margin) to price its contribution.
4. Program-side (f) work on the 278 never-PASS trials remains the only route
   past the 74.8% gate-side ceiling.
