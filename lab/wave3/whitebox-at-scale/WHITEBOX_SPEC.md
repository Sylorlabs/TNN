# White-box at scale — specification

Wave-3 investigator, 2026-09-19. Native-lab work; prototype in `trial/`
(Zag, this Linux VM); prereg `PREREG_WB3.md`; results
`TRIAL_RESULTS_WB3.md` (2469/2469 checks pass natively).

Micah's constraint is non-negotiable: **TNN stays a white box at real
scale.** MA1 proved the toy-scale version: every state change audited,
replay reconstructs exact state, refusals audited ("conscious" =
no state change without an audit entry). This spec answers what
white-box-ness *requires* when the toy era ends — without letting any
layer become "trust me."

## 1. Why toy-scale auditing doesn't survive scale (the problem)

MA1's ledger is complete: 10 words per op, every op, forever. At real
scale — millions of memory writes, many partitions, long horizons —
three costs explode: ledger bytes, replay time, and inspection cost.
The naive responses each smuggle in a trust-me layer:

| Naive response | The trust-me layer it creates |
|---|---|
| Audit less (drop entries when full) | "The missing history didn't matter" — unverifiable |
| Sample ops randomly | "The sample is representative" — statistical, not structural; and RNG in the system is now banned (program law A2) |
| Summarize opaquely | "The summary is faithful" — who checks the summarizer? |
| Keep a parallel "overview" structure | The overview can drift from the ledger; which one is ground truth? |

The requirement, then: a **visibility budget the learner manages
deliberately**, where every economizing decision is itself maximally
visible, and where summaries are *verifiable*, not trusted. That is
selective audit.

## 2. Requirements (non-negotiable)

- **R1 — Attribution.** Every state change is attributable to a ledger
  entry or a digest-covered batch record. No unattributed deltas. This is
  the MA1 "conscious" test generalized: `replay(ledger) == live_state`
  must hold at any scale, for the audited subset (§4).
- **R2 — The visibility budget is itself visible.** Audit levels are
  declared per-slot state; every level change is a FULL ledger entry with
  before/after. An overseer can always answer "why is this slot only
  summary-audited?" with a ledger entry, never a shrug.
- **R3 — Structural floors (anti-self-blinding).** CORE region, pinned
  slots, LONG-tier promotions, stage changes, manifest updates, and
  audit-level changes are ALWAYS fully ledgered. The floors are in the op
  implementation's first lines (like `REFUSED_CORE`), not in a policy the
  learner can route around. The system cannot vote itself out of
  oversight: any path to reduced visibility passes through a fully
  visible deliberate op.
- **R4 — Summaries are replay-exact, not trusted.** The audited subset =
  every slot's exact current state + every FULL entry + every batch
  digest + the manifest history. Replay reconstructs all of it exactly;
  batch digests are *recomputed by the verifier* from ledger data. A
  digest is never taken on faith.
- **R5 — Manifests are replay-derivable.** The cached capability manifest
  must equal an independent fold of the ledger. Disagreement is a tamper
  signal, not a display bug. No "trust the cache" layer.
- **R6 — Inspection answers come from store+ledger only.** No parallel
  overview structures that could drift. Every inspection API reads the
  same two arrays the replay reads.
- **R7 — Fail-closed ledger.** On capacity exhaustion the store refuses
  new mutations; it never drops history. (MEMORY_SAFETY.md layer 3,
  preserved at scale.)
- **R8 — Deterministic.** The same op sequence produces byte-identical
  ledgers. No RNG anywhere in the system — no random sampling, no
  stochastic tie-breaks, no seeded RNG in the learner (program law A2).
  Determinism is what makes ledgers diffable and replays checkable.

## 3. Selective audit: the mechanism

### 3.1 Two levels, one decision op

Each slot carries `alevel ∈ {FULL, SUMMARY}`.

- **FULL**: every op on the slot appends a complete entry —
  `(op, slot, rc, before×3, after×3, stage)`, 10 words — MA1 semantics
  unchanged, including audited refusals.
