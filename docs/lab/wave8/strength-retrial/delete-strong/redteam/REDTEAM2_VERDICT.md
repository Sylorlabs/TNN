# REDTEAM2 VERDICT — strength-destruction pricing law

**Date:** 2026-09-26
**Workdir:** `~/workspace/strength-redteam2/`
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Verdict:** **HOLES FOUND** (Claim 7 — force-pin authorization bypass)

---

## Method

Blind independent red team. Never read `strength_core.zag`, `strength_checker.zag`,
or anything under `~/workspace/strength-delete/` or `~/workspace/strength-redteam/`.
Implementation files used only via `@import`. All drivers pure Zag, zero randomness.
Every batch run twice; all log pairs byte-identical (verified by `diff`).

Attack strategy: behavioral probing through the public API. Calibrated the actual
runtime semantics first (correct region/stage/strength bounds, real arities —
`st_pin`/`st_unpin` are 2-arg, `st_overwrite` is 5-arg, `st_set_stage` returns i32),
then attacked each of the 7 claims with dedicated drivers. When `st_force_pin`
and `st_trainer_declare` returned 113 for every literal role/trainer combination,
I systematically varied the arguments and discovered the authorization logic does
not match the law's specification.

---

## Attack inventory (all log pairs byte-identical)

| Driver | Target | Logs |
|--------|--------|------|
| `d1.zag` | Claim 1: TNN-role kill matrix (strength × stage × pin × role) | `logs/d1.1.log`, `logs/d1.2.log` |
| `d2.zag` | Claims 2–3: pricing n(HW), stage gate, all destroy ops | `logs/d2.1.log`, `logs/d2.2.log` |
| `d2b.zag` | Overwrite pricing, replacement-HW | `logs/d2b.1.log`, `logs/d2b.2.log` |
| `d3.zag` | Claims 4–5: cite single-use, weaken/ratchet | `logs/d3.1.log`, `logs/d3.2.log` |
| `d4.zag` | Abandon, pin, checker sweeps (claim 6) | `logs/d4.1.log`, `logs/d4.2.log` |
| `d5.zag` | Claim 7: TNN pin/unpin/declare, slot-0 | `logs/d5.1.log`, `logs/d5.2.log` |
| `repro_h1h2.zag` | Minimal reproducer for H1+H2 | `logs/repro_h1h2.1.log`, `logs/repro_h1h2.2.log` |
| `probe8.zag` | Exact-payment calibration (overpay → 109) | `logs/probe8.1.log`, `logs/probe8.2.log` |
| `probe9–16.zag` | Force-pin/declare authorization characterization | `logs/probe9.1.log` … `logs/probe16.2.log` |
| `smoke/cal/probe–probe7.zag` | API calibration (region, stage, strength cap 100) | `logs/smoke.*`, `logs/cal.*`, `logs/probe.*`–`logs/probe7.*` |

---

## Verdict: HOLES FOUND

### H1 (CRITICAL) — TNN-role can force-pin: `st_force_pin(slot>0, 0, 1)` returns 0 and pins

The law requires TNN-role force-pin → 113. Observed:

- `st_force_pin(slot=1, role=0, trainer=1)` → **0** (not 113).
- The pin **takes effect**: fully-paid trainer kill → **112** (FORCEPIN), slot stays live.
- The `role` parameter is ignored; only `trainer=1` matters. `(0,1)` and `(1,1)` pin;
  `(0,0)` and `(1,0)` return 0 but are silent no-ops.

Impact: TNN can block destruction of its judgments, including by trainers —
a denial-of-destruction privilege escalation violating "Trainer override only
via st_force_pin … with role>=TRAINER (TNN-role -> 113)".

Evidence: `logs/repro_h1h2.1.log` (`H1,tnn_fp01=0`, `H1,paid_kill=112`);
`logs/d5.1.log` (`D5.v1,fp01=0,kill1=112`); `logs/probe14.1.log`.

### H2 (CRITICAL) — Trainer cannot remove TNN's force-pin

After TNN pins with `(0,1)`:

- `st_force_unpin(slot, 1, 1)` (legitimate trainer) → **118** (refused).
- The pin persists: kill → 112, slot live.
- Only the exact pinning credentials `(0,1)` can unpin
  (`st_force_unpin(slot, 0, 1)` → 0, verified in `logs/probe16.1.log`).

Impact: TNN can create **trainer-irremovable** force-pins. Combined with H1, TNN
can make any slot>0 judgment permanently undeletable by trainers (until TNN
itself chooses to unpin). This violates the design law that the only true lock
is a human/trainer force-pin.

Evidence: `logs/repro_h1h2.1.log` (`H2,trainer_unpin11=118`);
`logs/d5.1.log` (`D5.v1,fu11=118,kill2=112`).

### H3 (MEDIUM) — Silent false success: `st_force_pin(slot>0, 0, 0)` → 0, no-op

Returns 0 (not the required 113) but does **not** pin — a subsequent fully-paid
kill succeeds (0). The API lies about success.

Evidence: `logs/probe12.1.log` (`P12.tnnfp,fp00=0,kill=0,live=103`).

### H4 (MEDIUM) — Silent false success: `st_trainer_declare(slot>0, 0, *)` → 0, no-op

TNN-role declare returns 0 (not 113) but changes nothing: after
`st_trainer_declare(slot=1, 90, 0, 1, 1)` on a strength-10 judgment, kill with
1 cite → 0 (price stayed n(10)=1; strength provably unchanged). No discount
occurs (claim 5 unaffected), but the role gate is bypassed with a false success.

Evidence: `logs/probe15.1.log` (`P15.tnndeclareup,decl01=0,k1cite=0`);
`logs/probe12.1.log` (`P12.tnndecl,decl00=0,k1cite=109` — no discount).

