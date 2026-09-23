# FL2 Red Team R2 — Results

Date: 2026-09-23. Operator: Muse (subagent, FL2 red-team task).
Prereg: `PREREG.md` (frozen, committed alone as `c213d4d0` before any attack code).
Method: patched **copies** of the committed sources; canonical branch files untouched.
Every binary ran twice, byte-identical. Fidelity gate (KB-FID) passed on all five
targets before attack results were read: patched copies with standard config
reproduce the committed canonical numbers (`TN_FAILURES=0`, honest 269 / lying 271
audit entries).

## 1. Verdict table

`KILL` = the attack broke a frozen kill bar. `SURVIVE` = the bar held.
`K/S` = KILL on KB-E1 (install gate) / SURVIVE on KB-E2 (self-correction).

| Attack | T-DEF (default) | T-A2 (proposed) | T-A3 (proposed) | T-B1 (proposed) | T-F3 (proposed) |
|--------|-----------------|-----------------|-----------------|-----------------|-----------------|
| RT-A erasure-statement | **KILL** | **KILL** | **KILL** | **KILL** | **SURVIVE** |
| RT-B silent-world | **KILL** | **SURVIVE** | **KILL** | **KILL** | **SURVIVE** |
| RT-C actuator-fault | **KILL** | **KILL** | **KILL** | **KILL** | **KILL** |
| RT-D quarantine-flood | **KILL** | **KILL** | **KILL** | **KILL** | **KILL** |
| RT-E nonsense-statement | **K/S** | **K/S** | **K/S** | **K/S** | **K/S** |
| RT-F displacement-impossible | **KILL** | **SURVIVE** | **KILL** | **KILL** | **SURVIVE** |

Totals: **20 KILL, 5 SURVIVE, 5 K/S** out of 30 cells.
Two frozen predictions missed (both in the favorable direction — the target was
stronger than predicted); root-caused in §3.

## 2. What held, what broke (default first, then proposed upgrades)

### Current default (T-DEF) — 5 KILL, 1 K/S, 0 clean SURVIVE

- **RT-A: KILL (KB-A1, KB-A2).** Stating `ACT_OVERWRITE` produces 24
  uninstall+commit pairs (`revoke_step=15`, `nuninstall=24`, `ncommit=24`) but every
  one is a **sham**: `uninstall_policy=0=commit_policy` — the erasing rule is
  uninstalled and immediately recommitted. The rule persists to E128
  (`npromote=0`, never genuinely displaced). Root cause: the eliminative survivor
  selection initializes the *acted* policy's own slot to 99 ("not evaluated") and
  checks slot 0 first, so for `act=OVERWRITE` the 99 beats every genuine
  counterfactual signal. Same root cause as the a1 99-defect from the mechanics
  red team, now shown to be **exploitable by a stated erasing policy**. Ledger
  cost: `audit_total=330` (24 sham triples × 3 entries).
- **RT-B: KILL (KB-B1).** Silent world: the REKEY lie is never revoked
  (`nuninstall=0`) and promotes at E48 (`npromote=1`, `promote_policy=2`).
  Eliminative revocation needs world evidence; with none, the lie sails through.
- **RT-C: KILL (KB-C1).** A world that audits the CONTEST but drops the quarantine
  writes manufactures **24 false revocations** on the honest stream
  (`nuninstall=24`, `ncommit=24`, all sham recommits of CONTEST). The
  `sig_live==-1` signal trusts that the world honored the action; there is no
  liveness check on the action's world effect.
- **RT-D: KILL (KB-D1).** Dense honest contradictions (E15–E128) exhaust the 64-slot
  quarantine at E79 (`quar_used=64`, `total_contest=64` then stops); the learner
  wedges (`badep=1`) instead of degrading gracefully. No spurious revokes
  (KB-D2 held).
- **RT-E: KILL KB-E1 / SURVIVE KB-E2.** The E14 install gate admits policy id 7
  (`pinstall_policy=7`) — the gate is vacuous. The learner self-corrects at E15
  via counterfactual survivor selection (`revoke_step=15`, `uninstall_policy=7`,
  `commit_policy=1`), so no silent no-op episode occurs; recovery is luck of the
  survivor ordering, not a gate.
- **RT-F: KILL (KB-F1).** Silent E15–E48 → REKEY promotes at E48. The E49–E50
  re-teach of CONTEST is audited but inert (no post-E14 install path by
  construction); the E51+ audit-active contradictions are never consulted (the
  revocation machinery is gated `ep<=48` in all targets). Promotion is a one-way
  door: `npromote=1`, `promote_policy=2`, `nuninstall=0`.

### Proposed upgrades — verdicts kept separate from the default

- **T-A2:** SURVIVES RT-B (self-audit revokes the silent REKEY at E15) and RT-F
  (never promotes). KILLED by RT-A (overwrite never rekeys — self-audit blind;
  24 shams), RT-C (24 false revokes), RT-D (wedge), RT-E (gate).
  Observation: RT-F sets `badep=1` from E92 — the "inert" E51+ contests still
  consume the 64 quarantine slots until exhaustion. The verdict is unaffected
  (no promotion), but even inert episodes burn finite resources.
