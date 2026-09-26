# Phase A2 verdict — wiring the organs for long-horizon real audio

## What was built
Pure-Zag, zero-RNG standing audio sense wired into persistent live deliberation:
`real WAV → frozen organ + low-F0 guard → descriptor vector → persistent
deliberation (16-turn history, baseline, recall, prediction) → journal →
pure-Zag action renderer → output WAVs`.

The descriptor vector never crosses a process boundary (produced and consumed
inside `session_run`). The deliberation boundary sees only WAV bytes (via
session file paths), intent, and mode.

## Verdict: WIRING-WORKS (with stated limits)

### Earned
- **K-W1 ABLATION-DEAD: PASS** (p=0.00010 < 0.01). Replacing descriptors with
  a frozen silence vector changes 16/16 actions (→ all QUERY). Deliberation
  demonstrably consults the organ.
- **K-W2 ABLATION-DIRECTIONAL: PASS** (sign agreement 1.000 ≥ 0.70). The
  silence ablation uniformly suppresses responsiveness (all ordinal diffs
  negative) — changes track the descriptor manipulation, not noise.
- **K-W3 PYTHON-IN-PATH: PASS.** Per-episode path is `session_run` → pipe →
  `render_act`, both native Zag. Python only scores committed journals offline.
- **K-W4 NONDETERMINISM: PASS.** Three consecutive full S1 live runs
  byte-identical (journal SHAs + rendered WAV SHAs; see RUNLOG).
- **K-W5 BOUNDARY: PASS.** Only WAV bytes + intent + mode cross into the
  deliberation binary; descriptors are produced internally (see BOUNDARY.md).
- **Corpus discipline:** sealed (e49b2a12) before any trial binary opened the
  clips; scorer frozen (bcdd5b92) before scored runs. Order honored.
- **Real-audio hello-world:** 16-episode session on real + contrast material.
  The system NOTICEs novelty (EP1), ATTENDs to deviations (EP2, EP4),
  CONTINUES through steady state (EP3, EP5), and RECALLs both exact repeats
  (dist=0, correct turn) and similar sounds. Prediction: 4/15 hits.
- **Low-F0:** validated estimator 55–125 Hz on synthetic (100% frames ≤5%
  error, per-band); <55 Hz explicitly unvoiced (no-silent-misread by
  construction). The frozen organ's P-R4 anchor untouched.

### NOT earned / honest gaps
- **Real-material F0 FIXED/SCOPING:** no real 55–125 Hz ground-truth corpus
  exists in the lab; the ≥50-clip scoping bar is unmet. Reported as OPEN,
  not claimed.
- **Deliberation quality:** the recall threshold is permissive (novel clips
  EP6–9,11 recall to nearest neighbors at dist 2–39). This is honest
  nearest-neighbor generalization, not a wiring failure — but the "thinking"
  is shallow. Tuning it post-hoc would be overfitting; left as-is.
- **Scale:** 16 episodes, ~200 s of audio. Long-horizon at 100× is untested.
- **Shuffle ablation** (p=0.58) shows the deliberation is robust to field
  permutation — informative, not a kill-bar item.

## What happens when you wire it up
The system hears, remembers, and acts — deterministically. It is not
intelligent yet (the deliberation is a small state machine over coarse
descriptors), but the wire is live: change what it hears, and what it does
changes, significantly and directionally. That was the question. Answer: yes.
