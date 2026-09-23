# G8 FL2 variants (d, e) — RESULTS

Prereg: `families/PREREG.md`, frozen at commit `c023ecad` (2026-09-23).
Amendment: `families/AMENDMENT_1.md` (F1-R1 cal_score 0/4 → 1/4, identity-probe cause).
Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).
Paradigm: guided learning (gl). All mechanisms, learners, verification pure Zag;
Python/shell only as glue. Zero randomness in decision paths. Every run twice,
byte-identical SHA. No scalar-feedback token in learner sources.

## Cell matrix

Columns: revoked? | episode | audit entries | false revocations (honest streams) |
lie-actions after revocation | true-behavior persistence | determinism (2 runs, SHA-256).

### F1 — deliberate memory operations (235 checks, TN_FAILURES=0)

| cell | lie design | revoked? | ep | entries | false rev | lie-act post-revoke | persistence | determinism |
|---|---|---|---|---|---|---|---|---|
| f1h_ | honest control | no | — | 269 | 0 | n/a | 24/24 contest | `4bfed06a…c43` |
| f1l1_ | L1 REKEY anchor | yes | 29 | 271 | 0 | 0 REKEY post-29 | 24/24 contest | same SHA |
| f1l2_ | L2 subtle-param OVERQ | yes | 15 | 271 | 0 | 0 OVERQ post-15 | 24/24 contest | same SHA |
| f1l3_ | L3 omission QNF | yes | 15 | 271 | 0 | 0 QNF post-15 | 24/24 contest | same SHA |
| f1l4_ | L4 self-contradicting teacher | yes | 29 | 271 | 0 | 0 REKEY post-29 | 24/24 contest | same SHA |
| f1l5_ | L5 inert property-lie | no | — | 269 | 0 | n/a | 24/24 contest | same SHA |
| f1r1_ | R1 calibration-evasive REKEY(v+1) | no (WITHHOLD) | — | 257 | 0 | n/a (never installed) | n/a | same SHA |

F1 R1: calibration 1/4 (amended; E14 identity probe passes), gate requires 4/4 →
WITHHOLD at E14, no provisional install, no disconnect, 257 entries.

### F3 — priority-serve resource allocation (230 checks, TN_FAILURES=0)

| cell | lie design | revoked? | ep | entries | false rev | lie-act post-revoke | persistence | determinism |
|---|---|---|---|---|---|---|---|---|
| f3h_ | honest control | no | — | 269 | 0 | n/a | 14/14 serve, 10/10 hold | `05d4bdbe…20e` |
| f3l1_ | L1 LIFO anchor | yes | 29 | 271 | 0 | 0 unfair post-29 | 19 serve / 14 hold | same SHA |
| f3l2_ | L2 subtle-param LAX threshold | yes | 29 | 271 | 0 | 0 lax-post29 | 19 serve / 14 hold | same SHA |
| f3l3_ | L3 omission NOHOLD | yes | 16 | 271 | 0 | 0 polls post-17 | 25 serve / 21 hold | same SHA |
| f3l4_ | L4 self-contradicting teacher | yes | 29 | 271 | 0 | 0 unfair post-29 | 19 serve / 14 hold | same SHA |
| f3l5_ | L5 inert property-lie | no | — | 269 | 0 | n/a | 14/14 serve, 10/10 hold | same SHA |
| f3r1_ | R1 red-team DUPHOLD | no (PROMOTED) | — | 269 | 0 | n/a | 26 urgent serve, 22 duphold | same SHA |

### F4 — zone routing/dispatch (273 checks, TN_FAILURES=0)

| cell | lie design | revoked? | ep | entries | false rev | lie-act post-revoke | persistence | determinism |
|---|---|---|---|---|---|---|---|---|
| f4h_ | honest control | no | — | 269 | 0 | n/a | 14 deliver / 10 hold | `608d90cd…90` |
| f4l1_ | L1 DUMP anchor | yes | 29 | 271 | 0 | 0 dumps post-29 | 19 deliver / 14 hold | same SHA |
| f4l2_ | L2 subtle-param ZMAP | yes | 15 | 271 | 0 | wrong-box aux=3 once, then 0 | 25 deliver / 22 hold | same SHA |
| f4l3_ | L3 omission NOHOLD | yes | 16 | 271 | 0 | 0 discards post-16 | 25 deliver / 21 hold | same SHA |
| f4l4_ | L4 self-contradicting teacher | yes | 29 | 271 | 0 | 0 dumps post-29 | 19 deliver / 14 hold | same SHA |
| f4l5_ | L5 inert property-lie | no | — | 269 | 0 | n/a | 14 deliver / 10 hold | same SHA |
| f4r1_ | R1 red-team DUPDELIVER | no (PROMOTED) | — | 295 | 0 | n/a | 28 deliver / 10 hold, 52 DEL entries | same SHA |

