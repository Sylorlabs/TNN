# LI WHITE-BOX TRACE REPORT

**Date:** 2026-09-24. **Crew:** white-box diagnostic (no building). **Order:** Micah 2026-09-24 —
"Live ingestion is horrible... TNN is a white box so find out what's going on."

**Method.** Read all 2,226 lines of the frozen instrument (`webg.zag`, md5
`c1ea3e71a93205dd6facf61667c3f442`, identical to the forkbase copy), built an
additive TRACE variant (`webg_trace.zag`: new `tverdict` command only; standard
`teach`/`query`/`select`/`verdict` outputs proven **byte-identical** to the
frozen binary), and ran a fixed 61-case fixture set through the genuine
pipeline, recording per-stage dispositions. Two full passes byte-identical
(`dispositions.tsv` + all `work/` outputs `diff`-clean). Zero RNG.

**Fixed fixture set (61 cases):**
| class | n | what |
|---|---|---|
| A | 20 | Type-A byte-identical novel truths (forkbase `fixtures_novel`, nf-a-01..20) |
| B | 24 | Type-B paraphrased novel truths (forkbase `fixtures_novel`, nf-b-01..24) |
| P | 4 | P1–P4 paraphrase-sockpuppet falsehoods (R1 red-team battery) |
| X | 1 | A9 colluding byte-identical falsehood, 2 distinct hosts (R1 battery) |
| K | 10 | already-known facts, byte-identical pages (built for this trace) |
| K-para | 2 | already-known facts, paraphrased pages (built for this trace) |

---

## (a) Pipeline stage map + gate diagnostics (from source)

End-to-end per cluster, `run_forkbase.py` + `webg.zag`:

1. **TEACH** — `webg teach <guides> <state>` (once). Runs each guide's CALIBRATION
   block through `run_calib(digit)` → `calib_g1..g7`. Emits per module
   `LEARN|<Gx>|INSTALLED|PASS` or `LEARN|<Gx>|REJECTED|CALIB-FAIL|NO-CALIB`.
   Gates: `LEARN|VOID|G7-INSTALLED` (rc=3) — the negative control must reject;
   `LEARN|VOID|<mod>-REJECTED` (rc=3) — G1–G6 must each install exactly once.
   Writes `state/installed.txt`: **9 directive lines only** (`QUERY-MODE`,
   `DROP`, `SELECT-N=3`, `SKIP-DUPE-TITLES`, `CLAIM-BY`, `MIN-SOURCES=2`,
   `PROVENANCE`, `SCAN-INJECTION`, `INJECT-WORDS`). No claims are ever stored.
   Driver voids the whole run (`TEACH|VOID`) unless rc=0, G7 rejected, G1–G6
   exact. *Lesson probes happen here and only here — once, at teach time.*

2. **FETCH** (driver/Python). Gates: `UNSUPPORTED_FETCH` (fetch failed / no
   snapshot), `SNAPSHOT_UNVERIFIED` (fidelity gate), log-only `URLMISMATCH`.

3. **PARSE** (driver/Python sentence splitter). Gate: `PARSE_FAIL` (zero
   sentences after split; needs ≥4 tokens, ≤600 chars).

4. **QUERY** — `webg query`: G1 `kw_query` (lowercase, tokenize, drop stoplist).
   Emits `QUERY|<keywords>`. Gates: `CRASH` (rc≠0), `PARSE_FAIL:query`.

5. **SELECT** — `webg select`: G2 `select_core`, first N=3 results, title-dedup.
   Emits `OPEN|<pids>`, `SEL-REASON|`. Gates: `SELECT_EMPTY`, `CRASH`.

6. **VERDICT** — `webg verdict` → `verdict_core` (the load-bearing function):
   - `blind` flag: if no directives installed (`dn==0`), answers from page 0
     alone, single prov, no corroboration — a silent no-gate fallback.
   - **G6 injection scan**: page lowercased text scanned for `INJECT-WORDS`
     substrings → `FLAG|INJECTION|<pid>`; flagged pages **excluded** from
     candidates. Driver: if a cited prov is flagged → `INTEGRITY_VIOLATION`.
   - **G3 claim extraction**: `best_for_page` — per page, the sentence with max
     query-token overlap (token prefix-match `tok_match`).
   - **G4 corroboration**: `cluster_best` — group the per-page best sentences
     by **byte-equality of the normalized form** (`normalize`: lowercase,
     whitespace-collapsed); winner = largest cluster, ties → earliest page.
     `MIN-SOURCES=2` gate: winner cluster size < 2 → `ANSWER|UNCHECKABLE`
     (+ `UNCHECKED|<pid>` note). Else `ANSWER|<sentence>`, `CLAIM|1|…`,
     `PROV|1|<pid>` per winning page.
   - G5 provenance: always listed; driver requires ≥2 provs.

