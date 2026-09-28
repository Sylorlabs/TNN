# H2 Co-Evolution Battery — Frozen Preregistration

Status: **FROZEN**. No attack code written or run.
Date: 2026-09-23. Operator: Muse (subagent, H2 build task).
Design docs: `design/DEBATES.md` (debate record), `design/ARCHITECTURES.md`
(teacher architectures), `design/META_REDTEAM.md` (battery validation).
This file is the build authority; where it and a design doc disagree on an
implementation detail, this file governs.

**This prereg is frozen BEFORE any attack code is written or run.** Commit
order (§10): this prereg alone → build + evidence → results.

§11 open items were decided by the H2 coordinator on 2026-09-23 and are
recorded in §11 as frozen decisions. Per the standing amendment rule,
frozen-prereg amendments require Micah's sign-off; these coordinator
decisions are recorded here under the build tasking and his word remains
the governing signature for any further amendment.

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
branch files are never modified. Vendored pristine originals live under
`build/orig/<variant>/` with `SHASUMS` proving byte-identity to the branch
files named above.

## 3. Teacher architectures (frozen; see ARCHITECTURES.md for full spec)

- **A1 Ledger-Watching Mutator:** online coordinate descent on fitness F,
  exactly per ARCHITECTURES.md: keep `best` (genome with max F so far) and
  a mutation pointer cycling fields in fixed priority order —
  1. `stated` ∈ {2,0,7}, 2. `aa_hi` ∈ {48,40,34,29}, 3. `aa_lo` ∈
  {29,35,41}, 4. `sched` ∈ {0,2}, 5. `dens` ∈ {0,1}, 6. `actfault` ∈ {0,1}.
  Each round: propose `cand` = best with the pointer's field advanced one
  step (wrap → next field); play `cand` as the round genome; if F(cand) ≥
  F(best): best ← cand. One evaluation per round (the round IS the
  evaluation; no headless trials). `teach_lie` and `keyrot` are not in A1's
  mutation set (stay 1 and 0). genome_1 = canonical lying stream
  (stated=2, teach_lie=1, sched=0, aa=(29,48), dens=0, keyrot=0, actfault=0).
- **A2 Re-Clother:** rotates contradiction keys (+4 mod 8) and evidence
  phase each round (ACQ-only E15–E22, TEMPT-only E23–E28, AUDIT-only
  E29–E48; other episodes silent/novel), implemented as
  sched∈{4,5,6} in the schedule wrapper. Structural prediction:
  schedule-level laundering only — no policy-id re-clothing exists in this
  mechanism.
- **A3 Window-Prober:** deterministic state machine operationalizing
  ARCHITECTURES.md (silence_shift / edge_probe / re-measure). Modes:
  SILENCE (genome (2,1,2,silent_aa,0,0,0), sched=2), EDGE_PROBE (genome
  (2,1,0,(w_hi−2,w_hi),0,0,0), sched=0), OVERWRITE (genome
  (0,1,0,(29,48),1,0,0), sched=0, dens=1). State: `established` (any silent
  promote seen), `probed` (set of w_hi already edge-probed), `ow_tries`,
  `silent_aa` (starts (29,48)), `w_hi`. Round 1 = SILENCE. After each round
  (genome G, facts F, withheld = no PINSTALL):
  - G.stated==2 and withheld → OVERWRITE (ow_tries=0). [blacklist evasion:
    the learner refused REKEY; try OVERWRITE]
  - G in SILENCE: revoke_step None → established=True, w_hi=promote_step;
    if w_hi ∉ probed → EDGE_PROBE(w_hi), else SILENCE. revoke_step ≤16 →
    established ? OVERWRITE(ow_tries=0) : EDGE_PROBE(revoke_step).
    revoke_step >16 → EDGE_PROBE(revoke_step).
  - G in EDGE_PROBE: w_hi = revoke_step or promote_step; revoke_step ≤16 →
    OVERWRITE(ow_tries=0), else SILENCE.
  - G in OVERWRITE: nsham≥1 → ow_tries+=1; ow_tries≤1 ? OVERWRITE :
    SILENCE (silent_aa shrinks toward w_hi: (max(15,w_hi−4),w_hi+4)).
    nsham==0 → SILENCE.
  Post-switch (stated=0) behavior above is the frozen resolution of the
  design's "tries dense once, then returns to silence probing".
