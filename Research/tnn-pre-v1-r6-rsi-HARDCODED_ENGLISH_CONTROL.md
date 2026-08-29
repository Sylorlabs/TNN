# Hardcoded English prosthesis control

The user requested a deliberate hardcoded-English experiment. R6 implements it
as an isolated control. It cannot contribute to any TNN production gate.

The prosthesis receives:

- human-authored surface templates;
- human-authored semantic slot identities;
- a human-authored lexicon;
- explicit dictionary insertion for a novel label.

Results in the bounded generated world:

```text
covered authored grammar exact                 1.000
outside authored grammar exact                 0.000
single-typo exact                              0.125
sensory grounding                              false
withdrawal without internal training exact     0.000
co-trained raw-text substrate after withdrawal 0.9375
```

The control demonstrates why an artificial system can appear mature immediately:
it has been given the answer structure. Its perfect one-shot score is not
learning; `register(slot, value, label)` directly edits the lexicon.

Co-training is more informative. A generic raw-text substrate trained while the
prosthesis supplies meanings retains much of the bounded language after the
prosthesis is removed. That suggests a temporary scaffold may accelerate
acquisition, but the scaffold itself does not solve grounding, transfer,
pragmatics, natural speech, or open-domain English.

A future scaffold-withdrawal experiment should use a much richer natural corpus,
then test novel constructions and nonlinguistic transfer after complete removal.
