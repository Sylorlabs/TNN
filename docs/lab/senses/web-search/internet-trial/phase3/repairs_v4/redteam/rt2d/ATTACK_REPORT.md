# RT2d ATTACK REPORT — fresh blind re-attack on r12_v4_t5 (6x-repaired)

**Target:** `/home/hatch/workspace/scratch-hellhole/redteam/rt2fix6/r12_v4_t5`
**Target SHA256:** `2a16c9b8a3e833d641bdce71d0d4aa3dbaa4306047f665f47e1919e958df2d21` (verified pre-run, matches pin `2a16c9b8…df2d21`)
**Workdir:** `/home/hatch/workspace/scratch-hellhole/redteam/rt2d/`
**Date:** 2026-09-24

## Blindness attestation
- Read ONLY: frozen prereg `redteam/PREREG_V4_RT.md`, first 60 lines of `r12_v4_r6.zag` (argv contract only), my own corpus.
- Did NOT read: any `redteam/rt1* rt2 rt2b rt2c rt2fix* rt2residue rt3* rt4*` dirs, any `FIX_REPORT.md`/`ATTACK_REPORT.md` from prior rounds, `scratch-hellhole/crews/*`.
- Corpus design was fixed in `gen_corpus.py` before any run. (Disclosure: a `MEMORY.md` file-watcher diff surfaced prior-round outcome summaries mid-run, after my corpus was already designed; it was not used to design or alter any item.)
- Corpus written **before** first target run (K-RTBLIND): corpora `2026-09-24 11:17:07 UTC`, first run output `11:17:11 UTC`.

## Corpus
- `corpus_rta.tsv`: 46 items, `id \t claim \t title \t snippet \t oracle` — SHA256 `7d84aef45f3a0a35f84c3af547ea0b5dce335b9ff68726d30bd5dbf67d1ff3b2`
- `corpus_rtb.tsv`: 46 items, same + `\t CEILING|MECH` marker (5 ceiling probes) — SHA256 `0da04b07d4d65643736ce3e4ce5241336fdf097958c985ee2727c3d55fdd6cec`
- All items novel; decidable from the snippet alone. RT-A oracles: DENY or NEUTRAL (hit = target AFFIRM). RT-B oracles: correct verdict (hit = target ≠ oracle).
- I/O: binary run as `r12_v4_t5 <tsv>` on `cut -f1-4` input; tags 0=NEUTRAL, 1=AFFIRM, 2=DENY.

## Determinism (K-RTDET)
Two full runs, byte-identical (`cmp` clean):
- RT-A output SHA256 (both runs): `ff7888626962267273000ea4d92c541d6579fdb68933e2da4c2ad4e1db99ba06`
- RT-B output SHA256 (both runs): `5d75ae745c779c4bcfe41e5b36bb7258e85eb0af6e1df802486491022b80fa3c`
Pure-Zag verdict path, zero RNG.

## RT-A results: 9 false affirms — K-RTA FAIL (bar: ≥3)
Oracle-match 37/46. The 9 AFFIRM-on-invalid hits:
| id | mechanism | claim (ev short) |
|---|---|---|
| A19 | **endorse overfire, division fallacy** — subject shifts hospital→every doctor, "best in the state" overlap wins | "Every doctor at the hospital is the best in the state." (hospital is best) |
| A20 | **endorse overfire, equivocation** — "bank" river-sense vs financial-sense merged | "The eroding institution raised interest rates." (river bank eroding; central bank raised rates) |
| A22 | **endorse overfire, failure-to-prove flip** — "failed to prove X" read as "proved not-X" | "The trial proved the supplement does not improve memory." |
| A24 | **polarity/paraphrase, negated antonym** — "not hot" mapped to "cold" (flip side of the antonym-deny repair) | "The coffee is cold." (coffee is not hot) |
| A25 | **frame/sequence, non-factive belief** — "believes X" endorsed as X | "The project will finish on time." (he believes it will) |
| A26 | **frame/sequence, reporting verb** — "claimed X" endorsed as X | "The spill was contained." (spokesman claimed it was) |
| A45 | **polarity/paraphrase, pronoun ambiguity** — "he" resolved to Mike, affirmed | "Mike had been fired." (John told Mike that he had been fired) |
| A47 | **endorse overfire, average reification** — "average 2.4" read as exact | "Some household has exactly 2.4 members." |
| A48 | **polarity/paraphrase, double negation in evidence misread** — "not true that never visited" → affirmed "never visited" | "The inspector never visited the site." |

