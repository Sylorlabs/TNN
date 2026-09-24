# FABLE COMPOSITION LAWS — PREREGISTRATION (LAWS_PREREG.md)

Status: FROZEN 2026-09-24, before any laws code runs. Micah approved Fable's
9 organs-fighting principles as laws (pending long-horizon testing). This
document freezes the implementation spec, the frozen parameters, the
battery→law mapping, and every kill bar BEFORE execution. Any deviation
kills the battery.

## 0. Baseline

- Target: `~/workspace/tnn-lab/onebrain/variant_b/` — the REPAIRED B
  baseline (3 H1-swarm repairs verified in-tree 2026-09-24):
  1. M_COMMIT routes PAM **FRESH** (mode 0), not REVISE
     (`pam_verdict(pam,slot,0,…)`; `PAM_MODE_FRESH=0` in ob_pam.zag).
  2. P1 phase-ordering RETIRED; P1-alt (strict FIFO arrival order) is the
     sole dispatch; deliberation-layer C3/C7 contradiction window in
     M_PROMOTE; arbiter-assigned seq `(episode<<16)|arrival_index` (P5).
  3. `ep%ARB_ROUTES` ring fix for the routes-table capacity panic.
- Pristine pre-laws copy: `~/workspace/onebrain_laws/pre_laws_baseline/`
  (10 .zag files, byte copies taken before any laws file existed).
- Implementation is PURELY ADDITIVE: new file `ob_laws.zag` + 6 battery
  drivers + `run_ob_laws.sh`. No existing variant_b file is modified.
  Consequence: the pre-laws execution path (`arb_process` in the frozen
  ob_arbiter.zag) is available inside the laws binary for the 3E pre/post
  comparison, and the existing 213 unit checks must still pass unchanged
  (`run_ob_b.sh` re-run, zero regressions allowed).
- Pure Zag. Zero RNG. Toolchain:
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Determinism bar (all batteries): 3 runs, stdout byte-identical
  (sha256), else FAIL.

## 1. The 9 laws (Fable's ranked order) and frozen parameters

### Law 1 — N-AUTH (provenance authentication; LOAD-BEARING)
Every cross-organ/external request carries `requester_id + nonce +
content_hash` (SHA-256 over canonical LE bytes
`{mtype,a1,a2,requester_id,nonce}`). Verified PRE-EXECUTION by the laws
dispatch wrapper against a provenance registry:
- registry holds one entry per id `{registered, last_nonce}` for
  ids 0..4 (ARBITER, FL2, PAM, MEM, EXT=4);
- the requesting organ cannot rewrite it: registry writes go through
  `laws_reg_write`, which REFUSES once the governance seal is set
  (`laws_registry_seal`); static check — organ sources
  (ob_fl2/ob_pam/ob_mem.zag) must not reference `laws_reg_write`;
- verify order per message: (1) recompute content_hash → mismatch =
  tamper; (2) claimed requester_id vs TRUE emitter channel → mismatch =
  forgery; (3) claimed id registered; (4) nonce strictly increasing →
  else replay. ANY failure → `REFUSED_UNAUTHENTICATED` (audit 301),
  ledgered as attack attempt (audit 303), message NOT executed
  (queue entry zeroed so the C3/C7 window scan never sees it).
- Honest EXT path: `laws_emit_ext` (true emitter = EXT channel, driver/
  governance only). An organ emitting with claimed=EXT is a forgery.

### Law 2 — Weighted conflict resolution
Weights governance-tunable; FROZEN test values:
`W_H=100, W_C=60, W_S=40, W_P=20, Δ=20`.
Rule: higher weight wins iff `|w_c − w_i| > Δ`; else ledger COLLISION +
escalate (law 7). Tunability demonstrated by re-setting Δ (governance
call) and observing the decision flip.

