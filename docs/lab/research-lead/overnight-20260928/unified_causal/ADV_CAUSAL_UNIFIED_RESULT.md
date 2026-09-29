# Adversary Report: H-CAUSAL-UNIFIED Red Team

**Date:** 2026-09-29
**Adversary:** H-CAUSAL-UNIFIED Red Team
**Target:** H-CAUSAL-UNIFIED SURVIVES (28/28), commit ba065e172
**Prereg:** PREREG_CAUSAL_UNIFIED_ADV.md (frozen ae0c3e0d0 before execution)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python. Determinism via cmp/md5sum (shell).

## Verdict: H-CAUSAL-UNIFIED DOWNGRADED

Two kill criteria met (X-CU1, X-CU2). One downgrade (X-CU4 doc error).
The 28/28 frozen bars still pass, but the provenance query (K-CU3) is
buggy and contest capacity fails silently. The "decorative provenance
repaired" claim is invalid.

## X-CU1: Provenance Gaming — KILL (criterion met)

**Finding:** The `caus_hist` query reports a superseded count that does
not match the SUPERSEDED entries in its own hypotheses listing.

**Evidence (unified_causal/run_a.txt, frozen test output):**
- Hypotheses listing shows 4 entries with status=SUPERSEDED:
  H2 (action=2 cond=[any]), H6 (action=2 cond=[s0=2]),
  H7 (action=2 cond=[s0=2&s2=0]), H8 (action=2 cond=[s0=2&s2=1])
- CAUSHIST line reports: `superseded=2 open_contests=0`
- Count of `status=SUPERSEDED` in run_a.txt: 4
- Reported superseded: 2

**Root cause (unified_causal.zag line 2111-2119):**
```
fn fu_hist_count(W:[]u8)i32 {
  list_hypos(W);  // displays ENTRIES with ST_SUPER
  let n:i32=0;
  let i:i32=0;
  while(i<nep(W)){
    if(ep_st(W,i)==EP_SUP()){n=n+1;}  // counts EPISODES with EP_SUP
    i=i+1;
  }
  return n;
}
```
The function displays entries (hypotheses) but counts episodes
(observations). These are different stores. The result doc claims
"showing H2 and H6 with status=SUPERSEDED" but omits H7 and H8, and
the returned count (2) matches neither the displayed superseded
entries (4) nor the doc description.

**Impact:** A user querying provenance sees 4 superseded hypotheses
but is told superseded=2. The provenance is misleading. K-CU3
("queryable provenance") does not meet its stated bar.

## X-CU2: Contest Flooding — KILL (criterion met)

**Finding:** When contest capacity (8) is reached, additional
contradictions are silently dropped. No contest opened, no error
emitted, the conflicting evidence vanishes.

**Evidence (adversary test, 3/3 byte-identical, md5 9b61c631946d23b76a67cc99ffa36f11):**
- Fed contradictions at 10 distinct states (each: two episodes with
  same state/action, different outcomes)
- States 1-8: contests opened, nct=1..8, open_contests=1..8
- State 9 (2,0,0): nct_before=8, nct_after=8. No contest opened.
  Output: "X-CU2 CONFIRMED: 9th contradiction silently dropped"
- State 10 (2,0,1): nct_before=8, nct_after=8. No contest opened.
  Output: "X-CU2 CONFIRMED: 10th contradiction silently dropped"
- Query Q(2,0,0,2) on the dropped state: r=1, pred=(1,1,0).
  Confident prediction despite the contradictory evidence being lost.

**Root cause (unified_causal.zag line 1893-1901):**
```
let c:i32=find_contest(W,i,s0,s1,s2);
if(c<0){
  c=new_contest(...);  // returns -1 when c>=8 (line 1673)
} else {
  contest_feed(W,c,e,seq);
}
return;  // c=-1 silently ignored, contradiction dropped
```
The caller does not check for new_contest returning -1. The
contradiction is lost without trace.

**Impact:** Violates the K-CU5 guarantee of "explicit contest plus
withhold." Under flood, the mechanism silently loses evidence and
then issues confident predictions on states where it discarded
contradictions. This is worse than the U-A2 silent replacement it
was meant to fix: at least U-A2 was on a known-vulnerable path.

## X-CU3: Capacity Reduction — DOWNGRADE (partial, related to X-CU2)

**Finding:** The 8-contest cap has silent failure (see X-CU2). The
32-entry cap was not reached in adversary testing (nent=5 after
10 contradictions). The entry cap failure mode was not fully
characterized.

**Note:** new_entry returns -1 at 32 entries. The split_attempt caller
was not audited for -1 handling in this red team. The contest cap
bug (X-CU2) is confirmed; the entry cap remains untested at boundary.

## X-CU4: Source Audit — DOWNGRADE (documentation error, port faithful)

**Finding:** The "127 machinery functions" claim is wrong. The port
itself is faithful.

**Evidence:**
- Original causal_learn.zag: 129 functions
- Missing from unified: i64s, load_obs, parse_int (3 functions)
- Shared: 126 functions (129-3), not 127 as claimed
- Of 126 shared: 120 byte-identical modulo whitespace
- 3 cosmetic: e64 (i64s->i32s, since i64s not ported), get32/set32
  (param renamed i->off, whitespace)
- 2 extraction artifacts: emit_fx, list_hypos (trailing section
  comments captured by extraction script, not function body changes)
- 1 intentionally replaced: main (unified learner main, expected)

**No logic changes** beyond the two allowed classes:
(a) workspace rebasing (O_* offsets gain FUBASE+3600), and
(b) capacity guards (64->32 in new_entry, 16->8 in new_contest).

**Impact:** Documentation error only. The port is faithful. DOWNGRADE
for the incorrect "127" claim, not for port infidelity.

## Classification

Bounded L2 integration with confirmed bugs. The core 28/28
functionality survives, but:
1. K-CU3 provenance query is buggy (X-CU1). The "decorative provenance
   repaired" claim is INVALID. The count must be fixed to report
   superseded entries, not episodes.
2. Contest capacity fails silently (X-CU2). The "explicit contest plus
   withhold" guarantee does not hold under flood. Must either handle
   -1 explicitly or raise capacity with a clear error.
3. Function count claim is wrong (X-CU4). Correct to 126.

## Recommended repairs

1. Fix fu_hist_count to count entries with ST_SUPER, not episodes
   with EP_SUP. Or rename to clarify it counts episodes and update
   the doc. The current behavior is misleading under either reading.
2. Handle new_contest -1: emit an explicit error/warning, or implement
   contest eviction/merging. Silent drop is unacceptable.
3. Audit new_entry -1 handling in split_attempt for the same silent
   failure class.
4. Correct "127" to "126" in the result doc.

## Artifacts

- PREREG_CAUSAL_UNIFIED_ADV.md (frozen prereg, ae0c3e0d0)
- cu_adv.zag (adversary test source, /tmp; not committed per binary rule)
- Raw evidence: cu_adv_run1.txt (md5 9b61c631946d23b76a67cc99ffa36f11),
  3/3 byte-identical via cmp

## Commits

- Prereg: ae0c3e0d0 (frozen before execution)
- This report: [to be committed]

**Purity:** Pure Zag. No Python. No em dashes in documentation.
