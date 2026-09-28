# VERDICT — Integrated Round-2 Dialogue Repair

## Summary
The five families are merged in the required pipeline order. Round-2 achieves
18/18. All held-out probes pass (36/36). Every battery was run twice;
all pairs are byte-identical. Zero RNG. No held-out literals in source.
Canonical frozen files are unchanged (hashes verified).

**However, the PREREG_INT.md kill bar requiring the round-1 battery to be
byte-identical to the canonical baseline is FAILED: 7 answers differ.**
This verdict reports the failure honestly per the task requirements.

## Results

### Round-2 (18/18 PASS, byte-identical runs)
All 18 turns match the preregistered expected answers:
1. `Andy Weir wrote The Martian.` ✓
2. `Andy Weir was born in 1972.` ✓
3. `no.` ✓
4. `charles darwin was born first.` ✓
5. `the eiffel tower is taller.` ✓
6. `120` ✓ (F3 difference engine + carry)
7. `the eiffel tower was built first.` ✓ (F1 pair persists past turn 6)
8. `I don't know.` ✓ (F2 withhold)
9. `I don't know.` ✓
10. `Herman Melville was born in 1813.`→`1819.` ✓ (canonical fact)
11. `Yes. Herman Melville was born in 1819, not 1818. I was taught that.` ✓ (F4)
12. `no.` ✓
13. `I don't know.` ✓
14. `I don't know any jokes.` ✓ (F5)
15. `You asked: who wrote the martian?` ✓ (F5)
16. `I was taught that Andy Weir wrote The Martian.` ✓ (F4)
17. `I don't know.` ✓
18. `I can't forget.` ✓ (F5)

Logs: `round2_run1.log`, `round2_run2.log` (`cmp` clean).

### Held-outs (36/36 PASS, byte-identical runs)
- **F1** (8 turns): 7 T-PASS + H6t2 manual A-line exact match
  (`The Eiffel Tower was built in 1889.`) → 8/8
- **F2** (7 probes): 7/7 T-PASS (`I don't know.` on unanswerables)
- **F3** (10 turns): 10/10 T-PASS, including H8 "how much older..." → `10`
  (F3-before-F1 ordering verified: numeric difference wins over qualitative)
- **F4** (7 probes): 7/7 per HELDOUT.md substring criteria
  (H1: `1793`+`not 1792`+`taught`; H2: no `, not ` clause; H3: `330`+`not 300`;
  H4: no `, not ` clause; H5/H6/H7: `I was taught that` + fact, not bare)
- **F5** (7 probes): 7/7 T-PASS (2 joke, 3 memory-echo, 2 forget-challenge)

Logs: `heldout_f1_run1/2.log`, `heldout_f2_run1/2.log`,
`heldout_f3_run1/2.log`, `heldout_f4_run1/2.log`, `heldout_f5_run1/2.log`.

### Five-good-turn regression
The 5 turns that were good in the pre-repair 5/18 baseline are all good in
the merged system (it scores 18/18, a superset). No previously-good turn
regressed on round-2.

### Round-1 battery — KILL BAR FAILED (7 deltas)
Sections: FOLLOWUP 44/45, CORRECTION 45/45, REFERENT 57/60, WEIRD 30/30,
WEIRD_CLEAN 30/30, TOPIC 57/60, CONTRADICT 72/72, COMPOSE 28/28.
Canonical was 45/45, 60/60, 60/60 on the three affected sections.

The 7 deltas (merged vs canonical):
1. FU-08 t3: `The Amazon River is 6400 kilometers long.` → `I don't know.`
2. RE-01 t3: `The Louvre is in Paris.` → `I don't know.`
3. RE-06 t3: `The Louvre is in Paris.` → `I don't know.`
4. RE-11 t3: `The Louvre is in Paris.` → `I don't know.`
5. TO-02 t2: `Pride and Prejudice was published in 1813.` →
   `Jane Austen wrote the novel Pride and Prejudice.`
6. TO-07 t2: same as 5.
7. One further TO t2: same as 5.

Root causes:
- Deltas 1–4: F2's withhold gate declines "What about X?" follow-ups that
  the canonical system answered correctly. The gate is tuned for round-2
  unanswerables and is over-aggressive here. Each family passed round-1
  independently; the over-withhold emerges from the merged pipeline.
- Deltas 5–7: F4's ellipsis ("carry the previous question's shape") resolves
  "What about Pride and Prejudice?" → "who wrote pride and prejudice"
  because pv[8] holds entity 0 in the merged build where F4's fork left it
  <0. The merge interaction (pe3/eout state via F1's pre-retrieval
  gaz_scan) was not fully diagnosed. F4's fork alone does not fire the
  ellipsis here.

The two integrated runs are byte-identical to each other
(`round1_run1.log` vs `round1_run2.log`, `cmp` clean); they are NOT
byte-identical to the canonical baseline. Per PREREG_INT.md §kill-bar, this
is a failure of the integration.

### Determinism
Every battery (round-2, 5 held-outs, round-1) was run twice; all pairs
`cmp` clean. No RNG in source (`grep -c "rand\|rng\|random"` = 0).

### No-gaming
No held-out literal appears in the merged source (`sentinel-heldout`,
`heldout-h6t2`, `F5H-` all 0 matches). The integrator never opened the
probe files (only copied them as battery inputs).

### Canonical freeze
All five canonical files verify to their committed hashes (see BUILD_NOTES).

## Verdict
**CONDITIONAL FAIL.** The integration fully achieves its repair goals
(round-2 18/18, held-outs 36/36, deterministic, zero RNG, no gaming,
canonical frozen), but it does NOT satisfy the preregistered round-1
byte-identical kill bar (7 regressions: 4 F2 over-withholds, 3 F4
ellipsis over-fires). The failures are reported exactly above; the
evidence logs are committed alongside.
