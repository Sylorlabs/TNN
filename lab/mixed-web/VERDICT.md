# MIXED-WEB — verdict

**Question:** when the web gives mixed results, can TNN use logic to find the
truth — converging safely where evidence warrants it, withholding where it
doesn't?

**Method:** 29 live SearXNG queries recorded 2026-09-21 (frozen envelopes in
`live/`). 12 dropped at the preregistered inspection gate (1 relevant
result, or no genuine disagreement). **17 scored**, above the 16-question
coverage bar. Two arms replay the identical frozen evidence:

- **Arm A** — existing safe-withhold web-sense behavior (v2 `ws2_sense.zag`
  verbatim): converge only on 2+ corroboration, else withhold.
- **Arm B** — conflict-driven deliberation (`mw_sense.zag`, pure Zag, zero
  RNG): recency / majority / corroboration rules in frozen priority order,
  else withhold. Every verdict carries a hash-chained ledger reasoning chain.

**Determinism:** 5 full repetitions per arm, byte-identical logs.

## Kill bars

| Bar | Result |
|---|---|
| KB-MW-WRONG (one wrong convergence) | **PASS** — 13/13 B convergences match gold |
| KB-MW-GUESS (guessing on ambiguous evidence) | **PASS** — B withholds on all 3 UNDETERMINABLE questions |
| KB-MW-LEDGER (complete reasoning chain) | **PASS** — 17/17 chains complete; all ledger heads independently recomputed from the envelopes in Python and match |
| KB-MW-DET (nondeterminism) | **PASS** — 5/5 byte-identical per arm |
| Coverage (≥16 scored) | **PASS** — 17 scored (12 dropped, documented in `golds.json`) |
| VALUE-CONFIRMED (≥4 questions where B reaches the preregistered result and A does not) | **CONFIRMED** — exactly 4 |

## Per-question results

disp: arm-A disposition (6 = provisional-majority converge, 2 = withhold).
A "guessed" on all four withhold-expected questions.

| q | question | expected | B verdict | B chosen | rule | A disp | A chosen | gold | outcome |
|---|---|---|---|---|---|---|---|---|---|
| M01 | oldest university | CONVERGE | CONVERGE | U. of Bologna | MAJORITY | 6 | U. of Bologna | U. of Bologna | both right |
| M02 | telephone inventor | CONVERGE | CONVERGE | A.G. Bell | MAJORITY | 6 | A.G. Bell | A.G. Bell | both right |
| M03 | discovered America | CONVERGE | CONVERGE | Columbus | MAJORITY | 6 | Columbus | Columbus | both right |
| M05 | largest desert | CONVERGE | CONVERGE | Antarctic | MAJORITY | 6 | Antarctic | Antarctic | both right |
| M08 | tallest mountain | CONVERGE | CONVERGE | Everest | MAJORITY | 6 | Everest | Everest | both right |
| M10 | oldest civilization | CONVERGE | CONVERGE | Mesopotamia | CORROB | 6 | Mesopotamia | Mesopotamia | both right |
| M12 | light-bulb inventor | CONVERGE | CONVERGE | Edison | MAJORITY | 6 | Edison | Edison | both right |
| M13 | most-populous city | CONVERGE | CONVERGE | Tokyo | CORROB | 6 | Tokyo | Tokyo | both right |
| M15 | largest economy | CONVERGE | CONVERGE | United States | MAJORITY | 6 | United States | United States | both right |
| M20 | tallest waterfall | CONVERGE | CONVERGE | Angel Falls | MAJORITY | 6 | Angel Falls | Angel Falls | both right |
| R02 | largest population | CONVERGE | CONVERGE | India | RECENCY | 6 | India | India | both right |
| R04 | US president | CONVERGE | CONVERGE | D. Trump | RECENCY | 6 | D. Trump | D. Trump | both right |
| R06 | richest person | CONVERGE | CONVERGE | E. Musk | RECENCY | 6 | E. Musk | E. Musk | both right |
| M17 | fastest animal | WITHHOLD | WITHHOLD | — | TIE | 6 | Peregrine falcon | UNDETERMINABLE | **B right, A guessed** |
| M21 | oldest language | WITHHOLD | WITHHOLD | — | TIE | 6 | Sumerian | UNDETERMINABLE | **B right, A guessed** |
| M23 | largest pyramid | WITHHOLD | WITHHOLD | — | TIE | 6 | Giza | UNDETERMINABLE | **B right, A guessed** |
| R03 | FIFA champion | WITHHOLD | WITHHOLD | — | TIE | 6 | Argentina | Spain | **B right, A wrong** |

