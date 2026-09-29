# IU4-ADV RESULT: H-INTENT-UNIFIED4 Red Team

## Verdict: H-INTENT-UNIFIED4 DOWNGRADED (not killed)

Two preregistered attacks succeed. No frozen kill bar (K-IU4-1..K-IU4-4) is broken, so this is claim-narrowing, not a kill. The frozen 3/3 bars stand as executed.

## Methodology

Preregistered attacks with explicit kill criteria BEFORE any attack code or execution (PREREG_IU4_ADV.md, commit 5009ce0c8, strict ancestor of all attack artifacts). Pure Zag, pinned toolchain znc 2026.07.0-dev. No Python at any stage. Harness mechanism = lines 1..1387 of committed unified_learn.zag, cmp-verified byte-identical; only main() replaced. All empirical claims 3/3 byte-identical.

One build note: the first build used a wrong znc invocation (`znc build`, not a real subcommand) and silently left a stale binary from a prior session in place; the stale output was caught by output-content inspection before any conclusion was drawn, both harnesses were rebuilt with the correct `znc <source> -o <out>` syntax, and all reported evidence comes from the correct binaries. No conclusion rests on the stale run.

## Finding 1: X-IU4-1a SUCCEEDS — truncated-vs-truncated blind spot (DOWNGRADE)

The R4 truncated-conflict guard fires only when one candidate has em=1 and the other has em=0 with a truncated record. When BOTH records are truncated (true npairs > 16) and BOTH have em=0 for the query, neither guard fires and the decision falls through to score gap.

Fixture (3/3 byte-identical, md5 7aa5a5452f0c2c39c0233be66c6d15d7):
- Proc: 17 reverse pairs, `xab>bax` as 17th (unrecorded). Direct discovery, slot 0. Record true npairs=17, WARN fired.
- Bridge: 17 pairs, `xab>xxx` as 17th (unrecorded); first 16 induce IF input[0]=='x' THEN const-0 ELSE reverse (trace: `bridge: learned IF input[0]==120 THEN proc1 ELSE proc2`). Record true npairs=17, WARN fired.
- Query `xab`: proc em=0 score=10000, bridge em=0 cond_fire=1 score=30000, gap=20000.

Observed:
- `T DECIDE tag=A1-xab kind=1 slot=0 gap=20000 answer=[xxx]`
- Zero `VERBATIM-CONFLICT` lines, zero `TRUNCATED-CONFLICT-POSSIBLE` lines.
- Direct application in-harness: `A1-DIRECT proc_answer=[bax] bridge_answer=[xxx]` — genuine disagreement confirmed.

The training data genuinely contradicts itself (`xab` -> `bax` in proc pair 17, `xab` -> `xxx` in bridge pair 17), but the system answers `xxx` confidently with no diagnostic. This is the exact X-IU3-1a' failure mode, persisting one step beyond the repaired case. The IU4 claim "cap-robust conflict detection" narrows to the verbatim-vs-truncated case only. The repair closed the reported vector, not the conflict class.

## Finding 2: X-IU4-1b — over-broad withholding characterized (BOUNDARY)

Fixture: proc trained on 17 reverse pairs with unrelated 17th (`qwe>ewq`); bridge trained in-cap on `xab>xxx;...` (K-IU4-1 shape). Query `xab`: proc em=0 truncated (procedure generalizes to `bax`; `xab` never appears in proc training), bridge em=1.

Observed: `INTENT TRUNCATED-CONFLICT-POSSIBLE ... WITHHOLD AMBIGUOUS`, kind=-2.

No training pair contradicts here; the disagreement is generalization-vs-verbatim. The guard withholds anyway. The diagnostic honestly says "POSSIBLE", so this is not a misstatement, but it documents the precision cost of R4: any truncated record whose procedure generalizes differently from a verbatim candidate triggers a withhold, even with fully consistent training data. Boundary, not a kill.

## Finding 3: X-IU4-2a — dvals bound confirmed (BOUNDARY)

By source reading: `dvals` collects distinct values of `W[in_off+p]`, a single byte. At most 256 distinct byte values exist; `ndv` reaches 256 only after all values are seen, at which point `found==1` and no write occurs. `z_alloc(256)` is the exact upper bound. An empirical 256-distinct fixture is unreachable through the normal path (the WORK guard fires first at npairs>=86), so this stands as a source-level proof. No attack.

