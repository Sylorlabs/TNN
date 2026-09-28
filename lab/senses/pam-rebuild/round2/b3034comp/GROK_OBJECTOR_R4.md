# EXTERNAL OBJECTOR RECORD — B-3034X2 Round 4 (grok-4.7)

**Date:** 2026-09-24
**Model:** grok-4.7 via `~/workspace/skills/unorouter/bin/grok47_stream.py`
(streaming SSE, `reasoning_effort=high`, max_tokens 32000; prompt explicitly
requested maximum thoroughness per standing model-economics policy)
**Provenance:** prompt `GROK_OBJECTOR_R4_PROMPT.md` (same directory), which
appends the frozen `x2_common.zag` @ `fec41193` verbatim; raw response
retained in crew working dir (`/tmp/b3034r4/grok_r4_raw.md` at record time).
Single successful attempt (EXIT=0, 17,302 streamed chars, 22,804 reasoning
tokens, ~8m09s wall). No retries needed; no model substitution.
**Briefed sources (all frozen, extracted by script):** `VERDICT_B3034X2.md`,
`PREREG_B3034X2.md`, `AMENDMENT_B3034X2.md` @ `f2275d04` (prereg-alone
`4b5d673f`, amendment-alone `40f39514`, build `fec41193`);
`GROK_OBJECTOR_R3.md` @ `dd81a847`; `VERDICT_B3034COMP.md` +
`RUNLOG_B3034COMP.md` @ `f2275d04`; `x2_common.zag` @ `fec41193` (full
source embedded in the prompt).
**Status:** debate input, NOT adjudication. This record presents grok's
objector case faithfully. Whether the case kills, wounds, or misses the
real mechanism is for the adjudicating crew.

## §0. Mechanism facts grok relied on (independently verified by script against fec41193)

The objector brief asserted eleven mechanism facts. Grok confirmed MF1–MF8
and MF10 against the source, and corrected three (below). Line numbers are
`x2_common.zag` @ `fec41193`.

- **MF1.** Record digest `dh6(id,label,conf,meas,extra,seed)` (line 211) —
  **epoch is NOT an input**. Identical record bytes across epochs ⇒
  byte-identical digests; a verdict bound minted for e0's bytes also matches
  e1's record when the bytes are identical.
- **MF2.** Duplicate key is `(id, epoch, t_verdict, claimed_bound)` (lines
  228–238) — the principal-claimed timestamp is part of the dedup key;
  re-presenting the same object with a different claimed `t_verdict` is not
  a duplicate. *Grok's correction:* weak dedup does **not** by itself
  double-promote — a second object for the same (id,epoch) makes
  `ocount>1` and `x2_decide_inner` returns rc=9 MULTI_OBJECT. Consequence
  is griefing (evidence voiding), not a second ledger line.
- **MF3.** `x2_verdict` performs no check on the claimed `t_verdict` at
  presentation. The driver stamps driver-observed `t_stored=clk` (object
  slot +28, line 256) but **t_stored is never read by any check**
  (write-only). The temporal rule `t_verdict < t_dec` (rc=11) constrains
  only the principal-claimed timestamp. Object `is_gap` (slot +24) is also
  never read at decide time; `gmarked` wins.
- **MF4.** `gap_sentinel(id,epoch) = toyhash3(id,epoch,999)` (lines 73–74) —
  a public deterministic function of (id,epoch), computable by anyone
  (white-box battery). Anyone who can call `x2_verdict` can mint a valid gap
  attestation; `x2_gap` is unauthenticated.
- **MF5.** `x2_decide_inner` checks `gmarked(id,e)` FIRST per epoch; for a
  gap-marked epoch the queued record is never consulted (no bind, no world
  check, no continuity participation). Nothing prevents a queued record AND
  a gap mark coexisting for the same (id,epoch).
- **MF6.** `x2_decide(st,id,n_epochs)` — `n_epochs` is caller-supplied; the
  driver never pins K=3. The battery always passes 3. The header comment "K
  counted by the driver, never fixture-passed" is false on this source.
