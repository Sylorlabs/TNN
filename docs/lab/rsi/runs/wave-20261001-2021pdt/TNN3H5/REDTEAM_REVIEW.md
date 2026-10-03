# REDTEAM REVIEW: H5 ADVANCES verdict, second opinion

Lane TNN3H5, wave-20261001-2021pdt. Reviewer: TNN3H5-REDTEAM (independent;
no shared state with builder, implementer, or adversary workers).
Method: read-only analysis. Re-verified SHA-256 hashes (base
a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd;
tnn3_h5.bin 344ac89fb338ddbf46bea6be4c526d99410ea643278ab91fb06d76b7e33c4eb7;
both match the lane records). Read-only re-execution of committed sealed
binaries: w_r1.bin 3/3 runs hash
8d6ee6d85de33c9753b4eb1dae7b367596034ccc82925d1677a5fb5c481e8706,
matching the adversary's recorded KB-D1 hash exactly. Confirmed
empirically from the committed run logs: C1S bridge-query=100,
C2S bridge-query=900 (S1). No new builds, no new implementation, no
forbidden executables. Documentation rule observed: no em-dashes.

## VERDICT: DISSENT

The ADVANCES verdict does not stand. The named bar is **KB-B2**: under
the only operationalization consistent with the frozen prereg, it FAILS
on committed sealed evidence. The design flaw is the adversary's
fact-key operationalization of KB-B2, which (a) contradicts the prereg's
own TNN-2 baseline sentence, (b) is justified by a factually false
claim about the 1421pdt M3-W2 probe placement, and (c) renders the bar
non-discriminating (the unmodified TNN-2 baseline passes it too). Per
PREREG_H5.md section 10 ("Any single bar failing KILLS H5 for this
wave"), H5 is KILLED for this wave, not advanced. The R-family results
are genuine and stand as evidence, but they do not carry the wave
verdict under the frozen conjunctive rule. Details are attack by attack
below; the KB-B2 finding is the centerpiece (Attack 2B and Attack 5C).

What this dissent does NOT dispute: KB-W1/KB-B1 (guide supersession,
genuine), KB-W2 (MAP CON edges, real white-box), KB-R1, KB-G1, KB-D1,
KB-P1, the seal integrity, or the adversary's transparency (S1-S4 were
documented honestly). No bad faith is alleged; the false 1421pdt claim
may be misrecollection, but it is load-bearing for the
operationalization choice and must be named.

---

## Attack 1: Knowledge vs architecture (where is the learner-owned part?)

**Finding: the transition WRITE is generic; the transition TRIGGERS are
researcher-written per-type scans over learner-accumulated state. The
prereg's "driven by learner-maintained standing" clause is not
implemented, by the prereg's own admission. Bound, not kill.**

Code facts (tnn3_h5.zag, read directly):

- `supersede` (line 146) is 4 lines: `if(is_superseded(W,n)==0)
  {link_edge(W,n,3,n,0);}`. Uses only COMPARE and LINK. One function,
  called for UNCERT nodes, guides, MAPs, and facts. The edge-write is
  genuinely generic: three pre-existing special cases (ev_observe's
  inline fact edge, contradict_map's MAP-only dead path, t2_revise_graph
  as MAP-only patch operator) were folded into it or deleted. Net -22
  cognition lines. This part of the claim survives.
- The DECISION of what to supersede is not generic. Three separate
  researcher-written scans select targets:
  1. `resolve_uncertainty` (lines 792-818, 27 lines): scans for tag-30
     UNCERT nodes matching (s,r), then walks POLICY_ROOT type-10 edges
     and applies a guide-class predicate (tag 1, field24==-999, type-1
     edge to a tag-30 node). Guide-specific logic.
  2. `revise_on_contradict` (lines 687-704): scans tag-20 MAPs for DEP
     (type-1) edges to the contradicted fact. MAP-specific logic.
  3. `ev_observe` contradiction branch (lines 819-841): supersedes the
     activated fact node. Fact-specific logic.
- The trigger rule is fixed and content-blind by explicit ruling (Q2):
  "any OBSERVE on (s,r) with a pending UNCERT(s,r) resolves it, whether
  the observe confirms or contradicts." The learner decides nothing;
  the rule fires deterministically on a fixed pattern.

