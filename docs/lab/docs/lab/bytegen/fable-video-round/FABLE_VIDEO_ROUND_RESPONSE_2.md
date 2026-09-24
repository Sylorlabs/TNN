**Kill:** If S2 STILL-claim true-positive rate >10% at <1 scale-px displacement, path (a) is falsified — finer scales are hallucinating motion.

**Test 2: E_FLOOR recalibration around the p006 anomaly**
- **What it does:** p006 (ebar=57) triggered AMBIG despite E_FLOOR=64. Either the ebar measurement is wrong, or E_FLOOR is miscalibrated. Recompute ebar for p006 using the reference implementation from the S2 descriptor. If ebar is truly 57, sweep E_FLOOR from 50 to 70 in steps of 2 and measure AMBIG rate on the frozen battery.
- **Discriminator:** If lowering E_FLOOR to 56 makes p006 directional without breaking the frozen clips that currently pass (STILL at high ebar), E_FLOOR=64 is too conservative and the threshold needs recalibration. If p006's ebar is actually >64 when recomputed, the measurement code has a bug.
- **Kill:** If E_FLOOR ≤56 causes >5% of frozen-battery STILL clips to flip to directional, the energy floor is not the problem — p006 is genuinely ambiguous and the authority rule is working as designed.

**Test 3: Diagonal-anisotropy probe at 6px downsampling**
- **What it does:** The 6px downsampler averages 6×6 source blocks into single pixels. Diagonal motion at 45° experiences √2× more inter-pixel blending than axis-aligned motion, potentially lowering coherence. Generate synthetic clips with pure 45° motion at 1px/frame displacement and pure horizontal motion at the same displacement. Measure S2 coherence and directionality for both.
- **Discriminator:** If diagonal coherence is systematically lower (≥10% relative drop), the downsampler introduces anisotropy that biases the motion detector. If coherence is identical, the incoherence at 6px is not a downsampling artifact.
- **Kill:** If synthetic 45° motion at 1px/frame displacement produces coherence <0.6 while horizontal produces >0.7, the downsampler is guilty and needs a rotationally invariant filter (Lanczos, bicubic).

---

## 3. Where does the video path go next?

The video path is architecturally stable but strategically stuck. Three load-bearing questions have gone unasked:

### The 35 AMBIG real-world clips: wisdom or cowardice?

The system withholds on 35 real-world clips, calling them AMBIG. The authority two-piece rule says: trust S2 for STILL, trust S1 for direction when S2 is directional. AMBIG is the escape hatch when S2 is directional but energy is low. 

**The unasked question:** Are these 35 clips genuinely ambiguous, or is the system covering for a motion detector that hallucinates direction at low SNR?

**Experiment to answer it:** Human-label the 35 AMBIG clips for ground-truth motion (STILL / directional-with-consensus / directional-no-consensus). Measure S2's directional-claim true-positive rate on this set. If >60%, AMBIG is conservative but directional claims are trustworthy. If <40%, S2 is noisy at low energy and the authority rule is load-bearing. The 35-60% zone is the danger zone: the system can't tell signal from noise, and the path must either raise E_FLOOR or add a third-party adjudicator (S3, or a temporal-consistency filter).

### The diagonal incoherence at 6px: kernel guilt or motion chaos?

At 6px, diagonal motion produces lower coherence than axis-aligned motion in synthetic tests. Two hypotheses:

1. **Kernel guilt:** The 6×6 block-average downsampler blurs diagonal edges more than horizontal/vertical edges, reducing coherence.
2. **Motion chaos:** Real-world diagonal motion at 6px scale often involves sub-pixel wobble, rotation, or multi-object complexity that axis-aligned motion at the same scale doesn't.

**The unasked question:** Is the anisotropy in the kernel or the world?

**Experiment to answer it:** Test 3 above (diagonal-anisotropy probe) answers the kernel question. To answer the world question: filter the real-world 6px battery for clips with pure translational motion (no rotation, no sub-pixel jitter) using optical flow ground truth. Measure diagonal vs horizontal coherence on this clean set. If anisotropy persists, the world is guilty. If it disappears, the messy real-world clips are confounding the kernel test.

### The motion detector and the authority rule: partnership or crutch?

The two-piece authority rule exists because S2's directional claims are less reliable than S1's at low energy. But the motion detector (S2 coherence + ebar) was designed to *detect* motion, not *describe* it. The path treats S2 as both detector and describer, then overrides the descriptor half with S1 when S2's energy is low.

**The unasked question:** Should S2 be a pure detector, with S1 always describing direction when motion is detected?

**Experiment to answer it:** On the frozen battery, measure S1 vs S2 directional-claim agreement when both are directional. If agreement is >90%, S2's directional claim is redundant and the architecture can simplify to: S2 detects (STILL/MOVING), S1 describes (direction/path). If agreement is <70%, S2 and S1 see different motion fields, and the two-piece rule is adjudicating a genuine disagreement. The 70-90% zone means S2 adds marginal information — keep it but treat it as a tiebreaker, not an authority.

---

## 4. Ranked list of concrete, buildable experiments

Each experiment below is preregisterable: a native crew can execute from this description without interpretation.

### **Rank 1: S2 STILL-claim true-positive rate at <1 scale-px (Test 1)**
- **What to build:** Scan all frozen-battery clips where S2 claimed STILL and displacement (from ground truth or optical flow) is <1 scale-px. Count true positives (STILL claim correct) and false positives (finer scale claims direction).
- **Discriminator:** True-positive rate.
- **Kill threshold:** If >10%, path (a) is falsified.
- **Why first:** Directly tests path (a)'s core claim. Fastest to run (no new code, just analysis). If it kills path (a), saves all downstream work.

