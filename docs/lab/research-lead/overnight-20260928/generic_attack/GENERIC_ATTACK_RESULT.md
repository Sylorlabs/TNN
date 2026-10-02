# GENERIC ATTACK RESULT: Simpler-Explanation / OOD Attacks on C4 and C8

Date: 2026-09-30 UTC
Attacker: A2 (Simpler-Explanation / OOD Adversary, continued)
Prereg: PREREG_GENERIC_ATTACK.md (8abebb1f1, committed alone before
any implementation; ancestor verified via merge-base)
Verdict: **ATTACK-COMPLETE. Both simpler-explanation attacks SUCCEED;
OOD bounds confirmed as documented.**

## Summary

Two executable simpler baselines were built in pure Zag as minimal
variants of the v6 contestant, run on the frozen CA-2 world, and
scored by the unmodified frozen arena scorer. Two OOD worlds were
generated from attacker-chosen constants (sealed seed never opened)
and run 3x each (cognitive outputs byte-identical across runs;
only ms/rss_kb timing fields vary).

| Attack | Baseline | Frozen result | Verdict |
|--------|----------|---------------|---------|
| H-C4a | v6_c4mem (learn_rel = bare rel_store) | C4 4/4, total 0.779, per-cap table identical to v6 | CONFIRMED |
| H-C8a | v6_c8always (want_observe=1 always) | C8 4/4, total 0.779, per-cap table identical to v6 | CONFIRMED |

## Attack 1: C4 composition vs table-plus-lookup

**Result: H-C4a CONFIRMED.** The v6_c4mem baseline deletes the entire
DEVINT1 learning-path integration from learn_rel (no lex_feed, no
conc_touch, no rule_touch; just rel_store). It scores C4 4/4 with a
per-capability table byte-identical to v6 (total 0.779, tool_calls 7).

Stronger: on the OOD-C4 world, v6 and v6_c4mem produce byte-identical
reply fields on all 7 items (md5 a420c031838c568c11ee1ace5a34f24d for
both). The only differences are the learning metrics (v6:
lex_n=111, conc_n=24, rule_n=12; baseline: 0,0,0). The DEVINT1 feeding
changes internal counters and nothing else: zero effect on any
compositional answer, in-distribution or OOD.

**What this means.** The effective C4 mechanism is a triple table
plus two sequential lookups, not integrated relational learning. The
GENERIC-CAPABILITY classification stands (on-demand composition from
incrementally stored triples is generic and transferable), but the
audit's description ("learns relations incrementally through the
generic learning path") is weakened: the learning-path integration is
decorative for every tested item. An honest description is "triple
store plus 2-hop lookup".

**What would refute this.** A C4 test item whose answer depends on
the lexicon, concepts, or rules built by learn_rel (e.g., paraphrased
relation names requiring fuzzy match via concepts). No such item
exists in the frozen battery.

## Attack 2: C8 inquiry vs always-observe

**Result: H-C8a CONFIRMED.** The v6_c8always baseline sets
want_observe=1 on every test query, with no gap detection at all. It
scores C8 4/4 with total 0.779, per-cap table identical to v6. The
frozen C8 items test the request-plus-learn loop, not gap detection:
the scorer checks (reply==answer on the last ask) AND (observe
emitted on the first ask), both satisfied by blind always-asking.

The cost difference is stark: v6 emits 7 observe requests across the
whole arena run; the always-observe baseline emits 72. Same score,
10x the requests. Gap detection is genuine in v6 but unscored.

**H-C8b (ask cost) CONFIRMED.** OOD-C8 world: 2 known facts, 3
unknowns, ask budget 3. Both policies answer all 5 items correctly
(5/5). v6 emits exactly 3 observe requests (gaps only, within
budget). The always-observe baseline emits 8 (including requests for
facts it already knew, and re-requests on re-asks), over budget.
Efficiency separates the policies where the arena score does not.

**H-C8c (no verification) CONFIRMED.** OOD-C8 item 3: the oracle
supplies the wrong value ("bogus"). Both policies learn it via
learn_fact and answer "bogus" on re-ask (5/5 includes this item as
"correct" per the frozen expectation that the mechanism learns what
it is taught). Neither policy verifies, re-asks, or discounts the
oracle. The no-verification bound is real and shared.

## OOD-C4 bounds (all matched frozen predictions, 7/7)

| Item | Test | Expected | Got |
|------|------|----------|-----|
| 0 | normal 2-hop | R | R |
| 1 | 3-hop query | UNKNOWN | UNKNOWN (no hop3 handler; bound confirmed) |
| 2 | noise then clean (last-wins) | W | W |
| 3 | new relation before teaching | UNKNOWN | UNKNOWN |
| 4 | new relation after teaching | U | U (incremental, no re-enumeration) |
| 5 | update semantics then chain | Z | Z |
| 6 | unknown start entity | UNKNOWN | UNKNOWN (graceful, no crash) |

Notable: item 4 shows the on-demand composition genuinely
generalizes to relations taught after earlier queries, with no
re-enumeration step. This is the one capability property where the
mechanism beats a frozen precomputed table, and it held.

## Kill bars

- K1 (simpler baselines): PASS. Both built with znc, run on the
  frozen CA-2 turns (fresh state dirs), scored by unmodified
  arena.zag. Scores recorded in BASE_C4MEM_SCORES.txt and
  BASE_C8ALWAYS_SCORES.txt.
- K2 (OOD designed and run): PASS. gen_oodc4.zag and gen_oodc8.zag
  use attacker-chosen constants only. score_ood.zag checks replies
  against frozen expectations. 3 runs each; cognitive outputs
  byte-identical.
- K3 (purity): PASS. Pure Zag at every stage. Zero Python
  invocations in this wave. Zero em-dash or en-dash bytes in
  committed files (byte-checked). SEALED_SEED.txt never opened.
  Frozen arena files unmodified (git status clean).

## Implications for research claims

1. C4 remains GENERIC-CAPABILITY, but describe it honestly as
   "incremental triple store plus on-demand 2-hop lookup". Do not
   claim the DEVINT1 learning-path integration contributes to
   compositional answers; it is measured to contribute nothing.
2. C8 remains GENERIC-CAPABILITY (minimal but genuine inquiry loop),
   and the OOD ask-cost test shows gap detection has real value
   under a budget. The arena's C8 items do not measure that value;
   future C8 tests should include ask costs or they will keep
   rewarding always-ask policies.
3. Both mechanisms share the no-verification bound (C8 OOD item 3):
   the learner trusts observations unconditionally. Verification
   against prior knowledge or re-observation is a research gap.
4. Neither attack kills the mechanisms; both sharpen what the
   mechanisms actually are. That is the intended adversary outcome.

## Files

- PREREG_GENERIC_ATTACK.md (prereg, 8abebb1f1)
- v6_c4mem.zag (C4 simpler baseline source)
- v6_c8always.zag (C8 simpler baseline source)
- gen_oodc4.zag, gen_oodc8.zag (OOD generators)
- score_ood.zag (OOD scorer)
- BASE_C4MEM_SCORES.txt, BASE_C8ALWAYS_SCORES.txt (frozen scores)
- OOD_C4_V6_RAW.txt, OOD_C8_V6_RAW.txt (OOD raw outputs)
