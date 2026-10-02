# RESULT: Continuing Learner Extension (Noise + Schema Kind 2)

Worker: I1 Continuing Learner Integration Worker (follow-up).
Date: 2026-09-30 UTC.
Verdict: **LEARNER-EXTENDED** (all frozen kill bars pass).

Prereg: `2f9eddc5e` (committed alone before any implementation;
verified strict ancestor of the implementation commit via
`git merge-base --is-ancestor`).
Implementation: `contlearn2.zag` (this directory, pure Zag).
Raw: `CL2_RAW_1.txt` (md5 `bd91c6fec609dbf2078d40ab71711eab`).
Determinism: 3/3 byte-identical, exit 0, zero stderr on all runs.
Governance: pure Zag at every stage (znc, bash, grep, git only; no
Python); zero em-dash bytes in wave files; prereg strictly precedes
implementation; commits local on `tnn-native-lab`, owned paths only.

## 1. What was extended

Two gaps from INTEGRATION-PROTOTYPED (`9844fb753`) are closed:

1. **Noise exercises the ledger trigger.** Domain D4 is
   (6,6,6,1): the default holds for the 3 gate probes, the exception
   sits in the unprobed slot. The gate passes, the schema applies,
   the schema path scores 3/4 against the assumed fresh 4/4, the
   ledger goes -1, and the schema retires via the LEDGER trigger
   with consec = 0. Marker: `SCHEMA_RETIRED_LEDGER consec=0`.
   This is the first time the accuracy-ledger retirement trigger
   fires in any P7 run.

2. **Second schema kind: default + single exception.** Form
   (rel R, default D, exc_abs E, exc_obj O). Queries with no instance
   return O when subj == E, else D. The exception position is refit
   per domain from the 3 probes (exactly two agree, one differs);
   the unprobed slot is assumed to follow the default (disclosed
   inductive bias). Discovery installs kind 2 when exactly one of
   four instances differs, superseding a live kind-1 schema (new
   incarnation: consec and ledger reset; supersession counted).

Observed output (frozen binary, 3/3 identical):

```
SCHEMA_DISC rel=1 obj=4
DOM 2 GATE1=1 / APPLY dom=2 obj=2 learns=3 acc=4
DOM 3 GATE1=1 / APPLY dom=3 obj=0 learns=3 acc=4
DOM 4 GATE1=1 / APPLY dom=4 obj=6 learns=3 acc=3
SCHEMA_RETIRED_LEDGER consec=0
REDISCOVER rel=1 obj=5
DOM 6 GATE1=0 / FALLBACK dom=6 learns=4
SCHEMA2_DISC rel=1 default=3 excabs=62 excobj=9
DOM 7 GATE2=1 / APPLY2 dom=7 default=7 excpos=2 excobj=4 learns=3 acc=4
DOM 8 GATE2=0 / FALLBACK dom=8 learns=4
OPS_P7 28 / OPS_FRESH 32
LEDGER 0 / APPLIES 4 / RETIRED_LEDGER 1
S2DISC 1 / S2APP 1 / SUPERSEDED 1
K1 1 / K2 1 / K3A 1 / K3B 1
VERDICT LEARNER-EXTENDED
```

## 2. Kill bar evaluation

- K1 (ledger trigger exercised): PASS. RETIRED_LEDGER == 1 and the
  D4 marker shows consec=0, proving the ledger (not the
  consecutive-rejection counter) caused the retirement.
- K2 (second schema kind works): PASS. S2DISC == 1 (kind-2
  discovered at D6, superseding kind-1) and S2APP == 1 (kind-2
  applied at D7 with 4/4 accuracy, 3 learns vs 4 fresh).
- K3 (purity and determinism): PASS. Pure Zag at every stage; zero
  Python invocations; zero em-dash bytes (byte-checked); 3/3
  byte-identical runs, exit 0, zero stderr.
- K3a (kind-1 discovery): PASS. DISCOVERED >= 1 (D1 and D5).
- K3b (savings): PASS. OPS_P7 = 28 < OPS_FRESH = 32.

## 3. Interpretation

1. The P7 retirement machinery now has both triggers verified in
   live runs: consecutive-rejection (v1, D7/D8) and accuracy-ledger
   (this wave, D4). The two triggers discriminate correctly: the
   ledger fires when the schema's form still passes the gate but
   loses on unprobed queries; the rejection counter fires when the
   gate itself fails repeatedly.
2. Schema-kind supersession works: kind-1 (uniform default) hands
   off to kind-2 (default + exception) when the world stops being
   uniform but keeps a one-exception structure. The refit machinery
   carries over: default, exception position, and exception value
   are all re-estimated per domain from probes.
3. The full lifecycle now spans two schema kinds in one persistent
   run: discover kind-1, apply x3, ledger-retire under noise,
   rediscover kind-1, supersede to kind-2, apply kind-2, survive a
   mixed domain without spurious retirement. No resets, no task
   labels.

## 4. Honest scope and limits

- Two schema kinds, both researcher-supplied forms; the policy
  decides persistence and kind selection, the learner fills values.
  Bounded L1/L2. Not L3.
- Synthetic workload, exact-match retrieval, small scale (8 domains,
  4 slots).
- The unprobed-slot-follows-default assumption in kind-2 is a
  disclosed inductive bias; a domain violating it would show up as
  a ledger loss on the next noisy domain, which is exactly what
  the D4 mechanism now detects.
- acc_f = 4 is assumed, not measured (same convention as v1); the
  ledger is schema-minus-assumed-fresh, not schema-minus-measured.
- No transfer across changed surface representations; no LLM/human
  comparison; no claim beyond LEARNER-EXTENDED.
- No SURVIVES claim: promotion needs the full 11-step pipeline.

## 5. Files

- `PREREG_CONTLEARN2.md` (2f9eddc5e, frozen before implementation)
- `contlearn2.zag` (implementation, pure Zag)
- `CL2_RAW_1.txt` (md5 bd91c6fec609dbf2078d40ab71711eab; runs 2, 3 identical)
- `CL2_RESULT.md` (this file)