### **Rank 2: E_FLOOR recalibration on p006 (Test 2)**
- **What to build:** Recompute ebar for p006 using reference S2 code. If ebar <64, sweep E_FLOOR from 50 to 70 in steps of 2. For each threshold, measure: (1) Does p006 become directional? (2) How many frozen-battery STILL clips flip to directional?
- **Discriminator:** STILL-clip flip rate as E_FLOOR drops.
- **Kill threshold:** If >5% of STILL clips flip when E_FLOOR drops to p006's ebar, E_FLOOR is not the problem.
- **Why second:** p006 is the cleanest anomaly. If E_FLOOR is wrong, this is the smoking gun. If E_FLOOR is right, this rules out threshold miscalibration and focuses attention on the motion detector itself.

### **Rank 3: Diagonal-anisotropy kernel probe at 6px (Test 3)**
- **What to build:** Generate synthetic clips: (1) Pure 45° motion at 1px/frame, (2) Pure horizontal motion at 1px/frame. Both 100 frames, single moving object on static background. Downsample to 6px scale using the production 6×6 block-average kernel. Measure S2 coherence and directionality for both.
- **Discriminator:** Relative coherence drop for diagonal vs horizontal.
- **Kill threshold:** If diagonal coherence is ≥10% lower, the kernel is guilty.
- **Why third:** Tests a specific architectural hypothesis (kernel anisotropy) that, if true, requires a kernel swap (Lanczos/bicubic). If false, rules out a red herring and refocuses on motion-field complexity.

### **Rank 4: Human-label the 35 AMBIG clips**
- **What to build:** Export the 35 real-world AMBIG clips. Three human labelers (motion-tracking experience, blind to system output) label each clip: STILL / directional-with-consensus (≥2 labelers agree on direction within 45°) / directional-no-consensus. Measure S2 directional-claim true-positive rate against consensus labels.
- **Discriminator:** True-positive rate on human-consensus directional clips.
- **Kill threshold:** If <40%, S2 hallucinates direction at low energy and the authority rule is load-bearing. If >60%, AMBIG is over-conservative.
- **Why fourth:** Expensive (human labor), but answers whether AMBIG is wisdom or cowardice. If AMBIG is cowardice, the system can be more aggressive. If AMBIG is wisdom, the motion detector needs hardening before the system can drop the escape hatch.

### **Rank 5: S1-S2 directional-claim agreement when both are directional**
- **What to build:** Filter frozen battery for clips where both S1 and S2 claim direction (not STILL, not AMBIG). Measure angular agreement: ≤45° = agree, >45° = disagree. Report agreement rate.
- **Discriminator:** Agreement rate.
- **Kill threshold:** If <70%, S1 and S2 see different motion fields and the two-piece rule is adjudicating a genuine disagreement (keep it). If >90%, S2's directional claim is redundant (simplify to S2=detector, S1=describer).
- **Why fifth:** Architectural simplification question. Only matters if the system works; if path (a) is dead or AMBIG is broken, this question is premature. But if the system is basically sound, this determines whether the two-piece rule is load-bearing or a relic.

### **Rank 6: Temporal-consistency filter for AMBIG**
- **What to build:** For each AMBIG clip, check the 5-frame window before and after. If ≥3 neighboring frames are directional and agree on direction within 45°, override AMBIG and adopt the neighbor consensus. Measure: (1) How many AMBIG clips flip to directional? (2) Ground-truth accuracy of the flipped clips (requires human labels from Rank 4).
- **Discriminator:** True-positive rate on flipped clips.
- **Kill threshold:** If <50%, temporal consistency is a bad heuristic (motion can change frame-to-frame). If >70%, the single-frame motion detector is brittle and temporal context rescues it.
- **Why sixth:** Only makes sense after Rank 4 (need to know if AMBIG is over-conservative). If AMBIG is wisdom, this experiment is pointless. If AMBIG is cowardice, this tests whether temporal context can recover the withheld clips.

---

## Verdict

**Path (a):** S2 false-positives at fine scale.

**Reasoning:** The p006 anomaly (ebar=57 triggering AMBIG) and the 35 real-world AMBIG clips both suggest the motion detector is conservative, not aggressive. If S2 were hallucinating direction, we'd see AMBIG clips with high energy and clear motion; instead, we see AMBIG clips with low energy and human-legible ambiguity. The frozen-battery success rate (73/74 STILL-claim agreement across scales, plus the 1 sub-1-scale-px case) is too clean for a false-positive problem. Path (a) predicts we'd see STILL claims at S2 contradicted by finer scales at >1 scale-px displacement — the data says this happens ~1% of the time, not 10-20%.

**Path (b) implication:** The motion detector is sound. The 35 AMBIG clips are withheld because the system correctly recognizes low-SNR ambiguity. The diagonal incoherence at 6px is either a kernel artifact (fixable with a rotationally invariant downsampler) or a real-world motion-complexity effect (not fixable without a more sophisticated motion model). The authority two-piece rule is load-bearing: S1 and S2 likely disagree on direction at low energy, and the rule arbitrates.

**Single most important next experiment:** **Rank 1 (Test 1: S2 STILL-claim true-positive rate at <1 scale-px).** If this kills path (a), the entire investigation pivots to hardening the motion detector (raising E_FLOOR, adding temporal consistency, or replacing S2 with a learned model). If this validates path (a)'s absence, the system is architecturally sound and the work shifts to tuning (E_FLOOR recalibration, kernel anisotropy, AMBIG thresholds). This experiment is the hinge.