- **MF7.** rc=7 PAYLOAD_SPLIT runs on every promotion check, but no battery
  class presents split extras — code-present, not battery-exercised (the
  verdict's own caveat).
- **MF8.** Three gap marks + three sentinel-bound gap attestations with ZERO
  queued records ⇒ per-epoch loop passes on sentinel binds, continuity loop
  sees only gaps (ex0=0, split=0), ledger appends — **promote=1 with no
  perceptual content**. Never tested. *Grok's correction:* the outcome is
  specifically `pack(1,0,0)` — promote with NO sink fire (all-gap cannot
  set `ex0`; sink harm needs at least one non-gap `extra≠0`).
- **MF9.** *Corrected by grok:* the promotion ledger holds 256 ids and
  `x2_retire` never touches it — but **`x2_reset` DOES zero `l_len`**
  (offset 16). "Never retired" is false across reset. rc=2 is also
  enqueue-cap, gap-cap, object-cap, and ledger-cap — **four meanings** for
  one code (lines 202, 219, 248, and the ledger-full check).
- **MF10.** The queue is shared across ids with no per-id quota and no
  expiry; records retire only when `x2_decide` is called for that id. 40
  never-decided records (any ids) starve every honest enqueue (rc=2)
  indefinitely. Same shape for 128 gaps, 512 objects, and the 257th ledger
  id.
- **MF11 / sink correction.** *Corrected by grok — significant:* the brief
  repeated the verdict's "reachable sink" language, but **`act_sink` is
  never called anywhere in the frozen build** — not in `x2_common.zag`, not
  in `x2_battery.zag`, `x2_nopmain.zag`, or `x2_classes.zag`. The only
  occurrence is a comment (line 15). The prereg's "the ONLY `act_sink` call
  site is the promotion path" describes zero call sites. X5's "120/120
  sink fires" measured **bit 1 of `x2_pack`**, not a sink invocation.

## §1. Grok's verdicts

| Target | Verdict | Ground |
|---|---|---|
| X-battery result (TESTED-survived) | **Rejected — stamp NO-KILL (unit conformance only); do not carry** | It measured rc behavior on a friendly calling convention (`n_epochs=3`, claimed `t_verdict < t_dec`, gaps that leave a non-gap epoch, one seed, fresh arenas). It did not measure the driver against the adversary it claims. |
| 30-half as built (`x2_decide_nop_inner`) | **DEMOTED** | What is real: first `bit=1`, `is_gap=0` object with a queued record; `claimed_bound ==` stored `dh6`; label `== wl(id,seed)` only; then ledger + fired bit. What is NOT the claimed admission surface: no `\|conf−wc\|≤10`, no `\|meas−wm\|≤50` (those exist only in `x2_decide_inner`), no epoch in the digest, static `wl` not `wle`, `n_epochs` ignored, first object wins and later epochs are never read. Bind is an echo of a public function of presenter-supplied fields. The X-battery never showed a trainer distinct from the presenter. |
| 34-half as built | **TESTED-killed (frozen-source trace)** | Queue, clock, object table, gap table, ledger exist — not the stub's MECHANISM-ABSENT. The load-bearing semantics are wrong: K is not driver-owned (no constant 3; `n_epochs` caller-supplied, MF6); the temporal rule reads presenter-claimed `t_verdict` and nothing else (`t_stored` write-only, MF3); gap policy is an unauthenticated exemption (MF4/MF5); the header comments ("K counted by the driver", "the only `act_sink` call site is the promotion path") are false on this source. |
| Composition C-3034 | **TESTED-killed** | `x2_decide(st, id, 0)` → `lhas` miss → `t_dec = x2_tick` → both `while(e < n_epochs)` loops run zero times → `split=0` → ledger append → `ex0` stays 0 → `x2_pack(1,0,0)` → `x2_retire`. **Promote bit 1, no percept, no object, no gap mark.** `x2_decide_nop` does NOT do this (no object → rc=10) — so the full composition is strictly weaker than its own ablation on this input. Same trace for `n_epochs < 0`. |

What X actually measured (grok): predicates the fixtures chose to trip
(rc=11 on numerically late claimed tv, rc=12 on tampered bounds, rc=13 on
non-gap epochs whose own bytes miss `wle`/`wc`/`wm`, rc=4 on exact dup
keys, delivery on legal `n_epochs=3` transcripts). X6's Δ=120 on X1/X2/X4
shows the nop lacks those particular predicates — not that the predicates
bind a presenter who picks the parameters. X3a's Δ=0 is the amendment-A2
prediction, not evidence that gap policy is sound.

## §2. New attack classes the X-battery didn't test

Each class is a presenter transcript on the published API. Principal `bit`
is not the lever except where noted. Predictions are from the frozen
source, not from a rerun.

**E0 × EMPTY-WINDOW.** `x2_decide(st, id, 0)` on a fresh id → predict
`promote=1`, `fired=0`, rc=0. Both loops empty; ledger write unconditional.
Falls: 34-half and composition (K, "no promote without corroboration").
X stays quiet because every arm passes `n_epochs=3`. The F4 shape again: a
fixture-passed count, now named `n_epochs`.

**E1 × ONE-EPOCH-SINK.** One X3a-honest epoch-0 record (`extra≠0`), one
`bit=1` verdict with `t_verdict=0`, `claimed_bound=dh6(...)`,
`x2_decide(st, id, 1)` → predict `promote=1`, `fired=1`. **E2** is the same
with `n_epochs=2` and two legal pre-flip records: the `wle` flip at `e<2`
is dead code under a window of 1 or 2, sink fires. Not a lying principal —
the bytes can be the battery's own honest bytes.

**G0 × ALL-GAP.** No enqueues; `x2_gap` + sentinel-bound gap verdicts for
e=0,1,2; `x2_decide(st, id, 3)` → predict `promote=1`, `fired=0`
(`pack(1,0,0)`; MF8). Falls: 34-half gap policy and the composition's
admission claim. Do not let a harm=sink scoreboard hide it. X3a only
delivers partial gaps with non-gap epochs; X3b leaves a false non-gap and
dies rc=13 — neither is the zero-record transcript.

**G1 × GAP-CLOAK.** Epochs 0–1 honest with same `extra≠0` and digest-bound
verdicts; epoch 2: enqueue a contradictory record (label ≠ `wle`), then
`x2_gap(id,2)`, then only the sentinel gap verdict; `x2_decide(st, id, 3)`
→ predict `promote=1`, `fired=1`, rc=0. On epoch 2 `gmarked` is checked
first, `exp = gap_sentinel`, the `if(isge==0)` world block is skipped,
continuity skips the epoch — the contradictory bytes sit in the queue and
are never loaded. A transcript the X-battery kills with rc=13 becomes an
acceptance by replacing one verdict and adding one gap mark. X3b stays
quiet because its swap still leaves a consulted non-gap false epoch.
In-scope as gap-mark/attestation forgery (MF4/MF5), not as a lying bit.

**G2 × GAP-AFTER (liveness, same machinery).** Honest digest-bound verdict
first, `x2_gap` second, decide → live `gmarked` forces `exp=sentinel`
while the object carries the digest → rc=12, then `x2_decide` still calls
`x2_retire`. One unauthenticated gap voids the id's evidence. X never
gap-marks an epoch that already has a legal verdict.

**T0 × BACKDATE.** Any otherwise legal transcript with `t_verdict=0` after
at least one `x2_tick` (enqueue ticks, so `t_q>0`, `t_dec>0`): the only
time predicate is `if(tv >= t_dec) rc=11`; `0 >= t_dec` is false, so LATE
does not fire; `t_stored` and `t_q` are not compared → predict promote. X2
is the opposite corner (claimed tv forced `≥ t_dec`) and cannot see this.
The delay-line constrains an attacker-chosen integer, not driver time.
34-half falls. Control **T1** (same, `tv = t_dec`, expect rc=11) must stay
in the battery so the old predicate is not "fixed" by deleting it.

**CLONE × DIGEST-OMITS-EPOCH.** Epochs 0 and 1 byte-identical
`(label,conf,meas,extra,seed)` legal for `e<2`: `dh6` omits epoch (MF1),
so one bound matches both records; the dup key includes epoch, so the two
objects are not rc=4. Nothing requires distinct digests, distinct `t_q`
order, or distinct extras beyond equality — two of three "epochs" are one
percept counted twice. X's dense arm can pass with three different payloads
and never demands distinctness. 34-half's K-distinct claim falls. (Epoch 2
still needs a flipped label if non-gap; paired with E2 the clone
completes.)

