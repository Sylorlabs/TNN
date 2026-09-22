# FORK OPINIONS — B vs C visual imagination race

Compiled 2026-09-22. The lead's verdicts frame this document and are not relitigated: Fork A is DEAD ("looks the exact same"); Fork C "has potential but looks horrid right now"; Fork B "stunned" him as the most imagination-like. It is B vs C, B leading.

Voices: sol (gpt-5.6 via UnoRouter) · three fresh Muse-native critics (one interim A/C analyst who then completed B, two fully independent) · fifteen blind ordinary-vision judges (five per image, single question: "would you have guessed AI").

Normal vision throughout — no horror/genre priming, no hardcoded criteria, per the lead's law.

---

## 1. FORK B (r8b_alien_1024.png) — the unified trace

One interleaved act: deliberation and depiction alternate in a single program; the trace records depiction correcting deliberation three times (T10 dither, T11 moon, T12 orbit). A volcanic highland raymarched from a true 3D distance field under one deliberated sun vector. SHA/commit: see FORK_B report.

### What is genuinely good
- **One sun, one field.** Every shadow and shading gradient agrees on a single light direction — the massif's left faces glow amber, right faces fall dark, the sky warms toward the sun's azimuth and cools away. No per-asset light stories (Fork A's failure mode).
- **True 3D presence.** The raymarched field gives real occlusion — the massif has mass, the rift valley reads as carved, the near rubble lumps are smooth-min blended into one continuous surface. "Stickers are impossible by construction" is visibly true: none of A's pasted-stone halos.
- **Atmosphere continuity.** Aerial haze drowns distance toward the horizon color; sky and far ground meet in haze, not a hard backdrop line.
- **The feedback loop is real as a mechanism.** T10/T11/T12 record depiction judging deliberation — no other fork does this.

### The horrid list (located)
1. **The moon (upper left, ~x=20–120, y=45–145) is a black disc — measured, not impression.** Strict-interior pixel photometry: mean luminance ~11/255, max 14.6, no gradient in any direction. T12 claims "a young crescent (~14% lit, like a 3-day-old moon)" and "the dark side must read as a world" via planetshine. The render falsifies both. The feedback loop's flagship proof is a trace/image contradiction: it moved the moon and declared victory; the render still shows T11's black blob.
2. **Contour banding on the massif.** Elevation-following arc bands across the peaks (~x=150–500, y=280–520). T5 explicitly promises "strata live only in 3D noise on steep faces, never as contour rings." The image shows rings — the exact sin the trace disavows.
3. **The sun's disc — the "honesty anchor" — is missing.** T2: "I put the sun's disc IN the frame, low over the far ridge." Horizon crop: amber glow, no disc anywhere. The light has no visible source in frame.
4. **Ridge-line halo.** A pale band hugging the near hill's full silhouette (~y=640–700) reads as an edge artifact, not distant terrain.
5. **Clouds are flat smears.** Identical pale tone, no wind direction, no sun-side lighting — the same smear defect as A.
6. **Foreground unreadably dark.** "The near rubble must be the sharpest thing in frame" (T9) — but the foreground is a near-black field; the detail the trace is proudest of is buried by exposure. Dither speckle reads as white sparkle dots on ground and sky.
7. **Unexplained pale oval blob at the left horizon** (~x=30–90, y=490–510) — unaccounted shape, reads as artifact.

### Structural reading
B is a world-model raymarcher with a genuine see-then-reconceive loop — the only fork whose trace records depiction overruling deliberation. Strength: causal coherence (one sun vector, one field, everything asks the same field). Weakness: the conception is template procedural geology (fbm highland + ridged massif + noise-wandering rift + bowl-and-rim craters) — the procedural-terrain canon — and its defects are render-calibration failures the feedback loop saw but didn't fully fix. The loop corrects parameters toward the deliberated story rather than questioning the story: the moon got moved to make the crescent legible instead of the loop noticing the crescent never rendered.

### Ceiling at 10x
- The feedback loop is the ceiling-raiser — the only mechanism that can notice its own lies. But as run it tunes parameters toward the prior instead of reconceiving the prior; 10x more seeing gives sharper terrain with the same moon-shaped blind spot.
- The geology vocabulary is the ceiling: fbm + ridged noise + craters is the demo canon. 10x more is a sharper screensaver, not a more imagined world.
- No exposure discipline: near-black foreground and glowing sky coexist without a tone-mapping story. 10x detail at these exposures = 10x more buried pixels.

---

## 2. FORK C (r8c_alien_1024.png) — mind's-eye elaboration

Vague gist → 14 world decisions → 240 state-dependent fixations laying soft pigment dabs. Full treatment in CRITIC_AC_INTERIM.md; summary:

**Genuinely good:** the gas giant (upper right) is the most physically honest celestial body in the program — gradual terminator, night side retains zone structure, plausible limb darkening; the indigo-teal dusk mood hangs together as one continuous moment.

**Horrid (located):** (1) the "wind-carved arch" is a dark rectangular box with a cross inside it (~x=250–560, y=700–990) — the dab primitive cannot say "arch with an opening"; (2) the ventifact field (40 stones, dust tails) is absent; (3) the far-rim breach/dust glacier is absent; (4) the sky is empty despite 75 fixations claiming cirrus; (5) the moon is a smudged half-disc; (6) **fixation starvation, measured** — far rim 139 fixations, sky 75, gas giant 22, moon 4, stones/arch/hills/plain/breach/clouds **zero**. The interest map never let attention leave the focal anchor; 60% of the world commitments got nothing.

**Structural reading:** a painter that lights one sphere beautifully but cannot compose a world. Greedy attention starved the foreground; the single dab primitive can't express hard geometry, subtractive form, or linear features.

**Ceiling at 10x:** greedy-attention collapse (2400 fixations = photoreal far rim, still no stones), primitive bottleneck (sharper giant, same stamped box for the arch), world-commitment drift (the trace promises a world, the image shows ~40% of it — and the gap widens as Pass 2 gets more ambitious).

---

## 3. FORK A (r8a_alien_1024.png) — dead, for the record

**Genuinely good:** the big planet's marbled rust/teal texture; coherent three-tier composition; the central spire silhouette.

**Horrid (located):** (1) the planet's night side is pitch black — zero light transport, contradicting its own claimed one-sun logic; (2) terrain is paper-cut collage — flat purple ridge band and chocolate hill band with hard silhouettes, no slope lighting; (3) vertical striping artifacts through the ridge layer, shipped unrepaired; (4) foreground stones are pasted cutouts with no contact shadows or burial; (5) small moon with mismatched terminator; (6) grey-smear clouds with no wind or light direction.

**Structural reading:** an asset-composition pipeline — every new element is a new pasted layer; the light story is written per-asset, not per-world. **Ceiling:** the pastel-collage asymptote — more detail per layer only sharpens the edges between layers; no shared 3D scene means depth cues can only be faked per-stamp, and each fake adds inconsistency. Dead per the lead; no further repair.

---

## 4. sol's view

Consulted 2026-09-22 (gpt-5.6 via UnoRouter), normal vision, no horror/genre priming. Shown all three PNGs plus the lead's verdicts and the two measured contradictions (B's moon: black disc, interior max 16/255, vs the trace's claimed crescent; C's most-fixated region: local contrast std 10.25, smoother than the sky's 16.45).

**1. Which mechanism has the higher imagination ceiling: FORK B.** B's unified raymarched world-model can in principle generate new geometry, occlusion, depth, and lighting from one coherent scene representation — "unusual landforms can still cast the right shadows, recede in depth, and remain consistent under a changed sun." That is the path to a genuinely surprising image. C's ceiling is capped by the gap between its attention and its expression: soft dabs can enrich atmosphere, but are poorly suited to hard structures like arches, strata, or cliffs — the exact objects C's trace claims to render.

**2. Current ranking: B LEADS, BY A WIDE MARGIN.** "B is not cleanly successful, but it reads as a single landscape with a recognizable spatial organization: sky, distant terrain, mountain mass, and foreground. C reads more like an unfinished atmospheric painting whose intended objects are difficult to identify." The margin is on current image quality — "not necessarily permanent."

**3. Located defects.**

*Fork B:* (1) upper left — the moon is a featureless black disk, "especially damaging because the claimed crescent is a specific, visible semantic feature, and none of it appears in the render"; (2) bottom foreground crushed into near-black murk — the region the trace calls the sharpest has almost no readable form; (3) middle-to-lower horizon — a hard, nearly horizontal dark band reading as a compositing/terrain-boundary artifact, weakening the 3D impression.

*Fork C:* (1) lower foreground, center-left — the wind-carved arch reads as a dark rectangle with a cross-like mark; its primitive geometry is "visibly inadequate for the stated centerpiece"; (2) lower and middle terrain — a broad soft low-contrast wash with noise; the alleged strata are not legible; "the most-attended region is actually among the least structured parts of the image"; (3) upper-middle/right sky — planet and atmospheric marks compete as loose blobs; "no stable focal hierarchy: the planet is conspicuous, but the terrain does not establish a credible world beneath it."

**4. On the "B is the better image; C is the better mind" paradox: REFINED, not accepted.** "B is clearly the better image. C shows the more explicit self-monitoring procedure, because it revisits its own canvas and allocates attention. But the artifact does not demonstrate that it has a better mind. The fixation explanations are contradicted by the pixels, and its attention mechanism does not reliably improve the attended regions." sol's reformulation: **B has the better world model and picture; C has the more elaborate introspective control loop, but that loop currently lacks effective visual intervention.** Sharp note: "B may actually have the better underlying visual model, even though its trace overclaims what happened" — a direct challenge to Critic 2's ranking of C as the better mind.

**5. sol's decisive experiment — the relight test.** Identical brief to both forks: an alien canyon with a thin stone arch in the foreground, a crescent moon in the upper left, one visible cast shadow from the arch. Then rotate the sun 90° while preserving geometry and camera.
- **B passes iff:** the arch keeps recognizable hard geometry; the cast shadow moves consistently with the new sun; the crescent stays a crescent with its lit side changing consistently; depth ordering survives. **B fails** if the moon becomes a black disk again or the foreground collapses — proving the world and the renderer are coupled only by the author's hand.
- **C passes iff:** the arch is visibly an arch (not a rectangle); geometry is preserved across the revision; the shadow moves the correct direction; the crescent and terrain update without being repainted into unrelated soft blobs. **C fails** if the relight is a global color wash or the arch cannot survive as hard geometry.
The test's load-bearing question: "whether the mechanism has a reusable scene model rather than merely producing a plausible first-pass arrangement."

---

## 5. Native critics

### Critic 1 (interim A/C analyst, completed B)
The analysis in §§1–3 above is Critic 1's full treatment.

**Critic 1's B-vs-C ranking:** B wins on invented-vs-assembled — C is one beautifully lit sphere in a mood with ~60% of its world commitments missing; B is a whole world, all present, causally lit, with a mechanism that re-sees. But B's moon is a red flag exactly where B claims its unique strength (the feedback loop claimed a crescent; the render shows a disc).

### Critic 2 (fresh, independent)
Judged cold — never opened the interim analysis or round reports. All claims from the PNGs.

**Fork B:** Genuinely good — the dusk sky's color harmony (best of the three forks); the rim-lit ridgeline ("the most optically honest moment in the image"); the massif's ridged peak reading as real erosion-carved terrain. Horrid — (1) the moon is a featureless black disc (inner-disc mean ≈32/255, no crescent, no terminator), falsifying T12's reconception claim: "what renders is the very 'black disc' T12 says a black disc would mean 'the phase geometry failed'"; (2) the near rubble is an unreadable black knot — "the murkiest thing in frame," contradicting T9; (3) the haze band's ruler-straight top edge reads as a pasted stripe; (4) the pale-pink lozenge at (~180–340, ~490–590) — if this is the T2 "honesty anchor" sun disc, "it anchors nothing"; (5) stair-step tonal banding on far slopes; (6) pink-swirl marbling on dark rock reads as decoration, not strata; (7) the bottom third is featureless dark gradient with white speckle. Structural reading: a genuine single-world renderer — "everything optical is computed, everything geological is still procedural"; the failures cluster where computation was hand-specified (moon's phase specified not emergent; rubble = placed spheres, "the old family's sticker logic smuggled into the SDF"). The T10–T12 feedback episodes are real deliberation, "but note T10–T12 are all *photometric* corrections; none reconceived the world's content. The mind paints better than it invents."

**Fork C:** Genuinely good — the gas giant is "the best single object of all three forks"; the moon has a legible phase (the only moon of the three that bothers); the sky's blue-hour gradient with wind-drawn cirrus is moody and coherent; the image reads as "one picture, not a composite." Horrid — (1) the black rectangle "arch" is "the worst artifact of all three images" — hard-edged, with a faint dashed rectangular outline, torpedoing the scene; (2) nothing is ever in focus — the focal anchor is the same soft mush as everywhere else; fixations 40–239 read as "the same four reasons on loop" with no convergence to sharpness; (3) the 40 ventifact stones are invisible; (4) the breach/glacier is illegible; (5) the giant's limb is razor-sharp while its interior is uniformly blurred — "a soft sticker"; (6) the hash grain dominates everywhere and fights the "soft pigment" premise. Structural reading: "the most architecturally interesting of the three" — the fixation loop is a real perception-action loop (the 240-fixation log proves it ran), but the interest map is a greedy local optimizer over four dab variants that "converged to the global minimum of 'uniformly mushy dusk.'" The trace's vocabulary is richer than the renderer: "the mechanism dreams in higher resolution than it can paint."

**Critic 2's B-vs-C ranking: B leads — confirmed, but "narrower than the framing suggests, and for different reasons than the trace claims."** The table: B wins on craft and light coherence; C wins on world coherence (invented vs procedurally generated) and surprise capacity. Trace honesty: B FAILS (T12's crescent isn't in the render), C passes. "The honest summary: **B is the better image; C is the better mind.** B leads because the task includes craft and B's failures are local. But C's failure is a missing capability (mark-making vocabulary), while B's failure is a missing *behavior* (it never invents, only renders) — and behaviors are harder to bolt on than capabilities. If I had to bet on which architecture produces the stunning image at round 12, it would be C-with-hands, not B-with-knobs."

**Critic 2's decisive experiment — the Counterfactual World Test:** freeze both binaries' rendering code; change exactly one world-model input each — move the sun to the opposite side (B: negate the sun vector; C: change the D1/L1 sun commitment); then a structural change: delete the moon / add a terrain tier (B: remove moon sphere, alter heightfield masks; C: drop D11, add D15). Pass/fail: **B passes** iff both counterfactual renders show globally consistent consequences with zero hand-tuning — shadows flip across every surface, the moon's phase recomputes to a *measurably* visible crescent (>5% of disc pixels above sky luma on the lit side), no new stickers. **B fails** iff anything needs hand-patching (as T10–T12's photometric patches did) or the moon renders black again — "proving the world and the renderer are only coupled by the author's hand." **C passes** iff the arch renders as an arch (curved silhouette, legible opening, no rectangular edges — measurable boundary curvature) and ≥20 stones become individually legible with aligned dust tails. **C fails** iff 240 more fixations produce the same mush under the flipped sun. "Whichever fork passes its bar has demonstrated the mechanism, not the artifact — and that's the ceiling question."

### Critic 3 (fresh, independent)
Judged cold, normal vision, with pixel-level verification of the two load-bearing claims (B's moon, C's fixated rim). Method note: "judge the images, not the prose" — both traces overclaim relative to their artifacts.

**Fork B:** Genuinely good — the massif's strata banding on the right ridge faces is "the single best 'this is a world' passage in any of the three images"; rim-lit left slopes; the beautiful coherent sky; one continuous 3D surface with correctly dissolving distance haze. Horrid — (1) the moon is a pure black disc (interior max pixel **16/255** measured; no crescent, no planetshine) — "the artifact flatly contradicts the trace"; (2) the foreground is a "tar-blob" — T9/T11's corrections "didn't land"; (3) a summit fin reading as detached broken geometry; (4) a midground "cigar-rock" with a flat black bar for a shadow; (5) the floating orange lozenge at (~30–120, ~470–510) — the T2 "honesty anchor" sun disc — "reads as a hovering orange oval/UFO"; (6) half the image is near-black murk — "honest lighting, unwatchable composition." Structural reading: a genuine world-simulation renderer (SDF, per-pixel raymarch, marched shadows) — "architecturally the real thing, and the massif proves it." But: "when the light transport says 'this is black,' it's black" — no art direction, no fill strategy. And the celebrated feedback loop is, in this build, "narrative, not mechanism. The trace is a diary of intent; the binary is the verdict."

**Fork C:** Genuinely good — the small moon is "the most convincing single object in the image"; the dusk color field has watercolor charm; the giant's teal/gold palette is a nice color idea. Horrid — (1) the gas giant is "a smudged ball in a hard mask" — blurry smears inside a sharp circular boundary, the promised storm oval not visible; (2) "unmotivated orange bokeh-balls" floating in the sky, anchored to nothing; (3) chalk-smear cirrus with hard edges; (4) the "arch" is an illegible stamp — dark blurry rectangle, purple smudge, a vertical row of pale dashes reading as rivets — "total failure of the fork's emotional centerpiece"; (5) **the far rim is featureless murk — quantified: local contrast std 10.25, smoother than the sky (16.45)** — ~150 fixations produced zero crest, zero breach, zero strata: "the fixation reasons are fiction relative to the artifact"; (6) the focal anchor (430,400) is empty mauve blur; (7) global defocus + dirt grain. Structural reading: "C is B's mirror image: B computes light honestly but can't compose; C composes (in prose) but can't depict." The dab is a low-pass filter — every mark is a smoothing operation — so 240 "strata line" fixations produce zero strata. "The trace is the most imaginative artifact of the three; the image is the least."

**Critic 3's B-vs-C ranking: CONFIRM — B leads, by a wide margin, with one caveat.** B's load-bearing claim ("nothing placed, light derived") HOLDS on the massif and strata; C's ("fixations converge on legibility") FAILS — the most-fixated region is the smoothest, measured. B's worst defects are failures of fill/composition inside a sound architecture (fixable without changing it); C's are failures of the depiction primitive itself (needs a new mark-maker — "i.e., a different fork"). Caveat: "B's trace is not evidence — the artifact is. B leads on pixels, not on prose."

**Critic 3's decisive experiment — THE ARCH TEST.** Identical brief to both forks: "A wind-carved arch stands ~20 m from the camera, backlit by the low sun. The far landscape must be visible THROUGH its opening. Render it." This attacks each fork's load-bearing claim head-on: B must prove honesty can be readable (occlusion not paint, opening pixels match the far-field sightline, arch casts a sun-consistent shadow); C must prove attention can sharpen (≥4/5 blind viewers trace a continuous arch outline and describe structured content through the opening; mechanical edge bar: object/background gradient ratio ≥2.0 on the silhouette). "B must prove honesty can be readable; C must prove attention can sharpen. Whichever passes has the higher ceiling; if both fail, the program learns that neither current architecture clears the bar and the traces can't be trusted as progress metrics."

**Standing recommendation (Critic 3, for the program):** judge artifact-first, trace-second from here on — "any future 'feedback corrected X' claim should be verified by diffing the renders, not by reading the diary."

---

## 6. Blind ordinary-vision judges — "would you have guessed AI?"

Five independent judgments per image, random presentation order, neutral filenames (mapping withheld from judges).

Five independent judgments per image, random presentation order, neutral filenames (mapping: img1 = Fork C, img2 = Fork A, img3 = Fork B — withheld from judges).

| Image | YES (looks AI-made) | NO (reads as photo) | UNCERTAIN |
|---|---|---|---|
| img1 — Fork C | 4/5 | 0/5 | 1/5 |
| img2 — Fork A | 4/5 | 0/5 | 1/5 |
| img3 — Fork B | 4/5 | 0/5 | 1/5 |

No image scored a single NO — none reads as a real photograph. All three depict fantastical alien scenes with obvious digital-render artifacts. The three UNCERTAINs were honest hedges about the *kind* of synthetic (old-footage blur, hand-drawn-vs-AI style, thumbnail-passable stylization), not claims of photographic plausibility.

What the judges' one-liners caught unprompted: Fork C's arch-box ("square glyph-like artifact... garbled AI text-shapes half-melted into the ground"); Fork B's black-disc moon (two separate judges); Fork A's "flat-shaded purple mountains... cartoon planet with marble-print texture" and "cardboard cutout" rocks. The blind panel independently converged on each fork's located defects.

---

## 7. The B-vs-C ranking (all voices)

**Direction: unanimous. Margin: disputed. Ceiling: split.** Every voice ranks B ahead of C today; they disagree on how wide the lead is and on which architecture owns the higher ceiling.

### The four voices at a glance

| Voice | Ranking | Margin | Ceiling bet | Sharpest line |
|---|---|---|---|---|
| sol | B | **Wide** (on current image quality; "not necessarily permanent") | **B** — the world model can reconceive; C's primitive can't express its own decisions | "B has the better world model and picture; C has the more elaborate introspective control loop, but that loop currently lacks effective visual intervention." |
| Critic 1 (interim, completed B) | B | Clear | B, on invented-vs-assembled | B's black-disc moon is a red flag exactly where B claims its unique strength |
| Critic 2 (fresh, independent) | B | **Narrower than the framing** — "for different reasons than the trace claims" | **C-with-hands** — "B is the better image; **C is the better mind**." Would bet on C at round 12 | "B's failure is a missing *behavior* (it never invents, only renders) — behaviors are harder to bolt on than capabilities." |
| Critic 3 (fresh, independent) | B | **Wide, on pixels not prose** | B — C needs a new mark-maker, "i.e., a different fork" | "Judge artifact-first, trace-second. B's trace is a diary of intent; the binary is the verdict." |

Blind ordinary-vision judges (§6): no help on the ceiling question, and they were never asked it — 4/5 YES for all three images, zero NOs. Both load-bearing defects were caught unprompted by ordinary viewers: two judges on B's black-disc moon, one on C's arch-box.

### Where all four agree
- **B's moon is a black disc.** Four independent measurements (max pixel 14.6–32/255 across critics and sol's visual reading); the trace's "young crescent" is not in the render. The most reproduced fact in this document.
- **C's arch is a box.** Every voice names it the worst artifact of the three images — a hard rectangle, not an arch.
- **C's most-fixated region is the smoothest.** Measured 10.25 vs sky 16.45; ~150 "strata" fixations produced zero strata.
- **Both traces overclaim.** B's feedback diary and C's fixation reasons both assert corrections the pixels don't show. Critic 3's standing recommendation adopted: judge artifact-first from here on.

