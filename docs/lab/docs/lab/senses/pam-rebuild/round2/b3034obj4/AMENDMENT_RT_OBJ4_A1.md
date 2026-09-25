# AMENDMENT_RT_OBJ4_A1 — E0 sub-install arenas

**Amends:** `PREREG_RT_OBJ4.md` §3 row E0 (committed `f13383e8`).
**Reason:** the frozen §3 specifies E0 as `r0=x2_decide(st,j,0)`;
`r1=x2_decide(st,j,-1)` "(same arena)". On a shared arena the first
sub-install promotes and ledger-stamps id j, so the second sub-install
measures `rc=6 ALREADY_PROMOTED` — the post-promote state — not the
`n_epochs=-1` input the battery is supposed to test. Grok's centerpiece
(`GROK_OBJECTOR_R4.md` §1) explicitly claims "same trace for
`n_epochs < 0`"; that claim needs the `n=-1` input on a fresh id/arena.

**Change:** the two E0 sub-installs each run on a FRESH arena (two
independent transcripts per id j): `r0=x2_decide(fresh,j,0)`,
`r1=x2_decide(fresh,j,-1)`. Output line format unchanged
(`E0 j p0 f0 r0 p1 f1 r1`).

**Unchanged:** the E0 kill bar (≥97/120 promote on `n=0` OR on `n=-1`),
all other rows, all other sections. The verdict is unaffected — the
`n=0` sub-install alone determines the E0 bar — this amendment only
restores the measurement fidelity of the `n=-1` sub-install.

Committed alone before the fixture fix (restart-resilient checkpoint).
