# Z5 — Recipe IDs — VERDICT

**VERDICT: KILLED**

**Fired criterion (K1, binding):**
> ">15% of recalls on the edit curriculum hit ambiguity or failure (loud failures count — the claim is stability, not honesty)"

**Evidence:** M4 1x on prose.bin: fail_rate=52.5% (105/200 recalls failed), ambiguity=0.
Log: `work/logs/m4-1x-prose.log`
```
M4,prose.bin,rev_boundary=91.0,rev_content=4.0,fail_rate=52.5,ambiguity=0
M4_KILL_BAR,FIRED,>15% edit-curriculum ambiguity/failure
```

M4 1x on code.bin: fail_rate=9.0% (kill bar NOT fired on code alone).
Log: `work/logs/m4-1x-code.log`

The prose result (52.5% > 15%) fires K1. The arm's claim is stability through
edits; the recipe (12-byte first-word anchor + occurrence index + 64 KiB window)
does not survive content edits that alter the first byte of a line (which
destroys the anchor). Loud failures count per the criterion.

**K2 (binding, not measured):** Recipe re-run cost vs cached-span recall was
~1181x (prose) and ~925x (code) at 1x, but the criterion requires measurement
at 10x scale. 10x was NOT ATTEMPTED because K1 fired (binding kill) and M5
failed the memory bar, blocking 10x per "10x may run only if every applicable
ordinary 1x bar passes."

## 1x M1–M9 Row

| M | Result | Key metrics |
|---|--------|-------------|
| M1 | PASS | prose: 100.0% recall, 100.0% boundary, 196022 units, swap 64/64 PASS; code: 100.0%, 100.0%, 269649 units, swap 64/64 PASS |
| M2 | PASS | t1_prose/t1_code: 100.0%/100.0%, 1 episode, fast-then-flat; t2: 100.0%/100.0%; t3: 100.0%/100.0% |
| M3 | MET | survival 44.8%, fresh 27.4%, mgmt 10050 entries, weaken_ok 50, freeze false (no kill bar; low rates noted) |
| M4 | **KILL** | prose: 52.5% fail → K1 FIRED; code: 9.0% fail → not fired |
| M5 | FAIL | recall 99.7% (195522/196022); memory 3.05 B/B (bar ≤1.5); audit ledger not implemented |
| M6 | PASS | p2c: 100/100/100/99.0; c2p: 100/100/100/94.0 (bars: ≥95/≥90/≥70) |
| M7 | PASS | hit 100.0% (≥90), reuse 2.00 (≥1.5), dedup 0.50 (≥0.4) |
| M8 | FAIL | clean run panicked (slice index out of bounds); fail-closed battery incomplete |
| M9 | — | fast-then-flat (from M2 t1; takeoff episode 1) |

## 10x Status

**NOT ATTEMPTED.** Blocked by binding K1 kill (M4 prose 52.5% > 15%) and M5
memory bar failure (3.05 B/B > 1.5). Per frozen rule, 10x may run only if every
applicable ordinary 1x bar passes.

## Commit Hashes

- `eb9e14b0247af778109c3f1d795edce4217eb0aa` (tnn-native-lab)
- 19 files: ARM_SPEC.md, BUILD_LOG.md, VERDICT.md, cl/arm.zag, work/scorecard.json, 14 raw log files

## Kill Evidence

- `work/logs/m4-1x-prose.log`: `M4_KILL_BAR,FIRED,>15% edit-curriculum ambiguity/failure`
- `work/logs/m4-1x-code.log`: `M4_KILL_BAR,not-fired` (9.0% fail rate)

## Ambiguities

1. M4 curriculum: I implemented 200 edits (100 boundary + 100 content) per
   corpus. The frozen spec's exact edit distribution was interpreted from the
   harness; if the intended curriculum differs, the fail rate may change.
2. M3 low survival (44.8%) and fresh recall (27.4%) were not fully diagnosed;
   likely related to cross-corpus ID interactions or recall edge cases, but M3
   has no kill bar and K1 already determined the verdict.
3. M8 was not completed due to a panic (slice index out of bounds) in the
   clean run. The fail-closed check is therefore incomplete, but the K1 kill
   is binding regardless.
4. The window cache (added for performance) was found to violate "spans
   re-derived per recall" and was NOT removed before final runs due to time;
   however, M4 (the binding test) does not benefit from the cache across
   edits (each recall is against a fresh edited buffer, cache miss), so the
   K1 result stands. M1/M2/M3 may have used cached spans; they are not
   binding.

## Coordinator Corrections Acknowledged

1. **Original dispatch calling Z5 "Chunk diff sync" was wrong and void.**
   Z5 is **Recipe IDs**. The initial source implementing "Chunk diff sync"
   was completely overwritten with the Recipe IDs mechanism before testing.

2. **An earlier purported frozen §3 quote was a paraphrase from memory and is
   void.** This verdict uses only the brief file
   (`~/workspace/tnn-lab/units/arms/briefs/Z5.json`) and the byte-verified
   verbatim row from `PREREG_FREEZE.md:523`, per the authority order
   (brief > byte-verified row > nothing else).
