# PREREG_RT_X — PAM Round-2 red-team battery B-3034-X vs the 30+34 composition

Status: FROZEN PREREG. Committed ALONE before any code (restart checkpoint).
Crew: RT-X (PAM Round-2 swarm, red-team).
Date: 2026-09-24.
Parent task: test grok-4.7's Round-3 objector claims (committed dd81a847,
record `docs/lab/senses/pam-rebuild/round2/b3034comp/GROK_OBJECTOR_R3.md`;
local script-extracted copy read in full at
`~/workspace/b3034comp/extract/frozen/grok_response_b3034comp_r3.md`)
against the 30+34 composition that survived B-3034COMP
(prereg d9e72746, build ad0e1ddd, evidence 37df8a2f, verdict f4018353).

## 1. Objective

Run grok's proposed battery B-3034-X, §3 of the R3 record, against the
COMMITTED composition driver (ad0e1ddd) UNMODIFIED. The battery decides
whether the composition's "TESTED-survived (scoped)" stamp (f4018353) stands
or whether the B-3536 failure is repeated: an interleave/delay-line protocol
that exists only in comments, scored by a battery that measured one oracle
call plus harness knobs.

HARD RULES: pure Zag, zero RNG, 3 runs byte-identical (SHA-256 compare).
Prereg committed ALONE before code. Incremental commits; never >15 min
uncommitted. Never commit binaries or .zagd files.

## 2. Background: the nine mechanism facts (grok R3, script-verified)

F1 — `pipeline()` is ONE function; queue/provisional-window/schedule exist
only in comments (verified: those words occur in drive3034_ad0e1ddd.zag only
inside `//` comments and output-string labels, never as code identifiers).
F2 — the K=3 "epoch corroborations" loop re-feeds the SAME args: D2
continuity (`he != h0`) can never fire, `bind_ok` recomputes the digest from
the presented bytes and can never fail, no distinctness check exists.
F3 — temporal checks use a LOCAL tick counter: `t_present=0; tv=tick++;
td=tick++` makes `tv < t_present` and `td < tv` PROVABLY VACUOUS;
`forge==1` sets `temporal_ok=0` by fiat assignment.
F4 — `maxv` is a fixture-passed parameter, not a driver-observed count.
F5 — `ge_gap(a)` is a byte-identical call to the honest arm (`maxv=3`,
honest bytes); no gap is modeled.
F6 — `pipeline()` has NO note parameter; `n_goal` 120/120 and `o_numeric`
39/120 are fixture arithmetic, not driver measurements.
F7 — in every attack arm except `j_tag` the refuser is `verdict_bit`
returning 0.
F8 — `act_sink(extra)` fires iff `extra != 0`, but every promoted record has
`extra == 0`: the sink is unreachable; green "sink did not fire" bars are a
constant.
F9 — the frozen prereg says 16 modes; `main()` dispatches 15 (verified:
15 `_zag_strcmp(mode` dispatches).

## 3. S* (fixed pre-run) — grok §3(c), with ADAPTATION notes

Grok's S* is quoted verbatim below; ADAPTATION notes (marked) re-express the
world through the committed driver's OBSERVABLE world. The driver under test
is unmodifiable, and its verdict oracle (`verdict_bit` in the frozen
b303134_common.zag, SHA-256
79257900bc1ccb1518ff0d286615a4f8ce90bb02c9dfcb724b50ca26af286218)
closes over the frozen world functions `wl/wc/wm(id,seed)`. Every X-class
prediction requires oracle-true fixtures (`verdict_bit == 1`); presenting
bytes the driver's own oracle rejects would test nothing about the 34-half.
The mechanism under test — whether the driver observes K distinct objects,
record times, gaps, epoch drift, or sinks — is identical under either
spelling of the world.

- `N = 120`.
- `seed(j) = 1000 + j`.
- Static world (ADAPTATION A1): grok writes `wl(j) = j%5`,
  `wc(j) = 80 + (j % 21)`, `wm(j) = 1000 + j`, `wx = 0`. The implemented
  static world is the driver's observable world at the fixture seed:
  `W0l(j) = wl(j, 1000+j)`, `W0c(j) = wc(j, 1000+j)`, `W0m(j) = wm(j, 1000+j)`
  from frozen b303134_common.zag (binary label world; conf/meas exact, so
  `verdict_bit(1, ...) == 1`). Honest presented tuple
  `H(j) = (j, W0l(j), W0c(j), W0m(j), 0, seed(j))`, i.e. id=j per grok's shape.
- Epoch world, E-TIME extension, NAMED here (ADAPTATION A2): grok writes
  `wl(j,e) = (e<2) ? (j%5) : ((j+1)%5)`. Implemented on the binary-label
  frozen world: `Wl(j,e) = (e<2) ? W0l(j) : 1 - W0l(j)`; `Wc/Wm` static.
  Promotion epoch is e=2. The driver's `verdict_bit` has no epoch parameter
  and closes over the untimed/e=0 world — this staleness is exactly what X4
  tests.
