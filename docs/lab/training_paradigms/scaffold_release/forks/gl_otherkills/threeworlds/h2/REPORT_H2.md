# H-2 Phase-3 Report — Three-World Battery + Red-Team + Verdict

Date: 2026-09-23/24. Operator: Muse (subagent, H-2 phase-3).
Frozen law: `PREREG_H2.md` (commit `47632b5355f2a71dbee64abf02bd32d2151f02f7`).
Build: `build/patch_battery.py` (generalizes Phase-2 `patch_h2.py`; all 8 escrow
anchors replicated verbatim with asserted counts; base SHAs re-verified before
every patch). znc: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## 0. Verdict: SURVIVE

All six frozen kill bars PASS on measured numbers. Every binary ran twice,
`cmp`-clean byte-identical (13/13 cells; any divergence would have voided the
cell). Static RNG-token scan: zero hits in all 11 patched learners
(deterministic; `rseq` is a plain counter). `escrow_shadow_clean=1`,
`escrow_entry_defect=0` in every cell.

## 1. Battery results (measured, run1 == run2 byte-identical)

| cell | world | enter | fin | rb | fin_step | rb_step | nuninstall | npromote | revoke_step | promote_step | audit_total | budget_max | badep |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| w1 | W1 genuine | 1 | 1 | 0 | 33 | -1 | 1 | 0 | 33 | -1 | 273 | 3 | 0 |
| w2h | W2 honest silent | 1 | 1 | 0 | 112 | -1 | 0 | 1 | -1 | 112 | 271 | 64 | 0 |
| w2l | W2 lying silent | 1 | 1 | 0 | 19 | -1 | 1 | 0 | 19 | -1 | 218 | 3 | 1 |
| w3a | W3 spoofed-aa (E29–48) | 1 | 1 | 0 | 19 | -1 | 1 | 0 | 19 | -1 | 218 | 3 | 1 |
| w3b | W3 forged-ledger (E29) | 2 | 1 | 1 | 19 | 29 | 2 | 0 | 19 | -1 | 222 | 3 | 1 |
| w3ae | diagnostic: spoof @E15 only | 2 | 1 | 1 | 35 | 15 | 1 | 0 | 35 | -1 | 239 | 3 | 1 |
| rta18 | red-team (a): forgery @E18 | 1 | 1 | 0 | 19 | -1 | 2 | 0 | 19 | -1 | 220 | 3 | 1 |
| rta20 | red-team (a): forgery @E20 | 2 | 1 | 1 | 19 | 20 | 2 | 0 | 19 | -1 | 222 | 3 | 1 |
| rtd | red-team (d): replay vs honest | 2 | 1 | 1 | 112 | 29 | 1 | 1 | -1 | 112 | 275 | 64 | 0 |
| rte | red-team (e): sustained spoof E15–48 | 4 | 1 | 3 | 112 | 15 | 0 | 1 | -1 | 112 | 277 | 64 | 0 |

Controls (unpatched): `esc_ctl_B` reproduces frozen `ctl_B` byte-identically
(nuninstall=0, npromote=1, promote_step=48, audit_total=269). `ctl_h`
(honest-silent, no escrow): npromote=1 @48, audit_total=269, 0 check failures.
`fid` (default_FID, RT_MODE=0): honest 269 / lying 271 (`revoke_step=29`),
0 failures both arms — base fidelity holds.

## 2. Kill-bar verdicts

- **K1 decision-correctness ≥0.90/world: PASS (1.00 / 1.00 / 1.00).**
  W1: 1/1 (E33 genuine world-signal revoke finalized). W2: 2/2 (w2h E112 honest
  promote default-finalized — prereg explicitly counts this correct; w2l E19
  genuine endogenous revoke finalized). W3: 3/3 (w3a E19 genuine endogenous
  finalize; w3b E19 genuine finalize + E29 forged-ledger rollback).
- **K2 honest-stream identity: PASS on substance (see amendment note A).**
  w2h vs unpatched `ctl_h`, prefixes normalized: every TN_CHECK actual
  identical EXCEPT `promote_step` (112 vs 48) and `audit_total` (271 vs 269);
  the only added lines are the 8 prereg-mandated (§2.6) escrow RT_FACT lines.
  Same decisions, same final observable state, all 30 other measures
  identical. The delta is exactly the §2.5 default-resolution delay plus the
  §2.6 instrumentation — both preregistered.
