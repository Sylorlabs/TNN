# Authority law — universal T1–T3 gate + video/image instantiations

Micah APPROVED option B, 2026-09-24: **universal principle, per-path instantiation.**

## The universal law

Output feedback earns authority on a path only if ALL three hold:

- **T1:** the fault is detectable against a *plan-derived* expectation (never against the output's own statistics);
- **T2:** the correction map is *plan-pure* — constant in the measured output (Lipschitz-0, one-step, idempotent), so false positives are no-ops;
- **T3:** the output is *epistemically safe to re-ingest* — measuring it cannot install content the plan didn't author.

**Universal justification burden:** any path wanting output→plan contact must name, in writing, the information gap the output fills that the plan cannot compute.

**(D) vs (G):** deliberation-layer *reading* of output as evidence (allowed, acts only on the plan) vs *generative* feedback where rendered bytes condition the next unit (banned everywhere).

## File map

| File | What |
|---|---|
| `gate/gate.zag` | The universal gate module: law text, T2 proof protocol, `gate_register()` which REFUSES correction maps that read measured output, output-derived global gains, continuous servos, missing T2 certificates, unjustified latches, empty (G)-bans, unnamed information gaps. Plus `gate_sha_hex`. |
| `video/video.zag` | Video instantiation: two-piece rule (PAR frame path + stateless per-frame exception detect-and-reassert; piece 3 structurally absent). Renderer `frame = F(plan, f)`, zero cross-frame state. Detector: per-tile (sum,xor) vs scene-model recomputation, confirmed by full re-render + bit-exact diff. Includes T2 harness (8 distinct corruptions), VF-1–VF-4 fault battery, false-positive battery, 3× reruns, gate registration + 3 negative refusal tests. |
| `image/image.zag` | Image instantiation: pieces 1+2, piece 3 audited empty. Miniature of the three native paths (Path C pure field, Path A stroke log + eager application, Path B ordered layer program with `img_blend`). Region = 128×128 tile; detection = region re-render + bit-exact diff; correction = full layer/stroke replay from the plan (never forward-correct, never neighbor-match). Includes the five-point `d_blend`/`f3_blend` classification in the doc header, T2 harness (6 corruptions), F1/F2 battery, 3× reruns, gate registration + 3 negative refusal tests. |
| `R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag` | Vendored substrate copies (imports resolve relative to the importing file; these must sit next to the build root). |
| `EVIDENCE.md` | Verification numbers and SHA-256 digests from the runs. |

## Build & run (pure Zag, deterministic, zero RNG)

Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Build from this directory (imports resolve relative to the importing file):

```
cd ~/workspace/tnn-lab/bytegen/authority_law
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 video/video.zag -o /tmp/vid --run
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 image/image.zag -o /tmp/img --run
```

Each binary prints its T2 harness result, fault-battery result, rerun SHAs, gate registration verdict, and negative-test refusals, ending in `OVERALL PASS`.

## Video piece-3 rule (frozen wording, for future work)

No output-conditioned scene-event mechanism is built. A future proposal must clear all three gates:

1. **Plan-incomputability proof** — the measured value cannot be derived from the plan without the rendered bytes (name the hidden state or extra-buffer measurement; "inconvenient" fails).
2. **Battery demonstration** — preregistered, Micah-signed: a scene the plan-only path provably cannot author and the latch provably can.
3. **Non-interference proof** — the latch preserves piece 2's healing guarantee (corrupted frame still heals by single-frame re-render; committed values re-derivable plan-pure).

## Image piece-3 slot

Audited empty: no discrete measured-plan-fact exists in the image line. Filling it requires a frozen prereg amendment with a demonstrated discrete measured-plan-fact, signed by Micah.

## Hard boundaries honored

- The four production emitters (`f3_emit_wav`, `f3_emit_wav_hifi`, `f3_emit_avi`, `f3_emit_avi_g`) are **not touched**: they are "grandfathered post-pass mastering, flagged for plan-derivation review — they are not generation authority and not precedent" (image team's frozen wording). A separate gamma-disease repair crew owns them. Zero duplication.
- No frozen battery prereg was run. The fault batteries above are smoke/verification runs built into the drivers; the four preregistered fault batteries need Micah's signature first (sibling crew drafting).
- No binaries or `.zagd` cache files are committed.

## Spec gaps

None blocked implementation. Every sentence of the video and image authority recommendations was implementable as written:
- Video's "per-frame tile statistics from the scene model" is implemented as tile (sum,xor) recomputed from the plan every run (never frozen literals), with full re-render + bit-exact diff as confirmation.
- Image's "region checksum vs plan-derived expectation" alternative was not needed: the stronger option (re-render region to scratch + bit-exact diff) is implemented, which the recommendation calls "strictly stronger than audio's band predicate."
- One honest-limits note carried over from FAULT_ANALYSIS: the demonstration fault classes are artifact-level (VF-1–VF-4 / F1–F2). VF-6-class plan corruption (wrong plan authored) is undetectable by any output measurement by construction — the exception path heals artifact faults only, never plan faults.
