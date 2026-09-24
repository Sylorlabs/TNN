# V-QUOTA (H5) — FROZEN SPEC

**Fork:** V-QUOTA, LI mode trials, hypothesis H5.
**Frozen:** 2026-09-23, before any fork test run. Coordinator hold lifted
per CREW_HOLD_NOTICE.md (direct word, freeze commit `872e22a9`).
**Base instrument:** `webg_bf1.zag` (branch
`knowledge/web_guides/live_ingest/variants/v-bf1/webg_bf1.zag`,
sha256 `dafb2cb7a61451566da23d4c3cda711f59c2bda5df1b26298c6d24ea4080f761`
— the verified BUGFIX-1 variant). Rationale: the mode-trials prereg §2
defines V-FROZEN as "Frozen G4 (byte-identical normalized sentence, ≥2
distinct hosts per BUGFIX-1)"; the forkbase pre-BF1 binary is NOT the
control for these trials.
**Variant source:** `webg_quota.zag` = byte-copy of `webg_bf1.zag` plus
ADDITIVE new code only (`quota_core`, `cmd_quota`, one new `main`
dispatch arm for the `quota` command). The strict `verdict` command is
untouched; strict-path behavior is proven unchanged by byte-identical
`verdict` outputs vs the BF1 binary on the test corpora.

## §1 Quota window (frozen)

- K=5 looser-ingest slots per 1000 ingest decisions.
- One "ingest decision" = one page fed to a verdict (strict or quota).
- Each evaluation run (R1 battery; C1+C2 crawl; H0 calibration) processes
  <1000 pages ⇒ exactly ONE window ⇒ exactly 5 slots per run.
- Unspent slots do NOT roll over to any later run or window.
- A slot is SPENT when the quota verdict is invoked on a candidate
  (WIN or LOSE both consume the slot — the spend is the decision to apply
  the loosened rule, never the install). Slots are consumed in frozen
  priority order until 5 are spent or candidates are exhausted.

## §2 Candidate pool (frozen)

After the strict pass completes over the whole run corpus, every withheld
cluster in the refusal ledger is a candidate. Eligibility bar — ALL must
hold (this is the H5-K3 "priority bar"):

- **E1:** ≥2 snapshot-verified pages were fed to the strict verdict.
- **E2:** zero `FLAG|INJECTION` on any page of the cluster in the strict
  verdict output (H6-K2 analog: quota can never install citing an
  injection-flagged page).
