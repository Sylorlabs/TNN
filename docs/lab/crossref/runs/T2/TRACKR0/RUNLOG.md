# T2-TRACKR0 — RUNLOG (replacement crew)

## 2026-09-22 ~21:40 PDT — session start, inheritance survey
- Task received: T2-TRACKR0 replacement; predecessor killed by daemon restart.
- `~/workspace/scratch-crossref/T2/TRACKR0/` contained `clean/` (PREREG_TIER2.md, SCOPE.md, base64 copies, `ev/{b_t1,closeout,repair}/` with 12 evidence files + 2 score JSONs) and empty `crew/`. No RUNLOG/VERDICT from predecessor; no git clone in `clean/` (predecessor used API fetches, not a clone).
- Integrity decision: verify every inherited file against its pinned GitHub blob (bytes + git object hash) before trusting it.

## 2026-09-22 ~21:45 — prereg extraction (first task)
- Located T2-TRACKR0 section at line 95 of PREREG_TIER2.md; extracted claims checklist + decision rule.
- Fetched `docs/lab/crossref/PREREG_TIER2.md` at frozen commit `7b2100d09911c5c10252c5756c7def288e70bd1f` via gh-api → **byte-identical** to inherited copy (sha256 `90070c88e43aecb6ba3ee8df6d487f7bf1b1673bb12d3ad8dcd11d597ade4a9f`). Frozen section quoted verbatim in VERDICT.md.

## 2026-09-22 ~21:50 — pin freeze
- Prereg-named pins resolved via GitHub API:
  - `0489675d58e436b6a432e241d0336d3a34ed43d7` (closeout impl+evidence)
  - `18284131b3aaa3a4c2f1e0bd7264fa98c1b25ccd` (closeout pointer)
  - `53d5612c5ed077088b3ea0464cd620cc7f893c8d` (repair + retest)
- Task's expected pins `ce1e3b0b`, `bcd39f4b`: checked as commit prefixes, git trees — **do not exist** in sylorlabs/TNN (422 "No commit found", 404 on trees); absent from frozen prereg/SCOPE/crossref tree/all inherited files. Proceeded with prereg-named pins per prereg authority; discrepancy flagged in VERDICT.md §2 for parent reconciliation. (Repo is ~1 GB; no full clone — API blob verification with git-object-hash recomputation used instead; equivalent integrity for the pinned files.)

## 2026-09-22 ~21:55 — inherited evidence integrity (`crew/verify_blobs.py`)
- 12/12 files byte-identical to pinned blobs AND git object hashes verified (sha1 of `blob <len>\0`+content). Inherited state pristine; resumed.

## 2026-09-22 ~22:05 — source fetch + root-cause verification
- Fetched `docs/lab/units/r0/impl/arms/arms.zag` at repair pin (36,754 B, blob `9f29d27698ae`) and at closeout pin (34,989 B, blob `0ef39963fc2c`) → `crew/arms_repaired.zag`, `crew/arms_closeout.zag`.
- Pre-repair grounded block matches GROUNDED_BUG.md exactly: `G=min(C,8192)`; `mx[slot]=cix[g2]` (candidate index 0..C−1); `gtot=zalloc64(G)`, `gnx=zalloc64(G*256)`; `gtot[ge]`/`gnx[ge*256+b]` → OOB when C>8192.
- Repaired block: rank-indexed histograms via 16384-slot small table, rank/index split in scoring loop, repair-2 small-table re-scan; both repairs documented in code comments. Root-cause description verified.

## 2026-09-22 ~22:20 — independent Zag verifier (`crew/gen_verifier.py` → `verify_trackr0.zag`)
- Python glue transcribes numbers from the blob-verified JSONs/manifests into Zag string literals; ALL reasoning in Zag: decimal parse (1e15-scaled i64), composite `0.55*gh+0.25*ret+0.10*comp+0.10*rec`, tournament means, pairwise ranks, binding verdicts, 20-pair sha256 `u8eq` comparison, 4-decimal display checks.
- znc dialect notes hit: bare `{ }` blocks rejected (rewrote with unique names); `&&` and scalar `==` fine; `_zag_print/_zag_println/_zag_i64_to_str` idioms from arms.zag.
- Built with pinned `znc_linux_x86_64_abed8aa1 --no-zagd --no-analyze --no-foreground-cache` (no .zagd/binary copies; rebuilt from source).

## 2026-09-22 ~22:30 — verification runs
- First iteration caught two real findings, both investigated before finalizing:
  1. `fixed_window_64` recomputed-vs-stored Δ=2.5e-7 → traced to the JSON's 6-decimal-rounded `score_prose` (0.198437 vs 0.1984375); rank/verdict unaffected. Tolerance set to honest 1e-6 with deltas printed (erratum E2).
  2. Program computed repaired raw_micro binding rank **7/10**, but REPAIR.md prose claims "8 of 10" → checked `rank_table_repaired.json`: it records `binding_ranks.raw_micro=7`, `n_binding=10`. The .md prose conflated overall rank (8/11) with binding rank (7/10). Verdict unaffected (erratum E1).
- Also documented mixed 4-decimal convention: "0.8319" is truncation of exact 0.831952034689595; "0.8317" is rounding (erratum E3).
- Final: **3/3 runs byte-identical** (sha256 `28a6cdd9f91d018959913f92a508affd19dbb9608e827f06dd11833846e91360`), rc=0, **14/14 CHECKs PASS**, `ALL_CHECKS_PASS`. Source canary: no RNG/clock/entropy/syscall references (only "random_chunks" arm-name false positives).

## 2026-09-22 ~22:40 — deliverables
- Wrote `crew/VERDICT.md` (verdict **REPRODUCED**, full claim table, errata E1–E3, pin discrepancy, caveats) and this RUNLOG.
- No commits made (nothing to commit; verdict collection is the parent's step). No live workstreams touched. Scratch only; TMPDIR respected; no /tmp use.

## Notes / transient issues
- Runtime flaked 3× with "failed to store metadata for session ... timed out after 15s registering session metadata" on API exec calls; all succeeded on retry after 10–45 s waits. One early verifier run printed "aborted" with no output; the identical binary ran fine immediately after and 3× deterministically since — treated as a transient spawn flake, noted here.
- `clean/` was never a git clone (predecessor's API-fetch approach kept); integrity established per-blob instead.