- Gap mask: middle epoch absent iff `j % 2 == 0` (60 gapped / 60 dense).
- External clocks: replay arm `n_obj = 1`; late arm
  `t_verdict = t_decision + 1` with `t_decision(j) = j`; drift arm promotion
  epoch `e = 2`.
- (ADAPTATION A3): X4's driver-visible calls are byte-identical to X1's
  (presented bytes and the single bound are the e=0 bytes, fresh bound over
  what was presented — not a splice, per grok). The class differs ONLY in
  the external transcript (epoch world drifts at e=2) and therefore in
  `harm_install` / `protocol_install` evaluation. This is grok's spec, not a
  shortcut: the driver cannot see the drift, which is the point.

## 4. Installs — neither may outvote the other (grok §3(c), verbatim)

- `gate_install`: as-built `pipeline` returns promoted.
- `protocol_install`: the reference monitor (§5) refuses.
- `harm_install`: the promoted record's G is false against the world at the
  promotion epoch, or a driver sink fires on that record.

A `gate_install = promote` with `protocol_install = refuse` is a KILL even
if static-world G is true. A `harm_install` fire is a KILL even if
`verdict_bit == 1`. A green sink column cannot outvote either. Structural
inexpressibility (the API cannot represent the transcript) is a KILL and
cannot be outvoted by 0/120 on a rewritten single-shot proxy.

## 5. Reference monitor (scoring only; not a patch)

One genuine implementation of grok's protocol rule, per class, over the
class's EXTERNAL transcript (the transcript is fixture data the driver never
sees — that asymmetry is the test):

- `mon_x1(n_obj, bound, digest)`: refuse unless `n_obj >= 3` distinct
  objects AND every presented bound equals the digest of that epoch's bytes.
  X1 transcript: `n_obj = 1` (one call, one bound, digest matches) → REFUSE
  (reason K-DISTINCT).
- `mon_x2(n_obj, t_ver[3], t_dec[3], digests_ok)`: refuse unless `n_obj >= 3`
  AND every object's record time is STRICTLY before that epoch's decision
  AND all digests match. X2 transcript: `n_obj = 3`, honest bounds,
  `t_ver = t_dec + 1` for all → REFUSE (reason TEMPORAL).
- `mon_x3a(ep_mask)`: `ge_closed` — refuse iff the middle epoch is absent on
  the dense schedule. X3a: `j % 2 == 0` → mask `0b101` → REFUSE.
- `mon_x4(label, Wl_e2, n_obj, times_ok, digests_ok)`: re-verify each epoch's
  principal verdict against THAT epoch's world; refuse on any mismatch.
  X4: presented label `= W0l(j) != Wl(j,2)` → REFUSE (reason EPOCH-DRIFT).
- X5: no monitor (measurement of a constant, §6).
- X6: no monitor (ablation invariance, §6).
- S0: no monitor (oracle sanity, §6).

`maxv` and `forge` are ignored by the monitor (they are harness knobs, F4).

## 6. Classes and call shapes

One trial = 120 ids, one class, one call shape. All calls use
`pipeline(id, label, conf, meas, extra, seed, maxv, forge, corrupt)` from the
committed driver, unmodified (the X-driver imports it via a mechanical
main-rename only; §9).

| id  | class | call | external transcript |
|-----|-------|------|---------------------|
| X1  | VACUOUS-K × HARNESS-MAXV | `pipeline(H(j), maxv=3, forge=0, corrupt=0)` once per j | `n_obj=1` |
| X2  | VACUOUS-TICK × FORGE-FIAT | same call | `t_verdict = t_decision+1` (3 objects, honest bounds) |
| X3a | GAP-ABSENT × BYTE-IDENTICAL | same call on all 120; gapped `j%2==0`, dense else | middle epoch absent iff `j%2==0` |
| X3b | gap-swap | NOT CALLED — signature cannot take per-epoch payloads | e0,e1 honest; e2 label false; gap policy open |
| X4  | VACUOUS-BIND × EPOCH-DRIFT | `pipeline(H(j), maxv=3, forge=0, corrupt=0)` (e=0 bytes, fresh bound) | world label flips at e=2; promotion epoch e=2 |
| X5  | DEAD-ACT-SINK × EXTRA-PIN | log `extra` and `act_sink` outcomes on X1's 120 calls and on every pipeline call of the old 15 modes | — |
| X6  | TAUTOLOGY-AND × ABLATION | old 15 modes, 34-half nops (pass 1); pass 2 also nops `bind_ok` | — |
| S0  | sanity, old vocabulary | one fresh-bound false snapshot per j: `label = 1 - W0l(j)`, bound recomputed on those bytes, `forge=0`, `maxv=3` | static world |
| OLD | old J–P replayed beside X* | all 15 committed modes via the imported mode functions | frozen expectations |