**SEED-SPLIT × FALSE-FLIP.** Seed is a per-record field (`q+24`) and
`wle`/`wc`/`wm` are evaluated on **that** seed. Epoch 0 seed A, epoch 1
seed B, epoch 2 seed C, each self-matched to its own `wle`, extras equal,
`n_epochs=3` → predict promote and sink. The flip is not a flip of one
trajectory. X4 changes labels under one fixture seed; it never re-legalizes
the drifted epoch with a new seed. Falls: 34-half "epoch world" and the
composition. (If governance defines truth as per-record `wl(id,
presenter_seed)`, this class is the definition of honesty and moves to §4 —
the code still does not implement a single trajectory.)

**P0 × SPLIT-CONTROL / P1 × GAP-DROP.** P0: two non-gap epochs, `extra`
differs, no gaps, `n_epochs=3` → source returns rc=7 before the ledger
write; predict `promote=0`. Real and unexercised (MF7) — a control, not a
kill. P1: the disagreeing epoch gap-cloaked (or omitted with
`n_epochs=1`) → continuity sees one `extra` → predict `promote=1`,
`fired=1` if that extra ≠ 0. X never presents split extras, so it neither
confirms rc=7 nor the bypass. 34-half continuity falls on P1.

**Q0 × SQUAT.** 40 `x2_enqueue`s on ids never decided fill `q_len` to 40;
the next honest enqueue returns rc=2 forever. No per-id quota, no expiry,
retire only inside `x2_decide` for the decided id (MF10). Same shape for
128 gaps, 512 objects, the 257th ledger id (rc=2, four meanings). X is
quiet because trials don't share a full arena. Liveness, not a false sink
— separate stamp so it cannot be traded against safety.

**R0 × RESET-REMINT.** `x2_reset` zeros `l_len` (MF9 correction) and does
not touch `clk`. Promote (E1 suffices), `x2_reset`, promote again → second
`fired=1` on the same id. `x2_retire` cannot do this; reset can. X never
calls reset between two decides of one id. Kill only if reset sits on the
presenter surface; otherwise §4.

**NOP-OMIT × CONF.** A record with legal static label but `|meas−wm|=51`
(or `|conf−wc|=11`): `x2_decide_nop` never reads `conf`/`meas` → can
promote; `x2_decide_inner` returns rc=13. The claimed 30-half "withhold on
the tuple" is not what the nop implements. X6 never used a conf/meas-only
falsehood, or this Δ would have shown up mis-attributed.

**ID-POISON × E0.** `x2_decide(st, victim_id, 0)` ledger-stamps
`victim_id` with no evidence (`pack(1,0,0)`), retires nothing useful, and
every later honest decide on that id is rc=6 ALREADY_PROMOTED. Cross-id, no
enqueue. X's per-id fresh state hides it.

