# INTEG-BREAK Red Team Report

Worker: TNN red-team worker (depth 2/2), watchdog coordinator parent.
Ledger: follows H-COMPINTEG-1 (C295, verdict COMPOSITION-INTEGRATION-INCOMPLETE).
Prereg: frozen at commit 750ad6b15 ("Local only, never pushed."), PREREG.md + NAMECHECK.md Step 0 committed ALONE before any attack implementation.
Date: 2026-10-02.

All computation in pure Zag (pinned znc). Safebin toolchain guard active; `which python3` / `which python` return nothing.

## Verdicts (per target, against frozen bars; no global L3 claim)

| Target | Attack verdict | Guard verdict |
|---|---|---|
| T1 self-referential FACT substitution (K3) | PATHOLOGY-CONFIRMED | GUARD-PASS |
| T2 circular self-verification (K5) | PATHOLOGY-CONFIRMED | GUARD-PASS |
| T3 value-replay vs live-fact execution gap (I5) | PATHOLOGY-CONFIRMED | GUARD-PASS |

## Determinism record

Attack binary `rt_bin`: 3/3 byte-identical stdout.
sha256 `c48fe8f07b9fbf09a3b2642e14b0420d5d29034bc3cda37cc83b065f262f8e61` (rt_run1/2/3.txt).

Guard binary `rt_guard_bin`: 3/3 byte-identical stdout.
sha256 `5ca49343a0a3296e71b701a885dcbe050e844608becfc36bdddc986293b243c5` (rtg_run1/2/3.txt).

## T1: self-referential FACT substitution (K3)

ATTACK-SUCCEEDS bars (PREREG Section 2): all met.

- T1-A1: `MAPX=13 FL=4 SPEC-N=1 SELFREF-MAP=19`. A single specialize call on a [1,2]->99 MAP with a live learner FACT(11,71,14) [44/12==1] present creates a live [71]->14 trial (id 19) whose ET_DEP edge points at the learner fact. The filter in `ts_specialize_src` admits any live non-superseded tag-1 fact with matching subject and different relation; it has no provenance signal.
- T1-A2 characterization matrix: C1=1 (world relation substitutes), C2=1 (learner FACT substitutes, the pathology), C3=0 (same-relation excluded), C4=0 (superseded excluded), C5=0 (killed excluded). Matches hand derivation 1,1,0,0,0 exactly.
- T1-A3 explore pollution: with learner fact (11,71,14) and world fact (11,3,14) present, 4 explore cycles leave a live self-referential [71] trial (id 30) and FACT(11,74,99) score stuck at 1 (< 3). The [71]->14 trial executes to 14 on alternating cycles, so observations alternate 14/99 and the genuine contract never confirms.

Characterization answer. Substitution produces self-referential trials exactly when (a) a learner-originated FACT with the query subject exists and (b) `ts_specialize_src` runs (adapt bracket or explore). It is CORRUPTING when the licensing FACT is the learner's own reified prediction (unconfirmed belief bootstrapping itself into a reusable trial). It is USEFUL when the same shortcut is independently confirmed by the world: the C6 probe (world teaches (11,71,14) through the world channel alongside the learner fact) shows the world-licensed [71] MAP is a genuine reusable shortcut. So the discriminator is provenance of the licensing fact, not the substitution mechanism.

Guard GUARD-T1 (ts_patch_g.zag, +8/-0 lines): the candidate filter skips facts with the learner-origin bit set; world-channeled facts still license substitution.

- T1-G1: S1 `SPEC-N=0 SELFREF-MAP=-1` (pathology blocked); C6 `SPEC-N=1 WORLD-LIC=20 LEARNER-LIC=-1` (world-confirmed shortcut still reusable). GUARD-TEST bar met.
- T1-G2 control: no learner shortcut present; 4 explore cycles teach FACT(11,74,99) to score exactly 3 via the world-licensed [3,2] trial (id 23, DEP to world fact 4). Legitimate specialization survives. Control battery bar met.

## T2: circular self-verification (K5)

ATTACK-SUCCEEDS bars (PREREG Section 3): all met.

