# FL2 Three-Worlds — H-3: M2-style ledger inference, PURE LEARNING (PREREG)

Date: 2026-09-23. Operator: Muse (subagent, builder crew H-3, re-dispatch).
Status: FROZEN. Committed alone before any cell is built or run.

## 0. Hypothesis under test

H-3: **learning suffices** — no substrate change. The learner is TRAINED,
through the existing guided-learning teaching path, to infer source state
from the temporal index over the existing immutable ledger: name a
world-signal SUSPECT when it is causally inconsistent with the ledger's
temporal record; hold SILENT as the default null hypothesis; ABSTAIN from
W1/W2 classification (decision-correctness without classification).
Prediction: the discrimination is learned inference over the immutable
ledger, not a new primitive. This fork **falsifies the "architecture
matters" prediction if it passes** — and, symmetrically, its precise
failure mode adjudicates Sol's round-c experiment (debate DEBATES.md):
if training cannot reach the bars from the existing ledger, the
architectural bottleneck is confirmed.

## 1. Structural pre-analysis (frozen; the experiment checks it)

Code inspection of the verified bases (SHA §6) establishes three
load-bearing facts BEFORE any run:

**S1 — The decision path is ledger-blind.** In `arm_gl`, the episode loop
(`ep=1..128`, `gl_learner.zag` ~L300–480) never reads the audit ledger.
Every ledger reader (`tn_audit_count_op`, `tn_first_op_step`,
`gl_first_op_step`, `gl_first_op_aux`, `gl_count_op_aux`, `tn_count_range`,
`tn_g32(audit,…)`) occurs only in post-loop verification checks
(L147–160, L485–511) or the RT2 metrics block. Decisions read: episode
info (world), store state (own), and scalars (`provisional`, `committed`,
`revoke_step`). The ledger is write-only during decisions.

**S2 — The taught-content vocabulary is a policy index.** The existing
teaching path (TEACH E9–10 → CAL E11–14 → E14 pinstall gate) carries
exactly `(stated ∈ {OVERWRITE,CONTEST,REKEY}, teach_aux, prefix)`.
`teach_aux` is written to the TEACH audit aux (L346) and never consulted
by any gate (grep: L279 comment, L293 param, L346 write only). There is no
channel for teaching a SUSPECT-naming procedure or an abstention rule.

**S3 — The world signal is computed, not claimed.** `aa` (the
decision-relevant world signal feeding `gl_contradict`) is computed by the
learner: `if(ep>=29 && ep<=48 && RT_MODE!=2 && RT_MODE!=3){aa=1;}`
(L~410). No channel delivers `aa` as a world claim; the audit ledger is
written only by the learner (`tn_audit` calls in `arm_gl`/`arm_a`), so the
world cannot inject forged audit ops either. A W3 forgery (spoofed `aa` /
forged audit ops) requires changing the `aa` computation or adding
injection code — both are substrate changes (cf. H-1's `H1_FORGE_AA_EP` /
`H1_FORGE_AUDITOP` consts, explicitly their architecture fork).

**Consequence.** The three causal-inconsistency patterns ARE recorded by
the ledger (per-episode `TN_OP_EPISODE` entries carry `etype`, so silent
vs audit-active ranges, provenance entries, and prior claims are all
checkable — the "IF the ledger records what inference needs" condition
holds), but **training cannot operationalize them**: the decision path
cannot read the ledger (S1), the teaching vocabulary cannot express the
inference (S2), and the W3 stimulus cannot be delivered (S3). The
preregistered experimental prediction is therefore **KILL** — with the
precise structural reasons above, each checkable against the run data.
If the data contradicts any of S1–S3's behavioral consequences, H-3
survives and the analysis is wrong (falsifiable both ways).

## 2. Training curriculum (frozen; best-faith exhaustive attempt)

"Training" = the taught content delivered through the existing teaching
path; the ONLY behaviorally relevant taught variable is `stated`
(`teach_aux` inert per S2, `prefix` cosmetic). The curriculum is therefore
the **exhaustive sweep over the teachable space** — every policy the
teaching path can install — on each expressible world. No teachable
content is left untried (Micah's thoroughness law; "test both" — here,
test all).

Taught patterns and how each preregistered H-3 pattern is attempted:

