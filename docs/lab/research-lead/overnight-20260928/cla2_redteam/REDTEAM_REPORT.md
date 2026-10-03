# CLA-2 Red Team: Adversarial Audit Report

Target: `docs/lab/research-lead/overnight-20260928/cla2_build/cla2.zag`
Build commit: `e639904f2`. Prereg: `24351fd31`.
Amendments: `62e5ebb9f` (A1-A12), `0525377f3` (ISA ruling), `1fc77503b` (EXECUTE A-C).
Method: static source inspection + dynamic binary verification + fresh rebuild.
Toolchain guard: Step 0 in NAMECHECK.md. Stub PATH active. Zero Python invoked.

## Verdict: CLA2-REDTEAM-COMPLETE

Four of five vectors pass. One process-level ATTACK-SUCCESS (stale binary).
No scientific claim is broken. The implementation source is sound.

## Vector 1: Hidden researcher policy - ATTACK-PASS (with observations)

The bootstrap miss-policy (`bootstrap_miss`) is generic. It takes (subj, rel)
as parameters, gathers exemplars by structural match on relation ID, checks
equality of objects via EQ, and promotes a literal MAP on invariance. No
relation names, world IDs, task types, or domain constants appear. The
P-INV check is order-0 (equality), the minimal regularity, composable from
the generic EQ primitive. It is not a forbidden detector under the ISA
ruling (no FIND_POLYNOMIAL_ORDER, DETECT_NEGATION, BUILD_CAUSAL_RULE,
LEARN_PROCEDURE, FIND_THRESHOLD, or MAKE_CONDITIONAL in core; verified by
case-insensitive source scan, zero hits outside comments).

MISS_POLICY supersession: the hook exists (`miss_policy_set` writes node 1
payload[0]; node 1 is writable via ordinary WRITE per A12). No core process
writes it automatically, which is correct per design: the learner supersedes
when it promotes its first MAP. Not a hidden policy.

Observation 1: The K node (tag 903) is created with value 3 and no code path
ever revises it. The comment "the strengthen rule may revise it" is
aspirational. The value lives in learner state (writable in principle via
WRITE), and no core logic hardcodes K=3 (all reads go through `k_get`), so
the architecture supports revision. But no mechanism exercises it. Gap
between prereg "revisable" and implementation "frozen default." Not a break;
flag for the next builder wave.

Observation 2: `bootstrap_miss` creates cnt self-loop SUPPORTS edges plus one
USE self-loop on the promoted MAP to give it initial standing. This is a
bootstrap standing-inflation convention, not genuine evidence. Documented in
source comments, generic (no domain content), but worth noting: the MAP's
initial bid comes from self-authored edges, not from corroboration.

## Vector 2: Semantic cases - ATTACK-PASS

Zero string literals with domain terms in core logic (string scan: only test
output labels like "P1 PASS"). Zero switch/match statements on domain
concepts. Zero branches on world, task, or relation identity (grep for
"world"/"task" in code: zero hits). Numeric tag comparisons (101-104) appear
only in the EXECUTE dispatch, which is the closed ISA table, not a semantic
case.

## Vector 3: EXECUTE ISA sandbox - ATTACK-PASS (with observations)

The 4-op dispatch (MOVE=101, BRANCHEQ=102, INC=103, DEC=104) is closed.
Unknown op tags fall through to `return -999999` (clean FAIL). Step budget
(1000) enforced, exhaustion returns FAIL. MOVE/INC/DEC validate destination
slot >= 1000, else FAIL. BRANCHEQ with refs pointing at non-cell nodes fails
on the next iteration's tag check. `resolve_op` maps negative operands to 0.
Learner-constructed EXECUTE graphs cannot invoke ALLOC, LINK, WRITE, or any
non-EXECUTE primitive; the op semantics touch only frame slots and node
payload[0] reads.

The existing EXECUTE-FAIL test covers unknown tag 999 (verified passing in
fresh build). Budget exhaustion, invalid BRANCHEQ targets, and dst<1000
rejection are verified by code inspection but not covered by dedicated tests.
The dispatch is a simple if-else chain; static analysis is reliable here,
but a future hardening pass should add those three adversarial cases.

