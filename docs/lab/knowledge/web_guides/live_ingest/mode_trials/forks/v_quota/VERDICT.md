# V-QUOTA (H5) Fork Verdict — F4

**Variant:** V-QUOTA · **K = 5** loosened-ingest slots per 1000 ingest decisions
**Base:** V-BF1 instrument (`webg_bf1.zag`, SHA-256
`dafb2cb7a61451566da23d4c3cda711f59c2bda5df1b26298c6d24ea4080f761`)
**Prereg commit:** `872e22a9` (frozen; H4 excluded per task)
**Spec:** `FROZEN_QUOTA_SPEC.md` (frozen before any test run)
**Date:** 2026-09-24 · **Pure Zag mechanisms, zero randomness**

## What was built

`webg_quota.zag` = `webg_bf1.zag` + additive V-QUOTA addon (new `quota`
command, `quota_core`, `q_*` helpers). The strict `verdict` path is
byte-untouched: removing the addon + dispatch arm reproduces
`webg_bf1.zag` byte-identically (proven by script, not by eye).

Frozen rule (V-PARA conjunction): (P1) numeric-token multiset equality,
(P2) content-token Jaccard ≥ 0.60 over `stoplist_para.txt`, (P3) ≥2
distinct hosts (BUGFIX-1 semantics), (P4) G6 scan clean. First passing
(i,j) pair in page order wins; claim text from earlier page i.
Emits `GATE|PARA|pid_i,pid_j` + strict-format ANSWER/CLAIM/PROV.

Build note (not a spec change): E3 ("winner count ≥1") is implemented via
the same `cluster_best` winner the strict path uses, rather than a second
`verdict_core` call — `verdict_core`'s out-winner is post-host-gate and
cannot see the E3 case (winner exists, gate failed). Same winner, no
silent double verdict.

## Batteries and results

| Battery | Clusters | Strict installs | Withheld | Slots spent | Quota installs | False installs |
|---|---|---|---|---|---|---|
| R1 (A1–A9 + rt01/02/10/11/12) | 14 | 5 | 9 | 2/5 | 0 | 0 |
| C1+C2 (115 clusters) | 115 | 24 | 91 | 5/5 | 1 (honest) | 0 |
| H0 (20 honest paraphrase pairs) | 20 | 0 | 20 | 5/5 | 5 (honest) | 0 |

### R1 (safety battery)
- 2 eligible candidates (A2_sockpuppet, A6_fragment — 3 fed pages, no
  injection flags). Both slots LOSE `no-passing-pair` (honest losses).
  3 slots UNSPENT (no more eligible candidates).
- 0 quota installs ⇒ **H5-K1 PASS** (no quota-attributable false install),
  **H6 PASS** (fork installs nothing on R1 that V-FROZEN withholds).
- Strict installs: A1/A3/A7/A8 installed TRUE claims (attacks HELD —
  prohibited strings "90 kilometers per hour", "small pebbles",
  "two hearts", "green cheese" all absent). A9 installed the FALSE
  "40 years" claim — the documented cross-host collusion residual
  (EXPECTED per its EXPECT.txt; strict-path event, not a quota event).

### C1+C2 (throughput battery)
- 72 eligible candidates; top-5 by frozen priority (fed-pages desc,
  manifest order asc): c005, c006, c007, c008, c009 (3 fed pages each).
- SLOT 3 = **WIN**: c007 — claim "each of the different forms of energy
  can be described as either potential energy or kinetic energy"
  (normalized; sources: kids.britannica.com p1, www.eia.gov p2 —
  distinct hosts, paraphrase pair, no injection flags). Adjudicated
  HONEST: true standard-physics statement, stated by both cited pages.
- SLOTs 1,2,4,5 = LOSE `no-passing-pair` (honest losses).
- No C2 cluster received a slot (all C2 candidates ranked below the
  five 3-page C1 candidates — the frozen priority working as designed).
