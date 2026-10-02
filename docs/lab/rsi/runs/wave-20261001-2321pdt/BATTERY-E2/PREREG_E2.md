# PREREG_E2.md -- Single-guide content discrimination (tests H2a vs H2b)

Wave: wave-20261001-2321pdt, lane BATTERY-E2.
Status: FROZEN DESIGN. This file is committed alone before any E2
world is generated or any run is executed. Kill bars never move
after freezing.

## 0. Freeze record and provenance

E2 is the second-priority discriminating experiment from the
BATTERY-CLUSTER analysis
(docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-CLUSTER/CLUSTER_ANALYSIS.md),
testing H2a (absent content channel, guide-to-ACT interface) against
H2b (concurrency collapse, guide store under concurrency) for Cluster 2
(GUIDE CONTENT DECOUPLING). The post-freeze battery and v3 validation
showed constant CHOICE 30 under concurrent guides (PF-B1 pre=post=30,
PF-B2 30,30,30, v3 M2 0/8 informant routing); concurrency was never
separated from content, so H2a vs H2b is undecided.

Runs target the frozen TNN-2 binary, no source edits:

- `tnn2.zag` SHA-256:
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
- `freeze_shim2_bin` SHA-256:
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
- Pinned znc SHA-256:
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef

Binary hashes are verified before the first run and after the last
(E2-K3). Frozen sources are read-only; the anti-smuggling grep
(E2-K6) runs before execution.

## 1. Design

Two different single uncertainties, each in its own fresh run, one
ACT each. No concurrency anywhere. Guide content A (world E2-A) and
guide content B (world E2-B) name different missing facts and carry
different resolution-state context:

- E2-A: a bare single miss, then ACT. Content A = uncertainty about
  fact (81001, 81101). No other state.
- E2-B: one taught (resolved) fact, then a single miss on a different
  subject and relation, then ACT. Content B = uncertainty about fact
  (82001, 82101) with a resolved fact (82002, 82102, 82012) present
  in state.

At ACT time both worlds hold exactly one live guide, so the
presence bit is identical across runs; only guide content differs.
Material difference from PF-B1/PF-B2 and v3 M2: those worlds never
presented single guides in isolation with distinct content; every
prior constant-30 observation was under concurrency or sequential
episodes.

