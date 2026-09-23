# T2-TRACKR0 — VERDICT: **REPRODUCED**

**Family:** Track R0 closeout (representation), Type C (committed-evidence re-derivation).
**Crew:** T2-TRACKR0 — REPLACEMENT. Predecessor killed mid-run by runtime daemon restart (~2026-09-22 21:36 PDT); resumed from its partial state (see RUNLOG.md).
**Date:** 2026-09-22/23 PDT. **Deliverables:** this file + `RUNLOG.md` in `~/workspace/scratch-crossref/T2/TRACKR0/crew/`.

## 1. Frozen prereg — authoritative section, quoted verbatim

Source: `sylorlabs/TNN` branch `tnn-native-lab`, commit `7b2100d09911c5c10252c5756c7def288e70bd1f`,
`docs/lab/crossref/PREREG_TIER2.md`, section `T2-TRACKR0`. Fetched from the GitHub API at the
frozen commit and verified **byte-identical** (sha256 `90070c88e43aecb6ba3ee8df6d487f7bf1b1673bb12d3ad8dcd11d597ade4a9f`)
to the copy used for this replication.

> ## T2-TRACKR0 — Track R0 closeout (Type C)
>
> **Claims:** commits `0489675d58e4` + `18284131b3aa`: B-T1 verdict FAIL — literal ordering holds but `raw_micro` ranks 7/10 rather than dead last (independently-checked closeout reversed the earlier B-T1 PASS; original worker's scores were unreproducible and discarded); frozen-manifest rerun method; real heap-buffer overflow in `grounded_adaptive_mdl` above 8,192 candidates exposed. Grounded-adaptive-MDL arm repaired to honest FAIL (`53d5612c5ed0`): root cause index overflow (stored indices over all C candidates, allocated only G=min(C,8192)); repaired scores 0.8319 mean (0.8317 pg100, 0.8322 sqlite3.c), rank 7/11 — still FAIL (raw_micro not last; fixed_window 8/16/64 below it); all non-grounded arms kept golden hashes, reruns byte-identical. B-T5 split-to-merge FAIL. Overnight note: B-T1 FAIL stands but looks artifact-driven (XOR-collision relocations, perturbed-leg boundary at L=7) — probe amendment still unsigned.
> **Method:** Type C — re-derive the B-T1 FAIL from the frozen-manifest rerun evidence; verify the overflow root-cause description against the repaired code; verify golden hashes of non-grounded arms.
> **Rule:** REPRODUCED if B-T1 FAIL and the repair's 0.8319/rank-7/11 re-derive; the artifact-driven suspicion is recorded as an open amendment case, not a replication failure.

**Extracted claims checklist:**
1. Closeout commits `0489675d58e4`+`18284131b3aa`: B-T1 FAIL — literal ordering `predictive_surprise > fixed_window_4 > raw_micro` holds, but `raw_micro` ranks **7/10**, not dead last.
2. The independently-checked closeout reversed the earlier B-T1 PASS; the original worker's scores were unreproducible and discarded.
3. Frozen-manifest rerun method.
4. Real heap-buffer overflow in `grounded_adaptive_mdl` above 8,192 candidates, exposed by the closeout.
5. Repair commit `53d5612c5ed0` (honest FAIL): root cause = index overflow — stored indices spanned all C candidates while histograms allocated only G=min(C,8192).
6. Repaired scores: **0.8319 mean** (0.8317 pg100, 0.8322 sqlite3.c), **rank 7/11** — still FAIL (raw_micro not last; fixed_window 8/16/64 below it).
7. All non-grounded arms kept golden hashes; reruns byte-identical.
8. B-T5 split-to-merge FAIL.
9. Overnight note: B-T1 FAIL stands but looks artifact-driven (XOR-collision relocations, perturbed-leg boundary at L=7); probe amendment still unsigned.

**Decision rule (governing):** REPRODUCED iff B-T1 FAIL re-derives AND the repair's 0.8319/rank-7/11 re-derive.
The artifact-driven suspicion is an open amendment case, not a replication failure.

## 2. Frozen pins

| Pin | Full SHA | Status |
|---|---|---|
| Frozen prereg | `7b2100d09911c5c10252c5756c7def288e70bd1f` | resolves; PREREG_TIER2.md byte-identical to working copy |
| Closeout evidence (impl+evidence) | `0489675d58e436b6a432e241d0336d3a34ed43d7` | resolves — "B-T1 closeout: additive arms.zag R-7 leg + independent reproduction evidence" |
| Closeout evidence (pointer) | `18284131b3aaa3a4c2f1e0bd7264fa98c1b25ccd` | resolves — "B-T1 closeout: fill commit hash in VERDICT_SHEET.md and addendum" |
| Repair evidence | `53d5612c5ed077088b3ea0464cd620cc7f893c8d` | resolves — "grounded_adaptive_mdl heap-overflow repair + B-T1 retest (crew3)" |

⚠️ **Pin discrepancy — flagged for parent reconciliation.** The task listed expected pins `ce1e3b0b`, `bcd39f4b`.
Both were checked against `sylorlabs/TNN` as commit prefixes, git trees, and (by prefix impossibility) blobs:
**neither exists** (commits API: "No commit found for SHA"; trees API: 404), and neither appears in the frozen
prereg, the frozen SCOPE, the crossref working tree, or any inherited file. The prereg-named pins above all
resolve and were frozen instead, per the prereg's authority ("the prereg section governs") and SCOPE §2.2
("If a pin listed in the tier prereg doesn't hold the expected files, the crew stops" — here the prereg-listed
pins hold everything). The `ce1e3b0b`/`bcd39f4b` values look like a dispatcher transcription artifact; no
substitution was made — the governing document's own pins were used.

## 3. Claim-by-claim: committed claim vs re-derived measurement

Re-derivation engine: independent pure-Zag program `verify_trackr0.zag` (built from source with the pinned
`znc_linux_x86_64_abed8aa1 --no-zagd --no-analyze --no-foreground-cache`; zero RNG — source canary clean),
run **3× byte-identical** (sha256 `28a6cdd9f91d018959913f92a508affd19dbb9608e827f06dd11833846e91360`), **14/14 checks PASS**.
Integer-only arithmetic (1e15-scaled), composites recomputed as `0.55*grounded_hard + 0.25*retrieval_20way + 0.10*compression + 0.10*reconstruction`, tournament = mean of prose/code.

| # | Claim | Re-derived | Disposition |
|---|---|---|---|
| 1 | B-T1 FAIL; ordering holds; raw_micro 7/10, not dead last | ordering `ps(0.919045) > fw4(0.895896) > rm(0.770427)` holds; raw_micro overall **rank 7/10**, binding **6/9**; `dead_last_ok=false`, `binding_verdict=FAIL`, `order_ok=true` — all match the committed `rank_table.json` fields | ✓ REPRODUCED |
| 2 | Closeout reversed earlier PASS; original scores unreproducible, discarded | Evidence-internal: addendum documents claimed 0.6843 vs measured 0.9558 (predictive_surprise/pg100); grounded scores (0.5850/0.5799) unreproducible — arm crashed; closeout RUN_MANIFEST contains the failed sha256sum/stat lines for the missing grounded `.seg` files | ✓ consistent (record-level) |
| 3 | Frozen-manifest rerun method | `PROBE_MANIFEST.md` blob-verified at the closeout pin (git object `e9291f3cd637`); addendum §1 asserts frozen-before-execution and verbatim implementation | ✓ verified at pin |
| 4 | Real heap-buffer overflow above 8,192 candidates | Verified against pre-repair `arms.zag` at closeout pin: `G=min(C,8192)`; `mx[slot]` stores candidate **index** `cix[g2]` (0..C−1); `gtot`/`gnx` allocated G / G·256; `gtot[ge]`/`gnx[ge*256+b]` written with `ge` up to C−1 → OOB when C>8192 | ✓ REPRODUCED |
| 5 | Repair root cause = index overflow (indices over C, alloc G=min(C,8192)) | Verified against repaired `arms.zag` at repair pin: histograms indexed by candidate **rank** `rk` (0..G−1) drawn from a 16384-slot small table holding exactly the G candidates; scoring loop splits rank (→gtot/gnx) from candidate index (→cs/cc/cl); repair-2 small-table re-scan replaces the 1M-entry span-table probe. (Nuance: the `ge<G` invariant is enforced structurally — the small table can only yield ranks 0..G−1 — rather than by a comparison guard.) | ✓ REPRODUCED |
| 6 | Repaired 0.8319 mean (0.8317 pg100, 0.8322 sqlite3.c), rank 7/11, still FAIL | Recomputed from the committed score JSONs: prose 0.83168828571046 → **0.8317** (round), code 0.83221578366873 → **0.8322**, mean 0.831952034689595 → **0.8319** (trunc; round-half-up would read 0.8320 — see erratum E3); all within 1e-6 of stored values; grounded_adaptive_mdl **rank 7/11**; repaired binding verdict **FAIL** (ordering holds, raw_micro not last) | ✓ REPRODUCED |
| 7 | Non-grounded arms kept golden hashes, reruns byte-identical | Zag `u8eq` over all 20 arm×corpus sha256 pairs: closeout RUN_MANIFEST vs repair RUN_MANIFEST_REPAIRED → **20/20 MATCH**; both manifests record r1==r2 per pair | ✓ REPRODUCED (Type C: hash-table agreement re-derived; battery re-execution out of scope) |
| 8 | B-T5 split-to-merge FAIL | No B-T5 evidence was supplied to this crew (inherited set: b_t1/closeout/repair only); the prereg's Method and Rule do not cover B-T5 | recorded; out of rule scope; does not affect the verdict |
| 9 | Overnight note: FAIL stands but looks artifact-driven; probe amendment unsigned | Per the decision rule this is an **open amendment case, not a replication failure** | recorded as such |

## 4. Errata found in the committed evidence (none affect the verdict)

- **E1 — REPAIR.md prose error:** "binding ranks: predictive_surprise=1, fixed_window_4=2, raw_micro=**8 of 10** binding" is wrong. The committed `rank_table_repaired.json` itself records `binding_ranks.raw_micro=7`, `n_binding=10`, and the independent re-derivation confirms **7/10 binding** (8 is raw_micro's *overall* rank of 11; the author conflated the two, as also suggested by the "(was 7/10 unrepaired)" aside, which mixes overall and binding ranks). Verdict unaffected — raw_micro is not dead last under either numbering.
- **E2 — fixed_window_64 rounding in closeout `rank_table.json`:** stored `tournament_score` 0.460363387978469 equals the mean of the *6-decimal-rounded* stored composites (score_prose stored as 0.198437 vs full-precision 0.1984375); full-precision recomputation gives 0.460363637978469 (Δ=2.5e-7). Rank (10/10) and verdict unaffected.
- **E3 — mixed 4-decimal convention:** the frozen "0.8319" is *truncation* of the exact recomputed mean 0.831952034689595 (round-half-up would give 0.8320), while "0.8317" is *rounding* of prose. The exact values re-derive; only the display convention is inconsistent.

## 5. Verdict

**REPRODUCED.** B-T1 FAIL re-derives from the frozen-manifest closeout evidence (ordering holds, raw_micro 7/10 overall / 6/9 binding, not dead last), and the repair's 0.8319 mean / rank 7/11 re-derive from the committed score evidence with the overflow root cause verified against the repaired source. The artifact-driven suspicion (claim 9) is recorded as an open amendment case per the frozen rule — the probe amendment remains unsigned.

**Caveats / limits of this replication:** Type C throughout — no battery re-execution (the .seg corpora-scale outputs are not committed; only hashes). The r1==r2 byte-identity claims rest on the manifests' records, verified for cross-manifest hash agreement (20/20). B-T5 (claim 8) had no evidence supplied and sits outside the decision rule. The `ce1e3b0b`/`bcd39f4b` expected pins do not exist in the repo (see §2) — parent should reconcile the dispatch record.
