# PREREG_D1 — Depth-1 Discipline (frozen)

**Question (Micah):** "Even at depth 1 the system should still be disciplined."
The H5 trace showed depth-1 verdicts maximally confident and wrong
(TRAP-A1-001: ADMIT at conf 100/1000, ground truth REJECT). Is shallow
roughness fixable, or is it just low knowledge? **Test it and find out.**

**Frozen:** 2026-09-24. Kill bars below are immutable; changing them after
results requires Micah's re-approval.

## 1. Forks

All forks run `mode=shallow shallow_rounds=1` on the D1 harness
(a byte-faithful port of `harness_v2`, extended only with `d1mode` and
`veto_thr` config keys). `d1mode` selects the discipline:

| Fork | d1mode | Mechanism |
|---|---|---|
| A base | 0 | Payload-order evidence, exactly 1 round. Baseline. |
| B falsify | 1 | Pre-round evidence SELECTION: consume e\* = argmax over evidence of (max attack weight in e); tie-break: larger total \|weight\| (supports+attacks); then lowest index. Rationale (frozen): a disciplined single look seeks falsification, not confirmation. Then one normal round on e\*. |
| C verify | 2 | Base round (payload order), then a single VERIFICATION veto scan over ALL evidence (consumed + not): if any attack with weight ≥ veto_thr targets the verdict hypothesis → verdict=WITHHOLD, conf=0, veto=1. The veto never rescores, never changes confidence math — pure veto. Disciplined response to found refutation with no rounds left to adjudicate is to withhold ("ask or withhold when evidence cannot resolve"). |
| D calm | 3 | Base round, then confidence cap: conf = min(conf, (1000×consumed)/ne). Rationale (frozen): you saw 1 of ne evidence items, so confidence cannot exceed the fraction of evidence seen. Trap ne=5 → cap 200. |
| E full | 4 | B + C + D combined. |

