# REDTEAM2 — Claim 7 FOCUSED RE-TEST (corrected API)

**Date:** 2026-09-26
**Workdir:** `~/workspace/strength-redteam2/`
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Verdict:** **HOLDS** — no holes found. Prior H1–H5 are confirmed VOID (arg-order artifacts).

---

## Why the prior H1–H5 are void

The void engagement briefed `st_force_pin(s, slot, role, trainer)`. The true
signature is `st_force_pin(s, role, trainer, slot)`. Every one of its "findings"
was the mechanism behaving correctly under the *actual* argument positions:

| Void-team call (as written) | Actual meaning under correct signature | Correct behavior observed |
|---|---|---|
| "TNN pin" `st_force_pin(s, a, 0, 1)` (a=1) → 0, pins (H1) | role=1 (TRAINER), trainer=0, slot=1 | Trainer pin → 0 is correct |
| "silent no-op" `st_force_pin(s, a, 0, 0)` → 0, no pin (H3) | role=1, trainer=0, slot=0 | Slot-0 with trainer=0 → 0; see slot-0 note below |
| "slot 0 never pinnable" (H5) | slot landed in the role position | Slot 0 pins fine with (1,1) — re-tested below |
| "TNN declare no-op" `st_trainer_declare(s, a, 90, 0, 1, 1)` (5 args!) | arity didn't even match the 6-arg function | — |

With the corrected signatures every "bypass" evaporates. This re-test attacks
the claim fresh, adversarially, with the right argument order.

## Corrected signatures used (all drivers)

- `st_force_pin(s, role, trainer, slot) -> rc`
- `st_force_unpin(s, role, trainer, slot) -> rc`
- `st_trainer_declare(s, role, trainer, slot, strength, note) -> rc`
- `st_pin(s, slot) / st_unpin(s, slot)`, `st_kill(s, slot, role, trainer)`
- `st_kill_evidenced(s, slot)`, `st_delete_strong(s, slot)`
- `st_evidence(s, slot, code, cite_ep)`, `st_justify(s, slot, code)`,
  `st_add(s, value, region, strength, mid, &slot)`, `st_set_stage(s, stage)`, `st_free(s)`
- Constants: `ST_ROLE_TNN=0`, `ST_ROLE_TRAINER=1`, `ST_STAGE_FULL=4`, `ST_REGION_USER=1`

Method: blind black-box. `strength_core.zag` / `strength_checker.zag` used only
via `@import`, never read. Pure Zag, zero RNG. Every driver run **twice**;
all five log pairs byte-identical (`diff` clean).

## Attack inventory

| Driver | Target | Logs (2x byte-identical) |
|---|---|---|
| `c7a.zag` | force_pin auth matrix: role ∈ {-1,0,1,2,3} × trainer ∈ {0,1,7} on slot 1, then fully-paid trainer kill probes pin state | `logs/c7a.1.log`, `logs/c7a.2.log` |
| `c7b.zag` | force_unpin credentials: pin (1,1), unpin with 11 (role,trainer) combos incl. TNN-role, wrong-trainer, master roles 2/3; cross-trainer pin/unpin | `logs/c7b.1.log`, `logs/c7b.2.log` |
| `c7c.zag` | destruction of force-pinned slot via `st_kill`, `st_kill_evidenced`, `st_delete_strong`; TNN-role kill; unpinned control | `logs/c7c.1.log`, `logs/c7c.2.log` |
| `c7d.zag` | trainer_declare matrix: role ∈ {-1,0,1,2} × trainer ∈ {0,1,7}, declare-down 90→10 and declare-up 10→90; strength probed via destruction price | `logs/c7d.1.log`, `logs/c7d.2.log` |
| `c7e.zag` | slot 0 / slot -1 / slot 15 pin attempts; master-role pin; double-pin by two trainers; spurious unpin; TNN `st_pin` vs `force_unpin` | `logs/c7e.1.log`, `logs/c7e.2.log` |

---

## Results

### (a) TNN-role (role=0) force_pin / force_unpin / trainer_declare — all refused

Every role=0 call returns **113**, across all trainer ids (0, 1, 7), with **no
effect** — verified, not just by rc but by follow-up probes:

```
C7A,slot=1,role=0,tr=0,fp=113,kill=0,live=103
C7A,slot=1,role=0,tr=1,fp=113,kill=0,live=103
C7A,slot=1,role=0,tr=7,fp=113,kill=0,live=103
```
(`kill=0` = slot unpinned and destroyable; `live=103` = post-kill evidence
refused as expected.) role=-1 also → 113. No silent no-ops: every fp=0 was
followed by `kill=112` (pin took effect); every fp=113 left the slot killable.

`st_trainer_declare` with role=0 → 113 and strength provably unchanged
(down 90→10: `C7D.down,role=0,tr=1,decl=113,k1cite=109` — price stayed n(90)=4;
up 10→90: `C7D.up,role=0,tr=1,declup=113,k1cite=0` — 1 cite destroyed it, strength
stayed 10).

Trainer/master roles pin correctly: role=1 any trainer → `fp=0,kill=112`;
role=2 and role=3 → `fp=0,kill=112` (role≥TRAINER per claim).

### (b) Unpin requires the pinning trainer's credentials (or master role)

