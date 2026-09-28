# LI-HARDEN Crew B — CORROB-1 Verdict Report

Date: 2026-09-24. Branch: `tnn-native-lab`. Toolchain: pinned
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Binary SHA256: `8bbe4b2a359921bdfee88a7e281ba4ec527d9dea02ba9ee2e4f434368e17d32b`
(source: `corrob.zag`, pure Zag; Python used only for fixture generation,
drivers, and analysis — no Python in any decision path).

Frozen prereg: `knowledge/web_guides/live_ingest/harden/PREREG_LI_HARDEN_CORROB.md`
(committed `22901790f1605dde570c1a29ad3211ebd6f814e5` BEFORE any mechanism code
was written). The prereg was not amended after freezing. Consult-extension cases
(grok-4.7 + claude-fable-5.1, received after the freeze) were run as a clearly
labeled extension battery; outcomes are reported against the frozen mechanism,
not fitted to it.

Frozen `knowledge/web_guides/webg.zag` SHA verified before and after all work:
`3c5df800a3221bd29488ee9f6b12f0425b187093cfc26d69fb57a9cfcbbfe464`
(unchanged; never modified).

## 1. Mechanism designs

### CORROB-1 (frozen, `corrob verdict`)
Pure-Zag corroboration gate replacing the webg verdict step. Inputs: the real
driver-produced `pages.txt` (`P|pid|title`, `H|host`, metadata lines ignored,
`S|sentence`) and the query string. Steps, all deterministic, zero RNG:

1. Parse pages; select each page's candidate sentence with the frozen
   `best_for_page` query-overlap semantics (byte-identical port of webg).
2. Sort pages lexicographically by pid (canonical order) before ALL downstream
   work — retrieval order cannot influence any output.
3. Contradiction scan over every pair of non-empty candidates:
   - **C1 explicit negation**: contraction expansion (`isn't`→`is not`, …),
     then token-multiset symmetric difference of exactly one token in
     {not, never, no}.
   - **C2 numeric conflict**: non-numeric frames compared after dropping range
     connectors (`to/and/between/from`) adjacent to numbers; equal frames with
     unequal numeric multisets (leading-zero-insensitive) = contradiction.
   - Competing proper nouns / superlatives (Sydney/Canberra, Venus/Mercury)
     deliberately OUT of scope (unsound to adjudicate at token level).
4. Any contradiction → `ANSWER|UNCHECKABLE` + `GATE|CONTRADICTION|<pids>`
   regardless of majority. No 2v1 (or 3v2) majority can install over a visible
   contradiction.
5. Otherwise exact normalized-sentence clustering (byte equality; paraphrases
   do not cluster). Winner = largest cluster, tie → canonical-first.
   (Measurement note: under frozen SELECT-N=3 a true tie cannot reach the
   verdict layer — 3 opened pages give 2v1, 1v1v1, or unanimous — so the
   tie-break is dead code in practice.)
6. Install requires winning cluster ≥2 pages AND ≥2 distinct non-empty hosts.
   Empty hosts fail closed (never count toward quorum).
7. Diversity signals are report-only: `INFO|DIVERSITY|pages=|hosts=|titles=|
   shared_filler_max=`.
8. Output: `INFO|CANON|<pid order>`, `ANSWER|`, `CLAIM|1|<claim>|<pids>`,
   `PROV|1|<pid>` lines, or `ANSWER|UNCHECKABLE` + `GATE|`.

### CORROB-1D (experimental, `corrob verdictd`)
CORROB-1 plus: reads the non-opened result snippets (`R|pid|title|snippet`)
and tests each non-opened snippet against the winning claim with C1/C2.
A firing dissent → `ANSWER|UNCHECKABLE` + `GATE|DISSENT|<pid>`. Preregistered
expectation: catches numeric dissent crowded out by SELECT-N=3, not
proper-noun dissent.

### CORROB-1M (experimental, `corrob verdictm`)
CORROB-1 plus grok-G5 mirror dedup: pages are grouped by byte-identical
normalized sentence-body (all `S|` sentences; title excluded so trivial title
variation does not defeat it); each body-group contributes ONE vote
(canonical-first page). Fewer than 2 surviving groups → quorum fail.

