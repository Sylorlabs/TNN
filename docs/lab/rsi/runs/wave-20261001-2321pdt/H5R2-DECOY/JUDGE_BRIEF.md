# JUDGE_BRIEF: H5R2-DECOY (the discriminating world the baseline battery lacked)

## Provenance header

- RENDER_SHA: (sealed-eval commit: 8 assembled decoy world files, 8
  compiled world binaries, EVAL_DECOY.md with the 3/3 byte-identical
  full-stdout hashes; implementation commit 4511f5c64 strictly follows
  prereg freeze commit 51a4fe8e1)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: TNN3H5R H5R2 BUILD-PASS + H5R2-REPRO REPRO-PASS,
  then H5R2-BASELINE BASELINE-MATCHES via REVERT-TO-LATEST as the
  motivating result (the recency heuristic matched the gate on every
  bar of the four sealed worlds, so the gate was not shown necessary).
  This lane built the missing discriminating world the baseline lane
  named: one where the newest fact is NOT the live one.
- NEW_KNOWLEDGE_CLAIM: On decoy worlds where the newest fact is not
  the live one, the t2_prov_ok gate anchors every revert MAP to the
  live fact while the recency heuristic anchors to the decoy on 8/8
  probes, so the gate is necessary and recency does not subsume it.

## Verdict

DECOY-DISCRIMINATES. All five frozen kill bars hold: H5R2 8/8 "D ok";
REVERT-TO-LATEST 8/8 D-DECOY-FAIL (the pre-registered failure
signature: DEP edge to the decoy fact); NO-GATE 0/8 via D-DEP-FAIL to
the superseded original fact (its baseline-lane failure mode);
RANDOM-ANCHOR 2/8 (chance level); 3/3 byte-identical runs on all 8
worlds; the decoy fact itself answers correctly on all arms (no
adversarial-by-brokenness).

## The per-arm per-bar table (8 decoy probes)

| bar | H5R2 | (a) REVERT-TO-LATEST | (b) NO-GATE | (c) RANDOM-ANCHOR |
|---|---|---|---|---|
| D ok (target 8) | 8/8 | 0/8 | 0/8 | 2/8 |
| D-ANS ok (target 8) | 8/8 | 8/8 | 8/8 | 8/8 |
| D-DECOY-FAIL | 0 | 8 | 0 | 2 |
| D-DEP-FAIL (stale) | 0 | 0 | 8 | 4 |
| VAL-FAIL | 0 | 0 | 0 | 0 |
| 3/3 deterministic | yes | yes | yes | yes |

Frozen bars: DB-1 (H5R2 8/8) PASS; DB-2 (recency decoy-anchor >=5/8)
PASS at 8/8; DB-3 (controls as in the baseline lane) PASS; DB-4
(determinism) PASS; DB-5 (decoy genuineness) PASS. Hence
DECOY-DISCRIMINATES.

## What the evidence says, precisely

- The decoy family: after a revert on K=(b,RF2), a decoy OBSERVE
  teaches a new live fact on the unrelated key K2=(b,RD) with a newer
  creation timestamp. The revert MAP must anchor to K's live (older)
  fact. t2_gather enumerates the revert query's chain candidates in
  node-id order (stale, superseded-c1, live-reverted, decoy); H5R2's
  forward order plus the gate promotes the live-reverted candidate,
  while REVERT-TO-LATEST's reversed order promotes the decoy candidate.
- H5R2 white box (d1 P1): live MAP 65, DEP to node 36
  (87301,8702,87406) sup=0, the live reverted fact; decoy node 37
  untouched. All 8 probes identical in form.
- REVERT-TO-LATEST white box (d1 P1): live MAP 38, DEP to node 28
  (87301,8704,87406) sup=0, the decoy fact. All 8 probes. Value
  answers remain correct everywhere, so the failure is
  provenance-only: answers cannot discriminate these mechanisms; DEP
  edges can.
- NO-GATE white box (d1 P1): DEP to node 3 (87301,8702,87406) sup=1,
  the superseded original fact: its baseline-lane failure mode,
  unchanged by the decoy.
- The BASELINE-MATCHES result is resolved, not contradicted: recency
  explained the four-world battery only because on those worlds the
  newest fact happened to be the live one. The gate's necessity was
  untestable there; it is testable here, and it holds.

## Recommended next step

The gate survives its strongest simple alternative. Per the standing
execution rule, the next hypothesis begins: candidates are (1) a
stronger skeptic baseline that gates on liveness but not supersession,
or gates on recency-among-live (does "newest live fact" survive the
decoy?); (2) scaling the decoy family to more probes and to chained
(W3-style) decoys; (3) the composition-frontier comparative program
Micah ordered on 2026-10-02, which is independent of this lane.

## Process

Pure Zag throughout; safebin PATH; `which python3` printed nothing at
lane startup and at every check (NAMECHECK.md Step 0); zero
forbidden-executable invocations. Prereg freeze 51a4fe8e1 (2026-10-02
07:00:11 UTC) strictly precedes implementation 4511f5c64 (07:02:57
UTC) strictly precedes the sealed eval commit. No push; all commits
local on tnn-native-lab. A mechanism smoke test on disjoint unsealed
9xxx keys validated the prereg's mechanism claim before sealed
assembly; no sealed output was used to tune anything.
