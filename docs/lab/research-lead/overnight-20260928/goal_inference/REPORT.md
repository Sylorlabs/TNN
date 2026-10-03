# REPORT: H-GOALINF-1 Goal-Type Inference

**Verdict: GOAL-INFERENCE-COMPLETE (with routing table).**
All 5 tests PASS, 3/3 byte-identical. The learner infers the query goal
type from its own state: confident FACT with no walkable structure
routes RETRIEVE (fast, correct); walkable MAP structure routes
CONSTRUCT (genuine composition with promotion); a confident FACT
contradicted by structure triggers CONFLICT (the stale FACT is demoted
with the native supersession primitive and the answer is re-derived by
construction); weak or absent basis withholds honestly.

## 1. Question

H-COMPVER-2 resolved the ev_query hookup by making RETRIEVE (ev_query)
and CONSTRUCT (ev_cquery) distinct operations, leaving open whether the
goal type should be caller-specified or learner-inferred. H-GOALINF-1
tests the inference hypothesis with its own preregistered bar
(5fd4988d8): given a query (s,r), the learner decides RETRIEVE vs
CONSTRUCT from learner state only, no researcher goal flag.

## 2. Mechanism (unfrozen variant only)

- Base: gi_base.zag = byte-identical concatenation (cmp-verified) of
  H-COMPVER-2's lv2_base.zag + lv2_patch.zag. Copied, never edited.
- Patch: gi_patch.zag (226 lines). gi_factscan (best live
  non-superseded FACT by pred_score then bid, mirroring lv_predict);
  gi_probe (target-free greedy structural walk from s via
  un_candidates/un_satisfy, max 8 segments, no MAP reuse; read-only);
  gi_supersede (type-3 self-edge, the same primitive lv_observe uses on
  contradiction); gi_compose (compose_lv's body with caller-supplied
  pred/rel; the rel >= 3 gate unchanged); ev_iquery, the inference
  entry. Route codes in st[12]: 0 RETRIEVE, 1 CONSTRUCT,
  2 CONSTRUCT-CONFLICT, 3 WITHHOLD; probe MAP-execs in st[8].
- Inference rule: lv_setup with no basis -> WITHHOLD. Weak FACT
  (score < 3) -> CONSTRUCT via ev_cquery (internal withhold when
  unreliable; uncertainty is never a gamble). Confident FACT ->
  gi_probe: no chain -> RETRIEVE via ev_query; chain agrees with the
  FACT -> CONSTRUCT via ev_cquery; chain disagrees -> CONFLICT:
  gi_supersede the FACT, then gi_compose with the structural prediction
  (reliability = walked segments, scaffold, honestly labeled).
  Preregistered tiebreak rationale: a constructed answer is
  independently re-verified by execution (lv_verify_chain) while a FACT
  is opaque recall, so the verifiable channel wins.
- Driver: gi_driver.zag (272 lines). World builders and the evidence
  helper copied verbatim from H-COMPVER-2's driver; new gi_confirm
  helper (predict/resolve cycles that never write a FACT, so a taught
  FACT earns its own score) and the 5-test battery.

## 3. Battery and results (3/3 byte-identical)

SHA-256 of each run:
`abc1afdb0f796a1625edf7f121893e1b57f83c3ebf897abd92b46db215687291`
(runs 1, 2, 3 identical). Summary line: `GI-SUMMARY 1 1 1 1 1`.

### 3.1 T-RTRV: known FACT, no structure -> RETRIEVE (K1)

Bare world; ev_teach_in(201,80,42) + 5 confirm cycles: FACT (42,
score 5); no MAPs exist. ev_iquery(201,80,0,st).

| metric | value |
|---|---|
| route | 0 RETRIEVE (noprobe) |
| ans | 42 |
| cost | 1 |
| live MAPs | 0 -> 0 |
| probe execs | 0 |

PASS. Fast correct recall; the probe correctly found nothing to walk.

### 3.2 T-COMP: FACT + agreeing structure -> CONSTRUCT (K2)

T1 world; 5 lv_observe cycles (101,70) o=107: FACT (107, score 4);
probe walks 101->103->105->107, agreeing.

