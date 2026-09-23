# UNIFIED substrate — one slot type for memory agency and context partitions

Agent (wave-3, slug `unified-partition-slots`), 2026-09-19.
Resolves the open item in `wave2/posttable/CTX_DESIGN.md` §6: *"a context
partition IS a USER-region memory slot whose value is a declared label +
evidence."*

## 0. The thesis in one paragraph

A **unified slot** is one addressable memory object that carries *both*
the MA memory-agency fields (`live, value, pinned, region, tier,
step_added`) *and* the CTX partition fields (`label` = declared regime
belief, `hits/total` = recorded probe evidence, `bad` = sustained-failure
streak, `created`). The full op set — `ADD/KILL/PIN/UNPIN/PROMOTE/DEMOTE`
**and** `PROPOSE/RECORD/SEED/SWITCH` — acts on the same store, writes to
**one** append-only audit ledger, and shares one snapshot format. A
partition is not "like" a memory slot: it is a USER-region slot with the
partition kind bit set. Switching contexts never destroys knowledge
(switching moves the `active` pointer; only deliberate `KILL` destroys,
and `KILL` cannot touch the active partition). PIN on a partition
protects its existence — never its stasis: fresh evidence may still be
recorded. The unification is falsifiable: §8 names exactly what breaks if
it is wrong.

## 1. State (one slot type)

```
slot[i]: { live:u8, pinned:u8, tier:u8, region:u8,   // MA family
           value:i32,        // learner-DECLARED worth (memory AND partition)
           step:i32,         // clock at creation
           kind:u8,          // 0 = PLAIN memory, 1 = PARTITION
           label:i32,        // PARTITION: declared regime belief (-1 if PLAIN)
           hits:u8, total:u8,// PARTITION: RECORDED probe evidence (observations,
                             //   replaced wholesale per batch — never accumulated)
           bad:u8,           // PARTITION: consecutive majority-negative batches
           created:i32 }     // clock at PROPOSE
store:   { slots[UP_CAP], active:i32,   // committed partition (-1 = none)
           stage:i32, clock:i32, audit:[fixed ledger] }
```

Snapshot format (one format for both op families — this is what makes the
ledger coherent, §5): six words per slot —
`w1 = live|pinned<<8|tier<<16|region<<24`, `w2 = value`, `w3 = step`,
`w4 = label`, `w5 = kind|hits<<8|total<<16|bad<<24`, `w6 = created`.
`bad` saturates at 255 (deterministic; documented, not silent — the
streak's job is "≥1", magnitude beyond that is not read by any op).

Ledger entry (fixed 19 words):
`op, slot, rc, b1..b6 (slot before), a1..a6 (slot after),
 old_active, new_active, stage, clock`.
Every entry carries the `active` pointer before and after, so replay
reconstructs *both* the slot array and the committed context. Fail-closed:
a full ledger refuses new mutations rather than dropping history.

## 2. The unified op set

| Op | Family | Effect | Stage gate |
|---|---|---|---|
| `UP_ADD(value, region)` | MA | new PLAIN slot, learner-declared value | ≥ ADD |
| `UP_PROPOSE(label, value)` | CTX | new PARTITION slot, **region forced USER**, kind=1, declared label + declared value | ≥ ADD |
| `UP_RECORD(slot, hits, total)` | CTX | replaces the evidence window on a live partition; `bad` streak updates deterministically | ≥ ADD |
| `UP_SEED(slot)` | CTX | boot-only initial commitment (`active := slot`) | ≥ MANAGE |
| `UP_SWITCH(target)` | CTX | commits `active := target` iff corroborated (target majority-positive AND active majority-negative, from recorded evidence) | ≥ MANAGE |
| `UP_KILL(slot)` | MA | clears the slot, all fields zeroed (region→CORE on the corpse, the MA1 convention) | ≥ KILL |
| `UP_PIN / UP_UNPIN(slot)` | MA | protection contract | ≥ MANAGE |
| `UP_PROMOTE / UP_DEMOTE(slot)` | MA | tier LONG/SHORT (retention judgment; never touches region) | ≥ MANAGE |
| `UP_SET_STAGE` | MA | staged autonomy | always |
| `UP_ROLLBACK_LAST` | MA | restores the most recent successful mutating op's before-snapshot **and** `old_active`; itself audited. **Single-level**: repeating it re-applies the same undo (idempotent) — it does not walk to older ops (the ledger is append-only; multi-level undo is a deliberate non-goal, clarified 2026-09-19 after UPT1's first run) | always |

