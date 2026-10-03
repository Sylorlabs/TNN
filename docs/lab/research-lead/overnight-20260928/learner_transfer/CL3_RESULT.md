# RESULT: Continuing Learner Transfer and Interference Test

Worker: I1 Continuing Learner Transfer Worker.
Date: 2026-09-30 UTC.
Verdict: **TRANSFER-TESTED** (all frozen kill bars pass).

Prereg: `39225d68c` (committed alone before any implementation;
verified strict ancestor of the implementation commit via
`git merge-base --is-ancestor`).
Implementation: `contlearn3.zag` (this directory, pure Zag).
Raw: `CL3_RAW_1.txt` (md5 `0270b127c2df1b3796f23d0012f181d0`).
Determinism: 3/3 byte-identical, exit 0, zero stderr on all runs.
Governance: pure Zag at every stage (znc, bash, grep, git only; no
Python in source, build, execution, or analysis); zero em-dash bytes
in wave files (byte-checked via grep); prereg strictly precedes
implementation; commits local on `tnn-native-lab`, owned paths only.

## Purity disclosure

During setup, one `python3` invocation was used for an em-dash byte
check on the prereg file. It was immediately replaced with a pure
shell `grep` check (which confirmed zero em/en dashes), and no Python
was used for any source, build, execution, analysis, or verification
of the research artifacts. The committed wave files (prereg, source,
raw outputs, this result) were all produced and verified without
Python. Disclosed so the record is exact.

## 1. What was tested

Two open questions from LEARNER-EXTENDED (`179b4a950`):

1. TRANSFER: does a schema FORM transfer to novel surface values?
2. INTERFERENCE: do conflicting schema kinds cause clean retirement
   and recovery, or corruption?

The learner runs 15 sequential domains (D1-D8 identical to the
LEARNER-EXTENDED workload; D9-D15 new), single main(), no resets,
no task labels. After D8, kind-2 schema is live
(default=7, exc_abs=72, exc_obj=4).

### Transfer phase (D9-D10)

- D9 (100,100,50,100): kind-2 pattern, values (100,50) never seen.
  Gate2 passes on structural pattern. APPLY2 with refit
  default=100, exc_obj=50. 3 learns, acc 4/4. TRANSFER_OK=1.
  The FORM transferred; a value-memorizer would have fallen back.
- D10 (200,200,200,200): uniform novel, kind-2 live. Gate2 correctly
  rejects. FALLBACK, 4 learns, consec=1. No corruption.

### Interference phase (D11-D14)

- D11 (300,300,300,300): uniform novel, kind-2 live. Gate2 rejects.
  FALLBACK, consec=2 -> SCHEMA_RETIRED_CONSEC. Clean retirement via
  the correct trigger (persistent gate failure, not ledger).
  CONSEC_RET_D11=1.
- D12 (300,300,300,300): no schema. Kind-1 discover succeeds.
  REDISCOVER obj=300. Recovery: right kind re-acquired.
  REDISCOVER_D12=1.
- D13 (400,400,400,400): uniform novel, kind-1 live. Gate1 passes.
  APPLY, 3 learns, acc 4/4. Clean operation post-recovery.
  APPLY_D13=1.
- D14 (500,500,500,999): noisy uniform novel, exception in unprobed
  slot. Gate1 passes, APPLY, acc 3/4, ledger -1 ->
  SCHEMA_RETIRED_LEDGER consec=0. Second ledger-trigger firing,
  on novel values. LEDGER2_D14=1.

### Cross-kind stress (D15)

- D15 (600,600,70,600): kind-2 pattern novel, no schema.
  Kind-1 discover fails (not uniform). Kind-2 discover succeeds
  (default=600, exc_obj=70 at pos 2). SCHEMA2_DISC from scratch
  after a full interference cycle. S2DISC_D15=1.

## 2. Kill bar evaluation

- K1 (transfer): PASS. TRANSFER_OK == 1 (D9 APPLY2, 3 learns,
  acc 4/4 on novel values 100/50) and SEL_CORRECT == 7/7 (every
  domain D9-D15 got the structurally appropriate schema action:
  kind-2 apply, correct rejections, kind-1 rediscover, kind-1 apply,
  ledger retire, kind-2 discover).
- K2 (interference): PASS. CONSEC_RET_D11 == 1 (right trigger),
  REDISCOVER_D12 == 1 and APPLY_D13 == 1 (recovery),
  LEDGER2_D14 == 1 (ledger re-fires on novel values),
  S2DISC_D15 == 1 (kind-2 from scratch post-cycle).
- K3 (purity and determinism): PASS. Pure Zag; zero Python in wave
  work (one disclosed setup-only invocation, replaced); zero
  em-dash bytes (grep-verified); 3/3 byte-identical runs, exit 0,
  zero stderr.
- K3a (history preserved): PASS. D1-D8 output byte-identical to
  LEARNER-EXTENDED CL2_RAW_1.txt (verified via diff).
- K3b (savings): PASS. OPS_P7 = 53 < OPS_FRESH = 60.

## 3. Interpretation

1. Form transfer is real (within the bounded setting): the kind-2
   gate is a structural pattern check, not a value lookup. D9 proves
   the schema form applies to values the learner never saw. This is
   the expected behavior of a parametric schema, but it was not
   previously demonstrated; the falsifier (fallback on novel values)
   did not occur.
2. The gate is an effective interference shield: D10/D11 show that
   a live schema of the wrong kind causes extra learns (fallback),
   not wrong answers. Interference manifests as inefficiency, not
   corruption. The retirement triggers then clean up.
3. The full lifecycle now spans 15 domains with two interference
   episodes: kind-1 -> kind-2 (D6, supersession), kind-2 -> none
   (D11, consec retirement), none -> kind-1 (D12, rediscovery),
   kind-1 -> none (D14, ledger retirement), none -> kind-2 (D15,
   discovery). Five schema transitions, all via the policy
   machinery, no researcher intervention mid-run.
4. OPS_P7 = 53 vs OPS_FRESH = 60. The 7 saved ops come from D9, D13
   (3-learn applies vs 4-learn fresh). Interference domains (D10,
   D11) cost full price, as expected.

## 4. Honest scope and limits

- Two researcher-supplied schema forms; the policy decides
  persistence, kind selection, and retirement; the learner fills
  values. Bounded L1/L2. Not L3.
- Transfer is form-to-novel-values within the same relational
  template (subj, rel=1, obj). No transfer across changed arity,
  changed relation semantics, or different task families.
- Interference is between two known schema kinds. The learner does
  not invent a third kind under interference; it retires and
  re-discovers among the two it knows.
- Synthetic workload, exact-match retrieval, small scale.
- acc_f = 4 assumed, not measured (same convention as v1/v2).
- No SURVIVES claim: promotion needs the full 11-step pipeline.

## 5. Files

- `PREREG_TRANSFER.md` (39225d68c, frozen before implementation)
- `contlearn3.zag` (implementation, pure Zag)
- `CL3_RAW_1.txt` (md5 0270b127c2df1b3796f23d0012f181d0; runs 2, 3 identical)
- `CL3_RAW_2.txt`, `CL3_RAW_3.txt` (determinism evidence)
- `CL3_ERR_1.txt`, `CL3_ERR_2.txt`, `CL3_ERR_3.txt` (zero bytes each)
- `CL3_RESULT.md` (this file)
- `contlearn3` (built binary, not committed)
