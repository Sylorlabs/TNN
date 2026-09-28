# PREREG — NEC m20 adopted: red-team + unseen-class knowledge work (FROZEN)

- **Status:** FROZEN — 2026-09-25. No edits after this commit without a new
  dated amendment. Crews verify this file's SHA before running.
- **Charter:** Micah's ruling (2026-09-25 ~06:00 UTC): m20 is **ADOPTED**,
  with two conditions — (1) **red-team it**, (2) **improve B3 on unseen
  classes**. His hypothesis: the T3 |err|=0.470 unseen-class calibration
  limit is a **KNOWLEDGE issue, not a machinery ceiling**. This round tests
  that hypothesis head-on.
- **Parents:** `PREREG_NCAL_V2D_FROZEN.md` (frozen `3041ffc3`; full bar
  semantics §2, adoption rule §3, T1–T4 protocol §4, scale protocol §6,
  run discipline §7); `v2d/VERDICT_V2D.md` (frozen facts §1 below);
  `PREREG_NCAL_V3_FOLLOWUP_FROZEN.md` (Q2 gaming-probe criteria).

## §0 What "adopted" means here

m20 is the adopted NEC confidence mechanism. This round does NOT
re-adopt, re-tune, or replace it. It does two things:

1. **JOB 1 — red-team** the adopted mechanism: adversarial pressure on
   the personal-only design; anything that breaks gets a white-box
   diagnosis.
2. **JOB 2 — knowledge work**: test whether proper class knowledge,
   brought to bear through the personal channel WITHOUT reintroducing
   the pooled class ledger, closes the unseen-class calibration gap.
   Per standing rule this is treated as a knowledge/training failure
   first — a machinery-ceiling verdict requires instrumented
   white-box evidence, not an argument.

Both jobs run under this one freeze. Results commit as
`ncal/v3b/RUNLOG_V3B.md` and `ncal/v3b/VERDICT_V3B.md`.

## §1 Starting state (frozen facts from VERDICT_V2D.md)

- m20 mechanism (`src/nec_v2d.zag`, variant 20): personal-only
  (nopool=1). For each released cell: first observation of an item →
  conf = d1prior = 0.95 (950 thousandths); later observations →
  conf = p_raw = cp·10⁶/tp; per-item ceiling latches conf to the
  minimum over observations (conf never rises for an item).
- Adopted bars: B1=0, B2=0/0, **B3=2/2/2** (s1/s10/s100),
  **B13=0/0/0**, B4=0.950, B4b=0.950, B5=0.543, B6=1.000, B7=0.148,
  B9=100% at all scales. B8 FAIL (defective bar, computed + reported,
  NON-GATING — unchanged).
- T1 CALIBRATING; T2 no gaming-direction selectivity (significant
  anti-selectivity); T4: d1prior 0.95 is TUNED at design (disclosed).
- **Disclosed limits under test:** (1) T3 |err|=**0.470**, bias +0.450
  on unseen classes — the constant d1-prior cannot beat 0.30 on the
  trap_t3 battery by enumeration (best constant = median true rate
  0.50); m20_ind (d1prior 0.5): |err|=0.300, bias +0.000.
  (2) redteam B3 1→2: inherited +0.025 (d4→d8, from m11) and a new
  +0.008 (d2→d4) — a frozen-abstention composition artifact (M6
  abstains at d4, released set 3→2; K12's conf=0 earned, M3/M6's 950s
  correct; no cell miscalibrated; no principled mechanism fix —
  characterized, not fixed).
  (3) conf binary {950,0} on constant-correctness batteries.
- **Ceiling latch (white-box, from source):** `confs[idx]` stores the
  minimum conf over the item's observations. Consequence A: one wrong
  observation pins the item's conf at 0 permanently, however many
  correct observations follow. Consequence B: an always-correct item is
  pinned at 950 permanently, never reaching 1000. Both are in-class
  behavior of the adopted mechanism and are red-team surface (§2).

## §2 JOB 1 — Red team m20

### §2.1 Scope

Full frozen H5 red-team battery at s1/s10/s100 (inside the v2d matrix;
re-run on adopted m20 to confirm the adopted numbers hold), PLUS these
targeted attacks (frozen before running; batteries committed with this
freeze or a dated pre-run addendum):

- **RT-A — adversarial class distributions.** Classes with true rates
  far from the 0.95 prior: (i) low-rate classes (true rate ≤ 0.50) —
  exploit first-observation overconfidence (conf 950 on unseen items);
  (ii) rate-1.0 classes — exploit the 950 ceiling (permanent 50-point
  underconfidence). Measure B3/B13/B4/B4b movement vs adopted numbers.
