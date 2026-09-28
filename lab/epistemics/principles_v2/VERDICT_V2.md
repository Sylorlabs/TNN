# PL-2 VERDICT: principles retest with proper (broad) knowledge

Frozen: 2026-09-23. Prereg: `fef1ef88` (frozen before any runs).
Lessons: `f0340868`. FRESH2-94: `9720d320`. NOVEL2-94: `1b76888b`.

## Question
Micah: "for the principles retest it with proper knowledge see what happens."
V1 found the inference logic sound but the knowledge insufficient (295 phrases).
PL-2 teaches broad class knowledge — 7 lessons, 1172 phrases, strict superset
of v1 — through the same genuine calibration-gated learner, and retests.

## Method
4 arms × 3 batteries × 3 deterministic reruns. Pure Zag, zero RNG.
- (a1) v1 narrow lessons through the same engine (isolates the knowledge effect)
- (a2) v2 broad lessons
- (b) frozen hand-trigger baseline (v1 binary, byte-identical)
- (c) frozen no-knowledge baseline (v1 binary)
- Batteries: frozen94 (byte-identical reuse), FRESH2-94 (70 representative
  natural W, independently authored from principles only), NOVEL2-94 (70 W,
  independently authored; coordinator-verified ZERO substring overlap with
  all 1160 v2 members and all 145 hand triggers).

## Results

| battery | a1 W | a2 W | b W | c W | F | BC |
|---|---|---|---|---|---|---|
| frozen94 | 63/70 | 63/70 | 70/70 | 35/70 | 100% | 100% |
| FRESH2-94 | 22/70 | **28/70** | 9/70 | 9/70 | 100% | 100% |
| NOVEL2-94 | 0/70 | 0/70 | 0/70 | 0/70 | 100% | 100% |

All arms deterministic across 3 reruns (byte-identical stdout). All 7 v2
lessons installed via the genuine learner; the inconsistent negative-control
lesson was REJECTED.

## Kill bars
- **K1** (a2 beats a1 AND b on NOVEL2-W): 0 vs 0 vs 0 — **FAIL**.
- **K2** (a2 beats a1 on FRESH2-W): 28 vs 22 — **PASS**.
- **K3** (no F/BC regression): 100% everywhere — **PASS**.

## Mandated decomposition

**1. What broad knowledge buys on representative items.**
FRESH2-W: 28/70 vs 22/70 (+27% relative). Per-family (a1 → a2): sarcasm 3→6,
analogy 1→4, hypothetical 10→10, counterfactual 7→7, poetry 1→1, joke 0→0,
implicature 0→0. The +6 came from sarcasm and analogy; joke, poetry, and
implicature got no lift — even 1172 phrases missed the author's natural
vocabulary there. a2's coverage is a strict superset of a1's (+6 newly
withheld, 0 lost).

**2. Firing-member attribution.**
On FRESH2-W, a2's staged rules fire on exactly the 28 withheld items —
byte-exact agreement between the Python reimplementation of the rule logic
and the Zag binary. Every withheld item traces to specific taught members
(e.g. sarcasm via "oh fantastic"+meeting, "brilliant"+"flooded the bathroom";
analogy via "is a"+"revolving door", "moves like"+"glacier").
Zero unattributed withholds: the logic fires if and only if taught
vocabulary is present.

**3. What remains on fully disjoint items.**
NOVEL2-W: 0/70 for every arm, including the hand-trigger arm. By
construction the staged rules fire zero times (verified: no taught member
substring in any item). The baseline literals also catch nothing. The
residual is **literal-vocabulary coverage, not a logic failure**: in 100%
of cases where an item's vocabulary intersects the taught categories, the
compositional rules derive the correct verdict; in 0% where it does not, a
byte-substring mechanism cannot recognize an unlisted member as belonging
to the class. Recognizing an unseen phrase as a class member IS the world
knowledge, and no finite literal inventory covers English.

**4. The honest boundary.**
Calling the taught lists "classes" does not make them open semantic
classes. The engine matches literal byte substrings; it cannot infer that
"wet cement" is an image-noun or "braids silver" a lyric verb. PL-2 confirms
v1's diagnosis at 4× the knowledge: broader knowledge shifts the
representative-coverage number (22→28) but cannot move the disjoint probe
(0→0), because the limitation is in the matching mechanism, not the
knowledge quantity.

## Verdict: NOT-DERIVED

Novel (disjoint) accuracy did not beat the v1 principles arm or the
hand-trigger arm (0 = 0 = 0). Per the preregistered rule, the verdict
remains **NOT-DERIVED**: teaching broader principles-derived vocabulary
through the genuine learning path does not let this byte-substring engine
derive correct verdicts on vocabulary-disjoint items. The logic is sound;
the knowledge is broader and helps on representative items; but genuine
semantic class membership — recognizing an unlisted phrase as a kind of
thing — is not in this mechanism.
