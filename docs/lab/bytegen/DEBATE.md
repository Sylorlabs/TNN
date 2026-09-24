# BYTEGEN debate report — AR vs PAR

## Participants
- **Outside 2nd opinion**: grok-4.6 via UnoRouter (argued pro-AR; see transcript below).
- **Muse** (native): contra + adjudication on the evidence.

Procedural note: the prereg mandates a Sol + Muse debate. Sol (gpt-5.6-sol via
UnoRouter) was attempted twice with short prompts and returned `choices: null`
with 0 completion tokens both times — a provider-side empty completion, not a
prompt problem (standing known issue). Per Micah's rescinded model rule (any
UnoRouter model may serve as 2nd opinion; native preferred for opinions),
grok-4.6 was used as the outside voice instead. Flagged honestly; if Micah
wants a literal Sol take, rerun when the provider recovers.

## Grok's position (pro-AR, verbatim summary)
PAR's zero-state purity is elegant but fatally flawed for long-form work:
"when the plan itself is wrong, PAR has no mechanism to notice or correct
it. It renders the mistake forever." AR "sets gain, timbre, and pitch on the
basis of what actually exists in the waveform rather than the score," giving
self-recovery (131 ms perturbation then coherent parameters) and plan
correction (reads the sound it is making, like a human performer listening to
the take). "Long-form rendering is not about obeying a plan that may be
imperfect; it is about producing coherent sound that a listener experiences
as right. AR does that; PAR does not."

## Muse's contra
Grok's argument overstates what the experiment proved and understates PAR's
virtue:

1. **"Musical agency" is doing heavy lifting.** AR's servo is a 1-frame
   RMS/ZCR regulator, not musical understanding. It "corrected" the pitch
   because the trap was engineered so ZCR→pitch works on a pure 440 Hz tone.
   On real audio (chords, noise, overlapping voices) ZCR pitch inference
   fails, and a renderer that "corrects" the plan has no judgment about when
   the plan is right — it will "correct" right into wrong just as happily.
2. **Blind obedience is a feature, not a bug.** The plan is the specification.
   If the plan is wrong, fix the plan — a renderer that silently second-guesses
   it destroys the one property that makes long-form work tractable: that the
   score means what it says. PAR's 1.0 recurrence is a *requirement* for music
   (a chorus must sound like the chorus), not a theoretical nicety.
3. **The cascade result cuts both ways.** AR recovered *here* because this
   servo is contractive and integer-quantized. A sustained fault (or one tuned
   to the servo's dynamics) could keep it derailed indefinitely. PAR's immunity
   is structural, not contingent.
4. **The 0.74 is a real tax.** Twenty-two seconds of intervening history
   measurably altered a motif that the plan said to repeat identically. For
   long-form coherence — the actual goal — that drift compounds.

## Adjudication (evidence-weighted)
Neither side wins outright; the evidence supports a **per-task hybrid**,
which is also where Micah's standing laws point (figure-it-out wins ties;
his ears outrank metrics on quality — excerpts await his verdict):

- **Default to PAR** (parallel, pure, plan-explicit) for everything the plan
  fully specifies: exact reproducibility, immunity to cascades, perfect
  long-range recurrence, zero hidden state to debug.
- **Bounded AR feedback only where generated-output inspection is actually
  needed** (response dependencies like RT-LONG, adaptive leveling) — with the
  feedback's authority *limited* to designated parameters/regions, because
  unconstrained feedback demonstrably degrades long-range coherence
  (1.0 → 0.74) and introduces cascade risk.

Grok is right that a plan can be wrong and that output-awareness is a genuine
capability (RT-LONG is the experiment's sharpest result). Muse's caution is
that "the renderer fixes the plan" is only a virtue when the renderer's model
of "fixed" is trustworthy — here it is a ZCR threshold, not a musician. The
synthesis: give the plan the last word by default; let bounded feedback speak
only where the task provably needs ears on the waveform.

## Debate outcome
**Hybrid, PAR-default with bounded AR feedback.** Not an AR victory: the
evidence does not support handing the renderer general authority to override
the plan. Not a PAR shutout: RT-LONG proves output-conditioned generation is
a real capability with no parallel equivalent.
