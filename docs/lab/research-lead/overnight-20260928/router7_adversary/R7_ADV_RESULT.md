# R7_ADV_RESULT: H-ROUTER7 Independent Red Team Report

**Date:** 2026-09-29
**Adversary:** H-ROUTER7 Red Team (independent)
**Target:** H-ROUTER7 SURVIVES (frozen prereg `34347580c`; builder result
in `981459ee3`)
**Adversary prereg:** `8f795a1aa` (PREREG_R7_ADV.md), frozen before any
attack code, build, or run. Commit order verified below.
**Stance:** the H-ROUTER7 claims were assumed false.

## Verdict: H-ROUTER7 DOWNGRADED (not killed)

The R1 total-table headline is falsified as stated. All four frozen
builder bars (K-R7-1 through K-R7-4) still pass, the R2 s1>=1 scope
extension holds against every evasion attempt, and the independent
rebuild reproduces the committed output byte-for-byte. The mechanism
implements its design exactly; what fails is the categorical form of
the C1 claim, plus a trace-transparency defect at capacity.

Concretely:

1. **Capacity defeat (exploratory variant V2).** A 40-mark curriculum
   driven entirely through the public `teach` interface induces 25
   ACTIVE FX_SET equality entries. The 25th hits the `rt_add` 24-rule
   cap (`TABLE OVERFLOW`), the R1 explicit-fallback append is dropped
   by the same guard, and `route3(RT,nrt,0,10,0)` returns **-1**.
   The prereg C1 text ("guarantees the compiled routing table is total
   by design: every feature triple routes to a declared task code;
   route3 never silently returns -1") is false as stated.

2. **Misleading trace at capacity.** Two emits fire for rules that were
   never added: the entry loop's `TABLE-RULE` emit prints stale
   `RT[nrt-1]` content after an overflow refusal, and the R1
   explicit-fallback emit fires unconditionally even when `rt_add`
   refused the fallback. The trace claims totality while the table is
   not total. The "loud emit" transparency the R1 prereg relies on is
   itself unreliable at capacity.

Narrowed C1 (what the evidence supports): the compiled table is total
iff fewer than 24 rules are compiled before the fallback append. At
capacity the overflow guard drops further entries and the explicit
fallback; route3 can return -1 for uncovered triples; the TABLE-RULE
and explicit-fallback trace emits are unreliable at capacity.

Transparency note on verdict weight: the **frozen** X-R7-1 (fixture OF)
FAILED; the defeat was demonstrated by **exploratory** variant V2
(fully documented, 3x byte-identical, reproducible from the committed
harness). The four-condition frozen kill criterion is not literally
met, because its condition (b) assumed the explicit-fallback line would
be absent on overflow; the code emits it unconditionally, which is
itself part of the finding. Details in section 4.

## 1. Claims under test

C1 (R1): total routing table by design; route3 never silently
returns -1 (explicit terminal `[any]->WITHHOLD` fallback appended iff
no all-ANY rule was compiled).

C2 (R2): single-segment (s1==1) learn marks are family-checked;
the s1>=2 scope restriction is removed.

C3: no regressions vs H-ROUTER6 (K-R7-3); deterministic (K-R7-4).

## 2. Method

Harness `r7_adv.zag` = lines 1..1799 of the committed
`router7_learn.zag` blob (everything before `fn main`), copied verbatim
and cmp-verified against the blob in `981459ee3`, plus an attack-only
`main()`. No mechanism edits. Fixtures are driven through `teach` /
`run_induction` / `compile_thresholds` / `build_table_rest` / `route3` /
audit functions only. Exploratory variant harness `r7_adv_v2.zag` uses
the same verified mechanism region.

Toolchain: pinned `znc 2026.07.0-dev (edition 2026)`. Every attack
binary was built 3x and run 3x; all runs byte-identical via cmp
(adversary runs and V2 runs). Binaries live in /tmp only; none
committed.

Pure Zag. No Python at any stage. Fixtures are hand-written Zag string
literals (one small `rep_seg` helper builds repeated-segment lines into
exactly-sized buffers). Shell was used only for build/run/grep/cmp/diff
/md5sum.

X-R7-3 used `git show` of the committed blobs; no worktree source.

## 3. Code facts established by read-only review (pre-execution)

F1. `RT` is `z_alloc(192)`; 8 bytes per rule; at most 24 compiled rules.
`rt_add` emits `TABLE OVERFLOW` and returns `nrt` unchanged when
`nrt>=24`. The R1 fallback append goes through `rt_add`.

F2. `build_table_rest` compiles ACTIVE equality entries with FX_SET on
var0 (up to 64 indexed, each via `rt_add` capped at 24).
`compile_thresholds` runs first (up to 4 rules, s0v in {1,2}).

F3. `route_features` sets `s1=nseg >= 1` for every non-empty line
(capped at 9); the empty line gives `s0=pk=0`. A learn mark with s0 in
{1,2} always has s1>=1, so the s1>=1 lower bound excludes no reachable
learn mark of a checked content type.

F4. Query anchors require `s0==0 && s1==1`; `qk` (s2) is computed only
for single-segment `>`-free lines, so multi-segment lines always have
s2=0.

## 4. X-R7-1: capacity vs the total-table invariant

### 4a. Frozen fixture OF: FAILS (attack fails, mechanism holds)

Fixture OF (frozen): fresh world, 36 teaches as TC_PL (PROC_LEARN), seq
1..36, no conflicts:

- v=1..9: v copies of `aa>bb` joined by `;` (features (1,v,0))
- v=1..9: v copies of `1,0,0>1,0` joined by `;` (features (2,v,0))
- v=1..9: v copies of `aab` joined by `;` (features (0,v,0); (0,1,1)
  for v=1)
- v=1..9: v copies of `ab>1,0` joined by `;` (features (3,v,0))

Hand-derived expectation (prereg): 36 distinct triples induce >=24
ACTIVE FX_SET entries; the 25th overflows; the root [any] stays
FX_UNRES; fallback dropped; probe -1.

Observed (R7_ADV_RAW.txt, 3x byte-identical): the induction merged all
36 same-task marks into ONE entry. Evidence:

```
THRESH-COMPILE s0=1: no clean threshold (nn=0)
THRESH-COMPILE s0=2: no clean threshold (nn=0)
TABLE-RULE [any]->PROC_LEARN (from H0)
X-R7-1 TABLE-SIZE 1
X-R7-1 HASANY01=1
X-R7-1 PROBE(0,10,0)=11
```

No `TABLE OVERFLOW`. The induced `[any]->PROC_LEARN` (H0, ACTIVE)
makes the table total without any fallback; the probe routes 11
through it. Kill criterion condition (a) (`TABLE OVERFLOW` present)
not met. **X-R7-1 (frozen) FAILS.** The induction's merge bias defeats
naive capacity flooding: agreement without counterevidence
generalizes to [any].

### 4b. Exploratory variant V1: no overflow (20 rules, total)

V1 (exploratory, not preregistered): 31 marks with interleaved tasks
per s0 block to resist merging and to three-task the threshold
compiler (W@1, PL@{2,4,6,8}, CL@{3,5,7,9} for s0=1; W@1, CL@{2,4,6,8},
PL@{3,5,7,9} for s0=2; W@1, PL@{2..9} for s0=3; plus 4 query marks).

Observed: 20 compiled rules, `HASANY01=1` (induced `[any]->PROC_LEARN`
H29 ACTIVE), probe (0,10,0)=11. Still total; no overflow. The s0=3
block was absorbed into general entries ([s0=1]->CAUS_LEARN,
[s0=2]->PROC_LEARN overgeneralizations kept below specific rules by
first-match ordering).

### 4c. Exploratory variant V2: CAPACITY DEFEAT (the finding)

V2 (exploratory, not preregistered): V1 plus an s0=0 merge-resistant
block (W@1 as `aab` -> (0,1,1); PL@{2,4,6,8}, CL@{3,5,7,9} at (0,v,0)).
40 marks, 37 distinct feature triples, all through `teach`.

Observed (R7_ADV_V2_RAW.txt, 3x byte-identical):

```
TABLE-RULE [s0=1]->CAUS_LEARN (from H27)          (24th real rule)
TABLE OVERFLOW                                    (25th entry dropped)
TABLE-RULE [s0=2]->PROC_LEARN (from H31)          (STALE: RT[23] reprinted)
TABLE OVERFLOW                                    (fallback append refused)
TABLE-RULE [any]->WITHHOLD (explicit fallback: no induced [any] rule; total-table invariant)
                                                  (PHANTOM: rule not added)
V2 TABLE-SIZE 24
V2 HASANY01=0
V2 PROBE(0,10,0)=-1
```

Reading:

- 24 real rules compiled; the 25th ACTIVE entry hit the `rt_add` cap:
  `TABLE OVERFLOW`, entry dropped.
- The entry loop's `TABLE-RULE` emit is unconditional after `rt_add`,
  so it printed stale `RT[23]` content labeled `(from H31)` for the
  dropped entry. The trace claims a rule that does not exist.
- `hasany==0` (no induced all-ANY rule), so the R1 fallback append was
  attempted at nrt=24 and refused by the same guard: second
  `TABLE OVERFLOW`.
- The R1 explicit-fallback emit is unconditional inside
  `if(hasany==0)`, so it fired anyway: the trace claims
  `[any]->WITHHOLD (explicit fallback ...)` was appended. It was not:
  `TABLE-SIZE 24`, `HASANY01=0`.
- `route3(RT,nrt,0,10,0)` returns **-1**: s1=10 is unreachable via
  teach, no compiled rule covers it (all rules use CK_EQ on s1 with
  values <=9, or constrain s0), and no all-ANY rule exists.

This is exactly the failure mode R1 was built to eliminate, reached
through the public curriculum interface. The compile-time
`TABLE OVERFLOW` emits do not change the per-probe return path: a
consumer calling route3 on an uncovered triple gets a silent -1.

Kill-criterion accounting (frozen): (a) TABLE OVERFLOW present: YES;
(b) no explicit-fallback line: NO (the line IS present, phantom);
(c) HASANY01=0: YES; (d) probe -1: YES. The criterion is not literally
met because (b)'s assumption was wrong; the wrong assumption is itself
a finding (phantom emit). The attack's question, "is there a case
where route3 still returns -1," is answered YES.

### 4d. X-R7-1 conclusion

Frozen X-R7-1: FAILS. Exploratory V2: demonstrates a reachable defeat
of C1 as stated, plus a trace-transparency defect. C1 must be narrowed
(see Verdict). Recommended repair for a follow-up: gate both
`TABLE-RULE` emits on actual insertion (compare nrt before/after
`rt_add`), and when the fallback append is refused, emit a loud
non-totality warning instead of the phantom fallback line (options:
raise the cap, evict lowest-specificity rules, or fail loudly).

## 5. X-R7-2: single-segment evasion attempts: FAILS (mechanism holds)

Fixture S1E (frozen): `run_induction(W,0)` (honest anchors: qk=1 PROC
n=2, qk=2 CAUS n=2), then `ab>cd` as TC_CL seq 19 (features (1,1,0);
family CAUS vs PROC anchor: swapped) and `9,9,9>9,8` as TC_PL seq 20
(features (2,1,0); family PROC vs CAUS anchor: swapped).

Observed (R7_ADV_RAW.txt, 3x byte-identical):

```
TASK-FAMILY-INCONSISTENCY: s0=1 learn mark #19 CAUS_LEARN (CAUS) vs qk=1 query anchor PROC; string-like learn/query families disagree.
TASK-FAMILY-INCONSISTENCY: s0=2 learn mark #20 PROC_LEARN (PROC) vs qk=2 query anchor CAUS; triple-like learn/query families disagree.
X-R7-2 TFAM=3 (want bit0|bit1 = 3)
```

Both swapped single-segment marks are caught (bits 0 and 1). Four
LAW-CHANGE lines also appear (the causal contest machinery reacting to
the swapped marks, as the builder's prereg anticipated); that is
separate machinery and does not affect this bar. Kill criterion (zero
INCONSISTENCY lines or (tfam&3)==0) not met. **X-R7-2 FAILS.** C2
holds for the evasion set. Reachability note (F3): s1==0 learn marks
with s0 in {1,2} are unreachable through `teach`, so the s1>=1 lower
bound leaves no reachable gap.

Fixture S1C (frozen, disclosed-boundary calibration): S1E plus `zzz`
as TC_CQ seq 19 (features (0,1,1); contests the qk=1 anchor) and
`ab>cd` as TC_CL seq 20. Observed: `ANCHOR-CONTESTED: qk=1 query marks
disagree on family; no anchor established (n=3); learn marks for this
content type unchecked`, then `task-family-check-partial`, then
`no-task-family-inconsistency`. The H-ROUTER6 disclosed boundary
(contested anchors leave learns unchecked, loudly) is unchanged by R2.
No deviation; recorded as a confirmed boundary.

## 6. X-R7-3: regression and integrity: FAILS (mechanism holds)

- Rebuilt `router7_learn.zag` from the committed blob in `981459ee3`
  with pinned znc; 3 runs byte-identical via cmp.
- Rebuilt output byte-identical to committed `ROUTER7_RAW_OUTPUT.txt`
  (cmp clean).
- Six frozen sections (honest, gamed, confined, swap, pollution-swap,
  single-side) diffed against committed `ROUTER6_RAW_OUTPUT.txt`:
  differences are exactly (i) the program banner line, (ii) six
  `learn-marks s1>=2:` to `learn-marks s1>=1:` label lines, (iii) the
  same scope-text update inside one still-firing
  SINGLE-FAMILY-ANOMALY line in the confined section (counts
  unchanged), (iv) the extended SUMMARY/VERDICT block covering the two
  new sections. No other differences.
- All bars PASS in the rebuilt output: K-R7-1
  `[any-rule=1 probe=10 want 1,10]`, K-R7-2 `[single-segment tfam=1
  want bit0]`, K-R6-1, K-R6-2, K-R5-1, K-R5-2a, K-R5-2b, K-R5-2c,
  K-R4-1 through K-R4-5, `H-ROUTER7 AUTOMATED BARS PASS`.

Kill criterion (any difference, any extra diff, any FAIL) not met.
**X-R7-3 FAILS.** No silent changes; deterministic.

## 7. X-R7-4: new boundaries from R1/R2

4a (no laundering through the fallback): reran the builder's F-FB
fixture verbatim (honest curriculum + `ab>1,0`->CL at (3,1,0)).
`audit_replay` still reports `REPLAY-MISMATCH #19 mark CAUS_LEARN
routed WITHHOLD`, `REPLAY 18/19`. The explicit fallback routes the
out-of-scope attack mark to WITHHOLD instead of -1, but the replay
audit still surfaces it. The fallback does not launder the mark.
Boundary confirmed; no finding.

4b (single-family scope delta): minimal curriculum (anchors
`hello`/`world` PQ, `1,0,0`/`0,0,0` CQ; `ab>cd` PL at (1,1,0) so s0=1
learns exist ONLY at s1==1; `5,5,5>5,4;6,6,6>6,5` CL at (2,2,0)).
Observed: `no-single-family-anomaly`, SFANOM=0, TFAM=0. Under
H-ROUTER6's s1>=2 scope this curriculum fires SINGLE-FAMILY-ANOMALY
(s0=1 has no learns at s1>=2 while s0=2 has); under R2's s1>=1 scope
it does not. Classification: false-positive fix per the R2 rationale
(the s1>=2 restriction had no principled basis for learn marks; s0=1
does have a learn, just single-segment), not a diagnostic regression.
The task-family machinery is unaffected (families consistent here;
TFAM=0 correct). Recorded as a confirmed behavior delta.

## 8. Classification

Bounded L2+ structural learning with provenance diagnostics
(unchanged from the builder). The capacity defeat does not promote or
demote the mechanism's learning class; it narrows a safety invariant.
Not L3.

## 9. Governance disclosures

D1. Pure Zag. No Python at any stage: fixtures are hand-written Zag
string literals; the only non-Zag tooling is the pinned znc build and
POSIX shell (grep/cmp/diff/md5sum). The H-ROUTER6 red team's Python
harness-edit violation is not repeated here.

D2. Prereg `8f795a1aa` was committed alone before any attack code,
build, or run. Attack harnesses were assembled only after the freeze.

D3. Only `router7_adversary/` paths are staged in the result commit.
No binaries committed (builds in /tmp/r7adv, /tmp/r7reg only). No
worktree mechanism files touched; the mechanism region was
cmp-verified against the committed blob, never edited.

D4. X-R7-1 V1 and V2 are exploratory (post-prereg) variants, labeled
as such throughout. They cannot retroactively satisfy the frozen
four-condition kill criterion; they are reported as demonstrated
evidence with full reproduction artifacts, and the verdict weights
them explicitly (see Verdict).

D5. No em dashes in loop docs (checked).

D6. No worker-count claims made; scheduler state was not needed for
this task.

## 10. Commit lineage and reproduction

- Adversary prereg: `8f795a1aa` (PREREG H-ROUTER7 red team FROZEN).
- Target prereg: `34347580c`; target implementation/result:
  `981459ee3` (blob verified byte-identical to the harnessed region).
- This result commit: (filled at commit time).
- `git merge-base --is-ancestor 8f795a1aa HEAD` verified before
  pushing the result (prereg strictly precedes implementation/attack).

Reproduction:

1. `git show 981459ee3:docs/lab/research-lead/overnight-20260928/router7_learn.zag | sed -n '1,1799p'` >
   mechanism region; cmp against the first 1799 lines of
   `router7_adversary/r7_adv.zag` (identical by construction).
2. Build with pinned `znc 2026.07.0-dev (edition 2026)`:
   `znc r7_adv.zag -o r7_adv` (3x), `./r7_adv` (3x); outputs
   byte-identical to `R7_ADV_RAW.txt` (md5
   d829533e8c2680f6e82a93e0e284adaf).
3. `znc r7_adv_v2.zag -o r7_adv_v2` (3x), `./r7_adv_v2` (3x);
   byte-identical to `R7_ADV_V2_RAW.txt` (md5
   8752a7e76cf7917077ec52b170f32193).
4. X-R7-3: `git show 981459ee3:.../router7_learn.zag`, build, run 3x,
   cmp against the committed `ROUTER7_RAW_OUTPUT.txt`; diff the six
   frozen sections against committed `ROUTER6_RAW_OUTPUT.txt` as
   described in section 6.

## 11. Open recommendations (not verdicts)

R1. For H-ROUTER8: gate the `TABLE-RULE` emit and the explicit-fallback
emit on actual insertion; on a refused fallback append, emit a loud
non-totality warning (and consider raising the cap or evicting
lowest-specificity rules).

R2. The narrowed C1 should replace the categorical headline in the
research paper and CANONICAL_STATE: total iff <24 rules before the
fallback append; trace emits unreliable at capacity.

R3. V2's `[s0=1]->CAUS_LEARN` / `[s0=2]->PROC_LEARN` overgeneralized
entries (kept harmless only by first-match ordering beneath specific
rules) are worth a dedicated red-team pass on merge soundness.
