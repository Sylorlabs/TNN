# Preregistration: Q4 R3 Reuse Beyond the Installed Perfect Terminal

Status: FROZEN. This prereg's first commit strictly precedes any R3
implementation or run. Revival plan: 290f0d061, section 3. R3 question
(plan 3.1): does the kept structure improve later cognition when it is
NOT an installed perfect terminal?

## 1. Fixed kept component (plan 3.2)

- Artifact: the committed 7-op D from commit 5f56cc491 (Q4 F-PARCOND
  BUILD-PASS), kept node 1105, 7 operator nodes, 32/32 on evidence,
  64/64 true. No Phase-1 re-run is performed; R3 is independent of
  R1/R4 seeds.
- Behavior signature: D = (x1 & (x2^x3)) | ((x1^1) & (x2&x3)) over
  all 64 input combos. 64-bit signature (lo = bits 0..31, hi = bits
  32..63): lo = 0x68686868 = 1751672936, hi = 0x68686868 = 1751672936.
  Derived from the F-PARCOND truth table in ADV_SPEC.md (b4e9b6a14),
  which the kept D matched 64/64. The implementation recomputes the
  signature from the sealed D definition at runtime and asserts
  equality with these frozen constants (DSEAL check, section 5).

AMENDMENT 1 (before any arm ran): the decimal constant was
transcribed as 1751477352 in the original freeze; the correct
decimal for 0x68686868 is 1751672936 (verified via shell printf).
The first binary run voided itself on DSEAL (no arm executed), which
is the gate working as designed. This amendment corrects the
decimal only; the hex, the truth table, and all arms are unchanged.
- The artifact is correct (64/64 true) and non-minimal (a 5-op
  solution and a 4-op analytic form exist per the alternative
  explanation attack, 73d9637a2).

## 2. D_10 construction procedure (Arm 1 component)

- D_10 = the 7-op D padded to 10 ops with identity wrappers:
  w1 = (D AND 1), w2 = (w1 XOR 0), w3 = (w2 AND 1). Total 7 + 3 = 10
  operator nodes.
- The wrappers are behavioral identities: sig(w1) = sig(D) & ALL1 =
  sig(D); sig(w2) = sig(w1) ^ 0 = sig(D); sig(w3) = sig(w2) & ALL1 =
  sig(D). The implementation mechanically verifies sig(w3) == sig(D)
  (D10_OK check, section 5).
- The installed atomic terminal carries the verified D signature.
  The 10-op count is provenance metadata (documented here); the beam
  sees an atomic terminal, exactly as in the original Phase 2.

## 3. Arms

### Arm 1 (R3a, non-minimal robustness; plan 3.3)

- Component: D_10 installed as atomic terminal (verified signature).
- Sealed target (fam 7): C' = D_10 XOR X4, computed as
  ((((d & 1) ^ 0) & 1) ^ x4) where d is the sealed F-PARCOND D.
  Behaviorally identical to the original Phase 2 target; the
  wrappers are written out to mirror the artifact construction.
- Contrast: A-REUSE (D_10 terminal installed) vs A-SCRATCH (no
  library). Same evidence protocol as Q4 Phase 2: 8 passive samples
  (Y6-bias protocol, section 4) + up to 24 disagreement IVs.
- Frozen seed: 710101 for both A-REUSE and A-SCRATCH (shared seed =
  identical passive evidence; the contrast isolates the library).
- Bar: reuse final_true = 64/64 AND reuse_iv * 2 <= scratch_iv.
  Rationale (plan 3.3): robustness control; expected to pass if the
  Phase 2 reuse mechanism is sound and does not depend on the
  component being the learner's own sleek discovery.

### Arm 2 (R3-embed, non-trivial composition; plan 3.3)

- Component: the 7-op D installed as atomic terminal (verified
  signature). D is EMBEDDED as a subexpression, not top-level.
