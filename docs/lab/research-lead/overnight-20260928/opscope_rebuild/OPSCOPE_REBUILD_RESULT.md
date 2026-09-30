# OPSCOPE REBUILD RESULT: R1-R4 with K=2

## Verdict: OPSCOPE-REBUILD-PASS

## Kill bars

- K1 PASS. Prereg committed as `1fd2f0752` when the rebuild directory
  contained only the prereg file (no implementation files existed).
  The implementation commit follows it in ancestry.
- K2 PASS. F1-F5 executed with per-item results below.
- K3 PASS. Pure Zag throughout: source authoring, build (znc),
  runs, byte checks (shell-only `check_no_dash.sh`), verification
  (md5sum, grep, diff, sha256sum), and committing (git). No Python
  at any stage, including scratch and verification. 3/3
  byte-identical runs (md5 767f289ef5732dde430c9f625c9b44a6), exit
  0, zero stderr bytes. No em or en dash bytes in any new file.

## Code change from the prior implementation

Exactly one line, verified by diff against
`operator_scope_impl/opscope_learner.zag` (commit `f01c6b69d`):

```
326c326
<             if(popcnt(get32(W,5808+w*16+8))>=3){
---
>             if(popcnt(get32(W,5808+w*16+8))>=2){
```

World and harness files are byte-identical to the prior
implementation. Strict-majority binarization (`c*2>o`) carried over
unchanged. Built binary: 122579 bytes (same size as the prior
build, consistent with a constant-only change).

## Falsifier results

| F | Bar | Result |
|---|-----|--------|
| F1 | T1 (109,110,111) 3/3 + white-box OPREC | PASS (3/3, whitebox=1) |
| F2 | T3 scope-shift (109,110,111) | PASS (3/3) |
| F3 | source audit, no word-specific branches | PASS (0/0/0 hits) |
| F4 | ablation strictly worse on T1 | PASS (t1_full=3 vs t1_abl=0) |
| F5 | >=16/20 and SIZE 3/3 | PASS (20/20, SIZE 3/3) |

Per-item frozen test (pred/tgt as feature masks), identical on all
3 runs:
- 100-102 DIRECT "tak grn cub": 3/3 pass
- 103-105 DIRECT "tak blu tri": 3/3 pass
- 106-108 SYN "tak grn sph": 3/3 pass
- 109-111 NEG "tak not grn": 3/3 pass (pred=1 {tak}, tgt=1 {tak})
- 112-114 REL "tak biger tri": 3/3 pass
- 115-117 SIZE "tak smal tri": 3/3 pass
- 118-119 3WAY "tak big grn bal": 2/2 pass

F4 detail: ablated copy (operator table emptied, records intact)
re-ran the 20 items at 17/20 vs full 20/20; T1 under ablation 0/3
vs full 3/3 (negdrop=3). The drop is strictly localized to the
negation items, as the bar requires.

## F3 verbatim audit (shell grep on the committed learner file)

```
$ grep -c "not" opscope_learner.zag
0
$ grep -ci "negat" opscope_learner.zag
0
$ grep -c "is_negator" opscope_learner.zag
0
```

Inspection note: the routing predicate (`find_op`, `learn_update`)
tests only `OPREC.trigger_form` (W+5616+k*24), a runtime-bound unit
id. No branch in `opscope_learner.zag` mentions any word identity.
The word table lives solely in the excluded world file.

## Discovery trace (mechanism evidence)

At CHECK seen=40, the candidate table reads:

```
 w epc reclen sup mtch div cs cb gate
 1 12  1      12  12   2   40 28 1
```

installed_now=1. The true trigger (w=1) passes eligibility,
support (12>=4), consistency (12/12>=0.75), the revised diversity
bar (div=2>=2), and the zero-parameter gate (40>28 strict).
OPREC installs with trigger_form=1, scope=REST_OF_UTTERANCE,
signature=DELETION, created_at=40. Further installs at checks
50,60,70,80,90,100 (re-grounding replay keeps one active operator
per check; the table shows 7 active entries at test time, all
trig=1/sig=DELETION).

This matches the revision's section 8 expectation exactly: the
mechanism outcome is OPREC installation with F1, F2, F4 evaluable.

## What the learner creates vs what is authored

Authored: spans, UNION combiner, OPREC structure, DELETION
signature, routing, all constants (including revised K=2), (U,T)
mapping, binarization rule. The learner creates: the operator
inventory (7 OPREC entries installed online at checks 40..100),
all record vectors, support counts, and the routing bindings. The
binding of trigger unit 1 to the DELETION signature was discovered
from residual events, not authored. Bounded L2; no L3 claim.

## State and determinism

State: 8400 bytes (records 5232, oprec 192, dstat 192, epstore
2400), same layout as the prior run. Determinism: 3/3 md5-identical
(767f289ef5732dde430c9f625c9b44a6), exit 0, zero stderr.

## Artifacts

- PREREG_OPSCOPE_REBUILD.md (prereg, commit 1fd2f0752)
- opscope_world.zag (frozen battery; byte-identical to prior)
- opscope_learner.zag (R1-R4; one-line K change)
- opscope_harness.zag (training/test/F1-F5; byte-identical to prior)
- opscope_bin (122579-byte native binary)
- build.err (compiler warnings only)
- run1.txt, run2.txt, run3.txt (byte-identical raw outputs)
- run1.err, run2.err, run3.err (empty)

## Commits

- 1fd2f0752 prereg (K1)
- (this result commit)
