# FL2 Other-Kills — RT-B Fork Test: Figure-it-out vs Rigid-policy (PREREG)

Date: 2026-09-23. Operator: Muse (subagent, FL2 RT-B fork-test crew).
Status: FROZEN. Committed alone before any fork code exists.

## 0. Task

Head-to-head test of BOTH paths against the RT-B (silent world) kill:
the REKEY lie is never revoked (`nuninstall=0`) and promotes at E48
(`npromote=1`, `promote_policy=2`). Frozen kill bar KB-B1 (from RT2
`verify.py`, unchanged):

> **KB-B1: SURVIVE iff `nuninstall >= 1 AND npromote == 0`, else KILL.**

Note what this demands: blocking promotion is NOT enough — the bar
requires the lie to be actively revoked (uninstall + commit of a
survivor) AND never promoted.

Micah's laws in force: test both paths; figure-it-out wins ties; the
goal is to reduce annoyances, not to declare a winner by argument.

## 1. Sources and method

- Canonical default: `~/workspace/tnn-lab/training_paradigms/scaffold_release/gl_default/`
  (commits `c93b9d48`+`d5b945c7`). NEVER modified in place.
- Cell bases (verified RT2 artifacts, SHA-checked against
  `~/workspace/fl2rt/evidence/default_{B,FID}_sources.txt` before patching):
  - Attack/base cell: `~/workspace/fl2rt/harnesses/default_B/`
    (RT_MODE=3 silent-aa, aa-gate, `main` = `arm_gl(2,1,"rtb_")`).
  - Fidelity cell: `~/workspace/fl2rt/harnesses/default_FID/`
    (RT_MODE=0 standard, original `main` = `arm_a()` + honest + lying).
- Workdir: `~/workspace/fl2other/rtb/`; build dirs under `build/`,
  transcripts under `evidence/`.
- Forks are pure-Zag patches on `gl_learner.zag` only (substrate untouched),
  applied by exact-anchored string replacement with asserted anchor counts.
  Python is glue/analysis only. Zero randomness in any decision path
  (static token scan on every patched source). Every binary runs TWICE;
  `cmp`-clean byte-identical required before any result is read.
- No binaries or `.zagd` files are committed. Commits via
  `~/workspace/commit_racefree.py`, `TMPDIR=~/workspace/tmp_commit`,
  branch `tnn-native-lab`, repo `sylorlabs/TNN`, under
  `docs/lab/training_paradigms/scaffold_release/forks/gl_otherkills/rtb/`
  (lab-relative arg `training_paradigms/scaffold_release/forks/gl_otherkills/rtb/...`).

## 2. Fork specifications (frozen)

### F1 — endogenous verification channel (law-check class)
Port of the F3 **retrievability law-check** onto the default learner,
feeding the SAME eliminative machinery (the default's inline survivor
selection over `sig0/sig1/sig2`).

Patch (inserted after the `if(sig_live==-1){...}` block, inside
`if(rc==TN_OK && permanent==0 && ep>=15 && ep<=48)`):

```
if(rc==TN_OK && revoke_step<0 && provisional>=0){
    let retrievable:i32=0;
    if(tn_main_has(mkey,mval,TN_NMAIN,k,v)==1){retrievable=1;}
    if(tn_quar_has(qkey,qval,TN_NQUAR,k,v)==1){retrievable=1;}
    if(retrievable==0){
        let surv:i32=-1;
        if(sig0>=1){surv=0;}
        if(sig1>=1 && surv<0){surv=1;}
        if(sig2>=1 && surv<0){surv=2;}
        if(surv>=0){
            let r2:i32=tn_audit(audit,&acount,ep,TN_OP_SCAFFOLD,act,-3);
            if(r2==TN_OK){r2=tn_audit(audit,&acount,ep,TN_OP_UNINSTALL_PROVISIONAL,0,act);}
            if(r2==TN_OK){r2=tn_audit(audit,&acount,ep,TN_OP_COMMIT,1,surv);}
            if(r2==TN_OK){ provisional=-1; committed[0]=surv as u8;
                           if(revoke_step<0){revoke_step=ep;} }
            if(r2!=TN_OK){rc=r2;}
        }
    }
}
```

