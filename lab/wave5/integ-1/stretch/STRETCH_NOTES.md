# integ-1 stretch leg — mechanical scaling record (2026-09-20)

**Authority:** `PREREG_INTEG1.md` §3, "Stretch leg (conditional)": E=4800
(80 segments of 60), same ladder fractions ×10. Runs ONLY if the base leg
is green on every check and wall-clock allows. Base leg (2026-09-20):
137/137 INTEG_CHECK, INTEG_FAILURES,0, byte-identical reruns — green.
Wall-clock of base leg: seconds. Both conditions satisfied.

**Preregistered expectations:** identical signature-level results;
disconnect still at e=11; corruption phases 10× longer.

**What this file records:** `stretch/integ_stretch.zag` is `integ.zag`
with ONLY the mechanical ×10 scalings below plus a 2-line import-path
depth fix (`../../wave4/` → `../../../wave4/`, lines 23–24: the stretch
source lives one directory deeper, so the relative `@import` paths need
one more `../`; the imported files are byte-identical, Gate 1
hash-verifies them). No decision rule, no gate, no signature, no
threshold, no learner code, and no falsification criterion was changed.
Verified: `diff integ.zag stretch/integ_stretch.zag` shows exactly 58
changed lines, all listed here.

## Scale mapping (every changed literal)

| # | Location | Base | Stretch | Why |
|---|---|---|---|---|
| 1 | `IG_E` | 480 | 4800 | E=4800 per prereg |
| 2 | `IG_P0_END` | 96 | 960 | ladder fraction ×10 |
| 3 | `IG_P1_END` | 192 | 1920 | ladder fraction ×10 |
| 4 | `IG_P2_END` | 288 | 2880 | ladder fraction ×10 |
| 5 | `IG_P3_END` | 384 | 3840 | ladder fraction ×10 |
| 6 | `IG_NSEG` | 8 | 80 | 80 segments of 60 per prereg |
| 7 | `IG_BIG_CAP` | 2048 | 20480 | 4800×4=19200 entries max |
| 8 | monitored-label split `IG_P0_END+48` (driver + F-grader, 4 sites) | +48 | +480 | P1 first half ×10 |
| 9 | arm R `b_ntrap` / `b_trapcorrect` | 144 | 1440 | P2 960 inverted + P3 480 even-inverted |
| 10 | arm C `b_ntrap` | 192 | 1920 | P2 960 + P3 960 inverted |
| 11 | `claims_present` R/C | 192 | 1920 | P1+P3 claim episodes ×10 |
| 12 | `claims_present` F | 480 | 4800 | claims every episode |
| 13 | `e_trap_n` F | 480 | 4800 | preference trap every episode |
| 14 | `e_trap_n` R/C | 192 | 1920 | P1+P3 preference traps ×10 |
| 15 | `f_mon_n` / `f_unm_n` | 48 | 480 | P1 halves ×10 |
| 16 | G-family twin pairs (`sr_alloc`, loop, `IG_P3_END+48`, `g_count_inv`) | 48 | 480 | P4 twin pairs ×10 |
| 17 | `twin_claims_present` / `twin_prefa_trap` | 480 | 4800 | twin is a full E-episode run |
| 18 | `@import` paths (lines 23–24) | `../../wave4/` | `../../../wave4/` | depth fix: stretch source lives one dir deeper; imported files byte-identical (Gate 1) |

## Deliberately NOT scaled (scale-free by design)

- `fire_step`=11, streak=8, `nrefuse`/`nelim`/`ncommit` counts: P0
  behavior, prereg expects "disconnect still at e=11".
- Refusal probes e=5 / e=12, `legal_at_11`: fixed early episodes.
- Judge unit checks U1–U4 (`ig_judge_core` synthetic inputs 144/192,
  100/192, 95/192): synthetic threshold tests of the judge function,
  not run parameters.
- `g_sig` tripwire `inv>=3` and `b_sig` `retrack*2>=ntrap`: relative/
  fixed tripwires; `g_inv` is additionally asserted ==0 exactly.
- IL gate windows (e<=11 disconnect window; content-relative poison
  window): step-relative, not horizon-relative.
- Branch rule: count-based, no literal.

## Falsification

Same as the base leg (PREREG_INTEG1 §2): any INTEG_CHECK mismatch,
INTEG_FAILURES≠0, non-byte-identical reruns, RNG tokens, or
claims-channel leakage into the learner region ⇒ the stretch claim is
KILLED. A green stretch extends "truthful" from 480 to 4800 episodes;
it does not widen the trap envelope.