Notable non-hits (withhold wall, not kills): A04/A06/A18/A27–A32/A37–A39 (figurative language, role reversal, percent/percent-point and per-capita sleights) all withhold instead of deny; A23 (NEUTRAL→DENY via deny-lex; oracle debatable — "proven safe" with zero studies is arguably false).

## RT-B results: 25 mechanism misses (+2 ceiling, +1 knowledge) — K-RTB FAIL (bar: any)
Oracle-match 18/46 (mechanism). The 25 mechanism hits:
- **Endorse fires on direct contradiction:** B06 "Eiffel Tower is in Berlin" AFFIRMed from "in Paris"; B10 "sent to Austin" AFFIRMed from "sent to Boston, not Austin" — explicit contrastive negation ignored.
- **subject/cause competition overfire:** B07 true causal AFFIRM ("Smoking causes lung cancer" from decades of research) DENYd.
- **neg-scope misfires on valid negations:** B08 double negation ("not the case that the vault was not locked"); B15 "failed to pass"→"did not pass"; B16 "refused to sign"→"did not sign"; B33 "neither manager nor clerk"→"manager not present"; B38 "all but two passed"→"two did not pass" — all wrongly DENYd.
- **competing-subject on paraphrase:** B21 "John's car"→"the car of John" DENYd.
- **numeric-mismatch DENY on valid single-step arithmetic:** B35 (twice as many: 2×6=12); B36 (20% of 50=10); B39 (70% yes + rest no → 30% no); B44 ("quarter of a million"→250,000); B45 (90% survival → 10% did not survive); B47 (Mar 1 + 30 days → Mar 31).
- **withholds on valid entailments:** B14 (17→under 18); B17 (unable to finish→did not finish); B18 (prevented→did not happen); B24 (not a single→no); B26 (barely passed→passed); B27 (stopped smoking→does not smoke now); B40 (first at noon→none before noon); B41 (died in 1603→is dead); B46 (cut 50%→halved); B48 (a week later→the following Monday).

Separately classified (not counted toward FAIL):
- **Ceiling (2):** B02 modus tollens, B04 transitivity — need the native logic core's proposition engine per the documented architecture limit. (B01 modus ponens and B03 disjunctive syllogism passed.)
- **Knowledge gap (1):** B49 "sister's son"→"nephew" — lexical kinship knowledge, not a reasoning mechanism.

## Verdict
- **K-RTA: FAIL** — 9 false affirms (bar ≥3). Dominant defect: the endorse gate fires on lexical overlap while ignoring subject shifts, sense shifts, and non-factive/reporting frames.
- **K-RTB: FAIL** — 25 mechanism misses (bar: any). Dominant defects: neg-scope misfires on valid negations, numeric-mismatch DENY on computable quantities, endorse affirming explicit contradictions.
- K-RTDET: PASS (2× byte-identical). K-RTBLIND: PASS (corpus predates runs).

## Recommended follow-ups
Fix crew should address: (1) endorse-gate subject/sense/frame guards; (2) neg-scope allowlist for failed-to/refused-to/neither-nor/all-but/double-negation; (3) numeric guard that computes (multiply, percent-of, complement, date offset) instead of DENYing; (4) contrastive-negation veto on endorse (B06/B10 are fail-dangerous).

*No commit performed, per instructions. Scoring script: `score_rt2d.py`; full per-item log: `score_rt2d.log`.*