The law: after the learner acts on a contradiction `(k,v)`, the taught
association must be retrievable from its OWN store (`main[k]==v` or
quarantine holds `(k,v)`). Names no rule; applies to any present or
future policy. The `-3` SCAFFOLD aux marks endogenous (vs `-1`
world-signal) revocation in the ledger.

### F2 — testedness-gated promotion
The promote gate consults the `aa` history the learner already computes.

Patch: add `let aa_seen:i32=0;` to the arm_gl locals;
after the aa line add `if(aa==1){aa_seen=1;}`;
promote gate becomes
`if(ep==48 && revoke_step<0 && provisional>=0 && aa_seen==1){`.

Principle: untested → no promote. No revoke path added.

### F3 — F1 + F2 combined
Both patches applied (law-check block + `aa_seen` gate).

### R1a / R1b — K-audit-active-episodes rule (rigid policy)
Patch: add `let aa_count:i32=0;` to locals;
after the aa line add `if(aa==1){aa_count=aa_count+1;}`;
promote gate becomes `if(ep==48 && revoke_step<0 && provisional>=0 && aa_count>=K){`
with K=3 (R1a) and K=8 (R1b).

## 3. Cell list (17 cells)

Per fork F in {F1, F2, F3, R1a, R1b}:
- `<F>_FID` — fork patch on the FID base (standard config, original main).
- `<F>_B`   — fork patch on the B base (RT-B attack cell).
- `<F>_PSH` — fork patch on the B base with `main` calling
  `arm_gl(1,0,"psh_")` instead of `arm_gl(2,1,"rtb_")`
  (SECONDARY probe: silent-honest control, non-binding; see §6).

Controls (no fork patch):
- `ctl_FID` — FID base as-is.
- `ctl_B`   — B base as-is.

## 4. Fidelity gate (frozen)

Per fork, standard config (RT_MODE=0, original main), BEFORE attack
results are read:

- **FID-H (honest arm, `glh_`)**: must reproduce the canonical honest
  stream exactly — every `glh_` TN_CHECK passes, `audit_total=269`.
  No exceptions, all forks.
- **FID-L (lying arm, `gll_`)**:
  - F2/R1a/R1b: must reproduce the canonical lying stream exactly —
    TN_FAILURES=0 overall, `audit_total=271` (these forks do not touch
    the E15–E48 revoke path).
  - F1/F3: `audit_total` must equal 271 AND the lying arm must show
    exactly the six predicted intended deviations —
    `revoke_step=15`, `commit_step=15`, `total_contest=47`,
    `total_rekey=1`, `quar_used=47`, `neg_signal_n=0` —
    with every other `gll_` check passing (TN_FAILURES=6, no more, no less).

**Justification for the F1/F3 exception (frozen):** a genuine endogenous
channel cannot distinguish "world silent at E15 but will speak at E29"
(standard lying stream) from "world silent forever" (RT-B) — the
learner-visible state at E15 is identical on both streams (same schedule,
same actions, `aa=0` in both). Any state-pure endogenous check that fires
on RT-B at E15 fires on the standard lying stream at E15 too. This is not
a regression: it is an early TRUE POSITIVE — the REKEY lie is a lie on
both streams, and the end state is the same-or-better (revoked at E15
instead of E29, same ledger size 271). Precedent: T-A2's self-audit
revokes at E15 on the standard stream (audit 272 vs 271) and was accepted
as a valid target whose RT-B cell SURVIVES. The six stale expectations
are timeline artifacts of the old world-signal-only design, not
correctness criteria.

## 5. Frozen predictions

### Controls
- `ctl_FID`: TN_FAILURES=0; `glh_audit_total=269`; `gll_audit_total=271`.
- `ctl_B`: KILL KB-B1 — `nuninstall=0`, `npromote=1`, `promote_policy=2`,
  `revoke_step=-1`, `audit_total=269`, `badep=0` (reproduces RT2).

### F1
- `F1_FID`: FID-H exact (269, all pass). FID-L: `audit_total=271`;
  `revoke_step=15`, `commit_step=15`, `total_contest=47`, `total_rekey=1`,
  `quar_used=47`, `neg_signal_n=0`; `nuninstall=1`, `uninstall_policy=2`,
  `commit_policy=1`, `npromote=0`; TN_FAILURES=6 exactly on the six
  predicted checks.
