# REPORT: GOALINF Red Team, adversarial battery on learner-inferred goal-type routing

**Verdict: GOALINF-REDTEAM-COMPLETE (with per-attack scores).**
Four adversarial worlds against the frozen H-GOALINF-1 mechanism
(commit 9aa06e463, GOAL-INFERENCE-COMPLETE, 5/5 PASS). Scores:
A KILL, B BOUND, C BOUND, D BOUND. 3/3 byte-identical runs.
Nothing was fixed; the killed mechanism is reported as found.

Per-attack summary line from the battery:
`ATTACK-A-SCORE=KILL`, `ATTACK-B-SCORE=BOUND`,
`ATTACK-C-SCORE=BOUND`, `ATTACK-D-SCORE=BOUND`.

## 1. Target

H-GOALINF-1's ev_iquery infers RETRIEVE vs CONSTRUCT vs CONFLICT vs
WITHHOLD from learner state: confident FACT plus no walkable structure
routes RETRIEVE; a walkable structure agreeing with the FACT routes
CONSTRUCT; a structure contradicting the FACT routes CONFLICT
(supersede the FACT with the native type-3 primitive, re-derive by
verified construction, on the preregistered rationale that the
verifiable channel beats opaque recall); weak or absent basis
withholds. The red team attacks the routing rule, not the 5/5 battery
itself: each attack is a world the preregistered battery did not
cover, with success criteria fixed before the final runs.

## 2. Attack A: decoy structure vs confident CORRECT fact (KILL)

World: bare. FACT (201,80)=42 taught, then 5 gi_confirm cycles with
world outcome 42: score 5, confident, correct. Then a decoy chain
201..207 is laid via r=1 FACTs and four 2-link chain MAPs are promoted
by the learner's own trial/rebind machinery (ev_query with expected
values at world-build time, the same method T1's trains use). The
decoy answers a different relation family than the query; gi_probe is
relation-agnostic, so it walks the decoy.

Observed (`gi_run1.txt`):

| metric | value |
|---|---|
| probe walk | 201 -> 203 -> 205 -> 207, 3 MAP execs, greedy first-candidate |
| route | 2 CONSTRUCT-CONFLICT (demote=2) |
| correct FACT (42, score 5) | superseded (is_superseded=1) |
| answer | 207 via LV-COMP-SEGS n=3 (MAPs 23 34 45), tried=1 |
| live MAPs | 4 -> 5 (MAP_Z promoted on the decoy) |

KILL. This is T-STALE inverted: there the FACT was stale and the
structure was live; here the FACT is fresh and correct and the
structure is the decoy, and the routing cannot tell the difference.
The learner destroys correct confident knowledge (the 42 FACT earned
by five consistent world observations) and constructs the decoy
endpoint 207 through full verification (lv_verify_chain checks that the
composed graph executes to 207, which is internal execution
consistency, not world truth). The preregistered tiebreak rationale
("the verifiable channel beats opaque recall") has no staleness or
decoy detector: verification certifies that the structure is
self-consistent, not that it is live. Report section 7.1 anticipated
that the probe "could walk incidental chains" as a T-RTRV design note;
it did not cover the cascade demonstrated here: walk decoy, demote
correct FACT, confidently misconstruct, promote the misconstruction
as new learner structure. Not fixed, per the red-team brief.

## 3. Attack B: FACT score exactly at the boundary (BOUND)

Worlds: bare. B3 teaches (201,80)=42 plus 3 confirm cycles: score 3,
confident by exactly the threshold. B2 uses 2 confirm cycles: score 2,
weak by one unit. Btie teaches two FACTs (42 then 43, both score 0)
and compares lv_predict's choice against gi_factscan's choice.

Observed:

| case | fact score | route | answer |
|---|---|---|---|
| B3 | 3 | 0 RETRIEVE noprobe | 42 |
| B2 | 2 | 1 CONSTRUCT weakfact | -3 (LV-WITHHOLD rel=2) |
| Btie | tie (0,0) | lv_predict=42, factscan node picks 42 | agree=1 |

BOUND. One confirm cycle is the whole difference between an honest
withhold and a confident retrieve: the threshold at 3 is a sharp
deterministic discontinuity, and it is honestly labeled researcher
scaffold (reused threshold value, report section 8), so the
discontinuity itself is a boundary property, not a spec violation.
The "flips between runs" hypothesis does not survive contact with the
implementation: every tiebreak is a total order (score desc, bid desc,
scan order), lv_predict and gi_factscan share the identical ordering
code (Btie confirms they cannot diverge), and all three runs are
byte-identical. There is no nondeterminism to exploit; the boundary is
sharp, stable, and scaffold.

## 4. Attack C: stale FACT vs STALE structure, both channels wrong (BOUND)

World: bare. Stale confident FACT (301,80)=911, score 7 via 7 confirm
cycles. Stale walkable structure 301..307 (four chain MAPs from the
older world, same builder as attack A). Then the new ground truth 912
arrives twice through the teach channel: two live FACTs (301,80)=912
at score 0, outscored by the stale 911. The learner holds the truth in
its store and cannot use it. The probe walks 301 -> 303 -> 305 -> 307.

Observed:

| metric | value |
|---|---|
| route | 2 CONSTRUCT-CONFLICT (demote=2) |
| stale FACT (911, score 7) | superseded |
| answer | 307 via LV-COMP-SEGS n=3, tried=1, probeexecs=3 |
| the two 912 FACTs | live, ignored |