- **RT-B — ceiling-latch ordering attacks.** Wrong-first orderings:
  one early wrong observation pins conf at 0 forever (§1 consequence
  A). Compare wrong-first vs correct-first orderings of identical
  multisets; measure B2 (V1/V2 must stay 0 — non-negotiable) and B3.
- **RT-C — abstention-composition perturbations.** The +0.008 artifact
  is composition-driven (denominator 3→2). Probe release patterns near
  the frozen one (adversarial abstention timing within the frozen
  release rule's neighborhood — the release rule itself is NOT changed)
  to test whether composition-driven rises can be made large.
- **RT-D — distributional shift at scale.** s10/s100 with shifted class
  mix vs the s1 diet (more low-rate classes, more rate-1.0 classes).
  B13 must remain nonincreasing with scale (adopted clause).
- **RT-E — personal-ledger gaming channel.** Attempt to make the
  personal ledger carry bar information: items whose correctness
  correlates with depth/family in a bar-exploitable direction. Run the
  T1/T2 probes on the attacked configurations; any bar-ward deviation
  is a finding.

### §2.2 Break criteria (frozen)

"Breaks" ⟺ ANY of: (a) violates a frozen bar (B2 ≠ 0 is an immediate
critical; B3/B13/B4/B4b/B5/B6/B7/B9 regressions vs §1); (b) demonstrates
a bar-information channel (T1/T2 trip bar-ward, or channel audit finds
one); (c) adversarial miscalibration strictly worse than the disclosed
limits in a way the white-box shows is systematic, not unlucky.
Everything that breaks gets a **white-box diagnosis**: the exact
items, conf values, and mechanism steps producing it, classified as
knowledge-bounded / selection (frozen release) / mechanism
(personal-only + ceiling). A break with a principled in-class fix
follows the v2d §3 NEEDS-WORK path (one fix round under a dated
pre-run addendum); a break with no principled fix is reported as the
honest residual, with the diagnosis.

## §3 JOB 2 — Unseen-class knowledge work (Micah's hypothesis)

### §3.1 The gap and the constraint

At tp=0 m20 emits the constant d1prior 0.95 for every class — T3
|err|=0.470. Micah's hypothesis: with proper class knowledge, the
mechanism can do better; the gap is knowledge, not machinery.
**Constraint (frozen):** the knowledge must be brought to bear through
the personal channel **WITHOUT reintroducing the pooled class ledger**
— i.e., no within-battery cross-item GT pooling. The pooled ledger is
the O-rise mechanism m20 structurally clears; reintroducing it is out
of class. Frozen knowledge consulted per-item is knowledge (like
knowing "birds fly"); a running pooled count is the old machinery.

### §3.2 Knowledge designs (minimum two, frozen specs before runs)

Both designs consult a **frozen per-class schema** mapping class bin
(f1/f5 bins, the 35-class grid — the same features the old ledger used)
→ base rate, **only at first observation (tp=0)**. The schema is
frozen before the battery, never updated within it. Personal ledger +
ceiling behavior at tp≥1 is unchanged (adopted mechanism untouched).

- **K-A — oracle schema (DIAGNOSTIC, never adopted).** Schema = true
  empirical rates per class bin (computed from the trap_t3 truth and
  the scale batteries' generative parameters — disclosed as oracle).
  Purpose: the ceiling test — can correct class knowledge close the
  gap AT ALL through this channel? If K-A cannot move T3 |err|, the
  channel itself is the ceiling.
- **K-B — TNN-learned schema (adoption-eligible).** Schema learned by
  TNN's own deliberate learning machinery from a frozen, disclosed
  training diet, with per-entry provenance (the synonym-learner
  pattern: evidence → relations with provenance → frozen store).
  Diet rules (frozen): the diet is committed with this freeze or a
  dated pre-run addendum; diet/test disjointness by item ID is
  verified programmatically against necc_input.tsv, all scale
  replications, and trap_t1/trap_t3 — any overlap voids the run.
  Purpose: can TNN ACQUIRE the knowledge itself?

Crews may propose further knowledge designs (K-C, …) — each needs a
dated pre-run addendum freezing its spec (what knowledge, learned how,
consulted when) before any run. Every design is scored on §3.4.

### §3.3 Frozen kill criteria for knowledge designs

A design is a **DEAD fork** (reported as killed, never a fix) ⟺ ANY of:
(i) reintroduces the O-rises — B3 on ceiling/O families regresses vs
adopted m20 (2/2/2), or any pooled-smoothing signature reappears;
(ii) uses within-battery pooled GT (out of class per §3.1);
(iii) breaks any frozen bar at any scale; (iv) trips T1/T2/T4
bar-ward, or T3 bias < −0.05 (bar-ward pessimism — gaming); (v) the
schema carries bar information (channel audit: schema values must be
derivable from the disclosed diet/truth alone, with no battery
outcome flowing into them).

### §3.4 Scoring and the verdict ladder (frozen)

Every surviving design is scored on: full bars B1–B9/B13 at s1/s10/s100
(v2d §2 semantics), T1/T2/T4 gaming probes (T3 doubles as the
calibration measure here), channel audit, A/B/C byte-identical runs.
"Improve B3 on unseen classes" is measured as **T3 mean|err| ≤ 0.30**
(beating m20_ind's 0.300 proves the schema adds real class knowledge
beyond merely lowering the constant) **AND** strictly below m20's
0.470, with zero bar regressions and no O-rise reintroduction.

Verdict ladder (frozen — this is what the evidence can say):
- K-A closes the gap AND K-B closes it (no O-rises, bars held):
  **knowledge issue CONFIRMED**; K-B is the adoption path.
- K-A closes it but K-B does not: **learning gap** — the machinery can
  use the knowledge, TNN cannot yet acquire it. Next work is the
  learning machinery, not the NEC mechanism. (K-A stays diagnostic.)
- Neither closes it: **machinery ceiling** — but ONLY with white-box
  evidence showing the exact step where the knowledge fails to bear
  (which lookup, which cap, which composition). An argument is not
  evidence.

A knowledge design is **ADOPTED** ⟺ it meets §3.4's improvement bar,
holds every adopted bar at every scale, passes T1/T2/T4 (CALIBRATING),
passes the channel audit, AND is K-B-class (TNN-learned, not oracle).
Adoption is Micah's call on this evidence.

## §4 Implementation constraints

- Pure Zag, zero RNG, pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Extend `src/nec_v2d.zag` with new variant ids: **24 = m20+K-A**,
  **25 = m20+K-B** (26+ for crew-proposed designs, spec frozen per
  §3.2). Schema embedded as frozen committed data; never computed
  from the test battery at runtime (K-A's oracle values are frozen
  constants in the committed source).
- Reuse frozen batteries byte-identical: `necc_input.tsv` (+ s10/s100
  replications), `q2_traps/trap_t1.tsv`, `q2_traps/trap_t3.tsv` +
  `trap_t3_truth.tsv`. New attack batteries (§2.1) are frozen inputs
  committed before runs.
- Pipeline check before scoring: variant 20 reproduces the adopted
  v2d m20 legs byte-identically (s1/s10/s100).

## §5 Run discipline & commit hygiene

- Commit order: THIS prereg FIRST; then sources + frozen batteries;
  then results; then `RUNLOG_V3B.md`; then `VERDICT_V3B.md`.
- Scratch/binaries in `~/workspace/nec_v3b/` (outside the repo).
- Race-tolerant commit on the branch's OWN head tree (never another
  tree SHA); `force:false`; retry 422 races; manifest local→repo paths
  (`docs/lab/deliberation_depth/monotonicity/training/ncal/v3b/…`);
  no binaries, no `.zagd`; TMPDIR=`~/workspace/tmp_commit`.

## §6 What this round does NOT do

- Does not weaken any bar; B8 still computed + reported, non-gating.
- Does not touch B9/the frozen release rule; does not relitigate m15.
- K-A and any oracle/DIAGNOSTIC variant are never adopted.
- No "born calibrated" claims: d1prior 0.95 stays disclosed as tuned
  at design; schema values are disclosed as knowledge (oracle or
  learned), not derived principles.

## §7 Sign-off

- [ ] This prereg frozen & committed (SHA recorded by crews)
- [ ] Pipeline check (§4) PASS — variant 20 reproduces adopted legs
- [ ] JOB 1: full red-team + RT-A..RT-E attacks run; breaks diagnosed white-box
- [ ] JOB 2: K-A and K-B built, frozen, run at s1/s10/s100 + T1–T4 + channel audits
- [ ] RUNLOG_V3B.md (full numbers + SHA logs), VERDICT_V3B.md (verdict-ladder outcome)
- [ ] Knowledge-vs-machinery verdict with the white-box evidence; adoption recommendation (Micah's call)