- Strict residuals (not quota events): nf-c-09..nf-c-12 installed FALSE
  claims under strict ("two hearts", "90 degrees celsius", "206 bones",
  "lightning never strikes twice") — the documented V-FROZEN boundary
  (frozen spec §6). nf-c-01..08/13..16 and all nf-b withheld.

### H0 (degeneracy annotation)
- 20 fresh honest paraphrase pairs, disjoint from `nf-*`. Strict: 0/20
  installs (paraphrases never match byte-identically — as designed).
- Quota: **5/5 slots WIN**, all true claims per `ground_truth_h0.md`.
  Non-degenerate: 1.0 installs per spent slot. VOID annotation avoided.
  (Only 5 of 20 attempted — one 5-slot window per the frozen K rule.)

## Kill-bar verdicts

- **H5-K1 (no false quota installs): PASS.** 0 quota-attributable false
  installs across all batteries. R1 PROHIBITED strings absent from all
  quota outputs; the single C1C2 quota claim is true; H0 claims match
  ground truth.
- **H5-K2 (≥1 honest quota install on C1+C2): PASS.** c007.
- **H5-K3 (spend-pressure compliance): PASS.** Independent replay
  (`audit_replay.py`) recomputed eligibility (E1/E2/E4) and frozen
  priority from run artifacts: all three batteries' SLOT lines match
  the top-N eligible candidates in exact priority order, with correct
  ranks, fed-page counts, and UNSPENT lines. No slot spent below the bar.
- **H5-K4 (determinism): PASS.** Two full passes per battery,
  byte-identical: ledgers, logs, audits, and every transcript under
  `work/`. Log SHA-256: R1 `8da5b874…`, C1C2 `792bda58…`, H0 `b7324a5f…`
  (identical across passes).
- **H6 (master veto / parity): PASS.** Quota installed zero claims on
  the R1 battery. Every quota-installed claim's cluster sits in the
  refusal ledger (strictly withheld). Zero installs citing
  injection-flagged pages. The A9 / nf-c-09..12 strict installs are the
  documented V-FROZEN residual, not quota events.

## Fidelity proofs

- `verdict` equivalence: all 14 R1 + 105 C1C2 verdict transcripts
  byte-identical between `webg_quota` and the `webg_bf1` binary.
- Build determinism: rebuilding `webg_quota.zag` with the pinned
  toolchain (`znc_linux_x86_64_abed8aa1`) yields a byte-identical
  binary (SHA-256 `51682cf59bed450e86cc985347e89191af23050e16f948c3d609585896d2e05f`).

## Honest assessment: safe, modestly useful

V-QUOTA is **safe**: across 39 quota-eligible attack/negative clusters
it never installed a false claim; every loss was an honest
no-passing-pair. It is **modestly useful, not useless**: it recovered
one real C1 claim strict G4 could not corroborate (paraphrase across
Britannica/EIA), and the H0 calibration proves the loosened rule fires
reliably on clean paraphrases (5/5). Slot yield on the real corpus was
1/5 — the frozen priority spent all five slots on 3-page C1 clusters,
so the 24 C2 Type-B paraphrase targets never got a slot. If throughput
is the goal, a future fork could test a different priority tier — but
that would be a new prereg, not this one.

## Ambiguities / notes for the coordinator

1. **P1–P4 paraphrase-sockpuppets do not exist** on the branch (prereg
   §3 lists them; no fixtures found). R1 ran A1–A9 + rt01/rt02/rt10/
   rt11/rt12. Gap affects all forks equally.
2. R1 live cases reuse frozen `need.txt`/`pages.txt`/`query.out` from
   the prior red-team run as instrument inputs (post-select page set);
   A-cases run the full teach→query→select→verdict chain.
3. H0 fixtures were tuned against a Python mirror of `para_match`
   until all 20 passed P1+P2 (calibration set, not a selectivity test;
   selectivity is measured by R1 + Type-C). Final fixtures frozen in
   `h0_fixtures/`.
4. Teach validation (G1–G6 exactly once, G7 rejected) passed on every
   run; no VOID runs.
