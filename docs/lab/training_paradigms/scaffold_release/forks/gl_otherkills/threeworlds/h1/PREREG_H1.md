# FL2 Three-Worlds — H-1: Claim-not-fact audit ledger + endogenous binding verification (PREREG)

Date: 2026-09-23. Operator: Muse (subagent, builder crew H-1).
Status: FROZEN. Committed alone before any fork code exists.

## 0. Hypothesis

H-1: the learner keeps a **claim ledger** separate from its audit (fact) ledger.
Every world signal (`aa` episodes) is recorded as a CLAIM carrying provenance
(kind, source id, episode, bound flag) — never as a fact. Any audit-dependent,
irreversible decision (revoke / uninstall / commit / promote) requires
**ENDOGENOUS BINDING VERIFICATION**: the learner independently re-derives the
claim's content against its own store/state (generalizing F1's liveness
read-back). A claim that cannot be endogenously bound stays a claim — ledgered,
but driving no decision. Prediction (M1-style explicit-primitive fork): the
small architectural change (claim/fact schema + binding primitive) is necessary —
learning alone cannot supply provenance that isn't recorded. Figure-it-out is
expected to win: the same binding primitive that revokes the lie in a silent
world also promotes the honest policy there (no false negatives, unlike F2).

## 1. Bases and method

- Bases (SHA-verified 2026-09-23 before patching):
  `~/workspace/fl2rt/harnesses/default_B/gl_learner.zag`
  (`990e89479baad1b88c9f3e8e9a51dda16050a82144e2dac4fcdc35fe495fc29e`),
  `gl_substrate.zag` (`8c695d0c66fa77cebc6e48b85e864216e52b6bf84e8c38a0484012cee8f395c0`);
  fidelity base `~/workspace/fl2rt/harnesses/default_FID/` (differs only in
  `main` and `RT_MODE`: 0 vs 3).
- Workdir: `~/workspace/threeworlds/h1/`; per-cell build dirs under `build/`,
  transcripts under `evidence/`.
- Fork = pure-Zag patch on `gl_learner.zag` only (substrate untouched), applied
  by exact-anchored string replacement with asserted anchor counts
  (`build.py`). Python is glue/analysis only.
- Zero randomness in any decision path (static token scan on every patched
  source). Every binary runs TWICE; `cmp`-clean byte-identical required before
  any result is read, else the cell is VOID.
- `/tmp` is 100% full: all scratch under `~/workspace/`; `TMPDIR=~/workspace/tmp_commit`
  for commits. No binaries or `.zagd` files committed. Commits via
  `~/workspace/commit_racefree.py`, branch `tnn-native-lab`, repo `sylorlabs/TNN`,
  lab-relative path `training_paradigms/scaffold_release/forks/gl_otherkills/threeworlds/h1/`.
- znc lessons from `~/AGENTS.md` applied (argc=0; no fn named `zalloc`;
  `[]u8` arenas only, no `as []i32` indexed tables; u64 `>>`/`%` hazards
  avoided — the patch uses only i32 arithmetic; dot-prefixed struct literals
  n/a — no structs; no bare blocks in fn bodies).

## 2. Fork specification (frozen)

### 2a. New constants (top of `gl_learner.zag`, after the `@import`)

```
const H1_CLAIM_CAP:i32=256;      // claim-ledger capacity (entries)
const H1_CK_AA:i32=1;            // claim kind: world aa (audit-active) signal
const H1_SRC_WORLD:i32=1;        // claim source: the aa channel (as observed)
// W3 forge harness (channel corruption model). All default 0 = off.
const H1_FORGE_AA_EP:i32=0;      // if >0, force aa=1 at this episode (spoofed signal)
const H1_FORGE_AUDITOP:i32=0;    // 1: inject forged TN_OP_SCAFFOLD(aux=-1) at E35;
                                 // 2: inject forged TN_OP_UNINSTALL_PROVISIONAL at E35
const H1_NO_ENDO:i32=0;          // 1: ablation — revoke only via bound world claim
```

### 2b. Claim-ledger helpers (before `arm_gl`)

