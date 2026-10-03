# Amendment — FE3a signed (gated FE3b build authorized)

**Status:** SIGNED 2026-09-25, decided-autonomously-per-Micah's-order (PAM Round 4 autonomous governance dispatch).

## What was proved

(`docs/lab/pam/round4/gov_lh/repairs/VERDICT_CREW5_REPAIRS.md`, leg FE3a; `fe3a.zag` built with pinned znc, pure Zag, zero RNG; 3 runs byte-identical, sha256 `fe45c6d1…`; output byte-identical to the frozen Python prototype.)

Byte-identical sense-revision loop on the 10-exemplar toy:

```
it=0 T=100 reversals=1 first_rev=0 errs=10 T_next=99
it=1 T=99 reversals=1 first_rev=0 errs=8 T_next=98
it=2 T=98 reversals=1 first_rev=0 errs=6 T_next=97
it=3 T=97 reversals=0 errs=4 STOP
FINAL T=97 errs=4 iters=4
```

Matches the prereg's frozen prototype prediction exactly. **PASS** — the buildability kill-condition is discharged with measured evidence. (The 4 residual errors at convergence are the preregistered honest property of the toy: re-inspection agrees with the wrong A-window judgment there.)

## Effect

FE3b is buildable-in-principle; **the gated FE3b build may proceed under its own prereg**. This signature authorizes the build path only — FE3b itself is NOT adopted, tested, or judged by this signature. FE3b's own kill bars apply to its evidence when it lands.

*Signed 2026-09-25 — PAM Round 4 autonomous governance dispatch.*
