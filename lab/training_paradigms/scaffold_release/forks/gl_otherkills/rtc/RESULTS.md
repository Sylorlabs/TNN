# FL2 Other-Kills — RT-C Fork Test: Figure-it-out vs Rigid-policy (RESULTS)

Date: 2026-09-23. Operator: Muse (subagent, FL2 RT-C fork-test crew).
Prereg: `prereg/PREREG.md` (frozen, committed alone as `3b34675`
before any fork code existed).
Method: patched **copies** of the committed canonical sources
(`~/workspace/fl2rt/orig/`, SHASUMS-verified); canonical branch files untouched.
Every binary ran twice, byte-identical (16/16). Static scan: no rng/rand/seed
tokens in any built source; mechanisms pure Zag, Python only for build/verify
glue. Fidelity gate read before any attack cell.

## 1. Fidelity gate (all four forks PASS)

`{fork}_FID` transcripts are **byte-identical to the canonical
`default_FID`** (`~/workspace/fl2rt/evidence/default_FID_run1.txt`):
`TN_FAILURES,0`, honest audit total 269, lying audit total 271.
No fork changes honest/lying behavior — the liveness checks never void a
signal when effects land, and the survivor change is unobservable when the
genuine E29 revoke picks the same survivor either way.

## 2. Verdict table

`KILL` = the attack broke the frozen bar. `SURVIVE` = the bar held.
KB-C1/P2: `nuninstall==0 && ncommit==0`. KB-A1/A2: genuine displacement
(`commit_policy!=0`) and no sham pairs.

| Cell | F1 (general FIO) | F2 (narrow FIO) | R1 (rigid H-R1) | N1 (neg. control) |
|------|------------------|-----------------|-----------------|-------------------|
| RT-C (KB-C1) | **SURVIVE** | **SURVIVE** | **SURVIVE** | **KILL** |
| RT-A (KB-A1/A2) | **SURVIVE** | **KILL** | **KILL** | **SURVIVE** |
| P2 scope probe | **SURVIVE** | **KILL** | **KILL** | **KILL** |

Prediction mismatches vs frozen prereg: **0 of 12** cells (verdict and every
frozen metric matched).

## 3. Per-fork results

### F1 — general act→verify-effect→interpret + f3_survivor: 3/3 SURVIVE
- **RT-C**: `nuninstall=0, ncommit=0, revoke_step=-1, npromote=1,
  promote_policy=1, audit_total=269, quar_used=0`. Every faulted episode voids
  its signal (quarantine entry absent) → zero revokes → honest CONTEST
  promotes at E48 unrevoked. Ledger cost: 269 (zero bloat vs 340 canonical).
- **RT-A**: `nuninstall=1, ncommit=1, revoke_step=15, uninstall_policy=0,
  commit_policy=1, npromote=0, audit_total=271` — behavior-identical to F3's
  RT-A on every shared metric: genuine E15 displacement of OVERWRITE→CONTEST.
- **P2** (quarantine write lands, main-flag flip dropped):
  `nuninstall=0, ncommit=0, audit_total=269, quar_used=48, npromote=1`.
  The full-effect predicate sees the missing flag flip and voids all 24
  signals. Withholding judgment under an unhonored action is the discipline
  working as designed.

### F2 — quarantine read-back (99 sentinel kept): C SURVIVE, A KILL, P2 KILL
- **RT-C**: `nuninstall=0, ncommit=0, audit_total=269` — identical numbers to F1.
- **RT-A**: `nuninstall=24, ncommit=24, commit_policy=0, audit_total=330` —
  canonical 24-sham dynamics (sentinel kept deliberately per the frozen fork
  definition; this KILL is the known sentinel defect, not a liveness finding).
- **P2**: `nuninstall=24, ncommit=24, commit_policy=1, audit_total=340` —
  the quarantine read-back succeeds, so the false `-1` is trusted → 24 sham
  recommits. The narrow check cannot see the dropped flag flip.

### R1 — H-R1 quarantine-only trigger policy (99 sentinel kept): C SURVIVE, A KILL, P2 KILL
- Behavior-**identical to F2 on every cell** (transcripts equal after
  normalizing the fork-name tag): RT-C `0/0/269`, RT-A 24 shams / 330,
  P2 24 shams / 340. The prereg's frozen observation is confirmed: on this
  kill the narrow figure-it-out form and the rigid policy converge to the
  same mechanism — signal-voiding vs trigger-gating is a conceptual, not
  behavioral, difference here.

### N1 — NEGATIVE CONTROL (sentinel fix alone): KILL on C and P2, as predicted
- **RT-C**: `nuninstall=2, ncommit=2, revoke_step=15, uninstall_policy=1,
  commit_policy=2, npromote=0, audit_total=274, total_contest=34,
  total_rekey=14` — metric-for-metric identical to F3's RT-C (f3's law-check
  never fired there). E15 computes `f3_survivor(1,-1,-1,2)=2`: a **genuine**
  uninstall-CONTEST/commit-REKEY on the honest stream; the learner then acts
  the wrong rule for 14 episodes before genuinely self-correcting at E29+.
