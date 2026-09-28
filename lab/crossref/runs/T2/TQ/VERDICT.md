# T2-TQ VERDICT — TQ series replication (Type A)

**Crew:** T2-TQ (replacement crew; predecessor killed by daemon restart)
**Date:** 2026-09-23 PDT · **Frozen prereg commit:** `7b2100d09911c5c10252c5756c7def288e70bd1f` (tnn-native-lab)
**Run dir:** `~/workspace/scratch-crossref/T2/TQ/crew/`

## Frozen prereg section (quoted verbatim — authoritative)

From `docs/lab/crossref/PREREG_TIER2.md` at the frozen commit, §"T2-TQ":

> ## T2-TQ — TQ series: no knee on teacher noise; self-contradiction caught (Type A)
>
> **Claims:** TQ-CONFLICT done+committed (`107f6ca1`): 17/17 self-contradictions REJECTed at R1; end-state digest identical to Q1B. TQ-NOISY50/N25/PARTIAL committed; TQ-NOISY10 run1 complete (verdict pending — excluded). Finding: no knee on teacher noise — falsehood absorbs linearly (49/49 at 25%, 99/99 at 50%); §B.7 blind to value noise; self-contradiction caught by eliminative verification.
> **Method:** rerun TQ-CONFLICT and the committed TQ-NOISY legs from committed sources in clean checkout; ≥3 byte-identical.
> **Rule:** REPRODUCED if 17/17 REJECTed, digest identical to Q1B, and noisy legs show linear absorption with no knee; NOT REPRODUCED if a knee appears or any self-contradiction installs.

## Frozen pins

| Pin | Value | Status |
|---|---|---|
| Prereg commit | `7b2100d09911c5c10252c5756c7def288e70bd1f` | verified as object in clean clone |
| TQ-CONFLICT `107f6ca1` | `107f6ca108fbe9a6bf30a8c22dd168b798a8f791` ("Q1C teacher self-contradiction leg: PASS — 17/17 false assertions killed (R1), 0 withheld, learner end-state byte-identical to Q1B") | PRESENT — no STOP |
| Toolchain | `znc_linux_x86_64_abed8aa1`, sha256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` | pinned |

## What was rerun (all from the frozen commit's object store, byte-verified)

- Q1B control (`docs/lab/q1b-teacher-bakeoff/`, `q1b_driver.zag`) — no-drift check + digest anchor
- TQ-CONFLICT (`docs/lab/q1c-teacher-conflict/`, `q1c_driver.zag`)
- TQ-NOISY25 (`docs/lab/tq-noisy25/`, `tqn_driver.zag`)
- TQ-NOISY50 (`docs/lab/q1tq-noisy50/`, `q1tq_driver.zag`)
- TQ-NOISY10 **excluded per prereg** (present in tree, not run)

Each rebuilt from source with the pinned znc; each run **N=5**, all runs rc=0.

## Claim vs measured

| # | Frozen claim | Measured | Match |
|---|---|---|---|
| 1 | TQ-CONFLICT: 17/17 self-contradictions REJECTed at R1 | 17 `Q1C_P2` lines, all verdict=3 (`TB_V_REJECT`) / reason=1 (`TB_R1_INSUFFICIENT`); summary `Q1C_PASS2,conflicted,17,0,183,0,0` (0 other verdicts); 183 true re-assertions R5-redundant | ✅ |
| 2 | TQ-CONFLICT end-state digest identical to Q1B | Q1C learner digest `6317c2dcf17e850c6e1419f547a8723efdeeda3a9747baf5f8af019ba3092467` == independently rerun Q1B learned-leg learner digest `6317c2dcf17e850c6e1419f547a8723efdeeda3a9747baf5f8af019ba3092467`; teacher digest `6f387ee3…07c3dee756b5` == Q1B's (unmodified) | ✅ |
| 3 | No knee: 49/49 absorbed at 25% | `TQN_ABSORB,49,0,49,143,0` → 49 absorbed, 0 filtered, 49 taught-false | ✅ |
| 4 | No knee: 99/99 absorbed at 50% | `Q1TQ_ABSORB,noisy50,99,0,19` → 99 absorbed, 0 filtered, 19 untaught | ✅ |
| 5 | Absorption linear through origin, no filtering regime | 0%→0/0, 25%→49/49, 50%→99/99 absorbed; filtered=0 at every level | ✅ |
| 6 | §B.7 blind to value noise | Flaw battery 96/96 (12/12 × 8 slices, 0 tripwire) at 0%, 25%, AND 50% noise while true mastery falls 192→143→93/192 | ✅ |
| 7 | ≥3 byte-identical runs | N=5 byte-identical on all 4 legs; stdout SHA-256 matches committed `evidence/n5_sha256.txt` exactly for all 4; run1 stdout byte-identical (`cmp`) to committed `evidence/run1_stdout.txt` for all 4 | ✅ |
| 8 | Control: no tree drift | Q1B rerun stdout `407974c35c68b5e2a234d3d17bfdf1847201ba3f47811af6fa8e07222190d151` ×5 = Q1B canonical | ✅ |
| 9 | Zero RNG | Static token scan clean on all new decision-path files; 5/5 byte-identical empirical determinism on all legs | ✅ |
| 10 | Self-contradiction caught by eliminative verification | 0 withheld, 17/17 commit-true, `Q1C_UNCONFLICTED_MASTERY,conflicted,183,183`; unconflicted mastery untouched | ✅ |

Canonical hashes reproduced:
- q1b: `407974c35c68b5e2a234d3d17bfdf1847201ba3f47811af6fa8e07222190d151`
- q1c: `5f81826a65a73aed7579f8d7dc4d663aa28b92ebca97c6310b70ff72b592532e`
- tqn25: `e8983ac4e3e0b42360442015c45dc51b18267d5753a518c5b79784d337fd63d4`
- tqn50: `7aa4c7861682660723a1423ba015b75d8e0ecf224b64aedc9aaae8bcb6b3a0a3`

## Decision

**REPRODUCED.** Applying the frozen rule: 17/17 REJECTed at R1 ✓, end-state
digest identical to Q1B ✓, noisy legs show linear absorption with no knee ✓;
no knee appeared and no self-contradiction installed. Every rerunnable
committed headline bar matched; TQ-NOISY10 was excluded per the prereg's own
instruction.

Notes: "PARTIAL" in the prereg's "TQ-NOISY50/N25/PARTIAL committed" names the
series' committed governance status (DOC-SWEEP 2026-09-22 proposes N2/N3/N4
bars — none frozen/signed), not a replication outcome; no PARTIAL outcome
applies to this replication. Inherited-state and method deviations (corrupt
predecessor tarball, object-store extraction instead of full checkout) are
recorded in `RUNLOG.md`; all inputs were byte-verified against the frozen
commit. No box commit was made by this crew — parent to decide.
