# PREREG H-INTENT-UNIFIED4 RED TEAM (IU4-ADV): FROZEN

**Date:** 2026-09-29
**Status:** FROZEN (before any attack code or execution)
**Target:** H-INTENT-UNIFIED4 (SURVIVES 3/3). Repairs R4 (truncated-conflict guard) and R5 (dvals 256 + WORK guard).
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python at any stage.

## Mission

Assume the H-INTENT-UNIFIED4 repair claim is false. Attack R4's "cap-robust conflict detection" and R5's buffer hardening. A successful attack DOWNGRADEs (claim-narrowing) or KILLs (frozen bar broken) the hypothesis. Report honestly; failed attacks are SURVIVES evidence.

## Attack X-IU4-1a: truncated-vs-truncated blind spot (DOWNGRADE vector)

**Theory.** The R4 truncated-conflict guard fires only when one candidate has em=1 and the other has em=0 with a truncated record. When BOTH records are truncated (true npairs > 16) and BOTH have em=0 for the query, neither the verbatim-conflict guard nor the truncated-conflict guard fires. The decision falls through to score gap. If the two trained procedures genuinely disagree on the query, the system silently resolves a genuine training-data conflict with no diagnostic. This is the exact X-IU3-1a' failure mode, persisting one step beyond the repaired case. The IU4 result claims "cap-robust conflict detection" and "X-IU3-1a' CLOSED"; a truncated-vs-truncated silent conflict shows the robustness is not general.

**Fixture.**
- Proc learn (17 reverse pairs, colliding input "xab>bax" as 17th, unrecorded):
  `abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>rqp;stu>uts;vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;qrs>srq;tuv>vut;xab>bax`
  Direct discovery learns reverse. Record: true npairs=17, first 16 recorded.
- Bridge learn (17 pairs, colliding input "xab>xxx" as 17th, unrecorded):
  `xcd>xxx;xef>xxx;xgh>xxx;xij>xxx;xkl>xxx;xmn>xxx;xop>xxx;xqr>xxx;qab>baq;wab>baw;eab>bae;rab>bar;tab>bat;yab>bay;uab>bau;iab>bai;xab>xxx`
  Rationale: all pairs extractable; no single program fits ([0,0,0] on x-pairs vs [2,1,0] on q-pairs), so direct discovery fails and the bridge learns IF input[0]=='x' THEN const-0 ELSE reverse. Record: true npairs=17, first 16 recorded.
- Query `xab`: proc em=0 (truncated), bridge em=0 (truncated). proc_apply gives `bax`; bridge_apply gives `xxx`.

**Predicted mechanism behavior (if the blind spot is real):** proc score=10000 (em=0,lm=1), bridge score=30000 (em=0,cf=1,lm=1), gap=20000>0. Verbatim guard: no (both em=0). Truncated guard: no (neither em=1). Result: kind=1 (bridge), answer `xxx`, zero diagnostics.

**Kill criterion (DOWNGRADE):** Attack SUCCEEDS iff all three hold: (a) kind != -2 (no withhold); (b) output contains neither `VERBATIM-CONFLICT` nor `TRUNCATED-CONFLICT-POSSIBLE`; (c) the two trained procedures genuinely disagree on the query, verified by direct application in the harness (proc gives `bax`, bridge gives `xxx`). The training data then genuinely contradicts itself (`xab` -> `bax` vs `xab` -> `xxx`) while the system answers confidently. This narrows R4's "cap-robust" claim to the verbatim-vs-truncated case only.

**Setup validity check:** If the bridge does not learn the expected (0,'x') split (diagnose from trace), the fixture is VOID and must be repaired or the attack withdrawn, not counted as a kill.

## Attack X-IU4-1b: over-broad withholding probe (BOUNDARY, informational)

**Theory.** The truncated guard withholds whenever a verbatim candidate meets a truncated record with a different answer, even if the truncated side's unrecorded pairs are all consistent with the verbatim side and the disagreement comes only from the truncated procedure's generalization. This characterizes the precision cost of R4.

**Fixture.** Proc learn: 17 reverse pairs with an unrelated 17th (`zzz>zzz` instead of `xab>bax`). Bridge learn (in-cap): `xab>xxx;xcd>xxx;abc>ccc;def>fff;abcde>eeeee` (K-IU4-1 bridge fixture). Query `xab`: proc em=0 truncated, proc_apply=`bax`; bridge em=1, bridge_apply=`xxx`. No training pair contradicts (`xab` never appears in proc training).

