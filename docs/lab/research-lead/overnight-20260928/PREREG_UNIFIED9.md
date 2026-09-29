# H-UNIFIED9 Preregistration: merit-threshold eviction for the unified causal store (FROZEN)

**Date:** 2026-09-29
**Status:** FROZEN. Committed alone before any implementation edit, build, or run.
**Lineage:** `unified9_learn.zag` will be built as a verbatim copy (cmp-verified)
of the committed `unified8_learn.zag`, plus exactly the R10 change set below.
`unified8_learn.zag` will not be modified.

## Hypothesis

H-UNIFIED9: the unified learner's causal store can replace refuse-with-warning
capacity handling with the H-MEM5 merit-threshold eviction policy, so the
continuing learner never stops learning, without breaking any of the 22
surviving H-UNIFIED8 behaviors except the explicitly superseded K-U3-2
refuse-on-full contract.

This is the integration step the H-UNIFIED5 result explicitly deferred:
"Capacity remains refuse-with-warning; principled eviction is H-MEM lane
future work" and "a dedicated eviction-policy hypothesis (H-MEM lane)".
The H-MEM lane has since delivered H-MEM5 (SURVIVES 4/4, merit threshold
uses>=2, no grace). H-UNIFIED9 ports that policy into the unified causal
store. Classification target: bounded L2 integration repair. Not L3.

## The repair (R10, exact spec)

1. New workspace words:
   - `CMETA() = 1552`: 16 slots x 8 bytes of eviction metadata. Per slot:
     +0 `uses` (i32), +4 `bseq` (birth store-clock, i32). Region 1552..1680
     is free (causal store ends at 1552, work starts at 2048).
   - `CSEQ() = 65012`: causal store clock (i32). Advances ONLY when a new
     rule is stored (including via eviction). Corroborations, conflicts,
     and queries do not advance it.
   - `ECOUNT() = 65016`: cumulative evicted-rule counter (i32).
   - `CPROB() = 32`: merit youth window, in store-clock units. Adaptation
     note: H-MEM5 uses PROB=10 on a query clock for 8 slots; here the
     window is two full store turnovers (2x16) on the store clock, so a
     burst fill does not instantly age out the first-written rules.
   - `CMERITK() = 2`: merit threshold, ported unchanged from H-MEM5.
2. `cr_set` initializes `uses=0`, `bseq=CSEQ` for the (re)stored slot.
3. A rule is "exercised" (uses++) when: a learn episode corroborates it
   (clearn rc=0 path), a learn episode conflicts it (rc=2 path), or a query
   predicts through it (cpredict hit path). Definition disclosed here.
4. `clearn`, no free slot: instead of returning -1, select a victim:
   a. dead first: lowest-index slot with status=2 (CONFLICTED). Such slots
      never match in clearn/cpredict/coherence, so evicting them is safe.
   b. merit: among ACTIVE (status=0) slots with `cm_elig==1`, lowest uses,
      tie -> lowest slot index.
   c. fallback (none eligible: every slot young and merit>=2): lowest uses
      ignoring protection, tie -> lowest slot. Precedent: H-MEM5
      FALLBACK-ALL-PROTECTED. The learner never refuses.
   `cm_elig(slot)`: 0 (not eligible, i.e. protected) iff the slot is used,
   status==0, `CSEQ < bseq+CPROB` (young), and `uses >= 2`. Otherwise 1.
   Dead (status!=0) slots are always eligible. There is no grace: a
   newcomer with 0 or 1 uses is evictable immediately (H-MEM5 R2/R4).
5. Eviction emits a loud white-box trace naming the victim slot, its rule,
   its uses count, and the incoming episode; the fallback adds an
   explicit FALLBACK marker. ECOUNT++. The victim slot is re-stored via
   cr_set (metadata reset). clearn returns 3 (STORED_VIA_EVICT).
   The old -1 path is kept as defensive dead code only.
6. Handlers: `rc==3` counts as stored (it changed store state). Per-call
   eviction counts are reported in the ULEARN/UREVISE trace lines.
   The USTOREFULL branches are kept as defensive dead code.
7. The H-UNIFIED5 capacity-policy comment block is superseded by an R10
   comment block. Doc-only.

## Explicit non-goals

- No change to parse_ints, field_kind, route_line, operator_route,
  the proc/bridge path, or the coherence gate.
- No change to the 16-rule capacity itself.
- Router7 family-audit and revise7 provisional revisions are separate
  lanes and are not ported here.

