# REPORT: GEN-STATEFIX -- Verdict UPGRADE-TO-SUBSUMES

Date: 2026-10-03. Worker: GEN-STATEFIX. Lane:
`docs/lab/research-lead/overnight-20260928/gen_statefix/`.
Branch: `lane-genstatefix-20261003` (isolated; explicit pathspecs; local only).

## Verdict: UPGRADE-TO-SUBSUMES. Recommend retiring U as a separate mechanism.

The follow-up prereg to GEN-SUBSUMES-U (C397) landed the specified tried-state
reset in `gen_solve`. P5 (sequential contract growth) now passes: ANS=3 with
no widening, on the same arena where P2b grew the contract. Every other GEN
result is unchanged: all 9 subsumes-battery arms except P5 are byte-identical
to the frozen GEN-SUBSUMES-U output, and the full diamond battery is
byte-identical to the frozen COMPOSE-PAIR6-ADV GEN output. The residual
boundary characterized in C397 is closed. U is now the documented restriction
of GEN (single-round linear pool, predicted handshake, stateless trial
enumeration) and should be retired as a separate mechanism.

## Kill bar results

All frozen predictions from PREREG Sec 4 hit, except the auxiliary TRIES
prediction for P5 (see Erratum below; not a kill criterion). 3/3 runs
byte-identical per battery (stdout sha256
`c87c18964a6fd9a7554e76c23b96d0c1034c7cd5884afbc3bc9e686024925fad`
for the subsumes battery,
`962ca4f0f65228d92b007b5194852f2778d7b52e583442e8bf687b451bc76f84`
for the diamond battery; stderr empty).

- K1 GROWTH FIXED: PASS. P5 block:
  ```
  INTER=53
  INTER=-2
  INTER=51
  INTER=1
  INTER=-2
  INTER=3
  ARM=GEN PROB=P5 ANS=3 TRIES=6
  ```
  No WIDEN=1 in the P5 span. The second query on the P2b arena re-enumerates
  the trial space (tried1/tried2 reset), rides the grown contract
  (m0 outmask=3 from the census), and solves via COUNT(53,82)=3.
- K2 NO REGRESSION (subsumes battery): PASS. Every non-P5 block (P1, P2a,
  P2b, census, P3, Q1, Q2, Q3, Q4) byte-identical to `gsu_run1.txt`
  (verified by excising the P5 block by line range and diffing: empty).
- K3 NO REGRESSION (diamond battery): PASS. `gsf_diamond_run1.txt`
  byte-identical to `g1_run1.txt` (cmp empty): P1/P2a/P2b/P3 regression,
  Q1 diamond (ANS=5 TRIES=8), census, Q2 (ANS=5 TRIES=47, WIDEN=1 once).
- K4 DETERMINISM: PASS. 3/3 byte-identical per battery; stderr empty.
- K5 FIDELITY: PASS. `gsf_base.zag` empty diff vs `d6_base.zag`;
  `gsf_world.zag` empty vs `gsu_world.zag`; `gsf_main.zag` empty vs
  `gsu_main.zag`; every assembled region empty vs its reference;
  `gsf_gen.zag` diff vs `gsu_gen.zag` shows ONLY the PREREG Sec 2 hunk.
- K6 TOOLCHAIN: PASS. Safebin active for every command; `which python3`
  and `which python` return nothing; zero forbidden-executable
  invocations; pure Zag; shell only for znc/binary/git/assembly/verify.
- K7 HYGIENE: PASS. Zero em/en dash bytes in lane-authored docs
  (byte-verified). The only dash bytes in the lane are compiler-emitted:
  znc's own warning text ("result is discarded") inside the two build logs
  `gsf_compile_gsu.err` / `gsf_compile_diamond.err`; verified by grep that
  no other lane file contains them.

## Full new output (Battery A, identical across 3 runs)

P1/P2a/P2b/census/P3/Q1/Q2/Q3/Q4 blocks are byte-identical to the frozen
GEN-SUBSUMES-U output. The only changed block is P5 (old: `WIDEN=1` /
`ARM=GEN PROB=P5 ANS=-2 TRIES=0`; new: the K1 block above).

## Erratum (honest disclosure)

The frozen PREREG Sec 4 derivation predicted P5 TRIES=10, hand-derived as
(0,0) WALK(51,81)=52. The true logic gives INTER=53 on the first app:
`walkf` is transitive (follows the 81-chain 51->52->53 until no next step),
so pool=[51,53,1] after round 1 and (1,1) COUNT(53,82)=3 succeeds in round
2: TRIES=6, not 10. The bar-level predictions (ANS=3, no WIDEN=1) held
exactly, and TRIES was explicitly not a kill criterion, so K1 still passes
per its frozen text. The error was in my hand-derivation (I applied the
single-step WALK reading from the P1 route note instead of the transitive
`walkf` in the frozen base), not in the fix; the fixed logic behaved exactly
as specified. The prereg is NOT amended post-hoc; the error stands as
recorded.