| metric | value |
|---|---|
| route | 1 CONSTRUCT (agree) |
| ans | 107 |
| tried / rejected | 1 / 0 |
| probe execs | 3 |
| cost | 4 |
| live MAPs | 7 -> 8 |
| LINK14 out of newest MAP | 3 |

PASS. ev_cquery/compose_lv genuinely ran (tried=1, MAP promoted with
LINK14=3), not FACT recall.

### 3.3 T-STALE: confident WRONG FACT vs structure -> CONFLICT (K3)

T1 world; ev_teach_in(101,70,999) + 7 confirm cycles: FACT (999,
score 7); probe walks 101->103->105->107, contradicting the FACT.

| metric | value |
|---|---|
| route | 2 CONSTRUCT-CONFLICT (demote=129) |
| ans | 107 |
| stale FACT superseded | 1 (is_superseded) |
| tried / rejected | 1 / 0 |
| probe execs | 3 |
| cost | 4 |
| live MAPs | 7 -> 8 |

PASS. The learner detected the conflict, retired the stale FACT with
its native supersession primitive (a recorded revision event), and
re-derived 107 by construction. Stale recall (999) did not happen.

### 3.4 T-UNC: weak FACT -> CONSTRUCT route, honest withhold (K4)

T1 world; 2 evidence cycles: FACT (107, score 1 < 3).

| metric | value |
|---|---|
| route | 1 CONSTRUCT (weakfact) |
| ans | -3 (LV-WITHHOLD unreliable rel=1) |
| tried | 0 |
| live MAPs | 7 -> 7 |
| cost | 0 |

PASS. Uncertainty withholds; no gamble, no promotion on thin evidence.
The probe is skipped on the weak-FACT arm, so the withhold is free.

### 3.5 T-NE: no basis -> WITHHOLD (K5)

T1 world; no evidence. lv_setup finds no FACT and no MAP fallback.

| metric | value |
|---|---|
| route | 3 WITHHOLD (nobasis) |
| ans | -3 |
| live MAPs | 7 -> 7 |
| cost | 0 |

PASS.

## 4. Routing table and cost analysis (K6)

| test | learner state | inferred route | answer | correct |
|---|---|---|---|---|
| T-RTRV | FACT(42,5), no walk | 0 RETRIEVE | 42 | yes |
| T-COMP | FACT(107,4), walk agrees | 1 CONSTRUCT | 107 | yes |
| T-STALE | FACT(999,7) vs walk 107 | 2 CONFLICT | 107, FACT demoted | yes |
| T-UNC | FACT(107,1) weak | 1 CONSTRUCT | -3 withhold | yes |
| T-NE | no basis | 3 WITHHOLD | -3 | yes |

Routing accuracy 5/5. Missed CONSTRUCTs: 0. Cost totals: RETRIEVE 1,
CONSTRUCT 8 (4 + 4), WITHHOLD 0.

On waste (preregistered): T-COMP pays cost 4 where recall would have
cost 1. The 3 extra units are quantified, not hidden: 3 probe MAP-execs
plus 1 compose try. What they buy is learner-verified construction and
a promoted MAP_Z with LINK14 provenance and new type-15 co-use edges,
i.e., new persistent learner structure, which recall never creates.
Whether that price is worth paying per query is a policy question the
table now makes measurable; the mechanism reports the price honestly.

## 5. Kill bar scorecard

- K1 (T-RTRV route=0, ans=42, cost=1, MAPs unchanged, probeexecs=0):
  PASS.
- K2 (T-COMP route=1, ans=107, tried>=1, +1 MAP, LINK14=3): PASS.
- K3 (T-STALE route=2, ans=107, stale FACT superseded, tried>=1,
  +1 MAP): PASS.
- K4 (T-UNC route=1, ans=-3, tried=0, MAPs unchanged): PASS.
- K5 (T-NE route=3, ans=-3): PASS.
- K6 (routing accuracy 5/5; 0 missed CONSTRUCTs; waste quantified):
  PASS.
- K7 (3/3 byte-identical, SHA-256 recorded): PASS.
- K8 (0 modes/bridges/handlers/semantic cases; `expected` 0
  occurrences in gi_patch.zag; ev_iquery takes no goal flag and no
  researcher target; gi_base.zag cmp-verified): PASS.
- K9 (cognition lines recorded): 226 gi_patch.zag + 272 gi_driver.zag
  (105 verbatim copies + 167 new).