## Finding 4: X-IU4-2b SUCCEEDS — sq(64) fixed buffer panics (DOWNGRADE)

R5 sized `dvals` and added the WORK guard, but `bridge_learn` Step 1 uses `let sq:[]u8=z_alloc(64)` while `pextract` writes `out.len` i32s into it. A training pair with a >16-char output (each output char appearing exactly once in the input, so `pextract` returns `out.len` rather than -1) writes past the buffer.

Fixture (well-formed, routes PROC_LEARN):
`abcdefghijklmnopqrst>tsrqponmlkjihgfedcba;ABCDEFGHIJKLMNOPQRST>TSRQPONMLKJIHGFEDCBA`

Observed (3/3 identical, md5 e8966d45f8a728cab21c54db9640ef34):
- `ROUTE [...] -> PROC_LEARN (2+ segs, str>str)`, route=1
- `panic: slice index out of bounds`, exit 1.

The 64-byte `sq` (and the 64-byte per-pair `seqbase` slots, same 16-char assumption) is the same fixed-buffer class as X-IU3-2, missed by the R5 audit. The repair covered the reported vector (dvals) and one audit find (WORK/PAIRBASE), not the buffer class. DOWNGRADE.

## Finding 5: X-IU4-3 FAILS — regression holds

Rebuilt committed `unified_learn.zag` and `intent_learn.zag` with the pinned toolchain:
- Unified suite: 20/20, md5 904de9f83a2873c7a8862b71804a9065, matches frozen IU4 evidence. 3/3 byte-identical.
- Standalone suite: 10/10, md5 98315faec8faea24e75533892c0b240d, matches frozen IU4 evidence. 3/3 byte-identical.
No silent behavior change. No kill.

## Finding 6: X-IU4-4 FAILS — source audit clean

Verified by direct reading:
- (a) `o+8` stores true (uncapped) npairs in both `intent_record_proc` and `intent_record_br`.
- (b) `intent_exact_match` bounds its loop by `min(n,16)`.
- (c) The truncated guard implements the prereg logic exactly: em=1 vs em=0+truncated (either direction), answer comparison via kind-dispatched apply, withhold on difference, fall-through on agreement.
- (d) `dvals` is `z_alloc(256)` in both files (unified:520, intent:485).
- (e) WORK guard arithmetic matches the layout comment: seqbase npairs*64 + statbase npairs*4 + lenbase npairs*4 = npairs*72; guard `work+npairs*72>pairbase` fails honestly.
- (f) No test-answer literals in mechanism regions (all `xab`/`bax`/`xxx` literals are in `main()` test code, past line 1388).
- (g) All 8 intent functions byte-identical between `intent_learn.zag` and `unified_learn.zag` (verified per-function by extraction and cmp; an initial awk extraction bug that falsely flagged `intent_qscore` was caught and corrected by direct `grep -A` comparison).

The implementation is faithful to the frozen prereg. No downgrade.

## Classification

Bounded L2 integration, narrowed. Not L3 (unchanged).

## Recommended follow-ups for the parent

1. H-INTENT-UNIFIED5: generalize the truncated guard to the both-truncated case (e.g., when both records are truncated and answers differ, withhold with an explicit diagnostic); the X-IU4-1a fixture is the ready regression test (must yield kind=-2 in both orders).
2. H-INTENT-UNIFIED5: bound `sq` by input length (or cap outputs at 16 with an honest diagnostic); the X-IU4-2b fixture is the ready regression test (must not panic).
3. The research paper's H-INTENT-UNIFIED4 section needs both narrowed claims written in; the current "cap-robust" and buffer-audit language is now overstated.

## Commits (tnn-native-lab)

- `5009ce0c8` — PREREG_IU4_ADV.md (frozen before any attack code; strict ancestor verified).
- This commit — `iu4_adversary/iu4_adv.zag`, `iu4_adversary/iu4_adv_panic.zag`, `iu4_adversary/IU4_ADV_RAW.txt` (md5 7aa5a5452f0c2c39c0233be66c6d15d7, 3/3 identical), `iu4_adversary/IU4_ADV_PANIC_RAW.txt` (md5 e8966d45f8a728cab21c54db9640ef34, 3/3 identical), `iu4_adversary/IU4_ADV_RESULT.md`. Only adversary-owned files staged; concurrent workers' files untouched.

## Governance

Pure Zag throughout, no Python at any stage. No binaries committed (builds in /tmp only). No em dashes in loop documentation.
