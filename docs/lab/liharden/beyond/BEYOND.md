# BEYOND — mechanisms better than HL-1..HL-13 (measured)

Date: 2026-09-24. Crew: LI-HARDEN BEYOND. Method: pure-Zag deterministic probes
(zero RNG; every fixture × mechanism run twice, byte-identical), measured against
Crew B's frozen fixtures (`liharden/corrob/fixtures/`, 32 cases) plus 7 new BEYOND
fixtures. Standing rule applied throughout: when in doubt, test both; negative
results reported, not hidden.

Probe: `beyond.zag` (SHA-256 `4b9c3dd03963168c037d03f4ffeb8c381e41f3188a3561349795547e93d83718`),
built with the pinned toolchain `znc_linux_x86_64_abed8aa1`. Evidence:
`results3.tsv` (39 cases × 15 mechanisms × 2 reps = 1170 runs + header),
`sel_results.tsv` (selection-layer experiment). 7 new fixtures in `fixtures/`,
archive/registry pins in `pins/`.

## 0. Baseline honesty notes (read before the ranking)

Three probe defects from round 1 were found and fixed before the final numbers:
host-diversity counting never fired (`beq` needs equal lengths; `nhost` was
`nvotes` in round 1 — numerically harmless on these fixtures since every page
has a distinct hostname, but fixed with length-aware compare), the `read_stdin`
dead-loop analyzer warning (rewrote the increment), and contraction handling
(`isn't` → `is not`, so `C_neg2_contraction` now withholds under base, matching
Crew B). The probe's `base` opens **all** fixture pages, while Crew B
production opens only the top 3 — §6 measures that difference explicitly.

## 1. Ranked mechanisms (correctness gained per unit cost)

Gain = incremental attack kills vs probe-base on the 20 original attack
fixtures (+ kills on new BEYOND fixtures), with any H1–H12 honest regression
counted as a veto. Cost = LOC + fetch/state + pipeline burden.