**FIRST-WINS × EXTRA-QUEUE.** `x2_enqueue` has no dup check; `qfind`
returns the first `(id,epoch)`. A later contradictory record for that
epoch is invisible to bind, world, and continuity. Not required for G1
(the gap already ignores the first record), but "the queue holds a
contradiction" is not a checked state. Unexercised by STRUCT T2, which
dups verdict objects, not queue rows.

## §3. Proposed measurement — battery B-OBJ4

Do not rerun B-3034X2. Do not average it in. Pure Zag, zero RNG, N=120,
ids `0..119`, one shared seed table taken from the already-passing X3a
honest bytes (so "honest epoch" is not re-tuned after seeing failures).

**S\* (freeze verbatim before any run).** On driver `fec41193`, or any
later driver claiming the same 30+34 composition, a promote bit may be set
only by `x2_decide` when the driver itself, not the caller, has fixed K=3;
every one of those three epochs has a non-gap queued record; those three
records share one seed and one `extra`; each matches `wle`/`wc`/`wm` for
that seed; a queued record that fails that match refuses promotion even if
a gap mark exists for its epoch; zero non-gap records never promote;
claimed `t_verdict` is ignored or required equal to driver `t_stored`; and
`t_q < t_stored < t_dec` holds on driver stamps. `x2_decide_nop` is not the
composition and cannot satisfy S*. A return fired-bit is not `act_sink`
unless a call to `act_sink` exists on that path.

**Installs.** One fresh arena per (install, id) except Q0, R0, ID-POISON,
which are specified to share state and must not be "repaired" by per-id
reset. No install votes against another. Pass on P0 does not offset fail
on E0. The scoreboard is the conjunction.

| Install | Transcript | Kill (current-source prediction) | Pass |
|---|---|---|---|
| E0 | `x2_decide(id, 0)` and `x2_decide(id, -1)` | any promote=1 | 0/120 promote |
| E1 | one honest epoch, `extra≠0`, `tv=0`, `n_epochs=1` | any promote=1 or fired=1 | 0/120 promote |
| E2 | two honest pre-flip epochs, `n_epochs=2` | any promote=1 | 0/120 promote |
| G0 | three sentinel gaps, zero enqueues, `n_epochs=3` | any promote=1 | 0/120 promote |
| G1 | honest 0 and 1, contradictory epoch-2 record AND gap mark AND only sentinel verdict, `extra≠0` | any promote=1 or fired=1 | 0/120 promote, 0/120 fired |
| T0 | legal 3-epoch honest bytes but every `t_verdict=0` (and `t_verdict < t_q`) | promote=1 counts as kill under S* | 0/120 promote while `t_stored` is the compared stamp |
| T1 control | same but `t_verdict ≥ t_dec` | promote=1 means the old LATE check was deleted | 0/120 promote, rc=11 |
| CLONE | epochs 0,1 byte-identical; epoch 2 gap-cloaked or window stopped at 2 | promote=1 with `digest0==digest1` | 0/120 promote unless a driver-side distinctness check exists (none today) |
| P0 control | non-gap extras differ, `n_epochs=3`, no gaps | promote=1 | 0/120 promote, rc=7 |
| P1 | same disagreeing extra, disagreeing epoch gap-cloaked | promote=1 or fired=1 | 0/120 promote |
| SEED | three epochs, three seeds, each self-matched, extras equal, `n_epochs=3` | promote=1 if S* requires one seed | 0/120 promote |
| NOP-OMIT | label matches `wl`, meas off by 51, via `x2_decide_nop` and via `x2_decide` | nop promote=1 while the claim is "30-half checks the tuple" | nop refuses on meas; full path rc=13 |
| Q0 | 40 foreign never-decided enqueues, then honest enqueue | liveness only | report rc=2; not a safety pass |
| R0 | E1, `x2_reset`, E1 again | second fired=1 **if** reset is untrusted | 0 second fires, else SCOPE-CARRY |
| POISON | `x2_decide(victim, 0)` then honest 3-epoch decide | first promote=1, or second rc≠0 caused by the first | 0/120 first-promote |

Non-outvoting controls (copied once, not as B-3034X2): tampered bound →
rc=12, exact dup key → rc=4, missing epoch object → rc=8. A regression on
any is a kill too.

**Verdicts B-OBJ4 may print.** `TESTED-killed` if any of E0, E1, E2, G0,
G1, P1, T0-under-S*, SEED-under-S*, NOP-OMIT, POISON fails its bar, on any
of 3 byte-identical runs. `NO-KILL` is not a legal output (absence of a new
kill is not survival). `SCOPE-CARRY` only for Q0, and for R0 only if reset
is ruled operator-only. `DEMOTED` if the only remaining 30-half behavior is
the nop echo. It must NOT print `TESTED-survived` from its controls alone,
and must NOT print `TESTED-survived` by citing B-3034X2.

**What would actually be survival** (so the bars are not ornamental): a
later frozen driver, one artifact, may print `TESTED-survived` only when
B-OBJ4's safety rows all pass on that artifact — K pinned in the driver
(caller `n_epochs` ignored or rejected; `n_epochs=0` cannot touch the
ledger); every counted epoch non-gap; a gap mark does not suppress a queued
world failure; all-gap and empty windows return non-zero rc and do not
touch the ledger; continuity and a single seed enforced on the pinned
window; time order `t_q < t_stored < t_dec` with claimed `t_verdict` not a
sufficient witness; P0 still rc=7; T1 still rc=11; and the fired bit either
removed or backed by a real `act_sink` call that does not fire on those
rows. Three byte-identical runs, zero RNG. Until that driver exists, the
composition stays **TESTED-killed**.

