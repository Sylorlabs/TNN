# REPORT: FORMAL-MIGRATION E6.1 (BUILD-PASS)

Worker: FORMAL-MIGRATION. Date: 2026-10-03. Non-ledger task (claim
minting paused). Branch: tnn-native-lab. Commits local only, never
pushed. Lane:
docs/lab/research-lead/overnight-20260928/formal_migration/

Grounding: FRONTIER-AUDIT.md section 3, proposal E6.1 (MIGRATION),
citing formal_knowledge/REPORT.md section 10 (the unbuilt
induction-to-representation migration, P4 setup) and section 4.3
(induction path via contract_unify induct; migration as a gated
action requiring the disconfirmation evidence that motivated it).

## Verdict: BUILD-PASS (K0-K5 all hold)

The migration experiment is now built and executed. Formal
knowledge migrated: a learner-induced UNIQUENESS clause moved from
advisory strength (violable; duplicates kept committing on the list
store) to representational strength (keyed store; duplicates
unencodable), and it automatically constrains behavior in the new
substrate with no check running per insert.

## What was built

fm_main.zag (pure Zag, safebin, pinned znc 2026.07.0-dev, zero
analyzer warnings). Two arms on fixed deterministic schedules:

MIG arm. Phase J (56 attempts, keys cycling 1..7): the learner
records accept/reject judgments with 3 features from the fixed
feature library (f0 = key seen before, f1 = value > 1050
distractor, f2 = vacuous op-is-insert). induct runs a genuine Occam
single-feature search and writes the clause kind=1 (UNIQUENESS),
keyfield=field(f0)=0, status=ADVISORY. Phase A (30 attempts,
k=(j*5 mod 11)+1; keys 1..7 duplicate, 8..11 fresh): the advisory
clause predicts duplicate-iff-key-seen; each committed duplicate is
a disconfirmation attributed to the UNIQUENESS clause (consecutive
run; fresh key resets; run>=3 latches the migration request). The
learner attempts migrate whenever run>=2; the meta-gate refuses
pre-latch attempts with no state change and allows the latched one.
Migration copies the 68-entry list into a keyed store keyed on the
clause's own keyfield, promoting the clause to
ACTIVE-REPRESENTATIONAL. Phase P (200 attempts, keys cycling 1..7,
all duplicates) runs against the keyed store.

NOMIG control: identical 286-attempt schedule, list store
throughout, no induct, no migration.

## Results (3/3 byte-identical, sha256
41bc06027be648daf87e5b00513b958e577afa6ace62c1d24993ff4fab1d8e2c,
stderr empty; bytes verified against the frozen hand derivation
before trusting the binary)

FM-J 56 A 30 P 200
FM-INDUCT sel=0 kind=1 keyfield=0 status=2
FM-GATE refusals=2 noevidence=0 withevidence=1 fired_run=3
FM-MIGRATE keyfield=0 entries=11 status=3
FM-POST entries=11 dupkeys=0 newP=0 updP=200
FM-NOMIG entries=286 dupkeys=275
FM-K4 induct_kf=0 bind_kf=0 match=1
FM-END

Kill bars:
- K0 (induction genuine): sel=0. The search selected f0; f1 failed
  (reject at i=7 has f1=0) and f2 failed (accepts have f2=1). PASS.
- K1 (evidence-gated migration): fired_run=3, noevidence=0,
  refusals=2. Both pre-latch attempts (run=2 at j=1 and j=10) were
  refused with zero state change; the migration fired only at the
  preregistered 3-consecutive-disconfirmation bar. PASS.
- K2 (representational constraint): post-migration dupkeys=0,
  newP=0, updP=200. All 200 adversarial duplicate attempts executed
  as updates; zero duplicates committed; the keyed insert has no
  refusal branch. PASS.
- K3 (battery has teeth): NOMIG dupkeys=275 > 0. PASS.
- K4 (clause propagation): induct_kf=0, bind_kf=0, match=1. The
  field the keyed store binds is the field the learner's induct
  wrote; migration reads keyfield from the induced clause rather
  than hardcoding it. PASS.
- K5 (determinism): 3/3 byte-identical. PASS.

No-wire audit: grep for domain vocabulary over fm_main.zag empty
(structural vocabulary only: key/store/insert/clause/migrate).

## Answer to the question

Does formal knowledge migrate? Yes, in the precise sense the
design specified: the UNIQUENESS constraint moved from the clause
registry (advisory record, consulted at discretion, violable) into
the store's representation (keyed addressing, inviolable), by the
learner's own evidence-driven action through the meta-gate. The
migration was not scheduled: it fired when the disconfirmation
evidence reached the bar, and the gate refused two earlier
attempts, proving the evidence requirement is load-bearing.

Does it constrain behavior in the new substrate? Yes,
automatically: post-migration, the adversary's 200 duplicate
attempts could not commit a duplicate, with no per-insert check
running. The constraint is in the addressing (insert IS
write-to-slot), not in a refusal branch. The control arm proves
the counterfactual: without migration the same battery commits
275 duplicates.

## Wiring map (per REPORT section 4.2)

Researcher/protected: feature library, latch threshold (3),
meta-gate skeleton, store ops. Learner-owned: WHICH clause exists
(induct selected f0 from data), its params (keyfield=0 from the
selected feature), migration timing (evidence-driven, j=11), the
representation choice (list -> keyed). The clause that binds is
the clause the learner wrote (K4).

## Honest boundaries

- One predicate (UNIQUENESS), one migration direction
  (list -> keyed), 286-attempt scale. No multi-predicate
  interaction, no stale-constraint recovery (P4 proper is a
  separate experiment), no rename battery (E6.2).
- Impossibility is channel-relative (REPORT section 4.1): within
  the committed keyed store, not metaphysical.
- The rank invariant (FORMAL-COMPOSE-RERANK) and ESS records are
  named in the task as alternative formal knowledge; this
  experiment used UNIQUENESS per E6.1's design. Porting migration
  to the rank invariant (e.g. advisory rank belief -> rank-ordered
  edge store) is the natural follow-up.
- One implementation-order fix was made after the first
  successful run: the FM-K4 line was emitted before FM-NOMIG;
  the emit was reordered (values unchanged) so stdout matches the
  frozen prereg block exactly. No kill bar, prediction, or logic
  was altered.

## Files

formal_migration/: PREREG.md (frozen, committed alone first as
6136c847a), NAMECHECK.md, fm_main.zag, fm_bin (pinned znc build),
fm_compile.txt (zero analyzer warnings), fm_run1/2/3.txt
(byte-identical), fm_run1/2/3.err (empty), REPORT.md (this file).
