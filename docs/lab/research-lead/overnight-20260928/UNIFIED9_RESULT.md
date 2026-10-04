# H-UNIFIED9: RESULT (R10 merit-threshold eviction for the causal store)

**Date:** 2026-09-29
**Verdict: H-UNIFIED9 SURVIVES (26/26).** The unified learner's causal store
now evicts by merit instead of refusing when full. All four new kill bars
PASS; all 22 preserved H-UNIFIED8 checks PASS; 3/3 runs byte-identical.
Classification: bounded L2 integration repair (cross-mechanism adoption of
the H-MEM5 eviction policy). Not L3.

## Lineage (prereg strictly first)

- Prereg `PREREG_UNIFIED9.md` committed alone as `ecaa78494` before any
  implementation edit, build, or run. No amendments.
- `unified9_learn.zag` = committed `unified8_learn.zag` copied verbatim
  (cmp-verified), plus exactly the frozen R10 change set. `unified8_learn.zag`
  untouched. The committed `unified9_learn.zag` is the exact source built and
  run for the raw output below.
- Toolchain `znc 2026.07.0-dev (edition 2026)`. Builds in /tmp/u9 only.
  No binaries committed.
- Raw: `UNIFIED9_RAW_OUTPUT.txt` (md5 `7b690bc7b26940e4848e60920fcfc4e0`),
  3/3 runs byte-identical (cmp), exit 0, zero FAIL lines.
- Pure Zag throughout: no Python at any stage, including analysis and
  verification. Shell used only for build orchestration, grep, cmp, md5sum,
  diff, and git.
- Only owned paths staged: `PREREG_UNIFIED9.md` (already committed alone),
  `unified9_learn.zag`, `UNIFIED9_RAW_OUTPUT.txt`, `UNIFIED9_RESULT.md`
  (this file). Concurrent workers untouched; no broad git add.

## The repair (R10)

`clearn`, on a full 16-rule store, now selects an eviction victim instead of
returning -1. This ports the H-MEM5 policy into the causal rule base:

- Per-slot metadata at CMETA (1552): `uses` + `bseq` (birth store-clock).
- Store clock CSEQ (65012) advances only when a rule is stored. Youth
  window CPROB=32 store-clock units (two full turnovers; adaptation from
  H-MEM5's PROB=10, disclosed in prereg). Merit threshold CMERITK=2
  (ported unchanged). No grace: a newcomer with 0 or 1 uses is evictable.
- Eligibility: protected iff young AND uses>=2. Dead (CONFLICTED) slots are
  always eligible and are taken first (lowest index).
- Victim order: (a) dead slot, (b) lowest uses among eligible ACTIVE slots
  (tie: lowest slot), (c) fallback: lowest uses ignoring protection when
  every slot is protected (H-MEM5 FALLBACK-ALL-PROTECTED precedent). The
  learner never refuses.
- Merit is earned when a rule is exercised: corroborating learn, conflicting
  learn, or a query predicting through it (cpredict hit).
- Every eviction emits a loud UEVICT (or UEVICT-FALLBACK) trace naming the
  victim slot, its rule, and its uses; ECOUNT (65016) counts evictions
  cumulatively. clearn returns 3 (STORED_VIA_EVICT). Handlers count rc==3 as
  stored and report per-call evictions in ULEARN/UREVISE. The old -1/USTOREFULL
  paths are kept as defensive dead code (zero USTOREFULL traces in raw output).
- The H-UNIFIED5 capacity-policy comment is superseded by the R10 block.

## Self-caught bug during raw-output review (disclosed)

After the first build, review of the raw output showed spurious USTOREFULL
traces on non-full stores (e.g. L3 showed "2 dropped"). Root cause: a
dangling-else in my handler edit. I wrote

    if(rc==1 || rc==2 || rc==3){nstored=nstored+1;}
    if(rc==3){nevict=nevict+1;}
    else { ...USTOREFULL... }

so the else bound to the second if and rc==1/rc==2 fell into the drop
branch, corrupting ndrop/DCOUNT accounting on every store. Fixed in both
handlers to nest the evict increment inside the stored branch. Rebuilt,
reran 3/3. The committed source and raw output are from the fixed build.
The K-U3 PASS line had masked the bug (it checks predictions, not counts);
the trace review caught it. Lesson recorded: always diff preserved-section
ULEARN accounting lines against the prior raw output, not just PASS lines.

## Frozen kill-bar evidence

- **K-U9-1 PASS** (supersedes K-U3-2): 16 meritless rules filled; overfill
  `99,0,0>0,1` x2 returned 1; DCOUNT delta 0; ECOUNT delta 1; active 16;
  (99,0,0) fires s1=1; (10,0,0) gone; (11,0,0) still fires. UEVICT names
  R0 (uses=0): all young+meritless, argmin-uses tie -> slot 0.
- **K-U9-2 PASS**: R0 earned merit (2 corroborations); overfill evicted R1,
  not the null-policy victim R0. (10,0,0) still fires s1=1; (11,0,0) gone;
  (99,0,0) fires. UEVICT names R1. Merit protection is load-bearing.
- **K-U9-3 PASS**: operator revise marked R7 CONFLICTED; overfill evicted
  the dead rule first. (17,0,0) gone; (10,0,0) survives; (99,0,0) fires.
  UEVICT names R7 (uses=1, from the conflict exercise).
- **K-U9-4 PASS**: all 16 slots young with uses=2 (32 query hits, clock
  unmoved); overfill hit the fallback: UEVICT-FALLBACK names R0 (uses=2);
  (99,0,0) fires; ECOUNT delta 1. The learner never refuses.
- **K-U9-5 PASS**: all 22 preserved H-UNIFIED8 checks PASS. Output before
  the capacity block is byte-identical to UNIFIED8_RAW_OUTPUT.txt modulo
  the intentional banner change and the `, 0 evicted (H-UNIFIED9)` ULEARN
  suffix; output after the block is identical modulo the 23/23 -> 26/26
  count and the K-U3-2 -> K-U9-1..4 replacement. Zero evictions and zero
  USTOREFULL in all preserved sections.
- **K-U9-6 PASS**: 3/3 runs byte-identical (cmp), exit 0.

## Governance disclosures

- H-MEM5's independent red team was still pending when this port was
  designed. If that red team breaks the MEM5 policy, this port inherits the
  breakage and must be revisited. Ported: MERITK=2, no grace, elig
  structure, fallback-evict precedent. Adapted (H-UNIFIED9 choices):
  store-clock instead of query-clock, CPROB=32 (two turnovers), dead-first
  victim rule, uses earned via corroboration/conflict/query-hit.
- Disclosed cost: eviction can retire a rule that was blocking a
  contradictory episode at the coherence gate; a later identical episode
  then learns fresh. Retention must be earned. Every retirement is loud.
- Window expiry beyond 32 stores is not isolated in the frozen battery;
  the independent red team should probe long-horizon aging.
- K-U3-2 (refuse-with-warning) is SUPERSEDED by K-U9-1. Its contract is
  preserved in UNIFIED8_RESULT.md history.
- The dangling-else accounting bug above was caught by trace review before
  result commit, fixed, and rebuilt. Final evidence is from the fixed source.
- No em dashes in loop documentation.

## Files (branch `tnn-native-lab`, `docs/lab/research-lead/overnight-20260928/`)

- `PREREG_UNIFIED9.md` (commit `ecaa78494`, frozen before implementation)
- `unified9_learn.zag`
- `UNIFIED9_RAW_OUTPUT.txt` (md5 `7b690bc7b26940e4848e60920fcfc4e0`)
- `UNIFIED9_RESULT.md` (this file)

## Causal interpretation

The H-UNIFIED5 limitation ("capacity remains refuse-with-warning;
principled eviction is H-MEM lane future work") is closed by integrating
the H-MEM lane's delivered policy. The unified learner is now total over
capacity pressure: it never stops learning, and every retirement is
named, counted, and merit-ordered. This is bounded L2 integration work,
not L3: the policy is adopted and adapted, not invented, and every
behavior is white-box traceable.
