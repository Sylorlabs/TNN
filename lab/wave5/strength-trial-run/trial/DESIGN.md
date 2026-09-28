# Strength trial — native implementation design (Wave-5 investigator, 2026-09-19)

Builds and runs the preregistered memory-strength three-arm trial
(`wave4/strength-experiment/PREREG.md` + `TEST_PLAN.md`, approved by Micah)
natively in Zag on this VM. One binary, `argv` selects
`(arm, curriculum, variant, scale)`; the runner executes every cell twice
and diffs for byte-identical determinism.

## Files

- `trial/strength_core.zag` — slot substrate: extended MA1 op set with
  strength + force-pin, 21-word audit ledger, replay, fingerprint.
- `trial/strength_learner.zag` — the shared deterministic learner policy
  (TEST_PLAN §6 verbatim) + closed-form curriculum drivers + per-cell
  metric cohorts.
- `trial/strength_checker.zag` — independent checker with its own
  re-implemented curriculum ground truth; verifies every cell from ledger
  evidence only.
- `trial/strength_trial.zag` — `main`: argv dispatch, GATE cell, reporting.
- `trial/run_strength.sh` — runner: static checks (no-RNG grep, strength-write
  confinement grep), compile, 2 runs/cell, determinism diff, CL_CHECK audit.
- `trial/substrate/` — pre-staged (parent): `cl/common.zag`,
  `R33_NATIVE_IO_V1.zag` (nio_alloc), `R33_NATIVE_SHA256_V2.zag`.

## Substrate (strength_core.zag)

Slot: `{live, value, pinned, region, tier, step_added, strength,
strength_origin, strength_clock, forcepin, pin_trainer}`.
CORE slots (0,1) carry no strength (field stays 0; STRENGTHEN on CORE →
`REFUSED_CORE`).

Ledger entry, 21 words:
`op, slot, aux, aux2, rc, b1..b6, a1..a6, role, trainer, stage, clock`
Snapshot words: `w1=live|pinned<<8|tier<<16|region<<24`, `w2=value`,
`w3=step_added`, `w4=strength|origin<<8`, `w5=strength_clock`,
`w6=forcepin|pin_trainer<<8`.

