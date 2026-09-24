# RESULTS_EDGE.md — Workstream A edge-case results (M1 vs M2)

Frozen prereg: `m1m2_separation/PREREG_M1M2.md` (commit ac128f4eec2bb30b4ff2f64e4b2ff2bfd96c9dd3).
Drivers: `src/edge_m1.zag`, `src/edge_m2.zag`, tables `src/ec_streams.zag`.
Pure Zag, zero RNG, real vendored mechanisms. Runs: 2026-09-24, 3x each, byte-identical.

## Summary table

| EC | case | M1 | M2 | split? |
|---|---|---|---|---|
| 1 | five-deep chain A→B→C→D→E | 4 sup, q_now=105, history clean | identical | no |
| 2a | conflicting UPDATEs, B-first order | 1 sup (C wins), q_now=103 | identical | no |
| 2b | conflicting UPDATEs, C-first order | 1 sup (B wins), q_now=102 | identical | no |
| 3 | update during quarantine | gate refuses, q_now=102, trust −1 | identical | no |
| 4a | phantom UPDATE, no prior | ignored, q_now(key2)=−1 | identical | no |
| 4b | UPDATE with wrong ack | gate-fail, q_now=101 | identical | no |
| 5 | stale pending after mid-deliberation world replacement | completes, q_now=102; hist taught_ep=7 | completes, q_now=102; hist taught_ep=1 | metadata only |
| 6 | A→B→A→B flip-flop | history clean, q_asof correct | **history corrupt, q_asof(6)=101 WRONG** | **YES — M1 wins** |
| 7 | stale-echo race after supersession | B revoked, q_now=101, trust −1 | identical | no |

Detail: all summary stats (BAD, TRUST, SUP, GFAIL, HC, QNOW) per EC:
- EC1..EC9 M1 vs M2 summaries are identical except EC6/EC5 history metadata (below).

## EC6 — the decisive split (flip-flop A→B→A→B)

Stream: TEACH(101)@1, WORLD(101)@2-4, UPDATE→102@5, WORLD(102)@6-9,
UPDATE→101@10, WORLD(101)@11-14, UPDATE→102@15, WORLD(102)@16-19.

M1 history (correct — taught_ep copied O(1) from live key state):
- h0: 101→102, taught_ep=1, ended_ep=5
- h1: 102→101, taught_ep=5, ended_ep=10
- h2: 101→102, taught_ep=10, ended_ep=15

M2 history (wrong — m2_derive_taught scans for the EARLIEST matching teach):
- h0: 101→102, taught_ep=1, ended_ep=5
- h1: 102→101, taught_ep=5, ended_ep=10
- h2: 101→102, taught_ep=**1**, ended_ep=15  ← should be 10

Consequence — M2's h2 interval [1,15] overlaps h0 [1,5] and h1 [5,10];
the history is internally inconsistent, and historical queries return wrong answers:

| q_asof(ep) | truth | M1 | M2 |
|---|---|---|---|
| 2 | 101 | 101 | 101 |
| 6 | 102 | 102 | **101 (WRONG)** |
| 12 | 101 | 101 | 101 |
| 17 | 102 | 102 | 102 |

M2 reports the value during B's first reign (ep 6) as 101 (A) instead of 102 (B).
This is a genuine correctness failure of M2's figure-it-out derivation on
repeated values: earliest-match finds the ep-1 teach instead of the ep-10 teach.

## EC5 — metadata difference (not a wrong answer)

Mid-deliberation: UPDATE(A→B)@5 pending; WORLD(C)@6-7 revokes A, installs C;
WORLD(B)@8 completes the stale pending. Both complete it (SUP=1, q_now=102).
History taught_ep: M1=7 (copied from post-revocation key state — temporally odd),
M2=1 (earliest-match). No q_asof query distinguishes them in this stream;
recorded as a metadata divergence, not a correctness split.

## Verdict

One decisive correctness split: EC6 flip-flop. M1's SUPERSEDE primitive (O(1)
history copy from live state) keeps the taught-episode chain consistent across
repeated values; M2's ledger-scan derivation (earliest match) corrupts it and
returns wrong historical values. **M1 wins the edge-case battery.**
Combined with the frozen verdict precedence (correctness split outranks
efficiency), **M1 is the Workstream A winner.**
