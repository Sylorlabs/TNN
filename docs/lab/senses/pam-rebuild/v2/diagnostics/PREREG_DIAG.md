# PREREG — Deep-Dive Diagnostic Harness (PAMs v2, Team 7)

**Status: FROZEN 2026-09-23. No retroactive changes to probe definitions,
verdict rules, or kill bars after the self-application runs. Amendments go to Micah.**

## 1. What is built

A pure-Zag diagnostic harness (`diagnose.zag`) that automates the
knowledge-vs-machinery probe split from the Deep-Dive Method: given a frozen
behavioral-failure case record, it (a) reproduces + freezes the failure,
(b) instruments white-box internals, (c) runs a KNOWLEDGE probe battery and a
MACHINERY probe battery, and (d) emits a structured knowledge-vs-machinery
verdict with evidence pointers. Zero RNG. Byte-identical reruns.

The harness is case-agnostic: case specificity comes from two input files,
never from harness source edits.

## 2. Inputs (frozen formats)

`diagnose <case_record> <expect> <report_out>`

**case_record** — one line per trial, pipe-separated integers:
`seq|tcode|prog|jcode|jcorrect|conf|pred|meas|progF|disp|detail`
- `prog`: gate-consumed program verdict, 0=PASS 1=FAIL 2=UNRESOLVED
- `jcorrect`: 1 if the percept's judgment equals ground truth
- `conf`: integer confidence (percept layer)
- `progF`: independent-evidence program verdict, 0/1/2 (same coding)
- `disp`: recorded disposition, 0=PROVISIONAL_INSTALL 1=CORROBORATED
  2=PERMANENT_INSTALL 3=WITHHELD 4=CONFLICT_WITHHELD 5=NEGATIVE_EVIDENCE
  6=SUPPRESSED
- `detail`: reason code (0=new 1=corroborated 2=perm 3=perm-measure-diff
  4=prov-measure-diff 5=reversed_old 6=perm_seq 7=unresolved 8=neg 9=pred0
  10=stored 11=dup)

**expect** — `KEY=value` lines: `CASE`, `N_TRIALS`, `RK3_NUM`, `RK3_DEN`,
`RK3_BAR_NUM`, `RK3_BAR_DEN`, `REPLAY_MISMATCH_MAX`.
Python glue (`gen_case_record.py`) derives both files from frozen evidence;
the glue is not the instrument — the Zag binary is.

## 3. Harness phases (frozen)

1. **DIAG_LOAD** — parse both files into bounded arenas; SHA256 the raw case
   bytes → CASE_DIGEST; assert row counts match. Fail closed on parse error.
2. **DIAG_REPRODUCE** — recompute the headline failure metric from the record
   (correct-highconf = jcorrect==1 && conf>=700; installed = disp in {0,1,2});
   assert equals `RK3_NUM`/`RK3_DEN` exactly. Mismatch → report DIAG_FAIL,
   no verdict.
3. **DIAG_REPLAY (machinery fidelity)** — re-implement the documented gate
   disposition rule (negative-evidence table 256/task, provisional/permanent
   slots, fixed corroboration tolerances) over the case stream in order;
   compare predicted vs recorded `disp` per trial; count mismatches.
   Any mismatch ⇒ the implementation deviates from its design.
4. **DIAG_KNOW (knowledge battery, on the frozen record)** —
   - K1 knowledge presence: `progF==0` rate among correct-highconf.
   - K2 knowledge delivery: `prog==0` rate among correct-highconf
     (knowledge that reached the decision point).
   - K3 non-install bucketing: partition every non-installed correct-highconf
     trial into {never-PASS, conflict-withheld, suppressed, pred0-withheld}.
   - K4 adjudication gap: among conflict-withheld correct-highconf, count
     trials where conf>=700 (knowledge present in the record but unread by
     the rule) and where progF==0.
5. **DIAG_SYNTH (machinery battery, synthetic, knowledge held fixed)** —
   - M1 control: 1,200 closed-form synthetic trials (prog=0, pred=1,
     conf=800, jcode alternating per task, no prior permanent) → install
     rate must be 100%.
   - M2 conflict: seed each task's permanent slot with a differing jcode,
     then 1,200 synthetic trials (prog=0, pred=1, conf=800, conflicting
     jcode) → CONFLICT_WITHHELD rate must be 100%.
   All synthetic inputs are closed-form functions of the trial index.