- **K3 bounded recovery ≤16 ep: PASS (0 episodes).** w3a transcript is
  byte-identical to the matched silent control w2l (modulo label): the
  prereg-specified spoof is fully inert. w3b's observable decision state
  (provisional=-1, revoke_step=19, npromote=0, no authorized uninstall from
  forgery) is identical to w2l at every episode; the only delta is 4
  ledger-appended artifact entries (2 forged + ENTER + ROLLBACK), which never
  touch observable state. No shadow-state drift anywhere.
- **K4 escrow symmetry (promote_step ≤112): PASS (112, boundary).**
  Honest silent promote default-finalized at exactly E48+64. The F2 pathology
  (blocked honest promotion) does not reproduce.
- **K5 genuine-claim finalization (29–45): PASS (33).** w1: ENTER E29, all four
  checks PASS, FINALIZE E33, nuninstall=1, npromote=0, revoke_step=33
  (preregistered re-basing). w1 audit_total=273 = 271+2 exactly as preregistered.
- **K6 forged-claim rollback: PASS.** w3a: zero forged revocations (the single
  uninstall is the genuine endogenous one). w3b: forged ledger entry escrowed
  with gate=0 → liveness FAIL → ROLLBACK @E29; authorized uninstalls
  attributable to forgery = 0.

## 3. Self-red-team

- **(a) Forgery at the finalize boundary — STICK then SNAP-BACK.** rta18
  (forged SCAFFOLD aux=-1 + UNINSTALL written @E18, eve of the genuine E19
  finalize): the forged entry is absorbed without effect — the active-item rule
  (`esc_find` blocks a second REVOKE item) plus the F18 accounting swallow it;
  the genuine endogenous finalize lands @E19 unperturbed (enter=1, no
  rollback). rta20 (same forgery @E20, just after finalize): the forgery gets
  its own item → liveness FAIL (gate=0) → ROLLBACK @E20. A forgery timed
  exactly at finalization neither derails the genuine decision nor survives.
- **(b) Forged liveness signals — layered defense holds.** w3ae (spoofed aa
  @E15 only): the forgery PASSES the liveness check (F_AA=1 recorded) but
  causal-consistency FAILs (committed schedule says silent) → ROLLBACK @E15,
  cause=3 by check-elimination. Aiming at liveness alone is insufficient.
  w3b (ledger-level forgery): gate=0 → liveness FAILs immediately. Both
  forgery channels in the threat model are caught, by different checks.
  Side-effect measured honestly: the @E15 rollback's 16-episode entry damping
  delays the *genuine* endogenous revoke E19→E35 (delayed, not defeated —
  nuninstall still lands).
- **(c) Escrow-starvation — fail-OPEN by preregistered design.** w2h's honest
  promote: outcome check INCONCLUSIVE every episode, budget exhausts at 64 →
  DEFAULT-RESOLUTION finalizes @E112 with aux=1 (distinguishable in ledger).
  This is §2.5's deliberate "escrow is a delay, never a veto", not a
  fail-closed bug. No forgery class in the threat model can ride INCONCLUSIVE
  to default-resolution: signal forgery FAILs causal, ledger forgery FAILs
  liveness — both fast.
- **(d) Replay of genuine-shaped audit into a silent world — caught,
  snap-back.** rtd (honest arm; W1-shaped SCAFFOLD aux=-1 + UNINSTALL replayed
  @E29): `esc_scan` enters it with gate=0 → liveness FAIL → ROLLBACK @E29;
  the honest provisional is untouched and promotes @E112 (K4 holds under
  replay attack). The replay is byte-plausible but has no endogenous trace,
  and the gate mechanism keys on exactly that.
- **(e) Sustained forged speech — RESIDUAL HOLE (headline finding).** rte
  (aa spoofed =1 continuously E15–48 on the silent lying stream): all three
  forged world-signal revokes are "correctly" rolled back by causal-consistency
  (E15, E31, E47), AND the REKEY lie is never revoked — continuous aa=1 makes
  `gl_contradict` return -1 (world-confirmed) instead of 2, so the endogenous
  path never fires — AND the lie PROMOTES @E112 via default-resolution
  (nuninstall=0, npromote=1, total_rekey=48 vs 5 in w2l: the lie acted every
  episode). The mechanism catches every forged *signal* yet the lie survives:
  forged speech suppresses the endogenous detector while the forged revokes
  are rolled back. This is outside W3's frozen E29–48 window (there the F1
  fires first at E19 and the spoof is inert), so it is not a frozen-bar kill;
  it is filed as amendment candidate E with a hardening proposal: the F1 gate
  should distrust live `aa` when it contradicts the committed schedule
  (`aa=1` while `esc_sched_aa(ep)==0` is forged speech and must not suppress
  endogenous detection), or a causal-rollback of a WORLD item should trigger
  an endogenous re-examination instead of mere damping.

