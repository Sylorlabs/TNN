# PAM hypothesis elicitation prompt (sent to Sol and Grok-4.6, 2026-09-22)

You are advising a research program building TNN, a deterministic AI (pure Zag, zero randomness in any decision path, byte-identical reruns required). We are rebuilding PAMs (perceptual access modules) — TNN's perceptual organs for audio and vision. The old PAMs are DEAD: they were Python + weight files with NO contract for telling the memory system anything — they could label sounds but could not tell memory anything usable in a decision.

Latest frozen evidence you must respect:
- Head-to-head trial: Approach A (LLM-style raw values — sample values, pixel values) scored 72.6% viability; Approach B (human-style qualitative percepts — "I hear a laugh", "I see red") scored 54.0% and was KILLED per the frozen bar (needed >=60%). B was 2.42x cheaper in ops.
- CRITICAL FAILURE shared by both: memory integration catastrophically failed — 59% (A) / 55% (B) false-install rates under adversarial percepts. The deliberate-memory install gate cannot stop confident wrong percepts. Any new PAM must address this, not just improve labeling accuracy.
- Unification law: PAMs are organs of ONE brain, not separate models for separate jobs. Percepts must feed TNN's deliberate memory substrate and its deliberation.
- Human bars: audio output must be native field-recording quality (a human's ears judge; synthesis is banned); visual output must be realistic and imagined, not designed (a human's eyes judge).
- "Beautiful" is a scored dimension: elegance of the mechanism AND quality of its output. Efficient-but-ugly and beautiful-but-non-native both lose.

Propose EXACTLY 3 perceptual-architecture hypotheses for a BETTER form of PAM — not a refinement of A or B, but a new form. Each hypothesis must state all six of:

(a) NAME + one-paragraph statement of the architecture.
(b) PERCEPT: exactly what it produces — its format and granularity. Not raw values, not vague labels: something in between or beyond, specified concretely.
(c) MEMORY CONTRACT: the thing old PAMs lacked. Precisely what the percept TELLS the memory system, in what form, and step-by-step how memory uses it inside a real decision (install / withhold / deliberate). A percept that never changes a downstream decision is decoration — say which decisions change and how.
(d) EFFICIENCY: compute and memory per percept versus the raw-values approach, with the mechanism of the saving stated (not asserted).
(e) BEAUTY: why this is elegant — one mechanism doing the work of many, a single idea with wide reach — not a checklist of features.
(f) KILL BAR: a falsifiable, preregistrable bar. State the exact measurement, threshold, and conditions under which this hypothesis dies.

Be concrete, not poetic. Number your hypotheses H1/H2/H3 (Sol) or G1/G2/G3 (Grok).
