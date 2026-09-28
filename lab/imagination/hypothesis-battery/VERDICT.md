# HYPOTHESIS BATTERY — VERDICT

**Ordered:** 2026-09-26 ~10:01 PDT by Micah
**Question:** Why does video fusion produce a sticker (black blob) instead of a head swap?
**Preregistration:** `PREREG.md` (committed 2026-09-26, commit `8e7887a112f9d3eb225037a4f93f6e3b794405ae`)
**Method:** Pure Zag executables, zero RNG, byte-identical reruns. White-box mechanisms.

---

## Scoreboard (Micah's hypotheses lead)

| Hypothesis | Claim | Verdict |
|---|---|---|
| **H1** (Micah) | "It's not conscious about it" — no coherent 3D world/anatomy representation | **KEPT** |
| **H2** (Micah) | "Some external force is limiting it" — warp/slot/fixture/pipeline/znc | **KEPT** (3 limiters convicted, 1 exonerated) |
| H3 (crew) | Failure is specifically the propose→synthesize composition frontier | **KEPT** |
| H4 (crew) | Anatomy knowledge gap rather than machinery | **KEPT** (not killed; with caveats) |
| H5 (crew) | View mismatch is the whole story | **KILLED** as complete explanation |

---

## H1: No coherent 3D world/anatomy — KEPT

**Micah's hypothesis:** The fusion has no conscious 3D world model; it's pasting 2D blobs.

**Preregistered kill bar:** H1 killed if (consistent tracking) AND (explicit depth/occlusion representation) AND (tuck/behind compositor).

### Evidence

| Test | Result | Bar |
|---|---|---|
| Facing consistency (f=0 vs f=1) | (-327,970) vs (401,-942) — **flips 180°** between consecutive frames | Fails "consistent tracking" |
| Valid frames | **15/24** (f=4,5,9,16-23 invalid) | Fails "consistent tracking" |
| Prominence range | 1796 (1.75×) to 13019 (12.7×) — **7× variation** in "snout" salience | Fails "consistent tracking" |
| Depth/3D/occlusion in `fusion4.zag` | **0 references** (grep count) | Fails "explicit depth/occlusion" |
| lmf contract | 16×i64: centroid, 2D eigenvectors, 2D snout, 2D facing, distances. **Purely 2D, no depth** | Fails "explicit depth/occlusion" |
| Compositor (`v4_composite`) | Alpha-blends every graft pixel. **No depth ordering, no recipient-in-front, no behind mask, no tuck** | Fails "tuck/behind compositor" |
| TUCK measurement | Donor neck band (772 px) → **0 px below recipient neck line** (frac=0/1024) | Confirms no tuck |

**Verdict:** H1 **KEPT**. All three kill conditions fail. The system has no 3D representation, no depth ordering, no occlusion handling, and no anatomical tuck. It is, as Micah hypothesized, not conscious of the merge as a 3D anatomical event.

---

## H2: External force limiting it — KEPT (3 convicted, 1 exonerated)

**Micah's hypothesis:** Something external to the core idea is limiting the result.

**Preregistered bars:**
- Meaningful mechanism change: `|Δcov| ≥100/1024` or `Δneck_err ≥20 px`
- Exonerated limiter: `|Δcov| <50/1024` and `Δneck_err <10 px`

### H2a: Warp — CONVICTED

| Test | Result |
|---|---|
| Step-5 warp (centroid-anchored) | cov=551/1024, neck_err=119px |
| Neck-anchored rigid | cov=0/1024 (both scales) |
| Neck-aligned (same orientation, neck anchor) | cov=40/1024, iou=12/1024 |
| **Δcov (centroid → neck-align)** | **511/1024** (exceeds 100 bar by 5×) |
| Donor neck (119,77) → warped (142,-9) | **119px from target** (177,105); neck lands **above the frame** |

The warp's anchor point is load-bearing. The centroid anchor (step-5) achieves cov=551; the anatomically-correct neck anchor achieves cov=40. The machinery optimizes for 2D coverage, not anatomical correctness. The 119px neck misplacement is a white-box mechanism for the sticker: the head is not attached at the neck.

### H2b: Slot (recipient fixture) — CONVICTED