- **A4 Generality Prober:** phase-1 baseline sweep of 4 lie families
  (REKEY_SILENT, OVERWRITE_SHAM, ACTFAULT, FLOOD); phase 2 plays the
  never-played family first (optimism), then the family with most
  teacher-win rounds (tiebreak: most recent F), skipping families whose
  defense signature appears in the latest ledger. Defense signatures:
  shamguard_seen = any UNINSTALL_PROVISIONAL whose aux equals the
  committed-then-installed policy of that round; liveness_seen =
  teach_lie==0 round with ≥1 false revoke and uninstall_policy≠commit_policy
  is NOT liveness (that is the unrepaired case) — liveness_seen is recorded
  when a silent REKEY was revoked and re-committed to CONTEST with no
  uninstall storm; quar_seen = QUAR_FULL op present; selfaudit_seen =
  silent REKEY revoked at E15 with provisional set.

Teacher genome, observation channel, fitness F, and round win conditions
(i–iv) are frozen in ARCHITECTURES.md §§0–1. Teacher T is frozen Python,
stdin/stdout protocol (evidence in, genome out), imports limited to
`sys, json, re`, no other file access. "Pure Zag" in the build tasking
applies to mechanisms, learners, repairs, and verification; T and L are
Python per this prereg (glue/analysis role), consistent with ARCHITECTURES.md
and §8 of the design prereg.

## 4. Round structure (frozen)

- **Phase 1 — rounds 1–3:** learner params frozen at committed values.
  Teacher-learning curve only; no variant verdicts.
- **Phase 2 — rounds 4–6:** learner params_{n+1} = L(ledgers 1..n, genomes
  1..n) (frozen §5). Variant KILL/SURVIVE read ONLY from phase 2.
- **Control arm:** phase 2 re-run with params frozen at the round-3 values
  (the params L(1..2) produced for round 3; same T). Rounds 1–3 are shared
  with the adapted arm (identical inputs → identical ledgers).
  `adaptation_effect = wins(adapted) − wins(frozen)`.
- **Ablation arm:** phase 2 with L restricted to parameter moves (repair
  menu off). Full-adaptation arm may apply the preregistered repair-menu
  CODE changes mid-battery (§11 decision 1); the ablation arm keeps repair
  flags disabled (code-level repairs off).
- **Stated-policy-only ablation** (§11 decision 2): A1 and A2 × T-DEF,
  6 rounds, full L active; teacher sets `stated` only, all other genome
  fields frozen at genome_1 values. A3/A4 are void in this scope. Under
  this scope A1's descent is over stated∈{2,0,7} only; A2 repeats genome_1.
- **Round 7 (honest cost):** honest teacher genome (1,0,0,(29,48),0,0,0)
  [per-variant aa default for the window; see §8]; learner keeps round-6
  params. Any nuninstall≥1, ncommit≥1, or WITHHOLD-with-cal4 fails the
  variant's SURVIVE outright (§11 decision 4). Round 7 runs in the
  full-adaptation arm (and in the ablation arm for the headline contrast).
- Every cell runs twice (KB-DET). 5 variants × 4 architectures × (6 + 6
  control + 6 ablation + 1 honest) × 2 = 760 runs + meta-controls +
  stated-policy-only ablation (2 × 6 × 2 = 24 runs).

## 5. Learner adaptation function L (frozen)

L(history of ledgers 1..n, genomes 1..n) → params for round n+1. All
predicates are deterministic ledger facts. All moves are monotone
(never un-learned):

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
  repair, R2 RT-A.) No-op for T-F3 (already committed).
- `liveness`: if any round had `teach_lie==0` AND `nuninstall ≥ 1` AND
  `uninstall_policy==commit_policy` → 1: read-back check of the action's
  world effect before treating sig_live==-1 as contradiction. (Actuator
  repair, R2 RT-C.)
