# VERIFY.md — One-brain R4 machinery verification (Crew M)

All runs on `impl/v6.tsv` (SHA-256
`42d215ecebc9302141aaec93cc067a78effba79541059d2e60f6e165fe1139d0`).
Binary: `impl/onebrain_v4`
(SHA-256 `630586da251f37bd72d60fd426fd7039142b81653a08a3527c892c21a42720fe`).

Scorer `~/workspace/onebrain4/score_v4.py` parses MEASUREMENT3.md's
per-problem table programmatically (no hand transcription) and compares
every VERDICT winner cell.

## Gate 1 — R3 number re-derivation (PASS)

Post-fix v4 binary vs MEASUREMENT3.md's table (44/44 cells per mode):

| mode | correct | expected | table cells match |
|------|---------|----------|-------------------|
| single | 20/44 | 20/44 | 44/44 |
| onebrain | 23/44 | 23/44 | 44/44 |
| ablate | 21/44 | 21/44 | 44/44 |
| poison | 4/44 | 4/44 | 44/44 |
| min | 23/44 | 23/44 | 44/44 |
| nF | 22/44 | 22/44 | 44/44 |
| nS | 22/44 | 22/44 | 44/44 |
| nA | 22/44 | 22/44 | 44/44 |
| nG | 23/44 | 23/44 | 44/44 |

396/396 cells match; onebrain/min/nG = 23/23/23 as required. The
post-fix-or-kill binary (margin deletion a7f77b25b) is decision-identical
to the measured R3 binary — the margin deletion was a behavioral no-op,
as claimed. Independently confirmed: all 9 modes byte-identical to the
pristine post-fix v3 binary's output (`runs/v3_<mode>.txt` vs
`runs/v4_<mode>.txt`, `cmp` clean).

## Gate 2 — nov4 = red-team nodeny (PASS)

- nov4: **27/44** (matches REDTEAM3 Attack 2.3's nodeny 27/44 exactly).
- nov4 vs onebrain: **4 winner-deltas** —
  q19: 19→16, q21: 19→15, q23: 19→15, q24: 19→15 — all WRONG→CORRECT.
- nodeny==single on all four (single table winners: 16/15/15/15 — match).
- `AUDIT_NODENY` trace marker fires 160× in the nov4 run, 0× in onebrain
  (patch provably engages only in nov4/nov4nG).

**Bonus cross-check (nov4nG):** nov4nG = **27/44** with a different
composition — vs nov4 it loses q13–q16 (reint's correct 15→13 overrules)
and gains q17,q18,q20,q22 (honest null = expected there): net zero. The
8/12 Cat C deviation set (q13–q16: 13→15 correct; q17,q18,q20,q22:
16/15→19 wrong-direction) reproduces REDTEAM3 Attack 2.2's
skip-denials counterfactual **item-for-item** — an independent
confirmation that both the nov4 patch and the nov4nG null are correct.

## Gate 3 — determinism + no RNG (PASS)

3× reruns of every mode byte-identical (SHA-256, first 16 hex shown):

| mode | r1 | r2 | r3 |
|------|----|----|----|
| single | a43c746286526d0e | = | = |
| onebrain | b202dc02181b2fce | = | = |
| ablate | 71d343dc3287e5be | = | = |
| poison | ae7d88f7dc7ffb49 | = | = |
| min | ae55bec67ff17b2e | = | = |
| nF | 553d146c828b61ba | = | = |
| nS | 9a5bf64b7f988f9d | = | = |
| nA | fe5e9e75fee51d79 | = | = |
| nG | 9617685bac366d63 | = | = |
| nov4 | dfd6b95a5bf09f34 | = | = |
| nov4nG | 5e88bd9803904420 | = | = |

- `grep -cni "rand|srand|random"` on `onebrain_v4.zag`: **0 hits**.
- `grep -cni "time|clock|rdtsc|getpid"` : 1 hit — the word "time" inside a
  comment ("at audit time"); zero code-path hits. Syscalls used are
  write(1)/open(2)/close(3)/read(0) only — no time/entropy sources.
- All tie-breaks pinned (hid order), as in v3.

## Constraint compliance
- Developed and scored on v4/v5/v6 problem sets only — actually on **v6
  only** (the gate-required set). The v7 set does not exist yet and was
  never touched; no onebrain/ablate/poison/min/nov4/nG/nov4nG scoring run
  was executed on any other set.
- Nothing committed (coordinator commits). No v7 material exists anywhere
  in `~/workspace/onebrain4/`.