What is learner-owned: the STATE the scans operate over. Which UNCERT
nodes are pending (created by the learner's own misses via
miss_inquire), which MAPs carry DEP edges to which facts (created by the
learner's own trial-loop promotions), and which facts were contradicted
are all products of the learner's experience history. The sealed
evidence shows the firing is selective to that state, not
indiscriminate: R1's never-resolved control guide stays live with no
CON edge (run log: "R1 guide-live=1 (expect 1: never-resolved
control)"); R2's wrong-key observe resolves nothing (world code asserts
`sw_guide_con(W)!=0` -> FAIL; run shows DONE-OK). So the mechanism is:
researcher-fixed trigger rules over learner-accumulated structural
state. That is experience-triggered lifecycle, and the R-family
behavioral delta (ev_act 30 -> 0) is real.

But PREREG_H5.md section 1 hypothesizes the transition as "driven by
learner-maintained standing rather than researcher-written per-type
handlers", while section 3.8 explicitly disclaims standing machinery
("No standing machinery is connected (map_standing stays dormant). No
trigger counting is added (evidence-weighted triggers are H6/H11
territory, explicitly not claimed here).") The hypothesis sentence
overclaims relative to the specified and tested mechanism. The honest
characterization of what the sealed battery evidences: one generic
protected edge-write, fired by researcher-written per-type trigger
scans over learner-accumulated state. The "standing-driven" half is
H6/H11 territory and is not evidenced here. This bounds the
"generic transition" claim; it does not overturn any bar.

---

## Attack 2: Metric gaming (degenerate policies)

**Finding: two degenerates probed. Indiscriminate supersession is ruled
out by committed pre-run world assertions (not by the frozen bars
alone). Recency echo is flagged by the adversary (S2) and confirmed.
The serious gaming flaw is KB-B2's operationalization (2B below).**

Attack 2A: always-supersede (every node on every event). Ruled out by a
frozen bar: KB-R1 requires 12/12 retention probes correct and the
retention world contains interference with no contradictions; blanket
fact supersession would destroy retention. PASS 12/12 with zero MAP-CON
edges observed rules this out. Clean.

Attack 2B: selective-indiscriminate (supersede ALL guides on ANY
observe, supersede MAPs and facts on contradiction). This degenerate
PASSES ALL NINE FROZEN BARS as written:
- KB-W1 (>= 6 guide CON edges): R1 would show 5 (4 resolved + control),
  R2 4, total 9 >= 6. PASS.
- KB-B1 (8/8 zeros): PASS. KB-W2/KB-B2/KB-B3: contradiction path
  intact. PASS.
- KB-R1: the retention probes query facts and MAP keys, never guides;
  the one unrelated observe would kill two unrelated guides
  behaviorally invisibly. 12/12 PASS; zero MAP-CON edges PASS.
- KB-G1/D1/P1 unaffected.

What rules 2B out is NOT in the frozen bars. It is in the
adversary-committed world drivers (SHA-256 recorded pre-run, so sealed
evidence, not post-hoc): world_r1.zag asserts exactly 4 guide-CON edges
(`if(gc!=4)` -> "R1 KB-W1 FAIL") and exactly 1 live guide
(`if(gl!=1)` -> "R1 control-live FAIL"); world_r2.zag asserts the
wrong-key observe produces 0 guide CON edges and 4 live guides
("R2 wrongkey-CON FAIL" / "R2 wrongkey-live FAIL"). Both worlds printed
DONE-OK. So the degenerate is excluded by committed sealed evidence,
and the verdict does not secretly rest on it. But the calibration gap
is real: the frozen bars alone underdetermine selectivity. The exact
counts and the control/wrong-key checks should have been frozen bars
(KB-W1 already gestures at the falsifiable prediction; a "selectivity"
bar would have closed it). Recommendation for the next prereg, not a
verdict-overturning flaw: the evidence exists and was committed before
the run.

Attack 2C: recency echo on KB-B2 (S2). Confirmed and sharpened: the
adversary notes the fact-key query's expected value equals the most
recent observation. The white-box KB-W2 carries the causal weight, and
NC-2 (behavioral pass with zero white-box edges -> FAIL) is the guard.
NC-2 did not fire (8 MAP-CON deltas observed). However, see the central
finding below: on the fact key, the MAP path is not on the query route
at all (activate reads tag-1 facts only; the trial loop builds fresh
graphs and never consults MAPs), so KB-W2's causal link to KB-B2's
behavioral pass is asserted, not demonstrated, on the probed key. The
S2 caveat understates the problem.

---

## Central finding: KB-B2's operationalization is unfaithful to the frozen prereg

The frozen bar (PREREG_H5.md section 5):

> KB-B2 (behavioral, M3-W2 analog): on each of the 8 C-probes, the
> query after the second contradiction must return the twice-corrected
> value. TNN-2 silently no-oped and returned the first-patched value.
> PASS: 8/8.

The adversary operationalized "the query" as a query on the FACT key
(b,5202) (SEALED_WORLDS.md: "KB-B2: final query on the contradicted
FACT key after the second contradiction"). Three specific problems,
each evidence-cited:

**Problem 1: the prereg's baseline sentence is false on the fact key.**
"TNN-2 silently no-oped and returned the first-patched value" describes
MAP-key behavior only. Traced through the prereg's own documented base
facts: base ev_observe (line 836/844) wrote CON self-edges on
contradicted fact nodes and taught the new fact (H5 change 3.3 was net
0 on this hunk, folding only the edge-write; the teach predates H5);
activate (unchanged by H5) skips superseded tag-1 nodes and returns the
live match. After two contradictions on (b,5202), the only live tag-1
fact on that key holds the twice-corrected value, so the unmodified
TNN-2 baseline also returns it on the fact key. A bar the pre-change
baseline passes cannot evidence an advance. The baseline sentence is
true only for the MAP key, where the once-patched MAP answered. The
only prereg-coherent reading of KB-B2 is therefore the MAP key.

**Problem 2: the stated justification is factually false.**
SEALED_WORLDS.md: "The prereg pins the query without naming the key;
the fact key matches the builder dev tests D2/D3 and the 1421pdt M3-W2
probe placement." The 1421pdt claim is false. Quoted from
docs/lab/rsi/runs/wave-20261001-1421pdt/sealed_adv/SEALED_BATTERY_PREREG.md
section 3.8, the M3-W2 event stream ends:

```
OBSERVE 43102 43502 43119
QUERY 43101 43509 43119
```

and K-S12: "PASS iff the post-second-contradiction probe returns
43119." Key (43101, 43509) is the MAP key (promotion was
`QUERY 43101 43509 43103`); the fact key (43102, 43502) was contradicted
but never queried by the bar. The 1421pdt result confirms the MAP-key
semantics: "Second-contradiction probe FAIL (returned 43109, not
43119)" (RESULT_SEALED_ADV_BATTERY.md). The adversary's justification
for the weakening operationalization rests on a false premise.