| # | Mechanism | Kills Δ | Honest | Cost | Verdict |
|---|---|---|---|---|---|
| 1 | **ch1** assertion-polarity veto (negation-flipper scan stronger than HL-4) | +1 (`X_QUOTE1_polarity`) | 12/12 | ~30 LOC | **BUILD** — best ratio measured |
| 2 | **ch2** furniture-coupled repetition discount (narrower, safer HL-10) | +1 (`X_BOILER1_widget`) | 12/12 | ~40 LOC | **BUILD** |
| 3 | **Candidate-set expansion** (selection layer, §6) | +2 vs production behavior (`X_SATUR1_crowdout`, `C_numD_dissent`: top-3 INSTALL → expanded WITHHOLD) | 12/12, H8 intact under both | wider retrieval (latency/fetch) | **BUILD** — highest leverage; M3-as-ranking is partly a *selection* bug, not a verdict bug |
| 4 | **g1** archived rival-filler precedence (grok #1) | +1 new class (`F1_sydney` ARCHVETO) | 12/12 | pin pipeline (content-addressed, versioned) + closed-class templates | **BUILD for pinned classes** — highest-value oracle-adjacent mechanism; see §7 caveats |
| 5 | **g6** pinned primary registry (grok #6) | +1 (`F1_sydney` REGVETO) | 12/12 | registry governance (code is trivial; maintenance is the cost) | **BUILD where an oracle exists** |
| 6 | **w11** nameserver-apex clustering (fable Tier 2) | +1 class (`F_M3_NAIVE` OPCOIN) | 12/12 | ~40 LOC + DNS | **BUILD** — fable's §7 falsification reproduced: naive blocked, hardened evades, honest intact |
| 7 | **w12** CMS fingerprint overlap (fable Tier 2) | +1 class (`F_M3_NAIVE` CMSCOIN) | 12/12 | ~80 LOC | **BUILD** — lazy-attacker speedbump |
| 8 | **w3** operator-coincidence buildout (HL-13, fable Tier 3) | +1 class (`F_M3_NAIVE` OPCOIN2) | 12/12 | ~200 LOC + WHOIS pipeline | **BUILD as detection-only** cost-raiser |
| 9 | **g7** surprisal-conditional collapse (grok #7: HL-10 done safely) | +1 synthetic (`F7_longring` COPYCOLLAPSE) | 12/12 | ~50 LOC | **BUILD narrowly** — kills only long-sentence rings; short-claim rings (all original fixtures) untouched by design |
| 10 | **w6** domain-age 30-day (fable Tier 3) | kills impatient fixture (AGEBLOCK) | 12/12* | ~20 LOC on W3 pipeline | **DOWNGRADE to tax-only** — *fail-open on missing metadata here; WALL-RED `walltemp.zag` measured the negative: age gates pass patient W_S3 (369d) while flagging honest H_H1 (10d). Temporal separates old-from-novel, never true-from-false. Keep as delay signal, never truth signal |
| — | **g4** corroborated contradiction (grok #4) | **−5** (`C_neg2`, `C_num2`, `C_numD`, `X_SATUR1`, `X_SATUR1b` flip to INSTALL) | 12/12 | — | **REJECT** — exceeds grok's own "more than a couple" bar; worse, it installs the false 2000m claim over a single honest 500m dissenter |
| — | **g9** higher k=5 for templatic claims (grok #9) | 0 new | **7/12** (H1,H2,H4,H8,H9 + honest wire + true T4 withheld) | — | **REJECT as specified** — grok said "measure before shipping"; measured: not nearly free |
| — | **ch3** informativeness gate | 20/20 | **10/12** (H10,H11) | — | **REJECT** |
| — | **ch2b** naive surrounding-text collapse | 14/20 | **11/12** (H8) | — | **REJECT** — reproduces the HL-10 problem; independently cross-validates fable's W1 kill |
| — | **ch4** scope uniformity | 0 | 12/12 | — | **REJECT** — kills nothing on this battery |

Fable's ceiling sanity check (~$10→~$100 attacker cost + ~30d delay without
external feeds): consistent. w11/w12/w3/w6 together land the metadata-bundled
attacker at ~$100 + procurement friction; the hardened fixture (`F_M3_HARDENED`:
diversified WHOIS/NS/IP/CMS, whitelisted DNS) evades all of them — the wall
stands where fable said it stands. Note the framing tension: fable's ceiling
assumes *no external feeds*, but grok's #1 (g1) **is** an external feed (a
pinned archive). g1 sits outside fable's ceiling by construction.

## 2. Per-tier alternatives (≥1 per HL tier, all probed)

- **Tier 1 (HL-1..HL-5, parsing/normalization):** ch1 beats HL-4's scan on
  polarity attacks (+1 kill, 0 regression). g4 (corroborated contradiction)
  was the Tier-1 alternative we hoped for — measured and rejected (−5 kills).
  Candidate-set expansion (grok #4's first half, WALL-RED crack 2) belongs
  here architecturally: it is a *selection* repair, not a verdict gate.
- **Tier 2 (HL-6..HL-10, corroboration):** ch2 replaces HL-10's body-hash with
  a furniture-coupled discount (+1 kill, H8 preserved). g7 replaces HL-10 for
  the long-sentence subclass (short-claim rings exempt by construction —
  this is the grok-vs-fable HL-10 disagreement, probed: fable's bucket-(c)
  verdict holds for naive dedup, grok's length carve-out is the safe subset).
  w11/w12 add fable's Tier-2 metadata coincidence (lazy-attacker kills,
  12/12 honest).
- **Tier 3 (HL-11..HL-13, temporal/provenance):** w3 builds out HL-13
  (detection-only, honest about being a cost-raiser). w6 is the age tax,
  downgraded per WALL-RED's negative measurement. g6 is the registry oracle
  for closed classes. Grok #2 (dual-track PROVISIONAL/ASSERTED) and #3
  (claim-age on pinned crawl) are **unprobeable on these fixtures**
  (META=NONE everywhere; inventing timestamps would be fabrication) — the
  fixture extension they need is specified in §8. Grok himself demoted #2
  below #4 ("latency tax that misses the residual").

## 3. Grok × Fable cross-check (disagreements probed first)

| Question | Grok | Fable | Measured here |
|---|---|---|---|
| Archived rival-filler (grok #1) | kills F1/F4 for the impatient class | no equivalent; ceiling assumes no external feeds | **g1: F1 ARCHVETO, 12/12 honest, T4 passes via era-split** — grok's claim holds *inside* a pinned class; fable's ceiling is about the no-feed world, so no true contradiction |
| HL-10 replacement (grok #7 vs fable bucket-c) | length-gated collapse avoids H8 | HL-10 works but costs H8, resolvable only where the bar forbids | **Both right**: ch2b (naive) regresses H8 exactly as fable says; g7 (≥25-token gate) kills the long ring with 12/12 — grok's carve-out is the shippable subset |
| Corroborated contradiction (grok #4) | proposed; "re-run the 38, if more than a couple were single negations it's too expensive" | killed W5 (different mechanism — LLM contradiction graph) | **g4: 5 flips, rejected** — grok's own bar kills it |
| NS-apex (fable W11) | not evaluated | KEEP Tier 2, §7 falsification case | **w11: naive blocked / hardened evades / honest intact** — falsification pattern reproduced exactly |
| Age gates (grok #3/#5 vs fable W6) | useful as F-battery items; "prepaid pipeline" | KEEP but measure honest-publisher FN; taxes steer attackers to S2/S4 | **WALL-RED measured the negative** (walltemp.zag): burst gates collide with honest breaking news; age passes W_S3, flags H_H1 — downgraded to tax-only |
| R4 wire-echo | steelman holds | **reframing: R4 INSTALL is correct behavior**, upstream error | Adopted — R4 is out of scope for the wall-hop; target is M3-hardened-astroturf |
| §7 status | steelman holds except pinned-history + ranker-independent candidate set | valid within assumptions, not airtight; cheapest break = WHOIS+NS in observation set | **WALL-RED probe 1 measured the shape-identity** (W_R3 ≡ H_H1 on verdict-visible vector); cracks 1/2/5 measured as map expansions |

## 4. WALL-RED fold-in (independently verified where marked)

- **Crack 1 (functional-slot dissent, 10/10 on walldissent.zag):** consistent
  with g1's ARCHVETO on `F1_sydney`; division of labor (numeric/negation defer
  to HL-4) respected — g1 fires only on closed-class templates and passes
  everything else through.
- **Crack 2 (candidate-set expansion, wallsel.zag hidden_dissent=1):**
  **independently reproduced** in `sel_results.tsv`: `X_SATUR1_crowdout`
  top-3 → INSTALL (Crew B's production failure, byte for byte), expanded →
  WITHHOLD|CONTRADICTION; same split on `C_numD_dissent`; `H8_wire_truth`
  INSTALL under both (honest control: expansion finds nothing hidden, no
  false positive). M3-as-ranking is partly a selection bug.
- **Crack 3 (operator coincidence):** w11/w12/w3 reproduce wallmeta.zag's
  pattern (naive overlap=3 BLOCK, hardened 0 evades, honest 0 intact).
- **Crack 4 (temporal = tax, negative):** adopted — w6 downgraded; true
  breaking news permanently forbids promoting age to a truth signal.
- **Crack 5 (archived rival-filler veto):** **measured here** (WALL-RED
  flagged it highest-value unmeasured): g1 + `pins/pin1.txt` kills F1;
  `pins/pin2.txt` (era-split roll) lets T4 through; T4+stale-pin1 →
  WITHHOLD|ARCHVETO (the pin-discipline cost, quantified).
- **Remnant:** `F_M3_HARDENED` INSTALL under all 15 mechanisms = WALL-RED's
  A5/W_S3 (patient diversified false consensus, no prior conflicting filler)
  — no layer closes it. S1 entrenched consensus and R4-as-correct-behavior
  accepted as limits.

## 5. What the ranking recommends building

1. **ch1 + ch2** — cheapest kills per LOC, zero honest regression (2/20 new
   kills on the original battery).
2. **Candidate-set expansion past the selection cut** when the verdict-visible
   quorum is unanimous — the single highest-leverage change; it converts two
   production failures into withholds without touching the verdict predicate.
   Bound the expansion (one tier / pinned set) or selection becomes unbounded.
3. **g1** for pinned closed classes (capitals, officeholders, atomic
   numbers…), with era-split pins and a governed roll process — plus **g6**
   where a real registry oracle exists.
4. **w11 + w12** (Tier 2, cheap), **w3** as detection-only — honest
   cost-raisers, priced at ~$10→~$100 attacker cost, never sold as a seal.
5. **g7** narrowly for the long-sentence ring subclass; **w6** as a delay
   signal only.

## 6. Residuals (explicit)

- **A5/W_S3** patient diversified false consensus with no prior conflicting
  filler: no probed layer closes it. This is the genuine wall remnant.
- **A6/S1** entrenched false consensus outside any pinned oracle: accepted as
  limit (fable, grok, WALL-RED converge).
- **R3** compromised legitimate sites inside a time window: unfixable without
  breach-intelligence feeds.
- **R4** wire echo of falsehoods: INSTALL is correct mechanism behavior; fix
  belongs upstream (wire-service adjudication), outside KB-layer scope.
- **S2** uncorrected vandalism inside the window: grok #2 addresses it, but
  unprobeable on static fixtures; needs the F3/T2 correction fixtures.
- **S4** additive compromise with no rival filler and no retraction: invisible
  to content corroboration; archive absence is not evidence.

## 7. Caveats that must ship with g1 (grok's warnings, now measured)

1. **Pin discipline is the trust relocation.** Live archive APIs are not
   replayable — "just check Wayback" inside the decision path kills
   byte-identical reruns. The pin must be content-addressed and versioned;
   a stale pin freezes legitimate supersession (measured: T4 + pin1 →
   WITHHOLD|ARCHVETO). Whoever rolls the pin is now the integrity mechanism —
   staff it or don't ship it.
2. **Era-split or freeze.** T4 (capital moves, rename, revision) is not a
   corner — without era modeling, rank 1 either freezes the past or needs a
   maintenance process as fallible as the original problem. Measured: pin2's
   era-2 record lets T4 through; the rule is only as good as the roll.
3. **Closed-class scoping.** g1 fires only on the frozen template inventory
   (capital-of, closest-planet-to, …). Parser-gap neighbors of any pinned
   oracle fall back to the residual — grok's point 5 of the impossibility
   list. Keep the inventory small and frozen; over-broad parsing risks false
   dissent on idioms (WALL-RED crack 1's regression surface).
4. **Impatient-only.** A patient attacker who pre-dates the archive (S3-shape)
   beats g1. The value is forcing attackers into the much harder S3 game.

## 8. Fixture extensions needed (not built — specified, not faked)

- **F3/T2 correction fixtures** (vandalism + revert with timestamps) for
  grok #2 dual-track — needs temporal metadata the frozen fixtures lack.
- **Honest-publisher age distribution** (fable W6's FN measurement) — w6 is
  fail-open on missing `AGE_DAYS`; the breaking-news collision is measured
  by WALL-RED, the publisher-age distribution is not.
- **W_S3 patient fixture** (369-day diversified false history, no archived
  rival) — the remnant's canonical test; WALL-RED built one, we did not
  re-fixture it here.
- **H_BREAK honest breaking-news burst** — the permanent control against
  promoting any temporal signal to truth.

## 9. Reproduction

```
cd ~/workspace/liharden/beyond/work
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 beyond.zag -o beyond_bin
python3 run_beyond.py > results.tsv   # 39 cases x 15 mechs x 2 reps; asserts determinism
python3 sel_test.py                   # selection-layer experiment + stale-pin control
```

Determinism: the driver asserts rep1 == rep2 byte-identical for all 585
configurations and aborts on any mismatch. No randomness anywhere in the
probe or the fixtures.

## 10. Files

- `beyond.zag` — probe source (base + 14 mechanisms)
- `run_beyond.py`, `sel_test.py` — drivers
- `results3.tsv` — full battery; `sel_results.tsv` — selection experiment
- `fixtures/` — 7 new fixtures (F1_sydney, T4_supersede, F7_longring,
  T5_longwire, F_M3_NAIVE, F_M3_HARDENED, F_H_WIRE)
- `pins/` — pin1.txt (frozen pre-attack), pin2.txt (era-split roll),
  registry.txt, registry2.txt