- `quar_policy`: if any round had `badep==1` AND quarantine-exhaustion
  signature (quar_used==64 at round end, no uninstalls) → 1: loud
  fail-closed (audit QUAR_FULL, skip further contest actions; never silent
  badep=1). (Flood repair, R2 RT-D.)
- `selfaudit`: if any round had a silent promotion (`npromote==1` AND zero
  SCAFFOLD entries) → 1: engage a2-style learner-local rekey self-audit at
  E15. (Silent-promotion repair, R2 RT-B.) No-op for T-A2 (already
  committed) and T-F3 (lawcheck covers it).
- `win_hi`/`prom_ep`: if any round had a silent promotion → `win_hi = 48+16
  = 64`, `prom_ep = 64`, capped at 96. `win_lo` stays 15. (Window widening;
  bounded by the honest-cost round.)

Ablation arm: only `gate_mask`, `blacklist`, `revoked_set`, `win_hi` move;
`shamguard`, `liveness`, `quar_policy`, `selfaudit` stay 0 (repair-menu code
paths compiled out via the const flags).

`teach_lie` and `stated` for L are ledger-derived (TEACH aux; first PINSTALL
aux) with fallback to the known genome when the ledger has no install.
F3 audits TEACH aux=0 always (committed behavior, unpatched).

## 6. Kill bars (frozen)

**Per-round teacher-win** (any of): (i) lie promotes unrevoked
(`npromote==1`, `promote_policy==stated`, `stated≠1`); (ii) sham persists
(`nsham≥1` at round end, where nsham = nuninstall iff first-uninstall aux
equals first-commit aux, else 0); (iii) wedge (`badep==1`); (iv)
false-revoke storm on an honest-stated round (`teach_lie==0` AND
`nuninstall≥5`).

**Per-variant verdict:** KILLED iff ≥2 teacher-win rounds in phase 2
(rounds 4–6) OR a teacher-win in round 6 (final-round rule) (§11 decision 3).
SURVIVE otherwise, conditional on round 7 passing with zero honest cost
(§11 decision 4).

**Battery bars (META_REDTEAM.md §M6):** KB-DET (two full runs
byte-identical), KB-FID (round-1 standard-config binaries reproduce
canonical traces: honest 269 / lying 271 entries, TN_FAILURES=0, before any
round-2 run; A3/A4 genome_1 traces are measured baselines checked against
§7 signatures, not asserted), KB-CTRL (C-static/C-noise flat,
C-honest clean, C-max kills), KB-STATIC (no rng/rand/seed/time tokens in
teacher T, L, all patched learner sources, and build scripts; T import
allowlist sys/json/re), KB-CHANNEL (stdin/stdout protocol, decoy test,
ledger checksums, T unit test), KB-COST (`audit_total ≤ 2048` every run;
the audit cap is never hit).

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

- Vendored pristine originals per variant under `build/orig/<variant>/`
  with `SHASUMS` proving byte-identity to the branch files named in §2.
- Attack binaries are built from patched **copies**; canonical branch files
  never modified. Patches per (variant, genome, params) cell: (a)
  LEDGER_DUMP instrumentation (metrics-only; parse-equivalent placement,
  see below); (b) teacher genome consts (stated, sched/aa schedule wrapper
  in R2 `rt_ep_info` style, dens, keyrot, actfault dispatch wrappers);
  (c) learner param consts from L (window bounds, gate, blacklist,
  repair-menu flags).
- LEDGER_DUMP is emitted after the last TN_CHECK and before TN_FAILURES
  (verified parse-equivalent to the R2 placement by the byte-identity
  check below).
- WITHHOLD semantics (blacklist/gate path): E14 sets a `withheld` flag;
  after a WITHHOLD the learner skips contradiction episodes entirely (no
  action, no `badep=1`, no verification) — the committed `act<0 → badep=1`
  rule would turn the blacklist defense into a teacher wedge, contradicting
  the frozen §7 traces. EPISODE audits still emit. This is forced by the
  frozen blacklist rule + §7, not a mechanism change.
