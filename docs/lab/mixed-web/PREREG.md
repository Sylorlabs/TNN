# MIXED-WEB — preregistration (FROZEN 2026-09-21)

Micah's question (2026-09-21): "when the web gives mixed results, can it use
logic to find the truth?" The info-source trial proved search buys falsehood
detection (12/12 caught, 0/12 installed) and the new-mechanisms trial proved
2v1 conflicts resolve 36/36 — but neither tested the real case: LIVE search
returning GENUINELY MIXED results (sources disagreeing with each other), where
the TNN must use logic to converge on truth, not just withhold.

This prereg is frozen BEFORE any recording. Derivation rules (§3–§5) are
frozen; their outputs (classes, golds, expectations) are set pre-score from
the frozen envelopes, exactly like the info-source trial. Any change to the
rules below needs a dated amendment.

## 1. Arms

Same evidence in both arms: frozen live SearXNG envelopes (lumy primary,
proven transport from search v2). The ONLY difference is the decision logic.

| Arm | Logic | Provenance |
|---|---|---|
| A (baseline) | withhold-only: the v2 sense decide, verbatim — PROVISIONAL iff ≥2 domains agree and all agree; PROVISIONAL_MAJORITY iff ≥2 agree with disagreement; WITHHOLD otherwise. No recency, no independence counting. | `ws2_sense.zag` reused verbatim (mode 1, read-only) |
| B (deliberation) | conflict-driven deliberation with logic rules (§4): majority-of-independent-domains, recency (temporal questions), corroboration count; withhold on ties/insufficient/stale-conflict. Every verdict carries a complete ledger reasoning chain. | new `mw_sense.zag` (pure Zag, zero RNG) |

## 2. Questions (record 23, keep those with verified genuine disagreement)

Format: id, query string, question text, candidates (regex → canonical, frozen
order = match priority), temporal flag.

Non-temporal:
- M01 "oldest university in the world" — `university of bologna`→University of Bologna; `al[ -]?qarawiyyin`→Al-Qarawiyyin; `nalanda`→Nalanda
- M02 "inventor of the telephone" — `alexander graham bell|graham bell`→Alexander Graham Bell; `antonio meucci|meucci`→Antonio Meucci; `elisha gray`→Elisha Gray
- M03 "who discovered America" — `christopher columbus|columbus`→Christopher Columbus; `leif erikson|erikson`→Leif Erikson; `amerigo vespucci|vespucci`→Amerigo Vespucci
- M04 "how many countries are in Africa" — `\b54 countries\b`→54; `\b55 countries\b`→55; `\b56 countries\b`→56
- M05 "largest desert in the world" — `antarc\w*`→Antarctic; `\bsahara\b`→Sahara; `\barctic\b`→Arctic
- M06 "longest river in the world" — `\bnile\b`→Nile; `\bamazon\b`→Amazon; `\byangtze\b`→Yangtze
- M07 "largest lake in the world" — `caspian sea`→Caspian Sea; `lake superior`→Lake Superior; `lake baikal`→Lake Baikal
- M08 "tallest mountain in the world" — `mount everest|everest`→Mount Everest; `mauna kea`→Mauna Kea; `\bk2\b`→K2
- M09 "who wrote the first novel in history" — `murasaki`→Murasaki; `cervantes`→Cervantes
- M10 "oldest civilization in the world" — `mesopotamia`→Mesopotamia; `\begypt\b`→Egypt; `indus valley`→Indus Valley
- M11 "most spoken language in the world" — `\benglish\b`→English; `mandarin`→Mandarin; `\bspanish\b`→Spanish
- M12 "who invented the light bulb" — `\bedison\b`→Edison; `\bswan\b`→Swan; `\bdavy\b`→Davy
- M13 "most populous city in the world" — `\btokyo\b`→Tokyo; `\bdelhi\b`→Delhi; `\bshanghai\b`→Shanghai
- M14 "oldest city in the world" — `\bdamascus\b`→Damascus; `\bjericho\b`→Jericho; `\baleppo\b`→Aleppo
- M15 "largest economy in the world by nominal GDP" — `united states`→United States; `\bchina\b`→China; `\bjapan\b`→Japan
- M16 "which country has the most natural lakes in the world" — `\bcanada\b`→Canada; `\brussia\b`→Russia; `\bfinland\b`→Finland
- M17 "fastest animal in the world" — `peregrine falcon`→Peregrine falcon; `\bcheetah\b`→Cheetah; `\bsailfish\b`→Sailfish