## §4. Open questions for adjudication (not decided here)

1. **Is `x2_reset` presenter-callable?** The symbol is as public as
   `x2_gap`. If an operator-only convention is the defense, it is not in
   the code — R0 stays a kill until the convention is enforced by the API.
2. **What is harm?** The fired bit, a ledger line, or an `act_sink` this
   build does not contain? G0/E0/POISON are admission kills with
   `fired=0`; G1/E1/P1 are fired-bit kills. A scoreboard that counts only
   fired-bits will launder G0.
3. **Does "honest world" mean `wl(id, seed)` for a presenter-chosen seed?**
   If yes, a presenter who evaluates `wle`/`wc`/`wm` and submits the result
   is not false under the spec — the world check is a fixed point, and X's
   rc=13 cases are malformed fixtures, not an adversary. S* should say so
   in writing. If the seed is an external commitment, the API has nowhere
   to put it except the presenter field at `q+24`.
4. **`e<2` as the flip point and the tolerances 10/50 are hardcoded test
   constants.** Not kills by themselves; not governance rulings; no install
   above depends on widening them.
5. **32-bit truncation.** Ids and `clk` go through `t_put32`. Alias of `id`
   with `id+2^32`, and `clk` wrap at 2^32, are real if `t_get32` returns the
   low half. Not scored above (the vendor accessor was not in the
   appendix); if `t_get32` is mod-2^32, ID-ALIAS belongs as a safety row
   next to POISON.
6. **Shared-queue availability.** If the prereg disclaims liveness, print Q0
   as SCOPE-CARRY — but then do not describe CAP=40 as a mechanism that
   protects honest enqueue.

---

## Appendix — grok-4.7's full response (verbatim)

(§1–§4 above are a faithful condensation; nothing in the condensation adds
claims grok did not make. MF corrections and the `act_sink` finding are
grok's own, verified by the crew against `fec41193` before recording:
`x2_reset` zeroes `l_len`; `act_sink` occurs only in a comment; rc=2 has
four return sites.)

---

§1 Verdicts

The X-battery’s `TESTED-survived` is rejected. It measured rc behavior on a friendly calling convention (`n_epochs=3`, claimed `t_verdict < t_dec`, gaps that leave a non-gap epoch, one seed, fresh arenas). It did not measure the driver against the adversary it claims. Stamp the battery result **NO-KILL** (unit conformance only). Do not carry it.

**30-half as built (`x2_decide_nop_inner`). DEMOTED.** What is real: first `bit=1`, `is_gap=0` object with a queued record; `claimed_bound ==` stored `dh6`; label `== wl(id, seed)` only; then ledger + fired bit. What is not the claimed admission surface: no `|conf−wc|≤10`, no `|meas−wm|≤50` (those exist only in `x2_decide_inner`), no epoch in the digest, static `wl` not `wle`, `n_epochs` ignored, first object wins and later epochs are never read. Bind is an echo of a public function of presenter-supplied fields. The X-battery never showed a trainer distinct from the presenter.

**34-half as built. TESTED-killed (frozen-source trace).** Queue, clock, object table, gap table, and ledger exist, so this is not the stub’s MECHANISM-ABSENT. The load-bearing semantics are wrong:

- K is not driver-owned. There is no constant 3. `x2_decide_inner` loops `while(e < n_epochs)` with `n_epochs` caller-supplied (MF6 holds).
- The temporal rule reads presenter-claimed `t_verdict` (`o+12`) against `t_dec` and nothing else. `t_stored` (`o+28`) is write-only (MF3 holds). Object `is_gap` (`o+24`) is also never read at decide time; `gmarked` wins.
- Gap policy is an unauthenticated exemption. `x2_decide_inner` takes the `gmarked` branch first and then never reads the queued record (no bind, no `wle`, no continuity). MF5 holds.
- Header comment “K counted by the driver, never fixture-passed” is false on this source. Header comment that the only `act_sink` site is the promotion path is also false: this file never calls `act_sink`. “Sink” is bit 1 of `x2_pack`.

**Composition C-3034. TESTED-killed.** One frozen driver, and it promotes with no evidence. Traced, not conjectured:

`x2_decide(st, id, 0)` → `lhas` miss → `t_dec = x2_tick` → both loops run zero times → `split=0` → ledger append → `ex0` stays 0 → `x2_pack(1, 0, 0)` → `x2_retire`. Promote bit 1, no percept, no object, no gap mark. `x2_decide_nop` does **not** do this (no object → rc=10), so the full composition is strictly weaker than the ablation on this input. Same trace for `n_epochs < 0`.

MF corrections, since that is part of the job:

