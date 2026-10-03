# PREREG: BELIEF-PROVENANCE 1 (evidential adjudication between conflicting structures)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/belief_provenance/` only.
Worker: BELIEF-PROVENANCE subagent, 2026-10-03.
Parent mandate: overnight priority 9, belief reasoning from
provenance/evidence. TNN structures carry provenance (type-14 parent
links, type-15 co-use edges, type-16 combine provenance). The
question: can the learner REASON about belief strength from
provenance and evidence, not just store it?

## 1. What is being tested

Whether the learner can adjudicate between two CONFLICTING,
grounded structures using provenance/evidence features whose
evidential weight the learner itself learned from experience,
with no researcher-supplied trust rule in the decision path.

Concretely: the learner holds two structures that both start from
the same subject but execute to different terminals (genuine
conflict, both grounded, both with real observational support).
The query is open ended (no target to verify against, so this is
belief under uncertainty, not verification). The learner must
commit to one structure's output. The decision must come from
learner-owned evidential state, and the experiment must be able
to tell the difference between "the learner reasoned from
evidence" and "the researcher hardcoded which provenance wins".

## 2. What counts as "conflicting" (frozen definition)

Two MAP structures A, B are in conflict for a query subject s iff
ALL of the following hold (checked white box by the driver):

- C1: both are live MAPs with start == s.
- C2: both are grounded: every fact id in each structure's chain
  indexes a live fact row in the learner's fact store.
- C3: both have real support: corr >= 1 for each (corr counts are
  defined in section 3; in this experiment they are 8 and 2).
- C4: their executed terminals differ: m_exec(A, s) != m_exec(B, s).

If C1..C4 hold, the conflict is genuine: both structures are
built from real live facts and real observations, and they
disagree. There is no target to check the answer against at
decision time; the world's confirmation arrives only after the
learner commits (section 5).

## 3. Provenance features (frozen, learner maintained)

Each MAP carries, in learner state, maintained only by learner
machinery (never written directly by the driver):

- corr (u8): corroboration count. Incremented by the learner's
  `bp_observe` each time a world observation confirms the
  structure's terminal from its start. This is the evidence
  feature under test.
- rev (u8): revision count. Provisioned in the MAP layout, always
  0 in BP-1. Revision based adjudication is NOT tested here; it
  is an explicit open question (section 8).

Edge provenance, same types as the parent lanes (14/15/16), no new
edge types:

- type-14: delivery parent (answer node id 100+nn -> structure).
- type-15: co-consideration (winner <-> loser, both directions)
  written when one adjudication episode resolves.
- type-16: meta provenance (meta-row id 200+row -> winner and
  200+row -> loser). The learner's meta-belief has provenance.

Meta-table (learner-created persistent state): up to 32 rows of
[wcorr, lcorr, wmid, lmid, ep] = the winner's corr, the loser's
corr, winner mid, loser mid, episode index. A meta-row is written
by learner machinery after each resolved conflict episode, with
type-16 edges to both structures. The meta-table IS the learner's
learned evidential policy content.

## 4. The adjudicator (mechanism under test, disclosed)

New learner machinery, generic (works on any MAPs with corr
provenance; no domain content, no structure identity matching):

- `bp_adjudicate(st, s)`: scans live MAPs with start == s.
  n < 2 -> return -4 (no conflict). All terminals equal ->
  return -5 (agreement). Otherwise, for each candidate with corr
  value c, score(c) = number of meta-rows with wcorr == c. Pick
  the candidate with the highest score (ties broken by lower mid,
  disclosed). If the top score is tied (including 0 vs 0 on an
  empty table) -> return -3 (INDETERMINATE, no commitment).
- `bp_explore(st, s, revealed, hi_first, ep)`: fallback used only
  when adjudication returns -3. Tries candidates in order (higher
  corr first if hi_first, else lower corr first; alternating by
  episode, disclosed exploration machinery), executes each to its
  terminal, and takes the first whose terminal equals the world's
  revealed terminal. Writes the meta-row + t15 + t16 edges.
- `bp_confirm(st, wmid, lmid, revealed, ep)`: after an
  adjudication commitment, compares the committed structure's
  terminal to the revealed terminal by equality. On match writes
  the meta-row + t15 + t16 edges and returns 1; else returns 0
  and writes nothing.
- `bp_observe(st, mid, term_obs)`: executes mid from its start;
  if the terminal equals the observed terminal, corr[mid]++.
- `bp_deliver(st, mid, val)`: answer node + type-14 edge + ANS line.

The `revealed` terminal is a world observation supplied by the
driver; the learner never sees the world's regime except through
revealed terminals. The driver never selects structures: all
selection goes through the learner functions above.

## 5. Researcher/learner boundary (disclosed, load bearing)

Researcher-supplied (generic machinery, frozen, source disclosed):

