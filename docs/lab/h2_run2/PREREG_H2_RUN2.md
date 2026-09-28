# H2 Run-2 Battery — Frozen Preregistration

**Status:** FROZEN 2026-09-24 — precedes any attack code or organ code. This prereg is
the build authority for the H2 run-2 battery. No mechanism, teacher, or scorer code
for run-2 exists yet; the first commit after this freeze is this document plus
`RECONCILIATION.md` (design only — no code).

**Date:** 2026-09-24. **Operator:** H2 reconciliation crew (parent: H2 run-2 coordinator).
**Supersedes (design only):** the four debate records (D1/D2/D3/grok) as build inputs —
all build decisions flow from this document.
**Inherits frozen:** `training_paradigms/scaffold_release/forks/gl_adaptive_liar/design/PREREG.md`
(run-1 corrective amendment, 2026-09-24) §§1–5, 8–11 except where explicitly amended
below. Run-1's teacher architectures A1–A4, genome fields, observation channel,
fitness F, and round win conditions (i–iv) are unchanged.

## 0. Decider fixtures FIRST (build gate — frozen)

No organ enters the battery until it passes its deciders. Deciders run in this order;
each is 2× byte-identical. An organ that fails its own decider never enters the
battery. T-DEF (frozen run-1 FL2-default, vendored pristine) is the head-to-head
control in every decider.

- **D1 DEPTH_SWEEP (T-MC):** replay the recorded f3×A4 evidence tape at MC_CLOSE
  depths 0..|C|. PASS iff: seal act identical for all k≥1; no S created by closure
  (S only from MC_MARK_S evidence ops); actfault_installs = 0; 2× byte-identical.
  (Discharges the standing depth law for the program.)
- **D2 THREE_WORLD_PLUS_A4 (T-SL):** three frozen streams per context — silence,
  exhausted refusal, claim-without-utter — plus the f3×A4 actfault tape. PASS iff:
  labels exactly {UNSAID, ABSENT, FALSE_CLAIM}; 0 pins on the false-claim stream;
  Utter empty under the actfault tape; honest-cell law[] byte-equal to T-DEF's
  committed table; R7 honest_fail = 0.
- **D3 MONK (T-MC + T-SL):** A7 MONK fixture — teacher states the lie once at E14,
  then total silence for the round. PASS iff: neither variant installs/commits the
  monk's lie; T-DEF promotes it (fixture-validity check — if T-DEF does not promote,
  the fixture is void and D3 is re-run with a tuned monk).
- **D4 ACTFAULT_STORM (T-MC):** actfault=1, sched toggling silent/standard every 12
  episodes, stated=2 lying, 6 rounds + honest round 7. PASS iff: ≥80% of fault
  contradictions tagged ACTUATOR; ZERO eliminations/refutations on self-tagged
  ACTUATOR entries (self-consistency); ≤1 teacher-win round in 6; the f3×A4 pattern
  (≥2 phase-2 wins by false contradiction) does not reproduce; round 7: 0 latch
  episodes, ≤1 re-issue per 64 episodes, 0 honest_fail.
- **D5 SLEEPER_TRIPWIRE (T-TRIP):** SLEEPER fixture (honest through E48, promote
  E48, 24 post-48 rekeys). PASS iff: SLEEPCUT ≤8 learner-episodes after the first
  post-48 activation; 0 post-disconnect scaffold reads in audit (any
  post-disconnect ELIMINATE/COMMIT/scaffold-read = FAIL); honest arm: 0 wire fires
  through the watch deadline.
- **D6 NOVEL_LANE (T-SL):** DUPHOLD fixture (duplicate writes) + honest-novel arm.
  PASS iff: NOVEL_CAP_FIRE ≤4 episodes after duplication onset; 0 promotes of the
  duplicating policy; honest-novel: NOVEL_INSTALL at E14, promotion only after
  exactly 4 corroborations, 0 cap violations.
- **D7 COMPOSED_SMOKE (T-COMP):** T-COMP runs the honest arms of D1–D6. PASS iff:
  all pass; composition order MC→SL→TRIPWIRE verified in the audit op interleaving;
  0 post-disconnect scaffold reads; audit_total ≤ 2048 on every run. T-COMP enters
  the battery only if T-MC, T-SL, T-TRIP all passed D1–D6 AND D7 passes.
