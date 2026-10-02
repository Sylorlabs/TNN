# PREREG_POSTFREEZE.md -- Post-freeze sealed adversarial battery

Wave: wave-20261001-2321pdt, lane BATTERY.
Status: FROZEN DESIGN. This file is committed alone before any
post-freeze world is generated. Kill bars never move after freezing.

## 0. Freeze record and provenance

TNN-2 is frozen. No source edits are permitted during this battery.
The battery runs against the frozen binary:

- `tnn2.zag` SHA-256:
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
- `freeze_shim2_bin` SHA-256:
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
- Pinned znc SHA-256:
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef

This battery is the owner's standing order (highest priority): with
TNN-2 frozen, run a sealed adversarial battery on the three new
mechanisms: (a) runtime executable-graph construction,
(b) learner-originated uncertainty to guide to action,
(c) counterexample-driven revision. Worlds use the id block
60000-69999, disjoint from v3 (50000-59999) and from FW1-FW9.
No world is a trivial FW1-FW9 variant; each world's material
difference is stated. At least one world family per mechanism is
designed to be adversarial (try to break it, not confirm it).

Standing ruling: FW1-FW9 is a REGRESSION battery for TNN-2 only. A
9/9 establishes no broad generality and no L3. This post-freeze
battery is mechanism-targeted evidence only. No L3 claim on any
score (Criterion 0 not met; see section 8).

Adversary independence: the worker attests in NAMECHECK.md Step 0
that it has not authored mechanism-build or mechanism-repair code in
the previous two waves, and writes only inside its wave lane
directory.

## 1. Global constraints

PURE ZAG ONLY for all research logic. Shell only: invoke znc, run
binaries, git ops, move/copy files, sha256sum manifests.
Deterministic: each world is run 3 times from fresh state;
byte-identical transcripts required (PF-K2). No em-dashes in any
doc; check with check_no_dash.sh before commit. Commits local only
under docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY/; never push;
never git reset --hard; never rebase. Prereg committed alone first;
implementation in a separate commit (commit-order self-check).

## 2. World specifications

All streams are exact. QUERY (s,r,e) lines carry the oracle expected
value e (visible to the scorer only, never to the learner).

### 2.1 PF-A1: construction vs retrieval (adversarial to mechanism a)

Pits executable-graph construction against direct retrieval. A
retriever returns the wrong taught answer; a constructor builds the
P->Q composition and returns the right answer.

```
OBSERVE 60101 60601 60901
OBSERVE 60102 60601 60901
OBSERVE 60901 60602 60902
OBSERVE 60101 60609 60999
OBSERVE 60102 60609 60999
QUERY 60101 60609 60902
QUERY 60102 60609 60902
QUERY 60101 60601 60901
QUERY 60901 60602 60902
```

P maps 60101/60102 to 60901; Q maps 60901 to 60902. The direct
taught fact on the compose relation 60609 is 60999 (wrong). Probes
0-1: the composed answer is 60902; a retriever returns 60999.
Probes 2-3 (validity): direct retrieval of the taught P and Q
facts; must be hits, else the world failed to teach and is
WORLD-INVALID. Material difference from FW1-FW9 and v3: no prior
world pits a taught wrong answer against a constructed right answer
on the same probe.

### 2.2 PF-A2: selective composition with a distractor procedure (adversarial to mechanism a)

Tests whether construction (if it occurs) is selective. P->Q is the
valid composition; D is a distractor procedure sharing the subject
space but never part of a valid composition.

```
OBSERVE 60201 60611 60911
OBSERVE 60202 60611 60912
OBSERVE 60911 60612 60921
OBSERVE 60912 60612 60922
OBSERVE 60201 60613 60931
OBSERVE 60202 60613 60932
QUERY 60201 60619 60921
QUERY 60202 60619 60922
QUERY 60201 60629 60931
QUERY 60202 60629 60932
```

Probes 0-1: compose P(60611)->Q(60612) via the compose relation
60619. Probes 2-3: the distractor-compose relation 60629 is novel;
D was never part of a valid composition, so the correct answer is
the miss response (no spurious composition). The bar requires the
valid composition AND no spurious distractor composition. Material
difference: selectivity among procedures in the presence of a
distractor; no prior world tests composition when a distractor
procedure shares the subject space.

### 2.3 PF-B1: concurrent guides with selective resolution (adversarial to mechanism b)

Two uncertainties are live concurrently; one resolves. A
resolution-capable mechanism updates selectively; the frozen
mechanism's guides never resolve.

```
OBSERVE 60301 60701 60311
QUERY 60301 60701 60311
ACT
QUERY 60302 60701 60312
QUERY 60303 60701 60313
ACT
OBSERVE 60302 60701 60312
ACT
QUERY 60304 60701 60314
QUERY 60305 60701 60315
```

