# ADV_EXEC_RECORD: RT-HPIREV2 sealed adversarial execution (wave-20261001-2321pdt)

Independent adversary: RT-HPIREV2. The six ADV worlds were frozen in
ADV_SEAL.md (original seal 8b86b27d2, committed alone before any
adversarial executor source, binary, or transcript existed;
transparent erratum amendment 1c40232af correcting three
hand-transcription errors in the hash listing, with 30/30
sha256sum -c verification; no world file created, modified, or
tuned after the original seal; no execution preceded the amendment).

## Frozen mechanism binding

The claim under test is the frozen revision procedure (machinery
lines 1-606 of proc_revise2.zag at 847a8f10f). Note on the task's
"run the FROZEN lane binary": the lane binary s8_exec_bin
(aee1b6f2..., hash-verified in Part 1) hardcodes its five fixtures
in main and accepts only a family selector (A2/B1/B2/C2/D2); it
cannot be pointed at new world files. The adversarial executor
rt_adv_exec_bin therefore embeds the frozen machinery
byte-verbatim (prefix sha256
8d2b16ab31184758b2b724e19cb1fa9f96d5ff008a0674b6c95c1da8e227f712,
verified identical to the lane's record) plus a new staging main,
exactly the architecture the lane itself used for s8_exec.zag.
Binary sha256:
da58510e0a20d1a2956dc7556dfd5546870cd8e269b945d5a0d01b884f5e1e23
(100891 bytes). Cognition source delta = 0: no machinery line was
altered; only staging, prechecks, and scoring were added. No new
semantic cases, modes, bridges, routers, or handlers.

## Pre-execution verification

- Seal hashes: 30/30 sha256sum -c OK against ADV_SEAL.md
  (after the erratum amendment; the check that caught the three
  transcription errors is documented in ADV_SEAL.md).
- Transcription fidelity: per world, the binary's emitted STAGE
  lines diffed byte-exact against adv_sealed/ TW+FW+RW files:
  6/6 EXACT.
- Determinism: 18 runs (6 worlds x 3), all exit 0, all stderr
  files 0 bytes, per-world stdout 3/3 byte-identical:
  - S1: 6bbb3c341e6b3873f29729db8b2845f47b355bad530eef5943f5bd69f070ddcb
  - S2: 633c0878733673c97b669bc53d134c2e3bf994f07653c284996b5d1b0d2b7ace
  - S3: 8a468124f4afea538d632b36534d39be030a8ad88b2cfc0a6ec76fde64df7576
  - S4: 7be01e25eeabc8bc3f342cab66ba3c7f2641785fc6fb70818fe804f26fb03959
  - M1: 70cab434c64a6b6f85abcab964a39e79ea57e8dc6b0644ca430d4a59faaa29bd
  - M2: 00d821ee3e703eaebbccbbe1c4001db3b4a6003e0207bdf186f6fa9513e5c9d7
- Prechecks: V0/V1a-d/V2/V3 all PASS on all six worlds; no world
  voided. Measured values match the pre-freeze predictions exactly
  (S1: V0=608 DIAG (0,81) ALT=2 evals=6; S2: V0=0 DIAG (0,81)
  ALT=608 evals=8; S3: V0=3 DIAG (0,81) ALT=608 evals=8;
  S4: V0=38 DIAG (0,120) ALT=2 evals=6; M1: V0=38 DIAG (0,81)
  ALT=2 evals=6; M2: V0=38 DIAG (0,81) ALT=2 evals=6).

## Per-world results (run1 values; runs 2-3 byte-identical)

S1 (novel base: reversal index map 608; consequent repeat-input[0]):
- W1 fails_total=0 (5/5 EW correct). revision_evals=6 (<=25).
  reuse_correct=1, zero new revision lines after W3.
  Adversarial bar A-S1: PASS. The bound generalizes to the novel
  base program.

S2 (base identity; consequent reversal 608; FW length 6):
- W1 fails_total=0. revision_evals=8 (<=25). reuse_correct=1,
  zero new revision lines after W3.
  Adversarial bar A-S2: PASS. The bound generalizes to a
  non-trivial consequent and longer candidate list.

S3 (base repeat-input[1]; consequent reversal 608):
- W1 fails_total=0. revision_evals=8 (<=25). reuse_correct=1,
  zero new revision lines after W3.
  Adversarial bar A-S3: PASS.

S4 (RANK-BIAS BREAKER; true conflict (2,66), diagnosed (0,120)):
- W1 fails_total=1: `PREDICT p!Br -> rrrr [MISMATCH want pppp]`.
  The mechanism built IF(byte-equality(0,120), alt, v_old) and
  applied v_old to the held-out RW pair, whose true rule fires
  alt. revision_evals=6. W3: COUNTEREXAMPLE_DETECTED(p!Br),
  reuse_correct=0, zero new DIAGNOSIS/PRIMITIVE-CONSTRUCTED/
  VERSION lines after W3.
  Adversarial prediction CONFIRMED: the mechanism FAILS a valid
  single-conflict world whose true trigger is not the rank-1
  diagnosis. Note the failure is loud, not silent: W1 reports the
  failure and the W3 probe flags it. What breaks is the
  "revises correctly on every single-conflict world" half of the
  narrowed claim, not the "never silent" half.

M1 (MASKED SECOND CONFLICT; RW carries both conflicts):
- W1 fails_total=0 (5/5 EW correct). revision_evals=6.
  reuse_correct=1. The transcript's only COUNTEREXAMPLE_DETECTED
  is the expected FW presentation (V2); zero detection lines at
  or after W3; zero new revision lines after W3.
  Adversarial prediction CONFIRMED: silent success claim. The
  true world contains an uncovered second conflict (byte 66 at
  position 2 with no byte 81 at position 0, e.g. input "x!Bz",
  is mispredicted by the learned rule), yet the run reports
  success and flags nothing.

M2 (PROBED SECOND CONFLICT; RW carries only conflict 2):
- W1 fails_total=1: `PREDICT p!Br -> rrrr [MISMATCH want !!!!]`.
  W3: COUNTEREXAMPLE_DETECTED(p!Br), reuse_correct=0, zero new
  DIAGNOSIS/PRIMITIVE-CONSTRUCTED/VERSION lines after W3.
  Adversarial prediction CONFIRMED: explicit trip, mirroring the
  lane's K-SC-B S1-S3 conjuncts on a materially different layout.

## Cost accounting (machine-greppable, run1 values)

w_first_fit_tw: S1=608 S2=0 S3=3 S4=38 M1=38 M2=38
w_b1w_enumerated: 1055 (all worlds)
w_revision_evals: S1=6 S2=8 S3=8 S4=6 M1=6 M2=6
w_fails_total: S1=0 S2=0 S3=0 S4=1 M1=0 M2=1
w_reuse_correct: S1=1 S2=1 S3=1 S4=0 M1=1 M2=0
w_reuse_new_revision_lines: 0 (all 18 runs)
w_diag: S1=(0,81) S2=(0,81) S3=(0,81) S4=(0,120) M1=(0,81) M2=(0,81)
w_alt_first_fit: S1=2 S2=608 S3=608 S4=2 M1=2 M2=2
binary_bytes: rt_adv_exec_bin=100891
cognition_source_delta: 0
new_semantic_cases: 0
new_modes: 0
new_bridges: 0
new_routers: 0
new_handlers: 0

## Purity

Pure Zag at every stage. Executables invoked: safebin tools only
(bash, sha256sum, cmp, grep, sed, awk, sort, uniq, wc, head, cat,
znc, cp). `which python3` and `which python` print nothing under
the safebin PATH (NAMECHECK.md Step 0). No other interpreter or
compiler invoked. No em-dash or en-dash bytes in new docs
(byte-checked before commit).

No em-dashes or en-dashes appear in this file.