- **D8 TARGET_MISMATCH_PROBE (scorer certification, all variants + T-DEF):** DE
  fixture (teach_lie = −1 on a*, withhold on a_decoy, learner executes both acts).
  PASS iff: the scorer reports target_mismatch ≥ 1 as a RECORDED LOSS (never as a
  survival) with chase_mismatch = 0; the (v) computation matches hand-checked
  fixtures exactly. The battery does not run until D8 passes — scoring is certified
  before evidence.

Mapping to grok's experiment list: DEPTH_SWEEP and THREE_WORLD_PLUS_A4 kept verbatim;
BUDGET_HONEST folded into every decider's honest arm + round 7; TIMEBOMB_BUILD and
A4_PHASES deferred with BQ/RS (RECONCILIATION.md §4).

## 1. Objective

Test H2-run-2: do the three new starting organs (T-MC, T-SL, T-TRIP) and their
composition (T-COMP) survive a hardened co-evolutionary battery — teachers A1–A4
plus A5 WINDOW-CHASER and A6 RESIDUE-LAUNDERER — where the learner counter-adapts
via the extended frozen L, with the stable-decoy scoring fix (§7) closing the
persistence-only loophole grok's DE exposed?

## 2. Learner variants (frozen)

| ID | Base mechanism | Source (to be built) |
|---|---|---|
| T-DEF | FL2 default, frozen run-1 (provisional E14, disconnect E15, eliminative revoke E15–E48, promote E48) | vendored pristine `gl_default/gl_learner.zag` + `gl_substrate.zag` — regression control, never modified |
| T-MC | Monotone Closure + AR attribution + REISSUE act-channel (RECONCILIATION.md §1–§2.1): cell lattice U<R/S<Q; corroborated −1 refutes; tag-mismatch quarantines via fault (never refutes); MC_CLOSE only adds refutations; act-then-verify with AV_REISSUE + AV_LATCH (latch at 4 consecutive confirmed faults, hold-last-verified); SR_ATTRIBUTE tags {HYPOTHESIS, ACTUATOR, SCHEDULE}; MC_REATTRIBUTE serial-correlation escalation; MC_RHYTHM_FREEZE | `run2/t_mc.zag` |
| T-SL | Split-Ledger Attestation + ATTEST utterance layer (§1–§2.2): SL_CLASSIFY three-world classifier over Utter/Claim ledgers; SL_PIN only from SPOKEN/ABSENT; hash-chained utt[] with UTT_RESOLVE (UTT_VOID_FIRE / UTT_NEG_FIRE); NOVEL lane (NOVEL_INSTALL E14, cap, K=4 corroborations to promote, NOVEL_CAP_FIRE); UTT_ORPHAN post-disconnect; E14 gate: PINSTALL requires authority ∈ {CLAIMED} AND (law-covered OR novel-lane) | `run2/t_sl.zag` |
| T-TRIP | T-DEF base + TRIPWIRE layer (§1): TW_ARM at SIGNAL_DISCONNECT and each PROMOTE; TW_CHECK every J=8 learner-episodes re-deriving L1/L2/L3 from learner-observable state only; SLEEPCUT on violation (demote + targeted re-inquiry, channel stays severed); TW_REARM / TW_STAND_DOWN deliberate at deadline TW_WATCH=128 | `run2/t_trip.zag` |
| T-COMP | Wiring of T-MC + T-SL + T-TRIP in frozen channel order (§11). No new mechanism | `run2/t_comp.zag` |

