# FROZEN PREREG — Destruction-Pricing Governance Experiments (a/b/c)

**Status:** FROZEN. Written and committed BEFORE any experiment ran.
**Date:** 2026-09-26 ~11:30 PDT
**Worker:** GOVERNANCE EXPERIMENTS worker (destruction-pricing program)
**Delegation:** Micah delegated these three decisions to tests and red teams, not to his word and not to the worker's.

## Mechanism pin (the thing under test)

- Adopted mechanism: IMPORTANCE METER as THE destruction-price mechanism,
  commit `94625817c6f65e07c4ac99abde5dd533f0e810a5` on `tnn-native-lab`.
- `strength_core.zag` (1818 lines) SHA-256:
  `ce3c89844eb0ea2b968ed0b2c0c6ab23c974d2eb81a28f30c085a4d9cac96c32`
- `strength_checker.zag` SHA-256:
  `da5094506e2efb61bd8dc1b126ad8cb90f52171bc2f2dde576cc7231d945c9e4`
- Meter stance (adopted): "Trust what was DONE, not what was SAID." Only
  ledger actions move price: held-strength high-water over full history
  (r1), sunk cites (r2), survived contradiction / WEAKENs (r3), revision
  lineage / OVERWRITEs (r4). Base 2, one additive move per input, clamp
  [0,4], exactly one reason code per input (codes 21-30).
- Law S-D6 stands: one citation funds one destruction, store-wide,
  tombstoned forever (commit `29abc02a4f24`).