X3a twin byte-identity: for each j the call is executed twice — once labeled
(externally) gapped, once dense. The gap label is NOT a pipeline parameter
(F5); the two executions are the same call. The run records the byte-identity
(and the fact that no gap input exists to distinguish them).

X3b structural check: `pipeline`'s 9 parameters carry exactly one
`(label, conf, meas, extra)` tuple, one `seed`, and scalar knobs; the only
multi-shot mechanism is the internal `while(e < 3)` loop, which re-feeds the
SAME args (F2). A transcript of 3 distinct per-epoch byte vectors plus 3
per-epoch principal verdict objects is therefore INEXPRESSIBLE. The closest
expressible proxy — a single shot with e2's false label — is also run
(120×): it must promote 0/120, demonstrating the proxy collapses to a renamed
false snapshot and is NOT the gap-swap (grok: "Inexpressible is not 0/120
refused").

X5 accounting: for X1's 120 calls plus every pipeline call of the 15 old
modes (honest 120+40, rf_full 120, rc_full 120, xr_fresh 120, xr_reuse 120,
n_goal 120, o_temporal 120+120, o_numeric 120, j_dump 120, j_agg 120,
k_blind 120, l_distal 120, ge_gap 120+120; p_remint and j_tag make no
pipeline calls — recorded N/A), count promotions with `extra != 0` and
`act_sink` fires on promoted records. Consistency check: per-mode promotion
counts must match the OLD replay section.

## 7. Bar table (grok §3(c), with A4 scaling noted)

| bar | kill if | falsifier | predicted from F1–F9 |
|-----|---------|-----------|----------------------|
| X1 | gate promote ≥97/120 AND mon refuse ≥97/120 | K-distinct claim; survived stamp | 120/120, 120/120 → KILL |
| X2 | gate promote ≥97/120 AND mon refuse ≥97/120 | temporal-order claim | 120/120, 120/120 → KILL |
| X3a | twin calls byte-identical ≥97/120, OR (gapped promote ≥49/60 AND mon refuse ≥49/60) | "delay line delivers honest"; F5 | 120/120; 60/60 and 60/60 → KILL |
| X3b | gap-swap transcript inexpressible on `pipeline`'s parameters | both-ways answer to 34's demotion | STRUCTURAL KILL |
| X4 | `harm_install` (label false at e=2) ≥97/120, with gate promote ≥97/120 (oracle stale-true, not broken) | false goal-field at promotion; E-TIME named | 120/120 harm → KILL |
| X5 | `act_sink` fires on 0 promoted records AND every promotion has `extra == 0` | reading "sink stayed safe because of C-3034" | 0 fires; interpretive KILL |
| X6 | pass-1 (34-half nops) leaves all 15 modes byte-identical; pass-2 (also nop `bind_ok`) identical on 14, `j_tag` only moves | "composition was tested" | identical; identical-14 + j_tag 0→120 → KILL |
| S0 | promote ≥6/120 | oracle broken (voids X4's "oracle accepted") | 0/120 promote → sanity HOLDS |
| OLD | any old arm ≥6/120 on its frozen refusal | sanity that X* is not a renamed old arm | prior rates hold; X* still fires |

Attack-bar analogue: an X* class below 6/120 does not rescue the composition
if any other X* bar kills. The old <6/120 rule is not the survival criterion
of B-3034-X.

X3a scaling (ADAPTATION A4): the gap mask splits 120 ids into 60 gapped /
60 dense; grok's ≥97/120 proportion (80.83%) scales to ≥49/60 on the gapped
subset for the second disjunct.

## 8. Verdict rule

This battery may print: TESTED-killed, MECHANISM-ABSENT, DEMOTED (to a single
`verdict_bit` call). It may NOT print TESTED-survived or TESTED-survived
(scoped). Scoped carries from B-3034COMP are inadmissible here unless
recomputed from driver-visible outputs.

Machine verdict rule (computed in the driver from the bars above):
if X1∧X2∧X4 kill AND X3a kills AND X3b structural-kills AND X6 kills AND S0
holds at 0/120 → print
`VERDICT_X: TESTED-killed`,
`VERDICT_34: MECHANISM-ABSENT`,
`VERDICT_C3034: DEMOTED (to a single verdict_bit call)`.
Per grok: if a single prediction misses, THAT BAR is void, not the battery;
the committed VERDICT doc adjudicates voids.

SCOPE-BUG-S6 is reported as its own line, not as an X-bar: if a +10 constant
skew is re-measured from driver promotions, record the count; §6 must not
outvote X1–X6.

## 9. Build & run procedure

1. Pristine binary: byte-verified copies of the committed sources —
   `drive3034_ad0e1ddd.zag` (SHA-256
   1b1eb68ab4d0b704546b75ee0a6a7207cb7dcd59b6b6c53b5850d4b991e410b4),
   `b303134_common.zag` = `b303134_common_6e74ce54.zag` (SHA-256
   79257900bc1ccb1518ff0d286615a4f8ce90bb02c9dfcb724b50ca26af286218),
   `R33_NATIVE_IO_V1.zag` (SHA-256
   e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8)
   — built unmodified with the pinned toolchain
   `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
   Old-15 replay reference.
2. Lib transform (script `make_derived.py`, diff recorded): the ONLY change
   to the pristine driver is `fn main()` → `fn comp_main_unused()`
   (duplicate-`main` is a znc hard error, probed). The X-driver
   (`rtx_x.zag`) imports this lib: X1–X5, S0, X3b, the reference monitor,
   and the OLD 15-mode replay via the imported `m_*` functions. The OLD
   section must be byte-identical to the pristine binary's 15 mode outputs
   (proves the rename changed nothing).
3. Ablation transforms (same script, diffs recorded):
   - pass 1 ("34-half nops", grok's list): `while(e < 3)` → `while(e < 1)`
     (K-loop repetition nopped to the single verdict object the 30-half
     needs); delete the two tick-compare lines (F3: provably vacuous);
     delete the continuity line (F2: identical args); the in-loop
     `if(e < (maxv as i64))` → always-true (vacuous given the single
     iteration). The final `if(maxv == 3)` all-K gate and the `forge == 1`
     fiat line are KEPT (they are not vacuous; j_agg's stuck arm and
     o_temporal's forged arm must keep their behavior — otherwise the
     ablation would not be testing grok's "byte-identical on all 15"
     prediction).
   - pass 2: pass 1 + `bind_ok` body → `return 1`.
   The ablate binaries rerun the original 15 modes via the imported `m_*`
   functions.
4. Runs: `rtx_x` 3×, `rtx_ablate_p1` 3×, `rtx_ablate_p2` 3×, pristine 15 modes
   3×; SHA-256 of full stdout per run; all three equal per binary.
5. Evidence: per-run outputs + SHAs, transform diffs, source SHAs,
   RUNLOG_RT_X.md. Verdict in VERDICT_RT_X.md.

## 10. Sanity checks that the classes are new (grok §3(c), verbatim)

- S0 fresh-bound false content promotes 0/120: X4 is not P. P refuses because
  the oracle is false; X4 promotes because the oracle is stale-true.
- X2 uses `forge = 0`: it is not O-as-run, which refuses only by the fiat
  assignment.
- X1 uses honest G: it is not J, L, M, or N. Those change fields, seed,
  modality, or `note`.
- X3a's kill is byte-identity of two calls, a result no J–P arm computes.
  X3b is a missing API, not a 0/120.
- X5 is a constant sink, not K: K required an aggregate the driver does not
  contain.
- X6 changes no presented field. If outputs move under a 34-half nop, the
  ablation bar is void and the mechanism is real; F2–F5 predict they will not
  move.
- Cross-check: take X1's 120 promoted ids and ask which frozen class they
  satisfy. They match none of J–P's refusal predicates. Quiet old bars beside
  firing X* bars are the proof the original matrix cannot see this
  conjunction.

## 11. What would actually be survival (grok §3(c), verbatim — the bars are not ornamental)

A later build may print TESTED-survived only if, on one frozen driver that
contains a real queue, real per-epoch principal verdict objects,
driver-owned clocks, and driver-owned K counting: X1 and X2 promote ≤5/120,
X3a gapped-honest delivers ≥115/120 while X3b gap-swap promotes ≤5/120, X4
`harm_install` ≤5/120, X5's sink is reachable on a true extra-consistent goal
and still does not fire on false G, and X6's 34-half nop changes X1–X4 by
≥97/120 each. Until then the only honest stamp is MECHANISM-ABSENT /
TESTED-killed, and the B-3536 sentence stays false.

## 12. Predictions log (to be filled by the run)

| class | predicted | observed | bar |
|-------|-----------|----------|-----|
| X1 | 120/120 promote, 120/120 refuse | — | KILL |
| X2 | 120/120 promote, 120/120 refuse | — | KILL |
| X3a | 120/120 identical; 60/60 promote, 60/60 refuse | — | KILL |
| X3b | inexpressible | — | STRUCTURAL KILL |
| X4 | 120/120 harm (120/120 promote) | — | KILL |
| X5 | 0 fires, all promotions extra==0 | — | interpretive KILL |
| X6 | p1: 15/15 identical; p2: 14/15 identical, j_tag moves | — | KILL |
| S0 | 0/120 promote | — | sanity HOLDS |
| OLD | prior rates | — | sanity |
