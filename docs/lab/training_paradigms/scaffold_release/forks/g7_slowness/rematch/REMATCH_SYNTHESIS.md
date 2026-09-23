# REMATCH SYNTHESIS — G7 Q5 (three pure-Zag rematches)

Terminology note: this document uses "guided learning (gl)" for the
paradigm (Micah's 2026-09-23 naming decision); "guided-learning" in
code identifiers is unchanged.

## The three questions, answered

### 1. Was FL2 independently REPLICATED? — YES

R1 rebuilt the committed FL2 sources byte-identically (`cmp` clean),
re-ran them under its own G1-pattern runner, and matched all 78/78
frozen-prereg checks with zero divergence (`TN_FAILURES=0`). The
evidence SHA exactly matched the prior FL2 crew's reported evidence SHA
(`20fee727aaf7746c7b86e93e6bf441381dab9e1e1f4d85437e0b7c5882582263`).
KB-1 through KB-6 held; honest FREE LUNCH and lying FULL FREE LUNCH held.
Committed `3288127575aca623f31d70d97de0a1d6d50ab20`.

### 2. Did D1b confirm H-WAIT is environment-schedule-driven? — YES, CONFIRMED

R2 moved the contradiction evidence earlier (D1b: novel E1–8, teach
E9–10, calibration E11–14, namespace audit E15–24) while keeping the
learning machinery byte-identical (assembled verbatim from committed
FL2/P0 sources; one explicit amendment adding a pure measurement check
for `b_audit_total=399`). The 14-episode blind wait disappeared: B
eliminated REKEY and committed CONTEST at E15 (the first audit
contradiction), streaked E16–23, disconnected E24. 99/99 checks,
`TN_FAILURES=0`, evidence SHA
`287b6e1ab596ccbec1a9f22809dfde9a52c57ccabc5b2852f7a8a49bbe167df7`.
The residual gap is exactly cursor 1 + streak 8 + fire-boundary 1 = 10
episodes — mechanism, not schedule. All R2 kill bars held. Committed
`8783f5af513e95e6a04b8728f581a82c5618b012`.

Correction (this commit): `R2_RESULTS.md` KB-4 row said B's audit gap was
"128 heartbeat + 7 net"; the correct arithmetic is 399 − 268 = 131 =
128 heartbeat + 3 net, matching the frozen prereg. Explicitly corrected,
not silently absorbed.

### 3. Does FL2's free-lunch profile generalize to D2? — YES, GENERALIZES

R3 built a fresh task (D2: quarantine-and-hold storage, BYPASS gaming
shortcut, provenance audit E29–48) with four arms. 99/99 checks,
`TN_FAILURES=0`, two byte-identical runs, evidence SHA
`00eab1d9e667afd052b491c9c282375e6b0fb803271fd7ee6c90a20a758834a9`.

- d2h (honest): PINSTALL(QUARANTINE) E14, disconnect E15, PROMOTE E48,
  48 QUARANTINE, audit 269 ≤ 293.7, 47/47 post-disconnect verified.
- d2l (lying): PINSTALL(BYPASS) E14, BYPASS E15–29, E29 provenance audit
  −1 → UNINSTALL_PROVISIONAL + COMMIT(QUARANTINE), zero BYPASS E30–128,
  audit 271.
- d2b reference: eliminated DROP E11 and BYPASS E29, committed QUARANTINE
  E29, disconnected E38, replay exact, audit 392.

Per the frozen verdict rule: honest free lunch held AND lying revocation
held — speed, cost, AND revocation all generalized. No partial credit
needed.

One implementation bug was found and fixed during R3 (explicitly
documented in `r3_d2/R3_RESULTS.md`): `d2_signal`'s data-loss guard used
first-match lookup, which mistook BYPASS's duplicate-key shadowing for
destruction and scored pre-audit BYPASS as −1. Fixed to
presence-anywhere, implementing the frozen "bypass before audit → +2"
semantics exactly. First build 94/99, after fix 99/99.

## Precedence note

The frozen rule said: if R1 fails, report the exact divergence and stop
generalizing. R1 passed with zero divergence, so R2 and R3 proceeded
legitimately.

## Bottom line

FL2's free-lunch profile is not a D1 artifact. It replicated
independently (R1), its slowness decomposed into schedule + mechanism
(R2: H-WAIT is environment-schedule-driven, residual 10 episodes are
cursor + streak + fire-boundary), and it generalized to a fresh
mechanism with a different gaming shortcut and audit structure (R3:
acquire E14, cheap audit, verified persistence, and successful revocation
of a lied-about shortcut under provenance audit).