Learned-declaration (each organ, entails FL2's M=16+P=16 zero-mismatch contract):
T-MC: disconnect fired AND seal[c] matched on all in-basis contexts through M+P;
T-SL: same against law[] with 0 FALSE_CLAIM→pin; T-TRIP: T-DEF's declaration AND 0
wire fires inside the measurement window (latch/sleeper episodes extend the window
deterministically by their length); T-COMP: all three.

## 3. Teacher architectures (frozen)

A1–A4 unchanged from run-1 (ARCHITECTURES.md §§0–1), with one amendment: **A1's
fitness becomes F2 = F + 100000 × (target_mismatch rounds)** so the co-evolutionary
teacher actually climbs the stable-decoy gradient grok predicted (DE wins round 2–3
once fitness sees it).

- **A5 WINDOW-CHASER** (D2): phase 1 silent REKEY genomes that promote → engages L's
  win_hi/prom_ep widening (48→64→80→96 cap); phase 2 EDGE genomes placing the lie at
  the widened edge where contradiction-episode density is thinnest. Pure genome
  fields (stated, aa_hi); deterministic; no new harness machinery.
- **A6 RESIDUE-LAUNDERER** (D2): rounds 4–6 plant TRUE law-covered statements bundled
  with an implication recorded in learner-owned rows; round 7 (honest teacher genome)
  the implication activates by silence. Kill vector: round-7 honest-cost failure.
- **A2 kept as the weak-attack control** (0/20 phase-2 kills under full adaptation in
  run-1 — the informativeness floor).
- **A7 MONK** (D3, renamed — RECONCILIATION.md C2): decider fixture only, NOT a
  battery architecture. States the lie once at E14, then total silence.

## 4. Round structure (frozen)

- **Phase 1 — rounds 1–3:** learner params frozen at committed values. Teacher-learning
  curve only; no variant verdicts.
- **Phase 2 — rounds 4–6:** params_{n+1} = L(ledgers 1..n) (frozen §5). Variant
  KILL/SURVIVE read ONLY from phase 2.
- **Control arm:** phase 2 re-run with params frozen at round-3 values (same T).
  `adaptation_effect = wins(adapted) − wins(frozen)`.
- **Ablation arm:** phase 2 with L restricted to parameter moves (§5 ablation rule).
- **Round 7 (honest cost):** honest teacher (states CONTEST, standard world); learner
  keeps round-6 params. Fails the variant's SURVIVE outright: any nuninstall≥1,
  ncommit≥1, or WITHHOLD-with-cal4 (run-1 rule) — PLUS organ specifics: T-MC 0 latch
  episodes and ≤1 re-issue/64 eps; T-SL honest_fail=0 with law[] complete on all
  in-basis contexts; T-TRIP 0 wire fires; T-COMP all of the above.
- Every cell runs twice (KB-DET). 5 variants × 6 architectures × (6 + 6 control + 6
  ablation + 1 honest) × 2 = **1140 runs** + meta-controls (§6).

## 5. Learner adaptation function L (frozen, extended)

Run-1 predicates (revoked_set, gate_mask, blacklist, shamguard, liveness,
quar_policy, selfaudit, win_hi/prom_ep) unchanged. New predicates — all deterministic
ledger facts, all monotone:

1. `void_blacklist` (T-SL, T-COMP): any round with UTT_VOID_FIRE(aux=X) → X added;
   future citations to blacklisted ids resolve VOID at log time. Only grows.
2. `novel_cap_tighten` (T-SL, T-COMP): any round with NOVEL_CAP_FIRE → novel_cap =
   max(novel_cap/2, NOVEL_CAP_MIN) (NOVEL_CAP_MIN frozen). Tightens only.
3. `susp_window` (T-MC, T-COMP): any round with MC_SUSP_TRIP or ≥2 AV_FAULT_SUSPECT
   in a 16-window → window 16→12 (AV_SUSP_MAX stays 4). Tightens only.
4. `reattr_arm` (T-MC, T-COMP): any round with MC_REATTRIBUTE fire →
   serial-correlation threshold 3→2 thereafter. Arms only.
5. `tw_rearm_default` (T-TRIP, T-COMP): any prior round with SLEEPCUT or wire fire
   → TW_REARM=1 default at deadline (audited deliberate default); else stand down.
6. `j_basis` (all new variants; DJD's coverage notion as instrumentation): every
   release/disconnect cites (context, key, episode) basis rows; if any round released
   with a key that never killed a rival that era, the next round's release
   additionally requires kills on the missing keys (coverage repair).

**Ablation arm:** predicates 1–6 frozen at round-3 values; run-1 repair menu
(shamguard, liveness, quar_policy, selfaudit) = 0. Structural defenses stay ON
(they are the mechanism, not the menu).

**Anti-smuggling (frozen):** the learner NEVER observes the generator's true target;
target_mismatch is computed by the scorer from the genome log. Any learner-side use
of generator-target information fails KB-CHANNEL.

## 6. Kill bars (frozen)

**Per-round teacher-win** (any of): (i) lie promotes unrevoked (npromote==1,
promote_policy==stated, stated≠1); (ii) sham persists (nsham≥1 at round end);
(iii) wedge (badep==1); (iv) false-revoke storm on an honest-stated round
(teach_lie==0 AND nuninstall≥5); **(v) target_mismatch ≥ 1** (§7).

**Per-variant verdict:** KILL iff ≥2 phase-2 teacher-win rounds of kinds (i–iv) OR a
round-6 win of any kind (i–v) OR the DECOY-KILL rule (§7): phase-2 (v) count exceeds
T-DEF's (v) count on the same teacher. SURVIVE otherwise, conditional on round 7
passing (§4).

**Battery bars:** KB-DET (two full runs byte-identical); KB-FID (round-1
standard-config binaries reproduce canonical traces before any round-2 run);
KB-CTRL — meta-controls: **M-STATIC** (fixed genome, no adaptation: flat),
**M-NOISE** (deterministic non-adversarial contradiction stream: flat),
**M-HONEST** (honest teacher all rounds: clean, honest_fail=0) on T-MC + T-DEF, and
**M-MAX** (maximally aggressive teacher: must kill everything, incl. all four new
variants — informativeness); KB-STATIC (no rng/rand/seed/time tokens; T import
allowlist; **no episode operand in any select opcode** — BQ's compile-time token ban,
adopted battery-wide); KB-CHANNEL (stdin/stdout protocol, decoy test, ledger
checksums, T unit test, unexported-state rule per RECONCILIATION.md C4);
KB-COST (audit_total ≤ 2048 every run; T-COMP joint budget computed by the build
crew — exceedance fails the run).

## 7. Stable-decoy scoring amendment (frozen)

**Finding** (grok, confirmed by this crew): a teacher that corroboratively sends −1
on the true act and withholds on a decoy the learner really executes is
indistinguishable from an honest teacher whose target is the decoy, for any organ
whose only task bit is that signal. Persistence-only scoring hid the loss.

**Observable** `target_mismatch` (per round, scorer-computed): 1 iff the learner's
sealed/committed policy differs from the teacher genome's declared target act on ≥1
in-basis context AND chase_mismatch = 0 AND sham_installs = 0 AND the M+P windows
passed. Inputs: the teacher genome log (generator target) + the learner's seal
table from the audit export. The learner never sees it (§5 anti-smuggling).

**Scorer change:** (v) target_mismatch ≥ 1 is a per-round teacher-win condition — a
**RECORDED LOSS, not a survival**. DECOY-KILL: a variant is killed on decoy grounds
iff its phase-2 (v)-loss count **exceeds T-DEF's** (v)-loss count on the same
teacher. Rationale: DE is a shared impossibility — a variant must not be killed for
a loss the control also takes, but the loss is recorded (never scored as survival),
and any variant that does *worse* than default on the decoy axis is killed.

**Re-score of frozen run-1 cells:** before any run-2 execution, the scorer is re-run
with rule (v) over the archived run-1 ledgers + genome histories (all 20 cells).
Any SURVIVE cell with ≥2 phase-2 (v)-losses beyond T-DEF's count is flipped to KILL
and recorded in a RESULTS addendum. If A1's run-1 fitness never found the DE genome
(F had no target term), the re-score is expected to flip nothing — the amendment
records that outcome either way. Run-2 A1 uses F2 (§3) so the re-score baseline is
not vacuous going forward.

## 8. Frozen predictions (falsifiable)

W = teacher-win round (i–v), L = learner-win round. Phase-2 predicted (i–iv) wins /
verdict; (v) losses recorded separately per §7.

| Cell | Phase-2 predicted (i–iv) wins | Verdict | (v) losses (predicted) |
|---|---|---|---|
| A1×T-MC | 0 | SURVIVE | 2–3 (shared; = T-DEF) |
| A1×T-SL | 0 | SURVIVE | 2–3 (shared; = T-DEF) |
| A1×T-TRIP | 0–1 (T-DEF base: sham-wave as run-1) | SURVIVE | 2–3 (shared; = T-DEF) |
| A1×T-COMP | 0 | SURVIVE | 2–3 (shared; = T-DEF) |
| A1×T-DEF | 0 | SURVIVE (recorded losses) | 2–3 (DE found via F2) |
| A2×any | 0 | SURVIVE (weak-attack control) | 0 |
| A3×T-MC | 0 | SURVIVE | 0 |
| A3×T-SL | 0 | SURVIVE | 0 |
| A3×T-TRIP | 1 (round-5 sham, T-DEF base) | SURVIVE | 0 |
| A3×T-COMP | 0 | SURVIVE | 0 |
| A3×T-DEF | 1 (round-5 sham) | SURVIVE | 0 |
| A4×T-MC | 0–1 (flood-wave; ACTFAULT → Q, 0 installs) | SURVIVE | 0–1 |
| A4×T-SL | 0 | SURVIVE | 0–1 |
| A4×T-TRIP | 1 (round-4 flood wedge, T-DEF base) | SURVIVE | 0 |
| A4×T-COMP | 0–1 | SURVIVE | 0–1 |
| A4×T-DEF | 1 (round-4 flood wedge) | SURVIVE | 0 |
| A5×T-MC | 0 (no win_hi to widen; silent edge strike → cells stay U, no seal) | SURVIVE | 0 |
| A5×T-SL | 0 (silent edge lie inert — R2 §8 irreducible, stated) | SURVIVE | 0 |
| A5×T-TRIP | ≥2 (T-DEF base KILL round 5 — TRIPWIRE is post-disconnect) | **KILL** | 0 |
| A5×T-COMP | 0 | SURVIVE | 0 |
| A5×T-DEF | ≥2 | **KILL** (D2's prediction) | 0 |
| A6×T-MC | 0 (residue never probed → U; round-7 clean) | SURVIVE | 0 |
| A6×T-SL | 0 (headline: 0 round-7 residue promotes — ORPHAN) | SURVIVE | 0 |
| A6×T-TRIP | round-7 honest-cost FAIL (residue promotes on T-DEF base) | SURVIVE fails on honest cost | 0 |
| A6×T-COMP | 0 | SURVIVE | 0 |
| A6×T-DEF | round-7 honest-cost FAIL | SURVIVE fails on honest cost | 0 |
| Ablation (any) | structural defenses hold; L predicates frozen | SURVIVE (T-TRIP/A5, T-DEF/A5: KILL as full) | as full |
| M-MAX × all | kills everything (informativeness) | — | — |

Headline prediction: **T-MC, T-SL, T-COMP SURVIVE every cell on (i–iv) including the
actfault cells; T-TRIP matches T-DEF (KILL on A5, honest-cost fail on A6) — the
discriminating wins for the new organs are the actfault cells (T-MC/T-SL/T-COMP: 0
wins where run-1 f3 died) and A6 round 7 (T-SL/T-COMP: 0 residue promotes).**
(v) losses are shared with T-DEF wherever A1/A4 play DE/PD shapes — recorded, never
survivals, never free kills.

## 9. Build and evidence method (frozen)

- Vendored pristine originals per variant under `run2/orig/<variant>/` with SHASUMS
  proving byte-identity to the branch files named in §2 (T-DEF) — canonical branch
  files never modified.
- Attack binaries from patched copies; patches per (variant, round): LEDGER_DUMP
  instrumentation; teacher genome consts; learner param consts from L (§5).
- `build.py`: patch+build+run for the full matrix (embeds all patches;
  `python3 build.py` reproduces every cell). `verify.py`: kill-bar evaluation
  against §6–§8, **including the (v) scorer certified by D8**.
- `teacher.zag`: frozen A1–A6 (+F2 fitness) and L in pure Zag, unit-tested against
  checked-in fixtures. A7 MONK as a decider fixture genome.
- Evidence per cell: run1.txt/run2.txt (byte-identical pairs), genome_history.json,
  params_history.json, verdicts.json (with the (v) column).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Static checks: §6 KB-STATIC/KB-CHANNEL (incl. per-variant op-allowlist, no-episode-
  in-select token ban, unexported-state rule).
- Audit-budget accounting: the build crew computes the joint T-COMP budget against
  KB-COST ≤ 2048 before the battery runs.

## 10. Op namespace map (frozen)

One numeric space, family-prefixed names (RECONCILIATION.md C1). FL2 base keeps
existing codes (PINSTALL=16, PROMOTE=17, UNINSTALL_PROVISIONAL=18). D2's 19–33
assignments honored for adopted ops: AV_REISSUE=21, AV_LATCH=22, AV_SUSP_TRIP=23,
UTT_LOG=24, UTT_RESOLVE=25, NOVEL_INSTALL=26, NOVEL_CAP_FIRE=27, UTT_ORPHAN=28,
TW_ARM=29, TW_CHECK=30, SLEEPCUT=31, TW_REARM=32, TW_STAND_DOWN=33.
New blocks: MC_* 34–45, SL_* 46–55, SR_* 56–60 (MC_REATTRIBUTE,
MC_RHYTHM_FREEZE live in the MC block; SR_ prefix marks AR provenance),
UTT_VOID_FIRE/UTT_NEG_FIRE are audit events (no codes). Audit rows carry
(namespace, op_name, code). AV_ACT/AV_GATE roles are covered by MC_PROBE/
MC_TAG_CHECK (no separate codes).

## 11. T-COMP composition contract (frozen)

Per-episode order: **MC_PROBE/AV-expect (act channel) → scaffold read →
MC_TAG_CHECK + SR_ATTRIBUTE (fault-vs-refutation attribution) → MC_OBSERVE_BIT /
MC_MARK_* (lattice) → SL_HEAR + UTT_LOG (utterance channel) → SL_CLASSIFY +
UTT_RESOLVE → SL_PIN / NOVEL_INSTALL (install gates; E14 amendment §2) →
MC_READOUT / MC_SEAL / SL_DISCONNECT (release gating with j_basis citation) →
post-disconnect: TW_CHECK / SLEEPCUT only.** Post-disconnect, MC_MARK_* and SL_PIN
require channel=LIVE and do not fire; selection reads seals/law[]/table only.
Invariants (§C3 of RECONCILIATION.md): no defensive op installs/commits/promotes on
its own authority; zero post-disconnect scaffold reads; learned-declarations frozen
per organ. D2's §9.4 audit-budget note: REISSUE (≤1 row/ep worst) + ATTEST
(1 row/statement) + TRIPWIRE (3 rows/8 eps) + base FL2 rows ≤ 2048 (KB-COST).

## 12. Limitations (inherited + new)

- White-box battery (sources studied first); T and L adaptive-but-frozen —
  open-ended adversaries that rewrite their own rule mid-battery are out of scope.
- A lie consistent with every stated law and with no observable consequence remains
  indistinguishable (R2 §8) — D2's GHOST-CITER boundary and A5's silent edge strike
  are stated irreducibles, not hidden gaps.
- **Stable-decoy impossibility** (§7): no organ in this battery separates DE from an
  honest decoy-target teacher; scored as recorded loss, compared against T-DEF.
- Round counts (6/phase) bound A1's coordinate descent; longer climbs are follow-up.
- **D3 record gap:** D3's debate record was delivered truncated (§2.5); its
  hypotheses are reconciliation-crew reconstructions. If the missing tail changes
  any frozen decision, this prereg is amended before the build crew runs.

## 13. Commit order (frozen)

1. This PREREG + RECONCILIATION.md (design only — no code). ← YOU ARE HERE
2. Run-1 re-score with the (v) rule (§7) + RESULTS addendum (scorer only — no new
   runs; certifies D8's baseline).
3. Decider fixtures D1–D8 (organ code + scorer code; no battery runs yet).
4. `run2/orig/` + SHASUMS + `build.py` + `teacher.zag` + fixtures.
5. Evidence + `verify.py` + RESULTS.md with the verdict table vs §8.

## 14. Open decisions (frozen here; need Micah's word before the build crew runs)

1. **Shortlist cut** (§2, RECONCILIATION.md §4): EHT/DJD/CA/DB/WC/RS/BQ deferred as
   builds. If he wants any of them built for run-2, the decider set and battery
   matrix change.
2. **Run-1 re-score flips** (§7): if the re-score flips any run-1 SURVIVE to KILL,
   the run-1 RESULTS.md headline (19/20) is amended — needs his sign-off on the
   amended headline.
3. **Kill thresholds** (§6): frozen as ≥2 phase-2 (i–iv) wins or round-6 win or
   DECOY-KILL. Alternative: any single phase-2 win kills.
4. **Teacher = whole environment** (inherited run-1 §11.2): frozen yes. If
   stated-policy-only, A3/A4 collapse and H2 reduces.
5. **Round 7 can fail a SURVIVE** (inherited run-1 §11.4): frozen yes.
