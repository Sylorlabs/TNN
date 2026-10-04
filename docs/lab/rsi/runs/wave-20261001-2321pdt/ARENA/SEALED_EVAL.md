# SEALED EVALUATION: Arena INQ (wave-20261001-2321pdt)

Frozen prereg: PREREG_ARENA_INQUIRY.md (committed alone at 1156add31,
strictly before the implementation commit 0ddb5e9ce; commit-order
self-check verified by git merge-base). No amendment was needed; the
prereg ran unchanged.

## 1. Artifact identities

| Artifact | SHA-256 | Status |
|---|---|---|
| v6 base source (refreeze) | c6dbc20cf447dce7ab506576b42557a0542065e170bee6516558ecfb435d1e89 | matches refreeze record |
| INQ source (committed 0ddb5e9ce) | 456589d6aa01247596fa69b84289b9e2c7739e1ec755cfb1946fbbab14cbecce | 1204 lines |
| INQ binary bin/inq | 09f59dcbee0fcd443a911f2bf24bff883960f457d0ce9acd59506d3c38339b1d | rebuild from committed source byte-identical |
| world_gen (rebuilt) | c4c8340c818e6848c88e34f1989bf382ff097c69a71d6621c6bf28b58dc85211 | matches refreeze record |
| arena (rebuilt) | 3899577bc0c15c77711621071c14fd2cd35eab60360dc1ca71a2c2e2038ce076 | matches refreeze record |
| turns.jsonl (regenerated) | 0fc3edb0e2fe0d4b68e1d51a63c8cac243c8faefcd800122b2d9c1c97bcb2469 | matches sealed world, 131 turns, 68 items |
| PRE-RUN answer_key.json | a05ef916122ea9643fa69e4a4973b94ea1c603da642d9bd07788f61b89a07a51 | hash only, never opened |
| K6a binary (ask off) | 463bbf3fd160a0d24e6aa7ac59ea4521b6000c3cab4ac08b4e94c35c1516512f | one-line source delta |
| K6b binary (absorb off) | a94054a8d009248b4fc6fd951e4305ead41548826e08fa85edb63745749c6802 | one-line source delta |

The INQ source is the v6 base plus the marked INQ section (41 lines:
inq_emit, INQ_ASK_ON, INQ_ABSORB_ON, trace helpers) and two surgical
edits (observe emission on unknown fact query; learn_fact absorption on
observe_result). Diff vs v6 base: 69 lines added, 3 removed, all ASCII.

## 2. Sealed scores (3/3 runs identical)

| Cap | n | v6 refreeze | INQ run1 | INQ run2 | INQ run3 |
|-----|---|-------------|----------|----------|----------|
| 1 | 6 | 1.000 | 1.000 | 1.000 | 1.000 |
| 2 | 4 | 1.000 | 1.000 | 1.000 | 1.000 |
| 3 | 6 | 1.000 | 1.000 | 1.000 | 1.000 |
| 4 | 4 | 1.000 | 1.000 | 1.000 | 1.000 |
| 5 | 6 | 1.000 | 1.000 | 1.000 | 1.000 |
| 6 | 3 | 1.000 | 1.000 | 1.000 | 1.000 |
| 7 | 3 | 1.000 | 1.000 | 1.000 | 1.000 |
| 8 | 4 | 0.000 | 1.000 | 1.000 | 1.000 |
| 9 | 3 | 0.000 | 0.000 | 0.000 | 0.000 |
| 10 | 2 | 1.000 | 1.000 | 1.000 | 1.000 |
| 11 | 2 | 1.000 | 1.000 | 1.000 | 1.000 |
| 12 | 6 | 0.000 | 0.000 | 0.000 | 0.000 |
| 13 | 6 | 1.000 | 1.000 | 1.000 | 1.000 |
| 14 | 6 | 1.000 | 1.000 | 1.000 | 1.000 |
| 15 | 1 | 0.000 | 0.000 | 0.000 | 0.000 |
| 16 | 6 | 1.000 | 1.000 | 1.000 | 1.000 |
| TOTAL | 68 | 0.794 | 0.852 | 0.852 | 0.852 |

58/68 = 0.853 (scorer displays truncated 0.852). Gain: +4 items, all C8.
tool_calls rises 0 -> 7 (4 C8 asks + 3 C7 asks), the honest inquiry count.

## 3. Kill bar verdicts

K1 (C8 = 4/4): PASS. All four C8 items score 1000: first-ask replies carry
the observe field (first_obs=1) with reply "UNKNOWN"; re-ask replies equal
the keys exactly (turn 120 "wooden" and the three sibling items verified
in the trace: absorbs for all four oracle facts, zero re-ask asks).