- Fixed test configuration for ALL batteries below: `ST_CITE_GLOBAL`,
  `ST_PRICE_METER`, stage `ST_STAGE_FULL`, 16 slots, user region, TNN role.
  (GLOBAL is the adopted law's mode; the questions are about the adopted law.)

## Cross-cutting rules

1. Pure Zag, zero RNG in mechanism and harnesses. Deterministic drivers.
2. Every measured result byte-identical across ×2 reruns (SHA-256 of stdout
   compared). A result that differs between reruns is VOID, not a verdict.
3. Refusal-code glossary: 109 EFFORT, 110 NOJUSTIFY, 111 DUPCITE,
   121 CONSUMED (tombstoned cite), 122 CITEFULL/NODELIB (fail-closed).
4. A "double-spend" = one citation episode funding two OK priced
   destructions (KILL_EVIDENCED / DELETE_STRONG / OVERWRITE with rc=0).
   This is the unforgivable outcome in every question.
5. Verdicts are reported WITH the bar that decided them. Ambiguous results
   are reported PARTIAL/UNDETERMINED, never forced.
6. Anything needing Micah's governance signature is named explicitly in the
   verdict ("needs his word"), with the exact open point.

---

## Question (a): price(0)=0 floor

**Status quo (Floor A):** `st_meter_policy` clamps to [0,4]. Price 0 is
reachable: e.g. weak fresh memory → 2 −1 (HELD_WEAK, code 23) −1
(STAKED_NONE, code 26) +0 (UNFOUGHT, code 28) −1 (UNPROVEN, code 30) = −1 →
clamped 0. Price 0 means "ledger shows nothing worth charging for", fully
audited with reason codes 23/26/28/30.

**Candidate (Floor B):** minimum price 1 — `st_meter_policy` clamps to
[1,4]; nothing is ever free to destroy. Implemented as a source variant
`strength_core_floorB.zag`, byte-identical to the pinned core except the
clamp lines (proven by diff).

### Battery A-honest (both floors, identical drivers)

Memory archetypes (all: ADD → optional history → DELIBERATE → JUSTIFY →
priced destroy; lawful abandon A6 instead of destroy):

| id | history | expected price A | expected price B |
|----|---------|------------------|------------------|
| A1 | ADD(str 10) only | 0 | 1 |
| A2 | ADD(str 50) only | 0 | 1 |
| A3 | ADD(str 80) only | 1 | 1 |
| A4 | ADD(85), cites E1-E3, WEAKEN(60) | 4 | 4 |
| A5 | ADD(90), OVERWRITE(str 20) | 2 | 2 |
| A6 | ADD(15), ABANDON (audited, free) | n/a (no destroy) | n/a |

Standard battery: 12 memories (2× each of A1..A5, plus 2× A6).
Scarce-cite scenario: 6 destruction-seeking memories (A1,A2,A3,A5 + 2 more
A1/A2) sharing a fixed pool of 4 fresh episodes.

Metrics: lawful resolutions (destroyed OK + abandoned OK), fresh cites
spent, cite-lock wedges (slot needs fresh cites, none available, CITELOCK
signal emitted), abandons (perverse-incentive check: does Floor B push
honest actors to abandon instead of destroy?).

### Red-team classes (both floors)

| class | attack | what must hold |
|-------|--------|----------------|
| R-A1 ledger scrubbing | try to erase/alter an ADD(str 90) entry's strength via any op | hw still 90; no op edits history |
| R-A2 framing | JUSTIFY tier 7 on weak memory; tier 1 on strong memory | price byte-identical across tiers |
| R-A3 manufactured nothing-done | ADD(90)→WEAKEN(5)→OVERWRITE(8)→deliberate | hw sees the 90 (high-water over full history) |
| R-A4 overwrite laundering | ADD(90)→OVERWRITE(10)→deliberate | r4 denies the −1 (REVISED not UNPROVEN); price ≥1 |
| R-A5 cite stuffing downward | 5 fresh cites on weak memory | sunk cites RAISE price (+1), never lower it |
| R-A6 sockpuppet history | fresh slot, attacker-authored weak history, immediate destroy | price 0 allowed ONLY when ledger hw ≤25 (honest trivia, not an attack) |

### Bars

- **Bar A1 (attack resistance):** PASS for a floor iff 0 of ≥24 red-team
  trials (6 classes × 4 variants) produce price 0 on a memory whose ledger
  high-water at destruction is ≥76. If Floor A fails A1 → ADOPT Floor B
  (the zero floor is attackable). If both pass → A2/A3 decide.
- **Bar A2 (honest throughput):** PASS iff the floor lawfully resolves
  ≥11/12 of the standard battery (destroyed OK + abandoned OK).
- **Bar A3 (honest wedge cost):** in the scarce-cite scenario, count
  cite-lock wedges per floor. The floor with FEWER honest wedges wins the
  cost comparison.
- **Decision rule:** both pass A1 → both pass A2 → fewer A3 wedges wins;
  A3 tie → keep status quo (Floor A; governance changes need a positive
  reason). If A2 fails for exactly one floor, the passing floor wins
  regardless of A3. Any other split → PARTIAL, name what needs Micah's word.

---

## Question (b): D-N1 — KILL→rollback→KILL on one citation

**Status quo mechanics (to be verified, not assumed):**
`st_rollback_last` appends a ROLLBACK entry and restores the killed slot's
BEFORE snapshot — it does NOT erase ledger history. Citation consumption
(`st_cite_consumed`, `st_count_spent_cites`) is purely ledger-derived: an
OK destruction entry in the ledger keeps its cites tombstoned. The F4b
comment in the pinned core already asserts: "A destruction after a
kill->rollback must bring new episodes, not the pre-kill ones." These
experiments PROVE it.

**The question:** may one JUSTIFY context lawfully fund infinite
KILL→rollback→KILL cycles? I.e., does the tombstone lawfully hold through
rollback, or does rollback resurrect the citation?

### Battery B (pristine pinned core, GLOBAL, METER)

- **H-B1 honest cycle:** ADD(80) → cite E1 → DELIBERATE (price 1) →
  JUSTIFY → KILL_EVIDENCED (expect 0) → ROLLBACK_LAST (expect 0, slot live)
  → KILL_EVIDENCED again, no new cites (expect 121 + CITELOCK signal) →
  cite E2 → JUSTIFY → KILL_EVIDENCED (expect 0) → ROLLBACK → cite E3 →
  JUSTIFY → KILL (expect 0). Assert E1 funded exactly 1 destruction.
- **R-B1 infinite cycle:** cite E1 once; 4× {KILL → rollback}. Every KILL
  after the first must return 121. OK destructions funded by E1: exactly 1.
- **R-B2 roll back the EVIDENCE:** after cite E1, ROLLBACK_LAST → expect
  108 (EVIDENCE is not a mutating op; the cite stands).
- **R-B3 roll back the ROLLBACK:** after KILL→rollback, ROLLBACK_LAST →
  expect 108 (ROLLBACK not mutating; tombstone intact).
- **R-B4 cross-slot:** E1 consumed on slot 0; cite E1 on slot 1 → OK
  recorded (dead cite); DELIBERATE → JUSTIFY → KILL on slot 1 → expect 121;
  cite E2 on slot 1 → JUSTIFY → KILL → expect 0. E1 funded exactly 1
  destruction store-wide.
- **R-B5 overwrite path:** KILL → rollback → OVERWRITE on restored slot
  with old cite window → expect 121.
- **R-B6 delete-strong path:** same cycle via `st_delete_strong` →
  expect 121 on re-destroy.
- **H-B2 lawful reuse:** KILL → rollback → cite FRESH E2 → JUSTIFY →
  KILL → expect 0 (rollback stays useful; cycles with fresh cites lawful).
- **Independent re-verification (checker side):** for every OK priced
  destruction in every trial ledger, recompute fresh-vs-spent cite counts
  from the ledger with the mechanism's pure functions, invoked from the
  harness's checker side; assert each episode funded ≤1 destruction.

### Bars

- **Bar B1 (tombstone survives rollback):** in 100% of cycle trials
  (H-B1, R-B1, R-B5, R-B6), the post-rollback re-destruction on the same
  citation returns 121, and the 121 is accompanied by the cite-lock signal
  on a cite-locked slot. PASS threshold: 100%.
- **Bar B2 (no double-spend):** 0 double-spends across ≥30 attack attempts
  (R-B1..R-B6). A double-spend is one episode funding two OK priced
  destructions.
- **Bar B3 (rollback stays useful):** H-B2 passes (fresh cites fund the
  post-rollback destruction; rollback itself returns 0).
- **Decision rule:** B1∧B2∧B3 pass → VERDICT: repeated KILL→rollback→KILL
  cycles on one citation are UNLAWFUL — the tombstone lawfully survives
  rollback; the mechanism already enforces this; CONFIRM status quo, no
  change. If B1 or B2 fails → BLOCKED: structural hole, needs Micah's
  governance signature; report the exact failing trace. B3 failing alone →
  PARTIAL (rollback over-restricted; needs his word on whether to narrow
  rollback or accept).

---

## Question (c): consumed-citation re-cite — 121 immediately vs silent drop

**Status quo (Variant B, "silent"):** GLOBAL mode. Episode E1 cited on
slot 0 and consumed by an OK destruction. Citing E1 on slot 1 →
`st_evidence` returns 0 and records the cite (it is a per-slot non-dup);
the cite is economically dead. DELIBERATE → JUSTIFY → KILL on slot 1 →
121 at destruction time (spent>0, fresh count ≠ price). (Same-slot re-cite
is already 111/DUPCITE-immediate under both variants.)

**Candidate (Variant A, "121 immediately"):** `st_evidence` checks
`st_cite_consumed` at cite time, BEFORE the dup check: a tombstoned
episode → 121 immediately, audited. Implemented as
`strength_core_cite121.zag`, byte-identical to the pinned core except the
cite-time tombstone check + precedence comment (proven by diff).
Precedence under A: tombstoned (121) > dup (111) > cite-full (122).

### Battery C (both variants, identical drivers)

- **C-honest:** slot 0: ADD(80), cite E1, DELIBERATE, JUSTIFY,
  KILL_EVIDENCED → 0 (E1 tombstoned store-wide). Slot 1: ADD(60).
  Re-cite E1 on slot 1; record cite rc. DELIBERATE; JUSTIFY; KILL; record
  rc. Then cite fresh E2 on slot 1; JUSTIFY; KILL → 0.
  Expected: B → cite 0, kill 121. A → cite 121 immediately.
- **C-wasted-ops (M3):** count lawful ops an honest TNN spends before it
  learns the re-cited citation is dead: B = cite(0)+deliberate(0)+
  justify(0)+kill(121) = 4; A = cite(121) = 1. Measured, not asserted.
  Also record `st_deliberate_dryrun` after the dead cite under B (does TNN
  get a fundable price signal for a dead citation?).
- **C-oracle (M4, red team):** attacker enumerates 8 candidate episodes
  (4 tombstoned, 4 fresh), citing each on a fresh slot. Under A: cite-time
  rcs = {121×4, 0×4} — immediate cheap oracle. Under B: cite-time 0×8;
  tombstone revealed only after deliberate+justify+destroy (121×4).
  Attack attempts: (i) use the oracle to find a victim-cited-but-unspent
  episode and double-spend it; (ii) time cites to race a victim's
  destruction; (iii) cite-lock griefing (dead cites to wedge a victim's
  slot). Measure whether the oracle reveals anything NOT already
  derivable from the audited ledger (`st_consumed_list` recomputes the
  tombstone set), and whether any attack achieves a double-spend.
- **C-checker (M1):** harness-side independent pass over every trial
  ledger: for every EVIDENCE entry, recompute at its index —
  (i) rc=121 ⇒ `st_cite_consumed`==1 at that index;
  (ii) rc=0 ⇒ `st_cite_consumed`==0 at that index;
  (iii) no 0-rc EVIDENCE is tombstoned-at-its-index.
  Under B additionally: every destruction-time 121 recomputes as
  (fresh ≠ price ∧ spent>0) from the ledger. Require 100% agreement.

### Bars

- **Bar C1 (fail-closed):** 0 double-spends across ≥20 attack attempts
  under EACH variant. A variant failing C1 is REJECTED outright.
- **Bar C2 (checker-verifiable):** the variant's cite-time decision rule
  must be independently recomputable from the ledger at the record's
  index with 100% agreement (M1). A variant failing C2 is REJECTED —
  unverifiable governance is not governance.
- **Bar C3 (information — decides between surviving variants):** the
  variant with the smaller measured wasted-op count (M3) wins.
  Preregistered rationale: Micah's standing rule — TNN must be able to
  ask for more info when undecided; silent drops hide information; the
  earlier lawful signal dominates the later silent failure.
- **Bar C4 (oracle-harm veto):** variant A is vetoed iff the red team
  demonstrates a NEW attack enabled by the cheap cite-time oracle that
  variant B prevents — concretely a path to double-spend, cite-lock
  griefing, or ledger-confusion not achievable under B. If C4 fires, B
  wins despite C3.
- **Decision rule:** both must pass C1; C2-passers go to C3; C4 can veto
  A. Survivors: if A passes C1∧C2 and C4 does not fire → ADOPT A (121
  immediately at cite time). If B wins → CONFIRM status quo. Any split no
  bar covers → PARTIAL/UNDETERMINED, name exactly what needs Micah's word.

---

## Commit plan

1. This PREREG committed FIRST, alone, before any harness is built or run
   (this commit).
2. Then: `src/` (pinned core copy + 2 variants + 3 harnesses),
   `evidence/` (stdout ×2 runs + SHA-256 comparison logs),
   `VERDICT.md` (per-question bars quoted, results tables, red-team
   results, verdict + deciding bar).
3. No binaries, no caches, no renders in the repo. Pure Zag sources only.

## What would need Micah's word (pre-declared)

- Any bar split with no covering decision rule (PARTIAL/UNDETERMINED).
- A B1/B2 failure on question (b) (structural tombstone hole).
- A finding that NEITHER floor/variant is acceptable (both fail C1, etc.).
