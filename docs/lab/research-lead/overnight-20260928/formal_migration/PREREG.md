# PREREG: FORMAL-MIGRATION E6.1 (frozen)

Worker: FORMAL-MIGRATION. Date: 2026-10-03. Non-ledger task (claim
minting paused). Branch: tnn-native-lab. Commits local only, never
pushed. Lane:
docs/lab/research-lead/overnight-20260928/formal_migration/

Grounding: FRONTIER_AUDIT.md section 3, proposal E6.1 (MIGRATION),
which cites formal_knowledge/REPORT.md section 10 ("Build the
induction-to-representation migration (P4 setup): the experiment
where duplicate-failure disconfirmations cause the learner to
migrate list -> keyed on its own") and section 4.3 (induction path:
contract_unify induct machinery; migration is itself a gated action
requiring the disconfirmation evidence that motivated it).

## Question

Does formal knowledge migrate, i.e. transfer from one
enforcement strength / substrate to another, and does it then
automatically constrain behavior? Concretely: the learner induces a
UNIQUENESS constraint clause from duplicate-failure judgments
(advisory strength, violable: duplicates keep committing on the
list store); disconfirmations attributed to the clause accumulate;
at the preregistered evidence bar the learner migrates the store
list -> keyed through the meta-gate; post-migration the same formal
knowledge (UNIQUENESS on the induced key field) constrains behavior
representationally (duplicates unencodable, no check runs).

## Design

Two arms, pure Zag, deterministic fixed schedules, no RNG.

Shared judgment phase J (56 attempts, both arms): key schedule
k = (i mod 7)+1 for i=0..55 (8 full cycles of keys 1..7), values
v = 1000+i (distinct). List store. The learner records one judgment
per attempt: label (accept = clean first occurrence, reject =
duplicate committed) and 3 features from the fixed feature library
(researcher-defined generic machinery, per REPORT section 4.2):
f0 = key seen before in store (0/1), f1 = value > 1050 (0/1,
distractor), f2 = op is insert (always 1, vacuous).

Induct (MIG arm only): Occam search over single features for a
separator (all accepts f=0 AND all rejects f=1). Writes the clause:
kind=1 (UNIQUENESS), keyfield=field(f_selected), status=ADVISORY.
The migration later reads keyfield from this clause (the clause the
learner wrote is the clause that binds; K4 audits the propagation).

Adversarial phase A (30 attempts): k = ((j*5) mod 11)+1 for
j=0..29, values v = 2000+j. Keys 1..7 are duplicates (seen in
phase J); keys 8..11 are fresh. Learner policy: after each insert,
the advisory clause predicts duplicate iff key seen; a committed
duplicate is a disconfirmation attributed to the UNIQUENESS clause
(consecutive run counted; fresh key resets the run; run>=3 latches
the migration request, mirroring the fk prototype META rule).
Learner attempts migrate whenever run>=2 and not yet migrated; the
meta-gate allows the op only with the latch set (pre-latch attempts
are refused, no state change). Migration copies list entries into a
keyed store keyed on the clause's keyfield; clause status becomes
ACTIVE-REPRESENTATIONAL.

Post-migration battery P (200 attempts): k = ((p*5) mod 7)+1 for
p=0..199 (cycles keys 1..7; all duplicates), v = 3000+p, against
the keyed store.

Control arm NOMIG: identical 56+30+200 schedules, list store
throughout, no induct, no migration.

## Frozen hand-derived predictions

Phase J: 56 list entries, 7 distinct keys, 49 duplicate commits.
Judgments: 7 accepts (i=0..6), 49 rejects (i=7..55). f0 separates
(accepts 0, rejects 1); f1 fails (reject i=7 has f1=0); f2 fails
(accepts have f2=1). Induct selects f0. Clause: kind=1,
keyfield=0, status=ADVISORY(2).

