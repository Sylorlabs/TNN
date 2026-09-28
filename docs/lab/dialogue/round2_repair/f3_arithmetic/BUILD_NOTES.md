# BUILD_NOTES.md — F3-ARITHMETIC fork

## Toolchain

Pinned lab znc: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

Build (from `dialogue/round2_repair/f3_arithmetic/`):

```
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 dialogue.zag -o dialogue_bin
```

The directory must contain `R33_NATIVE_SHA256_V2.zag` and
`R33_NATIVE_IO_V1.zag` next to `dialogue.zag` (the `@import` chain resolves
them relative to the source file). The binary reads `kb.txt`, `gaz.txt`,
and `battery.txt` from the working directory at runtime.

## Result

- Binary: `dialogue_bin`, sha256
  `4c6ee1ddb284c5aac355a807e0800d7d370dd199ba3fd40683d2f2ded5eb9df2`
- Warnings only (4 pre-existing analyzer notes: one dead-loop heuristic in
  `gaz_scan`, three ignored-return-value notes on `proc_sentence`). No errors.

## What changed vs the frozen `dialogue/dialogue.zag` (diff summary)

1. `irregular_norm`: +7 comparative-adjective mappings (taller→tall,
   older→old, longer→long, bigger→big, smaller→small, earlier→early,
   later→late). Inflectional, closed-class; the general "-er" strip was
   deliberately rejected (would mangle "tower"/"water"/"author").
2. New helpers `diff_dim`, `mindist`, `nearest_event`, `year_val_ev`,
   `ent_year_val` (the difference engine: trigger detection, per-entity
   event-marker selection, live KB value lookup).
3. `do_compose`: new `pv` + `turn_no` parameters; the existing "which is
   taller" branch records the compared pair into `pv` slots 32/36/48/52;
   a new general how-much-difference branch (pair resolution → live value
   lookup → subtraction → bare-number emission; returns 0 / falls through
   when unresolvable).
4. `do_turn` step 3 passes `pv, turn_no` through to `do_compose`.
5. `main`: explicit init of the new `pv` slots at each DIALOGUE start
   (heap arrays are not reliably zeroed).

No changes to the v1 retrieval core, the stemmer, the gazetteer, the KB,
or any existing compose branch's output behavior.
