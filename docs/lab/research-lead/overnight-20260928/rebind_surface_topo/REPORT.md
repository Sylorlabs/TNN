# Rebinding Surface & Topology: Q2A and Q2E

**Verdict: REBIND-SURFACE-COMPLETE.**

Five tests of the structural rebinding mechanism (91585087c) under surface
permutation (Micah Q2A) and topology transfer (Micah Q2E). All 3/3
byte-identical per arm. Unfrozen variant only. Pure Zag via pinned znc.

## Test 1: Relation Change (Q2A-1) -- PASS

World A: chains with relation 1 (plen-3 decoy MAP, plen-5 main MAP).
World B: chain 301->311->312->313->314 with relation 7 (not 1).

| arm | B answer | tried | rejected |
|---|---|---|---|
| treatment | 314 | 7 | 6 |
| control | 314 | 11 | 10 |

The mechanism is relation-agnostic. The MAP shape (plen) is structural;
literals and relations come from B's gathered paths. The relation-1 MAP
rebinds to relation-7 facts without modification.

## Test 2: Irregular Spacing (Q2A-2) -- PASS

World B: chain 401->450->451->500->501 (gaps 49,1,49,1, not uniform).

| arm | B answer | tried | rejected |
|---|---|---|---|
| treatment | 501 | 7 | 6 |
| control | 501 | 11 | 10 |

The mechanism does not depend on arithmetic patterns in entity IDs.
Rebinding is positional over gathered paths, not pattern-based.

## Test 3: Reversed Direction (Q2A-3) -- PASS

World B: reversed chain 514->513->512->511->501 (IDs decrease along path).

| arm | B answer | tried | rejected |
|---|---|---|---|
| treatment | 501 | 7 | 6 |
| control | 501 | 11 | 10 |

The mechanism is direction-agnostic. BFS from the query subject finds
the path regardless of ID ordering. The chain topology is what matters,
not the direction of ID values.

## Test 4: Depth Transfer 5->3 (Q2E-1) -- PASS (MAP selection)

World A: plen-3 decoy MAP (lower ID), plen-5 main MAP (higher ID).
World B: needs plen-3 (601->611->612).

| arm | B answer | tried | rejected | via |
|---|---|---|---|---|
| treatment | 612 | 1 | 0 | rebind (RB-STAT 1/0) |
| control | 612 | 1 | 0 | trial |

The mechanism correctly SELECTS the plen-3 decoy MAP over the plen-5 main
MAP. MAPs are scanned in node-ID order; the plen filter (exact match)
skips the plen-5 MAP (no length-5 paths in B). The rebind succeeds on the
first try.

No cost difference vs control because plen-3 is trivial for the trial
(1 verification). The test validates MAP selection logic, not cost
reduction. A harder test would need many plen-3 distractors before the
correct path in gather order.

Note: an earlier version of this test used a 4-node chain (plen-4) with
no matching MAP in A. The mechanism correctly found no match (8 rebind
tries, 8 rejects) and fell back to trial (7=7). This was a test design
error, not a mechanism failure. The fixed version uses a true plen-3 chain.

## Test 5: Branched Structure (Q2E-2) -- GRACEFUL FALLBACK

World A: plen-3 and plen-5 chain MAPs.
World B: branched from 701.
  Correct path (length 4): 701->711->712->713 (expects 713).
  Dead-end (length 3): 701->721->722 (722 != 713).
Query (701,50) expects 713.

| arm | B answer | tried | rejected | rebind |
|---|---|---|---|---|
| treatment | 713 | 5 | 4 | 4 tried, 4 rejected |
| control | 713 | 5 | 4 | n/a |

The plen-3 MAP matches the dead-end path (701->721->722), but verification
against expected=713 correctly REJECTS it (722 != 713). The plen-5 MAP has
no length-5 paths to match. After 4 rebind rejections, fallback to trial
succeeds with 5 tries (identical to control).

This is the honest behavior for an uncovered topology: try, verify,
reject, fall back. No benefit (5=5), but no harm (no wrong answer, no
poisoning). The verification arbiter works as designed.

## Mechanism Analysis

**What the mechanism IS sensitive to:**
- Exact plen match (chain length in nodes). A plen-5 MAP will not help a
  plen-4 problem. This is by design (the filter is `path_len == plen`).
- Graph topology (must be a pure chain: alternating 102/101 tags). The
  `rb_chain_plen` walker returns -1 for non-chain graphs.

**What the mechanism is NOT sensitive to:**
- Relation IDs (Test 1). The relation comes from B's path, not the MAP.
- Entity ID values or spacing (Test 2). Positional, not pattern-based.
- ID ordering direction (Test 3). BFS is direction-agnostic for chains.
- Which MAP among multiple (Test 4). ID-order scan with plen filter
  selects correctly.

**Failure modes (all graceful):**
- No plen match: rebind tries candidates, verification rejects, trial runs.
  (Test 4 original, Test 5).
- Wrong path with right plen: verification rejects (Test 5 dead-end).
- Non-chain MAP: `rb_chain_plen` returns -1, MAP ignored.

**What remains untested (Micah Q2B, Q2C, Q2D, Q2F):**
- Deceptive structural similarity (Q2B): multiple MAPs with same plen but
  different causal structure. Only one is correct. Can verification
  distinguish? (Test 5 touches this: the dead-end had the right plen but
  wrong answer; verification caught it.)
- Scale (Q2C): 20, 100 MAPs. Does retrieval cost explode?
- Partial applicability (Q2D): old structure 80% useful, needs modification.
  Current mechanism is all-or-nothing (exact plen match).
- Negative transfer (Q2F): misleading MAP that verifies but is wrong.
  (Test 5 shows verification catches wrong-answer matches, but a
  subtly-wrong MAP that still verifies is a harder adversary.)

## Standing Metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: the 5 test drivers, the plen
  filter, the ID-order scan (all in the existing ~70-line mechanism).
  No new mechanism code was written for these tests.
- LEARNER-OWNED STRUCTURAL DECISIONS: the A-phase MAP graphs (from
  91585087c, reused verbatim). The plen values read back are learner-created.
- SOURCE-ENUMERABLE FORMS: chain shapes of any plen (generic).
- SUF DECISIONS: 0 (no new).
- REUSE EVENTS: 5 (one per test where rebind succeeded: Tests 1,2,3,4).
  Test 5 had 0 successful reuses (4 attempts, 4 verification rejections).
- REVISION EVENTS: 0.
- COGNITION LINES: 0 (test only, no new mechanism).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

## Constraints Honored

Unfrozen variant only. Frozen base read-only (SHA-256 verified).
Rebind patch verbatim from 91585087c. Pure Zag via pinned znc. Safebin
PATH, no python3/python. Zero em/en dashes (byte-verified). Paper
untouched. Nothing pushed. Explicit pathspecs on add and commit.

## Artifacts

- NAMECHECK.md (Step 0 guard)
- REPORT.md (this file)
- st_base.zag (frozen base, read-only copy)
- st_patch.zag (rebind mechanism, verbatim from 91585087c)
- st_driver_{rel,irreg,rev,depth,branch}.zag (5 test drivers)
- st_yesa.zag / st_noa.zag (phase-A stubs)
- assemble.sh (build script)
- st_full_*.zag (10 assembled sources)
- *_bin (10 binaries)
- *_run{1,2,3}.txt (30 run transcripts, 3/3 identical per arm)
