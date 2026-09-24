# FABLE VIDEO ROUND — deepest intuition on the video motion path

You are consulting as a deep technical advisor to the TNN research program (a native, deterministic AI built in pure Zag — no randomness anywhere in decision paths, byte-identical reruns required). Be maximally thorough. This is ONE batched round; give us your full depth now.

## Context: the video motion path

The program's flagship video-perception line is a multi-scale coherence-field motion detector ("motion4"), implemented natively in pure Zag, fully deterministic. It judges 8-frame clips as STILL / moving-with-direction / WITHHOLD (withhold is never an error). It works at three spatial scales: S0 (full resolution), S1, S2 (coarsest). Each scale independently claims direction or STILL; a resolution rule (§4.4) combines claims into a CANDIDATE judgment.

## The frozen MOTION4 kill battery (just completed, 2026-09-24)

Six batteries, seven kill bars K1–K7. Result: **6/7 PASS. K2 FAILS on both clauses.**

Key numbers:
- B1 (M3 synthetic primary): 57/60 correct, 0 false, 3 withhold (all `scale_disagree` on diagonal/south motion).
- B2 (M3 synthetic adversarial, 26 moving + 4 STILL, all 1px/frame): moving-catch **7/26**; 18 moving clips withheld with reason `still_dir_conflict`; **1 false** — p006 (truth: SW motion) judged STILL CANDIDATE at confidence 414.
- B3a (real-footage labeled windows): 13/13, 0 false.
- RM1 (fast translated real textures, 252 clips): 0 false on all 204 kill clips; 6px/frame correct-direction **81.3%** (78/96) vs 40% bar.
- RM2 (genuine real motion, 52 clips): 16/17 labeled correct, 0 false, 1 withhold; all 6 STILL correct.
- B4 (YT1 held-out): 8/13, 0 false, 5 withhold.
- K6 determinism (3× identical SHAs, byte-identical reruns, zero RNG) and K7 cost (973,568 ops/clip vs 1.5M budget): PASS.

## The K2 failure mechanism, precisely

Two frozen-mechanism consequences, recorded as anticipated mechanism-vs-bar tension (not scorer error, not tuning):

1. **The 18 withholds**: at 1px/frame, S2 claims STILL (it sees only 0.25 scale-px of motion — below its resolution) while S0/S1 claim coherent direction. Frozen P5 forces `still_dir_conflict` → WITHHOLD. So the coarsest scale's blindness vetoes the finer scales' genuine detection.

2. **The 1 false-STILL (p006)**: S0's evidence fell below E_FLOOR (ebar=57 < 64), so S0 WITHHOLDs rather than claiming direction. With no direction candidates left, S2's STILL claim passes unchallenged through §4.4 (StillCands ≠ ∅ → STILL CANDIDATE). A sub-threshold fine scale lets a blind coarse scale's STILL claim through.

Note the asymmetry: M3 (the predecessor) scored 0 false on p006 by withholding. M4's finer calibration made the false possible.

The repair-round proposal (frozen, awaiting a human signature — no source touched) offers two paths:
- **(a) Revise P5**: a scale that claims STILL while another claims coherent direction at ≥G_MIN_PM scale displacement has its STILL claim made ineligible as StillCands when it cannot resolve displacement d — "a scale that cannot see d may not claim stillness at d."
- **(b) Rewrite K2**: declare 1px/frame out of M4's scope; rewrite the bar instead of the mechanism.

Additional evidence: RM1's 18 six-px withholds (reason `incoherent`, S0's code) concentrate on diagonal directions (NE 9, NW 3, SE 2, SW 2, N 1). RM2's 35 AMBIG clips (excluded from scoring): clouds/deformation 6, ocean waves 6, atmospheric shimmer 6, pedestrians/multi-motion 9, FPV drone 6, cloud-no-coherence 1, deer 1. B1's 3 withholds are all `scale_disagree` on diagonal/south synthetic motion.

## The authority layer (just landed)

The video path now implements the universal three-gate feedback-authority law with a **two-piece rule**: piece 1 = PAR frame path (plan absolute, zero cross-frame state); piece 2 = stateless per-frame exception detect-and-reassert (re-render the faulted frame plan-pure, nothing else). Piece 3 (output-conditioned scene events) is **structurally denied** — it must clear three frozen gates (plan-incomputability proof, battery demonstration, non-interference proof) before it can exist. T2 machine-checkable protocol: 26/26. Both paths registered; negative refusal tests pass.

## What we ask of you

1. **Your deepest intuition: what is the K2 failure really telling us?** Is 1px/frame a fundamental limit (aliasing/quantization at the scale pyramid — the coarsest scale genuinely cannot resolve sub-scale-px motion, so its STILL claim is honest-but-blind) or a mechanism bug (the resolution rule trusts a blind witness)? Steelman both. Which reading does the diagonal-concentration evidence support?

2. **Path (a) vs path (b): which, and what would discriminate?** Design the concrete tests — with preregistrable kill criteria — that would decide between revising P5 and rewriting K2. Consider: is S2's STILL claim at 0.25 scale-px EVER correct when S0 sees coherent direction? (If never, path (a) kills zero true positives.) Is E_FLOOR=64 miscalibrated, given p006's ebar=57? What does the S0 sub-threshold withhold do to the whole resolution chain?

3. **Where does the video path go next?** Beyond the repair round: the diagonal incoherence at 6px, the 35 AMBIG real-world clips (clouds, waves, shimmer, crowds, drone footage — the path withholds on all of them; is that wisdom or cowardice?), the relationship between the motion detector and the authority two-piece rule. What are the load-bearing architectural questions nobody has asked yet?

4. **Concrete next tests.** Give us a ranked list of specific, buildable experiments — each with what it discriminates and what a kill looks like. Fable advises; native crews execute and verify, so be concrete enough that a crew can preregister from your description.

Do not hedge into vagueness. Commit to readings, name the discriminating evidence, and tell us where you'd bet.