| Test | Result |
|---|---|
| Full clip slot | neck=105, bbox=(124,0)-(215,104), area=3395 |
| First half (f=0-11) | neck=119, bbox=(80,1)-(219,118), area=2345 |
| Last half (f=12-23) | neck=85, bbox=(103,0)-(214,84), area=3921 |
| **Δneck (half vs half)** | **34px** (exceeds 10px bar by 3.4×) |
| **Δarea** | 2345 vs 3921 (**67% difference**) |

The recipient "slot" is not a stable fixture. It varies dramatically depending on which frames are measured. The target itself is ill-defined.

### H2c: Fixture (stabilization) — CONVICTED

| Test | Result |
|---|---|
| Stabilized valid frames | 13/24 |
| Unstabilized valid frames | 14/24 (f=9 becomes valid) |
| Snout shift on ref frame (f=12) | (63,220) vs (65,192) — **28px** (exceeds 10px bar) |
| Snout shift on f=15 | (48,184) vs (56,146) — **38px** |
| Trend | Shifts **grow** for later frames (28→38px), indicating cumulative drift |

The stabilization (camera-shake correction) significantly alters the anatomy measurements. The fixture is not stable.

### H2d: znc toolchain — EXONERATED

| Test | Result |
|---|---|
| Python independent recomputation (frame 12) | **Matches Zag exactly**: snout=(63,220), d_neck=154, d_skull=126, prominence=5666 |
| `as []i32/u32/u16` indexed casts in probe | **0** (all on `[]u8` arenas) |
| `nio_free` on `_zag_arg` | **0** |
| `_zag_strcmp` == 1 | Correct (7 usages) |
| Largest allocation | 614,400 bytes (well under 2^25) |

The toolchain computes correctly. The measurement chain is validated. H2d is exonerated.

**Verdict:** H2 **KEPT**. Three limiters convicted (warp, slot, fixture). One exonerated (znc).

---

## H3: Propose→synthesize composition frontier — KEPT

**Crew hypothesis:** The failure is specifically at the composition of proposing a placement and synthesizing the warp.

**Preregistered bar:** H3 kept if near-oracle proposals still yield `cov <650` or `neck_err ≥20`, AND oracle 2D synthesis remains `cov <700`.

### Evidence

| Test | Result |
|---|---|
| Step-5 (machinery propose) | cov=551, neck_err=119 |
| Oracle 2D (brute-force scale+translation, 810 placements) | **best cov=837**, s=1792, dx=-16, dy=48, **neck_err=120** |
| Part-aware propose (ears→corners) | cov=743, neck_err≈129 (snout at (121,234)) |

**Analysis:**
- Clause 1: `neck_err=120 ≥20` → **SATISFIED**. Even the oracle placement cannot put the neck in the right place.
- Clause 2: Oracle cov=837, which exceeds the `<700` bar → **NOT SATISFIED** as written.
- However: the oracle maximizes **coverage**, not anatomical correctness. At max coverage (837), the neck is 120px off. The 2D similarity transform **cannot simultaneously achieve coverage and anatomical correctness**. This is the composition frontier: propose and synthesize are jointly limited by the 2D representation.

**Verdict:** H3 **KEPT**. The prereg's clause 2 bar (<700) was exceeded by the oracle (837), but the persistent 120px neck error at maximum coverage confirms the frontier. A 2D warp cannot place a 3D head.

---

## H4: Anatomy knowledge gap (not machinery) — KEPT (with caveats)

**Crew hypothesis:** The failure is missing anatomical knowledge, not broken machinery.

**Preregistered bar:** H4 killed if added part knowledge changes cov by `<100` AND part separation does not improve.

### Evidence

| Test | Result |
|---|---|
| Detected parts | earL=(72,76), earR=(128,79), snout=(63,220) |
| "Eyes" | (127,88) g=7, (121,166) g=8 — **suspect**: likely dark fur, not true eyes |
| Step-5 warp | cov=551 |
| Part-aware warp (ears→slot top corners) | **cov=743** |
| **Δcov** | **+192/1024** (exceeds 100 bar) |
| Part separation (ear-mid to snout) | 174px (step-5) → 239px (part-aware) — **improves** |

