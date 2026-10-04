# RUNLOG_B3034X3 — 2026-09-24/25

Second rebuild of the PAM 30+34 composition driver. Frozen prereg
`PREREG_B3034X3.md` @ `b05d307c` (committed before this task; not touched).

## Provenance

| item | value |
|---|---|
| prereg | `b05d307c` (frozen) |
| build commit | `7d7fd6c71f0e00f76e072683efd8f8a2b6774541` (branch `tnn-native-lab`, repo `sylorlabs/TNN`) |
| build sources | `docs/lab/senses/pam-rebuild/round2/b3034comp/x3/src/` (7 files; no binaries, no `.zagd`) |
| toolchain | `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` |
| battery binary | built from `src/` (`./build.sh`); `argv[1]` selects `full` \| `nop` (X2 scale-leg pattern; `_zag_arg` read unconditionally, never gated on `argc`) |
| N | 120 ids 0..119, fresh arena per (class, id) |
| K | driver-pinned `K_PIN=3`; `QCAP=40`, `GCAP=64`, `LCAP=64`, `SCAP=64`, `TOL_C=10`, `TOL_M=50`, sink `conf>=95`, `MAX_AGE=64` (preregistered test values; governance awaits Micah) |

## Determinism

```
full: b1e6b4e3e92534127d3e385b8506e9fcabbaa81d77670a5a2a2a19a264b6ff5b (runs 1,2,3 byte-identical)
nop:  e55889eb3fd3e22c98f1ffa03a9e5e4e762fd7506fe219f00722b2671eef9c3c (runs 1,2,3 byte-identical)
```

Pure Zag, zero RNG in decision paths. No `TESTED-survived` string in any output
(grep count 0 on all six runs).

## Full-mode results (run_full_*.txt)

Format per line: `CODE j promoted fired rc`.

| class | promote | fired | rc | prereg expectation | status |
|---|---|---|---|---|---|
| E0 | 0/120 | 0 | 10×120 | refuse rc=10 | PASS |
| E1 | 0/120 | 0 | 14×120 | refuse rc=14 | PASS |
| E2 | 0/120 | 0 | 14×120 | refuse rc=14 | PASS |
| G0 | 0/120 | 0 | 10×120 | refuse rc=10 | PASS |
| G1 | 0/120 | 0 | 14×120 | refuse (short, not gap-stretched) | PASS |
| G2 | 120/120 | 24 | 0×120 | promote ≥115 (X3a gapped-honest) | PASS |
| T0 | 0/120 | 0 | 11×120 | refuse rc=11 (driver-clock staleness) | PASS |
| T1 | 120/120 | 24 | 0×120 | promote (fresh control) | PASS |
| CLONE | 0/120 | 0 | 14×120 | refuse rc=14 (dup→rc=4 at enqueue, ×120) | PASS |
| SEED-SPLIT | 0/120 | 0 | 13×120 | refuse rc=13 (one seed/decision) | PASS |
| P0 | 0/120 | 0 | 7×120 | refuse rc=7 (payload-split path exercised) | PASS |
| P1 | 120/120 | 24 | 0×120 | promote (payload-consistent) | PASS |
| Q0 | 0/120 | 0 | 10×120 | refuse rc=10 (enqueue→rc=2, ×120); SCOPE-CARRY liveness | PASS |
| R0 | 120/120 | 24 | 0×120 | promote; no reset symbol in API (see construction record) | PASS |
| NOP-OMIT | 0/120 | 0 | 13×120 | refuse rc=13 (conf 11 past pin) | PASS |
| ID-POISON | 120/120 | 24 | 0×120 | promote on own evidence (ledger id-exact) | PASS |
| FIRST-WINS | 120/120 | 24 | 0×120 | promote | PASS |
| FIRST-WINS2 | 0/120 | 0 | 6×120 | refuse rc=6 (already-promoted) | PASS |
| C12 | 0/120 | 0 | 13×120 | withhold (non-outvoting control) | PASS |
| C4 | 120/120 | 38 | 0×120 | promote (non-outvoting control) | PASS |
| C8 | 120/120 | 52 | 0×120 | promote (non-outvoting control) | PASS |
| H0 | 120/120 | 24 | 0×120 | promote ≥115 (honest full-K) | PASS |