6. **DIAG_CEIL** — gate-side ceiling: correct-highconf with prog==0 and
   pred==1 (max installable by ANY gate change); compare vs the bar
   (`RK3_BAR_NUM`/`RK3_BAR_DEN`); ceiling < bar ⇒ SPEC-TENSION flag.
7. **DIAG_VERDICT** — deterministic rules (§4) → structured verdict.
8. **DIAG_REPORT** — write the report: verdict, every number with its
   evidence pointer (case digest, ledger digest, report digest), repair
   class, red-team prompts, honest gap list.

## 4. Verdict taxonomy (frozen rules, evaluated in order)

- **MACHINERY-BUG** if REPLAY mismatches > `REPLAY_MISMATCH_MAX` or M1 < 100%:
  the mechanism does not execute its own design. Repair class: CODE-REPAIR.
- **KNOWLEDGE** (primary) if no machinery-bug and any K-bucket is non-empty:
  the failure is missing knowledge — a rule the white-box state could have
  supported but didn't contain (K4), or knowledge absent at the program
  layer (K1/K2 gaps). Repair class: RULE-ADDITION (deliberate audited
  revision) or PROGRAM-TEACHING. A surface patch that installs more without
  the missing adjudication rule is BLOCKED (it installs false permanents —
  cf. the cf2 counterexample in the R2-4 autopsy).
- **MACHINERY-BY-DESIGN** if no machinery-bug, all K-buckets empty, and the
  designed rule fully accounts for the failure: the mechanism is correct and
  the design is complete. Repair class: none at this layer.
- **SPEC-TENSION** (orthogonal flag): gate-side ceiling < bar. Repair class:
  SPEC-CHANGE (bar or contract), never a code patch.
- **INCONCLUSIVE** otherwise, with the gap list as the deliverable.

## 5. Audit ledger (frozen)

The harness keeps its own append-only 16-word audit ledger:
op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60 —
one entry per phase (before/after counters in b/a words). Op codes
101..108 = DIAG_LOAD..DIAG_REPORT. SHA256 over the ledger bytes →
LEDGER_DIGEST in the report. Ledger printed to the report file, not stdout.

## 6. Kill bars for the harness itself

- **KB-D1**: builds clean with the pinned toolchain
  (`toolchain/bin/znc_linux_x86_64_abed8aa1`), no analyzer errors.
- **KB-D2**: self-application on R2-4/RK-3 reproduces 104/1,102 exactly and
  REPLAY yields 0/11,840 mismatches (matches the independent Python replay).
- **KB-D3**: 3 runs byte-identical (report SHA256 identical across runs).
- **KB-D4**: M1 = 100% install, M2 = 100% CONFLICT_WITHHELD on synthetics.
- **KB-D5**: the emitted verdict contains all eight report sections (§3.8)
  with every number carrying an evidence pointer; no number is asserted
  without a pointer.
- **KB-D6**: zero RNG anywhere in the harness (static scan: no time/seed/
  random reads); all synthetic variation closed-form in the trial index.

## 7. Non-goals (frozen)

- The harness does NOT propose gate redesigns; it diagnoses. (The v2 fork
  crews own mechanisms.)
- The harness does NOT read truth at decision time; `jcorrect` is scoring
  metadata, never a probe input (probes use only `prog`, `conf`, `pred`,
  `meas`, `jcode`, `progF` — the white-box state).
- Python glue generates inputs; it never substitutes for a Zag probe.

## 8. Commit map

- This prereg: `senses/pam-rebuild/v2/diagnostics/PREREG_DIAG.md`
  (committed ALONE, this commit).
- Build outputs (later commit): `diagnose.zag`, `gen_case_record.py`,
  `case_r24_rk3.txt`, `expect_r24_rk3.txt`, substrate copies
  (`R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag` — byte-identical to
  the R2-4 sources, SHAs recorded), `DIAG_RUNLOG.md`,
  `DIAG_VERDICT_R24_RK3.md`, `DEEP_DIVE_METHOD.md`.
- Branch `tnn-native-lab`, via `commit_racefree.py`, TMPDIR set. No
  binaries, no `.zagd`.
