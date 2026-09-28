# VERDICT: pig-front generation audit — the 22 px, Fable, and the first honest generator

Date: 2026-09-26. Standing law under test: **"TNN shouldn't draw it should generate."**
Workdir: `~/workspace/pigfront/teach`. Prototype: `gentex.zag` (pure Zag, zero RNG).

## 1. The 22 px head-placement error, decomposed white-box

The committed taught run (`7a70c828dd39`) reported head error 22 px. Measured values:

| Quantity | Value | Source |
|---|---|---|
| Plan head center | (160, 112) | `taught_trace.txt` PLAN |
| Truth detector head centroid | (182, 112) | `compare_forka` on sealed forka front |
| Error | dx=22, dy=0, Manhattan 22 | subtraction |
| Plan snout | (182, 173) | taught trace |
| Truth snout | (186, 175) | detector |
| Taught ears | L=(74,42), R=(253,37) | taught trace (matched truth) |

Source inspection of the taught branch found the cause directly:

```zag
let hcy:i64 = 112;
h_put64(PLAN, 0, 160);   // head x = frame midpoint, HARDCODED
h_put64(PLAN, 8, hcy);
```

The comment above this code explains only the **vertical** placement (reasoned from ears and snout). The horizontal coordinate was never learned, never measured, never deliberated — it is the frame midpoint. Final decomposition:

| Candidate cause | Contribution to the 22 px metric |
|---|---|
| Hardcoded head x = 160 (frame center) instead of a learned/deliberated value | **22 px nominal — the entire reported error** |
| Renderer rounding, ellipse rasterization, deterministic texture seeds | **0 px** to this metric (it compares PLAN directly against the detector; none of those move PLAN) |
| Truth-detector uncertainty | **±1–3 px near nominal** (local luma-band perturbations: 60..175 → (181,112); 80..175 → (184,110); 70..165 → (179,122); 70..185 → (182,110)); up to **16 px under broad threshold changes** (60..185 → (166,114)). The detector centroid is not immutable ground truth |
| Snout descriptor/scaling residual (the small-error class) | dx=4, dy=2 — real but separate from the 22 px |
| Missing machinery/knowledge | **load-bearing**: no learned layout atom connects taught features (ears, snout) to the head centroid; the teaching-frame head centroid was never measured or stored |

Do not add detector uncertainty on top of the 22: the correct statement is **22 px nominal, with ±1–3 px detector uncertainty near nominal**. The 22 is not a renderer defect and not a noise artifact. It is a hardcoded centering assumption standing where a learned layout relation should be.

Cross-check on rendered images (independent Python detector, same band): old render head centroid (155.5, 109.1) → 26.5 px from truth; new prototype render (156.8, 104.0) → 25.2 px from truth. Same cause, same magnitude. The prototype deliberately did not touch placement.

## 2. Fable consultation

Fable (claude-fable-5.1 via UnoRouter streaming) was asked for: (A) a mechanistic drawing-vs-generating distinction with a testable line, (B) the minimal atom set, (C) how pixel synthesis should work under determinism, (D) the smallest honest step, (E) traps, (F) how the pig-front case should change. Three attempts were needed: the first returned EMPTY-CONTENT; the second returned a 3,579-char answer truncated mid-sentence; the continuation (10,080 chars) **drifted off TNN's constraints** (random coefficient sampling, PCA morphing, EfficientNet classifiers, learned inpainting — neural nets and RNG are both banned). Both substantive answers are quoted verbatim in §7. Ruling:

**Adopted (compatible with standing law):** the draw-vs-generate line — *"if any pixel's final value depends on a term that was invented rather than measured, it is drawing"*; patch atoms as measured micro-patterns clustered by measured frequency signatures; transition atoms as measured adjacency/co-occurrence; layout atoms as measured part centroids/sizes/overlaps. The prototype below implements the degenerate case (whole-region patches + measured color deltas) and passes the line test.

**Rejected (incompatible):** the continuation's synthetic-data pipeline — normal-distribution sampling (zero-RNG law), EfficientNet/segmentation/inpainting models (no neural machinery), hue/texture jitter (invention). Preserved verbatim as evidence, not used.

## 3. The prototype: measured-field texture transfer (`gentex.zag`)

