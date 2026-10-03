# PREREG: EPOCH-STRONG (frozen)

Non-ledger task. Lane
`docs/lab/research-lead/overnight-20260928/epoch_strong/`, file prefix
`es_`. Branch `tnn-native-lab`, commits local only, never pushed.

## 1. Task

LEARNER-EPOCH achieved 9/9 green for operation-owned stamping (the
weak sense of overnight priority 5): the mutation itself stamps the
epoch, but the epoch cell, its monotonic semantics, the choice of
mutation events as the signal, and the placement of the bump are all
researcher-designed. Its REPORT froze the honest verdict in advance:
"the learner did not invent versioning ... the strong sense, the
learner creating that operation body itself from experience, is not
demonstrated."

This experiment investigates the strong sense: can the learner create
the stamping operation from experience? The design is a
preregistered capability-gap probe, not a demonstration attempt:

- REMOVE the researcher-designed stamping (no versioning installed:
  `w_epoch_bump` becomes a documented no-op, never invoked; the epoch
  cell stays 0 forever).
- Give the learner the exact staleness-failure experience that should
  motivate invention: the N1 reorder with the proactive gate armed
  (twice), plus the adversarial in-place mutation, plus a
  content-neutral mutation discriminator.
- Freeze kill bars that discriminate presence vs absence of every
  invention signature: failure detection, recovery, behavioral change
  after failure experience, mutation-event tracking, and a static
  audit of the learner's write vocabulary and mutation-path position.

Writing a learner "invention" in Zag source would be the weak sense
one level removed (researcher-designed again). The only honest
experiment is to create the conditions for invention and measure what
the current machinery does with them.

## 2. Frozen design answers (before implementation)

**A1: what is the strong sense, exactly?** The learner, from
experience of staleness failures, creates the stamping operation
itself: it allocates a persistent cell, assigns it mutation-counter
semantics, composes an operation body ("on mutation, advance the
counter") from generic machinery, and attaches it to the mutation
path. No researcher-designed epoch cell, no researcher-placed bump,
no researcher-chosen signal.

**A2: what would it take? Capability decomposition (frozen).** Six
capabilities the current learner does not have, each necessary:

1. Learner-allocated persistent state with learner-chosen semantics.
   The L/S layouts are frozen; the learner fills researcher-defined
   slots (indexes, plans, contracts, stats). Nothing in the learner's
   write vocabulary allocates a new cell or assigns new semantics.
2. Learner-created operation bodies. Every op body (fact_add,
   specialize_*, spec_ensure_fresh, compose) is researcher-written;
   the learner never emits executable structure. Per the 2026-09-30
   protected-core ISA ruling, the prerequisite is the generic ISA
   plus EXECUTE exposed for runtime executable-graph construction
   (the TNN-2 post-freeze mechanism under test in other lanes, not
   present here).
3. Mutation-path interception: a hook or dispatch table the learner
   can write, so "on mutation" behavior can be attached. fact_add is
   a fixed researcher body with no indirection.
4. Failure attribution to a MISSING mechanism. SELFTRIG invalidates
   and revises existing contracts; it never posits a new detector or
   structure. The ES-B experience (stale answer, version-says-fresh,
   checksum-says-stale) must map to "my mutation tracking is absent",
   not just "the routing contract was wrong".
5. Probationary validation of invented mechanisms: shadow-testing a
   hypothesized tracker ("does the new counter predict the staleness
   the checksum sees?") before gating behavior on it.
6. Mutation-event observability. The learner never mutates the world
   and is not notified of mutations. Grep-verified on the frozen
   LEARNER-EPOCH source: zero `fact_add`/`fact_set_obj` calls in
   le_learn.zag, zero writes to cell 931 (4 reads only). The learner
   is not on the mutation path, so it cannot even observe the events
   it would stamp.

**A3: does it need to experience staleness failures first? What is
the minimal signal?** Failure experience is necessary but not
sufficient; the blocker is capability, not signal. The minimal signal
for inventing a mutation counter has three components: (i) the
unexplained-staleness signature (stale answers while the tracked
version says fresh and the checksum says stale); (ii) observable
mutation events (the learner must see the events it would track);
(iii) a cost or failure pressure favoring a cheap O(1) gate over the
O(nf) checksum. This probe supplies (i) in full (ES-B/C/D) and tests
whether the existing machinery can use it. Component (ii) is absent
by architecture (audit bar ES-B6). Predicted: the machinery detects
(via checksum) and recovers (via the reactive RETRY path) but
installs nothing and changes no gating policy.

**A4: L2 vs L3 classification (frozen).** If a learner with
capabilities A2.1-A2.6 constructed a monotonic counter plus
bump-on-mutate op from the generic ISA in response to staleness
failures, with versioning not enumerated by the researcher, that is
L2 structural learning at minimum. It is L3 only if it also meets
Criterion 0: runtime-defined semantics in learner-created persistent
state with only generic machinery in source (C0-A); open structural
form, never chosen from a finite researcher-enumerated family
(C0-B); unforeseen forms under sealed post-freeze worlds (C0-C);
cognitive reuse beyond the immediate bug (C0-D). A one-off counter
for one bug is L2+; versioning as a reusable invented primitive is
L3. This probe claims neither; it tests for precursor behaviors.

**A5: why a null-result probe?** Because a positive demonstration is
not constructible honestly in this lane: any "invention" written in
Zag is researcher code. The discriminating question is whether the
current machinery shows ANY invention signature when given the
motivating experience. The bars are framed to detect presence; the
prediction is absence, and the report will name exactly which
capability blocks each signature.

**A6: the ES-E discriminator rationale (frozen).** A content-neutral
mutation (same-value in-place write) is unobservable to every
content-based signal: nf unchanged, checksum unchanged,
content-epoch unchanged. Only a mutation-EVENT tracker (a
conservative counter, the strong-sense signature) responds to it.
LEARNER-EPOCH's researcher-designed epoch did respond (LE-B4:
e2 == e1+1 on a learner-op add). ES-B5 tests whether ANY learner
signal responds; predicted none. This separates "tracks mutation
events" (strong sense) from "tracks content" (everything the learner
currently has).