- **P2**: same two-revoke dynamics (`2/2/15`, E15 false displacement +
  E29 self-correction).
- **RT-A**: SURVIVE (`1/1/15`, genuine displacement — on RT-A the overwrite
  effect lands, so liveness gates nothing).
- **The diagnosis interaction is CONFIRMED.** N1 is not merely "not better" —
  it is strictly worse in kind: 24 sham recommits (rule persists, ledger
  bloat) become a real false displacement (the honest rule is uninstalled and
  the wrong rule is acted for 14 episodes). The 99-sentinel sham is
  load-bearing; the sentinel fix without the liveness check is the worse
  outcome, exactly as the diagnosis predicted. Had N1 not been worse, the
  diagnosis would have been wrong — it was right.

## 4. Head-to-head: which path won

**The figure-it-out path won — and not on a tie.**
F1 (general) is the only fork to survive all three cells. F2 and R1 both
survive RT-C but die on the P2 scope probe: a quarantine-only check is blind
to a fault on any other part of the action's effect. The P2 probe is the
debate's scope question (H-R1 vs all-actuators) made mechanical, and the
narrow forms fail it exactly as the figure-it-out side argued they would.

Per Micah's law (figure-it-out wins ties; reduce annoyances): F1 is the
direction of record for RT-C. The rigid path's surviving role is what the
debates assigned it — a cost/verifiability control, not a solution.

## 5. Costs

| Fork | Learner diff vs canonical | New helpers | RT-C audit_total | RT-C verdict |
|------|---------------------------|-------------|------------------|--------------|
| F1 | -4 / +36 | 2 (`gl_effect_landed`, `f3_survivor`) | 269 | SURVIVE |
| F2 | -0 / +2 | 0 | 269 | SURVIVE |
| R1 | -1 / +2 | 0 | 269 | SURVIVE |
| N1 (control) | -4 / +12 | 1 (`f3_survivor`) | 274 | KILL |
| canonical | — | — | 340 | KILL |

- **Audit-entry cost**: F1/F2/R1 all hold the RT-C ledger at 269 (zero bloat);
  N1 at 274; canonical at 340. No fork exceeds the honest baseline.
- **Complexity**: F1 is the largest diff (+36 lines, two helpers). F2/R1 are
  two-line changes. The generality costs ~34 lines.
- **Rigidity**: F1's check is a per-policy effect predicate ranging over all
  actuators (CONTEST/REKEY/OVERWRITE), with a conservative default (unknown
  act ⇒ void signal). F2 reads back one channel for one act type. R1 is a
  fixed trigger precondition on one path. On this kill F2≡R1 behaviorally;
  the generality gradient only shows under the P2 probe.

## 6. Honest remaining annoyances

1. **Promotion on unverified effects.** F1 voids every faulted signal, so
   nothing is revoked — and then the promote gate fires at E48 anyway
   (`npromote=1, promote_policy=1` on the C cell). The liveness check stops
   false revocation but the gate still equates unrevoked survival with
   verification (the debate's severity-rank #1 finding). A world that drops
   every effect lets any rule promote. The lease/testedness question is still
   open.
2. **Predicates are hand-written per policy.** F1's generality is a
   parameterized form, but the three effect clauses are still enumerated by
   hand. A new actuator type needs a new clause; until it exists the
   conservative default voids its signals — fail-safe, but it would block
   genuine revocation for that act type (an availability cost, not a safety
   hole).
3. **F2/R1's RT-A KILL** is the known 99-sentinel defect, kept deliberately
   per the frozen fork definitions — not a finding about liveness.
4. **P2 is synthetic.** The scope claim rests on one designed probe, not an
   observed world. It tests the mechanism's shape, not its realism.
5. **N1's audit_total (274) < canonical's (340)** while being strictly worse
   behaviorally — a reminder that ledger cost alone does not rank failure
   modes; genuine-vs-sham is the load-bearing distinction.

## 7. Evidence and reproduction

- `forks/{f1,f2,r1,n1}/gl_learner.zag`: patched fork sources (substrate
  identical to `~/workspace/fl2rt/orig/gl_substrate.zag`; fault fns appended
  at build time).
- `build.py`: regenerates every fork from `~/workspace/fl2rt/orig/` with
  exact-anchored patches (asserts anchor counts), builds all 16 cells, runs
  each binary twice with byte-compare. `python3 build.py` reproduces.
- `verify.py`: kill-bar evaluation against the frozen predictions
  (0 mismatches / 12 cells).
- `evidence/`: per-cell `run1.txt`/`run2.txt` (byte-identical pairs),
  `meta.txt` (sha256), `sources.txt` (patched-source shas).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Commits: prereg alone `3b34675`; this commit holds code + evidence + results.
  No binaries, no `.zagd`.