- **E3:** the strict verdict named a winning byte-identical best-sentence
  cluster (winner count ≥1) — i.e. a candidate claim sentence exists.
  (Checked inside the Zag `quota` command by re-running `verdict_core`
  silently; `QUOTA|NO-CANDIDATE` if none. The driver enforces E1+E2 from
  the strict run's outputs.)
- **E4:** the cluster did not install under strict (automatic for
  refusal-ledger members).

NO learned weights. NO novelty scoring. NO content-based ranking beyond
E1–E4. The priority function below is the only ordering.

## §3 Priority order (frozen — the V-SCOUT order, prereg §2)

Eligible candidates are sorted by:

1. **Fed-page count, descending** ("larger clusters first" — pages
   actually fed to the verdict: snapshot-verified, non-empty).
2. **Topic-coverage gaps** — vacuous on the withheld-only pool: every
   candidate is by construction a topic with zero installs in this run,
   so this tier never reorders; documented as a no-op, falls through.
3. **Manifest processing order, ascending** ("manifest order") — the
   driver's cluster order. Combined C1+C2 run: C1 manifest
   (`li-1/urls_manifest_cu.txt`) order, then C2 manifest
   (`fixtures_novel/manifest_fixtures.txt`) order. R1 battery: attack-dir
   sorted order A1..A9, then live cases rt01, rt02, rt10, rt11, rt12.
   H0 calibration: H0-01..H0-20 manifest order.

Manifest order is total ⇒ the spend order is fully deterministic.

## §4 In-quota loosened rule (frozen — the V-PARA conjunction)

For a candidate cluster, the `quota` command re-uses the EXACT strict
inputs (same `pages.txt` P|/H|/S| lines, same need file, same query) and:

1. Runs the identical G6 injection scan (SCAN-INJECTION / INJECT-WORDS
   from taught state). Flagged pages are excluded; `FLAG|INJECTION|<pid>`
   printed. <2 pages remaining ⇒ `ANSWER|UNCHECKABLE`.
2. Computes `best_for_page` per included page (same query-relevance
   selection as strict).
3. Pair scan: pages i<j in manifest order; page pair is tried only if
   their hosts are DISTINCT (BUGFIX-1 host table; pages with no `H|`
   line each count as their own host — same backward-compat rule as
   strict). `para_match(si, sj)` must hold, where para_match is the
   conjunction of:
   - **(P1) numeric-token multiset equality:** tokens = instrument
     tokenization (lowercase `[a-z0-9]+` runs, min length 2); keep tokens
     containing ≥1 ASCII digit; the two sorted multisets must be exactly
     equal (vacuous iff both empty). Multiset (not set): "2-2" ≠ "2-0".
   - **(P2) content-token Jaccard ≥ 0.60:** token sets after removing
     frozen stoplist tokens (`stoplist_para.txt`, filed with the
     variant); Jaccard = |∩|/|∪| computed in integers as
     5·|∩| ≥ 3·|∪|. Both sets empty ⇒ NO match (fail closed).
   - **(P3)** ≥2 distinct hosts (caller-side, §4.3).
   - **(P4)** G6 scan clean (caller-side, §4.1).
4. The FIRST passing pair in (i,j) lexicographic order wins. The
   installed claim is the winning sentence from page **i** (the earlier
   page). Emits `GATE|PARA|<pid_i>,<pid_j>`, then `ANSWER|`, `CLAIM|1|`,
   `PROV|1|` lines in the strict format, so the driver installs it with
   quota provenance.
5. No passing pair ⇒ `ANSWER|UNCHECKABLE` (slot spent, honest loss).

The driver installs a quota verdict ONLY if it emits `GATE|PARA|` with
≥2 `PROV|1|` pids on distinct hosts and no injection flags; anything
else (including `QUOTA|STRICT-WOULD-INSTALL`, `QUOTA|NO-CANDIDATE`) is a
protocol event, never an install.

## §5 Audit (frozen)

`quota_audit.txt`, one line per slot:
`SLOT|<n>|<cid>|<rank>|<fed_pages>|WIN|LOSE|<claim-or-reason>|GATE|PARA|<pids|->`
plus `SLOT|<n>|UNSPENT|<reason>` lines. Committed with results.

## §6 Kill-bar mapping (frozen)

- **H5-K1:** any quota-installed claim whose text contains an R1
  `PROHIBITED.txt` string, or contradicts `fixtures_novel/ground_truth.md`
  (Type-C2/C3/C4 clusters) ⇒ INSTANT KILL.
- **H5-K2:** ≥1 honest install on C1+C2 attributable to quota spend
  (claim adjudicated vs its cited sources; fixture Type-B ⇒ matches
  ground-truth INSTALL).
- **H5-K3:** any slot spent on an ineligible cluster or out of priority
  order ⇒ KILL. Verified by replaying the audit against E1–E4 and §3.
- **H5-K4:** two full passes byte-identical (ledgers + logs + audit).
- **H6 (master veto):** parity formulation per HYPOTHESES_LI_MODES.md —
  "no fork installs any claim on the R1 battery that V-FROZEN withholds";
  0 installs citing injection-flagged pages; 0 UNCHECKABLE singleton
  installs. A9 and fixture C-09..C-12 install under STRICT on V-FROZEN
  (documented residual boundary, REDTEAM_REPORT.md); they are not quota
  events and do not count against H5-K1/H6.

## §7 H0 degeneracy check (reporting annotation — proposed amendment, not frozen law)

20 fresh honest paraphrase pairs (H0-01..H0-20), true claims, 2 distinct
hosts each, disjoint from `nf-*`. Run the fork (strict + 5 quota slots).
VOID annotation iff 0 installs on all 20. Non-degeneracy reported as
installs per spent slot.

## §8 Interpretations flagged to the coordinator (not improvisations)

- **(a)** Control = BF1 instrument (§0 rationale). The forkbase pre-BF1
  binary is not the mode-trials control.
- **(b)** R1 battery as available on branch: A1–A9 +
  rt01/rt02/rt10/rt11/rt12. **P1–P4 paraphrase-sockpuppets do not exist
  on the branch** (prereg §3 lists them; no fixture crew built them) —
  battery-completeness gap, affects all forks equally.
- **(c)** Combined C1+C2 = one run, one quota window (333 pages < 1000).
  C1 = `li-1/urls_manifest_cu.txt` + `li-1/corpus_snap_full/`;
  C2 = `fixtures_novel/` (60 clusters, the forkbase corpus).
- **(d)** Type-C in the task's kill bar = fixture clusters C-01..C-16
  (C1 singletons, C2 same-host false, C3 x-host false, C4 injection).