Baseline ACT after the hit (no guide). Two misses create two
concurrent guides. Pre-resolution ACT (both guides live). The
OBSERVE resolves the 60302 uncertainty only. Post-resolution ACT: a
selective mechanism changes its action (one guide remains); the
frozen mechanism repeats the stale action. Validity: the two miss
QUERYs yield the learner's own miss response M. Collateral: 2
engagement probes on novel keys. Material difference: concurrent
(not sequential) guides with partial resolution; v3 M2-W2 had a
single guide and full resolution.

### 2.4 PF-B2: guide flood (adversarial to mechanism b)

Three concurrent guides from three distinct uncertainties. A
content-sensitive mechanism discriminates; the frozen mechanism
emits its constant guide action three times.

```
QUERY 60401 60801 60411
QUERY 60402 60802 60412
QUERY 60403 60803 60413
ACT
ACT
ACT
QUERY 60304 60701 60314
QUERY 60305 60701 60315
```

Three misses (distinct subjects and relations) create three
concurrent guides with no intervening resolution. Three ACTs: the
bar requires three pairwise-distinct actions, each differing from
the declared null action N (measured per the v3 protocol from a
fresh-state baseline; carried as a scorer parameter). Validity: all
three miss QUERYs yield M. Collateral: 2 engagement probes. Material
difference: concurrent flood vs the sequential episodes of v3 M2-W3;
tests whether concurrency induces any discrimination.

### 2.5 PF-C1: contradiction of a derived fact (adversarial to mechanism c)

Contradicts the DERIVED 2-hop fact directly, without touching its
taught links. A general reviser reconciles the exception; the frozen
mechanism's revise_on_contradict reverts promoted graphs when a
link is contradicted, and may revert here too.

```
OBSERVE 60501 60901 60502
OBSERVE 60502 60902 60503
QUERY 60501 60909 60503
QUERY 60501 60909 60503
OBSERVE 60501 60909 60513
OBSERVE 60951 60960 60971
OBSERVE 60952 60960 60972
OBSERVE 60953 60960 60973
OBSERVE 60954 60960 60974
QUERY 60501 60909 60513
QUERY 60501 60901 60502
QUERY 60502 60902 60503
```

The promotion QUERYs build the 2-hop chain 60501->60502->60503 for
the novel relation 60909. The contradiction OBSERVE (60501,60909,
60513) targets the DERIVED fact, not a taught link. Four
distractors intervene (recency-proof). Bar probe: 60513 (the
exception is honored). Validity: the promotion probes return 60503;
the taught-link probes return 60502/60503. Material difference:
contradicting a derived fact vs contradicting a taught link (FW5,
v3 M3-W2/W3). This is the adversarial core: it attacks the
revision operator at the point where derivation and observation
conflict.

### 2.6 PF-C2: cross-relation revision transfer (adversarial to mechanism c)

Tests whether a revision transfers across relations. A per-key
patcher revises only the contradicted relation; a general reviser
might transfer the shift pattern.

```
OBSERVE 60601 61001 60611
OBSERVE 60602 61001 60612
OBSERVE 60603 61001 60613
OBSERVE 60701 61002 60711
OBSERVE 60702 61002 60712
OBSERVE 60703 61002 60713
QUERY 60601 61009 60611
QUERY 60701 61019 60711
OBSERVE 60601 61001 60621
OBSERVE 60602 61001 60622
OBSERVE 60951 60960 60971
OBSERVE 60952 60960 60972
QUERY 60601 61009 60621
QUERY 60701 61019 60721
QUERY 60603 61001 60613
QUERY 60703 61002 60713
```

Laws: 61001 maps 6060x to 6061x (+10); 61002 maps 6070x to 6071x
(+10). Promotion QUERYs on the novel relations 61009/61019.
Systematic contradiction on 61001 (+20 shift: 60621/60622).
Distractors. Bar probes: (60601,61009) expects 60621 (the revised
relation); (60701,61019) expects 60721 (transfer: the +20 shift
applied to the analogous relation). Validity: promotion probes;
uncontradicted instances (60603, 60703) retain the original law.
Material difference: cross-relation transfer; no prior world tests
whether revision generalizes across relations.

## 3. Frozen kill bars PF-K1 through PF-K6

- PF-K1 (process: prereg ordering). PASS iff this file's SHA-256 was
  recorded before any post-freeze world file was created and the
  file is unmodified thereafter.
- PF-K2 (process: determinism). PASS iff all 6 world transcripts are
  byte-identical across 3 fresh-state runs.
- PF-K3 (process: frozen binary). PASS iff freeze_shim2_bin and
  tnn2.zag match the section 0 hashes before and after the battery,
  and zero modifications under the frozen cognition paths.