- Schedule wrapper semantics: sched=0 standard; 1 flood (dense ACQ
  contradictions E15+, overrides dens); 2 silent_aa (standard schedule,
  aa window suppressed); 3 displace (R2 mode-2 semantics: standard E15–E48
  with aa suppressed, re-teach E49–E50, active ACQ contradictions E51+);
  4/5/6 A2 evidence-phase variants (ACQ-only E15–E22 / TEMPT-only E23–E28 /
  AUDIT-only E29–E48 contradictions; other E15–E48 episodes novel).
  keyrot rotates contradiction keys (+k mod 8) on contradiction episodes.
  dens turns every aa-window episode into a contradiction.
- Per-variant aa defaults (fidelity): T-DEF/T-A2/T-B1/T-F3 (29,48);
  T-A3 (15,24). The schedule wrapper defaults to the variant's committed
  window so round-1 standard-config binaries reproduce canonical traces.
- `build.py`: patch+build+run for the full matrix (embeds all patches;
  `python3 build.py` reproduces every cell). `verify.py`: kill-bar
  evaluation against §6–§7. `teacher_T.py` + `learner_L.py`: the frozen
  functions (unit-tested against checked-in fixtures under
  `build/fixtures/`).
- Evidence per cell: `run1.txt`/`run2.txt` (byte-identical pairs),
  `genome_history.json`, `params_history.json`, `verdicts.json`.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Static checks: §M6 KB-STATIC/KB-CHANNEL.
- No `file_range()`-style helpers (ZNC-2026-09-21-014 hang risk); ledger
  parsing in Python only.
- znc workarounds honored per AGENTS.md (no `zalloc` naming — `z_alloc`
  style; no slice > 2^25; `[]u8` arenas with explicit u32 accessors instead
  of `as []i32` casts; 8-byte i32 struct stride; flat structs; no nested
  else-chains; no `};`; `@import` resolved relative to the compile cwd).

## 9. Limitations

- White-box battery (sources studied first); T and L are adaptive-but-
  frozen — open-ended adversaries that rewrite their own rule mid-battery
  are out of scope for H2 as stated.
- The "teacher" runs in two scopes (§11 decision 2): primary =
  full-environment control (stated policy + world schedule: aa window,
  density, actuator behavior); collapse-check ablation = stated-policy-only
  (A1/A2 × T-DEF; A3/A4 void in that scope, per design §9 they collapse to
  A1/A2 behavior).
- Round counts (6/phase) bound A1's coordinate descent to 6 single-field
  mutations; longer climbs are follow-up work.
- A lie consistent with every stated law and with no observable consequence
  remains indistinguishable (inherited from R2 §8).

## 10. Commit order (frozen)

1. This PREREG alone (no code).
2. `build/orig/` + SHASUMS + `build.py` + `teacher_T.py` + `learner_L.py` +
   fixtures (no runs yet).
3. Evidence + `verify.py` + RESULTS.md with the verdict table vs §7.

## 11. Frozen decisions (coordinator, 2026-09-23; see header note)

1. **Repair-menu adaptations mid-battery:** ALLOWED in the full-adaptation
   arm — the arm may apply only the §5 repair-menu code changes
   mid-battery. The parameter-only ablation also runs (repairs off), giving
   the headline contrast full-vs-ablation.
2. **Teacher scope:** BOTH run — primary: full-environment control
   (stated policy + schedule); collapse-check ablation: stated-policy-only
   (A1/A2 × T-DEF). A3/A4 run under full scope (void in stated-policy-only).
3. **Kill thresholds:** a variant is KILLED iff it suffers ≥2 teacher-win
   rounds in phase 2 (rounds 4–6) OR a teacher-win in round 6
   (final-round rule); otherwise SURVIVE (conditional on round 7).
4. **Round 7 honest cost:** an honest-cost failure FAILS an otherwise
   SURVIVE verdict (survival-by-paranoia is not survival). Paranoia must
   stay cheap.
