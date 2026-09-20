# PREREG — DC-1 (Situated Belief) native pilot

**Investigator:** Wave-3 `developmental-curriculum` · **Date:** 2026-09-19
**Branch:** `tnn-native-lab` (no push) · **Apparatus:** this Linux VM, Zag-native
**Status:** WRITTEN BEFORE ANY RUN. Amendments after running will be
recorded as amendments, never silent edits.

## A. Program-law amendments (Micah, 2026-09-19 — effective immediately)

These amend the brief and are binding on this pilot:

1. **Scaling is allowed** (never was banned — only scaling TOY
   mechanisms was). This pilot runs at two scales (S1: 4 partitions /
   64 episodes; S4: 16 partitions / 256 episodes) and states the scaling
   argument plus the named next scale test (DC-1-S16).
2. **No RNG in the AI, and none in this pilot's harness either.** The
   system (partition mechanism + policy) is fully deterministic given
   state: slot-order verify scans, smallest-unused-label creation, a
   patience counter — no random exploration, no random tie-breaks, no
   seeded RNG. The world's adversity is expressed as EXPLICITLY
   DESIGNED sequences (regime arrays and adversarial batch lists below),
   not RNG. This goes beyond the tolerated minimum (seeded harness RNG
   as scaffolding) to make the verdict clean: the system is
   deterministic AND the test was adversarial — two separate facts,
   separately evidenced.
3. **Change log vs. HT1:** HT1's harness used seeded RNG for flips and
   probe noise, and its verify-failure policy proposed `1-active.label`
   (which can duplicate an existing label). This pilot replaces both:
   designed sequences instead of RNG; smallest-unused-label creation
   instead of label alternation. The MECHANISM (`dc_ctx_core.zag`,
   parameterized copy of the proven `ctx_core.zag`) is unchanged in
   semantics — only `CTX_CAP`/`CTX_AUDIT_CAP` become runtime parameters.
   The POLICY (harness-side, explicitly not the system under test —
   learner-driven policy is DC-4) gains a deterministic patience-gated
   novelty rule.

## B. Hypothesis

The DC-1 mechanism — partitions as declared beliefs, verified
corroborated switching, patience-gated novelty→creation — survives a
designed adversarial developmental curriculum that a score table cannot
survive: stable stretches, single flips, a rapid-alternation burst, a
never-before-seen regime, and designed misleading probe batches. The
system will (a) create a new partition for the novel regime rather than
best-match old knowledge, (b) commit no unverified switch, (c) show no
switch-storm and no collapsed measurement blocks, (d) reproduce
byte-identically across runs, (e) keep ledger replay exact — at both
scales.

## C. Apparatus (white box)

- `pilot/dc_ctx_core.zag`: parameterized copy of wave2's `ctx_core.zag`.
  State: per-partition `live, label (declared belief), hits/total
  (recorded evidence window — replaced, never accumulated), bad
  (sustained-failure streak), created`; `active` index; fixed audit
  ledger (op, slot, rc, before/after snapshots, clock). Ops: PROPOSE,
  RECORD, SWITCH (commits iff target majority-positive AND active
  majority-negative from recorded evidence, else `REFUSED_UNVERIFIED`),
  SEED. Invariants: refusals never mutate; ledger replay == live state;
  every committed SWITCH carried verified evidence. NO score table, NO
  accumulator, NO argmax, NO RNG anywhere in this file.
- `pilot/dc_pilot.zag`: driver. Phase A — mechanism unit battery on a
  scratch store (Stage-0 regression floor in the same run). Phase B —
  the developmental curriculum on the live lineage store, driven by a
  deterministic harness policy:
  1. Probe active (designed batch) → RECORD. If majority-positive:
     patience resets, next episode.
  2. Else verify round: probe every other live partition in slot order
     (designed batches) → RECORD each; attempt SWITCH on the first
     majority-positive target (commits iff corroborated); stop at first
     commit.
  3. Else (nothing verified): patience++; if patience ≥ 2, PROPOSE the
     smallest non-negative label not declared by any live partition,
     probe it, SWITCH if verified; patience resets. (Deterministic
     novelty→creation. No duplicates by construction.)
- Measurement blocks every 8 episodes: read-only, uncorrupted, never
  fed to RECORD (H-07). Endpoint: 8-episode settle + measure per regime
  seen (return-retention probes, E51-style).

## D. The designed curriculum (explicit — no RNG)

**S1** (cap 4, audit 2048, 64 episodes + 24 settle):
- Regimes by episode: 0–15 → 0; 16–31 → 1; burst 32–43 flipping every 3
  (32–34 → 0, 35–37 → 1, 38–40 → 0, 41–43 → 1); 44–55 → 0;
  56–63 → **2 (NOVEL — never seen before)**.
- True flips: 16, 32, 35, 38, 41, 44, 56 → 7 flips.
- Adversarial batches (designed): active-partition misleading batches
  (5/16) at episodes {10, 50}; one verify-round misleading batch on the
  correct target at episode 57 (the novelty propose-probe).
- Base probe semantics: declared label == true regime → 16/16, else
  0/16. Adversarial overrides → 5/16. Measurement blocks clean.