Design: learn nothing analytic. Read the sealed teaching photograph, measure source regions, and construct each target part as **measured source pixel + measured color delta**. No ellipse shading, no `pf_hash2`/`pf_grain`/`pf_vnoise`, no invented gradients.

Measured quantities (all from the teaching photo, in-program):
- Head source region: flood-fill bbox under the same luma gate as `compare_forka` (note §5.4: it merges head+background — documented, not hidden)
- Background: mean of four 20×20 corner blocks = (138,127,114)
- Region means: head (142,133,127), snout window (88,75,77), earL (134,119,114), earR (96,104,104)
- Color deltas = plan color − source mean: head (−105,−100,−92) toward plan (37,33,35) [OBSERVED 24/24 side views]; snout (−25,−22,−20) toward plan (63,53,57) [TAUGHT frontal]; ears (0,0,0) — no plan color held, measured color kept

Target geometry = the committed taught plan (head (160,112) r=(86,86); snout (182,173) r=(73,49); ears (74,26)/(246,26) r=(11,21)). Region boundaries remain ellipse equations — the plan's deliberate construction decisions, documented as the remaining drawing primitive.

Test results:

| Check | Result |
|---|---|
| Byte-identical reruns | sha256 `8575e46a…` on two runs — identical |
| Transfer exactness (the line test) | 3,000/3,000 sampled pixels equal `measured_source + measured_delta` exactly — **no invented term in any checked pixel** |
| Texture fidelity, photo head region | residual std 12–14, lagH 0.66–0.82, lagV 0.51–0.59 (directional fur structure) |
| Texture fidelity, old render head region | residual std **1.1**, lagH 0.34, lagV 0.39–0.46 — the old "realistic" texture is nearly flat at 9-px scale; invented noise with no measured structure |
| Texture fidelity, new render head region | residual std 18–19, lagH 0.57, lagV 0.60 — measured structure preserved, same order as the photo |
| Head placement (new render) | detector (156.8,104.0) → 25 px from truth — **not fixed, by design** |
| Eyes | none drawn — P2 still not held; epistemic map untouched |

(Texture numbers cross-checked by an independent Python implementation; Zag and Python agree. Residual = pixel − 9×9 box mean; lags = lag-1 autocorrelation of residuals.)

Plain-English reading: the old renderer painted smooth dark ellipses with invented grain so fine it is statistically almost nothing. The new construction pastes real photographic fur — you can see individual strands and the snout's real nostrils. It is uglier at the edges (hard ellipse seams, flat background) but every pixel is accounted for: measured, or an explicitly documented construction decision.

## 4. What is missing (honest list)

1. **Learned layout atoms** — the 22 px cause. Nothing connects taught ears/snout to head-x.
2. **Patch atoms at finer granularity** — the prototype transfers whole regions; Fable's micro-pattern clustering (patch library + measured frequency signatures) is not built.
3. **Transition atoms** — seams are hard ellipse edges; no measured adjacency/co-occurrence between patches.
4. **Source segmentation** — the teaching photo's band mask merges head and background into one flood component, so the "head source region" includes background pixels. A better-measured region is needed.
5. **Region boundaries still drawn** — ellipse equations are deliberate construction decisions, not measurements.
6. **Flat background** — measured mean color only, no measured texture.
7. **Placement derivation not deliberated** — the head-x rule below is specified, not implemented.

## 5. Specified follow-ups (not yet built)

- **Head-x derivation.** Replace `h_put64(PLAN, 0, 160)` with a deliberated estimate from held measurements. Measured candidates on the committed taught values: ear-mid x = (74+253)/2 = 163.5 → 18.5 px error; taught snout x = 186 → 4 px error; mean(ear-mid, snout-x) = 174.75 → 7 px error. Any beats 22 px; the choice of rule must be deliberated (and preregistered before testing), not cherry-picked after seeing truth.
- **Patch atoms + transition atoms** per Fable's compatible atoms (§2, §7): build a measured patch library from the teaching photo, cluster by measured frequency signature, select deterministically, seam by measured boundary disagreement, abstain (`NO_MATCH`) where no patch fits.
- **Audit the other generation lines** with the same line test (audio synth ban already exists; image/video imagination lines need the pixel-provenance audit).

## 6. Bottom line for Micah