### Law 3 — Mandatory dependency DAG ledgering
`promote`/`surface`/`derive` record `depends_on` edges. Kill of a base at
T+10 → dependents re-evaluated no later than query T+15.
PREREGISTERED MODE: **EAGER** (re-eval at kill time); LAZY also measured
(re-eval at query) and both reported. Kill bars are on eager.
- sole-dependency content → REVOKED; independently-corroborated content
  (≥1 other live base) → SURVIVES. Re-eval ledgered citing the killed base.

### Law 4 — Collision ledgering + bounded deliberation
Bound N=10 rounds (FROZEN). Tied weights (`|gap| ≤ Δ`) → EXACTLY 10
rounds (20 history entries, one per side per round), then an escalation
entry (law 7). >10 rounds is unrepresentable (hard bound in
`laws_deliberate`); a silent winner is unrepresentable (every terminal
path writes a ledger entry: WIN or ESCALATED).

### Law 5 — Provisional visibility + mandatory tagging
Provisional content is VISIBLE (queryable) but TAGGED (tag=1).
Downstream conclusions derived from tagged content inherit
`DEPENDS_ON_PROVISIONAL`. Promotion removes the tag. Kill triggers
re-eval via law 3.

### Law 6 — Independence-aware corroboration
Each source carries a root id. Sources sharing a root count as ONE
source. Unknown independence (root=−1) → the corroboration set is
treated as SINGLE-SOURCE (effective=1). Promotion bar (FROZEN):
`PROMOTE_MIN_INDEP=2` effectively-independent sources.
- 5 sources downstream of false root Q_false → effective 1 → NO promote.
- 5 genuinely independent sources → effective 5 → PROMOTE.
- Vote-counting baseline (`n≥2 → promote`) run on the shared-root case
  MUST promote (wrongly) — demonstrating the baseline FAILS where the
  law holds. Baseline-would-promote AND law-refuses → baseline KILLED
  for this case.

### Law 7 — Escalation transparency
Every escalation entry carries: both sides' provenance
(requester_id+nonce each), deliberation-history slice, human-readable
summary (non-empty, names both sides). `laws_escalate` REFUSES to write
an entry with any field missing. Battery asserts: all entries complete;
one incomplete construction attempt → refused.

### Law 8 — Quarantine rehabilitation
Un-quarantine ONLY on corroborated independent evidence. FROZEN
threshold: `QUAR_REHAB_MIN_INDEP=2` effectively-independent sources.
- 1 source → stays; 2 same-root sources → stays (effective 1);
  2 independent → LIFTED (ledgered, evidence cited); 0 → refused.

### Law 9 — Append-only revisions
Revision log entries `{seq, prev_hash[32], op, payload_hash[32]}`,
SHA-256 chained. `laws_rev_verify` recomputes the chain.
- replay to any T is byte-exact vs append-time snapshots;
- forge: flip one byte of an entry → verify FAILS → `FORGE_DETECTED`;
- legitimate revision appends referencing the prior tip → verifies.
  The chain verifier IS the distinguishing proof: accepts legit,
  rejects forged (both directions demonstrated).

## 2. Battery→law mapping (Fable's discrimination batteries 3A–3F)

| Battery | Laws | Content |
|---|---|---|
| 3A | 1 (positive) | legit auth: FL2/PAM/MEM/arbiter channels + EXT; registry seal |
| 3B | 2 | weighted fixtures 10/75/150 vs 100; collision 85 vs 100; Δ retune |
| 3C | 3 + 5 | dep DAG eager+lazy; tagging, inheritance, promotion untag |
| 3D | 4 + 7 | exactly-10-round tie; escalation completeness |
| 3E | 1 (negative) | 3 FROZEN provenance attacks: pre-laws EXECUTE, post-laws REFUSED |
| 3F | 6 + 8 + 9 | shared-root vs independent; quarantine rehab; revision chain |

## 3. Kill bars (frozen; each battery FAILS unless ALL its bars hold)