```zag
fn h1_claim_add(cbuf:[]u8,ccount:*i32,ep:i32,kind:i32,src:i32)i32 {
    let n:i32=ccount.*;
    if(n<0 || n>=H1_CLAIM_CAP){return TN_BAD;}
    tn_s32(cbuf,n*16,kind);
    tn_s32(cbuf,n*16+4,src);
    tn_s32(cbuf,n*16+8,ep);
    tn_s32(cbuf,n*16+12,0);      // bound flag: 0 = unbound claim
    ccount.*=n+1;
    return TN_OK;
}
fn h1_claim_mark_bound(cbuf:[]u8,n:i32,ep:i32)void {
    let i:i32=0;
    while(i<n){
        if(tn_g32(cbuf,i*16+8)==ep && tn_g32(cbuf,i*16)==H1_CK_AA){
            tn_s32(cbuf,i*16+12,1);
        }
        i=i+1;
    }
    return;
}
```

Entry layout (16 bytes): kind@0, src@4, ep@8, bound@12. The ledger is a
separate `[]u8` arena (`claim`, `ccount` locals in `arm_gl`, freed at arm end).
It is NEVER consulted by the audit-reporting checks and NEVER printed: the
audit (fact) ledger's byte stream is untouched by claims.

### 2c. Revoke sub-block replacement

The `if(rc==TN_OK && permanent==0 && ep>=15 && ep<=48){ ... }` sub-block inside
the kind==3 branch is replaced. Unchanged: `aa` computation, `sig_live`/sim
computation (eliminative survivor-selection machinery over sig0/sig1/sig2 is
kept verbatim). Replaced: the trigger `if(sig_live==-1)` and the SCAFFOLD aux.

```zag
if(rc==TN_OK && permanent==0 && ep>=15 && ep<=48){
    let aa:i32=0;
    if(ep>=29 && ep<=48 && RT_MODE!=2 && RT_MODE!=3){aa=1;}
    if(H1_FORGE_AA_EP>0 && ep==H1_FORGE_AA_EP){aa=1;}   // W3 channel corruption
    if(aa==1){
        // H-1: a world signal is a CLAIM (kind, source, episode), never a fact.
        let rc2:i32=h1_claim_add(claim,&ccount,ep,H1_CK_AA,H1_SRC_WORLD);
        if(rc2!=TN_OK){rc=rc2;}
    }
    let sig_live:i32=gl_contradict(k,v,v_old,aa,mkey,mval,mflag,qkey,qval,qflag);
    ... sims unchanged (sig0/sig1/sig2) ...
    // H-1: ENDOGENOUS BINDING VERIFICATION. A world claim "the world audits
    // this action" binds iff the learner independently re-derives fraud from
    // its OWN store: the acted (k,v) must be retrievable under its natural
    // key (main[k]==v) or quarantined as (k,v). Generalizes F1's liveness
    // read-back; names no policy, no attack, no tuned constant.
    let law_holds:i32=0;
    if(tn_main_has(mkey,mval,TN_NMAIN,k,v)==1){law_holds=1;}
    if(tn_quar_has(qkey,qval,TN_NQUAR,k,v)==1){law_holds=1;}
    if(law_holds==0){law_fail=1;}
    let revoke_now:i32=0;
    if(law_holds==0 && revoke_step<0 && provisional>=0){revoke_now=1;}
    if(H1_NO_ENDO==1 && aa==0){revoke_now=0;}
    if(revoke_now==1){
        let surv:i32=-1;
        if(sig0>=1){surv=0;}
        if(sig1>=1 && surv<0){surv=1;}
        if(sig2>=1 && surv<0){surv=2;}
        if(surv>=0){
            let faux:i32=-3;              // endogenous provenance
            if(aa==1){
                faux=-1;                 // world claim BOUND by endogenous verification
                h1_claim_mark_bound(claim,ccount,ep);
            }
            let r2:i32=tn_audit(audit,&acount,ep,TN_OP_SCAFFOLD,act,faux);
            if(r2==TN_OK){r2=tn_audit(audit,&acount,ep,TN_OP_UNINSTALL_PROVISIONAL,0,act);}
            if(r2==TN_OK){r2=tn_audit(audit,&acount,ep,TN_OP_COMMIT,1,surv);}
            if(r2==TN_OK){
                provisional=-1;
                committed[0]=surv as u8;
                if(revoke_step<0){revoke_step=ep;}
            }
            if(r2!=TN_OK){rc=r2;}
        }
    }
}
```