## 2. Battery

- 38 prior red-team cases (frozen fixtures, real driver teach/query/select via
  frozen `bin_webg_bf1`; verdict step swapped for corrob).
- 12 honest fixtures H1–H12 (multi-host truth must install).
- 11 contradiction/paraphrase fixtures (C_neg1/2, C_num1/2/3, C_numD, P1).
- 13 consult-extension fixtures X_* (post-prereg; see §4).
- 3 modes × 2 reps = 420 runs. **210/210 case×mode pairs byte-identical
  across reps** (verdict-output SHA). Zero RNG in any decision path.
- Order permutations (H1, C_num1, X_COMP1, R2, reversed `order.txt`):
  4/4 byte-identical ANSWER/GATE/CLAIM/PROV lines. Retrieval-order
  independence confirmed.
- Driver bug found and fixed mid-battery: the state dir was shared across
  parallel modes, racing `teach` writes (2/210 apparent nondeterminisms, both
  traced to the race, both in webg select input, never in corrob output).
  Fixed by per-mode state dirs; full rerun is the reported evidence. (The
  original red-team battery shares the same pattern; its logs may carry the
  same race noise.)

## 3. Results

### 3a. 38 red-team cases: 23 → 5 false installs (18 killed)

| case | prior BF1 | CORROB-1 | gate |
|---|---|---|---|
| E_DM2, E_LD2, E_NM2, E_TS2 | false install | WITHHOLD | CONTRADICTION |
| G1–G6, G9 (glue/host attacks) | false install | WITHHOLD | CONTRADICTION |
| M1 (outnumbered 2v1) | false install | WITHHOLD | CONTRADICTION |
| M2a / M2b (2v2, both orders) | FI / false install | WITHHOLD / WITHHOLD | CONTRADICTION (identical) |
| P3 (case variant) | false install | WITHHOLD | CONTRADICTION |
| R2 (ring, numeric) | false install | WITHHOLD | CONTRADICTION |
| S1, S2, S3 (subdomain sybils) | false install | WITHHOLD | CONTRADICTION |
| E_LD3, E_TS3, M3, R3, R4 | false install | **FALSE INSTALL** | (unanimous opened) |
| all others | — | no change | — |

K1 kill bar: 18 of 23 prior false installs flip to withhold. The 5 survivors
are ALL unanimous-false among opened pages (honest dissent crowded out by
SELECT-N=3): R3/R4 (Sydney/Canberra, Venus/Mercury proper-noun rings),
E_LD3/E_TS3 (diversified-metadata evasions), M3 (3 plants rank first).

### 3b. Honest throughput: 12/12 under CORROB-1 and CORROB-1D; 11/12 under 1M

H1–H12 all install under `verdict` and `verdictd`, including H4 (2 exact +
honest paraphrase), H5 (range-format variant `100-150` does not false-fire
C2), H10 (punctuation variant clusters). Under `verdictm`, H8 (4-host
byte-identical wire truth) withholds — the exact trade-off grok-4.7 predicted:
mirror-dedup and honest syndicated truth pull opposite ways; you cannot keep
both for syndicated text.

### 3c. Paraphrase defense preserved
R2P ring: withheld (CONTRADICTION). P1 (7 distinct rewordings of a false
claim): no 2-cluster → withheld (QUORUM). 0 installs from paraphrase
variants; exact-match quorum still requires byte-identical normalized
assertions.

### 3d. Contradiction fixtures
C_neg1, C_neg2 (contraction), C_num1, C_num2 (mixed 2v1), C_num3 (2v2):
all `GATE|CONTRADICTION`. C_numD (honest 4th page): installs under `verdict`
(by design — dissent not opened), withholds under `verdictd`
(`GATE|DISSENT`). `verdictd` additionally kills M3 and X_SATUR1 (numeric
dissent in snippets); it cannot kill R3/R4/E_LD3/E_TS3 (proper-noun dissent,
out of C1/C2 scope) — exactly the preregistered expectation.

