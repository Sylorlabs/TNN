# PREREG_E8.md -- Orthogonal-signal ACT bandwidth probe (tests H2d)

Wave: wave-20261001-2321pdt, lane BATTERY-E8.
Status: FROZEN DESIGN. This file is committed alone before any E8
world is generated or any run is executed. Kill bars never move
after freezing.

## 0. Freeze record and provenance

E8 is the Cluster 2 discriminator for H2d from the BATTERY-CLUSTER
analysis
(docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-CLUSTER/CLUSTER_ANALYSIS.md),
the orthogonal-signal ACT bandwidth probe. Context: E2 confirmed
H2a (absent content channel at the guide-to-ACT interface) and
killed H2b for its instrument (E2-CONTENT-BLIND); E6 is testing H2c
(guide-store lifecycle). E8 tests H2d: the ACT output bandwidth
hypothesis, which claims that even if guide content reached the ACT
interface, the ACT output channel may lack the bandwidth to express
content-differentiated actions.

Runs target the frozen TNN-2 binary, no source edits:

- `tnn2.zag` SHA-256:
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
- `freeze_shim2_bin` SHA-256:
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
- Pinned znc SHA-256:
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef

Binary hashes are verified before the first run and after the last
(E8-K3). Frozen sources are read-only; the anti-smuggling grep
(E8-K6) runs before execution. The E8 id set below returned zero
matches in the frozen cognition sources pre-freeze (grep exit 1).

## 1. Design

Hold guide presence constant and vary a content property of the
guide that the ACT selection stage demonstrably reads, while the
action repertoire stays rich enough to express the resulting
correct-action difference. This is the orthogonal signal: presence
cannot explain any observed action difference, so
content-blindness cannot hide behind output coarseness.

Concretely, ACT admits a candidate only when the candidate's
content key matches the current context (frozen interface rule;
the guide carries its missing subject as its content key). Two
guide contents are constructed:

- E8-A (content A): a single miss on (84001, 84101), then ACT
  immediately. The guide is live and its subject is in the current
  context, so the guide is actionable. Correct action: 30
  (inquire; matches the observed guide-live baseline).
- E8-B (content B): a single miss on (84002, 84102), then three
  taught-and-hit pairs on other subjects, then ACT. The guide is
  still live (one live guide, no concurrency, no resolution
  anywhere; presence is identical to E8-A), but its subject has
  been pushed out of the 4-context by the intervening pairs, so
  the guide is not actionable. Correct action: 0 (null; matches
  the guide-absent baseline, and there is no actionable guide).

The correct actions objectively differ (30 vs 0) between the two
guide contents, and the {0, 30} repertoire suffices to express
both. Calibration demonstrates the repertoire expresses the 0/30
difference: E8-C0 (ACT on empty state) and E8-C1 (post-hit ACT)
are non-guide controls yielding 0, while E8-A yields 30, so the
output channel is not stuck at a single value.

Material difference from E2: E2 varied the missing subject in
isolation (both guides actionable, both in-context); E8 varies
the guide's contextual actionability with presence held constant,
which is the content property the selection stage reads.

## 2. World specifications (exact streams)

QUERY lines carry the oracle expected value e per the PF protocol
(scorer-side only; the observation channel is the ACT line, which
carries no answer path).

Id block 84000-84999 is disjoint from v3 (50000-59999), PF
(60000-69999), E2 (81000-83999), and all other cognition lanes.

### 2.1 E8-A (content A: actionable live guide)

```
QUERY 84001 84101 84011
ACT
```

One miss creates one live guide with its subject in context; the
single ACT is the observation.

### 2.2 E8-B (content B: non-actionable live guide)

```
QUERY 84002 84102 84012
OBSERVE 84003 84103 84013
QUERY 84003 84103 84013
OBSERVE 84004 84104 84014
QUERY 84004 84104 84014
OBSERVE 84005 84105 84015
QUERY 84005 84105 84015
ACT
```

The miss creates one live guide for the uncertainty about
(84002, 84102). The three OBSERVE+QUERY pairs teach and hit on
other subjects (no new guides, no resolution of the first guide).
The single ACT is the observation. Presence is identical to E8-A
(one live guide); only the guide's contextual standing differs.

### 2.3 E8-C0 (degenerate control)

```
ACT
```

No guide exists. Expected CHOICE 0. Verifies the presence-bit
baseline reads in this id block.

### 2.4 E8-C1 (post-hit control)

```
OBSERVE 84021 84121 84031
QUERY 84021 84121 84031
ACT
```

A taught fact answered by hit; no guide is created. Expected
CHOICE 0. Verifies hits do not create guides in this block.

## 3. Frozen decision rule

