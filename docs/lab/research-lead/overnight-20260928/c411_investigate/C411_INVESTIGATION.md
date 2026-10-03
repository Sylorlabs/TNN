# C411 INVESTIGATION: ledger data-loss incident (eaf6d7ba1 / d238f75ca)

**Worker:** C411-INVESTIGATE (analysis only; CLAIM_LEDGER.md not modified; claim minting paused)
**Date:** 2026-10-03
**Repo:** ~/workspace/tnn-rsi (branch examined: tnn-native-lab line; worktree on lane-ma4b-20261003)
**File:** docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md
**Toolchain note:** shell/git/grep only; no forbidden executables invoked.

## 1. Verdict

C411 (LIFETIME-META-2, META-LEARNING DEMONSTRATED) was **never written to CLAIM_LEDGER.md in any commit**. The faulty WATCHDOG commit `eaf6d7ba1` (2026-10-03 08:06:46 UTC) was supposed to mint it but instead **deleted 128 lines (C377-C408), 0 insertions**. The restore `d238f75ca` (2026-10-03 08:08:09 UTC) re-added **exactly** those 128 deleted lines (verified byte-identical inverse), returning the ledger to its pre-deletion state. C411 is absent after the restore **not because the restore dropped it, but because the faulty commit never wrote it**: there was nothing for the restore to recover. The LEDGER-RESTORE-CHECK observation ("C411 also absent") is correct as a state description; the mechanism is mint-failure, not restore-failure.

**C411 is fully reconstructible.** Its minted detail survives in the faulty commit's subject line, a staged admission entry already exists in `cbe2e5607` (STAGING ONLY, never appended, awaiting parent approval), and the complete experiment evidence (PREREG.md, REPORT.md, lm2.zag, frozen binary, 3/3 byte-identical run outputs) survives in commit `b5b4e003e`.

## 2. Incident timeline (tnn-native-lab line)

| Time (UTC 2026-10-03) | Commit | What it did |
|---|---|---|
| 08:06:34 | `b5b4e003e` LIFETIME-META-2 LM1b | Experiment committed: lane `lifetime_meta2/` (PREREG.md, REPORT.md, lm2.zag, lm2_bin, run1/2/3.txt). Full evidence preserved. |
| 08:06:46 | `eaf6d7ba1` WATCHDOG: ledger C411 | **Faulty mint.** Subject carries the C411 claim summary, but the diff is 128 deletions / 0 insertions: it deleted the C377-C408 tail block instead of appending the C411 entry. |
| 08:08:05 | `9bb51ff39` WATCHDOG: ledger C412 | Empty commit (no file changes at all). C412's mint also wrote nothing to the ledger. |
| 08:08:09 | `d238f75ca` WATCHDOG: restore | Restored the 128 deleted lines exactly (C377-C408). Ledger returned to the `ff8a2d8df` state. C411 still absent. |

Graph: `b5b4e003e` < `ff8a2d8df` < `eaf6d7ba1` < `9bb51ff39` < `d238f75ca` (linear on this line; all "Local only, never pushed").

## 3. Task verification results

### 3a. `git show eaf6d7ba1 --stat`: 128 deletions CONFIRMED

```
commit eaf6d7ba191cfbd2274b94286d973cc5f4e4c553
    WATCHDOG: ledger C411 (LIFETIME-META-2 META-LEARNING DEMONSTRATED:
    B5a ADV_C=672>=350, all 13 bars PASS, ~75 examples saved per typical
    episode; honest L1/L2-ish empirical-Bayes; 3/3 byte-identical).
    Local only, never pushed.

 .../canonical_ledger/CLAIM_LEDGER.md | 128 ---------------------
 1 file changed, 128 deletions(-)
```

128 deletions, **0 insertions**. The intended C411 entry was never written; the commit only deleted.

### 3b. Exactly what was deleted: C377-C408 (32 claims, 4 lines each)

Extracted all 32 deleted entry headers from the diff; they are exactly C377 through C408, each a 4-line block (blank / `- Cnnn (...)` / blank / `No em dashes were used in this entry (verified).`). 32 x 4 = 128 lines. **No C411 entry appears among the deleted lines** (the single "C411" string in the `git show` output is the commit subject line itself, not a ledger line).

### 3c. `git show d238f75ca --stat`: restore re-added exactly the deleted lines

```
commit d238f75caa4920d3e16eb85909ed716b58840902
    WATCHDOG: restore C377-C408 deleted by eaf6d7ba (third faulty WATCHDOG
    ledger commit, 128 lines deleted). Ledger restored to ff8a2d8df state.
    Local only, never pushed.

 .../canonical_ledger/CLAIM_LEDGER.md | 128 +++++++++++++++++++++
 1 file changed, 128 insertions(+)
```

