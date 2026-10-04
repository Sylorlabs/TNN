# REDTEAM_SELF.md: Adversarial self-review of DEVANG5

Role: red-team the builder's own work. Attack the load-bearing
claims: (1) FINREG is a genuinely new signal class, not a relabeled
old mechanism; (2) the K_DISC pass is real discrimination, not an
artifact; (3) the K_ABL failure is bar-miscalibration, not a
mechanism defect being excused.

## 1. Is FINREG genuinely different or "a parameter tweak with extra steps"?

Attack: "You added +-4*r to the joint. r is a frozen formula over
two counters. This is a hand-set bias with extra steps, no different
in kind from DEVANG4's margin weight."

Defense and honest assessment:

(a) The DECISION differs observably where old signals are
provably silent. On Family E the frozen DEVANG4 joint ranks the
wrong analysis first on all six probes by the frozen lexicon
arithmetic (40 vs 30, no tie, no beam luck); POSSEG ranks the truth
first (46 vs 24). The information doing the work (FIN_KNOWN /
FIN_NOVEL) is unreadable by any prior segmenter: DEVANG4's
segmenter signature has no access to it. A parameter tweak cannot
use information the old mechanism cannot read.

(b) The regularity is LEARNED, not hardcoded. The frozen part is
the weight 4; the strength r is estimated from the learner's own
segmentation history and is developmental (near 0 in cold start,
about 4 after Family A). A hardcoded prior would fire from episode
0; FINREG does not. The builder verified this property by
inspection of the update site (single site, pre-bump counts), not
by tuning.

(c) BUT: the red-team notes FINREG is a thin signal: one positional
prior (utterance-final), not a syntax learner. The prereg discloses
this ("one positional prior, not a syntax learner"). The structural
claim is correspondingly narrow: segmentation now conditions on
induced positional syntax, a new signal class, and that class does
load-bearing work (K_DISC gap 4). It is not claimed to be a general
solution to segmentation.

