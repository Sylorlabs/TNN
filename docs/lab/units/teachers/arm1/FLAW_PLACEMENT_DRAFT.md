# Flaw Placement Map — DRAFT-FOR-PARENT-WIRING

**Status: DRAFT.** Deterministic placement of the 12 flaws per slice: no RNG anywhere.
Placement is a pure function `f(slice_hash, flaw_index)` specified below; the resulting
positions are tabulated per slice for auditability.

## f — the placement function (normative)

```
slice_hash = SHA-256(b"TNN-TRACKB-ARM1-SLICE-v1|" || corpus_id || b"|" || slice_id
                     || b"|" || ASCII(corpus_start))      # 32 bytes, hex in manifest
u[j] = LE64(slice_hash[8*j .. 8*j+8])                        # j = 0..11

elig(S) = positive-judgment, non-ambiguous vocab entries with >= 2 in-slice occurrences,
          sorted by chunk_id.  (Ambiguous A1-A4 excluded: their boundary dispute is honest,
          never a flaw anchor.)

j = 0..3  (wrong-span):
  e   = elig[u[j] mod |elig|], skipping already-used entries (linear probe)
  occ = in-slice occurrences of e.pattern under e.rule; oi = (u[j]>>32) mod |occ|
  [a,b) = occ[oi];  m = 1 + ((u[j]>>40) mod 3);  sgn = +1 if (u[j]>>63)&1 else -1
  flaw = [a+sgn*m, b+sgn*m); if out of slice bounds, flip sgn (always valid: m<=3,
         occurrences are interior or the flip lands interior)
  grounds = occ[oi+1], occ[oi+2] (mod |occ|); conf = CONF(J_e, 2)

j = 4..7  (false-confidence):
  e, occ, oi, [a,b) as above (fresh entry)
  flaw = [a,b)            # TRUE span
  conf = 255
  grounds = [] if j even (missing) else two occurrences of elig[(idx(e)+3) mod |elig|]
            (contradictory: evidence for a DIFFERENT entry)

j = 8..9  (missing-grounding):
  e, occ, oi, [a,b) as above (fresh entry)
  flaw = [a,b);  grounds = [];  conf = CONF(J_e, 0)   # honest-range confidence, no evidence

j = 10..11 (plausible-false):
  cands = elig entries with pattern len>=4 and class in {func, content, kw}, in elig order
  for attempt = 0.. :
    e = cands[(u[j] mod |cands| + attempt) mod |cands|]
    occ = occurrences; oi = ((u[j]>>32) + attempt) mod |occ|; [a,b) = occ[oi]
    scan sa in 0..3, len in 3..8 (deterministic order): frag = [a+sa, a+sa+len)
      accept first frag with all-ASCII-letters, != pattern, span != [a,b),
      and not equal to any already-placed flaw span in this slice
  flaw = frag; grounds = []; conf = CONF(J_e, 1)
```

Worked properties (verified by the reference generator over all 8 slices):
- 12 distinct flaw spans per slice; wrong-span shifts ∈ {±1,±2,±3}; no flaw span is empty
  or out of bounds; false-confidence flaws sit on true spans at confidence 255;
- plausible-false fragments are 3–8 ASCII letters, never equal to a vocabulary pattern.

## Per-slice anchor table