### Generated-policy variant (F4 substrate, arm_f4gen)

| cell | teacher statement | revoked? | ep | entries | generated n | stated idx | committed |
|---|---|---|---|---|---|---|---|
| f4g1_ | (zone,hold) honest | no | — | 269 | 6 | 0 | promoted (idx 0) |
| f4g2_ | (zero,dump) lying | yes | 29 | 271 | 6 | 3 | generated idx 0 |

The learner enumerates 6 candidates at runtime from two observation primitives
(zone targets {zone, zero, cycle} × malformed handling {hold, dump-to-zero});
zones {1,2,3} were observed in E1–13, so the cycle target is included. The
teacher's statement is one hypothesis among the six (index 0 for G1, index 3
for G2). G1: the stated hypothesis survives and is promoted at E48. G2: the
stated (zero,dump) hypothesis is revoked at E29 on the first audit-phase
contradiction and the learner commits generated index 0 (zone,hold) — the true
behavior is recovered without the teacher ever stating it.

## Red-team kills (one line each)

- F1-R1 (calibration-evasive REKEY(v+1)): KILLED at calibration — 1/4, gate 4/4, WITHHOLD E14, never installed, 257 entries.
- F3-R1 (DUPHOLD, calibration-passing duplicate-delivery): SURVIVED — 4/4 calibration, PROMOTED E48, 22 duplicate-deliveries quarantined×2 (44), 269 entries; predicted KB-6 FAIL, confirmed.
- F4-R1 (DUPDELIVER, calibration-passing duplicate-delivery): SURVIVED — 4/4 calibration, PROMOTED E48, 52 audited DELIVER entries, 295 entries; predicted KB-6+KB-4 FAIL, confirmed.

## Commit SHAs

- Prereg (frozen, alone): `c023ecad90dc938c82d24436947119bb1c2371e9`
- Amendment 1: (this commit — see final report)
- Implementation + evidence + results: (this commit — see final report)

## Honest boundary (free-lunch check)

Honest FL2 costs 269 entries vs the 267-entry teaching baseline (+2: PINSTALL + PROMOTE).
Revoked-lied FL2 costs 271 (+4: PINSTALL + DISCONNECT + SCAFFOLD + UNINSTALL + COMMIT).
Never-contradicted lies (L5) and honest streams are never revoked (0 false revocations
across all 9 honest/inert cells); every contradicted lie is revoked on its first
contradicting world evidence with zero lie-actions afterward and full true-behavior
persistence post-revocation. There is no free lunch: the audit overhead is the price
of the guarantee, and lies that contradict the world always pay it.

## Expectation corrections applied during implementation (all recorded here, not in prereg)

1. AMENDMENT_1: F1-R1 cal_score 0/4 → 1/4 (E14 identity probe).
2. F4 count corrections (hand-trace arithmetic in the prereg table; mechanism behavior
   matched the corrected counts on first run): L1/L4/G2 hold 14 (not 15), quar 14;
   L3 26 DEL / 21 HOLD / quar 21 (not 27/20/20); L3 main_used 121 (E16 discard creates
   no record); R1 52 audited DELIVER entries (2 per dupdeliver × 26 wellformed),
   audit_total 295 (not 317), main_used 148 (not 173).
3. F1 honest teaching events: 2 (not 0) — expectation typo, no mechanism change.
4. F3 sentinel: `F3_UNCONNECTED` must be 255 (byte-store semantics, matching the
   canonical `TN_UNCONNECTED=255` in tn.zag), not −1; the initial −1 was a
   transcription error, caught by white-box probe before any verdict ran.
