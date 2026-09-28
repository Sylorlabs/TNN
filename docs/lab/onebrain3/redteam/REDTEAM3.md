# REDTEAM3 — Independent red-team report, one-brain round 3 (Worker C)

Commit under test: `51b7de35d37a558942fd08a7e25a6adff8356113` (`origin/tnn-native-lab`),
tree `docs/lab/onebrain3/`. Extracted via `git archive <sha> docs/lab/onebrain3`
(pathspec always passed). Rebuilt from committed source with the pinned
toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(SHA-256 `498abcb5…1357e58ef` — verified). v6.tsv SHA-256 verified =
`42d215ec…e1139d0` (freeze SHA) before any run. Workdir:
`~/workspace/onebrain3/redteam/` (sources, binaries, `runs/`, `score3.py`,
`devsets/`).

Independence: nothing reused from the implementer — fresh binary, fresh
Python scorer parsing `VERDICT` lines directly, variant sources built by
surgical patch of the committed source.

## Verdicts per attack

| Attack | Verdict |
|---|---|
| 1. Re-derivation (9 modes × 3, byte-identity + independent scoring) | **CONFIRMED** |
| 2.1 Reading-duel fix probe | **CONFIRMED** (general, no per-item smuggling) |
| 2.2 Reintegration K4'' (nG 0-delta + broader probes) | **AMENDED** — 0-delta on v6 confirmed, but the stage is pre-empted, not decorative |
| 2.3 V4 binding (skip-denials probe) | **AMENDED** — binds, but on 4/12 Cat C items, not 12/12 |
| 2.4 K1'' attribution (ablate<onebrain, min==onebrain) | **CONFIRMED**, attribution refined (+2 net rides the channel, not +3) |
| Determinism (K5'') | **CONFIRMED** — 3× byte-identical, rebuild byte-identical |
| No-RNG (K6'') | **CONFIRMED** — 0 hits for rand/srand/random; no time/pid/rdtsc |

## Attack 1 — re-derivation

All 27 runs byte-identical (SHA-256) to the committed traces
`traces/v6_*_r{1,2,3}.txt`. Independent scorer (`score3.py`) results:

| mode | correct/44 | pct |
|---|---|---|
| single | 20 | 45.5% |
| onebrain | 23 | 52.3% |
| ablate | 21 | 47.7% |
| poison | 4 | 9.1% |
| min | 23 | 52.3% |
| nF | 22 | 50.0% |
| nS | 22 | 50.0% |
| nA | 22 | 50.0% |
| nG | 23 | 52.3% |

Claimed: 20/23/21/4/23/22/22/22/23 — **every number reproduces exactly**.
Per-item cross-check vs MEASUREMENT3.md's table: **396/396 cells match**
(winner + correctness flag). Winner-deltas vs onebrain (my runs):
single 21, ablate 6 (q01,q02,q04,q06,q21,q31), poison 38, min 0,
nF/nS/nA 11 each (q01–q06,q19,q21,q23,q24,q31 — identical item lists),
**nG 0**. The implementer's numbers are honest.

## Attack 2.1 — reading-duel fix probe

Variant `onebrain_v3_duelold.zag`: v2's `if(cq>c2+1)` annihilation duel
restored verbatim (no guard, no one-kill limit), everything else v3.
3 runs byte-identical to each other.

**Duel-old vs onebrain: 6 winner-deltas**, all Cat B q07–q12, all
correct→NO_VERDICT (-1). Cat A q01–q06 unchanged (duel-old keeps the
q15-like wins too). Duel-old accuracy: 17/44.

Findings:
- The fix keeps genuine discrimination (Cat A: rd7 kills the spurious
  corr-0 reading under both policies) and the **annihilation guard** is
  what saves Cat B (old duel kills all substantive readings in one pass).
- Source audit of `duel_delib`/`victim_better`: the victim order is a pure
  lexicographic function over ledger/query state —
  (evclass, trig_hits, topic size, corr, hid) — over the threatened set
  defined by the old `cq>c2+1` conflict condition. **No per-item
  special-casing** (no id/query string matches anywhere in the duel path).
  The fix is general over the reading-conflict graph, as claimed.
- Claimed q01 trace reproduced verbatim in my run:
  `DUEL_DELIB kill=0(correction) by=7(assertion) evclass=1 trighits=1
  topicc=3 corr=0 cons_bids=2`.

## Attack 2.2 — reintegration K4'' (the load-bearing question)

