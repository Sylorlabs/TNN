# PREREG AMENDMENT 1 — Independent-Evidence Rule (V2-A / V2-D)

**Status: FROZEN 2026-09-23. Committed alone — before any hardening-fork build
output exists.**
**Amends:** `senses/pam-rebuild/v2/preregs/PREREG_V2-A.md` (§2) and
`senses/pam-rebuild/v2/preregs/PREREG_V2-D.md` (§2).
**Authority:** Micah — PAMs v2 follow-up item 4 (V2-A/V2-D hardening: YES, NEEDED).
**Scope:** the independent-evidence decision rule ONLY. No change to the frozen
11,840-trial batteries, fixtures, trial order, front-ends, ledgers, or the
already-recorded fork verdicts (V2-A DEAD on RK-3; V2-D ALIVE within the frozen
threat model stand as written).

## A1.1 Threat model (named explicitly)

The red-team battery (`v2/redteam/REDTEAM_V2.md`, 2026-09-23) confirmed the
correlated cross-span failure the forks' `EXPOSURE_CORRELATED_FAILURE.md`
files had documented as known-but-unhardened. The independent-evidence signal

```
ind := (jG == jF) AND (confF >= 700) AND (confG >= 700)
```

treats formation-independent agreement as evidence of truth. That inference is
valid ONLY under a threat model the red team showed to be false. The amended
threat model names three adversary capabilities:

- **T1 — Record-channel forgery.** The adversary writes arbitrary `(jG, confG)`
  fields into the gate's input records. The decoy stream (8 synthetic records
  with judgment flipped, `jG`/`confG` spoofed to 800 to agree) proves bare
  record-field agreement is forgeable: V2-A REVISE-installed 15 false judgments
  and V2-D ACCEPT-installed 19 false judgments on spoofed agreement alone.
  *Bare (jG, confG) fields are not a channel.*
- **T2 — Correlated cross-span fooling (common-mode front-end failure).** The
  adversary's stimuli fool the front-end IDENTICALLY on the F and G spans at
  high confidence (`jG == jF == wrong`, both conf ≥ 700). The in-prereg
  calibration P(signal | wrong high-conf) = 0.6% (R2-4 frozen families) does
  NOT transfer: on the 12 novel families the withhold stream showed 9/43
  (20.9%) of fired installs false. Genuine, high-confidence, attested agreement
  on a wrong judgment is possible and was observed.
- **T3 — Permanent-slot overwrite via trusted agreement.** One spoofed (T1) or
  correlated (T2) agreement record supersedes a permanent install with no
  adjudication ("conflicts are NOT adjudicated here", vgate_d.zag). A single
  record permanently poisons durable memory.

Under T1–T3, the frozen rule is a wrong-install engine: V2-D installed 43
ACCEPT_INSTALL on 288 UNRESOLVED trials (9 false), bypassing all withhold
logic because the rule has no prog requirement.

## A1.2 The exact rule change

The independent-evidence acceptance rule in PREREG_V2-A §2.2 and PREREG_V2-D
§2.1 is REPLACED in full by the following. (Definitions: `prog` 0=PASS
1=FAIL 2=UNRESOLVED; install bar conf ≥ 700 unchanged; corroboration
tolerances [8,40,60,4000,120,0] unchanged.)

**R1 — Prog gate (answers the V2-D withhold kill).** The independent-evidence
acceptance path fires ONLY on `prog = PASS` trials. UNRESOLVED trials are
withheld; FAIL trials become negative evidence. No acceptance-path disposition
may be emitted for a non-PASS trial, ever.

**R2 — Channel authentication (answers T1).** The G re-judgment counts as
independent evidence ONLY when it arrives over a REGISTERED, AUTHENTICATED
channel. The gate holds the channel's registration key; agreement counts only
when the record's channel attestation verifies:

```
gatt == sha256hex(CHANNEL_KEY || seq || "|" || fixture || "|" || jG || "|" || confG)
```