(d) The no-scene path change (seg_dp replaced by seg_posseg with
scn=0) is the honest answer to DEVANG4 red-team 1b ("the structural
difference exists only where a scene is present"). The new
mechanism now engages without a scene. The red-team confirms this
is a real change, not a comment change: K_SEG 12/12 was produced
through the new path.

Verdict on claim (1): structurally different (new information
class, learned, engaged with and without scene), but narrow (one
prior). Not a relabel.

## 2. Is the K_DISC pass real discrimination or an artifact?

Attacks considered:

(a) "Family E was designed by the same builder who designed the
mechanism; the 6/6 is circular." Counter: the discriminator's
adversarial structure (wrong analysis wins lexicon outright, 40 vs
30) was validated against the FROZEN DEVANG4 binary post-freeze
pre-implementation (2/6 measured, premise holds). The builder did
not tune the mechanism to Family E: the mechanism was fully
specified in the frozen prereg, and the Family E joints were
PREDICTED there (46 vs 24) before implementation existed. The
prediction confirmed exactly.

(b) "The premise passed only barely (2/6 = threshold)." True and
disclosed. The premise is a measurement, and 2/6 satisfies <= 2/6.
The red-team notes the fragility: had the frozen baseline scored
3/6, K_DISC would have failed as premise-failed. The builder does
not claim headroom on the premise; the discrimination gap (6/6 vs
2/6) is what carries the claim.

(c) "E2/E6 went right under the baseline for unknown reasons; maybe
POSSEG's 6/6 is partly luck." The builder could not hand-derive the
E2/E6 baseline behavior (documented in BUILD-LOG). However: POSSEG
got E2/E6 right AND E1/E3/E4/E5 right, while the baseline got only
E2/E6. The four probes where the baseline provably fails by
arithmetic (40 vs 30) all flipped under POSSEG. The mechanism
accounts for the flips it was designed for; the E2/E6 baseline
behavior remains unexplained but does not favor the baseline.

(d) Knowledge-vs-architecture confound: "Does POSSEG win because of
the FINREG signal, or because of something else in the
implementation?" The K_DELTA audit confines the implementation
delta to the FINREG machinery (119 diff lines, all reviewed). The
only behavioral delta is the finalTerm. The gap is attributable.

Verdict on claim (2): real discrimination, honestly bounded.

## 3. The K_ABL failure: miscalibration or excuse?

Attack: "You failed a frozen bar and are reclassifying it as
'bar-miscalibration' to protect the mechanism. This is exactly the
retroactive bar-weakening the governance forbids."

Defense:

(a) The verdict follows the frozen bar: BUILD-FAIL is reported,
not re-scoped. No bar was altered. The classification
(bar-miscalibration vs mechanism defect) does not change the
verdict; it changes what the next wave should do. That distinction
is legitimate and required for the research to progress.

(b) Evidence it is miscalibration, not mechanism defect:
(i) the learner scores 12/12 while the ablation scores 6/12: the
front-end doubles the ablation's score, which is the substantive
content of "load-bearing"; (ii) K_AUD passes, so the failure is
not the DEVANG2 segmentation-independence mode the bar was
designed to catch; (iii) the threshold (<= 5/12) was copied from
DEVANG4's prereg where the ablation scored 1/12 on longer words,
without adjusting for B-doubleprime's 3-char-heavy composition
where fixed-3 is accidentally correct. The builder should have
recalibrated; that is a prereg-authoring error, owned here.

(c) The red-team considered and rejected the alternative
classification "the front-end is not load-bearing": 12/12 vs 6/12
plus the K_DISC gap refute it.

(d) Fabrication check: all numbers come from mechanical scorers
(scoree prints only aggregates) or binary stdout; 3/3
byte-identical hashes recorded; no hand-computed number enters
any bar. The one hand-scored element (K_DISC premise) was
machine-generated output compared against prereg-explicit lines.

Verdict on claim (3): the failure is real (frozen bar missed),
the classification as miscalibration is evidenced, and the
BUILD-FAIL verdict stands regardless.

## 4. Metric gaming check

- K_SEG 12/12: the generator was validated solvable (throwaway
  12/12) but the sealed set was never read; the bar (raised to
  10/12) was met with headroom. No gaming.
- K_SEAL 14/20: met; the C2 tie is disclosed, not hidden.
- K_DISC 6/6: predicted in prereg, confirmed. No post-hoc tuning
  (no code change after any Family E observation; the only
  post-implementation Family E run is the sealed run itself).
- Family A numbers identical to DEVANG4: not copied; independently
  produced by the new binary (dev_fama.log). The identity is the
  finding (no regression), verified by diff of the two binaries'
  outputs during development.

## 5. Strongest remaining attack on the mechanism

FINREG learns exactly one regularity (utterance-final), and its
strength r saturates (ilog grows slowly). In domains where
utterances do not end with known words, r collapses toward 0 and
the mechanism reduces to DEVANG4. The C-doubleprime tie with C2
(14/20 each) shows the mechanism adds nothing where the vocabulary
is novel. The queued DEVANG6 work should either (a) generalize the
positional signal (more positions, conditional on utterance shape),
or (b) admit FINREG as a narrow prior and move the frontier to a
different signal class. The builder does not claim FINREG is the
last segmentation mechanism.

## 6. Process notes

- No forbidden executable invoked at any stage (pure Zag; safebin
  throughout; `which python3` empty).
- Commit order: prereg (6e787022b) < baseline (d19290d6f) <
  implementation (5c4848f93) < sealed package (cb8455d07) <
  sealed runs (this wave). Verified via git log.
- The prereg section 13 classification mapping did not cover the
  observed K_ABL failure mode; the builder overrode it with
  evidence and recorded the override in SEALED_EVAL.md rather
  than silently reclassifying.
- One prereg erratum (C-doubleprime "12 words" vs 11 listed)
  recorded in BUILD-LOG.md; the explicit list governed.
- No em dashes in any lane file (check_no_dash.sh clean).