## 3. Implementation (additive deltas over le_*, frozen)

- es_base.zag: le_base.zag with the stamping removed.
  `w_epoch_bump(S)` becomes a documented no-op ("stamping disabled:
  no versioning installed in this lane"); `fact_add` and
  `fact_set_obj` no longer call it (the mutation happens; nothing
  stamps). `w_epoch_get(S)` is kept so stage code can sample the dead
  cell for the ES-E discriminator. Nothing else in base changes.
- es_world.zag: byte-copy of le_world.zag (setup_world* already
  thread S; they call fact_add, which no longer stamps).
- es_module.zag: byte-copy of le_module.zag.
- es_learn.zag: byte-copy of le_learn.zag. The learner still records
  sg(S,931) at specialize time and spec_ver_stale still compares it:
  it now reads a dead signal (always 0). No learner code changes at
  all; the probe measures the unchanged machinery under the removed
  signal.
- es_main.zag: le_main.zag with Act 5 (the S14 block) replaced by the
  ES battery below. Everything before Act 5 is byte-identical, so
  Acts 1/2/S11 output is unchanged.
- New state cells: none. S+930, S+931, L+14020, L+14036, L+14040
  reused with the same roles.
- es_build.sh: assemble es_full.zag from the five parts, compile with
  the pinned znc. Pure shell + znc.

### ES-A SETUP

setup_worldA(S2,A); specialize_ret/vfy/cnt (fresh; records epoch 0,
checksum, nf 56). Print `ES-SETUP specworld=A liveworld=A`. Derive
r601x, o601x, r603x, tLE, gLE, GSLE exactly as LE S14A did
(runtime-derived; no world literals).

### ES-B N1 FAILURE, PROACTIVE GATE ARMED BUT BLIND

setup_worldA2(S2,A); specialize_ret/vfy/cnt (records A2 state);
setup_worldA(S2,A) restore (no stamp: nothing stamps in this lane).
Print the probe `ES-PROBE nf_stale=<m> ck_stale=<m> ver_stale=<m>`.
Snapshot cs/cg/steps AFTER the probe. ss(S2,930,1). Nine queries
ESQ0..ESQ8 on GSLE (okind 2). Print `ES-AUTO entry_mask=<m>` from
L+14020. ss(S2,930,0). Print `ES-COST arm=proactive-blind q=<q>
steps=<s> total=<t>`; stash total at L+14036.

### ES-C ADVERSARIAL SILENT STALENESS

setup_worldA(S2,A); specialize_ret/vfy/cnt (fresh). Find the first
two facts with rel == r603x (runtime-derived mj0, mj1); read fact
mj1's object mo1; call fact_set_obj(S2,A,mj0,mo1) (mutation happens;
nothing stamps). nf stays 56; the (601,621) answer is untouched.
Print `ES-MUTATE nf=<n> dup_at=<i> from=<j>`. Print the ES-PROBE
line. ss(S2,930,1); one query ESQ0A; print ES-AUTO; ss(S2,930,0).
The gate sees mask 0 and does nothing; the learner proceeds on a
stale index unaware the world changed.