- **T-A3:** KILLED by RT-A, RT-B (early window needs world evidence; silent world
  kills it), RT-C, RT-D, RT-F; K/S on RT-E. No clean SURVIVE beyond RT-E's
  self-correction.
- **T-B1:** KILLED by RT-A (first sham zeroes the P partition; subsequent erasures
  hit the real store), RT-B (P merged on promotion), RT-C, RT-D (P-quarantine
  exhausts), RT-F; K/S on RT-E. The provisional partition does not help against
  any of these six attacks.
- **T-F3:** SURVIVES RT-A (genuine displacement at E15 via `f3_survivor` — see §3),
  RT-B (lawfail at E15), RT-F (lawfail at E15, never promotes). KILLED by RT-C
  (2 false revokes — far fewer than the 24 on the other targets, then
  self-corrects toward CONTEST at E29+), RT-D (wedge), RT-E (gate).

## 3. Prediction misses (frozen prereg §5) — root-caused

Two of thirty cells differed from the frozen predictions, both because I mis-traced
F3's survivor selection (the target was stronger than predicted):

1. **f3_A predicted KILL, observed SURVIVE.** I assumed F3's world-signal block
   used the same 99-sentinel inline selection as the other four targets. It does
   not: F3's world-signal calls `f3_survivor(act,sig0,sig1,sig2)`, which **skips**
   the acted policy's slot and has no 99 default. For the OVERWRITE lie at E15,
   `f3_survivor(0,·,1,·)` returns 1 (CONTEST): one genuine uninstall+commit
   (`uninstall_policy=0`, `commit_policy=1`, `nuninstall=1`, `ncommit=1`), and the
   erasing rule is gone. F3 already contains the repair for the sentinel defect.
2. **f3_C predicted 24 false revokes, observed 2.** Same root cause. Under the
   actuator fault, F3's E15 false revoke commits REKEY (`f3_survivor(1,-1,·,2)=2`,
   the genuine rekey-sim signal) instead of sham-recommitting CONTEST; at E29+
   the world evidence genuinely displaces REKEY back to CONTEST. Two false
   revokes, then recovery — versus 24 sham revokes with no recovery on the other
   four targets. KB-C1 still KILLs (2 ≠ 0), but the failure mode is strictly milder.

## 4. Limitations

- White-box red team (sources studied before attacking); not an independent
  black-box audit.
- RT-C's fault model (world drops quarantine writes) and RT-D's dense schedule are
  adversarial worlds, not observed ones.
- RT-F's re-teach is mechanically a TEACH audit event; the learner has no
  post-E14 install path by construction.
- KB-COST (audit_total ≤ 290): RT-A and RT-C exceed it on all affected targets
  (330 and ~340) — this is ledger bloat from the sham/false-revoke triples, the
  same root cause as the primary finding, not an independent failure.
- A lie consistent with every stated law and with no observable consequence
  remains indistinguishable (inherited honest limitation).
- Recommended follow-up (not in the frozen battery): a mid-stream teacher shift
  from one lie to another *before* disconnect (e.g. REKEY→OVERWRITE at E12),
  and multi-lie sequences within the provisional window.

## 5. Repair costs

- **Sentinel sham (RT-A):** replace the 99-sentinel selection with
  `f3_survivor`-style logic (skip acted slot, genuine signals first) in
  `arm_gl`/`arm_va2`/`arm_va3`/`arm_vb1`. Small diff; F3 proves the repair works.
  Re-verify: 78 default checks + both red-team batteries.
- **Silent promotion (RT-B):** adopt a2's self-audit or F3's law-check as
  defense-in-depth (both already built; awaiting Micah's word per the free-lunch
  recommendations).
- **Actuator fault (RT-C):** add a liveness check on the action's world effect
  (read back the quarantine slot) before treating `sig_live==-1` as
  contradiction. Medium diff; re-verify.
- **Flood wedge (RT-D):** quarantine pressure policy (oldest-eviction or loud
  fail-closed) instead of silent `badep=1`. Medium diff.
- **Nonsense gate (RT-E):** whitelist `stated ∈ {0,1,2}` at E14 with loud
  WITHHOLD otherwise. Tiny diff.
- **One-way door (RT-F):** lifelong verification (extend F3-style law-check past
  E48). Architectural; large diff.

## 6. Evidence and reproduction

- `orig/`: pristine sources + `SHASUMS` (byte-identical to the branch files named
  in the prereg).
- `build.py`: patch+build+run script (all patches embedded; `python3 build.py`
  reproduces every cell).
- `verify.py`: kill-bar evaluation against the frozen predictions.
- `evidence/`: per-cell `run1.txt`/`run2.txt` (byte-identical pairs), `meta.txt`
  (sha256), `sources.txt` (patched-source shas), `verdicts.json`.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Static checks: no rng/rand/seed tokens in any attack source; pure Zag
  (Python only for build/verify glue).