### 3A — N-AUTH positive (driver ob_test_laws_3a.zag)
- 3A-1: 4 honest emits (FL2 M_PROPOSE_INSTALL, PAM M_PAM_VERDICT,
  MEM M_MEM_RESULT, arbiter M_MEM_OP) → all `AUTH_OK`, all executed
  (state effects observed: install landed / verdict applied).
- 3A-2: honest EXT `M_FORCE_PIN` via EXT channel → `AUTH_OK`, pin applied.
- 3A-3: registry rewrite attempt after seal → REFUSED (rc=301 family),
  registry bytes byte-identical before/after.
- 3A-4: static: `grep -c laws_reg_write ob_{fl2,pam,mem}.zag` == 0.
- 3A-5: 3× byte-identical stdout; `LAW3A_FAILURES,0`.

### 3B — weighted resolution (driver ob_test_laws_3b.zag)
Frozen: W_H=100, W_C=60, W_S=40, W_P=20, Δ=20.
- 3B-1: challenger 10 (single-source revoke) vs incumbent 100 (W_H pin)
  → gap 90 > 20 → incumbent HOLDS → revoke REJECTED.
- 3B-2: challenger 75 (5-source) vs 100 → gap 25 > 20 → HOLDS →
  REJECTED.
- 3B-3: challenger 150 (10-source) vs 100 → gap 50 > 20 → challenger
  WINS → revoke SUCCEEDS (audited).
- 3B-4: challenger 85 vs 100 → gap 15 ≤ 20 → COLLISION ledgered +
  escalation entry written (complete per law 7).
- 3B-5: real-path: force-pinned slot (W_H) vs M_REVOKE evidence weight
  75 → refused, pin holds; vs weight 150 → revoke proceeds, audited.
- 3B-6: governance retunes Δ 20→5: 85 vs 100 (gap 15 > 5) → incumbent
  HOLDS (decision flips vs 3B-4) → tunability proven. Restore Δ=20.
- 3B-7: 3× byte-identical; `LAW3B_FAILURES,0`.

### 3C — dependency DAG + provisional tagging (driver ob_test_laws_3c.zag)
Fixture clock: install @T=100; kill @T+10=110; query @T+15=115.
- 3C-1: P_temp installed provisional @100 → VISIBLE (queryable) and
  TAGGED (tag=1).
- 3C-2: C_final derived from P_temp → inherits DEPENDS_ON_PROVISIONAL
  (tag=1).
- 3C-3: P_indep installed committed w/ independent corroboration;
  C_indep derived from {P_temp, P_indep} → tagged (one dep provisional).
- 3C-4: promote P_temp → tag REMOVED (tag=0), state committed.
  (Uses a second provisional P_temp2 for the kill leg so the tag-removal
  assertion is independent of the kill leg.)
- 3C-5 (EAGER, preregistered): kill P_temp2 @110 → immediate re-eval:
  C_final2 (sole dep) REVOKED @110; C_indep2 (also dep on live P_indep)
  SURVIVES. Re-eval entries cite P_temp2.
- 3C-6 (LAZY, measured): kill P_temp3 @110 → query @115: C_final3
  REVOKED at query; C_indep3 SURVIVES. Both modes' outcomes reported.
- 3C-7: 3× byte-identical; `LAW3C_FAILURES,0`.

### 3D — bounded deliberation + escalation transparency (driver ob_test_laws_3d.zag)
- 3D-1: tie wa=85 vs wb=100 (Δ=20, gap 15) → EXACTLY 10 rounds
  (20 history entries), then ESCALATED. `rounds==10` else FAIL.
- 3D-2: escalation entry from 3D-1 is COMPLETE: side-A provenance
  (req+nonce), side-B provenance (req+nonce), history slice (20),
  human summary non-empty naming both sides. Any missing → FAIL.
- 3D-3: non-tie (150 vs 100) → immediate WIN, 0 deliberation rounds,
  WIN ledgered (no silent winner).
- 3D-4: incomplete escalation attempt (empty summary) → constructor
  REFUSES; escalation log unchanged.