**Problem 3: under the faithful (MAP-key) reading, H5 FAILS KB-B2 on
committed sealed evidence.** The battery itself contains the MAP-key
probe as the supplementary bridge query. Committed run logs:
"C1S bridge-query=100 (supplementary, non-bar)" and
"C2S bridge-query=900 (supplementary, non-bar)". Expected under KB-B2:
the twice-corrected values 300 and 623. Observed: the stale ORIGINAL
values 100 and 900, via promote_graph's shadowing exact-hit fact
(ev_teach_in inside promote_graph, tnn3_h5.zag line 543-558), which is
never contradicted, so the key never misses and the trial loop never
re-derives (adversary's own S1 mechanism account, verified in code).
On the actual M3-W2 probe placement, H5 returns a value staler than
TNN-2's (original c0 vs TNN-2's once-patched c1).

Consequence: KB-B2 passes only under an operationalization that the
frozen prereg's own text rules out. Under the faithful reading it
fails. PREREG_H5.md section 10: "H5 advances past this wave iff ALL of
KB-W1, KB-W2, KB-B1, KB-B2, KB-B3, KB-R1, KB-G1, KB-D1, KB-P1 pass. Any
single bar failing KILLS H5 for this wave." The ADVANCES verdict
therefore does not stand. This is the dissent.