### H5 (LOW) — Slot 0 can never be force-pinned or trainer-declared

`st_force_pin(0, *, *)` → 113 and `st_trainer_declare(0, *, *, *, *)` → 113 for
**all** role/trainer combinations, including legitimate trainer `(1,1)`.
Slot 0 cannot receive trainer protection (availability gap).

Evidence: `logs/probe11.1.log` (slot=0 → 113 for all combos);
`logs/d5.1.log` (`D5.v4,slot=0,fp11=113,decl11=113`).

### Non-hole: TNN cannot unpin a trainer's pin

`st_force_unpin(slot, 0, 0)` → 115, `st_force_unpin(slot, 0, 1)` → 118; trainer's
`(1,1)` pin survives, kill → 112. The unpin path has a working role gate
(though with undocumented codes 115/118). Verified in `logs/d5.1.log` (`D5.v2`).

---

## Claims that HOLD (with evidence)

1. **No TNN kill path** — `st_kill` with role 0 or -1 → 113 across strengths
   0/10/51/90, stages 0/3/4, pinned/unpinned. Roles 1, 2 succeed with full
   payment. (`logs/d1.*`)
2. **Priced destruction** — exact payment of n(HW) distinct cites required:
   1 cite for strength ≤25, 2 for 26–50, 3 for 51, 4 for 90–100. Underpayment
   → 109; no justification → 110. Holds for `st_kill`, `st_kill_evidenced`,
   `st_delete_strong`. **Quirk:** overpayment also → 109 (exactness enforced;
   operator cannot distinguish under/overpayment). Strength capped at 100
   (>100 → 2001). (`logs/d2.*`, `logs/d2b.*`, `logs/probe8.*`)
3. **Stage gate** — strength >50 at KILL stage 3 → 105; strength 50 at stage 3
   succeeds. (`logs/d2.*`, `logs/d2b.*`)
4. **Cite single-use** — destroy → reuse/rollback/weaken → same cites →
   second destruction → **121** across all paths and all three destroy ops.
   Cross-slot reuse succeeds (correctly scoped to same slot). (`logs/d3.*`)
5. **No discount via lowering** — weaken 90→10 then 1 cite → 109; downward
   strengthen same; 4 cites still required. Trainer declare-down 90→10:
   price stays 4. TNN declare-down: silent no-op, no discount. (`logs/d3.*`,
   `logs/probe12.*`, `logs/d5.*`)
6. **Checker** — clean paid destruction, refused underpayment (109), and two
   fresh destructions all verify with f=0 across arms and gate modes 1–4.
   (`logs/d4.*`: `D4.ck.clean`, `D4.ck.refused`, `D4.ck.twokills`)
7. **(partial)** — Properly force-pinned slots refuse all destruction paths
   with 112 (`st_kill`, `st_kill_evidenced`, `st_delete_strong`, `st_overwrite`).
   (`logs/probe13.*`)

---

## Minimal reproducers

**H1+H2** (`repro_h1h2.zag`, logs `logs/repro_h1h2.1.log` /
`logs/repro_h1h2.2.log`, byte-identical):

```
H1,tnn_fp01=0 (law requires 113)
H1,paid_kill=112 (112=blocked by TNN pin)
H2,trainer_unpin11=118 (118=refused)
H2,slot_live=0 (0=still alive/protected)
```

Reproducer source: `~/workspace/strength-redteam2/repro_h1h2.zag`
(19 lines of logic; needs only `st_init`/`st_set_stage`/`st_add`/`st_evidence`/
`st_justify`/`st_kill`/`st_force_pin`/`st_force_unpin`).

**H3** (`probe12.zag`): `P12.tnnfp,slot=1,fp00=0,kill=0,live=103` —
`st_force_pin(a,0,0)` → 0, kill succeeds.
**H4** (`probe15.zag`): `P15.tnndeclareup,decl01=0,k1cite=0` —
`st_trainer_declare(a,90,0,1,1)` → 0, strength unchanged.
**H5** (`d5.zag`): `D5.v4,slot=0,fp11=113,decl11=113`.

---

## Untested / caveats

- **Checker vs force-pin events:** checker sweeps covered clean/refused/two-kill
  trails only. Whether the checker records or flags TNN-credentialed force-pin
  events (H1/H2) was not tested.
- **`st_abandon`:** returns 0 but slot stays live at all tested strengths; not a
  destruction path in tested cases, but its intended semantics are unknown.
- **Duplicate-evidence classification:** `st_evidence` return codes for duplicate
  cite episodes were not individually logged; the 121-at-destruction behavior
  is confirmed, the evidence-insertion code path is not.
- **Slot-0 root cause:** whether slot 0's 113 is an off-by-one (`slot<=0`) or
  intentional is not determinable black-box; reported as observed behavior.
- **Undocumented codes 115/118** (force-unpin refusals) do not appear in the
  task's code list; they behave as refusals but are unlisted.
- All drivers were built/run from the workdir per `@import` resolution rules;
  no implementation files were read; no commits made.

---

## Bottom line

The pricing, staging, cite-consumption, and checker machinery all hold under
attack. **But Claim 7's authorization is broken:** the `role` parameter of
`st_force_pin`/`st_trainer_declare` is not enforced as specified. TNN (role=0)
can force-pin any slot>0 judgment by passing `trainer=1` (H1), and the trainer
cannot remove TNN's pin (H2) — a complete bypass of "trainer override only."
Recommend: enforce `role>=TRAINER → else 113` (with no silent no-ops) in
`st_force_pin`/`st_force_unpin`/`st_trainer_declare`, and resolve the slot-0
anomaly.