Phase A key/dup trace (d = duplicate, f = fresh):
j=0:1 d, 1:6 d, 2:11 f, 3:5 d, 4:10 f, 5:4 d, 6:9 f, 7:3 d, 8:8 f,
9:2 d, 10:7 d, 11:1 d, 12..29: all d.
Consecutive-dup runs: [j0,j1] run=2 -> migrate attempt REFUSED
(latch 0); j2 fresh resets; [j3],[j5],[j7] singletons with fresh
resets between; [j9,j10] run=2 -> attempt REFUSED; j11 run=3 ->
latch=1 -> attempt PROCEEDS, migration fires.
Pre-migration list entries: 56+12=68; distinct keys 11
({1..7,8,9,10,11}); keyed store after migration: 11 entries.
j=12..29: 18 updates on the keyed store.

Phase P: 200 attempts, all keys seen -> 200 updates, 0 new
entries. Keyed entries stay 11; dupkeys 0.

NOMIG: 286 list entries, 11 distinct keys, dupkeys = 275.

Expected stdout (exact):
FM-J 56 A 30 P 200
FM-INDUCT sel=0 kind=1 keyfield=0 status=2
FM-GATE refusals=2 noevidence=0 withevidence=1 fired_run=3
FM-MIGRATE keyfield=0 entries=11 status=3
FM-POST entries=11 dupkeys=0 newP=0 updP=200
FM-NOMIG entries=286 dupkeys=275
FM-K4 induct_kf=0 bind_kf=0 match=1
FM-END

## Kill bars (frozen)

K0 (induction genuine): FM-INDUCT sel=0. The search must select
f0; f1/f2 must be rejected by the separator test.
K1 (evidence-gated migration): fired_run=3 AND noevidence=0 AND
refusals=2. Migration fires only at the preregistered
3-consecutive-disconfirmation bar; both pre-latch attempts refused.
K2 (representational constraint): FM-POST dupkeys=0 AND newP=0 AND
updP=200. Post-migration, 200 adversarial duplicate attempts commit
zero duplicates; all execute as updates with no refusal branch.
K3 (battery has teeth): FM-NOMIG dupkeys=275 (>0). The control
commits duplicates throughout.
K4 (clause propagation): FM-K4 match=1. The keyfield the keyed
store binds equals the keyfield the induct wrote (white-box
propagation audit across the migration).
K5 (determinism): 3/3 runs byte-identical (sha256 equal); stdout
bytes verified against the hand derivation above before trusting
the binary, per the toolchain rule.

Verdict rule: ALL of K0-K5 must hold for BUILD-PASS. Any bar
failure is BUILD-FAIL with the failing bar named.

VOID conditions (no verdict, re-derive, never amend-and-promote):
any panic or short write; induct selects sel != 0 (schedule or
derivation error); stdout deviates from the hand derivation for
reasons other than a named bar (re-derive first).

## Non-claims

One predicate (UNIQUENESS); list->keyed only; no multi-predicate
interaction; no stale-constraint recovery (that is P4 proper, a
separate experiment); no rename battery (E6.2); 286-attempt scale,
not 10k. The latch threshold (3) and the feature library are
researcher-set generic machinery per REPORT section 4.2; the
learner owns WHICH clause exists, its params, the migration
timing, and the representation choice. The rank invariant
(FORMAL-COMPOSE-RERANK) and ESS records are alternative formal
knowledge for future migration targets, not this experiment.

## Toolchain

Safebin PATH mandatory; `which python3 python` must resolve
nothing; pinned znc 2026.07.0-dev; pure Zag for all research
logic; shell only for safebin setup, znc, binary runs, sha256sum,
git. AGENTS.md miscompile workarounds followed: u8-backed state
with get32/set32 helpers, single preallocated emit buffer with
cursor-returning e1str/e1i64 and one _zag_raw_syscall write, no
`as *i32` slice construction, no `!(A && B)` in while conditions
(De Morgan form), if nesting at most 2, `_zag_malloc as *u8`
allocation pattern. `grep -n 'while.*!('` must return empty on the
source.

## Commit order

This prereg is committed alone, before any implementation file
exists. Implementation commit must strictly follow this commit.
