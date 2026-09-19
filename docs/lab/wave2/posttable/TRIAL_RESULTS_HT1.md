# HT1 — Trial results: verified context switching under random switching

**Agent:** H · **Date:** 2026-09-19 · **Branch:** `tnn-native-lab` (no push)
**Prereg:** `../PREREG_HT1.md` · **Apparatus:** native Zag on this Linux VM
**Result: PASS — `HT1_FAILURES,0`, 11/11 checks, deterministic
(byte-identical across two runs).**

## The head-to-head (identical curriculum, both arms)

48 episodes, true regime flips p=1/6 per episode (seeded; **10 true
flips**), 15% learning-channel noise (above the toy's 10% LH-5 knee),
16-probe measurement blocks every 8 episodes (uncorrupted, read-only),
settle phase 8+8 episodes + 16 probes per regime at endpoint.

| Metric | CTX (no table) | Toy (R34 v3, unmodified) |
|---|---|---|
| Switches (10 true flips) | **11** | **357** |
| Collapsed blocks (≤4/16) | **0** | **2** (both 0/16) |
| Block positives /16 | 16,16,16,16,16,16 | 0,16,16,16,0,16 |
| Endpoint regime 0 | **16/16** | 16/16 |
| Endpoint regime 1 | **16/16** | **0/16 — regime destroyed** |

The toy's failure is the LH-5 signature exactly: the single-sample switch
rule turns 15% noise into a 35× switch-storm (357 switches for 10 real
flips), collapses whole blocks to 0/16, and destroys a regime at endpoint.
The CTX mechanism: 11 switches for 10 flips, zero collapsed blocks,
16/16 in both regimes at endpoint.

## What the CTX arm proves

1. **The corroboration rule holds under noise the toy dies on.**
   `ctx_switch_verified_scan` (audit-level): every committed SWITCH had
   target majority-positive AND old-active majority-negative recorded
   evidence. No switch committed on doubt.
2. **The refusal path is real** (`unit_refusals`, separate scratch
   store): switch to a majority-negative target → `REFUSED_UNVERIFIED`,
   state untouched; switch while the active belief still measures good →
   `REFUSED_UNVERIFIED`; genuinely corroborated switch → commits.
3. **Conscious accounting** (MA1's test, re-proven): refusals never
   mutate state; ledger replay from genesis == exact live state.
4. **Structural:** two live partitions with distinct declared labels at
   endpoint — it maintains separate contexts, not one relabeled slot.
5. **Determinism:** two full runs byte-identical.

The one extra switch (11 vs 10 flips) is a noise-induced wrong commit
that the same corroboration machinery detected and corrected next
episode — recovery by the mechanism, not by luck. Endpoints stayed
16/16 regardless.

## Honest boundaries

- The *policy* (when to probe, which label to propose) is protocol-fixed
  in the harness. HT1 proves the *mechanism*; learner-driven probe/switch
  timing is HT2.
- `REFUSED_UNVERIFIED` never fired during the curriculum run itself
  (noise at 15% rarely produces ambiguous 16-probe majorities); the
  refusal path is proven by the unit tests, not by the curriculum.
- Partitions are never destroyed in HT1 (no KILL op) — random switching
  cannot cause knowledge loss by construction, but slot pressure over
  longer horizons is untested.
- Two regimes only. More regimes = more partitions; the mechanism is
  regime-count-agnostic but unproven beyond 2.

## What it means for the program

1. **The toy is replaced, not patched.** There is no score table, no
   accumulator, no `reward<0` trigger in CTX. LH-6-style scale-ups stay
   banned: the decision procedure was the problem, never the table size.
2. **Corroboration is now a structural property**, in the op
   implementation — the same layer that makes CORE unkillable. Doubt has
   a mechanism, not just a policy.
3. **The R27 shape holds at small scale:** propose → measure →
   commit-or-refuse, with the reason in the ledger. The 58-revision
   decision procedure has a native miniature.
4. Next: HT2 (learner-driven probe timing + label proposal), then
   unifying partitions with MA memory slots (a partition *is* a
   USER-region slot whose value is a declared label + evidence).