## 4. Consult-extension battery (post-prereg; 13 attacks)

| # | consult attack | X-case | verdict | verdictd | verdictm | disposition |
|---|---|---|---|---|---|---|
| 1 | syndication/wire echo | X_WIRE1 | INSTALL | INSTALL | INSTALL | SURVIVES — wall |
| 2 | mirror multiplication | X_MIRROR1 | INSTALL | INSTALL | WITHHOLD | killed by 1M only |
| 3 | boilerplate injection | X_BOILER1 | INSTALL | INSTALL | INSTALL | SURVIVES — needs corpus DF |
| 4 | negation/quote strip | X_QUOTE1 | INSTALL | INSTALL | INSTALL | SURVIVES — needs polarity-aware extraction (G9) |
| 5 | normalization collision | X_NORM1 | WITHHOLD | WITHHOLD | WITHHOLD | KILLED — conservative normalization holds (no NFKC) |
| 6 | high-DF sentence | X_HIGHDF1 | INSTALL | INSTALL | INSTALL | SURVIVES — query/claim scope gap, out of layer |
| 7 | tie/order poison | M2a/M2b + 4 perms | WITHHOLD | WITHHOLD | WITHHOLD | KILLED — canonical order + contradiction; perms 4/4 identical |
| 8 | context drop | X_CTX1 | INSTALL | INSTALL | INSTALL | SURVIVES — scope gap |
| 9 | hidden-text channel | — | n/a | n/a | n/a | no verdict-layer fixture possible; extractor-layer (recommend G6 main-text-only) |
| 10 | feed vs page double count | X_FEED1 | INSTALL | INSTALL | INSTALL | SURVIVES — same-operator, A9-class |
| 11 | install-once race / claim TTL | — | n/a | n/a | n/a | post-install KB lifecycle; recommend fable-G4 claim TTL at KB layer |
| 12 | pre-bunking saturation | X_SATUR1 | INSTALL | WITHHOLD | INSTALL | killed by 1D (DISSENT); X_SATUR1b (honest opened) killed by all |
| 13 | temporal sandwiching | X_SAND1 | INSTALL | INSTALL | WITHHOLD* | *1M kill is incidental (identical filler in fixture); time is invisible at verdict layer — needs temporal provenance |
| 14 | wikipedia mirror farm | X_WIKI1 | INSTALL | INSTALL | WITHHOLD | killed by 1M only |
| 15 | cloak on fixed UA | — | n/a | n/a | n/a | retrieval-layer; recommend grok-G12 second fetch profile |
| 16 | compromised legitimate sites | X_COMP1 | INSTALL | INSTALL | INSTALL | SURVIVES — both models agree UNFIXABLE at this layer |
| — | platform sybils / CDN / IP literals / redirect swap / parser split / scheme twins / URL-param spoof / dangling host / confusables / cert rotation / DoH / split-horizon DNS | — | n/a | n/a | n/a | Crew A (glue) / network-layer domain; classified out of corroboration scope |

Frozen select already title-dedups identical-title mirrors (found during
testing: X_MIRROR1/X_WIKI1/H8 needed distinct titles to reach the verdict
layer) — a partial pre-existing defense; title-varied mirrors sail through
to the verdict layer, where only 1M stops them.

## 5. A9 verdict: DENTED, but SURVIVES as a wall — stated plainly

A9 (the attack where genuinely multiple hosts assert the same false claim)
survives. CORROB-1 + 1D + 1M kill every *detectable* coordination shape:
contradictory majorities (18/23 prior false installs), crowded-out numeric
dissent (1D), byte-identical mirror farms (1M, at the cost of honest wire
truth). What remains is *unanimous false agreement among sources the layer
cannot distinguish from true consensus*:

- **Wire echo** (X_WIRE1): 5 distinct real-looking eTLD+1s, diverse filler,
  byte-identical false sentence. Diversity metrics are IDENTICAL to honest
  fixtures (pages=3|hosts=3|titles=3|shared_filler_max=0 matches H1/H2/H3/H9
  exactly). No threshold on page/host/title/filler signals separates rings
  from honest truth — measured, not hypothesized.
