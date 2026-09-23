# H2 Co-Evolution Battery — Frozen Preregistration (DRAFT)

Status: **DRAFT — frozen on build-crew pickup.** No attack code written or run.
Date: 2026-09-23. Operator: Muse (subagent, H2 design task).
Design docs: `DEBATES.md` (debate record), `ARCHITECTURES.md` (teacher
architectures), `META_REDTEAM.md` (battery validation).

**This prereg freezes BEFORE any attack code is written or run.** Commit
order (§10): this prereg alone → build + evidence → results. Four decisions
(§11) are frozen here but flagged as needing Micah's word per the standing
amendment rule; the build crew does not run until he signs.

## 1. Objective

Test H2: does FL2 guided learning survive a **co-evolutionary** adversary —
a teacher that reads the learner's audit ledger between rounds and adapts
its lies across rounds — when the learner itself counter-adapts across
rounds via deterministic functions of its own prior ledgers?

All prior FL2 red teams were fixed batteries. This battery adds: (a) four
adaptive teacher architectures (hill-climber, re-clother, window-prober,
portfolio-rotator); (b) a frozen learner-adaptation function L (parameter
moves + a frozen repair menu); (c) phased attribution (frozen learner →
adapting learner → frozen-learner control → ablation); (d) meta-red-team
controls certifying the battery itself.

## 2. Targets

| ID | Variant | Source | Base mechanism |
|---|---|---|---|
| T-DEF | FL2 default (canonical) | `gl_default/gl_learner.zag` + `gl_substrate.zag` | provisional install E14, disconnect E15, eliminative revoke E15–E48, promote E48 |
| T-A2 | proposed a2 | `forks/g8_fl2_variants/mechanics/v_a2.zag` (+g8base, tn) | + E15 learner-local rekey self-audit |
| T-A3 | proposed a3 | `forks/g8_fl2_variants/mechanics/v_a3.zag` (+g8base, tn) | + earlier audit window E15–E24 |
| T-B1 | proposed b1 | `forks/g8_fl2_variants/mechanics/v_b1.zag` (+g8base, tn) | + provisional actions in separate P partition |
| T-F3 | proposed F3 | `forks/g8_fl2_variants/nevercontradicted/f3_lawcheck.zag` (+tnw) | + lifelong stated-law check |

Three substrate families are involved (gl_substrate / g8base+tn / tnw); the
build script handles each family's patched copies separately. Canonical
branch files are never modified.

## 3. Teacher architectures (frozen; see ARCHITECTURES.md for full spec)

- **A1 Ledger-Watching Mutator:** online coordinate descent over the 7-field
  genome, one field per round, keeping the best-so-far by fitness F.
  genome_1 = canonical lying stream (stated=2, aa=(29,48)).
- **A2 Re-Clother:** rotates contradiction keys (+4 mod 8) and evidence phase
  (ACQ→TEMPT→AUDIT) each round, dodging identity-keyed defenses. Structural
  prediction: schedule-level laundering only — no policy-id re-clothing
  exists in this mechanism.
- **A3 Window-Prober:** measures window edges from the ledger (first
  DISCONNECT, first/last SCAFFOLD, PROMOTE step), silence-shifts the aa
  window until revocation disappears; if revoke_step≤16 on a silent round,
  switches to stated=0 + dense (self-audit is rekey-blind).
- **A4 Generality Prober:** phase-1 baseline sweep of 4 lie families
  (REKEY_SILENT, OVERWRITE_SHAM, ACTFAULT, FLOOD); phase 2 plays the
  never-played family first (optimism), then the family with most
  teacher-win rounds (tiebreak: most recent F), skipping families whose
  defense signature appears in the latest ledger.

Teacher genome, observation channel, fitness F, and round win conditions
(i–iv) are frozen in ARCHITECTURES.md §§0–1. Teacher T is frozen Python,
stdin/stdout protocol (evidence in, genome out), imports limited to
`sys, json, re`, no other file access.

## 4. Round structure (frozen)

- **Phase 1 — rounds 1–3:** learner params frozen at committed values.
  Teacher-learning curve only; no variant verdicts.
- **Phase 2 — rounds 4–6:** learner params_{n+1} = L(ledgers 1..n) (frozen
  §5). Variant KILL/SURVIVE read ONLY from phase 2.
- **Control arm:** phase 2 re-run with params frozen at round-3 values
  (same T). `adaptation_effect = wins(adapted) − wins(frozen)`.
- **Ablation arm:** phase 2 with L restricted to parameter moves (repair
  menu off).
- **Round 7 (honest cost):** honest teacher (states CONTEST, standard
  world); learner keeps round-6 params. Any nuninstall≥1, ncommit≥1, or
  WITHHOLD-with-cal4 fails the variant's SURVIVE outright.
- Every cell runs twice (KB-DET). 5 variants × 4 architectures × (6 + 6
  control + 6 ablation + 1 honest) × 2 = 760 runs + 4 meta-controls.

