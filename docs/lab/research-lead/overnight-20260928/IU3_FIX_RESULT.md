# H-INTENT-UNIFIED3 RESULT: Repair of the IU2-ADV Red-Team Downgrade

## Verdict: H-INTENT-UNIFIED3 SURVIVES (8/8 kill-bar checks, 10/10 + 20/20 regressions)

All three IU2-ADV findings are addressed. The verbatim-vs-verbatim
heuristic resolution is closed by a new ambiguity guard, the 16-cap
truncation is explicit, and the bridge_learn crash is fixed. All
frozen H-INTENT-UNIFIED2 behaviors are preserved.

## What was repaired

### R1. X-IU2-1: verbatim-conflict guard (CLOSED)

Root cause: the em specificity term protected verbatim evidence
against a heuristic only when the heuristic side had no verbatim
evidence of its own. When both sides had em=1, the cf (20000) or lm
(10000) terms broke the tie silently. The qscore-tie guard never
fired because the scores differed (60000 vs 50000).

Repair: intent_winner now tracks em per candidate (ce[] array). After
top/second selection, if both have em=1, it computes both answers
(re-applying proc_apply/bridge_apply per kind) and compares byte-wise.
If the answers differ, the training data genuinely contradicts itself
on this input: WITHHOLD AMBIGUOUS (kind -2), with an explicit
"INTENT VERBATIM-CONFLICT" trace line. No heuristic term may silently
resolve a verbatim-vs-verbatim conflict. If the answers agree, the
contradiction is moot and the existing rules apply (avoids
over-broad withholding on duplicated training).

### R2. X-IU2-3: explicit cap warning (WARNED, boundary documented)

Root cause: intent_record_inputs capped at 16 with no diagnostic; the
17th input vanished silently.

Repair: when npairs > 16, emit "INTENT WARN: record cap 16 reached; N
training inputs, only first 16 recorded; em coverage incomplete".
The truncation behavior is unchanged (documented boundary); it is now
explicit in the trace instead of silent.

### R3. X-IU2-3b: split buffer sizing (FIXED)

Root cause: bridge_learn s1idx/s2idx were z_alloc(64) = 16 fixed i32
entries, but n1/n2 can reach npairs. Past 16 pairs on one split side,
the 17th write went out of bounds and panicked.

Repair: size both buffers as z_alloc(npairs*4). n1/n2 are bounded by
npairs by construction, so overflow is impossible.

## Mechanism (as implemented, identical in both files)

Applied identically to intent_learn.zag (standalone) and
unified_learn.zag (port). All 7 intent functions
(intent_record_inputs, intent_record_proc, intent_record_br,
intent_exact_match, intent_qscore, intent_winner, intent_trace_emit)
verified byte-identical between the files (md5 per function).
stress_learn.zag, genbias_test.zag, unified_adversary/ulib.zag
untouched.

## Frozen bars and results

- K-IU3-1 (X-IU2-1 closed): PASS. Red-team fixture (D2 "xab>bax;xcd>dcx",
  bridge "xab>xxx;..." cond (0,120), em_D2("xab")==1). Query "xab":
  kind -2 WITHHOLD AMBIGUOUS. Trace shows "INTENT VERBATIM-CONFLICT".
  (Was: silent bridge win, kind 1.)
- K-IU3-2 (X-IU2-3 warned): PASS. 17-pair fixture emits "INTENT WARN:
  record cap 16 reached; 17 training inputs, only first 16 recorded;
  em coverage incomplete" during T LEARN. in_count=16, em_D("tuv")=0
  (boundary behavior unchanged, now explicit).
- K-IU3-3 (X-IU2-3b fixed): PASS. 18-pair fixture (17 extractable on
  one split side) completes with rc=1000 (bridge learned), no panic.
  (Was: slice index out of bounds.)
- K-IU3-4 (no regressions): PASS. G4a (F1 interleaved) withholds;
  G4b (F2 verbatim) kind 0; G4c (F2b bridge) kind 1; G4d (F3
  len_match) abcd->dddd. Repaired intent_learn.zag main(): 10/10 PASS.
  Repaired unified_learn.zag main(): 20/20 PASS. Zero FAILs.
- K-IU3-5 (determinism): PASS. Three consecutive runs byte-identical
  (md5 c5c4ecc9cdcf6210ab6f630778515fd0).
- G5 (X-IU2-2 control): PASS. Pure em tie (abc: 50000 vs 50000)
  withholds kind -2. The new guard fires (both em=1, answers differ);
  verdict identical to the old tie rule.

Total: 8/8 kill-bar checks + 10/10 + 20/20 = 38/38.

## Evidence

- Prereg: PREREG_INTENT_UNIFIED3.md (commit e638bcb71), frozen before
  implementation. Commit order: prereg strictly precedes
  implementation.
- Implementation: intent_learn.zag (repaired), unified_learn.zag
  (repaired).
- Repair tests: iu3_fix.zag (byte-copy of repaired unified_learn.zag
  mechanism, lines 1-1312 verified identical by diff; main()
  replaced by G1-G5).
- Raw outputs (authoritative): IU3_FIX_RAW.txt (md5
  c5c4ecc9cdcf6210ab6f630778515fd0, 3 runs byte-identical),
  IU3_INTENT_REG_RAW.txt (10/10), IU3_UNIFIED_REG_RAW.txt (20/20).
- Toolchain: znc 2026.07.0-dev (edition 2026), pinned.
- Binaries not committed (repo convention); rebuild via
  znc iu3_fix.zag -o iu3_fix (etc.).

## Classification

Bounded L2 integration infrastructure. The repair composes the
validated specificity principle (verbatim evidence dominates
heuristics) with an explicit conflict-withhold rule. No
representational invention involved. Not L3.

## Boundaries

- The 16-input record cap remains; truncation is now explicit, not
  silent. Raising it is future work.
- The verbatim-conflict guard withholds on disagreement; it does not
  identify which record is correct. Adjudication is future work.
- len_match remains the weakest signal with the documented X-IU3
  boundary.
- Near-ties (em=1 vs em=0 with cf/lm deciding) are unchanged: only
  verbatim-vs-verbatim conflicts trigger the new guard.

## Governance

Pure Zag throughout. No Python used at any stage: no generators, no
verifiers, no analysis scripts, no scratch tooling. No em dashes in
new documentation or code. Prereg (e638bcb71) strictly precedes
implementation. Only repair-owned files staged and committed; no
other agent's files touched. The prereg commit swept in one unrelated
paper line from a concurrent agent (NQ1 status); content verified,
prereg intact.