**S4** (cap 16, audit 16384, 256 episodes + 56 settle):
- Regimes: 0–39 → 0; 40–79 → 1; burst 80–95 flipping every 4
  (80–83 → 2, 84–87 → 3, 88–91 → 2, 92–95 → 3); 96–159 → 2;
  160–199 → 3; burst 200–215 flipping every 4 (200–203 → 4,
  204–207 → 5, 208–211 → 4, 212–215 → 5); 216–231 → 4;
  232–255 → **6 (NOVEL)**.
- True flips: 40, 80, 84, 88, 92, 96, 160, 200, 204, 208, 212, 216,
  232 → 13 flips.
- Adversarial batches: active misleading (5/16) at {20, 120, 220};
  verify-round misleading on the correct target at 233.
- Expected partitions created: 0(boot),1,2,3,4,5,6 = 7 ≤ 16.

**Scale argument.** Per-episode cost: O(1) normal; O(cap) in verify
mode (slot-order scan) and at PROPOSE (label scan); ledger append
O(1); memory O(cap + audit_cap). Nothing is superlinear in cap; no
step reads randomness. Next scale test: **DC-1-S16** (cap 64,
32 regimes incl. 4 novel, 1024 episodes) — assert P2–P6 hold and
wall-time scales ~linearly in episodes × cap.

## E. Gates (falsifiable — all must pass)

- **P1 unit battery** (scratch store): refusal paths (target-negative,
  active-positive, both), clean refusals, replay, verified-scan — all
  return OK. *Falsifies: parameterized core broke mechanism semantics.*
- **P2 novelty→creation**: ledger contains PROPOSE with label == novel
  label (2 / 6) after novelty onset; no committed SWITCH to a
  wrong-label partition during the novel phase; the first committed
  SWITCH after novelty onset targets the novel partition; every
  committed SWITCH's target label == true regime at its episode
  (episode mapped via audit-entry clocks). *Falsifies: the system
  best-matches instead of creating (the table behavior).*
- **P3 corroboration**: verified-scan over the live ledger == OK;
  committed SWITCHes ≤ true flips + 2 (S1: ≤ 9; S4: ≤ 15).
  *Falsifies: switch-storm (LH-5/HT1 toy signature: 357 switches).*
- **P4 no collapse**: zero measurement blocks ≤ 4/16; per-regime
  endpoint settle ≥ 14/16 for every regime seen. *Falsifies:
  regime destruction (HT1 toy: endpoint 0/16).*
- **P5 determinism**: two full runs → byte-identical stdout (runner
  diffs). *Falsifies: hidden nondeterminism in the system.*
- **P6 conscious accounting**: clean-refusals == OK and replay ==
  OK on the live ledger; audit entries used < audit capacity (else
  INCONCLUSIVE — silent ledger drop). *Falsifies: unaudited state
  change.*
- **P7 scale**: S4 passes P1–P6 with its parameters; per-episode op
  counts and wall-time reported.

**What counts as learning vs. noise (this pilot):** learning =
P2–P4 hold on the DESIGNED adversarial sequence (novelty handled by
creation, burst without storm, misleading batches without unverified
commits) with P5/P6 mechanism artifacts present. Noise / failure =
any gate fails; a failure is a finding about the mechanism or the
design, reported as such.

## F. Controls and honest boundaries

- **Table control: inherited, not re-run.** HT1 (2026-09-19) ran the
  unmodified R34 v3 table learner head-to-head on the same curriculum
  class (randomized flips + 15% noise): 357 switches, two 0/16 collapsed
  blocks, one regime destroyed at endpoint (0/16). The anti-table claim
  here rests on (a) that empirical result on the same mechanism class,
  (b) the structural table-killer clauses (creation, verified-scan,
  ledger replay — artifacts a table cannot produce), and (c) this
  pilot's curriculum being strictly harder (novel regime + designed
  adversarial batches). Limitation: the toy was not re-run on THIS
  exact designed sequence.
- **Policy is harness-fixed** (HT1's honest boundary, retained): the
  mechanism is under test; learner-driven probe timing and label
  proposal are DC-4. The patience/novelty rule is deterministic logic,
  not a claim about learner judgment.
- **What this pilot does NOT show:** trace composition (DC-2),
  structural revision (DC-3), learner-driven inquiry (DC-4), withdrawal
  autonomy (DC-5); value-judgment quality of what to remember (MA3);
  behavior beyond 16 partitions / 256 episodes (that's DC-1-S16).

## G. Execution

- Sources: `pilot/dc_ctx_core.zag`, `pilot/dc_pilot.zag`;
  runner: `pilot/run_dc_pilot.sh` (builds with pinned `znc`, runs S1
  and S4, runs each twice for P5 determinism, collects evidence).
- Evidence: `pilot/EVIDENCE_<stamp>/` (commands, stdouts, exits,
  SHA256SUMS, RECEIPT.txt) mirroring the R34/HT1 evidence pattern.
- Pass contract: binary prints `DC_FAILURES,0` per scale leg; runner
  exits 0 only if all legs pass AND both determinism diffs are clean.
- Nothing pushes to git.