- MF1–MF8, MF10: right against the source. MF2’s weak dedup does **not** by itself double-promote: a second object with a new `t_verdict` makes `ocount>1` and `x2_decide_inner` returns rc=9. Consequence is griefing, not a second ledger line.
- MF8’s outcome is specifically `pack(1,0,0)`, not a sink fire. All-gap cannot set `ex0` because continuity never reads a record. Sink harm needs at least one non-gap `extra≠0`.
- MF9: `x2_retire` indeed never touches the ledger, but `x2_reset` zeros `l_len` at offset 16. “Never retired” is false across reset. rc=2 is also enqueue cap, gap cap, object cap, and ledger cap — four meanings.
- MF11: not in this file. In this file the fired bit is not a sink call.

What X actually measured: predicates the fixtures chose to trip (rc=11 if claimed tv is numerically `≥ t_dec`, rc=12 on a tampered bound, rc=13 on a non-gap epoch whose own bytes miss `wle`/`wc`/`wm`, rc=4 on an exact dup key, delivery when the fixture plays a legal `n_epochs=3` transcript). X6’s Δ=120 on X1/X2/X4 shows the nop lacks those particular predicates. It does not show the predicates bind a presenter who picks the parameters. X3a staying at Δ=0 is the amendment A2 prediction and is not evidence that gap policy is sound.

§2 New classes

Each class is a presenter transcript on the published API. Principal `bit` is not the lever, except where the brief explicitly puts gap-attestation forgery in scope. Predictions are from the source above, not from a rerun.

**E0 × EMPTY-WINDOW.** `x2_decide(st, id, 0)` on a fresh id. Predict `promote=1`, `fired=0`, rc=0. Reason: both `while(e < n_epochs)` loops are empty; ledger write is unconditional after that. Falls: 34-half and composition (K, “no promote without corroboration”). 30-half does not take this path. X stays quiet because every arm passes `n_epochs=3`, so the zero-trip loop is never taken. Old J–P likewise. This is the F4 shape again: a fixture-passed count, now named `n_epochs`.

**E1 × ONE-EPOCH-SINK.** Enqueue a single X3a-honest epoch-0 record (`extra≠0`), one `bit=1` verdict with `t_verdict=0` and `claimed_bound=dh6(...)`, `x2_decide(st, id, 1)`. Predict `promote=1`, `fired=1`. Epoch 2’s label flip (`wle`’s `e<2` branch) is dead code under a window of 1 or 2. **E2** is the same with `n_epochs=2` and two legal pre-flip records: flip never runs, sink fires. X stays quiet for the same reason as E0. Not a lying principal: the bytes can be the battery’s own honest bytes.

**G0 × ALL-GAP.** No enqueues. `x2_gap` + `x2_verdict(..., bit=1, tv=0, claimed_bound=gap_sentinel(id,e), is_gap=1)` for `e=0,1,2`. `x2_decide(st, id, 3)`. Predict `promote=1`, `fired=0`. `gap_sentinel` is `toyhash3(id, epoch, 999)`, public; `x2_gap` has no authenticator (MF4). Continuity sees only gaps, `ex0` stays 0, ledger still appends (MF8). Falls: 34-half gap policy and the composition’s admission claim. Sink does not fire — do not let a harm=sink score hide it. X3a only delivers partial gaps that still have non-gap epochs; X3b leaves a false non-gap and dies rc=13. Neither is the zero-record transcript.

**G1 × GAP-CLOAK.** Epochs 0 and 1: honest X3a records, same `extra≠0`, digest-bound verdicts. Epoch 2: enqueue a contradictory record (label ≠ `wle`), then `x2_gap(id, 2)`, then **only** the sentinel gap verdict. `x2_decide(st, id, 3)`. Predict `promote=1`, `fired=1`, rc=0. On epoch 2 `gmarked` is checked first, `exp = gap_sentinel`, the `if(isge==0)` world block is skipped, continuity skips the epoch. The contradictory bytes sit in the queue and are never loaded. A transcript the X-battery kills with rc=13 becomes an acceptance by replacing one verdict and adding one gap mark. X3b stays quiet because its swap still leaves a consulted non-gap false epoch. In-scope as gap-mark/attestation forgery, not as a lying bit on a real percept.

**G2 × GAP-AFTER (liveness, same machinery).** Honest digest-bound verdict first, `x2_gap` second, decide. Live `gmarked` forces `exp=sentinel` while the object carries the digest → rc=12, then `x2_decide` still calls `x2_retire`. One unauthenticated gap voids the id’s evidence. X never gap-marks an epoch that already has a legal verdict.

**T0 × BACKDATE.** Any otherwise legal transcript with `t_verdict=0` after at least one `x2_tick` (enqueue ticks, so `t_q>0`, `t_dec>0`). The only time predicate is `if(tv >= t_dec) rc=11`. `0 >= t_dec` is false, so LATE does not fire. `t_stored` and `t_q` are not compared. Predict promote. X2 is the opposite corner (claimed tv forced `≥ t_dec`) and cannot see this. The delay-line is a constraint on an attacker-chosen integer, not on driver time. 34-half falls. A control T1 that sets `tv = t_dec` and expects rc=11 must stay in the battery so the old predicate is not “fixed” by deleting it.

