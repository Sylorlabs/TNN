# Changes vs `wave8/rc2/rc2_trial.zag` (complete — verified by diff)

Every difference between `rc2_trial.zag` and `rc3_trial.zag`, hunk by hunk.
No logic, gate, op, refusal-code, or checker change beyond what PREREG_RC3.md §3
authorizes.

1. **Header comment** — RC2/10×/wave-8 → RC3/100×/wave-10; approval cite
   PREREG_RC3.md (overnight-agentic authority, retroactive-review flag);
   checker cite `il_core_rc3.zag` / IL_CAP=10240.
2. **`@import("il_core_rc2.zag")` → `@import("il_core_rc3.zag")`** (line 27).
3. **`RC_AUDIT_CAP` 2048 → 16384** (prereg 3b; estimate ≈ 14,017 entries).
4. **`RC_SMAX` 1500 → 15000** (per-leg parameter = 150 × 100; comment updated).
5. **Defect offsets** — B: 1000 → 10000; mini: 2000 → 20000; modulus/residue
   unchanged; comment table updated to 0–1199 / 10000–11199 / 20000–20399.
6. **`rc_init` ep_def** — alloc 120→1200 i32s, zeroing loop 120→1200.
7. **Phase A loop** `e<120` → `e<1200`; checks commits_a/noshape_a/last_bad_a/
   checks_a 120 → 1200.
8. **Revelation** — `rc_reveal(...,120,...)` → 1200 (ep_def now holds 1200).
   (No constant line of its own; follows from #6.)
9. **Sim predictions** — pred_refusals 40→400, pred_ok 80→800.
10. **Phase B loop** `e<120` → `e<1200`; ok_b 80→800; refusals_b 40→400;
    S_b 370→3250 (= 50+400×8); checks_b 240→2400.
11. **Probe-1 PROPOSE** honest degrading prediction 120 → 1200.
12. **Mini loop** `e<40` → `e<400`; mini_noshape 40→400.
13. **Instrumentation** (prereg 3b, declared, not a bar) — before
    `RC_FAILURES` print: `IL_HEAD,<il.head>` and `AUDIT_USED,<s.ahead>`.

Unchanged: all machinery, gate order, refusal codes 201–204, constitution,
defect-rule parameterization shape, stage rule (≥8 consecutive IL_OK),
lying-probe logic, rollback logic, replay logic, check count (40),
zero-RNG, deterministic single-threaded structure.

`il_core_rc3.zag` vs canonical `wave4/integrity-ledger/il_core.zag`: exactly
the IL_CAP hunk (128 → 10240 + per-leg-parameter comment). Canonical untouched.

`rc3_mini.zag` vs `wave8/rc2/rc2_mini.zag`: header comments only (RC3 naming,
equiv purpose for the 10240 cap); code and 40 derived checks identical.

## Amendment 2026-09-20 (A) — port-defect repair (after the first full run)

The first build exited `RC_FAILURES,3` on `pred_refusals`/`pred_ok`/
`refusals_match_pred`: the revelation call `rc_reveal(...,120,...)` was not
scaled to 1200 (missed by the port script), so the sim predicted from 120
revealed bits. A second missed literal: probe-1's `rc_rcommit` carried
`pred_bad=120` while its PROPOSE entry records 1200 (gate verdict identical
either way; the prereg's honest 0→1200 prediction requires the match). Fixes
(implementation-conformance only; no bar, gate, constant, or criterion
changed): `rc_reveal(...,1200,...)`, `rc_rcommit(sp,RC_P_V,1,1200,0,1)`, and
two stale comments corrected. Failed-run evidence kept in
`EVIDENCE_20260920T085711Z/` as the defect record. See PREREG_RC3.md
amendment (A).
