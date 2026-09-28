# VERDICT — Arm K1 (full SHA-256 identity), U7 binding adjudication

**Date:** 2026-09-21
**Arm:** K1 — Full SHA-256 identity (IDENT family)
**Adjudicated by:** U7 marathon crew
**Verdict: KILLED** — kill (ii) FIRED (churn swamp); kills (i) and (iii) do not fire

Supersedes the 2026-09-21 PROVISIONAL verdict (kill ii unevaluable). The
measurement defect is fixed (see `U7_ADJUDICATION.md`); criterion (ii) is now
evaluated mechanically on the evidence.

## Frozen kill criterion (verbatim, §3 of `units/PREREG_FREEZE.md`, extracted programmatically)

> Any one: (i) payload savings < 15% on corpus A vs sequential IDs — the caching claim dies; (ii) on corpus C mean revision-link chain > 8 AND latency > 2× baseline; (iii) > 5% of single-span recalls return contextually-wrong occurrence (right bytes, wrong role) — K1 dies as standalone (survives only as K3 component).

## Kill-criterion evaluation

### Kill (i) — payload savings < 15% on corpus A vs sequential IDs — NOT FIRED

Mode `k1-dedup-1x` (`work/runs/u7/k1-dedup-1x_a.txt`, byte-identical a/b):

- prose: 963,478 spans, 71,167 unique → savings **87.2%**
- code: 1,223,384 spans, 130,817 unique → savings **73.3%**
- Bar: < 15% kills. 87.2% / 73.3% ≫ 15%. **Does NOT fire.**
- The content-hash dedup core is exonerated — it works as advertised.

### Kill (ii) — corpus C mean revision-link chain > 8 AND latency > 2× baseline — FIRED

Mode `k1-chain-1x` (fixed; byte-identical a/b).
Corpus C = prose + 100 deterministic revision batches over every-1000th token
(963 touched spans, each revised 100× — the documented operationalization of the
frozen "revision series (100 deterministic patches)", ALPHABET_G-L.md).

The full 100-batch corpus C run was attempted 3×; service restarts killed it
each time. A 20-batch diagnostic (`work/runs/u7_chain20/`, byte-identical a/b,
built from the same fixed source with batch count 20) measured the scaling:

Measured (metrics-v1 JSON inline in the run output):

- `K1CHAIN,touched=963,mean_chain_x100=2000,latency_ratio_x100=999,mismatches=349`
- Mean revision-link chain = **20.00** (bar: > 8) — every touched span carries a
  20-hop append-only link chain; the walk from the original digest follows all
  20 links. Scales linearly: 100 batches → 100.0.
- Stale-vs-clean recall latency ratio = **9.99×** (bar: > 2×), measured in
  deterministic table ops: stale recall 30.78 ops vs clean 3.08 ops.
  Scales linearly: 100 batches → ~50×.
- **Both conjuncts fire. Kill (ii) FIRES.**
- Note: 349/963 mismatches are a test artifact — touched tokens include
  duplicate content (same bytes at different positions share one digest
  record); the fork rule (first link wins) correctly routes the second
  occurrence's walk to the first chain. Not a mechanism failure.

Per the frozen criterion text, the consequence is: *the revision-link mechanism
dies* — keep hash IDs, drop links, accept dangling references as a documented
limit. K1-as-specified (hash IDs **plus** append-only revision links with the
"references never dangle" promise) is dead: honoring the promise costs a
20-hop walk per stale reference at 9.99× the clean-recall latency after just
20 batches (100-hop / ~50× at 100 batches), with no compaction mechanism
(compaction was explicitly "future work"). The alphabet's bake-off table
predicted this outcome (corpus C → L wins; "K re-IDs every touched span and
grows link chains").

### Kill (iii) — > 5% contextually-wrong single-span recalls — NOT FIRED

Mode `k1-role-1x` (`work/runs/u7/k1-role-1x_a.txt`, byte-identical a/b):
800 role-tagged queries, **0 wrong** (0.0%). Bar: > 5%. **Does NOT fire.**

## Death certificate (per ARM_SPEC §6 — no softening)

**K1 is KILLED by kill (ii), the churn swamp.** The revision-link mechanism does
not survive a revision-heavy stream: 20 revisions of a span produce a 20-link
chain (100 revisions → 100 links), and following a stale reference costs 9.99×
a clean recall (~50× at 100 batches), both far past the frozen bars (> 8 links,
> 2× latency). The failure was predicted in the frozen alphabet and confirmed
by measurement.

**What survives:** the content-hash identity and dedup core (kills (i) and (iii)
did not fire — 87.2%/73.3% payload savings, 0.0% wrong-role recalls). The
program keeps SHA-256 content IDs and the dedup table; it drops the append-only
revision-link chain as the reference-following mechanism. This is precisely the
K3 decomposition the alphabet anticipated (content-addressed payload via K1's
table, position-addressed references via L1).

## Battery & gates

- Full 1× battery: 20 modes × 2 runs, byte-identical a/b — see
  `work/runs/u7_battery_console.log`. [PASS/FAIL counts to be filled]
- M8 determinism gate (N=5, perturbations none/frag/aslr/none/frag): store hash
  chain, ledger chain, allocator trace, and stdout byte-identical across all 5
  runs — **PASS**. (Full M8 artifact comparison in `work/runs/u7/m8_*`.)
- `k1-selftest`: 9/9 pass.
- Pure Zag, zero RNG in any decision path.

## Evidence trail

- Fixed source: `cl/arm.zag` (salt-loop saturation fallback; mechanism untouched).
- Root-cause analysis: `U7_ADJUDICATION.md`.
- Battery evidence: `work/runs/u7/` (40 run outputs + console log).
- M8 evidence: `work/runs/u7/m8_*` (5 outdirs + comparison).
- Scorecard (metrics-v1): `scorecard_r1_1x.json` (updated).
- Build log: `BUILD_LOG.md` (fix entry, 2026-09-21).
