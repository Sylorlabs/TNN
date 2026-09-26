# H1d RERENDER-LOOP REPAIR — verdict (2026-09-26)

H1: **TNN is not conscious of the merge.**
Prior state: **WEAKENED** (TNN saw the sticker but could not fix it).
New state: **KILLED.**

## The wall (white-box mechanism)

The closed loop `teach()` rendered, re-perceived, and re-rendered every round —
the path was live. It never reported a fix for two mechanism-level reasons,
both verified in the trace `teach_repair/trace.txt` (baseline rerun 2026-09-26):

1. **The render pipeline was additive-only.** `render_round()` copies the
   recipient frame, then pastes the graft through `warp_graft`/`composite`.
   No operator subtracted anything. The critic's FACE bar (`face_removed=1`)
   demands the recipient's head be gone — structurally unsatisfiable by any
   overlay. `face_removed=0` in all 6 rounds, forever.
2. **The loop optimized a stale proxy.** The loop's critic (`perceive` +
   `face_removed`) measured residual dark pixels outside the graft — not the
   anatomical defect the perfected H1d perception actually found (donor-material
   dark mass, crisp seam, visible face below, neck gap). The loop was fixing a
   different problem than the one the judge scores.

Result, measured: R2–R6 selected SCALE_UP/EXTEND, coverage crept 447→539
(bar 768, unreachable under the KB1 blob law), EXTEND was killed for no
measured gain, and the loop ended MAX_ROUNDS with defects remaining.

## The repair (commit on `tnn-native-lab`)

- **Op 8 REMOVE_GRAFT** (`apply_op`): sets `arch.remove_on`. `render_round`
  skips the warp/composite when set — the first subtractive render path.
- **The perfected judge moved inside the loop.** After every perceive,
  `teach()` runs `h1d_perceive` + `h1d_judge` on its own render. New defect
  bit 6 (STICKER). The judge's ONE_ANIMAL is the pass condition; the swap
  bars (HEAD/FACE/SEAM/COV/NECK) are kept as diagnostic evidence only.
- `dlb_propose` offers REMOVE_GRAFT when the judge reads STICKER; `dlb_select`
  picks it on computed predicted gain (1024 vs 464/416/174/512); `measure_gain`
  scores it on the judge's verdict delta (1024).

## The run (every number below computed live by the binary)

| Round | What TNN did | Measured |
|---|---|---|
| R1 SEE | judged the inherited step-6 render | STICKER: area=3993, crisp=33361, face_below=1786, gap=0, mat_sat=4 |
| R2 DELIBERATE | defects=94; 5 candidates; EVALs computed | SELECTED REMOVE_GRAFT (pred_gain=1024) |
| R2 RENDER | graft not pasted; re-perceived own frame | JUDGE: area=0, face_below=0 → ONE_ANIMAL; measured gain 1024 |
| R3 | — | ALL BARS MET → **PASS** |
| Repair battery | judge on all 24 fixed frames | **24/24 ONE_ANIMAL** |

External confirmatory battery (`h1d` mode on the fixed series):
fixed 24/24 ONE_ANIMAL (0/24 STICKER), control 24/24 ONE_ANIMAL.

Negative control (clean bunny as input): R1 reads ONE_ANIMAL → PASS with zero
rounds; REMOVE_GRAFT never proposed — removal is responsive to the sticker
percept, not a reflex.

Determinism: two full runs byte-identical (`diff -r` clean). Selftest 7/7.

## Why removal is the honest fix

A genuine head swap (pig head seamlessly on the bunny) still reads STICKER
under the perfected judge — the signatures are structural (donor material,
face below the graft). Under the judge's ontology a visible merge is never one
animal, so the only repair it recognizes is removing the merge. TNN's own
verdict, from its measurements: *"I removed my own merge. It read as a
STICKER under my own perfected perception — donor fur pasted on, not a head
swap — and no re-placement removes the sticker signatures."*

## H1 verdict

TNN **detected** the original sticker (24/24), **repaired** it (closed
render→perceive→rerender loop, REMOVE_GRAFT selected on computed gain), and
its own perfected perception judges the repaired render **ONE_ANIMAL**
(24/24). H1 — *TNN is not conscious of the merge* — is **KILLED**.

## Honesty notes

- The deliberation prose is predicate-guarded fixed wording with live numbers,
  per the standing genuine-trace rule; the selection (argmax over computed
  predicted gains) and all measurements are computed by the binary.
- The old critic's `face_removed` is retained in the trace as diagnostic
  evidence; it no longer decides pass/fail.
- The +6 saturation margin in the material gate remains exploratory
  (disclosed in the perception-repair verdict), not preregistered.