**Headline, honestly stated:** on all 13 converge-expected questions the two
arms agree — deliberation found no truth that simple majority-count missed.
Its entire measured value is on the withhold side: where the evidence is
genuinely split (3v2, 2v2, 3v2v1), B withholds while A converges on a guess —
and in R03 that guess is flatly wrong (stale majority: Argentina 3 domains
vs the true 2026 champion Spain, 1 domain).

## Representative ledger reasoning chains

**M12 — MAJORITY converge (Edison 6v1):**
`V|B|M12|CONVERGE|Edison|MAJORITY|Edison,6,1929|Davy,1,0|livescience.com,sciencefocus.com,allthatsinteresting.com|<head>`
Six independent domains assert Edison against one for Davy; 6 ≥ 3 and
6 ≥ 2×1 → MAJORITY fires. Head `d122fe2e…` recomputed independently from the
frozen envelope.

**R06 — RECENCY converge (Musk over Bezos):**
`V|B|R06|CONVERGE|Elon Musk|RECENCY|Jeff Bezos,1,2000|Elon Musk,3,2026|bloomberg.com,wikipedia.org,statista.com|<head>`
Newest candidate Musk (2026, 3 domains) is ≥3 years newer than Bezos (2000);
stale side (1 domain) is not ≥2× the newest (3) → converge on newest.

**M13 — CORROB converge (Tokyo 2v1v1):**
`V|B|M13|CONVERGE|Tokyo|CORROB|Delhi,1,0|Tokyo,2,0|Shanghai,1,0|brainly.com,youtube.com|<head>`
No majority (2 < 3), but best has ≥2 domains, only 4 distinct domains total,
runner-up ≤1 → CORROB fires.

**R03 — TIE withhold (the stale-majority trap):**
`V|B|R03|WITHHOLD||TIE|Argentina,3,2026|Spain,1,2026|Brazil,2,1950||<head>`
Argentina leads 3v2v1 but the lead is not 2× the runner-up, and the recency
gap test fails (Spain also 2026). Arm A converged on Argentina — wrong:
fifa.com's own page reports "Spain's World Cup 2026 triumph"; the Argentina
answers are stale pre-2026 sources. B's withhold is the preregistered
correct result here.

## Honest boundary

R03 shows the logic's limit, not just its value: a careful human reader of
the same evidence spots "Spain's World Cup 2026 triumph" on fifa.com — the
competition's own site — and converges on Spain. The frozen rules cannot
weight source authority; they see 3v2v1 and withhold. Withholding was safe
and preregistered-correct, but it is strictly weaker than what the evidence
permits. Source-authority weighting is the named next mechanism to test.

## Implementation repairs (no rule changes)

1. `mw_sense.zag` was written with a word-array ledger in comments but a
   string-field hash chain in code; oracle verifies the actual chain.
2. Removed a `mw_print_ledger` stub that referenced nonexistent helpers.
3. Fixed the D-op field layout in the unreachable nc==0 early-return path to
   match the standard (rule,chosen,chain,supp) layout.
4. Fixed the oracle's V-line parser (chain contains `|` separators).
5. Prereg amendments A1 (arm-A 6-pair cap documented) and A2 (six added
   questions M18–M23), both pre-record, no bar changes.

## Artifacts

- `PREREG.md` — frozen prereg + amendments A1/A2
- `live/` — 29 frozen SearXNG envelopes
- `golds.json` — 17 golds + 12 documented drops
- `src/` — `mw_sense.zag`, `mw_trial.zag`, `mw_cases.zag` (generated),
  `ws2_sense.zag`, R33 native libs
- `runs/` — `CASE_MANIFEST.txt`, `discovery.log`, 10 run logs
  (`mw_a_r0..4`, `mw_b_r0..4`), `SHA256SUMS`
- `record_mw.py`, `gen_mw.py`, `verify_mw.py` — recorder, generator,
  independent oracle
