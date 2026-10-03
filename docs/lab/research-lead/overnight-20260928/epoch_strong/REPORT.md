# REPORT: EPOCH-STRONG

## Verdict: all 11 kill bars green (ES-R1, ES-S1, ES-B1, ES-B2, ES-B3, ES-B4, ES-B5, ES-B6, ES-K1, ES-H1)

Non-ledger task. Branch `tnn-native-lab`, lane
`docs/lab/research-lead/overnight-20260928/epoch_strong/`, file prefix
`es_`. All commits local, never pushed.

This is a null result with teeth, preregistered as such. The probe
gave the learner the exact staleness-failure experience that should
motivate inventing versioning, twice, with the researcher-designed
stamping removed. The learner detected the failures (via the
checksum, off the live path), recovered from them (via the
pre-existing reactive RETRY safety net), installed no new tracking,
and changed no staleness-gating policy. Every invention signature
the bars were built to detect is absent. The honest answer to the
task's question is: premature. The six missing capabilities named in
the prereg (A2.1-A2.6) stand, each verified against the frozen
source and the run trace.

## What was built

Additive deltas over le_*: es_base.zag is le_base.zag with the
stamping removed (`w_epoch_bump` a documented no-op, never invoked;
`fact_add`/`fact_set_obj` mutate without stamping; `w_epoch_get`
kept to sample the dead cell); es_world/module/learn.zag are
byte-copies of le_* (the learner's machinery is unchanged, so the
probe measures it, not a redesign); es_main.zag is le_main.zag with
Act 5 (S14) replaced by the ES battery (ES-A setup, ES-B N1 failure
with the proactive gate armed but blind, ES-C adversarial silent
staleness, ES-D second exposure, ES-E content-neutral mutation
discriminator, ES-F summary). No new state cells.

## The honest answers

**Can the learner create the stamping operation from experience?**
No, not with this machinery. ES-B gave it the N1 stale-index failure
with the proactive flag armed: the gate computed mask 0 (ES-AUTO
entry_mask=0), the stale A2 index produced two disagreeing attempts,
and the learner fell back to the reactive RETRY path (2 RETRYs,
contract invalidation, generic third attempt). ES-D repeated the
identical failure after that experience: the failure signature is
unchanged on every discriminating field (ES-B4). ES-C showed a
content-changing mutation going completely unnoticed by the live
gate (ver_stale=0, mask 0, zero RETRYs, agree=1 on a stale index).
ES-E showed a mutation event leaving zero trace in any learner
signal (e0=0 e1=0, all three spec probes 0). At no point did any
learner code path allocate a cell, install an op body, or revise the
staleness-gating policy. The learner's write vocabulary during the
whole battery is fixed slots only (ES-B6).

**What would it take?** The six preregistered capabilities, each
necessary: (1) learner-allocated persistent state with
learner-chosen semantics; (2) learner-created operation bodies from
the generic ISA (the runtime executable-graph construction
mechanism under test in the TNN-2 post-freeze lanes, not present
here); (3) mutation-path interception (a learner-writable hook on
the world interface); (4) failure attribution to a missing
mechanism, not just revision of existing contracts; (5)
probationary validation of invented mechanisms before gating
behavior on them; (6) mutation-event observability (the learner is
not on the mutation path at all: zero fact_add/fact_set_obj calls
in es_learn.zag, verified by grep). Post-hoc observation, not a
frozen claim: a seventh gap is motivation. The cost pressure that
should favor a cheap O(1) counter over the O(nf) checksum exists
structurally, but the learner has no cost-deliberation machinery;
it does not select mechanisms by cost.

**Does it need to experience staleness failures first? What is the
minimal signal?** Failure experience is necessary but not
sufficient; the blocker is capability, not signal. The minimal
signal has three components: (i) the unexplained-staleness
signature (stale answers while the tracked version says fresh and
the checksum says stale): supplied in full by ES-B/C, and the
machinery could not use it; (ii) observable mutation events:
absent by architecture and not suppliable here; a future attempt
must make the learner the mutator or give it a mutation-event
stream; (iii) a cost/failure pressure favoring the invention: see
the seventh gap above.

**L2 or L3?** The preregistered classification stands. A
counter-plus-bump-op constructed from the generic ISA in response
to staleness failures, with versioning not researcher-enumerated,
would be L2 structural learning at minimum, and L3 only with C0-A
through C0-D (runtime-defined semantics in learner-created state;
open structural form; unforeseen forms under sealed worlds;
cognitive reuse beyond the one bug). Nothing here reaches either;
there is not even a precursor behavior to classify.

## Results per bar

- ES-R1 regression: PASS. es_run1.txt lines 1-97 byte-identical to
  le_run1.txt lines 1-97 (diff empty). Acts 1/2/S11 untouched.
- ES-S1 no versioning installed: PASS. `grep -c "w_epoch_bump(S);"
  es_base.zag` is 0; `grep -c "931" es_main.zag` is 0. The only
  epoch writer in LEARNER-EPOCH is gone; the cell is write-dead.
- ES-B1 version signal dead: PASS. ES-B probe exactly
  `ES-PROBE nf_stale=0 ck_stale=7 ver_stale=0`.