The 22 px was never a renderer problem — the taught branch hardcoded head-x to the frame midpoint, and no learning ever touched it. The old "realistic renderer" failed the generation test too: its texture is statistically almost flat, invented grain with no measured structure. The new prototype is the smallest honest step: photographic pixels, measured deltas, every pixel accounted for, byte-identical reruns, no invented eyes. Placement still wrong by ~25 px, edges still drawn — the verdict names exactly what is missing rather than banking the 22 as a win.

## 7. Fable transcripts (verbatim)

### 7a. First attempt — EMPTY (kept for the record)

File `fable_answer_gen.txt` (136 bytes):

```
[streamed chars=46 reasoning_chars=0 usage={}]
EMPTY-CONTENT: streamed result too short.
I am Claude Fable 5.1, developed by Anthropic.
```

### 7b. Second attempt — the useful answer (truncated mid-sentence at "stored as integer multi")

File `fable_answer_gen2.txt` (3,643 bytes). Verbatim:

```
A. **Mechanistic distinction: drawing vs generating**

Drawing: a human-authored analytic function maps spatial coordinates to pixel values. Ellipse(r, c, shading-gradient, noise-function) → color. The function is invented to *look like* the thing. The pixel's value is computed from a geometric model plus a hand-authored appearance model. The "knowledge" is the function signature and parameters.

Generating: a pixel's value is looked up or interpolated from a learned representation of *real data*, where that representation was extracted from photographs by statistical/compression operations (not authored). The function didn't exist before learning; the representation is the function.

Where the line is: if the pixel value depends on an equation someone wrote (ellipse, gradient, noise hash), it's drawing. If the pixel value depends on a representation extracted from real pixels via measurement operations (histograms, correlations, frequency decompositions, co-occurrence tables), it's generating — even if the extraction was simple. Measured texture pasted into a region is *generating* IF the pasted data was extracted from real photos by TNN's own primitives and IF placement preserves measured spatial statistics. It becomes drawing-with-extra-steps if: (a) the extraction discards the spatial structure that makes it photographic, or (b) placement ignores measured spatial relationships, or (c) a hand-authored function (gradient, noise) is interpolated between or on top of the extracted data.

The line: **does any pixel's final value depend on a term that was invented rather than measured?** If yes → drawing.

B. **Concrete architecture**

**Atoms are not shapes. Atoms are measured micro-patterns extracted from real photographs.**

Three atom vocabularies, each learned by measurement:

**1. Patch atoms (local texture)**
Operation: take a real photo, extract all overlapping N×N patches (say N=16) from a specific texture region (e.g., short fur on a flank). For each patch, record: the raw pixel grid, its local mean color, its local color-gradient vector, and its local frequency signature (a small integer encoding dominant spatial frequency and orientation — computed by a small-window DCT or simply horizontal/vertical/both energy ratio, all integer arithmetic). Cluster patches by (frequency-signature, mean-color-bucket, gradient-bucket). Each cluster centroid (or the cluster representative closest to centroid in L1) becomes a patch atom. Store: the raw N×N pixel data, its cluster label, and its measured metadata.

Quantity: a few hundred atoms per texture class (flank fur, ear skin, wet snout, eye rim) from maybe 50 source photos. Entire vocabulary fits in a few MB.

**2. Transition atoms (spatial adjacency rules)**
Operation: for each pair of texture classes that border each other in real photos (fur→ear, fur→snout), measure the statistics of how one class's patches transition to another's. Specifically: at the boundary, measure the frequency with which patch atom A from class X is horizontally/vertically adjacent to patch atom B from class Y. Store as a sparse co-occurrence table: {(atom_A, atom_B, direction): count}. Also measure the offset: when A borders B, what is the sub-pixel alignment shift (in pixels) that maximizes visual continuity? Store this as an integer offset.

**3. Layout atoms (spatial arrangement of parts)**
Operation: from real frontal photos of pigs, measure: part bounding boxes, part centroids, part overlap zones, color gradients across each part (top-to-bottom, left-to-right, stored as integer multi
```

(Note: the stream ended mid-sentence at "stored as integer multi" — that is where Fable stopped, not an edit.)

### 7c. The prompt that produced 7b (verbatim)

