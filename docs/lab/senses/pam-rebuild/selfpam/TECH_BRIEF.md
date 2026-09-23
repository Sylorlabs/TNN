# SELF-PAM — Technical Brief: the PAM admission gate as recon'd from the branch

**Date:** 2026-09-23 | **Branch:** `tnn-native-lab` (sylorlabs/TNN)
**Purpose:** Recon for Hypothesis 6 (SELF-PAM) — wire PAM admission machinery to
adjudicate TNN's OWN draft claims before output. This brief maps the surviving
gate machinery on the branch, its exact API, and the smallest buildable seam.
**Status:** recon only; nothing here authorizes a build.

**Headline finding:** there is no single "PAM admission gate" on the branch.
Three distinct survivors exist, each owning part of the API:

| # | Mechanism | What it is | Commits |
|---|---|---|---|
| G1 | R2-3 admission instrument | **Withhold-only** scorer of candidate gates. ALIVE. Cannot install by design. | `b43a1d60`, verdict R2-3 |
| G2 | cf1 corroborated-revision replay | **Install-capable** adjudication rule (pure Zag). The only survivor with a true-install path. Replay-verified, 0 false permanents. | `710367c3` (item 7) |
| G3 | R2-8 two-leg interventional gate | **Port spec only** — Python gate died on architecture; pure-Zag `gate.zag` never landed. Percept front-end pure Zag exists. | `ec124831` (DEAD on arch), spec in `b43a1d60` §2.6 |

Self-PAM therefore needs a composition: **G2's disposition engine as the
draft-claim adjudicator, gated behind G1's admission test, with G3's
leg-i/leg-ii rule as the independent-source truth check once ported.** No one
of them alone does "draft claim in → verdict out."

---

## 1. Gate API

### 1.1 G1 — R2-3 admission instrument (the withhold-only harness)

**Sources:** `docs/lab/senses/pam-rebuild/round2/forks/R2-3/src/`
- `sense.zag` (11,758 B) — the runner
- `r2p_gates.zag` (1,829 B) — candidate-gate registration interface
- `r2p_front.zag` (10,960 B) — naive percept front-end (judgment functions)
- `r2p_protos.zag` (1,771 B) — prototypes/constants
- `src/mirror/` — Python cross-validation mirror (analysis-only, 0/4,800 mismatches)

**CLI:** `sense <gate_id> <pair_dir> <report_path> <ledger_path>`

**Inputs.** A candidate gate is an integer id plus four registered functions
(in `r2p_gates.zag`):

- `gate_name(id) -> []u8` — human-readable name (report + ledger header)
- `gate_formation_src(id) -> i32` — 0 = F blob (formation span), 1 = G blob
- `gate_gate_src(id) -> i32` — 0 = F blob, 1 = G blob
- `gate_judge(id, task, evidence) -> i32` — percept judgment on the declared bytes

Hard constraints enforced by the runner before any pair executes:
`gate_valid(id)` must accept the id AND both src functions must return ∈ {0,1}.
A gate that cannot name disjoint evidence sets never runs. (`main` currently
hard-codes `gate_id ∈ {0,1}` — 0 = reference, 1 = broken positive control —
and both the range and `gate_valid` must be extended for new ids.)

**Decision law (per pair):** WITHHOLD iff `jf != jg` (formation judgment on
formation-src blob vs gate judgment on gate-src blob), else ADMIT. The runner
feeds the gate ONLY the bytes it declared.

**Outputs.** Deterministic `key=value` report + SHA-256 hash-chained ledger:
- `pairs_total`, `pairs_processed`, `pairs_error`, `pairs_withheld`,
  `pairs_admitted`, `overlap_pairs`, `overlap_pct_x100`
- Mechanical overlap audit: `gate_src == formation_src` → overlap on every
  pair (kill criterion: a candidate that passes with `overlap_pairs > 0`
  FALSIFIES THE INSTRUMENT).
- Bar: withhold rate on the 1,200 R2P pairs ≥ 90%, else the candidate is
  REJECTED before evaluation. Positive control id 1 must show 100% overlap
  and < 50% withhold (an instrument that passes everything is decoration).