### Where they genuinely disagree
- **Is C "the better mind"?** Critic 2 says yes — C's world coherence and surprise capacity outrank B's, and a missing capability (hands) is easier to add than B's missing behavior (invention). sol refines it away: C's loop is more elaborate but *ineffective* — "the artifact does not demonstrate that it has a better mind," and "B may actually have the better underlying visual model, even though its trace overclaims." Critic 1 sides toward B on invented-vs-assembled grounds.
- **Which ceiling is higher?** sol: B (the world model survives a re-conception; the dab primitive caps C). Critic 2: C-with-hands (round-12 bet). Critic 3: B, because C's fix requires replacing the primitive — "a different fork." Score: **2–1 for B's ceiling, with one principled dissent.**

### The Critic 2 caveat, preserved verbatim
sol's refinement does not erase the caveat — it sharpens it: B is unambiguously the better image today, and its failures are local (fill, exposure, composition inside a sound architecture); C's failure is a missing capability at the depiction layer. The honest residual is Critic 2's: the task includes craft, so B leads; but the imagination question — which mechanism can invent what it has never rendered — is still live, because B has not yet been observed inventing, only rendering.

### Synthesized ranking
**B leads the race.** Four voices, one direction, and the two artifact-first readers (sol, Critic 3) both say the margin is wide. C stays alive exactly where the lead put it — potential, currently horrid — with one concrete lifeline: hands. Until C can express a hard edge, the ceiling debate is B's to lose. The dissent is recorded, not resolved: if a future C renders its arch as an arch, this ranking gets reopened.

