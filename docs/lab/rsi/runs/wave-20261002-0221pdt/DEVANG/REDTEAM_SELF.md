# REDTEAM_SELF.md: Adversarial self-review of DEVANG4

Role: red-team the builder's own work. Attack the two load-bearing
claims: (1) the segmentation mechanism is genuinely different from
DEVANG3's (not a relabel); (2) the K_DISC failure is a mechanism
result worth learning from (not an excuse).

## 1. Is COSEG genuinely different or a relabeled DEVANG3?

Attack: "You kept the 2321pdt DP scoring, added a beam, and reranked
by a hand-weighted margin. The margin is just another scoring term.
This is a parameter tweak with extra steps."

Defense and honest assessment:

(a) The DECISION differs observably. On Family D, 2321pdt outputs
`3,6,8` on all six probes; COSEG outputs `3,8` on D3/D5 and `3,6` on
D1/D2/D4/D6. The outputs are not a monotonic transform of DEVANG3's:
COSEG's D3/D5 analyses ([tak][blupa][bal], [tak][trixo][bal]) are not
in 2321pdt's top-2 by lexicon score, so no reweighting of the DP
scores alone produces them without the margin term. The mechanism
provably uses information 2321pdt cannot access: 2321pdt's segmenter
signature is `(utt, uoff, n, W, tmp)` (no scene); COSEG's is
`(utt, uoff, n, W, tmp, ep)` and the margin reads the scene. A
scene-blind mechanism cannot condition on the scene, period.

(b) BUT: the difference only engages in scene mode. In no-scene mode
COSEG is literally `seg_dp` (same function, same call). The prereg
documents this as non-regression, but the red-team notes the
consequence: on the K_SEG family (the bar the task named first), the
"new mechanism" contributes nothing. The structural difference is
real but narrow: it exists only where a scene is present.

(c) The margin signal, as defined, is WEAKLY principled. "Best minus
second-best object score" measures decision confidence, not decision
correctness. Nothing in the design prevents a confident WRONG
interpretation from outscoring a diffident right one. This is not a
hypothetical: it is exactly the K_DISC failure mode (section 2). A
genuinely interpretation-driven segmenter should prefer the analysis
whose interpretation is best JUSTIFIED, not merely most decisive.
The prereg's coherence notion was under-specified, and the failure
exposes it.

Verdict on claim (1): structurally different (new signal class, new
information flow, observably different decisions), but the new signal
is a flawed operationalization of "interpretation coherence." Not a
relabel; a real mechanism with a real defect.

## 2. Why K_DISC failed: mechanism autopsy

The prereg's paper analysis considered, for D1 "takbaltagrn", the
candidates [tak][bal][ta][grn] (lex 28, margin 0, joint 8) and
[tak][balta][grn] (lex -5, margin 2, joint 30), concluding the true
analysis wins. It MISSED the candidate [tak][bal][tagrn] (lex 15,
margin 2, joint 50), which the beam correctly surfaces and which wins.

Why does [tak][bal][tagrn] have margin 2? Its novel segment "tagrn"
swallows the descriptor "grn", leaving "bal" to vote unopposed for
the red-ball distractor: scores (o0:-1, o1:+1, o2:-1), margin 2.
The true analysis [tak][balta][grn] also has margin 2 (grn votes for
the target). Margin ties; the lexicon tie-break (15 vs -5) favors the
wrong analysis because it retains more known words.

Two defects compound:

(i) The probe design assumed the distractor-voting shatter would have
margin 0. That holds only for the [tak][X][yy][Z] shatter, not the
[tak][X][yyZ] variant. The family does not isolate what the prereg
claimed. This is a test-design error by the builder.

(ii) The mechanism cannot distinguish "confident right" from
"confident wrong." Given margin parity, it falls back to lexicon
frequency, which systematically favors analyses that keep frequent
words as separate segments (the shatter bias the 2321pdt penalty was
designed to fix for merges, but which persists here because the
pieces are KNOWN words, not novel ones). This is a mechanism defect:
the coherence signal has no notion of which object SHOULD win.

Could a better coherence signal fix it within the frozen architecture?
Candidate: margin weighted by the FRACTION of the utterance explained
by grounded segments, or a penalty for novel segments that swallow
grounded substrings. Both are new design work, not bug fixes, and
are therefore DEVANG5 material, not corrections to this wave. The
prereg's design is frozen and was implemented exactly; the failure
belongs to the design.

## 3. What the passing bars do and do not show

- K_SEAL 12/20 (exactly at bar) with C2 at 14/20: the learner meets
  the bar, but fixed-width chunking beats it on this world. The
  red-team notes this undermines any "COSEG helps novel vocabulary"
  story for C-prime: the win over C0 (6/20) is real, but the
  mechanism's contribution over a dumb baseline is not demonstrated
  here.
- K_ABL passes (1/12, gap 2): the front-end is load-bearing, but note
  the gap is exactly 2 (the minimum). The ablation's K1 (8/10) is one
  word below the bar, same as DEVANG3's deviation pattern.
- K_AUD passes: the information-flow architecture is intact. The new
  signal did not open a statistics bypass. This is the strongest
  positive result of the wave: scene-conditioned segmentation WITHOUT
  breaking segmentation-dependence.
- K_SEG 4/12: the red-team grades this as a test-design failure, not
  a mechanism failure, BUT notes the builder wrote the test. A
  mechanism that cannot be evaluated by its author's own test is a
  process failure regardless of which side is at fault. The next
  B-family must be validated (with altered seeds) to be solvable in
  principle before freezing.

## 4. Strongest remaining attack on the research direction

"Interpretation coherence" as margin-maximization is the wrong
objective. The learner should segment so as to make the interpretation
EASY TO VERIFY or EASY TO CORRECT, not merely decisive. A decisive
wrong interpretation (margin 2 for the distractor) is worse than an
indecisive one, because the learner will act on it confidently. The
K_DISC probes demonstrate the mechanism confidently mis-segmenting.
Until coherence is tied to something the learner can check (prediction
of the NEXT episode? consistency across episodes? the speaker's
reaction?), scene-conditioned segmentation is just a new way to be
confidently wrong. The queued next step should either (a) define
coherence against a verifiable signal, or (b) abandon margin and find
a different second signal class (e.g. cross-episode consistency of the
lexicon, or predictiveness of segments for scene features).

## 5. Process notes

- The near-miss in NAMECHECK.md Step 0c (typed `python3 -c` as a
  presence check; name did not resolve; nothing executed) was poor
  discipline. It did not affect any result (all computation is Zag;
  the setup verification stands), but it is recorded because the
  governance rule is about the attempt pattern, not just outcomes.
- The prereg was frozen before implementation (c768b02be), the
  baseline before implementation, the sealed package before the
  sealed runs. No bar was altered after results. The K_DISC and K_SEG
  failures are reported as failures, not re-scoped.