**Verdict semantics:** ADMIT / WITHHOLD are the only two outputs, and there is
NO true-install path: a perverse always-withhold gate scores 100% (the
reference gate's exact score). G1 is a gatekeeper, not a gate — it keeps bad
gates out of the program; it cannot build a good one. For SELF-PAM, G1 is the
right **acceptance test** for the self-PAM gate (register it as a candidate
gate id and clear the 90% withhold bar), not the adjudicator.

### 1.2 G2 — cf1 corroborated-revision replay (the install-capable adjudicator)

**Sources:** `docs/lab/senses/pam-rebuild/v2/cf1_zag/`
- `cf1.zag` (19,417 B) — pure-Zag reimplementation of R2-4's cf1 rule
- `mrgf.tsv` (876,206 B) — deterministic pre-extracted `seq|phash|mrgF` table
- `FIDELITY.md` — fidelity report (Zag stream byte-identical to Python replay)
- `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag` — verbatim substrates

**CLI:** `cf1 <records_path> <mrgf_tsv_path> <cf1|margin>`

**Inputs.** Per-trial records, one per line, 11 pipe-separated fields:
`seq|tcode|fixture|prog|jcode|judgment|conf|pred|meas|phash|truth`

| Field | Meaning |
|---|---|
| `seq` | trial sequence number (0–11,839 in the R2-4 evidence) |
| `tcode` | task code 0–5 (colordisc/colorconst/shapetrans/pitchdisc/timbredisc/motiondir) |
| `fixture` | fixture identifier (informational) |
| `prog` | program self-verdict: 0 = PASS, 1 = negative-evidence record, 2 = FAIL |
| `jcode` | judgment integer code (per-task codebook) |
| `judgment` | judgment string (correctness = string-equality with `truth`) |
| `conf` | confidence, integer 0–1000 (700 = high-confidence bar) |
| `pred` | (g)-detection predicate: 0 = withheld from gate, 1 = gate-visible |
| `meas` | numeric measurement of the percept (feature value) |
| `phash` | 64-hex evidence hash — cross-bound to `mrgf.tsv`; mismatch ⇒ mrgF treated as unknown (-1), fail-closed |
| `truth` | ground-truth string (evidence-side; not consumed by the gate, used for metrics) |

Gate state (per task): `perm` (jc, meas, seq, valid), `prov` (same),
`chal` (stored challenger), `neg` table (6 × 256 × (jc, meas) + counts).
Tolerances per task: 8 / 40 / 60 / 4000 / 120 / 0 (`tol_of(tc)`).

**Verdict taxonomy (9 dispositions).** Install vs withhold vs flag semantics:

| Code | Disposition | Semantics |
|---|---|---|
| 0 | WITHHELD | default; or `pred==0` (never reached gate input); margin-mode: timbredisc CORROBORATED with `mrgF ≤ 382` |
| 1 | PROVISIONAL_INSTALL | first PASS installed provisionally (stored, not yet permanent) |
| 2 | CORROBORATED | PASS agreeing with a permanent incumbent (same jcode, within tolerance) |
| 3 | PERMANENT_INSTALL | second agreeing PASS promotes provisional → permanent |
| 4 | CONFLICT_WITHHELD | high-conf challenger disagrees with permanent, no corroboration — **never installed** |
| 5 | NEGATIVE_EVIDENCE | `prog==1` trial recorded into the negative-evidence table |
| 6 | SUPPRESSED | trial's (jcode, meas) matches a stored negative-evidence entry |
| 7 | REVISED_INSTALL | stored challenger corroborated by a second agreeing high-conf challenger → permanent becomes the challenger's judgment |
| 8 | CHALLENGER_PROV | high-conf challenger disagreeing with permanent stored as provisional challenger |

`is_install` = {1,2,3,7,8}; permanent installs = {3,7}. Install rules in one
line: nothing installs on its first appearance; a permanent is a
provisional re-observed within tolerance; a revision is a challenger
corroborated twice within tolerance. **Pointwise adjudication is banned by
construction:** a single disagreeing trial — even the 1145-class dominator
(conf 874, margin 10,410, strong=1, agree=1) — can only ever reach
CONFLICT_WITHHELD, never an install.

**Outputs.** stdout: `seq|disposition` per trial, seq order (11,840 lines on
the R2-4 evidence). stderr: `trials=… rk3=…/… false_perm=… rk2=…/… digest=…`
(SHA-256 of the LF-joined disposition stream with trailing LF).

**Measured:** RK-3 725/1,102 (65.8%), false permanent installs 0, RK-2
0/1,109; 3× byte-identical runs; Zag disposition stream 0/11,840 diffs vs
the Python replay. **Caveat:** replay-verified, not a theorem — the
contradiction matrix proved two correlated-wrong high-conf PASSes agreeing
within tolerance defeat the rule (CC1: seqs 10983/10992 → REVISED_INSTALL
false permanent, `v2/contradiction_matrix/CONTRADICTION_MATRIX.md`).

### 1.3 G3 — R2-8 two-leg interventional gate (spec; not yet pure Zag)

**Surviving pure-Zag source:** `docs/lab/senses/pam-rebuild/round2/forks/R2-8/src/sense_r28.zag`
— percept front-end, CLI `sense <task> <fixture_path>` → lines
`judgment=, confidence=, margin=, feature=, ops=` (6 tasks, integer-only,
confidence = 1000·margin/(margin+K_task), K per-task).

**The rule (Python eval_phase2.py — dead on architecture; pure-Zag port spec
in SURVIVOR_MECHANISMS.md §2.6, unbuilt):** per trial on (X, S, P1, P2, P3):
- leg-i: `(jx == js) ∧ (cx ≥ 700) ∧ (cs ≥ 700)` — agreement on an independent source, dual high-confidence
- leg-ii_k: `(jp_k != jx) ∨ |fx − fp_k| > 3σ_task` — each of ≥3 frozen perturbations flips the judgment or moves the feature beyond 3σ
- dispositions: INSTALL ⟺ leg-i ∧ all leg-ii; FAIL if ¬leg-i; else UNRESOLVED
- 3σ table (feature units): colordisc 2.8, colorconst 54.2, shapetrans 17.5, pitchdisc 40.2, timbredisc 2.6, motiondir 10.0 (integer fixed-point: compare `|fx−fp|*10 > T`, T = 28/542/175/402/26/100)
- Measured (Python): 0.11% false installs (13/11,630), 99.5% wrong-high-conf self-flagged, leg-ii ablation +13.70pp (13.81%→0.11%); install profile 36/11,630 (0.3%) — over-conservative, recall unmeasured

**Open blocker:** perturbation-mapping discrepancy (prereg says perturb the
independent source; the measured evidence perturbed the adjudicated source) —
frozen by amendment `f4ca485c`; must re-measure before any v2 install rule
adopts leg-ii.

---

## 2. Pure-Zag source paths (complete)

| Component | Path on branch (under `docs/lab/senses/pam-rebuild/`) |
|---|---|
| G1 runner | `round2/forks/R2-3/src/sense.zag` |
| G1 registration interface | `round2/forks/R2-3/src/r2p_gates.zag` |
| G1 front-end | `round2/forks/R2-3/src/r2p_front.zag` |
| G1 prototypes | `round2/forks/R2-3/src/r2p_protos.zag` |
| G1 Python mirror (xval) | `round2/forks/R2-3/src/mirror/` |
| G1 build substrates | R2-3's VERDICT names `R33_NATIVE_IO_V1.zag` + `R33_NATIVE_SHA256_V2.zag` in the build dir |
| G1 fixtures | `round2/fixtures/r2p/` (`r2p_<task>_<idx>.pair`, task 0–5, idx 0–199; 64-B header: task@4, idx@8, f_len@20, g_len@24, blobs@64) |
| G1 evidence | `round2/forks/R2-3/evidence/` (reports, ledgers, `GENERATOR_LEDGER_R2P.md`, `xval_log.txt`) |
| G1 verdict | `round2/forks/R2-3/VERDICT_R2-3.md` (§"Running a candidate gate") |
| G2 gate | `v2/cf1_zag/cf1.zag` |
| G2 aux table | `v2/cf1_zag/mrgf.tsv` |
| G2 substrates | `v2/cf1_zag/R33_NATIVE_IO_V1.zag`, `v2/cf1_zag/R33_NATIVE_SHA256_V2.zag` |
| G2 fidelity report | `v2/cf1_zag/FIDELITY.md` |
| G2 evidence | `round2/forks/R2-4/evidence/clean/{records.txt,sweep.jsonl,gate_dispositions.txt,ledger.txt,metrics.json}` |
| G3 front-end | `round2/forks/R2-8/src/sense_r28.zag` (+ R33 substrates in same dir) |
| G3 port spec | `v2/autopsy/SURVIVOR_MECHANISMS.md` §2.6 |
| Contradiction battery | `v2/contradiction_matrix/src/cm_main.zag` (+ generated `cm_records.zag`; scorer `score_cm.py`; `CONTRADICTION_MATRIX.md`) |
| Diagnostic harness | `v2/diagnostics/diagnose.zag` (+ `DEEP_DIVE_METHOD.md`) |
| Architecture | `v2/SYNTHESIS_V2.md` (commit `36b8a216`) |

Toolchain (all builds): pinned znc at
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

---

## 3. How to run the gate standalone on a claim + evidence set

Two runnable instruments exist today. Neither takes prose — both take
structured records, so a claim↔record codec is prerequisite for SELF-PAM.

**3.1 Run G1 (admission test for a candidate gate).**
1. Put `sense.zag`, `r2p_gates.zag`, `r2p_front.zag`, `r2p_protos.zag`,
   `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag` in one build dir.
2. Build with the pinned znc (→ ~94,418-byte native binary).
3. Register the candidate: add a new id to `r2p_gates.zag` (the four
   functions), extend the hard-coded `gate_id ∈ {0,1}` range in `main` and
   `gate_valid`.
4. Run: `./sense_bin <gate_id> docs/lab/senses/pam-rebuild/round2/fixtures/r2p/ report.txt ledger.txt`
5. Bar: `pairs_withheld / 1200 ≥ 90%`; kill: any pass with `overlap_pairs > 0`.
   Repeat ×3; reports and ledgers must be byte-identical; verify the hash chain.

**3.2 Run G2 (adjudicate a batch of claims).**
1. Build `v2/cf1_zag/cf1.zag` with its two R33 substrates in one build dir
   (pinned znc).
2. Prepare the claim set as `records.txt` (11 fields/line per §1.2) and a
   matching `mrgf.tsv` (`seq|phash|mrgF`) — `phash` MUST be the SHA-256 hex
   of the evidence bundle actually presented, cross-bound byte-for-byte, or
   the margin bar fails closed (`mrgF = -1`).
3. Run: `./cf1 records.txt mrgf.tsv cf1` (or `margin` for the timbredisc
   mrgF > 382 bar). stdout = `seq|disposition` lines; stderr = metrics + digest.
4. Repeat ×3; stdout must be byte-identical.

**3.3 What G2 needs per SELF-PAM draft claim.** Map one draft utterance to
one record: `tcode` = claim-type code (a frozen utterance-type codebook must
exist — cf1's six task codes do not cover prose), `jcode`/`judgment` = the
claim's semantic content (string-equality correctness only works for the
metrics, not the gate — the gate compares codes + tolerance), `conf` =
claim confidence 0–1000, `meas` = a numeric claim-signature with a
frozen per-type tolerance (the `tol_of` analog), `phash` = hash of the
evidence the claim rests on, `pred` = whether the claim reached the gate at
all. The **corroborator** must be C1-class: a frozen pure-Zag analytic
probe, diverse from and uncontrolled by the proposer, that agrees with the
draft — the second PASS is what installs.

---

## 4. In-flight work inventory (branch, last ~24h)

**Landed on `tnn-native-lab` touching `docs/lab/senses/pam-rebuild/`**
(all within ~17:55–23:04 PDT 2026-09-23; nothing after 23:04 — verified via
commits API):

- `b43a1d60` — Team 3 survivor mechanisms (`v2/autopsy/SURVIVOR_MECHANISMS.md`)
- `36b8a216` — `v2/SYNTHESIS_V2.md` (final synthesis, architecture, mechanism list M1–M9)
- Red-team: `0e38440f` (sealed fixtures/generator), `ed8b43a7` (attack harnesses, REDTEAM_V2.md)
- V2-B/V2-C source landings + build repairs: `cc4689f6`, `f74f4d8f`, `f9bc9992`, `e915358b`
- `dfde1297` R2-13 FS-F final (DEAD); `bc184831` PREREG V2-C AMEND1; `ec124831` R2-8 final verdict DEAD; `26fd4bb6` R2-16
- Coverage matrix: `aefe435f` (Crew D), `19dcb1a8` (V2-B gap-C verification/red-team), `230b477d` (Crew C)
- Preregs/amendments (frozen, alone before builds): `f61da3af` (PREREG_V2-IE_AMEND1, independent-evidence rule), `f4ca485c` (R2-8 perturbation-mapping freeze), `5bd979f2` (contradiction-matrix prereg), `98080233` (ceiling-test prereg), `5e31d282` (pointwise-revision ban test, item 2), `3ffb4962` (judgment-channel ban test, item 3)
- Follow-up executions: `06b27586` (item 6: contradiction-matrix execution + verdict), `f0f5f35f` (item 3: judgment-channel ban — ADOPT), `e7af4ff9`/`308fa2a1`/`dd4922f9` (item 2: pointwise-revision ban — MODIFY), `554e2242` (item 4: H1–H6 hardening battery), `73e5ffa5` (ceiling test: 4 experiments + verdict), `710367c3` (item 7: pure-Zag cf1 replay — PASS, 621/621, 0 false installs)

**Correction to the task text:** commit `0e551199` is NOT a PAMs amendment.
It is "Prereg amendment: F1.4 fixture correction + F2 chain scope" under
`docs/lab/knowledge/ingest_1gb/machinery/`. The PAMs follow-up amendments are
the `f61da3af`/`f4ca485c` pair above.

**Still open / in-flight (do not collide):**
- Item 1 (RK-3 spec-change): Micah ruled "test first"; ceiling test quantified
  the tension — full honest program theoretical max 954/1,102 = 86.6%,
  reachable ONLY via the corroborated-revision path. The spec decision itself
  is open (Micah's word).
- CC1 guard (from item 6's verdict): `mrgF ≥ task T3` challenger margin bar was
  deliberately excluded as "verify in Zag before adopting" — needs its own
  Zag verification experiment before any install path deploys.
- R2-8 pure-Zag `gate.zag` (§2.6 port spec): never built.
- V2-B (`vgate_b.zag`) and V2-C (`vsense_c.zag`): explicitly deferred by prereg call.
- Parallel coordinator rows in `v2/FORK_HYPOTHESIS_COVERAGE.md` marked
  IN-FLIGHT/COORDINATOR-OWNED (V2-A/V2-D build repair, Team 8b red-team) —
  no commits since the coverage matrix; assume live, do not duplicate.
- Sol settling experiments: preregistered sequential protocol and finite
  intervention registry — not run.

---

## 5. Assessment: the smallest integration seam for "draft claim in → verdict out"

**Recommended seam (minimal, branch-faithful):**

1. **`admit_claim(task, jcode, conf, meas, evhash) → disposition`**: extract
   cf1's gate-step (lines ~324–414 of `cf1.zag`) as an in-process Zag
   function, not a batch CLI. Keep the state arenas (perm/prov/chal/neg),
   the 700 bar, the tolerance table, and the disposition codes verbatim.
2. **Claim codec (the actual first build artifact):** draft utterance →
   the 6-field record. Requires three frozen tables that do not yet exist:
   a task/type codebook for utterance kinds, a `tol_of` analog per type,
   and an evidence-hash binding (`phash`) computed over the evidence the
   claim cites.
3. **C1-class corroborator as the second hit:** the install path needs a
   frozen pure-Zag analytic probe, diverse from and uncontrolled by the
   proposer, that agrees with the draft within tolerance. This is the
   install condition — first draft → PROVISIONAL (never emitted);
   corroborated → INSTALL; disagreed-but-uncorroborated →
   CONFLICT_WITHHELD (never emitted); negative-evidence match → SUPPRESSED.
4. **G1 admission test for the whole self-PAM gate:** register the
   self-PAM gate as a candidate id in `r2p_gates.zag` (its "formation" span
   = draft-production context, its "gate" span = independent re-measurement
   of the claim's subject) and clear the 90% withhold bar before the
   install rule is trusted.
5. **G3's leg-i/leg-ii as the strengthen-later truth check:** once the
   R2-8 port lands, independent-source agreement + perturbation-fragility
   becomes the install rule's admission leg.

**Explicit non-goals / prohibitions (from the branch's frozen verdicts):**
- A single draft can NEVER be installed on its own evidence — pointwise
  adjudication is machinery-banned (trial-1145 rule). Self-PAM is
  **corroboration-only revision**: historical corroboration or nothing.
- Withhold-everything is not a target; every safety bar ships with its
  recall pair (M9), or R2-8-style over-conservatism (0.3% install rate)
  passes while accepting no truths.
- Judgment-side acceptance channels are banned under the frozen threat
  model (MACHINERY ceiling, 0.0000 bits); only registered C1-class probes
  with their own false-installation budget.
- No install path deploys before the CC1 correlated-corroborator guard is
  verified in Zag.

**Smallest viable first deliverable:** `selfpam/admit_claim.zag` (cf1 gate-step
as a function) + the claim codec for ONE utterance type + a single C1-class
corroborator, registered as a G1 candidate gate, with the G2 verdict
taxonomy as its output. That is the seam; everything else is calibration.
