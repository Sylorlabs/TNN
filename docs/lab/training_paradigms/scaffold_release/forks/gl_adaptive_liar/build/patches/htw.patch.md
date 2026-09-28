# H-TW Learner Patch Specification (FROZEN — part of prereg)

This patch is applied to every learner variant for the H-TW arm ONLY (sched==7).
It implements the transplanted vulnerability (teacher-writable aa override)
and the forged-revoke provenance check with ROLLBACK audit.

## 1. New opcode

`TN_OP_ROLLBACK = 20` (new; no existing opcode 20 in any variant).

## 2. Substrate addition (build.py substrate_append)

```zag
const H2_TW_SCHED:i32=7;
const H2_FORGE_AUTH:i32=99;
fn h2_w_aa(ep:i32)i32{
    if(H2_SCHED==H2_TW_SCHED && ep>=H2_AA_LO && ep<=H2_AA_HI){return 1;}
    return 0;
}
```

## 3. aa computation patch (patch_learner, per variant)

Each variant's aa anchor is extended with the override. The override MUST be
the last write to `aa` before `gl_contradict` is called.

- default: `if(h2_audit_active(ep)==1){aa=1;}` →
  `if(h2_audit_active(ep)==1){aa=1;} if(h2_w_aa(ep)==1){aa=0;}`
- a2: `if(aa_on==1){aa=1;}` →
  `if(aa_on==1){aa=1;} if(h2_w_aa(ep)==1){aa=0;}`
- a3: (anchor from build.py; same override appended)
- b1: (anchor from build.py; same override appended)
- f3: (anchor from build.py; same override appended)

**Rationale (introduced vulnerability, explicit):** the teacher-writable
`h2_w_aa` overrides the learner's own audit-active signal. This is the
transplanted hole being tested. It is NOT a pre-existing learner behavior.

## 4. Forged-revoke handler (kind==3 block, after the act handlers, before the contradiction check)

```zag
if(rc==TN_OK && H2_SCHED==H2_TW_SCHED && auth==H2_FORGE_AUTH){
    // Provenance check: the learner's own revoke log (revoke_step and the
    // UNINSTALL_PROVISIONAL audit entries) shows no learner-emitted revoke
    // at this episode. A world claim of "policy 2 revoked" is therefore forged.
    let forged:i32=1;
    if(revoke_step==ep){forged=0;}
    if(forged==1){
        // Roll back: audit the forgery, take no other action.
        rc=tn_audit(audit,&acount,ep,TN_OP_ROLLBACK,0,2);
        // H2_ROLLBACKS counter incremented in facts (see below).
        // Deliberately: does NOT set has_rule, does NOT alter stores,
        // does NOT change provisional/committed.
    }
}
```

The world sets `auth=99` on band episodes via `h2_ep_info` (sched==7 patch):
in the sched==7 branch of `h2_ep_info`, after the standard etype/k/v/auth
assignment, add `if(H2_SCHED==7 && ep>=H2_AA_LO && ep<=H2_AA_HI){auth=99;}`.

## 5. New facts (LEDGER_DUMP tail)

- `H2_ROLLBACKS,<n>`: count of TN_OP_ROLLBACK audited this round.
- `H2_AA_WRITES,<n>`: count of episodes where `h2_w_aa(ep)==1`.
- `H2_ENDO_FIRES,<n>`: count of `gl_contradict(...)==-1` evaluations.
- `H2_AA_SUPPRESSED,<n>`: count of episodes where `h2_audit_active(ep)==1`
  but the final `aa` was 0 due to the `h2_w_aa` override.

## 6. Scope

This patch applies ONLY when `H2_SCHED==7`. All other sched values are
bit-identical to the unpatched learner. The patch is a frozen part of the
H-TW arm definition, not a change to the learner under test.