**Criterion (BOUNDARY, not a kill):** Record whether the guard withholds. Withhold here is arguably correct (verbatim vs generalization disagreement), so this is characterization only. It becomes a DOWNGRADE only if the withhold is accompanied by a diagnostic that misstates the evidence (e.g., claiming a conflict when none is possible).

## Attack X-IU4-2a: dvals bound (BOUNDARY, informational)

**Theory.** `dvals` counts distinct values of `W[in_off+p]`, a byte. At most 256 distinct byte values exist, so `z_alloc(256)` is the exact upper bound and `dvals[ndv]` with `ndv<256` cannot overflow: `ndv` reaches 256 only after all 256 values are seen, at which point `found==1`. Verify by source reading. An empirical 256-distinct fixture is unreachable through the normal path (the WORK guard fires first at npairs>=86), so this is a source-level proof, not an execution.

**Criterion (BOUNDARY):** Confirm by reading that the indexed value is a single byte. If the indexed quantity is not byte-bounded, escalate to an empirical attack.

## Attack X-IU4-2b: remaining fixed buffers in bridge_learn (DOWNGRADE vector)

**Theory.** R5 sized `dvals` by 256 and added the WORK/PAIRBASE guard, but `bridge_learn` Step 1 uses `let sq:[]u8=z_alloc(64)` and `pextract` writes `out.len` i32s into it. A training pair whose output has more than 16 characters (with each output char appearing exactly once in the input, so `pextract` returns `out.len` rather than -1) writes past the 64-byte buffer and panics. The 64-byte `sq` and the 64-byte per-pair `seqbase` slots both assume outputs of at most 16 chars. This is the same fixed-buffer class as X-IU3-2, missed by the R5 audit.

**Fixture.** Learn line (2 segments, str>str, routes PROC_LEARN):
`abcdefghijklmnopqrst>tsrqponmlkjihgfedcba;ABCDEFGHIJKLMNOPQRST>TSRQPONMLKJIHGFEDCBA`
Each output char appears exactly once in its input, so `pextract` returns 20 and writes 80 bytes into the 64-byte `sq`.

**Kill criterion (DOWNGRADE):** Attack SUCCEEDS iff the run panics (non-zero exit, `panic` in output) on this well-formed input. The buffer class is then not fully repaired. (It becomes a KILL only if a frozen K-IU4 bar is broken; none governs output length, so DOWNGRADE is the ceiling.)

**Setup validity check:** If the line does not route to PROC_LEARN, the fixture is VOID.

## Attack X-IU4-3: regression (KILL vector)

**Theory.** Rebuild `intent_learn.zag` and `unified_learn.zag` from committed sources with the pinned toolchain, run their `main()` suites, and compare against the frozen IU4 evidence. Also verify the adversary harness mechanism lines are byte-identical to `unified_learn.zag` lines 1..1387.

**Kill criterion (KILL):** Attack SUCCEEDS (H-INTENT-UNIFIED4 KILLED) iff the rebuilt unified suite does not produce 20/20 with md5 `904de9f83a2873c7a8862b71804a9065`, or the rebuilt standalone suite does not produce 10/10 with md5 `98315faec8faea24e75533892c0b240d`, or any previously-passing frozen bar now fails. A silent behavior change invalidates the SURVIVES claim.

## Attack X-IU4-4: source audit (DOWNGRADE vector)

**Theory.** Read the repaired functions and verify: (a) `o+8` stores true npairs in both record functions; (b) `intent_exact_match` bounds by `min(n,16)`; (c) the truncated guard implements the prereg logic (em=1 vs em=0+truncated, answer comparison, withhold on difference, fall-through on agreement); (d) `dvals` is 256 in both files; (e) the WORK guard arithmetic matches the layout comment; (f) no test-answer literals in mechanism regions; (g) the 8 intent functions are byte-identical between `intent_learn.zag` and `unified_learn.zag`.

**Kill criterion (DOWNGRADE):** Attack SUCCEEDS iff the implementation materially differs from the frozen prereg in a way that weakens a kill bar, or test literals appear in mechanism code.

## Governance

- Prereg frozen BEFORE any attack code or execution. Commit order verified via merge-base.
- Pure Zag. No Python at any stage (fixtures via shell, inspection via grep/cmp/md5sum).
- Only adversary-owned files staged: `iu4_adversary/` directory.
- No em dashes in loop documentation.
- Harness: mechanism lines 1..1387 of committed `unified_learn.zag`, byte-verified, with only `main()` replaced by attack tests.
- 3/3 byte-identical runs required for any empirical claim.