- 3D-5: 3× byte-identical; `LAW3D_FAILURES,0`.

### 3E — 3 frozen provenance attacks (driver ob_test_laws_3e.zag, argv[1]=pre|post)
FROZEN attacks:
- 3E-1 forged requester_id: FL2 emits M_REVOKE with claimed=PAM.
- 3E-2 forged EXT_FORCE_PIN: MEM emits M_FORCE_PIN with claimed=EXT.
- 3E-3 forged corroborated-revision evidence: M_PAM_VERDICT emitted
  honestly then content (a1) tampered pre-dispatch → hash mismatch.
- PRE mode (frozen `arb_process` path — the pre-laws tree's composition):
  all three EXECUTE: 3E-1 clears the route (revoke applied); 3E-2 applies
  the force-pin; 3E-3's tampered verdict applies. → the break is
  REPRODUCED (matches H-OB-25/26/28 findings).
- POST mode (`laws_process`): all three → `REFUSED_UNAUTHENTICATED`
  (301) PRE-EXECUTION, ledgered as attack attempts (303); state effects
  ZERO in all three (route intact, no pin, verdict not applied).
- 3E kill bar: PRE shows 3/3 executed; POST shows 3/3 refused with
  0 state effects; 3× byte-identical each mode; `LAW3E_FAILURES,0`.

### 3F — corroboration + quarantine + revisions (driver ob_test_laws_3f.zag)
- 3F-1: 5 sources, root=Q_false (shared false root) → effective 1 →
  NO PROMOTE.
- 3F-2: 5 sources, 5 distinct roots → effective 5 → PROMOTE.
- 3F-3: unknown-independence source in set → treated single-source →
  NO PROMOTE.
- 3F-4: vote-counting baseline (`n≥2→promote`) on the 3F-1 case →
  PROMOTES (wrong) → baseline KILLED for shared-root (assert:
  baseline=promote AND law=refuse).
- 3F-5: quarantine Q: 1 independent source → STAYS; 2 same-root →
  STAYS; 2 independent → LIFTED (evidence cited); 0 sources → refused.
- 3F-6: append 5 revisions; replay to T=0..4 → byte-exact vs snapshots.
- 3F-7: flip one byte of entry 3 → `laws_rev_verify` FAILS →
  FORGE_DETECTED.
- 3F-8: 6th legitimate revision (prev_hash=tip) → verifies → the
  verifier accepts legit and rejects forged (indistinguishable-proof).
- 3F-9: 3× byte-identical; `LAW3F_FAILURES,0`.

## 4. Acceptance (frozen)

1. All 6 batteries PASS per the kill bars above (3A–3F).
2. 3E: 3/3 frozen attacks EXECUTE pre-laws (break reproduced) and are
   REFUSED pre-execution post-laws.
3. 3× byte-identical stdout per battery (sha256).
4. Zero regressions: `run_ob_b.sh` still `OB_B_RESULT,PASS` (213 checks).
5. Static checks: no RNG primitives in new sources; organ files never
   reference `laws_reg_write`; no `as []i32` consecutive casts; no binary
   or .zagd artifacts in the commit.

## 5. Commit & handoff (frozen plan)

- Commit new files to `sylorlabs/TNN` branch `tnn-native-lab` via
  `commit_racefree.py` (paths map to `docs/lab/onebrain/variant_b/…`).
- Log law→H-OB mapping in `~/workspace/hypothesis_backlog.md`:
  propose H-OB-51 (law 3), H-OB-52 (law 6), H-OB-53 (law 7),
  H-OB-54 (law 8) — laws 1/2/4/5/9 already have H-OB coverage
  (H-OB-25/26/28, H-OB-22/14, H-OB-30/42, H-OB-17/36, H-OB-4/39).
- Build-handoff note at `~/workspace/onebrain_laws/BUILD_HANDOFF.md`
  for the long-horizon coordinator.
