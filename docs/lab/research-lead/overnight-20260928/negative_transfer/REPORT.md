# REPORT: NEG-TRANSFER-1 (NT1)

## Verdict

**PASS** per the frozen verdict mapping (PREREG Section 8). All five kill
bars hold; every frozen numeric prediction matched exactly.

## Frozen results (3/3 byte-identical)

- Run digest: `e89c61c7f62ff50cf5146d85df34ef3ad4bcac88a536afd648479bc33972219d`
- Binary digest: `880d7ddb43444b1be125c87be37518d64190011d50b8e6ed63c5196ec39277ad`
- Source digest: `644014ee8f9f602fb5deff1eec28da793a12887b6258e58fa96208a935a3c383`

```
NT1 ML1 CTRLA ttc=2 acc=24
NT1 ML1 CTRLB ttc=2 pc=1 acc=24
NT1 ML1 SEQ ttcA=2 accA=24 ttcB=4 pcB=3 accB=24
NT1 ML1 RETEST c_vb=6 nc=6 u=12 forget=0 nevict=0 nalias=0 nentries=36
NT1 ML0 ABL ttcA=2 ttcB=4 pcB=3 accB=24
NT1 ML0 RETEST c_vb=6 nc=6 u=0 forget=12 nevict=0 nalias=12 nentries=24
NT1 K1=1 K2=1 K3=1 K4=1 K5=1
NT1 VERDICT=PASS
```

## Kill-bar evaluation

- K1 (isolation learnability): PASS. Both families learned in isolation to
  100% within 2 passes (TTC_A_ctrl=2, TTC_B_ctrl=2). No VOID.
- K2 (retention where B does not contradict): PASS. ML1 retest NC=6/6,
  U=12/12. The 12 A-only keys, never mentioned during B training, are
  fully intact.
- K3 (selective revision, not erasure): PASS. All 6 contradicted keys
  revised to the B value (c_vb=6/6); FORGET=0 across all 24 A keys. The
  learner changed exactly what the evidence contradicted and nothing else.
- K4 (forward negative transfer bounded): PASS. D = pcB_seq - pcB_ctrl =
  3 - 1 = 2 <= 6. Prior A evidence measurably resisted B on contradicted
  keys (2 extra passes of ref accumulation before ref > sup triggered
  revision), then resolved. Interference is real, finite, and overcome by
  the same generic rule -- no special unlearning step.
- K5 (discriminative validity): PASS. ML0 (identical update/read rules,
  overlapping address map) learned A (ttc=2) and B (ttc=4) but forgot all
  12 aliased U keys (u=0/12, forget=12, nalias=12). The apparatus detects
  fragility; ML1's pass is not vacuous.

## What this establishes

1. Selective retention EMERGES from entry-local error-driven evidence
   revision with no protection mechanism: the learner has no task labels,
   no freeze flags, no "don't forget" logic (grep audit clean). Retention
   of the untouched and the merely-agreed, plus revision of the
   contradicted, falls out of one symmetric update rule.
2. The fragility source is isolated to ADDRESSING, not the update rule:
   ML0 differs from ML1 only in the address map and shows localized
   catastrophic forgetting on exactly the aliased keys (12/12), while
   revising contradicted keys and retaining agreed keys normally.
3. Negative transfer is quantified in both directions: A->B interference
   costs exactly 2 extra passes on contradicted keys (K4); B->A
   interference is zero on non-contradicted knowledge (K2) under
   dedicated addressing, total on aliased knowledge under overlapping
   addressing (K5).

## Honest boundaries (from PREREG Section 10, unchanged)

- ML1/ML0 are minimal surrogates for the principle (entry-local evidence
  revision vs overlapping addressing), not TNN's production memory
  substrate. This PASS establishes the principle and a discriminative
  measurement apparatus, not that TNN-as-built is robust.
- Families are memorized key-value mappings; the battery measures
  retention/revision dynamics, not rule induction. No L2/L3 claim.
- No capacity pressure was exercised (nevict=0 both arms); the eviction
  rule is implemented but untested. Pressure-driven forgetting is the
  preregistered follow-up.
- Single contradiction magnitude; graded contradiction out of scope.

## Recommended follow-up (preregistered, PREREG Section 9)

Port the winning rule (entry-local evidence revision + dedicated
addressing) to the shared continuing-learner substrate, rerun A/B/A there,
and test under capacity pressure with rule-structured families.

## Provenance

- Prereg frozen alone: commit `0c9e063` (PREREG.md + NAMECHECK.md only),
  strictly before implementation.
- Implementation + results: this commit. Pure Zag, safebin-only PATH,
  pinned znc 2026.07.0-dev. Zero forbidden-executable invocations.
- Build: `znc nt_full.zag -o nt_bin`; 3/3 runs byte-identical (cmp).
- Commits local only, explicit pathspecs, never pushed.