with frozen test registration key `CHANNEL_KEY = "PAMV2-REG-CHANNEL-2026-09-23"`.
(A production deployment replaces the test key with a real channel-key
ceremony; the mechanism — the gate verifies, the forger cannot sign — is what
is frozen here.) Bare `(jG, confG)` record fields, however agreeing, are
insufficient and are treated as absent independent evidence.

**R3 — Attested-agreement install bar.** No install of any kind (provisional
or permanent) is emitted unless the trial satisfies ALL of: `prog = PASS`,
`pred = 1`, `conf ≥ 700`, and attested agreement (`jG == jF`, `confG ≥ 700`,
valid `gatt`). Trials failing this are WITHHELD (detail `unattested` /
`lowconf` / `pred0`). Permanence requires a corroborating trial that ALSO
satisfies R3 (same task, same judgment class, |measure| within tolerance).

**R4 — Conflict adjudication (answers T3).** No permanent slot is overwritten
on agreement alone — conflicts are ADJUDICATED, never auto-applied. A
challenger satisfying R3 whose judgment class differs from the permanent slot's
is REVISE-installed (supersede with ledger audit) ONLY IF both hold:

  (a) **Historical corroboration (cf1-class):** at least one PRIOR trial in the
      stream with the same task, same judgment class, `prog = PASS`, and
      |measure| within the task tolerance;
  (b) **Challenger margin:** `mrgF ≥ T3`, where `mrgF := conf_challenger −
      conf_incumbent` (the incumbent's install confidence is stored with the
      permanent slot) and the frozen schedule `T3[task] = 100` for all six
      tasks.

  Otherwise the trial is CONFLICT_WITHHELD and the permanent slot stands.
  (Rationale, frozen: durable memory has hysteresis — a challenger must be a
  strictly stronger observation by a full confidence band, not merely an
  agreeing one.)

R1–R4 together: independent evidence = attested, PASS-gated agreement, and it
can INSTALL (subject to R3) but can only REVISE durable memory through
adjudication (R4).

## A1.3 What stays frozen

- The V2-A/V2-D fork verdicts and all frozen-battery bars (RK-1/2/3/5, B5, B6,
  B1, DD-1/DD-2) — this amendment governs the NEW hardening battery only.
- Front-ends, fixtures, the four red-team temptation streams
  (`rec_clean/rec_withhold/rec_install/rec_decoy.records`, 13 fields), the
  committed attack harnesses (`rt_records.zag`, `rt_score.zag`), and the sealed
  fixtures (hashes/counts/verdicts only — the hardening forks consume records,
  never fixture bytes).
- The hash-chained ledger construction and the disposition vocabulary scored
  by `rt_score.zag`.

## A1.4 Hardening fork battery (frozen)

Six pure-Zag gates, each a minimal delta isolating one design piece, all run
head-to-head on the four streams (3× byte-identical runs, ledgers verified):

| fork | base | exact rule delta under test |
|------|------|------------------------------|
| H1 | vgate_d | R1 only: `ind` requires `prog = PASS`. Isolates the withhold kill. |
| H2 | vgate_a | R1+R2: adjudicator's `ind` requires PASS + valid `gatt`; base install path UNCHANGED. Isolates authentication (does auth alone stop spoofed installs, or does the unattested base path still install decoys?). |
| H3 | vgate_a | R1+R2+R4: overwrite of permanent slots requires adjudication (corroboration + margin); first-install path unchanged. Isolates adjudication. |
| H4 | vgate_a | R1 + revision requires a corroborated second observation within tolerance (cf1-class, no margin, no auth). Isolates historical-corroboration-only revision. |
| H5 | vgate_a | **R1+R2+R3+R4 (the amended rule, composite).** |
| H6 | H5 | H5 with first-seen installs removed: a first R3-satisfying observation is WITHHELD `unconfirmed` and stored; PERMANENT_INSTALL only on a corroborating second R3 observation; R4 unchanged. Isolates the no-provisional strictness trade. |

H1–H4 are diagnostic ablations (expected to fail at least one bar each — that
is their purpose); H5 is the amendment's rule; H6 tests whether removing
provisional installs buys further false-install reduction and at what install
cost.

## A1.5 Kill bars (frozen; applied mechanically to H1–H6)

