# RESULTS — Senses Phase 2 (vision): RGB8 ingress envelope + OBSERVE contract at operating size

Date: 2026-09-20. Branch: `tnn-native-lab`.
Prereg: `PREREG_SENSES_PHASE2_VISION.md` (**frozen before build** — commit
`01977cfa92a6`; this file reports against it).
Measuring instrument: `../../PROPOSED_QUALBAR_SENSES_2026-09-20.md`
(**PROPOSED, UNSIGNED**). Nothing here is declared QUALIFIED; verdicts read
"meets proposed bar §X (vision)".

## Verdict: MEETS PROPOSED BAR §A–§E (VISION)

71/71 counted checks pass (16+9+10+24+12), all kill bars probed clean,
two-build hash identity, byte-identical reruns, static scans clean.

| Proposed § (vision) | Counted checks | Result |
|---|---|---|
| A — malformed/edge ingress battery | 16/16 | meets proposed bar |
| B — OBSERVE discipline (8 probes + audit scan) | 9/9 | meets proposed bar |
| C — kill / pin / recall semantics | 10/10 | meets proposed bar |
| D — paired twins, S1 discriminability | 24/24 | meets proposed bar |
| E — realistic envelopes | 12/12 | meets proposed bar |

107 total `CL_CHECK,se2v-*,actual,expected` lines emitted (71 counted +
36 setup/gate lines); every line actual == expected; all 107 names unique.

## What was built (pure Zag, native)

- `se_ingress.zag` — copied from phase 1, changed per prereg (changes
  marked `CHANGE-V2`): payload capacity 4096 → 12,288 B; record capacity
  32 → 64; RGB envelope 1..4 → 1..64 per axis; header gains
  channels(i32)@28 + bit-depth(i32)@32 with reserved[12]@36..48 still
  zero-required (RGB8: ch=3/bd=8; PCM: ch=1/bd=16); `se_build` sets
  channels/bit-depth from the encoding id.
- `se_memif.zag` — copied from phase 1 **unchanged** (contract, refusal
  codes -7201..-7210, 16-slot store, 256-entry audit).
- `se2v_main.zag` — new vision battery harness; `run_phase2_vision.sh` —
  new runner (static checks, two builds, two runs, replay diff, mechanical
  verification). No save/reload mode (proposed §I out of scope).
- Substrate vendored; hashes identical to phase 1 (`SUBSTRATE_SHA256.txt`).

## Kill-bar probes (bars did not fire)

| Bar | Probe | Result |
|---|---|---|
| K-SE1 | Two full harness runs, diffed | byte-identical stdout, empty diff |
| K-SE2 | 8 refusal probes + audit scan (§B) | exact codes; scan=1, zero silent admissions |
| K-SE3 | 16-item malformed battery (§A) | exact codes; refusals=16; record count and live-slot count unchanged |
| K-SE4 | Recall-buffer mutation (§C probe 8) | re-recall byte-identical to pristine record |
| K-SE5 | Static scan: no strength from observation bytes (memif + harness) | clean |
| K-SE6 | Static scan: RNG / wall-clock / threads / floats | clean |
| K-SE7 | Not exercised — no save mode in this harness (out of scope per prereg) | n/a |
| K-SE8 | kill pinned → -7206; kill CORE → -7207; no-evidence → -7210; legit kill ok; re-kill → -7208 (§C) | exact codes |

## Build determinism

Two independent znc compilations → identical binary SHA256
`90b49b4b4ac2449a01e45efbf5e49128b14582a1182a7ebd91e8673f1ebc2610`.
Harness logs: `logs/run_harness_a.txt`, `logs/run_harness_b.txt`;
`logs/replay_diff.txt` is empty. Both runs rc=0.

## Notes / honest boundaries

- Build emits benign A0102 warnings (discarded `se_build` return values in
  §C/§D fixture authoring); validity is transitively enforced because every
  admit re-validates and the checks require sequential admit ids.
- Trial-run bug caught pre-officially: the `plen-neq-wh3` fixture read one
  byte past the 12-byte pristine payload (slice OOB panic); fixed by
  authoring the 13th payload byte as a literal. The official battery never
  saw the bug.
- Twin pairs 2 (`px-permute`) and 11 (`px-chan-rotate`) carry identical byte
  histograms by construction — the histogram-confound probes the bar asks for.
- Pair 7 (`wh-transposed`) transposes the pixel layout so payload bytes (and
  hence provenance sha256) differ; a header-only transpose would have failed
  its own provenance check by design.
- Strengths are caller-declared literals/index expressions throughout
  (e.g. `1+k`, `20+f`, `11..34`); no observation-byte arithmetic anywhere in
  the admit or harness path.
- PCM validation path carried over unchanged and untested here (audio
  worker's scope). No live camera, no S2 perception, no classifier, no
  performance claims. Proposed §F–§I (full replay/build, static at bar
  level, churn, save/reload) are outside this worker's assignment.

## Files

- `PREREG_SENSES_PHASE2_VISION.md` (frozen pre-build)
- `se_ingress.zag`, `se_memif.zag`, `se2v_main.zag`
- `run_phase2_vision.sh`, `SUBSTRATE_SHA256.txt`, `substrate/`
- `logs/` (build hashes, harness runs A/B, empty replay diff)
- This file.

Excluded from commit (house convention): `se2v_bin_a`, `se2v_bin_b`,
`.zag-cache/`, `.zagd.semantic-ready`.