Verification: extracted the 128 deleted lines from `eaf6d7ba1` and the 128 added lines from `d238f75ca`; after stripping diff markers the two sets are **identical** (`diff` empty). Blob index returns from `427035b90` to `8060efbc8`, i.e. byte-identical to the pre-deletion (`ff8a2d8df`) state.

Precision note on the task phrasing "its restore d238f75ca dropped C411 entirely": the restore is a faithful inverse of the deletion. C411 was absent from the restore source (`ff8a2d8df`) because the faulty commit never minted it. The loss happened at mint time (0 insertions), not at restore time.

### 3d. C411 never entered the ledger in any commit

`git log --all --oneline -S "C411" -- <CLAIM_LEDGER.md path>` returns **no commits**: no commit in any branch ever added or removed the string "C411" in the ledger file. Current ledger (worktree branch and `tnn-native-lab` tip) contains `0` occurrences of a C411 entry; both end at C410.

## 4. What C411 was

C411 is the ledger claim for the **LIFETIME-META-2** experiment ("Does examples-to-criterion decrease with experience?"), minted by the WATCHDOG series. Four surviving sources describe it, in increasing detail:

**(a) Authoritative minted detail: the faulty commit's subject line.**
`eaf6d7ba1`: "LIFETIME-META-2 META-LEARNING DEMONSTRATED: B5a ADV_C=672>=350, all 13 bars PASS, ~75 examples saved per typical episode; honest L1/L2-ish empirical-Bayes; 3/3 byte-identical"

**(b) Staged admission entry** in `cbe2e5607` (`ledger_write/STAGED_LEDGER_ENTRIES.md`, STAGING ONLY, CLAIM_LEDGER.md untouched, awaiting parent approval):
`- C411 (LIFETIME-META-2; watchdog commit eaf6d7ba1, 2026-10-03 08:06:46 UTC): META-LEARNING DEMONSTRATED. Verdict: META-LEARNING DEMONSTRATED (all 13 bars PASS). B5a ADV_C=672>=350, all 13 bars PASS, ~75 examples saved per typical episode; honest L1/L2-ish empirical-Bayes; 3/3 byte-identical. Status: ADMITTED (watchdog series claim; detail as minted in commit subject).`

**(c) LEDGER-RECONCILE classification** (`92e42ea2d`, C457): C411 is one of "43 clean watchdog-only claims C411-C454" proposed for admission with caveats (canonical priority to existing C404-C410; C417 excluded as probable duplicate). Proposal is staged, not executed; minting paused.

**(d) Full experiment evidence** in `b5b4e003e` (`lifetime_meta2/`): PREREG.md (232 lines), REPORT.md (127 lines), lm2.zag (322 lines), lm2_bin (frozen binary), run1.txt/run2.txt/run3.txt (3/3 byte-identical, sha256 `1a68561a44809c804bc8d7c1775d68595cf220d4abc0fe87feea1f40d5b0bcba`).

## 5. Reconstruction

C411 **can be reconstructed in full**. The experiment record is complete; only the 4-line ledger entry text was never written. Two reconstruction artifacts are available:

### 5a. Already staged (by LEDGER-WRITE worker, commit cbe2e5607)

The exact append text in `ledger_write/STAGED_LEDGER_ENTRIES.md` (see 4b above), followed by the standard `No em dashes were used in this entry (verified).` trailer. This is the prepared canonical admission text. **It has not been appended; claim minting is paused pending parent approval.**

### 5b. Full-detail source record (from b5b4e003e:REPORT.md)

For the parent's reference when minting resumes, the complete finding behind C411:

- **Experiment:** LIFETIME-META-2, "Does examples-to-criterion decrease with experience?" Lane `lifetime_meta2/`, impl commit `b5b4e003e` (2026-10-03). Pure Zag, pinned znc, safebin-only (python3/python/perl/ruby/node unresolvable; zero forbidden invocations). Commit order honored (prereg before implementation).
- **Design:** 12 episodes of biased-coin bias learning; hidden bias p* per episode; 9 typical biases (76..84) + 3 atypical (40, 47, 54); N=1200 flips/episode/condition from INDEPENDENT streams; estimator est_n = (20*m + 100*h)/(20+n) with treatment m = floor(mean of past revealed biases), control m = 50; criterion |est_n - p*| < 5.
- **Frozen verdict: META-LEARNING DEMONSTRATED (cluster episodes).** B5a (primary, cluster-only advantage) PASSED at 672 >= 350 (1.92x the bar); all 13 bars PASS (B1 commit-order, B2 toolchain, B3 determinism, B4 novelty, B5a cluster-advantage, B5b decrease, B5c stability, B5d floor-validity, B5e stream-validity, B5f apparatus, B5g negative-transfer, B6 no-researcher-meta-rule, B7 opaque-ids). Nothing weakened or reinterpreted. 3/3 runs byte-identical.
- **Effect size:** persistent learner saved 672 examples over 9 typical episodes (~75/episode, ~37% of the naive ~88/episode control mean); examples-to-criterion fell from 63 (naive) to a late-typical mean of 3.3. Causally attributable to persistence (only treatment/control difference is the accumulated prior).
- **Honest boundary (stated in REPORT.md):** what was learned is the prior MEAN over biases: empirical-Bayes base-rate learning (L1/L2-ish). Not strategy invention, not L3. Estimator form, w=20, initial m=50 are researcher-supplied; the learned quantity is m. Negative transfer on atypical episodes (B5g: -86, sign as predicted) is part of the signature, not a defect. One frozen task distribution, one frozen seed triple; generalization untested.