### ES-D SECOND EXPOSURE (the learning test)

Repeat ES-B's N1 sequence exactly (setup_worldA2, specialize x3,
setup_worldA restore, probe, snapshot, nine queries ESQ0B..ESQ8B
with S+930=1, ES-AUTO, ES-COST arm=second-exposure stashed at
L+14040). Tests whether the ES-B/ES-C failure experience changed
the learner's staleness gating. The gate is hardcoded
(spec_ver_stale compare), so the prediction is an unchanged failure
signature.

### ES-E CONTENT-NEUTRAL DISCRIMINATOR

setup_worldA(S2,A); specialize_ret/vfy/cnt (fresh). Sample e0 =
w_epoch_get(S2); ck0 = world_ck(L2,A); nf0 = get32(A,0). One query
ESQd1 (agree expected). Read fact 0's object o0; call
fact_set_obj(S2,A,0,o0): a mutation event with zero content change.
Sample e1 = w_epoch_get(S2); ck1 = world_ck(L2,A); nf1. Print
`ES-NEUTRAL e0=<e0> e1=<e1> ck_same=<0/1> nf_same=<0/1>`. Print
`ES-PROBE2 nf_stale=<m> ck_stale=<m> ver_stale=<m>` (all three spec
signals after the neutral mutation). One query ESQd2 (agree
expected: the mutation left no trace any signal can see).

### ES-F SUMMARY

Print `ES-VERDICT blind_total=<B> secondexp_total=<D>` from the
stashed arm totals, then SUMMARY-EPOCHSTRONG with the standard
fields (agree, plans_built, plans_loaded, trials, declines, cs, cg,
hook, covdc, steps).

## 4. Frozen kill bars

- ES-R1 (regression, additive-only): es_run1.txt lines 1-97
  byte-identical to le_run1.txt lines 1-97 (Acts 1/2/S11).
- ES-S1 (no versioning installed): `grep -c "w_epoch_bump(S);"
  es_base.zag` is 0 (the bump is never invoked); `grep -c "931"
  es_main.zag` is 0 (stage code never names the cell; it samples via
  w_epoch_get only). The only epoch writer in LEARNER-EPOCH is gone.
- ES-B1 (version signal dead): the ES-B ES-PROBE line is exactly
  `ES-PROBE nf_stale=0 ck_stale=7 ver_stale=0`.
- ES-B2 (proactive gate blind): the ES-B block has exactly 2 RETRY
  lines; ESQ0 appears 3 times with (agree=0,vers=2), (agree=0,vers=2),
  (agree=1,vers=0); `ES-AUTO entry_mask=0`. The proactive arm
  degenerates to the reactive path: without the researcher signal
  the learner's proactive machinery contributes nothing.
- ES-B3 (silent adversarial staleness): the ES-C ES-PROBE line is
  exactly `ES-PROBE nf_stale=0 ck_stale=7 ver_stale=0`; ESQ0A is a
  single Q line with agree=1 vers=2. The world changed, the checksum
  knows, the version signal is dead, the gate does nothing, and the
  learner proceeds unaware (the answer is coincidentally right).
- ES-B4 (no learning from failure experience): the ES-D block matches
  ES-B on every discriminating field: identical ES-PROBE values,
  exactly 2 RETRY lines, ESQ0B's (agree,vers) sequence equals ESQ0's
  (agree=0,vers=2),(agree=0,vers=2),(agree=1,vers=0), and ES-AUTO
  entry_mask=0. The learner's staleness gating did not change after
  the ES-B/ES-C failure experience.