---

## 8. Decisive B-vs-C experiments proposed

### Candidate E1 — the re-conception test (Critic 1)
Give each fork a world element that CONTRADICTS its current visual vocabulary and requires changing the conception, not the paint: "the ground the camera stands on is not ground — it's the back of a colossal dormant organism; show evidence of this in the foreground without changing the sky."
- **Kills C if:** the dab primitive cannot express the contradiction — the foreground becomes more elaborate blur, or starvation means the foreground still gets zero fixations, so the demanded evidence never appears. Pass: a viewer can point to foreground features implying the organism.
- **Kills B if:** the distance-field world model can't absorb a conceptual re-conception — the organism becomes noise-displaced spheres (another geology template) rather than something that reads as alive, or the trace shows depiction proceeding without re-conceiving. Pass: the trace records a genuine re-conception moment (like T10/T11) and the render shows organism-evidence the original world model didn't contain.

[More candidates pending sol + Critics 2–3 — both delivered.]

### Candidate E4 — the relight test (sol)
Identical brief to both forks: an alien canyon with a thin stone arch in the foreground, a crescent moon in the upper left, one visible cast shadow from the arch. Then rotate the sun 90° while preserving geometry and camera view. The load-bearing question: "whether the mechanism has a reusable scene model rather than merely producing a plausible first-pass arrangement."
- **B passes iff:** the arch keeps recognizable hard geometry; the cast shadow moves consistently with the new sun; the crescent stays a crescent with its lit side changing consistently; depth ordering survives. **B fails** if the moon becomes a black disk again or the foreground collapses.
- **C passes iff:** the arch is visibly an arch; geometry is preserved across the revision; the shadow moves the correct direction; the crescent and terrain update without being repainted into unrelated soft blobs. **C fails** if the relight is a global color wash or the arch cannot survive as hard geometry.
- Note: E4 and the Counterfactual World Test (Critic 2) are the same test family — freeze renderer, transform world, check global consistency. Two independent voices converged on the family; it is the strongest candidate for the single decisive run.

---

## 9. Honest limits of this document
- Blind-judge scores measure "reads as AI," not imagination — a fork can lose the judges and still be the more imagination-like mechanism (the lead's own ranking already diverges from naive photorealism).
- All three images are single frames from deterministic programs; ceilings are projected, not measured.
- Critic 2 and Critic 3 worked without seeing Critic 1's analysis; agreement between them is independent convergence, disagreement is flagged as such.