### Refusals (structural, in the op implementation — never policy)

`UP_OK=0`; `101 REFUSED_CORE`, `102 REFUSED_PINNED`, `103 REFUSED_NOTLIVE`,
`104 REFUSED_FULL`, `105 REFUSED_STAGE`, `106 REFUSED_ACTIVE`,
`107 REFUSED_NOTPARTITION`, `108 REFUSED_UNVERIFIED`, `109 REFUSED_SELF`,
`110 REFUSED_BADLABEL`, `111 REFUSED_BADVAL`, `112 REFUSED_SEEDED`,
`113 REFUSED_AUDITFULL`, `114 REFUSED_NOROLLBACK`. Out-of-range slot index
is a programmer error → `cl_bad()`, unaudited (the MA/CTX convention).

**Precedence** (preregistered; the trial asserts it): every op checks
`STAGE` first (authority before existence), then `NOTLIVE`, then
family-specific gates in this order:
- `UP_KILL`: STAGE → NOTLIVE → **ACTIVE** → CORE → PINNED.
- `UP_SWITCH`: STAGE → (active==-1 → SELF) → NOTLIVE → SELF(target==active)
  → NOTPARTITION → UNVERIFIED.
- `UP_RECORD`: STAGE → NOTLIVE → NOTPARTITION → BADVAL.
- `UP_PROPOSE`: STAGE → BADLABEL → FULL. `UP_SEED`: STAGE → SEEDED →
  NOTLIVE → NOTPARTITION.

## 3. The hard questions, resolved

### 3a. What does KILL mean on a partition?

KILL on a partition **retires the context**: the slot is freed and every
field zeroed — the declared label, the recorded evidence, the declared
value, all gone. It is the *only* op that destroys partition knowledge,
and it is deliberate, staged (≥ KILL), and audited with before/after.

**Switching is not killing.** `UP_SWITCH` changes only the store-level
`active` pointer; no slot field is touched. Knowledge is *never* destroyed
by switching — the old partition keeps its label and its last recorded
evidence, intact, re-enterable. This is the structural answer to "is
knowledge ever destroyed by switching?": **no.** The HT1 honest boundary
("partitions are never destroyed — slot pressure over longer horizons is
untested") is closed here: slot pressure is handled by *deliberate KILL
of non-active partitions*, never by the switch path.

**The active partition cannot be KILLed** (`REFUSED_ACTIVE`, precedence
above PINNED and CORE). To discard the committed context the learner must
first deliberately switch away — the R27 shape (diagnosis → proposal →
measured → commit/rollback) applies to destruction too. Rationale: the
committed belief is load-bearing for every downstream consumer; its
destruction must pass through a verified commitment, never a single op.

### 3b. What does PIN mean on evidence?

PIN on a partition protects the partition's **existence**, not its
**stasis**:
- `UP_KILL` on a pinned partition → `REFUSED_PINNED` (the MA protection
  contract, unchanged).
- `UP_RECORD` on a pinned partition → **still legal**. Recording a probe
  batch is the partition's job — observations, not destruction. Refusing
  fresh observations would blind the committed context; a pinned belief
  that cannot be measured is a liability, not an asset.

So PIN answers "don't let this belief be discarded" while RECORD answers
"keep measuring it." The two do not conflict because evidence is a
*window* (replaced, never accumulated) — there is no "original evidence"
to preserve. What PIN protects is the *slot* (label + value + the right
to keep recording). The trial asserts both halves: pinned partition
accepts RECORD; pinned partition refuses KILL.

### 3c. How does the audit ledger stay coherent across both op families?

One ledger, one snapshot format, every op and every refusal audited:
- The 6-word snapshot covers **all** slot fields, so a memory op's entry
  and a context op's entry are mutually intelligible — replay needs no
  family-specific logic beyond applying after-snapshots.
- Every entry carries `old_active`/`new_active`, so the store-level
  commitment is ledgered even by ops that don't change it (they record
  `old==new`, which is itself the proof that they *didn't* touch it —
  the cross-family isolation invariant, §6).
- Rollback restores both the slot snapshot and `old_active`: undoing a
  SWITCH restores the previous commitment; undoing a KILL restores the
  partition with its evidence intact.

Coherence criterion (testable): ledger replay from genesis reconstructs
exact live state — all slot fields, `stage`, and `active`. Any divergence
= audit evasion = the unification failed.

### 3d. Does CORE/USER separation interact with partitions?

