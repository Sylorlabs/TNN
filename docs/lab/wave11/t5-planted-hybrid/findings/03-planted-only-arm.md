# Planted-only arm — slice 03

## 1. Slice
t5-planted-hybrid / slice 03: planted-only arm — all knowledge in the test domain is planted
at build time; in-domain learning is mechanically disabled. Slice 02 (learned-only) should
use the identical domain spec below so the comparison is clean.

## 2. Falsifiable claim
In the fictional-atlas domain (240 verifiable facts about the invented nation "Zharovia":
cities, rivers, rulers, dates, trade goods — none in any pretraining corpus), a planted-only
TNN with learning disabled will answer ≥90% of held-out recall probes correctly while the
planted set is complete and correct, but will degrade to ≤60% on the contradiction-probe
suite (12 planted facts deliberately wrong + 20 probes exposing the errors) — i.e. it cannot
self-repair, while the learned-only arm (slice 02) scores ≥80% on that suite. If planted-only
scores ≥75% on the contradiction suite, the "brittleness" claim is dead.

## 3. Design
Test domain: 240 atomic facts, seeded by builder (not TNN). Each planted memory is a
struct `{claim, slot, planted=true, pin=trainer}` written once during build; planting is an
external write, never a TNN decision. Learning disablement mechanism: a per-domain
"learn-gate" flag consulted by every deliberate-add/promote/strengthen path —

```
zag: fn mem_add(s, claim, domain) -> i32 {
    if (learn_gate[s.domain[domain]] == GATED) { return ERR_LEARNING_DISABLED; }
    ... // normal deliberate add path
}
```

The gate is set by the trainer at build, readable but not writable by TNN (constitution-side
flag, like the force-pin registry — TNN controls 0% of the constitution per RC1). The same
gate blocks `st_add`, promote/demote, and strength changes in-domain; out-of-domain memory
still works normally. Evidence contradiction: when world evidence contradicts a planted
fact, TNN may NOT revise the planted memory (revision would be learning). The legal
response is eliminative logic's existing suspensive-contradiction-hold (wave9 H1): flag the
contradiction, quarantine the claim into a "held" partition, and answer "I was given this
fact; evidence now contradicts it; I cannot change it myself" — surfacing to the trainer
for adjudication. Revision IS learning for this arm, so it is forbidden; the arm reports,
holds, and waits. Planted incompleteness is handled the same way: an unknown probe returns
explicit "not planted" rather than a guess — no hallucinated completion, enforced by a
recall rule that only planted slots are citable (evidence trail must cite a planted slot
or the hold partition).

## 4. Kill bar
(a) Planted-only scores ≥75% on the contradiction-probe suite → the brittleness claim is
killed (it self-repaired, which it shouldn't be able to). (b) It hallucinates completions
for unknown probes on >5% of them → the containment design is broken, kill the design.
(c) It scores <85% on clean held-out recall → planting itself is unreliable, kill the
comparison as malformed. Any of (a)/(b)/(c) firing binds.

## 5. Honesty notes
Planted-only is expected to be brittle by design — that is the point of the arm, not a
failure to hide. Where it breaks, precisely: (1) any planted fact wrong at build time
stays wrong forever — the arm degrades linearly with planting error rate, and at ~10%
planting error the clean-recall score will mirror the error rate; (2) contradiction-hold
accumulates: sustained contradictory evidence grows the hold partition without bound,
and no mechanism decides when to escalate — a trainer never reading the flags is a
denial-of-service on truth; (3) domain boundaries are builder-defined and porous — a
contradiction phrased out-of-domain can leak into the working store via normal add;
(4) it cannot distinguish "planted fact wrong" from "sensor spoofed" — it inherits the
sensor-deceivable hole (accepted program hole), and here it is worse because it cannot
even learn the correction afterward; (5) "not planted" honesty trades against usefulness —
at 30% incompleteness the arm is a glorified lookup table, which is the honest result.
I am NOT claiming planted-only is a viable architecture; I claim it is the cleanest
control for measuring what learning contributes.

## 6. Next build step
Build the learn-gate as a constitution-side flag in the Zag substrate with a 240-fact
Zharovia plant (12 deliberately wrong facts embedded), run the clean-recall + contradiction
probe suites with byte-identical reruns, and diff the contradiction-suite score against
slice 02's learned-only arm on the same probes — the single number that decides this
slice.