- T2-A1: stale prediction 209 (rel 3) survives a world change (202,2,209 killed; live truth 205). `lv_dfs` finds the [70] self-referential MAP (id 22, built from the learner's own FACT(201,70,209)), `t2_lu_first(201,70)` replays the stale fact to 209, verification succeeds against the stale graph, and MAP_Z (id 31) is promoted with LINK14 to m70. `T2-Q1=209` against live truth 205: confident-wrong.
- T2-A2 entrenchment: re-query re-promotes (`T2-Q2=209 MAP_Z2=39 LINK14toM70=1`); after retiring m70, `T2-Q3=209` via MAP_Z self-perpetuation (the promoted copy carries the stale chain forward). `TYPE15-COUNT=0`: the single-segment degenerate path writes no co-use edges, so entrenchment here flows through repeated MAP_Z promotion and the learner FACT's score (reached 3), not through type-15 edges. The loop is real and self-perpetuating without any co-use machinery.

Guard GUARD-T2 (lvcomp_patch_g.zag, +34/-1 lines): `lv_setup` records the prediction's source fact id in header slot 40; `lv_verify_chain` runs the self-license veto (`rt_selflicensed`): when every ET_DEP licensing fact of the verification graph IS the learner-originated prediction source, verification is vacuous and rejected (-2, no promotion). A refined rule: verification whose licensing set contains at least one non-source fact is allowed even on the degenerate single-fact path.

- T2-G1: directly injected circular MAP (defense in depth: GUARD-T1 already blocks specialize-built circular MAPs in the guard binary, so the adversary path is direct injection). `T2G-Q1=-2`, newest MAP unchanged (no promotion), and after retiring the injected MAP `T2G-Q3=-2`. The veto blocks the loop at both the injection point and the self-perpetuation point.
- T2-G2 controls: (i) world-grounded degenerate verification (source fact world-channeled, native MAP retired to isolate the path) verifies and promotes: `Q=314 LINK14=1`. (ii) non-degenerate verification verifies and promotes: `Q2=409 LINK14toMX=1`. Legitimate verification survives.

## T3: value-replay vs live-fact execution gap (I5)

ATTACK-SUCCEEDS bars (PREREG Section 4): all met.

- T3-A1: `PREKILL-EXEC=209`. After teach-then-kill (kill (202,2,209), teach (202,2,205)): `CC_RELSEQ=-1` (DEP-sensitive: the retired MAP's licensing edge is dead), `UNSAT_LN=2 UNSAT_NV=205` (`un_satisfy` re-derives 205 through the live-fact contract path), but `POSTKILL-EXEC=209` (`t2_exec` replays the baked 902 literal chain). `LU202=14 LUVAL=205` confirms live lookup sees the new fact. The divergence is exact: the same stale trial both fails DEP-sensitive checks and replays stale values.

Execution-path boundary (call-site census over the six frozen sources).

REPLAY (bake values at assembly, replay at execution): every `t2_exec` call site.
1. cc_base.zag:500 `t2_try_verify` (assembled-chain verification).
2. cc_base.zag:732 `t2_revise_graph` (graph revision check).
3. cc_base.zag:1266 `t_t2_revise` (test assertion).
4. lvcomp_patch.zag:62 `lv_verify_seg` (per-segment verification).
5. lvcomp_patch.zag:224 `lv_verify_chain` (native MAP path).
6. integ_patch.zag:77 INTEG per-segment executor.

RE-DERIVE (consult live facts at execution): `cc_relseq` (reads relations via SETREG ET_DEP edges, fails when a licensing fact is dead), `t2_lu_first` (live fact lookup), `t2_gather` / `un_satisfy` (contract path falls back to live facts).

Is replay load-bearing for a passing bar? No passing bar requires staleness. The I2-equivalent bar (12 via truncate trial) executes through the same replay path but with no intervening fact kill, so replay and re-derivation coincide there. Replay is an optimization that is observably wrong exactly when the world changes between assembly and execution.

Substrate-vs-modeling verdict: SUBSTRATE SEMANTIC BUG, not a prereg modeling error. `t2_exec`'s contract is to execute the trial's chain; the chain's ET_DEP licensing facts are its truth conditions. Executing a chain whose licensing facts are dead or superseded is executing a falsified hypothesis while the learner's own belief state (live facts) says otherwise. The gap is real in the frozen sources and reproducible minimally.

Guard GUARD-T3 (cc_base_g.zag, +50/-0 lines): `t2_exec` runs a licensing-liveness veto (`rt_lic_facts` walks the rebuilt graph's SETREG ET_DEP targets): if any licensing fact is dead or superseded, execution returns -999999 (INTEG-EXEC-STALE) instead of replaying.

- T3-G1: `STALE-EXEC=-999999` (stale trial vetoed), `FRESH-EXEC=205` (a trial assembled from live facts executes fine). GUARD-TEST bar met.
- T3-G2 controls: I2-equivalent `Q=12` with MAP_Z LINK14 to the [1] truncate trial (id 18); I4-equivalent `Q2=-3` with zero MAP/type-16 side effects. Control battery bar met.

## Cognition lines touched

Guarded copies only (frozen originals untouched, sha256-verified against C295 preregistration):

| File | Diff | Content |
|---|---|---|
| cc_base_g.zag | +50/-0 | GUARD-T1 learner-origin bit (ev_teach_in); GUARD-T3 rt_lic_facts + liveness veto in t2_exec |
| ts_patch_g.zag | +8/-0 | GUARD-T1 provenance gate in ts_specialize_src |
| lvcomp_patch_g.zag | +34/-1 | GUARD-T2 source recording (lv_setup, hg 40) + self-license veto (lv_verify_chain) |

New edge types: 0. New MAP types: 0. New opcodes/modes/bridges/handlers/semantic cases: 0. One reused free field (fact f12, free on tag-1 nodes; see correction below) and one free header slot (40). Driver sources (rt_attack.zag, rt_guardtest.zag) are harness, not cognition.

## Transparent correction: learner-origin field 44 -> 12

During guard testing the first guard binary showed inverted behavior (learner facts admitted, world facts blocked). Root cause: node slots are 40 bytes (`noff(n) = 64+n*40`), so field 44 aliases the NEXT node's field 4. The census that declared field 44 free checked usage but not node size. The guard was moved to fact field 12, which is genuinely free on tag-1 FACT nodes (the base itself notes f8/f12/f16 hold scores only on other tags; verified: no read of f12 on a tag-1 node anywhere in the six sources). The PREREG's bar ("exactly one new fact-field usage") is unchanged in intent; only the field number moved. The frozen PREREG text still says f44; this report records the correction. No bar was weakened: all guard bars passed after the fix, 3/3 deterministic.

## Files

Lane: docs/lab/research-lead/overnight-20260928/integ_break_redteam/
- PREREG.md, NAMECHECK.md (frozen at 750ad6b15, committed alone)
- rt_attack.zag (attack driver), rt_guardtest.zag (guard-test driver)
- cc_base_g.zag, ts_patch_g.zag, lvcomp_patch_g.zag (guarded copies; originals untouched)
- rt_build.sh (build script), rt_run1/2/3.txt, rtg_run1/2/3.txt (3/3 digests)
- rt_full.zag, rt_guard_full.zag (concatenated build inputs), rt_bin, rt_guard_bin (binaries)

## Open questions / follow-ups for the coordinator

1. GUARD-T1's provenance bit is set by the TEACH CHANNEL (ev_teach_in vs ev_teach). If the learner ever teaches through the world channel, provenance is lost. A learner-owned alternative: sign the fact at creation time rather than trusting the channel. Worth a follow-up probe.
2. GUARD-T2's veto is deliberately narrow (all licensing facts == the learner-originated source). A partial-overlap case (graph licensed by source + one world fact) still verifies; whether that admits a subtler loop is untested.
3. GUARD-T3 returns -999999 on stale execution. Callers currently treat it as a normal value; a real integration should route INTEG-EXEC-STALE into the adapt/revise path rather than propagating the sentinel.
4. T2-A2 showed entrenchment without co-use edges (TYPE15-COUNT=0). The co-use entrenchment vector from K5's original report needs a multi-segment variant to be tested separately.