- **KB-H1:** 0 false installs on ALL four streams. (False install = installed
  disposition — PROVISIONAL/PERMANENT/ACCEPT/REVISE — on a wrong judgment,
  per `rt_score.zag`.)
- **KB-H2:** withhold-everything stream: 0 installs (288/288 WITHHELD or
  SUPPRESSED).
- **KB-H3:** decoy stream: 0 false installs.
- **KB-H4:** install-nothing stream: installs > 0 (no collapse to the
  degenerate zero-install path — R2-4's disease).
- **KB-H5 (hard):** 3 full runs byte-identical per fork per stream
  (dispositions + ledger digests); every ledger hash-chain verified.

## A1.6 Pre-registered predictions

- H1: KB-H2 PASSES (43 → 0 installs on withhold). KB-H1/KB-H3 FAIL on decoy
  (decoys are prog=PASS; spoofed agreement still fires) and on clean (base-path
  false installs unchanged).
- H2: spoofed `ind` goes silent; KB-H3 improves but FAILS — the unattested base
  path still provisionally installs decoy records (prog=PASS, conf ≥ 700).
  Isolates the base-path gap the composite must close.
- H3: decoy REVISE/ACCEPT-overwrites → 0, but first-installs of decoys remain;
  KB-H3 FAILS. Clean: margin blocks the TMB-5 revise chain after the first
  provisional.
- H4: singleton decoys cannot revise; KB-H3 FAILS on first-installs; clean
  class-1 (self-corroborating TMB-5 RICH chain) still installs — corroboration
  alone does not beat T2.
- H5: KB-H2 ✓, KB-H3 ✓ (0 false — decoys lack valid `gatt`), KB-H4 ✓.
  KB-H1 on clean: residual predicted ≈ 2–3 — trials with GENUINE attested
  high-confidence agreement on wrong judgments (T2), which no record-field rule
  can separate from correct agreeing trials; the residual is attributed to the
  front-end per REDTEAM_V2.md §7.6 (standing observation), not to the gate.
- H6: KB-H2 ✓, KB-H3 ✓, KB-H4 ✓ (adjacent corroborating pairs still install);
  clean residual predicted ≤ H5's (first-seen false provisionals removed) at
  the cost of fewer correct installs.

## A1.7 Test streams (frozen)

The red-team's four committed record streams, unmodified (13 fields):
`rec_clean.records` (288), `rec_withhold.records` (288, prog forced
UNRESOLVED/pred 0), `rec_install.records` (44, prog=PASS & conf ≥ 700, sorted
for adjacency), `rec_decoy.records` (44 + 8 spoofed). Channel attestations
(`<stream>.gatt`, `seq|gatt_hex` sidecar) are built by deterministic Python
glue: `gatt = sha256hex(CHANNEL_KEY || seq || "|" || fixture || "|" || jG ||
"||" || confG)` for genuine records; 64 zeros for the 8 decoy records (the
forger holds no channel key — this is the T1 model, and the gate never sees
truth). The 8 decoy seqs are identified by byte-exact re-derivation of the
decoy construction (verified against the committed stream), not by hand.

## A1.8 Commit map

- This amendment: `senses/pam-rebuild/v2/preregs/PREREG_V2-IE_AMEND1.md`
  (committed ALONE, this commit).
- Hardening forks (later, additive commits): `senses/pam-rebuild/v2/hardening/`
  — `H1/`…`H6/`, each with `src/` (gate .zag + substrates + SOURCES.md),
  `evidence/` (RUNLOG, per-stream scores, digests), and the shared
  `gatt/` sidecars; `HARDENING_VERDICT.md` (head-to-head table, winning
  design(s), recommendation) at `v2/hardening/`.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Via
  `~/workspace/commit_racefree.py`, TMPDIR=`~/workspace/tmp_commit`,
  lab-relative paths (`senses/pam-rebuild/v2/...`). No binaries, no `.zagd`,
  additive-only.

**Laws:** pure Zag for mechanisms/learners/verification; Python only for
glue/analysis. Zero RNG in any decision path. Byte-identical reruns required
(≥3×).