All bars pass: GOAL-INFERENCE-COMPLETE (with routing table).

## 6. What this establishes

1. Goal-type inference from learner state works on all five arms: the
   routing decision is computed from FACT pred_scores, MAP walk
   outcomes, and lv_setup outputs, with no researcher flag in the
   query path.
2. The stale-FACT adversary is defeated: a confident-but-wrong FACT is
   detected by the target-free structural probe, retired with the
   learner's own supersession primitive, and the answer is re-derived
   by verified construction (107, not 999).
3. Uncertainty has a defined policy: weak FACT -> CONSTRUCT route ->
   honest withhold (-3), no gamble, no promotion. The "?" in the task
   is answered: withhold.
4. Cost is measurable per route: RETRIEVE 1, CONSTRUCT 4 (probe 3 +
   try 1) in these worlds, WITHHOLD 0; the CONSTRUCT premium on
   FACT-agreeing queries is quantified as the price of verification
   plus structural promotion.

## 7. What this does NOT establish / limitations

1. gi_probe is relation-agnostic (un_candidates admits any applicable
   MAP) and greedy (first candidate). A production probe should
   restrict walks to MAPs relevant to r. T-RTRV used a bare world
   partly for this reason; on a rich world the probe could walk
   incidental chains from an unrelated s.
2. The conflict tiebreak (prefer the verifiable channel) and the
   srel = walked-segments mapping are researcher scaffold, honestly
   labeled; the battery validates the routing, not the tiebreak's
   optimality.
3. The probe duplicates DFS work (3 probe execs + 1 compose try); an
   integrated design could reuse the probe's walk instead of
   re-searching.
4. The RETRIEVE arm passes expected=-999999 to ev_query; it is inert on
   the activate path exercised here, but if activate ever missed, the
   downstream stages would see the sentinel.
5. Only T1-world analogues were tested. Sealed adversarial worlds for
   goal-type inference are future work.
6. Erratum vs PREREG: T-STALE's stale FACT scores 7 after 7 confirm
   cycles, not 6 as written in the prereg (each cycle is +1 from 0).
   The kill bar (score >= 3) is unaffected.

## 8. Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: threshold value 3 (reused),
  srel = walked-segments mapping, the -999999 sentinel, world builders
  (frozen protocol), confirm-cycle counts, the conflict tiebreak
  rationale, the driver.
- LEARNER-OWNED STRUCTURAL DECISIONS: all pred_scores, all walk
  outcomes, all 5 routing decisions, the demotion event.
- SOURCE-ENUMERABLE FORMS: 0.
- SUF DECISIONS: 0.
- REUSE EVENTS: lv_setup prediction reused for routing; probe walk
  value reused as gi_compose target.
- REVISION EVENTS: 1 (T-STALE stale-FACT demotion via native
  supersession).
- COGNITION LINES: 226 (gi_patch.zag) + 272 (gi_driver.zag, 105
  verbatim + 167 new).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

## 9. Artifacts

- `PREREG.md` (frozen; committed alone before implementation,
  5fd4988d8)
- `NAMECHECK.md` (Step 0 guard, provenance, constraints)
- `REPORT.md` (this file)
- `gi_base.zag` (2444 lines: byte-identical concatenation of
  H-COMPVER-2 lv2_base.zag + lv2_patch.zag, cmp-verified)
- `gi_patch.zag` (226 lines: gi_factscan, gi_probe, gi_supersede,
  gi_compose, ev_iquery)
- `gi_driver.zag` (272 lines: 5-test battery)
- `gi_full.zag` (assembled, 2942 lines)
- `gi_bin` (pinned znc build)
- `gi_compile.txt` (warnings only, same A0102 class as H-COMPVER-2)
- `gi_run1.txt`, `gi_run2.txt`, `gi_run3.txt`
  (SHA-256 `abc1afdb0f796a1625edf7f121893e1b57f83c3ebf897abd92b46db215687291`, 3/3 identical)

Constraints honored: unfrozen variant only; frozen sources read-only
(copies, cmp-verified); pure Zag via pinned znc; safebin active, zero
Python invocations; zero em/en dashes byte-verified; research paper
untouched; nothing pushed; explicit pathspecs on git add and git commit.
