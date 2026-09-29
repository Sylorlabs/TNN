# Adversary Report: H-UNIFIED Red Team (U-A1..U-A5)

**Date:** 2026-09-29
**Target:** H-UNIFIED SURVIVES (9/9), unified_learn.zag (commit f5dd7cdc7)
**Prereg:** PREREG_UNIFIED_ADVERSARY.md (commit 1498235e7, frozen before execution)
**Stance:** Assumed false. Attacked the composition.
**Toolchain:** /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
**Purity:** Pure Zag. No Python anywhere. All attacks deterministic across
3 runs (byte-identical via cmp); diagnostic probe deterministic across 2 runs.

## Verdict: H-UNIFIED KILLED by U-A2 (compositional interference)

One kill criterion was met as frozen. Three downgrades confirmed. One attack
found nothing. The frozen 9/9 bars (K-U1..K-U5, K-A) still pass unchanged;
the kill concerns the GENERALIZATION of K-U5, not the frozen instances.
Lineage is preserved: the original SURVIVES verdict on the frozen items
stands, and is now superseded for the general claim by this report.

## U-A1: Router gaming -> DOWNGRADE (no kill)

Results (deterministic):
- A1a "321>123;654>456" (digit-string reverse lesson) -> WITHHOLD.
- A1b "1,2,3>4,5;7,8,9>0,1" (format-ambiguous) -> CAUS_LEARN, silently.
- A1c "12321" (digit-string query) -> WITHHOLD, not PROC_QUERY.
- A1f "12>34;56>78" (int pairs) -> WITHHOLD.
- Controls A1d/A1e route correctly (PROC_LEARN / CAUS_LEARN).

No well-formed str>str lesson was sent to a wrong store and no well-formed
iii>ii item was sent to PROC_LEARN, so the kill criterion was not met.
Downgrade: the authored format taxonomy silently excludes an entire task
class (procedures over digit strings: lessons and queries are unroutable)
and silently commits format-ambiguous items to one store with no ambiguity
signal. "Structure-inferred" routing is really "format-taxonomy" routing,
and the taxonomy has holes the designer did not enumerate.

## U-A2: Interference -> KILL (criterion met as frozen)

Trace (deterministic):
1. Genuine causal episodes learned via the frozen router path
   (route_line -> CAUS_LEARN -> handle_caus_learn). Verified:
   cpredict(1,0,0) yields s1=0 (the frozen K-U3 answer).
2. Interfering item "1,0,0>9,9;1,0,0>9,9": route_line returns CAUS_LEARN
   under the frozen router rules (no label trick; the harness routes exactly
   as the unified main would). handle_caus_learn marks R1 CONFLICTED and
   learns spurious R2 (IF s0==1 AND a==0 THEN s1:=9).
3. Re-check: cpredict(1,0,0) now yields s1=9. The previously verified answer
   changed.

The frozen kill criterion (previously verified answer changes after a
format-valid interfering item) is met. Verdict: KILL.

Scope and steelman, stated honestly:
- The causal learner in isolation behaved as designed: contradictory
  episodes -> mark conflicted -> learn new rule. That mechanism was
  validated under H-CAUSAL and is not the defect.
- The defect is compositional: H-UNIFIED promises an UNLABELED stream with
  no interference (K-U5), but its demultiplexer is format-only and the
  formats collide (U-A1 A1b). The causal store's revision policy assumes all
  iii>ii items are evidence about one causal system, an assumption the
  composition never re-examined.
- The result is worse than withholding: verified knowledge was not just
  lost, it was REPLACED. The learner now confidently asserts s1=9 where it
  previously (correctly) asserted s1=0. For a continuing learner this is
  silent catastrophic forgetting through format collision.
- The frozen K-U5 instances still pass; the property does not generalize.

Repair direction (not implemented by this adversary): the router must not
silently commit format-ambiguous items (ambiguity signal or withhold), or
stores need cross-item coherence gating before revision. Fixing the causal
revision policy itself would be fixing the wrong layer.

## U-A3: Bridge trigger misfire -> DOWNGRADE (no kill)

