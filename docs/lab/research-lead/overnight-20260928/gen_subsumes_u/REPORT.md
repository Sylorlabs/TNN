# REPORT: GEN-SUBSUMES-U -- Verdict PARTIAL (boundary characterized)

Date: 2026-10-03. Worker: GEN-SUBSUMES-U. Lane:
`docs/lab/research-lead/overnight-20260928/gen_subsumes_u/`.
Branch: `lane-gensubsumesu-20261003` (isolated; explicit pathspecs; local only).

## Verdict: PARTIAL. GEN subsumes U on single-query linear composition; one
residual boundary found and precisely characterized.

GEN reproduces U's answers exactly on all 5 of U's linear pipeline pairs,
fails honestly where U fails honestly, and succeeds where U succeeds on a
fresh learner. The residual boundary is multi-query arena reuse for contract
growth: the frozen `gen_solve` does not reset its per-query tried-state, so a
second query on the same arena returns ANS=-2 where U returns ANS=3. The
contract-growth representation itself is intact in GEN (census proves it);
the defect is trial-state scoping, and the fix is small and specified.

## Kill bar results

All 10 frozen predictions from PREREG Sec 4 hit exactly. 3/3 runs
byte-identical (stdout sha256
`72fd791c24c89638830463952557ddb21d51552fa96f254e97d252a376af8237`;
stderr empty).

- K1 PRIMARY SUBSUMPTION: PASS. GEN ANS equals U ANS on all 5 pairs:
  P1 65, P2a 2, P2b 2, P3 2, Q1 1. TRIES as predicted (4/6/6/6/6 vs U's
  3/3/7/3/2; try-count parity explicitly out of scope per PREREG Sec 5).
- K2 HONEST FAILURE: PASS. Q2 ANS=-2 with WIDEN=1 (TRIES=3); Q3 ANS=-2
  with WIDEN=1 (TRIES=9). No false positives where U honestly fails.
- K3 FRESH LEARNER: PASS. Q4 ANS=1 TRIES=6.
- K4 GROWTH BOUNDARY PROBE: prediction held (informative). P5 ANS=-2
  TRIES=0 with WIDEN=1, exactly as derived. Census after P2b shows
  m0 inmask=1 outmask=3 inmask2=0 n=2: the contract DID grow from P2b's
  success-recording (X.out {2} -> {1,2} via provenance closure), so
  representation-level growth works; the second query fails only because
  of stale tried-state (see Sec "The boundary").
- K5 DETERMINISM: PASS. 3/3 byte-identical; stderr empty.
- K6 FIDELITY: PASS. Base region byte-identical to pair6 `d6_base.zag`;
  composer region byte-identical to `d6_gen.zag` lines 1-239; world region
  byte-identical to pair5 `p5_full.zag` lines 336-391; all diffs empty.
- K7 TOOLCHAIN: PASS. Safebin active for every command; `which python3`
  and `which python` return nothing; zero forbidden-executable
  invocations; pure Zag; shell only for znc/binary/git/assembly/verify.
- K8 HYGIENE: PASS. Zero em/en dash bytes in lane docs (byte-verified).

## Full output (identical across 3 runs)

```
INTER=63
INTER=-2
INTER=-2
INTER=65
ARM=GEN PROB=P1 ANS=65 TRIES=4
INTER=44
INTER=-2
INTER=41
INTER=1
INTER=-2
INTER=2
ARM=GEN PROB=P2a ANS=2 TRIES=6
INTER=44
INTER=-2
INTER=41
INTER=1
INTER=-2
INTER=2
ARM=GEN PROB=P2b ANS=2 TRIES=6
CENSUS m=0 inmask=1 outmask=3 inmask2=0 n=2
CENSUS m=1 inmask=1 outmask=2 inmask2=0 n=2
CENSUS m=2 inmask=1 outmask=1 inmask2=0 n=1
CENSUS m=3 inmask=1 outmask=2 inmask2=0 n=1
WIDEN=1
ARM=GEN PROB=P5 ANS=-2 TRIES=0
INTER=34
INTER=-2
INTER=31
INTER=1
INTER=-2
INTER=2
ARM=GEN PROB=P3 ANS=2 TRIES=6
INTER=213
INTER=-2
INTER=205
INTER=-2
INTER=-2
INTER=1
ARM=GEN PROB=Q1 ANS=1 TRIES=6
INTER=-2
INTER=205
INTER=-2
WIDEN=1
ARM=GEN PROB=Q2 ANS=-2 TRIES=3
INTER=213
INTER=205
INTER=-2
INTER=-2
INTER=213
INTER=222
INTER=-2
INTER=222
INTER=222
WIDEN=1
ARM=GEN PROB=Q3 ANS=-2 TRIES=9
INTER=213
INTER=-2
INTER=205
INTER=-2
INTER=-2
INTER=1
ARM=GEN PROB=Q4 ANS=1 TRIES=6
```

## The subsumption evidence (single-query)

On every single-query arm, GEN's answer set covers U's:

1. Same answers, same intermediates. Q1 logs INTER=213 (the identical
   intermediate U logged) before the solving INTER=1: GEN finds the same
   X-then-Y route (205->213->1), not a spurious one. P3 logs INTER=34 as
   U did. P1/P2a/P2b traces show the same two-stage routes.
