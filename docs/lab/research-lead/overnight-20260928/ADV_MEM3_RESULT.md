# ADV_MEM3_RESULT.md -- H-MEM3 independent red-team report

Adversary: H-MEM3 independent red team (depth-1 subagent).
Date: 2026-09-29. Timezone: America/Los_Angeles.
Toolchain: /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
  (znc 2026.07.0-dev (edition 2026)).

## Verdict

H-MEM3 is DOWNGRADED. The five frozen bars stand (X-M3-3 regression SURVIVES,
X-M3-4 source audit SURVIVES), but the R1 causal claim is narrowed by a
confirmed attack. X-M3-1 CONFIRMED on both sub-probes: the CHURN-PREVENTED
verdict is selected-policy-scoped in a way that misleads, and probation
demonstrably causes harm. X-M3-2 CONFIRMED: the adversarial future defeats
replay selection while passing the independence check, confirming the
builder's disclosed limitation is load-bearing. The mechanism is not killed;
no frozen bar changes truth value. What changes is the interpretation:
the "genuine causal evidence" gloss on R1 is retracted to a scoped verdict
with a demonstrated gap, and a concrete probation-harm case is now on record.

Probe scorecard:
  X-M3-1a (counterfactual scope gap): CONFIRMED -> DOWNGRADE of R1 claim.
  X-M3-1b (probation harm): CONFIRMED -> concrete harm case recorded.
  X-M3-2a (adversarial future): CONFIRMED -> BOUNDARY (disclosed limit
    confirmed load-bearing).
  X-M3-2b (DIST-DIFFERS low bar): CONFIRMED -> informational.
  X-M3-3 (regression vs 5/5 frozen bars): SURVIVES.
  X-M3-4 (source audit): SURVIVES.

## Target and commit lineage

  Builder preregistration: PREREG_MEM3.md at commit d00461bff.
  Builder implementation and result: mem3_learn.zag and MEM3_RESULT.md at
    commit 903a2c16c ("H-MEM3 SURVIVES (5/5 bars)").
  Frozen builder output MD5: 486aadc1b838abbe5e474a0c97a7fb38.
  Adversary preregistration: PREREG_ADV_MEM3.md at commit 532c34dbf,
    committed strictly before the harness and before any frozen execution
    (verified: 532c34dbf is an ancestor of 36ec018e0).
  Adversary harness and raw evidence: mem3_adv.zag and ADV_MEM3_EVIDENCE.txt
    at commit 36ec018e0.
  This report: ADV_MEM3_RESULT.md (this file), committed after the above.
  Branch: tnn-native-lab. All commits local; no push authorized or attempted.

## Method

Preregistration preceded implementation, which preceded execution, which
preceded this report; each step is a separate local commit in that order.
Pure Zag throughout: no Python in fixture design, harness, build, execution,
or analysis. Two exploratory scratch runs in /tmp preceded the preregistration
to validate that the candidate fixtures reach the intended mechanism states;
they are not evidence, were not committed, and no verdict rests on them.
Every number below comes from the frozen harness (adversarial main committed
at 36ec018e0) built against the mechanism extracted from the frozen builder
commit 903a2c16c (lines 1-352, everything before "fn main" at line 353;
working tree verified byte-identical to the commit for that path), or from
the X-M3-3 rebuild of the committed source. The harness is deterministic:
the RANDOM menu policy is deterministic (k-th eligible slot,
k=(ev*5+1)%neligible), no RNG is used, all fixtures are fixed literal
streams. Raw output is preserved verbatim in ADV_MEM3_EVIDENCE.txt.

## X-M3-1: counterfactual honesty and probation harm

### What was attacked

R1's claim, as written in MEM3_RESULT.md, is that the churn counterfactual is
"genuine causal evidence": the ev2 CHURN-PREVENTED:1 verdict "correctly
attributes proc9's survival to probation" and the ev1 :0 verdict is "honest
(probation changed nothing for the selected policy)". The red team attacked
two gaps: (a) the verdict compares the selected policy's protected vs
unprotected victim but never recomputes the WINNER under no probation, so a
reader's natural reading of ":0" ("probation changed nothing overall") can be
false; (b) age-based probation can protect a useless newcomer and force the
eviction of a useful procedure, i.e. probation can cause harm by the
mechanism's own metric.

### Fixture (frozen in prereg)

learn procs 0..7; A_old (17 queries: 0x4, 1x4, 2x2, 3x2, 4x2, 5x2, 7x1);
T (20 queries: 6,6, 2,2, 3,3, 4,4, 5, 2,2,2, 3,3,3, 4,4, 5,5,5);
pressure(ev=0, newpid=8); Qb (9 queries: 6,6,6, 0,0, 1,1,1,2); then
measurements at ev=1 followed by the real pressure(ev=1, newpid=9).

