# Prereg: H-UNIFIED2 Red Team (U2-A1..U2-A4)

**Date:** 2026-09-29
**Status:** FROZEN before execution
**Target:** H-UNIFIED2 SURVIVES (12/12), `unified2_learn.zag` (commit 0eb7677fe)
**Parent prereg:** PREREG_UNIFIED2.md (commit bfd5bcb13)
**Stance:** Assume the repair claim is false. Attack the composition.
**Purity:** Pure Zag. No Python anywhere. Determinism: 3 runs byte-identical.

## Target claim under attack

H-UNIFIED2 claims three composition-layer repairs:
- Repair 1: coherence-gated causal revision. Contradictory episodes
  QUARANTINED, never committed. Verified knowledge protected.
- Repair 2: explicit AMBIGUOUS route code (5) for int-pair lessons and
  bare digit strings.
- Repair 3: subset direct discovery. Bridge no longer fires spuriously.

## Attacks

### X-U2-1: Quarantine bypass (truth-first order)

Feed verified causal knowledge FIRST through the gated path, exactly as
K-U2-1 does, then fire a battery of adversarial episodes through
`handle_caus_learn` and check whether any verified `cpredict` answer
changes.

Battery (each routed through `route_line`, fed through the gated
handler iff route is CAUS_LEARN):
- (a) control: "1,0,0>9,9;1,0,0>9,9" (original U-A2 attack). Expect:
  0 committed, 2 quarantined.
- (b) near-miss: "1,0,0>9,8;1,0,0>8,9" (both next-state fields differ).
- (c) novel state: "2,0,0>9,9;2,0,0>9,9" (no matching rule; coherent;
  learns a new rule; must not touch verified answers).
- (d) same state, different action: "1,0,1>9,9;1,0,1>9,9" (act=1; no
  rule with act=1; coherent; new rule; must not touch verified answers).
- (e) slow burn: alternate (b) with corroborating "1,0,0>1,0" episodes.

Verified answers (must hold after every battery item):
- cpredict(1,0,0) yields s1=0
- cpredict(0,0,0) yields s1=1
- active rule count stays 2 (plus exactly the new rules from (c),(d))

**Kill criterion X-U2-1:** any verified answer changes, or any ACTIVE
rule's effect field changes, after the battery. Then H-UNIFIED2 KILLED.

### X-U2-2: Quarantine denial of service

**X-U2-2a (poison-first ordering):** reverse the K-U2-1 order. Feed the
interfering item FIRST ("1,0,0>9,9;1,0,0>9,9"), then feed the legitimate
episodes ("1,0,0>1,0;1,0,0>1,0").

**Downgrade criterion X-U2-2a:** the legitimate episodes are quarantined
(committed 0) AND cpredict(1,0,0) yields s1=9. Then the gate is
order-dependent first-writer-wins protection, not veracity-dependent
protection: whoever reaches the unlabeled stream first wins permanently,
and true evidence arriving later is quarantined with no recovery path.
H-UNIFIED2 DOWNGRADED (frozen bars intact; generalization fails for
adversarial ordering, which matters on an unlabeled stream).

**X-U2-2b (capacity flood):** fill all 16 causal rule slots with coherent
junk (16 distinct novel (s0,act) states, e.g. s0=10..25, act=0), then
attempt legitimate novel learning (s0=99, act=0).

**Downgrade criterion X-U2-2b:** the legitimate novel rule is silently
dropped (no new rule; cpredict(99,0,0) withholds) after the flood.
H-UNIFIED2 DOWNGRADED on capacity liveness (verified knowledge intact;
claim does not promise capacity, so this is a boundary downgrade).

**X-U2-2c (contradictory flood control):** after truth-first learning,
flood 50 contradictory episodes. Expect: all quarantined, verified
answers intact, coherent novel learning still commits.

**Pass criterion X-U2-2c:** verified answers intact AND a subsequent
coherent novel episode commits. This is the control showing quarantine
itself is flood-proof; it does not save X-U2-2a/b.

### X-U2-3: AMBIGUOUS gaming

Battery through `route_line` only:
- Regression set (must NOT be 5): every learn item from the frozen
  K-U1..K-A suite: "abc>cba;xy>yx",
  "xab>xxx;xcd>xxx;abc>ccc;def>fff;abcde>eeeee",
  "0,0,0>0,1;0,0,0>0,1;1,0,0>1,0;1,0,0>1,0",
  "abc>cba;de>ed;ff>ff". Expect: 1,1,2,1 respectively.
- Over-trigger attempts (clear items that must not be 5):
  "ab>ba;cd>dc" (str>str lesson) expect 1;
  "0,0,1>0,0;2,1,0>1,1" (iii>ii) expect 2.
- Under-trigger attempts (digit-string procedure lessons):
  "12>34;56>78" expect 5; "1>2;3>4" expect 5;
  "123>321;456>654" expect 5.
- Documented case: "1,2,3>4,5;7,8,9>0,1" expect 2 (declared, not an
  attack success).

**Kill criterion X-U2-3:** any regression-set item routes 5 (a
previously store-routed learnable item now withholds). Then the
AMBIGUOUS code regresses learning. H-UNIFIED2 KILLED.

**Downgrade criterion X-U2-3:** a digit-string procedure lesson routes
to CAUS_LEARN (2) beyond the single documented case, i.e. the taxonomy
hole is bigger than declared. H-UNIFIED2 DOWNGRADED.

### X-U2-4: Source audit

- (a) grep the learning path (lines 1..1040 of unified2_learn.zag) for
  test-answer literals: "hello", "olleh", "xqw", "zzz", "ooooo", "dxc",
  "cxd", "9,9". Expect: zero in learning-path code (main-harness
  literals are allowed; the claim is about the learning machinery).
- (b) verify `caus_coherent` contains no state/action/effect constants
  (only structural offsets and comparisons).
- (c) verify the query path (handle_proc_query_unified,
  handle_caus_query) is byte-identical to f5dd7cdc7 (diff empty on those
  function bodies).
- (d) verify prereg commit bfd5bcb13 strictly precedes the
  implementation commit (already checked: ancestor OK; re-verify at
  report time).

**Kill criterion X-U2-4:** hardcoded test answers in learning-path
code, or query-path drift vs f5dd7cdc7. H-UNIFIED2 KILLED.

## Verdict rule

- Any KILL criterion met: H-UNIFIED2 KILLED.
- Any DOWNGRADE criterion met (no kill): H-UNIFIED2 DOWNGRADED, with the
  frozen 12/12 bars recorded intact and the generalization failure
  specified.
- All attacks fail: H-UNIFIED2 SURVIVES this red team.

## Honest limitations (declared before running)

1. The red team uses the same toolchain and the same library code as the
   builder; a shared blind spot in `clearn` semantics would be shared.
2. X-U2-2a attacks the threat model (adversarial ordering), not the
   frozen K-U2-1 bar; a downgrade here does not dispute the frozen replay.
3. No Python. Pure Zag. No em dashes in docs.