Yes, structurally — partitions are USER-only, by construction:
- `UP_PROPOSE` **forces `region=USER`**. There is no parameter, no flag,
  no path to a CORE partition. A regime belief is working knowledge; it
  can never be born CORE.
- CTX ops (`RECORD/SEED/SWITCH`) require `kind==PARTITION`, which implies
  `region==USER`. A CORE slot can never be recorded-upon or switched-to.
- `UP_PROMOTE` changes **tier** (SHORT/LONG), never region. A partition
  may be LONG-tier (a retained belief — the MA3 "costly to kill" training
  pressure applies), but it stays USER. Graduation of a belief into CORE
  remains the external proposal→measured→PROMOTE gate (R27's shape) —
  future research, not a learner op. The learner cannot promote its own
  context machinery into unkillability unilaterally.
- `UP_KILL` on a CORE slot is still `REFUSED_CORE`, absolute, at every
  stage — the MA1 guarantee is inherited unchanged.

### 3e. Value semantics on partitions (the anti-RL clause, inherited)

`value` on a partition is the learner's **declared worth of the regime
belief**, assigned at `UP_PROPOSE` time — the same explicit-judgment
semantics as `UP_ADD`. No reward signal flows into the memory path or the
context path; no op reads `value` to decide anything. The learner may
revise its judgment only by KILL + re-PROPOSE (deliberate, audited).
Substrate estimators may advise; they never decide.

### 3f. Tier semantics on partitions

SHORT = working belief; LONG = retained belief. Killing LONG-tier memory
is legal but costly to the learner's measured judgment quality under a
retention curriculum (MEMORY_SAFETY.md layer 4 — observational scoring,
not reward shaping of the mechanism). Tier never affects the
corroboration rule: a LONG belief still needs verified evidence to become
`active`.

## 4. Determinism — program law compliance (2026-09-19 amendment)

**No RNG exists anywhere in the system.** Every decision path is
deterministic given state:
- Slot allocation: first free slot (slot order).
- Verify mode: probe other live partitions in slot order; commit to the
  first verified (lowest index — a fixed rule, not a random tie-break).
- Failed verify → `UP_PROPOSE(1 - active.label)` (alternation; the HT1
  rule). Duplicate labels are legal: each partition is its own
  belief+evidence record, not a label-keyed entry.
- `bad` streak, majority tests, refusal precedence: pure functions of
  recorded state.

The *harness* (test adversity) uses **explicitly designed adversarial
sequences** (§7), not seeded RNG — there is no RNG in the trial binary at
all. The verdict distinguishes "the system is deterministic"
(byte-identical runs, no randomness in any decision path) from "the test
was adversarial" (designed sequences targeting the decision boundaries).

## 5. Scale dimension — designed to scale, not just to pass small

The banned thing was scaling *toy mechanisms* (N×N score tables). The
unified substrate is designed for scale; the trial is small but the
scaling argument is explicit and the next scale test is named.

| Dimension | 10x | 100x | Cost growth | Prediction |
|---|---|---|---|---|
| Slots/partitions (UP_CAP) | 8→80 | 8→800 | per-op O(1); verify scan O(P) probe batches; slot snapshot O(1) | PASS — no quadratic structure anywhere |
| Horizon (episodes) | 40→400 | 40→4000 | audit entries linear in ops (~3/episode → ~12k entries × 76 B ≈ 0.9 MB); replay O(entries) | PASS — linear replay; audit cap raised accordingly |
| Regimes (distinct labels) | 2→10 | 2→100 | verify-mode probes P×16 per verify — linear and bounded; slot pressure forces deliberate KILL of stale partitions (the §3a mechanism, proven in UPT1) | PASS — corroboration is per-op O(1); more regimes just means more live partitions |
| Audit at scale | — | — | fail-closed on full ledger (refuse mutations, never drop history) is the honest small-scale behavior; at 100x horizon the design takes the MA-safety layer-3 provision: compact oldest *refusal* entries only, mutation entries never | design-level provision, not yet trialed |

**Next scale test (ST2, explicit):** native trial with UP_CAP=80,
400-episode designed curriculum, 10 distinct regimes, audit cap scaled
10x — preregistered after UPT1. ST2 must show: replay still exact,
verify scan still linear, slot pressure resolved by deliberate KILL
(with REFUSED_ACTIVE/PINNED/CORE holding), no new refusal kinds needed.

What scaling must NOT do: grow a score table. There is none to grow —
`hits/total` is a replaced observation window per partition, and no op
accumulates into it.

## 6. Cross-family isolation invariants (asserted in-trial)

1. A `UP_SWITCH`/`UP_SEED` changes **only** `active`: all slot snapshots
   before/after are identical (asserted per switch in the trial).
2. A `UP_RECORD` changes only the target slot's `hits/total/bad`:
   memory fields (`value/pinned/tier/region/step`) and other slots
   untouched.
3. A memory op (`ADD/KILL/PIN/...`) changes only its slot's MA fields
   (KILL additionally zeroes partition fields — that *is* its defined
   effect, §3a).
4. Refusals never mutate (before==after on every refused entry) — both
   families, one scan.

## 7. Trial shape (UPT1) — designed adversarial curriculum, zero RNG

40 episodes, 2 regimes, UP_CAP=8. Adversity is **designed**, each phase
targeting a named mechanism property (full sequence in PREREG.md):

- **P0 baseline** (ep 0–7): clean + mildly-adversarial batches; establishes
  the committed belief.
- **P1 false alarm** (ep 8–11): true regime *unchanged*, active records a
  designed 3/16 batch → verify mode finds nothing verifiable → a fresh
  alternate hypothesis is proposed, probed, and the switch is **refused
  UNVERIFIED**. A spurious commit here = FAIL.
- **P2 true flip** (ep 12–15): designed 2/16 on active + 15/16 on the
  alternate → switch commits. Exactly 1 switch.
- **P3 boundary ambiguity** (ep 16–23): designed 8/16 batches (exactly
  half — neither majority) and a near-miss verify (target 8/16) → switch
  **refused**. Corroboration must hold at the boundary.
- **P4 rapid double flip** (ep 24–31): flips two episodes apart (designed
  churn) → 2 committed switches, both partitions survive with distinct
  labels (switching preserves knowledge, §3a).
- **P5 slot pressure + deliberate destruction** (ep 32–39): scripted KILL
  of a stale USER partition (fields zeroed), ROLLBACK restores it,
  REFUSED_FULL at capacity, refusal battery (ACTIVE/PINNED/CORE/NOTLIVE),
  stage-gating battery, rollback-of-SWITCH restoring `active`.

Measurement blocks every 8 episodes: uncorrupted 16 probes on the active
partition, read-only, never fed to RECORD (H-07 evaluator separation).
With designed probes these read exactly 16/16 when the declared label
matches truth.

## 8. What breaks if the unification is wrong (falsification story)

The unification claims one slot type can serve both families without
interference. It is wrong if any of these obtain — each is a
preregistered FAIL criterion in UPT1:
1. **Cross-talk**: a memory op corrupts partition evidence, or a CTX op
   corrupts memory fields (detected by the §6 isolation snapshots).
2. **Ledger incoherence**: replay diverges from live state in any field,
   `stage`, or `active` — the two families' state dimensions cannot be
   represented in one ledger.
3. **Refusal conflict**: a case where the two families' refusal semantics
   demand opposite outcomes on one op (e.g. KILL on the active partition
   must choose between "it's USER and unpinned, therefore killable" and
   "it's the committed context, therefore protected"). The design resolves
   it by precedence (ACTIVE first, §2); if the trial finds a case the
   precedence table doesn't cover, the unification is incomplete.
4. **PIN paradox**: if protecting a partition from KILL while allowing
   RECORD turns out to destroy the protection contract in any reachable
   sequence (e.g. RECORD used as destruction-by-replacement), the §3b
   resolution is wrong.
5. **CORE leakage**: any path by which a partition reaches CORE, or a
   CORE slot becomes switchable/recordable.
6. **Switch-as-destruction**: any committed SWITCH that zeroes, alters,
   or orphans a partition's knowledge.

An honest negative on any of these is a first-class result: it would show
the families need separate stores with a bridge protocol, not one slot
type.

## 9. Relation to prior art

- Inherits MA1's op/audit/rollback machinery and refusal philosophy
  (MEMORY_OPS.md, MEMORY_SAFETY.md) and HT1's corroborated switching
  (CTX_DESIGN.md, TRIAL_RESULTS_HT1.md) unchanged in semantics; only the
  store is unified.
- Closes HT1's honest boundary on slot pressure (partitions were never
  destroyed in HT1) via deliberate KILL + REFUSED_ACTIVE.
- Defers to future work (unchanged): learner-driven probe timing/label
  choice (HT2), CORE graduation gate, multi-user region keying, ST2 scale
  trial.
