# IU4 RESULT: H-INTENT-UNIFIED4 Repair Verification

## Verdict: H-INTENT-UNIFIED4 SURVIVES (3/3 kill bars, 3/3 determinism)

Both H-INTENT-UNIFIED3 red-team downgrades are repaired. No frozen kill bar broken. No regressions.

## Methodology

Preregister repairs with frozen kill bars before implementing. Pure Zag, pinned toolchain znc 2026.07.0-dev (edition 2026). No Python at any stage.

- Prereg: PREREG_INTENT_UNIFIED4.md (commit 75fb232ce), frozen before any implementation.
- Implementation: identical repairs in `intent_learn.zag` and `unified_learn.zag` (X-IU4 faithfulness invariant: all 8 intent functions byte-identical, verified by diff).
- Harness: iu4_verify.zag (mechanism lines 1..1387 of unified_learn.zag, byte-identical; only main() replaced with kill-bar tests).
- Raw evidence: IU4_VERIFY_RAW.txt (md5 3496de696a98caae8dd3d924c5a95ab5, 3 runs byte-identical).
- Commit order: prereg, then implementation, then harness plus raw plus this report. Only researcher-owned files staged.

## Repair R4: Cap-robust conflict detection (X-IU3-1a' CLOSED)

### Mechanism changes

1. **True npairs at o+8:** `intent_record_proc` and `intent_record_br` now store the TRUE npairs (uncapped) at record offset o+8, instead of `min(npairs,16)`. The recorded input list still holds min(npairs,16) entries. `intent_exact_match` bounds its loop by `min(n,16)`. This creates a persistent truncated-evidence flag: `truncated = (get32(W, rec+8) > 16)`. No record layout change; the 16-byte format is preserved.

2. **Truncated-conflict guard in intent_winner:** After the existing verbatim-conflict guard, a new guard checks: if one candidate has em=1 (verbatim) and the other has em=0 with a truncated record (true npairs > 16), compute both answers via proc_apply/bridge_apply dispatch by kind. If answers differ, emit "INTENT TRUNCATED-CONFLICT-POSSIBLE: verbatim candidate meets truncated record with different answer; WITHHOLD AMBIGUOUS" and return kind=-2. If answers agree, fall through to existing rules (no over-broad withholding).

### K-IU4-1 evidence (X-IU3-1a' fixture)

Fixture: proc trained on 17 reverse pairs with "xab>bax" as 17th (unrecorded); bridge trained on "xab>xxx;xcd>xxx;abc>ccc;def>fff;abcde>eeeee" (all recorded). Query "xab".

Observed (3/3 runs identical):
- "INTENT WARN: record cap 16 reached; 17 training inputs, only first 16 recorded; em coverage incomplete"
- cand kind=proc slot=0 exact_match=0 (truncated) score=10000
- cand kind=bridge slot=0 exact_match=1 score=60000
- "INTENT TRUNCATED-CONFLICT-POSSIBLE: verbatim candidate meets truncated record with different answer; WITHHOLD AMBIGUOUS"
- T DECIDE tag=K14-xab kind=-2 slot=-1 gap=50000

PASS: kind=-2 (WITHHOLD) with explicit diagnostic. H-IU3 behavior was kind=1, answer "xxx", zero diagnostics. The guard now fires because the proc record has true npairs=17 > 16 (truncated), the bridge has em=1, and proc_apply("xab")="bax" differs from bridge_apply("xab")="xxx".

## Repair R5: Distinct-value buffer sizing + WORK audit (X-IU3-2 CLOSED)

### Mechanism changes

1. **dvals sized by 256:** In `bridge_learn`, `dvals:[]u8=z_alloc(128)` changed to `z_alloc(256)`. Principled: a byte holds 256 distinct values; ndv counts distinct byte values at a position, so 256 is the exact upper bound. Applied at unified_learn.zag:503 and intent_learn.zag:468.

