# PINS — SCOPE-S DEPRECATION: EXECUTION ADDENDUM

**Crew:** P1 (marathon) · **Date:** 2026-09-21 ·
**Authority:** RDTDT brief `PINS_RDTDT_BRIEF.md` §§5–8 (D2-A verdict: Scope-S) +
Micah's 2026-09-21 standing instruction — evidence-decided items get EXECUTED,
not parked; tests determine outcomes, not preferences.
**Status:** EXECUTED and verified on the real tree. Single coherent change, one
commit.

## 1. What was deleted

`units/teachers/learner/store.zag` — the 9-line learner-side pin writer
`fn pins_add` (ex store.zag:149-157), replaced with a dated deletion note.
The same deletion was applied to the vendored copy
`forcepin/scratch/store.zag` (byte-identical twin; its scratch build never
called the writer, so it still builds).

**Scope-S, exactly as preregistered:** KEPT — `struct Pins`, `pins_init`,
`pins_check` (read-only), the `dlb_digest` pins fold, the always-0 `EV_PINRES`
emission. The retained ELIMINATE read path (`delib.zag:700`) is provably dead
with no writer (`pins_check` → 0 on all spans — 40/40 spans, T2-α).
**Not Scope-F:** full struct deletion was killed in D2 (breaks digests even
with zero pins, fails frozen B.4 replay).

