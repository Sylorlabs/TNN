# RESULTS — Senses Phase 2, AUDIO track (2026-09-20)

Branch: `tnn-native-lab`.
Prereg: `PREREG_SENSES_PHASE2_AUDIO.md` (frozen pre-build, commit
`ed5f29bc7931`) + `AMENDMENT-01_seq_k.md` (dated 2026-09-20, committed
with the build inputs at `f53bdb9931af`).
Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
This file reports against the frozen prereg. The proposed qualbar
(`PROPOSED_QUALBAR_SENSES_2026-09-20.md`) is UNSIGNED — results are
"meets proposed bar §X", never QUALIFIED.

## Verdicts (audio only)

| Proposed § | Result |
|---|---|
| §A-audio ingress battery | **meets proposed bar: 16/16** exact refusal codes; record count and live-slot count unchanged after battery; refusals == 16 |
| §B-audio OBSERVE discipline | **meets proposed bar: 9/9** (8 exact refusals + audit scan == 1) |
| §C-audio kill/pin/recall | **meets proposed bar: 10/10** exact codes; recall read-only; freed slot reusable with clean provenance |
| §D-audio paired twins | **meets proposed bar: 24/24** pairs distinguishable after admit → OBSERVE → RECALL (bytes differ AND provenance-sha256 differ), distinction survives per-pair save/reload |
| §E-audio realistic envelopes | **meets proposed bar: 12/12** (8 × 16,000 B round trips byte-identical; 4 ordered 4-frame sequences order-exact) |

Supporting lines (all actual==expected, enforced by the runner):
`se2a-a-n-unchanged`, `se2a-a-live-unchanged`, `se2a-a-refusals`,
`se2a-b-admit`, `se2a-b-fill-live-16`, `se2a-c-setup`, `se2a-c-pin`,
`se2a-zz-fails-total`. Harness total: 79 CL_CHECK lines, 79/79 pass.

## Replay / build identity (K-SE1)

- Two independent `znc` compilations of the frozen sources → identical
  binary SHA256: `7e6ca60f447ebf16164d5dae082da565a2224a565b9906d1a63c6c080302ec76`
- Two full harness runs from clean state → byte-identical stdout
  (empty diff). Both binaries exit 0.
- K-SE7 fresh-process verify (binary B on run-B store): 9/9 lines pass —
  records, slots, audit byte-identical after reload; twin distinction
  (rec-0 vs rec-1) survives.

## Kill bars (all probed, none fired)

| Bar | Probe | Result |
|---|---|---|
| K-SE1 | double build + double run + diff | identical hash, empty diff — PASS |
| K-SE2 | 7 judgment/strength/region/cite/rec refusals; audit scan on full store | exact codes; scan == 1 — PASS |
| K-SE3 | 16-item malformed battery | exact codes; n and live-slot count unchanged — PASS |
| K-SE4 | mutate caller buffer after admission; re-recall | stored bytes unchanged — PASS |
| K-SE5 | static scan: strength literals only at all 9 `mi_observe` call sites; no observation-byte arithmetic feeds strength | clean — PASS |
| K-SE6 | static scan: RNG / wall-clock / threads / floats | clean — PASS |
| K-SE7 | fresh-process reload + per-pair save/reload inside §D | byte-identical — PASS |
| K-SE8 | kill pinned → -7206; kill CORE → -7207 | exact codes — PASS |

## What was built

- `se2a_ingress.zag` — phase-1 ingress + 2 declared deltas: `SE_MAX_PAYLOAD`
  4096 → 16384 (admits §E's 16,000 B frames; 32 × 16,464 B < 2^25), and
  new `SE_BAD_RESERVED` (-7110) refusing nonzero reserved header bytes.
  Diff vs phase-1 is exactly these deltas (verified).
- `se2a_memif.zag` — verbatim phase-1 contract (16 slots, codes
  -7201..-7210); diff vs phase-1 is only the `@import` rename.
- `se2a_main.zag` — audio battery driver (`harness` / `verify` modes).
- `substrate/` — vendored R33 native IO + SHA256-V2 + cl/common, hashes
  match phase-1 `SUBSTRATE_SHA256.txt` byte-for-byte.
- `run_phase2_audio.sh` — static gates, double build, double run, replay
  diff, mechanical CL_CHECK verification, cross-build verify.

## Honest findings (no bar lowered)

1. **AMENDMENT-01 (pre-build).** The frozen prereg's §7 pinned sequence
   pattern `k=100+q*4+r`, which overflows i32 in the §2 formula
   (7999 × 791,917 = 6.3×10⁹ > 2³¹−1). Amended pre-build to k=8+q*4+r
   (max 7999 × 182,154 = 1.46×10⁹ < 2³¹−1), disjoint from the k=0..7
   single frames. Formula, envelope, counts unchanged.
2. **Save contract is create-exclusive.** `nio_open_child(...,create=1)`
   uses O_CREAT|O_EXCL: re-saving records/memif into the same directory
   fails with SE_IO (-7109). Found empirically — the first full run had
   22/24 §D checks failing (sv1=-7109) because all pairs shared one save
   dir. Fix: per-pair directories `se2a_d00`..`se2a_d23` (prereg said
   `se2a_dstore`; the per-pair naming is a mechanical consequence, no
   check criterion changed). This also serves as the negative control:
   the checks demonstrably FAIL when the machinery fails (22 lines at
   actual=0 pre-fix) — they are live, not vacuous.
3. **Zag build note.** `let ph:[]u8=mi.*.phash;` (struct *value*) is
   rejected with "aggregate let needs an aggregate initializer"; the
   correct form for a value (not pointer) is `mi.phash`. Two occurrences
   fixed; no semantic impact.
4. **Defined mappings (prereg §3).** "bits≠16" → encoding id 3 →
   SE_BAD_ENCODING (-7103): TNNRAW02 carries no PCM bits field; bit depth
   is implied by the encoding id. "Truncated header (79 B)" →
   SE_BAD_MAGIC (-7101): magic unreadable. If a distinct bits field/code
   is wanted, that is a dated amendment, not a reinterpretation.
5. **No proposed-bar number was unreachable.** The 16,000 B envelope
   required raising ingress capacity (documented delta, committed
   pre-build in the prereg) — a build change to meet the bar, not a
   lowering of it.

## Scope boundaries (carried)

Audio track only; vision is a separate worker. Fixtures are
deterministically authored encoded files — no live device qualified.
No classifier admitted. Strength is caller-declared (K-SE5). The
quarantined r34 learner core was not touched. The word QUALIFIED is not
used: the bar is unsigned and independent verification is pending.