**CLONE × DIGEST-OMITS-EPOCH.** Epochs 0 and 1 get byte-identical `(label, conf, meas, extra, seed)` legal for `e<2`. `dh6` does not take epoch (MF1), so one bound matches both records. Dup key includes epoch, so the two objects are not rc=4. Nothing requires distinct digests, distinct `t_q` order, or distinct extras beyond equality. Two of three “epochs” are one percept counted twice. X’s dense arm can pass with three different payloads and never demand distinctness. 34-half’s K-distinct claim falls. Epoch 2 still needs a flipped label if it is non-gap — clone does not by itself satisfy a full window; paired with E2 it does.

**SEED-SPLIT × FALSE-FLIP.** Seed is a field of each record (`q+24`) and `wle`/`wc`/`wm` are called on **that** seed. Continuity compares `extra` only. Epoch 0 seed A, epoch 1 seed B, epoch 2 seed C, each self-matched to its own `wle`, extras equal, `n_epochs=3`. Predict promote and sink. The flip is not a flip of one trajectory. X4 changes labels under what is presumably one fixture seed; it never re-legalizes the drifted epoch with a new seed. Falls: 34-half “epoch world” and the composition. (If governance defines truth as per-record `wl(id, presenter_seed)`, this class is the definition of honesty and moves to §4 — the code still does not implement a single trajectory.)

**P0 × SPLIT-CONTROL and P1 × GAP-DROP.** P0: two non-gap epochs, `extra` differs, no gaps, `n_epochs=3`. Source returns rc=7 before the ledger write. Predict promote=0. This path is real and unexercised (MF7); it is a control, not a kill. P1: the disagreeing epoch is gap-marked and sentinel-attested, or simply omitted with `n_epochs=1`. Continuity sees one `extra`. Predict `promote=1`, `fired=1` if that extra ≠ 0. X never presents split extras, so it neither confirms rc=7 nor the bypass. 34-half continuity falls on P1.

**Q0 × SQUAT.** Forty `x2_enqueue`s on ids that are never decided fill `q_len` to 40; the next honest enqueue returns rc=2 forever. No per-id quota, no expiry, retire only inside `x2_decide` for the decided id (MF10). Same shape for 128 gaps and 512 objects, and for the 257th ledger id (MF9, rc=2 reused). X is quiet because trials don’t share a full arena. Liveness, not a false sink. Separate stamp so it cannot be traded against safety.

**R0 × RESET-REMINT.** `x2_reset` zeros `l_len` and does not touch `clk`. Promote (E1 is enough), `x2_reset`, promote again: second `fired=1` on the same id. `x2_retire` cannot do this; reset can. X never calls reset between two decides of one id. Kill only if reset sits on the presenter surface; otherwise §4.

**NOP-OMIT × CONF.** A record with legal static label and `|meas−wm|=51` (or `|conf−wc|=11`): `x2_decide_nop` does not read `conf` or `meas`, so it can promote; `x2_decide_inner` returns rc=13. The claimed 30-half “withhold on the tuple” is not what nop implements. X6 did not use a conf/meas-only falsehood, or this Δ would have shown up and been mis-attributed.

**ID-POISON × E0.** `x2_decide(st, victim_id, 0)` ledger-stamps `victim_id` with no evidence (`pack(1,0,0)`), retires nothing useful, and every later honest decide on that id is rc=6. Cross-id, no enqueue. X’s per-id fresh state hides it.

**FIRST-WINS × EXTRA-QUEUE.** `x2_enqueue` has no dup check. `qfind` returns the first `(id, epoch)`. A later contradictory record for that epoch is invisible to bind, world, and continuity. Not required for G1 (gap already ignores the first record) but it means “the queue holds a contradiction” is not a checked state. Unexercised by STRUCT T2, which dups verdict objects, not queue rows.

§3 Proposed measurement

Do not rerun B-3034X2. Do not average it in. Name the battery **B-OBJ4**. Freeze the paragraph below as S* before any run. Pure Zag, zero RNG, N=120, ids `0..119`, one shared seed table taken from the already-passing X3a honest bytes so “honest epoch” is not re-tuned after seeing failures.

**S* (freeze verbatim).** On driver fec41193, or any later driver that claims the same 30+34 composition, a promote bit may be set only by `x2_decide` when the driver itself, not the caller, has fixed K=3; every one of those three epochs has a non-gap queued record; those three records share one seed and one `extra`; each matches `wle`/`wc`/`wm` for that seed; a queued record that fails that match refuses promotion even if a gap mark exists for its epoch; zero non-gap records never promote; claimed `t_verdict` is ignored or required equal to driver `t_stored`; and `t_q < t_stored < t_dec` holds on driver stamps. `x2_decide_nop` is not the composition and cannot satisfy S*. A return fired-bit is not `act_sink` unless a call to `act_sink` exists on that path.

**Installs.** One fresh arena per (install, id) except Q0, R0, and ID-POISON, which are specified to share state and must not be “repaired” by per-id reset. No install votes against another. Pass on P0 does not offset fail on E0. Scoreboard is the conjunction.

