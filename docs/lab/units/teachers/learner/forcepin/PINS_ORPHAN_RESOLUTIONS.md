# PINS — ORPHAN DISPOSITIONS & STALE LABELS: EVIDENCE RESOLUTIONS

**Crew:** P3 (marathon) · **Date:** 2026-09-21 ·
**Authority:** RDTDT brief `PINS_RDTDT_BRIEF.md` §§5–9 + Micah's 2026-09-21 standing
instruction ("tests determine outcomes, not preferences; anything the evidence +
preregistered bars decide gets DECIDED and DOCUMENTED, not escalated").
**Status:** All 6 items DECIDED by evidence. 3 applied to the live tree; 1 handed to
crew P1 (Scope-S deletion + `test_pins` rewrite) per the no-duplication rule; 2 PORT
specs handed to the hardened-FP-suite owner (also P1).
**Tree state at writing:** Scope-S deletion NOT yet applied — `pins_add` still at
`units/teachers/learner/store.zag:149`. Verified 2026-09-21 by grep (11 call sites:
1 definition + 10 in the 4 orphans, incl. `forcepin/scratch/store.zag:149` dead copy).
Crew P1 is executing the deletion; the dispositions below are decision records, valid
before and after it lands.

## Orphan 1 — `tests/test_pins.zag` → REWRITE (decided; execution = crew P1)

- **What it was:** the single live-tree caller of `pins_add` (line :30); frozen-verified
  as the "force-pin blocking test".
- **Evidence:** T2-α proved it cannot compile post Scope-S (`call to unknown function
  'pins_add'`) — its question ("does the learner-side pin block proposals?") no longer
  exists. T1-VACUITY proved it was vacuous: the suite stayed green under a neutered
  `fp_check`, i.e. it certified behavior it could not detect. Brief §2-S4: its
  "force-pin" header always described the *learner-side* registry, never B.6
  (`FORCE_PIN_VERDICT.md:17`).
- **Done:** disposition recorded here as decided-by-evidence. NOT touched by P3 — crew
  P1 is executing the Scope-S deletion + `test_pins` rewrite (probe pattern). The
  hardened replacement is drafted and evidence-complete:
  `~/workspace/pins-rdtdt/t1-3/harness/t13_hardened.zag` (T2-α: N=5 PASS on the real
  Scope-S tree, sha `2a6f8423…`; mutation `fp_check`→0 → FAIL rc=1, N=3,
  sha `093c4a8f…` — the vacuity is closed).

## Orphan 2 — `tests/test_selflock_probe.zag` → RETIRE-WITH-NOTE (applied)

- **What it was:** HTD Test Crew 2 self-lock probe; 3 `pins_add` call sites (:57/:145/:170).
- **Evidence:** writer-scenarios S2/S7/S7b are moot post Scope-S (T2-α compile-fail
  proven). What they proved is preserved in the file's retirement note and in the
  brief's corrected record: S3 — trainer retract of a self-pinned span SUCCEEDS
  (v=1/r=7, HS_KILLED; erase path consults only the FPStore; violation case S7);
  S7b — the GENUINE legacy-pin ELIMINATE veto (fresh span C[4,7), v=3/r=2, raw
  EV_PINRES=1, fp ledger delta=0; T2-β: CONFIRMED, closed by the deprecation);
  S8 — zero legacy-sourced EV_PINRES(1/2) events post-fix.
- **Done:** retirement note prepended to the live file; S8 stale label corrected
  (302, not 202 — see Stale label B). File still compiles on the current tree
  (verified 2026-09-21); runs byte-identical ×2 after edit (sha `d8223485…`).

## Orphan 3 — `tests/test4_audit.zag` → RETIRE-WITH-NOTE (applied)

- **What it was:** HTD Test Crew 4 audit-trail comparison; 1 `pins_add` call site (:52).
- **Evidence:** Scenario A exercised the deprecated writer (T2-α compile-fail proven).
  Its load-bearing observation is preserved in the file's retirement note, not in
  code: **A1 — `pins_add` wrote ZERO audit records** (learner-ledger delta = 0),
  the writer's indictment (S6 confirmed) and part of why deletion beat quarantine.
- **Done:** retirement note prepended to the live file; file still compiles on the
  current tree (verified 2026-09-21). Scenario B (the keeper — fp_pin trainer op=27
  entry; B2 blocked proposal v=3/r=2 with op=34 gate-refusal; B3 forged learner
  attempt refused 101 AND audited, fp_check stays 0) is a PORT, see below.

## Orphan 4 — `tests/test5_compliance.zag` → RETIRE-WITH-NOTE + PORT + label fix (applied)

- **What it was:** HTD Test Crew 5 ruling-compliance probe; 5 `pins_add` call sites
  (:45/:82/:99/:107/:133).
- **Evidence:** writer arms Q1/Q2/Q3 are moot post Scope-S (T2-α compile-fail proven).
  The "or PORT" alternative resolves to a single deduplicated port: test5's fp-path
  assertions (Q1 contrast fp_pin(T)/fp_gate_kill=102; Q2 fp_unpin on old pins
  →103/101; Q3 fp-disjoint round-trip) overlap the selflock S4/S5/S6 port — one port
  spec, not two. Preserved violation evidence: Q1 CONFIRMED (retract bit-identical
  pinned vs unpinned); Q2 CONFIRMED (monotone registry, zero removal symbols,
  fp_unpin→103/101); Q3a CONFIRMED (pin survives erasure); Q3b RETRACTED.
- **Done:** retirement note prepended; stale Q3 print corrected in place (see Stale
  label A). File still compiles on the current tree (verified 2026-09-21); runs
  byte-identical ×2 after edit (sha `86580d4a…`), corrected label in output.

## Stale label A — `test5_compliance.zag` Q3 print (corrected)

- **Was:** `" (3/2 = pin veto, un-overridable)\n"` — taught that re-proposal's 3/2 was
  the pin vetoing the trainer.
- **Evidence (T2-β):** the 3/2 came from the HS_KILLED dead-span pre-check
  (`delib.zag:653`, zero steps — fires for every re-proposed killed span, pinned or
  not). The pin was armed but never consulted; no trainer override of an actual pin
  veto was exercised. The genuine pin veto was always S7b. Quoted correction in
  T2-β §"Corrected Q3 label".
- **Done:** print now reads `" (3/2 = dead-span pre-check, NOT a pin veto;
  T2-beta corrected)\n"`, with a dated correction comment citing the pre-check
  line. The "span stays un-proposable forever" print is not carried forward (old
  registry deleted; force-pins stay trainer-gated and audited) — covered by the
  retirement note.

## Stale label B — `test_selflock_probe.zag` S8 gate-event value (corrected)

- **Was:** comment "a gate refusal adds 202" and the check `val == 202`.
- **Evidence:** T2-β event map: raw 1/2 = old-pin veto (delib.zag:709); 101/102 =
  fp veto (:711); 100 = no-fp baseline (unconditional); **302 = fp gate refusal**
  (`FP_REFUSED_PINNED(102)+200`). Live tree confirms: `delib.zag:713` emits
  `ev(EV_PINRES, fgrc + 200)`; fgrc=102 → 302. The 202 literal could never fire.
- **Done:** comment and check literal corrected to 302 with a dated correction note.
  S8 still passes (old-pins event seen=1, fp event seen=0 — no fp pins in scenario).

## FP-PORT SPEC (handoff — hardened-FP-suite owner, crew P1)

Verified 2026-09-21: `~/workspace/pins-rdtdt/t1-3/harness/t13_hardened.zag`
(80 lines) contains NONE of the following (no fp_unpin / op=34 / retract
assertions). They must be added to the hardened suite as the retirements land:

1. **From selflock S4:** trainer fp_pin on span B; trainer retract of B → refused
   v=3/r=2, unit stays HS_ADOPTED; forcepin ledger gains an op=34 gate-refusal
   entry with rc=102.
2. **From selflock S5:** learner-issued fp_unpin → refused 101; fp_check stays 1.
3. **From selflock S6:** trainer fp_unpin → rc=0; subsequent retract → v=1/r=7.
4. **From test4 Scenario B:** fp_pin(trainer, id=7, [10,20)) audited as
   forcepin-audit op=27 entry; blocked proposal v=3/r=2 with op=34 gate-refusal;
   forged learner fp_pin attempt → refused 101 AND audited, fp_check([10,20))=0.
5. **From test5 (deduped with 1–3):** fp contrast — fp_pin(T) rc=0,
   fp_gate_kill=102 on an fp-pinned span; fp_unpin(TRAINER)→103 and
   fp_unpin(LEARNER)→101 against old pins (post Scope-S: the old registry is
   gone, so these assert against a zero-pin registry — 103/101 must hold);
   fp_pin/fp_unpin round-trip on the disjoint fp registry leaves pins_check=0.

Build these once; do not duplicate. The hardened suite's acceptance bar already
proven: PASS on Scope-S tree (N=5, sha `2a6f8423…`); FAIL under `fp_check`→0
mutation (rc=1, N=3, sha `093c4a8f…`).

## Working papers (evidence)

- `~/workspace/pins-rdtdt/t2a_results.md` — T2-4 orphan compile-fail proofs,
  hardened suite + mutation results, retire-with-note drafts (applied here).
- `~/workspace/pins-rdtdt/t2b_results.md` — 7-claim misattribution audit (Q3b
  MISATTRIBUTED, Q1/Q2/Q3a/D1/D2 CONFIRMED), event map (1/2, 100, 101/102, 302),
  corrected Q3 label text.
- `~/workspace/pins-htd/` — original HTD evidence (Tests 1–5).
- Live tree lines grounded 2026-09-21: dead-span pre-check `delib.zag:653`;
  EV_PINRES gate emission `delib.zag:713`; writer `store.zag:149-157`.

## Kill-bar note (from the frozen RDTDT brief, unchanged)

Repair-into-strength stays PARKED (T2-γ: zero consumers, renewal defeats expiry at
zero cost, citation forgery 8/8 structural). Re-activation conditions: a consumer
appears, the strength trial's verdict sheet explicitly requests the mechanism, or
citation forgery gets a preregistered defense design.
