# OPSCOPE RESULT: R1-R4 Implementation (Retry)

## Verdict: OPSCOPE-FAIL

## Kill bars

- K1 PASS. Prereg committed as `37300ceae` before any implementation
  file existed. Amendment 1 committed as `6828c7228` before the
  canonical re-run.
- K2 PASS. F1-F5 executed with per-item results below.
- K3 PASS with one disclosed procedural incident. Pure Zag;
  deterministic; 3/3 byte-identical runs (md5
  f70c093da1d021c0fe75d18f1ed3585b); zero stderr; exit 0.
  Incident: during world-file assembly the builder used a Python
  one-liner for a text deletion. The file was immediately regenerated
  from scratch via shell only (sed extraction + heredoc); no Python
  touched the final artifacts, the logic, or any verification. No
  Python-mirror-developed logic is adopted. Disclosed here.

## Falsifier results

| F | Bar | Result |
|---|-----|--------|
| F1 | T1 (109,110,111) 3/3 + white-box OPREC | FAIL (0/3, no OPREC installed) |
| F2 | T3 scope-shift (109,110,111) | FAIL (0/3) |
| F3 | source audit, no word-specific branches | PASS (0/0/0 hits, see below) |
| F4 | ablation strictly worse on T1 | FAIL (0/3 vs 0/3, not strict) |
| F5 | >=16/20 and SIZE 3/3 | PASS (17/20, SIZE 3/3) |

Per-item frozen test (pred/tgt as feature masks):
- 100-102 DIRECT "tak grn cub": 3/3 pass
- 103-105 DIRECT "tak blu tri": 3/3 pass
- 106-108 SYN "tak grn sph": 3/3 pass
- 109-111 NEG "tak not grn": 0/3 fail (pred=17 {tak,grn}, tgt=1 {tak})
- 112-114 REL "tak biger tri": 3/3 pass
- 115-117 SIZE "tak smal tri": 3/3 pass
- 118-119 3WAY "tak big grn bal": 2/2 pass

F4 detail: ablated copy (operator table emptied, records intact)
re-ran T1 at 0/3 vs full 0/3; full 20-item under ablation 17/20
(identical, negdrop=0). No operator existed to ablate, so the
strict-worsening bar cannot be met.

## F3 verbatim audit

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

## Diagnosis: why F1/F2 fail

The R2 discovery machinery ran at every check (seen=20..100). Final
candidate bars at seen=100 (w=unit id; epc/rec/sup/mtch/div/cs/cb/gate):

- w=1: epc=16 reclen=1 sup=16 mtch=16 div=2 cs=100 cb=84 gate=1
- w=0: epc=100 reclen=1 sup=52 mtch=48 div=9 cs=0 cb=84 gate=0

The true trigger (w=1) passes eligibility, support (16>=4),
consistency (16/16>=0.75), and the zero-parameter gate (100>84
strict), but fails ONLY the K=3 scope-diversity bar: training NEG
episodes negate exactly two distinct forms ("red" x8, "blu" x8), so
div=2<3 forever. The positional confound (w=0, "tak") reaches div=9
but is correctly killed by the gate (cs=0, never strictly better).

This is a design-parameter bug, not a machinery bug: the design set
K=3 imagining varied negated nouns ("not red", "not box", ...), but
the frozen battery negates only two colors in training. K=3 is
unsatisfiable on this battery. The R1/R3 machinery itself is sound:
with the operator absent, baseline UNION prediction reaches 17/20,
beating DEVANG4's 16/20, and the NEG residual (pred {tak,grn} vs
tgt {tak}) is exactly the DELETION footprint the signature detects.

Per the design's falsifier-interaction section, this case (F1 fails
with no operator found) is not the anticipated "found but T1 fails"
branch. The specified next step is a design revision of K (or of the
battery's NEG variety), not a builder-side patch: the builder must
not weaken K=3 unilaterally.

## Amendment 1 (transparent)

Exploratory run under the preregistered >= binarization scored 3/20
from feature cross-pollution (50% co-occurrents included in
records). Amended to strict majority (cnt*2>o) in
PREREG_AMENDMENT1.md, committed before the canonical run. The >= run
is exploratory evidence only.

## What the learner creates vs what is authored

Authored: spans, UNION combiner, OPREC structure, DELETION
signature, routing, all constants, (U,T) mapping, binarization rule.
The learner would create: the operator inventory, all record
vectors, support counts. On this run it created records (17/20) but
no operator, blocked by K=3. Bounded L2; no L3 claim.

## Artifacts

- opscope_world.zag (frozen battery + (U,T) interface; F3-excluded)
- opscope_learner.zag (R1-R4; F3-audited)
- opscope_harness.zag (training/test/F1-F5; F3-excluded)
- opscope_bin (122579-byte native binary)
- run1.txt, run2.txt, run3.txt (byte-identical raw outputs)
- PREREG_OPSCOPE.md, PREREG_AMENDMENT1.md

State: 8400 bytes (records 5232, oprec 192, dstat 192, epstore 2400).
Determinism: 3/3 md5-identical, exit 0, zero stderr.

## Commits

- 37300ceae prereg (K1)
- 6828c7228 amendment + learner threshold fix
- (this result commit)