```
You are consulting on a hard architecture design question for TNN, a native AI system. Be concrete and mechanistic, not poetic. We will test the testable parts of your answer.

BACKGROUND
TNN is built in Zag (a low-level systems language): pure deterministic code, ZERO randomness anywhere in decision paths, byte-identical reruns required. No neural networks, no learned weights in the LLM sense, no tokenizer — raw bytes in, raw bytes out. Knowledge is stored as discrete atoms in a vocabulary; construction is deliberate (explicit placement decisions, audited).

THE PROBLEM
We have a "pig-front" experiment: TNN saw 24 side-view frames of a pig, then was taught one frontal photo (positions/colors of snout and ears measured from the real photo by TNN's own vision primitives — no hand-fed facts). TNN must construct what the pig's front looks like.

The current "realistic renderer" draws the construction like this (actual code): for each body part, rasterize a feathered ellipse; per-pixel color = base_color * (radial shading gradient) * (vertical lighting gradient) + hash(x,y,seed) noise for "fur grain" + value-noise for "mottle". All deterministic (integer hash of coordinates, no RNG). Epistemic labeling is separate: unknown regions render as flat unresolved fur, never invented detail.

This fools nobody. The lab director's verdict: "TNN shouldn't draw, it should generate. Current AI image generators would look horrible if they used drawings." He's right — a feathered ellipse with procedural noise is drawing, however nice the shading. A diffusion model never evaluates an ellipse equation; it samples pixels from a learned distribution.

Also relevant: TNN's image line has a vocabulary of SHAPES atoms (the honest-upscale experiment showed atoms that genuinely match are bit-exact, but the vocabulary is sparse and the system forces top-level blocks to take an atom even when none fits — we're adding a real "no atom fits" reject).

THE HARD QUESTION
What would a TNN-native image GENERATOR be — raw bytes out, photographic, using no drawing primitives (no ellipse equations, no analytic shading gradients, no invented noise)?

Constraints you must respect:
1. Deterministic: same knowledge + same construction intent = byte-identical pixels. No RNG, no stochastic sampling. (Deterministic given state — a fixed seed derived from the construction intent is acceptable if you explain exactly what it seeds.)
2. Knowledge is discrete atoms + deliberate construction decisions, all auditable. No black-box weight matrices.
3. It must be able to say "I don't know this region" (epistemic honesty is load-bearing, not a nice-to-have).
4. It must produce photographic pixels — fur that looks like photographed fur, not shaded noise.

Questions:
A. Mechanistically, what is the difference between drawing and generating? Is "measured texture pasted into a region" generating, or drawing with extra steps? Where exactly is the line?
B. Sketch the concrete architecture: what are the atoms of a TNN-native generator (not shapes — what?), how are they learned from real photos, and what is the pixel-synthesis step that turns atoms + a construction plan into photographic bytes WITHOUT evaluating any geometric primitive or shading equation?
C. How does deliberate construction interact with pixel synthesis? Who decides each pixel's value — the deliberator, the atom, or something else? Be specific about the data flow from "snout goes here, color like this" to actual bytes.
D. What knowledge must TNN hold that it currently doesn't? (Our diagnosis: it holds part positions and mean colors, but no texture statistics, no spatial distributions, no lighting model — and its head-center x was a hardcoded frame-center constant, correct only by luck.)
E. What is the smallest honest step from the current fur-ellipse renderer toward your architecture — something implementable in a few hundred lines of deterministic systems code, testable against a real photo?
F. Name the traps: what looks like progress toward generation but is still drawing?

We will implement (E) and measure it. Do not flatter us; tell us plainly if you think the constraints make photographic generation impossible and why.
```

### 7d. Continuation — DRIFTED OFF-CONSTRAINTS (verbatim, preserved as evidence, rejected in §2)

Continuation prompt (verbatim):

```
Continue exactly where you stopped. Your previous response ended mid-sentence at:

"**3. Layout atoms (spatial arrangement of parts)**
Operation: from real frontal photos of pigs, measure: part bounding boxes, part centroids, part overlap zones, color gradients across each part (top-to-bottom, left-to-right, stored as integer multi"

Pick up from there and complete sections B (finish layout atoms, then the pixel-synthesis step and data flow), C, D, E, and F. Keep the same concrete, mechanistic style. Do not repeat sections A or the beginning of B.
```

Continuation answer (verbatim — begins mid-sentence where 7b cut off):