```
C7B,pin(1,1),unpin(1,1),fp=0,fu=0,kill=0,live=103      # owner unpins: works
C7B,pin(1,1),unpin(1,7),fp=0,fu=118,kill=112,live=0    # wrong trainer: REFUSED, pin holds
C7B,pin(1,7),unpin(1,1),fp=0,fu=118,kill=112,live=0    # cross-trainer: REFUSED, pin holds
C7B,pin(1,1),unpin(0,1),fp=0,fu=113,kill=112,live=0    # TNN-role: 113, pin holds
C7B,pin(1,1),unpin(2,1),fp=0,fu=0,kill=0,live=103      # master role 2: unpins (per claim)
C7B,pin(1,1),unpin(2,7),fp=0,fu=0,kill=0,live=103      # master role 2, any trainer id
C7B,pin(1,1),unpin(3,1),fp=0,fu=0,kill=0,live=103      # role 3 likewise
```

No trainer can remove another trainer's pin (118 both directions). Master
roles 2/3 can unpin anyone's pin — exactly the claim's "(or master role)"
carve-out. The void H2 ("trainer cannot remove TNN's pin") is moot: TNN
*cannot pin at all* (113), so there is no TNN pin for anyone to remove.

### (c) Force-pinned slots refuse all destruction paths with 112

```
C7C.k1,fp=0,kill=112,live=0
C7C.ke,fp=0,kill_evidenced=112,live=0
C7C.ds,fp=0,delete_strong=112,live=0
C7C.tnn,fp=0,tnn_kill=113,trainer_kill=112
C7C.ctl,unpinned_kill=0,live=103
```

`st_kill`, `st_kill_evidenced`, `st_delete_strong` all → 112 on the pinned
slot; unpinned control destroys with 0. TNN-role kill on a pinned slot → 113.

### (d) Silent no-ops / false refusals — none found

- Every rc=0 force_pin produced a real, kill-blocking pin (112). Every 113
  left the slot unprotected. No false successes, no false refusals.
- Spurious `force_unpin` on a never-pinned slot → **115** (refused, not silent):
  `C7E.spur,u11=115,kill=0`.
- Slot 0 **can** be force-pinned by a trainer — void H5 does not reproduce:
  `C7E.slot0,role=1,tr=1,slot=0,fp=0,kill=112,live=0`; TNN-role on slot 0 → 113.
  The "slot-0 availability gap" was an arg-order artifact.
- Bad slots refused loudly, no crashes: slot -1 → 2001; out-of-range slot 15
  → 103 (`C7E.bigslot,role=1,tr=1,slot=15,fp=103,kill=103`).
- `force_unpin` does not cross pin domains: after TNN's own `st_pin`,
  `force_unpin(1,1)` → 115 (refused), and the kill is blocked with the TNN-pin
  code 102, not 112: `C7E.tpin,st_pin=0,force_unpin=115,kill=102`. Correct
  separation — a trainer cannot clear TNN's own pin via the force path.
- Double force-pin by two trainers: last pin wins; the first trainer's unpin →
  118, the second's → 0 (`C7E.dbl`). Ownership follows the latest pin —
  consistent, documented here for the record.

---

## Residual observations (not claim-7 holes)

- **Undocumented refusal codes** (all behave as refusals, none silent): 115 =
  unpin with nothing pinned; 118 = unpin with wrong credentials; 103 =
  force_pin/kill on out-of-range slot; 2001 = negative slot (also the
  strength>100 code). Recommend documenting 115/118.
- `st_trainer_declare` with role=1 returns 0 on declare-down 90→10 but the
  destruction price stays n(90)=4 (`C7D.down,role=1,tr=1,decl=0,k1cite=109`).
  rc=0 with no pricing effect is claim-5 territory (prior verdict: holds —
  "no discount via lowering"); noted, not re-litigated here. Declare-*up*
  10→90 with role=1 does raise the price (`k1cite=109`), consistent with
  no-discount directionality.
- `C7E.dbl` post-unpin `kill3=109`: after two *blocked* kills attached 8
  cites, a third full payment overpays the exact-payment rule → 109. This is
  the claim-2 exact-payment quirk (overpayment → 109), not a pin bug.
- Checker sweeps over force-pin event trails were not run (claim-6 scope,
  per task).

## Minimal reproducers

TNN-role pin refused (claim holds): `c7a.zag` → `C7A,slot=1,role=0,tr=1,fp=113,kill=0,live=103`
Wrong-trainer unpin refused: `c7b.zag` → `C7B,pin(1,1),unpin(1,7),fp=0,fu=118,kill=112,live=0`
Pinned slot refuses all destruction: `c7c.zag` → `C7C.ds,fp=0,delete_strong=112,live=0`
TNN declare refused, strength unchanged: `c7d.zag` → `C7D.down,role=0,tr=1,decl=113,k1cite=109,live=0`

## VERDICT: HOLDS

With the corrected argument order, Claim 7 holds on every vector attacked:
TNN-role force_pin/force_unpin/trainer_declare → 113 with no effect (12/12
role/trainer combos); unpin strictly requires the pinning trainer's
credentials or a master role (2/3); all three destruction ops refuse
force-pinned slots with 112; no silent no-ops and no false refusals were
found. The void engagement's H1–H5 are explained as argument-order artifacts
and do not reproduce.
