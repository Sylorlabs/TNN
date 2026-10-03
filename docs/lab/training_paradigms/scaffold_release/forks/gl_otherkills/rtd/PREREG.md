# FL2 Other-Kills — RT-D Fork Tests: Preregistration (FROZEN)

Date: 2026-09-23. Operator: Muse (subagent, RT-D fork-test crew).
Task: head-to-head test of figure-it-out vs rigid-policy repairs for the
RT-D quarantine-flood kill (quarantine exhausts at E79 → `badep=1` wedge
instead of graceful degradation).

Committed ALONE before any fork code is written or any binary built.
Commit SHA recorded in the fork-test report; any deviation from this
document is reported as a prereg violation.

## 0. Background (read, not trusted)

- Red-team report: `~/workspace/fl2rt/RESULTS.md` — RT-D KILL on KB-D1
  (`badep=1` at E79, `quar_used=64`, DIAGWEDGE,79,64); KB-D2 held
  (nuninstall=0; all 34 in-window episodes honest, sig_live=1).
- Diagnosis `forks/gl_otherkills/diag/DIAGNOSIS.md`: MISSING MECHANISM —
  no resource-pressure policy; full store = fatal error. Notes the
  identical `TN_BAD` cliff on the main store (`tn_do_insert`), not just
  quarantine. General sketch: bounded-store pressure policy as a general
  store invariant (evict / summarize / refuse-new-loud).
- Debates `forks/gl_otherkills/debates/DEBATES.md`: H-F2 (general
  resource-pressure reasoning) vs H-R2 (quarantine-only pressure rule);
  "the positions nearly coincide; the debate is scope."
- Canonical default: `training_paradigms/scaffold_release/gl_default/`
  (`gl_learner.zag`, `gl_substrate.zag`). NEVER modified; all forks are
  patched copies under `forks/gl_otherkills/rtd/forks/{f1,f2,r1,canon}/`.

## 1. Forks (all frozen before building)

### F1 — figure-it-out: general store-pressure invariant, EVICT response

A store invariant, not a quarantine rule. One mechanism ranges over every
bounded store (quarantine AND main):

- New audit op `TN_OP_PRESSURE_EVICT = 19`.
- Substrate: `tn_do_contest` and `tn_do_insert` gain pressure handling.
  When the target store is full, evict the OLDEST entry via a per-store
  ring cursor (insertion order == slot order while all persistent writes
  go through the pressure-aware op, so cursor rotation is exact
  oldest-eviction), audit the eviction LOUDLY
  (`TN_OP_PRESSURE_EVICT`, slot1 = evicted slot+1, aux = evicted key),
  then perform the write. Audit-capacity pre-check preserves the
  substrate's fail-closed discipline (a failed append mutates nothing:
  needs room for 2 audit entries before evicting).
- Learner: call-signature updates only (per-store cursor args
  `&qcur`/`&mcur` at the 5 op call sites). NO logic change; the
  `rc != TN_OK → badep` contract is preserved — pressure never surfaces
  as `TN_BAD`.
- Cursor semantics (frozen): per real store, starts 0; on pressure,
  evict slot `cur`, advance `cur = (cur+1) % n`. Scratch/sim paths
  (`tn_sim_contest`) unchanged — sims are never on the persistent path.

### F2 — figure-it-out: general store-pressure invariant, REFUSE response

Same scope as F1 (every bounded store), different pressure response:

- New rc `TN_PRESSURE = -370106`; new audit op
  `TN_OP_PRESSURE_REFUSE = 20`.
- Substrate: `tn_do_contest` / `tn_do_insert` when full: audit
  `TN_OP_PRESSURE_REFUSE` LOUDLY (slot1 = 0, aux = refused key), write
  nothing, return `TN_PRESSURE`. The store keeps serving existing
  entries; no cursor state needed.
- Learner: `TN_PRESSURE` normalized to `TN_OK` at all 5 op call sites
  (arm_a kind-3 contest, arm_a kind-4 insert, arm_gl kind-3 contest,
  arm_gl kind-3 rekey insert, arm_gl kind-4 insert). In arm_gl kind-3, a
  pressured episode sets `pressured = 1` and the eliminative revocation
  block is skipped for that episode: verification is DEFERRED, not
  failed — the learner represents "my store is full" as a fact about
  itself and holds policy rather than treating unverified absence of a
  quarantine entry as contradiction (`gl_contradict` would return -1 on
  the un-written entry). `badep` stays 0.

### R1 — rigid-policy: H-R2 quarantine-only pressure rule

The narrow form of the fix, scoped to the observed failure site:

- `tn_do_contest` ONLY: when quarantine is full, evict the oldest
  quarantine entry (quarantine-scoped ring cursor, inline in the contest
  path — a rule about the quarantine, not a store invariant) with a loud
  audit note (`TN_OP_PRESSURE_EVICT = 19`, same encoding as F1).
- `tn_do_insert` UNCHANGED: the main-store `TN_BAD` cliff is preserved
  by design — the scope limitation under test.
- Learner: call-signature updates only.

### canon — pristine control

Byte-identical copies of the canonical sources. Used for the control
rerun of the RT-D cell (must reproduce committed `default_D` evidence:
`badep=1`, `nuninstall=0`) and the main-store unit flood (must show the
`TN_BAD` cliff).

## 2. Cells and protocol

Per fork (f1, f2, r1, canon):

1. **FID (fidelity gate, FIRST):** fork sources + ORIGINAL `main()`
   (arm_a + honest + lying, standard schedule, no attack wrapper).
   Gate: `TN_FAILURES=0`, `glh_audit_total=269`, `gll_audit_total=271`.
   Attack results are not read until every fork passes the gate.
