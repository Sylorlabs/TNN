# UNIVERSAL_VS_PERPATH.md — should authority rules be universal or per-path?

## Position: per-path verdicts, universal *test*. Dialogue alone nearly settles it.

The audio authority rules (HYBRID_SPEC.md) are three specific mechanisms: a PAR-default pure renderer, a block exception detect-and-reassert, and a RESPOND octave latch. The question is whether these — or the principle behind them — should govern every generation path.

**Dialogue's answer: the rules cannot be universal, because dialogue is not the same kind of thing as audio rendering.** Three structural disqualifiers, each sufficient alone:

### 1. No sensor, no noise, no plan-independent fault class
The audio rules exist to solve *audio* problems: the waveform can be corrupted after a correct render (bit flips, dropouts — HYBRID_SPEC §2 fault model), and the pitch sensor has a characterized ±97-cent bias (HYBRID_SPEC §3). Every bound in §4 is calibrated to a measured physical channel.
Dialogue has no channel. Render and emission are the same memcopy (`rput`, dialogue.zag:867; `emit_fact`, :1481). There is no "after the render" for faults to strike in, and no sensor with a bias curve to gate. Porting the exception path to dialogue yields a `beq` assert, not a servo; porting the octave latch yields nothing at all (there is no measured quantity). **A universal rule that mandates mechanisms with no referent on a path is not universal — it's audio law imposed on foreigners.**

### 2. Epistemically loaded output
Audio's safety proofs rest on the output being epistemically neutral: a waveform carries no beliefs, so a false-positive correction is a no-op re-render (HYBRID_SPEC §2: "the band edges carry no safety risk, only a perf cost"). Dialogue's output is propositional content — claims that can be believed, cited, and reasoned from. The safety proof does not transfer; the failure mode (B1: constructed→belief leakage) has no audio analog and is strictly worse than any audio fault (WRONG_RULE_COST.md). **Universality would require the safety argument to hold on all paths. It holds on exactly the paths whose output is epistemically neutral. That is a per-path property.**

### 3. No sequential units — the question has no referent
PAR-vs-AR-vs-hybrid presupposes unit-by-unit rendering. Dialogue assembles responses atomically from plan content (PATH_MECHANICS.md §4). Asking "should dialogue use the hybrid?" is like asking whether a library should shelve books loud or quiet — the predicate doesn't apply. A universal *rule* stated in audio's vocabulary cannot even be evaluated on this path; a universal rule stated abstractly enough to apply ("feedback earns authority only on exception paths") is so abstract it decides nothing, and each path still needs its own fault model to instantiate it.

## What *should* be universal: the test, not the verdict

There is a genuine universal principle in the audio work, and it should be stated as a **test every path must pass**, with per-path verdicts:

> **Output feedback earns authority on a path only if all three hold:**
> **(T1)** the fault is detectable against a *plan-derived* expectation (not against the output's own statistics);
> **(T2)** the correction map is *plan-pure* — constant in the measured output (the Lipschitz-0 property), so false positives are no-ops;
> **(T3)** the output is *epistemically safe to re-ingest* — measuring it cannot install content into the plan that the plan didn't author.

Audio passes T1–T3: plan-derived RMS targets (§5), constant re-render map (§2), waveforms carry no beliefs. Hence: bounded exception + latch authority. **Dialogue fails T3 categorically** (output is propositional; re-ingestion risks belief corruption) and T1/T2 are vacuous (no noise → detection is an assert, correction is identity). Hence: no feedback authority, plan absolute.

Note what this framing buys: it explains *why* the audio rules are right for audio without making them law for dialogue, and it gives every other path (image, video, story) the same three questions instead of audio's answers. The story path — the sibling "other (template beat-fill)" classification — will likely land near dialogue; image/video (stateful-sequential canvas/voxel rendering, per the survey) will need their own T1–T3 analysis, and may legitimately land somewhere between.

## The one thing dialogue contributes back to the universal conversation

Dialogue proves that **"the plan keeps last word" is implementable without any feedback at all** — and that the implementation is *stronger* for it. The correction branch (dialogue.zag:1544–1614) is the dialogue analog of "plan keeps last word via re-render, never arbitration": on correction, the previous answer is *excluded* and retrieval re-runs from the new utterance + frozen KB. No arbitration between old output and new input. No servo. 45/45. That is the purest existing instance of the hybrid spec's authority moral — achieved by *deleting* the feedback channel rather than bounding it. If the universal test (T1–T3) is adopted, dialogue is its cleanest passing example of the "no authority" verdict.

## Recommendation to Micah

- **Do not universalize the audio mechanisms.** Adopt the T1–T3 test as the universal gate; let each path earn its own verdict.
- **Dialogue's verdict under T1–T3: no output feedback authority.** The six documents in this directory are the evidence.
- Expect image/video to be the hard cases (they have real sensors and real plan-independent faults — dropped frames, occluded voxels — but their outputs are also consumed by humans as *content*). Do not let audio's clean T3 pass prejudice the analysis there; run the test honestly per path.