- Observables: Y1..Y6 = input bits 0..5. D is computed on
  (Y1, Y2, Y3) = bits 0, 1, 2 (fixed by the committed artifact's
  signature). The plan's E = (D AND Y1) OR ((NOT D) AND Y2) is
  realized as E = (D AND Y4) OR ((NOT D) AND Y5): the two embedding
  observables are the frozen Y4 = bit 3 and Y5 = bit 4, the
  observables not used by D. Y6 = bit 5 is the decoy/confound,
  biased in the passive protocol (fresh arrangement relative to
  target E).
- Sealed target (fam 8): E = (d & y4) | ((d^1) & y5), d the sealed
  F-PARCOND D on bits 0..2.
- Contrast: A-REUSE vs A-SCRATCH. Same evidence protocol: 8 passive
  + up to 24 IVs.
- Frozen seed: 710202 for both A-REUSE and A-SCRATCH.
- Bar: reuse final_true = 64/64 AND reuse_iv * 2 <= scratch_iv AND
  HAS_D = 1, where HAS_D is the structural check that the reuse
  solution tree contains the installed D terminal (id 8, verified
  signature) as a subexpression (iterative subtree walk; section 5).
  Rationale (plan 3.3): reuse must cover discovering the embedding,
  a genuinely compositional task beyond one-step XOR.

### Arm 3 (R3b, changed surface; plan 3.3)

- DEFERRED. The structured-library extension (subtree grafting and
  remapping) has not been preregistered or built. Per plan 3.3 and
  3.4, Arm 3 is marked DEFERRED, not failed, and does not block
  R3-PASS.

## 4. Frozen mechanism and protocol

- Learner: the Q4 beam mechanism from q4_parcond.zag (5f56cc491),
  unchanged: beam width 32, score = acc*10000 - 200*opc, tie-break
  (score desc, opc asc, node asc), top-8 disagreement IV policy
  (select_iv), 8-sample passive protocol with bit-5 bias (6 biased +
  2 random), 24-round IV budget, hit criterion true accuracy
  >= 61/64, keep bars not re-run (no Phase 1).
- Terminals: Y1..Y6 (bits 0..5), const0, const1 (8 terminals);
  A-REUSE adds the D terminal (id 8) with the verified signature.
- Falsifiers:
  - F-R3-THIN (plan 3.4): Arm 2 reuse solution lacks D as a
    subexpression (HAS_D = 0). Reported as re-derivation, not
    reuse; the arm fails the reuse bar.
  - F-R3-SEAL (plan 3.4): Phase-2 hidden parameters (Arm 2
    Y-layout, decoy arrangement, seeds beyond the frozen values)
    leak to the learner side before scoring completes. Voids the
    affected arm. The sealed targets live in the harness-side
    sealed() function; the learner side observes only samples.
- Determinism: 3/3 byte-identical runs (md5), zero stderr.
- Purity: pure Zag at every stage (implementation, compilation,
  execution, verification). Zero Python anywhere, including byte
  checks (shell grep only). Zero em/en dash bytes (shell-verified
  before commit).

## 5. Mechanical checks (emitted by the binary)

- DSEAL: 1 iff runtime-computed D signature == frozen (lo, hi).
  Gates both arms; DSEAL = 0 voids the run (harness defect).
- D10_OK: 1 iff identity-wrapped signature == D signature.
  Documents the Arm 1 padding claim mechanically.
- HAS_D (Arm 2 reuse only): 1 iff the final reuse solution tree
  contains terminal id 8 with the verified D signature.
- Per arm-run: hit_iv (IVs to reach >= 61/64 true, 24 = never),
  final_true (/64), and the ratio test reuse_iv*2 <= scratch_iv.

## 6. Verdict

- R3-PASS: Arm 1 meets its bar AND Arm 2 meets its bar (with
  HAS_D = 1); Arm 3 deferred.
- R3-FAIL: Arm 1 or Arm 2 fails its bar.
- Commit order: this prereg is committed before any q4_r3.zag
  implementation work. The implementation commit will cite this
  prereg hash.

Builder label: PREREG (frozen, awaiting implementation).