| flaw | type | anchor entry | occurrence # | true span (slice-rel) | shift | flaw span (slice-rel) |
|---|---|---|---|---|---|---|
| F-S0-00 | wrong-span | T1-P011 `for` | 41 | 36100-36103 | +3 | 36097-36100 |
| F-S0-01 | wrong-span | T1-P014 `is` | 65 | 48353-48355 | +1 | 48352-48354 |
| F-S0-02 | wrong-span | T1-P009 `thou` | 85 | 27935-27939 | -1 | 27936-27940 |
| F-S0-03 | wrong-span | T1-P025 `love` | 23 | 16357-16361 | +3 | 16354-16358 |
| F-S0-04 | false-confidence | T1-P001 `the` | 0 | 30-33 | — | 30-33 |
| F-S0-05 | false-confidence | T1-P002 `and` | 0 | 107-110 | — | 107-110 |
| F-S0-06 | false-confidence | T1-P003 `of` | 0 | 300-302 | — | 300-302 |
| F-S0-07 | false-confidence | T1-P004 `to` | 0 | 701-703 | — | 701-703 |
| F-S0-08 | missing-grounding | T1-P005 `my` | 0 | 612-614 | — | 612-614 |
| F-S0-09 | missing-grounding | T1-P006 `in` | 0 | 8-10 | — | 8-10 |
| F-S0-10 | plausible-false | T1-P007 `that` | 0 | 880-884 | — | 880-883 |
| F-S0-11 | plausible-false | T1-P007 `that` | 0 | 880-884 | — | 881-884 |
| F-S1-00 | wrong-span | T1-P029 `death` | 6 | 36081-36086 | +2 | 36079-36084 |
| F-S1-01 | wrong-span | T1-P025 `love` | 54 | 30744-30748 | -2 | 30746-30750 |
| F-S1-02 | wrong-span | T1-P035 `fair` | 4 | 20537-20541 | +3 | 20534-20538 |
| F-S1-03 | wrong-span | T1-P016 `not` | 75 | 41724-41727 | +1 | 41723-41726 |
| F-S1-04 | false-confidence | T1-P001 `the` | 0 | 212-215 | — | 212-215 |
| F-S1-05 | false-confidence | T1-P002 `and` | 0 | 55-58 | — | 55-58 |
| F-S1-06 | false-confidence | T1-P003 `of` | 0 | 288-290 | — | 288-290 |
| F-S1-07 | false-confidence | T1-P004 `to` | 0 | 196-198 | — | 196-198 |
| F-S1-08 | missing-grounding | T1-P005 `my` | 0 | 96-98 | — | 96-98 |
| F-S1-09 | missing-grounding | T1-P006 `in` | 0 | 41-43 | — | 41-43 |
| F-S1-10 | plausible-false | T1-P007 `that` | 0 | 224-228 | — | 224-227 |
| F-S1-11 | plausible-false | T1-P007 `that` | 0 | 224-228 | — | 225-228 |
| F-S2-00 | wrong-span | T1-P007 `that` | 59 | 34911-34915 | +3 | 34908-34912 |
| F-S2-01 | wrong-span | T1-P016 `not` | 104 | 52484-52487 | +2 | 52482-52485 |
| F-S2-02 | wrong-span | T1-P030 `heart` | 0 | 18572-18577 | +1 | 18571-18576 |
| F-S2-03 | wrong-span | T1-P011 `for` | 23 | 17815-17818 | +3 | 17812-17815 |
| F-S2-04 | false-confidence | T1-P001 `the` | 0 | 610-613 | — | 610-613 |
| F-S2-05 | false-confidence | T1-P002 `and` | 0 | 932-935 | — | 932-935 |
| F-S2-06 | false-confidence | T1-P003 `of` | 0 | 552-554 | — | 552-554 |
| F-S2-07 | false-confidence | T1-P004 `to` | 0 | 134-136 | — | 134-136 |
| F-S2-08 | missing-grounding | T1-P005 `my` | 0 | 360-362 | — | 360-362 |
| F-S2-09 | missing-grounding | T1-P006 `in` | 0 | 901-903 | — | 901-903 |
| F-S2-10 | plausible-false | T1-P007 `that` | 0 | 820-824 | — | 820-823 |
| F-S2-11 | plausible-false | T1-P007 `that` | 0 | 820-824 | — | 821-824 |
| F-S3-00 | wrong-span | T1-P022 `his` | 96 | 64707-64710 | +3 | 64704-64707 |
| F-S3-01 | wrong-span | T1-P002 `and` | 166 | 47417-47420 | +2 | 47415-47418 |
| F-S3-02 | wrong-span | T1-P036 `ing` | 127 | 51262-51265 | -1 | 51263-51266 |
| F-S3-03 | wrong-span | T1-P024 `as` | 41 | 60346-60348 | -2 | 60348-60350 |
| F-S3-04 | false-confidence | T1-P001 `the` | 0 | 9-12 | — | 9-12 |
| F-S3-05 | false-confidence | T1-P003 `of` | 0 | 206-208 | — | 206-208 |
| F-S3-06 | false-confidence | T1-P004 `to` | 0 | 35-37 | — | 35-37 |
| F-S3-07 | false-confidence | T1-P005 `my` | 0 | 1319-1321 | — | 1319-1321 |
| F-S3-08 | missing-grounding | T1-P006 `in` | 0 | 451-453 | — | 451-453 |
| F-S3-09 | missing-grounding | T1-P007 `that` | 0 | 99-103 | — | 99-103 |
| F-S3-10 | plausible-false | T1-P007 `that` | 0 | 99-103 | — | 99-102 |
| F-S3-11 | plausible-false | T1-P007 `that` | 0 | 99-103 | — | 100-103 |
| F-S4-00 | wrong-span | T1-C006 `else` | 23 | 59258-59262 | +1 | 59257-59261 |
| F-S4-01 | wrong-span | T1-C005 `if` | 10 | 21569-21571 | +3 | 21566-21568 |
| F-S4-02 | wrong-span | T1-C014 `sqlite3_context` | 6 | 9449-9464 | +2 | 9447-9462 |
| F-S4-03 | wrong-span | T1-C008 `static` | 3 | 29735-29741 | -1 | 29736-29742 |
| F-S4-04 | false-confidence | T1-C001 `int` | 0 | 90-93 | — | 90-93 |
| F-S4-05 | false-confidence | T1-C002 `void` | 0 | 352-356 | — | 352-356 |
| F-S4-06 | false-confidence | T1-C003 `const` | 0 | 77-82 | — | 77-82 |
| F-S4-07 | false-confidence | T1-C004 `char` | 0 | 10-14 | — | 10-14 |
| F-S4-08 | missing-grounding | T1-C007 `return` | 0 | 18535-18541 | — | 18535-18541 |
| F-S4-09 | missing-grounding | T1-C009 `struct` | 0 | 4009-4015 | — | 4009-4015 |
| F-S4-10 | plausible-false | T1-C002 `void` | 0 | 352-356 | — | 352-355 |
| F-S4-11 | plausible-false | T1-C002 `void` | 0 | 352-356 | — | 353-356 |
| F-S5-00 | wrong-span | T1-C024 `SQLITE_` | 7 | 2010-2017 | -3 | 2013-2020 |
| F-S5-01 | wrong-span | T1-C006 `else` | 31 | 64743-64747 | -2 | 64745-64749 |
| F-S5-02 | wrong-span | T1-C001 `int` | 145 | 43690-43693 | -1 | 43691-43694 |
| F-S5-03 | wrong-span | T1-C014 `sqlite3_context` | 1 | 18529-18544 | -2 | 18531-18546 |
| F-S5-04 | false-confidence | T1-C002 `void` | 0 | 9421-9425 | — | 9421-9425 |
| F-S5-05 | false-confidence | T1-C003 `const` | 0 | 6100-6105 | — | 6100-6105 |
| F-S5-06 | false-confidence | T1-C004 `char` | 0 | 7498-7502 | — | 7498-7502 |
| F-S5-07 | false-confidence | T1-C005 `if` | 0 | 1882-1884 | — | 1882-1884 |
| F-S5-08 | missing-grounding | T1-C007 `return` | 0 | 17895-17901 | — | 17895-17901 |
| F-S5-09 | missing-grounding | T1-C008 `static` | 0 | 15524-15530 | — | 15524-15530 |
| F-S5-10 | plausible-false | T1-C002 `void` | 0 | 9421-9425 | — | 9421-9424 |
| F-S5-11 | plausible-false | T1-C002 `void` | 0 | 9421-9425 | — | 9422-9425 |
| F-S6-00 | wrong-span | T1-C017 `sqlite3_mutex` | 1 | 46797-46810 | -2 | 46799-46812 |
| F-S6-01 | wrong-span | T1-C001 `int` | 59 | 36289-36292 | -2 | 36291-36294 |
| F-S6-02 | wrong-span | T1-C018 `sqlite3_free` | 1 | 35610-35622 | +1 | 35609-35621 |
| F-S6-03 | wrong-span | T1-C011 `while` | 4 | 46423-46428 | +1 | 46422-46427 |
| F-S6-04 | false-confidence | T1-C002 `void` | 0 | 2258-2262 | — | 2258-2262 |
| F-S6-05 | false-confidence | T1-C003 `const` | 0 | 1507-1512 | — | 1507-1512 |
| F-S6-06 | false-confidence | T1-C004 `char` | 0 | 1571-1575 | — | 1571-1575 |
| F-S6-07 | false-confidence | T1-C005 `if` | 0 | 128-130 | — | 128-130 |
| F-S6-08 | missing-grounding | T1-C006 `else` | 0 | 729-733 | — | 729-733 |
| F-S6-09 | missing-grounding | T1-C007 `return` | 0 | 912-918 | — | 912-918 |
| F-S6-10 | plausible-false | T1-C002 `void` | 0 | 2258-2262 | — | 2258-2261 |
| F-S6-11 | plausible-false | T1-C002 `void` | 0 | 2258-2262 | — | 2259-2262 |
| F-S7-00 | wrong-span | T1-C007 `return` | 33 | 28905-28911 | +3 | 28902-28908 |
| F-S7-01 | wrong-span | T1-C008 `static` | 85 | 65364-65370 | +2 | 65362-65368 |
| F-S7-02 | wrong-span | T1-C011 `while` | 1 | 3087-3092 | +1 | 3086-3091 |
| F-S7-03 | wrong-span | T1-C012 `for` | 20 | 21549-21552 | +2 | 21547-21550 |
| F-S7-04 | false-confidence | T1-C001 `int` | 0 | 146-149 | — | 146-149 |
| F-S7-05 | false-confidence | T1-C002 `void` | 0 | 669-673 | — | 669-673 |
| F-S7-06 | false-confidence | T1-C003 `const` | 0 | 1246-1251 | — | 1246-1251 |
| F-S7-07 | false-confidence | T1-C004 `char` | 0 | 2989-2993 | — | 2989-2993 |
| F-S7-08 | missing-grounding | T1-C005 `if` | 0 | 742-744 | — | 742-744 |
| F-S7-09 | missing-grounding | T1-C006 `else` | 0 | 944-948 | — | 944-948 |
| F-S7-10 | plausible-false | T1-C002 `void` | 0 | 669-673 | — | 669-672 |
| F-S7-11 | plausible-false | T1-C002 `void` | 0 | 669-673 | — | 670-673 |

## Verification procedure (auditor)

1. Recompute `slice_hash` per slice from the corpus files (hashes in wiring spec §0).
2. Re-run `f` per the normative pseudocode above; every anchor/span must match the table.
3. Confirm the 12 flaw spans per slice match `sealed/SEALED_FLAW_MANIFEST_DRAFT.md` exactly.
4. Confirm no step uses randomness, wallclock, or unlogged state (code inspection).