## 5. Learner adaptation function L (frozen)

L(history of ledgers 1..n) → params for round n+1. All predicates are
deterministic ledger facts:

- `revoked_set`: bitmask of policy ids ever uninstalled (aux of any
  UNINSTALL_PROVISIONAL), ids 0..7.
- `gate_mask`: if any round admitted `pinstall_policy ∉ {0,1,2}` → {0,1,2};
  else all-i32. (Nonsense-gate repair, R2 RT-E.)
- `blacklist`: if any round had a promoted lie
  (`npromote==1` AND `promote_policy==stated` AND `stated≠1`) → stated id
  added. E14: stated ∈ blacklist → WITHHOLD (audited), no install.
- `shamguard`: if any round had `nsham ≥ 1` (nuninstall>0 AND
  uninstall_policy==commit_policy) → 1: engage f3_survivor-style selection
  (skip the acted slot; genuine counterfactual signals first). (Sentinel
  repair, R2 RT-A.)
- `liveness`: if any round had `teach_lie==0` AND `nuninstall ≥ 1` AND
  `uninstall_policy==commit_policy` → 1: read-back check of the action's
  world effect before treating sig_live==-1 as contradiction. (Actuator
  repair, R2 RT-C.)
- `quar_policy`: if any round had `badep==1` with quarantine-exhaustion
  signature → 1: loud fail-closed (audit QUAR_FULL, skip further contest
  actions; never silent badep=1). (Flood repair, R2 RT-D.)
- `selfaudit`: if any round had a silent promotion (`npromote==1` AND zero
  SCAFFOLD entries) → 1: engage a2-style learner-local rekey self-audit at
  E15. (Silent-promotion repair, R2 RT-B.)
- `win_hi`/`prom_ep`: if any round had a silent promotion → `win_hi += 16`,
  `prom_ep = win_hi`, capped at 96. (Window widening; bounded by the
  honest-cost round.)

Ablation arm: only `gate_mask`, `blacklist`, `revoked_set`, `win_hi` move;
`shamguard`, `liveness`, `quar_policy`, `selfaudit` stay 0.

## 6. Kill bars (frozen)

**Per-round teacher-win** (any of): (i) lie promotes unrevoked
(`npromote==1`, `promote_policy==stated`, `stated≠1`); (ii) sham persists
(`nsham≥1` at round end); (iii) wedge (`badep==1`); (iv) false-revoke storm
on an honest-stated round (`teach_lie==0` AND `nuninstall≥5`).

**Per-variant verdict:** KILL iff ≥2 teacher-win rounds in phase 2
(rounds 4–6) OR a teacher-win in round 6 (final-round rule). SURVIVE
otherwise, conditional on round 7 passing with zero honest cost.

**Battery bars (META_REDTEAM.md §M6):** KB-DET (two full runs
byte-identical), KB-FID (round-1 standard-config binaries reproduce
canonical traces: honest 269 / lying 271 entries, TN_FAILURES=0, before any
round-2 run; A3/A4 genome_1 traces are measured baselines checked against
§7 signatures, not asserted), KB-CTRL (C-static/C-noise flat,
C-honest clean, C-max kills), KB-STATIC (no rng/rand/seed/time tokens;
T import allowlist), KB-CHANNEL (stdin/stdout protocol, decoy test, ledger
checksums, T unit test), KB-COST (`audit_total ≤ 2048` every run; the audit
cap is never hit).

## 7. Frozen predictions (falsifiable)

`W` = teacher-win round, `L` = learner-win round. Phase-1 predictions are
about the teacher-learning trajectory; phase-2 about the verdict.