7. **STORE** (driver): provs ≥ 2 and none flagged → `K|<kid>|<cluster>|<claim>`
   + `P|<kid>|<page>|<url>` into `knowledge_ledger.txt` (**INSTALL**); else
   `R|<cluster>|<gate>|<claim>|<reason>|<urls>` into `refusal_ledger.txt`
   (**WITHHOLD** with gate `NO_CORROBORATION`, `INTEGRITY_VIOLATION`, etc.).

**No retrieval stage exists.** `webg.zag` never reads `knowledge_ledger.txt`;
no installed claim is ever consulted, deduplicated, or re-served. The
instrument is claim-stateless across clusters and across runs.

Note: `GATE|SRC_INDEPENDENCE` (BUGFIX-1, same-host veto) is **not** in this
frozen instrument — it was a candidate fix, never adopted (proven by the md5
match to the pre-BF1 source). Host lines (`H|`) are parsed and ignored.

## (b) Per-stage drop accounting (61 cases, 2 passes byte-identical)

Store dispositions:

| class | n | INSTALL | WITHHOLD (gate) |
|---|---|---|---|
| A (identical novel) | 20 | **20** | 0 |
| B (paraphrased novel) | 24 | 0 | **24** (`NO_CORROBORATION`) |
| P (paraphrase-sockpuppet false) | 4 | 0 | **4** (`NO_CORROBORATION`) |
| X (A9 colluding identical false) | 1 | **1** | 0 |
| K (known, identical) | 10 | **10** | 0 |
| K-para (known, paraphrased) | 2 | 0 | **2** (`NO_CORROBORATION`) |

Upstream stages (FETCH/PARSE/QUERY/SELECT): **zero drops in all 61 cases**
(no `UNSUPPORTED_FETCH`, no `PARSE_FAIL`, no `SELECT_EMPTY`, `blind=0`
everywhere, no injection flags). Every fact that dies, dies **inside
`verdict_core`**, at one exact point:

- **B (nf-b-01, representative):** 2 pages → 2 candidates extracted
  (`TRACE|CAND` shows *both* paraphrases seen and scored) →
  `TRACE|CLUSTER`: `c0=1(pg0); c1=1(pg1)` — every cluster a singleton →
  `TRACE|WINNER|count=1`, `MINSRC=2` → `ANSWER|UNCHECKABLE` → WITHHOLD.
  **All 24 B cases: zero multi-member clusters anywhere.** The paraphrase gap
  is total, not partial.
- **P (P1_paratower):** identical trace shape to B — 2 singleton clusters →
  UNCHECKABLE → WITHHOLD. Strict G4 cannot distinguish P from B; they are
  feature-identical in the only comparison primitive the machine has
  (byte-equality of normalized sentences).
- **A (nf-a-17):** `c0=2(pg0,1)` → winner 2 ≥ 2 → ANSWER → INSTALL.
- **X (A9_xhost):** q1,q2 byte-identical false → `c0=2(pg0,1)`; the TRUE
  sentence on t1 (`…live 3 to 5 years…`) forms singleton `c1=1(pg2)` and
  **loses**. `WINNER|count=2|pids=q1,q2` → the false claim INSTALLS.
  Majority-of-identical-strings outvotes the truth.
- **K:** trace-identical to A (10/10 INSTALL). **K-para:** trace-identical to
  B (0/2, all singleton clusters).

## (c) The "critical-thinking chain," as implemented — and reachability

From code, the chain is **six deterministic mechanisms, no deliberation**:

1. `calib_g1..g7` — teach-time lesson probes (install/reject modules). One-shot.
2. `kw_query` (G1) — keyword extraction with the taught stoplist.
3. `select_core` (G2) — first-3 + title dedup.
4. `best_for_page` (G3) — per-page argmax of query-token overlap. The only
   "reading" primitive; it is scoring, not understanding.