A canonical-style full entry consistent with neighboring entries would read (PROPOSED, NOT MINTED):

```
- C411 (LIFETIME-META-2; lane lifetime_meta2/, impl b5b4e003e, 2026-10-03): META-LEARNING DEMONSTRATED (cluster episodes). Frozen verdict per prereg mapping: B5a cluster-advantage PASS (ADV_C=672>=350, 1.92x bar) with B5d floor PASS. All 13 bars PASS, nothing weakened. Persistent learner saved ~75 examples per typical episode (672 over 9 typical episodes, ~37% of naive control mean); examples-to-criterion fell 63 naive to late-typical mean 3.3. 3/3 byte-identical runs (sha256 1a68561a...5b0bcba). Honest L1/L2-ish empirical-Bayes prior-mean learning; not L3 (estimator form, w=20, m0=50 researcher-supplied; learned quantity is m). Negative transfer on atypical episodes (B5g -86, sign as predicted) is signature, not defect. Pure Zag, pinned znc, safebin-only. Status: COMPLETE.

No em dashes were used in this entry (verified).
```

## 6. What was lost vs what survives

| Item | Status |
|---|---|
| C411 ledger entry text (the 4-line block) | **Lost**: never written to any commit; survives only as the commit subject summary. |
| C411 claim detail | **Survives**: commit subject (authoritative minted detail) + staged entry in `cbe2e5607` + full REPORT.md in `b5b4e003e`. |
| LIFETIME-META-2 experiment evidence | **Survives intact**: `b5b4e003e` holds PREREG.md, REPORT.md, lm2.zag, lm2_bin, run1-3.txt (on `tnn-native-lab`; not in current worktree checkout). |
| Prereg commit `77b1a98` (cited in REPORT.md) | **Not found** in this repo's object store; its content survives as PREREG.md inside `b5b4e003e`. |
| C377-C408 ledger entries | **Fully recovered** by `d238f75ca` (byte-identical inverse verified). |
| Ledger state after incident | Ends at C410; C411 absent on all branches checked. |

## 7. Pattern context (for the parent)

This was not an isolated glitch. The restore message calls `eaf6d7ba1` the "**third** faulty WATCHDOG ledger commit", and `8f4882eb1` (LEDGER-RESTORE RESTORE_PLAN.md) documents a **fourth identical failure**: `f20dddf0b` ("WATCHDOG: ledger C415", 2026-10-03 08:12:23 UTC) deleted 136 lines (C377-C410), 0 insertions. The recurring defect: the WATCHDOG ledger-mint step intermittently **deletes the ledger tail block instead of appending the new entry**, while the commit subject correctly carries the new claim's summary. Additionally, `9bb51ff39` ("WATCHDOG: ledger C412") is an **empty commit** (no file changes), so C412's mint also wrote nothing. The minting pipeline, not the restore pipeline, is the faulty component; minting is currently paused, which is the correct posture until the mint script is fixed and the staged entries (C411-C460 in `cbe2e5607`, with the post-proposal numbering collision documented there) are resolved by the parent.

## 8. Recommended follow-ups (parent decisions; not taken by this worker)

1. **Approve or amend the staged C411 entry** in `cbe2e5607` (`ledger_write/STAGED_LEDGER_ENTRIES.md`) when minting resumes; the full-detail record in section 5b is available to enrich it.
2. **Fix the WATCHDOG mint script** that deletes instead of appending (4 identical failures in one morning); consider a pre-commit guard asserting insertions > 0 on ledger-mint commits.
3. **Resolve the numbering collision** documented in the staged file header (watchdog minted C455/C456/C457 after the reconcile cutoff using numbers the proposal assigns to displaced claims).
4. **Decide the fate of C412** (`9bb51ff39`, empty commit): its claim text exists only in the subject, same as C411's original situation.
5. This worker modified nothing; no ledger changes were made or are proposed to be made by this report alone.