- corr increment on confirmed observation (generic evidence
  counting, like a counter in the ISA);
- conflict scan, meta-row schema, provenance edge writes;
- score = count of matching wcorr rows; argmax; tie -> -3;
- alternating exploration order when indeterminate;
- equality comparison for confirmation.

NOT researcher-supplied (learned content): WHICH corr value the
meta-table favors. No line of learner code compares corr
magnitudes, prefers newer/older structures, or prefers any
identity. The decision outcome varies only with the contents of
the learner-written meta-table.

How the experiment verifies the learner (not the researcher) made
the decision:

- (a) Source disclosure: the decision function contains no corr
  magnitude comparison and no recency or identity preference.
- (b) The flip: ARM-STANDARD and ARM-REVERSED present
  structurally identical phase-2 inputs (same corr values 8/2,
  same chain shapes, same entity layout; only node ids and
  entities are fresh). The learner commits to OPPOSITE structures
  in the two arms. No fixed researcher rule ("trust higher corr",
  "trust lower corr", "trust newer") produces opposite decisions
  on identical inputs; only the differing learner-owned
  meta-state explains the flip.
- (c) ARM-NOMETA: with an empty meta-table the learner returns
  -3 and commits to nothing, proving there is no hidden default
  researcher bias toward either provenance profile.
- (d) White box: the driver prints the full meta-table; the
  committed via= id must equal the argmax of the printed table.

## 6. Arms (each with a fresh learner state)

Phase-1 episode e (e = 0..9), base B(e) = 10 + e*10. Four facts:
(B,1,B+1), (B+1,1,B+2), (B,2,B+3), (B+3,2,B+4), taught in order
(fact ids 4e..4e+3). Two MAPs: hi id 2e, relseq [1,1], facts
[4e,4e+1], start B, end B+2; lo id 2e+1, relseq [2,2], facts
[4e+2,4e+3], start B, end B+4. Observations: hi x8 with
term_obs = B+2, lo x2 with term_obs = B+4 (corr hi = 8, lo = 2).
The world's regime R determines the revealed terminal:
R=HI -> revealed = B+2; R=LO -> revealed = B+4. Episode flow:
d = bp_adjudicate(B); if d == -3, w = bp_explore(B, revealed,
hi_first = (e even), e); else w = d and bp_confirm(w, other,
revealed, e) must return 1. Phase-1 episodes do not deliver ANS;
the meta-row is the learning record.