E2-D (degenerate control): a single ACT on empty state, no guide.
Verifies the presence bit reads in this id block (expected CHOICE 0,
matching PF-B1's guide-absent baseline).

Id blocks 81000-81999 (A), 82000-82999 (B), 83000-83999 (D) are
disjoint from v3 (50000-59999), PF (60000-69999), and all other
cognition lanes; the E2 id set returns zero matches in the frozen
cognition sources (verified pre-freeze, exit 1).

## 2. World specifications (exact streams)

QUERY lines carry the oracle expected value e per the PF protocol
(scorer-side only; the observation channel below is the ACT line,
which carries no answer path, so the oracle value cannot be matched
on the ACT channel).

### 2.1 E2-A (content A)

```
QUERY 81001 81101 81011
ACT
```

The miss creates one guide for the uncertainty about (81001, 81101);
the single ACT is the observation.

### 2.2 E2-B (content B)

```
OBSERVE 82002 82102 82012
QUERY 82001 82101 82011
ACT
```

The OBSERVE stores a resolved fact; the miss creates one guide for
the uncertainty about (82001, 82101), a different missing fact on a
different relation with different resolution-state context; the
single ACT is the observation.

### 2.3 E2-D (degenerate control)

```
ACT
```

No guide exists. Expected CHOICE 0.

## 3. Frozen decision rule

Observation channel: the single "CHOICE <n>" line produced by the
one ACT event in each transcript. Extraction: grep '^CHOICE ' on the
transcript; each world must yield exactly one CHOICE line
(E2-K2 would fail otherwise). Equality criterion: byte-identical
(the frozen binary is deterministic, so byte-identical is available;
no distributional fallback).

Frozen signatures:

- SIGNATURE-CONTENT-BLIND: CHOICE(E2-A) == CHOICE(E2-B)
  byte-identically, across all 3 runs of each world. The
  constant-guide story holds even without concurrency: guide
  content has no write path into action selection. Confirms H2a
  as the root cause of Cluster 2; kills H2b.
- SIGNATURE-CONTENT-SENSITIVE: CHOICE(E2-A) != CHOICE(E2-B) as
  byte strings, replicated across all 3 runs. The constant-30
  behavior collapses to a concurrency phenomenon: content does
  reach ACT for a single guide. Kills H2a; supports H2b and
  redirects the cluster (E7 sequential two-guide world becomes
  the next discriminating step per the cluster analysis).

Verdict names: E2-CONTENT-BLIND or E2-CONTENT-SENSITIVE. A mixed
outcome (identical on some runs, differing on others) fails E2-K2
determinism and voids the world pair rather than supporting either
signature.

Recorded design limitation: if SIGNATURE-CONTENT-SENSITIVE is
observed, a follow-up must rule out oracle-value echo (the QUERY
carries e); the ACT channel has no answer path, so echo is
structurally excluded, but the limitation is recorded for the
adversary.

## 4. Process bars

- E2-K1 (prereg ordering): PASS iff this prereg is committed alone
  before any E2 world is generated or any run executes; SHA-256
  re-verified unchanged at run time.
- E2-K2 (determinism): PASS iff all transcripts are byte-identical
  across 3 fresh-state runs within each world, and each transcript
  contains exactly one CHOICE line.
- E2-K3 (frozen binary): PASS iff freeze_shim2_bin and tnn2.zag
  match the section 0 hashes before the first run and after the
  last run.
- E2-K4 (seal integrity): PASS iff E2_MANIFEST.sha256 verifies all
  world files before execution.
- E2-K5 (block calibration): PASS iff E2-D yields CHOICE 0 on all
  3 runs. A different value voids block calibration (the
  presence-bit baseline does not hold in this id block) and the
  E2-A/E2-B comparison carries no verdict weight.
- E2-K6 (no leak / anti-smuggling): PASS iff the exact E2 id set
  returns zero matches in the frozen cognition sources
  (tnn2_build, core_freeze_tnn2_shim).
- K-C0A (zero new semantic cases): PASS iff (1) e2_worldgen.zag
  emits only the exact section 2 streams with no id-conditioned
  or value-conditioned branching; (2) the runner performs no
  transformation of transcripts and contains no logic keyed on
  world ids, subjects, relations, or CHOICE values beyond the
  byte comparison required by the section 3 decision rule;
  (3) audit greps over the harness sources are recorded in
  E2_RUN.md. A process-bar failure voids the affected world;
  K-C0A failure voids the lane result.

## 5. Execution and sealing

Tools (pure Zag, pinned znc; built only after this prereg freezes):
e2_worldgen.zag (streams from section 2; writes e2_worlds/).
Runner: shell script e2_run.sh that verifies binary hashes,
generates the manifest, and for each world runs 3 fresh-state runs
via `freeze_shim2_bin <world> <state.bin>` (exit 0 required, state
removed before each run), saving transcripts and per-run states to
e2_runs/ with sha256 records. Scoring: shell byte comparison of
the CHOICE lines per the section 3 rule. No Python anywhere.

A process-bar failure VOIDs the affected world. A calibration-gate
failure (E2-K5) VOIDs the comparison. There is no partial verdict.

## 6. No-patch-treadmill compliance

This is a discriminating experiment, not a repair. The outcome goes
back into the BATTERY-CLUSTER analysis as decided evidence for H2a
vs H2b. No mechanism change is proposed on any outcome.

## 7. Criterion 0 status (binding)

C0-A through C0-D are NOT MET. This experiment probes a frozen
researcher-authored mechanism on fresh structures. No score here may
be described as L3, L3-adjacent, or progress toward L3. Report as
mechanism-targeted evidence only.