```
ples at fixed intervals along each axis), and adjacency relationships (which parts are always touching, which never overlap).

These form a **layout-atom vector** per category: for each of the ~8 semantic parts, store its relative x/y centroid (normalized to body bounding box), relative width/height, z-order layer, and the mean color-channel values (R, G, B, alpha) sampled from a 7×7 grid overlaid on that part region. Across thousands of labeled images of, say, "fox" or "dog," you average these vectors to get a **prototype layout template**—a ghostly mean-shape that represents the spatial-semantic prior for that animal class.

**Pixel-synthesis step:** Given the layout template, you instantiate it by: (1) placing each part's silhouette (from the mask bank in section A) at the template's centroid coordinates, scaled to the template's relative dimensions; (2) applying the template's color gradient as a per-pixel color map—each of the 49 sample points on the 7×7 grid acts as a control point for bilinear interpolation, so the entire part region gets a smooth color field that matches the learned average; (3) compositing parts back-to-front using the z-order layer (e.g., torso first, then legs overlapping where the template says overlap occurs, then head on top); (4) running a feathering pass on every seam where two parts meet—blending a 3–6 pixel band using alpha gradients so transitions look organic rather than hard-cut.

**Data flow:** The output is one RGBA image per category in the template gallery. These are not yet diverse—they are the *mean exemplar*—but they give downstream stages a solid anchor to morph from.

---

**C. Diversification (breaking the mean)**

Now you need variation. Three orthogonal axes of transformation, applied combinatorially:

**C1. Pose morphing.** Using the layout-atom vectors from a pool of ~50+ real images per category, compute principal components (PCA) of the centroid positions. The first 3–5 PCs capture the dominant modes of variation (head tilt, tail curl, leg splay). To generate a new pose, sample a coefficient vector **c** from a normal distribution (mean 0, std 1), multiply by the PC basis, add back the mean layout, and produce a *new* layout template. The silhouette masks from A are re-placed at the new centroids. This gives you hundreds of spatially plausible poses per category without collecting more images.

**C2. Color/texture jitter.** Perturb the per-part color gradients: shift hue by ±15°, saturation by ±20%, brightness by ±12% (in HSL space), independently per part but constrained so that neighboring parts stay within a perceptually harmonious range (e.g., don't make the belly neon blue while the back is brown—enforce a co-delta limit of ΔE < 30 in CIELAB between adjacent parts). Optionally, overlay micro-textures (noise patterns, stripe frequencies, spot densities) sampled from the texture bank described in A2, at varying scales and orientations.

**C3. Silhouette variation.** Rather than using only the mean silhouette from A, randomly sample from the pool of per-category silhouettes, or interpolate between two silhouettes via shape-space morphing (linear blend of their landmark coordinates). This gives outline-level variation even within a single pose template.

**Combinatorial explosion:** With 50 poses × 10 color variants × 5 silhouette variants = 2,500 candidate images per category. After a perceptual deduplication pass (SSIM > 0.92 pairs are collapsed), you typically retain ~1,200–1,800 visually distinct images per category.

**Data flow output:** A diverse candidate gallery per category, each image being a fully composited RGBA PNG with a matching segmentation label (every pixel knows which part it belongs to and what the source was).

---

**D. Adversarial validation and hard-negative mining**

This is the quality gate. Three sub-stages run in sequence:

**D1. Real-vs-fake classifier.** Train a lightweight binary classifier (EfficientNet-B0 or similar) on the real images from stage 0 versus the generated images from C. Let it overfit hard. Then use it as an oracle: any generated image it confidently (>0.95) classifies as "real" is likely convincing; any it flags as "fake" gets routed to the refinement loop (section E). Additionally, inspect the classifier's GradCAM attention maps—if it's focusing on a part boundary that looks painted or a color band that's unnaturally smooth, those are specific failure modes to fix.

**D2. Semantic consistency checker.** For each generated image, run an off-the-shelf part-segmentation model (trained on real data) and compare its predicted part masks against the ground-truth labels you baked in at generation time. Compute per-part Intersection-over-Union (IoU). If any part's IoU < 0.6, the pose is anatomically implausible—e.g., a leg placed where a tail should be. Reject or flag for re-layout.

**D3. Hard-negative mining.** Take the images that *passed* D1 and D2, and feed them into a downstream task model (e.g., a fine-grained classifier or pose estimator that will ultimately consume this synthetic data). Train it on real data only, then evaluate on the synthetic candidates. Images where the task model's confidence *drops* relative to similar real images are "hard negatives"—they're technically valid but contain subtle artifacts that fool feature extractors. These get special treatment: either discard them, or route them to E with explicit artifact annotations so the refinement knows what to fix.

**Data flow output:** A validated subset (typically 60–80% of candidates survive), partitioned into three tiers: high-confidence (pass everything), borderline (passed D1/D2 but flagged by D3), and rejected (sent to E). Each image carries metadata: source category, pose coefficients, color-jitter params, silhouette ID, validation scores, and rejection reason if applicable.

---

**E. Refinement and artifact correction**

Handles the rejected and borderline images from D:

**E1. Boundary cleanup.** The most common artifact. Use a small learned inpainting model (or a classical Poisson blending approach) focused on part-boundary bands. The input is the generated image plus a binary mask of the 4–8 pixel zone around every part seam. The model learns to reconstruct just that band using the surrounding pixel context, constrained by the segmentation label so it doesn't bleed semantic information across boundaries.

**E2. Color reharmonization.** For images where the D1 classifier's attention maps highlight color discontinuities: re-run the per-pixel color interpolation with additional control points sampled from neighboring parts, enforcing gradient continuity at seams (the derivative of the color field should be smooth across the boundary, not just the value).

**E3. Texture refinement.** If micro-textures look tiled or repetitive (detectable via autocorrelation analysis), re-sample with phase-randomized versions of the same texture, and apply a local frequency-mixing blend (turbulence noise used as a blending mask between two texture scales).

**E4. Loop closure.** After correction, re-run D1 and D2. Images that now pass join the validated pool. Images that fail a second time are permanently discarded—they represent cases the generative pipeline cannot currently handle (e.g., extreme poses at the edge of the morph space).

**Data flow output:** A smaller batch of rescued images, merged into the tier-1 validated pool from D. Total final inventory per category: typically 800–1,500 images after all stages.

---

**F. Deployment and utilization**

The validated synthetic gallery now serves multiple roles:

**F1. Training data augmentation.** Mixed with real images at controllable ratios (e.g., 3:1 synthetic-to-real) for training downstream vision models. Because every synthetic image has pixel-perfect segmentation labels, pose metadata, and part-level color annotations—all of which are expensive to obtain manually—you effectively get free dense supervision.

**F2. Class expansion.** For rare or endangered species where you have <20 real images, the pipeline can generate hundreds of plausible examples from even a single real reference image plus the shared part library. The quality won't match the 800+ image categories, but it's enough to bootstrap a detector.

**F3. Failure-mode debugging.** The metadata trail (which parts were used, which pose PCs were sampled, which color jitter was applied) makes it possible to *diagnose* why a downstream model fails on a particular input: trace back to which synthetic training examples were most similar, inspect their generation parameters, and identify systematic biases in the pipeline.

**F4. Continuous refresh.** As new real images accumulate (from cameras, web scraping, etc.), they feed back into stage 0, which updates the silhouette banks, part libraries, and layout templates. The entire pipeline reruns periodically, producing updated galleries. The old galleries serve as regression tests—if a pipeline update causes quality degradation, the D1/D2 scores on the new batch will drop relative to the old batch, triggering investigation.

**Final data product:** A versioned, annotated, RGBA image library per category, each entry carrying: the image itself, a per-pixel part-label map, pose coefficients, color-jitter parameters, silhouette source ID, and a quality score vector (D1 realness, D2 semantic IoU, D3 task-model confidence). Stored as a structured dataset (images in a tile-based format like COCO or TFRecords for fast loading; metadata in a relational index for querying). Total storage: roughly 50–120 MB per 1,000 images at 512×512 resolution including all annotation layers.

---

That completes the pipeline. The core insight across all six stages is the same: **decompose** the image into semantically meaningful, independently controllable factors (shape, color, texture, pose, arrangement), **recombine** them under learned constraints, and **validate** the output against both perceptual and task-driven criteria—closing the loop with targeted corrections where validation fails.[streamed chars=10080 reasoning_chars=0 usage={}]
```