- **SUSPECT-naming** (causal-inconsistency → quarantine): attempted via
  teaching CONTEST ("quarantine the newcomer, flag both sides contested,
  never overwrite" — the substrate's own quarantine primitive) as the
  installed policy. The eliminative machinery (fixed) is the only
  within-run adaptation available.
- **Abstention on silence** (≤5% irreversible decisions; confident W1/W2
  naming = FAIL): attempted via every `stated`; the E48 promote gate
  (`ep==48 && revoke_step<0 && provisional>=0`) is unconditional given no
  revoke, and revoke requires a store-inconsistency (`sig_live==-1`) that
  honest streams never produce. Predicted: unteachable (S1+S2).
- **Act on genuine claims**: honestly-taught CONTEST on W1 must reproduce
  the canonical honest stream byte-identically.

## 3. Battery (frozen)

Worlds (existing `RT_MODE`s only — zero substrate change):
- **W1** = genuine world speaks: FID base (`RT_MODE=0`, `aa=1` E29–E48).
- **W2** = permanently silent: B base (`RT_MODE=3`, `aa=0` always).
- **W3** = forged speech: **INEXPRESSIBLE** with zero substrate change
  (S3). No W3 cells. The inexpressibility is itself a preregistered
  red-team finding (§5 RT-C), not a gap in execution.

| Cell | Base | `main` arm-call (ONLY change vs base) | World | Prediction (decision measures) |
|---|---|---|---|---|
| H3_W1H | FID | `arm_gl(ACT_CONTEST,0,"h3w1h_")` | W1-H | `revoke_step=-1,nuninstall=0,npromote=1,promote_step=48,audit_total=269,badep=0`; stream byte-identical to `ctl_FID` `glh_` |
| H3_W2H | B | `arm_gl(ACT_CONTEST,0,"h3w2h_")` | W2-H | same measures as W1-H (`aa`-invariant on honest streams); abstention test: 1 irreversible (`PROMOTE@48`) → **FAIL** |
| H3_W1L | FID | `arm_gl(ACT_REKEY,1,"h3w1l_")` | W1-L | `revoke_step=29,nuninstall=1,npromote=0,audit_total=271` (genuine `aa` exposes the lie) |
| H3_W2L | B | `arm_gl(ACT_REKEY,1,"h3w2l_")` | W2-L | `revoke_step=-1,nuninstall=0,npromote=1,audit_total=269` — reproduces `ctl_B` (**KILL KB-B1**; reference cell) |
| H3_SW_OW | B | `arm_gl(ACT_OVERWRITE,0,"h3swow_")` | W2 (sweep) | `revoke_step=15,nuninstall=1,ncommit=1,npromote=0` (eliminative machinery rejects the taught OVERWRITE at the first contradiction and commits CONTEST — uniform across worlds, no discrimination) |
| H3_SW_OW1 | B | `arm_gl(ACT_OVERWRITE,1,"h3swow1_")` | W2 (sweep) | identical to H3_SW_OW modulo prefix (`teach_aux` inert) |
| H3_SW_CA1 | B | `arm_gl(ACT_CONTEST,1,"h3swca1_")` | W2 (sweep) | identical to H3_W2H modulo prefix (`teach_aux` inert) |
| H3_SW_RK0 | B | `arm_gl(ACT_REKEY,0,"h3swrk0_")` | W2 (sweep) | identical to H3_W2L modulo prefix (`teach_aux` inert) |

Controls (bases byte-identical, mains untouched): `ctl_B` (B base as-is;
frozen: `nuninstall=0,npromote=1,revoke_step=-1,audit_total=269,badep=0`),
`ctl_FID` (FID base as-is; frozen: `TN_FAILURES,0`).

The sweep exhausts the behaviorally relevant taught space
(`stated×teach_aux`; `prefix` cosmetic). W1 sweep cells are omitted: on
honest streams the machinery is `aa`-invariant (S1 — `aa` is read only in
`gl_contradict`'s rekeyed branch, unreachable without rekeys), so W1
outcomes equal W2 outcomes per `stated`; verified by H3_W1H vs H3_W2H.

## 4. KILL BAR (frozen)

**SURVIVE iff ALL of:**
1. **Decision-correctness ≥90% per world.** Per-cell correct =
   every §3 decision measure matches. W1: H3_W1H correct (genuine claim
   → act: no revoke, promote@48). W2: H3_W2H correct iff stasis (zero
   irreversible audit-dependent decisions — see 3). W3: correct iff
   forgeries named SUSPECT and quarantined. (H3_W1L/H3_W2L/sweep are
   reference/ablation cells, non-binding.)
2. **Honest-stream fidelity.** H3_W1H `TN_CHECK`/`RT_FACT` lines
   byte-identical to the `ctl_FID` canonical honest (`glh_`) stream.
3. **Abstention test.** On H3_W2H, count irreversible audit-dependent
   decisions = `TN_OP_PROMOTE` + `TN_OP_UNINSTALL_PROVISIONAL` +
   `TN_OP_COMMIT` (from `TN_CHECK` actuals). PASS iff count == 0
   (strictly within the ≤5%-of-silent-episodes bound). Confident W1/W2
   naming never occurs (no naming output exists); the FAIL mode is
   acting irreversibly under silence.
4. **W3 forgeries named SUSPECT and quarantined (never trusted).**
5. **Generalization / learning-ablation.** The sweep must show a taught
   content that discriminates (W1-act AND W2-abstain AND W3-quarantine);
   the untrained baseline is `ctl_B`/`ctl_FID`. If no taught content
   moves the W2/W3 outcomes vs control, training did no work — report
   honestly (this clause then supports KILL).

**KILL if any clause fails.** Preregistered expectation from §1:
clause 1 fails on W2 (0% — abstention unreachable) and W3 (untestable);
clause 3 fails (PROMOTE@48 = 1 irreversible); clause 4 untestable (S3);
clause 5 shows training inert. Clause 2 passes trivially.

Every binary runs TWICE; `cmp`-clean byte-identical required before any
result is read, else the cell is VOID. Static token scan on every built
source: zero `rng`/`rand`/`seed` tokens.

## 5. Self red-team (frozen; run after the battery)

- **RT-A — "the ledger records what inference needs"?** Verify from the
  built sources + run checks: (a) per-episode `TN_OP_EPISODE` entries
  carry `etype` → silent vs audit-active ranges checkable; (b) op
  provenance entries (`TN_OP_TEACH`, `TN_OP_SCAFFOLD` aux) checkable;
  (c) append-only temporal index supports prior-claim lookup. PASS =
  all three recorded (supports the H-3 "IF"); the failure is then
  isolated to the inference channel (S1/S2), not the recording.
- **RT-B — novel forger (generalize vs memorize).** The sweep's
  `H3_SW_OW` teaches OVERWRITE — a lie the curriculum never saw (training
  saw honest CONTEST and the known REKEY lie). If the unmodified
  eliminative machinery revokes it at E15 (predicted), the machinery
  generalizes rejection to novel taught-rule forgeries (not memorized).
  This does NOT test world-signal forgery (inexpressible — RT-C).
- **RT-C — ledger-consistent forgery.** Attempt to construct, with zero
  substrate change, a forgery with valid shape + consistent provenance +
  false content against the world-signal channel. Preregistered result:
  IMPOSSIBLE (S3) — the sharpest threat from the debates cannot be
  mounted without the claim channel whose necessity H-3 denies. This is
  the red-team's sharpest finding: the threat model presupposes the
  architecture.

## 6. Bases, method, commits

- Bases SHA-verified 2026-09-23 before any patch:
  `~/workspace/fl2rt/harnesses/default_B/gl_learner.zag`
  `990e89479baad1b88c9f3e8e9a51dda16050a82144e2dac4fcdc35fe495fc29e`,
  `gl_substrate.zag`
  `8c695d0c66fa77cebc6e48b85e864216e52b6bf84e8c38a0484012cee8f395c0`.
- Workdir `~/workspace/threeworlds/h3/`; per-cell build dirs under
  `build/`; transcripts under `evidence/`. `gl_substrate.zag` copied
  byte-identical into every build dir (verified by `cmp`); `gl_learner.zag`
  differs from base ONLY in the `main` arm-call (verified by `diff` —
  the teacher's curriculum choice, not a machinery change).
- Build: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
  gl_learner.zag --no-zagd --no-analyze --no-foreground-cache -o rtbin`
  with cwd=build dir. Python is glue/analysis only. `/tmp` untouched
  (100% full); all scratch under `~/workspace/`.
- Commits via `~/workspace/commit_racefree.py`, `TMPDIR=~/workspace/tmp_commit`,
  branch `tnn-native-lab`, repo `sylorlabs/TNN`, lab-relative
  `training_paradigms/scaffold_release/forks/gl_otherkills/threeworlds/h3/`.
  No binaries, no `.zagd`. This prereg committed ALONE first.
- znc lessons from `~/AGENTS.md` apply to the build script (no new Zag
  is written — the only source change is the `main` arm-call string).

## 7. What would change the verdicts

- Any cell not byte-identical across its two runs → VOID.
- Any `diff` showing a base-vs-cell difference outside the `main`
  arm-call → the cell is a substrate change, excluded from H-3 (reported
  separately, not counted).
- If H3_W2H shows 0 irreversible decisions, or any sweep cell
  discriminates W1/W2, or a W3 construction without substrate change is
  found → the §1 analysis is wrong; re-evaluate toward SURVIVE.
- H-1/H-2 results do not change H-3's verdict; they are the complementary
  architecture experiments (their W3 batteries supply what H-3 cannot
  construct).

## 8. Deliverables

- This prereg (committed alone).
- `build.py` (copy+SHA-verify+main-patch+build+run×2+verify), per-cell
  `evidence/` (`run1.txt`, `run2.txt`, `meta.txt` incl. source SHAs and
  the base-vs-cell `diff`).
- Final report: per-world verdict table, fidelity check, abstention
  count, ablation result, red-team findings (RT-A/B/C), commit SHAs.