## Frozen kill bars

- **K-U9-1 (eviction replaces refusal; SUPERSEDES K-U3-2):** fresh W; fill
  16 slots with 8x `handle_caus_learn("1<0+2k>,0,0>0,1;1<1+2k>,0,0>0,1")`
  for k=0..7 (s0 = 10..25, all uses=0). Record DCOUNT/ECOUNT. Then
  `cap_rc = handle_caus_learn(W,"99,0,0>0,1;99,0,0>0,1")`. PASS iff:
  cap_rc==1, DCOUNT delta==0, ECOUNT delta==1, caus_active_count==16,
  cpredict(99,0,0) fires with s1==1, cpredict(10,0,0)==0 (R0 evicted:
  all young+meritless, argmin-uses tie -> slot 0), cpredict(11,0,0)==1
  (R1 survives). A UEVICT trace naming R0 with uses=0 must appear in raw
  output (grep-verified).
- **K-U9-2 (merit protection is load-bearing):** fresh W; fill as above;
  then `handle_caus_learn(W,"10,0,0>0,1;10,0,0>0,1")` (two corroborations:
  R0 uses=2; R0 is young: bseq=1, clock=16, 16<33). Then
  `handle_caus_learn(W,"99,0,0>0,1")`. PASS iff: returns 1, ECOUNT
  delta==1, cpredict(11,0,0)==0 (victim is slot 1, NOT the null-policy
  victim slot 0), cpredict(10,0,0)==1 with s1==1 (merit rule survives),
  cpredict(99,0,0)==1. UEVICT names R1.
- **K-U9-3 (conflicted-first):** fresh W; fill as above; then
  `handle_caus_revise(W,"!17,0,0>0,9")` (marks R7 CONFLICTED, returns 1);
  then `handle_caus_learn(W,"99,0,0>0,1")`. PASS iff: returns 1, ECOUNT
  delta==1, cpredict(17,0,0)==0 (dead rule evicted first), UEVICT names
  R7, cpredict(99,0,0)==1, caus_active_count==16.
- **K-U9-4 (all-protected fallback):** fresh W; fill as above; then
  cpredict-hit every slot twice (s0=10..25, 32 queries, uses=2 each,
  clock stays 16, all slots young: clock 17 < bseq+32 for all).
  Then `handle_caus_learn(W,"99,0,0>0,1")`. PASS iff: returns 1, ECOUNT
  delta==1, cpredict(10,0,0)==0 (fallback evicts slot 0: argmin uses tie),
  cpredict(99,0,0)==1, and a UEVICT-FALLBACK trace appears (grep).
- **K-U9-5 (no regression):** all other 22 frozen checks from the
  H-UNIFIED8 battery PASS unmodified (21 preserved pre-K-U8-1 blocks
  plus K-U8-1). Battery total: 26/26.
- **K-U9-6 (determinism):** 3/3 runs byte-identical (cmp), exit 0.

FAIL on any bar = hypothesis fails (repair or kill per loop rules).
K-U3-2 (refuse-with-warning) is SUPERSEDED by K-U9-1, not deleted from
history: the old contract is preserved in UNIFIED8_RESULT.md.

## Method

- Pure Zag throughout: no Python at any stage, including analysis and
  verification. Shell only for build orchestration, grep, cmp, md5sum,
  and git.
- Toolchain: /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
- Builds in /tmp/u9 only. No binaries committed.
- Only owned paths staged: PREREG_UNIFIED9.md (this file, alone, first),
  then unified9_learn.zag, UNIFIED9_RAW_OUTPUT.txt, UNIFIED9_RESULT.md.
  No broad git add. Concurrent workers untouched.

## Governance disclosures

- H-MEM5's independent red team was still pending when this port was
  designed. If that red team breaks the MEM5 policy, this port inherits
  the breakage and must be revisited. The port is of the policy as
  frozen in mem5_learn.zag (MERITK=2, no grace, elig structure,
  fallback-evict precedent); CPROB=32 and the store-clock are H-UNIFIED9
  adaptations, disclosed above.
- Eviction can retire a rule that was blocking a contradictory episode
  at the coherence gate; a later identical episode would then learn
  fresh. This is the disclosed cost of never refusing: retention must
  be earned (uses>=2). The UEVICT trace makes every retirement loud.
- Window expiry beyond 32 stores is not isolated in the frozen battery;
  the independent red team should probe long-horizon aging behavior.
- No em dashes in loop documentation.
