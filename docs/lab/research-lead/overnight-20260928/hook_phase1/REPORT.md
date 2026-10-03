# REPORT: HOOK-PHASE1

## Verdict

BUILD-PASS. All 10 frozen kill bars green (HQ-R1, HQ-A1, HQ-A2,
HQ-A3, HQ-A4, HQ-A5, HQ-A6, HQ-A7, HQ-H1; HQ-A1 counted separately
from HQ-R1 as the Phase-0 substrate check). Prereg fab65d9e0
committed strictly before any implementation.

This is infrastructure, not invention. Nothing in this lane claims
the learner learned, invented, or stamped anything. What was built:
(A2.3) a hook-slot consult in both world-mutation functions plus
install/uninstall helpers and a dispatch routine, verified inert
with slot 0 and verified to call the right slot exactly once per
mutation when a researcher-written probe body is installed. The
probe body is researcher-written; observing it fire is menu
selection, not invention (MUTATION-HOOK G3/G4).

## 1. Task

MUTATION-HOOK's incremental path: "Phase 1 (A2.3 inert dispatch, no
governance)". Build the hook dispatch infrastructure on
HOOK-PHASE0 (A2.6 event stream + A2.1 allocator/registry), with the
table inert (no learner-written bodies; that is A2.2, gated on
Micah's pending EXECUTE placement ruling). Verify the
infrastructure works: dispatch calls the right slot, inert means
no behavior change.

## 2. Implementation (additive deltas over HOOK-PHASE0, frozen)

Lane `docs/lab/research-lead/overnight-20260928/hook_phase1/`,
file prefix `hq_`, built on the HOOK-PHASE0 substrate (no
redesign).

- hq_world.zag, hq_module.zag, hq_learn.zag: byte copies of the hp_
  originals (cmp-verified identical, re-verified after the runs).
- hq_base.zag: hp_base.zag plus exactly three deltas:
  (a) fact_add gains `hk_fire(S,A,s,r,o);` inside the existing
  `if(n<64)` guard, after the 932 bump;
  (b) fact_set_obj gains `hk_fire(S,A,idx,0,o);` after the 932 bump;
  (c) appended A2.3 section: hk_install/hk_uninstall (slot writes),
  hk_bits (masked i64 reload), hk_fire (slot consult + indirect
  call). Lane-base code only: get32/set32, arithmetic, branch, plus
  fn-to-i64 / i64-to-fn casts and one indirect call (T1/T2-tested
  Zag language machinery, no new protected-core operation).
- hq_main.zag: hp_main.zag plus (a) top-level hq1_probe_body,
  RESEARCHER-WRITTEN: counts fires in S cell 1065, stashes the last
  payload (p0,p1,p2) in S cells 1066..1068; (b) STAGE HP-P1 (one
  contiguous block, zero removed lines) inserted after the
  SUMMARY-HOOKPHASE0 line, before o_flush. It exercises dispatch
  the way learner code could: pre-install inertness on both consult
  paths, install via fn bits, 70-add guard probe, set_obj payload
  probe, uninstall, would-be-fire probe.
- hq_build.sh mirrors hp_build.sh (pinned znc
  znc_linux_x86_64_abed8aa1, safebin PATH).

Cell audit (frozen in prereg): zero literal hits for 1063-1069 in
any hp_* source; the only computed access near the region is the
Phase-0 registry at 1030+n*4, n<8 (max cell 1061), count at 1062.
New cells: 1063/1064 (slot halves), 1065 (probe fire counter),
1066/1067/1068 (probe payload stash).

Payload convention (frozen, researcher-defined infrastructure
detail, no semantic claim): fact_add passes the stored triple
(s,r,o); fact_set_obj passes (idx,0,o). Consult placement:
post-commit, co-located with the A2.6 bump, so a rejected store
fires neither the counter nor the hook.

## 3. Results (frozen bars)

- HQ-R1 (regression): PASS. hq_run1.txt lines 1-146 byte-identical
  to hp_run1.txt lines 1-146. The consult is present on the hot
  mutation path and the pre-existing battery cannot observe it.
- HQ-A1 (Phase-0 substrate preserved): PASS. hq_run1.txt lines
  147-152 byte-identical to hp_run1.txt lines 147-152 (STAGE HP-P0
  block). Phase 1 did not perturb Phase-0 machinery.
- HQ-A2 (inert default): PASS. `f0=0` exactly: one fact_add and one
  fact_set_obj against slot 0 fired nothing on either consult
  path. A firing slot-0 consult would read f0>=1.
- HQ-A3 (fact_add dispatch exactness): PASS. `f1=64` exactly:
  70 adds produced 64 fires, matching the guard (64 stored, 6
  rejected) and the A2.6 counter delta. A consult outside the guard
  would read 70; a missing consult would read 0.
- HQ-A4 (add-path payload plumbing): PASS. `ap0=611 ap1=601
  ap2=621` exactly: the last add-phase payload is the stored
  triple (fact 0 of arena A: ES-E re-ran setup_worldA on A and
  wrote fact 0's object back unchanged; no later stage touches A).
  Wrong argument plumbing would fail this.
- HQ-A5 (fact_set_obj dispatch): PASS. `f2=67` and `lp0=2 lp1=0
  lp2=506` exactly: 3 set_obj calls fired, last payload (idx 2,
  placeholder 0, o=hs2c=506). A missing set_obj consult would read
  f2=64.
- HQ-A6 (uninstall restores inertness): PASS. `f3=67` exactly:
  after uninstall, 5 adds on a fresh arena plus 2 set_obj calls
  (7 would-be fires) produced zero new fires. A failed uninstall
  would read 74.
- HQ-A7 (protected core untouched, static audit): PASS.
  cmp-verified byte copies for world/module/learn; zero
  1063..1068/hk_ hits in world/module/learn; the base diff holds
  only the two consult lines and the hook section; zero modified
  tracked files outside the lane; znc untouched; new code uses only
  the frozen basis plus T1/T2-tested fn-value machinery.
- HQ-H1 (toolchain/hygiene): PASS. Safebin for all commands;
  `which python3`/`which python` empty; pure Zag; pinned znc;
  prereg committed alone before implementation (fab65d9e0);
  3/3 byte-identical runs, stderr empty, exit 0; zero em/en dash
  bytes; probe body labeled researcher-written; no invention
  claimed; no world literals in new executable code (probe triple
  and hs2c runtime-derived; hdok checks relational).
- Full HP-HOOK line exactly as frozen:
  `HP-HOOK f0=0 f1=64 f2=67 f3=67 ap0=611 ap1=601 ap2=621 lp0=2
  lp1=0 lp2=506`
- `SUMMARY-HOOKPHASE1 dispatch_ok=1`.

## 4. Toolchain finding (pre-prereg, kept honest)

Re-verifying the T2 fn-value round-trip pattern before freezing
the design exposed a latent ASLR hazard: reloading the i64 bits
with `(get32(S,off) as i64)` sign-extends bit 31, corrupting bits
32..63 of the fn address whenever the code address has bit 31 set.
The unmasked form segfaulted intermittently under ASLR (5/6 on one
probe binary, 4/10 on another). Masking the low half
(`&4294967295`) makes the round-trip exact; the full
install/fire/uninstall pattern ran 12/12 stable pre-prereg, and
the shipped binary ran 13/13 (3 frozen runs + 10 ASLR stress runs)
with exit 0 and byte-identical output. The mask is in the frozen
design. This is a toolchain-correctness detail of the probe
pattern, not a research result. Probe files live in /tmp only.

## 5. Honest labeling (what this is not)

- The slot, consult, install/uninstall helpers, and dispatch
  routine are researcher-placed infrastructure, not a learner
  invention. A learner writing fn bits to the slot would be
  selection among researcher-compiled bodies: menu selection under
  the L3 bar, explicitly not invention (MUTATION-HOOK G3/G4).
- The probe body is researcher-written. Its firing proves the
  dispatch path works; it proves nothing about learning.
- Phase 1 changes nothing about what the learner can DO with
  mutation events in the strong sense: no learner-constructed
  bodies exist, and none can until A2.2 lands (gated on the
  EXECUTE ruling). The strong sense of A2.3, and A2.4/A2.5, are
  not started here.
- The hook fires post-commit by design; pre-commit interception
  (veto/gating semantics) was not built and is not claimed.
- 56 facts is a toy world; the consult is O(1) machinery, not a
  scaling result.

## 6. Artifacts

- `NAMECHECK.md`: toolchain guard Step 0, scope, commit discipline,
  pre-prereg probe finding.
- `PREREG.md`: frozen kill bars (committed alone at fab65d9e0).
- `REPORT.md`: this file.
- `hq_base.zag`, `hq_world.zag`, `hq_module.zag`, `hq_learn.zag`,
  `hq_main.zag`, `hq_build.sh`: implementation.
- `hq_full.zag`, `hq_bin`, `hq_compile.txt`: build products.
- `hq_run1/2/3.txt`: 3/3 byte-identical (155 lines), stderr empty,
  exit 0. Plus 10/10 ASLR stress runs, exit 0, output identical
  (evidence in /tmp, not lane artifacts).

## 7. Follow-ups (not started)

- Phase 2 (A2.2, A2.3 strong sense, A2.5, A2.4): gated on Micah's
  EXECUTE placement ruling (MUTATION-HOOK G1). Not started here.
  This lane must not take that step unilaterally.