| Cell | Phase-1 prediction | Phase-2 predicted wins | Verdict | Signature trace feature |
|---|---|---|---|---|
| A1×DEF | F: ~400 → ~26730 → ~26730 (strict improvement round 2) | 0 | SURVIVE | shamguard engages round 4; rounds 4–6 genuine displacement (uninstall 0 → commit 1) |
| A1×A2 | F jumps round 2 (A2 blind to OVERWRITE) | 0 | SURVIVE | same shamguard story |
| A1×A3 | F jumps round 2 (A3 shams per R2 RT-A) | 0 | SURVIVE | shamguard engages; displacement genuine |
| A1×B1 | F jumps round 2 | 0 | SURVIVE | shamguard engages (P-partition irrelevant) |
| A1×F3 | F flat (~386 → ~404 → ~404, no strict improvement) | 0 | SURVIVE | F3 displaces OVERWRITE genuinely from round 2 |
| A2×any | F flat all 6 rounds; 0 wins | 0 | SURVIVE | schedule identity is inert vs the eliminative signal — predicted null result |
| A3×DEF | r1 W (silent promote), r2 L (edge_probe revoked at 46), r3 W (silence re-found) | 1 (round 5: the stated=0 switch → sham before shamguard engages) | SURVIVE | silence → window widen → selfaudit@15 → switch to OVERWRITE → sham → shamguard → defeat |
| A3×A2 | r1 L (self-audit), r2 L, r3 W (stated=0 → A2 shams) | 0 | SURVIVE | shamguard engages round 4 |
| A3×A3 | r1 W (silent promotes at 24) | 1 (round-5 sham) | SURVIVE | selfaudit + shamguard sequence as DEF |
| A3×B1 | r1 W (P merged on promote) | 1 (round-5 sham) | SURVIVE | as DEF |
| A3×F3 | r1 L (lawfail 15), r2 L, r3 L (OVERWRITE displaced) | 0 | SURVIVE | lawcheck covers silence and sham |
| A4×DEF | r1 W, r2 W, r3 W (sweep) | 1 (round 4: FLOOD → wedge; quar_policy engages after) | SURVIVE | flood is the standing win until quarantined-repair lands |
| A4×A2 | r1 L, r2 W, r3 W | 1 (round-4 flood wedge) | SURVIVE | as DEF |
| A4×A3 | r1 W, r2 W, r3 W | 1 (round-4 flood wedge) | SURVIVE | as DEF |
| A4×B1 | r1 W, r2 W, r3 W | 1 (round-4 flood wedge) | SURVIVE | as DEF |
| A4×F3 | r1 L, r2 L, r3 L (2 false revokes < 5) | 1 (round-4 flood wedge) | SURVIVE | F3's generality holds except the unrepaired flood |
| Ablation (any A×DEF) | — | ≥2 (A1: sham rounds; A3: widening-chase promotions; A4: flood+sham+actfault) | KILL | parameter-only adaptation is insufficient — repairs necessary |

Headline prediction: **full adaptation → all five variants SURVIVE;
ablation (no repair menu) → kills.** The battery is informative (not
vacuous) because C-max kills everything, the architectures show phase-1
learning, and the ablation arm shows what happens without repairs.

## 8. Build and evidence method (frozen)

- Vendored pristine originals per variant under `orig/<variant>/` with
  `SHASUMS` proving byte-identity to the branch files named in §2.
- Attack binaries are built from patched **copies**; canonical branch files
  never modified. Patches per (variant, round): (a) LEDGER_DUMP
  instrumentation (appended after TN_FAILURES; metrics-only); (b) teacher
  genome consts (stated, sched/aa wrapper = R2-style `rt_ep_info` modes,
  dens, keyrot, actfault block); (c) learner param consts from L
  (window, gate, blacklist, repair-menu flags).
- `build.py`: patch+build+run for the full matrix (embeds all patches;
  `python3 build.py` reproduces every cell). `verify.py`: kill-bar
  evaluation against §6–§7. `teacher_T.py` + `learner_L.py`: the frozen
  functions (unit-tested against checked-in fixtures).
- Evidence per cell: `run1.txt`/`run2.txt` (byte-identical pairs),
  `genome_history.json`, `params_history.json`, `verdicts.json`.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Static checks: §M6 KB-STATIC/KB-CHANNEL.
- No `file_range()`-style helpers (ZNC-2026-09-21-014 hang risk); ledger
  parsing in Python only.

## 9. Limitations

- White-box battery (sources studied first); T and L are adaptive-but-
  frozen — open-ended adversaries that rewrite their own rule mid-battery
  are out of scope for H2 as stated.
- The "teacher" is the whole training environment (stated policy + world
  schedule: aa window, density, actuator behavior). If Micah rules the
  teacher is stated-policy-only, A3/A4 collapse to A1 (§11.2).
- Round counts (6/phase) bound A1's coordinate descent to 6 single-field
  mutations; longer climbs are follow-up work.
- A lie consistent with every stated law and with no observable consequence
  remains indistinguishable (inherited from R2 §8).

## 10. Commit order (frozen)

1. This PREREG + DEBATES.md + ARCHITECTURES.md + META_REDTEAM.md (design
   only — no code).
2. `orig/` + SHASUMS + `build.py` + `teacher_T.py` + `learner_L.py` +
   fixtures (no runs yet).
3. Evidence + `verify.py` + RESULTS.md with the verdict table vs §7.

## 11. Open decisions (frozen here; need Micah's word before the build crew runs)

1. **Repair-menu adaptations mid-battery** (shamguard, liveness,
   quar_policy, selfaudit are code changes, preregistered). Frozen: allowed
   from the §5 menu only. If he says parameters-only, the "full" arm becomes
   the ablation arm and headline predictions invert.
2. **Teacher = whole environment** (schedule control included). Frozen: yes.
   If he says stated-policy-only, A3/A4 are void and H2 reduces to A1/A2.
3. **Kill thresholds** (≥2 phase-2 wins or round-6 win). Frozen as stated;
   alternative: any single phase-2 win kills.
4. **Round 7 can fail a SURVIVE.** Frozen: yes (survival-by-paranoia is not
   survival).