- ES-B5 (neutral-mutation discriminator): the ES-NEUTRAL line is
  exactly `ES-NEUTRAL e0=0 e1=0 ck_same=1 nf_same=1`; the ES-PROBE2
  line is exactly `ES-PROBE2 nf_stale=0 ck_stale=0 ver_stale=0`;
  ESQd2 is a single Q line with agree=1 vers=2. A mutation event
  occurred; zero learner signals responded. (Contrast LE-B4, where
  the researcher-designed epoch advanced on a learner-op mutation.)
- ES-B6 (invention audit, static): `grep -c "931" es_learn.zag` is 4
  (three specialize recording reads plus spec_ver_stale; zero
  writes: the learner has no write path to any version cell);
  `grep -c "fact_add\|fact_set_obj" es_learn.zag` is 0 (the learner
  is not on the mutation path and cannot observe mutation events).
  The learner's state-write vocabulary during the battery is fixed
  slots only (index buckets, recorded nf/ck/ver, contracts, plans,
  bindings, stats): no allocation, no op-body installation.
- ES-K1 (cost of no versioning): blind_total > 984 (LEARNER-EPOCH's
  proactive total with working stamping). The bar discriminates via
  the inequality plus the ES-B2 structural signature (2 RETRYs):
  working versioning bought proactive recovery at 984 with zero
  RETRYs; without it the armed gate pays reactive-scale cost.
- ES-H1 (toolchain/hygiene): safebin for all build/run/verify
  commands; pure Zag; pinned znc; prereg committed alone before
  implementation; 3/3 byte-identical runs, stderr empty, exit 0;
  zero em/en dash bytes in authored files; no world literals in new
  executable code (all tags/rels/objs/goals and the ES-E triple
  runtime-derived, same discipline as LE-H1).

## 5. Predicted mechanism trace (for the report, not a bar)

- ES-A: three setup calls stamp nothing; specialize records epoch 0,
  checksum, nf 56.
- ES-B probe: nf_stale=0 (56=56), ck_stale=7 (reorder flips the
  order-sensitive hash), ver_stale=0 (dead signal reads 0=0). The
  proactive gate computes mask 0 and re-specializes nothing
  (entry_mask=0). ESQ0: plan miss (st=2), ret_spec on the stale A2
  index over the live A world, att=1 agree=0 vers=2; SELFTRIG
  invalidates the RET coverage contract (RETRY att=1, dc=1,0,0);
  att=2 agree=0 vers=2 (RETRY att=2, dc=2,0,0, clause retired);
  att=3 generic (vers=0) agree=1. ESQ1..ESQ8: generic first-try
  agrees. Exactly 2 RETRY lines in the block.
- ES-C probe: nf_stale=0, ck_stale=7 (duplicated object flips the
  checksum), ver_stale=0. ESQ0A: plan hit, vers=2, agree=1 first
  try, zero RETRY lines: silent staleness.
- ES-D: same signature as ES-B on all ES-B4 fields (the gate is
  hardcoded; the revise-on-retire path in cov_induct re-inducts
  fresh contracts, so preconditions match).
- ES-E: e0=0, e1=0 (no-op bump; and no learner cell advances
  per-mutation-event); ck_same=1, nf_same=1; ES-PROBE2 all zeros;
  ESQd1/ESQd2 agree=1 vers=2.
- Estimated costs: blind_total at reactive scale (LE reactive was
  1152; the bar is the > 984 inequality, not the estimate).

## 6. What this does NOT claim

- This probe does not demonstrate learner-created stamping; the
  predicted outcome is that the current machinery cannot do it. A
  null result here is evidence about the architecture, not a failure
  of effort.
- Removing the bump does not remove the epoch concept from the
  source (the cell and its reads remain as a dead signal); the claim
  is only that no versioning is INSTALLED (no writer, ES-S1).
- 56 facts is a toy world; the cost inequality is structural
  (per-query check cost vs per-query index saving vs respec cost),
  not a scaling result.
- Whether failure experience plus the six A2 capabilities would be
  sufficient for genuine invention is not tested here; that needs
  the architecture delta (runtime executable-graph construction
  wired into the world-mutation interface, plus failure attribution
  to missing mechanisms and probationary validation), which is
  future work, likely as a consumer of the TNN-2 post-freeze
  executable-graph mechanism.
- ES follow-ups not in scope: content-change-only epoch,
  two-op enforcement, SI follow-ups 2-4 (checksum audit policy, cost
  at scale, proactive placement).