Observation: no memory bounds checking on node/frame indices (consistent with
the entire codebase's established u8-buffer pattern). This is not a semantic
sandbox escape: there is no privilege boundary within the single workspace.
Noted for completeness, not a finding.

## Vector 4: Standing derivation - ATTACK-PASS

`map_standing(m)` is defined as `return bid(W,m)`. Standing is computed from
live edge counts on every call, never stored. Source scan for
"standing"/"utility"/"confid" outside test output: exactly one hit, the
`map_standing` definition itself. The signed bid counts DEPENDS(1),
SUPPORTS(2), USE(6), CONFIRMS(7) as +1 and CONTRADICTS(3) as -1. GROUP shared
fate is structural (member inherits group edge counts via MEMBER edges), not
a scalar. Content-free aggregation confirmed.

## Vector 5: K1/K2/K3 - K1 VERIFIED, K2 QUALIFIED PASS, K3 PROCESS ISSUE

K1 (commit ordering): independently verified via `git merge-base
--is-ancestor`. Prereg `24351fd31`: ANCESTOR-OK. Integration spec
`62e5ebb9f`: ANCESTOR-OK. ISA ruling `0525377f3`: ANCESTOR-OK. EXECUTE
placement `1fc77503b`: ANCESTOR-OK. The builder's K1 claim holds.

K2 (zero-claims audit):
- Zero task-specific handlers: CONFIRMED by source scan.
- Zero hardcoded semantic cases: CONFIRMED (Vector 2).
- Zero modes: QUALIFIED. Header field HAGG (offset 16) selects among three
  aggregation forms (0=sum, 1=max, 2=threshold-count). This is prereg-
  authorized (P7 load-bearing test, PREREG_CLA2.md lines 207-208, 382-383),
  defaults to 0 in `cla2_init`, is not writable by the learner (header field,
  no learner API path), and the P7 test verifies outcome invariance across
  all three forms (fresh build: sum=15 max=15 thresh=15). It is a test-only
  switch, not a domain mode. The builder's "0 modes" claim is about
  domain/task modes; this qualification should be recorded.
- Zero bridges: CONFIRMED.
- Zero regularity detectors: CONFIRMED (Vector 1 scan).

K3 (process): ATTACK-SUCCESS on build hygiene. See below.

## Finding F1 (process): committed binary is stale

The committed `cla2_bin` (75449 bytes, sha256
52df50f543cf3f15577ff5f3e09387bced3cb09b35c2445a46a47ca730c4ace,
timestamped Sep 30 18:25) was built from an earlier source version. Running
it reports "SELF-TESTS PASSED: 7/8" with P10 FAIL (contradiction-recorded=0
contradicts-edges=1 old-retrievable=1 current=10).

A fresh build from the committed source with the pinned compiler
(`znc_linux_x86_64_abed8aa1`, 116799 bytes) reports "SELF-TESTS PASSED:
15/15" with P10 PASS (current=20). All 15 tests pass, including the 7 new
amendment tests (EXECUTE, EXECUTE-FAIL, SIGNED-BID, ACT, ACT-NULL,
BOOTSTRAP, REGISTERS).

Root cause: the builder fixed a real bug (activate() returning history nodes
with tag 3 instead of fact nodes; fixed by adding the `ng(W,n,0)==1` filter,
with the design rationale documented in the activate comment: history nodes
are consulted via the HISTORY step, not activation) but committed the source
fix without rebuilding the binary. The fix is legitimate, not a test
weakening: the P10 test itself is unchanged, and the corrected behavior
(current query returns 20, the post-contradiction value) is what the prereg
specifies.

Impact: the scientific claims (15/15) are true of the committed source but
not demonstrated by the committed binary artifact. Any downstream consumer
running `cla2_bin` as-is gets the stale 7/8 result with a P10 failure.

Recommendation: rebuild `cla2_bin` from the committed source with the pinned
compiler and amend the build commit, or record the fresh binary's sha256 in
the build report. Do not modify source.

## Summary table

| Vector | Result |
|---|---|
| 1. Hidden researcher policy | ATTACK-PASS (2 observations) |
| 2. Semantic cases | ATTACK-PASS |
| 3. EXECUTE ISA sandbox | ATTACK-PASS (test-coverage observation) |
| 4. Standing derivation | ATTACK-PASS |
| 5. K1/K2/K3 | K1 verified; K2 qualified pass; K3 ATTACK-SUCCESS (F1 stale binary) |

No finding breaks a scientific claim. F1 is a build-hygiene issue with a
clear remediation. Observations O1 (K never revised), O2 (bootstrap self-loop
standing), and the HAGG qualification are recorded for the architecture
ledger, not as failures.
