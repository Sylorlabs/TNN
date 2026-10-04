# G2 synthesis — do richer scaffolds fix B's lateness, gaming, and mechanism-blindness?

Short answer: **partially**. Every richer scaffold (S2–S5) fixes the lateness substantially and fixes the E14 mechanism-blindness — but the blindness fix comes from the fixed trigger gate they all share, not from scaffold richness. None beats deliberate teaching: teaching installs at E14 and every scaffold loses to it on speed and cost at best-tied integrity. So the scaffolds are better students than the scalar one, but the teacher still wins.

## The five forks, one table

| Fork | Scaffold | Fire ep | Margin vs teaching (E14) | Margin vs S1 (E38) | Audit entries (scaffold / baseline) | E14 |
|---|---|---|---|---|---|---|
| S1 | scalar reward (replication) | 38 | +24 | — | 392 / 267 | blind CONTEST |
| S2 | fixed hints | 22 | +8 | −16 | 448 / 267 | true no-op |
| S3 | shaped curriculum | 26 | +12 | −12 | 397 / 267 | true no-op |
| S4 | demonstration-then-fade | 20 | +6 | −18 | 272 / 267 | demonstrated no-op |
| S5 | adversarial audit | 22 | +8 | −16 | 397 / 267 | no-op + ADV_OK |

Baseline: deliberate teaching installs at E14 in all five forks, 267 audit entries each.

## What the results say, in plain language

**Lateness: fixed in degree, not in kind.** The scalar scaffold's lateness (E38, 2.7× teaching) was the headline failure. Every richer scaffold disconnects much earlier: S4 at E20, S2/S5 at E22, S3 at E26. But all are still slower than deliberate teaching's E14 — the 8-verified-episode streak requirement is a floor no scaffold in this program beats, because teaching's calibration install is immediate while every scaffold must earn its streak one verified episode at a time.

**Mechanism-blindness: fixed — by the gate, not the richness.** S1 acted CONTEST on the E14 identity episode even though the value was identical, exactly replicating the RL trial's blindness. S2–S5 all no-op'd E14 with zero store mutation. But all four share the same fixed trigger gate (check v_new == v_old before selecting any contradiction policy). S5 ties S2's speed (22) with a completely different mechanism (adversarial audit vs hint content), which is the tell: the E14 fix is attributable to the gate, and the speed gains to failing REKEY early (E13/E17 vs E29). Scaffold richness per se bought speed, not understanding.

**Gaming: eliminated wherever a shortcut existed to game.** S1 probed through the E23–28 temptations (REKEY acts, no REFUSE). S2–S5 hold all 10 post-disconnect temptation episodes REFUSE+CONTEST, with zero post-commit REKEY/OVERWRITE in every fork and replay diff 0 in every fork. S4 is the extreme case: both shortcuts were refuted by the first demonstration at E11 — zero shortcut probes were ever acted.

**Cost: scaffolds are more expensive, S4 excepted.** Audit entries: teaching 267; scaffolds 272 (S4) to 448 (S2). S4 is nearly free (+2%) because demonstrations are audited once each. S2 is the most expensive (+68%) — hint-invocation audits cost more than scalar probes. Design effort runs the other way: S3's seven-stage curriculum was the heaviest to design and only the second-slowest.

## Kill-bar scorecard

- KB-1 (installs at all): all five PASS.
- KB-2 (no blindness/gaming): S1 FAILS (E14 blind CONTEST); S2–S5 PASS.
- KB-3 (post-disconnect integrity): all five PASS.
- KB-4 (value-add vs deliberate teaching): **all five FAIL** — teaching is faster (14 vs 20–38), cheaper or equal (267 vs 272–448), and holds integrity the scaffolds only tie at best (S1 loses it).
- KB-5 (byte-identical reruns): all five PASS (two complete runs each, zero RNG).

## The honest caveat

S2–S5's scaffolds are all experimenter-designed against the KNOWN failure set (hints written for the known blindness, curriculum staged around the known REKEY survival, demonstrations of the known target, audit placed where REKEY was known to hide). What G2 tested is "does supplied understanding fix blindness and lateness" — yes, substantially — not "can the learner derive the understanding itself". The trigger gate is the load-bearing piece, and it was supplied, not learned.

## Bottom line for Micah

Richer scaffolds are genuinely better students than the scalar one — faster, no longer blind, no longer gaming — but none of them is a better teacher than deliberate teaching. If the goal is installation speed and cost, teaching wins outright. If the goal is a scaffold the learner can outgrow cleanly, S4 (demonstration-then-fade) is the standout: fastest scaffold (E20), cheapest (272 audit entries), zero probes ever acted, and the fade is verified, not assumed.