**Why deletion (evidence, not preference):** HTD Test 5 — the writer violated
Micah's ruling 3/3: retract of pinned vs unpinned span bit-identical (no
erase-cost linkage), zero removal symbols repo-wide (de-facto permanent
in-session), trainer could not clear (103) or override the veto (pin
survives its own content's erasure). HTD Test 4 A1 — the writer emitted zero
audit records. Ruling: learner pins = strength/importance, never permanent;
only trainer `fp_pin` is a true lock. A cost mechanism with no
strength-choosing policy and zero consumers is a loaded gun with no aim —
repair stays PARKED (T2-γ: renewal defeats expiry at zero cost; citation
forgery 8/8 structural).

## 2. test_pins.zag rewritten (the vacuous suite is gone)

The old suite was proven VACUOUS (T1-VACUITY): its "pinned" retest proposed
the already-adopted span, so the already-adopted pre-check fired before the
pin path — it stayed green under a neutered `fp_check` and certified
behavior it could not detect. Its header always described the learner-side
registry, never the B.6 force-pin.

The replacement is the HTD Test 3 §4 probe pattern
(`~/workspace/pins-rdtdt/t1-3/harness/t13_hardened.zag`, T2-α proven):
fresh DLB → `fp_pin(FP_CALLER_TRAINER)` on a span NEVER proposed before →
propose with good grounds → assert `verdict=3 reason=2` (R_R2) on exact AND
overlap spans, `verdict=1` on a clear span, `EV_PINRES(101)` present in the
tape (attribution channel). The test acts as trainer; HTD Sim B proved this
byte-identical to external pin installation.

Plus the P3 orphan-resolution PORTs (`forcepin/PINS_ORPHAN_RESOLUTIONS.md`,
handed to this suite's owner — deduplicated, built once):
- S4: trainer fp_pin on span B; trainer retract of B → refused 3/2, unit
  stays HS_ADOPTED(1); forcepin ledger gains op=34/rc=102 gate-refusal entry.
- S5: learner-issued fp_unpin → refused 101; fp_check stays 1.
- S6: trainer fp_unpin → rc=0; subsequent retract → 1/7, unit HS_KILLED(4).
- test4 Scenario B: fp_pin(trainer,id=7,[10,20)) audited as op=27 entry with
  d1=trainer/d2=7; blocked proposal 3/2 with op=34 gate-refusal; forged
  learner fp_pin attempt → refused 101 AND audited as the learner's action;
  fp_check stays 0 (pin NOT set).
- test5 dedup: fp contrast fp_pin(T) rc=0 / fp_gate_kill=102 on the pinned
  span; fp_unpin(TRAINER)→103 / fp_unpin(LEARNER)→101 on unpinned spans;
  fp_pin/fp_unpin round-trip on a disjoint span leaves the old Pins registry
  at pins_check=0 (write-dead, as designed).

## 3. Orphan dispositions executed (P3, evidence-decided)

- `tests/test_pins.zag` → REWRITE (this addendum's §2).
- `tests/test4_audit.zag` → RETIRED (Scenario A was the deleted writer; its
  load-bearing observation is preserved here: **A1 — `pins_add` wrote ZERO
  audit records**, the writer's indictment. Scenario B ported into §2).
- `tests/test5_compliance.zag` → RETIRED (writer arms Q1/Q2/Q3 moot; fp-path
  assertions ported into §2; stale Q3 label corrected in place before
  retirement — that 3/2 was the HS_KILLED dead-span pre-check, T2-β).
- `tests/test_selflock_probe.zag` → RETIRED (writer scenarios S2/S7/S7b moot;
  preserved observations: S3 trainer retract succeeds despite self-pin;
  S7b the genuine legacy-pin ELIMINATE veto, closed by this deprecation;
  S8 gate-event value corrected 202→302, T2-β).

The retired files are removed from the live suite (archived pre-deletion at
`~/workspace/pins-p1-work/retired_evidence/`); their retirement notes and
full disposition records live in `forcepin/PINS_ORPHAN_RESOLUTIONS.md`.

## 4. Doc corrections riding along

- `forcepin/forcepin.zag` header (and its `scratch/` twin): the
  "learner-writable (pins_add is called from learner-side code)" claim is
  now past tense with a dated Scope-S note.
- `FORCE_PIN_VERDICT.md` §7: dated execution note closing parked item 1.

## 5. Verification numbers (real tree, pure Zag, no RNG)

- **Suites PASS, byte-identical to pre-change baseline:** test_determinism,
  test_driver, test_retract, test_tripwire, forcepin/tests/test_forcepin —
  all rc=0, stdout shas identical to baseline (recorded pre-change
  `~/workspace/pins-p1-work/baseline_logs.sha`).
- **Rewritten test_pins: PINS PASS**, rc=0, N=5 runs byte-identical
  (sha `6d163988f81abc61713e43f517c00750f5a29428322ca294efb10c922746e26f`);
  MALLOC_PERTURB_ 0/165/17 → same sha.
- **Mutation bar (vacuity closed):** scratch tree with `fp_check` → `return 0`;
  suite FAILS rc=1 with 11 FAIL lines, zero panics, "PINS FAIL" — a dead pin
  path fails loudly instead of staying green.
- **dlb_digest sha-identical:** fixed zero-pin 4-proposal scenario, N=5 —
  all logs sha `3ca6295e291781f068f0853271f9244648d9fe6e44ab0dce6e80948ac4588d95`,
  the same sha T1-3/T2-α measured on baseline.
- **B.4 replay:** 964-byte tape recorded on the pre-change tree
  (sha `051306ec21c655d4edee86ce20df24d3b40b27c90086e4d4991406e9b3aaae45`)
  replays bit-for-bit on the Scope-S tree (964/964).
- **Compiler fence (proven):** temporary bogus caller reintroduced →
  `znc: error in main (line 4): native: call to unknown function 'pins_add'`
  (verbatim the RDTDT prediction); probe removed afterwards.
- **Static audit:** zero `fn pins_add` definitions and zero live-code
  `pins_add(` call sites in any buildable `.zag`. `static_audit.sh`: Claim A
  ok, Claim C ok; Claim B FAILs for the pre-existing parked reason
  (over-broad grep counts harness-actor `fp_pin(`/`fp_unpin(` calls in
  `tests/` — failed identically on the pristine tree; owner decision, brief
  §9.5, unchanged by this change).

**On "no remaining pins_add references anywhere":** buildable code and live
docs carry zero functional references. The token survives in (a) deletion-note
comments at the removal sites (deliberate — the fence's documentation),
(b) historical evidence briefs (`PINS_DECISION_BRIEF.md`,
`PINS_RDTDT_BRIEF.md`, `PINS_ORPHAN_RESOLUTIONS.md`, this addendum) — the
decision record must keep naming what was removed, or history is falsified.

## 6. Working papers

- `~/workspace/pins-rdtdt/` — RDTDT debate/test records (t1-1/t1-2/t1-3,
  t2a/t2b/t2c + logs); `~/workspace/pins-htd/` — HTD evidence (Tests 1–5).
- This crew's run evidence: `~/workspace/pins-p1-work/` (baseline shas,
  logs, tape, fence proof, static-audit log, retired-file archive).