K2 (zero regressions): PASS. Per-capability scores on C1-C7 and C9-C16
byte-identical to the v6 refreeze record on all three runs. The reply
stream diff vs the v6 refreeze run touches exactly 16 lines: 3 C7 lines
(observe field added, reply field still "UNKNOWN"), 12 C8-block lines
(4 first-asks, 4 re-asks UNKNOWN->value, 4 observe_result tail-metric
growth from absorbed facts), and the done line (tail metrics). No scored
reply field changed on any non-C8 item.

K3 (determinism): PASS. 3/3 byte-identical stripped reply streams
(sha256 3b1911236a81c742204f0800da14933ac713ed1e23c9905cf05bc4693dcbb46d;
ms and rss_kb excluded, the v6 K6 exclusion class) and 3/3 byte-identical
stderr traces (sha256 d664b9eb600250e5fb5a8f7a1ee98b9f2710cc416305bfd5e59d7e6d8be76488).
Zero RNG in decision paths.

K4 (pure Zag): PASS. `which python3` and `which python` print nothing at
lane start and lane end (safebin PATH throughout). Only znc-built binaries,
bash, safebin coreutils, and git read/commit ops were used. No
PROCESS-FAIL event.

K5 (sealed validity): PASS. world_gen and arena rebuilt from committed
sources with hashes matching the refreeze record; turns.jsonl regenerated
byte-identical to the sealed world; pre-run hashes recorded before the
contestant ran; the key file was hashed but never opened; worlddir is
arg-presence-checked only. Grep audit of the mechanism source for the 4
C8 oracle values and the 4 C8 entity/attr names: zero hits. Disclosure
(per prereg): the worker incidentally saw observe_result values while
verifying the turn protocol from the committed 1721pdt sealed world; they
are never used (requests parse entity/attr from the question; answers
come from the turn stream); the grep audit is the evidence.

K6 (negative controls): PASS.
K6a (INQ_ASK_ON=0, one-line delta): C8 = 0/4, total 54/68 = 0.794.
Without the request, first_obs never fires. Trace shows 4 absorbs but no
asks: absorption without inquiry is inert for scoring.
K6b (INQ_ABSORB_ON=0, one-line delta): C8 = 0/4, total 54/68 = 0.794.
Without absorption the re-asks stay UNKNOWN; the trace shows 11 asks (4
first-asks + 4 re-asks + 3 C7), confirming the mechanism re-asks whenever
the fact is still unknown. Both halves are causal; both ablations
reproduce the v6 baseline exactly, confirming the edits are inert when
disabled.

K7 (honesty preserved): PASS. All 3 C7 unknowable items reply exactly
"UNKNOWN" in all three sealed runs. The observe request is a request,
never an answer; no hallucination.

K8 (architecture): PASS. Delta: 69 lines added, 3 removed vs the v6 base.
0 new modes, 0 bridges, 0 routers, 0 task-specific admission gates, 0
hardcoded semantic cases, 0 hardcoded entities/attrs/values/answers
(keyword scan of added lines for mode/bridge/router/admission/gate: 0
hits). The two insertion points dispatch on existing turn kinds. The
inquiry trigger is not capability-gated: it fires on any unknown
fact/fact2 query. Learner-state structures created: absorbed facts in
the general fact store (visible in the stderr trace and fact_n growth);
capability comes from learner state, not new source logic.

K9 (no L3 claim): PASS (disclaimer recorded). INQ does not meet
Criterion 0: the "request the named missing fact" semantics is
researcher-authored handler logic (fails C0-A); the inquiry form is
fixed, not incrementally constructed from experience (fails C0-B); no
unforeseen representational forms are produced (fails C0-C); absorbed
facts are reused for answering but no new representation is invented
(fails C0-D). Plainly: INQ is L1/L2 fact-acquisition infrastructure (a
better ask-observe-answer loop), not L3 representational invention. No
L3 claim is made.

## Verdict: BUILD-PASS

K1 through K9 all PASS. C8 moves 0.000 -> 1.000; total moves 54/68
(0.794) -> 58/68 (0.853) with zero regressions on the other 15
capabilities; 3/3 byte-identical reruns.

## Scope reminders (unchanged)

INQ is a CANDIDATE mechanism only. No L3 claim (K9), no TNN-2 substrate
claim, no TNN-beats-LLM claim. The canonical 0.573 is not moved by this
result (only a clean refreeze reproducing composition without
contamination can move it). The LLM baseline comparison remains pending
credentials and is out of scope. Remaining zeros: C9 causal, C12
transfer, C15 goal. INQ was built on the v6 base, not on the TCNP
candidate binary; candidate integration is a separate later decision.

## Toolchain

safebin PATH for the whole lane; `which python3` prints nothing
(re-verified at lane end); zero Python or other interpreter invocations;
shell only sequenced pinned znc, built binaries, git read/commit ops,
and file copies. No PROCESS-FAIL event. Zero em-dash bytes in lane docs
(verified by check_no_dash.sh before each commit).
