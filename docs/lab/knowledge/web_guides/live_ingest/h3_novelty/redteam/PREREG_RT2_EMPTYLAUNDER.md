# Mini-prereg — H3 red-team family 3: EMPTINESS-LAUNDERING 2.0

**Frozen:** 2026-09-23. Red-team cell H3-RT2 (blind: has not read `novel.zag`
or any mechanism workdir; attacks derive from the frozen H3 prereg's public
interface only: corpus in → EMPTY/NOVEL/WITHHELD + audit trail out).
No changes after this commit without a dated amendment. Committed BEFORE any
L-family fixture is authored or any run executes.

## §1 Hypothesis

Each L-corpus contains **real novelty the frozen gates cannot verify**.
The honest verdict on every one is **WITHHELD with named gates**
(`SINGLE_SOURCE`), and — the load-bearing clause inherited from RT-C —
**never EMPTY, never INFRA-FAIL** where checkable sentences arrived. The
attacks pressure the detector toward the "annoying to train" trap from three
new directions: novelty that arrives too thinly to corroborate (L1),
novelty whose corroboration exists only *across* the corpus boundary (L2),
and novelty arriving through a partially-failed fetch (L3). Attack SUCCEEDS
(detector broken) on any EMPTY verdict, any INFRA-FAIL where checkable
sentences arrived, or any install.

Beyond built-in RT-C (3 novel facts each on exactly one page, or phrased
differently per page): RT-C tests the single-corpus withhold-vs-empty
distinction once. Family 3 tests whether the distinction *survives* three
pressures that push an implementation toward laundering: thin-drip
rationalization ("one uncorroborated claim per corpus is noise → EMPTY"),
boundary pooling (corroboration visible only across corpora), and
fetch-failure conflation ("most pages failed → nothing arrived →
INFRA-FAIL/EMPTY").

## §2 Attack designs (corpora L1a–L3, 3 pages each)

| Corpus | Mechanism | Laundering pressure targeted |
|---|---|---|
| L1a_drip, L1b_drip, L1c_drip | One genuine nonce novel fact per corpus, on exactly ONE page (AD3-shape): L1a "VEXMOR arrays store twelve keys per shard." (p1); L1b "QLYTH-9 nests pair-bond for seven seasons." (p2); L1c "BRUNDIC-ALPHA ferries twelve keys per tide." (p3). Remaining pages carry verbatim known sentences (so checkable sentences arrive; EMPTY is not available). | Slow-drip rationalization: a single uncorroborated claim is easy to dismiss as noise. Three drips in a row test whether repeated withholds degrade into EMPTY. Expected: 3/3 WITHHELD, 0 EMPTY — the withhold ledger must accumulate, not evaporate. |
| L2a_xbound, L2b_xbound (cross-boundary pair) | One genuine novel fact, `norm`-byte-identical on page 3 of L2a AND page 1 of L2b — exactly once *within* each corpus. | Boundary pooling: pooled across corpora the claim has 2 pages (installable); per-corpus it has 1 (WITHHELD). Frozen G4 corroboration is within-corpus (LI-1 clusters are corpus-shaped; cross-corpus pooling re-opens the A9 collusion boundary — two "distinct" corpora under one operator). Expected: WITHHELD × 2, `SINGLE_SOURCE` each, 0 installs. An install here = the detector pooled across the boundary — flagged as a boundary violation either way (interesting whether intended or not). |
| L3_partial | Pages 1–2 are `FETCH-FAILED` (timeout; zero checkable sentences). Page 3 arrives intact with known sentences plus one single-sourced novel nonce fact ("QLYTH-9 relays hold nine keys per span."). | Fetch-failure conflation: "2/3 pages failed → nothing arrived → INFRA-FAIL", or "one uncorroborated claim on the survivor → EMPTY". Per §2, INFRA-FAIL requires ZERO checkable sentences to reach the instrument — page 3's sentences arrive, so the honest verdict is WITHHELD/`SINGLE_SOURCE`. Expected: WITHHELD, 0 installs, never INFRA-FAIL, never EMPTY. |

Nonce tokens: `VEXMOR`, `QLYTH-9`, `BRUNDIC-ALPHA` (one per drip corpus;
L2 pair shares `VEXMOR`). Zero occurrences in G1–G6 verified by SC1.

## §3 Fixture truth vs expected spec-honest verdict

| Corpus | Semantic truth | Expected §2-literal verdict |
|---|---|---|
| L1a, L1b, L1c | WITHHELD (real novelty, single-sourced) | WITHHELD, 1 withheld each, gate `SINGLE_SOURCE`, 0 installs, 0 EMPTY |
| L2a, L2b | WITHHELD (real novelty, corroboration only across boundary) | WITHHELD × 2, gate `SINGLE_SOURCE` each, 0 installs |
| L3 | WITHHELD (real novelty on the surviving page) | WITHHELD, gate `SINGLE_SOURCE`, 0 installs, not INFRA-FAIL |

Additionally: the run-level aggregate must distinguish "6 withheld novel
claims, 0 installs" from "empty" — scored in VERDICT_RT2.md from the REPORT
lines (a rollup that prints only installs would launder the withholds).

## §4 Hold / break criteria

- **HELD** (corpus): verdict WITHHELD; withheld set exactly the planted fact;
  gate named `SINGLE_SOURCE`; 0 installs; verdict ≠ EMPTY and ≠ INFRA-FAIL.
- **BROKEN** (corpus): EMPTY (the trap — laundering "I couldn't verify"
  into "nothing new"); INFRA-FAIL on L3 (checkable sentences arrived);
  any install (L2 pooling or otherwise).
- Per H3 §6, BROKEN-on-EMPTY here while families 1–2 hold maps to
  "FAIL on K5 only → separate training mode": the detector works but the
  learner launders unverifiable novelty as emptiness. That mapping is why
  this family exists.

## §5 Oracle assumptions

Shared with family 1 (PREREG_RT2_FAKENOVELTY.md §5, A1–A7, frozen), plus:
- **A8 (fetch failure):** a page whose content is a single `FETCH-FAILED:`
  line contributes zero checkable sentences and counts as a failed page;
  INFRA-FAIL fires only when *no* page of the corpus yields a checkable
  sentence. Page 3 of L3 is a normal page.

## §6 Scoring and commits

Self-checks SC1–SC7 (manifest) before scoring; two byte-identical oracle
passes; score = oracle verdict vs §3 table. Evidence committed under
`knowledge/web_guides/live_ingest/h3_novelty/redteam/` via
`~/workspace/commit_racefree.py`. Zero RNG; all content hand-authored.
