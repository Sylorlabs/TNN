# DRAFT — Amendment proposal: scale-rot battery v2 (z.ai skeptic review)

**Status: AWAITING MICAH'S SIGNATURE — NOT ADOPTED. Nothing below has been run.**

**Source:** independent skeptic review of the scale-rot battery (`~/workspace/zai_relay/INBOX/scalerot-q1.answer.txt`, read in full 2026-09-27). Its verdict, up front: "as preregged, this battery mostly tests your harness, not your mechanisms."

**What the review got right (and this battery has now confirmed in part):**
- Replication legs test problem-count/throughput scale only. They miss KB growth, distinct-item interference, and per-item complexity.
- A deterministic system has no noise — every flip is a defect; the 5% K4 tolerance is one-sided (it is kept below as an accuracy-drop bar, but the flip bar stays absolute).
- The battery caught a REAL cross-item leak anyway (WO-SR-3: the `keya` arena), so replication is not worthless — but it is insufficient. Reclassify replication legs as throughput legs; add the legs below as the cognitive-scale legs.

**Proposed:** amend `docs/lab/scale_rot/PREREG.md` with the legs below. All are label-free (the review's key unlock: for a deterministic engine, "output must not change when irrelevant things change" needs no labels). Zero RNG anywhere. Each leg states its forbidden variable, its oracle, and its kill bar.

## Proposed new legs

| # | Leg | Mechanism(s) | Forbidden variable attacked | Oracle (label-free) |
|---|---|---|---|---|
| A1 | Order permutation | M1, M2 | position/order in batch | same item set in a FIXED permuted order (documented permutation table, no RNG) → per-item verdicts identical to canonical order |
| A2 | Dual arrangement | M1, M2 | position within copy clusters | block (copies adjacent) vs round-robin arrangement → identical per-item verdicts |
| A3 | Prefix consistency | M1, M2 | later items affecting earlier ones | run prefixes at several lengths (e.g. 10/30/100%); every earlier item's verdict identical as later items are appended |
| A4 | Perturbed copies | M1, M2 | content-hash memoization | each replica gets a unique NEUTRAL token (session string / renamed bystander, meaning-preserving) → verdicts must still match the unperturbed twin; distinguishes true invariance from cache replay |
| A5 | Decoy bids (M1) / decoy turns (M2) | M1, M2 | candidate-count scale | append dominated or fact-contradicted bids to each item (candidate count ×10) → winning verdict unchanged |
| A6 | Distractor KB | M2 | KB breadth and near-miss density | grow KB 10x/100x with template-generated facts including near-miss distractors about the same entities → per-probe verdicts unchanged; KB size and distractor density are SEPARATE sub-legs |
| A7 | Dialogue padding/stitching | M2 | dialogue length / multi-problem sessions | pad items with plausibly-irrelevant turns; stitch two frozen problems into one session with a constructed expected answer → per-turn verdicts unchanged |
| A8 | Chunker canaries | M3 | prefix growth moving boundaries | embed marker tokens at known offsets in growing prefixes → chunk-boundary positions relative to markers invariant; chunk-count/coverage linearity checked (does the chunker dedupe identical chunks?) |
| A9 | Fork-width sweep | M1 | fork count / merge order | force fork counts 1/4/16 on identical items → verdicts identical |
| A10 | Load determinism | M1, M2 | scheduling races | rerun legs under CPU/memory contention → byte-identical stdout |
| A11 | Wall-time / memory scaling bars | all | superlinear scaling | runtime ≤ linear with a preregged constant (10x leg ≤ ~1.5× the 1x wall time); peak memory ≤ linear; output line-count completeness checked |
| A12 | Planted-rot validation (mandatory) | battery itself | battery blindness | plant KNOWN rots — `budget = global/N`, an unstable tie-break comparator, fixed-K top-k over a growing KB — and verify the battery (old + new legs) catches each; a battery that cannot catch a planted rot cannot certify the absence of real rot |

## Proposed bar changes

1. **Purity contract (stated explicitly):** verdicts are a pure function of (item content, KB), invariant to batch composition, order, position, and scale. Every leg attacks one forbidden variable.
2. **K2 stays absolute** (any flip = FAIL). **K4 stays** (≤5 pp accuracy drop) but the report must state the accuracy CI honestly: 44 items ≈ ±15 pp at 95% — the replication legs add zero accuracy information; they certify invariance, not quality.
3. **Flip matching defined strictly:** match on full item-scoped IDs; assert the winner ∈ that item's own bid set; report clustering (copy-clustered flips ⇒ content-level coupling).
4. **Determinism scope extended:** hash stdout AND stderr, exit codes, and written artifacts; prereg the environment scope the byte-identity is claimed under.
5. **Tie-breaking:** mandate content-pure tie-breaking (pure function of content, e.g. lexicographic minimum bid ID); position-dependent tie-breaks are defects, not tolerance.
6. **Per-mechanism scale axes preregged:** each mechanism declares which scale axes it claims to survive (problem count, KB breadth, dialogue length, fork width, input bytes) — legs test claimed axes only.

## Out of scope for this amendment

Fixing WO-SR-3 (owning line). M4 until its dependency lands. Anything requiring new labeled items.

## Sign-off

- [ ] Micah signs → amendment adopted, legs scheduled.
- [ ] Micah declines → battery stays at v1 (replication legs only, reclassified as throughput legs in the next report).

*Drafted 2026-09-27 by the scale-rot 100x coordinator. Not enacted.*