- ES-B2 proactive gate blind: PASS. ES-B block has exactly 2 RETRY
  lines; ESQ0 three Q lines with (agree=0,vers=2), (agree=0,vers=2),
  (agree=1,vers=0); `ES-AUTO entry_mask=0`. Without the researcher
  signal the armed proactive machinery contributes nothing: the
  trace is the reactive path.
- ES-B3 silent adversarial staleness: PASS. ES-C probe exactly
  `ES-PROBE nf_stale=0 ck_stale=7 ver_stale=0`; ESQ0A a single Q
  line agree=1 vers=2; zero RETRY lines in ES-C. The world changed,
  the checksum knows, the live gate sees nothing, the learner
  proceeds on a stale index unaware.
- ES-B4 no learning from failure experience: PASS. ES-D matches
  ES-B on every discriminating field: identical probe values,
  exactly 2 RETRY lines, ESQ0B (agree,vers) sequence equals ESQ0's,
  `ES-AUTO entry_mask=0`. The staleness gate is hardcoded
  (spec_ver_stale compare); experience changed nothing.
- ES-B5 neutral-mutation discriminator: PASS. `ES-NEUTRAL e0=0 e1=0
  ck_same=1 nf_same=1` exactly; `ES-PROBE2 nf_stale=0 ck_stale=0
  ver_stale=0` exactly; ESQd2 single Q line agree=1 vers=2. A
  mutation event occurred; zero learner signals responded. Contrast
  LE-B4, where the researcher-designed epoch advanced on a
  learner-op mutation: the strong-sense signature (mutation-event
  tracking) is absent here, and no other learner cell exhibits it.
- ES-B6 invention audit: PASS. `grep -c "931" es_learn.zag` is 4
  (three specialize recording reads plus spec_ver_stale; zero
  writes); `grep -c "fact_add\|fact_set_obj" es_learn.zag` is 0.
  The learner has no write path to any version cell, is not on the
  mutation path, and cannot observe mutation events.
- ES-K1 cost of no versioning: PASS. `ES-VERDICT blind_total=1152
  secondexp_total=1152`; 1152 > 984 (LEARNER-EPOCH's proactive
  total with working stamping). The blind armed gate pays exactly
  the reactive-scale cost (1152 = LE's reactive total), and the
  second exposure costs the same as the first: no learning dividend
  whatsoever.
- ES-H1 toolchain/hygiene: PASS. Safebin for all build/run/verify
  commands; pure Zag; pinned znc; prereg committed alone before
  implementation (8b6b4ddcd); 3/3 byte-identical (sha256
  f4699c5babded63cb0ee2fa75a0ad45f922c0f5a325f5a59ae1876cb516d875c),
  stderr empty, exit 0; zero em/en dash bytes in authored files;
  86 A0102 note lines, same as le_compile.txt; no world literals in
  new executable code (the 601/603/813 hits in the battery region
  are variable/function names r601x/o601x/r603x/mk_goal813_E0 with
  runtime-derived values, same discipline as LE-H1).

SUMMARY-EPOCHSTRONG (frozen, reproduced exactly):
`agree=28 plans_built=5 plans_loaded=30 trials=12 declines=0 cs=2104
cg=3864 hook=1 covdc=0,0,0 steps=2688`.

## Recommendation

Do not attempt learner-created stamping in this lane again until
the prerequisite machinery exists. The minimal architecture delta
for a future EPOCH-STRONG-2: (a) runtime executable-graph
construction available to the learner (consumer of the TNN-2
post-freeze mechanism, not a reimplementation here); (b) the world
mutation interface dispatching through a learner-writable hook
table; (c) a learner-allocatable state region with a semantics
registry; (d) failure attribution that can posit a missing
detector from the unexplained-staleness signature (ver-says-fresh
+ checksum-says-stale + disagreeing answers); (e) probationary
validation of the hypothesized tracker against the checksum before
it gates re-specialization; (f) the learner as mutator or a
mutation-event stream so component (ii) of the minimal signal
exists. Until then, operation-owned stamping (LEARNER-EPOCH's weak
sense) remains the adopted discipline, and the strong sense stays
an explicitly open frontier, not a near-term experiment.

## Follow-ups (not claimed here)

1. EPOCH-STRONG-2 once (a)-(f) exist: the learner invents the
   stamping op from the ES-B experience; bars discriminate
   learner-created vs researcher-placed by source audit plus the
   ES-E neutral-mutation signature.
2. Content-change-only epoch, two-op enforcement, SI follow-ups 2-4
   (checksum audit policy, cost at scale, proactive placement):
   still open, untouched by this probe.

## Commits (local only)

- 8b6b4ddcd (prereg + namecheck, alone, pre-implementation)
- (implementation: es_*.zag sources + es_build.sh)
- (artifacts: es_full.zag, es_bin, es_compile.txt, es_run1/2/3.txt/err)
- (this report)

## Artifacts

- `es_base/world/module/learn.zag`: sources (base = le_base minus
  stamping; world/module/learn byte-copies of le_*)
- `es_main.zag`: le_main with Act 5 (S14) replaced by the ES
  battery (ES-A through ES-F)
- `es_build.sh`: build script
- `es_full.zag`, `es_bin`
- `es_run1/2/3.txt`: 3/3 byte-identical (146 lines), stderr empty
- `es_compile.txt`: clean compile log (86 A0102 note lines, same
  count as le_compile.txt)
