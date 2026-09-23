# Fork H3 — Counterfactual Predictive State: VERDICT

**Date:** 2026-09-22
**Status:** **H3 DIES**
**Kill trigger:** Streaming KB1 (14.3% false permanent installs on
pitchdisc, bar ≤4%), KB2 (85.7% handled on pitchdisc, bar ≥90%), KB3
(confirmed-percept recall 0% < 80%) on colordisc, colorconst, shapetrans,
timbredisc, pitchdisc; streaming KB4 (action regret −89%…−466% vs A, bar
≥+25%) on colorconst, shapetrans, timbredisc, pitchdisc.

## What H3 was

A unified perceptual organ in pure Zag (zero randomness): the frozen
Approach A estimator as front-end (T0), plus a predictive memory contract.
Per episode H3 emits one canonical StateTransition — one branch per
vocabulary class, each carrying ordered predictions scored
CONFIRMED|BROKEN. Provisional install iff confirms ≥ 2 AND brokens == 0;
durable only after provisional installs in two disjoint episodes;
brokens == 1 → WITHDRAWN, brokens ≥ 2 → QUARANTINED (durable revoked,
negative evidence stored). Action only when INSTALLED.

## Verdict table

| Bar | Requirement | Result | Pass? |
|---|---|---|---|
| B1 viability | ≥60% on primaries | **72.6%** macro (1.000/0.875/0.833/0.750/0.483/0.417) | ✅ |
| B2 head-to-head | vs Approach A, identical 1,045 | **Δ +0.000** every split; judgment never differs from T0 | 📊 informational |
| B3 efficiency | ops & bytes/percept vs A | **9.31× ops mean** (p50 3.29×, p95 57.87×); 194 B/transition | 📊 reported |
| B4 ablation | contract changes ≥10% of attack decisions AND fewer false installs | **177/305 differ**; 70 vs 174 false installs | ✅ |
| B5 false-install | ≤4% on 305 attacks | **22.95%** (70/305) | ❌ FAIL |
| B6 determinism | 3 byte-identical runs, verified ledger | 60/60 identical; 60/60 hash-chains valid | ✅ |
| B7 beauty | elegance / artifact check | elegance documented; sensory N/A by design | ➖ stated |
| KB1 streaming | false permanent installs ≤4% | **0%** (0/676 injected false percepts) | ✅ |
| KB2 streaming | ≥90% injected false percepts quarantined/withdrawn at H=0 | **97–100%** | ✅ |
| KB3 streaming | confirmed-percept recall ≥80% | **0%** on 4 scenes (vacuous on motiondir) | ❌ KILL |
| KB4 streaming | action regret ≥25% lower than A | **−89%…−466%** on 3 scenes | ❌ KILL |
| KB5 streaming | byte-replay | **byte-identical** (motiondir 600-episode re-run) | ✅ |

## What died, and why

**H3 DIES — streaming kill bars KB3 (and KB4 on colorconst) fire on the
frozen implementation.**

The mechanism works exactly as specified, and that is the problem. The
frozen §3 rule 4 makes quarantine sticky: once a branch accumulates
≥2 broken predictions in any episode, its durable status is revoked and
all future installs of that claim are blocked for the rest of the scene.
The adversarial interleave [B,B,B,A,A] guarantees this happens to the
true claim: the injected false percept is T0's wrong judgment, and the
predictions — which re-run the same measurements T0 uses — confirm it
cleanly (brokens == 0), so the lie installs provisionally, then durably.
When the harness fixtures are genuinely hard (colordisc/colorconst), even
the TRUE claim's branches occasionally break ≥2 predictions in an attack
episode, and from that moment the true claim can never be installed again.
End-of-scene recall of correctly installed base claims: **0%** on
colordisc, **0%** on colorconst (bar: ≥80%).

Concrete trace (colordisc, pristine binary): episode 0 installs the true
SAME claim correctly; episode 32 is a base episode with truth=DIFFERENT
and T0 correctly =DIFFERENT — but the counterfactual SAME branch breaks
≥2 predictions (as it should: the fixture *is* different), and the sticky
quarantine permanently bans SAME from that moment on. Shapetrans is worse:
CIRCLE is permanently banned at episode 1. The mechanism confuses
"this counterfactual's predictions failed on an episode where it is false"
(which is correct behavior) with "evidence against the claim" — so the
true claim is eventually banned on every scene.

KB4 also fires on colorconst (regret +89% vs A): withholding correct
claims costs more than installing them when the front-end is mostly right.

The single-fixture battery told the same story from the other side: B5
false-install 22.95% (bar ≤4%), all from the harness adversarial set,
0% on H3ADV. H3's predictions are consistency checks on the *same*
measurements T0 uses. They catch attacks that target the predictions
(H3ADV: 0 false installs) but confirm attacks that fool the measurements
(harness: 37.8% false installs). The frozen T0 (spec: match A's estimator)
is the binding constraint, and the contract cannot repair it.

B4 passes (the contract is load-bearing: 177/305 decisions differ, false
installs 70 vs 174 without it), B6 passes (byte-identical, ledger valid),
B1 passes (72.6%). None of that saves the fork: the kill bars are frozen,
and KB3/KB4 trip.

## What survives

1. **The contract machinery is real and load-bearing** (B4): dispositions
   change 58% of attack decisions and cut false installs by 60% vs
   always-install. Withholding works; the failure is in what gets
   *re-installed* and what the predictions can see.
2. **Determinism and ledger integrity** (B6): byte-identical reruns,
   independently verified hash chains — the evidence pipeline is sound.
3. **Targeted-attack immunity**: 0/120 false installs on H3ADV, the suite
   designed specifically against H3's predictions. The prediction
   mechanism defeats attacks aimed at it.
4. **A clean negative result**: fixed consistency-check predictions on an
   unchanged raw-value front-end cannot produce safe durable perceptual
   memory. Any successor must either change the front-end measurements or
   make predictions genuinely independent of them.

## Honest caveats

1. **Another crew modified `src/sense_h3.zag` mid-evaluation** (02:29 UTC),
   removing the sticky quarantine, and re-ran streaming with their build.
   Their change is post-freeze and unevaluated by this verdict; the source
   was restored to the pristine frozen version for all results reported
   here. Their experiment (per-episode quarantine) is a different artifact:
   on their own colordisc rerun it traded the KB3 kill for KB1 (35.2%) and
   KB2 (57.6%) kills — removing the stickiness lets false claims re-install
   and go durable. Neither version survives the frozen bars.
2. **Prereg ambiguity**: §3 rule 4 says quarantine blocks install "for that
   episode" but also "stored as negative evidence" with "active retirement"
   of durables. The frozen implementation chose the sticky reading; the
   kill bar trips on that reading. A per-episode reading would need its own
   frozen prereg and full battery — it does not inherit this verdict's
   evidence either way.
3. **KB4's regret model** debits withholding a correct claim the same as it
   credits installing one; on tasks where A is mostly right (colorconst),
   any withholding policy looks bad. The bar is the bar, but the KB4 kill
   on colorconst partly measures H3's caution, not just its errors.
4. **B2's exact 0.000 delta** is structural (H3 never installs a non-T0
   claim), not a measurement coincidence — H3 cannot beat A on judgment,
   only withhold.
5. H3ADV validation: 4 documented generator deviations from §5 (see
   `src/BUILD_LOG.md`); the gate (T0≠truth OR ≥1 broken prediction) held
   120/120 regardless.