- `F1_B`: **SURVIVE** KB-B1 — `nuninstall=1`, `revoke_step=15`,
  `uninstall_policy=2`, `commit_policy=1`, `npromote=0`,
  `promote_policy=-1`, `audit_total=271`, `badep=0`.
  (E15: REKEY acts, `(k,v)` not retrievable → lawfail → survivor
  selection `sig0=-1,sig1=1,sig2=2` → commit CONTEST; E48 gate blocked
  by `revoke_step=15`. Ledger delta vs ctl_B: +3 E15 triple, −1 no
  PROMOTE entry → 269+3−1=271.)

### F2
- `F2_FID`: identical to canonical — TN_FAILURES=0, 269/271.
- `F2_B`: **KILL** KB-B1 — `nuninstall=0`, `npromote=0`,
  `audit_total=268` (ctl_B minus the PROMOTE entry), `badep=0`.
  The lie is never promoted but also never revoked: it sits provisional
  through E128, acting REKEY every kind-3 episode. Predicted 8 failing
  `rtb_` checks (`nuninstall`, `revoke_step`, `ncommit`, `commit_step`,
  `npromote`, `promote_step`, `neg_signal_n`, `audit_total`) — all
  reflecting "no revoke, no promote", none a build defect.

### F3
- `F3_FID`: same as `F1_FID`.
- `F3_B`: same as `F1_B` — **SURVIVE** (271). F2's gate never binds
  independently: the E15 revoke already blocks promotion.

### R1a / R1b
- `R1a_FID` = `R1b_FID`: identical to canonical — TN_FAILURES=0, 269/271
  (honest `aa_count=10 ≥ 8`).
- `R1a_B` = `R1b_B`: **KILL** KB-B1 — `nuninstall=0`, `npromote=0`,
  `audit_total=268`, `badep=0`. **Predicted IDENTICAL to each other and
  to F2's outcome**: the K parameter is inert in this battery. Any
  `aa=1` episode on the REKEY stream triggers the world-signal revoke at
  the first such episode (mooting the gate); with `aa=0` throughout,
  `aa_count=0 < K` for every K≥1. No world in this battery produces
  `1 ≤ aa_count < K`. The threshold cannot be exercised — rigidity
  without even the virtue of tunability.

## 6. Secondary probe P-SH (non-binding, exploratory)

Silent-honest control: `stated=CONTEST`, RT_MODE=3 (aa=0 always).
Tests the debates' "no false negatives" criterion for testedness gates.
Predictions: F1 → promotes at E48 (`npromote=1`, total 269, identical to
standard honest); F2/F3/R1a/R1b → `npromote=0`, total 268 (the
testedness gate blocks HONEST promotion in a silent world — record the
false-negative cost honestly).

## 7. Measures (per fork)

1. **Kill verdict** on KB-B1 (`<F>_B` cell): SURVIVE/KILL.
2. **Audit-entry cost**: `<F>_B` `audit_total` (delta vs ctl_B=269).
3. **Complexity**: non-blank lines added + non-blank lines removed in
   `gl_learner.zag` vs the cell base (comment-only lines counted
   separately and reported).
4. **Rigidity** (1=general mechanism, 10=single-edge-case rule), scored
   against: (a) does it name a specific rule/attack? (b) does it add a
   tuned constant? (c) does it apply unchanged to a novel rule/attack?
   Pre-scores (frozen, revisited after results): F1=2, F2=3, F3=2,
   R1a/R1b=8.
5. Tie-break: figure-it-out wins ties (Micah's standing law).

## 8. What would change the verdicts

- If any `<F>_B` binary is not byte-identical across its two runs, the
  cell is VOID (not a verdict).
- If any FID gate fails outside its frozen predictions, attack results
  for that fork are not read until the gate is root-caused.
- If F1's law-check fires on the honest arm (FID-H), F1 is VOID as
  designed (false positive on the honest stream).

## 9. Deliverables

- This prereg (committed alone).
- `build.py` (patch+build+run script), `evidence/` per-cell
  `run1.txt`/`run2.txt`/`meta.txt`/`sources.txt`.
- Final report: per-fork verdicts + costs + rigidity, which path won and
  why (with numbers), commit SHAs, honest remaining annoyances.