BOUND. Both channels are wrong and the structure wins, exactly as the
preregistered tiebreak orders. The mechanism follows its spec: the
report's section 7.2 explicitly excludes tiebreak optimality from the
validated claims ("the battery validates the routing, not the
tiebreak's optimality"), so a both-wrong world resolving to the
structural channel is inside the admitted scaffold boundary. The
concrete gap this world exhibits: no staleness detection on the
structural channel, and no cross-check of MAP endpoints against newer
FACTs (the 912 evidence is present but the single-best scoring rule
buries it). Honest limitation, not a spec violation; scored BOUND,
not KILL.

## 5. Attack D: many weak FACTs, none confident (BOUND)

World: bare. Six FACTs (201,80)=42 taught; 2 gi_confirm cycles. The
rich-get-richer scoring (each cycle boosts only the single best FACT)
leaves the best at score 2: six agreeing observations, no single one
confident.

Observed:

| metric | value |
|---|---|
| live FACTs (201,80) | 6, all value 42 |
| best FACT score | 2 |
| route | 1 CONSTRUCT weakfact |
| answer | -3 (LV-WITHHOLD rel=2), tried=0 |

BOUND. The router consults only the single best FACT (gi_factscan);
collective weak evidence is invisible to it. But the mechanism follows
its preregistered uncertainty policy (K4: uncertainty is never a
gamble): it withholds honestly instead of gambling on the six-fold
agreement. No aggregation exists, which is an architectural boundary,
and the withhold is the safe failure mode, so this is BOUND rather
than KILL. A future router that sums weak evidence would change the
policy, not fix a violation.

## 6. Determinism

SHA-256 of each run:
`70094d20f061535f123675445d3a37e4cf8dd8f911645dbccd19a810586a07a7`
(runs 1, 2, 3 identical). Summary line: `GI-ATTACK-SUMMARY 1 1 1 1`
(all four attacks behaved as their criteria specify).

## 7. What this establishes

1. The CONFLICT arm's safety rests on an untested premise: that the
   contradicting structure is live. Attack A falsifies the premise
   with a concrete world: a 3-MAP decoy built by the learner's own
   machinery flips a correct confident FACT into a confidently
   constructed wrong answer, with the misconstruction promoted as new
   learner structure. The "verifiable channel" verifies execution
   consistency, not liveness.
2. The confidence threshold is a sharp, stable, deterministic
   discontinuity (attack B). No flip-between-runs behavior exists.
3. When both channels are wrong, the structural channel wins by
   preregistered tiebreak and the learner constructs the stale answer
   confidently while fresher (but outscored) evidence sits unused in
   its own store (attack C).
4. The router has no evidence aggregation: six agreeing weak FACTs
   withhold exactly like one (attack D), which is the specified
   uncertainty policy, not a violation.

## 8. What this does NOT establish / limitations of the red team

1. Only one decoy geometry was tested (a 6-link r=1 chain with 2-link
   MAPs). Other decoy shapes (contract-fallback walks, co-use ordered
   decoys, single long MAPs) are not covered.
2. Attack C's "world change through the teach channel" is one model of
   staleness; staleness arriving through lv_observe is processed by
   the revision machinery and was not attacked.
3. The red team did not test whether a staleness/recency signal on
   MAPs would rescue the CONFLICT arm; per the brief, nothing was
   fixed.
4. Attack D's six FACTs all share one value; conflicting weak FACTs
   were not tested.

## 9. Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: the four attack worlds,
  mk_chain builder, decoy expected values at world-build time,
  per-attack score criteria, the driver.
- LEARNER-OWNED STRUCTURAL DECISIONS: all pred_scores, all probe walk
  outcomes, all 4 routing decisions, both demotion events, both
  MAP_Z promotions.
- SOURCE-ENUMERABLE FORMS: 0.
- SUF DECISIONS: 0.
- REUSE EVENTS: gi_confirm copied verbatim from H-GOALINF-1 driver;
  mk_chain reuses the T1 train method (ev_query with expected).
- REVISION EVENTS: 2 (attack A correct-FACT demotion; attack C
  stale-FACT demotion, both via the native supersession primitive).
- COGNITION LINES: 218 (gi_attack.zag, new).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

## 10. Artifacts

- `NAMECHECK.md` (Step 0 guard, provenance, constraints)
- `REPORT.md` (this file)
- `gi_base.zag` (2444 lines: cp copy of the frozen H-GOALINF-1 base,
  cmp-verified, never edited)
- `gi_patch.zag` (226 lines: cp copy of the frozen H-GOALINF-1 patch,
  cmp-verified, never edited)
- `gi_attack.zag` (218 lines: the 4-attack battery driver, new)
- `gi_full.zag` (assembled, 2888 lines)
- `gi_bin` (pinned znc build)
- `gi_compile.txt` (warnings only, same A0102 class as H-GOALINF-1)
- `gi_run1.txt`, `gi_run2.txt`, `gi_run3.txt`
  (SHA-256 `70094d20f061535f123675445d3a37e4cf8dd8f911645dbccd19a810586a07a7`, 3/3 identical)

Constraints honored: frozen mechanism attacked, never modified
(copies, cmp-verified); pure Zag via pinned znc; safebin active, zero
Python invocations; zero em/en dashes byte-verified; research paper
untouched; nothing pushed; explicit pathspecs on git add and git commit.
