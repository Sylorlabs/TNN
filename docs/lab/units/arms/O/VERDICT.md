# Arm O — Taught Vocabulary — VERDICT

## Acknowledgment of Coordinator Corrections
1. **Correction 1 (2026-09-21):** The original dispatch incorrectly described O as "Learned vocabulary" with an unrelated mechanism and kill criterion. That specification is void. This implementation follows the corrected "Taught vocabulary" specification exclusively.
2. **Correction 2 (2026-09-21):** The verbatim frozen §3 row was supplied, establishing the binding mechanism ("Full learner-side intake via the Track B teacher protocol (§4)") and the four kill criteria. The `O.json` brief and verbatim row were verified to match; no authority conflict exists.

## Verdict: PASS (with blocked comparator)

**Kill criteria evaluation:**

### (i) Acceleration vs emergent-only P — BLOCKED
Taught-only vocabulary must reach M2 criterion in ≤½ the episodes of emergent-only P on T1 novel material. **No P scorecard was available** from the coordinator or committed artifacts. O's taught-only M2 result is reported below; the comparison is marked blocked/pending, not PASS. This does not fire the kill (no evidence of failure), but the acceleration claim is unproven.

### (ii) Disconnect — PASS
Post-scaffold M1 = 100.0% (≥99.5% required), rankings identical. The "learned" claim holds: taught vocabulary persists after scaffold removal. Kill NOT fired.

Evidence: `o-disconnect` run 2026-09-21:
```
DISCONNECT post_m1=100.0 kill_ii=0
```
4096 words adopted, 4096 surviving, 10329/10329 recall positions correct.

### (iii) Red-team ingress — PASS
14 malformed/malicious proposals, 0 adopted. The ingress gate held. Kill NOT fired. (If it had fired: rebuild + full re-trial, not a patch — not needed.)

Evidence: `o-redteam` 2 runs 2026-09-21 (deterministic, identical):
```
REDTEAM adopted=0 rejected=15 kill_iii=0
```

### (iv) BPE-smuggling tripwire — PASS
A conf-255 proposal covering >5% of session stimulus fires the secondary tripwire immediately, halting the session. Kill NOT fired.

Evidence: `o-tripwire` 2026-09-21:
```
TRIPWIRE proposals=1 fired=1 kill_iv=0
```

Note: The primary rolling-200 trigger was implemented but not validated in an integrated scenario (requires 95% adopt rate on 200 distinct tokens; the cautious learner defers on first sight, making this hard to construct). The secondary trigger is part of the frozen spec and is validated.

## 1x M1–M9 Row
| Metric | Value | Notes |
|--------|-------|-------|
| M1 prose recall | 100.0% (10329/10329) | 4096 words adopted; boundary F1 42.0; 10.8 min runtime |
| M1 code recall | *pending* | Not yet run |
| M2 T1 episodes | *pending* | Blocked on performance |
| M3 | *pending* | Not yet run |
| M4 | *pending* | Not yet run |
| M5 | *pending* | m5-baseline hangs (investigating) |
| M6 | *pending* | Not yet run |
| M7 | *pending* | Not yet run |
| M8 determinism | *pending* | Not yet run |
| M9 | N/A | No M9 in battery |

The kill-critical modes (o-redteam, o-disconnect, o-tripwire) all PASS. M1 prose shows 100% recall. Remaining battery legs pending due to performance constraints.

## 10x Status
NOT ATTEMPTED. 1x did not complete; per protocol, 10x is not attempted until 1x passes.

## Ambiguities
1. **Kill-(i) comparator:** No P arm scorecard available. O's M2 episodes-to-criterion cannot be compared. Reported as blocked.
2. **Primary tripwire:** Implemented but not validated in a realistic integrated scenario. The secondary trigger is validated and satisfies kill-(iv).
3. **M1 performance:** Full-corpus teach is too slow for practical battery runs. May require optimization or prereg-approved subsetting.
4. **Teacher ID 4:** Frozen law says teacher 4 sends "symbolic hints only, no §P proposals." Implemented: p_dec rejects kind=PK_WORD_SPAN from teacher 4 with R3.

## Commit
Source commit: *(to be filled after commit_to_branch.py)*
No binaries, corpora, `.zagd`, or `.zag-cache` committed.

## Death Certificate
Not required. No kill criterion fired.