### Raw results (frozen harness output, verbatim values)

At ev=0: all five policies tie at replay cost 0, so the documented LFU-first
tie-break selects LFU; LFU evicts slot7 (proc7, uses=1, lastq=17); proc8 is
stored at slot7 with prot_until=47. The ev0 verdict reads CHURN-PREVENTED:0
(protected and unprotected victims coincide at slot7).

At ev=1, pre-pressure measurements:
  bestp1 (protected winner)   = FIFO (policy 2)
  bestp0 (unprotected winner) = LFU  (policy 0)
  -> the winner FLIPS under no probation.
  pv3 (selected policy protected victim)   = slot0
  uv  (selected policy unprotected victim) = slot0
  -> the selected policy's victims coincide.
  v1 (actual eviction with probation)    = slot0
  v0 (eviction without probation)       = slot7
  -> the actual eviction changes. Slot7 holds proc8, the protected newcomer:
     without probation the winner (LFU) evicts slot7, i.e. churns proc8.
  c_prot (replay cost of the eviction with probation)    = 2
  c_unprot (replay cost of the eviction without probation) = 0
  uses of proc8 (newcomer) = 0 (never queried after learning)
  uses of proc0 (evicted)  = 6 (queried twice in Qb)

The real pressure(ev=1) then prints, verbatim:
  "selected: FIFO cost=2 STRICT"
  "evict slot0 proc0 uses=6 lastq=42"
  "[churn counterfactual] selected=FIFO protected-victim=slot0(proc0) unprotected-victim=slot0(proc0)"
  "CHURN-PREVENTED:0 (probation changed nothing for the selected policy)"
  "stored proc9 at slot0 prot_until=56"

Every preregistered expected value held (bestp1=2, bestp0=0, pv3=0, uv=0,
v1=0, v0=7, c_prot=2, c_unprot=0, uses_new=0, uses_old=6). X-M3-1a CONFIRMED.
c_prot > c_unprot with uses_new < uses_old. X-M3-1b CONFIRMED.

### Causal interpretation (precise)

The verdict's literal sentence, "probation changed nothing for the selected
policy", is TRUE: FIFO's protected and unprotected victims are both slot0.
The mechanism computes exactly what the preregistration says it computes,
and the print does not lie about that comparison.

But the verdict's natural reading is false at the outcome level. Probation
changed the winner from LFU to FIFO (protection removed slot7 from LFU's
eligible set, which changed every policy's victim table and therefore the
argmin), and the winner change moved the eviction from slot7 to slot0.
Without probation, LFU would have evicted slot7, which is exactly where the
probation-shielded newcomer proc8 sits. Probation is therefore the but-for
cause of proc8's survival in a state where the mechanism prints
CHURN-PREVENTED:0. The counterfactual answers "would the selected policy
have evicted a different slot without protection" while the reader hears
"did probation matter". Those are different questions, and the fixture
separates them.

The harm is equally concrete and is measured in the mechanism's own
currency. With probation, the mechanism evicts proc0 (uses=6, queried in the
window) at a window-replay cost of 2. Without probation, it would evict
proc8 (uses=0, never queried after learning) at a cost of 0. Age-based
probation shielded a useless newcomer and sacrificed a queried procedure,
making the eviction strictly worse (cost 0 became cost 2). This is the
failure mode the builder disclosed abstractly as "probation is age-based
rather than merit-based"; it is now a demonstrated case with exact numbers.

### Verdict mapping

X-M3-1 CONFIRMED downgrades the R1 causal claim. The frozen K-M3-1 bar still
passes (the selected-policy counterfactual values on the builder's streams
are unchanged and correct). The mechanism is not killed. What is retracted
is the "genuine causal evidence" interpretation: the verdict is honestly
scoped to the selected policy's victim comparison, it does not establish
that probation was causally inert overall, and probation can be both the
but-for cause of a newcomer's survival (while the verdict reads 0) and the
cause of a strictly worse eviction. Any future H-MEM revision that keeps a
churn verdict must either recompute the winner under no probation (a full
counterfactual) or label the verdict as selected-policy-scoped.

## X-M3-2: adversarial futures

### X-M3-2a: adversarial future targeting the evicted procedure

The builder's A2 pre-ev0 state was replicated exactly (learn 0..7, AA 33
queries, AW 20 queries). select_win(ev=0, win=20) returned LFU (policy 0),
matching the builder's A2 ev0 selection. The selected policy's victim was
slot5 holding proc5. The adversarial future F-ADV was built WITHOUT
hardcoding: 20 copies of the selected policy's victim proc id (proc5),
computed at runtime via victim()/st_pid().