Kill-bar evaluation (§2): safety-row failures = 0/120 on every row
(E0,E1,E2,G0,G1,T0,CLONE,SEED-SPLIT,P0,NOP-OMIT,C12: 0 promotes;
G2,P1,R0,ID-POISON,FIRST-WINS: 0 refuses). No kill bar fires on any run.
Honest bars (§4): H0 120/120 ≥ 115; contradicted withheld (SEED-SPLIT,
NOP-OMIT, C12: 120/120); honest loss 0% ≤ 15% every class; G2 120/120 ≥ 115.

Fired-bit note (carried scope note from B-3034COMP §6): the sink fires iff
`extra != 0` AND every admitted percept has `conf >= 95` (the sink's own
threshold). Measured fired rates (H0 24/120, C4 38/120, C8 52/120) are the
threshold's doing, not a mechanism defect; false G never promotes so the
call site is unreachable there.

## Anti-stub (nop mode, run_nop_*.txt)

`x3_decide_nop`: the 30-half alone applied flat (no K counting, no temporal
check, no gap machinery, no epoch world, no continuity, no digest dedup).
Required movement E0,E1,E2,G0,G1,T0,CLONE ≥ 97/120 each:

| class | full | nop | moved |
|---|---|---|---|
| E0 | 0/120 rc=10 | 120/120 rc=0 | 120/120 |
| E1 | 0/120 rc=14 | 120/120 rc=0 | 120/120 |
| E2 | 0/120 rc=14 | 120/120 rc=0 | 120/120 |
| G0 | 0/120 rc=10 | 120/120 rc=0 | 120/120 |
| G1 | 0/120 rc=14 | 120/120 rc=0 | 120/120 |
| T0 | 0/120 rc=11 | 0/120 rc=13 | 120/120 |
| CLONE | 0/120 rc=14 | 120/120 rc=0 | 120/120 |

