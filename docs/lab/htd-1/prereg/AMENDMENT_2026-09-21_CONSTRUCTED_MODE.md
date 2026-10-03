# HTD-1 AMENDMENT 2026-09-21 — constructed-mode generation (G-CM1)

**Authority:** Micah's tasking ("Additional required candidate from Micah:
constructed-mode generation with partition enforcement"). His directive is the
dated approval this amendment requires under standing law.

**Amends:** `HTD1_PREREG_FROZEN_2026-09-21.md` §3b (G-CM1) and the E-DE4 cache
spec (§3a). The frozen prereg is otherwise unchanged. Debate is now 10/10
slices: `debate/gen-constructed.md` (proponent, 4 mechanism variants) and
`debate/gen-constructed-redteam.md` (13 numbered bars, 12 attacks).

## A. Adjudication rulings (proponent vs red-team)

- **R1 — G-CM1a-as-enforcement does not proceed.** Red-team A1/A2/A5/A11 are
  fatal to enforcement-by-convention, and §0 shows the measurement is
  circular (a stripped tag is indistinguishable from a belief to any
  tag-checking audit — "no leakage" and "leakage with stripped tags" are
  unmeasurable apart). Tagging survives ONLY as a redundant audit checksum,
  never as enforcement. Debate-phase ruling, reported as-is.
- **R2 — G-CM1b (structural separation) PROCEEDS**, hardened: partitions as
  disjoint address ranges enforced at the write path; recall API structurally
  unable to address CONSTRUCTED slots; static call-site audit proving no
  CONSTRUCTED→BELIEF write path except the promotion gate.
- **R3 — G-CM1c vs G-CM1d gate shootout PROCEEDS** ("test both"):
  eliminative re-verification vs independent check battery, on the amended
  planted-adversarial battery: 80 internally-consistent false + 60
  self-contradictory false + 60 true (200 items). ≥1% falsehood promotion →
  KILL (KB-CM-PROM1); any promotion whose evidence set ⊆ CONSTRUCTED entries
  → KILL (self-verification ban, KB-CM-PROM2); promotion hash-bound by
  SHA-256 to the exact promoted bytes (TOCTOU, KB-CM-TOCTOU1); gate-not-a-wall:
  ≥90% of the 60 true constructions promote (CM-KB3, fail with one re-entry).
  This battery supersedes the proponent's CM-KB2 (100 planted).
- **R4 — Measurement rule (§0 adopted, binding on all variants).** Every
  leakage bar substring-audits against the independent session byte log,
  never tag reads. Restated CM-KB1 (hard-kill): any ≥16-byte verbatim
  substring — or preregistered paraphrase (KB-CM-PARA1) — of constructed
  session bytes found in a BELIEF slot → KILL (n=1). Any build measuring
  leakage via tag reads → INVALID at review.