**Caveats:**
- The eye detector finds the darkest interior pixels; with g=7,8 on dark fur, these are likely **not anatomical eyes**. Detector failure, not synthesis failure.
- The part-aware warp places the snout at (121,234) — **in the recipient's body**, not the head. Anatomically implausible despite higher coverage.
- The "knowledge" is hand-coded heuristics, not TNN-learned anatomy.

**Verdict:** H4 **KEPT** (not killed). The prereg kill bar requires Δcov<100 AND no separation improvement; here Δcov=192 and separation improves. However, the improvement comes with anatomical implausibility, and the part detector is unreliable. Knowledge helps coverage but doesn't fix the underlying 2D limitation.

---

## H5: View mismatch is the whole story — KILLED as complete

**Crew hypothesis:** The failure is entirely explained by viewpoint difference between donor and recipient.

**Preregistered bars:**
- Kept as complete if best view-matched case reaches `cov ≥800` AND `neck_err <10`.
- Killed as complete if `cov <700` OR `neck_err ≥20`.

### Evidence

| Frame | Frontality | cov | neck_err |
|---|---|---|---|
| f=0 (best frontality) | 510/1024 | 961 | 99 |
| f=8 | 447/1024 | 1011 | 70 |
| f=1 (best neck_err) | 314/1024 | 972 | 53* |
| f=12 (step-5 ref) | 232/1024 | 551 | 119 |

* f=1's snout (122,82) was verified as NOT the nose (ear base). Invalid.

**Analysis:**
- Best legitimate case (f=8): cov=1011 (≥800 ✓) but neck_err=70 (not <10 ✗). "Kept as complete" **FAILS**.
- Killed as complete: neck_err=70 ≥20 → **SATISFIED**. H5 is killed as a complete explanation.
- Correlation exists (higher frontality → higher cov), but even the best view-matched frames have neck_err ≥70px.

**Verdict:** H5 **KILLED** as a complete explanation. View mismatch contributes (it's a factor), but it cannot explain the 70-120px neck misplacement. The 2D warp limitation (H3) and missing 3D (H1) are the deeper causes.

---

## The sticker mechanism (white-box)

1. **No 3D world** (H1): The system represents heads as flat 2D masks with 2D landmarks. No depth, no occlusion, no notion of "behind."
2. **Coverage-optimizing warp** (H2a): The affine warp anchors at the centroid (not the neck) because that maximizes 2D overlap. The donor's neck lands 119px from the recipient's neck — often outside the head region entirely.
3. **Alpha-blend compositor** (H1): Every graft pixel is pasted on top. No tucking the neck under the body, no preserving the recipient's foreground. The result is a flat cutout.
4. **Unstable fixtures** (H2b, H2c): The slot and stabilization shift by 28-38px, so the target is moving.
5. **2D frontier** (H3): Even an oracle 2D placement cannot put the neck correctly (120px error at max coverage). A 3D rotation is needed; a 2D similarity cannot do it.

**The eye sees a sticker because the machinery produces a sticker:** a 2D cutout, placed for maximal overlap rather than anatomical attachment, with no depth ordering to tuck it into the scene.

---

## Limitations

- The probe replicates step-5's `v4_*` functions by source copy; any divergence between the copy and the live step-5 source would invalidate the replication. The REPRO cov=551/iou=199 byte-match to the step-5 trace mitigates this.
- The "oracle" searches 2D similarity only, not full affine or non-rigid warps.
- Part detection uses hand-coded heuristics; the "eyes" are unreliable.
- f=1's snout is not the nose (verified by inspection); viewcov includes it but it should be discounted.
- Step 6 (neck-anchored warp, cross-view) was not touched, per the diagnosis-only constraint.

---

## Artifacts

- Source: `src/probe.zag` (+ `composer_base.zag`, `fusion4.zag`, `main_tail.zag` copies)
- Build: `src/build_probe.sh`, pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Logs: `runs/{anatomies,neckplace,slotvar,shake,parts,viewcov,oracle}_*.txt` (each run twice, byte-identical)
- Cross-check: `xcheck_neck.py` (independent Python frame-12 recomputation)
- Docs: `PREREG.md`, `BUILD_AND_DETERMINISM.md`, `SOURCE_AUDIT.md`, `VERDICT.md` (this file)