Temporal (temporal=1):
- R01 "tallest completed building in the world" — `burj khalifa`→Burj Khalifa; `jeddah tower`→Jeddah Tower; `merdeka 118`→Merdeka 118
- R02 "largest country in the world by population" — `\bindia\b`→India; `\bchina\b`→China
- R03 "reigning FIFA World Cup champions" — `\bargentina\b`→Argentina; `\bspain\b`→Spain; `\bfrance\b`→France; `\bbrazil\b`→Brazil
- R04 "president of the United States" — `donald trump|trump`→Donald Trump; `joe biden|biden`→Joe Biden
- R05 "prime minister of the United Kingdom" — `keir starmer|starmer`→Keir Starmer; `rishi sunak|sunak`→Rishi Sunak
- R06 "richest person in the world" — `elon musk|musk`→Elon Musk; `jeff bezos|bezos`→Jeff Bezos; `bernard arnault|arnault`→Bernard Arnault

## 3. Recording (frozen rules)

- One live query per question via `ws_bridge2.py --backend lumy` (record-once).
- Envelope frozen to `live/<qid>.json`. If a query yields zero usable results
  → shortfall: question dropped, documented.
- Answer extraction (mechanical, in the generator): for each result, scan
  `title + " " + snippet` (lowercased) against the question's candidate
  regexes IN FROZEN ORDER; the first regex that matches assigns that
  candidate's canonical answer. No match → relevance 0 (logged to
  `runs/discovery.log`, not fed to the TNN).
- Recency extraction (mechanical): `recency = max(all \b(19\d{2}|20\d{2})\b in
  title+snippet)`, else 0.
- Cap: first 10 usable results per question fed (deterministic order = bridge rank).

## 4. Deliberation rules — arm B (frozen)

Per question, from the relevant results: dedup on (domain, answer); build the
candidate table in FIRST-SEEN order: answer → {distinct-domain count, recency =
max over its results}. Let best = first-seen candidate with strictly greatest
count; rc = greatest count among the rest; tot = distinct relevant domains.

Rules fire in order; the FIRST that fires decides. Rule codes are ledgered.

1. **RECENCY** (temporal questions only): newest = first-seen candidate with
   max recency. Fires iff rec(newest) ≥ 2000 AND count(newest) ≥ 2 AND
   (rec(newest) − rec(second-newest)) ≥ 3.
   - If newest == best → CONVERGE(newest, RECENCY).
   - Elif count(best) ≥ 2 × count(newest) → WITHHOLD(STALE_CONFLICT): the
     evidence genuinely conflicts (stale majority vs recent minority).
   - Else → CONVERGE(newest, RECENCY) (recency takes precedence on temporal
     questions; documented assumption).
2. **MAJORITY**: count(best) ≥ 3 AND count(best) ≥ 2 × rc → CONVERGE(best, MAJORITY).
3. **CORROB**: count(best) ≥ 2 AND tot ≤ 4 AND rc ≤ 1 → CONVERGE(best, CORROB).
4. Otherwise → WITHHOLD(rule = TIE if rc ≥ 1 else INSUFFICIENT).

Ledger chain (op 'D', hash-chained): every candidate with its count and
recency, the fired rule code, the chosen answer (or WITHHOLD), and up to 3
supporting distinct domains. A verdict without a complete chain trips
KB-MW-LEDGER.

## 5. Classes, golds, expectations (set pre-score from frozen envelopes)

- **Keep/drop** (inspection gate, documented per question): keep iff ≥2
  relevant results AND ≥2 distinct candidates each asserted by ≥1 domain
  (genuine disagreement verified by reading the envelope). Dropped questions
  are listed with cause; they are not scored.
- **Gold**: for each kept question, the factually correct answer AS BEST
  DETERMINED FROM THE EVIDENCE (one-line justification per question in the
  verdict). If the evidence is genuinely 50/50 and no determination is
  possible → gold = UNDETERMINABLE.
- **Expected** (mechanical, from §4 rules on the frozen envelopes):
  CONVERGE(answer) or WITHHOLD. Class: C (MAJORITY/CORROB fired),
  R (RECENCY fired), W (WITHHOLD fired).
