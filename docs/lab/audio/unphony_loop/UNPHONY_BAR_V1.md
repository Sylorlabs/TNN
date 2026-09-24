# UNPHONY LOOP — frozen success bar V1

Status: **FROZEN** — committed before the first loop hypothesis is tested.
No bar, tolerance, procedure, or kill rule below may change after the first
loop fork is inspected. Amendments require Micah's explicit sign-off and a
new version number (V2); the frozen copy stays in git history.

Date: 2026-09-24. Loop runner: night-shift subagent.

## 0. Why this loop exists

On 2026-09-23 Micah listened to the four AR/PAR motif clips
(`ar_motif.wav`, `ar_motif_recur.wav`, `par_motif.wav`, `par_motif_recur.wav`).
His verdict: 1 = horrible, 2 = same as 1, 3 = same but slightly different,
4 = same as 3. Conclusion: **TNN imagination audio is a phony.**
He declared this a stumped scenario and ordered a hypothesize → debate →
test loop, with heavy grok-4.7 and fable-5.1 involvement, until it is solved.

Critical evidence from the verdict: PAR's motif recurrence measured 1.000000
(perfect) and AR's 0.741083 (drifting) — yet both sounded equally horrible.
**Phoniness is therefore NOT recurrence drift.** Whatever makes the audio
phony lives elsewhere. Any hypothesis that "fixes" recurrence is dead on
arrival; the loop must find the real missing signature.

## 1. Scope

All TNN imagination audio: scene renders (kids, ocean, alien ocean), motif
renders (AR/PAR and future), and any new synthesis path. The AUDIO V11
child-voice line keeps its own frozen judge protocol
(`imagination_discovery/aud/b_alpha/JUDGE_PROTOCOL_V11.md`); this loop
coordinates with it (shared anchors, shared instrument philosophy) and
merges with it if the root cause is the same. Current working theory, to be
tested not assumed: the root cause IS the same — renders with pitch but no
physical source model (V11 diagnosis: F0 without formants, noise without a
glottal source) sound phony regardless of content.

## 2. The anchors (the only ground truth)

Real field recordings, **measurement-only**: never committed, never
redistributed, never used as render source material. Judges work from derived
measurements and blinded listening copies.

- Child-voice anchor: `aporee_kids_play_area_30s.wav` (SHA-256
  `6adafbf0143df1c1721377cd8eaa7f25aa6305fb4be6d12c6268d28281738960`),
  shared with V11.
- Motif/scene anchors: real recordings of the corresponding target class
  (real music for motif renders, real ambience for scene renders). The exact
  anchor files and their frozen measurements are recorded in an addendum
  BEFORE the first fork targeting that class is judged. No fork may be
  judged against an anchor chosen after the fork was heard.

## 3. Prong 1 — objective: the frozen discriminator

A frozen pure-Zag instrument measures a real-vs-render signature on the
anchor class. Bars cite the anchor's measured values with tolerances
derived from real-recording variance — never from renders.

For child-voice targets the loop reuses the V11 frozen instrument
(`voice_sig_frozen.zag`) and its bars unchanged. For other target classes
the loop freezes an equivalent instrument + bars in an addendum before
judging begins.

A fork passes Prong 1 iff its measured signature falls within real variance
on EVERY frozen bar for its target class.

## 4. Prong 2 — subjective: blind discrimination

- Blind ABX / forced-choice discrimination: a judge (human, or a frozen
  discriminator built ONLY from real-recording features) must not reliably
  distinguish the TNN render from the real target — performance at or near
  chance, with red-team calibration traps (known-real pairs the judge must
  get right, known-phony pairs the judge must catch) proving the test has
  teeth.
- Structured listening notes with a mandatory steelman: the judge must
  argue FOR the render being real before rejecting it.

## 5. The gate to Micah's ears (no-regression law)

A fork reaches Micah **only if it beats the current best fork on BOTH
prongs**. "Beats" means: strictly better objective-bar coverage AND
strictly better blind-discrimination score than best-so-far. Ties and
lateral moves do not ship.

- Ears outrank metrics: any unanimous ear rejection kills the fork, even
  with a perfect objective score (V10 taught us this).
- Every clip shipped to Micah carries a brief: what changed, what to listen
  for, what the frozen bars say. No regressions dressed as progress — ever.

## 6. Loop mechanics (frozen)

1. **HYPOTHESIZE** — grok-4.7 at highest reasoning, explicitly prompted to
   be super thorough (volume is fine; reasoning is cheap). fable-5.1 in
   batched thorough rounds for the hardest sub-questions. Native subagents
   generate their own hypotheses in parallel.
2. **DEBATE** — grok vs fable vs native argue each hypothesis.
   Mechanism-level arguments kill weak hypotheses BEFORE building. A
   hypothesis dies if it only re-derives a known failure (e.g. "fix
   recurrence") or cannot name the acoustic mechanism that makes audio real.
3. **TEST** — survivors built in pure Zag, zero RNG, byte-identical reruns.
   Tested against the frozen anchors (§2), never against other renders.
4. **RED-TEAM** — every fork is attacked for phoniness (adversarial
   listening, signature checks) BEFORE anything reaches Micah.
5. **LOOP** — failures generate new hypotheses; the loop turns until the
   bar in §3–§5 is met or Micah stops it.

## 7. Kill criteria for the loop itself

The loop stops when: (a) a fork passes both prongs and Micah signs off on
his ears, or (b) Micah stops it, or (c) three consecutive full rounds
produce zero prong movement AND fable's deep audit agrees the hypothesis
space for the current target class is exhausted — in which case the loop
reports the exhaustion honestly and proposes the next target class, rather
than grinding.