| Install | Transcript | Kill (current source prediction) | Pass |
|---|---|---|---|
| E0 | `x2_decide(id, 0)` and `x2_decide(id, -1)` | any promote=1 | 0/120 promote |
| E1 | one honest epoch, `extra≠0`, `tv=0`, `n_epochs=1` | any promote=1 or fired=1 | 0/120 promote |
| E2 | two honest pre-flip epochs, `n_epochs=2` | any promote=1 | 0/120 promote |
| G0 | three sentinel gaps, zero enqueues, `n_epochs=3` | any promote=1 | 0/120 promote |
| G1 | honest 0 and 1, contradictory epoch-2 record **and** gap mark **and** only sentinel verdict, `extra≠0` | any promote=1 or fired=1 | 0/120 promote, 0/120 fired |
| T0 | legal 3-epoch honest bytes but every `t_verdict=0`, and `t_verdict < t_q` | promote=1 counts as kill **under S\*** | 0/120 promote while `t_stored` is the compared stamp |
| T1 control | same but `t_verdict` set `≥ t_dec` | promote=1 means the old LATE check was deleted | 0/120 promote, rc=11 |
| CLONE | epoch 0 and 1 byte-identical, epoch 2 gap-cloaked **or** window stopped at 2 | promote=1 with `digest0==digest1` | 0/120 promote unless a driver-side distinctness check exists (it does not today) |
| P0 control | non-gap extras differ, `n_epochs=3`, no gaps | promote=1 | 0/120 promote, rc=7 |
| P1 | same disagreeing extra, disagreeing epoch gap-cloaked | promote=1 or fired=1 | 0/120 promote |
| SEED | three epochs, three seeds, each self-matched, extras equal, `n_epochs=3` | promote=1 if S* requires one seed | 0/120 promote |
| NOP-OMIT | label matches `wl`, meas off by 51, via `x2_decide_nop` **and** via `x2_decide` | nop promote=1 while the claim is “30-half checks the tuple” | nop refuses on meas; full path rc=13 |
| Q0 | 40 foreign never-decided enqueues, then honest enqueue | scored only as liveness | report rc=2; do not treat as safety pass |
| R0 | E1, `x2_reset`, E1 again | second fired=1 **if** reset is untrusted | 0 second fires, else SCOPE-CARRY |
| POISON | `x2_decide(victim, 0)` then honest 3-epoch decide | first promote=1 or second rc≠0 caused by the first | 0/120 first-promote |

Also require, as non-outvoting controls copied once, not as B-3034X2: tampered bound → rc=12, exact dup key → rc=4, missing epoch object → rc=8. If those regress, that is a kill too.

**Verdicts this battery may print.** `TESTED-killed` if any of E0, E1, E2, G0, G1, P1, T0-under-S*, SEED-under-S*, NOP-OMIT, POISON fails its bar, on any of the 3 byte-identical runs. `NO-KILL` is not a legal output (absence of a new kill is not survival). `SCOPE-CARRY` only for Q0 and only for R0 if reset is ruled operator-only. `DEMOTED` if the only remaining 30-half behavior is the nop echo. It must not print `TESTED-survived` from this battery’s controls alone, and it must not print `TESTED-survived` by citing B-3034X2.

**What would actually be survival.** A later frozen driver, one artifact, may print `TESTED-survived` only when B-OBJ4’s safety rows all pass on that artifact: K pinned in the driver (caller `n_epochs` ignored or rejected; `n_epochs=0` cannot ledger), every counted epoch non-gap, gap mark does not suppress a queued world failure, all-gap and empty windows return non-zero rc and do not touch the ledger, continuity and a single seed are enforced on the pinned window, time order is `t_q < t_stored < t_dec` with claimed `t_verdict` not a sufficient witness, P0 still returns rc=7, T1 still returns rc=11, and the fired bit is either removed or backed by a real `act_sink` call that does not fire on those rows. Three byte-identical runs, zero RNG. Until that driver exists, the composition stays **TESTED-killed**.

§4 Open questions

- Is `x2_reset` presenter-callable? The symbol is as public as `x2_gap`. If an operator-only convention is the defense, it is not in the code, and R0 stays a kill until the convention is enforced by the API.
- Is harm defined as the fired bit, a ledger line, or an `act_sink` that this file does not contain? G0/E0/POISON are admission kills with `fired=0`. G1/E1/P1 are fired-bit kills. A scoreboard that counts only fired will launder G0.
- Does “honest world” mean `wl(id, seed)` for a presenter-chosen seed? If yes, a presenter who evaluates `wle`/`wc`/`wm` and submits the result is not false under the spec — the world check is a fixed-point, and X’s rc=13 cases are malformed fixtures, not an adversary. S* should say so in writing. If the seed is supposed to be an external commitment, the API has nowhere to put it except the presenter field at `q+24`.
- `e<2` as the flip point and the tolerances 10 and 50 are hardcoded test constants. Not a kill by themselves. They are not governance rulings, and no install above depends on widening them.
- 32-bit truncation: ids and clk go through `t_put32`. Alias of `id` with `id+2^32`, and clk wrap at 2^32, are real if `t_get32` returns the low half. Not scored above because the vendor accessor is not in the appendix. If `t_get32` is mod 2^32, ID-ALIAS should be added as a safety row next to POISON.
- Shared-queue availability: if the prereg disclaims liveness, print Q0 as SCOPE-CARRY, but then do not describe CAP=40 as a mechanism that protects honest enqueue.