- PF-K4 (process: seal integrity). PASS iff the manifest verifies
  and grep of 60000-69999 over the frozen sources is clean.
- PF-K5 (mechanism bars). Per-world bars:
  - PF-A1: PASS iff probes 0-1 are both 60902 (construction beats
    retrieval). Validity: probes 2-3 are both hits (the taught P
    and Q facts are retrievable), else WORLD-INVALID.
  - PF-A2: PASS iff probes 0-1 are both correct (60921/60922) AND
    probes 2-3 are both the miss response (no spurious distractor
    composition).
  - PF-B1: PASS iff the post-resolution ACT differs from the
    pre-resolution ACT. Validity: both miss QUERYs yield M, else
    WORLD-INVALID. N is the baseline ACT action.
  - PF-B2: PASS iff the three ACT actions are pairwise distinct and
    each differs from N. Validity: all three misses yield M, else
    WORLD-INVALID.
  - PF-C1: PASS iff the bar probe returns 60513. Validity: promotion
    probes return 60503 and taught-link probes are correct, else
    WORLD-INVALID.
  - PF-C2: PASS iff the revised-relation probe returns 60621 AND the
    transfer probe returns 60721. Validity: promotion probes correct
    and uncontradicted instances retain the original law, else
    WORLD-INVALID.
- PF-K6 (process: no-leak). PASS iff the audit reports zero leaks.

## 4. Predicted outcomes (recorded before execution)

- PF-A1: predicted FAIL. The frozen mechanism retrieves the taught
  60999 (or misses); it does not construct P->Q.
- PF-A2: predicted FAIL on the composition probes (0/2); the
  distractor probes return the miss response (no composition to be
  spurious). The world is adversarial in that it demands selective
  composition under a distractor; the mechanism fails the positive
  demand.
- PF-B1: predicted FAIL. Pre=post=30 (stale guide persists;
  selective resolution absent).
- PF-B2: predicted FAIL. Actions 30,30,30 (no discrimination under
  concurrency).
- PF-C1: predicted FAIL. The contradiction of the derived fact
  triggers the revert path (as in v3 M3-W3); the bar probe returns
  the stale 60503, not 60513. This is the adversarial prediction:
  the mechanism's revision operator actively destroys the derived
  structure instead of honoring the exception.
- PF-C2: predicted FAIL. The revised-relation probe returns 60621
  (per-key patch works), but the transfer probe returns 60711
  (original law; no cross-relation transfer).

## 5. Calibration

Each world carries a degenerate control (must FAIL the bar) and a
competent control (must PASS the bar), implemented in pure Zag as
driver-level responders. If a degenerate control passes or a
competent control fails, the world is WORLD-VOID (battery defect);
no mechanism verdict is drawn from it.

- PF-A1: D = per-key latest responder (returns 60999). C =
  composer (builds P->Q, returns 60902; validity probes via the
  taught mappings).
- PF-A2: D = per-key latest (0/2 composition). C = selective
  composer (composes P->Q, retrieves D directly).
- PF-B1: D1 = constant action; D2 = stale action. C = selective
  resolver (changes action when one of two guides resolves).
- PF-B2: D = constant action. C = distinct actions per concurrent
  guide.
- PF-C1: D = global-recency responder (returns a distractor object).
  C = exception-honoring reviser (stores the derived-fact
  contradiction as an override).
- PF-C2: D = per-key latest (no transfer). C = transfer reviser
  (applies the observed shift to the analogous relation).

## 6. Execution and sealing

Tools (pure Zag, pinned znc; built after this prereg freezes):
pf_worldgen.zag (streams from section 2; manifest),
pf_sealed_score.zag (1:1 QUERY/ANSWER scoring plus per-world bars),
pf_controls.zag (section 5 policies), pf_audit_noleak.zag (PF-K6).
Each world runs 3 times from fresh state via freeze_shim2_bin;
transcripts saved; sha256 manifest; anti-smuggling grep before
execution. Sealing: this prereg committed alone; worlds generated
after; no post-freeze edits to sealed files (a defect voids the
world; replacement needs a new prereg section).

## 7. Verdicts

- Mechanism (a) SURVIVES-SEALED iff PF-A1 and PF-A2 PASS; else FAILS.
- Mechanism (b) SURVIVES-SEALED iff PF-B1 and PF-B2 PASS; else FAILS.
- Mechanism (c) SURVIVES-SEALED iff PF-C1 and PF-C2 PASS; else FAILS.
A process-bar failure VOIDs the battery. A calibration-gate failure
VOIDs the affected world. There is no partial-generality verdict.

## 8. Criterion 0 status (binding)

This battery probes frozen researcher-authored mechanisms on fresh
structures. C0-A through C0-D are NOT MET. No score here may be
described as L3, L3-adjacent, or progress toward L3. Report as
mechanism-targeted evidence only.
