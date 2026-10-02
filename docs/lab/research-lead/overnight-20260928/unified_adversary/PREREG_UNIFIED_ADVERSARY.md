# Prereg: H-UNIFIED Adversary (U-A1..U-A5)

**Date:** 2026-09-29
**Status:** FROZEN before execution
**Target:** H-UNIFIED SURVIVES (9/9), commit f5dd7cdc7 (unified_learn.zag)
**Stance:** Assume the claim is false. Attack the composition, not just the parts.

## What H-UNIFIED claims

One process, unlabeled stream, no reset. Structure-inferred routing plus
direct procedure discovery with bridge fallback plus causal learning plus
queries. Kill bars K-U1..K-U5 plus K-A all passed on the frozen test items.

## What the parts already concede (not attackable as kills)

- Routing predicates are authored structure checks (declared limitation 1).
- Bridge conditions are single (pos,val) equality (declared limitation 2).
- Procedure queries report every stored slot and rule; no intent selection
  (declared limitation 3).

A finding that restates a declared limitation is a DOWNGRADE at most, unless
it breaks a frozen bar as written.

## Attacks

### U-A1: Router gaming (misleading structural cues)

The router (route_line) classifies items by byte format only:
2+ str>str segs -> PROC_LEARN; 2+ iii>ii segs -> CAUS_LEARN;
bare string -> PROC_QUERY; 3-int tuple -> CAUS_QUERY; else WITHHOLD.

Adversarial inputs (frozen):
- A1a: "321>123;654>456" (digit-string reverse lesson; semantically a
  procedure lesson, but no segment is str>str under field_kind).
- A1b: "1,2,3>4,5;7,8,9>0,1" (format-ambiguous: valid procedure lesson on
  numeric strings AND valid causal episodes).
- A1c: "12321" (digit-string procedure query; field_kind = 1, not -1).

Kill criterion: KILL iff a well-formed 2+ str>str procedure lesson routes to
CAUS_LEARN, or a well-formed 2+ iii>ii causal item routes to PROC_LEARN
(wrong store). DOWNGRADE iff valid procedure lessons on digit strings are
WITHHELD (A1a, A1c) or format-ambiguous items are silently committed to one
store with no ambiguity signal (A1b).

### U-A2: Interference via format ambiguity (store corruption)

1. Learn genuine causal episodes:
   "0,0,0>0,1;0,0,0>0,1;1,0,0>1,0;1,0,0>1,0" via handle_caus_learn.
   Verify cpredict(1,0,0) yields s1=0 (the K-U3 answer).
2. Feed interfering item I = "1,0,0>9,9;1,0,0>9,9".
   Verify route_line(I) == 2 (CAUS_LEARN) under the frozen router rules,
   then handle_caus_learn(I).
3. Re-run cpredict(1,0,0).

Kill criterion: KILL iff the previously verified causal answer changes
(WITHHOLD or different value) after the format-valid interfering item.
The item is routed by the frozen router's own rules; no label trick is used.
Rationale: in an unlabeled stream the learner cannot distinguish "new
evidence about the same causal system" from "foreign data in causal
clothing". Silent corruption breaks no-interference as a general property
(K-U5 tested only two frozen instances).

### U-A3: Bridge trigger misfire (extraction veto)

bridge_learn Step 2 runs direct discovery ONLY if every pair extracted
(allok==1). One unextractable pair vetoes direct discovery for all pairs,
and Step 3 then searches splits over the extractable subset only.

Adversarial item T = "abc>cba;de>ed;ff>ff":
- "ff>ff" fails pextract ('f' occurs twice in input, cnt != 1), so allok=0.
- The extractable subset {"abc>cba","de>ed"} is jointly direct-discoverable
  (same shape as frozen K-U1, which found reverse).
- Predicted bridge behavior: split on pos 0, v=97 ('a'): side {abc>cba}
  dry-runs to reverse-equivalent (n-k-1), side {de>ed} dry-runs to
  broadcast-last (n-1). Bridge learns IF input[0]==97 THEN reverse
  ELSE broadcast-last.
- Probe "dxc": bridge ELSE branch gives "ccc"; the vetoed direct program
  (reverse) gives "cxd".

Procedure: verify route_line(T)==1; run handle_proc_learn_unified on T and
record rc; independently run handle_proc_learn_unified on "abc>cba;de>ed"
in a fresh workspace and record rc2; compare bridge_apply(bslot,"dxc")
against proc_apply(direct_slot,"dxc").

Kill criterion: KILL iff rc>=1000 (bridge fired) AND rc2 in 0..15 (direct
would have succeeded on the extractable subset) AND the two probe outputs
differ (behavioral divergence). DOWNGRADE iff bridge fired and direct would
have succeeded but outputs agree (spurious structure, wasted slots).

### U-A4: Query ambiguity (no procedure intent)

Setup: learn reverse from "abc>cba;xy>yx" (slot 0); learn broadcast-last
from "abc>ccc;def>fff" (slot 1). Query "abc" via
handle_proc_query_unified. Also exhibit the bridge-amplified case from the
frozen K-U2 setup: query "xqw" after the bridge rule exists (reverse slot
gives "wqx", bridge rule gives "xxx").

Criterion: DOWNGRADE iff two or more conflicting outputs are reported with
no ranking or intent signal. (Declared limitation 3, so DOWNGRADE not KILL;
the contribution is a concrete contradictory-output exhibit inside the
unified composition.)

### U-A5: Source audit (hardcoded answers)

Static audit of the learning path (unified_learn.zag lines 1..977,
everything except the main test harness) for literals or branches keyed on
frozen test data: "hello", "olleh", "xqw", "zzz", "ooooo", "abc", "cba",
"de", numeric literals 97/100/120 used as condition constants, and any
other test-tuned magic constants in route_line, pextract, pdiscover_*,
try_discover_pass, bridge_learn, bridge_apply, clearn, cpredict,
proc_apply, or the handlers. The main harness (lines 978+) legitimately
contains test strings.

Kill criterion: KILL iff a learning-path function contains a test-answer
literal or a branch conditioned on test-specific data. Each grep hit will
be individually inspected and judged in the report.

## Verdict rule

- Any KILL criterion met -> H-UNIFIED KILLED (with the successful attack
  named) or DOWNGRADED per the criterion.
- Findings that restate declared limitations -> DOWNGRADE with concrete
  exhibits, preserving the original SURVIVES verdict on the frozen bars.
- All attacks executed as preregistered, deterministic (3 runs,
  byte-identical via cmp), pure Zag, no Python.

## Commit order

This prereg is committed BEFORE any attack implementation or execution.
