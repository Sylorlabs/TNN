# REPORT: L2-TRUNCATE-XDOMAIN

**Verdict: L2-TRUNCATE-XDOMAIN-PASS** (K1-K8 all PASS, 0 falsifiers fired, F-COUNT silent)

Worker: L2 Adaptive Reuse subagent (depth 2/2), 2026-10-02.
Prereg: `PREREG.md` (frozen at 7a58fbfd4, committed alone before
any implementation). Pure Zag, safebin toolchain, zero
forbidden executables. Branch `lane-l2truncate-xdomain-20261002`
(worktree `~/workspace/tnn-rsi-l2truncate`), local only, never
pushed.

## What was built

A standalone pure-Zag learner (`learner.zag`, tx_ prefix, TX-
trace tags) holding an arithmetic aggregation MAP mA (id 1:
entry + 4 fold pairs, 9 hops, domain A) and a planning ROUTE MAP
mB0 (id 2, domain B). On a planning-domain aggregation query
Q2 with no native aggregation MAP, the cross-domain TRUNCATE
operator: (1) capability-searches the MAP inventory across
domains (distractor mD examined and rejected), (2) grounds the
FULL mA in domain B and records its failure (the 4th fold has
no grounding; the walk dead-ends), (3) enumerates strict
prefixes longest-first (k = nf-1 down to 1) and commits to the
first prefix whose target-domain grounding executes to the
query terminal with the required value, (4) promotes the
truncated Z (id 3) with type-16 derived-from provenance to mA,
verified by real execution before promotion. The cut point k=3
is chosen by the learner's enumeration policy; the driver
passes no length, no MAP id, no relation.

## Key numbers

- FULL arm Q2: A_SEARCH=285, A_EXEC=2 (frozen F-COUNT: silent,
  implementation matches the hand derivation exactly:
  capsearch 2 + full attempt 167 + k=3 attempt 116 = 285;
  verify + deliver = 2).
- Trace (run1): `TX-TRY k=4` -> two `FAIL-SHAPE` candidates ->
  `TX-FAIL k=4` -> `TX-FULL-FAIL` -> `TX-TRY k=3` ->
  `SHAPE-OK term=73 VERIFY-OK` -> `TX-OK k=3` ->
  `TX-ZBUILD rels=17,15,16,15,16,15,16 facts=10,11,12,13,14,15,16`
  -> `TX-VERIFY term=73 OK` -> `TX-PROMOTE z=3 t16=3->1` ->
  `ANS term=73 val=75 via=3`.
- Q2B: `ANS term=73 val=75 via=3` with no trunc phase.
- NOTRUNC arm Q2: `TX-FULL-FAIL`, `ANS term=-2 val=-2 via=-1`
  (A_SEARCH=169, t16=0): the full-X-only operator cannot solve
  it; truncation is REQUIRED.
- ABLATE-X (mA retired): capsearch all SKIP, `ANS -2`,
  t16=0, NM=3.
- FRESH (no MAPs): `ANS -2`, t16=0, NM=0.
- Determinism: 3/3 byte-identical runs, sha256
  `45e010f4494d12b8742d8aeb0a2b2f9a5229bc46386440ade6ab651c8afc82ff`.
- K6 audit: 12/12 frozen grep patterns return 0 hits on
  learner.zag (no relseq/fact literals, no world literals, no
  modes, no bridges, no python, no `as *i32`).

## Kill bars

- K1 PASS (X and Y exist before the task, work at home, learned
  independently): qa_via=1, qb_via=2, q2_via=3, disjoint
  relation sets (mA rels in {18,5,6}, mB0 rels all 7); shell:
  `Q QA` (line 2) < `Q QB` (4) < `Q Q2` (6).
- K2 PASS (full X fails; truncation REQUIRED): FULL_OK=0,
  `TX-FULL-FAIL` in trace, NOTRUNC arm ans=-2 with t16=0.
- K3 PASS (learner decides the cut): TRUNC_K=3,
  TRUNC_DECIDED=1 (flag set only inside the learner's
  descending-enumeration branch); shell: `TX-TRY k=4`,
  `TX-FAIL k=4`, `TX-TRY k=3`, `TX-OK k=3` in order;
  driver.zag contains zero `trunc_k`/`TRUNC_K` matches and
  tx_query takes no length parameter (only the TRUNC_ON
  causal-control flag).
- K4 PASS (truncated succeeds where full fails): q2_via=3,
  q2_val=75, FULL_OK=0; `TX-ZBUILD` and `ANS term=73 val=75
  via=3` verbatim in run1.
- K5 PASS (3/3 byte-identical sha256).
- K6 PASS (12/12 audit patterns zero hits).
- K7 PASS (ablation fails): ax_val=-2, ax_t16=0, ax_nm=3.
- K8 PASS (persists and reused): q2b_via=3, q2b_val=75,
  q2b_adapt=0 (TR_ENTERED stayed 0), Z live=1.

## Falsifiers

None fired (FALSIFIERS 0): F-NO-GROUND, F-WRONG-Z (Z header,
rels, facts, start/end, dom/cap, descriptor all match frozen
values), F-FULL-OK, F-NOTRUNC-PASS, F-ABLX-PASS, F-FRESH-PASS,
F-Q2B-RE, F-T16-COUNT (t16=1), F-NO-T16-SRC (3->1 present),
F-NO-LINK14, F-EDGE-NEW (all arms), F-COUNT (285/2 exact).

## What this demonstrates (and does not)

Demonstrates: the L2 TRUNCATE cell of the operation matrix
with cross-domain transfer. A learned procedure too long for
a target-domain grounding is shortened by a learner-owned
longest-verifying-prefix policy; the full form provably
fails (in-Zag flag + trace + no-truncate lesion arm); the
cut is not researcher-specified (driver names no length;
audit confirms); the truncated form carries derived-from
provenance, persists, and serves reuse without
re-computation. Cost accounting is exact and frozen
(285/2).

Does not demonstrate: generality beyond the one world
family (arithmetic aggregation x plan-cost aggregation);
adversarial robustness (world is builder-designed, not
sealed-adversary); integration with a continuing learner or
the frozen TNN core (standalone mechanism experiment, as
preregistered). The TRUNCATE operator, descriptor
extraction, fold search, and enumeration policy are
researcher-supplied generic machinery; the L2 claim is the
narrow one above.

## Residual footprint

0 modes, 0 bridges, 0 handlers, 0 new edge types (reused
14/16), 0 new opcodes, 0 new semantic cases. One new MAP-row
layout (40 bytes, 12 rel/fact slots) internal to this lane:
the 9-rel source does not fit the sibling lane's 8-rel rows.
No frozen source touched. Commits local with explicit
pathspec; nothing pushed.

## Files

- `PREREG.md` (frozen), `NAMECHECK.md` (Step 0 guard)
- `learner.zag`, `world.zag`, `driver.zag`, `tx_full.zag`
  (concatenated build input)
- `tx_bin` (pinned-znc binary), `tx_compile.txt`
- `tx_run1.txt`, `tx_run2.txt`, `tx_run3.txt` (byte-identical)
- `REPORT.md` (this file)
