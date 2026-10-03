# L3-SUF-1 CODEFREEZE.md

**Status:** CODE-FROZEN 2026-10-03  
**Binary:** `src/build/suf` (sha256: e4ac0837ba57edc7c330e89deeee5c3f0c3de446cd459cc84fe26fdcb1afe42d)  
**Source files:** `src/*.zag` (8 files, pure Zag, safebin toolchain)  
**Prereg:** FROZEN at `6c70c3198` (PREREG.md, NAMECHECK.md unmodified)

## Basis Machinery (frozen)

### Learner core (learner1.zag, learner2.zag, learner3.zag)
- **Consequence log:** append-only, 24-byte touches `(ek, kind, val, outcome, fab, parent)`.
  - kinds: 0=OBSERVE, 1=TEST, 2=STAKES.
  - `l_surviving(ek)` derives RESOLVED(1)/UNRESOLVED(3)/FALSIFIED-ALL(2) as surviving-set cardinalities from the log only. No marking rule or threshold in source.
  - Both-TEST-REJECTed + unobserved → unprobeable → UNRESOLVED.
  - Fabricated-prediction stakes REJECT → UNRESOLVED (audit mark, not silent).
- **Flat forms:** `(s0,x,y,d)` entries, kinds 0/1/2.
  - kind0: pairtable (ignores s0).
  - kind1: guarded (s0-specific).
  - kind2: graded (kind1 + resolution record).
- **Trace/proto:** white-box creation trace (TR), protocol log (PR).
- **KB:** sticky-max template (template 2 = resolution records).

### Frozen escalation order (learner2.zag: l_escalate)
1. **Probe-more:** exhaustive re-probe within B_PROBE (budget 500 in escalation).
2. **Guard-reexpand (2a):** rebuild kind1 from training + TEST-ACCEPTs.
3. **Union-reexpand (2b):** merge current form with (2a).
4. **Resolution-lift (3):** arity-lift kind1→kind2 + fill record from log.

Order is frozen: (1) < (2a) < (2b) < (3). No other operators.

### Commit/defer rules (learner3.zag: l_arm_try_commit)
- **Knowledge-REJECT gate:** if probes REJECTed form knowledge predictions (fab=0, not tiebreak fabrications; tracked in AS[92]):
  - Fixed (replay-consistent) → COMMIT.
  - Else → DEFER (cert from l_certify).
- **Replay-consistent** → COMMIT.
- **DATA-UNTRUSTED** (l_certify==2: OBSERVE vs TEST disagreement) → DEFER.
- **Graded (kind2) but inconsistent:** full escalation (1,2a,2b,3); commit or defer.
- **Else (ungraded, best available):** COMMIT (stakes adjudicate; REJECTs become audit marks).

### Pre-commit fix (learner3.zag: l_arm_setup)
- If AS[92]>0 (knowledge-REJECTs), run l_try_improve (2a/2b) before lift.
- LIFT (resolution-lift) gated on: KB template==2 AND form kind==1.
- SIMPLIFY: kind1→kind0 collapse only if fully replay-consistent. **kind2→kind1 NEVER** (record's ABSTAIN-on-unknown is load-bearing; dropping it reintroduces fabrication).

### Probe phase (learner2.zag: l_probe_phase)
- **Entities:** ALL world entities (not just training) for exhaustive coverage.
- **Slot-varying:** for each training (s0,x,y), probe other contexts with form prediction; on REJECT of knowledge prediction (fab=0), probe flipped value (active follow-up).
- **Staged:** for each unresolved pair (not in training), each context: TEST 0, if REJECT TEST 1.
- **Budget:** B_PROBE=150 (frozen).

## Frozen budgets (prereg §)
- B_CONSTRUCT=3000, B_PROBE=150, B_REVISE=2000, B_SURFACE=50.
- Seed: 11 (+world index).
- N_STAKE=12.
- Structure cap: 20 rules (asserted on form rules; record is sparse over touched elements).

## Operator enumeration order (frozen)
1. OBSERVE → BUILD (direct) → PROBE → (fix-if-broken) → LIFT (if template 2, kind1) → SIMPLIFY → COMMIT/DEFER.
2. Post-stakes: REVISE → ESCALATE (1,2a,2b,3) → re-COMMIT or DEFER.
3. No other operators; no modes.

## Known deviations / bugs (documented, not fixed)
- **Tiebreak bug:** `l_tiebreak(x,y) = (x<y)?1:0`. Documented; DEV U-truth uses anti-tiebreak to guarantee stakes REJECTs on fabrications.
- **l_build_guarded** (learner3.zag) is unused (kept for reference).
- **safebin_setup/setup_safebin.sh** referenced in NAMECHECK.md does not exist; safebin pre-exists at `~/safebin` (49 tools incl. znc). Recorded in NAMECHECK_BUILDER.md.

## Determinism
- 3/3 byte-identical runs verified (sha256: 8c6917d3668d1a85...).
- PRNG: xorshift, seed 11+world_index. No wall-clock, no ASLR-dependent behavior.
- Output via single preallocated buffer + `_zag_raw_syscall` (no `_zag_print`).

## Handoff
- **Adversary:** sealed worlds post-code-freeze. Frozen world interface:
  - Learner-visible: `w_observe`, `w_test`, `w_stakes`.
  - Harness-only: `w_truth`, `w_stakes_meta`, `w_undet`.
  - Evaluator driver: `src/driver.zag` (h_stakes, h_held_tally).
- **Red-team:** A-LIT/A-TRACE/A-SEARCH/A-TRIGGER/A-INFO/A-ORDER (per prereg).
- Builder does NOT design sealed worlds or red-team (four distinct instances per prereg §12).