## The fix (minimal diff, no redesign)

One hunk in `gen_solve`, inserted after the existing resets:

```
  // GEN-STATEFIX: per-query tried-state scoping. Clear tried1 (2304..3328)
  // and tried2 (count at 3328) so a later query on the same arena
  // re-enumerates the trial space. Contract-growth state lives in the
  // census-visible masks, not in these tables.
  let zti:i32=0;
  while(zti<256){
    set32(A,2304+zti*4,0);
    zti=zti+1;
  }
  set32(A,3328,0);
```

tried1 is 4 maps x 64 pool indices x 4 bytes (256 i32 cells, 2304..3328);
tried2 entries are governed by the count at 3328, so resetting the count
suffices. The done set is re-zeroed by every `gen_record` call and the visit
stack is locally indexed, so they needed no reset. On a fresh arena the
reset is a no-op on already-zero tables, which is why K2/K3 hold.

## Why the verdict upgrades

GEN-SUBSUMES-U established: GEN reproduces U's answers on all 5 pipeline
pairs, fails honestly where U fails honestly, succeeds on a fresh learner,
and solves the diamond U provably cannot. The sole residual boundary was
multi-query arena reuse for contract growth (stale tried-state). This lane
closed it: P5 now returns ANS=3 with no widening, and the census still shows
the grown contract (m0 outmask=3) that the fix rides on. Nothing else in
GEN's behavior moved. U's capability set is now covered by GEN on every
tested arm: 5 pairs, honest failures, fresh learning, the diamond, and
sequential growth.

## Recommendation

Retire U as a separate mechanism. U becomes the documented restriction of
GEN: single-round linear pool, predicted outmask INTERSECTS inmask
handshake, stateless per-query trial enumeration. GEN keeps every U
principle (kind-set contracts, compatibility admission, deterministic
ordered trial, end-to-end verification, failure-triggered widening,
provenance-based success-recording with contract growth) and generalizes
the trial space to rounds over a value pool with observed-kind checking and
per-query trial-state scoping.

## Architecture accounting

- Cognition lines added: 0 (logic), 10 (the fix hunk: 4 comment lines, 6
  code lines, all inside `gen_solve`).
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- New behavior classes/opcodes: 0.
- Researcher-owned: frozen base/composer/world/driver regions
  (byte-verified), the tried-state reset hunk, prereg predictions.
- Learner-owned: kind-set contracts (census), grown contract on m0,
  admitted/rejected sets per query, pool contents, composite outcomes.
- Pinned znc 2026.07.0-dev via safebin (same pinned compiler as the
  collapse, pair5, pair6, and subsumes batteries).

## What this does not establish

- Try-efficiency parity (out of scope by design; GEN trades tries for
  generality: P5 takes TRIES=6 where U took 4).
- Behavior on non-pipeline shapes beyond the established diamond.
- The side-effecting-MAP open question (all MAPs here are pure).
- Multi-query reuse beyond one sequential growth step.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/gen_statefix/`:
PREREG.md (frozen, committed alone before implementation),
NAMECHECK.md (Step 0 toolchain guard), `gsf_base.zag` (byte-copy of
`d6_base.zag`), `gsf_gen.zag` (fixed composer; sha256
`9d33729e1c2e6dbd6d2fb7de39c84afb99190980e8a0aac58cfbee72171206bb`),
`gsf_world.zag`, `gsf_main.zag`, `gsf_full_gsu.zag` (sha256
`b3167060cf1248dee49a2799a4df20f95a28a13d5806dd623f3c3578181ea56e`),
`gsf_full_diamond.zag` (sha256
`b3e9bf41db486046d5306c75ed34dc75e81b931a14a0c9aecc78b3c1938834b7`),
`gsf_bin_gsu` (sha256
`723cc7a3aab0f4659e6ae2abb5b4cc48473f19285869509dc193e5eaa599b2b9`),
`gsf_bin_diamond` (sha256
`f8c9b1c45be7ce8ac25f4f35a23da170785fa32ba1a8715bfe17ca1a16084ea8`),
`gsf_gsu_run1/2/3.txt` (byte-identical) + `.err` (empty),
`gsf_diamond_run1/2/3.txt` (byte-identical) + `.err` (empty),
REPORT.md (this file).

## Notable details

- The E0101 warning (`adding 0 has no effect` in frozen `gen_addval`) and
  the two A0102 notes are pre-existing in the pair6 source and were left
  untouched per the no-logic-change rule.
- The P5 INTER trace shows the fix riding the grown contract exactly as the
  C397 recommendation predicted: admission needs no widening because m0's
  outmask grew to {1,2} from P2b's success-recording.
- Git note: one commit attempt hit index.lock contention (routine on the
  shared branch); retried after 25s backoff and landed. Used `/usr/bin/git`
  directly per the safebin-symlink EPERM lesson. Explicit pathspecs on
  every commit.
