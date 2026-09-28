# Plan-formation verification (contender A, §4)

**Binary:** `src/form_par` (built 2026-09-24, pinned toolchain).
**Two-pass design:** pass 1 enumerates all non-RESPOND event specs into an
immutable table (directive order); pass 2 resolves every RESPOND against the
complete table. Theme text order cannot affect resolution.

## Results (2026-09-24, after hang fix + d_spbase corrections)

| Check | Result |
|---|---|
| `seq`/`rev`/`stride` formation orders | byte-identical plans (`cmp` PASS ×3) |
| Output vs frozen `bytegen/fixture/plan_v1.txt` | byte-identical (`cmp` PASS) |
| Slot coverage (all orders) | every slot computed exactly once |
| Directives/slots (theme_v1) | 12 directives, 1 struct, 23 slots |
| Cue-before-RESPOND vs cue-after-RESPOND | both resolve 440 Hz (nominal 880 ignored); renders bit-identical |
| RESPOND formation order-invariance | `seq`/`rev`/`stride` byte-identical on cue-after theme |
| Near-miss (nominal 460) | resolved 440.00 Hz, +0.00 cents |
| Sub-octave (nominal 220) | resolved 440 Hz |
| Polyphonic cue (louder 440) | resolved 440 Hz |
| Polyphonic tie | earliest event wins |

## Bug history (honest record)

1. **Sequential-xref defect:** first version resolved RESPOND against only
   previously-seen specs → cue-after-RESPOND kept nominal 880. Fixed by
   two-pass restructure.
2. **Infinite loop:** surgery left `di = di + 1` inside the outer `else`
   (pass-1 while never advanced on INST directives) and stole the while's
   closing brace from later code — braces balanced by accident, binary hung.
   Fixed by restoring proper nesting (verified with robust brace checker).
3. **d_spbase off-by-one:** recorded post-increment `nsp` instead of the
   RESPOND's own spec index. Fixed (record before increment).
4. **SPMAX-full guard:** unresolvable RESPOND slots now skipped, not emitted
   with garbage indices.

All four fixed and re-verified 2026-09-24. The current binary passes every
check above.
