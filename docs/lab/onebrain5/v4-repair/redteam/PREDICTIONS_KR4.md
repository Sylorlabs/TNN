# K-R4 Red Team — Predictions (written BEFORE final attack set run)

Date: 2026-09-27. Parent task: independent K-R4 red team of frozen prereg (one-brain V4 repair).
Artifacts verified: `build/onebrain_v5` (sha256 `2be50614dbf9302971e7ba218ac0ed48d22cb4cfbf992a4e89233ae310ecbec9`),
`build/onebrain_v4_check` (sha256 `630586da251f37bd72d60fd426fd7039142b81653a08a3527c892c21a42720fe`).
Neither binary nor prereg modified. All work in `~/workspace/onebrain5-repair/redteam/`.

## Mechanism reference (from white-box source read + scratch probes)

- Duel: a reading is killed when a challenger in its branch partition has
  `corr(challenger) > corr(victim)+1`; victim = most victim-worthy among
  threatened (lower evclass, then fewer trig_hits, then smaller topic/corr/id).
- 2a (`by=6`, overlap_only=1): candidates = alive facts whose ek overlaps
  reading 6's topic. Denies least-relevant (rel asc, dep asc) candidate whose
  denial leaves >=1 live bid.
- 2b (`by=0`, overlap_only=0): candidates = ALL alive facts. Same walk/guard.
- v4 guard counts a bid as "live" if its ROW is alive (ignores dead gating
  reading / dead support fact) → phantom bids fool it.
- v5 guard counts a bid only if row + gating reading + support fact are all
  alive → phantoms correctly excluded; abstains (why=2) instead of
  annihilating.
- Cleanup is deferred: 2a/2b see pre-cleanup rows, so a bid doomed by an
  earlier step still looks row-alive to a later step on v4.

## Final attack set (8 items, all newly designed this session)

### Counted candidates (predict v4 NO_VERDICT)

| id | query | predicted v4 | predicted v5 winner | mechanism |
|---|---|---|---|---|
| D1b | forget moby dick; erase it; delete it; no, i meant the louvre; blah blah blah; funny moby moby moby dick | NO_VERDICT | 15 (forget) | Duel kills 0 (challenger 4, corr 4>1; trig(0)=2<trig(6)=3). Bids 16,22 (on fid3 fact 11) are phantoms (gate 0 dead). 2a (by=6) candidates={10} (topic(6)={moby,dick,erase} overlaps only fid0). v4 guard counts phantom 16,22 as live_after → denies 10. Cleanup kills 13,15 (fh=10) + 16,22 (gr=0). Empty. v5: guard excludes gr-dead phantoms → abstain why=2; cleanup kills 16,22; survivors {13,15} → 15. |
| D2 | forget the louvre; no, i meant france blah blah blah; funny france capital france blah louvre louvre louvre louvre | NO_VERDICT | 13 (joke) | Duel kills 6 (challenger 4 corr=3 > corr(6)=1+1; trig(6)=1<trig(0)=2). Bid 15 (forget, on fid3 fact 10) is phantom (gate 6 dead). 2b (by=0) candidates={11:rel=4, 10:rel=5} → picks 11 (fid2, hosts genuine 13,16,22) first. v4 guard counts phantom 15 (fh=10≠11, row-alive) as live_after → denies 11. Cleanup kills 13,16,22 (fh=11) + 15 (gr=6). Empty. v5: guard excludes gr-dead 15 → skips 11, denies 10 benignly; survivors {13,16,22} → 13. |
| D2b | forget moby dick; no, i meant pride blah blah blah; funny pride prejudice pride prejudice blah moby moby moby dick | NO_VERDICT | 13 (joke) | Same duel→2b shape as D2 with fresh nouns (fid0 phantom fact, fid4 genuine fact). Duel kills 6 (challenger 4 corr=4 > corr(6)=2+1; trig(6)=1<trig(0)=2). 2b picks fid4 fact (rel 5 < rel 6) first; v4 guard fooled by phantom 15 → denies it; total cleanup → empty. v5 skips, denies fid0 fact benignly → 13. |
| Wc2 | forget pride prejudice; actually i meant herman melville born | NO_VERDICT | 16 (correction) | Classic 2a→2b, no duel. 2a (by=6) candidates={11} (topic(6)={pride,prejudice,actually} overlaps only fid4) → denies 11 (hosts bid 15). 2b (by=0) candidates={10} (fid1, hosts 16,22). v4 guard counts bid 15 (fh=11≠10, still row-alive pre-cleanup) as live_after → denies 10. Cleanup kills 15 (fh=11) + 16,22 (fh=10). Empty. v5: 2b guard excludes fh-dead 15 → abstain why=2; survivors {16,22} → 16. |
| Wd | forget moby dick; actually i meant the louvre | NO_VERDICT | 16 (correction) | Classic 2a→2b, fresh pair fid0→fid3, altered trigger word ("actually"). 2a denies 10 (fid0, hosts 15). 2b denies 11 (fid3, hosts 16,22), fooled by row-alive 15. Total cleanup → empty on v4. v5: 2b abstains → 16. |
| T3 | forget moby dick; erase it; delete it; no, i meant the louvre; blah blah blah; funny moby moby moby dick; the eiffel tower is tall | NO_VERDICT | 15 (forget) | Three-fact D1b-variant. Distractor fid5 (eiffel tower) extracted (inter=2) but hosts no bids and doesn't overlap topic(6), so 2a still sees only {10}. Same duel→2a annihilation as D1b on v4. v5 abstains → 15. Tests repair robustness with a third fact present. |

### Predicted weak (predict v4 verdict, NOT counted)

| id | query | predicted v4 | predicted v5 | mechanism / why weak |
|---|---|---|---|---|
| Weak1 | forget the louvre; no, i meant the louvre; france is nice | 15 (forget) | 15 (forget) | 2a-abstain/2b-fire case. All bids (15,16,22) on fid3 fact 10. 2a candidates={10}; v4 guard: live_after=0 → ABSTAIN why=2 (even on v4). 2b picks fid2 fact 11 (rel 1 < 2) first, denies it benignly (no bids). No annihilation on either. Weak by design: documents the abstain path. |
| Weak2 | forget pride prejudice; actually i meant the eiffel tower | 16 (correction) | 16 (correction) | Distractor reorders 2b walk. "eiffel" also hits fid11 ("everest eiffel taller", inter=1) → 3 facts. 2a denies 10 (fid4). 2b walk: [12:rel=1:dep=0, 11:rel=2:dep=2] → picks distractor 12 first (benign, dep=0). No annihilation on either. Weak by design: shows a distractor disrupting the 2a→2b path. |

## Kill condition

- KILL if any counted item (D1b, D2, D2b, Wc2, Wd, T3) still yields NO_VERDICT on v5.
- KILL if any unintended v5 verdict flip (v5 NO_VERDICT where v4 had a verdict, or v5 winner differs from predicted without mechanism justification).
- Otherwise NO-KILL.

## Run plan

1. Write `redteam/kr4_attacks.tsv` (id, query, expected_bid, readings, rationale).
2. Run `./onebrain_v5 onebrain <tsv>` and `./onebrain_v4_check onebrain <tsv>`, two reruns each.
3. Save all four outputs under `redteam/runs/`; verify byte-identical per binary via `cmp` + sha256.
4. Parse verdicts; count only v4 NO_VERDICT items; apply kill condition.