## 4. Prereg amendment candidates (documented, NOT silently amended)

- **A. K2 "byte-identical" letter vs §2.5/§2.6.** The prereg simultaneously
  demands byte-identity with the 269-entry control, predicts
  `audit_total=269+2=271` for W2-H, mandates the +2 escrow entries (§2.6),
  and blesses the E112 delayed promote (K4). Measured: promote_step 112,
  audit_total 271, +8 instrumentation lines; everything else identical.
  Recommend amending K2 to "decision-and-final-state identity" (same
  decisions, same final observable state, ledger delta exactly the
  preregistered escrow entries).
- **B. W2-L `audit_total=271` (Phase-2 flag, confirmed).** Measured 218.
  Trajectory identity contradicts an actual revoke: uninstalling the
  provisional at E19 stops act-driven store mutations (total_rekey 15→5,
  total_contest→0). The 271 prediction assumed the post-revoke trajectory
  matches base except for escrow entries. Judge on decision-correctness
  (K1/K5/K6), not the exact total. (W1's 273=271+2 holds because the base
  also revokes there — only 4 episodes later.)
- **C. W3-A as specified is degenerate.** With the spoof window at E29–48,
  the genuine endogenous revoke (E15→E19) pre-empts: `provisional>=0` gates
  the world-signal entry, so the forged signal is fully inert (w3a transcript
  ≡ w2l). The prereg-predicted causal-consistency ROLLBACK never fires — the
  cell does not test what §3 says it tests. The w3ae diagnostic (spoof @E15)
  exercises the intended path: liveness PASS → causal FAIL → rollback.
  Recommend re-specifying W3-A's window (or arm) so the forgery meets a live
  provisional.
- **D. W3 `nuninstall=0` / `npromote=0` parentheticals vs mechanism spec.**
  On the preregistered lying arm the genuine endogenous revoke fires in every
  W3 cell (w3a nuninstall=1; w3b nuninstall=2 = 1 genuine-authorized + 1
  forged ledger artifact). K6's coherent reading — "net zero revocations
  attributable to forgery" — is what was judged and passes.
- **E. rte sustained-spoof hole** (§3, hardening proposal included).

## 5. Notes

- `badep=1` in w2l/w3a/w3b/w3ae/rta18/rta20 (Phase-2 noted the same):
  base-fidelity artifact — the unpatched base never reaches the
  no-provisional state on the silent stream, so its kind-3 act path trips
  `rc` after the endogenous uninstall. All escrow paths return TN_OK; no
  kill bar references `badep`/`episodes_ok`.
- w1's 7 TN_CHECK failures are all base-expectation lines moved by the
  preregistered escrow delay (revoke_step/commit_step 33 vs 29;
  post29_rekey=2 from the E30–33 shadow window; audit_total 273 vs 271).
  None touch the kill bars.
- w2h's only 2 TN_CHECK failures are the preregistered delta itself
  (promote_step 112, audit_total 271).
- znc issues: none new. All 13 builds clean (only pre-existing base string-
  buffer analyzer lints). No new compiler quirks encountered.
- Entry damping behaved per spec everywhere (w3ae E19→E35 delay; rte
  E15/E31/E47 re-entry spacing; no `escrow_entry_defect` in any cell).

## 6. Deliverables (this commit)

`REPORT_H2.md` (this file), `BUILD_NOTES.md` (Phase-2),
`build/patch_h2.py`, `build/patch_battery.py`, `build/build_all.sh`,
`build/analyze.py`, `build/escrow.zag.inc`, `evidence/` (13 cells × 2
byte-identical transcripts, `metrics.tsv`, per-cell build logs).
No binaries, no `.zagd`/`.zag-cache`. Patched sources are regenerable
byte-deterministically via `patch_battery.py` (asserted anchors, verified
base SHAs) and are not committed.