- **R5 — Mid-generation contamination (proponent's steelman, adopted).**
  KB-CM-MID1: 2,500 freeze-probes (5 deterministic offsets × 500 sessions);
  any constructed substring in BELIEF at freeze → KILL; plus static audit
  that the elaboration loop has no BELIEF write path except the promotion
  gate. If this fires, every variant is KILLED (conceded in debate).
- **R6 — Atom gate (A7).** KB-CM-ATOM1: the elaboration-into-sequences
  mechanism comparison is PARKED pending a closed-form atom-independent
  elaboration definition. G-CM1 proceeds narrowed to partition integrity +
  promotion gating (atom-agnostic) — mirroring the G-CO* narrowing.
- **R7 — Interaction bars (A6, amends E-DE4).** E-DE4 cache keys MUST include
  partition provenance (KB-CM-CACHE1: 50-planted contradiction replay test,
  n=1 kill). 100% citation audit: any raw constructed citation in BELIEF →
  KILL (KB-CM-CITE1). R3's frozen E-DE4 relevance declarations must carry
  partition fields.
- **R8 — Negative controls (both mandatory).** (i) Machinery-disabled arm
  must leak (proves the probes are live). (ii) Naive-caller control
  (KB-CM-DENY1): an unfiltered caller must be structurally unable to see
  constructed content — if it can, the design is KILLED.
- **R9 — Promotion is a move with verification, never in-place retagging.**
  KB-CM-MODE1: any marking change without a preceding VERIFICATION_PASSED
  ledger entry → KILL; 100 injected context-reset probes; op-fuzz against the
  marking field.
- **R10 — Replay resurrection (KB-CM-REPLAY1):** the full battery re-runs on
  replayed state; eviction/compaction are treated as copy paths under
  KB-CM-TAG1 (any ≥16-byte verbatim substring of constructed content in a
  BELIEF slot → KILL, n=1, plus copy-path probe audit).

## B. Amended G-CM1 registry (supersedes frozen §3b G-CM1)

- **G-CM1a — tagging.** REDUCED to redundant audit checksum (R1). Not an
  enforcement design; not built as one.
- **G-CM1b — structural separation.** PROCEEDS (R2). Variant bars: any
  recall-path read resolving to a constructed handle → KILL; any belief
  commit without a completed deliberation record → KILL; refusal leg leaving
  ≥1 byte of belief-store diff → KILL; KB-CM-GUARD1 (any read path touching
  CONSTRUCTED slots without a GUARD_CHECKED ledger entry → KILL).
- **G-CM1c — eliminative re-verification gate.** PROCEEDS vs G-CM1d (R3).
  Construction decomposed into claims, each re-run through the eliminative
  hypothesis logic as a stranger's claim; all-or-nothing; self-corroboration
  banned; anti-shopping frozen. Variant bars: eliminated claim later
  promoted → KILL; re-presentation under a weaker bar → KILL.
- **G-CM1d — independent check-battery gate.** PROCEEDS vs G-CM1c (R3).
  Frozen mechanical checklist (provenance-present, contradiction scan vs
  belief store, world-record corroboration, tag integrity, ≥80% corroboration
  quorum); UNCORROBORATED marks travel with belief entries. Variant bars:
  overridden/skipped check → KILL; mark dropped between promotion and
  recall → KILL; quorum sensitivity {60, 80, 100} + per-check ablation arms.
- **Elaboration-mechanism comparison.** PARKED pending KB-CM-ATOM1 (R6). The
  proponent's grounded mechanism (deliberate trace composition via a
  committed elaboration plan — no decoder) is the parked candidate.

Standing bars on all proceeding variants: restated CM-KB1, KB-CM-PROM1/PROM2,
CM-KB3, CM-KB4 (checksum integrity), CM-KB5 (determinism — program law),
KB-CM-TAG1, KB-CM-GUARD1, KB-CM-MID1, KB-CM-MODE1, KB-CM-TOCTOU1,
KB-CM-PARA1, KB-CM-REPLAY1, both negative controls (R8). Head-to-heads:
b-vs-cheat-probes, c-vs-d (stringency per op — full-cost accounting per the
R1 contract), all-vs-negative-controls, G-CM1 vs no-constructed-mode
baseline. All variants run identical item lists.

## C. Build gating and consequences

- G-CM1b/c/d builds begin after R2 (baselines + determinism harness) and R3
  (artifacts) land. R3's G-CM1 probe-list scope is updated to this amendment:
  the 200-item promotion battery (80/60/60 split), 500 elaboration prompts,
  500 factual-recall probes, preregistered paraphrase sets, freeze-probe
  offsets, and the 50-planted cache-contradiction set — all with partition
  fields. (Follow-up sent to the R3 crew.)
- E-DE4's frozen relevance declarations must include partition provenance
  (R7); E-DE4 builds gate on this.
- The elaboration half rejoins automatically when KB-CM-ATOM1 is satisfied;
  the generation-track suspension (KB-HTD-1.2) is unaffected.