2. **WORK/PAIRBASE honest guard:** Audit found a latent capacity boundary: `bridge_learn` lays out seqbase=work (npairs*64), statbase=work+npairs*64 (npairs*4), lenbase=statbase+npairs*4 (npairs*4), requiring work+npairs*72 bytes. With WORK=2048 and PAIRBASE=8192, npairs >= 86 causes silent overlap corruption. Added guard at start of `bridge_learn`: if `work + npairs*72 > pairbase`, emit "bridge: WORK area too small for npairs=N; need M bytes; honest failure" and return -1. Converts silent corruption into explicit failure.

### K-IU4-2 evidence (129-pair fixture)

Fixture: 129 pairs with 129 distinct first-byte values at position 0, direct discovery failing (X-IU3-2 setup).

Observed (3/3 runs identical, exit code 0):
- "IU4-BIGLINE pairs=129 bytes=1031"
- "ROUTE [...] -> PROC_LEARN (2+ segs, str>str)"
- "bridge: WORK area too small for npairs=129; need 9288 bytes; honest failure"
- "ULEARN FAIL: no program and no bridge"
- "K-IU4-2 bridge rc=-1 (no panic: PASS)"

PASS: exit 0, no panic. H-IU3 behavior was panic "slice index out of bounds", exit 1. The dvals buffer no longer overflows (256 >= 129 distinct values); the WORK guard then fails honestly instead of corrupting PAIRBASE. Per the frozen K-IU4-2 bar, honest failure is PASS; the bar is "no panic", not "bridge learns successfully".

## K-IU4-3: Regression (all K-IU3 bars still PASS)

- **K-IU3-1 (in-cap verbatim conflict):** Fixture with proc "xab>bax;abc>cba" and bridge "xab>xxx;xcd>xxx" (both in-cap). Query "xab" yields kind=-2 with "INTENT VERBATIM-CONFLICT". PASS (verified in iu4_verify.zag K-IU4-3 section).
- **K-IU3-2 (17-pair WARN):** WARN emitted; record now stores true npairs=17 at o+8 (loop bound 16). The WARN text is unchanged. PASS.
- **K-IU3-3 (18-pair split):** The 18-pair fixture from X-IU3-3 still produces rc=1000 with no panic. The dvals change (128->256) and WORK guard (threshold 86) do not affect npairs=18. PASS by code inspection; the 18-pair path is exercised in the 20/20 unified suite.
- **K-IU4-4 (determinism):** 3/3 runs byte-identical (md5 3496de696a98caae8dd3d924c5a95ab5). PASS.
- **Full suite regression:** unified_learn.zag main() produces 20/20 with output md5 904de9f83a2873c7a8862b71804a9065, byte-identical to frozen IU3 output. intent_learn.zag main() produces 10/10 with output md5 98315faec8faea24e75533892c0b240d, byte-identical to frozen IU3 output. PASS.

## X-IU4 faithfulness invariant

All 8 intent functions (intent_record_inputs, intent_record_proc, intent_record_br, intent_exact_match, intent_qscore, intent_winner, intent_trace_emit, intent_init) are byte-identical between intent_learn.zag and unified_learn.zag (verified by diff). The bridge_learn changes (dvals 256, WORK guard) are present in both files; remaining diffs are pre-existing comments only.

## Classification

Bounded L2 integration infrastructure. The repairs make conflict detection robust to the record cap and make buffer sizing principled; they do not invent new representations. No L3 claim.

## Boundaries

- The truncated-conflict guard only fires when the truncated side's procedure answers differently. If a truncated record's procedure agrees with the verbatim candidate, no withhold occurs (no over-broad withholding).
- The WORK guard threshold is npairs >= 86 with default WORK=2048, PAIRBASE=8192. Larger WORK areas (or relocated PAIRBASE) would raise this bound; the guard computes it dynamically from the actual work/pairbase parameters.
- The 129-pair fixture now fails honestly at the WORK guard. A caller that provides a larger WORK area (e.g., work=2048, pairbase=16384) could attempt the full 129-pair split search; the dvals buffer (256) would not overflow.

## Governance

Pure Zag throughout. No Python used at any stage. Prereg (75fb232ce) strictly precedes implementation. Only researcher-owned files staged and committed: PREREG_INTENT_UNIFIED4.md (prereg commit), intent_learn.zag, unified_learn.zag, iu4_verify.zag, IU4_VERIFY_RAW.txt, and this report. No other agent's files touched. No em dashes in new documentation.
