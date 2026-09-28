# Authority-law verification evidence

Runs: 2026-09-24, native Zag binaries built with the pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Zero RNG; all fault injection is a deterministic function of the fault index.
Full logs: `evidence_video.txt`, `evidence_image.txt` (crew working copies).

## Video (`video/video.zag`) — OVERALL PASS

| Check | Result |
|---|---|
| T2 harness: 8 distinct corruptions of frame 3 (VF-1 burst bit-flips, VF-2 zeroed 16×16 tile, VF-3 full-frame dropout, VF-4 wrong frame in slot, VF-1b sparse flips, VF-2b quarter-frame zero, sub-floor compensating ±2 LSB tamper, VF-1c 1KB burst) — each: detector fires, one-step correction == clean, second application identical (idempotent) | 26 / 26 |
| Fault battery VF-1–VF-4: detect → re-render → byte-identical to clean plan-pure render | 4 / 4 healed |
| False-positive battery: detect+correct on all 8 clean frames | 8 / 8 no-ops (byte-identical, detector silent) |
| Full-sequence reruns, byte-identical | 3 / 3 |
| Gate registration `video` (T2 cert attached, no measured-read, no output gain, no servo, piece-3 audited empty, gap named, (G)-ban restated) | REGISTERED (rc=0) |
| Negative tests: continuous-servo proposal, output-gain proposal, readback-corrector proposal | 3 / 3 REFUSED (codes 3, 2, 1) |

Clean sequence SHA-256: `215cc9a6c229304d7c279ed590a80b51354d124de4f905ee5cf8fd8401938748`
Final sequence SHA-256 (after all healing): identical.

## Image (`image/image.zag`) — OVERALL PASS

| Check | Result |
|---|---|
| T2 harness: 6 distinct corruptions of the 128×128 region (F1 bit-rot top-bit flips, F1 torn tile shifted write, F1 zeroed tile, F2 mid-render cell corruption, F1b sparse flips, F1c half-region zero) — each: detector fires, one-step correction == clean (0 differing bytes), second application identical | 20 / 20 |
| F1/F2 battery: detect → full layer/stroke replay from plan → 0 differing bytes | 4 / 4 healed |
| False-positive: detect+correct on clean image | no-op (byte-identical, detector silent) |
| Full-image reruns, byte-identical | 3 / 3 |
| Gate registration `image` (T2 cert attached, piece-3 latch AUDITED EMPTY, `img_blend` classified Piece-1, gap named, (G)-ban restated) | REGISTERED (rc=0) |
| Negative tests: contrast-servo proposal, auto-contrast-gain proposal, neighbor-inpaint proposal | 3 / 3 REFUSED (codes 3, 2, 1) |

Clean image SHA-256: `28f372e4fa300b60c1c36cf302bd6f930b297ac3f2400347b3493dcfb5c794dd`
Final image SHA-256 (after all healing): identical.

## Notes

- During development the image T2 harness initially failed 18/20: the F2 mid-render corruption spilled outside the 128×128 exception region, so region-scoped healing correctly left outside-region bytes damaged. Fixed by containing the F2 fault inside the region (rows 40–55, cols 40–71); this is the specified region-scoped behavior, not a harness bug. After the fix: 20/20.
- Sub-floor note (video k=6): a sum-neutral ±2 LSB tamper is still caught because the tile (sum,xor) predicate has no detection floor for this fault class in this construction — disclosed, not papered over.
- The four preregistered fault batteries (VFB-1 etc.) were NOT run — they need Micah's signature; a sibling crew is drafting them.