- The generator emits expectations; the independent oracle (`verify_mw.py`)
  recomputes everything from the envelopes. They must agree.

## 6. Kill bars (applied mechanically by the oracle)

- **KB-MW-WRONG**: arm B CONVERGEs on an answer ≠ gold (on questions with a
  determined gold) even once → FAIL. This is the bar for "can logic find the
  truth".
- **KB-MW-GUESS**: arm B fails to WITHHOLD on any UNDETERMINABLE-gold
  question → FAIL.
- **KB-MW-LEDGER**: any arm-B verdict lacking a complete ledger reasoning
  chain (valid rule code; chain lists every oracle candidate with matching
  counts/recencies; chosen consistent with the rule) → FAIL.
- **KB-MW-DET**: N=5 full-output runs per arm must be byte-identical, else
  that arm FAILs on procedure.
- **Coverage**: <16 scored questions → UNDERPOWERED (reported, not a kill).

## 7. Decision rule (headline)

VALUE-CONFIRMED iff ≥4 questions where arm B's verdict == expected AND arm A's
verdict ≠ expected (A withholds where B converges, or A converges on the stale
/wrong answer). Report the full head-to-head table: per question, gold,
expected, A verdict, B verdict, B rule.

## 8. Constraints

Pure Zag, zero RNG in any decision path, byte-identical reruns. No single
slice over 2^25 (trivially satisfied). Real mechanisms, not stubs: the
deliberation logic must actually decide. Determinism is claimed over the
frozen envelopes (record-once, replay N=5 — same convention as search v2 and
info-source).

## 9. Files

- `PREREG.md` (this file, frozen)
- `record_mw.py` (live recorder) · `gen_mw.py` (envelope → `src/mw_cases.zag` + expectations)
- `src/mw_sense.zag` (arm-B deliberation) · `src/mw_trial.zag` (driver, argv a|b|all)
- `src/ws2_sense.zag` + `src/R33_*.zag` (arm-A baseline, reused verbatim from info-source)
- `verify_mw.py` (independent oracle) · `live/*.json` (frozen envelopes)
- `runs/*.log` (10 run logs) · `runs/CASE_MANIFEST.txt` · `runs/discovery.log`
- `SHA256SUMS` · `VERDICT.md`

## 10. Amendments

### 2026-09-21 — A1 / arm-A evidence window (pre-record)

The reused v2 sense (`ws2_sense.zag`) stores at most 6 distinct
(domain,answer) pairs per question (frozen v2 `WsV` layout); further results
are silently dropped by `ws_add_result`. Arm B (`mw_sense.zag`) holds 10.
Both arms are therefore FED the same first-10 usable results (§3 cap
unchanged), but arm A mechanically considers only the first 6 distinct
(domain,answer) pairs — frozen v2 behavior, not a trial choice. The
independent oracle replicates this cap in its arm-A recomputation. This is a
documented arm difference, not a bar change.

### 2026-09-21 — A2 / six added questions (pre-record)

The §2 battery recorded 23 questions; the inspection gate kept 14 with
genuine disagreement — below the §6 coverage bar of 16. Six further
genuinely-disputed questions are added (same frozen rules apply to them;
they are recorded after this amendment, inspected identically):

- M18 "who invented the World Wide Web" — `tim berners|berners-lee|berners lee`→Tim Berners-Lee; `vint cerf|cerf`→Vint Cerf; `robert kahn|kahn`→Robert Kahn
- M19 "who invented the airplane" — `wright brothers|wright`→Wright brothers; `santos.dumont|santos dumont`→Santos-Dumont
- M20 "what is the tallest waterfall in the world" — `angel falls`→Angel Falls; `tugela falls`→Tugela Falls; `kaieteur`→Kaieteur Falls
- M21 "what is the oldest language in the world" — `\btamil\b`→Tamil; `sanskrit`→Sanskrit; `sumerian`→Sumerian
- M22 "what was the first video game" — `\bpong\b`→Pong; `spacewar`→Spacewar!; `tennis for two`→Tennis for Two
- M23 "what is the largest pyramid in the world" — `cholula`→Great Pyramid of Cholula; `giza`→Great Pyramid of Giza