2. Honest failure parity. Q2/Q3: both mechanisms exhaust, fire WIDEN=1
   exactly once, and return ANS=-2. GEN's Q3 additionally explores the
   rel-93 chain (213->222) that U's pair-only trial space cannot reach;
   it still fails honestly, so the larger trial space introduces no false
   positives here.
3. Strict improvement on P2b. U needed WIDEN=1 (7 tries) because its
   predicted handshake (A.out INTERSECTS B.in) rejected the true pair
   under the misleading contract. GEN's observed-kind handshake admits
   (X,Y) directly: 6 tries, no widening. Generality pays for itself.
4. Fresh-learner parity. Q4 (all masks empty): GEN ANS=1, as U.

Structural reading: U's trial space {singles, ordered pairs} with the
predicted handshake is a restriction of GEN's pool-rounds with
observed-kind checking. On linear pipelines every U-admitted trial is
also GEN-tried (GEN's 1-app admission checks strictly fewer conditions
than U's single admission; the observed intermediate kind grounds what
U's predicted intersection guesses). Combined with the pair6 result (GEN
solves the diamond that U provably cannot: U exhausts at TRIES=14
ANS=-2), GEN's single-query capability set strictly contains U's.

## The boundary (multi-query arena reuse)

U's K5 growth behavior (collapse report): P2b solved on arena A3 grows
X's contract; a later query (51->3) on the same arena is admitted
without widening (TRIES=4, ANS=3). This is the composer's admission
adapting from experience, the documented L2 connection.

GEN's frozen `gen_solve` resets tries/found/ans, pool[0], kind[0],
provenance[0], nv=1, and the widened flag, but NOT the tried1/tried2
tables (keyed by pool index). After P2b, tried1 marks exist for every
(m,0). P5's round 1 (ns0=1) skips every cell as already-tried: zero new
tries, pool unchanged, quiet=1, so WIDEN=1 fires, round 2 is quiet again,
and the solve returns ANS=-2 TRIES=0. The census proves the failure is
NOT in recording: m0 outmask grew to 3 exactly as U's did. It is purely
per-query trial-state scoping.

Fix (specified, not implemented here; needs its own prereg): reset the
tried1 (2304..3328) and tried2 (3328..3588) regions in `gen_solve`
alongside the existing resets. No design change; no new mechanism.

## Recommendation

Do NOT retire U as a separate mechanism yet. U remains the only working
reference for sequential contract growth across queries on one arena.
Recommended sequence:

1. Follow-up prereg: land the tried-state reset in GEN, rerun this
   battery plus the pair6 diamond battery. Predicted: P5 ANS=3 (TRIES to
   be measured; admission should need no widening given the grown
   contract), no regressions elsewhere.
2. If that passes, verdict upgrades to SUBSUMES and U is retired:
   U becomes the documented restriction of GEN (single-round linear
   pool, predicted handshake, stateless trial enumeration).

## Architecture accounting

- Cognition lines added: 0 (logic), 50 (gsu_main.zag driver only:
  world setup calls and solve/report invocations).
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- New behavior classes/opcodes: 0.
- Researcher-owned: frozen base/composer/world regions (byte-verified),
  driver main, prereg predictions.
- Learner-owned: kind-set contracts (census), grown contract on m0,
  admitted/rejected sets per query, pool contents, composite outcomes.
- Pinned znc 2026.07.0-dev via safebin (same pinned compiler as the
  collapse, pair5, and pair6 batteries).

## What this does not establish

- Try-efficiency parity (out of scope by design; GEN trades tries for
  generality: worse on P1/P2a/P3/Q1/Q4, better on P2b).
- Behavior on non-pipeline shapes beyond the established diamond.
- The side-effecting-MAP open question from the pair6 report (all MAPs
  here are pure).
- That the tried-state fix introduces no regressions (follow-up work).

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/gen_subsumes_u/`:
PREREG.md (frozen, committed alone before implementation, commit
483243867), NAMECHECK.md (Step 0 toolchain guard), gsu_base.zag,
gsu_gen.zag, gsu_world.zag, gsu_main.zag (only new code), gsu_full.zag
(assembled), gsu_bin (sha256
7f529b691e47c5f99ea035fe3df972c876ad020f47c6d7f96099f6993126b4e8),
gsu_run1/2/3.txt (byte-identical) + .err (empty), REPORT.md (this file).

## Notable details

- The Q1 arm is the first time GEN has run on the 5th pair's world
  (entities 201-206/211-213/221-222, relations 91/92/93): GEN had
  previously only been exercised on the collapse battery and the diamond
  worlds. It solved it with the same intermediate U found.
- One transient-free build: the E0101 warning (`adding 0 has no effect`
  in frozen `gen_addval`) is pre-existing in the pair6 source and was
  left untouched per the no-logic-change rule.
- Git note: the first commit attempt failed on pathspec ordering
  (`--` before `-m`); retried as `commit -m ... -- <paths>` and
  succeeded. Used `/usr/bin/git` directly per the safebin-symlink EPERM
  lesson.
