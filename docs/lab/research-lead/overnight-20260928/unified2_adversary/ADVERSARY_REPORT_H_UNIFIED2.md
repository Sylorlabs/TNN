# Adversary Report: H-UNIFIED2 Red Team (X-U2-1..X-U2-4)

**Date:** 2026-09-29
**Target:** H-UNIFIED2 SURVIVES (12/12), `unified2_learn.zag` (commit 0eb7677fe)
**Prereg:** unified2_adversary/PREREG_U2_ADVERSARY.md (commit 4d9b05302, frozen before execution)
**Stance:** Assumed false. Attacked the composition.
**Toolchain:** /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc (2026.07.0-dev)
**Purity:** Pure Zag. No Python anywhere. All attacks deterministic 3/3 (byte-identical via cmp).

## Verdict: H-UNIFIED2 DOWNGRADED (two downgrades, no kill)

No kill criterion was met. Two downgrade criteria were demonstrated as
frozen. The frozen 12/12 bars (K-U2-1..K-U2-4) still pass unchanged; the
downgrades concern the GENERALIZATION of the repair, not the frozen
instances. Lineage is preserved: the SURVIVES verdict on the frozen
items stands, and is now bounded by this report for the general claim.

## X-U2-1: Quarantine bypass -> no bypass found (7/7)

Battery through the gated `handle_caus_learn`, truth-first order:
(a) original U-A2 replay: 0 committed, 2 quarantined;
(b) near-miss "1,0,0>9,8": 0 committed;
(c) novel state "2,0,0>9,9": 2 committed, new rule, active 3;
(d) same state different action "1,0,1>9,9": 2 committed, active 4;
(e) slow burn contradict-then-corroborate: 0 then 2 committed;
(f) ns0-differing coherent episode: 2 committed, no rule touched;
(g) s1-varied contradictory episode: 0 committed.
Verified answers (cpredict(1,0,0)->s1=0, cpredict(0,0,0)->s1=1) intact
after every item. No ACTIVE rule's effect field changed.

Analysis: the gate's match condition is exactly the superset of
`clearn`'s conflict condition over the same slot order, so any episode
`clearn` would use to mark an ACTIVE rule CONFLICTED is quarantined
first. For truth-first ordering the gate is sound. X-U2-1 kill
criterion not met.

## X-U2-2a: Poison-first ordering -> DOWNGRADE (criterion met as frozen)

Reversed the K-U2-1 order. Fed "1,0,0>9,9;1,0,0>9,9" FIRST: route 2,
2 committed, 1 active rule (IF s0==1 AND a==0 THEN s1:=9). Then fed the
legitimate "1,0,0>1,0;1,0,0>1,0": route 2, 0 committed, 2 quarantined.
cpredict(1,0,0) now yields s1=9.

The gate protects ACTIVE rules without provenance: it cannot
distinguish legitimate-first from poison-first. Whoever reaches the
unlabeled stream first wins permanently, and true evidence arriving
later is quarantined with no recovery path (the prereg's honest
limitation 1 makes the quarantine permanent through the stream).
The repair provides order-dependent first-writer-wins protection, not
veracity-dependent protection. On a genuinely unlabeled stream with no
trusted initial phase, this is the same silent-replacement failure mode
as U-A2 with the order reversed. DOWNGRADE, not kill: the frozen K-U2-1
replay (truth-first) still passes.

## X-U2-2b: Capacity flood -> DOWNGRADE (criterion met as frozen)

Truth-first (2 rules), then 14 distinct novel coherent states
(s0=10..23): 28 committed, active count 16 (CR_MAX). Then legitimate
novel "99,0,0>0,1;99,0,0>0,1": handler reports 2 committed, 0
quarantined, but active count stays 16 and cpredict(99,0,0) withholds.
The legitimate rule was silently dropped by `clearn`'s full-store
early return, while the handler reported success.

Two findings: (1) the 16-slot causal store is fillable with coherent
junk, after which legitimate novel learning is silently lost; verified
knowledge is intact, so this is a liveness/capacity boundary, not
corruption. (2) The handler's committed count is dishonest on a full
store: it counts episodes handed to `clearn`, not rules actually
stored. DOWNGRADE (boundary): the claim does not promise capacity, but
a continuing learner that silently drops learning while reporting
success has a real observability hole.

## X-U2-2c: Contradictory flood control -> PASS

50 contradictory episodes after truth-first learning: 0 committed, 50
quarantined, active count 2, verified answers intact, and a subsequent
coherent novel episode commits normally (active 3). The quarantine
mechanism itself is flood-proof: it stores nothing, so there is no
quarantine store to overwhelm. The X-U2-2a exploit works by seeding,
not by overwhelming.

## X-U2-3: AMBIGUOUS gaming -> no gaming found (15/15)

Route battery: all six frozen learn/query items keep their store
routes (1,1,2,1,3,4); clear str>str and iii>ii items never route 5;
all four digit-string procedure lessons route 5; the documented
"1,2,3>4,5;7,8,9>0,1" routes 2 as declared; mixed int/str withholds 0.
The code-5 branches only relabel previous silent-WITHHOLD branches;
no store routing changed, so the signal cannot be gamed into
misrouting. Repair 2 is an honest labeling change. Neither the kill
nor the downgrade criterion was met.

## X-U2-4: Source audit -> PASS

(a) Zero test-answer literals ("hello", "olleh", "xqw", "zzz",
"ooooo", "dxc", "cxd", "9,9", "1,0,0", "321>123", "12321") in the
learning path (unified2_learn.zag lines 1..1040). (b) `caus_coherent`
contains no state/action/effect constants, only structural offsets and
comparisons. (c) Query path (`handle_proc_query_unified`,
`handle_caus_query`) byte-identical to f5dd7cdc7 (diff empty).
(d) Prereg commit bfd5bcb13 strictly precedes implementation
(ancestor check OK at report time).

## Harness corrections (transparent)

During execution three harness bugs were found and fixed before the
final runs (attack intent unchanged; prereg criteria unchanged):
single-segment items do not route to CAUS_LEARN (router requires
nseg>=2), so battery items (e),(f),(g), the 2b flood, and the 2c novel
probe were rebuilt as 2-segment items. The first X-U2-1 run also
confirmed the router behavior the attacks depend on. All reported
numbers are from the corrected harnesses, deterministic 3/3.

## Artifacts

- unified2_adversary/PREREG_U2_ADVERSARY.md (frozen prereg)
- unified2_adversary/u2lib.zag (library portion, unified2_learn.zag lines 1..1040)
- unified2_adversary/attackN_main.zag and assembled attack_u2N.zag (N=1,2a,2b,2c,3)
- unified2_adversary/run_u2N_{a,b,c}.txt (3 deterministic runs each)
- unified2_adversary/ADVERSARY_REPORT_H_UNIFIED2.md (this file)

Binaries (attack_u2N) are NOT committed.

## Bottom line

Repair 1's coherence gate is sound for its frozen threat model
(truth-first): no bypass exists through the gated path, and the
quarantine itself cannot be flooded. But the protection is
order-dependent rather than veracity-dependent: poison that arrives
first becomes the "verified" knowledge and the truth is then
quarantined permanently (X-U2-2a), and the 16-slot store can be filled
with coherent junk that silently drops later legitimate learning while
the handler reports success (X-U2-2b). Repairs 2 and 3 show no
gameability. The learning machinery is clean of hardcoded answers and
the query path is unchanged. Recommended: a provenance or trust
distinction for the gate (or an explicit revision channel with
authority, H-REVISE2), honest committed-vs-stored accounting on a full
store, and capacity policy for the continuing learner.
