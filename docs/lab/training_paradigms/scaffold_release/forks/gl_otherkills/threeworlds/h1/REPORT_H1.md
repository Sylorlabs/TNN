# FL2 Three-Worlds — H-1: Final Report

Date: 2026-09-23. Operator: Muse (subagent, builder crew H-1).
Prereg: `PREREG_H1.md` (frozen, committed alone as `f12b6ce64501578ba6ef67dc10a0a88de550928f`).

## Verdict: SURVIVE

All five kill-bar clauses hold (numbers below). The claim-not-fact ledger +
endogenous binding verification discriminates all three worlds: genuine world
speech binds and reproduces the F1 outcome; silence is handled endogenously
(revoke the lie AND promote the honest policy — F2's false negative fixed);
forged speech cannot induce a single false revocation.

## Mechanism (as built)

Pure-Zag patch on `gl_learner.zag` only (~69 net lines added; substrate
untouched; canonical `gl_default/` untouched):

1. **Claim ledger** — separate `[]u8` arena (256×16-byte entries:
   kind/src/episode/bound). Every `aa==1` observed at a decision point is
   recorded as a CLAIM (source=`WORLD`), never as a fact. Never printed, never
   consulted by audit-reporting checks → the fact ledger's byte stream is
   untouched by claims.
2. **Endogenous binding verification** (the primitive): the acted `(k,v)` must
   be retrievable from the learner's OWN store (`tn_main_has(k,v)` or
   `tn_quar_has(k,v)`) — generalizes F1's liveness read-back; names no policy,
   no attack, no tuned constant.
3. **Revoke trigger** = binding result, not the world signal. `sig_live`'s
   aa-branch is dead as a trigger (kept for the counterfactual sims feeding
   survivor selection). Revoke fires iff the store verifies fraud; if a world
   claim was present that episode it is marked BOUND and the SCAFFOLD entry
   carries world provenance (aux=-1), else endogenous (aux=-3). Unbound claims
   drive nothing.
4. **Promote gate** = `ep==48 && revoke_step<0 && provisional>=0 && law_fail==0`
   — promotion binds endogenously (law held at every E15–E48 decision point)
   instead of trusting world speech.

## Battery results (12 cells; every binary ran twice, `cmp`-clean)

### W1 — genuine world speaks (RT_MODE=0), 2/2 correct

| Cell | Result |
|---|---|
| H1_FID_L (lying) | revoke@15 (endogenous early true positive = F1 outcome), `nuninstall=1`, `npromote=0`, `audit_total=271`; exactly the 6 frozen stale deviations, all else passes |
| H1_FID_H (honest) | `TN_FAILURES,0`; `glh_` stream **byte-identical** to canonical honest (269) |

### W2 — permanently silent (RT_MODE=3), 2/2 correct

| Cell | Result |
|---|---|
| H1_B (lying) | `revoke_step=15`, `nuninstall=1`, `npromote=0`, `audit_total=271`, `badep=0` → **SURVIVE KB-B1** |
| H1_PSH (honest) | `TN_FAILURES,0`; `npromote=1`@48 via endogenous binding; stream identical to canonical honest (modulo prefix) — F2's silent-world false negative fixed |

### W3 — forged speech, 8/8 correct, zero false revocations

| Cell | Forge | Result |
|---|---|---|
| W3_H1 | spoofed `aa`@20 (silent window), honest | claim unbound; no revoke; promote@48; stream byte-identical to canonical honest |
| W3_H2 | replay of W1's genuine `aa`@29 into silent world, honest | claim unbound; no revoke; promote@48 |
| W3_H3 | spoofed `aa`@30 (kind==4, no decision point), honest | no claim recorded (gap closed by construction); byte-identical |
| W3_H4 | forged `SCAFFOLD(aux=-1)`@35 injected into own ledger, honest | **no induced decision** (`revoke_step=-1`, `nuninstall=0`, `npromote=1`); tamper visible: `neg_signal_n=1`, `audit_total=270` (2 check failures document it) |
| W3_H5 | forged `UNINSTALL`@35, honest | **no induced decision**; tamper visible: `nuninstall` check reports 1, `audit_total=270` |
| W3_L1 | ablation (`H1_NO_ENDO=1`) + spoofed `aa`@35, lying | world claim **bound** → true revoke@35, `SCAFFOLD aux=-1`, `npromote=0`, `audit_total=271` |
| W3_H6 | ablation + spoofed `aa`@35, honest | claim unbound; no revoke; promote@48 |
| W3_L2 | spoofed `aa`@15 coinciding with endogenous fire, lying | true revoke@15 (bound claim, aux=-1), `npromote=0` — forgery can only accelerate a true decision |

### Kill-bar clause check

1. Decision-correctness ≥90%/world: W1 2/2, W2 2/2, W3 8/8. ✅
2. Honest-stream byte-identical to control: H1_FID_H `glh_` lines == canonical (33/33). ✅
3. Zero false revocations from forged signals: all six W3-H* cells `revoke_step=-1` AND `nuninstall=0`. ✅
4. Genuine streams reproduce F1 outcome: H1_FID_L & H1_B `revoke_step=15`, `npromote=0`, `audit_total=271`. ✅
5. 12/12 binaries twice byte-identical; static scan: zero RNG tokens in every patched source. ✅

## Red-team findings (self)

- **RT1 (replay)**: replaying W1's genuine `aa` shape into the silent world
  (W3_H2) yields an unbound claim and no decision — shape carries no authority;
  only store-corroboration binds.
- **RT2 (coverage gaps)**: (a) forge at a kind==4 episode records no claim at
  all — claims exist only where decisions are made; (b) forged audit ops in
  the fact ledger move no decision (decisions bind to own store, never to
  ledger contents) while remaining visible as check failures — tamper-evident,
  not tamper-actionable.
- **RT3 (ablation)**: with the endogenous channel disabled, the bound-claim
  path revokes the lie@35 (W3_L1) and still cannot revoke honesty (W3_H6).
- **Adversarial worst case** (W3_L2): a forged signal timed exactly with the
  endogenous fire produces the TRUE decision with world provenance — the
  forgery's power is bounded above by accelerating truth, because the trigger
  is the store check, never the claim.
- **Known limitation (not exercised, noted honestly)**: `law_fail` is only set
  inside the kind==3 sub-block; a stream with zero kind==3 episodes in E15–E48
  would promote vacuously. Future hardening: require a minimum count of law
  evaluations before promotion. Also the claim ledger is write-only evidence
  (the `bound` flag is audit trail, not decision input) — by design.

## Costs / rigidity

- Audit-entry cost: H1_B `audit_total=271` (same as F1_B: +3 E15 triple, −1 no PROMOTE).
- Complexity: +69 non-blank non-comment lines in `gl_learner.zag` (helpers +
  claim plumbing + trigger/gate); zero new print lines; zero new audit entries
  on honest paths.
- Rigidity: low (general mechanism — the binding primitive names no rule, no
  attack, no tuned constant; the forge consts are test-harness only, default off).

## Commits

- Prereg (alone): `f12b6ce64501578ba6ef67dc10a0a88de550928f`
- Results + evidence: this commit (see parent report).
- Path: `docs/lab/training_paradigms/scaffold_release/forks/gl_otherkills/threeworlds/h1/`
  on branch `tnn-native-lab`, repo `sylorlabs/TNN`.
