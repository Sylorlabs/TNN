# DIRECTIVE_RUBRIC.md — frozen referee rules for REF-FIRST (engine b)

Frozen with the build. The referee's control decisions are mechanical;
nothing is tuned per problem. Any change to this file is a rebuild.

## 1. Hypothesis agenda (referee-owned)

- H0 = WITHHELD (index 0; wins ties by lowest H5 index, as in DUAL).
- H1 = target claim (index 1).
- H2 = not(target) (index 2).
- Per-hypothesis referee state: evidence count, status
  (active / refuted-by-weighing / shelved / stalled-at-max-budget),
  depth-slice budget, last-selected round.

## 2. Priority rule (SELECT)

Among active, non-stalled hypotheses: **least-evidenced-first**
(evidence-item count supporting the hypothesis); tie ->
least-recently-selected (T first overall). A hypothesis stalls only when
its directive yields nothing AT the max budget; new claims from any line
clear all stalls (new information may unblock a line). This rule is
mechanical and deterministic; the audit logs every R SELECT with the
counts that decided it.

## 3. Directive form (referee-issued)

`R DIR#k: derive <goal>; depth-slice <b>; schemas {S_MP,S_UI,S_PBC};
premises usable(kind0/1)`

- goal: target (H_T) or not(target) (H_N).
- depth slice: the hypothesis's budget, +1 per selection, capped at the
  round bound (primary 8; B6X battery parameter, max 128).
- schema set: always all three committed schemas (frozen; the trust
  ledger never removes a schema from search, it only penalizes weighing).
- premise constraints: usable claims only (kind 0 premises/store,
  kind 1 derived; kind 2 subproof-local excluded outside subproofs).
- The derivation subroutine runs ONLY on a directive. There is no
  goal-less forward sweep. Directive returns: new claims + audit chains
  + contradiction flags (false newly derived).

## 4. Evidence rubric (frozen; same as DUAL so the two are comparable)

- Goal derived at depth d -> evidence item: supports its hypothesis with
  weight W(d), attacks the rival hypothesis with W(d).
- `false` derived -> evidence item: supports H0 with weight 1000,
  attacks H1 and H2 with weight 1000.
- W(d) = 1000/(1+d), minimum 1.
- No numeric score is invented without derivation backing: every weight
  cites the derivation depth of a claim present in the store (KB4).

## 5. Mid-search scoring

After each directive, the referee runs the REAL H5 deliberation
(dlb_delib.zag, verbatim) over the current partial evidence and logs
`R MID-SEARCH: leader=Hx conf=C margin=M rounds=R` plus the ledger head.
This is the referee scoring partial evidence mid-search. Frozen H5 config
(same as DUAL): mode=1, shallow_rounds=1, deep_rounds=12, amin=1, amax=12,
conf_thr=100, stab_win=2, eps=1, elim_margin=150, refute_thr=500,
evcap=128.

## 6. Referee decisions (deepen / switch / stop)

- Deepen: the priority rule re-selects a hypothesis -> its depth slice
  grows by 1.
- Switch: the priority rule selects the rival hypothesis.
- Stop: (a) target derived AND referee sustains H1 -> DERIVED;
  (b) not(target) derived AND referee sustains H2 -> REFUTED;
  (c) referee decisive (conf=1000); (d) agenda exhausted (every active
  hypothesis refuted, shelved, or stalled at max budget); (e) round bound.
- Final verdict: one more H5 deliberation over the full evidence,
  logged as R VERDICT.

## 7. Contradiction weighing (frozen rubric; same rule as HYB)

When a directive leaves both H and NOT-H derivable, the referee weighs:

    SCORE = PQ + 200*CORR - 10*DEPTH

- PQ (premise quality) = 1000 * (store-grounded support claims) /
  (all support claims), 1000 if the chain is empty. The support chain is
  walked through `C<digits>` audit refs. **Halved if any schema in the
  chain has trust < 500** (distrust penalty).
- CORR (independence) = distinct store-premise indices in the support
  chain, capped at 3 (proxy for premise-disjoint derivation paths).
- DEPTH = derivation depth of the goal claim.
- Higher score sustains; the loser is marked REFUTED-BY-WEIGHING
  (per-hypothesis withhold: kept in the audit trail, unrelated lines
  continue). Tie: the referee shelves the pair — withhold on that claim
  only — and the agenda continues.
- PBC audit fidelity: a PBC-discharged claim's audit cites the
  subproof's store premises (`S_PBC_BWD ASSUME:not(T) C1 C5 ...
  FALSE_DERIVED`), so PQ reflects the real chain.

## 8. Per-schema trust ledger (frozen rule)

- Starts uniform: S_MP=1000, S_PBC=1000, S_UI=1000.
- Changes ONLY via lost weighings: every schema appearing in the losing
  side's support chain loses 100 trust (floor 0). Logged as R TRUST.
- Effect: a derivation whose chain uses a schema with trust < 500 gets
  its PQ halved in future weighings (section 7). Distrust emerges from
  weighing outcomes, never from a hardcoded list.
- Same emergence rule as HYB so the two engines are comparable.

## 9. Withhold

Withhold is owned by the referee, per hypothesis. A refuted line does
not poison unrelated lines. Global WITHHELD is H0 winning the final
deliberation (or the agenda exhausting with nothing derived).