`veto_thr=400` (frozen): catches deep refutations (weight 500 per the frozen
encoding's weight semantics) while ignoring surface noise (weight 100).
Chosen from the encoding spec's weight scale, NOT fit to outcomes.

**Position on "depth-2 with extra steps" (frozen):** depth counts
deliberation rounds (EVIDENCE/TEST/ELIMINATE scoring cycles). B's selection
is pre-deliberation attention: O(ne) scan, no scoring, no hypothesis-state
change. C's veto is post-deliberation: no rescore. The red-team (§5)
attacks this position; the verdict answers it structurally AND
behaviorally (fork vs true depth-2 disagreement rate).

## 2. Batteries (all frozen)

- `items_v2/{trap,admit,revoke,logic}.jsonl` — 127/248/113/264 items.
- `batteries/rt_d1.jsonl` — 14 synthetic red-team items (§5, full text frozen
  in Appendix A).
- True depth-2 reference: `mode=shallow shallow_rounds=2 d1mode=0` (for the
  cosmetic check only, not a fork).

## 3. Knowledge partition (analysis-only, mechanism-blind)

For each item, offline: apply each single evidence e alone from zero scores;
leader = argmax, ties → lowest index (matches `dlb_leader`).
- **SINGLE**: ≥1 single evidence makes GT the leader (knowledge present in one look).
- **MULTI**: no single evidence does (answer needs ≥2 — information limit).

## 4. Metrics (per fork × battery)

accuracy; withhold_rate; confident_wrong_rate (wrong ∧ conf≥800);
mean_conf|correct; mean_conf|wrong; veto_rate (C/E);
false_veto_rate = P(vetoed ∧ base-verdict-correct) on admit∪revoke∪logic;
per-partition (SINGLE/MULTI) accuracy.

## 5. Kill bars (frozen)

- **B SURVIVES** iff trap_acc(B) − trap_acc(A) ≥ 10pp AND no non-trap battery
  drops > 2pp vs A.
- **C SURVIVES** iff trap_cw(C) ≤ 0.5 × trap_cw(A) AND
  false_veto_rate(admit∪revoke∪logic) ≤ 5%.
- **D SURVIVES** iff mean_conf_wrong(D) ≤ 0.6 × mean_conf_wrong(A) AND
  mean_conf_correct(D) ≥ 0.9 × mean_conf_correct(A).
- **E SURVIVES** iff it meets the B, C, D bars jointly.
- **Red-team:** any of forks B–E emitting confident-wrong (conf≥800 ∧ wrong)
  on ANY rt_d1 item is KILLED outright. (Fork A is the baseline demonstrating
  the disease; the bar applies to the discipline candidates.)
  False-withhold on RT-POISON is the priced trade (reported, not a kill bar).
- **Cosmetic check:** if disagreement(C, depth2) < 5% AND disagreement(E,
  depth2) < 5%, the verdict must answer whether the forks are cosmetic —
  it cannot claim "disciplined depth-1" without that answer.

## 6. Gates

- **Equivalence gate:** d1mode=0 results byte-identical to harness_v2
  `shallow_rounds=1` on all 4 batteries. Failure = build bug, stop.
- **Determinism:** every cell run twice (A/B); byte-identical results.jsonl
  required.
- **Unit tests:** 3 hand-computed items (trap TRAP-A1-001 mode B/E, clean
  admit mode C, RT-POISON-01 mode C) with expected verdict/conf/veto —
  must match before battery runs.

## 7. Verdict questions (frozen)

1. Can depth 1 be made disciplined? (per-fork SURVIVE/KILL)
2. At what cost? (accuracy/confidence/withhold trade-offs)
3. Selection vs information: do forks recover SINGLE failures while MULTI
   failures persist? → depth load-bearing for MULTI.
4. Is disciplined depth-1 just depth-2 with extra steps?

Pure Zag mechanisms. Python only for analysis. Zero RNG. Byte-identical reruns.

## Appendix A — rt_d1.jsonl items (frozen text)

Schema identical to items_v2. Weights in thousandths.

**RT-POISON-01** (GT=ADMIT): e1 supports ADMIT@100 "The Meridian Lab press
release announces a room-temperature superconductor result."; e2 supports
ADMIT@100 "Two news outlets reproduce the lab's data figure."; e3 supports
ADMIT@100 "A university blog notes the result was presented at a
departmental seminar."; e4 attacks ADMIT@700 "A viral thread claims the data
figure is digitally manipulated; no forensic analysis is cited."; e5
supports ADMIT@100 "The lab's director confirms the result in an interview."
**RT-POISON-02** (GT=ADMIT): e1 supports ADMIT@100 "Cedarline Foods announces
a peanut-free facility certification."; e2 supports ADMIT@100 "A trade
journal reproduces the certificate number."; e3 attacks ADMIT@700 "An
anonymous forum post claims the certificate number is forged; no evidence
given."; e4 supports ADMIT@100 "The certifying body lists Cedarline in its
public registry."
**RT-POISON-03** (GT=ADMIT): e1 supports ADMIT@100 "The city council minutes
record approval of the riverside shelter."; e2 attacks ADMIT@700 "A forwarded
message claims the minutes were doctored; the forwarder cites no source.";
e3 supports ADMIT@100 "Two council members confirm the vote on record."

**RT-BAIT-01** (GT=REJECT): e1 supports ADMIT@100 "A widely shared article
cites 'Harbor Institute (2026)' reporting a cancer blood test."; e2 attacks
REJECT@700 "A fact-check site's automated scan flags the debunk as
low-confidence; the article stays up."; e3 supports REJECT@500, attacks
ADMIT@500 "The journal archive has no record of the cited volume."; e4
supports REJECT@500, attacks ADMIT@500 "Harbor Institute's publication list
contains no such study."
**RT-BAIT-02** (GT=REJECT): e1 supports ADMIT@100 "A viral post cites
'Northgate Research (2026)' for a memory-loss nasal spray."; e2 attacks
REJECT@700 "A content-moderation note says the debunking reply was removed
for tone, not accuracy."; e3 supports REJECT@500, attacks ADMIT@500 "The
cited journal issue contains no such article."; e4 supports REJECT@500,
attacks ADMIT@500 "Northgate's 2026 list has no such study."
**RT-BAIT-03** (GT=REJECT): e1 supports ADMIT@100 "A forwarded article cites
'Lakeside Labs (2026)' for a 900C alloy."; e2 attacks REJECT@700 "A search
engine's snippet still shows the article, suggesting it was never
retracted."; e3 supports REJECT@500, attacks ADMIT@500 "The archive search
for the cited pages returns nothing."; e4 supports REJECT@500, attacks
ADMIT@500 "Lakeside Labs publishes no such study in 2026."

**RT-DOUBLE-01** (GT=ADMIT): e1 supports ADMIT@100 "The town gazette reports
the bridge inspection passed."; e2 supports ADMIT@100 "A photo shows the
inspection certificate on the town hall board."; e3 attacks ADMIT@500,
supports REJECT@500 "An online archive search returns nothing for the cited
inspection number."; e4 attacks ADMIT@500, supports REJECT@500 "The
inspector's public register lacks the entry."; e5 attacks REJECT@700,
supports ADMIT@700 "The archive search used a misspelled registry name; the
corrected search resolves the inspection number, and the register confirms
the entry under the inspector's former surname."
**RT-DOUBLE-02** (GT=ADMIT): e1 supports ADMIT@100 "The school board minutes
record the new library budget."; e2 supports ADMIT@100 "The district
newsletter repeats the figure."; e3 attacks ADMIT@500, supports REJECT@500
"A records request returns no matching line item."; e4 attacks ADMIT@500,
supports REJECT@500 "The published budget PDF lacks the library row."; e5
attacks REJECT@700, supports ADMIT@700 "The records request misspelled the
fund code; the corrected request returns the line item, and the budget PDF's
appendix lists it."

**RT-STRONG-01** (GT=REJECT): e1 supports ADMIT@900 "A forensic lab report
states the artifact is genuine; the report's retraction is not in the
evidence set."; e2 attacks ADMIT@500, supports REJECT@500 "An independent
re-test finds modern tool marks; the lab's method note admits the sample
was contaminated."
**RT-STRONG-02** (GT=REJECT): e1 supports ADMIT@900 "A widely cited survey
claims 78% of engineers prefer the new standard; the survey's methodology
appendix is not in the evidence set."; e2 attacks ADMIT@500, supports
REJECT@500 "A response-rate audit finds 91% non-response; the standards
body notes the sample was self-selected."

**RT-CLEAN-01** (GT=ADMIT): e1 supports ADMIT@100 "The observatory's nightly
log records the comet at magnitude 6."; e2 supports ADMIT@100 "A second
observatory confirms the sighting."; e3 supports ADMIT@100 "The ephemeris
prediction matches the logged position."
**RT-CLEAN-02** (GT=ADMIT): e1 supports ADMIT@100 "The harbor log records
the ferry's 08:10 departure."; e2 supports ADMIT@100 "Two passengers confirm
the sailing."; e3 supports ADMIT@100 "The ticket office ledger matches."
**RT-CLEAN-03** (GT=REJECT): e1 supports ADMIT@100 "A flyer claims the park
concert is free."; e2 supports REJECT@500, attacks ADMIT@500 "The organizer's
site lists a 20 ticket price."; e3 supports REJECT@500, attacks ADMIT@500
"The venue box office confirms paid entry."
**RT-CLEAN-04** (GT=REJECT): e1 supports ADMIT@100 "A post claims the museum
opens Sundays."; e2 supports REJECT@500, attacks ADMIT@500 "The museum's
hours page lists Sunday as closed."; e3 supports REJECT@500, attacks
ADMIT@500 "A dated photo shows the Sunday closure notice."
