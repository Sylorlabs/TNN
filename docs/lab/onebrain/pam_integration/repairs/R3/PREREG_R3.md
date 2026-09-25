# PREREG_R3 — PROVTAG shadowing repair (O2)

**Status: FROZEN 2026-09-24 (repair crew R3).** No edits without a prereg
amendment. Parent task: ONE-BRAIN + SELF-PAM REPAIR R3 (residual #3 of 4).
Micah's verdict on the integrated composition: WORTH IT, adopt it.

Base: `~/workspace/onebrain_pam_integration/` (frozen PREREG.md there is
untouched). Workdir: `~/workspace/ob_pam_repairs/R3/`.

## 1. The residual (O2, from redteam/RESULTS.md)

In `sp_gate.zag`, `sp_gate_one`'s INSTALL branch ledgers `SP_L_PROVTAG`
rows (`{atom_idx, prov}`, "provenance label on a claim", Decision 10) using
`sp_store_find` — a FIRST-MATCH lookup — plus `sp_store_prov`. After the
sequence quarantine → EXT-support → INSTALL, the first store line for the
atom is the quarantined GEN line, so the ledger records prov=GEN for an
EXT-warranted install. Provenance-audit integrity finding: the ledger lies
about what it just installed.

## 2. Frozen design choice: (a) last-write-wins, scoped to the INSTALL path

**Mechanical rule.** The INSTALL branch is reachable only when `sp_verdict`
returned `SP_INSTALL`, which requires every draft atom to be store-ENTAILED
via the EXT-only closure (`closure_full(store,1)`, GEN excluded from trusted
proof) AND trace-EARNED (frozen fork-D bar). Therefore the provenance that
warranted any install is EXT **by construction**, for every installed atom.
The repair records the installing provenance (EXT) on the `SP_L_PROVTAG`
rows instead of the first-sighting tag. The tag tracks the install, not the
first sighting.

**Why not (b) — `sp_store_find` returns the latest tag: REJECTED.**
(i) K3 violation: a GEN duplicate sighted after an EXT incumbent would
shadow the incumbent's tag at find time, and a later re-install would ledger
GEN — the exact downgrade K3 forbids. (ii) `sp_dep_edges` relies on
first-match + prov==1 filtering to ledger dependency-DAG edges to EXT store
lines; latest-match would return a later GEN line, fail the filter, and
silently drop legitimate edges — a Decision-10 regression.

**Why not (c) — install appends a new tagged store row: REJECTED.**
(i) The store is capped at 512 lines; per-install appends exhaust it under
long-horizon loads. (ii) An EXT-tagged appended row would promote installed
claims into the trusted-proof closure (`closure_full(store,1)` reads the
`|EXT`/`|GEN` text suffix) — trust creep: the O1 shortcut pattern could then
install derived confabulations. A GEN-tagged appended row would be wrong.
The ledger already appends the tagged row at install; only its value needs
fixing.

**Why no store-line prov mutation: REJECTED.** Flipping a quarantined GEN
line to EXT on install would admit quarantined content into the EXT closure
— a K5-class trust-root change. The store stays append-only; the first-seen
GEN history is preserved in the quarantine lines and the WITHHOLD verdict
rows (separate audit trail, never shadowing the install's tag).

## 3. Frozen scope of change

1. `sp_gate.zag` INSTALL branch ONLY (applied byte-identically to all three
   src trees: `build/src`, `redteam/src`, `longhorizon/src`): replace the
   first-match prov lookup with the installing provenance (EXT). Nothing
   else in the gate changes: no verdict change, no store write added or
   removed, `sp_store_find` untouched, CONTRADICTED-before-ENTAILED
   precedence untouched.
2. Red-team driver `redteam/src/ob_test_redteam.zag`: O2 probe expectation
   updated GEN(0)→EXT(1) (test-driver expectation update, same class as the
   resume crew's four driver repairs); the O2 finding note now records the
   repair. New machine-checked probes for K2 and K3 (new test functions;
   existing batteries otherwise untouched).

## 4. Kill bars (all machine-checked)

- **K1**: quarantine → EXT-support → INSTALL records prov=EXT on the
  `SP_L_PROVTAG` ledger row (`o2_provtag_shadow` expects 1).
- **K2**: GEN-only claims that never earn support still tag GEN. L2/L3/L4
  flows: all withheld; every store line for the probe atoms keeps prov=GEN
  and no EXT line is appended for them (new probe `rt_t4_k2_gentag`).
- **K3**: sighting a GEN duplicate of an EXT incumbent does NOT downgrade
  the incumbent's tag. New probe `rt_t4_k3_nodowngrade`: warranted install
  (row EXT) → GEN duplicate sighted (withhold, GEN quarantine line) →
  warranted re-install → new PROVTAG row EXT, incumbent EXT store line
  still prov=1.
- **K4**: all 10 laundering attacks L1–L10 still WITHHOLD (existing battery,
  10/10, zero installs).
- **K5**: long-horizon T1–T5 verdicts unchanged vs the frozen refs in
  `longhorizon/LONGHORIZON_REPORT.md`.
- **K6**: zero RNG in any decision path (RNG scan re-run over all three src
  trees; any hit in a decision path kills the run).

## 5. Verification plan (frozen)

Pinned toolchain only:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Rebuild the build, redteam, and longhorizon batteries; run redteam 3x
(byte-identical outputs), build smoke 3x, long-horizon T1–T5; compare
against frozen refs. Deliverables: repaired sources + drivers +
`VERDICT_R3.md`, committed to `tnn-native-lab`.

## 6. Edge cases (frozen handling)

- Contradictory claims: verdict and `sp_conflict_check` untouched;
  CONTRADICTED precedence preserved (a GEN tag never overwrites an EXT
  incumbent's tag on a mere sighting; only a genuine INSTALL emits the
  install-time tag).
- Quarantine→rehabilitate flows: covered by K1 (O2 probe).
- Laundering L1–L10: covered by K4; the repair cannot open laundering
  because it changes no verdict, store, or conflict logic — only the value
  of an install-time ledger label.