Phase-2 (fresh entities, base 200): facts 40..43 =
(200,1,201), (201,1,202), (200,2,203), (203,2,204). MAPs: hi id
20, relseq [1,1], facts [40,41], 200 -> 202; lo id 21, relseq
[2,2], facts [42,43], 200 -> 204. Observations: hi x8 (term
202), lo x2 (term 204). d2 = bp_adjudicate(200). On d2 >= 0:
bp_deliver(d2, terminal); bp_confirm(d2, other, revealed2, 10)
must return 1 (the learner's commitment is checked against the
world's confirmation; the learner must be RIGHT).

- ARM-STANDARD: phase-1 with R=HI (10 episodes), then phase-2
  with R=HI.
- ARM-REVERSED: phase-1 with R=LO (10 episodes), then phase-2
  with R=LO. The stale knowledge regime: the well corroborated
  structure encodes the old regime; the sparse one encodes the
  new regime.
- ARM-NOMETA: phase-2 only (MAPs id 0,1; facts 0..3; same 200
  base layout), R=HI. No phase-1, no reveal after -3, no
  meta-row. The honest indeterminate arm.

STANDARD and REVERSED phase-2 driver inputs are structurally
identical by construction (same corr values, same chain shapes,
same entity layout).

## 7. Frozen predictions (hand derived, exact)

Notation: meta-row = (wcorr, wmid, lcorr, lmid, ep).

ARM-STANDARD:
- Phase-1 ep0: adjudicate -> -3 (scores 0,0). Explore,
  hi_first=1: try mid0 term=12 == revealed 12 HIT. Meta-row 0 =
  (8,0,2,1,0). t15: 0<->1. t16: 200->0, 200->1.
- Phase-1 eps1..9: adjudicate -> mid 2e (score(8)=e,
  score(2)=0). Confirm OK each. Meta-row e = (8,2e,2,2e+1,e).
- After phase-1: NMETA=10, all rows wcorr=8/lcorr=2.
- Phase-2: adjudicate(200): cand mid20 corr8 term202 score10;
  mid21 corr2 term204 score0 -> win 20. ANS via=20 val=202.
  confirm(20,21,202,10) -> OK. Meta-row 10 = (8,20,2,21,10).
- Final: NMETA=11. LAST_VIA=20, LAST_VAL=202. Edges: t14=1
  (100->20), t15=22, t16=22, e_other=0. Counters: C_ADJ=11,
  C_EXPL=1, C_CONF=10.

ARM-REVERSED:
- Phase-1 ep0: adjudicate -> -3. Explore, hi_first=1: try mid0
  term=12 != revealed 14 MISS; try mid1 term=14 == 14 HIT.
  Meta-row 0 = (2,1,8,0,0).
- Phase-1 eps1..9: adjudicate -> mid 2e+1 (score(2)=e).
  Confirm OK. Meta-row e = (2,2e+1,8,2e,e).
- Phase-2: adjudicate(200) -> win 21 (score(2)=10).
  ANS via=21 val=204. confirm(21,20,204,10) -> OK.
  Meta-row 10 = (2,21,8,20,10).
- Final: NMETA=11. LAST_VIA=21, LAST_VAL=204. Edges: t14=1
  (100->21), t15=22, t16=22, e_other=0. C_ADJ=11, C_EXPL=1,
  C_CONF=10.

ARM-NOMETA:
- adjudicate(200): cand mid0 corr8 term202 score0; mid1 corr2
  term204 score0 -> tie -> -3. Driver logs INDETERMINATE, no
  reveal, no meta-row, no delivery.
- Final: NMETA=0, LAST_VIA=255. Edges: t14=0, t15=0, t16=0,
  e_other=0. C_ADJ=1, C_EXPL=0, C_CONF=0.

Predicted verdict: the learner adjudicates from learned
evidential state. STANDARD trusts the 8-corroboration structure;
REVERSED trusts the 2-corroboration structure; NOMETA abstains.
The flip on identical phase-2 inputs proves the decision came
from learner-owned experience, not a researcher rule.

## 8. Frozen kill bars

- K-1 determinism: 3/3 runs byte-identical per arm (sha256 of
  the run files).
- K-2 STANDARD: phase-2 via=20, val=202, confirm=1, NMETA=11,
  all 11 meta-rows (wcorr=8, lcorr=2). Every value exact.
- K-3 REVERSED: phase-2 via=21, val=204, confirm=1, NMETA=11,
  all 11 meta-rows (wcorr=2, lcorr=8).
- K-4 NOMETA: adjudicate=-3, NMETA=0, LAST_VIA=255, no ANS line
  in the NOMETA section.
- K-5 genuine conflict: phase-2 both candidates grounded (all
  chain facts live), corr 8 and 2, terminals differ (202 vs
  204); same checks on phase-1 ep0 candidates. In-driver
  white-box checks.
- K-6 the flip: viaS=20 AND viaR=21 AND viaS != viaR, with
  STANDARD rows all (8,2) and REVERSED rows all (2,8). A fixed
  researcher rule cannot produce this pair of outcomes.
- K-7 trace (shell grep): total ANS lines = 2; NOMETA section
  has 0 ANS lines; STANDARD phase-2 adjudicate win=20;
  REVERSED phase-2 adjudicate win=21; STANDARD ep0 shows
  EXPLORE-TRY mid=0 HIT before META-ROW r=0; REVERSED ep0 shows
  EXPLORE-TRY mid=0 MISS then mid=1 HIT.
- K-8 edge hygiene: t14 S=1/R=1/N=0; t15 S=22/R=22/N=0;
  t16 S=22/R=22/N=0; e_other=0 in every arm.
- F-VOID (terminal): any Python/C/JS/Rust invocation; any new
  mode, bridge, handler, opcode, or semantic case; any weakened
  bar; any learner read of the regime or of expected answers
  (the learner sees only revealed terminals as observations).

Verdict mapping: all K-1..K-8 PASS -> BP-1-PASS (learner
adjudicates from learned evidential state). K-6 fail with
K-2/K-3 pass -> researcher rule leak (decision not
evidence driven). K-4 fail (commitment with empty meta-table) ->
hidden default bias, VOID the evidential claim. Any F-VOID ->
VOID.

## 9. Open questions this lane does not claim

- Only corr is varied; rev (revision count) is provisioned but
  always 0. Revision based adjudication is untested.
- Only the 8-vs-2 corr profile is tested; other ratios and
  multi-candidate conflicts are not claimed.
- The adjudicator's argmax-over-counts is fixed generic
  machinery; this lane tests that the policy CONTENT is learned,
  not that the learning rule itself is learned.
- No regime change mid stream: whether the learner revises its
  meta-policy after the world flips is a follow-up (BP-2).
- One conflict pair per episode; competing partial structures
  untested.

## ONE-SYSTEM accounting (prereg)

- Cognition lines: 0 at prereg (implementation follows).
- New modes/bridges/handlers/semantic cases: 0 (frozen).
- New edge types: 0 (types 14/15/16 reused).
- Learner-state structures at prereg: 0.

To be ledgered C397.
