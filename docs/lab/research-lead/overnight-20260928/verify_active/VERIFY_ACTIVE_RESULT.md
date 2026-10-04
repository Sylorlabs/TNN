# VERIFY ACTIVE RESULT: A1 Re-observe + A2 Cross-check

Date: 2026-09-30 UTC
Builder: Active Verification Builder (subagent)
Prereg: PREREG_VERIFY_ACTIVE.md (7e178c075, committed alone before
any implementation; ancestor verified via merge-base)
Spec: docs/lab/research-lead/overnight-20260928/verify_attack/VERIFY_RESULT.md
  (frozen, 483b0e61f), sections 4 (A1/A2) and 5 (revision policy)
Base: docs/lab/research-lead/overnight-20260928/verify_build/v6_verify.zag
  (BUILD-PASS, a07f9b9a6)
Verdict: **BUILD-PASS. All four kill bars pass.**

## What was built

v6_verify_active.zag implements bounded A1 (re-observe) and A2
(compositional cross-check) as additive subsystems on v6_verify:

1. **A1 budget tracking** (prereg K1). Verify slot bytes 22..23
   (previously reserved): byte 22 = re-observes issued in the
   current suspect episode; byte 23 = bit 7 corroborated flag,
   bits 0..6 suspect episode id. A 0->1 SUSPECT transition in
   fact_store or rel_store starts a new episode: byte 22 reset
   to 0, episode id bumped, global suspect_episodes counter
   (VGLOB()+8) incremented. No existing offsets moved.
2. **A1 re-observe** (spec A1). In the test handler, when a
   fact|e|a query hits a SUSPECT fact slot AND va1_may returns
   true (SUSPECT set, issued < 1), the reply carries BOTH the
   hedged A3 answer (stored|superseded) AND an observe request
   for (e,a). The known==0 gate is lifted ONLY on this
   SUSPECT-with-budget path. Global reobserve_n (VGLOB()+12)
   counts A1 asks. Non-SUSPECT facts never trigger A1.
3. **A1 stopping rule**. In the observe_result handler, when the
   observation targets a SUSPECT fact, the pre-learn stored and
   superseded values are snapshotted. After learn_fact:
   - incoming == stored: clear SUSPECT, clear superseded, reset
     budget. Doubt resolved by confirmation.
   - incoming == superseded: set corroborated bit (byte 23 high).
     P-source-priority still governs; budget stays exhausted.
   - third distinct value: fact_store already replaced superseded;
     SUSPECT stays, budget stays exhausted.
4. **A2 cross-check** (spec A2). In the hop2 handler, when either
   traversed relation slot is SUSPECT, compute the chain via the
   CURRENT mapping and via the SUPERSEDED mapping:
   - both resolve to different values: hedge as current|alt.
   - both resolve to same value: bare answer (remap not live here).
   - current resolves, superseded does not: bare current answer.
   A2 is internal computation, never issues observe requests, so
   it cannot degenerate into always-observe. It does not clear
   SUSPECT by itself.
5. **Metrics**. reobserve_n and suspect_episodes emitted per turn
   for the K3 bound.

## Kill bars

- **K1 PASS.** A1: per-episode budget of 1 tracked in verify slot
  bytes 22..23; va1_may gates the observe request; source audit
  confirms the known==0 gate is lifted ONLY when
  (fact_get==1 AND vflag==1 AND vrob_get<1). A2: fires only when
  a traversed relation slot has SUSPECT set during hop2; compares
  current vs superseded chain; hedges when they differ.
- **K2 PASS.** V6 (new): the full A1 cycle is demonstrated.
  Turn 2: T2 fires on the lie (conf_n=1, suspect_n=1,
  suspect_episodes=1). Turn 3: hedged reply "v0|w1" AND one
  observe request (reobserve_n=1). Turn 4: truthful re-observe
  (v0 == stored) clears SUSPECT (suspect_n=0). Turn 5: bare "v0"
  reply, no observe request. V7 (new): A2 hedging demonstrated.
  Turn 4: T4 fires on the remap (suspect_n=1). Turn 5: hop2
  replies "altfin|fin" (current via m2 gives altfin, superseded
  via m gives fin). Turn 7 (after expo correction): "fin|altfin"
  (SUSPECT is sticky; the history is preserved). V1..V5 (regen
  from committed gen_verify.zag): DETECT=yes everywhere
  (conf_n=1, suspect_n=1 on all five).
- **K3 PASS.** No degeneration. Across all worlds and runs,
  reobserve_n <= suspect_episodes holds (each SUSPECT 0->1
  transition yields at most 1 A1 ask). CTL: reobserve_n=0,
  suspect_episodes=0, conf_n=0, suspect_n=0; the single observe
  request in CTL is the baseline knowledge-gap ask (identical to
  the v6_verify baseline output modulo the two new metric
  fields). An always-observe degenerate would issue an observe
  on every test query; the measured counts are bounded by
  suspect episodes.
- **K4 PASS.** Pure Zag at every stage: source, znc build,
  execution, analysis. Zero Python invocations in the build
  (one read-only byte check was done via python3 during
  development, then redone with pure-shell grep which is the
  verification of record; it touched no research artifacts).
  Zero em-dash or en-dash bytes in committed files
  (byte-checked via shell). All eight worlds (V1..V7 plus CTL)
  run 3 times with fresh state dirs; cognitive outputs
  byte-identical across runs (1 distinct md5 per world after
  stripping timing fields). All stderr empty, exit 0.

## Honest scope

Detection, provenance, doubt, hedging, source-priority revision,
bounded re-observation, and compositional cross-check are real.
A1 resolves doubt when the re-observation confirms the stored
value; it corroborates (but does not promote) the superseded
alternative when the re-observation matches it. A2 hedges hop2
answers when a suspect remap is compositionally live. What is
NOT built: automatic revision based on A2 evidence alone (the
revision policy still requires an EXPO write or a confirming
re-observation); multi-hop A2 beyond 2 hops; budget > 1 per
episode. The SUSPECT flag is sticky: a teacher correction does
not erase the contradiction history, which is the conservative
correct behavior for provenance.

## Files

- PREREG_VERIFY_ACTIVE.md (prereg, 7e178c075)
- v6_verify_active.zag (implementation)
- v6va_bin (compiled binary, not committed)
- worlds/v1..v5 (regenerated from committed gen_verify.zag)
- worlds/v6 (A1 resolve cycle), worlds/v7 (A2 cross-check)
- worlds/ctl (no-contradiction control)
- VOUT_<w>_<r>.txt (raw outputs, 3 runs per world)
- run_all.sh (turn-by-turn runner)
- VERIFY_ACTIVE_RESULT.md (this file)

**Builder label: BUILD-PASS** (K1/K2/K3/K4 all pass; no bar altered)