Note the same non-discrimination flaw affects KB-B3 as operationalized:
on the fact key, the TNN-2 baseline also supersedes the old fact and
teaches the new one per contradiction (pre-existing ev_observe
behavior), so the revert probe (re-observe v0, query returns v0 from a
fresh node) passes without any H5 machinery. The 1421pdt M3-W3 failure
(K-S13: "returned 43703, not 43713") was likewise on the MAP key, where
the stale taught fact short-circuited relearning. The battery's
C-family behavioral bars, as run, measure the pre-existing fact path,
not H5. I do not claim KB-B3 fails under a faithful reading (no
MAP-key revert probe was run); I claim it is non-discriminating as
run, so it lends no support to ADVANCES.

---

## Attack 3: The S1 caveat (re-derivation story fails for MAP keys)

**Finding: S1 is accurate and verified in code and logs; it bounds the
3.6 claim to unpromotion-only and reveals the MAP-key staleness above.**

Prereg 3.6 promised: "on the next miss for the key, ev_query's trial
loop (mp_run) runs against live facts and promote_graph creates a
fresh MAP whose DEP edges anchor to live fact nodes." Code check:
promote_graph (line 543) calls ev_teach_in(W,s,r,ans), teaching a live
tag-1 shadow fact on the MAP key. ev_query checks activate first, which
finds the shadow fact; the key therefore never misses; mp_run never
runs; no fresh MAP is promoted. The condition the story depends on
("on the next miss for the key") cannot occur for MAP keys. Confirmed
empirically: bridge queries return 100/900 via the shadow fact.

How much of the "generic transition" claim survives: the UNPROMOTION
half is demonstrated on both structure classes (8 guide CON edges,
8 MAP CON deltas, fact CON edges in revert probes; all via the one
supersede function). The RE-DERIVATION half is not demonstrated for
MAPs at all. Further, MAP supersession is behaviorally inert on every
key probed in this battery: activate reads tag-1 facts only, and
t2_trial builds fresh candidate graphs without consulting existing
MAPs, so a superseded MAP changes no query outcome here. The C-family
half of H5 is therefore white-box-only evidence: the transition fires,
but nothing in the battery shows the firing matters. Combined with the
central finding, the "M3-W2 fix" label on KB-B2 is unsupported; on the
key where M3-W was defined, the query is still stale.

---

## Attack 4: The context-flush world-design correction

**Finding: the correction was legitimate probe hygiene, not
world-reshaping. It does not threaten the verdict.**

Evidence for legitimacy:
- Documented transparently in SEALED_WORLDS.md before evaluation, with
  the failure mode stated (first ev_act probe returned 30).
- Family requirements unchanged: 8 resolution events, each followed by
  subject re-presentation (ctx_push) and an ev_act probe. The flush
  (ctx_push of 51991-51994 into the 4-slot window) only clears
  distractor subjects; the re-presentation re-adds the tested subject,
  so each probe still tests exactly the resolved guide.
- S3 positive control: pre-flush, ev_act returned 30 when a still-live
  guide's subject sat in context (the never-resolved control in R1, the
  not-yet-resolved 51201 guide in R2). That is correct selector
  behavior for live guides, so the 8/8 post-resolution zeros are
  attributable to supersession, not to a dead selector.
- The uncorrected worlds' KB-B1 failures were measurement
  contamination, not mechanism failure; the correction isolates the
  variable under test.
- The flush cannot mask over-supersession: the white-box exact counts
  (R1: exactly 4 guide-CON, exactly 1 live guide; R2: wrong-key
  resolves nothing) check selectivity independently.

Minor protocol note: the prereg did not specify context hygiene, so the
adversary had to invent it mid-course. It was the right call and it
was documented; future preregs should pin probe-isolation rules. Not
verdict-affecting.

---

## Attack 5: Bar calibration

**Finding: headroom was unneeded (8/8 observed vs >= 6/8 bars), but the
battery's discriminating power is unevenly distributed, and one bar
was load-bearing on a false premise.**

