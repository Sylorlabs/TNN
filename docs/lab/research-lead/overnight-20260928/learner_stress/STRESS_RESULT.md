# STRESS RESULT: Continuing-Learner Stress Battery
## Pressure + interference + correction-under-pressure + delayed reuse through corrected premises

Worker: Continuing-Learner Stress Worker
Date: 2026-09-30 PDT
Verdict: **LEARNER-STRESS-PASS** (all six frozen kill bars pass; see below)
Prereg: `4ca3a7196` (frozen alone before implementation) + Addendum 1
`e16897bc9` (pre-implementation clarification of K-S4(b); strict ancestors of
this result)
Implementation: `stress_learn.zag` (pure Zag, no Python)
Raw output: `STRESS_RAW_OUTPUT.txt` (md5 70caf707935ebaf1a7ce41bade529785)

Per Micah's 2026-09-29 directive this worker reports BUILD-PASS/BUILD-FAIL
style verdicts only (here LEARNER-STRESS-PASS/FAIL). No promotion to
SURVIVES/BOUNDED/DOWNGRADED/KILLED is claimed; those require the full
11-step frontier pipeline including independent red team.

## 1. What was built

One persistent continuing learner: single Zag program, single process,
single main(), 8 sequential phases. The learner exposes exactly two
operations and never receives phase labels, task IDs, or mode flags:
learn(subj, rel, obj) and query(subj, rel, expected). Single rule store,
capacity 36, consequence-weighted eviction (frozen DEVINT2 formula:
importance = 10*(correct - wrong) + 5*dependents - 8*contradictions + 1;
evict minimum, ties by lowest slot index). Revision in place on
contradiction (superseded_obj keeps the old label; slot never freed).
Exact-match retrieval (disclosed v1 scope limit). Two-hop composition is
harness-level authored infrastructure (answer = sign(r1 - r2)); the LEARNED
behavior under test is premise retrieval, each used premise registering
dependents++.

Goes beyond DEVINT2 (BUILD-PASS 5fd1e0977) on five dimensions: corrections
applied UNDER pressure to stale items; double-correction revision chains;
interference targeted at corrected items; delayed reuse THROUGH corrected
premises; two pressure waves with dynamically useful junk.

## 2. Raw results (from frozen binary, 3/3 byte-identical, exit 0, zero stderr)

- P1_RECALL 8/8 (foundation baseline)
- P2_JUNK 28 (30 taught, 2 evictions, both never-queried junk)
- P4_PRERECALL 8/8 (retention through pressure wave 1 + 22-rule interference)
- P4_CORR_210 5/5 (answers 8, the latest label)
- P4_CORR_511 5/5 (answers 180)
- P4_SUPERSEDED_210 6 (revision chain 4->6->8 preserved in provenance)
- P4_COLL_CHANGES 0/12 (zero collateral from 3 contradictions)
- P5_CORR 4/4 (corrected items survive targeted relation-overlap interference)
- P5_RECALL 8/8
- P6_TWOHOP 5/5 (all five compositions route through corrected premises)
- P7_JUNK 7 (see mechanism note 4 below)
- P8_RECALL 8/8 (foundation intact after pressure wave 2, corrected labels kept)
- P8_CORR 2/2
- FOUND_EVICT 0 (no foundation rule evicted in the entire lifetime)
- Evictions total 56: P2 2 junk, P3 22 plain junk, P5 12 interference
  remnants, P7 1 interference remnant + 19 new junk (see note 4)
- STATEHASH ticks strictly increasing: 16, 64, 108, 153, 201, 211, 231, 241

## 3. Frozen bar evaluation

- K-S1 (retention through pressure 1 + interference >= 7/8): 8/8. PASS.
- K-S2 (correction uptake under pressure): (a) 5/5 and 5/5 new labels;
  (b) double-correction chain resolves to latest label only (5/5 answer 8,
  superseded chain 4->6->8 recorded); (c) collateral 0/12. PASS.
- K-S3 (interference resistance of corrections): 4/4 corrected probes after
  targeted interference; foundation 8/8; zero foundation evictions. PASS.
- K-S4 (delayed reuse through corrected premises + pressure 2 survival):
  (a) two-hop 5/5 >= 4/5; (b) structural grep: learn() calls with foundation
  subjects (1..6) appear ONLY in the P1 teaching block (8 calls) and the P4
  correction block (3 calls); zero in P2/P3/P5/P6/P7/P8; no call re-asserts
  a superseded label; (c) P8 final recall 8/8 with corrected labels;
  (d) zero foundation evictions. PASS.
- K-S5 (determinism): 3/3 byte-identical runs, exit 0, zero stderr. PASS.
- K-S6 (persistence): single znc compile; single binary run per pass;
  8 STATEHASH lines with strictly increasing ticks; phases sequential in one
  main(); no labels, resets, or recompilation. PASS.

ALL SIX PASS. Verdict: **LEARNER-STRESS-PASS**.

## 4. Mechanism note (honest finding, not a bar)

P7 taught 20 junk rules with no interleaved queries. The consequence policy
evicted 19 of the 20 newcomers (each new junk has importance 1, lower than
every established item) plus 1 interference remnant, retaining all 8
foundation rules, all 6 dynamically-useful junk rules, and all 12 targeted
interference rules. The policy thus refuses to displace predictively useful
or depended-upon items for never-queried newcomers. This is the intended
consequence semantics working as designed, and it bounds a real behavior:
under this policy, genuinely new knowledge must EARN retention through use
(queries, dependents), exactly as the 6 P2 junk rules did (correct=3 each,
all survived both floods). A future revision hypothesis could test whether
this newcomer-churn delays acquisition of useful-but-not-yet-queried
knowledge.

## 5. Governance and disclosures

- Prereg 4ca3a7196 committed alone before any implementation; Addendum 1
  e16897bc9 committed pre-implementation; ancestry verified with
  git merge-base --is-ancestor.
- Pure Zag throughout: implementation, compile, runs, analysis
  (grep/awk/cmp/md5sum only). No Python anywhere.
- No em dashes in any documentation (check_no_dash.sh byte-verified).
- Owned paths only: docs/lab/research-lead/overnight-20260928/learner_stress/.
  Files: PREREG_STRESS.md, PREREG_STRESS_ADDENDUM1.md, stress_learn.zag,
  STRESS_RESULT.md, STRESS_RAW_OUTPUT.txt.
- Binary built only in /tmp (/tmp/stress_run), never staged.
- Compiler warnings: 25x A0102 (ignored return value of query in
  fire-and-forget probe loops) are non-fatal analyzer notes; build
  succeeded, behavior verified byte-identical across 3 runs. Same warning
  class as DEVINT2, disclosed identically.
- Authored infrastructure not claimed as learned: two-hop comparison
  operator, phase sequencing, integer episode coding, exact-match retrieval.
- Scope limits disclosed: exact-match retrieval only; integer-coded
  episodes; synthetic world with 2 deliberately false foundation facts.
- Baseline record: this battery ran against the CURRENT (pre-DDES)
  continuing learner, so the DDES-integrated learner can be compared later.

## 6. Exact commands (K-S6 documentation)

- Compile (once): /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc docs/lab/research-lead/overnight-20260928/learner_stress/stress_learn.zag -o /tmp/stress_run
- Run (3x): /tmp/stress_run > /tmp/stress_outN.txt 2> /tmp/stress_errN.txt
- Determinism: cmp out1 out2, cmp out1 out3 (identical); md5sum out1 =
  70caf707935ebaf1a7ce41bade529785; stderr files 0 bytes; exit 0.