Item "abc>cba;de>ed;ff>ff" (route -> PROC_LEARN):
- "ff>ff" fails pextract ('f' occurs twice), so allok=0 and Step 2 (direct
  discovery) is vetoed for the whole item even though the extractable
  subset {"abc>cba","de>ed"} is directly discoverable (verified: fresh
  workspace, direct slot 0, probe "dxc" -> "cxd").
- Bridge fired (rc=1000): IF input[0]==97 THEN proc0 ELSE proc1.
- Diagnostic probe: THEN("axyzb")="bzyxa", ELSE("hello")="olleh". Both
  branches are reverse-equivalent programs.

The frozen kill criterion required behavioral divergence; outputs agree on
the probe, so: DOWNGRADE, not kill. The finding is real regardless: a single
unextractable pair vetoes direct discovery for all pairs, and the bridge
then burns 2 proc slots plus 1 bridge rule to relearn (with a spurious
condition) what direct discovery would have learned in 1 slot. The trigger
logic conflates "extraction failed" with "direct discovery impossible",
which is false for the extractable subset.

## U-A4: Query ambiguity -> DOWNGRADE (declared limitation, now exhibited)

- After learning reverse (slot 0) and broadcast-last (slot 1), query "abc"
  reports 2 conflicting outputs ("cba", "ccc") with no ranking or intent
  signal.
- Bridge-amplified case: query "xqw" with a bridge rule plus two direct
  slots reports 4 outputs ("xxx", "www", "wqx", "xxx"), including a
  duplicate ("xxx" twice), with no way to select.

This is declared limitation 3 of the H-UNIFIED prereg, so DOWNGRADE, not
kill. The contribution is the concrete exhibit inside the unified
composition: contradictory and duplicated answers are the NORMAL output of
the query path once more than one procedure is stored, and the composition
adds no disambiguation.

## U-A5: Source audit -> PASS (no finding)

Audited the learning path (unified_learn.zag lines 1..977, everything except
the main harness):
- Zero occurrences of test-answer literals ("hello", "olleh", "xqw",
  "zzz", "ooooo") in learning-path code.
- "abc"/"cba" appear only inside the word "cbase" in a memory-layout
  comment.
- Numeric literals 97/100/120: only inside 1200 (buffer sizes) and 1000
  (bridge return-code offset, structural). No byte-valued condition
  constants.
- All emit strings are structural trace labels. All char comparisons are
  ASCII structural (59=';', 62='>', 44=',', 48..57=digits).
- No test-tuned branches or magic constants in route_line, pextract,
  pdiscover_direct/dry, try_discover_pass, bridge_learn, bridge_apply,
  clearn, cpredict, proc_apply, or the handlers.

The learning machinery contains no hardcoded test answers. U-A5 passes.

## Artifacts

- unified_adversary/PREREG_UNIFIED_ADVERSARY.md (frozen prereg)
- unified_adversary/ulib.zag (library portion, unified_learn.zag lines 1..977)
- unified_adversary/attack_uN_main.zag and assembled attack_uN.zag (N=1..4)
- unified_adversary/run_uN_{a,b,c}.txt (3 deterministic runs each)
- unified_adversary/probe_u3.zag, probe_u3_main.zag, probe_u3_{a,b}.txt
- unified_adversary/ADVERSARY_REPORT_H_UNIFIED.md (this file)

Binaries (*.zag build outputs, probe_u3, attack_uN) are NOT committed.

## Bottom line

H-UNIFIED's 9 frozen bars survive, but the composition has a fatal
generalization flaw: the unlabeled demultiplexer admits format-colliding
items that silently destroy and replace verified knowledge in another
store (U-A2 KILL). Additionally the router cannot see digit-string
procedure tasks (U-A1), the bridge trigger wastes structure on an
extraction veto (U-A3), and queries multiply contradictory answers with no
intent (U-A4). The learning core itself is clean of hardcoded answers
(U-A5). Recommended: fix the compositional interference (router ambiguity
signal or coherence-gated revision) before any further integration claims.