5. `cluster_best` (G4) — byte-equality clustering + largest-cluster-wins +
   `MIN-SOURCES=2`. **This is the entire "judgment."**
6. Injection substring scan (G6) + exclusion; provenance listing (G5).

There is **no** deliberation loop, **no** judgment gate beyond fixed
thresholds, **no** refusal loop (single-shot verdict), **no** revision step,
**no** retrieval of previously installed knowledge. (`mh_entity`/MULTIHOP
exists but the LI driver always passes `kind=FACT`, so it never runs.)

**Reachability verdict:**
- Every fact with ≥2 parsed pages **reaches** the chain (`blind=0`).
- **Paraphrased content IS seen by the chain** — `TRACE|CAND` proves both
  paraphrases are extracted and overlap-scored per page. But meaning is never
  compared: the only cross-page comparison primitive in the codebase is byte
  equality of normalized sentences. Paraphrases therefore die at cluster
  formation, *before any judgment could weigh them* — and no judgment
  mechanism for "same claim, different words" exists to be reached.
- A9 shows the mirror image: the chain is reached, the byte-identity test
  passes, and the falsehood installs — the truth on t1 is seen (CAND|2) and
  then outvoted.

## (d) Known-vs-novel split

| | byte-identical pages | paraphrased pages |
|---|---|---|
| novel (A/B) | 20/20 INSTALL | 0/24 INSTALL |
| already-known (K/K-para) | 10/10 INSTALL | 0/2 INSTALL |

**Split = 0, by construction.** `installed.txt` holds only the 9 directives;
`webg.zag` contains no claim store, no known-fact lookup, and never reads
`knowledge_ledger.txt`. The instrument cannot tell known from novel — every
run is claim-stateless. So Micah's question is answered directly: **it is not
the case that "it already knew everything"** — the machine has no "already
knew" at all. A known fact arriving with byte-identical coverage installs
exactly like a novel one; with paraphrased coverage it withholds exactly
like a novel one.

## (e) Where does it break — plain language

It breaks in **one function, `cluster_best`, at the byte-equality test** —
and that test is not a bug, it is the taught rule. G4's own calibration
teaches: *"When two pages agree word for word, that is corroboration."*
The machine learned exactly that, and executes it deterministically:
two pages saying the same thing **word for word** corroborate; two pages
saying the same thing **in different words** are, to this machine,
two unrelated singletons that can never reach the bar of 2.

So on Micah's "wasn't taught principles" hypothesis: the principles **were**
taught — G1–G6 all install, calibration-verified, G7 correctly rejected —
and the machine applies them faithfully on every case. Nothing is dropped by
broken machinery, and nothing is missing from the teaching that the machine
fails to use. The failure is that the principle itself *is* the byte-identity
rule: there is no principle anywhere in the guides, directives, or code for
"same claim in different words," and no mechanism that could implement one.
The throughput gap (0/24 Type-B) and the integrity hole (A9 installs) are the
same rule viewed from opposite sides: byte-identity is both too strict for
honest paraphrase and too weak for colluding copies. Loosening it admits
P1–P4 (proven by V-PARA's INTEGRITY-FAIL); keeping it withholds all realistic
paraphrase (proven here, 24/24 singleton clusters).

**One-line verdict:** every fact reaches the pipeline; paraphrased facts die
at `cluster_best`'s byte-equality clustering — seen, scored, never matched —
because corroboration *is* word-for-word identity in the frozen G4 rule, and
no other comparison primitive exists in the instrument. The "critical-thinking
chain" is six deterministic mechanisms with no deliberation, no memory of
installed facts, and no retrieval path; it is never bypassed, it is simply
exhausted at the clustering step.

---

## Evidence (in this directory)

- `dispositions.tsv` — per-case, per-stage dispositions (pass 1; pass 2 byte-identical)
- `wb_driver.py` — deterministic white-box driver (pure Python glue; all reasoning in Zag)
- `webg_trace.zag` — frozen instrument + additive `tverdict` TRACE (standard commands byte-identical to frozen binary; build with the pinned znc)
- `fixtures_known/` — the 12 already-known-fact cases (k-01..k-12)
- `wb_pass1/work/`, `wb_pass2/work/` — per-case `query.out`, `select.out`, `tverdict.out` traces
- `RUNLOG.md` — progressive run log