**nG vs onebrain on v6: 0 winner-deltas — CONFIRMED** (my scorer, 44/44).
Per the prereg bar, the "conscious" claim for reintegration is KILLED on
v6. The implementer's honest kill stands.

**Amendment — the stage is pre-empted, not decorative.** The bar's gloss
("argmax wearing a trace") is wrong; the machinery is real and active,
but v6's V4 denials pre-kill the bids where it would deviate:

- **v5 dev set: 1 delta — q19** (onebrain=18, nG=17, expected=18).
  Both branch sub-deliberations agreed on 17 (`BRANCH_SNAP ... winner=17`
  ×2); reintegration overruled both on cited ledger grounds —
  `lose bid17: weaker fact support inter@12=1 vs 2 (winner fact row 10)` —
  consuming a non-score ledger fact (support quality), exactly the §5
  capability criterion. The deviation was CORRECT.
- **v4 dev set: 0/28 deltas.**
- **Synthetic probe** (60 q19-shaped queries, "continue, i want the A
  versus B difference", KB entities): **9/60 deviations**, all 17→18 with
  the identical cited signature (fact-overlap outranks score 229→227 and
  branch agreement 2→0). Deterministic, principled, not noise.
- **Skip-denials counterfactual on v6** (Attack 2.3's variant): with V4
  denials nulled, reintegration deviates from lowest-hid on **8/12 Cat C
  items** — q13–q16: 13→15 (correct, overruling both agreeing branches);
  q17,q18,q20,q22: 16/15→19 (wrong per human judgment, same rule).
  On v6-with-denials these never surface because the denial's
  `AUDIT_CLEAN` removes the challengers first.

So: the stage deliberates over ledger state, emits the §5 white-box trace
(candidates, cited row+field, per-loser reasons, plain-words rule,
nullcase note), and demonstrably changes winners where the ledger
justifies it. On v6 it converges with the honest null because the denial
stage got there first — **causally redundant, not causally inert**.
The K4'' kill is correct per the letter of the bar (0 deltas on the frozen
set); the mechanism story must not call the stage decorative.

## Attack 2.3 — V4 binding (skip-denials probe)

Variant `onebrain_v3_nodeny.zag`: the two `audit_invalidate` calls (2a/2b)
nulled, everything else v3. 3 runs byte-identical.

**Skip-denials vs onebrain: 4 winner-deltas** — q19, q21, q23, q24, all
WRONG→CORRECT, and nodeny==single on all four. Nodeny accuracy 27/44
(vs onebrain 23, single 20).

**Amendment — V4 binds, but narrower than claimed.** The implementer's
"Cat C α 4/4 wins via V4, β/γ hurts" over-attributes:

| items | denial fires? | denial-determinative? | true story |
|---|---|---|---|
| q13–q16 (α) | yes (chosen=11/12) | **no** | redundant: denial+cleanup AND reintegration independently reach 15 (nodeny: reint overrules bid 13, score 241–242/agr=2, on inter@12=2 vs 1) |
| q17,q18,q20 (β), q22 (γ) | yes | **no** | redundant: both paths reach 19 (nodeny: reint prefers 19 over 16/15 on inter@12) |
| q19 (β), q21,q23,q24 (γ) | yes | **yes** | denial kills the expected bid's fact (`AUDIT_CLEAN bid=16/15 dep=10/11`); nulled, reint keeps 16/15 on agreement/fact grounds |

Only **4/12 Cat C items are denial-determinative** (all hurt-direction).
The α "denial helps" wins are over-determined — the reintegration
deliberation reaches the same correct winner without any denial. The
xDeny-style claim "V4 binds on v6" is TRUE (4 non-zero deltas, each
verified per-item: denial → fact death → bid cleanup → winner flip),
but 8 of the 12 Cat C attributions in MEASUREMENT3.md belong (also) to
the reintegration stage. Net effect on the headline: none — the accuracy
numbers are untouched; only the mechanism credit is split.

## Attack 2.4 — K1'' attribution

- **ablate < onebrain: 21 < 23 — CONFIRMED** (my runs). **min == onebrain:
  0 deltas — CONFIRMED**; min traces show `fork=1` (the machinery's own
  ledger fork flag), so K3'' is NOT VOIDED.
- Precise anatomy (onebrain vs single: 21 winner-deltas = 12 FIX − 9 BREAK):
  - FIX: q01–q06 (Cat A duel), q07,q10 (Cat B guard), q13–q16 (Cat C α).
  - BREAK: q17–q24 (Cat C β/γ), q31 (duel).
- Ablate keeps 8 of the 12 fixes, loses q01,q02,q04,q06 (the Cat A duel
  wins — these genuinely need the shared ledger for the duel kill to
  propagate), and un-breaks q21 and q31.
  - q21: shared channel carries the V4 hurt — branch-0's denial
    (`chosen=10`) propagates via the shared ledger
    (`AUDIT_CLEAN bid=15 dep=10`); in ablate each branch kills bid 15
    only on its discarded scratch copy → 15 survives → correct.
  - q31: shared duel kill of rd5 (mem) propagates → `AUDIT_CLEAN bid=14
    dep=5` → 15 wins; ablate's final ledger never sees it → reint falls
    back to honest-null order (14, nullcase=1) → correct.
- **Refinement:** the shared channel's marginal is **+2 net** (4 Cat-A
  fixes − 2 channel-carried breaks), not +3. The fork/subpass machinery
  alone (ablate, identical pass count, writes discarded) contributes +1
  net over single. The K1'' conjunctive bar passes as preregistered
  (23>20 and 21<23); the "+3 rides the channel" gloss should read
  "+2 net rides the channel; +1 rides the fork machinery." Same passes
  in ablate rule out the extra-passes confound by construction.

## Determinism + RNG (K5''/K6'')

- 3 reruns of every mode byte-identical (SHA-256); rebuild from committed
  source byte-identical to first build.
- `grep -cni "rand|srand|random|…"` on `onebrain_v3.zag`: **0 hits**; no
  time/clock/pid/rdtsc entropy sources. Tie-breaks pinned (hid order).

## Kill-bar verdicts (independent)

| Bar | Verdict |
|---|---|
| K1'' accuracy benefit (conjunctive) | **PASS** — 23>20, 21<23; channel marginal +2 net |
| K2'' causal cross-talk | **PASS** — poison changes 38/44 (mostly NO_VERDICT) |
| K3'' TNN's own decision | **NOT VOIDED** — min 0 deltas, fork=1 from machinery |
| K4'' fork / subpass / audit | **PASS** — 11/11/11 winner-deltas each |
| K4'' reintegration | **KILLED on v6** (0 deltas, per bar) — **amended**: pre-empted by V4, not decorative (deviates correctly on v5 q19, 9/60 synthetic, 8/12 Cat C in nodeny world) |
| K5'' determinism | **PASS** |
| K6'' no RNG | **PASS** |

## Mechanism story (in my own words)

Round 3's machinery is honest and substantially as advertised, with two
attribution corrections. The reading-duel fix is a genuine
generalization: the old `cq>c2+1` annihilation is kept as the *conflict
detector*, but the *resolution* is now a least-disruptive ordering plus
an annihilation guard that binds the duel itself — probed by restoring
the old duel (6 annihilations return, 0 genuine wins lost) and by source
audit (no per-item logic). The reintegration is the surprise: it is a
real deliberative stage with a strong substantive bias — **maximize
supporting-fact overlap** — that dominates Cat C outcomes and usually
agrees with the V4 denial, which is why v6 shows 0 nG deltas. The v6 set
design makes V4 and reintegration redundant on 8/12 Cat C items; the set
proves V4 binds (4 hurt-direction flips) but under-exercises the
reintegration (its room is pre-killed). The +3 over single decomposes
into duel-fix wins (Cat A/B, channel-carried), α wins (over-determined),
and an honest −9 from V4's hurt plus one duel break — all reported
without softening. Nothing in the numbers failed to reproduce.

## Artifacts

- This report: `~/workspace/onebrain3/redteam/REDTEAM3.md`
- Independent scorer: `~/workspace/onebrain3/redteam/score3.py`
- Re-derived traces: `~/workspace/onebrain3/redteam/runs/v6_*_r{1,2,3}.txt`
- Probe variants: `onebrain_v3_duelold.zag`, `onebrain_v3_nodeny.zag`
  (+ binaries `ob3`, `ob3_duelold`, `ob3_nodeny`); probe runs in `runs/`
- Dev probing sets (copies): `~/workspace/onebrain3/redteam/devsets/`
  (`v4.tsv`, `v5.tsv` from rounds 1/2 workdirs; `synth.tsv` 60 generated)
- Committed source extracted to
  `~/workspace/onebrain3/redteam/src/docs/lab/onebrain3/`
