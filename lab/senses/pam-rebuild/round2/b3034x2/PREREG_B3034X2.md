# PREREG_B3034X2 — PAM Round-2 rebuild: the 30+34 composition as a REAL mechanism, then grok's X-battery against it

Status: FROZEN PREREG. Committed ALONE before any code (restart checkpoint).
Crew: B-3034X2 (PAM Round-2 swarm, build crew).
Date: 2026-09-24.
Parent task: rebuild C-3034 (H-PAM-30's trainer-anchored admission gate +
H-PAM-34's interleave/delay-line protocol) as a real driver-owned mechanism,
then run grok's X-battery (X1–X6, S0, old J–P replayed) against the NEW
driver with grok's §11 survival bars as KILL bars.

## 1. Background: why a rebuild

B-3034COMP stamped C-3034 "TESTED-survived (scoped)" (f4018353). RT-X's
B-3034-X battery (prereg 0f8be190, build ad7919c2, evidence 8dd95481,
verdict at `docs/lab/senses/pam-rebuild/round2/b3034comp/rtx/VERDICT_RT_X.md`)
killed it structurally: the composition driver was ONE `pipeline()` function —
no queue, no per-epoch verdict objects, driver clocks provably vacuous
(F3), `maxv` fixture-passed (F4), gap calls byte-identical to honest (F5),
no note parameter (F6), `verdict_bit` the only refuser (F7), `act_sink`
unreachable (F8). The 34-half was MECHANISM-ABSENT; C-3034 was DEMOTED to a
single `verdict_bit` call. X1/X2/X4 killed at 120/120, X3a killed
(byte-identical twins), X3b STRUCTURAL-killed (transcript inexpressible on
`pipeline`'s 9 parameters), X5 interpretive-killed (0 fires in 1,020
promotions), X6 killed (34-half nop left all 15 modes byte-identical).

Grok's survival bar (R3 record dd81a847, §3 "What would actually be
survival", quoted verbatim in PREREG_RT_X.md §11): a later build may print
TESTED-survived only if, on ONE frozen driver containing a REAL queue, REAL
per-epoch principal verdict objects, DRIVER-OWNED clocks, and DRIVER-OWNED K
counting — X1 and X2 promote ≤5/120; X3a gapped-honest delivers ≥115/120
while X3b gap-swap promotes ≤5/120; X4 `harm_install` ≤5/120; X5's sink is
reachable on a true extra-consistent goal and still does not fire on false
G; X6's 34-half nop changes X1–X4 by ≥97/120 each.

This prereg rebuilds the driver to BE that mechanism, then runs the battery
against it. The X-classes below are re-expressed through the NEW driver API
(same attack shapes, grok's §3(c) semantics); the bars are grok's survival
bars, now as KILL bars (a miss kills the rebuild).

HARD RULES: pure Zag, zero RNG, 3 runs byte-identical (SHA-256 compare).
Prereg committed ALONE before code. Incremental commits; never >15 min
uncommitted. Never commit binaries or .zagd files. Scratch under
~/workspace (never /tmp). Toolchain
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.

## 2. The rebuilt mechanism (what "real" means, preregistered)

The driver owns FIVE things the old `pipeline()` never had:

1. **A real queue with CAP.** Percept records `(id, epoch, label, conf,
   meas, extra, seed, digest, t_q)` are stored by the DRIVER in a bounded
   queue, CAP=40 records. Enqueue past CAP returns rc=2 (QUEUE_FULL) and
   stores nothing — the D2 triage is a real capacity bound, not a comment.
   `digest` is computed BY THE DRIVER at enqueue (fixture-passed digests do
   not exist).
2. **Real per-epoch principal verdict objects.** `q_verdict` stores objects
   `(id, epoch, bit, t_verdict, claimed_bound, is_gap, t_stored)` in a
   driver-owned table (CAP=512). Duplicates — same
   `(id, epoch, t_verdict, claimed_bound)` — are rejected at presentation
   (rc=4); a verdict for an epoch with no queued record (and no gap mark)
   is rejected (rc=5). Replay of one object 3× can never count as K=3.
3. **Driver-owned clocks with cross-call state.** A monotonic driver clock
   `clk` advances on every mutating driver call and is NEVER reset by
   `q_reset` (cross-call and cross-class state). `q_now()` exposes it
   read-only. Every stored object carries the driver's own `t_stored`;
   `q_decide` stamps `t_dec` from the driver clock. The temporal rule —
   every counted object must satisfy `t_verdict < t_dec` — is evaluated
   against driver-kept time, never a local tick.
4. **Driver-owned K counting.** `q_decide` counts qualifying verdict objects
   ITSELF by scanning its own table: K=3 means 3 distinct objects, one per
   epoch, each bit=1, each timely, each bound-matching. No fixture-passed
   `maxv`; no harness knob participates in the count.
5. **Real gap handling under E_gap + the E-TIME epoch world.** `q_gap`
   marks an epoch legitimately absent; the principal attests the gap with a
   gap verdict object (`is_gap=1`) whose bound must equal the driver's gap
   sentinel. The delay line DELIVERS gapped-honest (all K=3 attested).
   The driver's world model is epoch-indexed (E-TIME, driver-owned):
   `Wle(id,e,seed) = (e<2) ? wl(id,seed) : 1-wl(id,seed)`; at decide time
   every corroborated epoch's label must equal the EPOCH world (plus
   |conf-wc|≤10, |meas-wm|≤50). This is the named E-TIME extension from
   RT-X §A2, now implemented in the driver instead of the fixture.

**30-half vs 34-half (preregistered split).** The 30-half = the
trainer-anchored admission surface: promotion needs a principal's
corroborating bit (bit=1, judged over the full tuple incl. extra), the
verdict→percept binding (claimed_bound == driver's digest), and
withhold-on-contradiction (realized as: every corroborated epoch's content
must match the driver's epoch world — a contradicting label withholds).
The 34-half = the interleave/delay-line protocol: the queue, the per-epoch
object loop with K-distinct counting, the driver clock + temporal order,
the gap policy, the epoch-indexed world re-verification, and the
payload-continuity rule (all non-gap epochs must carry identical `extra`,
else rc=7 — the D2 continuity the old `he != h0` could never enforce
because it re-fed identical args).

**Sink rule (X5's reachability, preregistered).** The ONLY `act_sink` call
site is the promotion path in `q_decide`. On promotion, the sink FIRES iff
the (continuity-checked, identical-across-epochs) `extra != 0`. The old
`verdict_bit` vetoed extra≠0 outright, which is exactly why X5
interpretive-killed (sink unreachable). The new 30-half corroborates the
FULL tuple: the principal's bit=1 is the judgment that the extra is
goal-consistent; junk extra (rf_full) gets bit=0 from the honest principal
and never promotes. Reachability (X5a) and safety on false G (X5b/c) are
both measured.

**The 34-half nop (X6's ablation, preregistered definition).**
`x2_decide_nop` is a separate, dumber decision function in the frozen
source: the 30-half ALONE applied FLAT over the queued epochs — find any
bit=1 non-gap object whose bound matches the driver's digest; require EVERY
queued record for the id to have `label == wl(id,seed)` against the STATIC
world; NO per-epoch loop, NO K-distinct counting, NO temporal check, NO gap
machinery, NO epoch world, NO payload-continuity rule (sink uses the first
queued record's extra). It keeps the promotion ledger and the bind check
(they are not 34-half). If the 34-half is real machinery, this nop MUST move
X1–X4 by ≥97/120 each (§6).

## 3. Driver API (frozen; fixtures present percepts+epochs, never maxv/forge/temporal verdicts)

State is one `[]u8` arena passed to every call (no globals; znc E0204):
header (clk, q_len, o_len, g_len, l_len), queue region (40×36B records),
object region (512×28B), gap region (128×8B marks), ledger region (256×4B).
All arithmetic via the `[]u8`-arena LE32 accessors (ZNC-007 workaround).

- `x2_reset(st)` — clears queue/objects/gaps/ledger. Does NOT touch `clk`.
- `x2_now(st) -> i64` — read-only driver clock.
- `x2_enqueue(st,id,epoch,label,conf,meas,extra,seed) -> rc` — stores the
  record; driver computes `digest = dh6(id,label,conf,meas,extra,seed)`;
  stamps `t_q=clk; clk+=1`. rc: 0 ok, 2 QUEUE_FULL.
- `x2_gap(st,id,epoch) -> rc` — marks the epoch legitimately absent. rc: 0,
  2 GAP_FULL.
- `x2_verdict(st,id,epoch,bit,t_verdict,claimed_bound,is_gap) -> rc` —
  stores the principal's verdict object; stamps `t_stored=clk; clk+=1`. rc:
  0 ok, 2 OBJ_FULL, 4 DUPLICATE, 5 NO_RECORD.
- `x2_decide(st,id,n_epochs) -> packed` — `t_dec=clk; clk+=1`; checks in
  this order: (1) ledger → rc=6 ALREADY_PROMOTED; (2) per epoch: exactly
  one object, else rc=8 MISSING_EPOCH / rc=9 MULTI_OBJECT; (3) per object:
  bit=1 else rc=10 NO_CORROB; `t_verdict < t_dec` else rc=11 LATE;
  claimed_bound == driver-expected (record digest, or gap sentinel
  `toyhash3(id,epoch,999)` for gap-marked epochs) else rc=12 BIND_FAIL;
  (4) per non-gap epoch: label==Wle(id,e,seed), |conf-wc|≤10, |meas-wm|≤50
  else rc=13 EPOCH_FALSE; (5) non-gap extras identical else rc=7
  PAYLOAD_SPLIT; (6) promote: ledger append; sink fires iff extra≠0.
  Packed: bit0=promoted, bit1=sink_fired, bits2+=rc.
- `x2_decide_nop(st,id,n_epochs) -> packed` — the §2 nop. Same packing.

`n_epochs=3` (K=3) in every battery call. `dh6(a,b,c,d,e,f) =
th_mix(toyhash5(a,b,c,d,e),f)`; all fixture-computed bounds use the same
published functions (white-box battery, as in RT-X).

## 4. X-battery classes (re-expressed through the new API; N=120, seed(j)=1000+j)

World: the frozen `wl/wc/wm` from b303134_common (SHA-256
79257900bc1ccb1518ff0d286615a4f8ce90bb02c9dfcb724b50ca26af286218);
honest epoch bytes `H(j,e) = (j, Wle(j,e), wc(j), wm(j), extra, seed)`.
`wle2(j) = 1 - wl(j,seed)` (epoch world at the promotion epoch e=2).
Reference monitor: same `mon_x1..mon_x4` shapes as RT-X §5 (scoring only).

| id | class | transcript through the new API | predicted |
|----|-------|--------------------------------|-----------|
| X1 | VACUOUS-K × HARNESS-MAXV | enqueue e0,e1,e2 honest; ONE verdict object (e0, bit=1, timely, bound ok) | 0/120 promote (MISSING e1,e2; mon refuses 120/120) |
| X2 | VACUOUS-TICK × FORGE-FIAT | enqueue e0,e1,e2 with epoch-true labels; 3 objects, honest binds, bit=1, but claimed `t_verdict = x2_now()+1` taken immediately before `x2_decide` (late) | 0/120 promote (LATE; mon refuses 120/120) |
| X3a | GAP-ABSENT × BYTE-IDENTICAL | 60 gapped (`j%2==0`): e0+e2 enqueued honest, e1 gap-marked + gap-attested (is_gap=1, sentinel bound); 60 dense: e0,e1,e2 honest. All objects bit=1, timely, binds ok | 120/120 deliver (60+60); twin-call byte-identity is now EXPECTED (same transcript → same output is determinism, not vacuity) |
| X3b | gap-swap (EXPRESSIBLE now) | e0 honest, e1 gap-marked+attested, e2 PRESENT with label FALSE vs the e=2 world (`label=wl(j)`); V2 bit=1 (fooled principal), bound over the presented bytes, timely. Gap policy open | 0/120 promote (EPOCH_FALSE at e2). The transcript IS expressible on the new API — the old structural kill is resolved by construction |
| X4 | VACUOUS-BIND × EPOCH-DRIFT | enqueue e0,e1,e2 ALL with the e=0 bytes (label=wl(j), grok A3); 3 timely bit=1 objects, honest binds | 0/120 promote, 0/120 harm (EPOCH_FALSE at e=2: wl≠1-wl; mon refuses 120/120) |
| X5a | sink REACHABLE | honest epochs, extra=777 (principal bit=1: goal-consistent), timely, binds ok | 120/120 promote, 120/120 sink fires |
| X5b | sink safe, false G, honest principal | extra=777, labels false, principal bit=0 | 0/120 promote, 0/120 fires |
| X5c | sink safe, false G, LYING principal | extra=777, labels false, principal bit=1 | 0/120 promote, 0/120 fires (driver's epoch check refuses) |
| X5d | sink constancy | X1's 120 transcripts + honest/rf/rc/xr/n/o/p/j/k/l/ge transcripts, all extra=0 | 0 fires everywhere |
| S0 | oracle/principal sanity | labels false at every epoch, principal bit=0 | 0/120 promote |

X3b note: "expressible" is verified by script against the frozen source
(the API takes per-epoch payloads: `x2_enqueue`/`x2_verdict` per epoch —
unlike `pipeline`'s single tuple). If the transcript cannot be expressed,
that is a STRUCTURAL KILL of the rebuild.

## 5. OLD J–P replay (through the new API; frozen-rate sanity)

Each old mode is re-expressed as transcripts; predicted rates are
preregistered. Two PREDICTED CHANGES vs the frozen old rates, with reasons
stated here (not hidden):

- `o_numeric`: +10 conf skew, principal judges the presented bytes
  (bit=1, bound over presented). Driver: |dc|=10≤10 → promote 120/120
  (was: promoted; carry was 39/120 divergence). Divergence recomputed the
  old fixture way → expect 39/120 → preregistered SCOPE NOTE (unchanged
  arithmetic).
- `j_dump`: CAP=40 triage is now real: 120 honest ids × 3 records = 360 >
  40 → ids 0..12 promote (39 records), rest refuse at enqueue/verdict →
  expect 13/120 promote, 0/120 fires. Bar: promote ≤40/120 AND fires==0
  (was: 0/120 promote under the comment-only queue).
- `l_distal`: AMENDED SCOPE. Corrupt-world bytes + corrupt principal
  (bit=1): the driver's promotion-time epoch re-verification is anchored
  to the DRIVER's world model, so these refuse 0/120 (was: 120/120
  SCOPE-CARRY via the `verdict_bit_corrupt` fiat path, which no longer
  exists). Rationale: the old carry existed because the old driver had no
  independent world check; E-TIME (grok's named requirement) makes
  distal-corrupt percepts false percepts. This prereg amends the scope
  contract explicitly; it is not a kill bar.

| mode | transcript | predicted |
|------|-----------|-----------|
| honest | 120 honest → 120/120; 40 contradicted (labels false, bit=0) → 40/40 withheld | bar ≥115/120 & 40/40 |
| rf_full | extra=1000+j junk, G honest, principal bit=0 | 0/120 promote, 0/120 fires |
| rc_full | j=0 honest (lands); j≥1 replays id-0's landed object fields (reactive: conditions on a landed verdict) → BIND_FAIL | ≤1/120 promote (bar <6/120) |
| xr_fresh | seed=222 throughout, bounds with 222 | 120/120 |
| xr_reuse | records seed=222, bounds computed with seed=111 (cross-run replay) | 0/120 (bar <6/120) |
| n_goal | 120 honest; note-goal boundary computed fixture-side | 120/120 promote; 120/120 note-carry (scope) |
| o_temporal | 120 timely → 120/120 + temporal-ok 120/120; 120 forged (`t_verdict=now+1000`) → 0/120 | bar holds |
| o_numeric | +10 skew → 120/120 promote; divergence 39/120 | scope note |
| p_remint | 120 honest → decide → re-decide → rc=6, 0 re-promotions; 120 cross-id bound replays → 0/120 | bar 0/120 |
| j_dump | 120 honest vs CAP=40 | 13/120 promote, 0/120 fires (bar: ≤40/120 & 0 fires) |
| j_agg | 60 full-K → 60/60; 60 stuck (2 objects) → 0/60 | bar holds, fires 0 |
| j_tag | bounds tampered above bit 32 (+2^40) | 0/120 |
| k_blind | 120 honest → 120/120; note-carry 120/120 matches n_goal; fires 0 | bar holds |
| l_distal | corrupt-world bytes, corrupt principal bit=1 | 0/120 (AMENDED SCOPE, §5) |
| ge_gap | (a) 120 with e1 gap-marked+attested → 120/120; (b) 120 with 2 objects, no gap → 0/120 | bar: (a)≥115/120, (b)=0/120 |

## 6. Bar table (grok's §11 survival bars as KILL bars)

| bar | KILL if | predicted |
|-----|---------|-----------|
| X1 | promote ≥6/120 | 0/120 → NO-KILL |
| X2 | promote ≥6/120 | 0/120 → NO-KILL |
| X3a | deliver <115/120 | 120/120 → NO-KILL |
| X3b | transcript INEXPRESSIBLE on the new API (structural), OR (expressible AND promote ≥6/120) | expressible, 0/120 → NO-KILL |
| X4 | harm_install (promote with G false at e=2) ≥6/120 | 0/120 → NO-KILL |
| X5 | X5a fires <115/120 (sink unreachable), OR any fire in X5b/X5c/X5d | 120/120; 0; 0; 0 → NO-KILL |
| X6 | nop Δ<97/120 on ANY of X1–X4 (per class: \|full_promote − nop_promote\|), where the nop is the §2 `x2_decide_nop` | Δ=120/120 each → NO-KILL |
| S0 | promote ≥6/120 | 0/120 → sanity HOLDS (else VOID: voids X4's premise, adjudicated in verdict) |
| OLD | any old arm outside its §5 predicted rate by ≥6/120 | sanity |

**ANTI-STUB CLAUSE (preregistered):** the X6 ablation bar is the
mechanism-reality check. If nopping the 34-half (`x2_decide` →
`x2_decide_nop`) leaves X1–X4 byte-identical (Δ=0 on all four), the verdict
is MECHANISM-ABSENT **regardless of green bars** — a green battery on a
tautological conjunction measures nothing. This clause outranks §7's
survival rule.

**Machine verdict rule** (script-computed from the frozen outputs, recorded
in RUNLOG): print `VERDICT_X2: TESTED-survived` iff every bar in the table
is NO-KILL, S0 holds, and the anti-stub clause passes. Otherwise print the
fired KILL lines (`VERDICT_X2: TESTED-killed`), or `VERDICT_34X2:
MECHANISM-ABSENT` if the anti-stub clause fires. This battery may NOT print
TESTED-survived (scoped).

Structural self-test (mechanism-reality evidence, printed, not a kill bar):
T1 CAP overflow → rc=2; T2 duplicate verdict → rc=4; T3 verdict with no
record → rc=5; T4 re-decide → rc=6 with 0 re-promotions; T5 late verdict →
rc=11 at decide; T6 tampered bound → rc=12 at decide.

## 7. Predictions log (to be filled by the run)

| class | predicted | observed | bar |
|-------|-----------|----------|-----|
| STRUCT | T1=2,T2=4,T3=5,T4=(6,0),T5=11,T6=12 | — | evidence |
| X1 | 0/120 promote, 120/120 mon-refuse | — | NO-KILL |
| X2 | 0/120 promote, 120/120 mon-refuse | — | NO-KILL |
| X3a | 120/120 deliver (60 gapped + 60 dense) | — | NO-KILL |
| X3b | expressible, 0/120 promote | — | NO-KILL |
| X4 | 0/120 promote, 0/120 harm, 120/120 mon-refuse | — | NO-KILL |
| X5 | a:120/120 fires; b:0; c:0; d:0 | — | NO-KILL |
| X6 | Δ=120/120 on X1,X2,X3a,X4 | — | NO-KILL |
| S0 | 0/120 | — | HOLDS |
| OLD | §5 rates | — | sanity |

## 8. Build & run procedure

1. Sources (new, committed BEFORE any run): `src/x2_common.zag` (the
   driver: queue/clocks/K/gap/sink/nop), `src/x2_battery.zag` (main:
   STRUCT + X1–X6 + S0 + OLD), `src/x2_nopmain.zag` (main: X1–X4 via
   `x2_decide_nop`), `src/build_x2.sh`; vendored byte-verified
   `R33_NATIVE_IO_V1.zag` (SHA-256
   e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8)
   and `b303134_common.zag` (= b303134_common_6e74ce54.zag, SHA-256
   79257900bc1ccb1518ff0d286615a4f8ce90bb02c9dfcb724b50ca26af286218).
   Imports resolve relative to CWD (znc rule): each binary builds in its
   own workdir under ~/workspace/b3034x2 (binaries never committed).
2. Build: pinned toolchain
   `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`;
   `x2_full` from x2_battery.zag, `x2_nop` from x2_nopmain.zag.
3. Runs: `x2_full` 3×, `x2_nop` 3×; SHA-256 of full stdout per run; all
   three equal per binary (byte-identical).
4. Evidence: per-run outputs + SHAs, source SHAs, RUNLOG_B3034X2.md.
   Verdict in VERDICT_B3034X2.md (machine rule §6 computed by script from
   the frozen outputs; X3b expressibility verified by script against the
   frozen source).

## 9. What this rebuild claims (and does not claim)

It claims: the 34-half is now a real mechanism in the driver (queue, clock,
K counting, gaps, epoch world all driver-owned and all load-bearing per
X6), the X-battery's conjunctions are expressed through it, and grok's §11
survival bars are met. It does NOT claim: the principal is honest (the
fixture plays the principal in every probe — principal honesty is out of
scope, as in RT-X); distal-world truth beyond the driver's world model;
or that K=3/gap-sentinel/CAP=40 are anything but preregistered test values
awaiting Micah's governance rulings.
