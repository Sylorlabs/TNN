# CONSCIOUS-KB AUDIO FORK — design (mandated fork for Round 3)

## Concept
The EDITING DECISIONS are made by TNN's deliberate memory agency operating
over a conscious KB — not by a fixed pipeline, not by a human. The fork is
an autonomous perceive→deliberate→edit→verify→commit loop whose every
decision is a KB operation.

## KB contents
1. SOURCE INVENTORY: real audio units as KB entries. Each entry: source
   file SHA-256, byte offset, duration, measured descriptors (F0 median,
   spectral centroid, HNR, RMS, tags like "laugh-fragment",
   "vowel-hold"). Installed only via deliberate install ops with
   provenance; no silent overwrites (KB-control properties, commit
   559c805c).
2. EDIT PLANS: sequences of edit ops (SELECT unit, CUT at sample points,
   ORDER, LAYER with gain, FADE bounded ≤5 ms, REPEAT) as KB entries,
   deliberated and committed before rendering.
3. AUDIT TRAIL: append-only log of every render decision; replayable to
   exact state.

## The autonomous loop (no human in the loop)
Given a target spec (a short descriptor list, e.g. "4 s, laughing-like,
child voice, F0 300-600 Hz"):
1. PERCEIVE: load KB inventory (real units only; synth entries refused).
2. DELIBERATE: deterministic selection rules pick units minimizing
   descriptor distance to target; join planner orders them minimizing
   boundary discontinuity (deterministic Viterbi, no RNG).
3. RENDER: apply the edit plan — cut/splice/order/layer/gain/fade. Every
   output sample is a selected real sample except bounded crossfades.
4. VERIFY: run the full analyzer gate battery on the render.
5. COMMIT or REVISE: pass → deliberate install of result + audit entry;
   fail → revise plan (bounded: max 5 revisions, then WITHHOLD honestly).
The loop is a runnable Zag program + driver. Activation = build it, prove
a full cycle end-to-end on a real target with zero human decisions,
commit it, leave it runnable via a single command with a standing target
queue it drains.

## Law compliance
- Every output sample traces to (source SHA, offset) — mechanical
  provenance audit, 100% coverage required.
- Crossfades ≤5 ms are the ONLY interpolated samples; disclosed, bounded,
  and the kill experiment tests whether they matter.
- No oscillators, no parametric excitation, no synthetic noise, no
  formant filters. Gain changes are scalar multiplies on real samples.

## Preregistered kill bars
- KB1: silent-overwrite probe refused (attempt install over an existing
  unit without deliberate op → must refuse).
- KB2: provenance audit 100% — every output sample maps to a KB unit.
- KB3: autonomy — full cycle completes with zero human decisions
  (witnessed, logged).
- KB4: all shared analyzer gates pass (frac_static, HNR, PERIODICITY,
  HF_ROLLOFF, PROSODY, TRANSIENT).
- KB5: 3× byte-identical reruns.
- SELF-KILL: swap the KB inventory for synth-generated units carrying
  identical descriptors; if output metrics don't collapse, the
  "real-audio" claim is vacuous and the fork DIES.

## Honest failure mode
Most likely: the deterministic selector picks units that are
individually fine but join audibly badly (choppy, "ransom-note" voice).
That tells us join-cost modeling — not unit quality — is the load-bearing
problem, and the fix is better boundary analysis, not better sources.