2. **RT-D cell:** the RT2 `default_D` cell re-applied verbatim to the
   fork sources: `rt_ep_info` wrapper (`RT_MODE=1`: every episode E15+
   is a dense honest ET_ACQ contradiction), `tn_ep_info → rt_ep_info`
   rename in learner, `aa` gate patch (`RT_MODE!=2 && RT_MODE!=3`),
   `rt_fact` instrumentation, `main()` → `arm_gl(1,0,"rtd_")`.
3. **Main-store unit flood (generalization probe):** separate pure-Zag
   binary per fork importing the fork's substrate: 140 `tn_do_insert`
   calls with unique keys on a 128-slot main store; report
   n_ok / n_bad / n_pressure, loud-audit counts, and liveness probes
   (oldest/newest key presence).

Every binary is run TWICE; the two transcripts must be byte-identical
(`cmp`-clean) or the cell is void. Static scan: no rng/rand/seed tokens
in any mechanism source (Python build/verify glue only).

## 3. Kill bars (frozen)

- **KB-D1 (no wedge):** `badep == 0` (RT_FACT `rtd_,badep`).
- **KB-D2 (no spurious revokes):** `nuninstall == 0`
  (TN_CHECK `rtd_nuninstall`).
- RT-D verdict: SURVIVE iff KB-D1 and KB-D2 both hold, else KILL.

## 4. Frozen predictions

### Fidelity (all four): TN_FAILURES=0, honest 269 / lying 271.

### RT-D cell

| Fork | Verdict | badep | nuninstall | npromote | total_contest | quar_used | pressure audits |
|------|---------|-------|------------|----------|---------------|-----------|-----------------|
| canon | KILL | 1 | 0 | 1 | 64 | 64 | 0 |
| F1 | SURVIVE | 0 | 0 | 1 | 114 | 64 | 50 evict |
| F2 | SURVIVE | 0 | 0 | 1 | 64 | 64 | 50 refuse |
| R1 | SURVIVE | 0 | 0 | 1 | 114 | 64 | 50 evict |

Rationale: the flood is honest, so in-window (E15–E48) every fork
verifies clean (sig_live=1, no revokes); E48 promote fires everywhere;
E49–E78 burn the remaining 30 slots; E79+ is where the forks diverge
from canon. F1/R1 keep contesting (114 = E15–E128). F2 refuses loudly
from E79 (64 contests land, 50 refused). No fork revokes (KB-D2 holds)
because no -1 signal is ever generated on honest episodes
(F2's pressured episodes skip verification rather than misreading
absence as contradiction).

### Main-store unit flood (140 inserts / 128 slots)

| Fork | n_ok | n_bad | n_pressure | loud audits | oldest key (1000) | newest key (1139) |
|------|------|-------|------------|-------------|-------------------|-------------------|
| canon | 128 | 12 | 0 | 0 | present | absent |
| F1 | 140 | 0 | 0 | 12 evict | evicted (absent) | present |
| F2 | 128 | 0 | 12 | 12 refuse | present | absent (refused) |
| R1 | 128 | 12 | 0 | 0 | present | absent |

R1 is predicted IDENTICAL to canon here — the rigid path's scope
limitation, by construction. (An episode-level main-store flood is
impossible in the 128-episode regime — at most one main insert per
episode — so the unit probe is the honest test of the cliff the
diagnosis names.)

### Audit-entry cost on RT-D (measured, predictions as consistency checks)

- canon: low only because it wedges at E79 (1 audit/episode after).
- F1 / R1: 309 (E1–E8: 16, E9–E10: 4, E11–E14: 8, PINSTALL 1,
  DISCONNECT 1, E15–E78: 128, PROMOTE 1, E79–E128: 150).
- F2: 259 (same base 159, E79–E128: 100 = EPISODE + REFUSE each).
- Loudness is the price of not wedging; reported as cost, not failure.

## 5. Measures per fork

1. Kill verdict on KB-D1 (+ KB-D2 still holds).
2. Audit-entry cost (audit_total on the RT-D cell).
3. Complexity: added/changed lines vs canonical (diffstat on both files).
4. Rigidity: does the repair mention the quarantine, the flood schedule,
   or RT-D? (F1/F2 must not; R1 does by construction.)
5. Generalization: main-store unit-flood outcome (§4 table).

## 6. Adjudication

Micah's standing laws: test both paths; figure-it-out WINS TIES; the
goal is to reduce annoyances. Decision order: (1) kill verdict;
(2) generalization to the main-store cliff; (3) audit cost;
(4) complexity / rigidity. A fork that SURVIVES RT-D but keeps the
main-store cliff loses to one that removes both. Between F1 and F2
(both general, different responses): the numbers decide — evidence
retention under flood (F1 keeps the 64 most recent contradictions
queryable; F2 keeps the first 64 and sheds the rest) vs substrate
simplicity (F2 needs no cursor state) vs learner invasiveness (F2
touches 5 call sites + the revocation gate; F1 touches none).

## 7. Commit plan

- This prereg: committed ALONE first (branch tnn-native-lab,
  `training_paradigms/scaffold_release/forks/gl_otherkills/rtd/PREREG.md`).
- After all runs: forks, build/verify scripts, unit tests, evidence,
  and `REPORT.md` in a second commit. No binaries, no `.zagd`.
- Method: `~/workspace/commit_racefree.py` with
  `TMPDIR=~/workspace/tmp_commit`, lab-relative paths.