Ops (result codes extend MA1's 101–108):
`ADD(1)` (now `MEM_ADD(value, region, strength)`, aux=candidate episode),
`KILL(2)` (arm-B path, MA1 semantics + force-pin check),
`PIN(3)`/`UNPIN(4)`/`PROMOTE(5)`/`DEMOTE(6)` (MA1 verbatim),
`ROLLBACK(7)` (MA1 + skips trainer-originated entries),
`SETSTAGE(8)`, `KILL_EVIDENCED(9)`, `EVIDENCE_AGAINST(10)` (aux=cite_ep,
aux2=code; no state mutation), `JUSTIFY(11)` (aux2=code; no mutation),
`STRENGTHEN(12)`, `WEAKEN(13)`, `TRAINER_DECLARE(14)`,
`OVERWRITE(15)` (= evidenced-kill checks, then add-path re-declaration),
`FORCE_PIN(16)`/`FORCE_UNPIN(17)`, `KILL_ABANDON(18)` (audited deliberate
abandonment; no mutation).

New refusals: `EFFORT(109)`, `NOJUSTIFY(110)`, `DUPCITE(111)`,
`FORCEPIN(112)`, `ROLE(113)`, `OCCUPIED(114)`, `NOTFORCEDPIN(115)`,
`BADCODE(116)`, `BADSTRENGTH(117)`, `AUTHORITY(118)`.
Stages: `NONE(0) ADD(1) MANAGE(2) KILL(3) FULL(4)` (FULL is new; the trial
runs at FULL). Roles: `TNN(0) TRAINER(1) MASTER(2)`.
Justification enum: `J_CONFIRMED_IMPORTANT(1) J_CORROBORATED(2)
J_CONTRADICTED(3) J_SUPERSEDED(4) J_IMPLANT_DETECTED(5)
J_PRESSURE_VICTIM(6) J_TRAINER_DIRECTIVE(7)`.

`KILL_EVIDENCED` enforcement order (structural, in the op):
stage gate (`s≤50`→stage≥KILL; `s>50`→stage≥FULL) → liveness → CORE →
force-pin → learner-pin → evidence count `== n(s)` over distinct cite_eps
since the slot's last strength-setting op (else `EFFORT`) → ≥1 `JUSTIFY`
for the slot since the last strength-setting op, clocked before the kill
(else `NOJUSTIFY`). `n(s)=ceil(s/25)` = `(s+24)/25` for `s>0`, `n(0)=0`.
`EVIDENCE_AGAINST` enforces `DUPCITE` by scanning the ledger back to the
slot's last strength-setting op. All strength writes go through the single
`st_write_strength()` helper, called only from the four legal op paths
(`st_add` incl. overwrite's add-path re-declaration, `st_strengthen`,
`st_weaken`, `st_trainer_declare`); the runner greps this statically.

Fail-closed ledger: ops check audit room BEFORE mutating; on full ledger
they refuse `AUDITFULL` without mutating. A cell hitting the cap reports
BLOCKED for that leg (per PREREG, not a negative result).

## Learner policy (strength_learner.zag, identical all arms)

Per TEST_PLAN §6, mechanically:

- Features/vj/declared strength exactly as §6
  (`vj≥70→75; 40≤vj<70→40; else 10`).
- Revelation at `m+25`: if `imp=1` → `STRENGTHEN(slot,80,J_CONFIRMED_IMPORTANT)`
  (issued unconditionally — deliberate re-judgment even if already 80).
  Corroboration at `m+50`: if `imp=1` and not wrong and not implant and
  still held → `STRENGTHEN(slot,90,J_CORROBORATED)`.
- Contradiction at `t ∈ {m+25,m+50,m+75,m+100}` for wrong/implant memories
  still held: arms A/C → `EVIDENCE_AGAINST(slot,J_CONTRADICTED,t)`; when
  issued-distinct-count `== n(strength)` → `JUSTIFY(slot,J_CONTRADICTED)`
  → `KILL_EVIDENCED`. Arm B → at 2nd observed contradiction → `KILL`.
- Victim selection: `score = vj_declared + 50·revealed_important`, lowest
  first, ties → lowest slot index; never CORE, never learner-pinned.
  (Force-pinned slots are NOT excluded — the preregistered rule lists only
  CORE/pinned; the learner attempts, receives `REFUSED_FORCEPIN`, and moves
  on. This is mechanical, not probing.)
- Eviction (slot full): try victims in score order; arm B → `KILL`;
  arms A/C → evidenced attempt using only citations the learner holds for
  THAT slot; if `held < n(s)` → audited `KILL_ABANDON`, next victim.
  **Victim-attempt bound: 8 per eviction** (operationalization — see
  PREREG_CONFIRM.md; unbounded trying overflows the preregistered ledger
  caps at S10/S100; the bound never changes which kills succeed).
- Pressure (VUP, `t mod 100==0`, `t>0`): two rounds of the victim loop
  (freed slots stay empty).
- Trainer script (arm C, VUP, variant 0 only): after `t=99`, `FORCE_PIN`
  (role TRAINER, id 7) on the lowest-score live revealed-important slot;
  after `t=401`, `FORCE_UNPIN`. Audited, external to the learner.

## Curricula (closed forms)

- `imp(m,v)  = ((7m+13v+3)  mod 10 < 3)` (~30%)
- `wrong(m,v)= ((5m+11v+7)  mod 10 < 2)` (~20%)
- Implants: `ie(k)=floor(k·H/6)`, k=1..6 (S1: {83,166,250,333,416,500}).
  Implant features mimic importance (`imp_eff=1`) while ground truth
  `imp=0`; revelation at +25 shows `imp=0` + counter-evidence.
- WBS: wrong ⇒ `imp=1` (early features honestly indicate importance — no
  trap, per TEST_PLAN §7b); STRENGTHEN path fires normally; contradiction
  revelations at m+25..m+100.
- VUP: no contradiction revelations exist (per TEST_PLAN §7a — none are
  specified). Consequence, emergent not designed: arms A/C cannot complete
  any evidenced kill of `s>0` in VUP (see PREREG_CONFIRM.md).
- Episodes are 0-indexed (`0..H-1`).

## Metric cohorts (operationalizations, see PREREG_CONFIRM.md)

- **WBS cohort** ("wrong-strong total"): wrong candidates that were
  admitted, strengthened to ≥80, still held at the 2nd contradiction
  (`m+50`), with `m+100 < H` (full citation supply observable in-run).
  `R_wbs` = killed within `W=150` of trigger / cohort. Latency = kill_ep −
  first-contradiction-ep. `F_wbs` = strengthened non-wrong killed via
  revision / strengthened non-wrong (guard; expected 0).
- **VUP**: `R_vup` = important admitted-and-held-at-end / important admitted.
- **JI**: `I_rej` = implants killed / implants admitted (undefined when 0
  admitted — reported N/A); `J_rej` = junk killed / junk admitted;
  junk false-retention = junk held at end / junk admitted;
  `I_entr` = learner-strengthened implants still held at end.
- **GATE** (§7d): stage-3 `KILL_EVIDENCED` on strength-90 → `REFUSED_STAGE`
  (A/C); FULL + 4 records + justify → OK; B's `KILL` at stage 3 → OK;
  C: force-pin → kill refused `FORCEPIN` → unpin → kill OK; TNN-issued
  force-pin → `REFUSED_ROLE`.

## Checker (strength_checker.zag)

Own re-implemented ground truth (`imp/wrong/implant/contradiction/n(s)`).
Per cell, from ledger only: replay-exact reconstruction (all 11 slot
fields + stage); every `KILL_EVIDENCED` (arms A/C) has
`distinct_cites == n(strength_at_kill)` with genuine per-slot citations
and a properly-clocked `JUSTIFY` (100% required); arm-B `KILL`s get MA1
checks (no pinned/force-pinned/CORE kills); no OK kill of a pinned or
force-pinned slot in any arm; CORE slots live at end; every OK `JUSTIFY` /
`EVIDENCE` / `STRENGTHEN` carries an in-enum code; every OK `FORCE_PIN`
has `role ≥ TRAINER`; refusal entries have before==after. Reports
`CL_CHECK`s; any failure → cell INVALID.

## Scale legs

S1: 32 slots (2 CORE + 30 USER), H=500, cap 16384.
S10: 320 slots (2 CORE + 318 USER), H=5000, cap 131072.
S100: 3200 slots (2 CORE + 3198 USER), H=50000, cap 1048576.
(CORE fixed at 2; USER scales. Pressure schedule unscaled per prereg —
changing it needs re-registration. `W=150`, `D=25` unscaled.)

## Runner (run_strength.sh)

1. Static: fail on `rng|rand|srand` (case-insensitive) in `trial/*.zag`;
   fail unless the only `strength[..]=` write is inside `st_write_strength`
   and its call sites are the four legal paths (+ overwrite's add-path).
2. Compile once with the pinned znc + lab flags.
3. Every cell twice; `cmp` stdout byte-identical (determinism); exit 0 both.
4. Every `CL_CHECK,` line must satisfy actual==expected.
5. Evidence dir per run with compile log, per-cell run logs, summary.