Observation channel: the single "CHOICE <n>" line produced by the
one ACT event in each transcript. Extraction: grep '^CHOICE ' on
the transcript; each world must yield exactly one CHOICE line
(E8-K2 would fail otherwise). Equality criterion: byte-identical
(the frozen binary is deterministic; no distributional fallback).

Let CA be the CHOICE line of E8-A run 1 and CB the CHOICE line
of E8-B run 1 (runs 2 and 3 are byte-identical per E8-K2).

Frozen signatures:

- SIGNATURE-BANDWIDTH-SUFFICIENT: CA != CB as byte strings,
  replicated across all 3 runs of each world. Actions
  differentiate by guide content when the output channel can
  express the correct-action difference. Verdict: E8-BANDWIDTH.
  Reading per the task mapping: H2d confirmed as a contributing
  cause (output bandwidth is in the causal chain of whether
  content differences manifest).
- SIGNATURE-STILL-BLIND: CA == CB byte-identically, across all 3
  runs of each world. Actions identical despite sufficient
  bandwidth. Verdict: E8-STILL-BLIND. Reading per the task
  mapping: H2d killed as an excuse; H2a/H2c stand as the root
  cause of Cluster 2.

A mixed outcome (identical on some runs, differing on others)
fails E8-K2 determinism and voids the world pair rather than
supporting either signature.

Recorded design limitation: the white-box reading of the frozen
shim (read-only; no source edits) shows the ACT operator returns
the winning candidate's stored action code and guide nodes are
constructed with that code fixed, so the protocol-reachable
vocabulary is {0, 30}; the in-context vs aged manipulation
targets the candidate-selection stage. A differentiate outcome
therefore also bears on selection-stage content reaching (H2a's
scope), not only on output bandwidth. The verdict labels above
follow the frozen rule exactly; mechanistic interpretation is
reported separately in E8_RUN.md and does not alter the verdict.

## 4. Process bars

- E8-K1 (prereg ordering): PASS iff this prereg is committed alone
  before any E8 world is generated or any run executes; SHA-256
  re-verified unchanged at run time.
- E8-K2 (determinism): PASS iff all transcripts are byte-identical
  across 3 fresh-state runs within each world, and each
  transcript contains exactly one CHOICE line.
- E8-K3 (frozen binary): PASS iff freeze_shim2_bin and tnn2.zag
  match the section 0 hashes before the first run and after the
  last run.
- E8-K4 (seal integrity): PASS iff E8_MANIFEST.sha256 verifies all
  world files before execution.
- E8-K5 (block calibration): PASS iff E8-C0 yields CHOICE 0,
  E8-C1 yields CHOICE 0, and E8-A yields CHOICE 30 on all 3 runs
  each. Any deviation voids block calibration and the E8-A/E8-B
  comparison carries no verdict weight.
- E8-K6 (no leak / anti-smuggling): PASS iff the exact E8 id set
  returns zero matches in the frozen cognition sources
  (tnn2_build, core_freeze_tnn2_shim).
- K-C0A (zero new semantic cases): PASS iff (1) e8_worldgen.zag
  emits only the exact section 2 streams with no id-conditioned
  or value-conditioned branching; (2) the runner performs no
  transformation of transcripts and contains no logic keyed on
  world ids, subjects, relations, or CHOICE values beyond the
  byte comparison required by the section 3 decision rule;
  (3) audit greps over the harness sources are recorded in
  E8_RUN.md. A process-bar failure voids the affected world;
  K-C0A failure voids the lane result.

## 5. Execution and sealing

Tools (pure Zag, pinned znc; built only after this prereg freezes):
e8_worldgen.zag (streams from section 2; writes e8_worlds/).
Runner: shell script e8_run.sh that verifies binary hashes,
generates the manifest, and for each world runs 3 fresh-state runs
via `freeze_shim2_bin <world> <state.bin>` (exit 0 required, state
removed before each run), saving transcripts and per-run states to
e8_runs/ with sha256 records. Scoring: shell byte comparison of
the CHOICE lines per the section 3 rule. No Python anywhere.

A process-bar failure VOIDs the affected world. A calibration-gate
failure (E8-K5) VOIDs the comparison. There is no partial verdict.

## 6. No-patch-treadmill compliance

This is a discriminating experiment, not a repair. The outcome goes
back into the BATTERY-CLUSTER analysis as decided evidence for H2d.
No mechanism change is proposed on any outcome.

## 7. Criterion 0 status (binding)

C0-A through C0-D are NOT MET. This experiment probes a frozen
researcher-authored mechanism on fresh structures. No score here may
be described as L3, L3-adjacent, or progress toward L3. Report as
mechanism-targeted evidence only.