Results:
  dist_differs(F-ADV vs the W=20 window) = 1 (passes the independence check)
  fut_score2 returned 0: "K-M3-2 FAIL (A2 F-ADV: selected not min)"
  per-policy misses on F-ADV: LFU=20, LRU=0, FIFO=0, LIFO=0, RANDOM=0
  n_tying_min=4 of 5
  -> the selected policy is the UNIQUELY WORST policy (20 misses vs 0 for
     every other policy) on a future that passes DIST-DIFFERS.

X-M3-2a CONFIRMED. Verdict mapping: BOUNDARY. This confirms the builder's own
disclosed limitation ("an adversarial future targeting the evicted procedure
defeats replay-based selection") is load-bearing rather than hypothetical.
It does not kill K-M3-2, whose bar is explicitly non-adversarial, but the
report records that the "validates against future queries" claim does not
survive adversarial futures: the selection procedure is defeated by a future
that the mechanism's own independence check accepts.

### X-M3-2b: the DIST-DIFFERS check is a low bar

F-NEAR was constructed as the builder's AW window with a single query
flipped (AW[0] from 6 to 5). dist_differs(F-NEAR)=1 (passes); dist_differs on
the identical window=0 (correctly rejects). X-M3-2b CONFIRMED (informational).
A one-query difference passes the independence check, so "each future passed
DIST-DIFFERS" is weak evidence of independence, and it is the context in
which X-M3-2a's DIST-DIFFERS pass must be read: the check screens for gross
distributional identity, not for adversarial intent. Note also that
dist_differs compares frequency vectors, so it is order-insensitive by
construction; a same-multiset-different-order future would read DIST-SAME.

## X-M3-3: regression against all 5/5 frozen H-MEM3 bars

The committed source at 903a2c16c was rebuilt with the pinned toolchain and
run three times. Results:
  3/3 runs byte-identical (cmp clean both pairs).
  MD5 of output: 486aadc1b838abbe5e474a0c97a7fb38, exactly the frozen hash.
  "K-M3-1 PASS" lines: 2 (ev1, ev2).
  "K-M3-2 PASS" lines: 6 (all six frozen futures).
  "K-M2-3 PASS" lines: 1 ("K-M2-3 PASS: 5 strict selections"; this is the
    retained label for the K-M3-3 strictness bar, documented in the source).
  "K-M3-4 PASS" lines: 1.
  "ALL BARS PASS" lines: 1.
  "FAIL" lines: 0.
  n_tying_min=1 of 5 on all six futures, so the selected policy was the
  unique minimum on all six: MEM3_RESULT.md's prose ("unique minimum on all
  six frozen futures") is accurate against the raw output.

X-M3-3: SURVIVES. Two prereg label corrections are recorded (the
preregistration wrote "K-M3-3 PASS" and "ALL CHECKS PASSED" from memory; the
frozen source prints "K-M2-3 PASS" and "ALL BARS PASS"). The substantive
criterion, all five bars passing with the overall pass verdict, is met; the
corrections are documentation of the prereg, not findings against the target.

## X-M3-4: source audit

Audited mem3_learn.zag at 903a2c16c (mechanism = lines 1-352; harness = fn
main), including a full diff against mem2_learn.zag (400 diff lines; every
delta matches one of the five documented repairs R1-R5; no undocumented
mechanism change).

  (a) R1: pressure() computes pv3/uv from the SELECTED policy's victims and
      the verdict logic matches the prereg, including the pv3<0 fallback-path
      branch. Correct.
  (b) R2: select_win() falls back to the unprotected argmin and emits
      FALLBACK-ALL-PROTECTED when the protected victim is <0; pressure()
      mirrors the fallback, sets the ST fallback flag, and uses up=0
      consistently in the printed table and in is_strict_up. Correct.
  (c) R3: dist_differs() compares per-proc frequency vectors of the future vs
      the W=win window with the lo<0 clamp; all call sites pass win=20.
      Correct; order-insensitivity is inherent (scope note, not a bug).
  (d) R4: fut_score2() gates on DIST-DIFFERS first, then applies the ties-min
      bar (get32(M,sel*4)==minm); n_tying_min is computed and printed.
      Correct.
  (e) R5: the flat round-robin boundary fixture is present, prints its
      SCOPE-NOTE, and is not wired to any bar. Correct.
  (f) Tie handling: argmin_pol uses strict <, so LFU (earliest in the menu)
      wins replay-cost ties. The K-M3-4 fallback expectation (unprotected LFU
      by tie-break on zero queries) follows from this rule. Correct and
      consistent with the regression output.
  (g) No fixture-specific answer literals in mechanism code: no hardcoded
      procedure ids, slot numbers, or expected miss counts outside fn main.
      All expectations live in the harness (the bars), as preregistered.
  (h) replay_cost() returns 999999 for v<0; victim() returns -1 only when no
      eligible slot exists; the all-protected path is exercised by the K-M3-4
      fixture and cannot crash. Correct.
  (i) RESULT prose accuracy: "unique minimum on all six" verified against
      the raw n_tying_min lines. Accurate.

One cosmetic wart (not a correctness bug): in the fallback path pressure()
prints "protected-victim=slot-1" (the raw -1) before the pv3<0 branch prints
the fallback-path message. The branch taken and the verdict are correct.

X-M3-4: SURVIVES. No correctness bug found.

## Overall H-MEM3 disposition

H-MEM3 is DOWNGRADED, not killed. Concretely:

  - The 5/5 frozen bars stand as executed: regression reproduces them
    byte-identically and the source audit finds the mechanism correct.
  - The R1 "genuine causal evidence" claim is narrowed to a
    selected-policy-scoped verdict with a demonstrated scope gap
    (X-M3-1a). The verdict print is literally true; its natural reading is
    not.
  - A demonstrated probation-harm case is on record: age-based probation
    shielded a never-queried newcomer and forced eviction of a queried
    procedure, turning a cost-0 eviction into a cost-2 eviction (X-M3-1b).
  - The adversarial-future limitation is confirmed load-bearing: a future
    that passes DIST-DIFFERS makes the selected policy uniquely worst
    (X-M3-2a). The independence check itself is a low bar (X-M3-2b).

H-MEM3 remains a bounded L2 experience-driven menu-selection mechanism with
honest provenance on its bars. It does not establish L3; nothing in this
red-team arc changes that classification in either direction.

## Boundaries and untested observations

  - The red team did not test whether a merit-based probation (protect by
    uses or recency instead of age) avoids the X-M3-1b harm case. That would
    be a new mechanism (H-MEM4 territory), not a red-team probe.
  - The red team did not run the full winner-recomputation counterfactual on
    the builder's own streams, so it is unknown whether the scope gap changes
    any frozen K-M3-1 verdict. The gap is demonstrated on the adversarial
    fixture only.
  - Adversarial futures were run at win=20 only; the 20/25/30 band claim was
    not attacked.
  - Source-level observation, not probed: st_query (lines 93-105 at
    903a2c16c) records a query only when the procedure is resident
    (st_find >= 0); queries for absent procedures are silently discarded (no
    Q entry, no sequence advance). The replay window therefore cannot contain
    evidence about procedures that were never stored, and selection cannot
    learn from misses of absent procedures. This is a real structural
    property of the mechanism, listed here as untested rather than as a
    finding.
  - H-MEM3 remains unintegrated into the unified learner (builder-disclosed).

## Governance disclosures

  - Pure Zag: no Python was used anywhere in this arc (fixtures, harness,
    build, execution, analysis, evidence assembly).
  - Preregistration (532c34dbf) strictly precedes the harness commit
    (36ec018e0), which strictly precedes this report; verified by ancestry
    check. Two exploratory /tmp scratch runs preceded the preregistration
    for fixture feasibility only; they are disclosed here and are not
    evidence.
  - All commits are local on tnn-native-lab; no push authorized or attempted.
  - Only adversary-owned paths were staged (PREREG_ADV_MEM3.md,
    mem3_adv.zag, ADV_MEM3_EVIDENCE.txt, ADV_MEM3_RESULT.md). Concurrent
    workers' files (intent_learn.zag, unified_learn.zag, IU4 files, paper
    edits, and others) were not touched; broad git add was never used.
  - No em dashes appear in this loop documentation.
  - Negative evidence preserved: no probe refuted; the X-M3-3 prereg label
    corrections and the fallback-path cosmetic wart are reported rather than
    hidden. If the frozen harness had failed to reproduce the exploratory
    expectations, the verdict would have followed the frozen harness.
  - Determinism: znc 2026.07.0-dev; harness fully deterministic; regression
    3/3 byte-identical with md5 486aadc1b838abbe5e474a0c97a7fb38.

## What the parent should do next

  - Record H-MEM3 as DOWNGRADED (R1 claim narrowed; bars intact) in the
    canonical state and the paper's status tables, with lineage to this
    report (ADV_MEM3_RESULT.md), the prereg (532c34dbf), the harness and
    evidence (36ec018e0), and the builder commits (d00461bff, 903a2c16c).
  - The X-M3-1b harm case and the X-M3-1a scope gap are the natural seeds
    for H-MEM4: merit-based probation, or a full winner-recomputation
    counterfactual, would be new preregistered hypotheses, not patches to
    H-MEM3's frozen bars (which must not be retroactively altered).