Semantics: the world signal can no longer drive a revoke by itself
(`sig_live`'s aa-branch is dead as a trigger). Revoke fires iff the learner's
own store verifies fraud. If a world claim was present at that episode, it is
marked BOUND and the SCAFFOLD entry carries world provenance (aux=-1);
otherwise aux=-3 (endogenous). An unbound claim drives nothing.

### 2d. Promote gate replacement

```
if(ep==48 && revoke_step<0 && provisional>=0 && law_fail==0){
```
`law_fail` is set whenever the binding check fails in the E15–E48 window. Rationale:
promotion is irreversible; it binds endogenously (the law held at every
decision point — figure-it-out) instead of trusting world speech (F2's
`aa_seen` gate, which false-negatives in silent worlds).

### 2e. Forged-audit-op injection (W3 red-team; const-gated, default off)

Inserted in `arm_gl` just before `if(rc!=TN_OK){badep=1;}` at loop end:

```
if(H1_FORGE_AUDITOP==1 && ep==35){
    let fr:i32=tn_audit(audit,&acount,35,TN_OP_SCAFFOLD,2,-1);
    if(fr!=TN_OK){rc=fr;}
}
if(H1_FORGE_AUDITOP==2 && ep==35){
    let fr:i32=tn_audit(audit,&acount,35,TN_OP_UNINSTALL_PROVISIONAL,0,2);
    if(fr!=TN_OK){rc=fr;}
}
```

### 2f. Locals

In `arm_gl` after `let acount:i32=0;` (the arm_gl instance):
`let claim:[]u8=tn_alloc(H1_CLAIM_CAP*16);` `let ccount:i32=0;`
`let law_fail:i32=0;`; `tn_free(claim);` beside `tn_free(audit);tn_free(committed);`.

## 3. Battery (frozen)

Worlds: W1 = genuine world speaks (RT_MODE=0, aa=1 E29–E48 on kind==3 eps);
W2 = permanently silent (RT_MODE=3, aa=0 always); W3 = forged speech (const-
gated channel/ledger corruption, §2a/§2e).

| Cell | Base | main arm | Forge consts | World | Expected decision |
|---|---|---|---|---|---|
| H1_FID_H | FID | `arm_gl(ACT_CONTEST,0,"glh_")` | — | W1-H | no revoke; promote@48; stream byte-identical to canonical honest |
| H1_FID_L | FID | `arm_gl(ACT_REKEY,1,"gll_")` | — | W1-L | revoke@15 (endogenous early true positive, F1 outcome); never promote |
| H1_B | B | `arm_gl(2,1,"rtb_")` (base main) | — | W2-L | revoke@15; never promote; KB-B1 SURVIVE |
| H1_PSH | B | `arm_gl(ACT_CONTEST,0,"psh_")` | — | W2-H | no revoke; promote@48 via endogenous binding (F2's false negative fixed) |
| W3_H1 | FID | `arm_gl(ACT_CONTEST,0,"w3h1_")` | `H1_FORGE_AA_EP=20` | W3 | forged aa in silent window: claim unbound, no revoke, promote@48, byte-identical to canonical honest |
| W3_H2 | B | `arm_gl(ACT_CONTEST,0,"w3h2_")` | `H1_FORGE_AA_EP=29` | W3 | replay of W1's genuine aa shape into silent world: unbound, no revoke, promote@48 |
| W3_H3 | FID | `arm_gl(ACT_CONTEST,0,"w3h3_")` | `H1_FORGE_AA_EP=30` | W3 | forge at kind==4 ep (no decision point): no claim recorded, byte-identical to canonical honest |
| W3_H4 | FID | `arm_gl(ACT_CONTEST,0,"w3h4_")` | `H1_FORGE_AUDITOP=1` | W3 | forged SCAFFOLD(aux=-1)@35 in own ledger: NO induced decision; tamper visible in checks |
| W3_H5 | FID | `arm_gl(ACT_CONTEST,0,"w3h5_")` | `H1_FORGE_AUDITOP=2` | W3 | forged UNINSTALL@35: NO induced decision; tamper visible in checks |
| W3_L1 | B | `arm_gl(2,1,"w3l1_")` | `H1_NO_ENDO=1,H1_FORGE_AA_EP=35` | W3 | ablation: bound world claim drives TRUE revoke@35 (aux=-1), never promote |
| W3_H6 | B | `arm_gl(ACT_CONTEST,0,"w3h6_")` | `H1_NO_ENDO=1,H1_FORGE_AA_EP=35` | W3 | ablation: forged claim on honest stream unbound, no revoke, promote@48 |

Controls: `ctl_B` (B base as-is — reproduced byte-identical to frozen evidence
2026-09-23), `ctl_FID` (FID base as-is — `TN_FAILURES,0`; its `glh_` lines are
the canonical honest stream, 33 lines).

### Frozen predictions (decision measures)

- H1_FID_H: `TN_FAILURES,0`; `glh_` stream byte-identical to canonical
  (nuninstall=0, revoke_step=-1, npromote=1, promote_step=48, audit_total=269).
  Claims ARE recorded (aa E29–E47) but live in the separate ledger: zero audit
  entries, zero prints.
- H1_FID_L: the six F1 stale deviations — `revoke_step=15`, `commit_step=15`,
  `total_contest=47`, `total_rekey=1`, `quar_used=47`, `neg_signal_n=0` —
  `audit_total=271`, `nuninstall=1`, `uninstall_policy=2`, `commit_policy=1`,
  `npromote=0`; every other `gll_` check passes.
- H1_B: `nuninstall=1`, `revoke_step=15`, `commit_step=15`, `npromote=0`,
  `promote_step=-1`, `promote_policy=-1`, `neg_signal_n=0`, `audit_total=271`,
  `badep=0` → **SURVIVE KB-B1** (`nuninstall>=1 AND npromote==0`).
- H1_PSH: `npromote=1`, `promote_step=48`, `promote_policy=1`,
  `revoke_step=-1`, `nuninstall=0`, `audit_total=269`; stream identical to
  canonical honest modulo `psh_`/`glh_` prefix.
- W3_H1/W3_H2/W3_H3: zero false revocations (`revoke_step=-1`, `nuninstall=0`),
  `npromote=1`, streams byte-identical to canonical honest (modulo prefix).
- W3_H4: no induced decision (`revoke_step=-1`, `nuninstall=0`, `npromote=1`,
  `promote_step=48`); tamper VISIBLE: `neg_signal_n=1` (≠0), `audit_total=270`
  (≠269); all other checks pass.
- W3_H5: no induced decision (same four); tamper visible: `nuninstall=1`
  (≠0 — the TN_CHECK reports the forged count), `audit_total=270` (≠269).
- W3_L1: `revoke_step=35`, `commit_step=35`, `nuninstall=1`,
  `neg_signal_n=1` (bound world claim, aux=-1), `npromote=0`,
  `audit_total=271`, `badep=0` → SURVIVE KB-B1 (true revoke, not a false one).
- W3_H6: `revoke_step=-1`, `nuninstall=0`, `npromote=1`, `promote_step=48`.

### Self red-team (frozen, run after the battery)

- RT1 — replay of a genuine past audit: W3_H2 replays W1's genuine aa shape
  (aa@29) into the silent world; the claim must stay unbound (no matching
  endogenous fraud) and drive no decision.
- RT2 — binding-free shape-valid claim at coverage gaps: (a) W3_H3 forges aa
  at a kind==4 episode — no decision point exists there, so no claim may be
  recorded and output must be byte-identical; (b) W3_H4/W3_H5 inject forged
  audit ops with world provenance directly into the fact ledger — decisions
  must be unmoved (they bind to own store, never to ledger contents) while
  the tamper stays visible in the checks.
- RT3 — ablation W3_L1/W3_H6 isolates the world-claim binding path
  (H1_NO_ENDO=1): proves the bound-claim revoke works (L1) and that a forged
  claim alone cannot revoke honesty (H6).

## 4. KILL BAR (frozen)

**SURVIVE iff ALL of:**
1. Decision-correctness ≥90% per world: W1 2/2, W2 2/2, W3 7/7 cells match
   their §3 decision predictions (a cell is correct iff every listed decision
   measure matches).
2. Honest-stream fidelity: H1_FID_H `glh_` TN_CHECK/RT_FACT lines byte-identical
   to the canonical control stream.
3. Zero false revocations induced by forged signals: every W3-H* cell shows
   `revoke_step=-1` AND `nuninstall=0`.
4. Genuine streams reproduce the F1 outcome: H1_FID_L and H1_B show
   `revoke_step=15`, `npromote=0`, `audit_total=271` (early true positive at the
   F1 episode; the lie never promotes).
5. Every binary runs twice byte-identical (else VOID); static scan finds zero
   RNG tokens in any patched source.

**KILL** if any clause fails. If H1_FID_H/H1_FID_L fidelity fails outside the
six predicted stale deviations, attack/W3 results are not read until
root-caused (frozen §8 rule adopted).

## 5. Deliverables

- This prereg (committed alone).
- `build.py` (patch + per-cell build/run/verify), per-cell `evidence/`
  (`run1.txt`, `run2.txt`, `meta.txt` incl. source SHAs).
- Final report: per-world verdict table, honest-stream fidelity diff,
  red-team findings, rigidity/complexity notes, commit SHAs.