- **SUMMARY**: successful ops append a compact record —
  `(op, slot, after×3, seq)`, 6 words — grouped into deterministic
  batches (§3.3). Before-words are *not* stored for summarized ops.
  **Refusals on SUMMARY slots are still FULL entries** (a refusal is
  high-signal; MA1's clean-refusal invariant stays global).

**Who decides.** The learner, deliberately, via `AUDIT_SET(slot, level)`:
stage-gated (≥ MANAGE), always itself a FULL entry. Substrate estimators
(op-frequency counters, etc.) may **advise**; they never decide — the
MA1 anti-RL clause extends to audit: no optimizer, no sampling, no
reward signal anywhere near the visibility budget. The learner's audit
*policy* (which slots deserve SUMMARY) is declared in the capability
manifest (§5) as data; the per-slot levels are the auditable record of
that policy in action.

**The default is FULL.** New slots are FULL; downgrading to SUMMARY is a
deliberate audited act. Visibility first, economy by decision — never
the reverse. (This is the opposite of "audit less by default and hope.")

### 3.2 Structural floors (what can never be summarized)

Enforced in the op implementations, unconditional:

- `AUDIT_SET(slot, SUMMARY)` on a CORE-region slot → `AUDIT_LOCKED` (refused, audited).
- `AUDIT_SET(slot, SUMMARY)` on a pinned slot → `AUDIT_LOCKED`.
- `PIN` and `PROMOTE_TO_LONGTERM` force the slot to FULL as part of the
  op (protection and long-term retention are high-stakes by definition).
- `AUDIT_SET`, `SUM_FLUSH`, `MANIFEST_UPDATE`, `SET_STAGE` entries are
  always FULL. Refusals are always FULL.

The shape of the guarantee: the set of things that can reduce future
visibility is exactly the set of things that are maximally visible now.
There is no path from "fully audited" to "less audited" that isn't
itself fully audited.

### 3.3 Batching and digests (deterministic)

Summary records accumulate in an open batch. The batch closes
**deterministically**: every `BATCH=8` records (auto-close), or on an
explicit deliberate `SUM_FLUSH`, or implicitly before any FULL entry is
appended (invariant: *no open batch spans a FULL entry* — this keeps
replay a single in-order fold with no clock merge).

The close appends a FULL `BATCH_CLOSE` entry committing
`(batch_id, count, digest, clock_first, sum_offset)`. The digest is a
deterministic polynomial rolling mixer over the batch's records in
sequence order (seed 17, base 31) — logic-driven, no RNG. Batch ids are
a checked chain: a missing or reordered `BATCH_CLOSE` fails replay.

Honest characterization: the digest is **tamper-evidence, not a
cryptographic commitment**. Threat model: accidental corruption and
ledger-bypass mutation paths (the MEMORY_SAFETY.md "audit evasion"
threat). Malicious same-user mutation resistance is explicitly not
claimed (cf. ZAG_PLAYBOOK.md §9). The digest's job is to make "the
summary doesn't match the records" mechanically detectable — which the
trial proves against two designed tamper injections (T1/T2).

### 3.4 The honest degradation: what SUMMARY gives up

Dropping before-words for summarized ops has exactly one cost:
**per-op rollback degrades to batch-boundary rollback** for SUMMARY
slots. After-words still reconstruct every state exactly (R1 holds);
what's lost is the single-op "before" snapshot. Restoration to any
batch boundary is via replay-prefix — deterministic, no special op
needed, and therefore no new trusted mechanism.

An overseer asking "what did this slot look like before op X?" gets a
ground-truth answer with its reason: "state at the last batch boundary
before X; per-op history is unavailable because the slot was
SUMMARY-level by audited decision D at clock T." A declared, auditable
limitation — not a gap.

### 3.5 What selective audit is NOT (anti-patterns, banned)

- **Not sampling.** Every op is recorded (compactly). There is no
  "representative subset" argument anywhere.
- **Not lossy summarization.** The compact record plus the batch digest
  reconstructs exact state. Nothing about *what happened* is
  approximated; only per-op *before*-states are coarsened to batch
  boundaries.
- **Not a parallel overview.** There is one ledger and one record array.
  The manifest (§5) is a replay-derivable view, not a second source of
  truth.
- **Not adaptive-behind-your-back.** Level changes are deliberate ops,
  never background heuristics. There is no TTL, no GC, no decay — the
  MA1 paradigm ("everything that happens to a memory is an audited
  deliberate act") survives scale intact.

## 4. The audited subset, precisely

"Full replay still reconstructs the audited subset exactly" means:

| In the subset (replay-exact) | Explicitly not in the subset |
|---|---|
| Every slot's current fields (live/value/pinned/region/tier/step/**alevel**) | Per-op before-words of summarized ops (batch-boundary granularity instead) |
| Every FULL entry verbatim (incl. all refusals) | Nothing else |
| Every compact record verbatim, digest-verified | |
| Every batch digest (recomputed, not trusted) | |
| The manifest history (each update's declared digest verified at replay) | |

Anything not in the left column is a deliberate, declared, audited
limitation — which is exactly what keeps the right column from becoming
a trust-me layer.

## 5. Capability manifests

A manifest is an **inspectable declaration of what the system can
currently do**, updated only by deliberate ops:

- **Contents (v0):** autonomy stage, audit policy id (the learner's
  declared visibility policy), `config_digest` (deterministic mixer over
  all per-slot levels + stage + policy), and fold-derived counts
  (full/summary ops, batches, refusals). Deliberately small: the manifest
  declares *configuration*, not *knowledge* — slot contents are not
  duplicated into it.
- **Update rule:** `MANIFEST_UPDATE` only. Always a FULL entry carrying
  old/new `(policy, config_digest)`. No background process may touch it.
- **No-trust-me closure:** `INSPECT_MANIFEST` recomputes the digest by
  folding the ledger's visibility-relevant ops independently and compares
  against the cache. Match = verified; mismatch = tamper signal. The
  manifest is a cached *view* of the ledger, and the view is checked.
- **What manifests are for:** an overseer reads current capability
  without replaying the whole ledger — but can always demand the replay
  behind any manifest claim. Staged-autonomy unlocks (MEMORY_SAFETY.md
  §4) and structural-revision promotions (R27's
  `diagnosis → proposal → measured → PROMOTE/rollback`) are the natural
  future contents: each promotion decision already has the audited shape
  a manifest entry needs.

## 6. Inspection API (overseer questions with ground-truth answers)

Every API reads only the live store and the two ledger arrays (R6):

| Question | API | Ground truth source |
|---|---|---|
| What can the system currently do? | `INSPECT_MANIFEST` | manifest cache vs independent ledger fold (must match) |
| How much is fully vs compactly audited, per region? | `INSPECT_COVERAGE` | region bits folded from entries + records, cross-checked against independent counts |
| Why is slot S in this state? | `INSPECT_WHY(slot)` | last entries/records touching S, with clocks and batch seqs — the CTX_DESIGN §5 requirement ("every commitment carries its reason") |
| Does the ledger reconstruct current state? | `INSPECT_REPLAY` | full replay: exact state equality + digest chain + refusal cleanliness + manifest digests |
| What are the last N events? | ledger tail scan | the append-only arrays themselves |

**The closure argument (no trust-me layer).** Each API's answer is
*derived*, not *asserted*: manifests are re-derived (§5), coverage is
cross-checked between two independent folds, WHY reads the same entries
replay reads. The remaining trust is explicit and minimal — the
**trusted computing base**: (1) the op implementations' refusal checks
(first lines, structural like `REFUSED_CORE`); (2) the append-only
writer (fail-closed, never overwrites); (3) the replay function itself.
White-box doesn't mean zero trust; it means the trust is named,
bounded, and inspectable — everything else is verified data.

## 7. Scale analysis (program law A1)

**Cost model.** All structures are fixed-capacity arrays. Per-op cost is
O(1) (one record append + O(1) digest update). Replay is O(ledger
entries). Batch digest verification is O(batch). Nothing is
superlinear; nothing allocates per op.

**Measured (native, this VM).** The trial runs the identical protocol at
1x (64 slots, 5 churn blocks) and 10x (640 slots, 50 churn blocks):

- Marginal ledger cost per churn op: **952 B / 26 ops = 36.6 B/op,
  exactly equal at both scales** (integer-exact:
  `(bytes₂−bytes₁)×26 == (ops₂−ops₁)×952`).
- Replay returns exact (`rc=0`) at both scales; manifest re-derivation
  matches at both scales; all 2469 checks pass at both scales.
- Determinism: two independent 1x runs produce byte-identical ledgers
  (program law A2 evidence — "the system is deterministic").

**What 10x does and doesn't show.** It shows the mechanism's costs are
linear in ops and slots with no hidden superlinear term, and that the
structural floors hold under 10x churn. It does not show 100x.

**Next scale test (WB3-SCALE-100x, explicit).** Same protocol at 100x
(6400 slots, 500 churn blocks): gate = marginal bytes/op still exactly
952/26 AND replay still exact AND wall-clock replay time linear in
entries. If replay time goes superlinear, the fix is *indexed* replay
(batch-level skip via verified digests) — designed then, not assumed
now. **Bigger tables are still dead** (program law A1): scaling here
means more slots/records through the same deliberate-op machinery, never
N×N score structures.

## 8. Determinism (program law A2)

There is **no RNG in the system and none in the harness**: batching is
count-deterministic, digests are a deterministic mixer, op sequences are
explicitly designed, tie-breaks don't exist (first-empty-slot allocation
is positional, not random). The double-run check (byte-identical
ledgers across independent runs) is the trial's evidence. Determinism
is load-bearing for audit: only deterministic ledgers are diffable, and
only diffable ledgers let an overseer distinguish "the system changed"
from "the record changed."

## 9. Adversity as designed curricula (program law A3)

The world may be unpredictable; the test harness is not. All adversarial
cases are explicit designed sequences, no seeded RNG even as scaffolding:

- **T1 — ledger-bypass mutation of a summary record** (flip an
  after-word out-of-band): replay must report digest mismatch (rc=2).
  Proves summaries aren't trusted.
- **T2 — out-of-band state mutation** (clear a live flag with no ledger
  entry): replay must report divergence (rc=1). Proves R1 has teeth.
- **T3 — ledger exhaustion**: the next mutation must refuse
  (`AUDIT_FULL`), the ledger must be intact, replay must still pass.
  Proves R7 fail-closed.

The verdict distinguishes the two claims: "the system is deterministic"
(double-run evidence, §8) vs "the test was adversarial" (T1–T3, this
section). A deterministic system under adversarial test is exactly the
combination the law demands.

## 10. What this does NOT show / open questions (honest negatives)

1. **Judgment quality.** Whether the learner *chooses* good audit levels
   is protocol-fixed here (as MA1 fixed values). Training the visibility
   budget — which memories earn SUMMARY, when to re-upgrade to FULL —
   is later work in the MA Phase-4 shape (adversarial curricula,
   withdrawal test). This spec proves the *machinery*, not the judgment.
2. **The SUMMARY tradeoff's policy wisdom.** Batch-granular rollback for
   summarized ops is mechanically sound; whether it's *acceptable* for a
   given deployment is a policy judgment, declared per-slot, auditable —
   not settled here.
3. **100x.** Named next test (§7), not claimed.
4. **Manifest schema evolution.** v0 covers configuration; carrying
   promotion decisions (R27 shape) and staged-unlock records is designed
   (§5) but not prototyped.
5. **Multi-region serving.** CORE/USER separation exists (floors keyed on
   it); per-user USER partitions are future work per MEMORY_OPS.md §5.
6. **Digest strength.** Tamper-evidence, not cryptographic commitment
   (§3.3). Upgrading the mixer is a contained change; the replay
   *structure* doesn't depend on which deterministic function is used.

## 11. Relation to prior art (laws honored)

- **MA1/MA2/MA3** (`wave2/memoryagency/`): the op set, staged autonomy,
  append-only ledger, and fail-closed overflow are inherited unchanged;
  selective audit *extends* the ledger, it doesn't replace it.
- **CTX_DESIGN.md §5**: "every commitment carries its reason in the
  ledger" → `INSPECT_WHY`.
- **MEMORY_SAFETY.md**: four defense layers preserved; audit evasion
  (layer-3 threat) is what T1/T2 test.
- **DO_NOT_REPEAT.md**: no score tables anywhere; no RL/reward-shaping
  (the audit path carries no reward signal); no aggregate-only reporting
  (coverage is per-region, counts are exact); no RNG in the system;
  evaluator-separation discipline kept (the trial's assertions are
  protocol-fixed, judgment quality explicitly not claimed).
- **R27 lineage** (`brain/STATE_SCHEMA.md`): the manifest is the native
  descendant of `self_revision_history` — measured structural decisions
  with authorship, replayable.

## 12. Prototype map

- `trial/wb3_core.zag` — the store: ops, two-level ledger, deterministic
  batching/digests, replay, inspection API (~600 lines Zag, integer-only).
- `trial/trial_wb3.zag` — driver: 1x/10x protocol, double-run
  determinism, T1–T3 adversity.
- `trial/run_wb3.sh` — runner; every `CL_CHECK` line verified
  actual==expected; evidence bundles per run.

One binary, no external tools, no network, no RNG. The white box stays
open because every economizing decision the system makes about its own
visibility is itself the most visible thing in the ledger.