- **Compromised legitimate sites** (X_COMP1): both consult models agree this
  is unfixable at the corroboration layer — and fable-5.1 adds it is *correct*
  behavior under a 2-source design: two genuinely independent trusted sites
  agreeing SHOULD install.
- **Diversified proper-noun rings** (E_LD3/E_TS3): metadata diversified by
  design, proper-noun claims outside C1/C2, honest page crowded out.

**Cheapest provenance signal that WOULD fix the fixable remainder:**
shared non-host operator coincidence across the quorum — identical
author/CMS/link-target/timestamp (the `A/CG/L/T` metadata the driver already
emits). Measured: this signal is present on the R3/R4/M3 quorums and would
withhold all three; it is absent (META=NONE or diversified) on every honest
install and on E_LD3/E_TS3 (which diversified it away — the expected attacker
adaptation, escalating to trust tiers). Cost is ~50 lines at the verdict
layer — BUT it requires the metadata pipeline the production glue was
explicitly forbidden to emit (E_NM2 lesson), so it is a pipeline decision,
not a verdict-layer patch, and it was NOT implemented (frozen prereg; would
also need its own red-team against metadata forgery). Beyond that signal,
the wall is structural: no host/text/metadata heuristic at this layer
distinguishes wire echo or compromised sites from true consensus. The fixes
that remain are trust tiers / publisher reputation (fable G5), claim TTL +
revalidation (fable G4), and human adjudication — all above this layer.

## 6. Prereg deviations (honest accounting)

1. **K7 arithmetic error (frozen, not amended):** K7 text says "11 expected
   residuals" but names 13 (S1–S3=3, G1–G6=6, R3/R4/E_TS3/E_LD3=4).
2. **S/G expectations were wrong:** prereg expected S1–S3, G1–G6 to still
   false-install as glue residuals. Observed: ALL withhold — the opened sets
   include an honest numerically-contradicting page, so C2 fires despite
   broken host parsing. The mechanism is stronger than preregistered here.
3. **Residual list:** observed CORROB-1 residuals are E_LD3, E_TS3, M3, R3,
   R4 (5). M3 (crowding shape) was not in K7's list; S1–S3/G1–G6 dropped out.
4. **Paraphrase figure:** prereg cited historical "6/7 withheld"; measured now:
   all paraphrase variants withheld, 0 installs (R2P via CONTRADICTION, P1
   7/7 via no-cluster QUORUM).
5. **K4 M3 expectation** ("INSTALL (3v2 majority…)") confirmed: opens
   q1,q2,q3 unanimous → INSTALL; killed only by 1D dissent.
6. Prereg heading date says 2026-09-23; work ran 2026-09-24. Artifact
   preserved as committed.

## 7. Kill-bar assessment

- "0 false installs with zero throughput regression": NOT MET in full —
  CORROB-1 gives 5/38 false installs (all unanimous-opened crowding/wire
  shapes) with 12/12 throughput. The 5 are characterized above; 3 fall to a
  (not-yet-pipelined) metadata-coincidence signal, 2 (wire echo,
  compromised/diversified rings) are structural wall.
- No regressions: every case the prior battery got right, CORROB-1 gets right;
  18 flips are all kills, 0 new misses.
- Determinism: 210/210 byte-identical reruns; 4/4 order permutations
  identical; zero RNG in any decision path.

## 8. Evidence and reproduction

- Source: `corrob.zag` (pure Zag, ~1090 lines) + pinned-toolchain binary
  (SHA256 `8bbe4b2a…e17d32b`).
- Battery: `run_corrob.py` (driver), `gen_fixtures.py`,
  `gen_consult_fixtures.py`, `run_battery.sh`, `analyze.py`, `analyze2.py`;
  32 fixtures; 420 run logs; `logs/battery_stdout.txt` summary lines.
- Evidence committed under
  `knowledge/web_guides/live_ingest/harden/corrob/` (source, fixtures,
  drivers, analysis scripts, per-case summary TSV, this report). The 420 raw
  logs (8.3MB) are summarized in `battery_summary.tsv`; representative raw
  logs included per gate class.