- 6/8 vs 8/8: the 6/8 thresholds would admit a flaky trigger (2/8
  misses); observed 8/8 on KB-W1/KB-W2 gives margin, and KB-B1 at
  strict 8/8 is the tight behavioral bar for the R-family. A weaker
  mechanism check: a guide-only mechanism (no MAP supersession) would
  fail KB-W2's white-box count, so the conjunction does require the
  MAP path to fire. The battery is not passable by a guide-only
  variant. That is genuine calibration strength.
- Uneven discrimination (new finding): KB-B1 is discriminating
  (TNN-2 returned 30; H5 returns 0). KB-W1/KB-W2 are discriminating as
  white-box (zero edges in baseline). KB-B2 and KB-B3 as operationalized
  are NON-discriminating (baseline passes; traced in the central
  finding). KB-R1/KB-G1/KB-D1/KB-P1 are hygiene bars. So of the nine
  bars, the advance is carried by exactly three: KB-W1, KB-B1 (guide
  lifecycle, real behavioral delta) and KB-W2 (MAP edge-writing,
  behaviorally inert in this battery).
- The 8/8 observations exceed the 6/8 bars, but headroom on a
  non-discriminating bar is meaningless: KB-B2 at 8/8 on the fact key
  measures nothing about H5.

---

## What survives, and what the honest verdict is

Survives as genuine, adversary-tested evidence:
1. H5 wires a generic protected edge-write (supersede, 4 lines,
   COMPARE+LINK only) into the cognition path with net -22 cognition
   lines, no new modes/bridges/handlers/ISA additions (KB-G1 verified).
2. On sealed resolution worlds, experience writes CON self-edges on
   guide-class nodes (8/8) and resolved guides stop firing (ev_act 8/8
   zeros vs TNN-2's 30). The prereg's falsifiable prediction does not
   fire. Selectivity is demonstrated (control stays live, wrong-key
   resolves nothing). This is the M2-W2 fix, real.
3. The same transition fires on MAPs (8/8 CON deltas) and facts
   (revert probes), i.e., the write is generic across structure
   classes. Determinism and process bars are clean (KB-D1 spot-check
   independently reproduced: 3/3 identical hashes).

Does not survive:
1. KB-B2 as an "M3-W2 analog": fails under the prereg-faithful
   (MAP-key) reading on committed sealed evidence (100 != 300;
   900 != 623). The passing reading is unfaithful and
   non-discriminating.
2. The 3.6 re-derivation story for MAP keys (S1, code-verified).
3. Any behavioral consequence of MAP supersession in this battery
   (inert on all probed query paths).
4. The hypothesis sentence's "driven by learner-maintained standing":
   not implemented per the prereg's own section 3.8; triggers are
   researcher-fixed scans over learner-accumulated state.

## Verdict restated

**DISSENT.** Bar KB-B2, faithfully operationalized per the frozen
prereg's baseline sentence (MAP key, the 1421pdt M3-W2 probe
placement), FAILS: committed sealed evidence shows the MAP-key query
returning the stale original values (C1S=100, C2S=900) instead of the
twice-corrected values. The adversary's fact-key operationalization
contradicts the prereg's TNN-2 baseline description, rests on the
false claim that the fact key matches the 1421pdt M3-W2 probe
placement (1421pdt probed the MAP key: `QUERY 43101 43509`, K-S12
expecting 43119), and renders the bar non-discriminating since the
unmodified baseline passes it. Per PREREG_H5.md section 10, a single
failed bar KILLS H5 for this wave. **H5 does not advance; the
ADVANCES verdict is overturned.** Under VOID discipline, H5 may return
only via a fresh prereg plus fresh sealed worlds. That fresh prereg
should: pin the query key explicitly (MAP key for any M3-W2/M3-W3
analog), confront the shadow-fact root cause (promote_graph's taught
answer fact is never contradicted, so the MAP key never misses),
promote selectivity assertions (exact CON counts, control-live,
wrong-key) to frozen bars, and replace or repair the
non-discriminating fact-key behavioral bars.

Deliverables: NAMECHECK_REDTEAM.md, REDTEAM_REVIEW.md (this file), both
in docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5/. No commits made;
coordinator commits.
