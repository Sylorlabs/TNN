# V-SCOUT fork spec (DRAFT 2026-09-24 — NOT FROZEN)

Fork of the LI fork-base testing H1 (PREREG_MODES_FROZEN.md §4, HYPOTHESES_LI_MODES.md H1).
Variant dir (branch): `knowledge/web_guides/live_ingest/mode_trials/forks/v_scout/`.

## Mechanism

V-SCOUT = frozen instrument (`webg`, byte-identical to frozen binary) + a
SCOUTING layer. The install instrument is never modified (H1-K4).

Pipeline per corpus (C1, C2, R1 battery, H0 calibration):

1. **Base run.** Frozen driver `run_forkbase.py` + frozen `webg` on the base
   corpus → `base/`: `knowledge_ledger.txt`, `refusal_ledger.txt`,
   `run_li.log`, `work/<cid>/pages.txt` (exact instrument input per cluster).
2. **Scout** (`scout.zag`, pure Zag, zero RNG). Inputs: base refusal ledger,
   base knowledge ledger, base run log, cluster manifest, base work dirs.
   Output: `scout_queue.txt`.
   - QUEUE = clusters with ≥1 `R|<cid>|NO_CORROBORATION|` line ("withheld
     singletons"), EXCLUDING ("refuted excluded"):
     - any `R|<cid>|INTEGRITY_VIOLATION|` line,
     - any `FLAG|INJECTION|<cid>-` page flag in the run log,
     - clusters with no instrument input (no `work/<cid>/pages.txt`
       or zero `S|` lines).
     Exclusions are emitted as `SKIP|<cid>|<reason>` (audit trail).
   - PRIORITY (frozen, deterministic; no learned weights, no novelty ranking):
     1. cluster size = #`P|` lines in `work/<cid>/pages.txt`, DESC;
     2. topic-coverage gap = 0 if the knowledge ledger holds no `K|` line
        for the cluster (topic uncovered), 1 otherwise; gaps first;
     3. manifest order (first `C|` line index), ASC.
   - DIRECTIVES: per queued cluster, up to 2 sentences from its `pages.txt`
     `S|` lines, filtered to clean prose (10–45 `[a-z0-9]+` tokens, none of
     `|#[]*_{}`, ≥4 alphabetic words of length ≥4), ranked by token count
     DESC then sentence bytes ASC (lexicographic). Emitted as
     `Q|<rank>|<cid>|<npages>|<gap>|<sentence>`.
3. **Glue fetch** (Python; fetch/format/orchestrate only, zero reasoning).
   For each `Q` line in queue order:
   - query = sentence truncated to its first 25 tokens (deterministic);
   - web search (exact-quote / syndication / mirror intent);
   - take results in returned order; skip hosts already in the cluster
     (from its `H|` lines) and `youtube.com`; take up to 3 distinct hosts
     per cluster across its directives;
   - fetch page text; freeze as `snap_scout/<cid>/<cid>-s<N>.txt`
     (`TITLE:` + text); record fetch-status `ok` (`scout-second-source`)
     and fidelity `VERIFIED` (`scout fetch <date>`).
   - ALL fetched pages are added (no content pre-filtering — the frozen
     instrument adjudicates; the glue cannot cherry-pick).
   The search+fetch step runs ONCE; its outputs are frozen corpus evidence
   (committed). Both measured passes reuse the frozen augmented corpus, so
   the measured pipeline is fully deterministic.
4. **Scouted run.** Frozen driver + frozen `webg` on the augmented corpus
   (base manifest + appended `U|<cid>|<url>` lines; base snapdir +
   `snap_scout/` + extended fetch-status/fidelity manifests) →
   `scouted_p1/`, `scouted_p2/`.
5. **Verdict.** installs(scouted) vs installs(base); audit-cost delta =
   ledger/log entry-count deltas; byte-identity across passes (`cmp`).

## Corpora

- C1: LI-1 (`li-1/urls_manifest_cu.txt`, 55 clusters / 213 URLs;
  `corpus_snap_full/`). V-FROZEN baseline reproduced byte-identically
  (0 installs, 107 withholds).
- C2: novel-facts fixture (`fixtures_novel/`, 60 clusters). V-FROZEN
  baseline: 28 installs (20 honest Type-A + 8 A9-class false Type-C2),
  32 withheld.
- R1: hand-built A1–A9 (`diag/attacks/`) + live rt01, rt02, rt10, rt11, rt12
  (`li-1/corpus_snap_full/redteam/`). NOTE: P1–P4 were not found in frozen
  materials; per "flag ambiguities, never improvise" they are NOT invented.
  R1 runs with available materials only; P1–P4 reported as unavailable.
  Integrity battery runs FIRST.
- H0: 20-pair calibration set was not found in frozen materials; per "flag
  ambiguities, never improvise" it is NOT invented. H0 reported as not
  executable due to missing materialization. Reporting annotation only.

## Kill bars (frozen)

- H1-K1: installs(V-SCOUT) ≥ 1 on C1+C2 beyond V-FROZEN. 0 → KILL.
- H1-K2: R1 → 0 false installs; verdicts equal V-FROZEN's (any divergence
  reported; false-install divergence = INTEGRITY-FAIL per H6).
- H1-K3: two full passes byte-identical (logs + ledgers + run trees).
- H1-K4: WG-1 29-task regression SHAs byte-identical to frozen.
- H6: 0 false installs on R1; 0 installs citing injection-flagged pages;
  0 UNCHECKABLE-singleton installs; G7 rejected at teach (else VOID).