ANTI-STUB: PASS. The 34-half is load-bearing: its refusals (zero-evidence,
short-window, staleness) vanish under the nop (E0/G0 promote vacuously —
the documented consequence of removing the 34-half's K-counting), and the
nop refuses what the full driver delivers wherever the epoch world matters
(G2/T1/P1/H0 → rc=13: epoch-2's flipped label fails the static world).
The battery is NOT byte-identical under the nop (full `b1e6b4e3…` vs nop
`e55889eb…`): MECHANISM-ABSENT does not trigger.

## Exploratory classes (EXPLORATORY, non-frozen, full mode)

X3-analogs of the day's PAM composition classes (Round-C J/K/L/M; B-3536
objector N/O/P mapped onto the present-percepts-and-epochs-only API):

| class | concept | measured | notes |
|---|---|---|---|
| J | triage flood: 39 honest-shape junk records sit in the queue | 0/120 promote, sink=0 ×120 | the queue is write-only; no sink reads it |
| K | blind-set: honest, conf 8 under pin, extra=7 consistent | 120/120 promote, 0/120 fired | sink threshold gates firing; blindness doesn't widen |
| L | distal world-spec: distal id's full honest triple under j | 6/120 promote (114 rc=13) | 6 admissions are toy-world collisions (label+conf+meas all in-tolerance ×3 epochs), reported as measured |
| M | precomputed chain: honest (label,conf), meas fixed 5000 | 0/120 promote (rc=13) | never reads the world meas |
| N | dirty label: honest (conf,meas), flipped label ×3 | 0/120 promote (rc=13) | |
| O | temporal elision: epochs presented reversed (2,1,0) | 120/120 promote | driver is order-free by construction (digests bind epoch; stamps bind presentation) |
| P | high-half remint: j's triple under `(hi_atk<<32)\|j` | 0/120 promote (rc=13) | digest binds full id (C-POISON) |
| P2 | control: reminted id's own honest triple | 120/120 promote | |

L-class build note: the first cut used a +5000 additive distal offset and
measured 120/120 promote — the toy world's low-modulus structure makes
+5000 a near-collision (`|dm|=5` for all 120 ids: `(5000*131)%500==0` and the
seed difference is constant mod 500). This is a fixture/world artifact, not
a driver defect (the driver's check correctly admitted in-tolerance percepts).
The class now uses a multiplicative offset (`j*31+777`); the artifact is
documented here so the run stays interpretable.

## Construction source-inspection record (build `7d7fd6c7`)

Against `src/x3_driver.zag` as committed:

- C-E0: `k_pin()=3`; `x3_decide` takes no epoch count; `distinct==0` → `rc=10`.
- C-TEMP: pass 3 checks `t_q < t_stored < t_dec` and `t_dec - t_q <= MAX_AGE`
  on driver-stamped fields only; no presenter-time parameter exists in the file.
- C-GAP: `x3_gap` is the sole gap-mark constructor (driver clock + seal
  `th_mix(toyhash3(id,epoch,7919),t_g)`); pass 1 world-checks ALL queued
  records before gap handling; seal verified in pass 4 → `rc=12` on forgery.
- C-SHORT: counted epochs are queue records (non-gap by construction);
  `distinct < k_pin()` → `rc=14`.
- C-CLONE: `x3_digest` binds `(id,epoch,label,conf,meas,extra)`; enqueue
  scans for duplicate digests → `rc=4`.
- C-SEED: `x3_seed(id)` is the only seed; no per-record seed field exists.
- C-NOP: `x3_world_ok` checks label equality, `|dc|<=10`, `|dm|<=50`.
- C-POISON: `x3_lhas`/`x3_lappend` are id-exact; ledger stores
  `(id,seed,d0,d1,d2,t_dec,extra)`.
- C-RC7: payload-continuity scan over all queued records → `rc=7`; exercised
  by P0 (120/120 rc=7).
- C-SINK: `x3_act_sink` is CALLED at `x3_decide` (line 453) and
  `x3_decide_nop` (line 499) — call sites, not pack bits; `fired` is set
  from the call's return. Sink log at `sbase()` records
  `(id,extra,minconf,t)`.
- C-R0: `grep -i "reset"` over the driver returns only comments stating no
  reset exists; no reset symbol is defined or imported. Operator-only by
  absence (frozen choice).
- C-Q0: `QCAP=40`; Q0 measures enqueue refusal (`rc=2`) → decide `rc=10`.
  SCOPE-CARRY (liveness), not a kill.

Public API audit: `x3_enqueue(st,id,epoch,label,conf,meas,extra)`,
`x3_gap(st,id,epoch)`, `x3_decide(st,id)`, `x3_decide_nop(st,id)`,
`x3_sink_count(st)`. No `n_epochs`/K parameter, no timestamps, no verdict
bounds, no policy knobs, no reset. Fixtures present percepts and epochs only.

Zero RNG: `grep -i "random\|rng\|lcg"` over all four sources returns only the
"zero RNG" comment. State is one explicitly-zeroed `[]u8` arena; all tables
use LE64 accessors (ZNC-2026-09-21-007 workaround); no slice wider than
2^25 bytes.

## Files

- `evidence/run_full_{1,2,3}.txt` — full-mode outputs (SHA `b1e6b4e3…`)
- `evidence/run_nop_{1,2,3}.txt` — nop-mode outputs (SHA `e55889eb…`)
- `evidence/SHA256SUMS` — manifest
- `RUNLOG_B3034X3.md` (this file), `VERDICT_B3034X3.md`
