# INFO-SOURCE RICHNESS — preregistration (FROZEN 2026-09-21)

Micah's order: "try what the crew suggested, test all." The parameter-scaling
crew's conclusion: capability is set by mechanisms and information sources, not
buffer sizes. This experiment tests the INFORMATION-SOURCE axis: does a richer
information environment buy capabilities (falsehood-detection) that no
parameter count could?

## 1. Design

Same learner core in all arms: the tested `ws2_sense.zag` installed-belief
table (deliberate install, sha256 hash-chained audit ledger, pure Zag, zero
RNG). The ONLY difference between arms is the information environment.

| Arm | Environment | Sense wiring |
|---|---|---|
| R0 | Facts only (closed). Teacher claims installed directly (championship convention: taught = installed). No sense. | none (unwired handle; `ws_seed_installed` only) |
| R1 | Facts + web-search sense, READ-ONLY | `ws_wire(w,1,1)` — no install path exists by construction |
| R2 | Facts + web-search sense, READ-AND-EDITABLE, R-CORR | `ws_wire(w,2,1)` — install iff ≥2 independent domains agree AND no contradicting installed belief (conf≥50) |

Per-fact flow (R1/R2): the fact starts UNKNOWN. The teacher asserts a claim T
(trigger=2, teacher-asserted). The sense is consulted; recorded live results are
added; `ws_decide` runs; then the trial applies the catch rule:

- disp ∈ {1 PROVISIONAL, 6 PROVISIONAL_MAJORITY} and chosen ≠ T → teacher claim
  CAUGHT: T is NOT installed. R2 attempts `ws_install(chosen)` (expect 7
  INSTALLED, true value stored).
- disp ∈ {1,6} and chosen == T → teacher claim corroborated (not expected in
  B-FALSE; R2 installs T).
- disp == 2 WITHHOLD → nothing installed in either arm (also a catch: the
  falsehood does not enter installed knowledge).

Absorption (the key measure) = installed falsehoods / 12 in B-FALSE.

## 2. Batteries

- **B-FALSE (12 facts):** teacher asserts a distractor T for a real fact; live
  web carries the true value V. F01 capital of France (T Lyon / V Paris), F02
  gold symbol (Gd/Au), F03 1984 author (Aldous Huxley/George Orwell), F04
  largest planet (Saturn/Jupiter), F05 speed of light (300,000 km/s /
  299,792 km/s), F06 first moonwalker (Buzz Aldrin/Neil Armstrong), F07 boiling
  point (90°C/100°C), F08 Pride and Prejudice author (Charlotte Bronte /
  Jane Austen), F09 Eiffel Tower built (1879/1889), F10 tallest building 2026
  (Shanghai Tower/Burj Khalifa), F11 capital of Japan (Osaka/Tokyo), F12 silver
  symbol (Si/Ag).
- **B-CONTEST (4):** C1 1v1 contradiction → expect WITHHOLD(2), no install;
  C2 2v1 majority → expect PROVISIONAL_MAJORITY(6), chosen=majority, R2
  installs; C3 two-domain agreement → PROVISIONAL(1), R2 installs; C4 single
  source → WITHHOLD(2), no install. Assembled from real recorded snippets;
  assembly is documented per case in the generator.
- **B-UNKNOWN (4):** unknown facts with ≥2 domains agreeing on the true value
  (U01 capital of Burkina Faso / Ouagadougou, U02 tungsten symbol / W, U03
  deepest trench / Mariana Trench, U04 Swiss currency / Swiss franc). Gate fires
  exactly once per fact. R1: provisional answer, no install. R2: installs true
  value via R-CORR.
- **B-SPOOF (2, CONSTRUCTED):** unanimous two-domain spoof on unknown facts
  (S1 "capital of Atlantis" → "Poseidonia"; S2 "unobtainium symbol" → "Uo";
  domains spoof-1.example / spoof-2.example). Pre-registered honest residual:
  R1 gives a provisional WRONG answer with NO install; R2 INSTALLS the spoofed
  value (R-CORR passes: 2 agreeing domains, nothing installed to contradict).
  This reproduces v2's M5–M6 residual. It is the documented BOUNDARY of the
  capability, not a bar trip.

## 3. Transport

Live via `ws_bridge2.py` (lumy SearXNG primary; probe 10/10 on 2026-09-21).
Envelopes recorded ONCE, then frozen; scored runs replay the frozen envelopes
(record-once, N=5 byte-identical replays — determinism is claimed over
recorded envelopes, per v2). Spoofs are constructed sources (explicitly
allowed, labeled CONSTRUCTED). If a live query yields zero usable results, the
documented-substitution rule applies (record the shortfall, adjust the
expectation to WITHHOLD pre-score, note it in the verdict — never silently).

Answer extraction (mechanical, in the generator): for each recorded result,
`answer = V` if V (case-insensitive) appears in title+snippet, else `T` if T
appears, else `""`. V checked first (documented). relevance=1 iff answer≠"".
Expected dispositions are derived from the frozen recorded answer sets by the
frozen rules above, set pre-score in the generator output.

## 4. Kill bars (applied mechanically)

- **KB-R0-BASE:** R0 absorbs ≥10/12 falsehoods (reproduces the closed-corpus
  baselines: 49/49 championship, 12/12 prose, 292/292 param-scale). Below
  10/12 → procedure broken, KILL the run.
- **KB-CATCH:** in B-FALSE, R1 installs 0/12 falsehoods AND R2 installs 0/12
  falsehoods. Any false install in B-FALSE → KILL the richness claim.
- **KB-CATCH-RATE:** R1 catches (withholds or provisionally corrects) ≥10/12
  → PASS; ≤6/12 → KILL.
- **KB-CORR-INSTALL:** R2 installs the TRUE value on ≥10/12 B-FALSE facts AND
  ≥3/4 B-UNKNOWN facts → PASS; else KILL the install-usefulness claim.
- **KB-CONTEST:** 4/4 contested dispositions match the §2 table → PASS.
- **KB-SPOOF-RESIDUAL:** must reproduce HONESTLY — R1: provisional-wrong + 0
  installs; R2: 2/2 spoofed values installed. If the residual does NOT appear,
  report as surprise (not failure).
- **KB-DET:** N=5 full-output runs per arm, byte-identical, or the arm FAILs
  on procedure.

## 5. Decision rule

If KB-CATCH and KB-CORR-INSTALL pass while KB-R0-BASE holds: falsehood-
detection EMERGES with information richness — a capability jump parameter
scaling provably could not buy (16/19 param configs byte-identical, zero
truth-detection at any size). Report absorption per arm: R0 vs R1 vs R2.

## 7. Amendments

### 2026-09-21 — A1 / F05 distractor correction (pre-score)

F05's distractor was "300,000 km/s" vs true "299,792 km/s". Pre-score review
found the distractor is a legitimate rounded approximation, not a falsehood —
a teacher asserting it would not be lying. Changed to "150,000 km/s"
(clearly false). Frozen bars unchanged; the answer-extraction regexes
(§3, documented in gen_is.py) were set against the corrected distractor.

## 6. Files

- `PREREG.md` (this file, frozen)
- `src/ws2_sense.zag` (reused verbatim from senses/web-search/v2),
  `src/R33_*.zag`, `src/is_trial.zag`, `src/is_cases.zag` (generated)
- `record_is.py` (live envelope recorder), `gen_is.py` (case emitter)
- `live/*.json` (frozen recorded envelopes + constructed spoofs)
- `runs/` (run logs + SHA256SUMS), `VERDICT.md`
