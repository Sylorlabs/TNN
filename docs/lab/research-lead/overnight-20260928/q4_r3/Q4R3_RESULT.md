# Q4 R3 Result: Arms 1-2

Date: 2026-09-30. Worker: Q4-R3 Implementer.
Prereg: c17fe8cda (frozen before implementation), amendment 1: 5e5e2add6
(before any arm ran; corrected D signature decimal, no arm executed
before the amendment).
Implementation: q4_r3.zag (pure Zag, compiled with znc 2026.07.0-dev).
Revival plan: 290f0d061, section 3. Arm 3: DEFERRED (plan 3.3, 3.4).

## Verdict: R3-FAIL

Arm 1 PASSES its bar. Arm 2 FAILS its bar (reuse reaches 53/64, not
64/64). R3-PASS requires Arms 1 AND 2 (plan 3.4). The revival
conjunction (plan section 7) therefore fails; the honest bounded-L2
claim from Q4_CLAIM_REVISION.md stands unchanged. The localized
weakness is defined in "Failure localization" below.

## Kill bars

- K1 (prereg frozen before implementation): PASS. Prereg c17fe8cda
  committed before q4_r3.zag was written. Amendment 1 (5e5e2add6)
  corrected a decimal transcription error and was committed before
  any arm ran; the first binary self-voided on DSEAL with zero arms
  executed. The scored implementation matches the amended prereg.
- K2 (Arms 1-2 complete): PASS. All four arm-runs executed:
  A1-REUSE, A1-SCRATCH, A2-REUSE, A2-SCRATCH.
- K3 (pure Zag, deterministic): PASS. Zag at every stage. 3/3
  byte-identical runs (md5 7ed09fda269b59cdbbf75e0df720661c), zero
  stderr on all runs. Zero Python anywhere (byte checks via shell
  grep only). Zero em/en dash bytes (shell-verified before commit).

## Mechanical checks

- DSEAL 1: runtime-recomputed D signature == frozen (lo = hi =
  0x68686868 = 1751672936). The kept-D artifact (5f56cc491, node
  1105) is correctly installed.
- D10_OK 1: identity-wrapped signature == D signature. The Arm 1
  padding claim (7-op D padded to 10 ops with (x AND 1), (x XOR 0)
  wrappers) is mechanically verified as behavioral identity.

## Arm 1 (R3a, non-minimal robustness): PASS

Target C' = D_10 XOR X4 (fam 7). Seed 710101 (shared).

- A1-REUSE (D_10 terminal installed): hit_iv = 0, final_true = 64/64.
- A1-SCRATCH (no library): hit_iv = 24 (never reached), final_true
  = 56/64.
- Ratio: 0 * 2 <= 24. Bar (64/64 AND reuse_iv * 2 <= scratch_iv):
  MET. A1-PASS = 1.

The reuse advantage does not depend on the component being the
learner's own sleek discovery; the padded non-minimal artifact
reuses identically. This robustness control passes as expected.

## Arm 2 (R3-embed, non-trivial composition): FAIL

Target E = (D AND Y4) OR ((NOT D) AND Y5) (fam 8), D embedded as a
subexpression. Seed 710202 (shared).

- A2-REUSE (D terminal installed): hit_iv = 24 (never reached
  61/64), final_true = 53/64, HAS_D = 1.
- A2-SCRATCH (no library): hit_iv = 24, final_true = 50/64.
- Bar (64/64 AND reuse_iv * 2 <= scratch_iv AND HAS_D = 1): NOT MET.
  A2-PASS = 0. F-R3-THIN did NOT fire (HAS_D = 1; the solution does
  contain D, so this is not re-derivation).

## Failure localization (diagnostic, non-governing)

A separate diagnostic binary (/tmp, not committed, same frozen seed)
replayed A2-REUSE with per-round beam-top reporting, plus a manual
sanity build of E from raw signatures:

- E_SANITY 64/64: the sealed target E is correct and the installed D
  signature is the right component. No harness defect. F-R3-SEAL did
  not fire.
- Beam trajectory: from r=6 onward the beam's top node is a 3-op
  expression containing D that fits the growing evidence (up to
  29/32) but generalizes to only 53/64 true. The true 4-op E was
  never generated in any of the 25 beam extensions.

Mechanism: the 200/opc simplicity tax creates a trap. The 3-op
overfitter scores ~9400 at full evidence fit (10000 - 600) versus
9200 for the true 4-op E (10000 - 800). The greedy top-32 beam locks
onto the simpler wrong expression early; subsequent generations
build combinations of overfitters rather than the clean
AND(D,Y4) / NOT D / AND(~D,Y5) chain, so E is never expressed. The
IV policy cannot recover because the top-8 hypotheses are all
overfitter variants.

This is a real mechanism limitation, not a component or target
defect: the frozen Q4 beam's greedy filtering plus strong
simplicity bias defeats compositional reuse when a simpler
evidence-fitting expression exists. It is the same simplicity tax
that helped Phase 1 find the minimal D, now working against the
true compositional form.

## Honest scope

- R3 tested reuse of the committed D artifact. Arm 1 confirms the
  original Phase 2 reuse is robust to a non-minimal (padded)
  component. Arm 2 shows the reuse does NOT extend to discovering a
  non-trivial embedding under the current beam/search.
- Per revival plan section 7, R3-FAIL means the Q4 discovery revival
  fails. R1, R2, and R4 are independent experiments and may still
  run for their own information value, but they cannot revive the
  conjunction.
- The defined next target: a search mechanism that does not let a
  simpler evidence-fitting expression permanently block the true
  compositional form (beam diversity, tax annealing, or explicit
  compositional construction operators).

## Files

- PREREG_Q4R3.md: frozen prereg + amendment 1 (c17fe8cda,
  5e5e2add6)
- q4_r3.zag: implementation (pure Zag)
- q4_r3_bin: compiled binary (untracked, not committed)
- build.err: compiler log (warnings only)
- Q4R3_RAW_1/2/3.txt: 3/3 byte-identical raw outputs
  (md5 7ed09fda269b59cdbbf75e0df720661c)
- Q4R3_RAW_1/2/3.err: empty stderr logs
- Q4R3_RESULT.md: this file

Raw output (all three runs identical):

Q4-R3
DSEAL 1 dlo=1751672936 dhi=1751672936
D10_OK 1
A1-REUSE hit_iv=0 final_true=64/64
A1-SCRATCH hit_iv=24 final_true=56/64
A1 REUSE_IV 0 true=64/64
A1 SCRATCH_IV 24 true=56/64
A1-PASS 1
A2-REUSE hit_iv=24 final_true=53/64
A2-SCRATCH hit_iv=24 final_true=50/64
A2 REUSE_IV 24 true=53/64 HAS_D=1
A2 SCRATCH_IV 24 true=50/64
A2-PASS 0
R3-PASS 0
DONE
